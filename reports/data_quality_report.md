# Data Quality & Integrity Report

**Dataset:** Condition Based Maintenance of Naval Propulsion Plants (UCI ML Repository #316)
**Audit Phase:** Phase 1 — Ingestion and Data Quality Audit

---

## 1. Executive Summary

- **Total Rows:** 11,934
- **Total Columns:** 18
- **Duplicate Rows:** 0
- **Missing Values (NaN/null):** 0 (0.0%)
- **Non-Finite / Infinite Values:** 0
- **Zero-Variance Constant Columns:** ['T1', 'P1']
- **Near-Constant Columns (std < 0.01):** ['kMt']
- **Identical Column Pairs:** [('Ts', 'Tp')]

---

## 2. Column-Level Descriptive & Diagnostic Profile

| Column | Dtype | Min | Max | Mean | Median | Std | Skew | IQR Outliers | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `lp` | `float64` | 1.138 | 9.3 | 5.167 | 5.14 | 2.626 | 0.02 | 0 | Normal |
| `v` | `float64` | 3 | 27 | 15 | 15 | 7.746 | 0.00 | 0 | Normal |
| `GTT` | `float64` | 253.5 | 7.278e+04 | 2.725e+04 | 2.163e+04 | 2.215e+04 | 0.77 | 0 | Normal |
| `GTn` | `float64` | 1308 | 3561 | 2136 | 1924 | 774.1 | 0.57 | 0 | Normal |
| `GGn` | `float64` | 6589 | 9797 | 8201 | 8482 | 1091 | -0.14 | 0 | Normal |
| `Ts` | `float64` | 5.304 | 645.2 | 227.3 | 175.3 | 200.5 | 0.81 | 0 | Normal |
| `Tp` | `float64` | 5.304 | 645.2 | 227.3 | 175.3 | 200.5 | 0.81 | 0 | Normal |
| `T48` | `float64` | 442.4 | 1116 | 735.5 | 706 | 173.7 | 0.56 | 0 | Normal |
| `T1` | `float64` | 288 | 288 | 288 | 288 | 0 | 0.00 | 0 | **Zero Variance** |
| `T2` | `float64` | 540.4 | 789.1 | 646.2 | 637.1 | 72.68 | 0.43 | 0 | Normal |
| `P48` | `float64` | 1.093 | 4.56 | 2.353 | 2.083 | 1.085 | 0.71 | 0 | Normal |
| `P1` | `float64` | 0.998 | 0.998 | 0.998 | 0.998 | 0 | 0.00 | 0 | **Zero Variance** |
| `P2` | `float64` | 5.828 | 23.14 | 12.3 | 11.09 | 5.337 | 0.63 | 0 | Normal |
| `Pexh` | `float64` | 1.019 | 1.052 | 1.029 | 1.026 | 0.01039 | 0.77 | 0 | Normal |
| `TIC` | `float64` | 0 | 92.56 | 33.64 | 25.28 | 25.84 | 0.90 | 192 | IQR Outliers (192) |
| `mf` | `float64` | 0.068 | 1.832 | 0.6624 | 0.496 | 0.5071 | 1.00 | 0 | Normal |
| `kMc` | `float64` | 0.95 | 1 | 0.975 | 0.975 | 0.01472 | 0.00 | 0 | Normal |
| `kMt` | `float64` | 0.975 | 1 | 0.9875 | 0.9875 | 0.0075 | 0.00 | 0 | Near Constant |

---

## 3. Critical Structural Findings

### 3.1 Constant Sensors (Zero-Variance)
- `T1` (GT Compressor inlet air temperature) = 288.0 K (15 °C) across all 11,934 samples (std = 0.0).
- `P1` (GT Compressor inlet air pressure) = 0.998 bar across all 11,934 samples (std = 0.0).
> **Methodological Implication:** Constant columns contribute zero information to distance-based or variance-based clustering and cause division by zero during standard Z-score scaling. They will be safely dropped during Phase 2 preprocessing.

### 3.2 Exact Duplicate Columns
- Pair (`Ts`, `Tp`): Starboard Propeller Torque and Port Propeller Torque are mathematically identical (max absolute difference = 0.0) across all 11,934 records.
> **Methodological Implication:** Keeping both represents exact collinear redundancy. Retaining one propeller torque channel prevents artificial double-weighting in distance calculations.

### 3.3 Massive Feature Scale Disparities
- Maximum standard deviation: `GTT` (std = 22148.61)
- Minimum non-zero standard deviation: `kMt` (std = 0.0075)
- Ratio of max to min scale: **2,953,024.7x**
> **Methodological Implication:** Without scaling, features like shaft torque (`GTT`, std > 22,000) completely dominate Euclidean distance, rendering temperature and pressure features invisible to clustering.

### 3.4 Collinearity & Redundancy (Pearson |r| >= 0.95)

| Feature 1 | Feature 2 | Pearson r | Physical Relationship |
| :--- | :--- | :--- | :--- |
| `Ts` | `Tp` | 1.0000 | Strong Thermodynamic Coupling |
| `lp` | `v` | 0.9999 | Strong Thermodynamic Coupling |
| `P48` | `P2` | 0.9994 | Strong Thermodynamic Coupling |
| `GTT` | `Ts` | 0.9992 | Strong Thermodynamic Coupling |
| `GTT` | `Tp` | 0.9992 | Strong Thermodynamic Coupling |
| `GTT` | `P48` | 0.9989 | Strong Thermodynamic Coupling |
| `Ts` | `P48` | 0.9980 | Strong Thermodynamic Coupling |
| `Tp` | `P48` | 0.9980 | Strong Thermodynamic Coupling |
| `P48` | `Pexh` | 0.9979 | Strong Thermodynamic Coupling |
| `GTT` | `P2` | 0.9976 | Strong Thermodynamic Coupling |
| `P2` | `Pexh` | 0.9963 | Strong Thermodynamic Coupling |
| `Ts` | `Pexh` | 0.9962 | Strong Thermodynamic Coupling |
| `Tp` | `Pexh` | 0.9962 | Strong Thermodynamic Coupling |
| `Ts` | `P2` | 0.9962 | Strong Thermodynamic Coupling |
| `Tp` | `P2` | 0.9962 | Strong Thermodynamic Coupling |
| `GTT` | `Pexh` | 0.9960 | Strong Thermodynamic Coupling |
| `GTn` | `P2` | 0.9960 | Strong Thermodynamic Coupling |
| `GTn` | `P48` | 0.9951 | Strong Thermodynamic Coupling |
| `GTT` | `mf` | 0.9951 | Strong Thermodynamic Coupling |
| `T2` | `P2` | 0.9944 | Strong Thermodynamic Coupling |
| `Ts` | `mf` | 0.9944 | Strong Thermodynamic Coupling |
| `Tp` | `mf` | 0.9944 | Strong Thermodynamic Coupling |
| `GTn` | `Pexh` | 0.9940 | Strong Thermodynamic Coupling |
| `P48` | `mf` | 0.9927 | Strong Thermodynamic Coupling |
| `T48` | `T2` | 0.9923 | Strong Thermodynamic Coupling |
| `T2` | `P48` | 0.9917 | Strong Thermodynamic Coupling |
| `GTT` | `T48` | 0.9911 | Strong Thermodynamic Coupling |
| `Pexh` | `mf` | 0.9910 | Strong Thermodynamic Coupling |
| `T48` | `P2` | 0.9905 | Strong Thermodynamic Coupling |
| `GTT` | `T2` | 0.9902 | Strong Thermodynamic Coupling |
| `GTT` | `GTn` | 0.9897 | Strong Thermodynamic Coupling |
| `T48` | `P48` | 0.9894 | Strong Thermodynamic Coupling |
| `GTn` | `T2` | 0.9893 | Strong Thermodynamic Coupling |
| `P2` | `mf` | 0.9893 | Strong Thermodynamic Coupling |
| `GTn` | `Ts` | 0.9886 | Strong Thermodynamic Coupling |
| `GTn` | `Tp` | 0.9886 | Strong Thermodynamic Coupling |
| `Ts` | `T2` | 0.9874 | Strong Thermodynamic Coupling |
| `Tp` | `T2` | 0.9874 | Strong Thermodynamic Coupling |
| `v` | `GGn` | 0.9866 | Strong Thermodynamic Coupling |
| `T48` | `mf` | 0.9863 | Strong Thermodynamic Coupling |
| `lp` | `GGn` | 0.9860 | Strong Thermodynamic Coupling |
| `Ts` | `T48` | 0.9860 | Strong Thermodynamic Coupling |
| `Tp` | `T48` | 0.9860 | Strong Thermodynamic Coupling |
| `TIC` | `mf` | 0.9855 | Strong Thermodynamic Coupling |
| `T2` | `Pexh` | 0.9835 | Strong Thermodynamic Coupling |
| `lp` | `T2` | 0.9827 | Strong Thermodynamic Coupling |
| `v` | `T2` | 0.9812 | Strong Thermodynamic Coupling |
| `GTn` | `mf` | 0.9802 | Strong Thermodynamic Coupling |
| `T48` | `Pexh` | 0.9801 | Strong Thermodynamic Coupling |
| `GTn` | `T48` | 0.9796 | Strong Thermodynamic Coupling |
| `GTT` | `TIC` | 0.9779 | Strong Thermodynamic Coupling |
| `Ts` | `TIC` | 0.9775 | Strong Thermodynamic Coupling |
| `Tp` | `TIC` | 0.9775 | Strong Thermodynamic Coupling |
| `T2` | `mf` | 0.9765 | Strong Thermodynamic Coupling |
| `P48` | `TIC` | 0.9757 | Strong Thermodynamic Coupling |
| `Pexh` | `TIC` | 0.9742 | Strong Thermodynamic Coupling |
| `P2` | `TIC` | 0.9721 | Strong Thermodynamic Coupling |
| `T48` | `TIC` | 0.9697 | Strong Thermodynamic Coupling |
| `lp` | `P2` | 0.9691 | Strong Thermodynamic Coupling |
| `v` | `P2` | 0.9670 | Strong Thermodynamic Coupling |
| `GGn` | `T2` | 0.9667 | Strong Thermodynamic Coupling |
| `lp` | `P48` | 0.9631 | Strong Thermodynamic Coupling |
| `GTn` | `TIC` | 0.9623 | Strong Thermodynamic Coupling |
| `lp` | `GTn` | 0.9621 | Strong Thermodynamic Coupling |
| `lp` | `T48` | 0.9612 | Strong Thermodynamic Coupling |
| `lp` | `GTT` | 0.9610 | Strong Thermodynamic Coupling |
| `v` | `P48` | 0.9606 | Strong Thermodynamic Coupling |
| `v` | `GTn` | 0.9604 | Strong Thermodynamic Coupling |
| `lp` | `Ts` | 0.9592 | Strong Thermodynamic Coupling |
| `lp` | `Tp` | 0.9592 | Strong Thermodynamic Coupling |
| `v` | `T48` | 0.9588 | Strong Thermodynamic Coupling |
| `T2` | `TIC` | 0.9587 | Strong Thermodynamic Coupling |
| `v` | `GTT` | 0.9582 | Strong Thermodynamic Coupling |
| `v` | `Ts` | 0.9564 | Strong Thermodynamic Coupling |
| `v` | `Tp` | 0.9564 | Strong Thermodynamic Coupling |
| `lp` | `Pexh` | 0.9534 | Strong Thermodynamic Coupling |
| `v` | `Pexh` | 0.9508 | Strong Thermodynamic Coupling |

---

## 4. Anti-Leakage Quarantine Verification

- Degradation variables `kMc` and `kMt` have been identified and quarantined.
- Ingestion contracts guarantee that `kMc` and `kMt` are stored strictly in `DatasetContainer.targets`.
- Neither `kMc` nor `kMt` will enter any clustering algorithm or feature transformer.

## 5. Non-Intervention Principle Adherence

- **No features were dropped during this phase.**
- **No outliers were removed.**
- **No scaler was chosen or applied.**
- Data quality was observed, characterized, and documented to inform Phase 2 design choices.
