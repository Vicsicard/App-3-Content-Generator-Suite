import { writeContent } from '../../utils/contentWriter.ts';

interface StyleProfile {
  voice: string[];
  themes: string[];
}

export async function generateInstagramPost(transcript: string, styleProfile: StyleProfile) {
  // Extract key insights from the transcript chunks
  const chunks = transcript.split('## [Chunk').slice(1);
  const insights = chunks.map(chunk => {
    const quote = chunk.match(/> Speaker \d+: (.+?)(?=\n|$)/)?.[1] || '';
    return quote.trim();
  }).filter(Boolean);

  // Create an engaging Instagram post
  const mainQuote = insights[0]; // Use the first insight as the main quote
  const reflection = insights[1]; // Use the second insight for reflection
  
  // Generate an excerpt that summarizes the content
  const excerpt = `A visually engaging post focusing on professional development with actionable insights and thoughtful reflections on career growth.`;

  const instagramContent = `# Level Up Your Leadership Game 

"${mainQuote}"

This insight changed everything for me. When we focus on authenticity rather than perfection, we create space for real growth.

Three ways I've applied this in my own journey:
1 Embracing vulnerability as a leadership strength
2 Prioritizing connection over projection
3 Finding opportunities in challenges

As ${reflection} reminds us, the path isn't always straight, but it's worth it.

What's one authentic leadership practice that's transformed your approach? Share below! 

#LeadershipJourney #AuthenticityMatters #GrowthMindset #ProfessionalDevelopment`;

  await writeContent('output_instagram.md', instagramContent, {
    section: 'instagram',
    title: "Authentic Leadership: Level Up Your Game",
    platform: 'instagram',
    caption: 'Leadership insights and growth mindset',
    excerpt: excerpt, 
    scheduledDate: new Date().toISOString(),
    status: 'draft',
    tags: ['leadership', 'growth', 'authenticity', 'development']
  });

  return instagramContent;
}
