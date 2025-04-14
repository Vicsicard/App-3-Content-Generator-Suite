import { createClient } from '@supabase/supabase-js';
import dotenv from 'dotenv';

dotenv.config();

const supabaseUrl = process.env.SUPABASE_URL;
const supabaseKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

export const supabase = supabaseUrl && supabaseKey ? createClient(supabaseUrl, supabaseKey) : undefined;

export interface ContentWriteOptions {
  section?: string;
  content: string;
  title?: string;
  status?: string;
  tags?: string[];
  excerpt?: string;
}

export async function writeContentToSupabase(
  section: string,
  content: string,
  options?: ContentWriteOptions
) {
  if (!supabase) {
    console.warn('Supabase client not initialized - skipping database write');
    return null;
  }

  try {
    const { data, error } = await supabase
      .from('content')
      .insert([
        {
          section,
          content,
          status: options?.status || 'draft',
          title: options?.title,
          tags: options?.tags,
          excerpt: options?.excerpt,
          updated_at: new Date().toISOString()
        }
      ])
      .select();

    if (error) throw error;
    return data;
  } catch (error) {
    console.error('Error writing to Supabase:', error);
    throw error;
  }
}
