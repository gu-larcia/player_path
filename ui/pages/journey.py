"""Journey page - historical progression analysis."""

import streamlit as st
from typing import Dict, Any

from analysis import PlayerProfile
from ui.components import render_section_header, render_data_coverage
from ui.charts import create_journey_timeline


def render_journey_page(
    profile: PlayerProfile,
    journey_data: Dict[str, Any],
) -> None:
    """Render historical progression analysis page."""
    
    timeline = journey_data.get("timeline", [])
    milestones = journey_data.get("milestones", [])
    coverage = journey_data.get("data_coverage", "Unknown")
    snapshot_count = journey_data.get("snapshot_count", 0)
    
    render_data_coverage(coverage, snapshot_count)
    
    if snapshot_count < 2:
        st.warning("📈 **Limited Historical Data**")
        st.caption(
            "Journey visualization requires multiple snapshots over time. "
            "This player's WiseOldMan profile doesn't have enough historical data yet."
        )
        
        with st.expander("How to get more data"):
            st.write(
                "Historical snapshots are created when the player is tracked via the "
                "RuneLite plugin or when their profile is updated on WiseOldMan."
            )
        
        render_section_header("Current Snapshot", "📸")
        render_current_snapshot(profile)
        return
    
    render_section_header("Progression Timeline", "📈")
    
    timeline_fig = create_journey_timeline(timeline, milestones)
    st.plotly_chart(timeline_fig, use_container_width=True, config={'displayModeBar': False})
    
    if milestones:
        render_section_header("Milestones Detected", "🏅")
        
        for m in sorted(milestones, key=lambda x: x["date"], reverse=True):
            date_str = m["date"].strftime("%Y-%m-%d")
            col1, col2 = st.columns([1, 3])
            col1.caption(date_str)
            col2.write(m['description'])
    
    if len(timeline) >= 2:
        render_section_header("Progress Summary", "📊")
        
        first = timeline[0]
        last = timeline[-1]
        
        level_gain = last["total_level"] - first["total_level"]
        xp_gain = last["total_xp"] - first["total_xp"]
        ehp_gain = last["ehp"] - first["ehp"]
        ehb_gain = last["ehb"] - first["ehb"]
        
        days = (last["date"] - first["date"]).days
        
        col1, col2, col3, col4 = st.columns(4)
        
        col1.metric(
            "Total Levels",
            f"+{level_gain:,}" if level_gain >= 0 else str(level_gain),
            delta=f"over {days} days"
        )
        
        if xp_gain >= 1_000_000:
            xp_str = f"+{xp_gain/1_000_000:.1f}M"
        else:
            xp_str = f"+{xp_gain:,}"
        col2.metric("Total XP", xp_str)
        
        col3.metric("EHP Gained", f"+{ehp_gain:.1f}")
        col4.metric("EHB Gained", f"+{ehb_gain:.1f}")
        
        if days > 0:
            st.divider()
            st.write(f"**Daily Averages** (over {days} days)")
            
            col1, col2, col3 = st.columns(3)
            
            daily_xp = xp_gain / days
            if daily_xp >= 1_000_000:
                col1.write(f"📊 XP/day: **{daily_xp/1_000_000:.2f}M**")
            else:
                col1.write(f"📊 XP/day: **{daily_xp:,.0f}**")
            
            col2.write(f"⏱️ EHP/day: **{ehp_gain/days:.2f}**")
            col3.write(f"⚔️ EHB/day: **{ehb_gain/days:.2f}**")


def render_current_snapshot(profile: PlayerProfile) -> None:
    """Render current snapshot summary when no history available."""
    
    col1, col2 = st.columns(2)
    col1.metric("Total Level", f"{profile.total_level:,}")
    col2.metric("Total XP", f"{profile.total_experience:,}")
    
    if profile.last_updated:
        st.caption(f"Last updated: {profile.last_updated.strftime('%Y-%m-%d %H:%M')} UTC")
