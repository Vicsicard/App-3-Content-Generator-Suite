import { writeContent } from '../../utils/contentWriter';

export async function generateTwitterPost(transcript: string, styleProfile: any) {
  // Twitter-specific requirements:
  // - 280 character limit
  // - Supports hashtags
  // - More casual tone
  // - Thread support
  const twitterContent = `# Twitter Post
Quick insight: Leadership is about empowering others.

Follow up with actionable tips in thread below 🧵

#Leadership #Growth`;

  await writeContent('output_twitter.md', twitterContent, {
    section: 'social',
    platform: 'twitter',
    caption: 'Leadership insights thread',
    scheduledDate: new Date().toISOString(),
    status: 'draft',
    tags: ['leadership', 'thread']
  });

  return twitterContent;
}
