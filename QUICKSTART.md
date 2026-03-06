# Quick Start Guide - Matchmaker

Get started with Matchmaker in 5 minutes!

## Installation

```bash
# Clone or download the project
cd openclaw-match-maker

# Install dependencies
pip install -e .

# Or just install requirements
pip install -r requirements.txt
```

## 1. Create a Person Profile

```python
from matchmaker import Person, PersonalityTraits, Lifestyle, Values, Interests

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
        neuroticism=40
    ),
    lifestyle=Lifestyle(
        sleep_schedule="night-owl",
        exercise_frequency="weekly",
        social_activity="moderately-social",
        work_life_balance="balanced",
        travel_frequency="occasional",
        pets="has-dogs",
        smoking="never",
        drinking="social"
    ),
    values=Values(
        marriage_view="open",
        children_plan="want",
        family_importance=80,
        career_importance=70,
        communication_style="diplomatic"
    ),
    interests=Interests(
        categories=["tech", "travel", "music"],
        specific_hobbies=["photography", "hiking"],
        favorite_activities=["coffee date", "museum visit"]
    )
)
```

## 2. Analyze Profile

```python
import asyncio
from matchmaker import Matchmaker

async def analyze():
    matchmaker = Matchmaker()
    profile = await matchmaker.analyze_profile(alex)

    print(f"Dating Readiness: {profile.dating_readiness}")
    print(f"Overall Score: {profile.overall_score}/100")
    print("\nStrengths:")
    for strength in profile.strengths:
        print(f"  • {strength}")

asyncio.run(analyze())
```

## 3. Run Complete Example

```bash
# Run the complete demo
python3 examples/basic_example.py

# Run tests
python3 test_complete.py
```

---

Happy matching! 💕
