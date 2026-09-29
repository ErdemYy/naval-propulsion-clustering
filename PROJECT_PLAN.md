# Project Plan: Naval Propulsion Clustering

**Academic Title:** *Unsupervised Discovery of Operating and Performance Degradation Profiles in Naval Gas Turbine Propulsion Systems*

---

## 1. Project Objectives
1. Perform rigorous, reproducible unsupervised learning on multivariate gas turbine propulsion system data.
2. Characterize operating envelopes and assess whether subtle degradation profiles naturally group into distinct clusters without supervision.
3. Quantify post-hoc correlation between discovered clusters and true physical degradation parameters ($kMc$, $kMt$) without introducing data leakage into the training phase.
4. Deliver a robust, tested Python package alongside an interactive local Streamlit dashboard and academic documentation suitable for university defense.

---

## 2. Multi-Phase Roadmap

### Phase 0: Project Foundation & Architecture (Current Phase)
- [x] Establish directory hierarchy and package structure.
- [x] Configure build metadata (`pyproject.toml`), environment guidelines, and `.gitignore`.
- [x] Formulate core governance documents: `PROJECT_PLAN.md`, `METHODOLOGY.md`, `LIMITATIONS.md`, `EXPERIMENT_LOG.md`.
- [x] Formulate architectural blueprint in `docs/ARCHITECTURE.md`.
- [x] Build minimal configuration and utility primitives (deterministic seeding, structured logging).
- [ ] Review and lock architectural baseline before proceeding to ingestion.

### Phase 1: Dataset Acquisition & Exploratory Data Analysis (EDA) - COMPLETED
- [x] Ingest the raw Naval Propulsion Plants dataset into `data/raw/` with verifiable checksums and manifest.
- [x] Audit data types, missing values, zero-variance columns, and distribution ranges.
- [x] Inspect physical sensor properties (pressures, temperatures, shaft speeds, fuel flow rate).
- [x] Map out target degradation columns (`kMc`, `kMt`) and ensure strict boundary isolation.
- [x] Conduct correlation analysis, multicollinearity checks, and scale disparity profiling in `notebooks/01_dataset_exploration.ipynb`.
- [x] Generate publication-quality diagnostic figures in `reports/figures/phase1/`.
- [x] Produce formal data dictionary in `docs/DATA_DICTIONARY.md` and audit report in `docs/PHASE_1_AUDIT.md`.

### Phase 2: Preprocessing, Scaling & Dimensionality Exploration - COMPLETED
- [x] Implement scikit-learn compatible preprocessors: `ColumnFilterTransformer`, `TelemetryScaler`, `OperatingRegimeNormalizer`.
- [x] Feature screening: mandatory removal of zero-variance `T1`, `P1` and exact clone `Tp` documented in `feature_screening.csv`.
- [x] Scaler comparison across `StandardScaler`, `RobustScaler`, and `MinMaxScaler` documented in `scaler_comparison.json`.
- [x] Outlier investigation: classified 99% ordinary, 1% boundary extremes in `outlier_report.json`.
- [x] Operating-condition analysis: proved operating speed `v` explains 99.33% of sensor variance in `operating_regime_report.json`.
- [x] PCA analysis: proved PC1 explains 97.41% due to plant load coupling; PCA rejected as pre-clustering filter.
- [x] Formally registered 5 candidate representations (R1 to R5) in `representation_registry.json`.
- [x] Generated Phase 2 research notebook `02_preprocessing_experiments.ipynb` and formal audit in `docs/PHASE_2_AUDIT.md`.

### Phase 3: Unsupervised Model Development & Clustering Experiments - COMPLETED
- [x] Implement standardized model wrappers: `KMeansClusterer`, `AgglomerativeClustererWrapper`, `DBSCANClustererWrapper`, `GMMClustererWrapper`.
- [x] Experiment Group A-E: Evaluated K-Means sweeps ($k=2 \dots 12$) across R1, R2, R3, R4, R5.
- [x] Proved operating regime recovery in unconditioned telemetry: $k=9$ recovers ship speed with ARI $0.877$ (R1) and $0.844$ (R2 without speed setpoints).
- [x] Proved primary degradation discovery in R5 (Within-Speed Normalized): K-Means ($k=2$) discovers compressor degradation with $\eta^2 = 0.446$ ($p < 10^{-100}$); $k=3$ discovers both $kMc$ ($\eta^2 = 0.511$) and $kMt$ ($\eta^2 = 0.301$).
- [x] Multi-seed stability analysis: 10 random seeds confirmed mean pairwise ARI $\ge 0.994$.
- [x] Algorithm comparisons: Agglomerative Ward confirmed K-Means structure ($ARI = 0.962$); documented DBSCAN and GMM negative findings.
- [x] Generated 10 publication-quality diagnostic figures in `reports/figures/phase3/`.
- [x] Produced Phase 3 research notebook `03_clustering_experiments.ipynb` and audit in `docs/PHASE_3_AUDIT.md`.

### Phase 4: Scientific Validation & Final Model Selection (Complete)
- [x] Rigorous pairwise degradation validation using Mann-Whitney $U$ tests with Benjamini-Hochberg FDR adjustments.
- [x] Effect size analysis: Cliff's delta ($d$) and rank-biserial correlations across all cluster pairs.
- [x] Proved critical distinction: Candidate A turbine decay has $p = 6.69 \times 10^{-36}$ but negligible effect size ($d = 0.1321$), refuting turbine detection for $k=2$.
- [x] Proved selective multi-component discovery: Candidate B ($k=3$) decouples turbine decay ($kMt$ Cliff's $d = -0.7673, \eta^2 = 0.3007$) from compressor decay ($kMc$ Cliff's $d \ge 0.84, \eta^2 = 0.5109$).
- [x] Bootstrap stability validation ($B=100$ with replacement): Candidate A achieved Mean ARI = $0.9844$ (95% CI: $[0.9699, 0.9983]$); Candidate B achieved Mean ARI = $0.9434$ (95% CI: $[0.7923, 0.9904]$).
- [x] Degradation grid coherence: Verified spatial contiguity across $51 \times 26$ ($1,326$ cells) with $>82\%$ speed consistency.
- [x] Operating-speed invariance: Candidate A proportions strictly invariant across speeds ($49.77\% \pm 2.22\%$, Cramér's V = $0.0418$).
- [x] Robust standardized telemetry profiles with 95% bootstrap CIs confirming thermodynamic consistency (elevated $T_2, T_{48}, m_f$ under compressor degradation).
- [x] Model Selection Verdict: Option C (Dual-model hierarchy: Candidate A as Primary Baseline Model, Candidate B as Secondary Diagnostic Model).
- [x] Serialized final models to `models/final/` with complete `model_manifest.json` and verified local Windows reload.
- [x] Published `reports/final_model_validation.md`, `docs/PHASE_4_AUDIT.md`, 6 publication figures, and 42/42 passing unit tests.

### Phase 5: Local Streamlit Dashboard Implementation (Complete)
- [x] Built modular, professional local Streamlit application architecture in `app/`.
- [x] Implemented service layer: `model_service.py` (manifest validation, immutable loading), `data_service.py` (cached data, demo presets), and `inference_service.py` (zero-leakage inference, centroid distances).
- [x] Implemented 8 UI view components: Overview, Operating Regime, Primary Profile (K=2), Multi-Component Profile (K=3), Degradation Map, New Observation Analysis, Model Comparison, and Methodology & Limitations.
- [x] Incorporated live university defense demonstration mode with pre-configured physical presets (Nominal, Compressor Decay, Turbine Decay) and post-hoc reference verification.
- [x] Verified complete local offline autonomy on Windows OS with zero external APIs, zero cloud credentials, and zero silent retraining.
- [x] Authored `docs/PHASE_5_AUDIT.md`, `docs/PRESENTATION_DEMO.md`, and added 9 dedicated unit tests in `tests/test_app_services.py` (51/51 total tests passing).

### Phase 6: Final Academic Synthesis, Documentation & Presentation (Complete)
- [x] Conducted comprehensive audit of all source-of-truth artifacts in `docs/FINAL_AUDIT_NOTES.md`.
- [x] Authored full Turkish university research report in `reports/FINAL_UNIVERSITY_REPORT_TR.md` (24 formal sections).
- [x] Authored formal English research abstract in `reports/ABSTRACT_EN.md`.
- [x] Compiled definitive publication figure catalog in `docs/FINAL_FIGURE_CATALOG.md` (10 prioritized figures).
- [x] Created 16-slide university defense presentation outline in `docs/PRESENTATION_OUTLINE_TR.md`.
- [x] Created step-by-step live demo script with backup plan in `docs/LIVE_DEMO_SCRIPT_TR.md`.
- [x] Formulated 21 evidence-based defense question-and-answer responses in `docs/DEFENSE_QA_TR.md`.
- [x] Formulated claims safety checklist in `docs/CLAIMS_CHECKLIST_TR.md` (Safe, Requires Qualification, Do Not Say).
- [x] Rewrote `README.md` as professional GitHub documentation hub.
- [x] Documented all dataset citations, methodology papers, and software libraries in `docs/SOURCES.md`.
- [x] Conducted 12-point final project certification audit in `docs/FINAL_PROJECT_AUDIT.md`.
- [x] Confirmed 100% test pass rate (51/51 tests passing in ~6.5 seconds).

---

## 3. Milestones & Checkpoints

| Milestone | Deliverables | Verification Criteria |
| :--- | :--- | :--- |
| **M0: Architecture Base** | Directory tree, config system, base package, test scaffold | Unit tests pass, structure reviewed |
| **M1: EDA & Verification** | EDA notebook, data inspection report, column catalog | Verified no missing data anomalies, $kMc$/$kMt$ isolated |
| **M2: Preprocessing Pipeline** | Reusable transformers, feature selection, scaling tests | Deterministic transformations, unit test coverage |
| **M3: Clustering Benchmarks** | Clustering suite, parameter sweeps, logged runs | Intrinsic metrics logged in `experiments/outputs/` |
| **M4: Validation & Physics** | Statistical test results, degradation correlation analysis | Rigorous p-values, clear operating vs. degradation separation |
| **M5: Local Dashboard** | Working Streamlit application, visualization views | Flawless local launch via `streamlit run app/main.py` |
| **M6: Defense Readiness** | Final report, test suite passing, slides and demo script | Academic quality, zero unverified claims |
