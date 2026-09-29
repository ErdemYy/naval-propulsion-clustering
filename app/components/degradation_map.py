"""Degradation grid mapping component visualizing post-hoc spatial coherence."""

from __future__ import annotations

import streamlit as st

from app.components.shared import render_academic_disclaimer, render_metric_card
from app.services.data_service import get_figure_path, load_phase4_validation_results


def render_degradation_map_page() -> None:
    """Render the 2D degradation map component."""
    render_academic_disclaimer()

    st.title("🗺️ 2D Factorial Degradation Grid Map")
    st.markdown(
        """
        The simulated dataset has an exact **factorial degradation design** with 51 $kMc$ states (compressor decay) 
        and 26 $kMt$ states (turbine decay), producing **1,326 unique grid coordinates**, each evaluated across 9 ship speeds.
        """
    )

    st.markdown(
        """
        <div class="academic-banner">
            <strong>⚠️ Zero-Leakage Notice:</strong> This map visualizes post-hoc correspondence between learned 
            clusters and the dataset's reference degradation grid. The degradation indicators ($kMc, kMt$) 
            were <strong>NOT</strong> used during clustering or normalizer fitting.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Model Selection Toggle
    col_toggle, col_space = st.columns([1, 2])
    with col_toggle:
        model_choice = st.radio(
            "Select Clustering Model to Inspect:",
            options=["Candidate A (K=2, Primary)", "Candidate B (K=3, Multi-Component)"],
            index=0,
            horizontal=True,
        )

    st.markdown("---")

    p4_results = load_phase4_validation_results()

    if "K=2" in model_choice:
        # Candidate A Map
        col_m1, col_m2 = st.columns([1.4, 0.6])
        with col_m1:
            fig_path = get_figure_path("phase4", "degradation_grid_k2.png")
            if fig_path.exists():
                st.image(str(fig_path), caption="Candidate A (K=2) Cluster Map across kMc × kMt Degradation Plane", use_container_width=True)
            else:
                st.info("Figure degradation_grid_k2.png not found.")

        with col_m2:
            st.markdown("#### Grid Spatial Metrics")
            render_metric_card("Grid Resolution", "51 × 26", "1,326 unique degradation states")
            render_metric_card("Mean Speed Consistency", "86.24%", "Agreement across all 9 speed setpoints")
            render_metric_card("Median Consistency", "88.89%", "8 out of 9 speeds agree")
            
            st.markdown(
                r"""
                **Spatial Structure Observations:**
                - Clusters form a clean, contiguous vertical boundary around $kMc \approx 0.975$.
                - Low $kMc$ ($< 0.975$) is assigned to Cluster 1 across almost all $kMt$ coordinates.
                - High $kMc$ ($\ge 0.975$) is assigned to Cluster 0.
                - Verifies that unsupervised clustering forms coherent physical regions rather than noisy scatter.
                """
            )
    else:
        # Candidate B Map
        col_m1, col_m2 = st.columns([1.4, 0.6])
        with col_m1:
            fig_path = get_figure_path("phase4", "degradation_grid_k3.png")
            if fig_path.exists():
                st.image(str(fig_path), caption="Candidate B (K=3) Cluster Map across kMc × kMt Degradation Plane", use_container_width=True)
            else:
                st.info("Figure degradation_grid_k3.png not found.")

        with col_m2:
            st.markdown("#### Grid Spatial Metrics")
            render_metric_card("Grid Resolution", "51 × 26", "1,326 unique degradation states")
            render_metric_card("Mean Speed Consistency", "82.17%", "Agreement across all 9 speed setpoints")
            render_metric_card("Median Consistency", "88.89%", "8 out of 9 speeds agree")

            st.markdown(
                r"""
                **Spatial Structure Observations:**
                - **Cluster 2 (Orange):** Dominates low $kMc$ ($kMc < 0.965$) regardless of turbine decay.
                - **Cluster 0 (Blue):** Dominates high $kMc$ ($> 0.970$) when turbine decay is severe ($kMt \le 0.985$).
                - **Cluster 1 (Purple):** Dominates high $kMc$ ($> 0.970$) when turbine is nominal ($kMt > 0.985$).
                - Confirms that $K=3$ discovers both degradation axes without supervision.
                """
            )
