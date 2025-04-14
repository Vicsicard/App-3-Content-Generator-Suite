import * as fs from 'fs/promises';
import { generateBlogPost } from './content_generator/generators/blog_generator.ts';
import { generateFacebookPost } from './content_generator/generators/social/facebook_generator.ts';
import { generateInstagramPost } from './content_generator/generators/social/instagram_generator.ts';
import { generateLinkedInPost } from './content_generator/generators/social/linkedin_generator.ts';
import { generateTwitterPost } from './content_generator/generators/social/twitter_generator.ts';
import { generateWebsiteContent } from './content_generator/generators/website_generator.ts';

async function main() {
  try {
    // Read input files
    const styleProfile = await fs.readFile('./input/style-profile.md', 'utf-8');
    const transcript = await fs.readFile('./input/transcript_chunks.md', 'utf-8');

    // Parse style profile sections
    const sections = styleProfile.split('##').filter(Boolean);
    const voiceSection = sections.find(section => section.trim().startsWith('voice:'));
    const themesSection = sections.find(section => section.trim().startsWith('themes:'));

    if (!voiceSection || !themesSection) {
      throw new Error('Could not find voice or themes sections in style profile');
    }

    const voice = voiceSection
      .split('\n')
      .filter(line => line.trim().startsWith('- '))
      .map(line => line.trim().slice(2))
      .filter(Boolean);

    const themes = themesSection
      .split('\n')
      .filter(line => line.trim().startsWith('- '))
      .map(line => line.trim().slice(2))
      .filter(Boolean);

    const styleProfileData = { voice, themes };

    // Generate all content
    console.log('Generating blog post...');
    await generateBlogPost(transcript, styleProfileData);
    console.log('Blog post generated successfully!');

    console.log('\nGenerating website content...');
    await generateWebsiteContent(transcript, styleProfileData);
    console.log('Website content generated successfully!');

    console.log('\nGenerating social media posts...');
    
    console.log('Generating Facebook post...');
    await generateFacebookPost(transcript, styleProfileData);
    console.log('Facebook post generated successfully!');

    console.log('Generating Instagram post...');
    await generateInstagramPost(transcript, styleProfileData);
    console.log('Instagram post generated successfully!');

    console.log('Generating LinkedIn post...');
    await generateLinkedInPost(transcript, styleProfileData);
    console.log('LinkedIn post generated successfully!');

    console.log('Generating Twitter post...');
    await generateTwitterPost(transcript, styleProfileData);
    console.log('Twitter post generated successfully!');

    console.log('\nAll content generated successfully!');

  } catch (error) {
    console.error('Error generating content:', error);
    process.exit(1);
  }
}

main();
