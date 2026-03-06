"""Person data model - represents an individual seeking a match."""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class PersonalityTraits(BaseModel):
    """Personality characteristics using Big Five model."""

    openness: int = Field(..., ge=0, le=100, description="Openness to experience (0-100)")
    conscientiousness: int = Field(..., ge=0, le=100, description="Conscientiousness level (0-100)")
    extraversion: int = Field(..., ge=0, le=100, description="Extraversion vs introversion (0-100)")
    agreeableness: int = Field(..., ge=0, le=100, description="Agreeableness level (0-100)")
    neuroticism: int = Field(..., ge=0, le=100, description="Emotional stability (0-100, lower is more stable)")

    # Optional MBTI type
    mbti: Optional[str] = Field(None, description="MBTI type (e.g., INTJ, ENFP)")


class Lifestyle(BaseModel):
    """Lifestyle and daily habits."""

    sleep_schedule: str = Field(..., description="Sleep pattern: early-bird, night-owl, flexible")
    exercise_frequency: str = Field(..., description="Exercise habit: daily, weekly, rarely, never")
    social_activity: str = Field(..., description="Social preference: very-social, moderately-social, homebody")
    work_life_balance: str = Field(..., description="Work balance: workaholic, balanced, life-first")
    travel_frequency: str = Field(..., description="Travel preference: frequent, occasional, rarely, never")
    pets: Optional[str] = Field(None, description="Pet ownership: has-dogs, has-cats, has-other, want-pets, no-pets")
    smoking: str = Field(..., description="Smoking status: never, social, regular, trying-to-quit")
    drinking: str = Field(..., description="Drinking habit: never, social, regular")
    diet: Optional[str] = Field(None, description="Dietary preference: vegetarian, vegan, pescatarian, omnivore")


class Values(BaseModel):
    """Core values and beliefs."""

    marriage_view: str = Field(..., description="Marriage attitude: priority, open, not-priority, not-interested")
    children_plan: str = Field(..., description="Children plan: want, open, dont-want, have-children")
    family_importance: int = Field(..., ge=0, le=100, description="Family importance (0-100)")
    career_importance: int = Field(..., ge=0, le=100, description="Career importance (0-100)")
    religion: Optional[str] = Field(None, description="Religious belief: none, buddhist, christian, muslim, other")
    religion_importance: Optional[int] = Field(None, ge=0, le=100, description="Religion importance (0-100)")
    political_view: Optional[str] = Field(None, description="Political leaning: liberal, moderate, conservative, not-political")
    money_attitude: str = Field(..., description="Money view: saver, balanced, spender")
    communication_style: str = Field(..., description="Communication: direct, diplomatic, avoid-conflict")


class Interests(BaseModel):
    """Hobbies and interests."""

    categories: List[str] = Field(..., description="Interest categories: sports, arts, music, gaming, reading, cooking, travel, tech, outdoor, indoor")
    specific_hobbies: List[str] = Field(..., description="Specific hobbies and activities")
    favorite_activities: List[str] = Field(..., description="Favorite date activities")
    media_preferences: Optional[Dict[str, List[str]]] = Field(None, description="Media preferences: movies, tv, music, books")


class Person(BaseModel):
    """Complete person profile for matchmaking."""

    # Basic info
    id: Optional[str] = Field(None, description="Unique identifier")
    name: str = Field(..., description="Person's name")
    age: int = Field(..., ge=18, le=100, description="Age")
    gender: str = Field(..., description="Gender: male, female, non-binary, other")
    location: str = Field(..., description="City or region")

    # Detailed profile
    personality: PersonalityTraits = Field(..., description="Personality traits")
    lifestyle: Lifestyle = Field(..., description="Lifestyle and habits")
    values: Values = Field(..., description="Core values and beliefs")
    interests: Interests = Field(..., description="Hobbies and interests")

    # Additional info
    occupation: Optional[str] = Field(None, description="Current occupation")
    education: Optional[str] = Field(None, description="Education level")
    bio: Optional[str] = Field(None, description="Self-written bio or description")

    # Preferences for partner
    partner_preferences: Optional[Dict[str, Any]] = Field(None, description="Desired partner characteristics")
    deal_breakers: Optional[List[str]] = Field(None, description="Absolute deal breakers")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Alex Chen",
                "age": 28,
                "gender": "male",
                "location": "San Francisco, CA",
                "personality": {
                    "openness": 85,
                    "conscientiousness": 70,
                    "extraversion": 60,
                    "agreeableness": 75,
                    "neuroticism": 40,
                    "mbti": "ENFP"
                },
                "lifestyle": {
                    "sleep_schedule": "night-owl",
                    "exercise_frequency": "weekly",
                    "social_activity": "moderately-social",
                    "work_life_balance": "balanced",
                    "travel_frequency": "occasional",
                    "pets": "has-dogs",
                    "smoking": "never",
                    "drinking": "social",
                    "diet": "omnivore"
                },
                "values": {
                    "marriage_view": "open",
                    "children_plan": "want",
                    "family_importance": 80,
                    "career_importance": 70,
                    "religion": "none",
                    "money_attitude": "balanced",
                    "communication_style": "diplomatic"
                },
                "interests": {
                    "categories": ["tech", "travel", "music", "cooking"],
                    "specific_hobbies": ["photography", "hiking", "guitar", "cooking"],
                    "favorite_activities": ["coffee date", "museum visit", "outdoor concert"]
                },
                "occupation": "Software Engineer",
                "education": "Bachelor's Degree"
            }
        }
