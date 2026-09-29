"""Overview page component for the Naval Propulsion Clustering dashboard."""

from __future__ import annotations

import streamlit as st

from app.components.shared import render_academic_disclaimer, render_metric_card
from app.services.data_service import load_cached_dataset
from app.services.model_service import load_model_manifest


def render_overview_page() -> None:
    """Render the project overview page."""
    render_academic_disclaimer()

    st.title("⚓ Naval Propulsion Clustering Dashboard")
    st.subheader(
        "Unsupervised Discovery of Operating and Performance Degradation Profiles "
        "in Naval Gas Turbine Propulsion Systems"
    )

    st.markdown(
        """
        > **Project Purpose:** The application explores whether within-operating-regime normalized propulsion telemetry 
        > contains stable profiles associated with compressor and turbine degradation indicators, without providing degradation 
        > labels to the clustering models.
        """
    )

    # Key dataset and model metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_metric_card("Dataset Size", "11,934", "Steady-state rows")
    with col2:
        render_metric_card("Raw Sensor Channels", "18", "Telemetry channels")
    with col3:
        render_metric_card("Clustering Features", "11", "Excluding constants/speed")
    with col4:
        render_metric_card("Operating Regimes", "9", "3 to 27 knots")

    st.markdown("---")

    # Retained Models Summary
    st.subheader("🎯 Retained Models (Phase 4 Scientific Selection)")
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown(
            """
            <div class="metric-card" style="border-left: 4px solid #3b82f6;">
                <div class="metric-card-title">Primary Scientific Model</div>
                <div class="metric-card-value" style="font-size: 1.3rem;">KMeans (k=2) on R5</div>
                <div class="metric-card-subtitle" style="margin-top: 8px;">
                    <strong>Role:</strong> Authoritative baseline for binary degradation discovery.<br>
                    <strong>Separation:</strong> Silhouette = 0.2813 (highest intrinsic cohesion)<br>
                    <strong>Speed Independence:</strong> Speed ARI = 0.0002 (complete decoupling)<br>
                    <strong>Compressor Signal:</strong> kMc Cliff's delta = +0.7709 (Large effect)<br>
                    <strong>Stability:</strong> Mean Bootstrap ARI = 0.9844 [95% CI: 0.970–0.998]
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_b:
        st.markdown(
            """
            <div class="metric-card" style="border-left: 4px solid #8b5cf6;">
                <div class="metric-card-title">Secondary Diagnostic Model</div>
                <div class="metric-card-value" style="font-size: 1.3rem;">KMeans (k=3) on R5</div>
                <div class="metric-card-subtitle" style="margin-top: 8px;">
                    <strong>Role:</strong> Specialized multi-component degradation model.<br>
                    <strong>Turbine Signal:</strong> kMt Cliff's delta = -0.7673 (Large effect)<br>
                    <strong>Compressor Signal:</strong> kMc Cliff's delta = +0.8689 (Large effect)<br>
                    <strong>Component Resolution:</strong> Separates nominal, turbine decay, compressor decay<br>
                    <strong>Stability:</strong> Mean Bootstrap ARI = 0.9434 [95% CI: 0.792–0.990]
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # Methodology Flow Diagram
    st.subheader("🔬 High-Level Methodology Flow")
    st.markdown(
        """
        ```text
        [Raw Telemetry (18 channels)] 
                   │
                   ▼ (Remove constant T1, P1 and duplicate Tp)
        [Cleaned Telemetry (15 channels)] 
                   │
                   ▼ (Condition on commanded speed v ∈ {3..27 kts})
        [Within-Speed Normalization (R5: mean=0, std=1 per speed setting)]
                   │
                   ▼ (Unsupervised K-Means clustering, ZERO LEAKAGE)
        [Learned Cluster Profiles (k=2, k=3)]
                   │
                   ▼ (Post-hoc hypothesis tests: Mann-Whitney U, Cliff's delta, Bootstrap CIs)
        [Scientific Degradation Association Validation]
        ```
        """
    )

    st.markdown("---")

    # 5-Minute Live Presentation Guide
    with st.expander("⏱️ 5-Minute University Presentation Walkthrough Guide", expanded=False):
        st.markdown(
            """
            Recommended sequence for a live 5–7 minute defense presentation:
            1. **Step 1 (Overview - 1 min):** Highlight that the dataset contains 11,934 observations with 9 speeds and that degradation indicators ($kMc, kMt$) were strictly quarantined.
            2. **Step 2 (Operating Regime - 1 min):** Show how speed explains 99.33% of raw sensor variance, and how unconditioned clustering (R1/R2) merely reconstructs ship speed (ARI ≈ 0.88).
            3. **Step 3 (Primary Model - 1.5 min):** Demonstrate that within-speed normalized K-Means ($k=2$) eliminates speed coupling (ARI ≈ 0.0002) and discovers compressor degradation ($d = 0.771$) with 98.4% bootstrap stability.
            4. **Step 4 (Multi-Component Model - 1.5 min):** Explain how $k=3$ resolves both turbine ($d = -0.767$) and compressor degradation into three distinct thermodynamic regimes.
            5. **Step 5 (Interactive Demo - 1 min):** Load a sample observation on the **New Observation Analysis** page to show real-time nearest profile assignment.
            """
        )
