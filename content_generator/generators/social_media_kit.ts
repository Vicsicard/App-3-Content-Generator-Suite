import {
  generateLinkedInPost,
  generateTwitterPost,
  generateInstagramPost,
  generateFacebookPost
} from './social';
import { writeContent } from '../utils/contentWriter';

export async function generateSocialMediaKit(transcript: string, styleProfile: any) {
  // Generate platform-specific content
  const linkedinContent = await generateLinkedInPost(transcript, styleProfile);
  const twitterContent = await generateTwitterPost(transcript, styleProfile);
  const instagramContent = await generateInstagramPost(transcript, styleProfile);
  const facebookContent = await generateFacebookPost(transcript, styleProfile);

  // Combine all content into a kit
  const socialKitContent = `# Social Media Content Kit

## LinkedIn Post
${linkedinContent}

## Twitter Post
${twitterContent}

## Instagram Post
${instagramContent}

## Facebook Post
${facebookContent}`;

  // Save the combined kit to file (for backward compatibility)
  await writeContent('output_social_kit.md', socialKitContent, {
    section: 'social',
    title: 'Social Media Content Kit',
    status: 'draft'
  });

  return socialKitContent;
}
