"""Custom CSS styles for the dashboard."""

from config import COLORS

CUSTOM_CSS = f"""
<style>
    /* Import distinctive fonts */
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Nunito:wght@300;400;600;700&display=swap');
    
    /* Global styles */
    .stApp {{
        font-family: 'Nunito', sans-serif;
    }}
    
    /* Headers with medieval flair */
    h1, h2, h3 {{
        font-family: 'Cinzel', serif !important;
        color: {COLORS['primary']} !important;
        letter-spacing: 0.5px;
    }}
    
    /* Player card styling */
    .player-card {{
        background: linear-gradient(145deg, {COLORS['surface']} 0%, {COLORS['background']} 100%);
        border: 1px solid {COLORS['primary']}40;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }}
    
    .player-card h2 {{
        margin-bottom: 8px;
        font-size: 28px;
    }}
    
    .player-card .subtitle {{
        color: {COLORS['muted']};
        font-size: 14px;
        margin-bottom: 16px;
    }}
    
    /* Archetype badge */
    .archetype-badge {{
        display: inline-block;
        background: linear-gradient(135deg, {COLORS['primary']}30 0%, {COLORS['secondary']} 100%);
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
        margin-top: 4px;
    }}
    
    /* Stat grid */
    .stat-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
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
    
    /* Section headers */
    .section-header {{
        display: flex;
        align-items: center;
        gap: 12px;
        margin: 32px 0 16px 0;
        padding-bottom: 8px;
        border-bottom: 2px solid {COLORS['primary']}40;
    }}
    
    .section-header h3 {{
        margin: 0;
        font-size: 20px;
    }}
    
    /* Data coverage indicator */
    .data-coverage {{
        background: {COLORS['secondary']}40;
        border-left: 3px solid {COLORS['primary']};
        padding: 12px 16px;
        border-radius: 0 8px 8px 0;
        margin: 16px 0;
        font-size: 13px;
        color: {COLORS['muted']};
    }}
    
    .data-coverage strong {{
        color: {COLORS['text']};
    }}
    
    /* Top items list */
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
    
    /* Empty state */
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
    
    /* Account type badges */
    .account-badge {{
        display: inline-block;
        padding: 4px 10px;
        border-radius: 4px;
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-left: 8px;
    }}
    
    .account-badge.ironman {{
        background: #808080;
        color: white;
    }}
    
    .account-badge.hardcore {{
        background: #8B0000;
        color: white;
    }}
    
    .account-badge.ultimate {{
        background: #1a1a1a;
        color: #808080;
        border: 1px solid #808080;
    }}
    
    .account-badge.group {{
        background: #006400;
        color: white;
    }}
    
    /* Metric bar */
    .metric-bar {{
        height: 8px;
        background: {COLORS['background']};
        border-radius: 4px;
        overflow: hidden;
        margin-top: 8px;
    }}
    
    .metric-bar-fill {{
        height: 100%;
        border-radius: 4px;
        transition: width 0.5s ease;
    }}
    
    /* Category colors */
    .combat {{ color: {COLORS['combat']}; }}
    .gathering {{ color: {COLORS['gathering']}; }}
    .artisan {{ color: {COLORS['artisan']}; }}
    .support {{ color: {COLORS['support']}; }}
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
    color = "#22c55e" if has_key else "#eab308"
    icon = "🔑" if has_key else "⚠️"
    return f"""
    <div style="text-align: right; font-size: 12px; color: #888;">
        {icon} {rate_limit}
    </div>
    """


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
