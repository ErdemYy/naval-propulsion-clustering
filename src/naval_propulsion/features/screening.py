"""Feature screening and redundancy diagnostics.

Detects zero-variance columns, exact duplicates, and near-duplicates,
and produces a formal decision table distinguishing mandatory removal,
candidate removal, and candidate retention.
"""

from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

from naval_propulsion.utils.paths import get_experiments_dir


def screen_features(
    df: pd.DataFrame,
    target_columns: tuple[str, ...] = ("kMc", "kMt"),
) -> pd.DataFrame:
    """Analyze feature variance, duplication, and produce screening decision table.

    Parameters
    ----------
    df : pd.DataFrame
        Complete 18-column naval propulsion dataset.
    target_columns : tuple[str, ...], default=("kMc", "kMt")
        Columns to exclude from telemetry feature screening (quarantined targets).

    Returns
    -------
    pd.DataFrame
        Screening decision table with columns:
        [feature, variance, duplicate_group, proposed_action, reason]
    """
    telemetry_cols = [c for c in df.columns if c not in target_columns]
    records: list[dict[str, str | float]] = []

    # Detect exact duplicates
    exact_duplicates: dict[str, str] = {}
    for i in range(len(telemetry_cols)):
        for j in range(i + 1, len(telemetry_cols)):
            c1, c2 = telemetry_cols[i], telemetry_cols[j]
            if (df[c1] == df[c2]).all():
                exact_duplicates[c2] = c1  # c2 is a duplicate of c1

    for col in telemetry_cols:
        series = df[col]
        var_val = float(series.var(ddof=1))

        if var_val == 0.0 or series.nunique() <= 1:
            prop_action = "mandatory removal"
            dup_grp = "none"
            reason = "Zero variance constant sensor (simulated ambient boundary condition)."
        elif col in exact_duplicates:
            master = exact_duplicates[col]
            prop_action = "mandatory removal"
            dup_grp = f"{master}/{col}"
            reason = f"Exact mathematical clone of {master} (|{col} - {master}| == 0 everywhere)."
        elif col == "lp":
            prop_action = "candidate removal"
            dup_grp = "operating_demand"
            reason = "Lever position is commanded operating demand; perfectly collinear with ship speed v."
        elif col == "v":
            prop_action = "candidate retention"
            dup_grp = "operating_regime"
            reason = "Ship speed defines discrete operating regimes; retained as regime index for conditional analysis."
        else:
            # Check near-duplicates (r > 0.999)
            high_corrs = []
            for other in telemetry_cols:
                if other != col and other not in ("T1", "P1") and other not in exact_duplicates:
                    corr = float(series.corr(df[other]))
                    if abs(corr) >= 0.999:
                        high_corrs.append(other)

            if high_corrs:
                prop_action = "candidate retention"
                dup_grp = f"near_dup({','.join(high_corrs)})"
                reason = f"Extremely high thermodynamic correlation with {high_corrs}, candidate for correlation pruning."
            else:
                prop_action = "candidate retention"
                dup_grp = "none"
                reason = "Informative thermodynamic telemetry feature with non-zero variance."

        records.append({
            "feature": col,
            "variance": var_val,
            "duplicate_group": dup_grp,
            "proposed_action": prop_action,
            "reason": reason,
        })

    decision_df = pd.DataFrame(records)
    return decision_df


def save_feature_screening_table(
    decision_df: pd.DataFrame,
    output_path: Path | None = None,
) -> Path:
    """Save screening decision table to CSV."""
    target_path = output_path or (get_experiments_dir() / "outputs" / "phase2" / "feature_screening.csv")
    target_path.parent.mkdir(parents=True, exist_ok=True)
    decision_df.to_csv(target_path, index=False)
    return target_path
