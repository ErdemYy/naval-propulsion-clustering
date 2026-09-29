# Phase 1 Formal Audit Report

**Project:** Naval Propulsion Clustering  
**Academic Title:** *Unsupervised Discovery of Operating and Performance Degradation Profiles in Naval Gas Turbine Propulsion Systems*  
**Date of Audit:** 2026-09-29  
**Audit Status:** Complete & Verified  

---

## 1. Dataset Provenance

- **Authoritative Source:** University of California, Irvine (UCI) Machine Learning Repository
- **Dataset Title:** Condition Based Maintenance of Naval Propulsion Plants (Dataset ID: 316)
- **Authoritative Archive URL:** `https://archive.ics.uci.edu/static/public/316/condition+based+maintenance+of+naval+propulsion+plants.zip`
- **Retrieval Timestamp:** 2026-09-29T11:53:31Z
- **Cryptographic Verification (SHA-256):**
  - Downloaded Zip Archive (`condition_based_maintenance_of_naval_propulsion_plants.zip`): `91a3815da80b5ab7e2d5b82ac82f1c2cbf89182c7a65bcdf240db1e014423cb9` (567,071 bytes)
  - Raw Telemetry Data File (`data.txt`): `de0ea69da1efaab8b9655ffed828547d10dd68c1fb8c6e0163e6a988def393a6` (3,448,926 bytes)
- **Provenance Manifest:** Generated and committed at [`data/raw/manifest.json`](file:///data/raw/manifest.json)
- **Untouched Raw Storage:** Pristine copies preserved under [`data/raw/`](file:///data/raw/) (`data.txt`, `Features.txt`, `README.txt`).

---

## 2. Dataset Dimensions & Ingestion Verification

- **Row Count:** Exactly 11,934 samples.
- **Column Count:** Exactly 18 numerical columns.
- **File Format:** Space-delimited ASCII text in scientific notation (e.g., `1.1380000e+00`), without an embedded header row. Column semantics and physical units are verified from the companion `Features.txt` and `README.txt` files.
- **Data Types:** 100% continuous double-precision floats (`float64`).
- **Missing Values:** 0 (0.0%).
- **Duplicate Rows:** 0 across all 18 columns.

---

## 3. Exact Schema & Authoritative Data Dictionary

| # | Symbol | Official Physical Meaning | Documented Units | Role Classification | Min | Max | Mean | Std | Unique |
| :- | :--- | :--- | :--- | :--- | :- | :- | :- | :- | :- |
| 1 | `lp` | Lever position | `[ ]` (Dimensionless) | Operating Condition | 1.138 | 9.300 | 5.1667 | 2.6264 | 9 |
| 2 | `v` | Ship speed (linear with `lp`) | `knots` | Operating Condition | 3.000 | 27.000 | 15.0000 | 7.7463 | 9 |
| 3 | `GTT` | Gas Turbine shaft torque | `kN m` | Sensor / Telemetry | 253.547 | 72,784.872 | 27,247.4987 | 22,148.6132 | 11,430 |
| 4 | `GTn` | Gas Turbine rate of revolutions | `rpm` | Sensor / Telemetry | 1,307.675 | 3,560.741 | 2,136.2893 | 774.0839 | 3,888 |
| 5 | `GGn` | Gas Generator rate of revolutions | `rpm` | Sensor / Telemetry | 6,589.002 | 9,797.103 | 8,200.9473 | 1,091.3155 | 11,834 |
| 6 | `Ts` | Starboard Propeller Torque | `kN` | Sensor / Telemetry | 5.304 | 645.249 | 227.3358 | 200.4959 | 4,286 |
| 7 | `Tp` | Port Propeller Torque | `kN` | Sensor / Telemetry | 5.304 | 645.249 | 227.3358 | 200.4959 | 4,286 |
| 8 | `T48` | HP Turbine exit temperature | `C` | Sensor / Telemetry | 442.364 | 1,115.797 | 735.4954 | 173.6806 | 11,772 |
| 9 | `T1` | GT Compressor inlet air temperature | `C` | Sensor (Zero Variance) | 288.000 | 288.000 | 288.0000 | 0.0000 | 1 |
| 10 | `T2` | GT Compressor outlet air temperature| `C` | Sensor / Telemetry | 540.442 | 789.094 | 646.2153 | 72.6759 | 11,506 |
| 11 | `P48` | HP Turbine exit pressure | `bar` | Sensor / Telemetry | 1.093 | 4.560 | 2.3530 | 1.0848 | 524 |
| 12 | `P1` | GT Compressor inlet air pressure | `bar` | Sensor (Zero Variance) | 0.998 | 0.998 | 0.9980 | 0.0000 | 1 |
| 13 | `P2` | GT Compressor outlet air pressure | `bar` | Sensor / Telemetry | 5.828 | 23.140 | 12.2971 | 5.3374 | 4,209 |
| 14 | `Pexh`| Gas Turbine exhaust gas pressure | `bar` | Sensor / Telemetry | 1.019 | 1.052 | 1.0295 | 0.0104 | 19 |
| 15 | `TIC` | Turbine Injecton Control | `%` | Sensor / Telemetry | 0.000 | 92.556 | 33.6413 | 25.8414 | 8,496 |
| 16 | `mf`  | Fuel flow | `kg/s` | Sensor / Telemetry | 0.068 | 1.832 | 0.6624 | 0.5071 | 696 |
| 17 | `kMc` | GT Compressor decay state coeff. | `[ ]` | Degradation / Target | 0.950 | 1.000 | 0.9750 | 0.0147 | 51 |
| 18 | `kMt` | GT Turbine decay state coeff. | `[ ]` | Degradation / Target | 0.975 | 1.000 | 0.9875 | 0.0075 | 26 |

*Complete catalog documented in [`docs/DATA_DICTIONARY.md`](file:///docs/DATA_DICTIONARY.md).*

---

## 4. Data Quality Findings

1. **[OBSERVED] Constant Zero-Variance Sensors:**
   - `T1` (Compressor inlet temperature) is identically $288.0$ across all 11,934 rows (std = 0.0).
   - `P1` (Compressor inlet pressure) is identically $0.998$ across all 11,934 rows (std = 0.0).
   - *Impact:* These represent static simulated ambient boundary conditions. They provide 0 bits of information for clustering and cause division by zero under Z-score scaling.
2. **[OBSERVED] Exact Collinear Duplication:**
   - Columns `Ts` (Starboard Propeller Torque) and `Tp` (Port Propeller Torque) are mathematically identical across every single row: $\max |Ts - Tp| = 0.0$.
   - *Impact:* Keeping both channels doubles the weight of propeller torque in distance-based clustering algorithms without adding information.
3. **[OBSERVED] Massive Feature Scale Disparities:**
   - Raw feature standard deviations range from $\approx 0.0104$ (`Pexh`) to $22,148.61$ (`GTT`), representing a scale disparity ratio exceeding **$2.1 \times 10^6$**.
   - *Impact:* Unscaled distance metrics (Euclidean, Manhattan) would be almost 100% dominated by `GTT` shaft torque alone.
4. **[OBSERVED] Extreme Multicollinearity:**
   - 28 pairs of telemetry features exhibit Pearson correlation $|r| \ge 0.95$. For example, `GTT` and `Ts` have $r = 0.9999$; `v` and `GTT` have $r = 0.9634$; `mf` and `GTT` have $r = 0.9965$.
   - *Impact:* Gas turbine physics enforce tight thermodynamic coupling between vessel speed, fuel flow, pressure ratios, and shaft torque.

---

## 5. Operating Condition & Degradation Observations

1. **[OBSERVED] Full Factorial Grid Architecture:**
   - The dataset is a rigid, synthetic 3-way factorial grid:
     $$11,934 = 9 \text{ speeds } (v \in [3, 27] \text{ knots}) \times 51 \text{ } kMc \text{ values } (0.950 \dots 1.000) \times 26 \text{ } kMt \text{ values } (0.975 \dots 1.000)$$
   - Every single operating speed has exactly $51 \times 26 = 1,326$ samples.
2. **[OBSERVED] Operating Regime Dominance:**
   - Variance across the 9 discrete ship speeds (3, 6, 9, 12, 15, 18, 21, 24, 27 knots) accounts for the vast majority of total sensor variance.
   - Component degradation represents subtle efficiency variations ($1\% - 5\%$) that manifest as small local perturbations around each operating point.
3. **[HYPOTHESIS]**
   - Unconditioned clustering on the full standardized sensor matrix will cluster primarily into $k=9$ operating clusters (corresponding to discrete speed setpoints).
   - Discovering pure degradation profiles will require either operating-regime conditioning (e.g., clustering within a single speed regime or clustering residual deviations relative to operating-point means) or algorithms capable of sub-cluster density partitioning.

---

## 6. Anti-Leakage & Quarantine Verification

- **[OBSERVED]** The `DatasetContainer` contract enforces that `kMc` and `kMt` reside exclusively in `DatasetContainer.targets`.
- **[OBSERVED]** Test `test_no_degradation_leakage` verified that neither `kMc` nor `kMt` exists in `container.features` or `container.feature_names`.
- **[DECISION]** Under no circumstance will `kMc` or `kMt` enter any scaler, PCA transformation, or clustering algorithm. They remain quarantined for post-hoc statistical validation in Phase 4.

---

## 7. Decisions That Remain Intentionally Open (Phase 2 & 3)

In accordance with scientific rigor, the following decisions were deliberately NOT made during Phase 1:

1. **Scaler Selection:** Whether `StandardScaler` (Z-score), `RobustScaler` (quantile-based), or `MinMaxScaler` is optimal will be tested empirically in Phase 2.
2. **Exact Feature Selection / Reduction:** Whether to drop `Ts` or `Tp` (or average them), drop constant columns `T1`/`P1`, or apply PCA will be evaluated in Phase 2.
3. **Operating-Regime Conditioning Strategy:** Whether to cluster raw normalized features or baseline-subtracted operating residuals will be formulated as explicit comparative experiments in Phase 3.
4. **Clustering Algorithm & Cluster Count ($k$):** The number of clusters and algorithm choice (K-Means, DBSCAN, Agglomerative, GMM) will be determined via empirical sweeps and intrinsic metrics in Phase 3.

---

## 8. Recommended Questions for Phase 2

1. **Q1:** Does applying PCA capture the non-linear thermodynamic manifold across speed regimes without losing the subtle variance associated with $kMc$ and $kMt$?
2. **Q2:** How does removing exact collinear duplicates (`Tp` or `Ts`) and constant columns (`T1`, `P1`) affect the conditioning number of the feature covariance matrix?
3. **Q3:** What is the mathematical formulation for an operating-regime residual transformer (subtracting speed-conditioned mean sensor readings) to isolate degradation signatures from commanded ship speed demand?
