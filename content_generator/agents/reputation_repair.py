"""
Reputation Repair Agent.

Creates reputation management content from narrative transcripts.
"""

from typing import Dict, List, Any
from pathlib import Path
from .base_agent import ContentAgent
from content_generator.utils.content_writer import format_markdown_section


class ReputationRepairAgent(ContentAgent):
    """Reputation repair agent that creates reputation management content."""
    
    def generate(self) -> str:
        """Generate reputation repair content using transcript and style profile."""
        # Extract key points and style data
        key_points = self._extract_key_points()
        style_data = self._parse_style_profile()
        
        # Generate content sections
        overview = self._generate_overview(key_points, style_data)
        response = self._generate_response(key_points, style_data)
        action_plan = self._generate_action_plan(style_data)
        
        # Combine all sections
        repair_content = [
            "# Reputation Management Content\n",
            overview,
            response,
            action_plan
        ]
        
        return "\n".join(repair_content)
        
    def _extract_key_points(self) -> List[Dict[str, str]]:
        """Extract key points from transcript."""
        points = []
        current_point = []
        
        for line in self.transcript.split('\n'):
            if line.startswith('Speaker 2:'):
                if current_point:
                    points.append({
                        'topic': current_point[0][:50],
                        'context': ' '.join(current_point)
                    })
                    current_point = []
                current_point.append(line.replace('Speaker 2:', '').strip())
            elif current_point:
                current_point.append(line.strip())
                
        # Add final point
        if current_point:
            points.append({
                'topic': current_point[0][:50],
                'context': ' '.join(current_point)
            })
            
        return points[:3]  # Return top 3 points
        
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
        
    def _generate_overview(self, points: List[Dict[str, str]], style: Dict[str, List[str]]) -> str:
        """Generate situation overview."""
        theme = style['themes'][0] if style['themes'] else 'Professional Excellence'
        overview = [
            "## Situation Overview\n",
            f"In alignment with our commitment to {theme}, we want to address several key points:\n"
        ]
        
        for point in points:
            overview.append(f"- {point['topic']}\n")
            
        return "\n".join(overview)
        
    def _generate_response(self, points: List[Dict[str, str]], style: Dict[str, List[str]]) -> str:
        """Generate detailed response."""
        response = ["## Our Response\n"]
        
        for point in points:
            response.extend([
                "### Addressing the Topic\n",
                f"{point['context']}\n",
                "Our commitment to transparency and improvement remains steadfast.\n"
            ])
            
        return "\n".join(response)
        
    def _generate_action_plan(self, style: Dict[str, List[str]]) -> str:
        """Generate action plan."""
        value = style['values'][0] if style['values'] else 'integrity'
        action_plan = [
            "## Moving Forward\n",
            f"We are taking concrete steps to uphold our {value}:\n",
            "1. Enhanced Communication\n",
            "2. Proactive Engagement\n",
            "3. Continuous Improvement\n",
            "\nWe value your trust and are committed to maintaining it.\n"
        ]
        return "\n".join(action_plan)
