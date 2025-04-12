import { writeContent } from '../../utils/contentWriter';

export async function generateLinkedInPost(transcript: string, styleProfile: any) {
  // LinkedIn-specific requirements:
  // - Professional tone
  // - Up to 3000 characters
  // - Supports hashtags
  // - Can include multiple paragraphs
  const linkedInContent = `# LinkedIn Post
This is a professional post for LinkedIn.

Key points:
- Professional insight
- Industry expertise
- Thought leadership

#ProfessionalDevelopment #Leadership`;

  await writeContent('output_linkedin.md', linkedInContent, {
    section: 'social',
    platform: 'linkedin',
    caption: 'Professional insights and thought leadership',
    scheduledDate: new Date().toISOString(),
    status: 'draft',
    tags: ['professional', 'leadership']
  });

  return linkedInContent;
}
