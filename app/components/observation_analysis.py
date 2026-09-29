"""Interactive new observation analysis and profile assignment component."""

from __future__ import annotations

from typing import Any
import numpy as np
import pandas as pd
import streamlit as st

from app.components.shared import render_academic_disclaimer, render_metric_card
from app.services.data_service import get_demo_observations, load_cached_dataset
from app.services.inference_service import (
    REQUIRED_TELEMETRY,
    VALID_SPEEDS,
    assign_observation_profile,
)


def render_observation_analysis_page() -> None:
    """Render the observation analysis and demonstration component."""
    render_academic_disclaimer()

    st.title("🔍 New Observation Profile Assignment")
    st.markdown(
        """
        Evaluate any multivariate telemetry observation against the learned clustering models.
        The observation is conditionally normalized using the serialized `OperatingRegimeNormalizer` 
        and assigned to its **closest learned profile** based on Euclidean distance to cluster centroids.
        """
    )

    st.markdown(
        """
        <div class="academic-banner">
            <strong>🔒 Anti-Leakage Protocol:</strong> Only commanded speed ($v$) and the 11 clustering-eligible 
            telemetry channels are accepted. Reference degradation coefficients ($kMc, kMt$) are 
            <strong>never requested</strong> or utilized during inference.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Demo Presets / Example Loader
    demo_cases = get_demo_observations()
    st.subheader("💡 Load Demonstration Preset (Recommended for Live Demo)")

    col_btn1, col_btn2, col_btn3 = st.columns(3)
    preset_choice = None

    with col_btn1:
        if st.button("Load Case 1: Nominal Baseline", use_container_width=True):
            preset_choice = "nominal"
    with col_btn2:
        if st.button("Load Case 2: Compressor Decay", use_container_width=True):
            preset_choice = "compressor_decay"
    with col_btn3:
        if st.button("Load Case 3: Turbine Decay", use_container_width=True):
            preset_choice = "turbine_decay"

    # Maintain session state for input fields
    if "observation_inputs" not in st.session_state:
        st.session_state.observation_inputs = demo_cases["nominal"]["inputs"].copy()
        st.session_state.current_preset = "nominal"

    if preset_choice:
        st.session_state.observation_inputs = demo_cases[preset_choice]["inputs"].copy()
        st.session_state.current_preset = preset_choice
        st.success(f"Loaded: {demo_cases[preset_choice]['label']}")

    st.markdown("---")

    # Model and Speed Selection
    col_sel1, col_sel2 = st.columns(2)
    with col_sel1:
        model_mode = st.radio(
            "Evaluation Model:",
            options=["Primary Scientific Model (K=2)", "Secondary Diagnostic Model (K=3)"],
            index=0,
            horizontal=True,
        )
        model_key = "k2" if "K=2" in model_mode else "k3"

    with col_sel2:
        current_v = float(st.session_state.observation_inputs.get("v", 18.0))
        speed_idx = VALID_SPEEDS.index(current_v) if current_v in VALID_SPEEDS else 5
        selected_speed = st.selectbox(
            "Commanded Ship Speed (v) [knots]:",
            options=VALID_SPEEDS,
            index=speed_idx,
            help="Conditioning variable required for within-speed normalization.",
        )
        st.session_state.observation_inputs["v"] = float(selected_speed)

    st.markdown("### 🎛️ Telemetry Feature Values")
    st.caption("Adjust or inspect the 11 clustering-eligible telemetry sensors:")

    # 11 telemetry input fields in 3 columns
    telemetry_cols = list(REQUIRED_TELEMETRY)
    c1, c2, c3 = st.columns(3)

    input_values: dict[str, float] = {"v": float(selected_speed)}

    for idx, feat in enumerate(telemetry_cols):
        target_col = c1 if idx % 3 == 0 else (c2 if idx % 3 == 1 else c3)
        val = float(st.session_state.observation_inputs.get(feat, 0.0))
        with target_col:
            new_val = st.number_input(
                f"{feat}",
                value=val,
                format="%.3f",
                key=f"input_{feat}",
            )
            input_values[feat] = float(new_val)
            st.session_state.observation_inputs[feat] = float(new_val)

    st.markdown("---")

    # Assignment Execution
    if st.button("🚀 Analyze Observation & Assign Profile", type="primary", use_container_width=True):
        try:
            result = assign_observation_profile(input_values, model_choice=model_key)
            
            st.subheader("🎯 Assignment Result")

            res_c1, res_c2 = st.columns([1, 1.2])

            with res_c1:
                render_metric_card(
                    "Closest Learned Profile",
                    f"Cluster {result['assigned_cluster']}",
                    result["closest_profile_name"],
                )
                render_metric_card(
                    "Distance to Centroid (L2)",
                    f"{result['centroid_distance']:.4f}",
                    f"Distances: {', '.join([f'C{k}: {v:.2f}' for k, v in result['all_distances'].items()])}",
                )

            with res_c2:
                st.markdown(
                    f"""
                    <div class="metric-card" style="border-left: 4px solid #10b981;">
                        <div class="metric-card-title">Thermodynamic Profile Characterization</div>
                        <div style="font-size: 0.95rem; color: #e2e8f0; line-height: 1.5; margin-top: 6px;">
                            {result['profile_description']}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            # Post-hoc Ground-Truth Verification (Only if loaded from preset)
            current_preset_key = st.session_state.get("current_preset")
            if current_preset_key and current_preset_key in demo_cases:
                gt_ref = demo_cases[current_preset_key]["ground_truth_reference"]
                st.markdown("#### 🔬 Post-Hoc Ground-Truth Benchmark (Reference Only)")
                gt_c1, gt_c2, gt_c3 = st.columns(3)
                with gt_c1:
                    render_metric_card("True Reference kMc", f"{gt_ref['kMc']:.3f}", "Compressor Decay State")
                with gt_c2:
                    render_metric_card("True Reference kMt", f"{gt_ref['kMt']:.3f}", "Turbine Decay State")
                with gt_c3:
                    st.info(
                        "**Scientific Validation:** These reference labels were quarantined and revealed strictly "
                        "post-assignment to verify whether the unsupervised clustering assignment agrees with true degradation."
                    )

            # Standardized z-score deviation plot
            st.markdown("#### Normalized Residual Vector (z-scores relative to speed setpoint)")
            df_z = pd.DataFrame({
                "Feature": list(result["normalized_features"].keys()),
                "Standardized Deviation (z)": list(result["normalized_features"].values()),
            })
            st.bar_chart(df_z.set_index("Feature"))

        except Exception as e:
            st.error(f"Inference error: {e}")
