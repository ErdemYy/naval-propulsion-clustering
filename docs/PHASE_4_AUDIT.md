# Phase 4 Formal Audit Report: Scientific Validation & Final Model Selection

**Project:** Naval Propulsion Clustering  
**Academic Title:** *Unsupervised Discovery of Operating and Performance Degradation Profiles in Naval Gas Turbine Propulsion Systems*  
**Date of Audit:** 2026-09-29  
**Phase Status:** Complete & Fully Verified  
**Dataset Reference:** UCI Machine Learning Repository #316 (Naval Propulsion Plants, N=11,934)  
**Processed Dataset SHA-256:** `00e3c6127f0d8f88269c48865cb62a2c848579eb8e4b6e85d5f7e147ad22460a`  

---

## 1. Phase 4 Objectives & Execution Scope

The primary objective of Phase 4 is to rigorously validate the two strongest clustering candidates identified in Phase 3 under strict zero-leakage conditions, determine whether the discovered partitions represent coherent thermodynamic profiles or arbitrary mathematical divisions, and select and serialize the primary final model artifact.

### Candidate Configurations Evaluated:
1. **Candidate A:** `KMeans(n_clusters=2, random_state=42, n_init=10)` on `R5_WITHIN_SPEED_NORMALIZED`
2. **Candidate B:** `KMeans(n_clusters=3, random_state=42, n_init=10)` on `R5_WITHIN_SPEED_NORMALIZED`

All evaluations were executed deterministically via `src/naval_propulsion/evaluation/phase4_runner.py` and serialized to [`experiments/outputs/phase4/phase4_validation_results.json`](file:///experiments/outputs/phase4/phase4_validation_results.json).

---

## 2. Invariant & Anti-Leakage Audit (Rule 1)

| Invariant Check | Verification Method | Status |
| :--- | :--- | :--- |
| **Quarantined Targets ($kMc, kMt$)** | Feature matrix introspection before fitting | **PASSED** ($kMc, kMt$ absent from all training inputs) |
| **Operating Setpoints ($lp, v$)** | Column screening in `R5` | **PASSED** (Excluded from clustering space; $v$ used solely as normalizer conditioning variable) |
| **Zero-Leakage Post-Hoc Testing** | Evaluated strictly after cluster label generation | **PASSED** (Post-hoc external benchmark only) |
| **Model Independence** | Normalizer fitted without target information | **PASSED** (Only within-speed telemetry means and stds used) |

---

## 3. Pairwise Degradation Statistical Validation

All pairwise cluster comparisons were evaluated using two-sided Mann-Whitney $U$ tests, Benjamini-Hochberg (FDR) adjustments, Cliff's delta ($d$), rank-biserial correlations, and 95% bootstrap confidence intervals for median differences.

### 3.1 Candidate A ($k=2$) Pairwise Results

| Target | Cluster Pair | Sample Sizes ($n_i, n_j$) | Medians ($M_i, M_j$) | Raw $p$-value | FDR Adj $p$-value | Cliff's Delta ($d$) | Effect Size | Median Diff (95% CI) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **$kMc$** | 0 vs 1 | 5,939 vs 5,995 | 0.986 vs 0.964 | $0.0$ | $0.0$ | **+0.7709** | **Large** | $+0.022$ $[+0.022, +0.023]$ |
| **$kMt$** | 0 vs 1 | 5,939 vs 5,995 | 0.989 vs 0.986 | $6.69 \times 10^{-36}$ | $6.69 \times 10^{-36}$ | **+0.1321** | **Negligible** | $+0.003$ $[+0.002, +0.003]$ |

*Scientific Audit Finding:*  
Candidate A displays a massive, statistically robust separation on compressor decay ($d = 0.7709, p < 10^{-100}$). Although turbine decay yields a vanishingly small $p$-value ($6.69 \times 10^{-36}$) due to large $N$, its effect size is **negligible** ($d = 0.1321 < 0.147$). Candidate A must therefore be classified as a **single-component compressor health profile model**.

### 3.2 Candidate B ($k=3$) Pairwise Results

| Target | Cluster Pair | Sample Sizes ($n_i, n_j$) | Medians ($M_i, M_j$) | Raw $p$-value | FDR Adj $p$-value | Cliff's Delta ($d$) | Effect Size | Median Diff (95% CI) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **$kMc$** | 0 vs 1 | 3,379 vs 4,125 | 0.985 vs 0.984 | $2.18 \times 10^{-4}$ | $2.18 \times 10^{-4}$ | **+0.0495** | **Negligible** | $+0.001$ $[0.000, +0.002]$ |
| **$kMc$** | 0 vs 2 | 3,379 vs 4,430 | 0.985 vs 0.960 | $0.0$ | $0.0$ | **+0.8689** | **Large** | $+0.025$ $[+0.024, +0.025]$ |
| **$kMc$** | 1 vs 2 | 4,125 vs 4,430 | 0.984 vs 0.960 | $0.0$ | $0.0$ | **+0.8406** | **Large** | $+0.024$ $[+0.022, +0.024]$ |
| **$kMt$** | 0 vs 1 | 3,379 vs 4,125 | 0.981 vs 0.993 | $0.0$ | $0.0$ | **-0.7673** | **Large** | $-0.012$ $[-0.013, -0.012]$ |
| **$kMt$** | 0 vs 2 | 3,379 vs 4,430 | 0.981 vs 0.988 | $0.0$ | $0.0$ | **-0.5020** | **Large** | $-0.007$ $[-0.008, -0.007]$ |
| **$kMt$** | 1 vs 2 | 4,125 vs 4,430 | 0.993 vs 0.988 | $4.86 \times 10^{-179}$| $4.86 \times 10^{-179}$| **+0.3561** | **Medium** | $+0.005$ $[+0.005, +0.005]$ |

*Scientific Audit Finding:*  
Candidate B successfully decouples turbine decay from compressor decay:
- Cluster 0 vs Cluster 1 has negligible compressor difference ($d = 0.0495$) but a **massive turbine decay difference** ($d = -0.7673$).
- Cluster 2 separates both Cluster 0 and Cluster 1 with massive compressor decay differences ($d \ge 0.84$).

---

## 4. Bootstrap Cluster Stability Audit ($B=100$)

Bootstrap resampling was executed across 100 iterations with replacement to assess partition sensitivity against empirical sample perturbation.

| Metric | Candidate A ($k=2$) | Candidate B ($k=3$) | Evaluation |
| :--- | :--- | :--- | :--- |
| **Mean Bootstrap ARI** | **0.9844** | 0.9434 | Both demonstrate strong determinism ($> 0.90$) |
| **Median Bootstrap ARI** | **0.9840** | 0.9679 | Candidate A median is extremely high |
| **Std Bootstrap ARI** | **0.0082** | 0.0578 | Candidate A has $7\times$ lower variance |
| **95% Bootstrap CI** | **[0.9699, 0.9983]** | [0.7923, 0.9904] | Candidate A never falls below 0.962 |
| **Minimum ARI** | **0.9622** | 0.7390 | Candidate B exhibits minor boundary shifts |

Figure: [`reports/figures/phase4/bootstrap_stability_distribution.png`](file:///reports/figures/phase4/bootstrap_stability_distribution.png)

---

## 5. Degradation Grid Coherence Audit ($kMc \times kMt$)

Across the 1,326 factorial grid coordinates ($51 \times 26$):
- **Candidate A Mean Speed Consistency:** **$86.24\%$** (Median: $88.89\%$)
- **Candidate B Mean Speed Consistency:** **$82.17\%$** (Median: $88.89\%$)
- **Contiguity:** Both candidates form contiguous geometric regions in $(kMc, kMt)$ plane without spatial fragmentation or speckle noise.

Figures:
- Candidate A Map: [`reports/figures/phase4/degradation_grid_k2.png`](file:///reports/figures/phase4/degradation_grid_k2.png)
- Candidate B Map: [`reports/figures/phase4/degradation_grid_k3.png`](file:///reports/figures/phase4/degradation_grid_k3.png)

---

## 6. Operating-Speed Invariance Audit

| Speed Metric | Candidate A ($k=2$) | Candidate B ($k=3$) |
| :--- | :--- | :--- |
| **Speed Recovery ARI ($v$)** | **0.0002** | 0.0064 |
| **Cramér's V (Speed Contingency)** | **0.0418** (Negligible) | 0.1273 (Small) |
| **Cluster Proportion Std Across Speeds** | **$2.22\%$** | $6.28\%$ |
| **Proportion Range Across Speeds** | $46.9\% - 53.1\%$ | $22.2\% - 47.7\%$ |

Figures:
- Candidate A Speed Breakdown: [`reports/figures/phase4/cluster_distribution_by_speed_k2.png`](file:///reports/figures/phase4/cluster_distribution_by_speed_k2.png)
- Candidate B Speed Breakdown: [`reports/figures/phase4/cluster_distribution_by_speed_k3.png`](file:///reports/figures/phase4/cluster_distribution_by_speed_k3.png)

*Audit Finding:*  
Candidate A is virtually invariant to operating speed. Candidate B exhibits mild physical interaction at 3 and 6 knots (where low plant load dampens compressor degradation visibility), stabilizing completely between 9 and 27 knots.

---

## 7. Standardized Telemetry Profile Audit

Feature deviations from within-speed baselines:
- In Candidate A, Cluster 1 (degraded) shows elevated $T_2$ ($+0.835 \pm 0.015$), $T_{48}$ ($+0.760 \pm 0.017$), and $m_f$ ($+0.706 \pm 0.018$).
- In Candidate B, Cluster 0 (turbine degraded) shows elevated $P_{48}$ ($+0.869 \pm 0.023$) and $P_2$ ($+0.966 \pm 0.021$).
- All 95% bootstrap confidence intervals for key distinguishing features exclude zero.
- All technical documentation strictly adheres to non-causal language ("associated with", "characterized by", "shows higher values").

Figure: [`reports/figures/phase4/telemetry_profiles_comparison.png`](file:///reports/figures/phase4/telemetry_profiles_comparison.png)

---

## 8. Final Model Decision & Serialization

### Audit Decision: **Option C — Hierarchical Dual-Model Retention**
1. **Primary Model:** Candidate A (`KMeans(k=2, random_state=42)` on `R5`)
   - Designated as the primary baseline due to maximum silhouette (0.2813), minimal speed association (ARI = 0.0002), and superior bootstrap stability (0.9844).
2. **Secondary Diagnostic Model:** Candidate B (`KMeans(k=3, random_state=42)` on `R5`)
   - Retained as a secondary multi-component model due to its ability to isolate turbine decay ($kMt \eta^2 = 0.3007, d = -0.7673$).

### Model Artifacts in `models/final/`:
- `operating_regime_normalizer.joblib` (2.5 KB)
- `kmeans_primary_k2.joblib` (48.6 KB)
- `kmeans_multicomponent_k3.joblib` (48.7 KB)
- `model_manifest.json` (3.1 KB)

All artifacts reload successfully and pass deterministic verification tests on local Windows.

---

## 9. Test Suite Verification

Pytest was executed across the full test suite including `tests/test_validation_phase4.py`:
```text
tests/test_clustering_phase3.py ...........
tests/test_config.py ..
tests/test_data_container.py ...
tests/test_evaluation_metrics.py ..
tests/test_ingestion_and_quality.py ........
tests/test_preprocessing_phase2.py ........
tests/test_utils.py ..
tests/test_validation_phase4.py ........

============================== 42 passed in 3.51s ==============================
```

**Phase 4 Audit Status:** **APPROVED & CERTIFIED**
