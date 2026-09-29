# Final Scientific Model Validation & Candidate Selection Report

**Project Title:** Unsupervised Discovery of Operating and Performance Degradation Profiles in Naval Gas Turbine Propulsion Systems  
**Phase:** Phase 4 — Scientific Validation and Final Model Selection  
**Evaluation Date:** 2026-09-29  
**Execution Environment:** Python 3.12 (win32), Scikit-Learn 1.9.1, SciPy 1.15.2, Joblib 1.6.0  
**Dataset Reference:** UCI Machine Learning Repository #316 (Naval Propulsion Plants, N=11,934)  

---

## 1. Project Research Question

> **Primary Scientific Research Question:**  
> *Can unsupervised machine learning discover meaningful operating-condition and performance-degradation-related profiles in a simulated naval gas turbine propulsion system when the dominant commanded operating condition is controlled, without providing degradation labels to the clustering model?*

This report concludes the formal experimental evaluation of the two strongest clustering candidates identified in Phase 3:
- **Candidate A:** `KMeans(n_clusters=2, random_state=42)` on Representation `R5_WITHIN_SPEED_NORMALIZED`
- **Candidate B:** `KMeans(n_clusters=3, random_state=42)` on Representation `R5_WITHIN_SPEED_NORMALIZED`

---

## 2. Experimental Design & Anti-Leakage Protocol

### Zero-Leakage Invariant
In strict compliance with **Rule 1**, the component degradation indicators ($kMc$: compressor decay state coefficient, $kMt$: turbine decay state coefficient) were **completely quarantined** during all feature screening, within-speed transformation, and clustering steps. 
- Neither $kMc$ nor $kMt$ was ever included in any feature matrix, nor used to tune hyperparameters or choose cluster counts.
- They were used **strictly post-hoc** as external ground-truth benchmarks to test whether the unsupervised partitions discovered physically meaningful degradation phenomena.

### Preprocessing & Representation R5
As established in Phase 2, commanded ship speed $v$ explains 99.33% of raw sensor variance, masking subtle degradation signals. Representation `R5_WITHIN_SPEED_NORMALIZED` applies conditional within-speed z-score normalization:
$$z_{ij} = \frac{x_{ij} - \mu_j(v_i)}{\sigma_j(v_i)}$$
across the 11 clustering-eligible telemetry channels: `('GTT', 'GTn', 'GGn', 'Ts', 'T48', 'T2', 'P48', 'P2', 'Pexh', 'TIC', 'mf')`.

---

## 3. Candidate A (k=2) Experimental Results

Candidate A partitions the 11,934 observations into 2 balanced clusters:
- **Cluster 0:** $n = 5,939$ (49.77%)
- **Cluster 1:** $n = 5,995$ (50.23%)

### Intrinsic & Regime Independence Metrics
- **Silhouette Coefficient:** $0.2813$ (highest intrinsic separation among all representations)
- **Davies-Bouldin Index:** $1.3917$
- **Calinski-Harabasz Index:** $5543.4$
- **Speed Recovery ARI ($v$):** $0.0002$ (complete decoupling from operating speed)
- **Speed Recovery NMI ($v$):** $0.0006$

### Post-Hoc Degradation Profiling
- **Compressor Decay ($kMc$):**
  - $\eta^2 = 0.4459$ (Large effect size)
  - Kruskal-Wallis $H = 5321.4, p < 10^{-100}$
  - Cluster 0: Mean $= 0.9849 \pm 0.0108$, Median $= 0.9860$, 95% Bootstrap CI $= [0.9846, 0.9851]$
  - Cluster 1: Mean $= 0.9652 \pm 0.0111$, Median $= 0.9640$, 95% Bootstrap CI $= [0.9649, 0.9655]$
- **Turbine Decay ($kMt$):**
  - $\eta^2 = 0.0131$ (Negligible effect size)
  - Cluster 0: Mean $= 0.9884 \pm 0.0075$, Median $= 0.9890$
  - Cluster 1: Mean $= 0.9866 \pm 0.0074$, Median $= 0.9860$

*Finding:* Candidate A acts as a dedicated, binary **compressor health discriminator**, separating healthy compressor states ($kMc \approx 0.985$) from degraded compressor states ($kMc \approx 0.965$) while remaining largely agnostic to turbine decay.

---

## 4. Candidate B (k=3) Experimental Results

Candidate B partitions the dataset into 3 well-populated clusters:
- **Cluster 0:** $n = 3,379$ (28.31%)
- **Cluster 1:** $n = 4,125$ (34.57%)
- **Cluster 2:** $n = 4,430$ (37.12%)

### Intrinsic & Regime Independence Metrics
- **Silhouette Coefficient:** $0.2593$
- **Davies-Bouldin Index:** $1.2918$
- **Calinski-Harabasz Index:** $4889.7$
- **Speed Recovery ARI ($v$):** $0.0064$ (near-zero operating speed coupling)
- **Speed Recovery NMI ($v$):** $0.0103$

### Post-Hoc Degradation Profiling
- **Compressor Decay ($kMc$):**
  - $\eta^2 = 0.5109$ (Large effect size)
  - Kruskal-Wallis $H = 6097.4, p < 10^{-100}$
  - Cluster 0: Mean $= 0.9837 \pm 0.0110$, Median $= 0.9850$
  - Cluster 1: Mean $= 0.9826 \pm 0.0116$, Median $= 0.9840$
  - Cluster 2: Mean $= 0.9613 \pm 0.0083$, Median $= 0.9600$
- **Turbine Decay ($kMt$):**
  - $\eta^2 = 0.3007$ (Large effect size)
  - Kruskal-Wallis $H = 3588.4, p < 10^{-100}$
  - Cluster 0: Mean $= 0.9816 \pm 0.0055$, Median $= 0.9810$ (Degraded turbine)
  - Cluster 1: Mean $= 0.9920 \pm 0.0060$, Median $= 0.9930$ (Nominal turbine)
  - Cluster 2: Mean $= 0.9877 \pm 0.0070$, Median $= 0.9880$ (Intermediate turbine)

*Finding:* Candidate B resolves both compressor AND turbine degradation, distinguishing three distinct thermodynamic profiles:
1. **Cluster 1 (Nominal Baseline):** High compressor health ($kMc \approx 0.983$) + High turbine health ($kMt \approx 0.992$)
2. **Cluster 0 (Degraded Turbine Profile):** High compressor health ($kMc \approx 0.984$) + Degraded turbine ($kMt \approx 0.982$)
3. **Cluster 2 (Degraded Compressor Profile):** Degraded compressor ($kMc \approx 0.961$) + Intermediate turbine ($kMt \approx 0.988$)

---

## 5. Statistical Validation: Pairwise Tests & Effect Size Analysis

To avoid misinterpreting statistical significance purely due to large sample size ($N=11,934$), every pairwise cluster comparison was evaluated with:
- Two-sided Mann-Whitney $U$ test
- Benjamini-Hochberg (FDR) multiple comparison adjustment
- Cliff's delta ($d$) non-parametric effect size
- Rank-biserial correlation ($r_{rb}$)
- Bootstrap 95% confidence intervals for median difference ($\Delta \text{Median}$)

### Pairwise Comparison Table

| Candidate | Target | Comparison | Raw $p$-value | Adjusted $p$-value (FDR) | Cliff's Delta ($d$) | Interpretation | Median Diff (95% CI) |
|---|---|---|---|---|---|---|---|
| **Cand A ($k=2$)** | $kMc$ | Cluster 0 vs 1 | $0.0$ | $0.0$ | **+0.7709** | **Large** | $+0.022$ $[+0.022, +0.023]$ |
| **Cand A ($k=2$)** | $kMt$ | Cluster 0 vs 1 | $6.69 \times 10^{-36}$ | $6.69 \times 10^{-36}$ | **+0.1321** | **Negligible** | $+0.003$ $[+0.002, +0.003]$ |
| **Cand B ($k=3$)** | $kMc$ | Cluster 0 vs 1 | $2.18 \times 10^{-4}$ | $2.18 \times 10^{-4}$ | **+0.0495** | **Negligible** | $+0.001$ $[0.000, +0.002]$ |
| **Cand B ($k=3$)** | $kMc$ | Cluster 0 vs 2 | $0.0$ | $0.0$ | **+0.8689** | **Large** | $+0.025$ $[+0.024, +0.025]$ |
| **Cand B ($k=3$)** | $kMc$ | Cluster 1 vs 2 | $0.0$ | $0.0$ | **+0.8406** | **Large** | $+0.024$ $[+0.022, +0.024]$ |
| **Cand B ($k=3$)** | $kMt$ | Cluster 0 vs 1 | $0.0$ | $0.0$ | **-0.7673** | **Large** | $-0.012$ $[-0.013, -0.012]$ |
| **Cand B ($k=3$)** | $kMt$ | Cluster 0 vs 2 | $0.0$ | $0.0$ | **-0.5020** | **Large** | $-0.007$ $[-0.008, -0.007]$ |
| **Cand B ($k=3$)** | $kMt$ | Cluster 1 vs 2 | $4.86 \times 10^{-179}$ | $4.86 \times 10^{-179}$ | **+0.3561** | **Medium** | $+0.005$ $[+0.005, +0.005]$ |

### Statistical Insights
1. **Critical Role of Effect Size:** In Candidate A, $kMt$ has an astronomically small $p$-value ($6.69 \times 10^{-36}$) solely due to the large sample size, yet its Cliff's delta is **0.1321 (Negligible)**. Without effect size analysis, one might mistakenly claim Candidate A detects turbine decay. The effect size definitively refutes that claim.
2. **Selective Dissociation in Candidate B:** In Candidate B, Cluster 0 vs Cluster 1 shows a **negligible difference in compressor decay** ($d = 0.0495$), but a **massive difference in turbine decay** ($d = -0.7673$). This demonstrates that Candidate B successfully decouples turbine decay from compressor decay.

---

## 6. Bootstrap Stability Validation ($B=100$)

Cluster stability was evaluated over 100 bootstrap repetitions with replacement ($N=11,934$). For each bootstrap sample, K-Means was fit and projected onto the full original dataset to evaluate Adjusted Rand Index (ARI) against the reference solution.

| Stability Metric | Candidate A ($k=2$) | Candidate B ($k=3$) |
|---|---|---|
| **Mean Bootstrap ARI** | **0.9844** | 0.9434 |
| **Median Bootstrap ARI** | **0.9840** | 0.9679 |
| **Standard Deviation** | **0.0082** | 0.0578 |
| **95% Confidence Interval** | **[0.9699, 0.9983]** | [0.7923, 0.9904] |
| **Minimum ARI Observed** | **0.9622** | 0.7390 |
| **Maximum ARI Observed** | **0.9990** | 0.9926 |
| **Stability Classification** | **Highly Deterministic** | **Stable with Minor Boundary Sensitivity** |

![Bootstrap Stability Distribution](file:///c:/Users/Okul/OneDrive/Belgeler/naval-propulsion-clustering/reports/figures/phase4/bootstrap_stability_distribution.png)

*Limitations of Bootstrap Stability:*  
Bootstrap resampling draws samples with replacement, creating repeated instances that slightly inflate local point density. In continuous factorial grids without empty margins, bootstrap variance primarily reflects sensitivity at the decision boundaries rather than multimodal instability. Candidate A demonstrates near-immunity to resampling perturbations.

---

## 7. Degradation Grid Coherence Analysis ($kMc \times kMt$)

The dataset comprises an exact factorial grid of 51 $kMc$ states $\times$ 26 $kMt$ states ($1,326$ unique cells), each evaluated across 9 ship speeds.

### Grid Consistency Metrics
- **Candidate A ($k=2$):** Mean speed consistency across all 1,326 cells $= 86.24\%$ (median $= 88.89\%$).
- **Candidate B ($k=3$):** Mean speed consistency across all 1,326 cells $= 82.17\%$ (median $= 88.89\%$).

![Degradation Grid k=2](file:///c:/Users/Okul/OneDrive/Belgeler/naval-propulsion-clustering/reports/figures/phase4/degradation_grid_k2.png)
![Degradation Grid k=3](file:///c:/Users/Okul/OneDrive/Belgeler/naval-propulsion-clustering/reports/figures/phase4/degradation_grid_k3.png)

### Spatial Coherence Findings
- **Candidate A:** Partitions the $kMc \times kMt$ plane cleanly into two vertical/diagonal halves: low $kMc$ ($kMc < 0.975$) vs high $kMc$ ($kMc \ge 0.975$). The boundary is spatially contiguous, confirming that the cluster assignments represent coherent thermodynamic regimes rather than noisy or scattered artifacts.
- **Candidate B:** Partitions the 2D plane into three distinct contiguous zones:
  - Low $kMc$ across all $kMt$ (Cluster 2)
  - High $kMc$ with low $kMt$ (Cluster 0)
  - High $kMc$ with high $kMt$ (Cluster 1)
- *Non-causality warning:* These maps demonstrate spatial association in sensor-derived representation space; they do not imply physical causality or fault progression trajectories.

---

## 8. Operating-Speed Invariance Analysis

To verify that the discovered profiles are not artifacts of specific operating speeds, cluster proportions were evaluated across each of the 9 commanded speeds ($v = 3 \dots 27$ knots).

### Speed Proportion Breakdown

| Commanded Speed ($v$) | Candidate A: Clust 0 | Candidate A: Clust 1 | Candidate B: Clust 0 | Candidate B: Clust 1 | Candidate B: Clust 2 |
|---|---|---|---|---|---|
| **3 knots** | 52.19% | 47.81% | 37.33% | 40.35% | 22.32% |
| **6 knots** | 52.19% | 47.81% | 29.71% | 47.74% | 22.55% |
| **9 knots** | 47.81% | 52.19% | 28.51% | 29.56% | 41.93% |
| **12 knots** | 51.73% | 48.27% | 27.45% | 33.79% | 38.76% |
| **15 knots** | 47.36% | 52.64% | 29.41% | 30.24% | 40.35% |
| **18 knots** | 46.91% | 53.09% | 29.79% | 28.36% | 41.86% |
| **21 knots** | 51.21% | 48.79% | 22.25% | 35.90% | 41.86% |
| **24 knots** | 50.53% | 49.47% | 23.83% | 33.64% | 42.53% |
| **27 knots** | 47.96% | 52.04% | 26.55% | 31.52% | 41.93% |
| **Mean $\pm$ Std** | **$49.77\% \pm 2.22\%$** | **$50.23\% \pm 2.22\%$** | $28.31\% \pm 4.29\%$ | $34.57\% \pm 6.14\%$ | $37.12\% \pm 8.40\%$ |

![Speed Invariance k=2](file:///c:/Users/Okul/OneDrive/Belgeler/naval-propulsion-clustering/reports/figures/phase4/cluster_distribution_by_speed_k2.png)
![Speed Invariance k=3](file:///c:/Users/Okul/OneDrive/Belgeler/naval-propulsion-clustering/reports/figures/phase4/cluster_distribution_by_speed_k3.png)

### Invariance Summary
- **Candidate A:** Cramér's $V = 0.0418$ (Negligible association with speed). Across all 9 speeds, cluster proportions stay tightly clustered within $46.9\% - 52.2\%$. Discovered profiles are genuinely speed-invariant.
- **Candidate B:** Cramér's $V = 0.1273$ (Small association). At low speeds ($3, 6$ kts), the plant load is minimal, dampening compressor degradation symptoms (Cluster 2 proportion drops to 22.3%), whereas at intermediate-to-high speeds ($9 \dots 27$ kts), proportions stabilize near $42\%$.

---

## 9. Standardized Telemetry Profile Robustness

Standardized telemetry deviations (z-scores relative to operating speed baseline) were computed along with 95% bootstrap confidence intervals for cluster means ($B=500$).

![Telemetry Profiles Comparison](file:///c:/Users/Okul/OneDrive/Belgeler/naval-propulsion-clustering/reports/figures/phase4/telemetry_profiles_comparison.png)

### Physical Telemetry Associations (Non-Causal Language)
- **Candidate A:**
  - **Cluster 0 (Compressor Nominal Profile):** Characterized by below-baseline temperatures ($T_2: -0.843 \pm 0.013$, $T_{48}: -0.767 \pm 0.016$) and below-baseline fuel flow ($m_f: -0.713 \pm 0.017$). Characterized by above-baseline exhaust pressure ($P_{exh}: +0.626 \pm 0.021$).
  - **Cluster 1 (Compressor Degraded Profile):** Characterized by above-baseline temperatures ($T_2: +0.835 \pm 0.015$, $T_{48}: +0.760 \pm 0.017$) and above-baseline fuel flow ($m_f: +0.706 \pm 0.018$).
  - *Thermodynamic Consistency:* When compressor efficiency degrades, more fuel is demanded to sustain commanded shaft torque, elevating turbine inlet/outlet temperatures. All 95% CIs exclude 0, demonstrating robustness across resampling.
- **Candidate B:**
  - **Cluster 1 (Nominal Baseline):** Exhibits lowest fuel flow ($m_f: -1.063 \pm 0.014$), lowest $T_{48}$ ($-1.046 \pm 0.015$), and lowest turbine inlet temperature control valve opening ($TIC: -0.936 \pm 0.019$).
  - **Cluster 0 (Degraded Turbine Profile):** Exhibits elevated high-pressure turbine exit pressure ($P_{48}: +0.869 \pm 0.023$) and compressor outlet pressure ($P_2: +0.966 \pm 0.021$), accompanied by lower generator speed ($GT_n: -0.940 \pm 0.026$) and gas generator speed ($GG_n: -0.934 \pm 0.021$).
  - **Cluster 2 (Degraded Compressor Profile):** Characterized by pronounced elevations in $T_2$ ($+0.962 \pm 0.017$), $GG_n$ ($+0.891 \pm 0.017$), and $T_{48}$ ($+0.778 \pm 0.021$).

---

## 10. Formal Candidate Comparison Table

| Evaluation Criterion | Candidate A (`KMeans(k=2)`) | Candidate B (`KMeans(k=3)`) | Scientific Assessment |
|---|---|---|---|
| **1. Intrinsic Separation** | **Silhouette = 0.2813**, CH = 5543.4 | Silhouette = 0.2593, CH = 4889.7 | Candidate A shows superior cluster cohesion and separation. |
| **2. Speed Independence** | **Speed ARI = 0.0002**, Cramér's V = 0.0418 | Speed ARI = 0.0064, Cramér's V = 0.1273 | Candidate A is exceptionally decoupled from speed setpoints. |
| **3. Cluster Stability** | **Bootstrap ARI = 0.9844** (95% CI: 0.970–0.998) | Bootstrap ARI = 0.9434 (95% CI: 0.792–0.990) | Candidate A is exceptionally stable and boundary-robust. |
| **4. Compressor Decay ($kMc$)** | $\eta^2 = 0.4459$, Cliff's $d = 0.7709$ (Large) | **$\eta^2 = 0.5109$**, Cliff's $d = 0.8689$ (Large) | Candidate B captures slightly more $kMc$ variance. |
| **5. Turbine Decay ($kMt$)** | $\eta^2 = 0.0131$, Cliff's $d = 0.1321$ (Negligible) | **$\eta^2 = 0.3007$**, Cliff's $d = -0.7673$ (Large) | **Candidate B decisively discovers turbine decay**; Cand A misses it. |
| **6. Pairwise Separation** | Single pair; large for $kMc$, negligible for $kMt$ | 3 pairs; cleanly dissociates $kMc$ and $kMt$ | Candidate B provides component-resolved separation. |
| **7. Degradation-Grid Coherence**| Clean vertical half-plane (consistency: 86.2%) | 3 contiguous geometric zones (consistency: 82.2%) | Both exhibit coherent non-random spatial structure. |
| **8. Speed Invariance** | **Proportion Std = 2.22%** across speeds | Proportion Std = 6.28% across speeds | Candidate A is nearly perfectly invariant across all 9 speeds. |
| **9. Interpretability** | Binary: Nominal vs Degraded Compressor | Tripartite: Nominal, Turbine-Degraded, Compressor-Degraded | Candidate B offers greater physical granularity. |
| **10. Simplicity & Parsimony**| **Parsimonious (Occam's Razor)** | Complex (lower silhouette, 3 clusters) | Candidate A minimizes risk of boundary partitioning artifacts. |

---

## 11. Final Model Selection & Scientific Verdict

### Selected Outcome: **Option C — Hierarchical Dual-Model Scientific Retention**
Neither model completely renders the other obsolete; they serve two distinct, rigorous academic purposes:

1. **Primary Scientific Model:** **Candidate A (`KMeans(n_clusters=2, random_state=42)` on R5)**
   - **Role:** Authoritative baseline model for binary degradation discovery.
   - **Scientific Justification:** Maximizes intrinsic separation (Silhouette 0.2813), exhibits near-perfect operating speed invariance (speed ARI = 0.0002, speed proportion standard deviation = 2.2%), demonstrates 98.44% bootstrap stability, and unambiguously isolates compressor health ($kMc$ Cliff's delta = 0.7709) without over-partitioning a continuous space.
2. **Secondary Diagnostic Model:** **Candidate B (`KMeans(n_clusters=3, random_state=42)` on R5)**
   - **Role:** Specialized multi-component degradation model.
   - **Scientific Justification:** For inquiries specifically investigating whether unsupervised learning can differentiate between multiple failing components, Candidate B successfully isolates turbine decay ($\eta^2 = 0.3007$, Cliff's delta = -0.7673) while maintaining solid stability (Bootstrap ARI = 0.9434).

Both models and the shared `OperatingRegimeNormalizer` have been serialized into `models/final/` with complete metadata documented in `models/final/model_manifest.json`.

---

## 12. Academic Limitations

1. **Simulation-Based Telemetry:** The dataset is generated from a numerical numerical simulator of a CODAG naval propulsion plant. It lacks real-world sensor noise, sensor drift, missing data, and telemetry corruption.
2. **Steady-State Nature:** All 11,934 observations represent static thermodynamic equilibrium at fixed discrete speeds and decay coefficients. Dynamic throttle transients, sea-state disturbances, and ambient temperature cycles are absent.
3. **Artificial Factorial Grid:** The uniform factorial grid ($9 \times 51 \times 26$) does not reflect realistic operational lifecycles, where components degrade gradually and continuously over thousands of operating hours.
4. **Reference Indicators:** $kMc$ and $kMt$ are simulated model parameters, not measurable physical quantities in operational vessels.
5. **No Causality:** Clustering discovers geometric partitions in high-dimensional sensor residual space that correlate strongly with degradation states. It does not establish causal direction.

---

## 13. Legitimate Claims Supported by Evidence vs Prohibited Claims

### Claims Fully Supported by Experimental Evidence:
- Within-speed conditional normalization successfully strips dominant operating speed variance (speed ARI drops from 0.8769 in R1 to 0.0002 in R5).
- Unsupervised K-Means ($k=2$) discovers a partition that correlates strongly with compressor decay ($kMc$ $\eta^2 = 0.4459$, Cliff's delta = 0.7709) with 98.44% bootstrap stability across resampling.
- Unsupervised K-Means ($k=3$) discovers a three-way partition that differentiates high turbine decay ($kMt \approx 0.982$) from high compressor decay ($kMc \approx 0.961$) and nominal baseline health ($kMt \approx 0.992, kMc \approx 0.983$).
- Discovered cluster assignments occupy spatially contiguous zones in the 2D degradation grid and show consistent membership across 9 operating speeds.

### Claims That Must NEVER Be Made:
- **NO claim of real-time marine deployment:** The models were not validated on sea trials or physical ships.
- **NO claim of automatic fault diagnosis:** The clusters are unlabelled statistical partitions; clinical or operational diagnosis requires domain-expert thresholding and causal verification.
- **NO claim of remaining useful life (RUL) or failure prediction:** The data contains no time dimension, no temporal sequence, and no time-to-failure records.
- **NO claim of turbine decay detection for Candidate A:** Despite $p = 6.69 \times 10^{-36}$, the effect size ($d = 0.1321$) is negligible.
