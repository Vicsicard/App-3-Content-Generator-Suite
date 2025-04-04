"""
Blog Generator Agent
Creates compelling blog articles in markdown format from narrative transcripts.

The agent analyzes the transcript content and applies the author's style profile
to generate engaging thought-leadership content.
"""

from typing import Dict, List, Tuple, Any
import re
from datetime import datetime
from collections import Counter
from pathlib import Path


def extract_style_signals(style_profile: str) -> Dict[str, List[str]]:
    """
    Extract key style elements from the style profile.
    
    Args:
        style_profile (str): Raw style profile content
        
    Returns:
        Dict containing structured style elements:
        - voice: Writing voice characteristics
        - themes: Key topics and themes
        - values: Core values and beliefs
        - emotional_tone: Emotional range and tone
        - relatability: Connection points with audience
    """
    # Initialize return structure
    signals = {
        'voice': [],
        'themes': [],
        'values': [],
        'emotional_tone': [],
        'relatability': []
    }
    
    # Split into lines and clean
    lines = [line.strip() for line in style_profile.split('\n') if line.strip()]
    
    # Track current section
    current_section = None
    
    # Common voice indicators
    voice_indicators = {
        'professional': ['formal', 'expert', 'authoritative'],
        'conversational': ['casual', 'friendly', 'approachable'],
        'authentic': ['genuine', 'honest', 'real'],
        'passionate': ['enthusiastic', 'energetic', 'dynamic']
    }
    
    # Common emotional tone indicators
    tone_indicators = {
        'positive': ['optimistic', 'upbeat', 'inspiring'],
        'balanced': ['measured', 'thoughtful', 'analytical'],
        'empathetic': ['understanding', 'compassionate', 'supportive'],
        'direct': ['straightforward', 'clear', 'frank']
    }
    
    for line in lines:
        # Check for section headers
        if ':' in line:
            key, value = [part.strip() for part in line.split(':', 1)]
            key = key.lower()
            
            # Process voice traits
            if 'voice' in key or 'tone' in key:
                signals['voice'].extend([
                    trait for indicator, traits in voice_indicators.items()
                    if indicator in value.lower()
                    for trait in traits
                ])
                signals['emotional_tone'].extend([
                    tone for indicator, tones in tone_indicators.items()
                    if indicator in value.lower()
                    for tone in tones
                ])
            
            # Process themes
            elif 'theme' in key or 'topic' in key:
                signals['themes'].extend([
                    theme.strip()
                    for theme in value.split(',')
                    if theme.strip()
                ])
            
            # Process values
            elif 'value' in key or 'belief' in key:
                signals['values'].extend([
                    val.strip()
                    for val in value.split(',')
                    if val.strip()
                ])
            
            # Process relatability
            elif 'audience' in key or 'reader' in key:
                signals['relatability'].extend([
                    point.strip()
                    for point in value.split(',')
                    if point.strip()
                ])
    
    # Clean up and deduplicate
    for key in signals:
        signals[key] = list(set(signals[key]))
        
    # Ensure at least one item in each category
    for key in signals:
        if not signals[key]:
            if key == 'voice':
                signals[key] = ['professional']
            elif key == 'emotional_tone':
                signals[key] = ['balanced']
            elif key == 'themes':
                signals[key] = ['expertise']
            elif key == 'values':
                signals[key] = ['authenticity']
            elif key == 'relatability':
                signals[key] = ['shared experience']
    
    return signals


def analyze_transcript(transcript_text: str) -> List[Dict[str, Any]]:
    """
    Analyze transcript for key moments and themes.
    
    Args:
        transcript_text (str): Raw transcript content
        
    Returns:
        List of dictionaries containing:
        - section: Section identifier (e.g., "Q1", "Background")
        - content: Raw text content
        - quotes: List of notable quotes
        - insights: Key ideas or takeaways
        - emotional_weight: Importance score (0-10)
        - tags: List of moment types (challenge, breakthrough, etc.)
    """
    # Initialize storage for analyzed chunks
    chunks = []
    
    # Pattern for section headers and quotes
    section_pattern = r'^##\s+(.+)$'
    quote_pattern = r'"([^"]+)"'
    
    # Emotional and pivotal moment indicators
    emotional_indicators = {
        'challenge': ['difficult', 'struggle', 'challenge', 'hard', 'obstacle'],
        'breakthrough': ['realized', 'discovered', 'breakthrough', 'finally', 'success'],
        'reflection': ['learned', 'understand', 'reflect', 'think about'],
        'achievement': ['accomplished', 'achieved', 'proud', 'milestone'],
        'transition': ['changed', 'shifted', 'moved', 'transformed']
    }
    
    # Split transcript into sections
    current_section = None
    current_content = []
    
    for line in transcript_text.split('\n'):
        # Check for new section
        section_match = re.match(section_pattern, line, re.MULTILINE)
        
        if section_match:
            # Save previous section if it exists
            if current_section and current_content:
                content_text = '\n'.join(current_content)
                
                # Extract quotes
                quotes = re.findall(quote_pattern, content_text)
                
                # Analyze emotional weight and tags
                emotional_weight = 0
                tags = set()
                
                for indicator_type, words in emotional_indicators.items():
                    for word in words:
                        if word.lower() in content_text.lower():
                            emotional_weight += 1
                            tags.add(indicator_type)
                
                # Extract key insights (sentences with important indicators)
                insights = []
                sentences = re.split(r'[.!?]+', content_text)
                for sentence in sentences:
                    sentence = sentence.strip()
                    # Look for insight indicators
                    if any(word in sentence.lower() for word in [
                        'because', 'realized', 'learned', 'important',
                        'key', 'critical', 'essential', 'discovered'
                    ]):
                        insights.append(sentence)
                
                chunks.append({
                    'section': current_section,
                    'content': content_text,
                    'quotes': quotes,
                    'insights': insights,
                    'emotional_weight': min(emotional_weight, 10),  # Cap at 10
                    'tags': list(tags)
                })
            
            # Start new section
            current_section = section_match.group(1)
            current_content = []
        else:
            if line.strip():
                current_content.append(line.strip())
    
    # Don't forget to add the last section
    if current_section and current_content:
        content_text = '\n'.join(current_content)
        quotes = re.findall(quote_pattern, content_text)
        
        emotional_weight = 0
        tags = set()
        for indicator_type, words in emotional_indicators.items():
            for word in words:
                if word.lower() in content_text.lower():
                    emotional_weight += 1
                    tags.add(indicator_type)
        
        insights = []
        sentences = re.split(r'[.!?]+', content_text)
        for sentence in sentences:
            sentence = sentence.strip()
            if any(word in sentence.lower() for word in [
                'because', 'realized', 'learned', 'important',
                'key', 'critical', 'essential', 'discovered'
            ]):
                insights.append(sentence)
        
        chunks.append({
            'section': current_section,
            'content': content_text,
            'quotes': quotes,
            'insights': insights,
            'emotional_weight': min(emotional_weight, 10),
            'tags': list(tags)
        })
    
    # Sort chunks by emotional weight
    chunks.sort(key=lambda x: x['emotional_weight'], reverse=True)
    
    return chunks


def identify_central_theme(transcript_data: List[Dict[str, Any]], 
                         style_data: Dict[str, List[str]]) -> Tuple[str, List[Dict[str, Any]]]:
    """
    Identify the most prominent theme that aligns with style profile.
    
    Args:
        transcript_data: List of analyzed transcript chunks
        style_data: Dictionary of style signals
        
    Returns:
        Tuple containing:
        - Central theme as a string
        - List of relevant content chunks for this theme
    """
    # Theme candidates from both sources
    style_themes = set(theme.lower() for theme in style_data['themes'])
    style_values = set(value.lower() for value in style_data['values'])
    
    # Extract potential themes from transcript
    transcript_themes = []
    theme_chunks = {}  # Map themes to relevant chunks
    
    # Common theme words that might appear in content
    theme_indicators = {
        'leadership': ['lead', 'guide', 'direct', 'inspire'],
        'innovation': ['new', 'create', 'develop', 'change'],
        'growth': ['learn', 'improve', 'grow', 'progress'],
        'challenge': ['obstacle', 'difficult', 'overcome'],
        'success': ['achieve', 'accomplish', 'win'],
        'transformation': ['change', 'evolve', 'transform'],
        'expertise': ['know', 'understand', 'master'],
        'authenticity': ['genuine', 'real', 'true'],
        'impact': ['effect', 'influence', 'difference']
    }
    
    # Analyze each chunk for themes
    for chunk in transcript_data:
        chunk_text = chunk['content'].lower()
        chunk_insights = ' '.join(chunk['insights']).lower()
        
        # Track which themes appear in this chunk
        chunk_themes = set()
        
        # Look for theme indicators in content
        for theme, indicators in theme_indicators.items():
            if any(indicator in chunk_text for indicator in indicators):
                chunk_themes.add(theme)
                transcript_themes.append(theme)
                
                # Store chunk for this theme
                if theme not in theme_chunks:
                    theme_chunks[theme] = []
                theme_chunks[theme].append(chunk)
        
        # Add any style themes that appear directly in content
        for theme in style_themes:
            if theme in chunk_text or theme in chunk_insights:
                chunk_themes.add(theme)
                transcript_themes.append(theme)
                if theme not in theme_chunks:
                    theme_chunks[theme] = []
                theme_chunks[theme].append(chunk)
    
    # Count theme frequencies
    theme_counter = Counter(transcript_themes)
    
    # Score themes based on:
    # 1. Frequency in transcript
    # 2. Presence in style profile
    # 3. Emotional weight of associated chunks
    theme_scores = {}
    
    for theme, count in theme_counter.items():
        # Base score from frequency
        score = count * 10
        
        # Bonus if theme appears in style profile
        if theme in style_themes:
            score += 30
        if theme in style_values:
            score += 20
            
        # Bonus for emotional weight of chunks
        if theme in theme_chunks:
            total_weight = sum(chunk['emotional_weight'] 
                             for chunk in theme_chunks[theme])
            score += total_weight * 5
            
        theme_scores[theme] = score
    
    # Select highest scoring theme
    if theme_scores:
        central_theme = max(theme_scores.items(), key=lambda x: x[1])[0]
    else:
        # Fallback to first style theme if no themes detected
        central_theme = next(iter(style_themes), 'personal growth')
    
    # Get relevant chunks for the chosen theme
    relevant_chunks = theme_chunks.get(central_theme, [])
    
    # Sort chunks by emotional weight
    relevant_chunks.sort(key=lambda x: x['emotional_weight'], reverse=True)
    
    # Capitalize theme words for title
    central_theme = ' '.join(word.capitalize() for word in central_theme.split())
    
    return central_theme, relevant_chunks


def format_blog_article(theme: str, content_chunks: List[Dict], 
                       style: Dict[str, List[str]]) -> str:
    """
    Format transcript insights into a polished blog article.
    
    Args:
        theme: Central theme for the article
        content_chunks: List of relevant content chunks
        style: Style signals dictionary
        
    Returns:
        Formatted blog article in markdown
    """
    def count_words(text: str) -> int:
        """Count words in text, excluding markdown symbols."""
        # Remove markdown symbols and extra whitespace
        clean_text = re.sub(r'[#*_\->`]', '', text)
        words = clean_text.split()
        return len(words)
    
    # Ensure we have enough content
    if len(content_chunks) < 3:
        # Duplicate last chunk if needed
        while len(content_chunks) < 3:
            content_chunks.append(content_chunks[-1])
    
    # Get style characteristics
    voice = style['voice'][0] if style['voice'] else 'professional'
    tone = style['emotional_tone'][0] if style['emotional_tone'] else 'balanced'
    
    # Format title based on theme
    if 'challenge' in theme.lower():
        title = f"Overcoming {theme}: A Journey of Growth"
    elif 'success' in theme.lower():
        title = f"Achieving {theme}: Lessons Learned"
    elif 'innovation' in theme.lower():
        title = f"Revolutionizing Through {theme}"
    else:
        title = f"The Power of {theme}: A Personal Perspective"
    
    # Build introduction
    intro_chunk = content_chunks[0]
    intro_quote = intro_chunk['quotes'][0] if intro_chunk['quotes'] else None
    intro_insight = intro_chunk['insights'][0] if intro_chunk['insights'] else None
    
    intro = f"## Introduction\n\n"
    if intro_quote:
        intro += f"_{intro_quote}_ "
    if intro_insight:
        intro += intro_insight
    else:
        intro += f"The journey through {theme.lower()} is one that transforms us in unexpected ways. "
    intro += f"\n\nIn this article, we'll explore the profound impact of {theme.lower()} "
    intro += "and the lessons that emerge from embracing this challenge.\n"
    
    # Build main sections
    sections = []
    section_titles = {
        'challenge': ["The Initial Challenge", "Breaking Through Barriers", "Embracing Growth"],
        'success': ["The Foundation", "Key Breakthroughs", "Sustaining Success"],
        'innovation': ["Identifying Opportunities", "Creating Solutions", "Driving Change"],
        'growth': ["Understanding the Journey", "Key Milestones", "Transformative Insights"]
    }
    
    # Select appropriate section titles
    title_set = next((titles for key, titles in section_titles.items() 
                     if key in theme.lower()), 
                    ["The Beginning", "The Journey", "The Transformation"])
    
    # Format each section
    for i, (chunk, section_title) in enumerate(zip(content_chunks[:3], title_set)):
        section = f"## Section {i+1}: {section_title}\n\n"
        
        # Add section content
        if chunk['insights']:
            section += chunk['insights'][0] + " "
        
        # Add supporting quote if available
        if chunk['quotes']:
            section += f"\n\n> _{chunk['quotes'][0]}_\n\n"
        
        # Add reflection based on emotional tags
        if chunk['tags']:
            if 'breakthrough' in chunk['tags']:
                section += "\nThis breakthrough moment illustrates the transformative power of perseverance. "
            elif 'challenge' in chunk['tags']:
                section += "\nFacing this challenge head-on revealed important truths about resilience. "
            elif 'reflection' in chunk['tags']:
                section += "\nThis realization opened new perspectives on growth and possibility. "
        
        sections.append(section)
    
    # Build conclusion
    conclusion = "## Conclusion\n\n"
    conclusion += f"The journey through {theme.lower()} teaches us that growth comes "
    conclusion += "not just from success, but from every step along the way. "
    
    # Add final quote if available
    final_quotes = [q for chunk in content_chunks for q in chunk['quotes']]
    if final_quotes:
        conclusion += f"\n\n> _{final_quotes[-1]}_"
    
    # Combine all parts
    article_parts = [
        f"# {title}",
        "*Inspired by real experiences and insights*",
        "---",
        intro,
        "---",
        *sections,
        "---",
        conclusion
    ]
    
    # Join with proper spacing
    article = "\n\n".join(article_parts)
    
    # Check word count and adjust if needed
    word_count = count_words(article)
    while word_count < 600:
        # Add more insights from chunks if available
        for chunk in content_chunks:
            if len(chunk['insights']) > 1:
                for section in sections:
                    if chunk['insights'][0] in section:
                        section += " " + chunk['insights'][1]
                        break
        # Recombine and recount
        article = "\n\n".join(article_parts)
        word_count = count_words(article)
        if word_count >= 600:
            break
    
    while word_count > 900:
        # Trim insights while preserving quotes
        for i, section in enumerate(sections):
            sentences = re.split(r'(?<=[.!?])\s+', section)
            if len(sentences) > 3 and not sentences[-1].startswith('>'):
                sections[i] = ' '.join(sentences[:-1])
        # Recombine and recount
        article = "\n\n".join(article_parts)
        word_count = count_words(article)
        if word_count <= 900:
            break
    
    # Save to output directory
    output_dir = Path(__file__).parent.parent / "output" / "app3"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "output_blog.md"
    output_file.write_text(article, encoding='utf-8')
    
    return article


def generate(transcript_text: str, style_profile: str) -> str:
    """
    Generate a blog article from transcript content using the author's style profile.

    Args:
        transcript_text (str): Raw content of transcript_chunks.md file
            Contains the narrative text that will form the basis of the blog article.
            Expected to be in markdown format with potential section headers.

        style_profile (str): Raw content of style-profile.md file
            Contains the author's writing style preferences, tone, and voice guidelines.
            Used to ensure the generated content matches the author's style.

    Returns:
        str: A complete blog article in markdown format.
            Includes title, sections, and proper markdown formatting.

    Process:
    1. Extract style signals from style profile
    2. Analyze transcript for pivotal moments and themes
    3. Select central theme and supporting content
    4. Format article in markdown with consistent voice
    """
    # 1. Extract style signals
    style = extract_style_signals(style_profile)
    
    # 2. Analyze transcript chunks
    analyzed_chunks = analyze_transcript(transcript_text)
    
    # 3. Identify central theme and relevant content
    theme, content_chunks = identify_central_theme(analyzed_chunks, style)
    
    # 4. Format final article
    article = format_blog_article(theme, content_chunks, style)
    
    return article
