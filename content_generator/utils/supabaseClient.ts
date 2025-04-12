import { createClient } from '@supabase/supabase-js';

const supabaseUrl = 'https://aqicztygjpmunfljjuto.supabase.co';
const supabaseAnonKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFxaWN6dHlnanBtdW5mbGpqdXRvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDM3MDU1ODIsImV4cCI6MjA1OTI4MTU4Mn0.5e2hvTckSSbTFLBjQiccrvjoBd6QQDX0X4tccFOc1rs';

export const supabase = createClient(supabaseUrl, supabaseAnonKey);

// Helper function to write content to Supabase
export async function writeContentToSupabase(
  section: string,
  content: string,
  options?: {
    title?: string;
    type?: string;
    platform?: string;
    scheduledDate?: string;
    caption?: string;
    tags?: string[];
  }
) {
  try {
    const { data, error } = await supabase
      .from('content')
      .insert([
        {
          section,
          content,
          status: 'draft',
          ...options
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
