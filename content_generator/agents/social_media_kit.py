"""Social Media Kit Agent.

Creates social media content from narrative transcripts.
"""

from typing import Dict, List, Any
from pathlib import Path
from .base_agent import ContentAgent
from content_generator.utils.content_writer import format_markdown_section


class SocialMediaKitAgent(ContentAgent):
    """Social media kit agent that creates social media content."""
    
    def generate(self) -> str:
        """Generate social media content using transcript and style profile."""
        # Extract content elements and style data
        content_elements = self._extract_content_elements()
        style_data = self._parse_style_profile()
        
        # Generate social media content
        linkedin = self._generate_linkedin_posts(content_elements, style_data)
        twitter = self._generate_twitter_posts(content_elements, style_data)
        instagram = self._generate_instagram_posts(content_elements, style_data)
        
        # Combine all content
        social_content = [
            "# Social Media Content Kit\n",
            linkedin,
            twitter,
            instagram
        ]
        
        return "\n".join(social_content)
        
    def _extract_content_elements(self) -> Dict[str, List[str]]:
        """Extract content elements from transcript."""
        elements = {
            'insights': [],
            'quotes': [],
            'topics': []
        }
        current_section = None
        current_text = []
        
        for line in self.transcript.split('\n'):
            if line.startswith('Speaker 2:'):
                if current_text:
                    text = ' '.join(current_text)
                    if '"' in text:
                        elements['quotes'].append(text)
                    elif any(word in text.lower() for word in ['key', 'important', 'critical']):
                        elements['insights'].append(text)
                    else:
                        elements['topics'].append(text)
                    current_text = []
                current_text.append(line.replace('Speaker 2:', '').strip())
            elif current_text:
                current_text.append(line.strip())
                
        # Process final section
        if current_text:
            text = ' '.join(current_text)
            if '"' in text:
                elements['quotes'].append(text)
            elif any(word in text.lower() for word in ['key', 'important', 'critical']):
                elements['insights'].append(text)
            else:
                elements['topics'].append(text)
                
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
        
    def _generate_linkedin_posts(self, content: Dict[str, List[str]], style: Dict[str, List[str]]) -> str:
        """Generate LinkedIn posts."""
        insights = content['insights'][:2] if content['insights'] else []
        themes = style['themes'][:2] if style['themes'] else []
        
        linkedin = [
            "## LinkedIn Posts\n"
        ]
        
        for i, (insight, theme) in enumerate(zip(insights, themes), 1):
            linkedin.extend([
                f"### Post {i}\n",
                f"🎯 {theme}\n" if theme else "🎯 Professional Insight\n",
                f"{insight}\n" if insight else "Sharing valuable insights from my professional journey.\n",
                "#ProfessionalDevelopment #Leadership #Growth\n"
            ])
            
        return "\n".join(linkedin)
        
    def _generate_twitter_posts(self, content: Dict[str, List[str]], style: Dict[str, List[str]]) -> str:
        """Generate Twitter posts."""
        quotes = content['quotes'][:3] if content['quotes'] else []
        
        twitter = [
            "\n## Twitter Posts\n"
        ]
        
        for i, quote in enumerate(quotes, 1):
            # Ensure tweet is under 280 characters
            tweet = quote[:240] + "..." if len(quote) > 240 else quote
            twitter.extend([
                f"### Tweet {i}\n",
                f"{tweet}\n",
                "#ProfessionalGrowth #Success\n"
            ])
            
        return "\n".join(twitter)
        
    def _generate_instagram_posts(self, content: Dict[str, List[str]], style: Dict[str, List[str]]) -> str:
        """Generate Instagram posts."""
        topics = content['topics'][:2] if content['topics'] else []
        values = style['values'][:2] if style['values'] else []
        
        instagram = [
            "\n## Instagram Posts\n"
        ]
        
        for i, (topic, value) in enumerate(zip(topics, values), 1):
            instagram.extend([
                f"### Post {i}\n",
                f"✨ {value}\n" if value else "✨ Professional Excellence\n",
                f"{topic}\n" if topic else "Sharing insights and inspiration.\n",
                ".⁣\n.⁣\n.⁣\n",
                "#ProfessionalDevelopment #Growth #Success\n"
            ])
            
        return "\n".join(instagram)
