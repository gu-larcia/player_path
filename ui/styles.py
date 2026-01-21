"""Custom CSS styles for the dashboard."""

# Minimal CSS - just for font import
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Nunito:wght@300;400;600;700&display=swap');
</style>
"""


def render_empty_state(title: str, message: str, icon: str = "📭") -> str:
    """Render an empty state message."""
    return f"""
### {icon} {title}

{message}
"""


def render_api_status(has_key: bool, rate_limit: str) -> str:
    """Render API status indicator."""
    icon = "🔑" if has_key else "⚠️"
    return f"{icon} {rate_limit}"


def get_account_badge(player_type: str) -> str:
    """Get display text for account type."""
    if not player_type or player_type == "regular":
        return ""
    return f" ({player_type.replace('_', ' ').title()})"
