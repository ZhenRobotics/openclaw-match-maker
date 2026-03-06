"""
Basic example demonstrating Matchmaker usage.

This example shows:
1. Creating person profiles
2. Analyzing profiles
3. Finding match compatibility
4. Generating icebreakers
"""

import asyncio
from matchmaker import Matchmaker, Person, PersonalityTraits, Lifestyle, Values, Interests


async def main():
    # Initialize matchmaker
    matchmaker = Matchmaker()

    # Create first person profile
    alex = Person(
        name="Alex Chen",
        age=28,
        gender="male",
        location="San Francisco, CA",
        personality=PersonalityTraits(
            openness=85,
            conscientiousness=70,
            extraversion=60,
            agreeableness=75,
            neuroticism=40,
            mbti="ENFP"
        ),
        lifestyle=Lifestyle(
            sleep_schedule="night-owl",
            exercise_frequency="weekly",
            social_activity="moderately-social",
            work_life_balance="balanced",
            travel_frequency="occasional",
            pets="has-dogs",
            smoking="never",
            drinking="social",
            diet="omnivore"
        ),
        values=Values(
            marriage_view="open",
            children_plan="want",
            family_importance=80,
            career_importance=70,
            religion="none",
            money_attitude="balanced",
            communication_style="diplomatic"
        ),
        interests=Interests(
            categories=["tech", "travel", "music", "cooking"],
            specific_hobbies=["photography", "hiking", "guitar", "cooking"],
            favorite_activities=["coffee date", "museum visit", "outdoor concert"]
        ),
        occupation="Software Engineer",
        education="Bachelor's Degree",
        bio="Tech professional who loves exploring new restaurants and outdoor adventures on weekends."
    )

    # Create second person profile
    jamie = Person(
        name="Jamie Taylor",
        age=27,
        gender="female",
        location="San Francisco, CA",
        personality=PersonalityTraits(
            openness=80,
            conscientiousness=75,
            extraversion=55,
            agreeableness=80,
            neuroticism=35,
            mbti="INFJ"
        ),
        lifestyle=Lifestyle(
            sleep_schedule="flexible",
            exercise_frequency="weekly",
            social_activity="moderately-social",
            work_life_balance="balanced",
            travel_frequency="frequent",
            pets="want-pets",
            smoking="never",
            drinking="social",
            diet="vegetarian"
        ),
        values=Values(
            marriage_view="open",
            children_plan="want",
            family_importance=85,
            career_importance=65,
            religion="none",
            money_attitude="balanced",
            communication_style="direct"
        ),
        interests=Interests(
            categories=["travel", "arts", "music", "cooking"],
            specific_hobbies=["painting", "yoga", "cooking", "photography"],
            favorite_activities=["art gallery", "hiking", "cooking together"]
        ),
        occupation="UX Designer",
        education="Master's Degree",
        bio="Creative soul who finds joy in art, travel, and meaningful conversations over good food."
    )

    print("=" * 60)
    print("MATCHMAKER DEMO")
    print("=" * 60)
    print()

    # 1. Analyze Alex's profile
    print("1. PROFILE ANALYSIS: Alex Chen")
    print("-" * 60)
    alex_profile = await matchmaker.analyze_profile(alex)
    print(f"Overall Score: {alex_profile.overall_score}/100")
    print(f"Dating Readiness: {alex_profile.dating_readiness}")
    print(f"Profile Type: {alex_profile.profile_type}")
    print(f"Ideal Match Type: {alex_profile.ideal_match_type}")
    print()
    print("Strengths:")
    for strength in alex_profile.strengths:
        print(f"  ✓ {strength}")
    print()
    print("Recommendations:")
    for rec in alex_profile.recommendations:
        print(f"  → {rec}")
    print()

    # 2. Analyze Jamie's profile
    print("2. PROFILE ANALYSIS: Jamie Taylor")
    print("-" * 60)
    jamie_profile = await matchmaker.analyze_profile(jamie)
    print(f"Overall Score: {jamie_profile.overall_score}/100")
    print(f"Dating Readiness: {jamie_profile.dating_readiness}")
    print(f"Profile Type: {jamie_profile.profile_type}")
    print()

    # 3. Find match compatibility
    print("3. COMPATIBILITY ANALYSIS: Alex & Jamie")
    print("-" * 60)
    match = await matchmaker.find_match(alex, jamie)
    print(f"Overall Compatibility: {match.compatibility.overall_score}/100")
    print(f"Match Quality: {match.compatibility.match_quality}")
    print(f"Relationship Potential: {match.relationship_potential}")
    print()
    print("Dimension Scores:")
    print(f"  • Personality: {match.compatibility.personality_compatibility}/100")
    print(f"  • Lifestyle: {match.compatibility.lifestyle_compatibility}/100")
    print(f"  • Values: {match.compatibility.values_alignment}/100")
    print(f"  • Interests: {match.compatibility.interests_overlap}/100")
    print()
    print("Why Good Match:")
    for reason in match.why_good_match:
        print(f"  ✓ {reason}")
    print()
    print("Potential Challenges:")
    for issue in match.potential_issues:
        print(f"  ⚠ {issue}")
    print()

    # 4. Generate icebreakers
    print("4. ICEBREAKER SUGGESTIONS: Alex → Jamie")
    print("-" * 60)
    icebreakers = await matchmaker.generate_icebreakers(alex, jamie)
    print("Opening Lines (choose one):")
    for i, line in enumerate(icebreakers.opening_lines[:3], 1):
        print(f"  {i}. {line}")
    print()
    print("Shared Interests to Discuss:")
    for topic in icebreakers.shared_interests[:4]:
        print(f"  • {topic}")
    print()
    print("First Date Ideas:")
    for idea in icebreakers.date_ideas[:3]:
        print(f"  • {idea['activity']}")
        print(f"    Reason: {idea['reason']}")
    print()
    print("Personality Tips:")
    for tip in icebreakers.personality_tips[:3]:
        print(f"  → {tip}")
    print()

    print("=" * 60)
    print("DEMO COMPLETE!")
    print("=" * 60)
    print()
    print(f"Verdict: Alex and Jamie have a {match.compatibility.match_quality} match")
    print(f"with {match.compatibility.overall_score}/100 compatibility!")
    print()


if __name__ == "__main__":
    asyncio.run(main())
