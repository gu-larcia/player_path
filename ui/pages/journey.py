"""Journey page - historical progression analysis."""

import streamlit as st
from typing import Dict, Any, List

from config import COLORS
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
    
    # Data availability notice
    render_data_coverage(coverage, snapshot_count)
    
    if snapshot_count < 2:
        st.markdown(f"""
        <div style="
            text-align: center;
            padding: 60px 20px;
            background: {COLORS['surface']};
            border-radius: 12px;
            margin: 20px 0;
        ">
            <div style="font-size: 48px; margin-bottom: 16px;">📈</div>
            <div style="font-size: 20px; color: {COLORS['text']}; margin-bottom: 8px;">
                Limited Historical Data
            </div>
            <p style="color: {COLORS['muted']}; max-width: 500px; margin: 0 auto;">
                Journey visualization requires multiple snapshots over time. 
                This player's WiseOldMan profile doesn't have enough historical data yet.
            </p>
            <div style="margin-top: 20px; padding: 16px; background: {COLORS['background']}; border-radius: 8px;">
                <div style="color: {COLORS['muted']}; font-size: 13px;">
                    <strong>How to get more data:</strong><br>
                    Historical snapshots are created when the player is tracked via the 
                    RuneLite plugin or when their profile is updated on WiseOldMan.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Still show current stats summary
        render_section_header("Current Snapshot", "📸")
        render_current_snapshot(profile)
        return
    
    # Timeline visualization
    render_section_header("Progression Timeline", "📈")
    
    timeline_fig = create_journey_timeline(timeline, milestones)
    st.plotly_chart(timeline_fig, use_container_width=True, config={'displayModeBar': False})
    
    # Milestones list
    if milestones:
        render_section_header("Milestones Detected", "🏅")
        
        for m in sorted(milestones, key=lambda x: x["date"], reverse=True):
            date_str = m["date"].strftime("%Y-%m-%d")
            st.markdown(f"""
            <div style="
                display: flex;
                align-items: center;
                padding: 12px 16px;
                background: {COLORS['surface']};
                border-radius: 8px;
                margin-bottom: 8px;
                border-left: 3px solid {COLORS['primary']};
            ">
                <div style="color: {COLORS['muted']}; width: 100px; font-size: 13px;">
                    {date_str}
                </div>
                <div style="color: {COLORS['text']};">
                    {m['description']}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Gains summary
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
        
        with col1:
            st.metric(
                "Total Levels",
                f"+{level_gain:,}" if level_gain >= 0 else str(level_gain),
                delta=f"over {days} days"
            )
        
        with col2:
            if xp_gain >= 1_000_000:
                xp_str = f"+{xp_gain/1_000_000:.1f}M"
            else:
                xp_str = f"+{xp_gain:,}"
            st.metric("Total XP", xp_str)
        
        with col3:
            st.metric("EHP Gained", f"+{ehp_gain:.1f}")
        
        with col4:
            st.metric("EHB Gained", f"+{ehb_gain:.1f}")
        
        # Daily averages
        if days > 0:
            st.markdown("---")
            st.markdown(f"**Daily Averages** (over {days} days)")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                daily_xp = xp_gain / days
                if daily_xp >= 1_000_000:
                    st.write(f"📊 XP/day: **{daily_xp/1_000_000:.2f}M**")
                else:
                    st.write(f"📊 XP/day: **{daily_xp:,.0f}**")
            
            with col2:
                st.write(f"⏱️ EHP/day: **{ehp_gain/days:.2f}**")
            
            with col3:
                st.write(f"⚔️ EHB/day: **{ehb_gain/days:.2f}**")


def render_current_snapshot(profile: PlayerProfile) -> None:
    """Render current snapshot summary when no history available."""
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div style="
            background: {COLORS['surface']};
            padding: 20px;
            border-radius: 8px;
        ">
            <div style="color: {COLORS['muted']}; font-size: 12px; text-transform: uppercase;">
                Total Level
            </div>
            <div style="color: {COLORS['text']}; font-size: 32px; font-weight: bold;">
                {profile.total_level:,}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="
            background: {COLORS['surface']};
            padding: 20px;
            border-radius: 8px;
        ">
            <div style="color: {COLORS['muted']}; font-size: 12px; text-transform: uppercase;">
                Total XP
            </div>
            <div style="color: {COLORS['text']}; font-size: 32px; font-weight: bold;">
                {profile.total_experience:,}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    if profile.last_updated:
        st.caption(f"Last updated: {profile.last_updated.strftime('%Y-%m-%d %H:%M')} UTC")
