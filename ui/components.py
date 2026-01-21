"""Reusable UI components."""

import streamlit as st
from typing import Dict, List, Optional, Any

from config import COLORS
from analysis import PlayerProfile


def render_player_card(profile: PlayerProfile) -> None:
    """Render the main player info card using native Streamlit components."""
    
    # Account type badge
    badge = ""
    if profile.player_type and profile.player_type != "regular":
        badge = f" • {profile.player_type.replace('_', ' ').title()}"
    
    # Header
    st.subheader(f"{profile.display_name}{badge}")
    st.caption(f"Combat {profile.combat_level} • {profile.total_level} Total • Build: {profile.build.title()}")
    
    # Archetype
    st.info(f"**{profile.archetype}** — {profile.archetype_description}")
    
    # Stats in columns
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Level", f"{profile.total_level:,}")
    col2.metric("Total XP", f"{profile.total_experience:,}")
    col3.metric("EHP", f"{profile.ehp:,.1f}")
    col4.metric("EHB", f"{profile.ehb:,.1f}")


def render_data_coverage(coverage: str, snapshot_count: int) -> None:
    """Render data coverage indicator."""
    icon = "📊" if snapshot_count > 10 else "📉" if snapshot_count > 0 else "❓"
    st.caption(f"{icon} **Historical Data:** {coverage}")


def render_top_items(
    items: List[tuple],
    title: str,
    value_formatter: callable = lambda x: f"{x:,}",
    icon: str = "🏆"
) -> None:
    """Render a ranked list of items."""
    
    st.subheader(f"{icon} {title}")
    
    if not items:
        st.caption("No data available")
        return
    
    for name, value in items:
        display_name = name.replace("_", " ").title()
        col1, col2 = st.columns([3, 1])
        col1.write(display_name)
        col2.write(f"**{value_formatter(value)}**")


def render_section_header(title: str, icon: str = "📊") -> None:
    """Render a section header with icon."""
    st.subheader(f"{icon} {title}")


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
    
    if category and category in SKILL_CATEGORIES:
        skill_names = SKILL_CATEGORIES[category]
    else:
        skill_names = [s for s in skills.keys() if s != "overall"]
    
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
        st.dataframe(df, hide_index=True, use_container_width=True)
    else:
        st.info("No skill data available")
