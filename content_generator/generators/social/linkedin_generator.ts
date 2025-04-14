import { writeContent } from '../../utils/contentWriter.ts';

interface StyleProfile {
  voice: string[];
  themes: string[];
}

export async function generateLinkedInPost(transcript: string, styleProfile: StyleProfile) {
  // Extract key insights from the transcript chunks
  const chunks = transcript.split('## [Chunk').slice(1);
  const insights = chunks.map(chunk => {
    const quote = chunk.match(/> Speaker \d+: (.+?)(?=\n|$)/)?.[1] || '';
    return quote.trim();
  }).filter(Boolean);

  // Create a professional LinkedIn post
  const mainQuote = insights[0]; // Use the first insight as the main quote
  const reflection = insights[1]; // Use the second insight for reflection
  const callToAction = insights[2]; // Use the third insight for call to action

  const linkedInContent = `# The Power of Authentic Leadership

One of the most profound realizations in my leadership journey has been this:

"${mainQuote}"

This insight fundamentally changed my approach to leadership and personal growth. Here's what I discovered:

${reflection}

The results have been transformative:
• Deeper connections with team members
• More innovative solutions emerging naturally
• Increased trust and psychological safety
• Authentic, purpose-driven culture

Most importantly: ${callToAction}

What's been your experience with authentic leadership? How has staying true to your unique perspective influenced your professional journey?

#AuthenticLeadership #ProfessionalDevelopment #PersonalGrowth #LeadershipJourney`;

  await writeContent('output_linkedin.md', linkedInContent, {
    section: 'linkedin',
    title: "The Power of Authentic Leadership: Professional Insights",
    platform: 'linkedin',
    caption: 'Thought leadership on authentic leadership',
    scheduledDate: new Date().toISOString(),
    status: 'draft',
    tags: ['leadership', 'coaching', 'authenticity']
  });

  return linkedInContent;
}
