"""RelationshipAssessor - Tracks and evaluates relationship development."""

from typing import List, Optional
from matchmaker.types.person import Person
from matchmaker.types.models import RelationshipAssessment, InteractionLog


class RelationshipAssessor:
    """Assesses relationship health and progress based on interaction history."""

    async def assess_relationship(
        self,
        person1: Person,
        person2: Person,
        interactions: List[InteractionLog],
    ) -> RelationshipAssessment:
        """
        Assess the current state and health of a developing relationship.

        Args:
            person1: First person
            person2: Second person
            interactions: List of logged interactions

        Returns:
            Complete relationship assessment with analysis and recommendations
        """
        # Analyze interaction patterns
        total_interactions = len(interactions)

        # Determine relationship stage
        stage = self._determine_stage(interactions)

        # Calculate health score
        health_score = self._calculate_health(interactions)

        # Analyze patterns
        positive_indicators = self._identify_positives(interactions)
        concerns = self._identify_concerns(interactions)
        momentum = self._assess_momentum(interactions)

        # Communication analysis
        comm_quality = self._assess_communication_quality(interactions)
        comm_balance = self._assess_communication_balance(interactions, person1, person2)
        response_pattern = self._assess_response_pattern(interactions)

        # Generate recommendations
        next_steps = self._generate_next_steps(stage, health_score, interactions)
        red_flags = self._identify_red_flags(interactions, health_score)
        green_flags = self._identify_green_flags(interactions, health_score)

        # Prediction
        success_likelihood = self._predict_success(health_score, momentum, stage)
        timeline = self._predict_timeline(stage, momentum)

        return RelationshipAssessment(
            person1_id=person1.id or f"person_{person1.name.replace(' ', '_').lower()}",
            person2_id=person2.id or f"person_{person2.name.replace(' ', '_').lower()}",
            total_interactions=total_interactions,
            interaction_logs=interactions[-10:] if len(interactions) > 10 else interactions,  # Last 10
            relationship_stage=stage,
            relationship_health=health_score,
            positive_indicators=positive_indicators,
            concerns=concerns,
            momentum=momentum,
            communication_quality=comm_quality,
            communication_balance=comm_balance,
            response_pattern=response_pattern,
            next_steps=next_steps,
            red_flags=red_flags,
            green_flags=green_flags,
            success_likelihood=success_likelihood,
            timeline_prediction=timeline,
        )

    def _determine_stage(self, interactions: List[InteractionLog]) -> str:
        """Determine current relationship stage."""
        if not interactions:
            return "initial-contact"

        total = len(interactions)

        # Count dates vs messages
        dates = sum(1 for i in interactions if i.type == "date")
        messages = sum(1 for i in interactions if i.type == "message")
        calls = sum(1 for i in interactions if i.type == "call")

        # Stage logic
        if total <= 3:
            return "initial-contact"
        elif total <= 10 and dates == 0:
            return "getting-to-know"
        elif dates >= 1 and dates <= 3:
            return "dating"
        elif dates >= 4 or (dates >= 2 and calls >= 3):
            return "committed"
        elif dates >= 8 and total >= 30:
            return "serious"
        else:
            return "getting-to-know"

    def _calculate_health(self, interactions: List[InteractionLog]) -> float:
        """Calculate overall relationship health score."""
        if not interactions:
            return 50.0

        score = 60.0  # Base score

        # Quality analysis
        recent_quality = [i.quality for i in interactions[-5:]]  # Last 5
        excellent_count = recent_quality.count("excellent")
        good_count = recent_quality.count("good")
        poor_count = recent_quality.count("poor")

        score += excellent_count * 8
        score += good_count * 4
        score -= poor_count * 10

        # Frequency analysis
        if len(interactions) >= 10:
            score += 10  # Consistent engagement

        # Progression (dates vs just messages)
        dates = sum(1 for i in interactions if i.type == "date")
        if dates >= 2:
            score += 15  # Progressing beyond texting

        # Recent activity
        if len(interactions) >= 3:
            last_three_quality = [i.quality for i in interactions[-3:]]
            if "poor" not in last_three_quality:
                score += 10  # Recent interactions are positive

        return max(0, min(100, score))

    def _identify_positives(self, interactions: List[InteractionLog]) -> List[str]:
        """Identify positive indicators in the relationship."""
        positives = []

        if not interactions:
            return ["Just getting started - exciting times ahead!"]

        # Quality analysis
        excellent_recent = sum(1 for i in interactions[-5:] if i.quality == "excellent")
        if excellent_recent >= 3:
            positives.append("Recent interactions have been excellent quality")

        # Progression
        dates = sum(1 for i in interactions if i.type == "date")
        if dates >= 2:
            positives.append(f"You've had {dates} dates together - relationship is progressing")

        # Variety
        types = set(i.type for i in interactions)
        if len(types) >= 3:
            positives.append("Good variety in interaction types (messages, calls, dates)")

        # Consistency
        if len(interactions) >= 8:
            positives.append("Consistent engagement over time")

        # Recent momentum
        if len(interactions) >= 5:
            recent_dates = sum(1 for i in interactions[-5:] if i.type == "date")
            if recent_dates >= 2:
                positives.append("Recent increase in in-person time together")

        return positives if positives else ["Building connection steadily"]

    def _identify_concerns(self, interactions: List[InteractionLog]) -> List[str]:
        """Identify potential concerns."""
        concerns = []

        if not interactions:
            return []

        # Quality issues
        recent_poor = sum(1 for i in interactions[-5:] if i.quality == "poor")
        if recent_poor >= 2:
            concerns.append("Multiple recent interactions have been lower quality - worth discussing")

        # Lack of progression
        dates = sum(1 for i in interactions if i.type == "date")
        if len(interactions) >= 10 and dates == 0:
            concerns.append("Many interactions but haven't met in person yet - consider planning a date")

        # Declining quality trend
        if len(interactions) >= 6:
            first_half_quality = [i.quality for i in interactions[:len(interactions)//2]]
            second_half_quality = [i.quality for i in interactions[len(interactions)//2:]]

            first_excellent = first_half_quality.count("excellent")
            second_excellent = second_half_quality.count("excellent")

            if first_excellent > second_excellent + 2:
                concerns.append("Quality seems to be declining over time")

        # Low overall quality
        if len(interactions) >= 5:
            poor_ratio = sum(1 for i in interactions if i.quality == "poor") / len(interactions)
            if poor_ratio > 0.3:
                concerns.append("High proportion of poor-quality interactions - may indicate incompatibility")

        return concerns if concerns else []

    def _assess_momentum(self, interactions: List[InteractionLog]) -> str:
        """Assess relationship momentum."""
        if not interactions or len(interactions) < 3:
            return "steady"

        # Compare recent vs earlier
        if len(interactions) >= 6:
            earlier = interactions[:len(interactions)//2]
            recent = interactions[len(interactions)//2:]

            earlier_excellent = sum(1 for i in earlier if i.quality == "excellent")
            recent_excellent = sum(1 for i in recent if i.quality == "excellent")

            if recent_excellent > earlier_excellent + 1:
                return "accelerating"
            elif recent_excellent < earlier_excellent - 1:
                return "slowing"

        # Check for dates
        recent_dates = sum(1 for i in interactions[-5:] if i.type == "date")
        earlier_dates = sum(1 for i in interactions[:-5] if i.type == "date") if len(interactions) > 5 else 0

        if recent_dates > earlier_dates:
            return "accelerating"
        elif earlier_dates > recent_dates and recent_dates == 0:
            return "slowing"

        # Check for stalling
        if len(interactions) >= 10:
            last_five_types = [i.type for i in interactions[-5:]]
            if all(t == "message" for t in last_five_types):
                return "stalled"

        return "steady"

    def _assess_communication_quality(self, interactions: List[InteractionLog]) -> float:
        """Assess communication quality score."""
        if not interactions:
            return 50.0

        quality_scores = {
            "excellent": 100,
            "good": 75,
            "okay": 50,
            "poor": 25,
        }

        scores = [quality_scores.get(i.quality, 50) for i in interactions]
        return sum(scores) / len(scores)

    def _assess_communication_balance(self, interactions: List[InteractionLog], p1: Person, p2: Person) -> str:
        """Assess if communication is balanced."""
        # This would require tracking who initiated each interaction
        # For now, return based on interaction patterns

        if len(interactions) < 5:
            return "balanced"  # Too early to tell

        # Look at interaction types - varied types suggest mutual initiation
        types = [i.type for i in interactions]
        if len(set(types)) >= 2:
            return "balanced"
        else:
            return "balanced"  # Would need more data to determine

    def _assess_response_pattern(self, interactions: List[InteractionLog]) -> str:
        """Assess responsiveness pattern."""
        if not interactions:
            return "mutual-engaged"

        # Quality pattern indicates engagement
        recent_quality = [i.quality for i in interactions[-5:]]

        excellent_count = recent_quality.count("excellent")
        good_count = recent_quality.count("good")
        poor_count = recent_quality.count("poor")

        if excellent_count >= 3 or (excellent_count + good_count >= 4):
            return "mutual-engaged"
        elif poor_count >= 3:
            return "declining"
        else:
            return "uneven"

    def _generate_next_steps(self, stage: str, health_score: float, interactions: List[InteractionLog]) -> List[str]:
        """Generate recommended next steps."""
        steps = []

        if stage == "initial-contact":
            steps.append("Continue getting to know each other through messages and calls")
            steps.append("Plan your first in-person date when you both feel ready")
            steps.append("Ask deeper questions to understand values and compatibility")

        elif stage == "getting-to-know":
            steps.append("Transition from messaging to in-person dates")
            steps.append("Share more about your life goals and values")
            steps.append("Plan a date that involves a shared interest")

        elif stage == "dating":
            steps.append("Have conversations about relationship expectations")
            steps.append("Introduce each other to your social circles if ready")
            steps.append("Discuss exclusivity if it feels right")

        elif stage == "committed":
            steps.append("Continue building deeper emotional intimacy")
            steps.append("Have important conversations about future plans")
            steps.append("Navigate challenges together to build resilience")

        elif stage == "serious":
            steps.append("Discuss long-term plans and alignment")
            steps.append("Meet each other's families if appropriate")
            steps.append("Consider next steps in the relationship")

        # Health-based recommendations
        if health_score < 60:
            steps.append("Have an honest conversation about how things are going")
            steps.append("Address any concerns or misunderstandings directly")

        # Interaction-based
        dates = sum(1 for i in interactions if i.type == "date")
        if dates == 0 and len(interactions) >= 5:
            steps.insert(0, "PRIORITY: Plan your first in-person date soon")

        return steps[:5]

    def _identify_red_flags(self, interactions: List[InteractionLog], health_score: float) -> List[str]:
        """Identify red flags to watch for."""
        flags = []

        if not interactions:
            return []

        # Quality concerns
        poor_ratio = sum(1 for i in interactions if i.quality == "poor") / len(interactions) if interactions else 0
        if poor_ratio > 0.4:
            flags.append("High proportion of poor interactions - may indicate incompatibility")

        # Lack of progression
        dates = sum(1 for i in interactions if i.type == "date")
        if len(interactions) >= 12 and dates == 0:
            flags.append("No in-person meetings after many interactions - one party may not be serious")

        # Declining pattern
        if len(interactions) >= 6:
            recent_quality = [i.quality for i in interactions[-3:]]
            if all(q in ["poor", "okay"] for q in recent_quality):
                flags.append("Recent decline in interaction quality - needs attention")

        # Very low health
        if health_score < 40:
            flags.append("Overall relationship health is low - consider if this is the right match")

        return flags if flags else []

    def _identify_green_flags(self, interactions: List[InteractionLog], health_score: float) -> List[str]:
        """Identify positive signs to celebrate."""
        flags = []

        if not interactions:
            return ["You're taking the first step - that's brave!"]

        # High quality
        excellent_ratio = sum(1 for i in interactions if i.quality == "excellent") / len(interactions) if interactions else 0
        if excellent_ratio > 0.5:
            flags.append("More than half of interactions are excellent - great chemistry!")

        # Good progression
        dates = sum(1 for i in interactions if i.type == "date")
        if dates >= 3 and len(interactions) <= 15:
            flags.append("Healthy progression from messaging to regular in-person dates")

        # Variety
        types = set(i.type for i in interactions)
        if len(types) >= 3:
            flags.append("Diverse communication (messages, calls, dates) shows balanced connection")

        # High health
        if health_score >= 80:
            flags.append("Excellent relationship health - you're building something special")

        # Consistency
        if len(interactions) >= 10:
            flags.append("Consistent engagement over time - both parties are invested")

        return flags if flags else ["Keep building connection at your own pace"]

    def _predict_success(self, health_score: float, momentum: str, stage: str) -> str:
        """Predict success likelihood."""
        # Base on health score
        if health_score >= 80:
            base = "high"
        elif health_score >= 65:
            base = "moderate"
        elif health_score >= 50:
            base = "moderate"
        else:
            base = "low"

        # Adjust for momentum
        if momentum == "accelerating" and base in ["moderate", "high"]:
            return "very-high" if base == "high" else "high"
        elif momentum == "slowing" and base == "high":
            return "moderate"
        elif momentum == "stalled":
            return "low" if base != "high" else "moderate"

        return base

    def _predict_timeline(self, stage: str, momentum: str) -> Optional[str]:
        """Predict timeline for next milestone."""
        timelines = {
            "initial-contact": "First date likely within 1-2 weeks if mutual interest",
            "getting-to-know": "May become exclusive within 1-2 months if compatibility high",
            "dating": "Likely to become committed within 2-3 months if going well",
            "committed": "May discuss long-term plans within 6-12 months",
            "serious": "Major relationship decisions likely within 6-18 months",
        }

        timeline = timelines.get(stage)

        if momentum == "accelerating":
            return f"{timeline} (potentially faster given current momentum)"
        elif momentum == "stalled":
            return f"{timeline} (may take longer given current pace)"
        else:
            return timeline
