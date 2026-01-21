"""Player profiling and playstyle analysis."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
import math

from config import SKILLS, SKILL_CATEGORIES, BOSS_CATEGORIES, ARCHETYPE_CONFIG


@dataclass
class SkillData:
    """Skill statistics for a player."""
    name: str
    level: int
    experience: int
    rank: int
    ehp: float = 0.0
    
    @property
    def virtual_level(self) -> int:
        """Calculate virtual level beyond 99."""
        if self.experience < 13034431:  # Level 99 XP
            return self.level
        # Virtual level calculation
        xp_table = [0, 83, 174, 276, 388, 512, 650, 801, 969, 1154, 1358, 1584, 1833, 2107, 
                    2411, 2746, 3115, 3523, 3973, 4470, 5018, 5624, 6291, 7028, 7842, 8740,
                    9730, 10824, 12031, 13363, 14833, 16456, 18247, 20224, 22406, 24815,
                    27473, 30408, 33648, 37224, 41171, 45529, 50339, 55649, 61512, 67983,
                    75127, 83014, 91721, 101333, 111945, 123660, 136594, 150872, 166636,
                    184040, 203254, 224466, 247886, 273742, 302288, 333804, 368599, 407015,
                    449428, 496254, 547953, 605032, 668051, 737627, 814445, 899257, 992895,
                    1096278, 1210421, 1336443, 1475581, 1629200, 1798808, 1986068, 2192818,
                    2421087, 2673114, 2951373, 3258594, 3597792, 3972294, 4385776, 4842295,
                    5346332, 5902831, 6517253, 7195629, 7944614, 8771558, 9684577, 10692629,
                    11805606, 13034431]
        
        for level in range(99, 127):
            xp_for_level = int(sum(math.floor(l + 300 * 2**(l/7)) / 4 for l in range(1, level + 1)))
            if self.experience < xp_for_level:
                return level - 1
        return 126


@dataclass
class BossData:
    """Boss kill count data."""
    name: str
    kills: int
    rank: int
    ehb: float = 0.0
    
    @property
    def display_name(self) -> str:
        """Human-readable boss name."""
        return self.name.replace("_", " ").title()


@dataclass
class PlayerProfile:
    """Complete player profile with computed analytics."""
    
    # Basic info
    username: str
    display_name: str
    player_id: int
    player_type: str  # regular, ironman, etc.
    build: str  # main, lvl3, f2p, etc.
    
    # Core stats
    combat_level: int
    total_level: int
    total_experience: int
    
    # Efficiency metrics
    ehp: float
    ehb: float
    
    # Detailed data
    skills: Dict[str, SkillData] = field(default_factory=dict)
    bosses: Dict[str, BossData] = field(default_factory=dict)
    
    # Snapshot info
    last_updated: Optional[datetime] = None
    snapshot_count: int = 0
    first_snapshot: Optional[datetime] = None
    
    # Computed fields (populated by analyze())
    archetype: str = ""
    archetype_description: str = ""
    playstyle_scores: Dict[str, float] = field(default_factory=dict)
    skill_category_xp: Dict[str, int] = field(default_factory=dict)
    top_skills: List[Tuple[str, int]] = field(default_factory=list)
    top_bosses: List[Tuple[str, int]] = field(default_factory=list)
    
    def analyze(self):
        """Compute all derived analytics for this profile."""
        self._compute_skill_categories()
        self._compute_top_skills()
        self._compute_top_bosses()
        self._compute_playstyle_scores()
        self._determine_archetype()
    
    def _compute_skill_categories(self):
        """Calculate total XP per skill category."""
        self.skill_category_xp = {}
        for category, skill_names in SKILL_CATEGORIES.items():
            total = sum(
                self.skills[s].experience 
                for s in skill_names 
                if s in self.skills
            )
            self.skill_category_xp[category] = total
    
    def _compute_top_skills(self):
        """Find top 5 skills by XP (excluding overall)."""
        skill_xp = [
            (name, data.experience) 
            for name, data in self.skills.items() 
            if name != "overall"
        ]
        skill_xp.sort(key=lambda x: x[1], reverse=True)
        self.top_skills = skill_xp[:5]
    
    def _compute_top_bosses(self):
        """Find top 5 bosses by kill count."""
        boss_kc = [
            (name, data.kills) 
            for name, data in self.bosses.items() 
            if data.kills > 0
        ]
        boss_kc.sort(key=lambda x: x[1], reverse=True)
        self.top_bosses = boss_kc[:5]
    
    def _compute_playstyle_scores(self):
        """Calculate playstyle dimension scores (0-100)."""
        config = ARCHETYPE_CONFIG
        
        # EHP/EHB balance (0 = pure PvM, 100 = pure skiller)
        if self.ehb > 0:
            ratio = self.ehp / self.ehb
            if ratio > config["ehp_ehb_ratio_skiller"]:
                skiller_score = 100
            elif ratio < config["ehp_ehb_ratio_pvmer"]:
                skiller_score = 0
            else:
                # Linear interpolation
                skiller_score = (ratio - config["ehp_ehb_ratio_pvmer"]) / (
                    config["ehp_ehb_ratio_skiller"] - config["ehp_ehb_ratio_pvmer"]
                ) * 100
        else:
            skiller_score = 100 if self.ehp > 0 else 50
        
        self.playstyle_scores["skiller_vs_pvmer"] = skiller_score
        
        # Boss diversity
        bosses_with_kc = len([b for b in self.bosses.values() if b.kills > 0])
        diversity_score = min(100, bosses_with_kc / config["boss_diversity_high"] * 100)
        self.playstyle_scores["boss_diversity"] = diversity_score
        
        # Raid focus
        raid_kc = sum(
            self.bosses[b].kills 
            for b in BOSS_CATEGORIES.get("Raids", []) 
            if b in self.bosses
        )
        raid_score = min(100, raid_kc / config["raid_kc_threshold"] * 100)
        self.playstyle_scores["raid_focus"] = raid_score
        
        # Skill balance (how evenly distributed is XP across categories)
        if self.skill_category_xp:
            values = list(self.skill_category_xp.values())
            mean_xp = sum(values) / len(values)
            if mean_xp > 0:
                variance = sum((v - mean_xp) ** 2 for v in values) / len(values)
                cv = (variance ** 0.5) / mean_xp  # Coefficient of variation
                # Lower CV = more balanced, convert to 0-100 score
                balance_score = max(0, 100 - cv * 100)
            else:
                balance_score = 50
        else:
            balance_score = 50
        
        self.playstyle_scores["skill_balance"] = balance_score
        
        # Combat focus (combat XP / total XP)
        combat_xp = self.skill_category_xp.get("Combat", 0)
        total_xp = self.total_experience
        combat_focus = (combat_xp / total_xp * 100) if total_xp > 0 else 50
        self.playstyle_scores["combat_focus"] = combat_focus
    
    def _determine_archetype(self):
        """Determine player archetype based on scores."""
        scores = self.playstyle_scores
        
        # Primary archetypes based on EHP/EHB ratio
        skiller_score = scores.get("skiller_vs_pvmer", 50)
        raid_score = scores.get("raid_focus", 0)
        diversity_score = scores.get("boss_diversity", 0)
        balance_score = scores.get("skill_balance", 50)
        
        # Decision tree for archetype
        if skiller_score > 80:
            if balance_score > 70:
                self.archetype = "Balanced Skiller"
                self.archetype_description = "Well-rounded skill training across all categories"
            else:
                # Find dominant skill category
                if self.skill_category_xp:
                    top_cat = max(self.skill_category_xp.items(), key=lambda x: x[1])
                    self.archetype = f"{top_cat[0]} Specialist"
                    self.archetype_description = f"Focused primarily on {top_cat[0].lower()} skills"
                else:
                    self.archetype = "Skiller"
                    self.archetype_description = "Focuses on skill training over combat"
        
        elif skiller_score < 30:
            if raid_score > 70:
                self.archetype = "Raider"
                self.archetype_description = "Heavy focus on raid content (CoX, ToB, ToA)"
            elif diversity_score > 70:
                self.archetype = "Boss Hunter"
                self.archetype_description = "Experienced across many different bosses"
            else:
                # Check for specific boss focus
                if self.top_bosses:
                    top_boss = self.top_bosses[0][0]
                    for category, bosses in BOSS_CATEGORIES.items():
                        if top_boss in bosses:
                            self.archetype = f"{category} Specialist"
                            self.archetype_description = f"Primary focus on {category.lower()} content"
                            break
                    else:
                        self.archetype = "PvMer"
                        self.archetype_description = "Focuses on boss content and combat"
                else:
                    self.archetype = "PvMer"
                    self.archetype_description = "Focuses on boss content and combat"
        
        else:
            # Hybrid player
            if raid_score > 50 and balance_score > 50:
                self.archetype = "Completionist"
                self.archetype_description = "Balanced progression across skilling and PvM"
            elif raid_score > 50:
                self.archetype = "Raiding Hybrid"
                self.archetype_description = "Mixes raid content with skill training"
            else:
                self.archetype = "All-Rounder"
                self.archetype_description = "Enjoys varied content without strong specialization"
        
        # Account type modifiers
        if self.player_type and self.player_type != "regular":
            type_name = self.player_type.replace("_", " ").title()
            self.archetype = f"{type_name} {self.archetype}"


def build_player_profile(player_data: Dict, snapshots: List[Dict] = None) -> PlayerProfile:
    """
    Build a PlayerProfile from WOM API data.
    
    Args:
        player_data: Response from /players/{username} endpoint
        snapshots: Optional list of historical snapshots
    
    Returns:
        Populated and analyzed PlayerProfile
    """
    # Extract basic info
    username = player_data.get("username", "Unknown")
    display_name = player_data.get("displayName", username)
    player_id = player_data.get("id", 0)
    player_type = player_data.get("type", "regular")
    build = player_data.get("build", "main")
    
    # Extract latest snapshot data
    latest = player_data.get("latestSnapshot", {})
    
    # Parse skills
    skills_data = latest.get("data", {}).get("skills", {})
    skills = {}
    for skill_name in SKILLS:
        if skill_name in skills_data:
            s = skills_data[skill_name]
            skills[skill_name] = SkillData(
                name=skill_name,
                level=s.get("level", 1),
                experience=s.get("experience", 0),
                rank=s.get("rank", -1),
                ehp=s.get("ehp", 0.0)
            )
    
    # Parse bosses
    bosses_data = latest.get("data", {}).get("bosses", {})
    bosses = {}
    for boss_name, b in bosses_data.items():
        kills = b.get("kills", 0)
        if kills >= 0:  # WOM uses -1 for untracked
            bosses[boss_name] = BossData(
                name=boss_name,
                kills=kills,
                rank=b.get("rank", -1),
                ehb=b.get("ehb", 0.0)
            )
    
    # Extract computed metrics
    computed = latest.get("data", {}).get("computed", {})
    ehp = computed.get("ehp", {}).get("value", 0.0)
    ehb = computed.get("ehb", {}).get("value", 0.0)
    
    # Core stats
    overall_skill = skills.get("overall", SkillData("overall", 1, 0, -1))
    combat_level = player_data.get("combatLevel", 3)
    
    # Snapshot metadata
    last_updated = None
    updated_str = player_data.get("updatedAt") or player_data.get("lastChangedAt")
    if updated_str:
        try:
            if updated_str.endswith("Z"):
                updated_str = updated_str[:-1] + "+00:00"
            last_updated = datetime.fromisoformat(updated_str)
        except ValueError:
            pass
    
    snapshot_count = 0
    first_snapshot = None
    if snapshots:
        snapshot_count = len(snapshots)
        if snapshots:
            try:
                dates = []
                for snap in snapshots:
                    created = snap.get("createdAt")
                    if created:
                        if created.endswith("Z"):
                            created = created[:-1] + "+00:00"
                        dates.append(datetime.fromisoformat(created))
                if dates:
                    first_snapshot = min(dates)
            except ValueError:
                pass
    
    # Build profile
    profile = PlayerProfile(
        username=username,
        display_name=display_name,
        player_id=player_id,
        player_type=player_type,
        build=build,
        combat_level=combat_level,
        total_level=overall_skill.level,
        total_experience=overall_skill.experience,
        ehp=ehp,
        ehb=ehb,
        skills=skills,
        bosses=bosses,
        last_updated=last_updated,
        snapshot_count=snapshot_count,
        first_snapshot=first_snapshot,
    )
    
    # Run analysis
    profile.analyze()
    
    return profile


def compute_journey_data(snapshots: List[Dict]) -> Dict[str, Any]:
    """
    Process snapshots into journey visualization data.
    
    Returns dict with:
        - timeline: list of {date, total_level, total_xp, ehp, ehb}
        - milestones: list of detected milestones
        - data_coverage: description of available history
    """
    if not snapshots:
        return {
            "timeline": [],
            "milestones": [],
            "data_coverage": "No historical data available",
            "snapshot_count": 0,
        }
    
    timeline = []
    
    for snap in sorted(snapshots, key=lambda x: x.get("createdAt", "")):
        created = snap.get("createdAt")
        if not created:
            continue
        
        try:
            if created.endswith("Z"):
                created = created[:-1] + "+00:00"
            date = datetime.fromisoformat(created)
        except ValueError:
            continue
        
        data = snap.get("data", {})
        skills = data.get("skills", {})
        computed = data.get("computed", {})
        
        overall = skills.get("overall", {})
        
        timeline.append({
            "date": date,
            "total_level": overall.get("level", 0),
            "total_xp": overall.get("experience", 0),
            "ehp": computed.get("ehp", {}).get("value", 0),
            "ehb": computed.get("ehb", {}).get("value", 0),
        })
    
    # Detect milestones (simplified)
    milestones = []
    level_thresholds = [500, 750, 1000, 1250, 1500, 1750, 2000, 2277]
    
    if len(timeline) >= 2:
        for i in range(1, len(timeline)):
            prev_level = timeline[i-1]["total_level"]
            curr_level = timeline[i]["total_level"]
            
            for threshold in level_thresholds:
                if prev_level < threshold <= curr_level:
                    milestones.append({
                        "date": timeline[i]["date"],
                        "type": "total_level",
                        "value": threshold,
                        "description": f"Reached {threshold} total level"
                    })
    
    # Compute data coverage
    if timeline:
        first_date = min(t["date"] for t in timeline)
        last_date = max(t["date"] for t in timeline)
        days_covered = (last_date - first_date).days
        
        if days_covered < 7:
            coverage = f"{len(timeline)} snapshots over {days_covered} days (limited history)"
        elif days_covered < 30:
            coverage = f"{len(timeline)} snapshots over {days_covered} days"
        elif days_covered < 365:
            months = days_covered // 30
            coverage = f"{len(timeline)} snapshots over ~{months} months"
        else:
            years = days_covered / 365
            coverage = f"{len(timeline)} snapshots over ~{years:.1f} years"
    else:
        coverage = "No historical data available"
    
    return {
        "timeline": timeline,
        "milestones": milestones,
        "data_coverage": coverage,
        "snapshot_count": len(timeline),
    }
