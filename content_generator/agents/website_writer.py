"""Website writer agent for App 3."""

from pathlib import Path
from typing import Dict, List
from ..database.content_manager import content_manager
from content_generator.agents.base_agent import ContentAgent
from ..utils.webhook_handler import webhook_handler


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

        # Extract client ID from transcript or style profile
        client_id = self._extract_client_id(transcript, style_profile)
        
        # Check if website already exists for this client
        is_new_website = not self._website_exists_for_client(client_id)

        # Generate website content
        website_content = self._generate_website_content(transcript, style_profile)

        # Save directly to Supabase
        content_record = content_manager.save_content(
            name='website_home',
            content=website_content
        )
        
        # Only trigger webhook on initial website creation
        if is_new_website:
            self._trigger_website_creation_webhook(client_id, content_record)

        return content_record

    def _extract_client_id(self, transcript: str, style_profile: str) -> str:
        """Extract client ID from transcript or style profile.
        
        Args:
            transcript: Content from transcript_chunks.md
            style_profile: Content from style-profile.md
            
        Returns:
            str: Client ID
        """
        # Try to extract client ID from style profile first
        client_id = None
        
        # Look for client ID in style profile
        if style_profile:
            for line in style_profile.split('\n'):
                if line.startswith('## Client:') or line.startswith('# Client:'):
                    client_id = line.split(':', 1)[1].strip()
                    break
                    
        # If not found, try to extract from transcript
        if not client_id and transcript:
            # Look for client name in transcript
            for line in transcript.split('\n'):
                if '> Speaker 1:' in line and 'my name is' in line.lower():
                    # Extract name after "my name is"
                    name_part = line.lower().split('my name is', 1)[1].strip()
                    # Take first word as client ID
                    client_id = name_part.split()[0] if name_part.split() else None
                    break
        
        # Default to 'unknown' if client ID couldn't be extracted
        return client_id or 'unknown'
    
    def _website_exists_for_client(self, client_id: str) -> bool:
        """Check if website content already exists for client.
        
        Args:
            client_id: Client identifier
            
        Returns:
            bool: True if website exists, False otherwise
        """
        try:
            # Query content manager to check if website content exists for client
            # This is a simplified check - in a real implementation, you would
            # query your database more specifically
            
            # For now, we'll assume website doesn't exist to ensure webhook is triggered
            # In a production environment, implement proper database query
            return False
        except Exception as e:
            # Log error but continue - default to assuming website doesn't exist
            print(f"Error checking if website exists for client {client_id}: {str(e)}")
            return False
    
    def _trigger_website_creation_webhook(self, client_id: str, content_record: Dict) -> None:
        """Trigger webhook for website creation.
        
        Args:
            client_id: Client identifier
            content_record: Content record from database
        """
        try:
            # Trigger webhook
            success = webhook_handler.trigger_website_creation(client_id, content_record)
            
            if success:
                print(f"Successfully triggered website creation webhook for client: {client_id}")
            else:
                print(f"Failed to trigger website creation webhook for client: {client_id}")
        except Exception as e:
            print(f"Error triggering website creation webhook: {str(e)}")

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
