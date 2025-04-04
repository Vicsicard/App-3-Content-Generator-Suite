"""
Newsletter Writer Agent

Converts narrative transcripts into engaging newsletter introductions
that drive reader engagement while maintaining the speaker's authentic voice.

The agent analyzes the transcript content and style profile to create
a compelling 200-300 word introduction that captures key insights
and emotional resonance.
"""

from typing import Dict, List, Optional, Tuple
import re
from datetime import datetime
from pathlib import Path

def extract_email_voice(style_profile: str) -> Dict[str, str]:
    """
    Extract voice and tone characteristics for email writing.
    
    Args:
        style_profile (str): Raw style profile content
        
    Returns:
        Dict containing voice and tone guidance
    """
    # Voice/tone mapping based on style indicators
    voice_indicators = {
        'inspiring': ['visionary', 'motivational', 'uplifting', 'passionate'],
        'raw': ['authentic', 'honest', 'vulnerable', 'real'],
        'thoughtful': ['reflective', 'analytical', 'insightful', 'measured'],
        'bold': ['confident', 'direct', 'assertive', 'strong']
    }
    
    # Default tone
    tone_profile = {
        'voice': 'thoughtful',
        'tone': 'reflective'
    }
    
    # Extract style elements
    style_lower = style_profile.lower()
    
    # Determine voice style
    max_matches = 0
    for voice, indicators in voice_indicators.items():
        matches = sum(1 for ind in indicators if ind in style_lower)
        if matches > max_matches:
            max_matches = matches
            tone_profile['voice'] = voice
    
    # Determine tone based on voice and context
    if tone_profile['voice'] == 'inspiring':
        tone_profile['tone'] = 'motivational'
    elif tone_profile['voice'] == 'raw':
        tone_profile['tone'] = 'authentic'
    elif tone_profile['voice'] == 'thoughtful':
        tone_profile['tone'] = 'reflective'
    else:  # bold
        tone_profile['tone'] = 'confident'
    
    return tone_profile


def identify_newsletter_angle(transcript_text: str) -> Tuple[str, List[str]]:
    """
    Identify compelling angle and supporting quotes.
    
    Args:
        transcript_text (str): Raw transcript content
        
    Returns:
        Tuple of (theme, relevant quotes)
    """
    # Theme patterns to search for
    theme_patterns = {
        'starting over': ['begin again', 'fresh start', 'new chapter'],
        'finding purpose': ['calling', 'mission', 'purpose', 'meaning'],
        'overcoming fear': ['fear', 'doubt', 'overcome', 'courage'],
        'personal growth': ['grow', 'learn', 'develop', 'evolve'],
        'letting go': ['release', 'let go', 'move on', 'accept'],
        'building trust': ['trust', 'relationship', 'connect', 'bond']
    }
    
    # Find theme matches
    theme_matches = {}
    text_lower = transcript_text.lower()
    
    for theme, indicators in theme_patterns.items():
        matches = sum(1 for ind in indicators if ind in text_lower)
        if matches > 0:
            theme_matches[theme] = matches
    
    # Select primary theme
    selected_theme = max(theme_matches.items(), key=lambda x: x[1])[0] if theme_matches else 'personal growth'
    
    # Extract relevant quotes
    quotes = []
    quote_pattern = r'"([^"]+)"'
    all_quotes = re.findall(quote_pattern, transcript_text)
    
    # Filter quotes related to theme
    for quote in all_quotes:
        if any(ind in quote.lower() for ind in theme_patterns[selected_theme]):
            quotes.append(quote)
    
    # Take up to 2 most relevant quotes
    return selected_theme, quotes[:2]


def compose_newsletter_intro(tone: Dict[str, str], theme: str) -> str:
    """
    Compose engaging 2-3 sentence email introduction.
    
    Args:
        tone: Voice and tone guidance
        theme: Primary content theme
        
    Returns:
        str: Email introduction
    """
    # First sentence hooks based on tone
    hooks = {
        'inspiring': "Ever wonder what it takes to truly transform {theme}?",
        'raw': "Ever feel like {theme} isn't what everyone makes it out to be?",
        'thoughtful': "Ever feel like you're becoming someone new—but your life hasn't caught up yet?",
        'bold': "Ever feel like it's time to completely reimagine {theme}?"
    }
    
    # Second sentence transitions based on tone
    transitions = {
        'inspiring': "This week, [Speaker 1] reveals the unexpected path that led to a breakthrough in",
        'raw': "This week, [Speaker 1] opens up about the real challenges and triumphs of",
        'thoughtful': "This week, [Speaker 1] shares how they walked away from a version of success that no longer fit—and the risk of",
        'bold': "This week, [Speaker 1] challenges conventional wisdom about"
    }
    
    # Build introduction
    hook = hooks.get(tone['voice'], hooks['thoughtful'])
    hook = hook.format(theme=theme)
    
    transition = transitions.get(tone['voice'], transitions['thoughtful'])
    ending = "rebuilding something more honest."
    
    return f"{hook}\n\n{transition} {ending}"


def format_newsletter(tone: Dict[str, str], intro: str, theme: str, quote: str = "") -> str:
    """
    Format newsletter in required markdown structure.
    
    Args:
        tone: Voice and tone guidance
        intro: Composed introduction
        theme: Main content theme
        quote: Optional highlight quote
        
    Returns:
        str: Formatted markdown content
    """
    # Create subject line based on theme and tone
    subject_templates = {
        'inspiring': "What if {theme} was just the beginning?",
        'raw': "The truth about {theme} nobody talks about",
        'thoughtful': "What happens when {theme} changes everything?",
        'bold': "Ready to rethink everything about {theme}?"
    }
    
    subject = subject_templates.get(tone['voice'], subject_templates['thoughtful'])
    subject = subject.format(theme=theme)
    
    # Format content blocks
    content = [
        f"## ✉️ Subject: {subject}",
        "",
        "Hi there,",
        "",
        intro
    ]
    
    # Add quote if provided
    if quote:
        content.extend([
            "",
            f"> \"{quote}\""
        ])
    
    # Add call to action
    content.extend([
        "",
        "Read the full story ➜"
    ])
    
    return "\n".join(content)


def count_words(text: str) -> int:
    """Count words in text, excluding markdown symbols."""
    clean_text = re.sub(r'[#*_\->`✉️➜]', '', text)
    return len(clean_text.split())


def generate(transcript_text: str, style_profile: str) -> str:
    """
    Generate a compelling newsletter introduction from transcript and style profile.
    
    Args:
        transcript_text (str): Raw content from transcript_chunks.md
        style_profile (str): Raw content from style-profile.md
        
    Returns:
        str: Formatted newsletter introduction (200-300 words)
        
    Raises:
        ValueError: If no valid quotes found or word count requirements not met
    """
    # Extract email voice and tone
    tone_profile = extract_email_voice(style_profile)
    
    # Identify main theme and quotes
    theme, quotes = identify_newsletter_angle(transcript_text)
    
    # Ensure we have at least one real quote
    if not quotes:
        raise ValueError("No valid quotes found in transcript")
    quote = quotes[0]
    
    # Compose introduction
    intro = compose_newsletter_intro(tone_profile, theme)
    
    # Format newsletter
    newsletter = format_newsletter(tone_profile, intro, theme, quote)
    
    # Validate word count
    word_count = count_words(newsletter)
    
    # Adjust content to meet word count requirements
    if word_count < 200:
        # Expand intro by adding context
        expanded_intro = intro + "\n\nThis conversation dives deep into what it really means to embrace change and growth."
        newsletter = format_newsletter(tone_profile, expanded_intro, theme, quote)
    elif word_count > 300:
        # Trim intro while preserving quote
        intro_parts = intro.split("\n\n")
        if len(intro_parts) > 1:
            intro = "\n\n".join(intro_parts[:2])  # Keep first two paragraphs
            newsletter = format_newsletter(tone_profile, intro, theme, quote)
    
    # Final word count validation
    final_count = count_words(newsletter)
    if not (200 <= final_count <= 300):
        raise ValueError(f"Newsletter length ({final_count} words) outside required range (200-300 words)")
    
    # Save to output file
    output_dir = Path(__file__).parent.parent / "output" / "app3"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "output_newsletter.md"
    
    try:
        output_file.write_text(newsletter, encoding='utf-8')
    except Exception as e:
        raise IOError(f"Failed to save newsletter: {str(e)}")
    
    return newsletter
