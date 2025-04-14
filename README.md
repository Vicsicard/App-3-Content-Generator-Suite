# Content Generator Suite

A TypeScript-based content generation system that creates various types of content from transcripts and style profiles.

## Content Types and Sections

The generator creates content for different sections, each with its specific purpose:

1. **Blog Posts** (`section: 'blog'`)
   - Long-form content for the blog section
   - Example: "Finding Your Authentic Path: A Journey of Self-Discovery"

2. **Website Content** (`section: 'website'`)
   - Main website content and pages
   - Example: "Annie's Leadership Coaching Website"

3. **Bio Content** (`section: 'bio'`)
   - Professional biography and short descriptions
   - Example: "Annie's Short Bio"

4. **Social Media Posts**
   - Facebook (`section: 'facebook'`) - Engaging posts with personal insights
   - Twitter (`section: 'twitter'`) - Thread-style content with key takeaways
   - Instagram (`section: 'instagram'`) - Visual-focused content with carousel layouts
   - LinkedIn (`section: 'linkedin'`) - Professional thought leadership content

## Database Schema

Content is stored in Supabase with the following section constraints:
- Valid sections: 'bio', 'blog', 'facebook', 'twitter', 'instagram', 'linkedin', 'website', 'story'
- Each section can have unique content per user
- Social media content includes platform-specific metadata

## Usage

1. Install dependencies:
```bash
npm install
```

2. Build the project:
```bash
npm run build
```

3. Generate all content:
```bash
npm run start:all
```

## Content Structure

Each content type follows a specific format:

1. **Blog Posts**
   - Title
   - Main content with insights from transcripts
   - Tags and metadata

2. **Website Content**
   - Main website sections
   - Service descriptions
   - About sections

3. **Bio Content**
   - Professional biography
   - Short form descriptions
   - Key accomplishments

4. **Social Media Posts**
   - Platform-specific formatting
   - Engagement hooks
   - Hashtags and captions
   - Scheduled posting dates

## Development

The project uses TypeScript and follows a modular structure:
- `/generators` - Content generation logic for each type
- `/utils` - Shared utilities and database interactions
- `/input` - Source files (transcripts, style profiles)
- `/output` - Generated content files
