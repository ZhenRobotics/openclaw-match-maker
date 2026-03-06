"""Matcher - Intelligent matching algorithm for compatibility scoring."""

from typing import List
from matchmaker.types.person import Person
from matchmaker.types.models import MatchResult, CompatibilityScore
from datetime import datetime


class Matcher:
    """Calculates compatibility between two people using multi-dimensional algorithm."""

    def __init__(self, weights: dict = None):
        """
        Initialize matcher with optional custom weights.

        Args:
            weights: Custom weights for compatibility dimensions
        """
        self.weights = weights or {
            "personality": 0.30,
            "lifestyle": 0.25,
            "values": 0.30,
            "interests": 0.15,
        }

    async def calculate_compatibility(self, person1: Person, person2: Person) -> MatchResult:
        """
        Calculate comprehensive compatibility between two people.

        Args:
            person1: First person
            person2: Second person

        Returns:
            Complete match result with scores and insights
        """
        # Calculate component scores
        personality_score = self._match_personality(person1, person2)
        lifestyle_score = self._match_lifestyle(person1, person2)
        values_score = self._match_values(person1, person2)
        interests_score = self._match_interests(person1, person2)

        # Calculate overall score
        overall_score = (
            personality_score * self.weights["personality"]
            + lifestyle_score * self.weights["lifestyle"]
            + values_score * self.weights["values"]
            + interests_score * self.weights["interests"]
        )

        # Calculate complementarity
        complementarity = self._calculate_complementarity(person1, person2)

        # Determine match quality
        match_quality = self._determine_quality(overall_score)

        # Generate insights
        strengths = self._identify_strengths(person1, person2, personality_score, lifestyle_score, values_score, interests_score)
        challenges = self._identify_challenges(person1, person2, personality_score, lifestyle_score, values_score, interests_score)
        growth_areas = self._identify_growth_areas(person1, person2)

        # Create compatibility score
        compatibility = CompatibilityScore(
            overall_score=round(overall_score, 1),
            personality_compatibility=round(personality_score, 1),
            lifestyle_compatibility=round(lifestyle_score, 1),
            values_alignment=round(values_score, 1),
            interests_overlap=round(interests_score, 1),
            match_quality=match_quality,
            complementarity_score=round(complementarity, 1),
            strengths=strengths,
            challenges=challenges,
            growth_areas=growth_areas,
        )

        # Generate match insights
        why_good_match = self._why_good_match(person1, person2, compatibility)
        potential_issues = self._potential_issues(person1, person2, compatibility)
        relationship_potential = self._assess_potential(overall_score, complementarity)

        # Generate recommendations
        date_suggestions = self._suggest_first_dates(person1, person2)
        communication_tips = self._communication_tips(person1, person2)

        return MatchResult(
            person1_id=person1.id or f"person_{person1.name.replace(' ', '_').lower()}",
            person1_name=person1.name,
            person2_id=person2.id or f"person_{person2.name.replace(' ', '_').lower()}",
            person2_name=person2.name,
            compatibility=compatibility,
            why_good_match=why_good_match,
            potential_issues=potential_issues,
            relationship_potential=relationship_potential,
            first_date_suggestions=date_suggestions,
            communication_tips=communication_tips,
            match_date=datetime.now().strftime("%Y-%m-%d"),
        )

    def _match_personality(self, p1: Person, p2: Person) -> float:
        """Calculate personality compatibility."""
        pers1 = p1.personality
        pers2 = p2.personality

        # Some traits benefit from similarity, others from complementarity
        # Openness: similarity is good
        openness_match = 100 - abs(pers1.openness - pers2.openness)

        # Conscientiousness: moderate similarity
        conscientiousness_match = 100 - abs(pers1.conscientiousness - pers2.conscientiousness) * 0.7

        # Extraversion: can be complementary (not too extreme)
        extra_diff = abs(pers1.extraversion - pers2.extraversion)
        extraversion_match = 100 - extra_diff * 0.5 if extra_diff < 60 else 70  # Some difference okay

        # Agreeableness: similarity is good
        agreeableness_match = 100 - abs(pers1.agreeableness - pers2.agreeableness) * 0.8

        # Neuroticism: lower combined is better
        combined_neuroticism = (pers1.neuroticism + pers2.neuroticism) / 2
        neuroticism_match = 100 - combined_neuroticism * 0.6

        # Average
        score = (openness_match + conscientiousness_match + extraversion_match + agreeableness_match + neuroticism_match) / 5

        return max(0, min(100, score))

    def _match_lifestyle(self, p1: Person, p2: Person) -> float:
        """Calculate lifestyle compatibility."""
        ls1 = p1.lifestyle
        ls2 = p2.lifestyle

        score = 70.0  # Base score

        # Sleep schedule compatibility
        if ls1.sleep_schedule == ls2.sleep_schedule:
            score += 15
        elif (ls1.sleep_schedule == "flexible" or ls2.sleep_schedule == "flexible"):
            score += 10
        else:
            score -= 10  # Different schedules

        # Exercise compatibility
        exercise_compat = {"daily": 4, "weekly": 3, "rarely": 2, "never": 1}
        e1 = exercise_compat.get(ls1.exercise_frequency, 2)
        e2 = exercise_compat.get(ls2.exercise_frequency, 2)
        score += 10 - abs(e1 - e2) * 3

        # Social activity compatibility
        social_compat = {"very-social": 3, "moderately-social": 2, "homebody": 1}
        s1 = social_compat.get(ls1.social_activity, 2)
        s2 = social_compat.get(ls2.social_activity, 2)
        score += 10 - abs(s1 - s2) * 4

        # Work-life balance
        if ls1.work_life_balance == ls2.work_life_balance:
            score += 10
        elif "balanced" in [ls1.work_life_balance, ls2.work_life_balance]:
            score += 5

        # Smoking - critical compatibility
        if ls1.smoking == ls2.smoking:
            score += 10
        elif "never" in [ls1.smoking, ls2.smoking] and "regular" in [ls1.smoking, ls2.smoking]:
            score -= 20  # Major incompatibility

        # Drinking
        if ls1.drinking == ls2.drinking:
            score += 5

        # Pets
        if ls1.pets and ls2.pets:
            if "no-pets" in ls1.pets and "has-" in ls2.pets:
                score -= 10
            elif "has-" in ls1.pets and "has-" in ls2.pets:
                score += 5

        return max(0, min(100, score))

    def _match_values(self, p1: Person, p2: Person) -> float:
        """Calculate values alignment - most critical dimension."""
        v1 = p1.values
        v2 = p2.values

        score = 50.0  # Base score

        # Marriage view - very important
        marriage_compat = {
            ("priority", "priority"): 25,
            ("priority", "open"): 20,
            ("open", "open"): 20,
            ("open", "not-priority"): 15,
            ("not-priority", "not-priority"): 15,
            ("priority", "not-interested"): -20,
            ("open", "not-interested"): -10,
        }
        marriage_key = tuple(sorted([v1.marriage_view, v2.marriage_view]))
        score += marriage_compat.get(marriage_key, marriage_compat.get((v2.marriage_view, v1.marriage_view), 10))

        # Children plan - CRITICAL
        if v1.children_plan == v2.children_plan:
            score += 25  # Perfect alignment
        elif "open" in [v1.children_plan, v2.children_plan]:
            score += 15  # One is flexible
        elif v1.children_plan == "want" and v2.children_plan == "dont-want":
            score -= 30  # Deal breaker
        elif v1.children_plan == "dont-want" and v2.children_plan == "want":
            score -= 30  # Deal breaker

        # Family importance
        family_diff = abs(v1.family_importance - v2.family_importance)
        score += max(0, 15 - family_diff * 0.2)

        # Career importance - complementarity can work
        career_diff = abs(v1.career_importance - v2.career_importance)
        if career_diff < 30:
            score += 10
        else:
            score += 5  # Difference can work if acknowledged

        # Religion - if important to either, must align
        if v1.religion and v2.religion and v1.religion_importance and v2.religion_importance:
            if v1.religion_importance >= 70 or v2.religion_importance >= 70:
                if v1.religion == v2.religion:
                    score += 15
                else:
                    score -= 20  # Significant incompatibility

        # Communication style
        if v1.communication_style == v2.communication_style:
            score += 10
        elif "diplomatic" in [v1.communication_style, v2.communication_style]:
            score += 5  # Diplomatic can bridge differences

        return max(0, min(100, score))

    def _match_interests(self, p1: Person, p2: Person) -> float:
        """Calculate interests overlap."""
        int1 = p1.interests
        int2 = p2.interests

        # Category overlap
        common_categories = set(int1.categories) & set(int2.categories)
        category_score = len(common_categories) / max(len(int1.categories), len(int2.categories)) * 100

        # Hobby overlap
        common_hobbies = set(int1.specific_hobbies) & set(int2.specific_hobbies)
        hobby_score = len(common_hobbies) / max(len(int1.specific_hobbies), len(int2.specific_hobbies), 1) * 100

        # Activity overlap
        common_activities = set(int1.favorite_activities) & set(int2.favorite_activities)
        activity_score = len(common_activities) / max(len(int1.favorite_activities), len(int2.favorite_activities), 1) * 100

        # Weighted average (category overlap is most important)
        score = category_score * 0.5 + hobby_score * 0.3 + activity_score * 0.2

        # Bonus if they have complementary interests (some overlap, some unique)
        if 0.2 < len(common_categories) / len(set(int1.categories) | set(int2.categories)) < 0.7:
            score += 10  # Sweet spot - enough shared, enough to learn from each other

        return min(100, score)

    def _calculate_complementarity(self, p1: Person, p2: Person) -> float:
        """Calculate how well they complement each other."""
        score = 50.0

        # Personality complementarity
        p1_pers = p1.personality
        p2_pers = p2.personality

        # If one is highly neurotic, other should be stable
        if (p1_pers.neuroticism >= 70 and p2_pers.neuroticism <= 40) or \
           (p2_pers.neuroticism >= 70 and p1_pers.neuroticism <= 40):
            score += 15

        # If one is highly conscientious, it helps
        if max(p1_pers.conscientiousness, p2_pers.conscientiousness) >= 75:
            score += 10

        # Extraversion balance
        extra_avg = (p1_pers.extraversion + p2_pers.extraversion) / 2
        if 40 <= extra_avg <= 70:  # Balanced together
            score += 10

        # Lifestyle complementarity
        # If one is career-focused and other is family-focused, can work
        if abs(p1.values.career_importance - p2.values.family_importance) < 20:
            score += 10

        return min(100, score)

    def _determine_quality(self, overall_score: float) -> str:
        """Determine match quality label."""
        if overall_score >= 85:
            return "excellent"
        elif overall_score >= 75:
            return "very-good"
        elif overall_score >= 65:
            return "good"
        elif overall_score >= 50:
            return "fair"
        else:
            return "poor"

    def _identify_strengths(self, p1: Person, p2: Person, pers_score: float, life_score: float, val_score: float, int_score: float) -> List[str]:
        """Identify relationship strengths."""
        strengths = []

        if val_score >= 80:
            strengths.append("Strong alignment on core values and life goals")
        if pers_score >= 80:
            strengths.append("Highly compatible personalities")
        if int_score >= 70:
            strengths.append("Great shared interests for quality time together")
        if life_score >= 75:
            strengths.append("Compatible lifestyles and daily routines")

        # Specific alignments
        if p1.values.children_plan == p2.values.children_plan and p1.values.children_plan != "open":
            strengths.append(f"Perfect alignment on family planning: both {p1.values.children_plan} children")

        if p1.values.marriage_view == p2.values.marriage_view:
            strengths.append(f"Aligned on marriage: both {p1.values.marriage_view}")

        return strengths[:6]

    def _identify_challenges(self, p1: Person, p2: Person, pers_score: float, life_score: float, val_score: float, int_score: float) -> List[str]:
        """Identify potential challenges."""
        challenges = []

        if val_score < 60:
            challenges.append("Significant differences in core values - will need open communication")
        if life_score < 60:
            challenges.append("Different lifestyles may require compromise and flexibility")
        if int_score < 40:
            challenges.append("Limited shared interests - will need to explore new activities together")

        # Specific issues
        if p1.lifestyle.sleep_schedule != p2.lifestyle.sleep_schedule and "flexible" not in [p1.lifestyle.sleep_schedule, p2.lifestyle.sleep_schedule]:
            challenges.append(f"Different sleep schedules: {p1.name} is {p1.lifestyle.sleep_schedule}, {p2.name} is {p2.lifestyle.sleep_schedule}")

        if p1.values.children_plan != p2.values.children_plan and "open" not in [p1.values.children_plan, p2.values.children_plan]:
            challenges.append("Different views on having children - requires serious discussion")

        return challenges[:5]

    def _identify_growth_areas(self, p1: Person, p2: Person) -> List[str]:
        """Identify areas for mutual growth."""
        return [
            "Learning from each other's unique perspectives and experiences",
            "Developing new shared interests and activities",
            "Supporting each other's personal and professional goals",
            "Building strong communication patterns from the start",
        ]

    def _why_good_match(self, p1: Person, p2: Person, compatibility: CompatibilityScore) -> List[str]:
        """Generate reasons why this is a good match."""
        reasons = []

        if compatibility.overall_score >= 75:
            reasons.append(f"High overall compatibility score of {compatibility.overall_score}/100")

        if compatibility.values_alignment >= 75:
            reasons.append("Strong alignment on life goals and values")

        # Find specific commonalities
        common_interests = set(p1.interests.categories) & set(p2.interests.categories)
        if common_interests:
            reasons.append(f"Shared interests: {', '.join(list(common_interests)[:3])}")

        if abs(p1.age - p2.age) <= 5:
            reasons.append("Similar life stage and age")

        if p1.values.communication_style == p2.values.communication_style:
            reasons.append(f"Compatible communication styles: both {p1.values.communication_style}")

        return reasons[:5]

    def _potential_issues(self, p1: Person, p2: Person, compatibility: CompatibilityScore) -> List[str]:
        """Identify potential issues to be aware of."""
        issues = []

        if compatibility.values_alignment < 65:
            issues.append("Values differences may require ongoing discussion and compromise")

        if p1.lifestyle.sleep_schedule != p2.lifestyle.sleep_schedule:
            issues.append("Different daily schedules may limit time together")

        if compatibility.interests_overlap < 50:
            issues.append("Will need to actively build shared activities and interests")

        return issues if issues else ["No major issues identified - good match overall"]

    def _assess_potential(self, overall_score: float, complementarity: float) -> str:
        """Assess long-term relationship potential."""
        combined = (overall_score + complementarity) / 2

        if combined >= 80:
            return "high"
        elif combined >= 70:
            return "medium-high"
        elif combined >= 55:
            return "medium"
        elif combined >= 40:
            return "medium-low"
        else:
            return "low"

    def _suggest_first_dates(self, p1: Person, p2: Person) -> List[str]:
        """Suggest personalized first date ideas."""
        suggestions = []

        common_interests = set(p1.interests.categories) & set(p2.interests.categories)

        if "coffee" in str(p1.interests.favorite_activities).lower() or "coffee" in str(p2.interests.favorite_activities).lower():
            suggestions.append("Coffee date at a cozy cafe - low pressure, good for conversation")

        if "arts" in common_interests:
            suggestions.append("Visit an art museum or gallery - shared interest to discuss")

        if "outdoor" in common_interests or "sports" in common_interests:
            suggestions.append("Scenic walk or light hike - active and allows natural conversation")

        if "music" in common_interests:
            suggestions.append("Live music venue or concert - enjoy music together")

        if "cooking" in common_interests or "cooking" in p1.interests.specific_hobbies + p2.interests.specific_hobbies:
            suggestions.append("Cooking class or food market tour - interactive and fun")

        # Default suggestions
        if not suggestions:
            suggestions = [
                "Coffee or drinks at a popular local spot",
                "Casual dinner at a restaurant with good ambiance",
                "Walk in a scenic park or neighborhood",
            ]

        return suggestions[:5]

    def _communication_tips(self, p1: Person, p2: Person) -> List[str]:
        """Provide communication tips based on personalities."""
        tips = []

        # Based on communication styles
        if p1.values.communication_style == "direct" and p2.values.communication_style == "avoid-conflict":
            tips.append(f"{p1.name}: Be gentle with directness. {p2.name}: Practice speaking up when something matters")

        if p1.values.communication_style == p2.values.communication_style == "diplomatic":
            tips.append("Both diplomatic - great! Just ensure you're also honest about needs and boundaries")

        # Based on personality
        if p1.personality.extraversion >= 70 and p2.personality.extraversion <= 40:
            tips.append(f"{p1.name}: Give {p2.name} space to recharge. {p2.name}: Communicate social needs clearly")

        if p1.personality.neuroticism >= 70 or p2.personality.neuroticism >= 70:
            tips.append("Create a safe space for expressing feelings without judgment")

        # General tips
        tips.append("Ask open-ended questions to learn about each other deeply")
        tips.append("Share your expectations and goals early to ensure alignment")

        return tips[:5]
