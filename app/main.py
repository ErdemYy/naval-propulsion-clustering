"""Streamlit local dashboard entrypoint.

This application provides an interactive interface for exploring naval gas turbine
sensor measurements, cluster projections, and post-hoc degradation correlations.
"""

from __future__ import annotations

import streamlit as st


def main() -> None:
    """Run the Streamlit interactive dashboard."""
    st.set_page_config(
        page_title="Naval Propulsion Clustering",
        page_icon="⚓",
        layout="wide",
    )

    st.title("⚓ Naval Propulsion Clustering")
    st.subheader(
        "Unsupervised Discovery of Operating and Performance Degradation Profiles "
        "in Naval Gas Turbine Propulsion Systems"
    )

    st.info(
        "Project Foundation Phase Active. Machine learning pipeline and interactive dashboard "
        "views will be connected during Phase 5 according to PROJECT_PLAN.md."
    )


if __name__ == "__main__":
    main()
