"""Player Profile page - main profile view."""

import streamlit as st
from typing import Dict, Any

from analysis import PlayerProfile
from ui.components import (
    render_player_card,
    render_data_coverage,
    render_top_items,
    render_section_header,
    format_xp,
)
from ui.charts import (
    create_skill_radar,
    create_playstyle_bars,
    create_ehp_ehb_display,
)


def render_profile_page(
    profile: PlayerProfile,
    journey_data: Dict[str, Any],
) -> None:
    """Render the main player profile page."""
    
    # Player card at top
    render_player_card(profile)
    
    # Data coverage notice
    render_data_coverage(
        journey_data.get("data_coverage", "Unknown"),
        journey_data.get("snapshot_count", 0)
    )
    
    st.divider()
    
    # Two-column layout for core visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        render_section_header("Skill Balance", "⚖️")
        radar_fig = create_skill_radar(profile.skills)
        st.plotly_chart(radar_fig, use_container_width=True, config={'displayModeBar': False})
    
    with col2:
        render_section_header("Playstyle Profile", "🎯")
        bars_fig = create_playstyle_bars(profile.playstyle_scores)
        st.plotly_chart(bars_fig, use_container_width=True, config={'displayModeBar': False})
    
    st.divider()
    
    # EHP/EHB display
    render_section_header("Efficiency Metrics", "⏱️")
    efficiency_fig = create_ehp_ehb_display(profile.ehp, profile.ehb)
    st.plotly_chart(efficiency_fig, use_container_width=True, config={'displayModeBar': False})
    
    st.divider()
    
    # Top skills and bosses side by side
    col1, col2 = st.columns(2)
    
    with col1:
        render_top_items(
            profile.top_skills,
            "Top Skills",
            value_formatter=format_xp,
            icon="📚"
        )
    
    with col2:
        render_top_items(
            profile.top_bosses,
            "Top Bosses",
            value_formatter=lambda x: f"{x:,} KC",
            icon="💀"
        )
