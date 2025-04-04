#!/usr/bin/env python3
"""
Test script for blog generator output format
"""

from agents.blog_generator import generate

# Test input content
TEST_TRANSCRIPT = """
# Speaker Interview

## Background
I've been in the industry for 15 years, focusing on innovation.

## Key Insights
The biggest challenge was adapting to rapid change.
"""

TEST_STYLE = """
Voice: Professional
Tone: Conversational
Themes: Innovation, Leadership
Values: Authenticity, Growth
"""

def main():
    """Test blog generator output format"""
    print("Testing blog generator output format...")
    
    # Generate blog article
    article = generate(TEST_TRANSCRIPT, TEST_STYLE)
    
    # Print output
    print("\nGenerated Article:\n")
    print(article)
    
    # Basic format checks
    checks = [
        ("Title", article.startswith("# ")),
        ("Introduction", "## Introduction" in article),
        ("Three sections", article.count("## Section") == 3),
        ("Conclusion", "## Conclusion" in article),
        ("Quote format", article.count("> _\"") > 0)
    ]
    
    print("\nFormat Checks:")
    for name, passed in checks:
        status = "✓" if passed else "✗"
        print(f"{status} {name}")

if __name__ == "__main__":
    main()
