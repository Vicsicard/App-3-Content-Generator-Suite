import { writeContent } from '../utils/contentWriter';

export async function generateBio(transcript: string, styleProfile: any) {
  // Your existing bio generation logic here
  const bioContent = `# Test Bio
This is test bio content.`;

  // Write to both file and database
  await writeContent('output_bio.md', bioContent, {
    section: 'about',
    title: 'About Me',
    status: 'draft'
  });

  return bioContent;
}
