import { writeContent } from '../utils/contentWriter.ts';

interface StyleProfile {
  voice: string[];
  themes: string[];
}

export async function generateBio(transcript: string, styleProfile: StyleProfile) {
  // Extract key insights from the transcript chunks
  const chunks = transcript.split('## [Chunk').slice(1);
  const insights = chunks.map(chunk => {
    const quote = chunk.match(/> Speaker \d+: (.+?)(?=\n|$)/)?.[1] || '';
    return quote.trim();
  }).filter(Boolean);

  // Create a compelling bio that captures Annie's authentic voice
  const bioContent = `# About Annie

I'm a leadership coach and speaker who believes in the power of authentic self-expression. ${insights[0].split('.')[0]}, and that journey has shaped everything I do today.

${insights[1]} This realization became the foundation of my coaching philosophy.

${insights[2]} Now, I help others discover their authentic leadership style and create meaningful impact in their own unique way.

## My Approach

I believe that true leadership emerges when we:
• Embrace our unique perspectives
• Trust our inner wisdom
• Show up authentically
• Create space for others to do the same

## What I Offer

• Leadership Development Programs
• One-on-One Coaching
• Speaking Engagements
• Workshop Facilitation

## My Values

${styleProfile.themes.slice(0, 5).map(theme => `• ${theme}`).join('\n')}

## Speaking Style

${styleProfile.voice.slice(0, 5).map(trait => `• ${trait}`).join('\n')}

Let's work together to unlock your authentic leadership potential and create lasting impact.`;

  await writeContent('output_bio.md', bioContent, {
    section: 'about',
    title: 'About Annie - Leadership Coach & Speaker',
    status: 'draft',
    tags: ['bio', 'about', 'leadership'],
    excerpt: "Leadership coach and speaker passionate about authentic self-expression and helping others create meaningful impact."
  });

  return bioContent;
}
