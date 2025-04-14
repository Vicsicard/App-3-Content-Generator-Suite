"""Bio generator agent."""

from .base_agent import ContentAgent

class BioWriter(ContentAgent):
    """Generates bio content from transcript chunks."""
    
    def generate(self, transcript: str, style_profile: str) -> str:
        """Generate bio content from transcript and style profile.
        
        Args:
            transcript: Content from transcript_chunks.md
            style_profile: Content from style-profile.md
            
        Returns:
            Generated bio as HTML string
        """
        # Extract style elements and chunks
        style = self._extract_style_elements(style_profile)
        chunks = self._get_chunks(transcript)
        
        # Generate bio
        bio = []
        
        # Add header
        bio.append("<article class='bio'>")
        bio.append("<h1>Professional Biography</h1>")
        
        # Generate sections
        bio.extend(self._generate_overview(chunks, style))
        bio.extend(self._generate_expertise(chunks, style))
        bio.extend(self._generate_impact(chunks, style))
        
        # Add footer
        bio.append("<section class='connect'>")
        bio.append("<h2>Let's Connect</h2>")
        bio.append("<p>Ready to explore how we can create meaningful impact together? Let's connect and discuss how my unique perspective can benefit your organization.</p>")
        bio.append("</section>")
        bio.append("</article>")
        
        return '\n'.join(bio)
    
    def _generate_overview(self, chunks: list[str], style: dict) -> list[str]:
        """Generate overview section."""
        overview = []
        overview.append("<section class='overview'>")
        overview.append("<h2>Professional Overview</h2>")
        
        # Add intro text
        overview.append("<p>A transformative leader and authentic voice in professional development, I specialize in helping individuals and organizations unlock their unique potential through embracing authenticity and purposeful growth.</p>")
        
        # Use first chunk for key quote
        if chunks:
            paragraphs = chunks[0].strip().split('\n\n')
            if paragraphs:
                overview.append(f"<blockquote>{paragraphs[0].strip()}</blockquote>")
        
        overview.append("</section>")
        return overview
    
    def _generate_expertise(self, chunks: list[str], style: dict) -> list[str]:
        """Generate expertise section."""
        expertise = []
        expertise.append("<section class='expertise'>")
        expertise.append("<h2>Areas of Expertise</h2>")
        
        # Add core expertise areas
        expertise.append("<ul>")
        expertise.append("<li><strong>Authentic Leadership Development:</strong> Guiding professionals to lead with authenticity and purpose</li>")
        expertise.append("<li><strong>Strategic Vision & Impact:</strong> Creating meaningful change through purposeful action and clear direction</li>")
        expertise.append("<li><strong>Personal Brand Development:</strong> Helping individuals articulate and leverage their unique value proposition</li>")
        
        # Add themes from style profile
        if style.get('themes'):
            for theme in style['themes']:
                expertise.append(f"<li><strong>{theme.title()}:</strong> Empowering others to embrace their authentic strengths</li>")
        
        expertise.append("</ul>")
        expertise.append("</section>")
        return expertise
    
    def _generate_impact(self, chunks: list[str], style: dict) -> list[str]:
        """Generate impact section."""
        impact = []
        impact.append("<section class='impact'>")
        impact.append("<h2>Impact & Results</h2>")
        
        # Add impact intro
        impact.append("<p>Through my work in authentic leadership and professional development, I have:</p>")
        
        # Add achievements
        impact.append("<ul>")
        impact.append("<li>Guided professionals in discovering and leveraging their authentic leadership style</li>")
        impact.append("<li>Developed frameworks for translating personal insights into actionable growth strategies</li>")
        impact.append("<li>Created lasting impact through authentic connection and purposeful engagement</li>")
        
        # Use last chunk for additional achievements
        if chunks:
            paragraphs = chunks[-1].strip().split('\n\n')
            for p in paragraphs:
                if p.strip():
                    impact.append(f"<li>{p.strip()}</li>")
        
        impact.append("</ul>")
        impact.append("</section>")
        return impact
