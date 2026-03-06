"""
Complete test suite for Matchmaker system.

Tests all 4 core modules:
1. Profile analysis
2. Compatibility matching
3. Icebreaker generation
4. Relationship assessment
"""

import asyncio
from matchmaker import (
    Matchmaker,
    Person,
    PersonalityTraits,
    Lifestyle,
    Values,
    Interests,
    InteractionLog
)


def create_test_person1() -> Person:
    """Create first test person."""
    return Person(
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
        bio="Tech professional who loves exploring new restaurants."
    )


def create_test_person2() -> Person:
    """Create second test person."""
    return Person(
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
        bio="Creative soul who finds joy in art and travel."
    )


async def test_profile_analysis():
    """Test 1: Profile Analysis"""
    print("Testing 1/4: Profile Analysis...")

    matchmaker = Matchmaker()
    person = create_test_person1()

    profile = await matchmaker.analyze_profile(person)

    # Assertions
    assert profile.overall_score > 0 and profile.overall_score <= 100, "Overall score out of range"
    assert profile.profile_completeness > 0, "Completeness should be positive"
    assert len(profile.strengths) > 0, "Should have at least one strength"
    assert profile.dating_readiness in ["ready", "mostly-ready", "needs-work", "not-ready"], "Invalid readiness"

    print(f"  ✓ Profile Score: {profile.overall_score}/100")
    print(f"  ✓ Dating Readiness: {profile.dating_readiness}")
    print(f"  ✓ Profile Type: {profile.profile_type}")
    return True


async def test_compatibility_matching():
    """Test 2: Compatibility Matching"""
    print("Testing 2/4: Compatibility Matching...")

    matchmaker = Matchmaker()
    person1 = create_test_person1()
    person2 = create_test_person2()

    match = await matchmaker.find_match(person1, person2)

    # Assertions
    assert match.compatibility.overall_score >= 0 and match.compatibility.overall_score <= 100, "Score out of range"
    assert match.compatibility.personality_compatibility >= 0, "Personality score should be >= 0"
    assert match.compatibility.lifestyle_compatibility >= 0, "Lifestyle score should be >= 0"
    assert match.compatibility.values_alignment >= 0, "Values score should be >= 0"
    assert match.compatibility.interests_overlap >= 0, "Interests score should be >= 0"
    assert len(match.why_good_match) > 0, "Should have reasons for match"

    print(f"  ✓ Overall Compatibility: {match.compatibility.overall_score}/100")
    print(f"  ✓ Match Quality: {match.compatibility.match_quality}")
    print(f"  ✓ Reasons: {len(match.why_good_match)} identified")
    return True


async def test_icebreaker_generation():
    """Test 3: Icebreaker Generation"""
    print("Testing 3/4: Icebreaker Generation...")

    matchmaker = Matchmaker()
    person1 = create_test_person1()
    person2 = create_test_person2()

    icebreakers = await matchmaker.generate_icebreakers(person1, person2)

    # Assertions
    assert len(icebreakers.opening_lines) > 0, "Should have opening lines"
    assert len(icebreakers.questions_to_ask) > 0, "Should have questions"
    assert len(icebreakers.date_ideas) > 0, "Should have date ideas"
    assert icebreakers.style_advice, "Should have style advice"

    print(f"  ✓ Opening Lines: {len(icebreakers.opening_lines)}")
    print(f"  ✓ Questions: {len(icebreakers.questions_to_ask)}")
    print(f"  ✓ Date Ideas: {len(icebreakers.date_ideas)}")
    return True


async def test_relationship_assessment():
    """Test 4: Relationship Assessment"""
    print("Testing 4/4: Relationship Assessment...")

    matchmaker = Matchmaker()
    person1 = create_test_person1()
    person2 = create_test_person2()

    # Create interaction history
    interactions = [
        InteractionLog(date="2024-03-01", type="message", quality="good", notes="Great conversation"),
        InteractionLog(date="2024-03-02", type="message", quality="excellent", notes="Really clicked"),
        InteractionLog(date="2024-03-05", type="call", quality="excellent", notes="Talked for 2 hours"),
        InteractionLog(date="2024-03-08", type="date", quality="excellent", notes="Coffee date went great"),
        InteractionLog(date="2024-03-12", type="date", quality="excellent", notes="Hiking date was fun"),
    ]

    assessment = await matchmaker.assess_relationship(person1, person2, interactions)

    # Assertions
    assert assessment.total_interactions == 5, "Should count all interactions"
    assert assessment.relationship_health >= 0 and assessment.relationship_health <= 100, "Health score out of range"
    assert assessment.relationship_stage in ["initial-contact", "getting-to-know", "dating", "committed", "serious"], "Invalid stage"
    assert len(assessment.positive_indicators) > 0, "Should have positive indicators"
    assert len(assessment.next_steps) > 0, "Should have next steps"

    print(f"  ✓ Total Interactions: {assessment.total_interactions}")
    print(f"  ✓ Relationship Health: {assessment.relationship_health}/100")
    print(f"  ✓ Stage: {assessment.relationship_stage}")
    print(f"  ✓ Success Likelihood: {assessment.success_likelihood}")
    return True


async def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("MATCHMAKER TEST SUITE")
    print("=" * 60)
    print()

    tests = [
        ("Profile Analysis", test_profile_analysis),
        ("Compatibility Matching", test_compatibility_matching),
        ("Icebreaker Generation", test_icebreaker_generation),
        ("Relationship Assessment", test_relationship_assessment),
    ]

    results = []
    for name, test_func in tests:
        try:
            result = await test_func()
            results.append((name, True, None))
            print(f"✅ Test Passed: {name}")
        except AssertionError as e:
            results.append((name, False, str(e)))
            print(f"❌ Test Failed: {name}")
            print(f"   Error: {e}")
        except Exception as e:
            results.append((name, False, str(e)))
            print(f"❌ Test Error: {name}")
            print(f"   Error: {e}")
        print()

    # Summary
    print("=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    passed = sum(1 for _, success, _ in results if success)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    print()

    for name, success, error in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {name}")
        if error:
            print(f"  Error: {error}")

    print()
    if passed == total:
        print("🎉 All tests passed! Matchmaker system is ready to use.")
    else:
        print(f"⚠️  {total - passed} test(s) failed. Please review.")

    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(run_all_tests())
