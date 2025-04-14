"""Website writer agent for App 3."""

from pathlib import Path
from typing import Dict, List
from ..database.content_manager import content_manager
from content_generator.agents.base_agent import ContentAgent


class WebsiteWriter(ContentAgent):
    """Generates website content from transcript and style profile."""
    
    def __init__(self, input_dir: str = 'input'):
        """Initialize website writer.

        Args:
            input_dir: Directory containing input files
        """
        super().__init__()
        self.input_dir = Path(input_dir)

    def generate(self, transcript: str = None, style_profile: str = None) -> Dict:
        """Generate website content and save to Supabase.

        Returns:
            Dict containing the saved content record
        """
        # Load input files
        if transcript is None or style_profile is None:
            transcript_path = self.input_dir / 'transcript_chunks.md'
            style_path = self.input_dir / 'style-profile.md'

            transcript = transcript_path.read_text() if transcript_path.exists() else ""
            style_profile = style_path.read_text() if style_path.exists() else ""

        # Generate website content
        website_content = self._generate_website_content(transcript, style_profile)

        # Save directly to Supabase
        return content_manager.save_content(
            name='website_home',
            content=website_content
        )

    def _generate_website_content(self, transcript: str, style_profile: str) -> str:
        """Generate website content from inputs.

        Args:
            transcript: Content from transcript_chunks.md
            style_profile: Content from style-profile.md

        Returns:
            Generated markdown content
        """
        # Extract core content elements from transcript
        elements = {
            'expertise': [],
            'journey': [],
            'insights': []
        }

        # Parse transcript chunks for key elements
        chunks = transcript.split('## [Chunk')
        for chunk in chunks[1:]:
            if '> Speaker 2:' in chunk:
                quote = chunk.split('> Speaker 2:')[1].split('\n')[0].strip()

                # Extract journey moments
                if any(word in quote.lower() for word in ['started', 'began', 'realized', 'learned']):
                    elements['journey'].append(quote)

                # Extract insights
                if any(word in quote.lower() for word in ['discovered', 'found', 'understand']):
                    elements['insights'].append(quote)

                # Extract expertise
                if any(word in quote.lower() for word in ['expert', 'specialize', 'focus']):
                    elements['expertise'].append(quote)

        # Parse style profile for voice and themes
        style_data = {
            'voice': [],
            'themes': []
        }

        current_section = None
        for line in style_profile.split('\n'):
            if line.startswith('## '):
                current_section = line[3:].lower().strip(':')
            elif line.startswith('- ') and current_section in style_data:
                style_data[current_section].append(line[2:].strip())

        # Generate website sections
        sections = []

        # Generate home hero section
        expertise = elements['expertise'][0] if elements['expertise'] else ""
        hero = [
            "# [CLIENT_NAME]",
            expertise if expertise else "[PROFESSIONAL_TITLE]",
            "",
            "[CONTACT_LINK]"
        ]
        sections.append("\n".join(hero))

        # Generate about section
        if elements['expertise']:
            about = [
                "## About",
                elements['expertise'][0]
            ]
            sections.append("\n".join(about))

        # Generate story section
        if elements['journey']:
            story = ["## Journey"]
            for moment in elements['journey'][:3]:
                story.append(f"\n{moment}")
            sections.append("\n".join(story))

        # Generate blog highlights section
        if elements['insights']:
            blog = ["## Writing"]
            for i, insight in enumerate(elements['insights'][:2], 1):
                blog.extend([
                    f"\n### {insight.split('.')[0]}",
                    f"[blog-{i}]"
                ])
            sections.append("\n".join(blog))

        # Generate video section
        video = [
            "## Videos",
            "[video-1]",
            "[video-2]",
            "[video-3]"
        ]
        sections.append("\n".join(video))

        # Generate contact section
        contact = [
            "## Contact",
            "[contact-form]",
            "[email]"
        ]
        sections.append("\n".join(contact))

        # Join sections with markdown separator
        return "\n\n---\n\n".join(sections)
