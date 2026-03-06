"""IcebreakerGenerator - Creates personalized conversation starters and date ideas."""

from typing import List, Dict
from matchmaker.types.person import Person
from matchmaker.types.models import IcebreakerSuggestion


class IcebreakerGenerator:
    """Generates personalized icebreakers and conversation suggestions based on two people's profiles."""

    async def generate_icebreakers(self, person: Person, match: Person) -> IcebreakerSuggestion:
        """
        Generate personalized icebreakers for initiating conversation with a match.

        Args:
            person: The person who will initiate
            match: The person they want to talk to

        Returns:
            Complete icebreaker suggestions with opening lines, topics, and date ideas
        """
        # Generate opening lines
        opening_lines = self._generate_opening_lines(person, match)

        # Find conversation topics
        shared_interests = self._find_shared_interests(person, match)
        unique_starters = self._generate_unique_starters(person, match)
        questions = self._generate_questions(match)

        # Date planning
        date_ideas = self._generate_date_ideas(person, match)

        # What to avoid
        topics_to_avoid = self._identify_avoidance_topics(match)
        pitfalls = self._identify_communication_pitfalls(match)

        # Tips
        personality_tips = self._generate_personality_tips(match)
        style_advice = self._generate_style_advice(person, match)

        return IcebreakerSuggestion(
            opening_lines=opening_lines,
            shared_interests=shared_interests,
            unique_conversation_starters=unique_starters,
            questions_to_ask=questions,
            date_ideas=date_ideas,
            topics_to_avoid=topics_to_avoid,
            conversation_pitfalls=pitfalls,
            personality_tips=personality_tips,
            style_advice=style_advice,
        )

    def _generate_opening_lines(self, person: Person, match: Person) -> List[str]:
        """Generate personalized opening lines."""
        lines = []

        # Find common ground
        common_interests = set(person.interests.categories) & set(match.interests.categories)
        common_hobbies = set(person.interests.specific_hobbies) & set(match.interests.specific_hobbies)

        # Interest-based openers
        if common_hobbies:
            hobby = list(common_hobbies)[0]
            lines.append(f"Hey! I noticed you're into {hobby}. I'm actually working on [related project/activity] - would love to hear your thoughts on it!")

        if "travel" in common_interests:
            lines.append(f"Hi {match.name}! Saw you enjoy travel. What's been your favorite destination so far? I'm always looking for recommendations!")

        if "music" in common_interests:
            lines.append(f"Hey! Fellow music lover here. What have you been listening to lately? Always on the hunt for new artists to discover.")

        if "cooking" in common_interests or "cooking" in match.interests.specific_hobbies:
            lines.append(f"Hi! I see you're into cooking. Do you have a signature dish? I'm always trying to expand my repertoire.")

        # Personality-based openers
        if match.personality.extraversion >= 70:
            lines.append(f"Hi {match.name}! Your profile caught my eye - you seem like someone with great energy. What's something fun you've done recently?")
        elif match.personality.extraversion <= 40:
            lines.append(f"Hey {match.name}, your profile resonates with me. I'd love to hear about what you're passionate about - I find meaningful conversations so much better than small talk.")

        # Bio-based (if available)
        if match.bio and len(match.bio) > 20:
            lines.append(f"Hi! I really enjoyed reading your profile - especially [reference something specific from bio]. Tell me more about that?")

        # Generic but warm
        lines.append(f"Hey {match.name}! I think we have some really interesting things in common. How's your week going?")

        return lines[:5]

    def _find_shared_interests(self, person: Person, match: Person) -> List[str]:
        """Identify shared interests for conversation topics."""
        shared = []

        common_categories = set(person.interests.categories) & set(match.interests.categories)
        for cat in common_categories:
            shared.append(f"{cat.capitalize()} - explore specific aspects you both enjoy")

        common_hobbies = set(person.interests.specific_hobbies) & set(match.interests.specific_hobbies)
        for hobby in common_hobbies:
            shared.append(f"{hobby.capitalize()} - share experiences and tips")

        common_activities = set(person.interests.favorite_activities) & set(match.interests.favorite_activities)
        for activity in common_activities:
            shared.append(f"{activity.capitalize()} - plan to do this together")

        return shared[:6] if shared else ["Explore each other's unique interests to learn something new"]

    def _generate_unique_starters(self, person: Person, match: Person) -> List[str]:
        """Generate conversation starters based on match's unique traits."""
        starters = []

        # Based on match's unique interests not shared by person
        unique_interests = set(match.interests.categories) - set(person.interests.categories)
        if unique_interests:
            interest = list(unique_interests)[0]
            starters.append(f"I see you're into {interest} - I don't know much about it but would love to learn! What got you started?")

        # Based on occupation
        if match.occupation:
            starters.append(f"What's it like working in {match.occupation}? I'm curious about [specific aspect]")

        # Based on location
        if match.location:
            starters.append(f"You're in {match.location} - what do you love most about living there?")

        # Based on values
        if match.values.family_importance >= 70:
            starters.append("Family seems important to you - tell me about your family! Any fun traditions?")

        # Based on lifestyle
        if match.lifestyle.travel_frequency in ["frequent", "occasional"]:
            starters.append("What's on your travel bucket list? I'm always dreaming about my next adventure!")

        return starters[:5]

    def _generate_questions(self, match: Person) -> List[str]:
        """Generate good questions to ask the match."""
        questions = []

        # Personality-based questions
        if match.personality.openness >= 70:
            questions.append("What's something new you've tried recently that you really enjoyed?")
            questions.append("If you could learn any skill instantly, what would it be?")

        # Interest-based questions
        if "reading" in match.interests.categories:
            questions.append("What's the best book you've read recently? I'm always looking for recommendations!")

        if "sports" in match.interests.categories or match.lifestyle.exercise_frequency in ["daily", "weekly"]:
            questions.append("How do you like to stay active? Any sports or activities you're passionate about?")

        # Values-based questions
        if match.values.family_importance >= 70:
            questions.append("What do you value most in relationships and friendships?")

        # Lifestyle questions
        questions.append("What does a perfect weekend look like for you?")
        questions.append("What are you most looking forward to in the next few months?")

        # Deeper questions (for after initial rapport)
        questions.append("What's something most people don't know about you?")
        questions.append("What matters most to you in life right now?")

        return questions[:8]

    def _generate_date_ideas(self, person: Person, match: Person) -> List[Dict[str, str]]:
        """Generate personalized date ideas with reasoning."""
        ideas = []

        common_interests = set(person.interests.categories) & set(match.interests.categories)

        # Based on shared interests
        if "coffee" in ' '.join(person.interests.favorite_activities + match.interests.favorite_activities).lower():
            ideas.append({
                "activity": "Coffee at a cozy local cafe",
                "reason": "Low-pressure environment perfect for getting to know each other through conversation"
            })

        if "arts" in common_interests:
            ideas.append({
                "activity": "Visit an art museum or gallery opening",
                "reason": "Shared interest in arts provides natural conversation topics and reveals aesthetic preferences"
            })

        if "outdoor" in common_interests or "sports" in common_interests:
            ideas.append({
                "activity": "Scenic hike or walk in a beautiful park",
                "reason": "Active date allows conversation while enjoying nature - low pressure and healthy"
            })

        if "music" in common_interests:
            ideas.append({
                "activity": "Live music performance or concert",
                "reason": "Shared love of music creates excitement and provides conversation topics"
            })

        if "cooking" in common_interests:
            ideas.append({
                "activity": "Cooking class or food market exploration",
                "reason": "Interactive and fun - shows creativity and allows teamwork"
            })

        # Based on personality compatibility
        if match.personality.extraversion >= 60 and person.personality.extraversion >= 60:
            ideas.append({
                "activity": "Try a new restaurant or trendy bar",
                "reason": "Both enjoy social settings - vibrant atmosphere matches energy"
            })
        elif match.personality.extraversion <= 50 and person.personality.extraversion <= 50:
            ideas.append({
                "activity": "Quiet bookstore browse followed by coffee",
                "reason": "Both appreciate quieter settings - allows for intimate conversation"
            })

        # Universal good first dates
        if len(ideas) < 3:
            ideas.append({
                "activity": "Walk and talk in a scenic neighborhood",
                "reason": "Classic first date - allows flexible length and natural conversation flow"
            })

        return ideas[:6]

    def _identify_avoidance_topics(self, match: Person) -> List[str]:
        """Identify topics that might not resonate well initially."""
        avoid = []

        # Based on values
        if match.values.religion == "none" or not match.values.religion:
            avoid.append("Religion or spiritual topics (at least initially)")

        if match.values.political_view == "not-political":
            avoid.append("Political discussions - they prefer to avoid politics")

        # Based on lifestyle
        if match.lifestyle.work_life_balance == "life-first":
            avoid.append("Excessive work talk - they prioritize life outside work")

        # Based on personality
        if match.personality.extraversion <= 40:
            avoid.append("Overwhelming group hangout suggestions early on - they may prefer one-on-one")

        if match.personality.neuroticism >= 70:
            avoid.append("Heavy or intense topics too soon - build trust gradually")

        # General early dating
        avoid.append("Ex-relationship details (save for later when trust is built)")
        avoid.append("Controversial hot-button issues on first dates")

        return avoid[:5]

    def _identify_communication_pitfalls(self, match: Person) -> List[str]:
        """Identify communication styles to avoid."""
        pitfalls = []

        if match.values.communication_style == "direct":
            pitfalls.append("Being too vague or indirect - they appreciate honesty")

        elif match.values.communication_style == "diplomatic":
            pitfalls.append("Being overly blunt or harsh - they value tact and kindness")

        elif match.values.communication_style == "avoid-conflict":
            pitfalls.append("Being too confrontational early on - create safe space first")

        if match.personality.agreeableness >= 75:
            pitfalls.append("Taking advantage of their agreeableness - ask for their genuine preferences")

        if match.personality.neuroticism >= 65:
            pitfalls.append("Dismissing their feelings - validate emotions even if you disagree")

        # General pitfalls
        pitfalls.append("Dominating the conversation - ask questions and listen actively")
        pitfalls.append("Being on your phone - show you're present and interested")

        return pitfalls[:5]

    def _generate_personality_tips(self, match: Person) -> List[str]:
        """Generate tips based on match's personality."""
        tips = []

        p = match.personality

        if p.openness >= 70:
            tips.append("They're open to new experiences - suggest creative or unique date ideas")

        if p.conscientiousness >= 70:
            tips.append("They appreciate planning and reliability - follow through on what you say")

        if p.extraversion >= 70:
            tips.append("They're energized by social interaction - group activities can work well")
        elif p.extraversion <= 40:
            tips.append("They recharge through alone time - respect their need for space between dates")

        if p.agreeableness >= 75:
            tips.append("They're empathetic and cooperative - create collaborative date experiences")

        if p.neuroticism >= 60:
            tips.append("Emotional security matters - be consistent and reassuring in communication")
        else:
            tips.append("They're emotionally stable - appreciate their groundedness")

        return tips[:5]

    def _generate_style_advice(self, person: Person, match: Person) -> str:
        """Generate overall approach recommendation."""
        match_pers = match.personality

        if match_pers.extraversion >= 70:
            return "Be energetic and enthusiastic! They respond well to confidence and social warmth. Don't be afraid to suggest fun, social activities."

        elif match_pers.extraversion <= 40:
            return "Take a thoughtful, genuine approach. They value depth over breadth - focus on meaningful one-on-one conversation rather than flashy gestures."

        elif match_pers.openness >= 75:
            return "Be creative and show your unique side! They appreciate novelty and intellectual stimulation. Share your passions and be open to their ideas."

        elif match.values.communication_style == "direct":
            return "Be authentic and straightforward. They appreciate honesty and clarity. Say what you mean and ask directly for what you want."

        elif match.values.communication_style == "diplomatic":
            return "Balance warmth with respect. Be kind and considerate in how you phrase things. Show interest while being mindful of boundaries."

        else:
            return "Be yourself while staying attuned to their responses. Show genuine interest, ask thoughtful questions, and let the conversation flow naturally."
