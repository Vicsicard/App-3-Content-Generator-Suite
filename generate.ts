import * as fs from 'fs/promises';
import { generateBlogPost } from './content_generator/generators/blog_generator.ts';

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

    // Generate blog post
    console.log('Generating blog post...');
    console.log('Voice:', voice);
    console.log('Themes:', themes);
    await generateBlogPost(transcript, { voice, themes });
    console.log('Blog post generated successfully!');

  } catch (error) {
    console.error('Error generating content:', error);
    process.exit(1);
  }
}

main();
