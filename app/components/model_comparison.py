"""Model comparison component providing formal side-by-side evaluation."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from app.components.shared import render_academic_disclaimer, render_metric_card
from app.services.data_service import get_figure_path, load_phase4_validation_results


def render_model_comparison_page() -> None:
    """Render the formal model comparison page."""
    render_academic_disclaimer()

    st.title("⚖️ Formal Candidate Comparison & Evaluation Matrix")
    st.markdown(
        """
        Following Phase 4 scientific validation, the two candidate configurations were compared across 
        intrinsic clustering separation, operational independence, resampling stability, and post-hoc degradation recovery.
        No artificial composite scoring is applied; the decision is grounded in empirical trade-offs.
        """
    )

    # Formal Comparison Table
    comparison_data = [
        {
            "Metric / Criterion": "Number of Clusters (k)",
            "Candidate A (Primary Baseline)": "2",
            "Candidate B (Secondary Diagnostic)": "3",
            "Scientific Implication": "A is parsimonious; B offers component resolution.",
        },
        {
            "Metric / Criterion": "Designated Role",
            "Candidate A (Primary Baseline)": "Primary Scientific Model",
            "Candidate B (Secondary Diagnostic)": "Secondary Multi-Component Model",
            "Scientific Implication": "A for binary degradation; B for component dissociation.",
        },
        {
            "Metric / Criterion": "Silhouette Coefficient",
            "Candidate A (Primary Baseline)": "0.2813",
            "Candidate B (Secondary Diagnostic)": "0.2593",
            "Scientific Implication": "A achieves superior geometric cluster cohesion (+0.022).",
        },
        {
            "Metric / Criterion": "Davies-Bouldin Index",
            "Candidate A (Primary Baseline)": "1.3917",
            "Candidate B (Secondary Diagnostic)": "1.2918",
            "Scientific Implication": "Both exhibit solid cluster separation (< 1.50).",
        },
        {
            "Metric / Criterion": "Calinski-Harabasz Index",
            "Candidate A (Primary Baseline)": "5543.4",
            "Candidate B (Secondary Diagnostic)": "4889.7",
            "Scientific Implication": "A achieves higher between-to-within variance ratio.",
        },
        {
            "Metric / Criterion": "Operating Speed Independence (ARI vs v)",
            "Candidate A (Primary Baseline)": "0.0002",
            "Candidate B (Secondary Diagnostic)": "0.0064",
            "Scientific Implication": "Both successfully decouple operating speed setpoints.",
        },
        {
            "Metric / Criterion": "Operating Speed Invariance (Cramér's V)",
            "Candidate A (Primary Baseline)": "0.0418 (Negligible)",
            "Candidate B (Secondary Diagnostic)": "0.1273 (Small)",
            "Scientific Implication": "A is invariant across all 9 speeds (std = 2.2%).",
        },
        {
            "Metric / Criterion": "Bootstrap Stability (Mean ARI, B=100)",
            "Candidate A (Primary Baseline)": "0.9844 [95% CI: 0.970–0.998]",
            "Candidate B (Secondary Diagnostic)": "0.9434 [95% CI: 0.792–0.990]",
            "Scientific Implication": "A is exceptionally deterministic under sample perturbation.",
        },
        {
            "Metric / Criterion": "Compressor Decay Signal (kMc eta-squared)",
            "Candidate A (Primary Baseline)": "0.4459 (Large)",
            "Candidate B (Secondary Diagnostic)": "0.5109 (Large)",
            "Scientific Implication": "B captures slightly higher compressor degradation variance.",
        },
        {
            "Metric / Criterion": "Turbine Decay Signal (kMt eta-squared)",
            "Candidate A (Primary Baseline)": "0.0131 (Negligible)",
            "Candidate B (Secondary Diagnostic)": "0.3007 (Large)",
            "Scientific Implication": "B successfully discovers turbine decay; A misses it.",
        },
        {
            "Metric / Criterion": "Turbine Decay Pairwise Cliff's Delta",
            "Candidate A (Primary Baseline)": "+0.1321 (Negligible)",
            "Candidate B (Secondary Diagnostic)": "-0.7673 (Large: Clust 0 vs 1)",
            "Scientific Implication": "B achieves strong non-parametric turbine dissociation.",
        },
    ]

    df_comp = pd.DataFrame(comparison_data)
    st.table(df_comp.set_index("Metric / Criterion"))

    st.markdown("---")

    # Bootstrap Stability Distribution Comparison Figure
    st.subheader("📊 Bootstrap Resampling Stability Distribution (B=100)")
    boot_fig = get_figure_path("phase4", "bootstrap_stability_distribution.png")
    if boot_fig.exists():
        st.image(str(boot_fig), caption="Empirical bootstrap ARI distributions for Candidate A (k=2) vs Candidate B (k=3)", use_container_width=True)
    else:
        st.info("Figure bootstrap_stability_distribution.png not found.")

    st.markdown("---")

    # Decision Rationale
    st.subheader("🎓 Scientific Selection Justification")
    st.markdown(
        r"""
        1. **Why Candidate A is the Primary Model:**  
           Applying Occam's razor, Candidate A ($k=2$) provides the most parsimonious description of the primary 
           thermodynamic failure mode (compressor fouling/decay). It achieves the highest intrinsic silhouette score (0.2813), 
           near-zero operating speed correlation (ARI = 0.0002), and outstanding bootstrap stability (0.9844).
        2. **Why Candidate B is Retained as Secondary Model:**  
           For investigations requiring multi-component diagnostic resolution, Candidate B ($k=3$) is mathematically justified. 
           It captures both compressor ($\eta^2 = 0.511$) and turbine decay ($\eta^2 = 0.301$), isolating turbine-degraded 
           states that remain concealed within the binary solution.
        """
    )
