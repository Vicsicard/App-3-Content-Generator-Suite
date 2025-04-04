"""Input loading utilities for content generation."""

from pathlib import Path


def load_transcript(path: str) -> str:
    """
    Load transcript content from markdown file.
    
    Args:
        path: Path to transcript markdown file
        
    Returns:
        Full transcript content as string
    """
    transcript_path = Path(path)
    if not transcript_path.exists():
        raise FileNotFoundError(f"Transcript file not found: {path}")
        
    content = transcript_path.read_text(encoding='utf-8')
    char_count = len(content)
    print(f"Loaded transcript: {char_count} characters")
    return content


def load_style_profile(path: str) -> str:
    """
    Load style profile content from markdown file.
    
    Args:
        path: Path to style profile markdown file
        
    Returns:
        Full style profile content as string
    """
    profile_path = Path(path)
    if not profile_path.exists():
        raise FileNotFoundError(f"Style profile not found: {path}")
        
    content = profile_path.read_text(encoding='utf-8')
    char_count = len(content)
    print(f"Loaded style profile: {char_count} characters")
    return content
