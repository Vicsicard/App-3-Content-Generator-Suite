"""Reputation writer agent for App 3."""

from pathlib import Path
from typing import Dict, List
from ..database.content_manager import content_manager
from content_generator.agents.base_agent import ContentAgent

class ReputationWriter(ContentAgent):
    """Generates reputation repair content from transcript and style profile."""
    
    def __init__(self, input_dir: str = 'input'):
        """Initialize reputation writer."""
        super().__init__()
        self.input_dir = Path(input_dir)
        
    def generate(self) -> Dict:
        """Generate reputation repair content and save to Supabase.
        
        Returns:
            Dict containing the saved content record
        """
        # Load input files
        transcript_path = self.input_dir / 'transcript_chunks.md'
        style_path = self.input_dir / 'style-profile.md'
        
        transcript = transcript_path.read_text() if transcript_path.exists() else ""
        style = style_path.read_text() if style_path.exists() else ""
        
        # Generate repair content
        repair_content = self._generate_repair_content(transcript, style)
        
        # Save directly to Supabase
        return content_manager.save_content(
            name='reputation_repair',
            content=repair_content,
            type='response',  # This is a response document
            format='markdown'  # Markdown formatted content
        )
        
    def _generate_repair_content(self, transcript: str, style: str) -> str:
        """Generate reputation repair content from inputs.
        
        Args:
            transcript: Content from transcript_chunks.md
            style: Content from style-profile.md
            
        Returns:
            Generated markdown content
        """
        # Extract key elements
        situation = self._extract_situation(transcript)
        concerns = self._extract_concerns(transcript)
        values = self._extract_values(style)
        
        # Generate response sections
        acknowledgment = self._generate_acknowledgment(situation, concerns)
        explanation = self._generate_explanation(situation, values)
        action_plan = self._generate_action_plan(concerns, values)
        commitment = self._generate_commitment(values)
        
        # Format final response
        response = [
            "# Professional Response\n",
            "## Acknowledgment\n",
            acknowledgment,
            "\n## Explanation\n",
            explanation,
            "\n## Action Plan\n",
            action_plan,
            "\n## Our Commitment\n",
            commitment
        ]
        
        return "\n".join(response)
    
    def _extract_situation(self, transcript: str) -> Dict[str, str]:
        """Extract situation details from transcript."""
        situation = {
            'context': '',
            'impact': '',
            'stakeholders': []
        }
        
        # Parse transcript for situation details
        chunks = transcript.split('## [Chunk')
        for chunk in chunks[1:]:
            if 'situation:' in chunk.lower():
                situation['context'] = chunk.split('situation:')[1].split('\n')[0].strip()
            if 'impact:' in chunk.lower():
                situation['impact'] = chunk.split('impact:')[1].split('\n')[0].strip()
            if 'stakeholders:' in chunk.lower():
                stakeholders = chunk.split('stakeholders:')[1].split('\n')[0].strip()
                situation['stakeholders'] = [s.strip() for s in stakeholders.split(',')]
                
        return situation
    
    def _extract_concerns(self, transcript: str) -> List[str]:
        """Extract key concerns from transcript."""
        concerns = []
        chunks = transcript.split('## [Chunk')
        for chunk in chunks[1:]:
            if 'concern:' in chunk.lower():
                concern = chunk.split('concern:')[1].split('\n')[0].strip()
                concerns.append(concern)
        return concerns
    
    def _extract_values(self, style: str) -> List[str]:
        """Extract company values from style profile."""
        values = []
        if 'values:' in style.lower():
            values_section = style.split('values:')[1].split('\n\n')[0]
            values = [v.strip('- ').strip() for v in values_section.split('\n') if v.strip().startswith('-')]
        return values if values else ['integrity', 'transparency', 'accountability']
    
    def _generate_acknowledgment(self, situation: Dict[str, str], concerns: List[str]) -> str:
        """Generate acknowledgment section."""
        acknowledgment = [
            "We understand the concerns raised regarding " + situation['context'] + ". ",
            "We recognize the impact this has had on " + ', '.join(situation['stakeholders']) + ". ",
            "\nSpecifically, we acknowledge:"
        ]
        
        for concern in concerns:
            acknowledgment.append(f"\n- {concern}")
            
        return '\n'.join(acknowledgment)
    
    def _generate_explanation(self, situation: Dict[str, str], values: List[str]) -> str:
        """Generate explanation section."""
        explanation = [
            f"We want to provide context about {situation['context']}. ",
            f"As an organization built on {', '.join(values)}, we take full responsibility for addressing this situation. ",
            "\nHere's what happened:",
            f"\n- {situation['impact']}"
        ]
        
        return '\n'.join(explanation)
    
    def _generate_action_plan(self, concerns: List[str], values: List[str]) -> str:
        """Generate action plan section."""
        action_plan = ["We are taking immediate steps to address these concerns:"]
        
        for i, concern in enumerate(concerns):
            action = f"Implementing new {values[i % len(values)]}-based protocols"
            action_plan.append(f"\n- {action} to prevent {concern.lower()}")
            
        return '\n'.join(action_plan)
    
    def _generate_commitment(self, values: List[str]) -> str:
        """Generate commitment section."""
        commitment = [
            f"Our commitment to {values[0]} remains unwavering. ",
            "We will:",
            "\n- Provide regular updates on our progress",
            "- Maintain open channels of communication",
            "- Continue to uphold the highest standards of professional conduct",
            "\nWe appreciate your trust and patience as we work to rebuild confidence in our organization."
        ]
        
        return '\n'.join(commitment)
