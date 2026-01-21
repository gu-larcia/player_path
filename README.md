# OSRS Player Analytics ⚔️

A player profiling and playstyle analysis dashboard for Old School RuneScape, powered by the [WiseOldMan](https://wiseoldman.net/) API.

## Features

### 👤 Player Profile
- Automatic playstyle archetype classification (Skiller, PvMer, Raider, All-Rounder, etc.)
- Skill category radar chart (Combat, Gathering, Artisan, Support)
- Playstyle dimension scoring
- EHP/EHB efficiency gauges
- Top skills and bosses at a glance

### 📚 Skills Analysis
- Interactive treemap of XP distribution
- Category breakdowns with filtering
- 99+ skill tracking with virtual levels
- XP totals by category

### 💀 Boss Analysis
- Kill count breakdown by boss
- Content category groupings (Raids, GWD, Slayer, Wilderness, etc.)
- Raid experience highlights
- PvM summary statistics

### 📈 Journey Visualization
- Historical progression timeline (when data available)
- Milestone detection
- Progress summaries over time
- Graceful handling of sparse historical data

## Quick Start

### Deploy to Streamlit Cloud (Recommended)

1. Fork or clone this repository
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Create a new app pointing to your repository
4. Optionally add your `WOM_API_KEY` in Secrets
5. Deploy!

### Local Development

```bash
# Clone the repository
git clone <your-repo-url>
cd osrs_player_analytics

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Optional: Set up API key for higher rate limits
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Edit .streamlit/secrets.toml with your API key

# Run the app
streamlit run app.py
```

## Configuration

### API Key

An API key enables higher rate limits (100 req/min vs 20 req/min).

**Local:** Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` and add your key.

**Streamlit Cloud:** Add `WOM_API_KEY = "your-key"` in app Settings → Secrets.

Request an API key via the [WiseOldMan Discord](https://wiseoldman.net/discord).

## Project Structure

```
osrs_player_analytics/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md
├── .streamlit/
│   └── secrets.toml.example
├── config/
│   ├── __init__.py
│   └── settings.py        # App configuration, skill/boss definitions
├── services/
│   ├── __init__.py
│   └── wom_client.py      # WiseOldMan API client
├── analysis/
│   ├── __init__.py
│   └── profiling.py       # Player profiling & archetype detection
└── ui/
    ├── __init__.py
    ├── styles.py          # Custom CSS
    ├── components.py      # Reusable UI components
    ├── charts.py          # Plotly chart builders
    └── pages/
        ├── __init__.py
        ├── profile.py     # Main profile page
        ├── skills.py      # Skills detail page
        ├── bosses.py      # Boss/PvM page
        └── journey.py     # Historical journey page
```

## Playstyle Archetypes

The app automatically classifies players into archetypes based on their stats:

| Archetype | Description |
|-----------|-------------|
| **Balanced Skiller** | Well-rounded skill training across all categories |
| **[Category] Specialist** | Focused primarily on one skill category |
| **Raider** | Heavy focus on raid content (CoX, ToB, ToA) |
| **Boss Hunter** | Experienced across many different bosses |
| **PvMer** | General focus on boss content and combat |
| **Completionist** | Balanced progression across skilling and PvM |
| **All-Rounder** | Enjoys varied content without strong specialization |

Account type (Ironman, HCIM, etc.) is prepended when applicable.

## Data Limitations

Historical data availability depends on how long a player has been tracked by WiseOldMan:
- Players actively using the RuneLite plugin have regular snapshots
- Some players may only have their current state with no history
- The app gracefully handles sparse data, showing what's available

## Tech Stack

- **Python 3.11+**
- **Streamlit** - Dashboard framework
- **Plotly** - Interactive visualizations
- **Pandas** - Data manipulation
- **WiseOldMan API v2** - OSRS player data

## API Rate Limits

| Configuration | Rate Limit |
|--------------|------------|
| Without API key | 20 req/min |
| With API key | 100 req/min |

## Contributing

Contributions welcome! Feel free to open issues or submit PRs.

## License

MIT

## Credits

- [WiseOldMan](https://wiseoldman.net/) for the excellent OSRS tracking API
- Built with [Streamlit](https://streamlit.io/) and [Plotly](https://plotly.com/)
