"""Enhanced Social Media Writer Agent for App 3.

This enhanced social media writer creates authentic, personalized social media content by:
1. Directly incorporating the client's actual language from transcript chunks
2. Utilizing the voice, themes, and values analysis from the style profile
3. Preserving the client's unique expressions and emotion in each platform's posts
"""

from pathlib import Path
import re
import random
from typing import Dict, List, Optional, Tuple
import logging

from .base_agent import ContentAgent
from ..database.content_manager import content_manager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnhancedSocialMediaWriter(ContentAgent):
    """Creates authentic social media content using the client's actual language."""
    
    def __init__(self, input_dir: str = 'input'):
        """Initialize enhanced social media writer.
        
        Args:
            input_dir: Directory containing input files
        """
        super().__init__()
        self.input_dir = Path(input_dir)
        self.platforms = ['linkedin', 'twitter', 'instagram', 'facebook']
        self.posts_per_platform = 4
    
    def generate(self, transcript: str = None, style_profile: str = None) -> Dict:
        """Generate authentic social media content from transcript and style profile.
        
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
        
        # Score and categorize chunks for different platforms
        scored_chunks = self._score_chunks_for_social(chunks, voice_profile)
        
        # Generate social media content for each platform
        all_posts = {}
        for platform in self.platforms:
            # Generate multiple posts for each platform
            platform_posts = self._generate_platform_posts(
                platform, 
                scored_chunks, 
                voice_profile
            )
            
            all_posts[platform] = platform_posts
            logger.info(f"Generated {len(platform_posts)} posts for {platform}")
        
        # Format all posts into a single markdown document
        social_content = self._format_social_posts(all_posts)
        
        # Save to Supabase
        return content_manager.save_content(
            name='social_media',
            content=social_content
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
    
    def _score_chunks_for_social(
        self, 
        chunks: List[Dict], 
        voice_profile: Dict
    ) -> Dict[str, List[Dict]]:
        """Score and categorize chunks for different social platforms.
        
        Args:
            chunks: List of transcript chunks
            voice_profile: Voice profile from style-profile.md
            
        Returns:
            Dict mapping platform to list of scored chunks
        """
        # Platform-specific criteria
        platform_criteria = {
            'linkedin': {
                'professional': 1.5,
                'insightful': 1.5,
                'educational': 1.3,
                'thought_leadership': 1.2,
                'length_range': (50, 200),  # Ideal content length in words
                'emotion_keywords': ['professional', 'growth', 'development', 'leadership', 'expertise']
            },
            'twitter': {
                'concise': 2.0,
                'memorable': 1.5,
                'punchy': 1.3,
                'thought_provoking': 1.2,
                'length_range': (10, 60),  # Ideal content length in words
                'emotion_keywords': ['impactful', 'perspective', 'insight', 'passion', 'challenge']
            },
            'instagram': {
                'visual': 1.5,
                'inspirational': 1.5,
                'emotional': 1.3,
                'story_based': 1.2,
                'length_range': (30, 100),  # Ideal content length in words
                'emotion_keywords': ['beautiful', 'inspiring', 'journey', 'transformation', 'authentic']
            },
            'facebook': {
                'relatable': 1.5,
                'conversational': 1.5,
                'personal': 1.3,
                'engaging': 1.2,
                'length_range': (40, 150),  # Ideal content length in words
                'emotion_keywords': ['connection', 'community', 'sharing', 'experience', 'story']
            }
        }
        
        # Score chunks for each platform
        platform_chunks = {platform: [] for platform in self.platforms}
        
        for chunk in chunks:
            content = chunk.get('content', '')
            if not content:
                continue
                
            # Basic checks
            content_words = len(content.split())
            content_lower = content.lower()
            
            for platform, criteria in platform_criteria.items():
                score = 0
                
                # Length score (optimal length gets highest score)
                min_len, max_len = criteria['length_range']
                if min_len <= content_words <= max_len:
                    score += 1.0
                elif content_words < min_len:
                    # Too short, but can still be usable
                    score += 0.5
                elif content_words <= max_len * 1.5:
                    # Longer than ideal but still usable
                    score += 0.7
                else:
                    # Way too long, less suitable
                    score += 0.2
                
                # Keyword matching
                keyword_matches = sum(1 for keyword in criteria['emotion_keywords'] if keyword in content_lower)
                score += keyword_matches * 0.3
                
                # Score based on sentence structure
                # Short, punchy sentences for Twitter
                if platform == 'twitter':
                    sentences = re.split(r'[.!?]', content)
                    short_sentences = [s for s in sentences if len(s.split()) <= 15]
                    score += len(short_sentences) * 0.2
                
                # Professional insights for LinkedIn
                if platform == 'linkedin':
                    if any(word in content_lower for word in ['learned', 'discovered', 'understand', 'approach', 'strategy']):
                        score += 0.5
                
                # Emotional content for Instagram
                if platform == 'instagram':
                    if any(word in content_lower for word in ['feel', 'emotion', 'experience', 'journey', 'transformation']):
                        score += 0.5
                
                # Relatable stories for Facebook
                if platform == 'facebook':
                    if any(word in content_lower for word in ['remember', 'time', 'when', 'story', 'share']):
                        score += 0.5
                
                # Add chunk with its score for this platform
                platform_chunks[platform].append({
                    'chunk': chunk,
                    'score': score
                })
        
        # Sort chunks by score for each platform
        for platform in platform_chunks:
            platform_chunks[platform].sort(key=lambda x: x['score'], reverse=True)
        
        return platform_chunks
    
    def _generate_platform_posts(
        self, 
        platform: str, 
        scored_chunks: Dict[str, List[Dict]], 
        voice_profile: Dict
    ) -> List[Dict]:
        """Generate posts for a specific platform.
        
        Args:
            platform: Social media platform
            scored_chunks: Dict mapping platform to scored chunks
            voice_profile: Voice profile dictionary
            
        Returns:
            List of post dictionaries for the platform
        """
        # Select top chunks for this platform
        platform_best_chunks = scored_chunks.get(platform, [])
        
        # Generate number of posts requested
        posts = []
        for i in range(self.posts_per_platform):
            # Use chunks in score order, cycling if necessary
            index = i % len(platform_best_chunks) if platform_best_chunks else 0
            
            if platform_best_chunks:
                chunk_data = platform_best_chunks[index]
                chunk = chunk_data['chunk']
                chunk_content = chunk.get('content', '')
            else:
                chunk_content = ""
            
            # Generate platform-specific post
            if platform == 'linkedin':
                post = self._generate_linkedin_post(chunk_content, voice_profile)
            elif platform == 'twitter':
                post = self._generate_twitter_post(chunk_content, voice_profile)
            elif platform == 'instagram':
                post = self._generate_instagram_post(chunk_content, voice_profile)
            elif platform == 'facebook':
                post = self._generate_facebook_post(chunk_content, voice_profile)
            else:
                post = self._generate_generic_post(platform, chunk_content, voice_profile)
            
            posts.append(post)
        
        return posts
    
    def _generate_linkedin_post(
        self, 
        chunk_content: str, 
        voice_profile: Dict
    ) -> Dict:
        """Generate a LinkedIn post from chunk content.
        
        Args:
            chunk_content: Content from transcript chunk
            voice_profile: Voice profile dictionary
            
        Returns:
            LinkedIn post dictionary
        """
        # Extract key professional insights
        sentences = re.split(r'(?<=[.!?])\s+', chunk_content)
        
        # Find professional sentences
        professional_keywords = ['professional', 'expertise', 'learned', 'approach', 
                               'strategy', 'insight', 'understand', 'growth',
                               'development', 'leadership', 'experience']
        
        professional_sentences = []
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in professional_keywords):
                professional_sentences.append(sentence)
        
        # Use professional sentences or regular sentences if none found
        selected_sentences = professional_sentences if professional_sentences else sentences
        
        # Craft the post content
        post_content_parts = []
        
        # Create a thought-leadership hook
        themes = voice_profile.get('themes', [])
        values = voice_profile.get('values', [])
        
        theme = random.choice(themes) if themes else "professional growth"
        value = random.choice(values) if values else "authentic leadership"
        
        hooks = [
            f"I've been reflecting on the importance of {theme} in today's landscape.",
            f"A question I often get asked: How do we truly embody {theme}?",
            f"The intersection of {theme} and {value} creates powerful opportunities.",
            f"One principle that has guided my work: {value} is the foundation of lasting impact."
        ]
        
        post_content_parts.append(random.choice(hooks))
        
        # Add the client's actual insights
        if selected_sentences:
            # Use first sentence as a direct quote
            post_content_parts.append(f"As I often say, \"{selected_sentences[0]}\"")
            
            # Use additional sentences if available
            if len(selected_sentences) > 1:
                additional_insight = selected_sentences[1]
                post_content_parts.append(additional_insight)
        
        # Add reflection/call to action
        reflections = [
            f"How are you approaching {theme} in your work?",
            f"I'd love to hear your thoughts on this perspective.",
            f"What has been your experience with {value} in your professional journey?",
            f"Have you found similar insights in your work?"
        ]
        
        post_content_parts.append(random.choice(reflections))
        
        # Add hashtags
        hashtags = f"#{''.join(theme.split())} #ProfessionalDevelopment #{''.join(value.split())}"
        post_content_parts.append(hashtags)
        
        # Join all parts with proper spacing
        post_content = "\n\n".join(post_content_parts)
        
        # Create title from theme
        title = f"Professional Insight: {theme.title()}"
        
        return {
            'title': title,
            'content': post_content,
            'platform': 'LinkedIn'
        }

    def _generate_twitter_post(
        self, 
        chunk_content: str, 
        voice_profile: Dict
    ) -> Dict:
        """Generate a Twitter post from chunk content.
        
        Args:
            chunk_content: Content from transcript chunk
            voice_profile: Voice profile dictionary
            
        Returns:
            Twitter post dictionary
        """
        # Extract concise, impactful statements
        sentences = re.split(r'(?<=[.!?])\s+', chunk_content)
        
        # Find concise sentences
        concise_sentences = [s for s in sentences if 5 <= len(s.split()) <= 15]
        
        # If no concise sentences, use the shortest ones available
        if not concise_sentences and sentences:
            concise_sentences = sorted(sentences, key=lambda s: len(s.split()))[:2]
        
        # Use concise sentences or the original content if none found
        if concise_sentences:
            main_content = concise_sentences[0]
        else:
            # Take the first part of the chunk content (Twitter friendly)
            words = chunk_content.split()
            if len(words) > 20:
                main_content = ' '.join(words[:20]) + "..."
            else:
                main_content = chunk_content
        
        # Create engaging tweet content
        themes = voice_profile.get('themes', [])
        values = voice_profile.get('values', [])
        
        theme = random.choice(themes) if themes else "personal growth"
        
        # Format as a thought-provoking tweet
        tweet_content = f"\"{main_content}\"\n\nReflecting on {theme.lower()} and its impact on our journeys.\n\n"
        
        # Add hashtags
        hashtags = "#" + ''.join(theme.split()) + " "
        if values:
            value = random.choice(values)
            hashtags += "#" + ''.join(value.split())
        else:
            hashtags += "#PersonalDevelopment"
            
        tweet_content += hashtags
        
        # Create title from theme
        title = f"Twitter Insight: {theme.title()}"
        
        return {
            'title': title,
            'content': tweet_content,
            'platform': 'Twitter'
        }
    
    def _generate_instagram_post(
        self, 
        chunk_content: str, 
        voice_profile: Dict
    ) -> Dict:
        """Generate an Instagram post from chunk content.
        
        Args:
            chunk_content: Content from transcript chunk
            voice_profile: Voice profile dictionary
            
        Returns:
            Instagram post dictionary
        """
        # Extract visual, emotional, inspirational content
        sentences = re.split(r'(?<=[.!?])\s+', chunk_content)
        
        # Look for emotional, inspirational sentences
        emotion_keywords = ['feel', 'emotion', 'heart', 'soul', 'spirit', 'journey', 
                          'transformation', 'experience', 'authentic', 'true']
        
        emotional_sentences = []
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in emotion_keywords):
                emotional_sentences.append(sentence)
        
        # Use emotional sentences or regular sentences if none found
        selected_sentences = emotional_sentences if emotional_sentences else sentences
        
        # Create Instagram caption
        caption_parts = []
        
        # Start with a powerful quote or statement
        if selected_sentences:
            main_quote = selected_sentences[0]
            caption_parts.append(f"✨ \"{main_quote}\" ✨")
        
        # Add personal reflection
        themes = voice_profile.get('themes', [])
        values = voice_profile.get('values', [])
        
        theme = random.choice(themes) if themes else "personal journey"
        value = random.choice(values) if values else "authenticity"
        
        reflections = [
            f"This captures the essence of {theme} for me.",
            f"I've found that embracing {value} changes everything.",
            f"On this journey of {theme}, I've discovered the power of {value}.",
            f"This truth has transformed how I approach {theme} in my work and life."
        ]
        
        caption_parts.append(random.choice(reflections))
        
        # Add more substance from additional sentences if available
        if len(selected_sentences) > 1:
            additional_content = selected_sentences[1]
            caption_parts.append(additional_content)
        
        # Add engagement question
        questions = [
            f"How does {theme} show up in your life?",
            f"What does {value} mean to you?",
            f"Have you experienced this truth in your own journey?",
            f"What's one way you're embracing {theme} today?"
        ]
        
        caption_parts.append(random.choice(questions))
        
        # Add hashtags
        hashtags = [
            f"#{theme.replace(' ', '')}", 
            f"#{value.replace(' ', '')}", 
            "#PersonalGrowth", 
            "#AuthenticLiving", 
            "#Transformation"
        ]
        
        caption_parts.append(' '.join(hashtags))
        
        # Join all parts with proper spacing
        caption = "\n\n".join(caption_parts)
        
        # Create title from theme
        title = f"Visual Inspiration: {theme.title()}"
        
        return {
            'title': title,
            'content': caption,
            'platform': 'Instagram'
        }
    
    def _generate_facebook_post(
        self, 
        chunk_content: str, 
        voice_profile: Dict
    ) -> Dict:
        """Generate a Facebook post from chunk content.
        
        Args:
            chunk_content: Content from transcript chunk
            voice_profile: Voice profile dictionary
            
        Returns:
            Facebook post dictionary
        """
        # Extract relatable, story-based content
        sentences = re.split(r'(?<=[.!?])\s+', chunk_content)
        
        # Look for story elements and relatable content
        story_keywords = ['story', 'remember', 'when', 'experience', 'learned',
                         'realized', 'discovered', 'journey', 'path', 'moment']
        
        story_sentences = []
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in story_keywords):
                story_sentences.append(sentence)
        
        # Use story sentences or regular sentences if none found
        selected_sentences = story_sentences if story_sentences else sentences
        
        # Create Facebook post content
        post_parts = []
        
        # Create conversational opener
        openers = [
            "I was reflecting today on something important...",
            "I wanted to share a thought that's been on my mind lately.",
            "Something I've been thinking about that might resonate with you too.",
            "A perspective that's been meaningful in my journey."
        ]
        
        post_parts.append(random.choice(openers))
        
        # Include client's actual words
        if selected_sentences:
            # Join first two sentences if available
            if len(selected_sentences) >= 2:
                client_words = f"{selected_sentences[0]} {selected_sentences[1]}"
            else:
                client_words = selected_sentences[0]
                
            post_parts.append(client_words)
        
        # Add personal connection
        themes = voice_profile.get('themes', [])
        values = voice_profile.get('values', [])
        
        theme = random.choice(themes) if themes else "connection"
        value = random.choice(values) if values else "community"
        
        connections = [
            f"This connects deeply to {theme} in ways that continue to surprise me.",
            f"I've found that embracing {value} changes everything.",
            f"When we embrace this truth about {theme}, everything shifts.",
            f"This perspective has shaped how I approach {value} in my life and work."
        ]
        
        post_parts.append(random.choice(connections))
        
        # Add engagement question
        questions = [
            f"Does this resonate with your experience of {theme}?",
            f"How has {value} shown up in your life lately?",
            f"I'd love to hear your thoughts on this.",
            f"Has your journey with {theme} revealed similar insights?"
        ]
        
        post_parts.append(random.choice(questions))
        
        # Join all parts with proper spacing
        post_content = "\n\n".join(post_parts)
        
        # Create title from theme
        title = f"Community Reflection: {theme.title()}"
        
        return {
            'title': title,
            'content': post_content,
            'platform': 'Facebook'
        }
    
    def _generate_generic_post(
        self, 
        platform: str, 
        chunk_content: str, 
        voice_profile: Dict
    ) -> Dict:
        """Generate a generic post when platform specific formatting isn't available.
        
        Args:
            platform: Social media platform
            chunk_content: Content from transcript chunk
            voice_profile: Voice profile dictionary
            
        Returns:
            Generic post dictionary
        """
        # Extract key sentences
        sentences = re.split(r'(?<=[.!?])\s+', chunk_content)
        
        # Create post content
        post_parts = []
        
        # Include client's actual words
        if sentences:
            # Use first sentence
            post_parts.append(f"\"{sentences[0]}\"")
            
            # Add another sentence if available
            if len(sentences) > 1:
                post_parts.append(sentences[1])
        
        # Add theme reference
        themes = voice_profile.get('themes', [])
        theme = random.choice(themes) if themes else "personal development"
        
        post_parts.append(f"This insight about {theme} has been transformative in my work.")
        
        # Add engagement prompt
        post_parts.append(f"What's your experience with {theme}? I'd love to hear your thoughts!")
        
        # Add hashtags
        post_parts.append(f"#{theme.replace(' ', '')} #PersonalGrowth #ProfessionalDevelopment")
        
        # Join all parts with proper spacing
        post_content = "\n\n".join(post_parts)
        
        # Create title
        title = f"{platform.title()} Post: {theme.title()}"
        
        return {
            'title': title,
            'content': post_content,
            'platform': platform.title()
        }
    
    def _format_social_posts(self, all_posts: Dict[str, List[Dict]]) -> str:
        """Format all social media posts into a single markdown document.
        
        Args:
            all_posts: Dict mapping platform to list of post dictionaries
            
        Returns:
            Combined social media posts content as markdown string
        """
        # Add title
        formatted_content = ["# Social Media Posts\n"]
        
        # Add each platform's posts
        for platform in self.platforms:
            platform_posts = all_posts.get(platform, [])
            if not platform_posts:
                continue
            
            # Add platform header
            formatted_content.append(f"## {platform.title()} Posts\n")
            
            # Add each post
            for i, post in enumerate(platform_posts):
                post_num = i + 1
                title = post.get('title', f"{platform.title()} Post {post_num}")
                content = post.get('content', '')
                
                formatted_content.append(f"### {title}")
                formatted_content.append(f"```\n{content}\n```")
                
                # Add separator between posts (except after the last one)
                if i < len(platform_posts) - 1:
                    formatted_content.append("---")
            
            # Add separator between platforms (except after the last one)
            if platform != self.platforms[-1]:
                formatted_content.append("\n---\n")
        
        # Join all parts with proper spacing
        return "\n\n".join(formatted_content)
