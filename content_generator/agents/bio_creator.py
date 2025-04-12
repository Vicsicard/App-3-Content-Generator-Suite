"""
Bio Creator Agent

Creates professional biographies from narrative transcripts.
"""

from typing import Dict, List, Any
from pathlib import Path
from .base_agent import ContentAgent
from content_generator.utils.content_writer import format_markdown_section


class BioCreatorAgent(ContentAgent):
    """Bio creator agent that creates professional biographies."""
    
    def generate(self) -> str:
        """Generate biography content using transcript and style profile."""
        # Extract bio elements and style data
        bio_elements = self._extract_bio_elements()
        style_data = self._parse_style_profile()
        
        # Generate bio sections
        intro = self._generate_intro(bio_elements, style_data)
        expertise = self._generate_expertise(bio_elements, style_data)
        achievements = self._generate_achievements(bio_elements, style_data)
        
        # Combine all sections
        biography = [
            "# Professional Biography\n",
            intro,
            expertise,
            achievements
        ]
        
        return "\n".join(biography)
        
    def _extract_bio_elements(self) -> Dict[str, List[str]]:
        """Extract biographical elements from transcript."""
        elements = {
            'intro': [],
            'expertise': [],
            'achievements': []
        }
        current_section = None
        current_text = []
        
        for line in self.transcript.split('\n'):
            if line.startswith('Speaker 2:'):
                if current_text:
                    text = ' '.join(current_text)
                    if any(word in text.lower() for word in ['background', 'started', 'began']):
                        elements['intro'].append(text)
                    elif any(word in text.lower() for word in ['expert', 'specialize', 'focus']):
                        elements['expertise'].append(text)
                    elif any(word in text.lower() for word in ['achieve', 'accomplish', 'success']):
                        elements['achievements'].append(text)
                    current_text = []
                current_text.append(line.replace('Speaker 2:', '').strip())
            elif current_text:
                current_text.append(line.strip())
                
        # Process final section
        if current_text:
            text = ' '.join(current_text)
            if any(word in text.lower() for word in ['background', 'started', 'began']):
                elements['intro'].append(text)
            elif any(word in text.lower() for word in ['expert', 'specialize', 'focus']):
                elements['expertise'].append(text)
            elif any(word in text.lower() for word in ['achieve', 'accomplish', 'success']):
                elements['achievements'].append(text)
                
        return elements
        
    def _parse_style_profile(self) -> Dict[str, List[str]]:
        """Parse style profile into structured data."""
        style_data = {
            'themes': [],
            'values': [],
            'tone': []
        }
        current_section = None
        
        for line in self.style_profile.split('\n'):
            if line.startswith('## '):
                current_section = line[3:].lower().strip(':')
            elif line.startswith('- ') and current_section in style_data:
                style_data[current_section].append(line[2:])
                
        return style_data
        
    def _generate_intro(self, bio: Dict[str, List[str]], style: Dict[str, List[str]]) -> str:
        """Generate biography introduction."""
        theme = style['themes'][0] if style['themes'] else 'professional excellence'
        intro_text = bio['intro'][0] if bio['intro'] else f"A dedicated professional focused on {theme}"
        
        intro = [
            "## Professional Overview\n",
            intro_text + "\n"
        ]
        return "\n".join(intro)
        
    def _generate_expertise(self, bio: Dict[str, List[str]], style: Dict[str, List[str]]) -> str:
        """Generate expertise section."""
        expertise_items = bio['expertise'][:3] if bio['expertise'] else [f"Expertise in {theme}" for theme in style['themes'][:3]]
        
        expertise = [
            "\n## Areas of Expertise\n"
        ]
        
        for item in expertise_items:
            expertise.append(f"- {item}\n")
            
        return "\n".join(expertise)
        
    def _generate_achievements(self, bio: Dict[str, List[str]], style: Dict[str, List[str]]) -> str:
        """Generate achievements section."""
        achievements = bio['achievements'][:3] if bio['achievements'] else []
        values = style['values'][:3] if style['values'] else []
        
        achievement_section = [
            "\n## Key Achievements\n"
        ]
        
        # Add achievements with value alignment
        for achievement, value in zip(achievements, values):
            achievement_section.extend([
                f"### {value}\n" if value else "### Achievement",
                f"{achievement}\n" if achievement else "Demonstrated excellence in professional endeavors.\n"
            ])
            
        return "\n".join(achievement_section)
