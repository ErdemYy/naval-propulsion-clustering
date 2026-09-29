# Live Defense Presentation Script: 5–7 Minute Walkthrough

**Project:** Naval Propulsion Clustering  
**Academic Title:** *Unsupervised Discovery of Operating and Performance Degradation Profiles in Naval Gas Turbine Propulsion Systems*  
**Audience:** University Evaluation Committee / Defense Panel  
**Platform:** Local Windows Laptop (Streamlit Offline Dashboard)  

---

## 1. Preparation Before Speaking
1. Open PowerShell / Command Prompt in the repository folder:
   ```powershell
   streamlit run app/main.py
   ```
2. Maximize the browser window at `http://localhost:8501`.
3. Set the sidebar navigation to **1. Overview**.

---

## 2. Minute-by-Minute Presentation Script

### Minute 0:00 – 1:00 | Slide / Page: 1. Overview
- **Opening:**  
  *"Good morning committee members. Today I am presenting our unsupervised machine learning project on Naval Gas Turbine Propulsion Systems."*
- **Key Points:**
  - *"We analyzed 11,934 steady-state observations from a simulated Combined Diesel and Gas (CODAG) naval plant across 9 ship speeds."*
  - *"The central scientific question was: Can unsupervised learning discover meaningful component degradation profiles when we strictly withhold degradation labels from the clustering algorithm?"*
  - *"Point out the **Anti-Leakage Protocol**: Both compressor decay ($kMc$) and turbine decay ($kMt$) were strictly quarantined and never used during training."*

---

### Minute 1:00 – 2:15 | Slide / Page: 2. Operating Regime Analysis
- **Transition:** Switch sidebar to **2. Operating Regime Analysis**.
- **The Core Scientific Obstacle:**  
  *"The first critical hurdle in industrial equipment clustering is operating point bias."*
- **Visual Evidence:**
  - Point to the metrics: *"In raw telemetry (R1), ship speed $v$ explains 99.33% of sensor variance. A baseline K-Means algorithm merely groups data by commanded speed with an Adjusted Rand Index of 0.8769."*
  - *"Even when we explicitly remove speed and lever position (R2), coupled thermodynamics allows the algorithm to reconstruct ship speed with an ARI of 0.8440."*
  - *"Our solution was **conditional within-speed normalization (R5)**: z-scoring each sensor relative to its speed setpoint. This drops the speed ARI to 0.0002, successfully decoupling plant load from equipment health."*

---

### Minute 2:15 – 3:30 | Slide / Page: 3. Primary Degradation Profile (K=2)
- **Transition:** Switch sidebar to **3. Primary Degradation Profile (K=2)**.
- **The Primary Scientific Model:**  
  *"Having decoupled operating speed, we evaluated clustering models on the normalized manifold. Our primary scientific model is K-Means with k=2."*
- **Empirical Findings:**
  - *"Silhouette score peaks at 0.2813. Resampling over 100 empirical bootstrap repetitions with replacement proved exceptional stability with a mean ARI of 0.9844."*
  - Point to the cluster cards: *"Post-hoc Mann-Whitney U testing reveals that Cluster 0 associates with nominal compressor health ($kMc \approx 0.985$), while Cluster 1 associates with degraded compressor health ($kMc \approx 0.965$) with a **Large effect size (Cliff's delta = +0.7709, p < 1e-100)**."*
  - Point out the speed breakdown chart: *"Cluster proportions stay strictly invariant between 46.9% and 53.1% across all 9 speed setpoints."*

---

### Minute 3:30 – 4:30 | Slide / Page: 4. Multi-Component Profile (K=3)
- **Transition:** Switch sidebar to **4. Multi-Component Profile (K=3)**.
- **Why Secondary Diagnostic Model is Justified:**  
  *"While k=2 is parsimonious, our effect size analysis proved it is completely blind to turbine decay (Cliff's delta = 0.132, negligible)."*
- **The Multi-Component Discovery:**  
  *"When we expand to k=3, the model discovers both degradation modes simultaneously:"*
  - **Cluster 1:** Nominal Baseline ($kMt \approx 0.992, kMc \approx 0.983$)
  - **Cluster 0:** Degraded Turbine Profile ($kMt \approx 0.982$, Cliff's delta = -0.767, Large effect)
  - **Cluster 2:** Degraded Compressor Profile ($kMc \approx 0.961$, Cliff's delta = +0.869, Large effect)
  - *"This proves that unsupervised clustering can dissociate multiple failing subsystems when plant load is controlled."*

---

### Minute 4:30 – 5:30 | Slide / Page: 5. Degradation Map
- **Transition:** Switch sidebar to **5. Degradation Map**.
- **Spatial Coherence in 2D:**  
  *"Here we project cluster assignments onto the factorial degradation grid ($51 \times 26 = 1,326$ cells)."*
- **Key Observation:**  
  - Toggle between $[K=2]$ and $[K=3]$:
  - *"Notice that the clusters form contiguous, geometrically clean regions rather than noisy scatter. Agreement across all 9 speed setpoints exceeds 82% across the entire plane."*
  - *"Remember, these coordinates were never seen by the model during training."*

---

### Minute 5:30 – 6:45 | Slide / Page: 6. New Observation Analysis (Live Demo)
- **Transition:** Switch sidebar to **6. New Observation Analysis**.
- **Interactive Live Demonstration:**  
  *"To prove reproducibility, our dashboard includes an inference service that evaluates multivariate observations in real time."*
- **Action Sequence:**
  1. Click **'Load Case 2: Compressor Decay'**.
  2. Explain: *"The system loads raw telemetry at 18 knots without knowing its degradation state."*
  3. Click **'Analyze Observation & Assign Profile'**.
  4. Show the result: *"The inference pipeline normalizes the sample using our serialized transformer and measures Euclidean distance to cluster centroids."*
  5. *"It immediately assigns this observation to **Cluster 1 (Compressor Degradation Association)** with an elevated temperature residual profile."*
  6. Point to the revealed reference box: *"Our post-hoc benchmark confirms true reference $kMc = 0.950$ (severe compressor decay)."*

---

### Minute 6:45 – 7:15 | Slide / Page: 8. Methodology & Limitations (Closing)
- **Transition:** Switch sidebar to **8. Methodology & Limitations**.
- **Scientific Honesty & Closing Statement:**  
  *"To maintain academic integrity, we conclude with our defined boundaries:"*
  - *"This work is based on numerical steady-state simulations and does not claim real-world naval deployment or real-time failure prediction."*
  - *"However, it conclusively proves our research thesis: within-regime normalization enables unsupervised learning to discover robust degradation profiles in complex turbomachinery."*
  - *"The codebase is fully tested with 51 passing unit tests and is open for questions. Thank you."*
