"""Custom CSS styles for the dashboard."""

from config import COLORS

# Convert hex colors to rgba for transparency support
def hex_to_rgba(hex_color: str, alpha: float) -> str:
    """Convert hex color to rgba string."""
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return f"rgba({r}, {g}, {b}, {alpha})"

# Pre-compute rgba values
PRIMARY_20 = hex_to_rgba(COLORS['primary'], 0.2)
PRIMARY_40 = hex_to_rgba(COLORS['primary'], 0.4)
SECONDARY_40 = hex_to_rgba(COLORS['secondary'], 0.4)
MUTED_30 = hex_to_rgba(COLORS['muted'], 0.3)

CUSTOM_CSS = f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Nunito:wght@300;400;600;700&display=swap');
    
    .stApp {{
        font-family: 'Nunito', sans-serif;
    }}
    
    h1, h2, h3 {{
        font-family: 'Cinzel', serif !important;
        color: {COLORS['primary']} !important;
    }}
    
    .player-card {{
        background: linear-gradient(145deg, {COLORS['surface']} 0%, {COLORS['background']} 100%);
        border: 1px solid {PRIMARY_40};
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }}
    
    .archetype-badge {{
        display: inline-block;
        background: linear-gradient(135deg, {PRIMARY_20} 0%, {COLORS['secondary']} 100%);
        border: 1px solid {COLORS['primary']};
        border-radius: 20px;
        padding: 8px 20px;
        font-family: 'Cinzel', serif;
        font-weight: 600;
        font-size: 16px;
        color: {COLORS['primary']};
        margin: 12px 0;
    }}
    
    .archetype-description {{
        color: {COLORS['muted']};
        font-style: italic;
        font-size: 13px;
    }}
    
    .stat-grid {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 16px;
        margin-top: 20px;
    }}
    
    .stat-item {{
        text-align: center;
        padding: 16px;
        background: {COLORS['background']};
        border-radius: 8px;
        border: 1px solid {COLORS['surface']};
    }}
    
    .stat-value {{
        font-size: 24px;
        font-weight: 700;
        color: {COLORS['text']};
        font-family: 'Cinzel', serif;
    }}
    
    .stat-label {{
        font-size: 12px;
        color: {COLORS['muted']};
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 4px;
    }}
    
    .section-header {{
        display: flex;
        align-items: center;
        gap: 12px;
        margin: 32px 0 16px 0;
        padding-bottom: 8px;
        border-bottom: 2px solid {PRIMARY_40};
    }}
    
    .section-header h3 {{
        margin: 0;
        font-size: 20px;
    }}
    
    .data-coverage {{
        background: {SECONDARY_40};
        border-left: 3px solid {COLORS['primary']};
        padding: 12px 16px;
        border-radius: 0 8px 8px 0;
        margin: 16px 0;
        font-size: 13px;
        color: {COLORS['muted']};
    }}
    
    .top-item {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 12px 16px;
        background: {COLORS['surface']};
        border-radius: 6px;
        margin-bottom: 8px;
        border-left: 3px solid {COLORS['primary']};
    }}
    
    .top-item-name {{
        font-weight: 600;
        color: {COLORS['text']};
    }}
    
    .top-item-value {{
        font-family: 'Cinzel', serif;
        font-weight: 700;
        color: {COLORS['primary']};
    }}
    
    .empty-state {{
        text-align: center;
        padding: 60px 20px;
        color: {COLORS['muted']};
    }}
    
    .empty-state-icon {{
        font-size: 48px;
        margin-bottom: 16px;
    }}
    
    .empty-state-title {{
        font-family: 'Cinzel', serif;
        font-size: 20px;
        color: {COLORS['text']};
        margin-bottom: 8px;
    }}
    
    .account-badge {{
        display: inline-block;
        padding: 4px 10px;
        border-radius: 4px;
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        margin-left: 8px;
    }}
    
    .account-badge.ironman {{ background: #808080; color: white; }}
    .account-badge.hardcore {{ background: #8B0000; color: white; }}
    .account-badge.ultimate {{ background: #1a1a1a; color: #808080; border: 1px solid #808080; }}
    .account-badge.group {{ background: #006400; color: white; }}
</style>
"""


def render_empty_state(title: str, message: str, icon: str = "📭") -> str:
    """Render an empty state message."""
    return f"""
    <div class="empty-state">
        <div class="empty-state-icon">{icon}</div>
        <div class="empty-state-title">{title}</div>
        <p>{message}</p>
    </div>
    """


def render_api_status(has_key: bool, rate_limit: str) -> str:
    """Render API status indicator."""
    icon = "🔑" if has_key else "⚠️"
    return f'<div style="text-align: right; font-size: 12px; color: #888;">{icon} {rate_limit}</div>'


def get_account_badge(player_type: str) -> str:
    """Get HTML for account type badge."""
    if not player_type or player_type == "regular":
        return ""
    
    badge_class = ""
    if "hardcore" in player_type.lower():
        badge_class = "hardcore"
    elif "ultimate" in player_type.lower():
        badge_class = "ultimate"
    elif "group" in player_type.lower():
        badge_class = "group"
    elif "iron" in player_type.lower():
        badge_class = "ironman"
    
    display_name = player_type.replace("_", " ").title()
    return f'<span class="account-badge {badge_class}">{display_name}</span>'
