"""Base agent class for all content generators."""

from abc import ABC, abstractmethod
from typing import Dict

class ContentAgent(ABC):
    """Base class for all content generation agents."""
    
    def __init__(self):
        """Initialize base agent."""
        pass
        
    @abstractmethod
    def generate(self, transcript: str, style_profile: str) -> str:
        """Generate content from transcript and style profile.
        
        Args:
            transcript: Content from transcript_chunks.md
            style_profile: Content from style-profile.md
            
        Returns:
            Generated content as HTML string
        """
        pass
    
    def _extract_style_elements(self, style_profile: str) -> Dict[str, list]:
        """Extract style elements from style profile.
        
        Args:
            style_profile: Content from style-profile.md
            
        Returns:
            Dict[str, list]: Dictionary of style elements
        """
        elements = {
            'voice': [],
            'themes': [],
            'values': [],
            'emotional_tone': [],
            'relatability': []
        }
        
        current_section = None
        for line in style_profile.split('\n'):
            if line.startswith('## '):
                current_section = line[3:].lower().strip(':')
            elif line.startswith('- ') and current_section in elements:
                elements[current_section].append(line[2:])
                
        return elements
    
    def _get_chunks(self, transcript: str) -> list[str]:
        """Extract chunks from transcript.
        
        Args:
            transcript: Content from transcript_chunks.md
            
        Returns:
            list[str]: List of transcript chunks
        """
        chunks = []
        current_chunk = []
        
        for line in transcript.split('\n'):
            if line.startswith('### Chunk'):
                if current_chunk:
                    chunks.append('\n'.join(current_chunk))
                current_chunk = []
            elif line.strip() and not line.startswith('#'):
                current_chunk.append(line)
                
        if current_chunk:
            chunks.append('\n'.join(current_chunk))
            
        return chunks
