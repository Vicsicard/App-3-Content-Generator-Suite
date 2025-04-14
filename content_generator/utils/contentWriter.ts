import { supabase } from './supabaseClient.ts';
import * as fs from 'fs/promises';
import * as path from 'path';

interface ContentOptions {
  section?: string;
  title?: string;
  type?: string;
  platform?: 'linkedin' | 'facebook' | 'instagram' | 'twitter';
  scheduledDate?: string;
  caption?: string;
  tags?: string[];
  status?: 'draft' | 'approved' | 'published';
  thumbnail?: string;
  video_id?: string;
  excerpt?: string;
  user_id?: string;
}

export async function writeContent(
  filename: string,
  content: string,
  options?: ContentOptions
) {
  // Default user_id for Annie's content
  const defaultUserId = 'annie-123';  // We should get this from environment or config
  const userId = options?.user_id || defaultUserId;

  // Ensure output directories exist
  const outputDirs = ['output/app3', 'output/for_app4'];
  await Promise.all(
    outputDirs.map(dir => fs.mkdir(dir, { recursive: true }))
  );

  // Write to files (maintain backward compatibility)
  await Promise.all(
    outputDirs.map(dir => 
      fs.writeFile(path.join(dir, filename), content, 'utf-8')
    )
  );

  // Write to Supabase if configured
  if (supabase && options?.section) {
    try {
      // First, check if content already exists for this user and section
      const { data: existingContent, error: fetchError } = await supabase
        .from('content')
        .select('id')
        .eq('user_id', userId)
        .eq('section', options.section)
        .eq('platform', options.platform || null)  // Include platform for social posts
        .single();

      if (fetchError && fetchError.code !== 'PGRST116') {  // PGRST116 is "not found" error
        console.error('Error checking for existing content:', fetchError);
        throw fetchError;
      }

      let result;
      if (existingContent?.id) {
        // Update existing content
        result = await supabase
          .from('content')
          .update({
            content,
            title: options.title,
            type: options.type,
            platform: options.platform,
            scheduled_date: options.scheduledDate,
            caption: options.caption,
            tags: options.tags,
            status: options.status || 'draft',
            thumbnail: options.thumbnail,
            video_id: options.video_id,
            excerpt: options.excerpt,
            updated_at: new Date().toISOString()
          })
          .eq('id', existingContent.id)
          .select();
      } else {
        // Insert new content
        result = await supabase
          .from('content')
          .insert([
            {
              content,
              section: options.section,
              title: options.title,
              type: options.type,
              platform: options.platform,
              scheduled_date: options.scheduledDate,
              caption: options.caption,
              tags: options.tags,
              status: options.status || 'draft',
              thumbnail: options.thumbnail,
              video_id: options.video_id,
              excerpt: options.excerpt,
              user_id: userId
            }
          ])
          .select();
      }

      if (result.error) {
        console.error('Error writing to Supabase:', result.error);
        throw result.error;
      }

      const action = existingContent ? 'Updated' : 'Created';
      console.log(`${action} ${options.section} content for user ${userId}`);

    } catch (error) {
      console.error('Error writing to Supabase:', error);
      throw error;
    }
  }
}

// Helper function to map filenames to content sections
function mapFilenameToSection(filename: string): string {
  const sectionMap: { [key: string]: string } = {
    'output_blog.md': 'blog',
    'output_social_posts.md': 'social',
    'output_newsletter.md': 'newsletter'
  };
  return sectionMap[filename] || 'other';
}
