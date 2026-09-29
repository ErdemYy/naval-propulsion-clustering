# Naval Propulsion Clustering

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Tests Passing](https://img.shields.io/badge/tests-51%2F51%20passing-brightgreen.svg)]()
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)]()
[![Platform: Windows / Linux](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-lightgrey.svg)]()

**Academic Title:** *Unsupervised Discovery of Operating and Performance Degradation Profiles in Naval Gas Turbine Propulsion Systems*  
**Research Domain:** Machine Learning, Unsupervised Clustering, Industrial Condition Monitoring, Turbomachinery  
**Dataset:** UCI Machine Learning Repository Dataset #316 (Naval Propulsion Plants, N=11,934)  

---

## 📌 Executive Summary

In industrial and naval turbomachinery, continuous sensor measurements are abundantly available, but explicit equipment degradation labels are rarely accessible during operational service. Furthermore, **operational plant load** (commanded ship speed $v$) introduces variance that dwarfs subtle physical deterioration signatures.

This research investigates whether distinct, physically meaningful operating conditions and component degradation profiles (compressor decay and turbine decay) can be discovered in a naval Combined Diesel and Gas (CODAG) propulsion plant purely through **unsupervised clustering**, without providing degradation labels to the clustering algorithms.

### Key Scientific Findings:
- **Operating Speed Dominance:** Commanded ship speed $v$ explains **99.33% of raw sensor variance** ($\eta^2 \ge 0.965$ across all telemetry channels). Naive clustering algorithms on unconditioned telemetry merely group data by operating speed setpoints (Adjusted Rand Index $\text{ARI} = 0.8769$).
- **Within-Speed Normalization ($R5$):** Z-scoring telemetry conditionally within each operating speed setting decouples the operating setpoint ($\text{ARI} = 0.0002$) while preserving residual degradation signals.
- **Strict Zero-Leakage (Rule 1):** Compressor ($kMc$) and turbine ($kMt$) decay coefficients were strictly quarantined from model inputs and used exclusively for post-hoc statistical validation.
- **Primary Scientific Model (`KMeans(k=2)`):** Discovers a parsimonious compressor degradation profile ($kMc$ Cliff's delta $d = +0.7709$, Large effect, $p < 10^{-100}$) with **98.44% bootstrap stability** ($B=100$) and high speed invariance ($49.77\% \pm 2.22\%$).
- **Secondary Diagnostic Model (`KMeans(k=3)`):** Resolves both compressor decay ($d = +0.8689$) and turbine decay ($d = -0.7673$, Large effect), isolating nominal, turbine-degraded, and compressor-degraded thermodynamic states.

---

## 🏛️ System Architecture

```text
naval-propulsion-clustering/
├── pyproject.toml              # Declarative package build configuration
├── README.md                   # Main project overview and documentation
├── PROJECT_PLAN.md             # Multi-phase project roadmap & milestones
├── METHODOLOGY.md              # Formal experimental protocols
├── LIMITATIONS.md              # Boundary conditions & scientific constraints
├── EXPERIMENT_LOG.md           # Immutable experiment registry
├── app/                        # Professional local Streamlit dashboard
│   ├── main.py                 # Dashboard entrypoint & startup validator
│   ├── components/             # Modular Streamlit views (Overview, Profiles, Map, Demo)
│   └── services/               # Zero-leakage inference, cached data, model loaders
├── src/naval_propulsion/       # Core production & research package
│   ├── data/                   # Verified data loaders & container abstractions
│   ├── preprocessing/          # Screening, scalers, and Within-Speed Normalizer
│   ├── features/               # Correlation pruning & representation registry
│   ├── clustering/             # Standardized model wrappers (K-Means, GMM, Ward, DBSCAN)
│   ├── evaluation/             # Metrics, bootstrap stability, and pairwise MWU/FDR tests
│   └── visualization/          # Publication-grade plotting modules
├── models/final/               # Serialized final models & model_manifest.json
├── experiments/outputs/        # Machine-readable JSON metrics and sweeps
├── reports/                    # Formal university reports & publication figures
│   ├── FINAL_UNIVERSITY_REPORT_TR.md # Full Turkish academic research report
│   ├── ABSTRACT_EN.md          # Formal English research abstract
│   └── figures/                # High-resolution publication plots
├── docs/                       # Formal audit logs & defense preparation guides
│   ├── PRESENTATION_OUTLINE_TR.md   # 16-slide university defense plan
│   ├── LIVE_DEMO_SCRIPT_TR.md       # 5-7 minute live dashboard demo script
│   ├── DEFENSE_QA_TR.md             # 21 instructor defense questions & answers
│   └── CLAIMS_CHECKLIST_TR.md       # Presentation-safe speaking guidelines
└── tests/                      # 51 automated pytest unit and integration tests
```

---

## 📊 Experimental Results & Model Comparison

| Evaluation Criterion | Candidate A (Primary Baseline: K=2) | Candidate B (Secondary Diagnostic: K=3) |
| :--- | :--- | :--- |
| **Number of Clusters ($k$)** | **2** (Parsimonious) | **3** (Multi-Component) |
| **Silhouette Coefficient** | **0.2813** (Highest cohesion) | 0.2593 |
| **Davies-Bouldin Index** | 1.3917 | **1.2918** |
| **Calinski-Harabasz Index** | **5543.4** | 4889.7 |
| **Operating Speed Recovery ($\text{ARI vs } v$)** | **0.0002** (Completely decoupled) | 0.0064 |
| **Speed-wise Proportion Std** | **2.22%** ($49.77\% \pm 2.22\%$) | 6.28% ($28.3\% \dots 37.1\%$) |
| **Bootstrap Stability (Mean ARI, $B=100$)** | **0.9844** [95% CI: 0.970–0.998] | 0.9434 [95% CI: 0.792–0.990] |
| **Compressor Signal ($kMc$ $\eta^2$)** | 0.4459 (Large effect) | **0.5109** (Large effect) |
| **Compressor Signal (Cliff's Delta $d$)** | **+0.7709** (Large effect) | **+0.8689** (Large effect) |
| **Turbine Signal ($kMt$ $\eta^2$)** | 0.0131 (Negligible effect) | **0.3007** (Large effect) |
| **Turbine Signal (Cliff's Delta $d$)** | +0.1321 (Negligible effect) | **-0.7673** (Large effect) |
| **Degradation Grid Speed Consistency** | **86.24%** (Median: 88.89%) | 82.17% (Median: 88.89%) |

---

## 🚀 Quickstart & Local Installation

### Prerequisites
- Python >= 3.10 (tested on Python 3.12 64-bit Windows)
- Git

### 1. Clone & Set Up Virtual Environment
```powershell
git clone https://github.com/ErdemYy/naval-propulsion-clustering.git
cd naval-propulsion-clustering

python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

### 2. Run Automated Test Suite
To verify the complete test suite (51 tests):
```powershell
pytest
```

### 3. Launch the Local Streamlit Dashboard
The dashboard operates **completely offline** on your local machine:
```powershell
streamlit run app/main.py
```
Open your browser at 👉 **`http://localhost:8501`**.

---

## 🖥️ Streamlit Local Dashboard Modules

The interactive dashboard provides 8 modular views:
1. **Overview:** Project context, dataset summary, and 8-stage methodology flow.
2. **Operating Regime Analysis:** Empirical demonstration of speed dominance ($v$ explains 99.33% variance) and representation comparisons (R1 vs R2 vs R5).
3. **Primary Degradation Profile (K=2):** Cluster distributions, silhouette metrics, and large compressor decay separation ($d = +0.771$).
4. **Multi-Component Profile (K=3):** Simultaneous discovery of turbine decay ($d = -0.767$) and compressor decay ($d = +0.869$).
5. **Degradation Map:** Interactive 2D mapping across all 1,326 factorial ($kMc \times kMt$) grid states.
6. **New Observation Analysis:** Real-time profile assignment with 3 demo presets (Nominal, Compressor Decay, Turbine Decay) and post-hoc verification.
7. **Model Comparison:** Formal evaluation matrix across 11 criteria without artificial composite scores.
8. **Methodology & Limitations:** Comprehensive documentation of academic boundaries and ethics.

---

## ⚠️ Academic Boundaries & Disclaimers

This project is an academic research demonstration developed for university study. The following boundaries strictly apply:
- **Simulation-Based Data:** Telemetry originates from a numerical simulator of a CODAG propulsion plant; it lacks real-world sensor noise and sea-state turbulence.
- **Steady-State Gözlemleri:** Data captures static thermodynamic equilibria; dynamic throttle transients are absent.
- **No Fault Diagnosis or Failure Prediction:** The system does not predict remaining useful life (RUL) or future failure, as the data contains no time dimension.
- **No Military/Naval Deployment Claims:** The software has not been tested on physical vessels and must not be used for shipboard control or critical operations.

---

## 📄 Key Documentation Links
- 📘 [Full University Report (Turkish)](file:///reports/FINAL_UNIVERSITY_REPORT_TR.md)
- 🇬🇧 [English Academic Abstract](file:///reports/ABSTRACT_EN.md)
- 🎙️ [Live Defense Presentation Script (5–7 min)](file:///docs/PRESENTATION_DEMO.md)
- 📊 [16-Slide Presentation Plan](file:///docs/PRESENTATION_OUTLINE_TR.md)
- ❓ [Defense Q&A Guide (21 Questions)](file:///docs/DEFENSE_QA_TR.md)
- 🛡️ [Claims Safety Checklist](file:///docs/CLAIMS_CHECKLIST_TR.md)
- 🖼️ [Final Figure Catalog](file:///docs/FINAL_FIGURE_CATALOG.md)
- 📜 [Final Project Audit & Verification](file:///docs/FINAL_PROJECT_AUDIT.md)

---

## 📜 License & Provenance
- **Dataset:** UCI Machine Learning Repository Dataset #316 (Coraddu et al., 2016).
- **Code License:** MIT License.
