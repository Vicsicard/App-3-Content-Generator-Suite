"""Social media writer agent for App 3."""

from content_generator.agents.base_agent import ContentAgent
from pathlib import Path
from typing import Dict, List
from ..database.content_manager import content_manager


class SocialMediaWriter(ContentAgent):
    """Generates social media content from transcript and style profile."""
    
    def __init__(self, input_dir: str = 'input'):
        """Initialize social media writer."""
        super().__init__()
        self.input_dir = Path(input_dir)

    def generate(self, transcript: str = None, style_profile: str = None) -> Dict:
        """Generate social media content from transcript and style profile."""
        # Load input files
        if transcript is None:
            transcript_path = self.input_dir / 'transcript_chunks.md'
            transcript = transcript_path.read_text() if transcript_path.exists() else ""
        
        if style_profile is None:
            style_path = self.input_dir / 'style-profile.md'
            style_profile = style_path.read_text() if style_path.exists() else ""

        # Generate social media content
        social_content = self._generate_social_content(transcript, style_profile)

        # Save directly to Supabase
        return content_manager.save_content(
            name='social_posts',
            content=social_content,
            type='carousel',  # This is a carousel-style post set
            platform='linkedin'  # Default to LinkedIn
        )

    def _generate_social_content(self, transcript: str, style: str) -> str:
        """Generate social media content from inputs.

        Args:
            transcript: Content from transcript_chunks.md
            style: Content from style-profile.md

        Returns:
            Generated markdown content
        """
        # Extract content elements and style data
        content_elements = self._extract_content_elements(transcript)
        style_data = self._parse_style_profile(style)

        # Generate platform-specific content
        linkedin = self._generate_linkedin_posts(content_elements, style_data)
        twitter = self._generate_twitter_posts(content_elements, style_data)
        instagram = self._generate_instagram_posts(content_elements, style_data)

        # Combine all content
        content = [
            "# Social Media Content Kit\n",
            "## LinkedIn Posts\n",
            linkedin,
            "\n## Twitter Posts\n",
            twitter,
            "\n## Instagram Posts\n",
            instagram
        ]

        return "\n".join(content)

    def _extract_content_elements(self, transcript: str) -> Dict[str, List[str]]:
        """Extract content elements from transcript."""
        elements = {
            'quotes': [],
            'insights': [],
            'themes': []
        }

        # Parse transcript chunks
        chunks = transcript.split('## [Chunk')
        for chunk in chunks[1:]:
            if '> Speaker 2:' in chunk:
                quote = chunk.split('> Speaker 2:')[1].split('\n')[0].strip()
                elements['quotes'].append(quote)

                # Extract insights
                if any(word in quote.lower() for word in ['realized', 'learned', 'discovered', 'found']):
                    elements['insights'].append(quote)

                # Extract themes
                if 'impact' in quote.lower():
                    elements['themes'].append('impact')
                if 'authentic' in quote.lower():
                    elements['themes'].append('authenticity')
                if 'perspective' in quote.lower():
                    elements['themes'].append('perspective')

        return elements

    def _parse_style_profile(self, style: str) -> Dict[str, List[str]]:
        """Parse style profile into structured data."""
        style_data = {
            'voice': [],
            'themes': []
        }

        current_section = None
        for line in style.split('\n'):
            if line.startswith('## voice:'):
                current_section = 'voice'
            elif line.startswith('## themes:'):
                current_section = 'themes'
            elif line.startswith('- ') and current_section:
                style_data[current_section].append(line[2:].strip())

        return style_data

    def _generate_linkedin_posts(self, content: Dict[str, List[str]], style: Dict[str, List[str]]) -> str:
        """Generate LinkedIn posts."""
        posts = []

        # Post 1: Insight-driven
        if content['insights']:
            insight = content['insights'][0]
            posts.append(
                "🌟 The Power of Authenticity\n\n"
                f"{insight}\n\n"
                "This realization transformed my approach to leadership and impact. "
                "When we embrace our unique perspectives, we don't just grow - "
                "we inspire others to do the same.\n\n"
                "#AuthenticLeadership #PersonalGrowth #ProfessionalDevelopment"
            )

        # Post 2: Quote-driven
        if content['quotes']:
            quote = content['quotes'][0]
            posts.append(
                "💫 Your Journey to Impact\n\n"
                f"\"{quote}\"\n\n"
                "Every transformative journey begins with a single step: "
                "choosing to be authentically you.\n\n"
                "What's your story of embracing authenticity?\n\n"
                "#Leadership #PersonalDevelopment #AuthenticSelf"
            )

        return "\n\n---\n\n".join(posts)

    def _generate_twitter_posts(self, content: Dict[str, List[str]], style: Dict[str, List[str]]) -> str:
        """Generate Twitter posts."""
        posts = []

        # Post 1: Key insight
        if content['insights']:
            posts.append(
                "✨ " + content['insights'][0] + "\n\n"
                "#AuthenticLeadership"
            )

        # Post 2: Engagement question
        posts.append(
            "💭 Question for you:\n\n"
            "What's the one thing you wish you'd known earlier about being authentic "
            "in your professional journey?\n\n"
            "#CareerGrowth #Authenticity"
        )

        return "\n\n---\n\n".join(posts)

    def _generate_instagram_posts(self, content: Dict[str, List[str]], style: Dict[str, List[str]]) -> str:
        """Generate Instagram posts."""
        posts = []

        # Post 1: Quote with image suggestion
        if content['quotes']:
            posts.append(
                "📸 Image: Professional headshot with quote overlay\n\n"
                f"\"{content['quotes'][0]}\"\n\n"
                "Your journey to authenticity is unique. Embrace it.\n\n"
                ".\n"
                ".\n"
                ".\n"
                "#AuthenticLeadership #PersonalGrowth #ProfessionalDevelopment "
                "#Leadership #CareerCoaching #PersonalBranding #Success #Growth"
            )

        return "\n\n---\n\n".join(posts)
