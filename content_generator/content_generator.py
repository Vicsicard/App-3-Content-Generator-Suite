#!/usr/bin/env python3
"""
Content Generator Suite - Main Runner Script
Processes input files and coordinates AI agents to generate multiple content formats.
"""

import sys
from pathlib import Path
import click
from typing import Dict, Tuple
import logging
from datetime import datetime
import platform

def verify_python_version():
    """Verify that Python 3.10.x is being used."""
    version = platform.python_version()
    if not version.startswith('3.10.'):
        print(" ERROR: This application requires Python 3.10")
        print(f"Current version: {version}")
        print("Please switch to Python 3.10 and try again")
        sys.exit(1)
    return True

# Verify Python version before anything else
verify_python_version()

# Import storage managers
from content_generator.storage.input_storage import input_storage
from content_generator.storage.supabase_storage import storage_manager

# Import all agents
from content_generator.agents.blog_generator import BlogGenerator
from content_generator.agents.show_notes_writer import ShowNotesWriter
from content_generator.agents.bio_writer import BioWriter
from content_generator.agents.ad_copy_writer import AdCopyWriter
from content_generator.agents.reputation_writer import ReputationWriter
from content_generator.agents.social_media_writer import SocialMediaWriter
from content_generator.agents.website_writer import WebsiteWriter

# Import enhanced content generators
from content_generator.agents.enhanced_bio_writer import EnhancedBioWriter
from content_generator.agents.enhanced_blog_generator import EnhancedBlogGenerator
from content_generator.agents.enhanced_social_media_writer import EnhancedSocialMediaWriter
from content_generator.utils.authentic_content_coordinator import authentic_content_coordinator

# Define agent output mapping
AGENT_TYPES = {
    'blog_generator': BlogGenerator,
    'show_notes_writer': ShowNotesWriter,
    'bio_writer': BioWriter,
    'ad_copy_writer': AdCopyWriter,
    'reputation_writer': ReputationWriter,
    'social_media_writer': SocialMediaWriter,
    'website_writer': WebsiteWriter
}

# Define enhanced agent mapping
ENHANCED_AGENT_TYPES = {
    'bio_writer': EnhancedBioWriter,
    'blog_generator': EnhancedBlogGenerator,
    'social_media_writer': EnhancedSocialMediaWriter
}

# Define content type mapping
CONTENT_TYPES = {
    'blog_generator': 'blog',
    'show_notes_writer': 'show_notes',
    'bio_writer': 'bio',
    'ad_copy_writer': 'ad',
    'reputation_writer': 'reputation',
    'social_media_writer': 'social',
    'website_writer': 'website'
}

def setup_logging():
    """Set up logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(levelname)s:%(message)s'
    )

# Set up logging configuration
setup_logging()

def run_agent(agent_name: str, transcript: str, style: str, client_id: str, use_enhanced: bool = False) -> None:
    """Run a single agent and store its output.
    
    Args:
        agent_name: Name of the agent (for logging)
        transcript: Transcript content
        style: Style profile content
        client_id: Client identifier
        use_enhanced: Whether to use enhanced generators for supported content types
    """
    try:
        # Determine which agent class to use
        if use_enhanced and agent_name in ENHANCED_AGENT_TYPES:
            agent_class = ENHANCED_AGENT_TYPES[agent_name]
            logging.info(f"Using enhanced {agent_name} for more authentic content")
        else:
            agent_class = AGENT_TYPES[agent_name]
            
        # Initialize agent
        agent = agent_class()
        
        # Generate content
        content = agent.generate(transcript, style)
        
        # Store in Supabase
        content_type = CONTENT_TYPES[agent_name]
        metadata = {
            'client_id': client_id,
            'generator': agent_name,
            'enhanced': use_enhanced,
            'generated_at': datetime.now().isoformat()
        }
        
        storage_path = storage_manager.store_content(
            content_type=content_type,
            content=content,
            metadata=metadata
        )
        
        logging.info(f"Successfully ran {agent_name} and stored at {storage_path}")
        
    except Exception as e:
        logging.error(f"Error running {agent_name}: {str(e)}")
        raise

def run_content_generation(client_id: str, use_enhanced: bool = True) -> None:
    """Run content generation with all agents.
    
    Args:
        client_id: Client identifier (e.g. 'annie')
        use_enhanced: Whether to use enhanced generators for supported content types
    """
    logging.info(f"Starting content generation for client: {client_id}")
    
    try:
        if use_enhanced:
            # Use the authentic content coordinator for enhanced generation
            logging.info("Using enhanced content generators for authentic voice...")
            
            # Generate all content using authentic content coordinator
            authentic_content_coordinator.generate_all_content(client_id)
            
            logging.info("Successfully generated enhanced content using authentic voice")
            
            # Run remaining regular agents
            regular_agents = [name for name in AGENT_TYPES if name not in ENHANCED_AGENT_TYPES]
            
            if regular_agents:
                # Load input files from Supabase
                logging.info("Fetching input files from Supabase for remaining agents...")
                transcript_path = f"client-files/{client_id}/transcript_chunks.md"
                style_path = f"client-files/{client_id}/style-profile.md"
                
                transcript = input_storage.fetch_input_file(transcript_path)
                style = input_storage.fetch_input_file(style_path)
                
                # Run each regular agent
                for agent_name in regular_agents:
                    logging.info(f"Running {agent_name}...")
                    run_agent(agent_name, transcript, style, client_id, use_enhanced=False)
                
        else:
            # Use original content generation flow
            logging.info("Using original content generators...")
            
            # Load input files from Supabase
            logging.info("Fetching input files from Supabase...")
            transcript_path = f"client-files/{client_id}/transcript_chunks.md"
            style_path = f"client-files/{client_id}/style-profile.md"
            
            print(f"Fetching input files for client {client_id}:")
            print(f"- Transcript: {transcript_path}")
            print(f"- Style Profile: {style_path}")
            
            transcript = input_storage.fetch_input_file(transcript_path)
            print(f"Successfully fetched {transcript_path}")
            
            style = input_storage.fetch_input_file(style_path)
            print(f"Successfully fetched {style_path}")
            
            logging.info("Successfully loaded input files")
            
            # Run each agent
            for agent_name in AGENT_TYPES:
                logging.info(f"Running {agent_name}...")
                run_agent(agent_name, transcript, style, client_id, use_enhanced=False)
            
    except Exception as e:
        logging.error(f"Content generation failed: {str(e)}")
        raise

@click.command()
@click.option('--client', required=True, help='Client identifier (e.g. annie)')
@click.option('--use-enhanced', default=True, help='Whether to use enhanced generators for supported content types')
def main(client: str, use_enhanced: bool):
    """Main entry point for content generator."""
    try:
        run_content_generation(client, use_enhanced)
    except Exception as e:
        logging.error(f"Failed to generate content: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
