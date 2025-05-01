"""Authentic Content Coordinator for App 3.

Coordinates the enhanced content generators to ensure all generated content
maintains the client's authentic voice and expressions throughout all formats.
"""

import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from ..agents.enhanced_bio_writer import EnhancedBioWriter
from ..agents.enhanced_blog_generator import EnhancedBlogGenerator
from ..agents.enhanced_social_media_writer import EnhancedSocialMediaWriter
from ..storage.input_storage import input_storage
from ..database.content_manager import content_manager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AuthenticContentCoordinator:
    """Coordinates all enhanced content generation to ensure voice consistency."""
    
    def __init__(self, input_dir: str = 'input'):
        """Initialize the authentic content coordinator.
        
        Args:
            input_dir: Directory containing input files
        """
        self.input_dir = Path(input_dir)
        
        # Initialize enhanced content generators
        self.bio_writer = EnhancedBioWriter(input_dir)
        self.blog_generator = EnhancedBlogGenerator(input_dir)
        self.social_media_writer = EnhancedSocialMediaWriter(input_dir)
    
    def generate_all_content(self, client_id: str = "annie") -> Dict[str, Dict]:
        """Generate all content types using the enhanced generators.
        
        Args:
            client_id: Client identifier for retrieving input files
            
        Returns:
            Dictionary mapping content type to content records
        """
        logger.info(f"Generating all authentic content for client: {client_id}")
        
        # Fetch transcript and style profile
        transcript, style_profile = self._load_input_files(client_id)
        
        # Generate all content types
        bio_result = self.generate_bio(transcript, style_profile)
        blog_result = self.generate_blog_posts(transcript, style_profile)
        social_result = self.generate_social_media(transcript, style_profile)
        
        # Collect all results
        results = {
            'bio': bio_result,
            'blog_posts': blog_result,
            'social_media': social_result
        }
        
        logger.info(f"Successfully generated all content for client: {client_id}")
        return results
    
    def generate_bio(
        self, 
        transcript: Optional[str] = None, 
        style_profile: Optional[str] = None
    ) -> Dict:
        """Generate authentic bio content.
        
        Args:
            transcript: Content from transcript_chunks.md (optional)
            style_profile: Content from style-profile.md (optional)
            
        Returns:
            Dictionary containing the saved content record
        """
        logger.info("Generating authentic bio content")
        
        # Load input files if not provided
        if transcript is None or style_profile is None:
            transcript, style_profile = self._load_input_files()
        
        # Generate and save bio content
        return self.bio_writer.generate(transcript, style_profile)
    
    def generate_blog_posts(
        self, 
        transcript: Optional[str] = None, 
        style_profile: Optional[str] = None
    ) -> Dict:
        """Generate authentic blog posts.
        
        Args:
            transcript: Content from transcript_chunks.md (optional)
            style_profile: Content from style-profile.md (optional)
            
        Returns:
            Dictionary containing the saved content record
        """
        logger.info("Generating authentic blog posts")
        
        # Load input files if not provided
        if transcript is None or style_profile is None:
            transcript, style_profile = self._load_input_files()
        
        # Generate and save blog posts
        return self.blog_generator.generate(transcript, style_profile)
    
    def generate_social_media(
        self, 
        transcript: Optional[str] = None, 
        style_profile: Optional[str] = None
    ) -> Dict:
        """Generate authentic social media content.
        
        Args:
            transcript: Content from transcript_chunks.md (optional)
            style_profile: Content from style-profile.md (optional)
            
        Returns:
            Dictionary containing the saved content record
        """
        logger.info("Generating authentic social media content")
        
        # Load input files if not provided
        if transcript is None or style_profile is None:
            transcript, style_profile = self._load_input_files()
        
        # Generate and save social media content
        return self.social_media_writer.generate(transcript, style_profile)
    
    def _load_input_files(self, client_id: str = "annie") -> Tuple[str, str]:
        """Load transcript and style profile from storage.
        
        Args:
            client_id: Client identifier
            
        Returns:
            Tuple of (transcript_content, style_profile_content)
        """
        logger.info(f"Loading input files for client: {client_id}")
        return input_storage.fetch_input_files(client_id)


# Create singleton instance
authentic_content_coordinator = AuthenticContentCoordinator()
