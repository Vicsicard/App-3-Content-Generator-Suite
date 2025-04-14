"""Show notes generator agent."""

from .base_agent import ContentAgent

class ShowNotesWriter(ContentAgent):
    """Generates show notes from transcript chunks."""
    
    def generate(self, transcript: str, style_profile: str) -> str:
        """Generate show notes from transcript and style profile.
        
        Args:
            transcript: Content from transcript_chunks.md
            style_profile: Content from style-profile.md
            
        Returns:
            Generated show notes as HTML string
        """
        # Extract style elements and chunks
        style = self._extract_style_elements(style_profile)
        chunks = self._get_chunks(transcript)
        
        # Generate show notes
        notes = []
        
        # Add header
        notes.append("<article class='show-notes'>")
        notes.append("<h1>Episode Show Notes</h1>")
        
        # Generate sections
        notes.extend(self._generate_overview(chunks, style))
        notes.extend(self._generate_key_points(chunks, style))
        notes.extend(self._generate_resources(chunks, style))
        
        # Add footer
        notes.append("<section class='connect'>")
        notes.append("<h2>Connect With Us</h2>")
        notes.append("<p>Want to continue the conversation? Connect with us on social media or visit our website.</p>")
        notes.append("</section>")
        notes.append("</article>")
        
        return '\n'.join(notes)
    
    def _generate_overview(self, chunks: list[str], style: dict) -> list[str]:
        """Generate overview section."""
        overview = []
        overview.append("<section class='overview'>")
        overview.append("<h2>Episode Overview</h2>")
        
        # Use first chunk for overview
        if chunks:
            paragraphs = chunks[0].strip().split('\n\n')
            for p in paragraphs:
                if p.strip():
                    overview.append(f"<p>{p.strip()}</p>")
        
        overview.append("</section>")
        return overview
    
    def _generate_key_points(self, chunks: list[str], style: dict) -> list[str]:
        """Generate key points section."""
        points = []
        points.append("<section class='key-points'>")
        points.append("<h2>Key Points</h2>")
        points.append("<ul>")
        
        # Process middle chunks for key points
        for chunk in chunks[1:-1]:
            paragraphs = chunk.strip().split('\n\n')
            for p in paragraphs:
                if p.strip():
                    points.append(f"<li>{p.strip()}</li>")
        
        points.append("</ul>")
        points.append("</section>")
        return points
    
    def _generate_resources(self, chunks: list[str], style: dict) -> list[str]:
        """Generate resources section."""
        resources = []
        resources.append("<section class='resources'>")
        resources.append("<h2>Resources & Links</h2>")
        
        # Use last chunk for resources
        if chunks:
            paragraphs = chunks[-1].strip().split('\n\n')
            for p in paragraphs:
                if p.strip():
                    resources.append(f"<p>{p.strip()}</p>")
        
        resources.append("</section>")
        return resources
