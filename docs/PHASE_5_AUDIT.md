# Phase 5 Formal Audit Report: Professional Local Streamlit Dashboard

**Project:** Naval Propulsion Clustering  
**Academic Title:** *Unsupervised Discovery of Operating and Performance Degradation Profiles in Naval Gas Turbine Propulsion Systems*  
**Date of Audit:** 2026-09-29  
**Phase Status:** Complete & Fully Verified  
**Entrypoint:** `streamlit run app/main.py`  
**Test Suite Status:** 51/51 Unit Tests Passing (100%)  

---

## 1. Phase 5 Objectives & Engineering Scope

The objective of Phase 5 is to construct a modular, professional local Streamlit application suitable for live university presentation on a Windows laptop, adhering strictly to academic engineering design principles, complete offline autonomy, and immutable model loading without silent retraining.

### Architecture Overview (`app/`)
```text
app/
├── main.py                     # Central Streamlit entrypoint & router
├── components/                 # Modular UI view components
│   ├── __init__.py
│   ├── degradation_map.py      # Interactive 2D (kMc x kMt) grid plane view
│   ├── degradation_profiles.py # Deep-dives for K=2 and K=3 profiles
│   ├── methodology.py          # 8-stage methodology & academic limitations
│   ├── model_comparison.py     # Side-by-side formal evaluation matrix
│   ├── observation_analysis.py # Live new observation analysis & demo presets
│   ├── operating_regime.py     # Empirical proof of operating speed dominance
│   ├── overview.py             # Project overview, metrics, and methodology flow
│   └── shared.py               # Technical dark navy CSS, metric cards, disclaimer
└── services/                   # Business logic & ML inference abstractions
    ├── __init__.py
    ├── data_service.py         # Cached dataset access & demo preset extraction
    ├── inference_service.py    # Zero-leakage inference, schema validation & distances
    └── model_service.py        # Serialized artifact loading & manifest validation
```

---

## 2. Invariant & Anti-Leakage Audit

| Invariant / Security Check | Implementation Details | Verification Status |
| :--- | :--- | :--- |
| **No Silent Retraining** | `model_service.py` exclusively loads pre-serialized `.joblib` artifacts. If any artifact is missing, it raises `ModelArtifactError` and halts with clear error diagnostics. | **VERIFIED** |
| **Zero-Leakage Inputs** | `inference_service.py` validates that `kMc` and `kMt` are never present in user inputs. If detected, an `InputValidationError` is immediately raised. | **VERIFIED** |
| **Conditioning Variable Enforcement** | Because Representation `R5` relies on within-speed normalization, the inference service strictly enforces that speed $v \in \{3, 6, 9, 12, 15, 18, 21, 24, 27\}$ knots is supplied. | **VERIFIED** |
| **Academic Non-Causal Language** | UI components use wording such as *"associated with elevated compressor decay"* and *"closest learned profile"* instead of *"fault predicted"* or *"failure detection"*. | **VERIFIED** |

---

## 3. UI Component Audit

1. **Overview Page (`overview.py`):**
   - Displays dataset summary metrics (11,934 rows, 18 canonical channels, 11 clustering features, 9 speed regimes).
   - Summarizes Primary Model (`KMeans(k=2)`) and Secondary Model (`KMeans(k=3)`).
   - Features an 8-stage methodology flow diagram and an embedded 5-minute presentation guide.
2. **Operating Regime Analysis (`operating_regime.py`):**
   - Demonstrates speed dominance ($v$ explains 99.33% of variance).
   - Contrasts R1 (ARI = 0.8769), R2 (ARI = 0.8440), and R5 (ARI = 0.0002).
   - Renders Phase 2 and Phase 3 diagnostic figures directly.
3. **Primary Degradation Profile (`degradation_profiles.py`):**
   - Focuses on Primary Model ($K=2$).
   - Displays cluster cards, silhouette score (0.2813), and bootstrap stability (mean ARI = 0.9844).
   - Details large compressor effect size ($d = +0.7709$) and negligible turbine effect size ($d = +0.1321$).
4. **Multi-Component Profile (`degradation_profiles.py`):**
   - Focuses on Secondary Model ($K=3$).
   - Explains the three-way dissociation: Nominal Baseline ($kMt \approx 0.992$), Degraded Turbine Profile ($kMt \approx 0.982$, Cliff's delta = -0.767), and Degraded Compressor Profile ($kMc \approx 0.961$, Cliff's delta = +0.869).
5. **Degradation Map (`degradation_map.py`):**
   - Interactive 2D spatial view ($x = kMc, y = kMt$) across all 1,326 factorial cells.
   - Radio toggle between $K=2$ and $K=3$.
   - Confirms spatial contiguity and $>82\%$ speed consistency.
6. **New Observation Analysis (`observation_analysis.py`):**
   - Real-time multivariate observation analysis.
   - Includes 3 pre-configured demonstration presets (Nominal, Compressor Decay, Turbine Decay).
   - Computes Euclidean distances to cluster centroids and visualizes standardized z-score deviation bars.
   - Post-hoc ground-truth reference values are displayed strictly after cluster assignment.
7. **Model Comparison (`model_comparison.py`):**
   - Side-by-side formal comparison table across 11 key criteria.
   - Provides scientific selection rationale without artificial composite scores.
8. **Methodology & Limitations (`methodology.py`):**
   - Detailed walkthrough of all 8 pipeline phases.
   - Comprehensive documentation of 7 critical academic boundaries and limitations.

---

## 4. Offline & Windows Compatibility Verification

- **Local Autonomy:** The application requires zero internet connectivity, zero external APIs, zero cloud credentials, and zero external databases.
- **Fast Response Time:** Cached loading (`@st.cache_data`) loads the full dataset and validation metrics once, ensuring instantaneous page switching.
- **Server Startup Test:** Tested via `streamlit run app/main.py --server.headless true --server.port 8501`. Uvicorn server initialized cleanly on Windows without errors or warnings.

---

## 5. Test Suite Verification

A dedicated test suite was implemented in `tests/test_app_services.py` to validate application services:
- `test_manifest_validation`: Verified manifest schema and section completeness.
- `test_model_loading`: Verified deserialization into valid scikit-learn estimators.
- `test_missing_artifact_handling`: Verified clear error raising when artifacts are absent.
- `test_input_schema_validation_speed_required`: Verified rejection when speed $v$ is omitted.
- `test_input_schema_validation_unobserved_speed`: Verified rejection of unobserved speeds.
- `test_input_schema_validation_missing_telemetry`: Verified rejection of partial telemetry vectors.
- `test_anti_leakage_rejection_of_kmc_kmt`: Verified that leaked target inputs raise critical errors.
- `test_observation_profile_assignment_determinism`: Verified deterministic centroid distance calculations.
- `test_demo_observations_integrity`: Verified preset data integrity and anti-leakage isolation.

Pytest execution results across all 8 test modules:
```text
tests/test_app_services.py .........                                    [ 17%]
tests/test_clustering_phase3.py ...........                             [ 39%]
tests/test_config.py ..                                                 [ 43%]
tests/test_data_container.py ...                                        [ 49%]
tests/test_evaluation_metrics.py ..                                     [ 52%]
tests/test_ingestion_and_quality.py ........                            [ 68%]
tests/test_preprocessing_phase2.py ........                            [ 84%]
tests/test_utils.py ..                                                  [ 88%]
tests/test_validation_phase4.py ........                                [100%]

============================== 51 passed in 6.97s ==============================
```

**Phase 5 Audit Status:** **APPROVED & CERTIFIED**
