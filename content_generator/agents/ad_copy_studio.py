"""
Ad Copy Studio Agent

Generates concise, emotionally resonant ad copy for marketing and positioning.
Creates various formats including intros, CTAs, headlines, and promo captions
while maintaining consistent voice and emotional impact.
"""

from typing import Dict, List, Tuple
import re
from pathlib import Path


def extract_key_messaging(style_profile: str) -> Dict[str, List[str]]:
    """
    Extract key message pillars and emotional resonance markers.
    
    Returns:
        Dict containing message pillars, themes, and emotional markers
    """
    messaging = {
        'pillars': [],    # Core message themes (e.g., courage, transformation)
        'emotions': [],   # Emotional resonance markers
        'voice': '',      # Voice characteristics
        'keywords': []    # Key terms to weave in
    }
    
    for line in style_profile.split('\n'):
        # Extract message pillars from Theme section
        if 'Theme:' in line or 'theme:' in line:
            themes = re.findall(r'[\w\s]+(?:,|$)', line.split(':', 1)[1])
            messaging['pillars'].extend(t.strip() for t in themes if len(t.strip()) > 0)
        
        # Extract emotional markers from Emotional Tone
        if 'Emotion' in line or 'emotion' in line:
            emotions = re.findall(r'[\w\s]+(?:,|$)', line.split(':', 1)[1])
            messaging['emotions'].extend(e.strip() for e in emotions if len(e.strip()) > 0)
        
        # Extract voice characteristics
        if 'Voice:' in line or 'voice:' in line:
            messaging['voice'] = line.split(':', 1)[1].strip()
        
        # Extract keywords from style markers
        if any(marker in line.lower() for marker in ['key term', 'keyword', 'phrase']):
            words = re.findall(r'[\w\s]+(?:,|$)', line.split(':', 1)[1])
            messaging['keywords'].extend(w.strip() for w in words if len(w.strip()) > 0)
    
    # Limit to top 3 pillars
    messaging['pillars'] = messaging['pillars'][:3]
    
    return messaging


def extract_resonant_quotes(transcript_text: str) -> List[Dict[str, str]]:
    """
    Extract and process emotionally powerful quotes.
    
    Returns:
        List of dicts containing original and shortened quotes
    """
    quotes = []
    current_quote = []
    
    for line in transcript_text.split('\n'):
        if line.startswith('Speaker 1:'):
            content = line.replace('Speaker 1:', '').strip()
            
            # Look for quoted content
            if '"' in content:
                quote_match = re.search(r'"([^"]+)"', content)
                if quote_match:
                    quote = quote_match.group(1)
                    
                    # Score quote for emotional impact
                    impact_words = ['transform', 'change', 'realize', 'truth', 'power', 'voice']
                    emotion_words = ['feel', 'believe', 'fear', 'hope', 'dream', 'trust']
                    
                    impact_score = sum(1 for word in impact_words if word.lower() in quote.lower())
                    emotion_score = sum(1 for word in emotion_words if word.lower() in quote.lower())
                    total_score = impact_score + emotion_score
                    
                    if total_score > 0:  # Only keep impactful quotes
                        # Create shortened version
                        shortened = quote
                        if len(shortened.split()) > 12:  # Shorten long quotes
                            words = shortened.split()
                            if len(words) > 15:
                                # Keep first and last parts for context
                                shortened = ' '.join(words[:8]) + '...' + ' '.join(words[-4:])
                        
                        quotes.append({
                            'original': quote,
                            'shortened': shortened,
                            'impact_score': total_score
                        })
    
    # Sort by impact and return top 2-3 quotes
    quotes.sort(key=lambda x: x['impact_score'], reverse=True)
    return quotes[:3]


def validate_copy(variants: Dict[str, str]) -> None:
    """
    Validate copy against strict content rules.
    Raises ValueError if rules are violated.
    """
    # Check for placeholders
    placeholder_patterns = [
        r'\[.*?\]',           # [text]
        r'<.*?>',            # <text>
        r'INSERT|REPLACE',    # Common placeholder words
        r'YOUR_|MY_|OUR_'    # Template variables
    ]
    
    # Check for AI marketing clichés
    marketing_cliches = [
        'unlock your potential',
        'take your * to the next level',
        'transform your life',
        'game-changing',
        'revolutionary',
        'breakthrough',
        'innovative solution',
        'empower yourself'
    ]
    
    for section, content in variants.items():
        # Check for empty content
        if not content.strip():
            raise ValueError(f"{section} cannot be empty")
            
        # Check for placeholders
        for pattern in placeholder_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                raise ValueError(f"Placeholder found in {section}: {content}")
        
        # Check for marketing clichés
        for cliche in marketing_cliches:
            if cliche.replace('*', r'\w+') in content.lower():
                raise ValueError(f"Marketing cliché found in {section}: {cliche}")
        
        # Check word count limits
        words = content.split()
        if section == 'headline' and len(words) > 12:
            raise ValueError(f"Headline too long ({len(words)} words): {content}")
        elif len(words) > 40:
            raise ValueError(f"{section} too long ({len(words)} words): {content}")


def create_copy_variants(messaging: Dict[str, List[str]], quotes: List[Dict[str, str]]) -> Dict[str, str]:
    """
    Create ad copy variants using messaging and quotes.
    """
    variants = {
        'intro': '',
        'cta': '',
        'headline': '',
        'subheadline': '',
        'promo': ''
    }
    
    pillars = messaging['pillars']
    emotions = messaging['emotions']
    keywords = messaging['keywords']
    voice = messaging['voice']
    
    # Create headline from shortened quote or key message
    if quotes:
        quote = quotes[0]['shortened']
        if len(quote.split()) <= 12:
            variants['headline'] = quote.rstrip('.')
        else:
            # Use first pillar for punchy headline
            variants['headline'] = f"{pillars[0].capitalize()}. Unfiltered." if pillars else "Your Story. Unfiltered."
    
    # Create subheadline with transformation arc
    if len(pillars) > 1:
        variants['subheadline'] = f"From {pillars[1]} to {emotions[0] if emotions else 'impact'}"
    
    # Create intro using voice style and pillar
    if quotes and len(quotes) > 1:
        # Use second best quote for intro if it's concise
        intro_quote = quotes[1]['shortened']
        if len(intro_quote.split()) <= 40:
            variants['intro'] = intro_quote
        else:
            variants['intro'] = f"Bringing {pillars[0]} to life through authentic storytelling"
    
    # Create CTA with active voice
    if keywords:
        action = next((k for k in keywords if k.endswith('ing')), 'sharing')
        variants['cta'] = f"Start {action} your story today"
    else:
        variants['cta'] = "Let's craft your story together"
    
    # Create promo with emotional resonance
    if emotions and quotes:
        variants['promo'] = f"{emotions[0].capitalize()} meets authenticity. This is your moment."
    
    # Validate against content rules
    validate_copy(variants)
    
    return variants


def generate(transcript_text: str, style_profile: str) -> str:
    """
    Generate marketing ad copy variants.
    """
    # Extract messaging and quotes
    messaging = extract_key_messaging(style_profile)
    quotes = extract_resonant_quotes(transcript_text)
    
    # Generate and validate copy variants
    variants = create_copy_variants(messaging, quotes)
    
    # Format output with exact markdown
    copy = [
        "## ✨ One-Sentence Intro",
        variants['intro'],
        "",
        "## 🔁 Call to Action",
        variants['cta'],
        "",
        "## 🧠 Headline",
        variants['headline'],
        "",
        "## 💡 Subheadline",
        variants['subheadline'],
        "",
        "## 🎯 Promo Caption",
        variants['promo']
    ]
    
    # Save to output file
    output_dir = Path(__file__).parent.parent / "output" / "app3"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "output_ad_copy.md"
    
    content = "\n".join(copy)
    output_file.write_text(content, encoding='utf-8')
    
    return content


"""
Ad Copy Studio Agent

Creates compelling ad copy from narrative content.
"""

from typing import Dict, List, Any
from pathlib import Path
from .base_agent import ContentAgent
from content_generator.utils.content_writer import format_markdown_section


class AdCopyStudioAgent(ContentAgent):
    """Ad copy studio agent that creates advertising content."""
    
    def generate(self) -> str:
        """Generate ad copy using transcript and style profile."""
        # Extract selling points and style data
        selling_points = self._extract_selling_points()
        style_data = self._parse_style_profile()
        
        # Generate ad sections
        headlines = self._generate_headlines(selling_points, style_data)
        body_copy = self._generate_body_copy(selling_points, style_data)
        cta = self._generate_cta(style_data)
        
        # Combine all sections
        ad_copy = [
            "# Ad Copy Content\n",
            headlines,
            body_copy,
            cta
        ]
        
        return "\n".join(ad_copy)
        
    def _extract_selling_points(self) -> List[Dict[str, str]]:
        """Extract key selling points from transcript."""
        points = []
        current_point = []
        
        for line in self.transcript.split('\n'):
            if line.startswith('Speaker 2:'):
                if current_point:
                    points.append({
                        'benefit': current_point[0][:50],
                        'details': ' '.join(current_point)
                    })
                    current_point = []
                current_point.append(line.replace('Speaker 2:', '').strip())
            elif current_point:
                current_point.append(line.strip())
                
        # Add final point
        if current_point:
            points.append({
                'benefit': current_point[0][:50],
                'details': ' '.join(current_point)
            })
            
        return points[:3]  # Return top 3 selling points
        
    def _parse_style_profile(self) -> Dict[str, List[str]]:
        """Parse style profile into structured data."""
        style_data = {
            'themes': [],
            'values': [],
            'tone': []
        }
        current_section = None
        
        for line in self.style_profile.split('\n'):
            if line.startswith('## '):
                current_section = line[3:].lower().strip(':')
            elif line.startswith('- ') and current_section in style_data:
                style_data[current_section].append(line[2:])
                
        return style_data
        
    def _generate_headlines(self, points: List[Dict[str, str]], style: Dict[str, List[str]]) -> str:
        """Generate ad headlines."""
        theme = style['themes'][0] if style['themes'] else 'Excellence'
        headlines = ["## Headlines\n"]
        
        for point in points:
            headlines.extend([
                f"### 🎯 Transform Your {theme} Today!\n",
                f"Discover how to {point['benefit'].lower()}...\n"
            ])
            
        return "\n".join(headlines)
        
    def _generate_body_copy(self, points: List[Dict[str, str]], style: Dict[str, List[str]]) -> str:
        """Generate ad body copy."""
        body = ["## Body Copy\n"]
        
        for point in points:
            body.extend([
                "### Key Benefit\n",
                f"{point['details']}\n"
            ])
            
        return "\n".join(body)
        
    def _generate_cta(self, style: Dict[str, List[str]]) -> str:
        """Generate call-to-action copy."""
        value = style['values'][0] if style['values'] else 'success'
        cta = [
            "## Call to Action\n",
            f"Ready to achieve {value}?",
            "Click now to get started!\n",
            "Limited time offer - Don't miss out! 🚀\n"
        ]
        return "\n".join(cta)
