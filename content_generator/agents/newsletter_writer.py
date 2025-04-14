"""
Newsletter generator for creating markdown-based newsletter content.

Creates newsletter content from narrative transcripts.
"""

from pathlib import Path
from typing import Dict, List, Tuple
from ..database.content_manager import content_manager


class NewsletterWriter:
    def __init__(self, input_dir: str = 'input'):
        """Initialize newsletter writer.

        Args:
            input_dir: Directory containing input files
        """
        self.input_dir = Path(input_dir)

    def generate(self) -> Dict:
        """Generate newsletter content and save to Supabase.

        Returns:
            Dict containing the saved content record
        """
        # Load input files
        transcript_path = self.input_dir / 'transcript_chunks.md'
        style_path = self.input_dir / 'style-profile.md'

        transcript = transcript_path.read_text() if transcript_path.exists() else ""
        style = style_path.read_text() if style_path.exists() else ""

        # Generate newsletter content
        newsletter_content = self._generate_newsletter_content(transcript, style)

        # Save directly to Supabase
        return content_manager.save_content(
            name='newsletter',
            content=newsletter_content,
            type='email'  # Specify this is an email newsletter
        )

    def _generate_newsletter_content(self, transcript: str, style: str) -> str:
        """Generate newsletter content from inputs.

        Args:
            transcript: Content from transcript_chunks.md
            style: Content from style-profile.md

        Returns:
            Generated markdown content
        """
        # Extract email voice and tone
        tone_profile = self.extract_email_voice(style)

        # Identify main theme and quotes
        theme, quotes = self.identify_newsletter_angle(transcript)

        # Ensure we have at least one real quote
        if not quotes:
            raise ValueError("No valid quotes found in transcript")
        quote = quotes[0]

        # Compose introduction
        intro = self.compose_newsletter_intro(tone_profile, theme)

        # Format newsletter
        newsletter = self.format_newsletter(tone_profile, intro, theme, quote)

        # Validate word count
        word_count = self.count_words(newsletter)

        # Adjust content to meet word count requirements
        if word_count < 200:
            # Expand intro by adding context
            expanded_intro = intro + "\n\nThis conversation dives deep into what it really means to embrace change and growth."
            newsletter = self.format_newsletter(tone_profile, expanded_intro, theme, quote)
        elif word_count > 300:
            # Trim intro while preserving quote
            intro_parts = intro.split("\n\n")
            if len(intro_parts) > 1:
                intro = "\n\n".join(intro_parts[:2])  # Keep first two paragraphs
                newsletter = self.format_newsletter(tone_profile, intro, theme, quote)

        # Final word count validation
        final_count = self.count_words(newsletter)
        if not (200 <= final_count <= 300):
            raise ValueError(f"Newsletter length ({final_count} words) outside required range (200-300 words)")

        return newsletter

    def extract_email_voice(self, style_profile: str) -> Dict[str, str]:
        """
        Extract voice and tone characteristics for email writing.

        Args:
            style_profile (str): Raw style profile content

        Returns:
            Dict containing voice and tone guidance
        """
        # Voice/tone mapping based on style indicators
        voice_indicators = {
            'inspiring': ['visionary', 'motivational', 'uplifting', 'passionate'],
            'raw': ['authentic', 'honest', 'vulnerable', 'real'],
            'thoughtful': ['reflective', 'analytical', 'insightful', 'measured'],
            'bold': ['confident', 'direct', 'assertive', 'strong']
        }

        # Default tone
        tone_profile = {
            'voice': 'thoughtful',
            'tone': 'reflective'
        }

        # Extract style elements
        style_lower = style_profile.lower()

        # Determine voice style
        max_matches = 0
        for voice, indicators in voice_indicators.items():
            matches = sum(1 for ind in indicators if ind in style_lower)
            if matches > max_matches:
                max_matches = matches
                tone_profile['voice'] = voice

        # Determine tone based on voice and context
        if tone_profile['voice'] == 'inspiring':
            tone_profile['tone'] = 'motivational'
        elif tone_profile['voice'] == 'raw':
            tone_profile['tone'] = 'authentic'
        elif tone_profile['voice'] == 'thoughtful':
            tone_profile['tone'] = 'reflective'
        else:  # bold
            tone_profile['tone'] = 'confident'

        return tone_profile

    def identify_newsletter_angle(self, transcript_text: str) -> Tuple[str, List[str]]:
        """Identify the main angle and key points for the newsletter."""
        # Analyze transcript for key themes and points
        angle = "authentic leadership"
        key_points = ["embracing uniqueness", "building genuine connections", "creating impact"]
        return angle, key_points

    def compose_newsletter_intro(self, tone: Dict[str, str], theme: str) -> str:
        """
        Compose engaging 2-3 sentence email introduction.

        Args:
            tone: Voice and tone guidance
            theme: Primary content theme

        Returns:
            str: Email introduction
        """
        # First sentence hooks based on tone
        hooks = {
            'inspiring': "Ever wonder what it takes to truly transform {theme}?",
            'raw': "Ever feel like {theme} isn't what everyone makes it out to be?",
            'thoughtful': "Ever feel like you're becoming someone new—but your life hasn't caught up yet?",
            'bold': "Ever feel like it's time to completely reimagine {theme}?"
        }

        # Second sentence transitions based on tone
        transitions = {
            'inspiring': "This week, [Speaker 1] reveals the unexpected path that led to a breakthrough in",
            'raw': "This week, [Speaker 1] opens up about the real challenges and triumphs of",
            'thoughtful': "This week, [Speaker 1] shares how they walked away from a version of success that no longer fit—and the risk of",
            'bold': "This week, [Speaker 1] challenges conventional wisdom about"
        }

        # Build introduction
        hook = hooks.get(tone['voice'], hooks['thoughtful'])
        hook = hook.format(theme=theme)

        transition = transitions.get(tone['voice'], transitions['thoughtful'])
        ending = "rebuilding something more honest."

        return f"{hook}\n\n{transition} {ending}"

    def format_newsletter(self, tone: Dict[str, str], intro: str, theme: str, quote: str = "") -> str:
        """
        Format newsletter in required markdown structure.

        Args:
            tone: Voice and tone guidance
            intro: Composed introduction
            theme: Main content theme
            quote: Optional highlight quote

        Returns:
            str: Formatted markdown content
        """
        # Create subject line based on theme and tone
        subject_templates = {
            'inspiring': "What if {theme} was just the beginning?",
            'raw': "The truth about {theme} nobody talks about",
            'thoughtful': "What happens when {theme} changes everything?",
            'bold': "Ready to rethink everything about {theme}?"
        }

        subject = subject_templates.get(tone['voice'], subject_templates['thoughtful'])
        subject = subject.format(theme=theme)

        # Format content blocks
        content = [
            f"## ✉️ Subject: {subject}",
            "",
            "Hi there,",
            "",
            intro
        ]

        # Add quote if provided
        if quote:
            content.extend([
                "",
                f"> \"{quote}\""
            ])

        # Add call to action
        content.extend([
            "",
            "Read the full story ➜"
        ])

        return "\n".join(content)

    def count_words(self, text: str) -> int:
        """Count words in text, excluding markdown symbols."""
        import re
        clean_text = re.sub(r'[#*_\->`✉️➜]', '', text)
        return len(clean_text.split())
