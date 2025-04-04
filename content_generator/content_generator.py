#!/usr/bin/env python3
"""
Content Generator Suite - Main Runner Script
Processes input files and coordinates AI agents to generate multiple content formats.
"""

import sys
from pathlib import Path
import click
from typing import Dict, Tuple

# Import input loader
from utils.input_loader import load_transcript, load_style_profile

# Import all agents
from agents import (
    blog_generator,
    show_notes_builder,
    newsletter_writer,
    social_media_kit,
    bio_creator,
    ad_copy_studio,
    reputation_repair
)

# Define agent output mapping
AGENT_OUTPUTS = {
    'blog_generator': 'output_blog.md',
    'show_notes_builder': 'output_show_notes.md',
    'newsletter_writer': 'output_newsletter.md',
    'social_media_kit': 'output_social_posts.md',
    'bio_creator': 'output_bio.md',
    'ad_copy_studio': 'output_ad_copy.md',
    'reputation_repair': 'output_reputation.md'
}

# Define agent execution order
AGENT_ORDER = [
    (blog_generator, 'blog_generator'),
    (show_notes_builder, 'show_notes_builder'),
    (newsletter_writer, 'newsletter_writer'),
    (social_media_kit, 'social_media_kit'),
    (bio_creator, 'bio_creator'),
    (ad_copy_studio, 'ad_copy_studio'),
    (reputation_repair, 'reputation_repair')
]

def save_output(content: str, filename: str, output_dir: Path) -> None:
    """Save generated content to output file."""
    output_path = output_dir / filename
    output_path.write_text(content, encoding='utf-8')
    print(f"Saved: {filename}")

@click.command()
@click.option('--transcript', required=True, type=click.Path(exists=True), help='Path to transcript_chunks.md')
@click.option('--style', required=True, type=click.Path(exists=True), help='Path to style-profile.md')
def main(transcript: str, style: str) -> None:
    """
    Main entry point for Content Generator Suite.
    Loads input files and coordinates content generation across all agents.
    """
    # Ensure output directory exists
    output_dir = Path(__file__).parent / "output" / "app3"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        # Load input files
        print("Loading input files...")
        transcript_content = load_transcript(transcript)
        style_content = load_style_profile(style)
        print("Files loaded successfully")
        
        # Process with each agent in order
        print("\nGenerating content...")
        for agent, agent_name in AGENT_ORDER:
            print(f"Running {agent_name}...")
            output = agent.generate(transcript_content, style_content)
            save_output(output, AGENT_OUTPUTS[agent_name], output_dir)
            
        # Print final success message
        print("\n App 3 Content Generator Suite complete.")
        print(f"All content saved to: {output_dir}")
        
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
