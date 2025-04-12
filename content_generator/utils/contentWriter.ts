import { supabase } from './supabaseClient';
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
}

export async function writeContent(
  filename: string,
  content: string,
  options?: ContentOptions
) {
  // Ensure output directories exist
  const outputDirs = ['output/app3', 'output/for_app4'];
  await Promise.all(
    outputDirs.map(dir => fs.mkdir(dir, { recursive: true }))
  );

  // Write to files (maintain backward compatibility)
  await Promise.all(
    outputDirs.map(dir => 
      fs.writeFile(
        path.join(dir, filename),
        content,
        'utf-8'
      )
    )
  );

  // Map filename to section if not provided
  const section = options?.section || mapFilenameToSection(filename);
  
  // Special handling for Instagram posts
  if (options?.platform === 'instagram') {
    // Generate visual content filename
    const visualFilename = filename.replace('.md', '_visual.png');
    
    // Save placeholder for visual content
    await Promise.all(
      outputDirs.map(dir =>
        fs.writeFile(
          path.join(dir, visualFilename),
          'Placeholder for Instagram visual', // This would be replaced with actual image generation
          'utf-8'
        )
      )
    );

    // Update options with visual content path
    options.thumbnail = `output/app3/${visualFilename}`;
  }

  // Write to Supabase
  try {
    const { data, error } = await supabase
      .from('content')
      .insert([
        {
          section,
          content,
          status: options?.status || 'draft',
          title: options?.title,
          type: options?.type,
          platform: options?.platform,
          scheduledDate: options?.scheduledDate,
          caption: options?.caption,
          tags: options?.tags,
          thumbnail: options?.thumbnail,
          video_id: options?.video_id,
          updated_at: new Date().toISOString()
        }
      ])
      .select();

    if (error) throw error;
    return data;
  } catch (error) {
    console.error('Error writing to Supabase:', error);
    // Don't throw - allow file writing to continue even if DB fails
    return null;
  }
}

function mapFilenameToSection(filename: string): string {
  const mapping: Record<string, string> = {
    'output_blog.md': 'blog',
    'output_bio.md': 'about',
    'output_social_kit.md': 'social',
    'output_newsletter.md': 'blog',
    'output_show_notes.md': 'blog',
    'output_ad_copy.md': 'social',
    'output_reputation.md': 'blog'
  };
  
  return mapping[filename] || 'blog';
}
