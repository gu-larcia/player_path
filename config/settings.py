"""Configuration settings for OSRS Player Analytics."""

# App metadata
APP_TITLE = "OSRS Player Analytics"
APP_ICON = "⚔️"
APP_VERSION = "1.0.0"
APP_SUBTITLE = "Playstyle profiling & journey visualization"

# WiseOldMan API
WOM_API_BASE = "https://api.wiseoldman.net/v2"
WOM_USER_AGENT = "OSRS-Player-Analytics/1.0"

# Cache TTLs (seconds)
CACHE_TTL_PLAYER = 600       # 10 min - player details
CACHE_TTL_SNAPSHOTS = 900    # 15 min - historical snapshots
CACHE_TTL_ACHIEVEMENTS = 900  # 15 min - achievements

# OSRS Skill definitions
SKILLS = [
    "overall", "attack", "defence", "strength", "hitpoints", "ranged",
    "prayer", "magic", "cooking", "woodcutting", "fletching", "fishing",
    "firemaking", "crafting", "smithing", "mining", "herblore", "agility",
    "thieving", "slayer", "farming", "runecrafting", "hunter", "construction"
]

# Skill categories for radar charts
SKILL_CATEGORIES = {
    "Combat": ["attack", "strength", "defence", "hitpoints", "ranged", "magic", "prayer"],
    "Gathering": ["mining", "fishing", "woodcutting", "farming", "hunter"],
    "Artisan": ["smithing", "crafting", "fletching", "cooking", "firemaking", "herblore", "construction"],
    "Support": ["agility", "thieving", "slayer", "runecrafting"],
}

# Bosses grouped by content type
BOSS_CATEGORIES = {
    "Raids": ["chambers_of_xeric", "chambers_of_xeric_challenge_mode", "theatre_of_blood", 
              "theatre_of_blood_hard_mode", "tombs_of_amascut", "tombs_of_amascut_expert"],
    "GWD": ["commander_zilyana", "general_graardor", "kreearra", "kril_tsutsaroth", "nex"],
    "Slayer": ["cerberus", "abyssal_sire", "kraken", "thermonuclear_smoke_devil", 
               "grotesque_guardians", "alchemical_hydra"],
    "Wilderness": ["callisto", "venenatis", "vetion", "chaos_elemental", "scorpia", 
                   "king_black_dragon", "chaos_fanatic", "crazy_archaeologist"],
    "Other": ["zulrah", "vorkath", "corporeal_beast", "giant_mole", "kalphite_queen",
              "dagannoth_prime", "dagannoth_rex", "dagannoth_supreme", "sarachnis",
              "the_gauntlet", "the_corrupted_gauntlet", "nightmare", "phosanis_nightmare",
              "phantom_muspah", "duke_sucellus", "the_leviathan", "the_whisperer", "vardorvis"],
}

# Playstyle archetype thresholds
ARCHETYPE_CONFIG = {
    "ehp_ehb_ratio_skiller": 3.0,      # EHP/EHB > 3 = skiller-leaning
    "ehp_ehb_ratio_pvmer": 0.5,        # EHP/EHB < 0.5 = PvM-leaning
    "efficiency_threshold": 0.7,        # EHP/total_hours > 0.7 = efficiency-focused
    "boss_diversity_high": 10,          # 10+ bosses with KC = diverse
    "raid_kc_threshold": 50,            # 50+ raid KC = raider
}

# Color scheme
COLORS = {
    "primary": "#D4AF37",      # Gold
    "secondary": "#2E4A3F",    # Dark green
    "accent": "#8B4513",       # Saddle brown
    "background": "#1A1A1A",   # Near black
    "surface": "#2D2D2D",      # Dark gray
    "text": "#E8E8E8",         # Light gray
    "muted": "#888888",        # Muted gray
    "combat": "#DC143C",       # Crimson
    "gathering": "#228B22",    # Forest green
    "artisan": "#4169E1",      # Royal blue
    "support": "#9932CC",      # Purple
}
