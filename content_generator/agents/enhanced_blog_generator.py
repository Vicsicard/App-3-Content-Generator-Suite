"""Enhanced Blog Generator Agent for App 3.

This enhanced blog generator creates authentic, personalized blog content by:
1. Directly incorporating the client's actual language from transcript chunks
2. Utilizing the voice, themes, and values analysis from the style profile
3. Preserving the client's unique expressions and storytelling patterns
"""

from pathlib import Path
import re
from typing import Dict, List, Optional, Tuple
import logging
import random

from .base_agent import ContentAgent
from ..database.content_manager import content_manager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnhancedBlogGenerator(ContentAgent):
    """Creates authentic blog content using the client's actual language."""
    
    def __init__(self, input_dir: str = 'input'):
        """Initialize enhanced blog generator.
        
        Args:
            input_dir: Directory containing input files
        """
        super().__init__()
        self.input_dir = Path(input_dir)
    
    def generate(self, transcript: str = None, style_profile: str = None) -> Dict:
        """Generate authentic blog content from transcript and style profile.
        
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
        
        # Generate blog topics based on themes and client's language
        blog_topics = self._generate_blog_topics(voice_profile, chunks)
        logger.info(f"Generated {len(blog_topics)} blog topics")
        
        # Generate blog posts for each topic
        blog_posts = []
        for topic in blog_topics:
            blog_post = self._generate_blog_post(
                topic, 
                voice_profile, 
                chunks
            )
            blog_posts.append(blog_post)
            
            logger.info(f"Generated blog post: {topic['title']}")
        
        # Combine all blog posts into single markdown document
        blog_content = self._format_blog_posts(blog_posts)
        
        # Save to Supabase
        return content_manager.save_content(
            name='blog_posts',
            content=blog_content
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
    
    def _generate_blog_topics(
        self, 
        voice_profile: Dict, 
        chunks: List[Dict]
    ) -> List[Dict]:
        """Generate blog topics based on themes and client's language.
        
        Args:
            voice_profile: Voice characteristics from style profile
            chunks: List of transcript chunks
            
        Returns:
            List of blog topic dictionaries
        """
        # Extract themes and values from voice profile
        themes = voice_profile.get('themes', [])
        values = voice_profile.get('values', [])
        
        # Categorize chunks by theme relevance
        theme_chunks = {}
        for theme in themes:
            theme_chunks[theme] = []
            theme_words = set(theme.lower().split())
            
            for chunk in chunks:
                chunk_content = chunk.get('content', '').lower()
                if chunk_content and any(word in chunk_content for word in theme_words):
                    theme_chunks[theme].append(chunk)
        
        # Generate blog topics based on themes and client content
        blog_topics = []
        
        # Create topics from the top 3 themes (or fewer if less available)
        top_themes = sorted(
            themes, 
            key=lambda t: len(theme_chunks.get(t, [])), 
            reverse=True
        )[:3]
        
        for theme in top_themes:
            relevant_chunks = theme_chunks.get(theme, [])
            if not relevant_chunks:
                continue
                
            # Sort chunks by length to find substantial ones for topic generation
            substantial_chunks = sorted(
                relevant_chunks, 
                key=lambda c: len(c.get('content', '')), 
                reverse=True
            )[:3]
            
            # Generate title based on theme and substantial chunk content
            if substantial_chunks:
                main_chunk = substantial_chunks[0]
                title = self._generate_topic_title(theme, main_chunk['content'])
                
                blog_topics.append({
                    'title': title,
                    'theme': theme,
                    'main_chunk': main_chunk,
                    'supporting_chunks': substantial_chunks[1:] if len(substantial_chunks) > 1 else []
                })
        
        # If we need more topics (aiming for 4 total), create from values
        while len(blog_topics) < 4 and values:
            value = values.pop(0)
            # Find chunks relevant to this value
            value_chunks = []
            value_words = set(value.lower().split())
            
            for chunk in chunks:
                chunk_content = chunk.get('content', '').lower()
                if chunk_content and any(word in chunk_content for word in value_words):
                    value_chunks.append(chunk)
            
            if value_chunks:
                # Sort chunks by length to find substantial ones
                substantial_chunks = sorted(
                    value_chunks, 
                    key=lambda c: len(c.get('content', '')), 
                    reverse=True
                )[:3]
                
                # Generate title based on value and substantial chunk content
                if substantial_chunks:
                    main_chunk = substantial_chunks[0]
                    title = self._generate_topic_title(value, main_chunk['content'])
                    
                    # Check if this title is too similar to existing ones
                    if not any(self._title_similarity(title, topic['title']) > 0.7 for topic in blog_topics):
                        blog_topics.append({
                            'title': title,
                            'theme': value,  # Using value as theme
                            'main_chunk': main_chunk,
                            'supporting_chunks': substantial_chunks[1:] if len(substantial_chunks) > 1 else []
                        })
        
        # If we still need more topics, create generic ones
        generic_themes = ["Personal Growth", "Professional Development", "Success Strategies", "Mindset Shifts"]
        while len(blog_topics) < 4 and generic_themes:
            generic_theme = generic_themes.pop(0)
            
            # Find any substantial chunks not yet used
            used_chunks = set()
            for topic in blog_topics:
                used_chunks.add(topic['main_chunk'].get('number', -1))
                for chunk in topic.get('supporting_chunks', []):
                    used_chunks.add(chunk.get('number', -1))
            
            # Find unused substantial chunks
            substantial_chunks = [
                chunk for chunk in sorted(
                    chunks, 
                    key=lambda c: len(c.get('content', '')), 
                    reverse=True
                )
                if chunk.get('number', -1) not in used_chunks
            ][:3]
            
            if substantial_chunks:
                main_chunk = substantial_chunks[0]
                title = self._generate_topic_title(generic_theme, main_chunk['content'])
                
                blog_topics.append({
                    'title': title,
                    'theme': generic_theme,
                    'main_chunk': main_chunk,
                    'supporting_chunks': substantial_chunks[1:] if len(substantial_chunks) > 1 else []
                })
        
        return blog_topics[:4]  # Return maximum 4 topics
    
    def _title_similarity(self, title1: str, title2: str) -> float:
        """Calculate simple similarity between two titles.
        
        Args:
            title1: First title
            title2: Second title
            
        Returns:
            Similarity score between 0 and 1
        """
        # Convert to lowercase and split into words
        words1 = set(title1.lower().split())
        words2 = set(title2.lower().split())
        
        # Calculate Jaccard similarity
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        return intersection / union if union > 0 else 0
    
    def _generate_topic_title(self, theme: str, chunk_content: str) -> str:
        """Generate blog post title based on theme and chunk content.
        
        Args:
            theme: Theme or value
            chunk_content: Content from transcript chunk
            
        Returns:
            Blog post title
        """
        # Extract key phrases from chunk content
        key_phrases = self._extract_key_phrases(chunk_content)
        
        # Format a title combining theme and key phrase
        if key_phrases:
            phrase = random.choice(key_phrases)
            
            # Generate title patterns
            title_patterns = [
                f"{phrase}: The Key to {theme}",
                f"How to {phrase} to Enhance Your {theme}",
                f"The Power of {theme}: {phrase}",
                f"{theme}: {phrase} for Success",
                f"Mastering {theme} Through {phrase}",
                f"{phrase}: A Pathway to {theme}"
            ]
            
            return random.choice(title_patterns)
        else:
            # Fallback title patterns
            title_patterns = [
                f"The Power of {theme}",
                f"Unlocking Your Potential Through {theme}",
                f"How {theme} Transforms Your Journey",
                f"{theme}: The Foundation of Success",
                f"Mastering {theme} in Your Life and Work"
            ]
            
            return random.choice(title_patterns)
    
    def _extract_key_phrases(self, text: str) -> List[str]:
        """Extract meaningful key phrases from text.
        
        Args:
            text: Text to extract phrases from
            
        Returns:
            List of key phrases
        """
        # Split into sentences
        sentences = re.split(r'[.!?]', text)
        
        # Extract verb phrases
        verb_phrases = []
        for sentence in sentences:
            # Look for verb-centered phrases
            verb_matches = re.findall(r'\b(?:how to|ways to|learning to|being able to|can help|should|must|need to|trying to|working on|focus on|prioritize|develop|create|build|understand|realize)\b\s+([^,.!?;:]+)', sentence, re.IGNORECASE)
            verb_phrases.extend(verb_matches)
        
        # Extract noun phrases
        noun_phrases = []
        for sentence in sentences:
            # Look for important noun phrases
            noun_matches = re.findall(r'(?:the|a|an|my|your|our)?\s+(?:importance|power|value|benefit|impact|role|key|secret|essence|heart|core)\s+of\s+([^,.!?;:]+)', sentence, re.IGNORECASE)
            noun_phrases.extend(noun_matches)
            
            # Look for "X is Y" definitions
            definition_matches = re.findall(r'([^,.!?;:]{3,30})\s+(?:is|are|means|represents)\s+([^,.!?;:]+)', sentence, re.IGNORECASE)
            for match in definition_matches:
                if len(match[0].split()) <= 4:  # Short subject
                    noun_phrases.append(match[0])
        
        # Clean up and combine phrases
        all_phrases = verb_phrases + noun_phrases
        cleaned_phrases = [phrase.strip() for phrase in all_phrases if 3 <= len(phrase.split()) <= 8]
        
        # If no good phrases found, try simpler extraction
        if not cleaned_phrases:
            for sentence in sentences:
                # Take first part of longer sentences
                if len(sentence.split()) >= 6:
                    simplified = ' '.join(sentence.strip().split()[:6])
                    if simplified:
                        cleaned_phrases.append(simplified)
        
        # Remove duplicates
        unique_phrases = list(set(cleaned_phrases))
        
        return unique_phrases
    
    def _generate_blog_post(
        self, 
        topic: Dict, 
        voice_profile: Dict, 
        all_chunks: List[Dict]
    ) -> Dict:
        """Generate a complete blog post.
        
        Args:
            topic: Blog topic dictionary
            voice_profile: Voice profile from style-profile.md
            all_chunks: All transcript chunks
            
        Returns:
            Dictionary with blog post content
        """
        # Extract chunks to use
        main_chunk = topic['main_chunk']
        supporting_chunks = topic.get('supporting_chunks', [])
        
        # Find additional relevant chunks based on theme
        theme_words = set(topic['theme'].lower().split())
        additional_chunks = [
            chunk for chunk in all_chunks
            if chunk.get('number') != main_chunk.get('number') and
            chunk.get('number') not in [c.get('number') for c in supporting_chunks] and
            any(word in chunk.get('content', '').lower() for word in theme_words)
        ]
        
        # Sort additional chunks by relevance (presence of theme words)
        additional_chunks.sort(
            key=lambda c: sum(1 for word in theme_words if word in c.get('content', '').lower()),
            reverse=True
        )
        
        # Combine all chunks we'll use
        all_relevant_chunks = [main_chunk] + supporting_chunks + additional_chunks[:3]
        
        # Generate the blog content
        title = topic['title']
        introduction = self._generate_blog_introduction(title, main_chunk, voice_profile)
        body_sections = self._generate_blog_body(title, all_relevant_chunks, voice_profile)
        conclusion = self._generate_blog_conclusion(title, all_relevant_chunks, voice_profile)
        
        # Format the complete blog post
        blog_post = {
            'title': title,
            'content': f"# {title}\n\n{introduction}\n\n{body_sections}\n\n{conclusion}"
        }
        
        return blog_post
    
    def _generate_blog_introduction(
        self, 
        title: str, 
        main_chunk: Dict, 
        voice_profile: Dict
    ) -> str:
        """Generate blog post introduction.
        
        Args:
            title: Blog post title
            main_chunk: Main transcript chunk for this topic
            voice_profile: Voice profile dictionary
            
        Returns:
            Introduction paragraph as string
        """
        # Extract the main content
        main_content = main_chunk.get('content', '')
        
        # Split main content into sentences
        sentences = re.split(r'(?<=[.!?])\s+', main_content)
        
        # Select up to 2 key sentences for direct quotes
        key_sentences = []
        for sentence in sentences:
            # Find meaningful sentences (not too short or long)
            if 5 <= len(sentence.split()) <= 25 and any(c.isalpha() for c in sentence):
                key_sentences.append(sentence)
                if len(key_sentences) >= 2:
                    break
        
        # Create introduction with direct quotes
        intro_parts = []
        
        # Add a hook based on the title
        title_parts = title.split(':')
        if len(title_parts) > 1:  # Title has a colon
            main_topic = title_parts[0].strip()
            intro_hook = f"{main_topic} is a critical aspect that I've seen transform both my life and the lives of those I work with."
        else:
            intro_hook = f"In my experience, what we're exploring today is often the difference maker for those seeking meaningful change."
            
        intro_parts.append(intro_hook)
        
        # Add direct quote if available
        if key_sentences:
            quote = key_sentences[0]
            # Format as a direct quote
            intro_parts.append(f'As I often say, "{quote}"')
            
            # Add second sentence if available, but not as a quote
            if len(key_sentences) > 1:
                intro_parts.append(key_sentences[1])
                
        # Add a transition to the body
        intro_parts.append("Let's explore this topic together and uncover the insights that can make a significant difference in your journey.")
        
        # Join all parts with proper spacing
        return "\n\n".join(intro_parts)
    
    def _generate_blog_body(
        self, 
        title: str, 
        relevant_chunks: List[Dict], 
        voice_profile: Dict
    ) -> str:
        """Generate blog post body.
        
        Args:
            title: Blog post title
            relevant_chunks: Relevant transcript chunks
            voice_profile: Voice profile dictionary
            
        Returns:
            Blog body content as string
        """
        # Extract themes and determine section topics
        title_theme = title.split(':')[0].strip() if ':' in title else title
        
        # Generate 2-3 section topics based on title and available chunks
        if len(relevant_chunks) >= 3:
            # We can create 3 sections
            section_count = 3
        else:
            # Fewer chunks available, create 2 sections
            section_count = 2
        
        # Create section headings based on title theme
        section_headings = self._generate_section_headings(title_theme, section_count)
        
        # Distribute chunks across sections
        sections = []
        chunks_per_section = len(relevant_chunks) // section_count
        remaining_chunks = len(relevant_chunks) % section_count
        
        chunk_index = 0
        for i in range(section_count):
            # Determine how many chunks to use for this section
            section_chunk_count = chunks_per_section
            if remaining_chunks > 0:
                section_chunk_count += 1
                remaining_chunks -= 1
                
            # Get chunks for this section
            section_chunks = relevant_chunks[chunk_index:chunk_index + section_chunk_count]
            chunk_index += section_chunk_count
            
            # Generate section content
            section_content = self._generate_section_content(
                section_headings[i], 
                section_chunks, 
                voice_profile
            )
            
            sections.append(section_content)
        
        # Join all sections with proper spacing
        return "\n\n".join(sections)
    
    def _generate_section_headings(
        self, 
        theme: str, 
        count: int
    ) -> List[str]:
        """Generate section headings based on theme.
        
        Args:
            theme: Main theme for the blog post
            count: Number of sections to generate
            
        Returns:
            List of section heading strings
        """
        # Common section patterns
        patterns = [
            [
                f"Understanding {theme}",
                f"The Impact of {theme}",
                f"Implementing {theme} in Your Life"
            ],
            [
                f"The Essence of {theme}",
                f"Why {theme} Matters",
                f"Practical Steps for {theme}"
            ],
            [
                f"Discovering {theme}",
                f"The Transformative Power of {theme}",
                f"Making {theme} Work for You"
            ],
            [
                f"The Foundations of {theme}",
                f"Building on {theme}",
                f"Living {theme} Every Day"
            ]
        ]
        
        # Select a random pattern and return the requested number of headings
        selected_pattern = random.choice(patterns)
        return [f"## {heading}" for heading in selected_pattern[:count]]
    
    def _generate_section_content(
        self, 
        heading: str, 
        chunks: List[Dict], 
        voice_profile: Dict
    ) -> str:
        """Generate content for a blog section.
        
        Args:
            heading: Section heading
            chunks: Transcript chunks for this section
            voice_profile: Voice profile dictionary
            
        Returns:
            Section content as string
        """
        section_parts = [heading]
        
        # If no chunks available, return just the heading
        if not chunks:
            return heading
            
        # Create paragraphs from chunks
        for i, chunk in enumerate(chunks):
            chunk_content = chunk.get('content', '')
            
            # For the first chunk, use it more directly
            if i == 0:
                # Split into sentences
                sentences = re.split(r'(?<=[.!?])\s+', chunk_content)
                
                # Format as direct quote + commentary
                if sentences:
                    main_sentence = sentences[0]
                    section_parts.append(f'"{main_sentence}"')
                    
                    # Add commentary based on remaining sentences
                    if len(sentences) > 1:
                        commentary = ' '.join(sentences[1:])
                        section_parts.append(commentary)
            else:
                # For subsequent chunks, incorporate key insights
                insights = self._extract_key_insights(chunk_content)
                if insights:
                    section_parts.append(insights)
        
        # Add transition or reflective question at the end
        reflection = self._generate_reflection_question(heading)
        section_parts.append(reflection)
        
        # Join all parts with proper spacing
        return "\n\n".join(section_parts)
    
    def _extract_key_insights(self, text: str) -> str:
        """Extract key insights from chunk text.
        
        Args:
            text: Transcript chunk text
            
        Returns:
            Formatted insight text
        """
        # Split into sentences
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        # Select meaningful sentences (not too short)
        meaningful = [s for s in sentences if len(s.split()) >= 5]
        
        if not meaningful:
            return text
            
        # Combine selected sentences
        if len(meaningful) >= 2:
            # Use first and last meaningful sentence
            combined = f"{meaningful[0]} {meaningful[-1]}"
        else:
            combined = meaningful[0]
            
        return combined
    
    def _generate_reflection_question(self, heading: str) -> str:
        """Generate a reflection question related to the section.
        
        Args:
            heading: Section heading
            
        Returns:
            Reflection question string
        """
        # Extract main topic from heading (removing "## " prefix)
        topic = heading[3:]
        
        # Question patterns
        question_patterns = [
            f"How might {topic.lower()} show up differently in your life?",
            f"What would change if you fully embraced {topic.lower()}?",
            f"Where do you see opportunities to apply {topic.lower()} in your journey?",
            f"In what ways could {topic.lower()} transform your approach?",
            f"What's one small step you could take today related to {topic.lower()}?"
        ]
        
        return random.choice(question_patterns)
    
    def _generate_blog_conclusion(
        self, 
        title: str, 
        relevant_chunks: List[Dict], 
        voice_profile: Dict
    ) -> str:
        """Generate blog post conclusion.
        
        Args:
            title: Blog post title
            relevant_chunks: Relevant transcript chunks
            voice_profile: Voice profile dictionary
            
        Returns:
            Conclusion paragraph as string
        """
        conclusion_parts = ["## Final Thoughts"]
        
        # Find impactful statements for conclusion
        impact_statements = []
        for chunk in relevant_chunks:
            content = chunk.get('content', '')
            
            # Look for concluding statements
            conclusion_markers = [
                'ultimately', 'in conclusion', 'finally', 'remember', 
                'most important', 'key takeaway', 'what matters', 
                'in the end', 'looking ahead'
            ]
            
            # Split into sentences
            sentences = re.split(r'(?<=[.!?])\s+', content)
            
            for sentence in sentences:
                if any(marker in sentence.lower() for marker in conclusion_markers):
                    impact_statements.append(sentence)
                    
                # Also look for short, powerful statements
                elif 5 <= len(sentence.split()) <= 15:
                    if any(word in sentence.lower() for word in ['believe', 'know', 'trust', 'power', 'impact']):
                        impact_statements.append(sentence)
        
        # If we found impact statements, use the most powerful one
        if impact_statements:
            conclusion_parts.append(f'"{impact_statements[0]}"')
        else:
            # Create a generic conclusion based on title
            title_theme = title.split(':')[0].strip() if ':' in title else title
            conclusion_parts.append(f"The journey with {title_theme} is ongoing, and each step you take builds on the last.")
        
        # Add a call to action
        conclusion_parts.append("I invite you to reflect on these insights and consider how they might apply to your unique circumstances. What feels most resonant? Where can you begin implementing these ideas today? The power of this work emerges when you make it your own.")
        
        # Add a personal sign-off
        conclusion_parts.append("As always, I'm here to support your journey. Let's continue the conversation.")
        
        # Join all parts with proper spacing
        return "\n\n".join(conclusion_parts)
    
    def _format_blog_posts(self, blog_posts: List[Dict]) -> str:
        """Format all blog posts into a single markdown document.
        
        Args:
            blog_posts: List of blog post dictionaries
            
        Returns:
            Combined blog posts content as markdown string
        """
        # Add title
        formatted_content = ["# Blog Posts\n"]
        
        # Add each blog post with separator
        for i, post in enumerate(blog_posts):
            formatted_content.append(post['content'])
            
            # Add separator between posts (except after the last one)
            if i < len(blog_posts) - 1:
                formatted_content.append("\n---\n")
        
        # Join all parts with proper spacing
        return "\n\n".join(formatted_content)
