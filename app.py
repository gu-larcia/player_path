"""OSRS Player Analytics

Playstyle profiling and journey visualization using WiseOldMan data.
"""

import streamlit as st
from typing import Optional

from config import (
    APP_TITLE, APP_ICON, APP_VERSION, APP_SUBTITLE,
    WOM_API_BASE, WOM_USER_AGENT,
    CACHE_TTL_PLAYER, CACHE_TTL_SNAPSHOTS,
)
from services import WOMClient
from analysis import build_player_profile, compute_journey_data
from ui import (
    CUSTOM_CSS,
    render_empty_state,
    render_api_status,
    render_profile_page,
    render_skills_page,
    render_bosses_page,
    render_journey_page,
)


# Page configuration
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ===== Cached API Functions =====

@st.cache_resource
def get_api_client() -> WOMClient:
    """Get singleton API client with optional API key from secrets."""
    api_key = None
    
    try:
        api_key = st.secrets.get("WOM_API_KEY", None)
    except Exception:
        pass
    
    return WOMClient(
        base_url=WOM_API_BASE,
        api_key=api_key,
        user_agent=WOM_USER_AGENT
    )


@st.cache_data(ttl=CACHE_TTL_PLAYER, show_spinner=False)
def fetch_player(_client: WOMClient, username: str):
    """Fetch player details."""
    try:
        return _client.get_player_details(username)
    except Exception as e:
        st.error(f"Failed to fetch player: {e}")
        return None


@st.cache_data(ttl=CACHE_TTL_SNAPSHOTS, show_spinner=False)
def fetch_snapshots(_client: WOMClient, username: str):
    """Fetch player snapshots."""
    try:
        return _client.get_player_snapshots(username)
    except Exception as e:
        st.warning(f"Could not fetch snapshots: {e}")
        return []


@st.cache_data(ttl=60, show_spinner=False)
def search_players(_client: WOMClient, query: str):
    """Search for players."""
    try:
        return _client.search_players(query)
    except Exception as e:
        return []


def main():
    """Main application."""
    
    # Initialize session state
    if "current_player" not in st.session_state:
        st.session_state.current_player = None
    if "player_profile" not in st.session_state:
        st.session_state.player_profile = None
    if "journey_data" not in st.session_state:
        st.session_state.journey_data = None
    
    # Header
    col1, col2 = st.columns([4, 1])
    with col1:
        st.title(f"{APP_ICON} {APP_TITLE}")
        st.caption(f"v{APP_VERSION} • {APP_SUBTITLE}")
    
    # Initialize client
    client = get_api_client()
    rate_info = client.get_rate_limit_status()
    
    with col2:
        st.markdown(
            render_api_status(rate_info["has_api_key"], rate_info["rate_limit"]),
            unsafe_allow_html=True
        )
    
    # Sidebar - Player Search
    with st.sidebar:
        st.header("🔍 Player Search")
        
        # Search input
        search_query = st.text_input(
            "Username",
            placeholder="Enter RSN...",
            help="Search for any OSRS player tracked by WiseOldMan"
        )
        
        # Search button
        search_clicked = st.button("Search", use_container_width=True, type="primary")
        
        # Search results
        if search_query and search_clicked:
            with st.spinner("Searching..."):
                results = search_players(client, search_query)
            
            if results:
                st.success(f"Found {len(results)} player(s)")
                
                for player in results[:10]:  # Limit to 10 results
                    display = player.get("displayName", player.get("username", "Unknown"))
                    player_type = player.get("type", "regular")
                    
                    type_badge = ""
                    if player_type != "regular":
                        type_badge = f" ({player_type.replace('_', ' ').title()})"
                    
                    if st.button(
                        f"{display}{type_badge}",
                        key=f"player_{player.get('id', display)}",
                        use_container_width=True
                    ):
                        st.session_state.current_player = display
                        st.rerun()
            else:
                st.warning("No players found. Try a different search term.")
        
        st.divider()
        
        # Quick load for known player
        st.subheader("Quick Load")
        direct_username = st.text_input(
            "Direct username",
            placeholder="Exact RSN",
            key="direct_load"
        )
        
        if st.button("Load Profile", use_container_width=True):
            if direct_username:
                st.session_state.current_player = direct_username
                st.rerun()
        
        st.divider()
        
        # Current player info
        if st.session_state.current_player:
            st.subheader("📋 Current Player")
            st.write(st.session_state.current_player)
            
            if st.button("🔄 Refresh Data", use_container_width=True):
                # Clear cache for this player
                st.cache_data.clear()
                st.rerun()
            
            if st.button("❌ Clear", use_container_width=True):
                st.session_state.current_player = None
                st.session_state.player_profile = None
                st.session_state.journey_data = None
                st.rerun()
        
        st.divider()
        
        # Links
        st.subheader("🔗 Links")
        st.link_button(
            "WiseOldMan",
            "https://wiseoldman.net",
            use_container_width=True
        )
    
    # Main content
    if not st.session_state.current_player:
        # Welcome state
        st.markdown("""
        <div style="
            text-align: center;
            padding: 80px 20px;
        ">
            <div style="font-size: 64px; margin-bottom: 20px;">⚔️</div>
            <h2 style="color: #D4AF37; font-family: 'Cinzel', serif;">
                Welcome to OSRS Player Analytics
            </h2>
            <p style="color: #888; max-width: 600px; margin: 20px auto;">
                Search for any Old School RuneScape player to analyze their playstyle,
                skill distribution, boss experience, and account progression.
            </p>
            <p style="color: #666; font-size: 14px;">
                Use the sidebar to search for a player by their RuneScape name.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Sample players to try
        st.markdown("---")
        st.subheader("Try these players:")
        
        sample_players = ["Zezima", "Lynx Titan", "Woox"]
        cols = st.columns(len(sample_players))
        
        for i, player in enumerate(sample_players):
            with cols[i]:
                if st.button(player, use_container_width=True):
                    st.session_state.current_player = player
                    st.rerun()
        
        return
    
    # Load player data
    with st.spinner(f"Loading {st.session_state.current_player}..."):
        player_data = fetch_player(client, st.session_state.current_player)
    
    if not player_data:
        st.markdown(
            render_empty_state(
                "Player Not Found",
                f"Could not find player '{st.session_state.current_player}' on WiseOldMan. "
                "They may not be tracked yet.",
                "❌"
            ),
            unsafe_allow_html=True
        )
        return
    
    # Load snapshots
    with st.spinner("Loading historical data..."):
        snapshots = fetch_snapshots(client, st.session_state.current_player)
    
    # Build profile
    profile = build_player_profile(player_data, snapshots)
    journey_data = compute_journey_data(snapshots)
    
    # Store in session state
    st.session_state.player_profile = profile
    st.session_state.journey_data = journey_data
    
    # Tab navigation
    tabs = st.tabs([
        "👤 Profile",
        "📚 Skills",
        "💀 Bosses",
        "📈 Journey",
    ])
    
    # Profile tab
    with tabs[0]:
        render_profile_page(profile, journey_data)
    
    # Skills tab
    with tabs[1]:
        render_skills_page(profile)
    
    # Bosses tab
    with tabs[2]:
        render_bosses_page(profile)
    
    # Journey tab
    with tabs[3]:
        render_journey_page(profile, journey_data)


if __name__ == "__main__":
    main()
