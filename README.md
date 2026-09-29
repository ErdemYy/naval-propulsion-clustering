# Naval Propulsion Clustering

**Academic Title:** *Unsupervised Discovery of Operating and Performance Degradation Profiles in Naval Gas Turbine Propulsion Systems*

An academic machine learning research project for exploring unsupervised learning, clustering methodologies, and profile discovery on multivariate measurements from naval gas turbine propulsion systems.

---

## 1. Project Overview & Purpose

This project investigates whether distinct, physically meaningful operating conditions and degradation-related profiles can be discovered in a naval propulsion plant purely through **unsupervised clustering**, without providing degradation labels or ground-truth decay states during training.

### Authoritative Dataset Provenance:
- **Source:** UCI Machine Learning Repository (Dataset ID: 316)
- **Dataset Name:** Condition Based Maintenance of Naval Propulsion Plants
- **Source Archive:** `https://archive.ics.uci.edu/static/public/316/condition+based+maintenance+of+naval+propulsion+plants.zip`
- **Integrity Digest (data.txt SHA-256):** `de0ea69da1efaab8b9655ffed828547d10dd68c1fb8c6e0163e6a988def393a6`
- **Total Records:** 11,934 rows x 18 continuous numeric columns
- **Provenance Manifest:** [`data/raw/manifest.json`](file:///data/raw/manifest.json)
- **Data Dictionary:** [`docs/DATA_DICTIONARY.md`](file:///docs/DATA_DICTIONARY.md)
- **Phase 1 Audit Report:** [`docs/PHASE_1_AUDIT.md`](file:///docs/PHASE_1_AUDIT.md)
- **Phase 2 Audit Report:** [`docs/PHASE_2_AUDIT.md`](file:///docs/PHASE_2_AUDIT.md)
- **Phase 3 Audit Report:** [`docs/PHASE_3_AUDIT.md`](file:///docs/PHASE_3_AUDIT.md)
- **Representation Registry:** [`experiments/outputs/phase2/representation_registry.json`](file:///experiments/outputs/phase2/representation_registry.json)

### Key Methodological Guardrails:
1. **Strictly Unsupervised Discovery:** The core machine learning task is unsupervised clustering. It is not framed as a supervised regression or classification problem.
2. **Feature Integrity (Target Separation):** Compressor decay state coefficient ($kMc$) and Turbine decay state coefficient ($kMt$) are **strictly quarantined** in `DatasetContainer.targets`. They are excluded from all clustering inputs and reserved exclusively for post-hoc validation.
3. **No Unsubstantiated Predictive Claims:** We avoid claims of "predicting failure" unless supported by rigorous empirical validation and appropriate time-series/degradation methodology.
4. **Distinction of Layers:** The project explicitly separates:
   - Mathematical clustering outputs (partitions, densities, cluster centroids).
   - Statistical evaluations (silhouette, Davies-Bouldin, ANOVA, Kruskal-Wallis).
   - Domain engineering interpretation (gas turbine thermodynamic relations).
   - Methodological limitations and threats to validity.
5. **Local & Cloudless Execution:** Designed to execute seamlessly on local environments (specifically tested for local Windows OS) with zero cloud infrastructure dependencies.
6. **Deterministic Reproducibility:** Fixed random seeds, structured configurations, and pipeline isolation ensure all experiments are end-to-end reproducible.

---

## 2. Directory Structure

```text
naval-propulsion-clustering/
├── .gitignore               # Ignored artifacts, datasets, caches
├── pyproject.toml           # Package metadata, dependencies, build settings
├── README.md                # Project documentation overview
├── PROJECT_PLAN.md          # Multi-phase project plan and milestones
├── METHODOLOGY.md           # Formal academic methodology & experimental protocol
├── LIMITATIONS.md           # Engineering & methodological limitations
├── EXPERIMENT_LOG.md        # Reproducible experiment registry & audit log
├── configs/                 # YAML configuration files (models, pipelines)
├── data/
│   ├── raw/                 # Immutable original dataset files
│   └── processed/           # Sanitized, scaled, or feature-engineered datasets
├── notebooks/               # Exploratory and prototyping Jupyter notebooks
├── src/
│   └── naval_propulsion/    # Core production & research Python package
│       ├── config/          # Configuration schemas and loading utilities
│       ├── data/            # Dataset loading and validation logic
│       ├── preprocessing/   # Cleaning, scaling, outlier handling
│       ├── features/        # Feature filtering, selection, dimensionality reduction
│       ├── clustering/      # Clustering algorithms, baselines, and wrappers
│       ├── evaluation/      # Unsupervised metrics and post-hoc statistical validation
│       ├── visualization/   # Publication-quality plotting and figures
│       └── utils/           # Reproducibility seeds, I/O, and logging
├── experiments/
│   ├── configs/             # Experiment-specific run specifications
│   └── outputs/             # Output metrics, tables, and serialized metadata
├── models/                  # Serialized clustering estimators and scalers
├── reports/
│   └── figures/             # High-resolution figures generated for reports
├── app/                     # Streamlit local interactive dashboard
├── tests/                   # Pytest suite (unit & integration tests)
└── docs/
    └── ARCHITECTURE.md      # Detailed software and ML system architecture
```

---

## 3. Quickstart & Installation

### Requirements
- Python >= 3.10
- Local Windows or POSIX environment

### Setup Virtual Environment
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

### Running Tests
```powershell
pytest
```

---

### Launching the Local Academic Dashboard
```powershell
streamlit run app/main.py
```
The dashboard runs completely offline on your local Windows laptop at `http://localhost:8501`.

---

## 4. Academic Documentation & Audit Links
- [Phase 1 Audit (Ingestion & Quality)](file:///docs/PHASE_1_AUDIT.md)
- [Phase 2 Audit (Preprocessing & Representations)](file:///docs/PHASE_2_AUDIT.md)
- [Phase 3 Audit (Controlled Clustering Experiments)](file:///docs/PHASE_3_AUDIT.md)
- [Phase 4 Audit (Scientific Validation & Selection)](file:///docs/PHASE_4_AUDIT.md)
- [Phase 5 Audit (Local Streamlit Dashboard)](file:///docs/PHASE_5_AUDIT.md)
- [Final Model Validation Report](file:///reports/final_model_validation.md)
- [Live Presentation & Defense Guide](file:///docs/PRESENTATION_DEMO.md)
- [Software Architecture](file:///docs/ARCHITECTURE.md)
- [Project Plan](file:///PROJECT_PLAN.md)
- [Methodology & Protocols](file:///METHODOLOGY.md)
- [Limitations & Boundary Conditions](file:///LIMITATIONS.md)
- [Experiment Registry](file:///EXPERIMENT_LOG.md)
