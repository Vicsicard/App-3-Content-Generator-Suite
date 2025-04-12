# Content Generator Suite (App 3)

Welcome to the Content Generator Suite! This application takes your transcript and style profile (from Apps 1 & 2) and generates a complete content package including blog posts, newsletters, social media content, and more.

## 🚨 CRITICAL REQUIREMENTS

- **Python Version**: This app MUST run on Python 3.10 ONLY
- **Virtual Environment**: Use ONLY venv310

## 🚀 Quick Start

1. **Setup Virtual Environment**:
   ```bash
   python -m venv venv310
   venv310\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Prepare Input Files**:
   - Place your transcript in: `input/transcript_chunks.md`
   - Place your style profile in: `input/style-profile.md`

3. **Run Content Generator**:
   ```bash
   python -m content_generator.content_generator --transcript input/transcript_chunks.md --style input/style-profile.md
   ```

4. **Find Generated Content**:
   All content will be in `output/app3/`:
   - `output_blog.md`: Blog post
   - `output_newsletter.md`: Newsletter
   - `output_social_posts.md`: Social media content
   - `output_bio.md`: Professional biography
   - `output_ad_copy.md`: Advertisement copy
   - `output_reputation.md`: Reputation management content
   - `output_website.md`: Website content
   - `output_show_notes.md`: Show notes

## 📁 Directory Structure

```
App 3 Content Generator Suite/
├── content_generator/       # Main package
│   ├── agents/             # Content generation agents
│   ├── utils/              # Utility functions
│   └── content_generator.py # Main entry point
├── input/                  # Place input files here
│   ├── transcript_chunks.md
│   └── style-profile.md
├── output/                 # Generated content
│   └── app3/              # Output directory
├── tests/                 # Test files
├── requirements.txt       # Dependencies
├── setup.py              # Package setup
└── START_HERE.md         # This file
```

## ✅ Content Types Generated

1. **Blog Post**
   - Professional article with introduction, main points, and conclusion
   - Style-aligned writing voice

2. **Newsletter**
   - Engaging email content
   - Clear call-to-action

3. **Social Media Kit**
   - Platform-specific posts (LinkedIn, Twitter, Instagram)
   - Hashtag suggestions
   - Engagement prompts

4. **Professional Bio**
   - Compelling personal narrative
   - Highlights and achievements

5. **Ad Copy**
   - Attention-grabbing headlines
   - Persuasive body copy
   - Clear value propositions

6. **Reputation Management**
   - Professional responses
   - Brand-aligned messaging

7. **Website Content**
   - SEO-optimized copy
   - Clear value proposition
   - Engaging calls-to-action

8. **Show Notes**
   - Episode summary
   - Key points and timestamps
   - Resource links

## 🔍 Troubleshooting

1. **Python Version Error**:
   - Ensure you're using Python 3.10
   - Check with: `python --version`

2. **Missing Dependencies**:
   - Rerun: `pip install -r requirements.txt`
   - Ensure you're in the venv310 environment

3. **File Not Found Errors**:
   - Verify input files are in the correct location
   - Check file names match exactly

4. **Output Issues**:
   - Check `output/app3/content_generator.log` for details
   - Ensure write permissions in output directory

## 📝 Notes

- All content is generated in Markdown format
- Content maintains consistent voice and style from profile
- Each content type is optimized for its platform/purpose
- Log files track generation process and any issues

## 🔄 Integration with Other Apps

1. **From App 1 (Self-Cast Studio)**:
   - Use the transcript from `completed_transcripts/[DATE]_[TIME]_[CATEGORY]/`

2. **From App 2 (Style Profiler)**:
   - Use the style profile from App 2's output directory

## 🆘 Need Help?

Check the following resources:
- `docs/` directory for detailed documentation
- Log files in `output/app3/content_generator.log`
- Issue tracker on repository
