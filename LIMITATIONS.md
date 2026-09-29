# Project Limitations & Threat to Validity Analysis

**Academic Title:** *Unsupervised Discovery of Operating and Performance Degradation Profiles in Naval Gas Turbine Propulsion Systems*

---

## 1. Domain & Simulation Data Limitations
1. **Numerical Simulator Origin & Full Factorial Design:**
   - The UCI Naval Propulsion Plants dataset (#316) is confirmed to be generated from a numerical simulator of a CODAG naval vessel (Frigate).
   - Ingestion confirms that the dataset is a rigid, synthetic full factorial grid of 9 operating points ($v \in [3, 27]$ knots) $\times$ 51 compressor decay values ($kMc \in [0.95, 1.0]$) $\times$ 26 turbine decay values ($kMt \in [0.975, 1.0]$) = 11,934 samples.
   - It represents synthetic grid sampling rather than stochastic maritime operations or continuous wear-and-tear journeys.

2. **Simulated Boundary Conditions (Zero-Variance Telemetry):**
   - Ingestion audit confirms that Compressor Inlet Temperature `T1` is fixed at $288.0$ K ($15^\circ$C) and Compressor Inlet Pressure `P1` is fixed at $0.998$ bar across all 11,934 rows (standard deviation = 0.0).
   - In addition, Starboard and Port Propeller Torques (`Ts`, `Tp`) are mathematically identical ($|Ts - Tp| = 0.0$ everywhere).
   - In real-world ships, ambient temperature fluctuates continuously and propeller hydrodynamic loading differs between port and starboard during turns or sea drift.

3. **Steady-State Operational Assumption:**
   - Samples represent quasi-steady operating conditions across various ship speeds and component decay states.
   - Dynamic transients (e.g., sudden emergency crash-stop maneuvers, acceleration spikes, turbine start-up/shut-down cycles) are not represented in discrete steady-state records.

4. **Absence of Temporal Run-to-Failure Trajectories:**
   - The dataset provides snapshots across a grid of operating points and decay states rather than continuous, unrolled time-series trajectories down to component breakdown.
   - **Critical Constraint:** Without timestamped run-to-failure sequences, we **cannot claim Remaining Useful Life (RUL) prediction or immediate failure forecasting**. All degradation conclusions must remain strictly characterizations of condition profiles.

---

## 2. Machine Learning & Methodological Limitations

1. **Dominance of Operating Variables over Degradation Signatures (Mathematically Proven in Phase 2):**
   - Analysis of variance proved that commanded ship speed $v$ explains an average of **99.33% of total variance** across all telemetry sensors ($\eta^2 \ge 0.965$ for all features).
   - In contrast, component degradation ($kMc \in [0.95, 1.0]$, $kMt \in [0.975, 1.0]$) represents a subtle 1% to 3.5% within-speed variation.
   - Standard unsupervised clustering on globally scaled features is mathematically forced to partition along speed regimes rather than degradation states.
   - Decoupling speed from degradation requires conditional within-regime normalization (Representation R5) or operating-regime stratified clustering.

2. **Infeasibility of Blind Dimensionality Reduction (PCA Limit):**
   - PCA diagnostic evaluation proved that **PC1 accounts for 97.41% of total variance** with uniform positive loadings ($\approx 0.27$ to $0.28$) across all telemetry features, capturing the 1D thermodynamic plant operating line.
   - Prematurely projecting data into 2 or 3 principal components before clustering discards the minor residual components (PC3 to PC6) where degradation signatures reside.
   - PCA is strictly restricted to diagnostic visualization and must not be used as an automatic pre-clustering filter without comparative proof.

3. **Inductive Biases of Clustering Algorithms:**
   - **K-Means:** Assumes convex, isotropic (spherical), equally-sized clusters with similar variances. Non-linear thermodynamic manifolds may be artificially fragmented.
   - **DBSCAN:** Assumes uniform density across clusters. Varying density between low-speed idle points and high-speed full-power points can cause under-clustering or excessive noise classification.
   - **Hierarchical Clustering:** High memory and quadratic computational complexity $\mathcal{O}(n^2)$ can become restrictive for large datasets without sub-sampling.
   - **Gaussian Mixture Models:** Expectation-Maximization can be vulnerable to local optima and covariance singularity in high-dimensional feature spaces.

3. **Absence of Ground Truth for Unsupervised Objectives:**
   - Unsupervised metrics (Silhouette, Davies-Bouldin) evaluate geometric properties in the transformed space, which do not inherently guarantee thermodynamic or engineering relevance.
   - High silhouette scores may merely reflect well-spaced operational discrete throttle settings rather than meaningful degradation segmentation.

---

## 3. Engineering & Deployment Scope

1. **Local Demonstration Scope:**
   - The project is architected for local deployment on standard Windows workstations.
   - Heavy distributed clustering (e.g., Apache Spark, massive parallel hyperparameter grids) is outside the scope of this course project.
2. **Safety & Operational Decisions:**
   - The findings of this project are for academic exploration only and must never be used for real-world automated engine control or safety-critical maintenance decisions without comprehensive marine validation.
