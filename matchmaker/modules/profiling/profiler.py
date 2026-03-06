"""Profiler - Analyzes person data and generates multi-dimensional profile."""

from typing import List
from matchmaker.types.person import Person
from matchmaker.types.profile import Profile, ProfileDimension


class Profiler:
    """Analyzes person information and creates detailed profile with scores."""

    def __init__(self, weights: dict = None):
        """
        Initialize profiler with optional custom weights.

        Args:
            weights: Custom weights for dimensions (default: equal weights)
        """
        self.weights = weights or {
            "personality": 0.30,
            "lifestyle": 0.25,
            "values": 0.30,
            "interests": 0.15,
        }

    async def analyze_person(self, person: Person) -> Profile:
        """
        Analyze a person and generate their profile.

        Args:
            person: Person object with complete information

        Returns:
            Profile with scores and analysis
        """
        # Analyze each dimension
        personality_dim = self._analyze_personality(person)
        lifestyle_dim = self._analyze_lifestyle(person)
        values_dim = self._analyze_values(person)
        interests_dim = self._analyze_interests(person)

        # Calculate overall score
        overall_score = (
            personality_dim.score * self.weights["personality"]
            + lifestyle_dim.score * self.weights["lifestyle"]
            + values_dim.score * self.weights["values"]
            + interests_dim.score * self.weights["interests"]
        )

        # Calculate completeness
        completeness = self._calculate_completeness(person)

        # Determine profile type and ideal match
        profile_type = self._determine_profile_type(person)
        ideal_match_type = self._determine_ideal_match(person, profile_type)

        # Overall analysis
        strengths = self._identify_strengths(person, [personality_dim, lifestyle_dim, values_dim, interests_dim])
        weaknesses = self._identify_weaknesses(person, [personality_dim, lifestyle_dim, values_dim, interests_dim])
        recommendations = self._generate_recommendations(person, weaknesses)

        # Dating readiness
        dating_readiness = self._assess_readiness(overall_score, completeness)

        return Profile(
            person_id=person.id or f"person_{person.name.replace(' ', '_').lower()}",
            person_name=person.name,
            overall_score=overall_score,
            profile_completeness=completeness,
            personality_score=personality_dim,
            lifestyle_score=lifestyle_dim,
            values_score=values_dim,
            interests_score=interests_dim,
            strengths=strengths,
            weaknesses=weaknesses,
            recommendations=recommendations,
            profile_type=profile_type,
            ideal_match_type=ideal_match_type,
            dating_readiness=dating_readiness,
        )

    def _analyze_personality(self, person: Person) -> ProfileDimension:
        """Analyze personality traits."""
        p = person.personality

        # Calculate score based on clarity and balance
        scores = [p.openness, p.conscientiousness, p.extraversion, p.agreeableness, 100 - p.neuroticism]
        avg_score = sum(scores) / len(scores)

        # Check for balance (not all extreme values)
        extremes = sum(1 for s in scores if s < 20 or s > 80)
        balance_bonus = max(0, 20 - extremes * 5)

        score = min(100, avg_score * 0.8 + balance_bonus)

        strengths = []
        if p.openness >= 70:
            strengths.append("High openness to new experiences")
        if p.conscientiousness >= 70:
            strengths.append("Organized and reliable")
        if p.extraversion >= 60:
            strengths.append("Socially confident")
        elif p.extraversion <= 40:
            strengths.append("Comfortable with solitude and deep connections")
        if p.agreeableness >= 70:
            strengths.append("Empathetic and cooperative")
        if p.neuroticism <= 40:
            strengths.append("Emotionally stable")

        considerations = []
        if p.openness >= 80:
            considerations.append("May need partner who appreciates spontaneity")
        if p.extraversion >= 80:
            considerations.append("May need social partner or understanding of social needs")
        elif p.extraversion <= 20:
            considerations.append("May prefer quieter dates and gradual relationship building")
        if p.neuroticism >= 70:
            considerations.append("May benefit from emotionally stable partner")

        return ProfileDimension(
            name="Personality",
            score=round(score, 1),
            strengths=strengths or ["Well-defined personality traits"],
            considerations=considerations or ["Balanced personality profile"],
        )

    def _analyze_lifestyle(self, person: Person) -> ProfileDimension:
        """Analyze lifestyle compatibility factors."""
        ls = person.lifestyle

        # Score based on lifestyle clarity and health
        score = 75.0  # Base score

        # Positive factors
        if ls.exercise_frequency in ["daily", "weekly"]:
            score += 10
        if ls.work_life_balance == "balanced":
            score += 10
        if ls.smoking == "never":
            score += 5

        # Potential challenges
        if ls.sleep_schedule in ["early-bird", "night-owl"]:
            score -= 5  # Extreme schedules may limit compatibility
        if ls.work_life_balance == "workaholic":
            score -= 10

        score = max(0, min(100, score))

        strengths = []
        if ls.exercise_frequency in ["daily", "weekly"]:
            strengths.append("Active and health-conscious")
        if ls.work_life_balance == "balanced":
            strengths.append("Healthy work-life balance")
        if ls.travel_frequency in ["frequent", "occasional"]:
            strengths.append("Enjoys travel and adventure")
        if ls.social_activity == "moderately-social":
            strengths.append("Balanced social life")

        considerations = []
        if ls.sleep_schedule == "night-owl":
            considerations.append("Night owl schedule may affect date timing")
        elif ls.sleep_schedule == "early-bird":
            considerations.append("Early bird schedule - morning dates preferred")
        if ls.work_life_balance == "workaholic":
            considerations.append("Heavy work focus may limit availability")
        if ls.pets and "has-" in ls.pets:
            considerations.append(f"Pet owner - partner should be comfortable with {ls.pets}")

        return ProfileDimension(
            name="Lifestyle",
            score=round(score, 1),
            strengths=strengths or ["Clear lifestyle preferences"],
            considerations=considerations or ["Flexible lifestyle"],
        )

    def _analyze_values(self, person: Person) -> ProfileDimension:
        """Analyze core values clarity."""
        v = person.values

        # Score based on clarity and consistency
        score = 80.0  # Base score for having clear values

        # Clarity bonus
        if v.marriage_view in ["priority", "open"]:
            score += 5
        if v.children_plan in ["want", "open", "dont-want"]:  # Clear stance
            score += 5
        if v.family_importance >= 60:
            score += 5
        if v.career_importance >= 60:
            score += 5

        score = min(100, score)

        strengths = []
        if v.marriage_view == "priority":
            strengths.append("Clear about marriage goals")
        if v.children_plan in ["want", "dont-want"]:
            strengths.append("Clear about family planning")
        if v.family_importance >= 70:
            strengths.append("Strong family values")
        if v.communication_style in ["direct", "diplomatic"]:
            strengths.append(f"Clear communication style: {v.communication_style}")

        considerations = []
        if v.marriage_view == "not-interested":
            considerations.append("Not interested in marriage - important to align with partner")
        if v.children_plan == "want":
            considerations.append("Wants children - crucial alignment point")
        elif v.children_plan == "dont-want":
            considerations.append("Doesn't want children - crucial alignment point")
        if v.religion and v.religion_importance and v.religion_importance >= 70:
            considerations.append(f"Religion important - {v.religion} values matter")

        return ProfileDimension(
            name="Values",
            score=round(score, 1),
            strengths=strengths or ["Defined core values"],
            considerations=considerations or ["Flexible value system"],
        )

    def _analyze_interests(self, person: Person) -> ProfileDimension:
        """Analyze interests diversity and depth."""
        interests = person.interests

        # Score based on diversity and specificity
        num_categories = len(interests.categories)
        num_hobbies = len(interests.specific_hobbies)
        num_activities = len(interests.favorite_activities)

        # Diversity score
        diversity_score = min(100, num_categories * 12.5)  # 8 categories = 100

        # Depth score
        depth_score = min(100, (num_hobbies * 20 + num_activities * 15))

        score = diversity_score * 0.6 + depth_score * 0.4

        strengths = []
        if num_categories >= 5:
            strengths.append("Diverse range of interests")
        if num_hobbies >= 4:
            strengths.append("Well-developed hobbies")
        if "sports" in interests.categories or "outdoor" in interests.categories:
            strengths.append("Active lifestyle interests")
        if "arts" in interests.categories or "music" in interests.categories:
            strengths.append("Creative and cultural interests")

        considerations = []
        if num_categories <= 2:
            considerations.append("Limited interest diversity may reduce match opportunities")
        if num_hobbies <= 2:
            considerations.append("Could develop more specific hobbies for conversation")

        return ProfileDimension(
            name="Interests",
            score=round(score, 1),
            strengths=strengths or ["Has defined interests"],
            considerations=considerations or ["Balanced interests"],
        )

    def _calculate_completeness(self, person: Person) -> float:
        """Calculate profile completeness percentage."""
        completeness = 100.0  # Start with full if all required fields present

        # Optional fields that improve completeness
        if not person.occupation:
            completeness -= 5
        if not person.education:
            completeness -= 5
        if not person.bio:
            completeness -= 10
        if not person.partner_preferences:
            completeness -= 15
        if not person.personality.mbti:
            completeness -= 5

        return max(0, completeness)

    def _determine_profile_type(self, person: Person) -> str:
        """Determine overall profile type."""
        p = person.personality
        ls = person.lifestyle
        interests = person.interests

        # Simple classification logic
        if p.extraversion >= 70 and "travel" in interests.categories:
            return "outgoing-adventurer"
        elif p.openness >= 70 and p.extraversion <= 40:
            return "intellectual-homebody"
        elif ls.work_life_balance == "balanced" and p.agreeableness >= 70:
            return "balanced-social"
        elif "arts" in interests.categories and p.openness >= 70:
            return "creative-open-minded"
        elif ls.exercise_frequency in ["daily", "weekly"] and "outdoor" in interests.categories:
            return "active-health-conscious"
        else:
            return "well-rounded-balanced"

    def _determine_ideal_match(self, person: Person, profile_type: str) -> str:
        """Suggest ideal match type."""
        match_map = {
            "outgoing-adventurer": "adventurous-social-partner",
            "intellectual-homebody": "thoughtful-deep-thinker",
            "balanced-social": "empathetic-stable-partner",
            "creative-open-minded": "artistic-appreciative-partner",
            "active-health-conscious": "fitness-oriented-partner",
            "well-rounded-balanced": "compatible-balanced-partner",
        }
        return match_map.get(profile_type, "compatible-balanced-partner")

    def _identify_strengths(self, person: Person, dimensions: List[ProfileDimension]) -> List[str]:
        """Identify overall profile strengths."""
        strengths = []

        # Collect from dimensions
        for dim in dimensions:
            if dim.score >= 80:
                strengths.append(f"Strong {dim.name.lower()} profile")

        # Additional overall strengths
        if person.bio:
            strengths.append("Has thoughtful self-description")
        if person.partner_preferences:
            strengths.append("Clear about partner preferences")

        return strengths[:5]  # Top 5

    def _identify_weaknesses(self, person: Person, dimensions: List[ProfileDimension]) -> List[str]:
        """Identify areas for improvement."""
        weaknesses = []

        for dim in dimensions:
            if dim.score < 60:
                weaknesses.append(f"{dim.name} could be more developed")

        if not person.partner_preferences:
            weaknesses.append("Missing partner preferences")
        if not person.bio:
            weaknesses.append("Missing personal bio")

        return weaknesses

    def _generate_recommendations(self, person: Person, weaknesses: List[str]) -> List[str]:
        """Generate actionable recommendations."""
        recommendations = []

        if "Missing partner preferences" in str(weaknesses):
            recommendations.append("Define specific partner preferences to improve match quality")
        if "Missing personal bio" in str(weaknesses):
            recommendations.append("Add a personal bio to help matches understand you better")
        if "Interests" in str(weaknesses):
            recommendations.append("Develop more hobbies for better conversation topics")

        # Always add general advice
        recommendations.append("Keep profile updated as you grow and change")

        return recommendations[:5]

    def _assess_readiness(self, overall_score: float, completeness: float) -> str:
        """Assess dating readiness based on scores."""
        combined = (overall_score + completeness) / 2

        if combined >= 85:
            return "ready"
        elif combined >= 70:
            return "mostly-ready"
        elif combined >= 50:
            return "needs-work"
        else:
            return "not-ready"
