# Experiment Log & Registry

**Project:** Naval Propulsion Clustering  
**Objective:** Maintain an immutable, reproducible record of all exploratory and benchmark clustering experiments.

---

## 1. Registry Schema

Every experiment must record:
- **Experiment ID (`EXP-XXX`):** Unique sequential identifier.
- **Date & Timestamp:** Execution date (ISO 8601).
- **Hypothesis / Objective:** What research question or behavior is being tested.
- **Data & Feature Config:** Subset of features used, scaling method, dimensionality reduction applied.
- **Model & Hyperparameters:** Algorithm name, distance metric, cluster count $k$, initialization, etc.
- **Random Seed:** Specific deterministic seed used.
- **Intrinsic Evaluation Metrics:** Silhouette Score ($s$), Davies-Bouldin ($DB$), Calinski-Harabasz ($CH$).
- **Post-Hoc Degradation Signals:** $kMc$ & $kMt$ Kruskal-Wallis $p$-value / effect size across clusters.
- **Artifact Path:** Relative path to serialized model and summary plots in `experiments/outputs/`.
- **Conclusions / Next Actions:** Brief takeaway based on data.

---

## 2. Experiment Records

| Exp ID | Date | Model / Config | Features & Scaler | Intrinsic Metrics ($s$ / $DB$) | Degradation Correlation ($p_{kMc}$ / $p_{kMt}$) | Status | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **AUDIT-01** | 2026-09-29 | Phase 1 Data Ingestion & Quality Audit | All 18 Canonical Channels (Unscaled) | N/A (Unsupervised Ingestion Phase) | N/A (Targets quarantined: `kMc`, `kMt`) | **Completed** | Full factorial verified: 9 speeds x 51 kMc x 26 kMt = 11,934 rows. T1 & P1 constant. Ts == Tp duplicate. |
| **AUDIT-02** | 2026-09-29 | Phase 2 Preprocessing & Feature Engineering | Candidate Reps R1 through R5 | N/A (Preprocessing Stage) | N/A (Targets quarantined: `kMc`, `kMt`) | **Completed** | Screening confirmed mandatory removal of T1, P1, Tp. Speed v explains 99.33% of variance; PC1 explains 97.41%. |
| **EXP-001** | 2026-09-29 | K-Means Baseline ($k=9$) | R1 All Valid (StandardScaler) | $s=0.7816$ / $DB=0.4071$ | N/A (Speed recovery focus) | **Completed** | Discovers operating regimes: ARI vs Speed = 0.8769, NMI = 0.9315. |
| **EXP-002** | 2026-09-29 | K-Means Speed Excluded ($k=9$) | R2 Excl Speed (StandardScaler) | $s=0.7699$ / $DB=0.4285$ | N/A (Coupled physics focus) | **Completed** | Coupled physics reconstructs speed setpoints (ARI = 0.8440). |
| **EXP-003** | 2026-09-29 | K-Means Primary Degradation ($k=2$) | R5 Within-Speed Normalized | $s=0.2813$ / $DB=1.3917$ | $p_{kMc} < 10^{-100}$ ($\eta^2=0.446$) | **Completed** | Successfully decouples speed (ARI=0.0002) and discovers compressor decay. |
| **EXP-004** | 2026-09-29 | K-Means Joint Degradation ($k=3$) | R5 Within-Speed Normalized | $s=0.2593$ / $DB=1.2918$ | $p_{kMc} < 10^{-100}$, $p_{kMt} < 10^{-100}$ | **Completed** | Discovers both compressor decay ($\eta^2=0.511$) and turbine decay ($\eta^2=0.301$). |
| **EXP-005** | 2026-09-29 | Hierarchical Ward ($k=2$) | R5 Within-Speed Normalized | $s=0.2646$ / $DB=1.4420$ | Matches K-Means ($ARI = 0.962$) | **Completed** | Independent algorithm family confirms K-Means degradation partition. |

---

## 3. Experiment Execution Protocol
1. Create a declarative config YAML in `experiments/configs/` specifying all hyperparameters.
2. Run via the centralized experiment runner (`python -m naval_propulsion.clustering.runner --config experiments/configs/exp_xxx.yaml`).
3. Outputs (metrics JSON, confusion/distribution plots, fitted model) are automatically written to `experiments/outputs/EXP-XXX/`.
4. Update this markdown table with summary results.
