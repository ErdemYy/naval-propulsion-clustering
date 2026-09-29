# Unsupervised Discovery of Operating and Performance Degradation Profiles in Naval Gas Turbine Propulsion Systems

**Author:** Erdem Y.  
**Institution / Scope:** University Academic Capstone Research Project  
**Date:** September 2026  
**Repository:** [ErdemYy/naval-propulsion-clustering](https://github.com/ErdemYy/naval-propulsion-clustering)  

---

## Abstract

This research investigates the unsupervised discovery of operating-condition and component degradation-associated profiles in naval Combined Diesel and Gas (CODAG) propulsion systems using multivariate sensor telemetry. Analyzing the authoritative UCI Machine Learning Repository Dataset #316 (11,934 steady-state observations across 9 ship speed regimes), analysis reveals that commanded operating speed ($v$) accounts for 99.33% of raw sensor variance, causing naive unconditioned clustering algorithms to exclusively reconstruct operating speed setpoints (Adjusted Rand Index $\text{ARI} = 0.8769$) rather than equipment degradation.

To resolve this operational bias, a conditional within-speed normalization representation ($R5$) was formulated, which eliminates operating setpoint coupling ($\text{ARI} = 0.0002$) while preserving residual thermodynamic variation. In strict adherence to an anti-leakage protocol, ground-truth compressor ($kMc$) and turbine ($kMt$) degradation decay coefficients were quarantined from all model inputs and reserved exclusively for post-hoc validation.

On the normalized representation manifold, K-Means ($k=2$) was selected as the **Primary Scientific Model**, exhibiting the highest geometric silhouette score ($0.2813$), multi-seed determinism ($\text{ARI} = 0.9994$), and resampling stability over 100 bootstrap repetitions ($\text{Mean ARI} = 0.9844, 95\%\text{ CI: }[0.970, 0.998]$). Post-hoc Mann-Whitney $U$ and non-parametric effect size analyses confirm that $k=2$ cleanly separates compressor degradation with a large effect size (Cliff's delta $d = +0.7709, \eta^2 = 0.4459, p < 10^{-100}$) while remaining largely agnostic to turbine decay ($d = +0.1321$, negligible). To investigate multi-component degradation dissociation, K-Means ($k=3$) was retained as a **Secondary Diagnostic Model**, successfully separating nominal baseline states ($kMt \approx 0.992, kMc \approx 0.983$), degraded turbine states ($d = -0.7673, \eta^2 = 0.3007$), and degraded compressor states ($d = +0.8689, \eta^2 = 0.5109$).

The pipeline is verified by a 51-test automated suite and served via an offline local Streamlit dashboard. The methodology proves that unsupervised clustering can uncover component-level degradation profiles in complex turbomachinery when operational load regimes are rigorously decoupled, though findings remain subject to the limitations of steady-state numerical simulation.

**Keywords:** Unsupervised Learning, Clustering, Gas Turbines, Operating Regime Normalization, Data Leakage Invariant, Condition-Based Maintenance, Cliff's Delta, Bootstrap Stability.
