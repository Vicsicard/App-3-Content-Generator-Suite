"""Input loading utilities for content generation."""

from pathlib import Path
from ..storage.input_storage import input_storage


def load_transcript(path: str) -> str:
    """
    Load transcript content from Supabase storage.
    
    Args:
        path: Path to transcript markdown file (ignored, using client_id instead)
        
    Returns:
        Full transcript content as string
    """
    try:
        # Fetch from Supabase storage
        transcript, _ = input_storage.fetch_input_files()
        char_count = len(transcript)
        print(f"Loaded transcript: {char_count} characters")
        return transcript
    except Exception as e:
        raise RuntimeError(f"Failed to load transcript: {str(e)}")


def load_style_profile(path: str) -> str:
    """
    Load style profile content from Supabase storage.
    
    Args:
        path: Path to style profile markdown file (ignored, using client_id instead)
        
    Returns:
        Full style profile content as string
    """
    try:
        # Fetch from Supabase storage
        _, style_profile = input_storage.fetch_input_files()
        char_count = len(style_profile)
        print(f"Loaded style profile: {char_count} characters")
        return style_profile
    except Exception as e:
        raise RuntimeError(f"Failed to load style profile: {str(e)}")
