"""
Social Media Kit Generator

Creates platform-optimized social media posts from transcripts and style profiles.
Generates engaging content for LinkedIn, Facebook, and Twitter/X while maintaining
brand voice and emotional resonance.
"""

from typing import Dict, List, Tuple
import re
from datetime import datetime
from pathlib import Path


def extract_voice_style(style_profile: str) -> Dict[str, str]:
    """
    Extract voice characteristics and writing style.
    
    Args:
        style_profile (str): Raw style profile content
        
    Returns:
        Dict with voice style guidance
    """
    # Voice indicators
    formal_indicators = ['professional', 'strategic', 'expert', 'authority']
    personal_indicators = ['authentic', 'vulnerable', 'real', 'raw']
    
    # Analyze style profile
    profile_lower = style_profile.lower()
    formal_count = sum(1 for ind in formal_indicators if ind in profile_lower)
    personal_count = sum(1 for ind in personal_indicators if ind in profile_lower)
    
    # Determine primary voice style
    voice_style = {
        'tone': 'formal' if formal_count > personal_count else 'personal',
        'perspective': 'third-person' if formal_count > personal_count else 'first-person'
    }
    
    return voice_style


def find_key_quotes(transcript_text: str, count: int = 3) -> List[str]:
    """
    Find multiple unique, impactful quotes from Speaker 1.
    
    Args:
        transcript_text (str): Raw transcript content
        count (int): Number of quotes to return
        
    Returns:
        List[str]: Best matching quotes, ordered by impact
    """
    # Extract Speaker 1 quotes
    quotes = []
    lines = transcript_text.split('\n')
    
    for line in lines:
        if line.startswith('Speaker 1:'):
            quote = line.replace('Speaker 1:', '').strip()
            if '"' in quote:
                # Clean up quote
                quote = re.search(r'"([^"]+)"', quote)
                if quote:
                    quotes.append(quote.group(1))
    
    if not quotes:
        raise ValueError("No valid quotes found from Speaker 1")
    
    # Score quotes by impact and emotion
    impact_words = ['realized', 'learned', 'discovered', 'changed', 'transformed']
    emotion_words = ['felt', 'believed', 'feared', 'hoped', 'dreamed']
    
    scored_quotes = []
    for quote in quotes:
        impact_score = sum(1 for word in impact_words if word.lower() in quote.lower())
        emotion_score = sum(1 for word in emotion_words if word.lower() in quote.lower())
        total_score = impact_score + emotion_score
        scored_quotes.append((total_score, quote))
    
    # Sort by score and return unique quotes
    unique_quotes = []
    seen_themes = set()
    
    for _, quote in sorted(scored_quotes, key=lambda x: x[0], reverse=True):
        # Simple theme detection to avoid similar quotes
        theme = ' '.join(word.lower() for word in quote.split()[:3])
        if theme not in seen_themes:
            unique_quotes.append(quote)
            seen_themes.add(theme)
            if len(unique_quotes) == count:
                break
    
    return unique_quotes


def generate_linkedin_post(transcript_text: str, style_profile: str, quote: str) -> str:
    """Generate a professional LinkedIn post with personal insight."""
    voice = extract_voice_style(style_profile)
    
    # Create hook based on voice style
    if voice['tone'] == 'formal':
        hook = "The difference between change and transformation? One alters your path. The other reshapes your story."
    else:
        hook = "Ever notice how the biggest shifts in life start with the smallest moments of truth?"
    
    # Build narrative paragraphs
    if voice['perspective'] == 'first-person':
        narrative = (
            "When I sat down with [Speaker 1], I expected insights about success. "
            "What emerged was a raw conversation about courage, identity, and the "
            "price of staying silent.\n\n"
            "Their journey challenged everything I thought I knew about growth—and "
            "what it truly means to build a life that aligns with your values."
        )
    else:
        narrative = (
            "[Speaker 1]'s story challenges our assumptions about transformation. "
            "It's not about finding a better path—it's about having the courage to "
            "question the destination itself.\n\n"
            "Their journey reveals how authentic growth often means letting go of "
            "the very things we thought would make us feel secure."
        )
    
    # Format post
    post = [
        "## 🔗 LinkedIn",
        "",
        hook,
        "",
        narrative,
        "",
        f"> \"{quote}\"",
        "",
        "The real insight? Transformation isn't about becoming someone new. "
        "It's about having the courage to be who you already are.",
        "",
        "#AuthenticLeadership #PersonalGrowth #Transformation #CourageToChange #TruthTelling"
    ]
    
    return "\n".join(post)


def generate_facebook_post(transcript_text: str, style_profile: str, quote: str) -> str:
    """Generate a warm, relatable Facebook post."""
    # Create emotional opener
    opener = "Sometimes the most powerful stories are the ones we're most afraid to tell."
    
    # Build personal story
    story = (
        "Listening to [Speaker 1] share their journey reminded me how often we "
        "trade authenticity for approval. How we build lives that look perfect "
        "on paper, while our hearts whisper for something else entirely."
    )
    
    # Format post
    post = [
        "## 📘 Facebook",
        "",
        opener,
        "",
        story,
        "",
        f"> \"{quote}\"",
        "",
        "If this resonates, know you're not alone. Your truth matters more than any script society handed you."
    ]
    
    return "\n".join(post)


def generate_twitter_post(transcript_text: str, style_profile: str, quote: str) -> str:
    """Generate a punchy, impactful Twitter post."""
    # Format quote-based post
    if len(quote) <= 180:  # Leave room for hashtags
        post = [
            "## 🐦 Twitter/X",
            "",
            f"\"{quote}\"",
            "",
            "Your truth is waiting. Listen.",
            "",
            "#AuthenticLife #BraveTruth"
        ]
    else:
        # Create insight-based post using quote theme
        theme_words = quote.split()[:6]  # Use first few words to maintain connection
        insight = (
            "When your silence costs more than your fear of speaking up—"
            "that's where transformation begins."
        )
        post = [
            "## 🐦 Twitter/X",
            "",
            insight,
            "",
            "#CourageToChange #TruthTelling"
        ]
    
    return "\n".join(post)


def generate(transcript_text: str, style_profile: str) -> str:
    """
    Generate platform-optimized social media posts.
    
    Args:
        transcript_text (str): Raw content from transcript_chunks.md
        style_profile (str): Raw content from style-profile.md
        
    Returns:
        str: Formatted social media kit in markdown
        
    Raises:
        ValueError: If no valid quotes found or content requirements not met
    """
    # Get unique quotes for each platform
    quotes = find_key_quotes(transcript_text, count=3)
    if len(quotes) < 3:
        raise ValueError("Not enough unique quotes found for all platforms")
    
    # Generate platform-specific posts with unique quotes
    linkedin_post = generate_linkedin_post(transcript_text, style_profile, quotes[0])
    facebook_post = generate_facebook_post(transcript_text, style_profile, quotes[1])
    twitter_post = generate_twitter_post(transcript_text, style_profile, quotes[2])
    
    # Format final output
    social_kit = [
        linkedin_post,
        "",
        "---",
        "",
        facebook_post,
        "",
        "---",
        "",
        twitter_post
    ]
    
    # Save to output file
    output_dir = Path(__file__).parent.parent / "output" / "app3"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "output_social_kit.md"
    
    content = "\n".join(social_kit)
    output_file.write_text(content, encoding='utf-8')
    
    return content
