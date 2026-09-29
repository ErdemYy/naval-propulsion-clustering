"""Shared UI components, styling, and academic disclaimer banners for Streamlit."""

from __future__ import annotations

import streamlit as st


def apply_academic_styling() -> None:
    """Inject custom CSS for dark navy technical academic dashboard aesthetic."""
    st.markdown(
        """
        <style>
        /* Base typography & container aesthetics */
        .main .block-container {
            padding-top: 1.5rem;
            padding-bottom: 2rem;
            max-width: 1200px;
        }
        
        /* Metric card styling */
        .metric-card {
            background-color: #0f1c2e;
            border: 1px solid #1e3a5f;
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 12px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.15);
        }
        .metric-card-title {
            font-size: 0.82rem;
            color: #8da4c4;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 6px;
        }
        .metric-card-value {
            font-size: 1.6rem;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 4px;
        }
        .metric-card-subtitle {
            font-size: 0.8rem;
            color: #5c7a9c;
        }
        
        /* Academic disclaimer banner */
        .academic-banner {
            background-color: #14233c;
            border-left: 4px solid #3b82f6;
            padding: 10px 16px;
            border-radius: 4px;
            font-size: 0.85rem;
            color: #c9d8eb;
            margin-bottom: 18px;
        }
        
        /* Warning banner */
        .warning-banner {
            background-color: #2a1b14;
            border-left: 4px solid #f97316;
            padding: 10px 16px;
            border-radius: 4px;
            font-size: 0.85rem;
            color: #fed7aa;
            margin-bottom: 18px;
        }

        /* Profile highlight pill */
        .profile-pill {
            display: inline-block;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 0.8rem;
            font-weight: 600;
            margin-right: 6px;
            margin-bottom: 6px;
        }
        .pill-blue { background-color: #1e3a8a; color: #93c5fd; }
        .pill-orange { background-color: #7c2d12; color: #fdba74; }
        .pill-purple { background-color: #4c1d95; color: #d8b4fe; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_academic_disclaimer() -> None:
    """Render prominent academic scope banner to prevent operational deployment misinterpretations."""
    st.markdown(
        """
        <div class="academic-banner">
            <strong>🎓 Academic Decision-Support Tool:</strong> This application is a local university research 
            demonstration evaluating unsupervised machine learning on numerical simulation telemetry. 
            It does <strong>NOT</strong> predict future failure, diagnose active faults, or monitor live vessels in real time.
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_metric_card(title: str, value: str, subtitle: str = "") -> None:
    """Render a styled technical metric card."""
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-card-title">{title}</div>
            <div class="metric-card-value">{value}</div>
            <div class="metric-card-subtitle">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
