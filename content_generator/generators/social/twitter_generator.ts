import { writeContent } from '../../utils/contentWriter.ts';

interface StyleProfile {
  voice: string[];
  themes: string[];
}

export async function generateTwitterPost(transcript: string, styleProfile: StyleProfile) {
  // Extract key insights from the transcript chunks
  const chunks = transcript.split('## [Chunk').slice(1);
  const insights = chunks.map(chunk => {
    const quote = chunk.match(/> Speaker \d+: (.+?)(?=\n|$)/)?.[1] || '';
    return quote.trim();
  }).filter(Boolean);

  // Create a Twitter thread
  const mainQuote = insights[0]; // Use the first insight as the main quote
  const reflection = insights[1]; // Use the second insight for reflection
  const callToAction = insights[2]; // Use the third insight for call to action

  const twitterContent = `# Finding Your Path - A Thread 

1/ Truth bomb: ${mainQuote.split('.')[0]}.

2/ The journey wasn't easy. ${reflection.split('.')[0]}.

3/ The game-changer? ${callToAction.split('.')[0]}.

4/ Your uniqueness isn't just a differentiator—it's your superpower.

5/ Stop following others' blueprints. Start creating your own.

6/ Remember: authenticity attracts authenticity.

#AuthenticLeadership #BeYourself`;

  await writeContent('output_twitter.md', twitterContent, {
    section: 'twitter',
    title: "Authentic Leadership Thread: Key Insights",
    platform: 'twitter',
    caption: 'Thread on authentic leadership insights',
    scheduledDate: new Date().toISOString(),
    status: 'draft',
    tags: ['leadership', 'authenticity', 'thread']
  });

  return twitterContent;
}
