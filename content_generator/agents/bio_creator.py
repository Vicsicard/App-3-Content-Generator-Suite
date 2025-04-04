"""
Bio Creator Agent

Generates tailored professional bios from transcripts and style profiles.
Creates distinct versions for personal websites, LinkedIn profiles, and
professional directories while maintaining consistent voice and authenticity.
"""

from typing import Dict, List, Tuple
import re
from pathlib import Path


def extract_professional_details(transcript_text: str) -> Dict[str, str]:
    """Extract key professional information from transcript."""
    details = {
        'current_role': '',
        'expertise': [],
        'background': [],
        'values': [],
        'impact_areas': [],
        'speaking_topics': [],
        'quotes': []  # Store actual quotes for authenticity
    }
    
    current_quote = []
    for line in transcript_text.split('\n'):
        if line.startswith('Speaker 1:'):
            content = line.replace('Speaker 1:', '').strip()
            
            # Collect quotes for authenticity
            if '"' in content:
                quote = re.search(r'"([^"]+)"', content)
                if quote:
                    details['quotes'].append(quote.group(1))
            
            # Extract role and expertise
            if any(word in content.lower() for word in ['i am', 'my role', 'i work as', 'i help']):
                if not details['current_role']:  # Take first mention only
                    details['current_role'] = content
            
            # Extract expertise areas
            if any(word in content.lower() for word in ['specialize', 'focus on', 'expertise']):
                details['expertise'].append(content)
            
            # Extract background avoiding generic phrases
            if any(word in content.lower() for word in ['background', 'experience', 'previously', 'before']):
                if not any(phrase in content.lower() for phrase in ['passionate about', 'driven', 'dedicated']):
                    details['background'].append(content)
            
            # Extract concrete values, not generic statements
            if any(word in content.lower() for word in ['believe', 'value', 'mission']):
                if len(content.split()) > 5:  # Avoid short, generic statements
                    details['values'].append(content)
            
            # Extract specific impact examples
            if any(word in content.lower() for word in ['impact', 'achieve', 'help', 'create']):
                if not any(phrase in content.lower() for phrase in ['passionate', 'dedicated', 'committed']):
                    details['impact_areas'].append(content)
            
            # Extract speaking topics with specificity
            if any(word in content.lower() for word in ['speak', 'teach', 'present', 'workshop']):
                if any(specific in content.lower() for specific in ['about', 'on', 'regarding']):
                    details['speaking_topics'].append(content)
    
    return details


def analyze_brand_voice(style_profile: str) -> Dict[str, str]:
    """
    Extract brand voice characteristics and tone.
    
    Args:
        style_profile (str): Raw style profile content
        
    Returns:
        Dict containing voice guidance
    """
    voice = {
        'tone': 'professional',  # professional, warm, formal
        'perspective': 'first-person',  # first-person, third-person
        'values': [],
        'themes': [],
        'relatability_markers': []
    }
    
    # Analyze style profile content
    lines = style_profile.split('\n')
    for line in lines:
        # Extract tone preferences
        if any(word in line.lower() for word in ['tone', 'voice', 'style']):
            if 'warm' in line.lower():
                voice['tone'] = 'warm'
            elif 'formal' in line.lower():
                voice['tone'] = 'formal'
        
        # Extract perspective preference
        if 'third person' in line.lower():
            voice['perspective'] = 'third-person'
        
        # Extract values and themes
        if any(word in line.lower() for word in ['value', 'believe', 'theme']):
            voice['values'].append(line.strip())
        
        # Extract relatability markers
        if any(word in line.lower() for word in ['connect', 'relate', 'resonate']):
            voice['relatability_markers'].append(line.strip())
    
    return voice


def format_website_bio(details: Dict[str, str], voice: Dict[str, str]) -> str:
    """Format bio for personal website (150-200 words)."""
    # Use specific role description
    role = details['current_role']
    if not role or len(role.split()) < 3:  # Ensure meaningful role description
        role = "helps leaders transform their stories into impact"
    
    # Find a meaningful quote for authenticity
    quote = next((q for q in details['quotes'] if len(q.split()) > 5), None)
    
    # Build narrative using concrete details
    parts = []
    
    # Opening with specific focus
    parts.append(f"[Speaker 1] {role}.")
    
    # Add background if available, otherwise skip
    if details['background']:
        background = details['background'][0]
        if len(background.split()) > 5:  # Only use substantial background
            parts.append(f"\n\nDrawing from {background.lower()}")
    
    # Add concrete value statement if available
    if details['values']:
        value = details['values'][0]
        if len(value.split()) > 5:
            parts.append(f"\n\n{value}")
    
    # Add impact with quote if available
    if quote:
        parts.append(f'\n\nAs they often say, "{quote}"')
    
    return "".join(parts)


def format_linkedin_bio(details: Dict[str, str], voice: Dict[str, str]) -> str:
    """Format bio for LinkedIn (250-300 words)."""
    parts = []
    
    # Current focus using specific language
    if details['expertise']:
        expertise = details['expertise'][0]
        parts.append(expertise)
    else:
        parts.append(details['current_role'])
    
    # Add unique background elements
    if len(details['background']) >= 2:
        background = details['background'][1]  # Use different background than website
        parts.append(f"\n\nBringing perspective from {background.lower()}")
    
    # Add specific impact examples
    if details['impact_areas']:
        impact = details['impact_areas'][0]
        if len(impact.split()) > 5:
            parts.append(f"\n\n{impact}")
    
    # Add collaboration focus with specific topics
    if details['speaking_topics']:
        topics = details['speaking_topics'][0]
        parts.append(f"\n\nCurrently exploring conversations around {topics.lower()}")
    
    return "".join(parts)


def format_directory_bio(details: Dict[str, str], voice: Dict[str, str]) -> str:
    """Format bio for professional directories (75-100 words)."""
    parts = []
    
    # Use specific expertise
    if details['expertise']:
        expertise = next((e for e in details['expertise'] if len(e.split()) > 3), None)
        if expertise:
            parts.append(f"[Speaker 1] {expertise}.")
    else:
        parts.append(f"[Speaker 1] {details['current_role']}.")
    
    # Add unique background element
    if details['background']:
        background = details['background'][-1]  # Use different background than other bios
        parts.append(f"\n\n{background}")
    
    # Add specific speaking topics
    if details['speaking_topics']:
        topics = details['speaking_topics'][-1]  # Use different topics than LinkedIn
        parts.append(f"\n\nAvailable for {topics.lower()}")
    
    return "".join(parts)


def generate(transcript_text: str, style_profile: str) -> str:
    """Generate tailored professional bios."""
    # Extract details and ensure we have minimum required content
    details = extract_professional_details(transcript_text)
    if not details['current_role'] and not details['expertise']:
        raise ValueError("Insufficient professional details found in transcript")
    
    # Analyze voice and ensure we have style guidance
    voice = analyze_brand_voice(style_profile)
    if not voice['values']:
        raise ValueError("No style guidance found in profile")
    
    # Generate unique bios
    website_bio = format_website_bio(details, voice)
    linkedin_bio = format_linkedin_bio(details, voice)
    directory_bio = format_directory_bio(details, voice)
    
    # Verify we don't have placeholder content
    if any(placeholder in website_bio.lower() for placeholder in ['[role]', '[expertise]', '[background]']):
        raise ValueError("Could not generate complete website bio - missing key information")
    
    # Format final output
    bios = [
        "## 🌐 Website Bio",
        website_bio,
        "",
        "---",
        "",
        "## 🔗 LinkedIn Bio",
        linkedin_bio,
        "",
        "---",
        "",
        "## 📇 Directory Bio",
        directory_bio
    ]
    
    # Save to correct output file
    output_dir = Path(__file__).parent.parent / "output" / "app3"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "output_bio.md"
    
    content = "\n".join(bios)
    output_file.write_text(content, encoding='utf-8')
    
    return content
