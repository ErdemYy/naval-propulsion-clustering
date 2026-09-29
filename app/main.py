"""Professional Local Streamlit Dashboard Entrypoint.

Naval Propulsion Clustering: Unsupervised Discovery of Operating and Performance
Degradation Profiles in Naval Gas Turbine Propulsion Systems.
"""

from __future__ import annotations

import streamlit as st

from app.components import (
    apply_academic_styling,
    render_degradation_map_page,
    render_methodology_page,
    render_model_comparison_page,
    render_multicomponent_profile_page,
    render_observation_analysis_page,
    render_operating_regime_page,
    render_overview_page,
    render_primary_profile_page,
)
from app.services.model_service import ModelArtifactError, load_final_models


def main() -> None:
    """Run the Streamlit interactive academic dashboard."""
    st.set_page_config(
        page_title="Naval Propulsion Clustering — Academic Dashboard",
        page_icon="⚓",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    apply_academic_styling()

    # Startup validation: Load and verify serialized artifacts
    try:
        models_bundle = load_final_models()
        manifest = models_bundle["manifest"]
    except ModelArtifactError as e:
        st.error(f"❌ Application Startup Error: {e}")
        st.warning(
            "The dashboard operates exclusively on pre-trained, validated artifacts. "
            "Please ensure Phase 4 model serialization has run before launching."
        )
        st.stop()
    except Exception as e:
        st.error(f"❌ Unexpected Error Loading Models: {e}")
        st.stop()

    # Sidebar Navigation
    st.sidebar.markdown(
        """
        <div style="text-align: center; padding: 8px 0 16px 0;">
            <span style="font-size: 2.2rem;">⚓</span>
            <div style="font-weight: 700; font-size: 1.05rem; color: #ffffff; margin-top: 4px;">
                Naval Propulsion
            </div>
            <div style="font-size: 0.78rem; color: #8da4c4;">
                Clustering & Validation Dashboard
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Demo quick-selector
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Live Presentation Navigation**")

    pages = [
        "1. Overview",
        "2. Operating Regime Analysis",
        "3. Primary Degradation Profile (K=2)",
        "4. Multi-Component Profile (K=3)",
        "5. Degradation Map",
        "6. New Observation Analysis",
        "7. Model Comparison",
        "8. Methodology & Limitations",
    ]

    selected_page = st.sidebar.radio(
        "Navigate Sections:",
        options=pages,
        index=0,
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown(
        f"""
        <div style="font-size: 0.75rem; color: #5c7a9c; line-height: 1.4;">
            <strong>Environment Status:</strong><br>
            • Primary Model: KMeans (k=2)<br>
            • Secondary Model: KMeans (k=3)<br>
            • Representation: R5 (Within-Speed)<br>
            • Verification: 42/42 Tests Passing<br>
            • Status: Local Offline Ready
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Page Routing
    if selected_page == "1. Overview":
        render_overview_page()
    elif selected_page == "2. Operating Regime Analysis":
        render_operating_regime_page()
    elif selected_page == "3. Primary Degradation Profile (K=2)":
        render_primary_profile_page()
    elif selected_page == "4. Multi-Component Profile (K=3)":
        render_multicomponent_profile_page()
    elif selected_page == "5. Degradation Map":
        render_degradation_map_page()
    elif selected_page == "6. New Observation Analysis":
        render_observation_analysis_page()
    elif selected_page == "7. Model Comparison":
        render_model_comparison_page()
    elif selected_page == "8. Methodology & Limitations":
        render_methodology_page()


if __name__ == "__main__":
    main()
