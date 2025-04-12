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

# Import input loader
from content_generator.utils.input_loader import load_transcript, load_style_profile

# Import all agents
from content_generator.agents.blog_generator import BlogGeneratorAgent
from content_generator.agents.show_notes_builder import ShowNotesBuilderAgent
from content_generator.agents.newsletter_writer import NewsletterWriterAgent
from content_generator.agents.social_media_kit import SocialMediaKitAgent
from content_generator.agents.bio_creator import BioCreatorAgent
from content_generator.agents.ad_copy_studio import AdCopyStudioAgent
from content_generator.agents.reputation_repair import ReputationRepairAgent
from content_generator.agents.website_generator import WebsiteGeneratorAgent

# Define agent output mapping
AGENT_OUTPUTS = {
    'blog_generator': 'output_blog.md',
    'show_notes_builder': 'output_show_notes.md',
    'newsletter_writer': 'output_newsletter.md',
    'social_media_kit': 'output_social_posts.md',
    'bio_creator': 'output_bio.md',
    'ad_copy_studio': 'output_ad_copy.md',
    'reputation_repair': 'output_reputation.md',
    'website_generator': 'output_website.md'
}

# Define agent execution order
AGENT_ORDER = [
    (BlogGeneratorAgent, 'blog_generator'),
    (ShowNotesBuilderAgent, 'show_notes_builder'),
    (NewsletterWriterAgent, 'newsletter_writer'),
    (SocialMediaKitAgent, 'social_media_kit'),
    (BioCreatorAgent, 'bio_creator'),
    (AdCopyStudioAgent, 'ad_copy_studio'),
    (ReputationRepairAgent, 'reputation_repair'),
    (WebsiteGeneratorAgent, 'website_generator')
]

def setup_logging(output_dir: Path) -> None:
    """Set up logging configuration."""
    log_file = output_dir / "content_generator.log"
    
    # Create a formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    
    # Set up file handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    
    # Set up console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    logging.info("Content Generator Suite starting...")

def save_output(content: str, filename: str, output_dir: Path) -> None:
    """Save generated content to output file."""
    try:
        # Ensure output directory exists
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / filename
        output_path.write_text(content, encoding='utf-8')
        logging.info(f" Saved: {filename}")
    except Exception as e:
        logging.error(f"Failed to save {filename}: {str(e)}")
        raise

def run_agent(agent_class, agent_name: str, transcript: str, style: str) -> str:
    """Run a single agent with error handling."""
    try:
        logging.info(f"Running {agent_name}...")
        # Instantiate the agent
        agent_instance = agent_class(style, transcript)
        # Generate content
        return agent_instance.generate()
    except Exception as e:
        logging.error(f"Error in {agent_name}: {str(e)}")
        return f"# Error in {agent_name}\nFailed to generate content: {str(e)}"

def run_content_generation(transcript_text: str, style_data: str, output_dir: Path) -> None:
    """Run content generation with all agents."""
    # Process with each agent in order
    logging.info("\nGenerating content...")
    success_count = 0
    total_agents = len(AGENT_ORDER)
    start_time = datetime.now()
    
    for agent_class, agent_name in AGENT_ORDER:
        try:
            output = run_agent(agent_class, agent_name, transcript_text, style_data)
            save_output(output, AGENT_OUTPUTS[agent_name], output_dir)
            success_count += 1
        except Exception as e:
            logging.error(f"Agent {agent_name} failed: {str(e)}")
            continue
                
    # Log completion
    end_time = datetime.now()
    duration = end_time - start_time
    logging.info(f"\n Content generation complete ({success_count}/{total_agents} agents successful)")
    logging.info(f"Duration: {duration.total_seconds():.2f} seconds")
    logging.info(f"Files saved in: {output_dir}")

@click.command()
@click.option('--transcript', required=True, type=click.Path(exists=True), help='Path to transcript chunks file')
@click.option('--style', required=True, type=click.Path(exists=True), help='Path to style profile file')
def main(transcript: str, style: str) -> None:
    """Main entry point for content generator."""
    try:
        # Set up output directory
        package_root = Path(__file__).parent.parent
        output_dir = package_root / "output" / "app3"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Set up logging
        setup_logging(output_dir)
        
        logging.info("Loading input files...")
        # Load input files
        transcript_text = load_transcript(transcript)
        style_data = load_style_profile(style)
        
        logging.info("Starting content generation...")
        # Run content generation
        run_content_generation(transcript_text, style_data, output_dir)
        
    except Exception as e:
        logging.error(f"Content generation failed: {str(e)}")
        raise

if __name__ == "__main__":
    main()
