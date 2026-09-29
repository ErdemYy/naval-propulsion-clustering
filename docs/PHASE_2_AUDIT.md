# Phase 2 Formal Audit Report: Preprocessing, Feature Engineering & Operating-Condition Analysis

**Project:** Naval Propulsion Clustering  
**Academic Title:** *Unsupervised Discovery of Operating and Performance Degradation Profiles in Naval Gas Turbine Propulsion Systems*  
**Date of Audit:** 2026-09-29  
**Phase Status:** Complete & Verified  

---

## 1. Feature Screening & Redundancy Analysis

### 1.1 Zero-Variance Sensors
- **[OBSERVED]** Compressor inlet temperature `T1` ($288.0$ K) and compressor inlet pressure `P1` ($0.998$ bar) exhibit zero variance ($\sigma^2 = 0.0$) across all 11,934 records.
- **[DECISION]** **Mandatory removal.** Zero-variance features carry 0 bits of information for clustering and cause mathematical division-by-zero errors in standard scaling ($z = (x - \mu)/\sigma$).

### 1.2 Exact Duplicate Sensors
- **[OBSERVED]** Starboard Propeller Torque (`Ts`) and Port Propeller Torque (`Tp`) are exact mathematical clones across all 11,934 records:
  $$\max |Ts - Tp| = 0.0$$
- **[DECISION]** **Mandatory removal of `Tp`.** Retaining both channels artificially doubles the geometrical distance penalty along the propeller torque axis without introducing any new information.

### 1.3 Screening Decision Table
The complete machine-readable decision table is persisted in [`experiments/outputs/phase2/feature_screening.csv`](file:///experiments/outputs/phase2/feature_screening.csv):

| Feature | Variance | Proposed Action | Duplicate Group | Justification |
| :--- | :--- | :--- | :--- | :--- |
| `T1` | $0.000$ | **Mandatory Removal** | None | Constant simulated ambient temperature ($288$ K). |
| `P1` | $0.000$ | **Mandatory Removal** | None | Constant simulated ambient pressure ($0.998$ bar). |
| `Tp` | $40,198.60$ | **Mandatory Removal** | `Ts/Tp` | Exact clone of `Ts` ($|Tp - Ts| = 0$ everywhere). |
| `lp` | $6.898$ | **Candidate Removal** | `operating_demand` | Commanded lever position; collinear ($r = 0.9999$) with ship speed `v`. |
| `v` | $60.005$ | **Candidate Retention** | `operating_regime` | Discrete operating speed setpoint (3 to 27 knots). |
| `GTT` | $4.91 \times 10^8$ | **Candidate Retention** | `near_dup(Ts)` | Gas turbine shaft torque; primary thermodynamic output. |
| `GTn` | $5.99 \times 10^5$ | **Candidate Retention** | None | Gas turbine rotational speed. |
| `GGn` | $1.19 \times 10^6$ | **Candidate Retention** | None | Gas generator rotational speed. |
| `Ts` | $40,198.60$ | **Candidate Retention** | `near_dup(GTT)` | Propeller torque; retained representative for propulsion load. |
| `T48` | $30,164.93$ | **Candidate Retention** | None | High-pressure turbine exit temperature. |
| `T2` | $5,281.78$ | **Candidate Retention** | None | Compressor outlet temperature. |
| `P48` | $1.177$ | **Candidate Retention** | `near_dup(P2)` | Turbine exit pressure. |
| `P2` | $28.488$ | **Candidate Retention** | `near_dup(P48)` | Compressor outlet pressure. |
| `Pexh` | $1.08 \times 10^{-4}$ | **Candidate Retention** | None | Exhaust gas pressure. |
| `TIC` | $667.78$ | **Candidate Retention** | None | Turbine injection control percentage. |
| `mf` | $0.257$ | **Candidate Retention** | None | Fuel mass flow rate. |

---

## 2. Correlation Analysis & Feature Representations

- **[OBSERVED]** Telemetry features exhibit intense collinearity: 40 feature pairs have Pearson correlation $|r| \ge 0.98$. Commanded ship speed `v` and lever position `lp` have $r = 0.9999$.
- **[EXPERIMENT]** Formulated two primary feature sets:
  1. **Representation A (Minimal-Cleaning):** Retains all 13 non-constant, non-duplicate sensors (`lp`, `v`, `GTT`, `GTn`, `GGn`, `Ts`, `T48`, `T2`, `P48`, `P2`, `Pexh`, `TIC`, `mf`).
  2. **Representation B (Reduced-Correlation):** Prunes collinear duplicates by retaining one representative per physical subsystem: `v` (speed), `GTT` (torque), `GTn` (power turbine RPM), `GGn` (gas generator RPM), `T48` (turbine exit temp), `T2` (compressor exit temp), `P2` (compressor exit pressure), `TIC` (injection control), `mf` (fuel flow).
- **[DECISION]** Both Representation A and Representation B are registered in [`representation_registry.json`](file:///experiments/outputs/phase2/representation_registry.json) so Phase 3 clustering experiments can empirically test whether collinearity pruning improves or degrades cluster stability.

Figures:
- Pearson Heatmap: [`reports/figures/phase2/pearson_correlation.png`](file:///reports/figures/phase2/pearson_correlation.png)
- Spearman Heatmap: [`reports/figures/phase2/spearman_correlation.png`](file:///reports/figures/phase2/spearman_correlation.png)

---

## 3. Scaler Comparison

- **[OBSERVED]** Transformed distribution diagnostics:
  - **StandardScaler:** Produces transformed feature values in $[-1.69, +2.31]$ (mean = 0.0, std = 1.0). Equalizes geometric variance across all axes.
  - **RobustScaler:** Produces transformed feature values in $[-1.08, +2.18]$ (median = 0.0, overall std = 0.68). Prevents scale compression from operating boundary tails.
  - **MinMaxScaler:** Compresses all features into $[0.0, 1.0]$ (mean = 0.38, std = 0.31). Strictly preserves relative distances but sensitive to extreme boundary setpoints.
- **[DECISION]** Scaler choice is not hard-coded. `StandardScaler` is designated as the primary baseline, with `RobustScaler` and `MinMaxScaler` retained in the registry for comparative benchmark in Phase 3.
- **Figure:** [`reports/figures/phase2/scaler_comparison.png`](file:///reports/figures/phase2/scaler_comparison.png)
- **Data Report:** [`experiments/outputs/phase2/scaler_comparison.json`](file:///experiments/outputs/phase2/scaler_comparison.json)

---

## 4. Outlier Investigation

- **[OBSERVED]**
  - **Univariate:** Zero robust z-score outliers ($|z_{robust}| > 3.5$) across almost all sensors. Only `TIC` has 192 IQR boundary points.
  - **Multivariate:** Mahalanobis distance with $\chi^2$ cutoff ($p = 0.001$) identified 119 samples (1.0% of dataset).
  - **Sample Classification:**
    - Ordinary: **11,815 samples (99.0%)**
    - Potentially extreme: **119 samples (1.0%)**
    - Highly extreme: **0 samples (0.0%)**
- **[OBSERVED & INTERPRETATION]** The 119 potentially extreme points occur strictly at the operational boundary extremes: minimum idle speed (3 knots) and maximum flank speed (27 knots).
- **[DECISION]** **No outliers will be dropped.** These points represent valid physical boundary operating regimes of the naval vessel, not sensor errors or noise artifacts.
- **Data Report:** [`experiments/outputs/phase2/outlier_report.json`](file:///experiments/outputs/phase2/outlier_report.json)

---

## 5. Operating Condition Dominance Analysis

- **[OBSERVED]** Analysis of variance across the 9 discrete ship speeds ($v \in [3, 27]$ knots) reveals that **operating speed explains an average of 99.33% of total sensor variance across all telemetry channels**:
  - `Ts` (Propeller Torque): **100.00%** explained by speed ($\eta^2 = 1.000$)
  - `GTn` (Turbine RPM): **99.98%** explained by speed ($\eta^2 = 0.9998$)
  - `GGn` (Gas Gen RPM): **99.94%** explained by speed ($\eta^2 = 0.9994$)
  - `GTT` (Shaft Torque): **99.86%** explained by speed ($\eta^2 = 0.9986$)
  - `mf` (Fuel Flow): **99.58%** explained by speed ($\eta^2 = 0.9958$)
  - `T48` (Turbine Exit Temp): **97.70%** explained by speed ($\eta^2 = 0.9770$)
  - `TIC` (Injection Control): **96.59%** explained by speed ($\eta^2 = 0.9659$)
- **[MATHEMATICAL FACT]** Between-speed variance dwarfs within-speed variance by a factor of 30 to 5,000.
- **[SCIENTIFIC IMPLICATION]** Unconditioned clustering on globally scaled telemetry will 100% simply discover the 9 operating speed setpoints. Subtle component degradation ($kMc \in [0.95, 1.0]$, $kMt \in [0.975, 1.0]$) accounts for $< 3.5\%$ of variance and is completely hidden by commanded vessel speed.
- **Figure:** [`reports/figures/phase2/operating_speed_profiles.png`](file:///reports/figures/phase2/operating_speed_profiles.png)
- **Data Report:** [`experiments/outputs/phase2/operating_regime_report.json`](file:///experiments/outputs/phase2/operating_regime_report.json)

---

## 6. Within-Regime Normalization Transformer

- **[EXPERIMENT]** Implemented [`OperatingRegimeNormalizer`](file:///src/naval_propulsion/preprocessing/transformers.py#L76-L162) in `src/naval_propulsion/preprocessing/transformers.py`.
- **[MATHEMATICAL SPECIFICATION]** For each telemetry sensor $j$ and sample $i$ under operating regime $v_i$:
  $$z_{ij} = \frac{x_{ij} - \mu_j(v_i)}{\sigma_j(v_i)}$$
- **[INVARIANTS VERIFIED]**
  - Uses strictly clustering-eligible telemetry and operating condition $v$.
  - Zero leakage of degradation targets $kMc$ and $kMt$.
  - Verified by `test_within_speed_normalization_determinism`: transforms within-speed means to $0.000$ and within-speed std to $1.000$.
- **[DECISION]** This transformer forms the foundation of **Representation R5 (Within-Speed Normalized)**.

---

## 7. PCA / Dimensionality Reduction Findings

- **[OBSERVED]**
  - **PC1 alone accounts for 97.41% of total variance.**
  - **PC1 + PC2 account for 99.34% of total variance.**
  - **Component Loadings:** Every single sensor feature has an identical positive loading on PC1 of $\approx +0.27$ to $+0.28$.
- **[SCIENTIFIC INTERPRETATION]** PC1 is the 1D thermodynamic plant operating line governed by commanded ship speed. Component degradation ($kMc$, $kMt$) is compressed into minor residual components (PC3 to PC6).
- **[DECISION]** **PCA will NOT be applied as an automatic dimensionality reduction step prior to clustering.** Prematurely keeping 2 or 3 principal components would discard degradation signatures. PCA is retained for diagnostic visualization only.
- **Figures:**
  - Scree Plot: [`reports/figures/phase2/pca_explained_variance.png`](file:///reports/figures/phase2/pca_explained_variance.png)
  - Loadings Heatmap: [`reports/figures/phase2/pca_loadings.png`](file:///reports/figures/phase2/pca_loadings.png)
- **Data Report:** [`experiments/outputs/phase2/pca_analysis.json`](file:///experiments/outputs/phase2/pca_analysis.json)

---

## 8. Candidate Feature Representations for Phase 3

Formally registered in [`experiments/outputs/phase2/representation_registry.json`](file:///experiments/outputs/phase2/representation_registry.json):

1. **`R1_ALL_VALID_TELEMETRY` (Baseline):** All 13 valid sensors including $v$ and $lp$, globally standardized. Hypothesized to discover operating regimes ($k \approx 9$).
2. **`R2_WITHOUT_OPERATING_DEMAND`:** 11 sensors excluding $v$ and $lp$, globally standardized. Tests whether operating regimes still dominate via coupled physics.
3. **`R3_REDUCED_CORRELATION`:** 9 pruned sensors (|r| < 0.985), globally standardized. Tests impact of collinearity removal.
4. **`R4_ROBUST_SCALED_TELEMETRY`:** 11 sensors scaled via RobustScaler. Tests boundary outlier sensitivity.
5. **`R5_WITHIN_SPEED_NORMALIZED` (Recommended Degradation Candidate):** 11 sensors normalized conditionally within each operating speed. Hypothesized to strip speed variance and expose subtle degradation profiles.

---

## 9. Unresolved Methodological Questions (For Phase 3)

1. **Q1:** In Representation R1 and R2, does K-Means with $k=9$ recover the 9 discrete ship speeds with near-100% Adjusted Rand Index?
2. **Q2:** In Representation R5 (Within-Speed Normalized), do clustering algorithms partition points by compressor decay ($kMc$) or turbine decay ($kMt$)?
3. **Q3:** Which clustering family (K-Means, Hierarchical, DBSCAN, or GMM) achieves the highest intrinsic silhouette score and stability on Representation R5?
