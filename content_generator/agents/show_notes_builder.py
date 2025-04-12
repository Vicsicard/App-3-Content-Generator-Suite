"""
Show Notes Builder Agent

Converts narrative transcripts into engaging podcast-style show notes
that are SEO-friendly and emotionally resonant.

The agent analyzes the transcript content and style profile to create
structured show notes that capture key moments and insights while
maintaining the speaker's authentic voice.
"""

from typing import Dict, List, Optional, Tuple
import re
from datetime import datetime
from collections import Counter
from pathlib import Path
from .base_agent import ContentAgent


class ShowNotesBuilderAgent(ContentAgent):
    """Show notes builder agent that creates podcast-style notes from transcripts."""
    
    def generate(self) -> str:
        """Generate show notes using transcript and style profile."""
        # Extract key highlights
        highlights = extract_highlights(self.transcript)
        
        # Create episode summary
        summary = summarize_episode(self.style_profile, highlights)
        
        # Craft teaser hook
        teaser = craft_teaser(self.style_profile, highlights)
        
        # Format final show notes
        show_notes = format_show_notes(teaser, summary, highlights)
        
        return show_notes


def extract_highlights(transcript_text: str) -> List[str]:
    """
    Extract 4-6 major moments or insights from the transcript.
    
    Args:
        transcript_text (str): Raw transcript content
        
    Returns:
        List[str]: 4-6 key highlights with emotional framing
    """
    # Pattern for finding insights and emotional moments
    insight_patterns = [
        r'(?:realized|discovered|learned|understood|found out) that[^.!?]*[.!?]',
        r'(?:most|biggest|key|critical|important)[^.!?]*(?:was|is|were)[^.!?]*[.!?]',
        r'(?:changed|transformed|improved)[^.!?]*[.!?]',
        r'(?:breakthrough|success|achievement)[^.!?]*[.!?]'
    ]
    
    # Extract all potential insights
    insights = []
    for pattern in insight_patterns:
        matches = re.finditer(pattern, transcript_text, re.IGNORECASE)
        for match in matches:
            insight = match.group(0).strip()
            if len(insight.split()) >= 5:  # Ensure substantial content
                insights.append(insight)
    
    # Score insights by emotional weight
    emotional_words = {
        'high': ['transformative', 'breakthrough', 'incredible', 'amazing'],
        'medium': ['important', 'significant', 'valuable', 'meaningful'],
        'low': ['interesting', 'helpful', 'useful', 'good']
    }
    
    scored_insights = []
    for insight in insights:
        score = 0
        for weight, words in emotional_words.items():
            if any(word in insight.lower() for word in words):
                score += {'high': 3, 'medium': 2, 'low': 1}[weight]
        scored_insights.append((score, insight))
    
    # Sort by score and select top 4-6 insights
    scored_insights.sort(reverse=True)
    selected = [insight for _, insight in scored_insights[:6]]
    
    # Format highlights with emotional framing
    formatted_highlights = []
    for insight in selected[:min(6, max(4, len(selected)))]:
        # Add emotional framing if not present
        if not any(word in insight.lower() for word in sum(emotional_words.values(), [])):
            if 'learned' in insight.lower():
                insight = f"In a powerful moment of clarity, {insight}"
            elif 'challenge' in insight.lower():
                insight = f"Through perseverance, {insight}"
            elif 'success' in insight.lower():
                insight = f"In a remarkable achievement, {insight}"
            else:
                insight = f"In a key insight, {insight}"
        
        formatted_highlights.append(insight)
    
    return formatted_highlights


def summarize_episode(style_profile: str, highlights: List[str]) -> str:
    """
    Create an overview paragraph using style profile elements.
    
    Args:
        style_profile (str): Raw style profile content
        highlights (List[str]): Extracted highlights
        
    Returns:
        str: 4-5 sentence episode summary
    """
    # Extract style elements
    voice_patterns = {
        'expert': r'(?:expert|authority|professional)[^.!?]*',
        'authentic': r'(?:authentic|genuine|real)[^.!?]*',
        'relatable': r'(?:relatable|approachable|friendly)[^.!?]*'
    }
    
    # Determine voice style
    voice_style = 'authentic'  # default
    for style, pattern in voice_patterns.items():
        if re.search(pattern, style_profile, re.IGNORECASE):
            voice_style = style
            break
    
    # Create framing based on voice style
    if voice_style == 'expert':
        opener = "In this illuminating episode, our guest shares invaluable insights"
        authority = "Drawing from years of experience"
    elif voice_style == 'authentic':
        opener = "In this heartfelt conversation, our guest opens up"
        authority = "Speaking from personal experience"
    else:  # relatable
        opener = "In this engaging discussion, our guest takes us through"
        authority = "Through their journey"
    
    # Extract key themes
    themes = re.findall(r'theme[s]?:([^.]*)', style_profile, re.IGNORECASE)
    theme_phrase = ""
    if themes:
        theme_list = [t.strip() for t in themes[0].split(',')]
        if theme_list:
            theme_phrase = f" about {', '.join(theme_list[:2])}"
    
    # Construct summary
    summary = f"{opener}{theme_phrase}. "
    summary += f"{authority}, they explore the challenges and triumphs that shaped their path. "
    
    # Add highlight-based content
    if highlights:
        key_highlight = highlights[0].lower()
        if 'learned' in key_highlight or 'discovered' in key_highlight:
            summary += "Their journey reveals powerful lessons about growth and resilience. "
        elif 'challenge' in key_highlight or 'obstacle' in key_highlight:
            summary += "Through facing significant challenges, they uncovered transformative insights. "
        else:
            summary += "Their story demonstrates the power of perseverance and vision. "
    
    summary += "This episode offers both practical wisdom and inspiring perspectives for listeners on their own journey."
    
    return summary


def craft_teaser(style_profile: str, highlights: List[str]) -> str:
    """
    Create an engaging hook-style teaser.
    
    Args:
        style_profile (str): Raw style profile content
        highlights (List[str]): Extracted highlights
        
    Returns:
        str: Single teaser sentence
    """
    # Extract emotional tone and themes
    emotional_tone = 'inspiring'  # default
    if 'tone:' in style_profile.lower():
        tone_line = re.search(r'tone:([^.]*)', style_profile, re.IGNORECASE)
        if tone_line:
            tone = tone_line.group(1).lower().strip()
            if 'challenge' in tone or 'struggle' in tone:
                emotional_tone = 'challenging'
            elif 'success' in tone or 'achievement' in tone:
                emotional_tone = 'triumphant'
            elif 'authentic' in tone or 'honest' in tone:
                emotional_tone = 'raw'
    
    # Create teaser based on emotional tone and highlights
    if emotional_tone == 'challenging':
        teaser = "What happens when you face your biggest fears and emerge stronger?"
    elif emotional_tone == 'triumphant':
        teaser = "Discover how one decision can transform challenge into extraordinary success."
    elif emotional_tone == 'raw':
        teaser = "An honest conversation about what it really takes to chase your dreams."
    else:  # inspiring
        teaser = "This episode reveals the unexpected path to finding your true purpose."
    
    # Customize based on highlights if available
    if highlights:
        main_highlight = highlights[0].lower()
        if 'learned' in main_highlight or 'discovered' in main_highlight:
            teaser = f"The surprising truth about {main_highlight.split('learned')[1].strip()}"
        elif 'biggest' in main_highlight or 'most important' in main_highlight:
            teaser = f"What happens when you {main_highlight.split('was')[1].strip()}"
    
    return teaser


def format_show_notes(teaser: str, summary: str, highlights: List[str]) -> str:
    """
    Format all components into final show notes.
    
    Args:
        teaser (str): Hook-style teaser
        summary (str): Episode summary
        highlights (List[str]): Key moments and insights
        
    Returns:
        str: Formatted show notes in markdown following required spec
    """
    # Build show notes structure
    show_notes = [
        "## 🎙️ Episode Teaser",
        "",
        f"> {teaser}",
        "",
        "---",
        "",
        "## 📝 Episode Summary",
        "",
        summary,
        "",
        "---",
        "",
        "## 🔑 Highlights & Takeaways",
        ""
    ]
    
    # Add highlights as bullet points
    for highlight in highlights:
        show_notes.append(f"- {highlight}")
    
    # Join with proper spacing and return
    return "\n".join(show_notes)


def generate(transcript_text: str, style_profile: str) -> str:
    """
    Generate podcast-style show notes from transcript and style profile.
    
    Args:
        transcript_text (str): Raw content from transcript_chunks.md
        style_profile (str): Raw content from style-profile.md
        
    Returns:
        str: Formatted show notes in markdown format
    """
    def count_words(text: str) -> int:
        """Count words in text, excluding markdown symbols."""
        # Remove markdown symbols and extra whitespace
        clean_text = re.sub(r'[#*_\->`🎙️📝🔑]', '', text)
        return len(clean_text.split())
    
    # Extract key highlights (limited to reduce word count)
    highlights = extract_highlights(transcript_text)[:4]  # Max 4 highlights
    
    # Create episode summary (keep it concise)
    summary = summarize_episode(style_profile, highlights)
    if count_words(summary) > 100:  # Limit summary length
        sentences = re.split(r'(?<=[.!?])\s+', summary)
        summary = ' '.join(sentences[:3]) # Keep first 3 sentences
    
    # Craft teaser hook
    teaser = craft_teaser(style_profile, highlights)
    
    # Format show notes
    show_notes = format_show_notes(teaser, summary, highlights)
    
    # Validate word count
    total_words = count_words(show_notes)
    if total_words > 500:
        # Trim highlights if needed
        while total_words > 500 and len(highlights) > 2:
            highlights.pop()
            show_notes = format_show_notes(teaser, summary, highlights)
            total_words = count_words(show_notes)
    
    # Ensure non-empty output
    if not show_notes.strip():
        raise ValueError("Failed to generate show notes: Output is empty")
    
    # Save to output directory
    output_dir = Path(__file__).parent.parent / "output" / "app3"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "output_show_notes.md"
    output_file.write_text(show_notes, encoding='utf-8')
    
    return show_notes
