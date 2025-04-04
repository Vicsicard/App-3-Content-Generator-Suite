#!/usr/bin/env python3
"""
Test script to verify input file loading functionality.
"""

import sys
from pathlib import Path
from utils.input_loader import load_transcript, load_style_profile

def main():
    # Set up paths
    base_path = Path(__file__).parent / "output" / "for_app3"
    transcript_path = base_path / "transcript_chunks.md"
    style_profile_path = base_path / "style-profile.md"
    
    # Test file existence
    print("Checking input files...")
    if not transcript_path.exists():
        print(f"Error: Transcript file not found at {transcript_path}")
        return 1
    if not style_profile_path.exists():
        print(f"Error: Style profile file not found at {style_profile_path}")
        return 1
    
    try:
        # Load transcript
        transcript_content = load_transcript(str(transcript_path))
        print(f"Transcript loaded successfully:")
        print(f"Characters: {len(transcript_content)}")
        
        # Load style profile
        style_profile_content = load_style_profile(str(style_profile_path))
        print(f"Style profile loaded successfully:")
        print(f"Characters: {len(style_profile_content)}")
        
        print("\nAll files loaded successfully!")
        return 0
        
    except Exception as e:
        print(f"Error loading files: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
