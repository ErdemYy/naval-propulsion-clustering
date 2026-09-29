"""Operating regime analysis component illustrating the speed dominance problem."""

from __future__ import annotations

from pathlib import Path
import streamlit as st

from app.components.shared import render_academic_disclaimer, render_metric_card
from app.services.data_service import get_figure_path, load_phase3_summary_results


def render_operating_regime_page() -> None:
    """Render the operating regime analysis page."""
    render_academic_disclaimer()

    st.title("⚙️ Operating Regime Analysis & The Normalization Problem")
    st.markdown(
        """
        A central scientific challenge in industrial and marine diagnostics is that **operational plant load** 
        (e.g., commanded ship speed $v$) introduces variance that dwarfs subtle equipment degradation signatures.
        """
    )

    # Core comparative metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        render_metric_card(
            "R1: All Telemetry",
            "ARI = 0.8769",
            "Clustering (k=9) directly recovers ship speed setpoints",
        )
    with col2:
        render_metric_card(
            "R2: Excluded Speed/Demand",
            "ARI = 0.8440",
            "Removing setpoints fails: physics couples speed into telemetry",
        )
    with col3:
        render_metric_card(
            "R5: Within-Speed Normalized",
            "ARI = 0.0002",
            "Speed variance eliminated; isolates degradation signals",
        )

    st.markdown("---")

    # Narrative explanation
    st.subheader("📊 Empirical Proof of Operating Speed Dominance")
    st.markdown(
        r"""
        In Phase 2, ANOVA diagnostics proved that commanded ship speed $v$ explains **99.33% of total sensor variance** 
        ($\eta^2 \ge 0.965$ across every individual sensor channel). 
        Furthermore, Principal Component Analysis showed that **PC1 accounts for 97.41% of variance**, representing the 
        1-dimensional steady-state plant load line.
        """
    )

    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("#### Variance Explained by Speed Regime")
        p2_fig = get_figure_path("phase2", "variance_by_operating_regime.png")
        if p2_fig.exists():
            st.image(str(p2_fig), caption="Eta-squared of ship speed across telemetry channels (Phase 2)", use_container_width=True)
        else:
            st.info("Figure variance_by_operating_regime.png not found.")

    with col_right:
        st.markdown("#### Speed Recovery Across Feature Representations")
        p3_fig = get_figure_path("phase3", "k_vs_speed_recovery_ari.png")
        if p3_fig.exists():
            st.image(str(p3_fig), caption="Clustering alignment with ship speed setpoints (ARI vs Speed) across R1..R5 (Phase 3)", use_container_width=True)
        else:
            st.info("Figure k_vs_speed_recovery_ari.png not found.")

    st.markdown("---")

    # Methodological Conclusion
    st.subheader("💡 Methodological Conclusion")
    st.info(
        "**Key Insight:** Simply dropping operating demand setpoints ($v$ and $lp$) is scientifically insufficient because "
        "turbomachinery physics tightly couples shaft speeds, pressures, and temperatures to commanded speed (ARI remains 0.8440). "
        "Only conditional within-regime normalization ($R5$) decouples the operating setpoint (ARI drops to 0.0002), "
        "allowing unsupervised algorithms to discover subtle degradation profiles without leaking ground-truth degradation labels."
    )
