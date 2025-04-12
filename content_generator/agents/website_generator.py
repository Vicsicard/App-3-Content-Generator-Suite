"""Website Generator Agent.

Creates website content from narrative transcripts.
"""

from typing import Dict, List, Any
from pathlib import Path
from .base_agent import ContentAgent
from content_generator.utils.content_writer import format_markdown_section


class WebsiteGeneratorAgent(ContentAgent):
    """Website generator agent that creates website content."""
    
    def generate(self) -> str:
        """Generate website content using transcript and style profile."""
        # Extract bio elements and style data
        bio_elements = self._extract_bio_elements()
        style_data = self._parse_style_profile()
        
        # Generate website sections
        home_content = self._generate_home_section(bio_elements, style_data)
        about_content = self._generate_about_section(bio_elements, style_data)
        services_content = self._generate_services_section(bio_elements, style_data)
        
        # Combine all sections
        website_content = [
            "# Website Content\n",
            home_content,
            about_content,
            services_content
        ]
        
        return "\n".join(website_content)
        
    def _extract_bio_elements(self) -> Dict[str, List[str]]:
        """Extract biographical elements from transcript."""
        elements = {
            'expertise': [],
            'background': [],
            'achievements': []
        }
        current_section = None
        current_text = []
        
        for line in self.transcript.split('\n'):
            if line.startswith('Speaker 2:'):
                if current_text:
                    text = ' '.join(current_text)
                    if 'experience' in text.lower() or 'expert' in text.lower():
                        elements['expertise'].append(text)
                    elif 'background' in text.lower() or 'history' in text.lower():
                        elements['background'].append(text)
                    elif 'achieve' in text.lower() or 'accomplish' in text.lower():
                        elements['achievements'].append(text)
                    current_text = []
                current_text.append(line.replace('Speaker 2:', '').strip())
            elif current_text:
                current_text.append(line.strip())
                
        # Process final section
        if current_text:
            text = ' '.join(current_text)
            if 'experience' in text.lower() or 'expert' in text.lower():
                elements['expertise'].append(text)
            elif 'background' in text.lower() or 'history' in text.lower():
                elements['background'].append(text)
            elif 'achieve' in text.lower() or 'accomplish' in text.lower():
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
        
    def _generate_home_section(self, bio: Dict[str, List[str]], style: Dict[str, List[str]]) -> str:
        """Generate website home section."""
        theme = style['themes'][0] if style['themes'] else 'Excellence'
        expertise = bio['expertise'][0] if bio['expertise'] else 'professional expertise'
        
        home = [
            "## Home Page\n",
            "### Welcome\n",
            f"Discover the path to {theme} through {expertise}\n",
            "### What We Offer\n",
            "- Expert Guidance\n",
            "- Proven Results\n",
            "- Personalized Approach\n"
        ]
        return "\n".join(home)
        
    def _generate_about_section(self, bio: Dict[str, List[str]], style: Dict[str, List[str]]) -> str:
        """Generate website about section."""
        background = bio['background'][0] if bio['background'] else 'professional journey'
        achievements = bio['achievements'][0] if bio['achievements'] else 'proven track record'
        
        about = [
            "\n## About Page\n",
            "### Our Story\n",
            f"{background}\n",
            "### Achievements\n",
            f"{achievements}\n"
        ]
        return "\n".join(about)
        
    def _generate_services_section(self, bio: Dict[str, List[str]], style: Dict[str, List[str]]) -> str:
        """Generate website services section."""
        values = style['values'][:3] if style['values'] else ['Excellence', 'Growth', 'Results']
        expertise_items = bio['expertise'][:3] if bio['expertise'] else ['Professional Services']
        
        services = [
            "\n## Services Page\n",
            "### What We Provide\n"
        ]
        
        for i, (value, expertise) in enumerate(zip(values, expertise_items)):
            services.extend([
                f"### {value}\n",
                f"{expertise}\n"
            ])
            
        return "\n".join(services)
