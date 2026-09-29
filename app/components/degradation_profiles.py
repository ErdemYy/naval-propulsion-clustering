"""Degradation profiles component for Candidate A (k=2) and Candidate B (k=3)."""

from __future__ import annotations

import streamlit as st

from app.components.shared import render_academic_disclaimer, render_metric_card
from app.services.data_service import get_figure_path, load_phase4_validation_results


def render_primary_profile_page() -> None:
    """Render the Primary Degradation Profile (k=2) page."""
    render_academic_disclaimer()

    st.title("🛡️ Primary Degradation Profile (Candidate A: K=2)")
    st.markdown(
        """
        The **Primary Scientific Model** is `KMeans(n_clusters=2, random_state=42)` fitted on 
        `R5_WITHIN_SPEED_NORMALIZED`. It provides a parsimonious, mathematically robust distinction 
        along the compressor degradation axis.
        """
    )

    # Core metric row
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_metric_card("Silhouette Cohesion", "0.2813", "Highest intrinsic separation")
    with c2:
        render_metric_card("Speed Independence", "ARI = 0.0002", "Decoupled from commanded speed")
    with c3:
        render_metric_card("Compressor Signal (kMc)", "Cliff's d = +0.771", "Large effect size (p < 1e-100)")
    with c4:
        render_metric_card("Bootstrap Stability", "Mean ARI = 0.9844", "95% CI: [0.970, 0.998]")

    st.markdown("---")

    # Cluster Breakdown
    col_c0, col_c1 = st.columns(2)
    with col_c0:
        st.markdown(
            """
            <div class="metric-card" style="border-left: 4px solid #2b5c8f;">
                <div class="metric-card-title">Cluster 0: Compressor Nominal Association</div>
                <div class="metric-card-value" style="font-size: 1.25rem;">n = 5,939 (49.77%)</div>
                <div class="metric-card-subtitle" style="margin-top: 6px;">
                    <strong>kMc Mean:</strong> 0.9849 ± 0.0108 (Median: 0.9860)<br>
                    <strong>kMt Mean:</strong> 0.9884 ± 0.0075 (Median: 0.9890)<br>
                    <strong>Telemetry Profile:</strong> Below-baseline temperatures (T2: -0.843, T48: -0.767) 
                    and below-baseline fuel flow (mf: -0.713).
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_c1:
        st.markdown(
            """
            <div class="metric-card" style="border-left: 4px solid #d95f02;">
                <div class="metric-card-title">Cluster 1: Compressor Degradation Association</div>
                <div class="metric-card-value" style="font-size: 1.25rem;">n = 5,995 (50.23%)</div>
                <div class="metric-card-subtitle" style="margin-top: 6px;">
                    <strong>kMc Mean:</strong> 0.9652 ± 0.0111 (Median: 0.9640)<br>
                    <strong>kMt Mean:</strong> 0.9866 ± 0.0074 (Median: 0.9860)<br>
                    <strong>Telemetry Profile:</strong> Above-baseline temperatures (T2: +0.835, T48: +0.760) 
                    and elevated fuel flow (mf: +0.706) to sustain torque.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # Visualizations
    st.subheader("📈 Telemetry Deviation & Speed Invariance")
    col_v1, col_v2 = st.columns(2)

    with col_v1:
        st.markdown("#### Speed-Wise Cluster Proportions")
        spd_fig = get_figure_path("phase4", "cluster_distribution_by_speed_k2.png")
        if spd_fig.exists():
            st.image(str(spd_fig), caption="Proportions across operating speeds remain tightly bounded (46.9% - 53.1%, std = 2.22%)", use_container_width=True)
        else:
            st.info("Figure cluster_distribution_by_speed_k2.png not found.")

    with col_v2:
        st.markdown("#### Telemetry Feature Deviation Profiles")
        tel_fig = get_figure_path("phase4", "telemetry_profiles_comparison.png")
        if tel_fig.exists():
            st.image(str(tel_fig), caption="Standardized cluster deviations (z-scores) relative to operating speed baseline with 95% CIs", use_container_width=True)
        else:
            st.info("Figure telemetry_profiles_comparison.png not found.")

    st.markdown("---")

    # Scientific Interpretation Alert
    st.markdown(
        """
        <div class="academic-banner">
            <strong>🔬 Statistical Note on Turbine Decay:</strong> While Candidate A produces an astronomically small 
            p-value for turbine decay ($p = 6.69 \\times 10^{-36}$) due to the large sample size ($N=11,934$), 
            its Cliff's delta is <strong>0.1321 (Negligible)</strong>. 
            Candidate A must therefore be characterized strictly as a <em>single-component compressor profile discriminator</em>.
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_multicomponent_profile_page() -> None:
    """Render the Multi-Component Profile (k=3) page."""
    render_academic_disclaimer()

    st.title("🧩 Multi-Component Degradation Profile (Candidate B: K=3)")
    st.markdown(
        """
        The **Secondary Diagnostic Model** is `KMeans(n_clusters=3, random_state=42)` fitted on 
        `R5_WITHIN_SPEED_NORMALIZED`. It resolves the key limitation of $K=2$ by discovering 
        a secondary partition along the turbine degradation axis.
        """
    )

    # Core metric row
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_metric_card("Silhouette Score", "0.2593", "Good tripartite cohesion")
    with c2:
        render_metric_card("Turbine Signal (kMt)", "Cliff's d = -0.767", "Large effect size (p < 1e-100)")
    with c3:
        render_metric_card("Compressor Signal (kMc)", "Cliff's d = +0.869", "Large effect size (p < 1e-100)")
    with c4:
        render_metric_card("Bootstrap Stability", "Mean ARI = 0.9434", "95% CI: [0.792, 0.990]")

    st.markdown("---")

    # 3 Cluster Profile Cards
    p1, p2, p3 = st.columns(3)

    with p1:
        st.markdown(
            """
            <div class="metric-card" style="border-left: 4px solid #7570b3;">
                <div class="metric-card-title">Cluster 1: Nominal Baseline</div>
                <div class="metric-card-value" style="font-size: 1.2rem;">n = 4,125 (34.57%)</div>
                <div class="metric-card-subtitle" style="margin-top: 6px;">
                    <strong>kMc Mean:</strong> 0.9826 (Median: 0.9840)<br>
                    <strong>kMt Mean:</strong> 0.9920 (Median: 0.9930)<br>
                    <strong>Profile:</strong> Highest overall component health. Lowest fuel flow (mf: -1.063) 
                    and lowest turbine exit temperature (T48: -1.046).
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with p2:
        st.markdown(
            """
            <div class="metric-card" style="border-left: 4px solid #2b5c8f;">
                <div class="metric-card-title">Cluster 0: Turbine Degradation</div>
                <div class="metric-card-value" style="font-size: 1.2rem;">n = 3,379 (28.31%)</div>
                <div class="metric-card-subtitle" style="margin-top: 6px;">
                    <strong>kMc Mean:</strong> 0.9837 (Median: 0.9850)<br>
                    <strong>kMt Mean:</strong> 0.9816 (Median: 0.9810)<br>
                    <strong>Profile:</strong> High compressor health but degraded turbine. Elevated pressures 
                    (P48: +0.869, P2: +0.966) and lower shaft speeds (GTn: -0.940).
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with p3:
        st.markdown(
            """
            <div class="metric-card" style="border-left: 4px solid #d95f02;">
                <div class="metric-card-title">Cluster 2: Compressor Degradation</div>
                <div class="metric-card-value" style="font-size: 1.2rem;">n = 4,430 (37.12%)</div>
                <div class="metric-card-subtitle" style="margin-top: 6px;">
                    <strong>kMc Mean:</strong> 0.9613 (Median: 0.9600)<br>
                    <strong>kMt Mean:</strong> 0.9877 (Median: 0.9880)<br>
                    <strong>Profile:</strong> Pronounced compressor decay. Characterized by elevated temperatures 
                    (T2: +0.962, T48: +0.778) and high fuel flow (mf: +0.680).
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # Speed Invariance Chart
    st.subheader("📈 Operating Speed Invariance for K=3")
    col_img, col_txt = st.columns([1.2, 0.8])

    with col_img:
        spd_k3_fig = get_figure_path("phase4", "cluster_distribution_by_speed_k3.png")
        if spd_k3_fig.exists():
            st.image(str(spd_k3_fig), caption="Cluster proportions across commanded speeds for K=3", use_container_width=True)
        else:
            st.info("Figure cluster_distribution_by_speed_k3.png not found.")

    with col_txt:
        st.markdown(
            """
            #### Physical Speed-Decay Interaction
            - **Low Speeds (3 & 6 knots):** Cluster 2 (Compressor Degradation) accounts for ~22% of samples because low plant load dampens compressor degradation symptoms.
            - **Cruise & Full Power (9 to 27 knots):** Cluster proportions stabilize near 42% for Cluster 2, 28% for Cluster 0, and 30% for Cluster 1.
            - **Independence:** Cramér's $V = 0.1273$ confirms small operating-speed association, preserving the overall independence of the multi-component profile.
            """
        )
