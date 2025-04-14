import { writeContent } from '../utils/contentWriter.ts';

interface StyleProfile {
  voice: string[];
  themes: string[];
}

export async function generateBlogPost(transcript: string, styleProfile: StyleProfile) {
  // Extract key insights from the transcript chunks
  const chunks = transcript.split('## [Chunk').slice(1);
  const insights = chunks.map(chunk => {
    const quote = chunk.match(/> Speaker \d+: (.+?)(?=\n|$)/)?.[1] || '';
    return quote.trim();
  }).filter(Boolean);

  // Create blog post structure
  const title = "Finding Your Authentic Path: A Journey of Self-Discovery";
  const introduction = `In a world where everyone seems to have a pre-written script for success, finding your own authentic path can feel like navigating uncharted territory. Today, we explore a personal journey that demonstrates how embracing your unique perspective can lead to genuine impact and meaningful connections.`;

  const mainContent = insights.map(insight => {
    // Transform each insight into a blog section
    return `## ${insight.split('.')[0]}
    
${insight}

${generateReflection(insight, styleProfile)}`;
  }).join('\n\n');

  const conclusion = `The journey to authenticity isn't always straightforward, but it's invariably worthwhile. When we stop trying to fit into someone else's mold and start embracing our unique perspectives, we don't just transform ourselves – we inspire others to do the same.`;

  const blogContent = `# ${title}

${introduction}

${mainContent}

${conclusion}`;

  // Write to both file and database
  await writeContent('output_blog.md', blogContent, {
    section: 'blog',
    title,
    tags: ['personal-growth', 'authenticity', 'leadership', 'self-discovery'],
    excerpt: introduction.split('.')[0] + '.',
    status: 'draft'
  });
  
  return blogContent;
}

function generateReflection(insight: string, styleProfile: StyleProfile): string {
  // Use style profile themes to generate relevant reflections
  const themes = styleProfile.themes || [];
  
  // Map themes to reflective questions and insights
  const reflections = themes
    .filter(theme => insight.toLowerCase().includes(theme.toLowerCase()))
    .map(theme => {
      switch (theme) {
        case 'Personal growth':
          return 'This moment of realization exemplifies how personal growth often comes from challenging our existing beliefs.';
        case 'Finding purpose':
          return 'When we align our actions with our authentic purpose, the path forward becomes clearer.';
        default:
          return 'This insight reflects a deeper truth about our journey toward authenticity and purpose.';
      }
    });

  return reflections[0] || 'This realization opens up new possibilities for growth and connection.';
}
