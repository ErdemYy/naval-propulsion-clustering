"""Methodology and academic limitations component."""

from __future__ import annotations

import streamlit as st

from app.components.shared import render_academic_disclaimer


def render_methodology_page() -> None:
    """Render the methodology and academic limitations page."""
    render_academic_disclaimer()

    st.title("📚 Methodology & Academic Limitations")

    # 1. Methodology Walkthrough
    st.subheader("🔬 8-Stage Research Methodology Pipeline")
    st.markdown(
        r"""
        1. **Authoritative Dataset Ingestion (Phase 1):**  
           Ingestion of UCI Machine Learning Repository Dataset #316 (Naval Propulsion Plants). Verification of 11,934 steady-state observations and SHA-256 data integrity.
        2. **Data Quality & Ingestion Contracts (Phase 1):**  
           Formal contract verification confirming zero missing values, zero duplicated rows, and strict isolation of target variables.
        3. **Feature Screening & Pruning (Phase 2):**  
           Identification and mandatory removal of zero-variance constant channels ($T_1 = 288.0$ K, $P_1 = 0.998$ bar) and exact mathematical duplicates ($T_p \equiv T_s$).
        4. **Operating-Condition Analysis (Phase 2):**  
           Statistical demonstration that commanded ship speed $v$ explains 99.33% of raw sensor variance, proving that unconditioned clustering merely groups by speed setpoints.
        5. **Conditional Within-Speed Normalization (Phase 2):**  
           Construction of Representation R5 ($z_{ij} = (x_{ij} - \mu_j(v_i)) / \sigma_j(v_i)$) across the 11 clustering-eligible telemetry channels, eliminating operating point bias.
        6. **Controlled Unsupervised Clustering (Phase 3):**  
           Execution of systematic K-Means sweeps ($k=2 \dots 12$), hierarchical linkage tests, DBSCAN density evaluations, and GMM covariance tests without degradation labels.
        7. **Multi-Seed & Bootstrap Stability Validation (Phase 3 & 4):**  
           Resampling validation across 10 random initialization seeds and 100 empirical bootstrap repetitions with replacement to verify partition determinism.
        8. **Post-Hoc Degradation Validation with Zero-Leakage (Phase 4):**  
           Rigorous non-parametric hypothesis testing (Mann-Whitney U, Benjamini-Hochberg FDR, Cliff's delta) strictly evaluating cluster associations against quarantined $kMc$ and $kMt$.
        """
    )

    st.markdown("---")

    # Anti-Leakage Invariant
    st.subheader("🛡️ Strict Anti-Leakage Protocol (Rule 1)")
    st.markdown(
        """
        <div class="academic-banner">
            <strong>Core Invariant:</strong> The degradation indicators ($kMc, kMt$) were quarantined in 
            <code>DatasetContainer.targets</code> and completely excluded from all feature engineering, scaling, 
            dimensionality reduction, hyperparameter selection, and model fitting steps. 
            They were utilized strictly post-hoc to evaluate whether the discovered clusters correlate with physical component degradation.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # Academic Limitations
    st.subheader("⚠️ Academic Limitations & Scope Boundaries")
    st.markdown(
        """
        <div class="warning-banner">
            <strong>Critical Scientific Limitations:</strong>
            <ul>
                <li><strong>Simulation-Based Telemetry:</strong> Telemetry originates from a numerical simulator of a CODAG 
                naval propulsion plant. It lacks real-world sensor noise, telemetry dropouts, calibration drift, and unmodeled sea-state turbulence.</li>
                <li><strong>Steady-State Observations:</strong> Observations represent static thermodynamic equilibrium at fixed discrete 
                speeds and decay settings. Transient throttle maneuvers, rapid acceleration, and thermal inertia are not captured.</li>
                <li><strong>Artificial Factorial Grid:</strong> The uniform factorial degradation grid ($9 \times 51 \times 26$) does not reflect 
                realistic temporal degradation dynamics, where machines deteriorate gradually over thousands of operating hours.</li>
                <li><strong>Reference Indicators:</strong> $kMc$ and $kMt$ are simulation model decay coefficients, not physical sensors on a ship.</li>
                <li><strong>Correlation is Not Causality:</strong> Clustering discovers geometric partitions in high-dimensional residual space 
                that correlate with degradation; it does not prove physical causal direction.</li>
                <li><strong>No Real-World Naval Deployment Claims:</strong> The system has not been tested on operational vessels and 
                must not be used for real-time shipboard control or critical naval operations.</li>
                <li><strong>No Fault Diagnosis or Failure Prediction:</strong> The models do not predict remaining useful life (RUL) 
                or future component failure because the dataset contains no time dimension.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
