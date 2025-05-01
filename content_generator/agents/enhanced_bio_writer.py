"""Enhanced Bio Writer Agent for App 3.

This enhanced bio writer creates authentic, personalized bio content by:
1. Directly incorporating the client's actual language from transcript chunks
2. Utilizing the voice, themes, and values analysis from the style profile
3. Preserving the client's unique expressions and storytelling patterns
"""

from pathlib import Path
import re
from typing import Dict, List, Tuple
import logging

from .base_agent import ContentAgent
from ..database.content_manager import content_manager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnhancedBioWriter(ContentAgent):
    """Creates authentic bio content using the client's actual language."""
    
    def __init__(self, input_dir: str = 'input'):
        """Initialize enhanced bio writer.
        
        Args:
            input_dir: Directory containing input files
        """
        super().__init__()
        self.input_dir = Path(input_dir)
    
    def generate(self, transcript: str = None, style_profile: str = None) -> Dict:
        """Generate authentic bio content from transcript and style profile.
        
        Args:
            transcript: Content from transcript_chunks.md
            style_profile: Content from style-profile.md
            
        Returns:
            Dict containing the saved content record
        """
        # Load input files if not provided
        if transcript is None or style_profile is None:
            transcript_path = self.input_dir / 'transcript_chunks.md'
            style_path = self.input_dir / 'style-profile.md'

            transcript = transcript_path.read_text() if transcript_path.exists() else ""
            style_profile = style_path.read_text() if style_path.exists() else ""
        
        # Extract voice fingerprint and client language patterns
        voice_profile = self._extract_voice_profile(style_profile)
        chunks = self._parse_transcript_chunks(transcript)
        
        # Find pivotal moments, insights, and personal expressions
        pivotal_moments = self._extract_pivotal_moments(chunks)
        key_insights = self._extract_key_insights(chunks)
        expertise_statements = self._extract_expertise_statements(chunks)
        
        # Generate bio sections using authentic language
        bio_content = self._generate_authentic_bio(
            voice_profile,
            pivotal_moments,
            key_insights, 
            expertise_statements
        )
        
        # Save to Supabase
        return content_manager.save_content(
            name='bio',
            content=bio_content
        )
    
    def _extract_voice_profile(self, style_profile: str) -> Dict:
        """Extract detailed voice profile from style profile.
        
        Args:
            style_profile: Content from style-profile.md
            
        Returns:
            Dict containing voice characteristics and themes
        """
        profile = {
            'voice': [],
            'themes': [],
            'values': [],
            'emotional_tone': {},
            'relatability': {}
        }
        
        current_section = None
        for line in style_profile.split('\n'):
            # Handle section headers
            if line.startswith('## '):
                section_name = line[3:].lower().strip(':')
                current_section = section_name
                continue
                
            # Handle list items in known sections
            if line.startswith('- ') and current_section in profile:
                if isinstance(profile[current_section], list):
                    profile[current_section].append(line[2:].strip())
            
            # Handle emotional tone and relatability scores
            if current_section == 'emotional_tone' and ':' in line:
                key, value = line.split(':', 1)
                if key.strip() and value.strip():
                    try:
                        profile['emotional_tone'][key.strip()] = float(value.strip())
                    except ValueError:
                        profile['emotional_tone'][key.strip()] = value.strip()
                        
            if current_section == 'relatability' and ':' in line:
                key, value = line.split(':', 1)
                if key.strip() and value.strip():
                    try:
                        profile['relatability'][key.strip()] = float(value.strip())
                    except ValueError:
                        profile['relatability'][key.strip()] = value.strip()
        
        return profile
    
    def _parse_transcript_chunks(self, transcript: str) -> List[Dict]:
        """Parse transcript into structured chunks with metadata.
        
        Args:
            transcript: Content from transcript_chunks.md
            
        Returns:
            List of structured chunk dictionaries
        """
        chunks = []
        current_chunk = None
        
        for line in transcript.split('\n'):
            # New chunk marker
            if line.startswith('## [Chunk'):
                if current_chunk and 'content' in current_chunk:
                    chunks.append(current_chunk)
                
                # Extract chunk number and initialize new chunk
                chunk_match = re.search(r'## \[Chunk (\d+)\]', line)
                chunk_num = int(chunk_match.group(1)) if chunk_match else len(chunks) + 1
                
                current_chunk = {
                    'number': chunk_num,
                    'timestamp': None,
                    'content': None
                }
                
            # Timestamp line
            elif line.startswith('**Timestamp'):
                if current_chunk:
                    timestamp_match = re.search(r'\*\*Timestamp\*\*: (.*)', line)
                    if timestamp_match:
                        current_chunk['timestamp'] = timestamp_match.group(1).strip()
                        
            # Speaker 2 content (the client)
            elif line.startswith('> Speaker 2:'):
                if current_chunk:
                    content = line.replace('> Speaker 2:', '').strip()
                    current_chunk['content'] = content
        
        # Add the last chunk if exists
        if current_chunk and 'content' in current_chunk:
            chunks.append(current_chunk)
            
        return chunks
    
    def _extract_pivotal_moments(self, chunks: List[Dict]) -> List[Dict]:
        """Extract pivotal moments from transcript chunks.
        
        These are statements about transformative experiences,
        realizations, or turning points in the client's journey.
        
        Args:
            chunks: List of structured transcript chunks
            
        Returns:
            List of chunks containing pivotal moments
        """
        pivotal_markers = [
            'realized', 'turning point', 'changed', 'transformed',
            'shift', 'moment', 'when i', 'started to', 'began to',
            'discovered', 'learned'
        ]
        
        return [
            chunk for chunk in chunks 
            if chunk.get('content') and any(marker in chunk['content'].lower() for marker in pivotal_markers)
        ]
    
    def _extract_key_insights(self, chunks: List[Dict]) -> List[Dict]:
        """Extract key insights from transcript chunks.
        
        These are statements about learnings, beliefs, or 
        philosophies that define the client's approach.
        
        Args:
            chunks: List of structured transcript chunks
            
        Returns:
            List of chunks containing key insights
        """
        insight_markers = [
            'believe', 'understand', 'know that', 'learned that',
            'realized that', 'insight', 'philosophy', 'approach',
            'think that', 'found that', 'discovered that'
        ]
        
        return [
            chunk for chunk in chunks 
            if chunk.get('content') and any(marker in chunk['content'].lower() for marker in insight_markers)
        ]
    
    def _extract_expertise_statements(self, chunks: List[Dict]) -> List[Dict]:
        """Extract expertise statements from transcript chunks.
        
        These are statements about the client's skills, expertise,
        or professional focus areas.
        
        Args:
            chunks: List of structured transcript chunks
            
        Returns:
            List of chunks containing expertise statements
        """
        expertise_markers = [
            'specialize', 'expert', 'focus on', 'skilled', 'experience',
            'help people', 'help clients', 'approach to', 'methodology',
            'passion', 'dedicated to', 'committed to'
        ]
        
        return [
            chunk for chunk in chunks 
            if chunk.get('content') and any(marker in chunk['content'].lower() for marker in expertise_markers)
        ]
    
    def _generate_authentic_bio(
        self, 
        voice_profile: Dict, 
        pivotal_moments: List[Dict],
        key_insights: List[Dict],
        expertise_statements: List[Dict]
    ) -> str:
        """Generate authentic bio using the client's actual language.
        
        Args:
            voice_profile: Voice characteristics from style profile
            pivotal_moments: List of pivotal moment chunks
            key_insights: List of key insight chunks
            expertise_statements: List of expertise statement chunks
            
        Returns:
            Generated bio content as markdown string
        """
        # Initialize bio sections
        bio_sections = []
        
        # Add title
        bio_sections.append("# Professional Biography\n")
        
        # Generate introduction using the client's actual language
        intro = self._generate_introduction(
            voice_profile, 
            pivotal_moments, 
            expertise_statements
        )
        bio_sections.append(intro)
        
        # Generate journey/story section using pivotal moments
        journey = self._generate_journey_section(
            voice_profile, 
            pivotal_moments
        )
        bio_sections.append(journey)
        
        # Generate approach/philosophy section using key insights
        approach = self._generate_approach_section(
            voice_profile, 
            key_insights
        )
        bio_sections.append(approach)
        
        # Generate expertise section
        expertise = self._generate_expertise_section(
            voice_profile, 
            expertise_statements
        )
        bio_sections.append(expertise)
        
        # Generate closing section
        closing = self._generate_closing_section(
            voice_profile, 
            key_insights
        )
        bio_sections.append(closing)
        
        # Combine all sections with proper spacing
        return "\n\n".join(bio_sections)
    
    def _generate_introduction(
        self, 
        voice_profile: Dict, 
        pivotal_moments: List[Dict],
        expertise_statements: List[Dict]
    ) -> str:
        """Generate authentic introduction section.
        
        Args:
            voice_profile: Voice characteristics from style profile
            pivotal_moments: List of pivotal moment chunks
            expertise_statements: List of expertise statement chunks
            
        Returns:
            Introduction section as markdown string
        """
        intro_parts = ["## Introduction\n"]
        
        # Start with a direct statement of expertise if available
        if expertise_statements:
            # Use the most concise expertise statement for the intro
            sorted_statements = sorted(
                expertise_statements, 
                key=lambda x: len(x.get('content', ''))
            )
            
            # Get the shortest statement that's still substantial
            expertise_statement = next(
                (s for s in sorted_statements if len(s.get('content', '')) > 30),
                sorted_statements[0] if sorted_statements else None
            )
            
            if expertise_statement:
                intro_parts.append(expertise_statement['content'])
        
        # Add a pivotal moment if available
        if pivotal_moments:
            # Find a pivotal moment that mentions journey beginnings
            journey_beginnings = [
                m for m in pivotal_moments 
                if any(word in m.get('content', '').lower() for word in ['started', 'began', 'journey', 'path'])
            ]
            
            if journey_beginnings:
                # Use the first journey beginning statement
                intro_parts.append(journey_beginnings[0]['content'])
            else:
                # Use the first pivotal moment
                intro_parts.append(pivotal_moments[0]['content'])
        
        # Incorporate voice characteristics for authentic tone
        if voice_profile.get('voice'):
            voice_traits = voice_profile['voice'][:2]  # Use top 2 voice traits
            
            # Create connecting statement based on voice traits
            if 'authentic' in ' '.join(voice_traits).lower():
                connector = "I believe authenticity is the foundation of meaningful connection and impact."
            elif 'passionate' in ' '.join(voice_traits).lower():
                connector = "I'm passionate about creating genuine impact through this work."
            elif 'professional' in ' '.join(voice_traits).lower():
                connector = "My professional approach is built on a foundation of expertise and genuine connection."
            else:
                connector = "My work is centered around creating meaningful connections and lasting impact."
                
            intro_parts.append(connector)
        
        # Join all parts with proper spacing
        return "\n\n".join(intro_parts)
    
    def _generate_journey_section(
        self, 
        voice_profile: Dict, 
        pivotal_moments: List[Dict]
    ) -> str:
        """Generate journey/story section using pivotal moments.
        
        Args:
            voice_profile: Voice characteristics from style profile
            pivotal_moments: List of pivotal moment chunks
            
        Returns:
            Journey section as markdown string
        """
        # Get themes to incorporate
        themes = voice_profile.get('themes', [])
        theme_words = ' '.join(themes).lower()
        
        # Determine section title based on themes
        if 'journey' in theme_words:
            section_title = "## My Journey"
        elif 'story' in theme_words:
            section_title = "## My Story"
        elif 'growth' in theme_words:
            section_title = "## My Growth Path"
        elif 'transformation' in theme_words:
            section_title = "## My Transformation"
        else:
            section_title = "## My Professional Journey"
        
        journey_parts = [section_title + "\n"]
        
        # Select up to 3 pivotal moments to include
        selected_moments = pivotal_moments[:3] if len(pivotal_moments) >= 3 else pivotal_moments
        
        # Add each pivotal moment as a paragraph
        for moment in selected_moments:
            journey_parts.append(moment['content'])
        
        # If we have voice traits about personal journey, add them
        journey_related_voice = [
            trait for trait in voice_profile.get('voice', [])
            if any(word in trait.lower() for word in ['story', 'journey', 'path', 'growth', 'evolution'])
        ]
        
        if journey_related_voice and len(journey_parts) < 5:
            connecting_statement = f"This journey has shaped my {journey_related_voice[0].lower()} approach to my work."
            journey_parts.append(connecting_statement)
        
        # Join all parts with proper spacing
        return "\n\n".join(journey_parts)
    
    def _generate_approach_section(
        self, 
        voice_profile: Dict, 
        key_insights: List[Dict]
    ) -> str:
        """Generate approach/philosophy section using key insights.
        
        Args:
            voice_profile: Voice characteristics from style profile
            key_insights: List of key insight chunks
            
        Returns:
            Approach section as markdown string
        """
        # Get values to incorporate
        values = voice_profile.get('values', [])
        value_words = ' '.join(values).lower()
        
        # Determine section title based on values
        if 'philosophy' in value_words:
            section_title = "## My Philosophy"
        elif 'approach' in value_words:
            section_title = "## My Approach"
        elif 'belief' in value_words or 'believe' in value_words:
            section_title = "## My Core Beliefs"
        else:
            section_title = "## My Professional Philosophy"
        
        approach_parts = [section_title + "\n"]
        
        # Select up to 3 key insights to include
        selected_insights = key_insights[:3] if len(key_insights) >= 3 else key_insights
        
        # Add each key insight as a paragraph
        for insight in selected_insights:
            approach_parts.append(insight['content'])
        
        # Join all parts with proper spacing
        return "\n\n".join(approach_parts)
    
    def _generate_expertise_section(
        self, 
        voice_profile: Dict, 
        expertise_statements: List[Dict]
    ) -> str:
        """Generate expertise section.
        
        Args:
            voice_profile: Voice characteristics from style profile
            expertise_statements: List of expertise statement chunks
            
        Returns:
            Expertise section as markdown string
        """
        # Get themes to incorporate
        themes = voice_profile.get('themes', [])
        theme_words = ' '.join(themes).lower()
        
        # Determine section title based on themes
        if 'expertise' in theme_words:
            section_title = "## My Expertise"
        elif 'focus' in theme_words:
            section_title = "## My Focus Areas"
        elif 'specialization' in theme_words or 'specialize' in theme_words:
            section_title = "## My Specializations"
        else:
            section_title = "## Areas of Expertise"
        
        expertise_parts = [section_title + "\n"]
        
        # Create a list of expertise areas
        expertise_parts.append("I specialize in:")
        
        # Extract expertise areas from statements
        expertise_areas = []
        for statement in expertise_statements:
            content = statement.get('content', '')
            
            # Look for phrases like "I specialize in X" or "I focus on X"
            specialization_match = re.search(r'(?:specialize|focus|expertise).+?(in|on)\s+(.+?)(?:\.|\,|$)', content, re.IGNORECASE)
            if specialization_match:
                expertise_area = specialization_match.group(2).strip()
                if expertise_area and expertise_area not in expertise_areas:
                    expertise_areas.append(expertise_area)
        
        # If we couldn't extract specific areas, use the statements themselves
        if not expertise_areas and expertise_statements:
            for statement in expertise_statements[:3]:
                expertise_areas.append(statement['content'])
        
        # Add default areas if we still don't have any
        if not expertise_areas:
            # Use themes from voice profile as expertise areas
            if themes:
                expertise_areas = [f"{theme}" for theme in themes[:3]]
            else:
                expertise_areas = [
                    "Personal and professional development",
                    "Authentic leadership",
                    "Creating meaningful impact"
                ]
        
        # Format as bullet points
        for area in expertise_areas:
            expertise_parts.append(f"* {area}")
        
        # Join all parts with proper spacing
        return "\n\n".join(expertise_parts)
    
    def _generate_closing_section(
        self, 
        voice_profile: Dict, 
        key_insights: List[Dict]
    ) -> str:
        """Generate closing section.
        
        Args:
            voice_profile: Voice characteristics from style profile
            key_insights: List of key insight chunks
            
        Returns:
            Closing section as markdown string
        """
        closing_parts = ["## Let's Connect\n"]
        
        # Use a powerful insight for the closing if available
        if key_insights:
            # Find insights that mention connection or impact
            connection_insights = [
                i for i in key_insights 
                if any(word in i.get('content', '').lower() for word in ['connect', 'impact', 'together', 'help', 'support'])
            ]
            
            if connection_insights:
                closing_parts.append(connection_insights[0]['content'])
            else:
                # Use the last key insight
                closing_parts.append(key_insights[-1]['content'])
        else:
            # Generate a closing based on voice profile
            themes = ' '.join(voice_profile.get('themes', [])).lower()
            values = ' '.join(voice_profile.get('values', [])).lower()
            
            if 'impact' in themes or 'impact' in values:
                closing_parts.append("I'm committed to creating meaningful impact through authentic connection and purposeful collaboration.")
            elif 'growth' in themes or 'development' in themes:
                closing_parts.append("I'm passionate about supporting others in their growth journey through authentic connection and shared purpose.")
            else:
                closing_parts.append("I look forward to connecting and exploring how we can create meaningful impact together.")
        
        # Add a call to action
        closing_parts.append("Ready to explore how we can work together? Let's connect and discuss how my unique approach can benefit your journey.")
        
        # Join all parts with proper spacing
        return "\n\n".join(closing_parts)
