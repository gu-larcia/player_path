"""Bosses page - PvM activity analysis."""

import streamlit as st
from typing import Dict, Any

from config import BOSS_CATEGORIES, COLORS
from analysis import PlayerProfile
from ui.components import render_section_header
from ui.charts import create_boss_distribution


def render_bosses_page(profile: PlayerProfile) -> None:
    """Render detailed boss/PvM analysis page."""
    
    # Check if player has any boss KC
    total_kc = sum(b.kills for b in profile.bosses.values() if b.kills > 0)
    bosses_killed = len([b for b in profile.bosses.values() if b.kills > 0])
    
    if total_kc == 0:
        st.markdown("""
        <div style="
            text-align: center;
            padding: 60px 20px;
            color: #888;
        ">
            <div style="font-size: 48px; margin-bottom: 16px;">🏰</div>
            <div style="font-size: 20px; color: #E8E8E8; margin-bottom: 8px;">
                No Boss Kills Recorded
            </div>
            <p>This player hasn't killed any tracked bosses yet, or their data hasn't been updated.</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Summary stats
    render_section_header("PvM Summary", "⚔️")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Kill Count", f"{total_kc:,}")
    
    with col2:
        st.metric("Bosses Killed", bosses_killed)
    
    with col3:
        st.metric("EHB", f"{profile.ehb:,.1f}")
    
    st.markdown("---")
    
    # Top bosses chart
    render_section_header("Kill Count Breakdown", "💀")
    
    boss_chart = create_boss_distribution(profile.bosses, top_n=15)
    st.plotly_chart(boss_chart, use_container_width=True, config={'displayModeBar': False})
    
    st.markdown("---")
    
    # Boss categories breakdown
    render_section_header("Content Categories", "🗂️")
    
    for cat_name, boss_names in BOSS_CATEGORIES.items():
        cat_bosses = [
            (name, profile.bosses[name].kills)
            for name in boss_names
            if name in profile.bosses and profile.bosses[name].kills > 0
        ]
        
        if not cat_bosses:
            continue
        
        cat_bosses.sort(key=lambda x: x[1], reverse=True)
        cat_total = sum(kc for _, kc in cat_bosses)
        
        with st.expander(f"**{cat_name}** — {cat_total:,} total KC"):
            for boss_name, kc in cat_bosses:
                display_name = boss_name.replace("_", " ").title()
                pct = (kc / cat_total) * 100
                
                st.markdown(f"""
                <div style="
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    padding: 8px 0;
                    border-bottom: 1px solid {COLORS['surface']};
                ">
                    <span style="color: {COLORS['text']};">{display_name}</span>
                    <span style="color: {COLORS['primary']}; font-weight: bold;">
                        {kc:,} <span style="color: {COLORS['muted']}; font-weight: normal;">({pct:.1f}%)</span>
                    </span>
                </div>
                """, unsafe_allow_html=True)
    
    # Raid experience highlight
    st.markdown("---")
    render_section_header("Raid Experience", "🏆")
    
    raid_bosses = BOSS_CATEGORIES.get("Raids", [])
    raid_data = [
        (name, profile.bosses[name])
        for name in raid_bosses
        if name in profile.bosses and profile.bosses[name].kills > 0
    ]
    
    if raid_data:
        cols = st.columns(len(raid_data))
        
        raid_display_names = {
            "chambers_of_xeric": "CoX",
            "chambers_of_xeric_challenge_mode": "CoX CM",
            "theatre_of_blood": "ToB",
            "theatre_of_blood_hard_mode": "ToB HM",
            "tombs_of_amascut": "ToA",
            "tombs_of_amascut_expert": "ToA Expert",
        }
        
        for i, (name, boss) in enumerate(raid_data):
            display = raid_display_names.get(name, name.replace("_", " ").title())
            with cols[i]:
                st.markdown(f"""
                <div style="
                    text-align: center;
                    padding: 20px;
                    background: {COLORS['surface']};
                    border-radius: 12px;
                    border: 1px solid {COLORS['primary']}40;
                ">
                    <div style="
                        color: {COLORS['primary']};
                        font-size: 28px;
                        font-weight: bold;
                        font-family: 'Cinzel', serif;
                    ">
                        {boss.kills:,}
                    </div>
                    <div style="color: {COLORS['muted']}; font-size: 12px; margin-top: 4px;">
                        {display}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("No raid completions recorded. Time to form a team!")
