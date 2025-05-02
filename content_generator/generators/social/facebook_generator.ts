import { writeContent } from '../../utils/contentWriter.ts';

interface StyleProfile {
  voice: string[];
  themes: string[];
}

export async function generateFacebookPost(transcript: string, styleProfile: StyleProfile) {
  // Extract key insights from the transcript chunks
  const chunks = transcript.split('## [Chunk').slice(1);
  const insights = chunks.map(chunk => {
    const quote = chunk.match(/> Speaker \d+: (.+?)(?=\n|$)/)?.[1] || '';
    return quote.trim();
  }).filter(Boolean);

  // Create an engaging Facebook post
  const mainQuote = insights[0]; // Use the first insight as the main quote
  const reflection = insights[1]; // Use the second insight for reflection
  const callToAction = insights[2]; // Use the third insight for call to action

  // Generate an excerpt that summarizes the content
  const excerpt = `A focused discussion on authentic leadership featuring insights on personal growth, finding your path, and challenging conventional wisdom.`;

  const facebookContent = `# Finding Your Authentic Path 

${mainQuote}

This really hit home for me. So often, we get caught up in trying to follow someone else's roadmap to success, but here's what I've learned:

${reflection}

And you know what's amazing? ${callToAction}

What's your experience with finding your authentic path? Has there been a moment when you realized you needed to chart your own course? Share your story below! 

#AuthenticLeadership #PersonalGrowth #FindingYourPath`;

  await writeContent('output_facebook.md', facebookContent, {
    section: 'facebook',
    title: "Finding Your Authentic Path: A Leadership Journey",
    platform: 'facebook',
    caption: 'Authenticity and personal growth journey',
    excerpt: excerpt, // Added excerpt field
    scheduledDate: new Date().toISOString(),
    status: 'draft',
    tags: ['leadership', 'authenticity', 'personal-growth']
  });

  return facebookContent;
}
