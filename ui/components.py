"""Reusable UI components."""

import streamlit as st
from typing import Dict, List, Optional, Any

from config import COLORS
from analysis import PlayerProfile
from .styles import get_account_badge


def render_player_card(profile: PlayerProfile) -> None:
    """Render the main player info card."""
    
    badge = get_account_badge(profile.player_type)
    
    st.markdown(f"""
    <div class="player-card">
        <h2>{profile.display_name}{badge}</h2>
        <div class="subtitle">
            Combat {profile.combat_level} • {profile.total_level} Total • Build: {profile.build.title()}
        </div>
        
        <div class="archetype-badge">{profile.archetype}</div>
        <div class="archetype-description">{profile.archetype_description}</div>
        
        <div class="stat-grid">
            <div class="stat-item">
                <div class="stat-value">{profile.total_level:,}</div>
                <div class="stat-label">Total Level</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">{profile.total_experience:,}</div>
                <div class="stat-label">Total XP</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">{profile.ehp:,.1f}</div>
                <div class="stat-label">EHP</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">{profile.ehb:,.1f}</div>
                <div class="stat-label">EHB</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_data_coverage(coverage: str, snapshot_count: int) -> None:
    """Render data coverage indicator."""
    
    icon = "📊" if snapshot_count > 10 else "📉" if snapshot_count > 0 else "❓"
    
    st.markdown(f"""
    <div class="data-coverage">
        {icon} <strong>Historical Data:</strong> {coverage}
    </div>
    """, unsafe_allow_html=True)


def render_top_items(
    items: List[tuple],
    title: str,
    value_formatter: callable = lambda x: f"{x:,}",
    icon: str = "🏆"
) -> None:
    """Render a ranked list of items."""
    
    st.markdown(f"""
    <div class="section-header">
        <span style="font-size: 24px;">{icon}</span>
        <h3>{title}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    if not items:
        st.markdown("""
        <div style="color: #888; font-style: italic; padding: 20px;">
            No data available
        </div>
        """, unsafe_allow_html=True)
        return
    
    for name, value in items:
        display_name = name.replace("_", " ").title()
        st.markdown(f"""
        <div class="top-item">
            <span class="top-item-name">{display_name}</span>
            <span class="top-item-value">{value_formatter(value)}</span>
        </div>
        """, unsafe_allow_html=True)


def render_section_header(title: str, icon: str = "📊") -> None:
    """Render a section header with icon."""
    st.markdown(f"""
    <div class="section-header">
        <span style="font-size: 24px;">{icon}</span>
        <h3>{title}</h3>
    </div>
    """, unsafe_allow_html=True)


def format_xp(xp: int) -> str:
    """Format XP with appropriate suffix."""
    if xp >= 1_000_000_000:
        return f"{xp / 1_000_000_000:.2f}B"
    elif xp >= 1_000_000:
        return f"{xp / 1_000_000:.1f}M"
    elif xp >= 1_000:
        return f"{xp / 1_000:.1f}K"
    return str(xp)


def render_skill_table(skills: Dict[str, Any], category: Optional[str] = None) -> None:
    """Render a skill table, optionally filtered by category."""
    from config import SKILL_CATEGORIES
    
    # Determine which skills to show
    if category and category in SKILL_CATEGORIES:
        skill_names = SKILL_CATEGORIES[category]
    else:
        skill_names = [s for s in skills.keys() if s != "overall"]
    
    # Build table data
    rows = []
    for name in skill_names:
        if name in skills:
            s = skills[name]
            rows.append({
                "Skill": name.title(),
                "Level": s.level,
                "XP": s.experience,
                "Rank": s.rank if s.rank > 0 else "-",
            })
    
    if rows:
        import pandas as pd
        df = pd.DataFrame(rows)
        df["XP"] = df["XP"].apply(lambda x: f"{x:,}")
        df["Rank"] = df["Rank"].apply(lambda x: f"{x:,}" if isinstance(x, int) else x)
        st.dataframe(
            df,
            hide_index=True,
            use_container_width=True,
        )
    else:
        st.info("No skill data available")
