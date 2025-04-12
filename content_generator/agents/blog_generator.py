"""Blog Generator Agent.

Creates blog content from narrative transcripts.
"""

from typing import Dict, List, Any
from collections import Counter
from pathlib import Path
from .base_agent import ContentAgent
from content_generator.utils.content_writer import format_markdown_section


class BlogGeneratorAgent(ContentAgent):
    """Blog generator agent that creates blog content."""
    
    def generate(self) -> str:
        """Generate blog content using transcript and style profile."""
        # Extract content elements and style data
        content_elements = self._extract_content_elements()
        style_data = self._parse_style_profile()
        
        # Generate blog sections
        intro = self._generate_intro(content_elements, style_data)
        main_content = self._generate_main_content(content_elements, style_data)
        conclusion = self._generate_conclusion(content_elements, style_data)
        
        # Combine all sections
        blog_post = [
            "# Blog Post\n",
            intro,
            main_content,
            conclusion
        ]
        
        return "\n".join(blog_post)
        
    def _extract_content_elements(self) -> Dict[str, List[str]]:
        """Extract content elements from transcript."""
        elements = {
            'topics': [],
            'insights': [],
            'examples': []
        }
        current_section = None
        current_text = []
        
        # Use Counter to identify most frequent topics
        topic_counter = Counter()
        
        for line in self.transcript.split('\n'):
            if line.startswith('Speaker 2:'):
                if current_text:
                    text = ' '.join(current_text)
                    # Count word frequency for topic identification
                    words = [word.lower() for word in text.split() if len(word) > 4]
                    topic_counter.update(words)
                    
                    if any(word in text.lower() for word in ['key', 'important', 'critical']):
                        elements['insights'].append(text)
                    elif any(word in text.lower() for word in ['example', 'instance', 'case']):
                        elements['examples'].append(text)
                    else:
                        elements['topics'].append(text)
                    current_text = []
                current_text.append(line.replace('Speaker 2:', '').strip())
            elif current_text:
                current_text.append(line.strip())
                
        # Process final section
        if current_text:
            text = ' '.join(current_text)
            words = [word.lower() for word in text.split() if len(word) > 4]
            topic_counter.update(words)
            
            if any(word in text.lower() for word in ['key', 'important', 'critical']):
                elements['insights'].append(text)
            elif any(word in text.lower() for word in ['example', 'instance', 'case']):
                elements['examples'].append(text)
            else:
                elements['topics'].append(text)
                
        # Add top topics if none were explicitly identified
        if not elements['topics'] and topic_counter:
            top_topics = [topic for topic, _ in topic_counter.most_common(3)]
            elements['topics'] = [f"Exploring {topic}" for topic in top_topics]
                
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
        
    def _generate_intro(self, content: Dict[str, List[str]], style: Dict[str, List[str]]) -> str:
        """Generate blog introduction."""
        theme = style['themes'][0] if style['themes'] else 'Professional Excellence'
        topic = content['topics'][0] if content['topics'] else f"Exploring {theme}"
        
        intro = [
            "## Introduction\n",
            f"In today's exploration of {theme}, we'll dive deep into {topic}.\n"
        ]
        return "\n".join(intro)
        
    def _generate_main_content(self, content: Dict[str, List[str]], style: Dict[str, List[str]]) -> str:
        """Generate main blog content."""
        insights = content['insights'][:3] if content['insights'] else []
        examples = content['examples'][:3] if content['examples'] else []
        values = style['values'][:3] if style['values'] else []
        
        main_content = [
            "\n## Main Content\n"
        ]
        
        # Add key insights with value alignment
        for i, (insight, value) in enumerate(zip(insights, values), 1):
            main_content.extend([
                f"### {value}\n" if value else f"### Key Point {i}\n",
                f"{insight}\n" if insight else "Exploring professional insights and growth opportunities.\n"
            ])
            
        # Add examples if available
        if examples:
            main_content.append("\n### Real-World Applications\n")
            for example in examples:
                main_content.append(f"- {example}\n")
                
        return "\n".join(main_content)
        
    def _generate_conclusion(self, content: Dict[str, List[str]], style: Dict[str, List[str]]) -> str:
        """Generate blog conclusion."""
        theme = style['themes'][0] if style['themes'] else 'professional excellence'
        
        conclusion = [
            "\n## Conclusion\n",
            f"As we continue to explore {theme}, these insights provide valuable guidance for growth and development.\n",
            "\n### Next Steps\n",
            "Ready to learn more? Let's connect and explore these topics further.\n"
        ]
        return "\n".join(conclusion)
