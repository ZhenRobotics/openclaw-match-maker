"""
Matchmaker - AI-Powered Dating Match System

A professional matchmaking skill for OpenClaw that helps single individuals
find compatible partners through intelligent matching algorithms.
"""

from matchmaker.matchmaker import Matchmaker
from matchmaker.types.person import Person, PersonalityTraits, Lifestyle, Values, Interests
from matchmaker.types.profile import Profile, ProfileDimension
from matchmaker.types.models import (
    MatchResult,
    CompatibilityScore,
    IcebreakerSuggestion,
    RelationshipAssessment,
    InteractionLog
)

__version__ = "0.1.0"
__all__ = [
    "Matchmaker",
    "Person",
    "PersonalityTraits",
    "Lifestyle",
    "Values",
    "Interests",
    "Profile",
    "ProfileDimension",
    "MatchResult",
    "CompatibilityScore",
    "IcebreakerSuggestion",
    "RelationshipAssessment",
    "InteractionLog",
]
