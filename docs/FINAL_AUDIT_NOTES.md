# Final Academic Audit Notes & Consistency Reconciliation

**Project:** Naval Propulsion Clustering  
**Date:** 2026-09-29  
**Purpose:** Reconcile all numerical values, metrics, and descriptions across Phases 0–5 before authoring the final university report and presentation assets.

---

## 1. Provenance & Dataset Invariants
- **UCI Machine Learning Repository Dataset #316:** *Condition Based Maintenance of Naval Propulsion Plants* (Coraddu et al.).
- **Raw File Integrity:** `data/raw/data.txt` SHA-256 = `de0ea69da1efaab8b9655ffed828547d10dd68c1fb8c6e0163e6a988def393a6`.
- **Processed File Integrity:** `data/processed/naval_propulsion.csv` SHA-256 = `00e3c6127f0d8f88269c48865cb62a2c848579eb8e4b6e85d5f7e147ad22460a`.
- **Record Dimension:** Exactly 11,934 rows $\times$ 18 continuous numerical features. Zero missing values, zero duplicated records.
- **Factorial Structure:** $9 \text{ speeds } (3 \dots 27 \text{ kts}) \times 51 \text{ } kMc \text{ states } (0.950 \dots 1.000) \times 26 \text{ } kMt \text{ states } (0.975 \dots 1.000) = 11,934$.

---

## 2. Feature Screening & Invariants
- **Removed Channels (Mandatory):**
  - $T_1$ (Compressor inlet temperature): Constant at $288.0$ K ($\sigma = 0$).
  - $P_1$ (Compressor inlet pressure): Constant at $0.998$ bar ($\sigma = 0$).
  - $T_p$ (Port-side propeller torque): Identical to $T_s$ (Starboard-side torque) with $\max |T_s - T_p| = 0.0$ (exact duplicate).
- **Quarantined Targets:**
  - $kMc$ (Compressor decay state coefficient) and $kMt$ (Turbine decay state coefficient) quarantined in `DatasetContainer.targets`. Strictly zero-leakage during preprocessing, feature transformation, and clustering.
- **Clustering-Eligible Channels (11 features):**
  `('GTT', 'GTn', 'GGn', 'Ts', 'T48', 'T2', 'P48', 'P2', 'Pexh', 'TIC', 'mf')`.

---

## 3. Representation & Clustering Benchmarks
- **Operating Speed Dominance:**
  - One-way ANOVA: Commanded speed $v$ explains **$99.33\%$** of raw sensor variance.
  - PCA: PC1 explains **$97.41\%$** of total variance (1D steady-state plant load line).
  - Unconditioned clustering on R1 ($k=9$): Recovers speed setpoints with $\text{ARI} = 0.8769, \text{NMI} = 0.9315$.
  - Demands-excluded clustering on R2 ($k=9$): Recovers speed setpoints with $\text{ARI} = 0.8440, \text{NMI} = 0.9068$ due to coupled turbomachinery physics.
- **Within-Speed Normalization (R5):**
  - $z_{ij} = (x_{ij} - \mu_j(v_i)) / \sigma_j(v_i)$.
  - Decouples operating speed: $\text{ARI vs Speed} = 0.0002$ ($K=2$) and $0.0064$ ($K=3$).

---

## 4. Retained Model Metrics (Reconciled Source of Truth)

All values verified against [`models/final/model_manifest.json`](file:///models/final/model_manifest.json) and [`experiments/outputs/phase4/phase4_validation_results.json`](file:///experiments/outputs/phase4/phase4_validation_results.json):

| Metric | Candidate A (Primary, K=2) | Candidate B (Secondary, K=3) |
| :--- | :--- | :--- |
| **Cluster Counts** | Cluster 0: 5,939 (49.77%), Cluster 1: 5,995 (50.23%) | Cluster 0: 3,379 (28.31%), Cluster 1: 4,125 (34.57%), Cluster 2: 4,430 (37.12%) |
| **Silhouette Score** | **0.2813** | 0.2593 |
| **Davies-Bouldin Index** | 1.3917 | **1.2918** |
| **Calinski-Harabasz Index** | **5543.4** | 4889.7 |
| **Speed Recovery ARI ($v$)** | **0.0002** | 0.0064 |
| **Speed Recovery NMI ($v$)** | **0.0006** | 0.0103 |
| **Speed Proportion Std** | **2.22%** ($49.77\% \pm 2.22\%$) | 6.28% ($28.3\% \pm 4.3\%, 34.6\% \pm 6.1\%, 37.1\% \pm 8.4\%$) |
| **Cramér's V (Speed Contingency)** | **0.0418** (Negligible) | 0.1273 (Small) |
| **Bootstrap ARI Mean ($B=100$)** | **0.9844** | 0.9434 |
| **Bootstrap ARI 95% CI** | **[0.9699, 0.9983]** | [0.7923, 0.9904] |
| **Multi-Seed ARI Mean (10 seeds)** | **0.9994** | 0.9937 |
| **$kMc$ Post-Hoc $\eta^2$** | 0.4459 (Large) | **0.5109** (Large) |
| **$kMc$ Pairwise Cliff's Delta** | **+0.7709** (Large, Clust 0 vs 1) | Clust 0 vs 1: +0.0495 (Negligible)<br>Clust 0 vs 2: **+0.8689** (Large)<br>Clust 1 vs 2: **+0.8406** (Large) |
| **$kMt$ Post-Hoc $\eta^2$** | 0.0131 (Negligible) | **0.3007** (Large) |
| **$kMt$ Pairwise Cliff's Delta** | +0.1321 (Negligible, Clust 0 vs 1) | Clust 0 vs 1: **-0.7673** (Large)<br>Clust 0 vs 2: **-0.5020** (Large)<br>Clust 1 vs 2: **+0.3561** (Medium) |
| **Degradation Grid Speed Consistency** | Mean: 86.24%, Median: 88.89% | Mean: 82.17%, Median: 88.89% |

*Reconciliation Note:* Early Phase 3 exploratory ANOVA script estimated $kMt$ $\eta^2 = 0.0189$ prior to centering refinement. Phase 4 formal calculation verified exact sum of squares $\eta^2 = 0.0131$. The Cliff's delta of $+0.1321$ confirms that turbine decay under $K=2$ is negligible regardless.

---

## 5. Artifact & Code Verification
- Serialized artifacts in `models/final/`:
  - `operating_regime_normalizer.joblib`
  - `kmeans_primary_k2.joblib`
  - `kmeans_multicomponent_k3.joblib`
  - `model_manifest.json`
- Test Suite: 51/51 tests passing across 8 test modules.
- Streamlit application tested and verified on local Windows.
