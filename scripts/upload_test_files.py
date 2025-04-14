"""Script to upload test files to Supabase storage."""

import os
from supabase import create_client

def upload_test_files():
    """Upload test files to Supabase storage."""
    # Initialize Supabase client
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    
    if not supabase_url or not supabase_key:
        raise ValueError("Supabase URL and key must be set in environment variables")
        
    client = create_client(supabase_url, supabase_key)
    bucket_name = "content"
    
    # Sample content
    transcript = """### Chunk 1
In this episode, we dive deep into the fascinating world of AI and its impact on modern business.
Our guest expert shares insights on how companies can leverage machine learning to transform their operations.

### Chunk 2
The discussion then moves to practical implementation strategies and common pitfalls to avoid.
Real-world examples demonstrate both successes and failures in AI adoption.

### Chunk 3
We conclude with future predictions and actionable advice for businesses looking to start their AI journey.
Key takeaways include the importance of data quality and building the right team."""

    style_profile = """## Voice:
- Professional yet approachable
- Tech-savvy but not overly technical
- Engaging and conversational

## Themes:
- AI and machine learning
- Business transformation
- Practical implementation
- Future trends

## Values:
- Innovation
- Education
- Practicality
- Accessibility

## Emotional Tone:
- Optimistic
- Confident
- Thoughtful
- Encouraging

## Relatability:
- Speaks to both technical and non-technical audiences
- Uses real-world examples
- Acknowledges challenges while offering solutions"""

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
    upload_test_files()
