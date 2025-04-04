#!/usr/bin/env python3
"""
Test script to verify blog generator requirements
"""

import re
from pathlib import Path
from agents.blog_generator import generate


def count_words(text: str) -> int:
    """Count words in text, excluding markdown symbols."""
    # Remove markdown symbols and extra whitespace
    clean_text = re.sub(r'[#*_\->`]', '', text)
    words = clean_text.split()
    return len(words)


def check_voice_consistency(blog_text: str, style_profile: str) -> bool:
    """Check if blog maintains voice from style profile."""
    # Extract voice characteristics from style profile
    voice_markers = ['professional', 'casual', 'formal', 'conversational']
    profile_voice = [m for m in voice_markers if m.lower() in style_profile.lower()]
    
    # Check if these markers appear consistently in the blog
    if profile_voice:
        blog_lower = blog_text.lower()
        # Simple check: voice markers should appear proportionally in the text
        return any(m in blog_lower for m in profile_voice)
    return True


def verify_markdown_structure(blog_text: str) -> bool:
    """Verify proper markdown structure."""
    required_elements = [
        (r'^# .+', 'Main title'),
        (r'## Introduction', 'Introduction section'),
        (r'## Section \d+:', 'Numbered sections'),
        (r'## Conclusion', 'Conclusion section'),
        (r'> _.+_', 'Quoted text')
    ]
    
    for pattern, element in required_elements:
        if not re.search(pattern, blog_text, re.MULTILINE):
            print(f"Missing: {element}")
            return False
    return True


def main():
    """Run comprehensive blog generator tests."""
    # Test input files
    test_files_dir = Path(__file__).parent / "output" / "for_app3"
    transcript_file = test_files_dir / "transcript_chunks.md"
    style_file = test_files_dir / "style-profile.md"
    
    print("Loading test files...")
    transcript = transcript_file.read_text(encoding='utf-8')
    style_profile = style_file.read_text(encoding='utf-8')
    
    print("\nGenerating blog article...")
    blog_content = generate(transcript, style_profile)
    
    # Run tests
    word_count = count_words(blog_content)
    voice_check = check_voice_consistency(blog_content, style_profile)
    structure_check = verify_markdown_structure(blog_content)
    placeholder_check = blog_content != "DRAFT" and "[Content will be generated" not in blog_content
    
    # Print results
    print("\nTest Results:")
    print(f"1. Word Count: {word_count} words {'✓' if 600 <= word_count <= 900 else '✗'}")
    print(f"2. Voice Consistency: {'✓' if voice_check else '✗'}")
    print(f"3. Markdown Structure: {'✓' if structure_check else '✗'}")
    print(f"4. Real Content (No Placeholders): {'✓' if placeholder_check else '✗'}")
    
    # Save output for inspection
    output_dir = Path(__file__).parent / "output" / "app3"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "output_blog.md"
    output_file.write_text(blog_content, encoding='utf-8')
    print(f"\nBlog saved to: {output_file}")


if __name__ == "__main__":
    main()
