"""Preprocessing transformers and pipeline components.

Provides scikit-learn compatible transformers for feature dropping,
telemetry scaling, and within-regime conditional normalization.
"""

from __future__ import annotations

from typing import Any, Literal, Sequence
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import MinMaxScaler, RobustScaler, StandardScaler

from naval_propulsion.preprocessing.pipeline import BasePreprocessor


class ColumnFilterTransformer(BaseEstimator, TransformerMixin):
    """Transformer to drop specific columns (e.g., zero-variance, duplicates, or operating variables)."""

    def __init__(self, drop_columns: Sequence[str] | None = None) -> None:
        self.drop_columns = list(drop_columns) if drop_columns else []
        self.retained_columns_: list[str] = []

    def fit(self, X: pd.DataFrame, y: Any = None) -> ColumnFilterTransformer:
        if not isinstance(X, pd.DataFrame):
            raise TypeError("Input X must be a pandas DataFrame to track column names.")
        self.retained_columns_ = [c for c in X.columns if c not in self.drop_columns]
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        if not isinstance(X, pd.DataFrame):
            raise TypeError("Input X must be a pandas DataFrame.")
        cols_to_keep = [c for c in self.retained_columns_ if c in X.columns]
        return X[cols_to_keep].copy()


class TelemetryScaler(BaseEstimator, TransformerMixin):
    """Configurable scaler wrapping StandardScaler, RobustScaler, or MinMaxScaler.

    Preserves DataFrame column names and indices.
    """

    def __init__(
        self,
        scaler_type: Literal["standard", "robust", "minmax"] = "standard",
    ) -> None:
        self.scaler_type = scaler_type
        self.columns_: list[str] = []

        if scaler_type == "standard":
            self.scaler_ = StandardScaler()
        elif scaler_type == "robust":
            self.scaler_ = RobustScaler()
        elif scaler_type == "minmax":
            self.scaler_ = MinMaxScaler()
        else:
            raise ValueError(f"Unknown scaler_type: {scaler_type}. Choose 'standard', 'robust', or 'minmax'.")

    def fit(self, X: pd.DataFrame | np.ndarray, y: Any = None) -> TelemetryScaler:
        if isinstance(X, pd.DataFrame):
            self.columns_ = list(X.columns)
            X_arr = X.to_numpy()
        else:
            self.columns_ = [f"feat_{i}" for i in range(X.shape[1])]
            X_arr = X

        self.scaler_.fit(X_arr)
        return self

    def transform(self, X: pd.DataFrame | np.ndarray) -> pd.DataFrame:
        if isinstance(X, pd.DataFrame):
            index = X.index
            cols = list(X.columns)
            X_arr = X.to_numpy()
        else:
            index = None
            cols = self.columns_
            X_arr = X

        transformed_arr = self.scaler_.transform(X_arr)
        return pd.DataFrame(transformed_arr, index=index, columns=cols)


class OperatingRegimeNormalizer(BaseEstimator, TransformerMixin):
    """Conditionally normalizes telemetry features within each discrete operating regime.

    For each unique operating regime setting (e.g. ship speed `v`), computes
    within-regime mean and standard deviation:
        z_{ij} = (x_{ij} - mu_j(v_i)) / sigma_j(v_i)

    Ensures zero leakage of degradation coefficients (kMc, kMt).
    Preserves DataFrame indices, column names, and allows attaching regime metadata.
    """

    def __init__(
        self,
        regime_column: str = "v",
        robust: bool = False,
        eps: float = 1e-9,
    ) -> None:
        self.regime_column = regime_column
        self.robust = robust
        self.eps = eps
        self.regime_stats_: dict[float, dict[str, tuple[float, float]]] = {}
        self.telemetry_columns_: list[str] = []

    def fit(self, X: pd.DataFrame, y: Any = None) -> OperatingRegimeNormalizer:
        if not isinstance(X, pd.DataFrame):
            raise TypeError("OperatingRegimeNormalizer requires a pandas DataFrame input.")

        if self.regime_column not in X.columns:
            raise ValueError(
                f"Regime column '{self.regime_column}' not found in input DataFrame columns: {list(X.columns)}"
            )

        self.telemetry_columns_ = [c for c in X.columns if c != self.regime_column]
        self.regime_stats_ = {}

        unique_regimes = X[self.regime_column].unique()
        for regime in unique_regimes:
            subset = X[X[self.regime_column] == regime][self.telemetry_columns_]
            stats_dict: dict[str, tuple[float, float]] = {}

            for col in self.telemetry_columns_:
                col_data = subset[col]
                if self.robust:
                    center = float(col_data.median())
                    q75 = float(col_data.quantile(0.75))
                    q25 = float(col_data.quantile(0.25))
                    scale = (q75 - q25) / 1.349  # Normal-consistent IQR scale
                else:
                    center = float(col_data.mean())
                    scale = float(col_data.std(ddof=1)) if len(col_data) > 1 else 1.0

                if scale < self.eps:
                    scale = 1.0  # Avoid division by zero for near-constant within-regime features

                stats_dict[col] = (center, scale)

            self.regime_stats_[float(regime)] = stats_dict

        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        if not isinstance(X, pd.DataFrame):
            raise TypeError("Input X must be a pandas DataFrame.")

        if self.regime_column not in X.columns:
            raise ValueError(f"Regime column '{self.regime_column}' missing during transform.")

        result = pd.DataFrame(index=X.index, columns=self.telemetry_columns_, dtype=np.float64)

        for regime, stats_dict in self.regime_stats_.items():
            mask = X[self.regime_column] == regime
            if not mask.any():
                continue

            subset = X.loc[mask, self.telemetry_columns_]
            for col in self.telemetry_columns_:
                center, scale = stats_dict[col]
                result.loc[mask, col] = (subset[col] - center) / scale

        # Check if any unknown regimes were encountered
        if result.isna().any().any():
            nan_rows = result.isna().any(axis=1).sum()
            raise ValueError(
                f"Found {nan_rows} rows with unobserved operating regime values during transform."
            )

        return result
