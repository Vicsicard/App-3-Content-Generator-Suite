"""Blog generator agent."""

from .base_agent import ContentAgent

class BlogGenerator(ContentAgent):
    """Generates blog posts from transcript chunks."""
    
    def generate(self, transcript: str, style_profile: str) -> str:
        """Generate blog post from transcript and style profile.
        
        Args:
            transcript: Content from transcript_chunks.md
            style_profile: Content from style-profile.md
            
        Returns:
            Generated blog post as HTML string
        """
        # Extract style elements and chunks
        style = self._extract_style_elements(style_profile)
        chunks = self._get_chunks(transcript)
        
        # Generate blog post
        blog_post = []
        
        # Add header
        blog_post.append("<article class='blog-post'>")
        blog_post.append("<h1>Finding Your Authentic Path: A Journey of Self-Discovery</h1>")
        
        # Generate sections
        blog_post.extend(self._generate_intro(chunks, style))
        blog_post.extend(self._generate_main_content(chunks, style))
        blog_post.extend(self._generate_conclusion(chunks, style))
        
        # Add footer
        blog_post.append("<section class='cta'>")
        blog_post.append("<h2>Ready to Begin Your Journey?</h2>")
        blog_post.append("<p>Connect with us to explore how you can embrace your authentic self and create lasting impact.</p>")
        blog_post.append("</section>")
        blog_post.append("</article>")
        
        return '\n'.join(blog_post)
    
    def _generate_intro(self, chunks: list[str], style: dict) -> list[str]:
        """Generate blog introduction."""
        intro = []
        intro.append("<section class='intro'>")
        intro.append("<h2>Introduction</h2>")
        intro.append("<p>In a world where everyone seems to have a pre-written script for success, finding your own authentic path can feel like navigating uncharted territory. Today, we explore a personal journey that demonstrates how embracing your unique perspective can lead to genuine impact and meaningful connections.</p>")
        
        # Use first chunk for intro quote
        if chunks:
            paragraphs = chunks[0].strip().split('\n\n')
            if paragraphs:
                intro.append(f"<blockquote>{paragraphs[0].strip()}</blockquote>")
        
        intro.append("</section>")
        return intro
    
    def _generate_main_content(self, chunks: list[str], style: dict) -> list[str]:
        """Generate main blog content."""
        content = []
        content.append("<section class='main-content'>")
        content.append("<h2>The Journey to Authenticity</h2>")
        
        # Process middle chunks
        sections = ['The Turning Point', 'Embracing Your Truth', 'Making an Impact']
        for i, chunk in enumerate(chunks[1:-1], 0):
            section_title = sections[min(i, len(sections)-1)]
            content.append(f"<section class='content-section'>")
            content.append(f"<h3>{section_title}</h3>")
            
            paragraphs = chunk.strip().split('\n\n')
            for p in paragraphs:
                if p.strip():
                    content.append(f"<p>{p.strip()}</p>")
            
            content.append("</section>")
        
        content.append("</section>")
        return content
    
    def _generate_conclusion(self, chunks: list[str], style: dict) -> list[str]:
        """Generate blog conclusion."""
        conclusion = []
        conclusion.append("<section class='conclusion'>")
        conclusion.append("<h2>Embracing Your Path</h2>")
        conclusion.append("<p>The journey to authenticity isn't always straightforward, but it's invariably worthwhile. When we stop trying to fit into someone else's mold and start embracing our unique perspectives, we don't just transform ourselves – we inspire others to do the same.</p>")
        
        # Use last chunk for conclusion
        if chunks:
            paragraphs = chunks[-1].strip().split('\n\n')
            if paragraphs:
                conclusion.append(f"<blockquote>{paragraphs[-1].strip()}</blockquote>")
        
        conclusion.append("</section>")
        return conclusion
