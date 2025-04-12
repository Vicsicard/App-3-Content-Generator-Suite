import { writeContent } from '../utils/contentWriter';

export async function generateBlogPost(transcript: string, styleProfile: any) {
  // Your existing blog generation logic here
  const blogContent = `# Test Blog Post
This is a test blog post content.`;

  // Write to both file and database
  await writeContent('output_blog.md', blogContent, {
    section: 'blog',
    title: 'Test Blog Post',
    tags: ['test'],
    excerpt: 'This is a test blog post.',
    status: 'draft'
  });

  return blogContent;
}
