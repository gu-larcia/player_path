"""Skills Detail page - deep dive into skill data."""

import streamlit as st

from config import SKILL_CATEGORIES
from analysis import PlayerProfile
from ui.components import render_section_header, render_skill_table
from ui.charts import create_skill_distribution


def render_skills_page(profile: PlayerProfile) -> None:
    """Render detailed skills analysis page."""
    
    render_section_header("Skill Distribution", "📊")
    
    treemap_fig = create_skill_distribution(profile.skills)
    st.plotly_chart(treemap_fig, use_container_width=True, config={'displayModeBar': False})
    
    st.divider()
    
    render_section_header("Skills by Category", "📚")
    
    categories = list(SKILL_CATEGORIES.keys())
    selected_category = st.selectbox(
        "Select category",
        options=["All Skills"] + categories,
        index=0,
    )
    
    if selected_category == "All Skills":
        render_skill_table(profile.skills)
    else:
        render_skill_table(profile.skills, selected_category)
    
    st.divider()
    
    render_section_header("Category XP Totals", "📈")
    
    col1, col2 = st.columns(2)
    
    for i, (cat, xp) in enumerate(profile.skill_category_xp.items()):
        col = col1 if i % 2 == 0 else col2
        with col:
            st.metric(cat, f"{xp:,} XP")
    
    st.divider()
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
                st.metric(name.title(), f"99{over_99}")
    else:
        st.info("No skills at level 99 yet. Keep grinding!")
