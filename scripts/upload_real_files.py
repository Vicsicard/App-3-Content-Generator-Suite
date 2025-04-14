"""Script to upload real input files to Supabase storage."""

import os
from pathlib import Path
from supabase import create_client

def upload_real_files():
    """Upload real input files to Supabase storage."""
    # Initialize Supabase client
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    
    if not supabase_url or not supabase_key:
        raise ValueError("Supabase URL and key must be set in environment variables")
        
    client = create_client(supabase_url, supabase_key)
    bucket_name = "content"
    
    # Get real file paths
    project_root = Path(__file__).parent.parent
    transcript_file = project_root / "input" / "transcript_chunks.md"
    style_file = project_root / "input" / "style-profile.md"
    
    if not transcript_file.exists():
        raise FileNotFoundError(f"Transcript file not found at {transcript_file}")
    if not style_file.exists():
        raise FileNotFoundError(f"Style profile file not found at {style_file}")
    
    # Read file contents
    transcript = transcript_file.read_text(encoding='utf-8')
    style_profile = style_file.read_text(encoding='utf-8')
    
    # Create paths
    client_id = "annie"
    base_path = f"client-files/{client_id}"
    transcript_path = f"{base_path}/transcript_chunks.md"
    style_path = f"{base_path}/style-profile.md"
    
    # Upload files
    try:
        # Upload transcript
        client.storage.from_(bucket_name).upload(
            path=transcript_path,
            file=transcript.encode(),
            file_options={"content-type": "text/markdown"}
        )
        print(f"Uploaded {transcript_path}")
        
        # Upload style profile
        client.storage.from_(bucket_name).upload(
            path=style_path,
            file=style_profile.encode(),
            file_options={"content-type": "text/markdown"}
        )
        print(f"Uploaded {style_path}")
        
    except Exception as e:
        print(f"Error uploading files: {str(e)}")

if __name__ == "__main__":
    upload_real_files()
