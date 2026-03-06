"""
Matchmaker - Main class providing all matchmaking services.

This is the primary interface for the Matchmaker system.
"""

from typing import List, Optional
from matchmaker.types.person import Person
from matchmaker.types.profile import Profile
from matchmaker.types.models import MatchResult, IcebreakerSuggestion, RelationshipAssessment, InteractionLog
from matchmaker.modules.profiling.profiler import Profiler
from matchmaker.modules.matching.matcher import Matcher
from matchmaker.modules.icebreaker.ice_generator import IcebreakerGenerator
from matchmaker.modules.relationship.assessor import RelationshipAssessor


class Matchmaker:
    """
    Main Matchmaker class providing AI-powered dating match services.

    Services:
    - Profile analysis and scoring
    - Compatibility matching between two people
    - Personalized icebreaker and conversation suggestions
    - Relationship progress tracking and assessment
    """

    def __init__(
        self,
        profiling_weights: Optional[dict] = None,
        matching_weights: Optional[dict] = None,
    ):
        """
        Initialize Matchmaker with optional custom weights.

        Args:
            profiling_weights: Custom weights for profile dimensions
            matching_weights: Custom weights for matching dimensions
        """
        self.profiler = Profiler(weights=profiling_weights)
        self.matcher = Matcher(weights=matching_weights)
        self.icebreaker_generator = IcebreakerGenerator()
        self.relationship_assessor = RelationshipAssessor()

    # ==================== Profile Analysis ====================

    async def analyze_profile(self, person: Person) -> Profile:
        """
        Analyze a person's profile and generate detailed assessment.

        Args:
            person: Person object with complete information

        Returns:
            Profile with multi-dimensional scores and recommendations

        Example:
            ```python
            matchmaker = Matchmaker()
            profile = await matchmaker.analyze_profile(person)
            print(f"Dating readiness: {profile.dating_readiness}")
            print(f"Overall score: {profile.overall_score}/100")
            ```
        """
        return await self.profiler.analyze_person(person)

    # ==================== Matching ====================

    async def find_match(self, person1: Person, person2: Person) -> MatchResult:
        """
        Calculate compatibility between two people.

        Args:
            person1: First person
            person2: Second person

        Returns:
            Complete match result with compatibility scores and insights

        Example:
            ```python
            matchmaker = Matchmaker()
            match = await matchmaker.find_match(alex, jamie)
            print(f"Compatibility: {match.compatibility.overall_score}/100")
            print(f"Match quality: {match.compatibility.match_quality}")
            ```
        """
        return await self.matcher.calculate_compatibility(person1, person2)

    async def batch_match(self, person: Person, candidates: List[Person], top_n: int = 10) -> List[MatchResult]:
        """
        Match one person against multiple candidates and return top matches.

        Args:
            person: The person looking for matches
            candidates: List of potential matches
            top_n: Number of top matches to return

        Returns:
            List of top match results sorted by compatibility score

        Example:
            ```python
            matchmaker = Matchmaker()
            top_matches = await matchmaker.batch_match(alex, all_candidates, top_n=5)
            for match in top_matches:
                print(f"{match.person2_name}: {match.compatibility.overall_score}/100")
            ```
        """
        matches = []
        for candidate in candidates:
            match = await self.matcher.calculate_compatibility(person, candidate)
            matches.append(match)

        # Sort by overall compatibility score
        matches.sort(key=lambda m: m.compatibility.overall_score, reverse=True)

        return matches[:top_n]

    # ==================== Icebreakers ====================

    async def generate_icebreakers(self, person: Person, match: Person) -> IcebreakerSuggestion:
        """
        Generate personalized icebreakers and conversation starters.

        Args:
            person: The person who will initiate
            match: The person they matched with

        Returns:
            Complete icebreaker suggestions including opening lines, topics, and date ideas

        Example:
            ```python
            matchmaker = Matchmaker()
            icebreakers = await matchmaker.generate_icebreakers(alex, jamie)
            print("Opening lines:")
            for line in icebreakers.opening_lines:
                print(f"  - {line}")
            ```
        """
        return await self.icebreaker_generator.generate_icebreakers(person, match)

    # ==================== Relationship Assessment ====================

    async def assess_relationship(
        self,
        person1: Person,
        person2: Person,
        interactions: List[InteractionLog],
    ) -> RelationshipAssessment:
        """
        Assess relationship health and progress based on interaction history.

        Args:
            person1: First person
            person2: Second person
            interactions: List of logged interactions between them

        Returns:
            Complete relationship assessment with health score and recommendations

        Example:
            ```python
            matchmaker = Matchmaker()
            interactions = [
                InteractionLog(date="2024-03-01", type="message", quality="good"),
                InteractionLog(date="2024-03-02", type="date", quality="excellent"),
            ]
            assessment = await matchmaker.assess_relationship(alex, jamie, interactions)
            print(f"Relationship health: {assessment.relationship_health}/100")
            print(f"Stage: {assessment.relationship_stage}")
            ```
        """
        return await self.relationship_assessor.assess_relationship(person1, person2, interactions)

    # ==================== Combined Workflows ====================

    async def complete_match_analysis(self, person1: Person, person2: Person) -> dict:
        """
        Run complete match analysis including compatibility, icebreakers, and recommendations.

        Args:
            person1: First person
            person2: Second person

        Returns:
            Dictionary containing match result and icebreaker suggestions

        Example:
            ```python
            matchmaker = Matchmaker()
            analysis = await matchmaker.complete_match_analysis(alex, jamie)
            print("Compatibility:", analysis['match'].compatibility.overall_score)
            print("First date ideas:", analysis['icebreakers'].date_ideas)
            ```
        """
        # Get match result
        match_result = await self.find_match(person1, person2)

        # Generate icebreakers
        icebreakers = await self.generate_icebreakers(person1, person2)

        return {
            "match": match_result,
            "icebreakers": icebreakers,
        }

    async def full_profile_and_matches(
        self,
        person: Person,
        candidates: List[Person],
        top_n: int = 5,
    ) -> dict:
        """
        Analyze person's profile and find their best matches.

        Args:
            person: The person's profile to analyze
            candidates: List of potential matches
            top_n: Number of top matches to return

        Returns:
            Dictionary containing profile analysis and top matches

        Example:
            ```python
            matchmaker = Matchmaker()
            result = await matchmaker.full_profile_and_matches(alex, all_candidates)
            print("Profile score:", result['profile'].overall_score)
            print("Top match:", result['matches'][0].person2_name)
            ```
        """
        # Analyze person's profile
        profile = await self.analyze_profile(person)

        # Find top matches
        top_matches = await self.batch_match(person, candidates, top_n)

        return {
            "profile": profile,
            "matches": top_matches,
        }
