"""Page modules."""

from .profile import render_profile_page
from .skills import render_skills_page
from .bosses import render_bosses_page
from .journey import render_journey_page

__all__ = [
    "render_profile_page",
    "render_skills_page",
    "render_bosses_page",
    "render_journey_page",
]
