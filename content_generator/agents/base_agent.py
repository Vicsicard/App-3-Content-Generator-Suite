"""Base agent class for content generation."""
from abc import ABC, abstractmethod
from typing import Dict, Any
import logging

class ContentAgent(ABC):
    """Base class for all content generation agents."""
    
    def __init__(self, style_profile: str, transcript: str):
        """Initialize the agent with style profile and transcript.
        
        Args:
            style_profile: Content of style-profile.md
            transcript: Content of transcript_chunks.md
        """
        self.style_profile = style_profile
        self.transcript = transcript
        self.logger = logging.getLogger(self.__class__.__name__)
        
    @abstractmethod
    def generate(self) -> str:
        """Generate content in markdown format.
        
        Returns:
            str: Generated content in markdown format
        """
        pass
    
    def _extract_style_elements(self) -> Dict[str, Any]:
        """Extract style elements from style profile.
        
        Returns:
            Dict[str, Any]: Dictionary of style elements
        """
        elements = {
            'voice': [],
            'themes': [],
            'values': [],
            'emotional_tone': [],
            'relatability': []
        }
        
        current_section = None
        for line in self.style_profile.split('\n'):
            if line.startswith('## '):
                current_section = line[3:].lower().strip(':')
            elif line.startswith('- ') and current_section in elements:
                elements[current_section].append(line[2:])
                
        return elements
    
    def _get_chunks(self) -> list[str]:
        """Extract chunks from transcript.
        
        Returns:
            list[str]: List of transcript chunks
        """
        chunks = []
        current_chunk = []
        
        for line in self.transcript.split('\n'):
            if line.startswith('### Chunk'):
                if current_chunk:
                    chunks.append('\n'.join(current_chunk))
                current_chunk = []
            elif line.strip() and not line.startswith('#'):
                current_chunk.append(line)
                
        if current_chunk:
            chunks.append('\n'.join(current_chunk))
            
        return chunks
