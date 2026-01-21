"""Skills Detail page - deep dive into skill data."""

import streamlit as st
from typing import Dict, Any

from config import SKILL_CATEGORIES, COLORS
from analysis import PlayerProfile
from ui.components import render_section_header, render_skill_table
from ui.charts import create_skill_distribution


def render_skills_page(profile: PlayerProfile) -> None:
    """Render detailed skills analysis page."""
    
    render_section_header("Skill Distribution", "📊")
    
    # Treemap showing XP distribution
    treemap_fig = create_skill_distribution(profile.skills)
    st.plotly_chart(treemap_fig, use_container_width=True, config={'displayModeBar': False})
    
    st.markdown("---")
    
    # Category breakdown
    render_section_header("Skills by Category", "📚")
    
    # Category selector
    categories = list(SKILL_CATEGORIES.keys())
    selected_category = st.selectbox(
        "Select category",
        options=["All Skills"] + categories,
        index=0,
    )
    
    # Display skill table
    if selected_category == "All Skills":
        render_skill_table(profile.skills)
    else:
        render_skill_table(profile.skills, selected_category)
    
    st.markdown("---")
    
    # XP summary by category
    render_section_header("Category XP Totals", "📈")
    
    col1, col2 = st.columns(2)
    
    category_colors = {
        "Combat": COLORS["combat"],
        "Gathering": COLORS["gathering"],
        "Artisan": COLORS["artisan"],
        "Support": COLORS["support"],
    }
    
    for i, (cat, xp) in enumerate(profile.skill_category_xp.items()):
        col = col1 if i % 2 == 0 else col2
        color = category_colors.get(cat, COLORS["muted"])
        
        with col:
            st.markdown(f"""
            <div style="
                background: {COLORS['surface']};
                border-left: 4px solid {color};
                padding: 16px;
                margin-bottom: 12px;
                border-radius: 0 8px 8px 0;
            ">
                <div style="color: {COLORS['muted']}; font-size: 12px; text-transform: uppercase;">
                    {cat}
                </div>
                <div style="color: {COLORS['text']}; font-size: 24px; font-weight: bold;">
                    {xp:,} XP
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Virtual levels info
    st.markdown("---")
    render_section_header("99+ Skills", "✨")
    
    maxed_skills = [
        (name, skill.virtual_level, skill.experience)
        for name, skill in profile.skills.items()
        if skill.level >= 99 and name != "overall"
    ]
    
    if maxed_skills:
        maxed_skills.sort(key=lambda x: x[2], reverse=True)
        
        cols = st.columns(4)
        for i, (name, vlvl, xp) in enumerate(maxed_skills):
            with cols[i % 4]:
                over_99 = f" ({vlvl})" if vlvl > 99 else ""
                st.markdown(f"""
                <div style="
                    text-align: center;
                    padding: 12px;
                    background: {COLORS['surface']};
                    border-radius: 8px;
                    margin-bottom: 8px;
                ">
                    <div style="color: {COLORS['primary']}; font-weight: bold;">
                        {name.title()}
                    </div>
                    <div style="color: {COLORS['text']}; font-size: 18px;">
                        99{over_99}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("No skills at level 99 yet. Keep grinding!")
