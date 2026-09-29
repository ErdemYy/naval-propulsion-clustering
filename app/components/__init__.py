"""Streamlit application UI components."""

from app.components.degradation_map import render_degradation_map_page
from app.components.degradation_profiles import (
    render_multicomponent_profile_page,
    render_primary_profile_page,
)
from app.components.methodology import render_methodology_page
from app.components.model_comparison import render_model_comparison_page
from app.components.observation_analysis import render_observation_analysis_page
from app.components.operating_regime import render_operating_regime_page
from app.components.overview import render_overview_page
from app.components.shared import (
    apply_academic_styling,
    render_academic_disclaimer,
    render_metric_card,
)

__all__ = [
    "apply_academic_styling",
    "render_academic_disclaimer",
    "render_degradation_map_page",
    "render_methodology_page",
    "render_metric_card",
    "render_model_comparison_page",
    "render_multicomponent_profile_page",
    "render_observation_analysis_page",
    "render_operating_regime_page",
    "render_overview_page",
    "render_primary_profile_page",
]
