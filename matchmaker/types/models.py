"""Result models for matching, icebreaker, and relationship assessment."""

from typing import List, Dict, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class CompatibilityScore(BaseModel):
    """Detailed compatibility breakdown between two people."""

    overall_score: float = Field(..., ge=0, le=100, description="Overall compatibility (0-100)")

    # Component scores
    personality_compatibility: float = Field(..., ge=0, le=100, description="Personality match score")
    lifestyle_compatibility: float = Field(..., ge=0, le=100, description="Lifestyle compatibility score")
    values_alignment: float = Field(..., ge=0, le=100, description="Values alignment score")
    interests_overlap: float = Field(..., ge=0, le=100, description="Shared interests score")

    # Analysis
    match_quality: str = Field(..., description="Match quality: excellent, very-good, good, fair, poor")
    complementarity_score: float = Field(..., ge=0, le=100, description="How well they complement each other")

    strengths: List[str] = Field(..., description="Relationship strengths")
    challenges: List[str] = Field(..., description="Potential challenges")
    growth_areas: List[str] = Field(..., description="Areas for mutual growth")


class MatchResult(BaseModel):
    """Complete match result between two people."""

    person1_id: str = Field(..., description="First person ID")
    person1_name: str = Field(..., description="First person name")
    person2_id: str = Field(..., description="Second person ID")
    person2_name: str = Field(..., description="Second person name")

    compatibility: CompatibilityScore = Field(..., description="Detailed compatibility scores")

    # Match insights
    why_good_match: List[str] = Field(..., description="Top reasons why this is a good match")
    potential_issues: List[str] = Field(..., description="Potential issues to be aware of")
    relationship_potential: str = Field(..., description="Long-term potential: high, medium-high, medium, medium-low, low")

    # Recommendations
    first_date_suggestions: List[str] = Field(..., description="Suggested first date activities")
    communication_tips: List[str] = Field(..., description="Tips for effective communication")

    match_date: Optional[str] = Field(None, description="Date of match analysis")


class IcebreakerSuggestion(BaseModel):
    """Personalized icebreaker and conversation suggestions."""

    # For initial contact
    opening_lines: List[str] = Field(..., description="Suggested opening messages (3-5 options)")

    # Conversation topics
    shared_interests: List[str] = Field(..., description="Topics based on shared interests")
    unique_conversation_starters: List[str] = Field(..., description="Unique topics based on their profile")
    questions_to_ask: List[str] = Field(..., description="Good questions to get to know them")

    # Date planning
    date_ideas: List[Dict[str, str]] = Field(..., description="Personalized date ideas with activity and reason")

    # What to avoid
    topics_to_avoid: List[str] = Field(..., description="Topics that might not resonate")
    conversation_pitfalls: List[str] = Field(..., description="Communication styles to avoid")

    # Tips
    personality_tips: List[str] = Field(..., description="Tips based on their personality")
    style_advice: str = Field(..., description="Overall approach recommendation")


class InteractionLog(BaseModel):
    """Log of interaction between two people."""

    date: str = Field(..., description="Interaction date")
    type: str = Field(..., description="Type: message, call, date, meeting")
    quality: str = Field(..., description="Quality: excellent, good, okay, poor")
    notes: Optional[str] = Field(None, description="Notes about the interaction")


class RelationshipAssessment(BaseModel):
    """Assessment of relationship progress and health."""

    person1_id: str = Field(..., description="First person ID")
    person2_id: str = Field(..., description="Second person ID")

    # Interaction history
    total_interactions: int = Field(..., description="Total number of interactions")
    interaction_logs: Optional[List[InteractionLog]] = Field(None, description="Detailed interaction history")

    # Current status
    relationship_stage: str = Field(..., description="Stage: initial-contact, getting-to-know, dating, committed, serious")
    relationship_health: float = Field(..., ge=0, le=100, description="Relationship health score (0-100)")

    # Analysis
    positive_indicators: List[str] = Field(..., description="Positive signs")
    concerns: List[str] = Field(..., description="Potential concerns")
    momentum: str = Field(..., description="Momentum: accelerating, steady, slowing, stalled")

    # Communication analysis
    communication_quality: float = Field(..., ge=0, le=100, description="Communication quality (0-100)")
    communication_balance: str = Field(..., description="Balance: balanced, person1-dominant, person2-dominant")
    response_pattern: str = Field(..., description="Response pattern: mutual-engaged, uneven, declining")

    # Recommendations
    next_steps: List[str] = Field(..., description="Recommended next steps")
    red_flags: List[str] = Field(..., description="Red flags to watch for")
    green_flags: List[str] = Field(..., description="Positive signs to celebrate")

    # Prediction
    success_likelihood: str = Field(..., description="Success likelihood: very-high, high, moderate, low, very-low")
    timeline_prediction: Optional[str] = Field(None, description="Predicted timeline for next milestone")
