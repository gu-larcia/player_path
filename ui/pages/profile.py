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
    create_ehp_ehb_gauge,
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
    
    # EHP/EHB gauges
    render_section_header("Efficiency Metrics", "⏱️")
    gauge_fig = create_ehp_ehb_gauge(profile.ehp, profile.ehb)
    st.plotly_chart(gauge_fig, use_container_width=True, config={'displayModeBar': False})
    
    # Efficiency explanation
    with st.expander("What are EHP and EHB?"):
        st.markdown("""
**EHP (Efficient Hours Played)** estimates how many hours you've spent training skills,
assuming optimal methods. Higher EHP indicates more time spent skilling.

**EHB (Efficient Hours Bossed)** estimates how many hours you've spent killing bosses,
based on expected kills per hour at each boss. Higher EHB indicates more PvM experience.

The ratio of EHP to EHB helps determine your playstyle orientation:
- **High EHP, Low EHB** → Skiller-oriented
- **Low EHP, High EHB** → PvM-oriented
- **Balanced** → All-rounder
""")
    
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
