# Research Methodology & Experimental Protocol

**Academic Title:** *Unsupervised Discovery of Operating and Performance Degradation Profiles in Naval Gas Turbine Propulsion Systems*

---

## 1. Research Questions (RQ)

- **RQ1:** Can unsupervised clustering algorithms identify distinct, coherent operating regimes in a naval gas turbine propulsion plant based solely on multivariate physical sensor measurements?
- **RQ2:** To what extent do clusters formed in the sensor feature space reflect variations in component health (specifically Compressor Decay State $kMc$ and Turbine Decay State $kMt$), without those decay states being visible to the algorithms?
- **RQ3:** Are cluster boundaries dominated primarily by high-variance operating variables (e.g., ship speed, shaft torque, fuel flow) rather than subtle degradation effects, and does normalization/feature engineering reveal degradation-sensitive sub-profiles?
- **RQ4:** Which clustering family (partitioning, density-based, hierarchical, or mixture models) offers the most physically interpretable partition according to intrinsic cluster validation metrics and stability checks?

---

## 2. Core Methodological Principles

### 2.1 Pure Unsupervised Paradigm
Clustering is exploratory and descriptive. We deliberately avoid framing this problem as supervised degradation regression or classification. Algorithms receive an unlabelled feature matrix $\mathbf{X} \in \mathbb{R}^{n \times d}$.

### 2.2 Strict Target Isolation Protocol
The dataset provides two degradation state indicators:
- $kMc$: Compressor degradation coefficient (decay state, domain $[0.95, 1.00]$, grid step 0.001, 51 levels)
- $kMt$: Turbine degradation coefficient (decay state, domain $[0.975, 1.00]$, grid step 0.001, 26 levels)

```text
+-----------------------------------------------------------+
| Full Measurement Record (Raw Sensors + Degradation State)  |
| 11,934 samples = 9 speeds * 51 kMc levels * 26 kMt levels |
+-----------------------------+-----------------------------+
                              |
              +---------------+---------------+
              |                               |
              v                               v
    [ Sensor Features X ]           [ Ground Truth Targets y ]
    (16 channels: lp, v, GTT,       (kMc, kMt coefficients)
     GTn, GGn, Ts, Tp, T48, T1,               |
     T2, P48, P1, P2, Pexh, TIC, mf)          |
              |                               |
              v                               |
    +-------------------+                     |
    | Clustering Pipeline|                    |
    | (Unsupervised)    |                     |
    +---------+---------+                     |
              |                               |
              v                               v
    [ Cluster Assignments C ] -----> [ Post-Hoc Analysis & Validation ]
                                     (Distributions, Hypothesis Tests,
                                      Thermodynamic Profiling)
```

**Guardrail Rules:**
1. Neither $kMc$ nor $kMt$ will ever enter any scaler, transformer, dimensionality reduction step, or clustering model.
2. In the source code, sensor features $\mathbf{X}$ and targets $\mathbf{y}$ are partitioned immediately at data ingestion inside `DatasetContainer`.
3. Post-hoc evaluation assesses whether cluster assignments $C_i$ exhibit statistically significant shifts in $kMc$ and $kMt$ via non-parametric tests.

### 2.3 Feature Representations for Experimental Evaluation
Phase 2 established 5 controlled feature representations to test competing clustering hypotheses in Phase 3:
1. **`R1_ALL_VALID_TELEMETRY` (Baseline):** 13 valid sensors including commanded speed and lever position (`lp`, `v`, `GTT`, `GTn`, `GGn`, `Ts`, `T48`, `T2`, `P48`, `P2`, `Pexh`, `TIC`, `mf`), standard scaled.
2. **`R2_WITHOUT_OPERATING_DEMAND`:** 11 telemetry features excluding commanded setpoints `lp` and `v`, standard scaled.
3. **`R3_REDUCED_CORRELATION`:** 9 pruned telemetry features across distinct subsystems (|r| < 0.985), standard scaled.
4. **`R4_ROBUST_SCALED_TELEMETRY`:** 11 telemetry features transformed via RobustScaler (median centering, IQR scaling).
5. **`R5_WITHIN_SPEED_NORMALIZED` (Degradation Hypothesis Candidate):** 11 telemetry features normalized conditionally within each discrete operating speed regime:
   $$z_{ij} = \frac{x_{ij} - \mu_j(v_i)}{\sigma_j(v_i)}$$
   This decouples the dominant operating speed variance (which accounts for 99.33% of raw variance) to evaluate whether unsupervised clustering can isolate subtle component degradation signatures ($kMc$, $kMt$).

### 2.4 Layered Analytical Separation
Every reported observation must be clearly cataloged under one of four distinct layers:
1. **Mathematical / Algorithmic Finding:** (e.g., "K-Means with $k=4$ achieved a silhouette score of 0.58 on standardized features").
2. **Statistical Relationship:** (e.g., "Kruskal-Wallis test rejected the null hypothesis of equal median $kMc$ across clusters with $p < 10^{-5}$, $\eta^2 = 0.22$").
3. **Engineering Interpretation:** (e.g., "Cluster 1 corresponds to high-speed cruise where turbine inlet temperature $T_4$ exceeds 1100 K; lower $kMt$ values within this cluster indicate degradation-induced thermal stress").
4. **Methodological Caveat / Limitation:** (e.g., "Synthetic steady-state simulation data does not account for sea-state dynamic transients or sensor drift over time").

---

## 3. Evaluation Framework

### 3.1 Intrinsic Unsupervised Metrics (Internal Quality)
These metrics require no ground truth and assess geometric separation and compactness:
- **Silhouette Coefficient ($s$):** Measures cohesion relative to separation (range $[-1, 1]$).
- **Davies-Bouldin Index ($DB$):** Ratio of within-cluster scatter to between-cluster separation (lower is superior).
- **Calinski-Harabasz Index ($CH$):** Variance ratio criterion (higher is superior).

### 3.2 Stability & Sensitivity Analysis
- Assessment of cluster stability across varied random initialization seeds.
- Subsampling perturbation (bootstrap cross-validation) to determine Jaccard similarity of cluster memberships across iterations.

### 3.3 Post-Hoc Physical & Statistical Validation
- **Visual Distributions:** Kernel Density Estimates (KDE) and boxplots of $kMc$ and $kMt$ conditioned on cluster index.
- **Hypothesis Testing:**
  - One-way ANOVA or Kruskal-Wallis $H$-test across clusters for continuous decay coefficients.
  - Pairwise Mann-Whitney $U$ tests with Benjamini-Hochberg FDR correction.
  - Physical balance check across operating variables (e.g., Lever position, Ship speed) to detect confounding.

---

## 4. Reproducibility Standards

1. **Global Seed Control:** A centralized deterministic seed utility (`set_all_seeds(seed=42)`) will govern all stochastic operations (NumPy, Python random, scikit-learn estimators).
2. **Declarative Configuration:** All hyperparameters, feature sets, and filepaths will reside in declarative YAML/dataclass configurations.
3. **Traceable Logs:** Every execution will append its parameter set, commit hash, date, and metrics to `EXPERIMENT_LOG.md`.
