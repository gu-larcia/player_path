"""Bosses page - PvM activity analysis."""

import streamlit as st

from config import BOSS_CATEGORIES
from analysis import PlayerProfile
from ui.components import render_section_header
from ui.charts import create_boss_distribution


def render_bosses_page(profile: PlayerProfile) -> None:
    """Render detailed boss/PvM analysis page."""
    
    total_kc = sum(b.kills for b in profile.bosses.values() if b.kills > 0)
    bosses_killed = len([b for b in profile.bosses.values() if b.kills > 0])
    
    if total_kc == 0:
        st.warning("🏰 **No Boss Kills Recorded**")
        st.caption("This player hasn't killed any tracked bosses yet, or their data hasn't been updated.")
        return
    
    render_section_header("PvM Summary", "⚔️")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Kill Count", f"{total_kc:,}")
    col2.metric("Bosses Killed", bosses_killed)
    col3.metric("EHB", f"{profile.ehb:,.1f}")
    
    st.divider()
    
    render_section_header("Kill Count Breakdown", "💀")
    
    boss_chart = create_boss_distribution(profile.bosses, top_n=15)
    st.plotly_chart(boss_chart, use_container_width=True, config={'displayModeBar': False})
    
    st.divider()
    
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
                col1, col2 = st.columns([3, 1])
                col1.write(display_name)
                col2.write(f"**{kc:,}** ({pct:.1f}%)")
    
    st.divider()
    render_section_header("Raid Experience", "🏆")
    
    raid_bosses = BOSS_CATEGORIES.get("Raids", [])
    raid_data = [
        (name, profile.bosses[name])
        for name in raid_bosses
        if name in profile.bosses and profile.bosses[name].kills > 0
    ]
    
    if raid_data:
        raid_display_names = {
            "chambers_of_xeric": "CoX",
            "chambers_of_xeric_challenge_mode": "CoX CM",
            "theatre_of_blood": "ToB",
            "theatre_of_blood_hard_mode": "ToB HM",
            "tombs_of_amascut": "ToA",
            "tombs_of_amascut_expert": "ToA Expert",
        }
        
        cols = st.columns(len(raid_data))
        for i, (name, boss) in enumerate(raid_data):
            display = raid_display_names.get(name, name.replace("_", " ").title())
            with cols[i]:
                st.metric(display, f"{boss.kills:,}")
    else:
        st.info("No raid completions recorded. Time to form a team!")
