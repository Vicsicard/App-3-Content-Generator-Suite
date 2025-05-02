import { writeContent } from '../../utils/contentWriter.ts';

interface StyleProfile {
  voice: string[];
  themes: string[];
}

export async function generateTwitterPost(transcript: string, styleProfile: StyleProfile) {
  // Extract key sentences from the transcript chunks
  const chunks = transcript.split('## [Chunk').slice(1);
  const insights = chunks.map(chunk => {
    const quote = chunk.match(/> Speaker \d+: (.+?)(?=\n|$)/)?.[1] || '';
    return quote.trim();
  }).filter(Boolean).slice(0, 3);

  // Generate a concise Twitter post
  const selectedInsight = insights[0] || "The key to success is authenticity and staying true to your values.";
  
  // Generate an excerpt that summarizes the content
  const excerpt = `A concise reflection on leadership principles and authentic connection with your audience.`;

  // Make sure the tweet is under 280 characters
  let tweetContent = `"${selectedInsight.substring(0, 200)}" 

What's your take on this? #Leadership #Authenticity #Growth`;

  // Ensure tweet is under character limit
  if (tweetContent.length > 280) {
    tweetContent = tweetContent.substring(0, 277) + '...';
  }

  await writeContent('output_twitter.md', tweetContent, {
    section: 'twitter',
    title: "Leadership Insight of the Day",
    platform: 'twitter',
    caption: 'Thought-provoking leadership quote',
    excerpt: excerpt, 
    scheduledDate: new Date().toISOString(),
    status: 'draft',
    tags: ['leadership', 'quote', 'insight']
  });

  return tweetContent;
}
