"""Profile model - analyzed user profile with scores."""

from typing import List, Dict, Optional
from pydantic import BaseModel, Field


class ProfileDimension(BaseModel):
    """Score for one dimension of the profile."""

    name: str = Field(..., description="Dimension name")
    score: float = Field(..., ge=0, le=100, description="Score (0-100)")
    strengths: List[str] = Field(..., description="Key strengths in this dimension")
    considerations: List[str] = Field(..., description="Things to consider")


class Profile(BaseModel):
    """Analyzed user profile with multi-dimensional scores."""

    person_id: str = Field(..., description="Person identifier")
    person_name: str = Field(..., description="Person's name")

    # Overall readiness
    overall_score: float = Field(..., ge=0, le=100, description="Overall profile quality (0-100)")
    profile_completeness: float = Field(..., ge=0, le=100, description="Profile completeness (0-100)")

    # Dimension scores
    personality_score: ProfileDimension = Field(..., description="Personality clarity score")
    lifestyle_score: ProfileDimension = Field(..., description="Lifestyle compatibility score")
    values_score: ProfileDimension = Field(..., description="Values clarity score")
    interests_score: ProfileDimension = Field(..., description="Interests diversity score")

    # Analysis
    strengths: List[str] = Field(..., description="Overall profile strengths")
    weaknesses: List[str] = Field(..., description="Areas for improvement")
    recommendations: List[str] = Field(..., description="Actionable recommendations")

    # Summary
    profile_type: str = Field(..., description="Profile type: outgoing-adventurer, intellectual-homebody, balanced-social, etc.")
    ideal_match_type: str = Field(..., description="Suggested ideal match type")
    dating_readiness: str = Field(..., description="Dating readiness: ready, mostly-ready, needs-work, not-ready")

    class Config:
        json_schema_extra = {
            "example": {
                "person_id": "p001",
                "person_name": "Alex Chen",
                "overall_score": 82.5,
                "profile_completeness": 90.0,
                "personality_score": {
                    "name": "Personality",
                    "score": 85,
                    "strengths": ["High openness to new experiences", "Good emotional stability"],
                    "considerations": ["May need partner who appreciates creativity"]
                },
                "lifestyle_score": {
                    "name": "Lifestyle",
                    "score": 80,
                    "strengths": ["Healthy work-life balance", "Active lifestyle"],
                    "considerations": ["Night owl schedule may limit early morning activities"]
                },
                "values_score": {
                    "name": "Values",
                    "score": 85,
                    "strengths": ["Clear family values", "Balanced priorities"],
                    "considerations": ["Open communication about long-term plans important"]
                },
                "interests_score": {
                    "name": "Interests",
                    "score": 80,
                    "strengths": ["Diverse interests", "Good mix of active and creative hobbies"],
                    "considerations": ["Look for partner with some shared interests"]
                },
                "strengths": [
                    "Well-rounded personality profile",
                    "Clear values and life goals",
                    "Healthy lifestyle habits",
                    "Diverse interests for conversation"
                ],
                "weaknesses": [
                    "Could be more specific about partner preferences",
                    "Night owl schedule may limit dating options"
                ],
                "recommendations": [
                    "Define more specific partner preferences",
                    "Consider being flexible with schedule for dates",
                    "Highlight your unique combination of tech and creative interests"
                ],
                "profile_type": "balanced-creative-professional",
                "ideal_match_type": "intellectual-active-partner",
                "dating_readiness": "ready"
            }
        }
