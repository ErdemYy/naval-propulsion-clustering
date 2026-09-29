# Formal Data Dictionary

**Dataset:** Condition Based Maintenance of Naval Propulsion Plants  
**Authoritative Source:** UCI Machine Learning Repository (Dataset ID: 316)  
**Authoritative Documentation Files:** `Features.txt` and `README.txt` (Coraddu et al., 2014)  
**Physical System:** Numerical simulator of a naval vessel (Frigate) with a Combined Diesel and Gas Turbine (CODAG) propulsion plant.  
**Total Records:** 11,934  
**Total Columns:** 18  

---

## 1. Variable Role Classification Definitions

- **Operating Condition:** Variables representing external operational demand or commanded vessel maneuvering setpoints (`lp`, `v`).
- **Sensor / Telemetry:** Direct physical measurements from thermodynamic sensors, shaft encoders, or engine controllers (`GTT`, `GTn`, `GGn`, `Ts`, `Tp`, `T48`, `T1`, `T2`, `P48`, `P1`, `P2`, `Pexh`, `TIC`, `mf`).
- **Degradation / Reference:** Internal physical decay state coefficients representing component degradation (`kMc`, `kMt`). **Strictly held out from unsupervised training feature sets.**

---

## 2. Comprehensive Column Catalog

| # | Column Name | Dtype | Unit | Official Physical Meaning | Min | Max | Mean | Median | Std | Missing | Unique | Role Classification |
| :- | :--- | :--- | :--- | :--- | :- | :- | :- | :- | :- | :- | :- | :--- |
| 1 | `lp` | `float64` | `[ ]` (Dimensionless) | Lever position | 1.138 | 9.300 | 5.1667 | 5.1400 | 2.6264 | 0 | 9 | Operating Condition |
| 2 | `v` | `float64` | `knots` | Ship speed (linear function of lever position `lp`) | 3.000 | 27.000 | 15.0000 | 15.0000 | 7.7463 | 0 | 9 | Operating Condition |
| 3 | `GTT` | `float64` | `kN m` | Gas Turbine shaft torque | 253.547 | 72784.872 | 27247.4987 | 21630.6590 | 22148.6132 | 0 | 11,430 | Sensor / Telemetry |
| 4 | `GTn` | `float64` | `rpm` | Gas Turbine rate of revolutions | 1307.675 | 3560.741 | 2136.2893 | 1924.3260 | 774.0839 | 0 | 3,888 | Sensor / Telemetry |
| 5 | `GGn` | `float64` | `rpm` | Gas Generator rate of revolutions | 6589.002 | 9797.103 | 8200.9473 | 8482.0815 | 1091.3155 | 0 | 11,834 | Sensor / Telemetry |
| 6 | `Ts` | `float64` | `kN` | Starboard Propeller Torque | 5.304 | 645.249 | 227.3358 | 175.2680 | 200.4959 | 0 | 4,286 | Sensor / Telemetry |
| 7 | `Tp` | `float64` | `kN` | Port Propeller Torque | 5.304 | 645.249 | 227.3358 | 175.2680 | 200.4959 | 0 | 4,286 | Sensor / Telemetry |
| 8 | `T48` | `float64` | `C` | HP Turbine exit temperature | 442.364 | 1115.797 | 735.4954 | 706.0380 | 173.6806 | 0 | 11,772 | Sensor / Telemetry |
| 9 | `T1` | `float64` | `C` | GT Compressor inlet air temperature | 288.000 | 288.000 | 288.0000 | 288.0000 | 0.0000 | 0 | 1 | Sensor / Telemetry (Zero Variance) |
| 10 | `T2` | `float64` | `C` | GT Compressor outlet air temperature | 540.442 | 789.094 | 646.2153 | 637.1415 | 72.6759 | 0 | 11,506 | Sensor / Telemetry |
| 11 | `P48` | `float64` | `bar` | HP Turbine exit pressure | 1.093 | 4.560 | 2.3530 | 2.0830 | 1.0848 | 0 | 524 | Sensor / Telemetry |
| 12 | `P1` | `float64` | `bar` | GT Compressor inlet air pressure | 0.998 | 0.998 | 0.9980 | 0.9980 | 0.0000 | 0 | 1 | Sensor / Telemetry (Zero Variance) |
| 13 | `P2` | `float64` | `bar` | GT Compressor outlet air pressure | 5.828 | 23.140 | 12.2971 | 11.0920 | 5.3374 | 0 | 4,209 | Sensor / Telemetry |
| 14 | `Pexh` | `float64` | `bar` | Gas Turbine exhaust gas pressure | 1.019 | 1.052 | 1.0295 | 1.0260 | 0.0104 | 0 | 19 | Sensor / Telemetry |
| 15 | `TIC` | `float64` | `%` | Turbine Injecton Control | 0.000 | 92.556 | 33.6413 | 25.2765 | 25.8414 | 0 | 8,496 | Sensor / Telemetry |
| 16 | `mf` | `float64` | `kg/s` | Fuel flow | 0.068 | 1.832 | 0.6624 | 0.4960 | 0.5071 | 0 | 696 | Sensor / Telemetry |
| 17 | `kMc` | `float64` | `[ ]` (Dimensionless) | GT Compressor decay state coefficient | 0.950 | 1.000 | 0.9750 | 0.9750 | 0.0147 | 0 | 51 | Degradation / Reference (Target) |
| 18 | `kMt` | `float64` | `[ ]` (Dimensionless) | GT Turbine decay state coefficient | 0.975 | 1.000 | 0.9875 | 0.9875 | 0.0075 | 0 | 26 | Degradation / Reference (Target) |

---

## 3. Physical Units & Measurement Standards

- **Temperatures (`T48`, `T1`, `T2`):** Documented in `[C]` (Celsius) in `Features.txt`. However, standard atmospheric reference temperature for `T1` is recorded as 288.0, which corresponds physically to 288.0 K (14.85 °C / 15 °C ISO standard day). The numerical values are preserved unmodified.
- **Pressures (`P48`, `P1`, `P2`, `Pexh`):** Documented in `[bar]` (1 bar = 100 kPa).
- **Torques (`GTT`, `Ts`, `Tp`):** Shaft torque in `[kN m]` (kilonewton-meters) and propeller torques in `[kN]`.
- **Rotational Speeds (`GTn`, `GGn`):** Documented in `[rpm]` (revolutions per minute).
- **Fuel Flow (`mf`):** Documented in `[kg/s]`.
- **Degradation Coefficients (`kMc`, `kMt`):** Multiplicative efficiency degradation factors:
  - $kMc \in [0.95, 1.00]$: 1.00 represents pristine compressor state; 0.95 represents 5% compressor decay.
  - $kMt \in [0.975, 1.00]$: 1.00 represents pristine turbine state; 0.975 represents 2.5% turbine decay.

---

## 4. Methodological Invariants & Quarantine Protocol

1. **Target Separation:** `kMc` and `kMt` are strictly quarantined. Under no circumstances will columns 17 or 18 be supplied to scaling, PCA, or unsupervised clustering algorithms.
2. **Deterministic Layout:** The dataset represents a full 3-way factorial grid:
   $$\text{Samples} = 9 \text{ speeds } \times 51 \text{ } kMc \text{ decay values } \times 26 \text{ } kMt \text{ decay values } = 11,934 \text{ rows}$$
3. **Collinearity Redundancy:** `Ts` and `Tp` are exact mathematical duplicates ($|Ts - Tp| = 0$ for all rows), indicating symmetric twin-shaft propeller torque modeling in the simulator.
4. **Zero-Variance Sensors:** `T1` and `P1` are constant ambient boundary conditions (variance = 0) and will be formally filtered prior to distance-based clustering in Phase 2.
