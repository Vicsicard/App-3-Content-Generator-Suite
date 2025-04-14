"""Content manager for storing App 3 markdown outputs in Supabase.

Maps generator outputs to the content table with proper sections and metadata.
"""

from typing import Dict, Optional, List
from datetime import datetime
import re
import os
import logging
from .supabase_client import supabase

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ContentManager:
    """Manages storing markdown content in Supabase content table."""
    
    # Map of generator names to section info
    SECTION_MAPPING = {
        'blog_post': {'section': 'blog', 'title': 'Blog Post'},
        'website_home': {'section': 'website', 'title': 'Website Content'},
        'bio': {'section': 'bio', 'title': 'Professional Bio'},
        'newsletter': {'section': 'newsletter', 'title': 'Newsletter'},
        'social_posts': {'section': 'social', 'title': 'Social Media Posts'},
        'ad_copy': {'section': 'ad_copy', 'title': 'Ad Copy'},
        'show_notes': {'section': 'show_notes', 'title': 'Show Notes'},
        'reputation_repair': {'section': 'reputation', 'title': 'Reputation Content'}
    }
    
    # Default tags
    DEFAULT_TAGS = ["auto", "import", "draft"]
    
    def __init__(self):
        """Initialize content manager."""
        self.client = supabase.get_client()
        # Get test user ID from environment or use default
        self.test_user_id = os.getenv('TEST_USER_ID', "user_2vUz4MiEOKyCcxq4ny4xwsuwlG9")
        
    def _generate_slug(self, name: str, attempt: int = 0) -> str:
        """Generate URL-friendly slug from name and timestamp.
        
        Args:
            name: Base name to use
            attempt: Number of retry attempts for collision
            
        Returns:
            Slug string like 'blog-post-2025-04-13' or 'blog-post-2025-04-13-1'
        """
        base = name.replace('_', '-')
        timestamp = datetime.now().strftime("%Y-%m-%d")
        slug = f"{base}-{timestamp}"
        if attempt > 0:
            slug += f"-{attempt}"
        return slug
        
    def _extract_excerpt(self, content: str, max_length: int = 150) -> str:
        """Extract excerpt from content (first 1-2 lines or summary).
        
        Args:
            content: Markdown content
            max_length: Maximum excerpt length
            
        Returns:
            Short excerpt string
        """
        # Remove markdown headers
        clean_content = re.sub(r'#.*?\n', '', content)
        
        # Get first paragraph
        paragraphs = clean_content.split('\n\n')
        first_para = next((p for p in paragraphs if p.strip()), "")
        
        # Truncate if needed
        if len(first_para) > max_length:
            first_para = first_para[:max_length].rsplit(' ', 1)[0] + '...'
            
        return first_para or "Auto-imported content"
        
    async def _check_existing_content(self, section: str, title: str, user_id: str) -> Optional[Dict]:
        """Check if content already exists for section + title + user.
        
        Args:
            section: Content section
            title: Content title
            user_id: User ID
            
        Returns:
            Existing content record if found, None otherwise
        """
        result = await self.client.table('content')\
            .select('id, slug')\
            .eq('section', section)\
            .eq('title', title)\
            .eq('user_id', user_id)\
            .execute()
            
        return result.data[0] if result.data else None
        
    def save_content(self,
                    name: str,
                    content: str,
                    user_id: Optional[str] = None,
                    title: Optional[str] = None,
                    excerpt: Optional[str] = None,
                    tags: Optional[List[str]] = None,
                    type: Optional[str] = None,
                    platform: Optional[str] = None,
                    platforms: Optional[List[str]] = None,
                    scheduled_date: Optional[datetime] = None,
                    video_id: Optional[str] = None,
                    thumbnail: Optional[str] = None,
                    caption: Optional[str] = None,
                    publish_metadata: Optional[Dict] = None,
                    retry: Optional[bool] = None) -> Dict:
        """Save markdown content directly to Supabase.
        
        Args:
            name: Content name (e.g. 'blog_post', 'website_home')
            content: Raw markdown content
            user_id: Optional Clerk user ID (uses TEST_USER_ID if None)
            title: Optional content title (uses default if None)
            excerpt: Optional short summary (auto-generated if None)
            tags: Optional list of tags (uses defaults if None)
            type: Optional content subtype
            platform: Optional single platform (e.g. LinkedIn)
            platforms: Optional list of platforms
            scheduled_date: Optional scheduled publish date
            video_id: Optional linked video ID
            thumbnail: Optional preview image
            caption: Optional thumbnail caption
            publish_metadata: Optional JSON metadata for publishing
            retry: Optional boolean for retry status
            
        Returns:
            Dict containing the inserted record data
        
        Raises:
            ValueError: If name is not in SECTION_MAPPING
            RuntimeError: If database operation fails
        """
        if name not in self.SECTION_MAPPING:
            raise ValueError(f"Invalid content name: {name}")
        
        # Get section info
        section_info = self.SECTION_MAPPING[name]
        final_user_id = user_id or self.test_user_id
        final_title = title or section_info['title']
        
        # Check for existing content
        try:
            existing = self._check_existing_content(
                section_info['section'],
                final_title,
                final_user_id
            )
            if existing:
                logger.warning(
                    f"Content already exists for section='{section_info['section']}' "
                    f"title='{final_title}' user='{final_user_id}' "
                    f"with id='{existing['id']}'"
                )
        except Exception as e:
            logger.error(f"Error checking for existing content: {str(e)}")
        
        # Generate unique slug
        attempt = 0
        while True:
            try:
                slug = self._generate_slug(name, attempt)
                # Check if slug exists
                result = self.client.table('content')\
                    .select('id')\
                    .eq('slug', slug)\
                    .execute()
                if not result.data:
                    break
                attempt += 1
            except Exception as e:
                logger.error(f"Error checking slug uniqueness: {str(e)}")
                break
        
        # Prepare database record
        record = {
            'user_id': final_user_id,
            'section': section_info['section'],
            'title': final_title,
            'content': content,
            'status': 'draft',
            'slug': slug,
            'excerpt': excerpt or self._extract_excerpt(content),
            'tags': tags or self.DEFAULT_TAGS,
            'type': type,
            'platform': platform,
            'platforms': platforms,
            'scheduled_date': scheduled_date.isoformat() if scheduled_date else None,
            'video_id': video_id,
            'thumbnail': thumbnail,
            'caption': caption,
            'publish_metadata': publish_metadata,
            'retry': retry
        }
        
        # Insert into database
        try:
            result = self.client.table('content').insert(record).execute()
            
            if not result.data:
                raise RuntimeError("No data returned from insert operation")
                
            logger.info(
                f"✓ Saved {name} content to database:\n"
                f"  ID: {result.data[0]['id']}\n"
                f"  Section: {section_info['section']}\n"
                f"  Title: {final_title}\n"
                f"  Slug: {slug}"
            )
            return result.data[0]
            
        except Exception as e:
            error_msg = f"Failed to save content: {str(e)}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)
        
    def get_content(self, user_id: str, section: Optional[str] = None) -> List[Dict]:
        """Retrieve content for a user.
        
        Args:
            user_id: Clerk user ID
            section: Optional section filter
            
        Returns:
            List of content records
        """
        try:
            query = self.client.table('content').select('*').eq('user_id', user_id)
            
            if section:
                query = query.eq('section', section)
                
            result = query.execute()
            return result.data
            
        except Exception as e:
            error_msg = f"Failed to retrieve content: {str(e)}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)
        
    def update_content(self, content_id: str, updates: Dict) -> Dict:
        """Update existing content record.
        
        Args:
            content_id: UUID of content to update
            updates: Dict of fields to update
            
        Returns:
            Updated content record
        """
        try:
            # Ensure we can't change user_id or override draft status
            if 'user_id' in updates:
                del updates['user_id']
            if updates.get('status') == 'published':
                logger.warning("Cannot publish content through update, use publish_content instead")
                del updates['status']
            
            result = self.client.table('content').update(updates).eq('id', content_id).execute()
            
            if not result.data:
                raise RuntimeError(f"No data returned from update operation")
                
            logger.info(f"✓ Updated content {content_id}")
            return result.data[0]
            
        except Exception as e:
            error_msg = f"Failed to update content: {str(e)}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)
        
    def delete_content(self, content_id: str) -> None:
        """Delete content record.
        
        Args:
            content_id: UUID of content to delete
        """
        try:
            self.client.table('content').delete().eq('id', content_id).execute()
            logger.info(f"✓ Deleted content {content_id}")
            
        except Exception as e:
            error_msg = f"Failed to delete content: {str(e)}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)
            
    def publish_content(self, content_id: str) -> Dict:
        """Publish content by setting status to published.
        
        Args:
            content_id: UUID of content to publish
            
        Returns:
            Updated content record
        """
        return self.update_content(content_id, {
            'status': 'published',
            'published_at': datetime.now().isoformat()
        })

# Create singleton instance
content_manager = ContentManager()
