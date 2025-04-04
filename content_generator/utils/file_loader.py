"""
File loader utility for Content Generator Suite.
Handles loading and validation of input markdown files.
"""

from pathlib import Path
from typing import Tuple


def load_input_files(transcript_path: str, style_profile_path: str) -> Tuple[str, str]:
    """
    Load and validate the input markdown files.
    
    Args:
        transcript_path (str): Path to transcript_chunks.md
        style_profile_path (str): Path to style-profile.md
        
    Returns:
        Tuple[str, str]: Contents of transcript and style profile files
        
    Raises:
        FileNotFoundError: If either file doesn't exist
        ValueError: If files are empty or invalid
    """
    # Convert to Path objects for better handling
    transcript_file = Path(transcript_path)
    style_profile_file = Path(style_profile_path)
    
    # Validate file existence
    if not transcript_file.exists():
        raise FileNotFoundError(f"Transcript file not found: {transcript_path}")
    if not style_profile_file.exists():
        raise FileNotFoundError(f"Style profile file not found: {style_profile_path}")
        
    # Validate file extensions
    if transcript_file.suffix.lower() != '.md':
        raise ValueError(f"Transcript file must be .md format: {transcript_path}")
    if style_profile_file.suffix.lower() != '.md':
        raise ValueError(f"Style profile file must be .md format: {style_profile_path}")
    
    # Read file contents
    transcript_content = transcript_file.read_text(encoding='utf-8').strip()
    style_profile_content = style_profile_file.read_text(encoding='utf-8').strip()
    
    # Validate content
    if not transcript_content:
        raise ValueError(f"Transcript file is empty: {transcript_path}")
    if not style_profile_content:
        raise ValueError(f"Style profile file is empty: {style_profile_path}")
        
    return transcript_content, style_profile_content
