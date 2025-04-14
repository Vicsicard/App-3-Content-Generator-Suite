import { writeContent } from '../utils/contentWriter.ts';

interface StyleProfile {
  voice: string[];
  themes: string[];
}

export async function generateWebsiteContent(transcript: string, styleProfile: StyleProfile) {
  // Extract key insights from the transcript chunks
  const chunks = transcript.split('## [Chunk').slice(1);
  const insights = chunks.map(chunk => {
    const quote = chunk.match(/> Speaker \d+: (.+?)(?=\n|$)/)?.[1] || '';
    return quote.trim();
  }).filter(Boolean);

  // Create short bio content
  const bioContent = `# Short Bio

Leadership coach and speaker passionate about authentic self-expression. ${insights[0].split('.')[0]}. I help others discover their authentic leadership style and create meaningful impact in their own unique way.`;

  // Save bio separately with 'bio' section
  await writeContent('output_short_bio.md', bioContent, {
    section: 'bio',  // Using 'bio' for the short bio
    title: "Annie's Short Bio",
    status: 'draft',
    tags: ['bio', 'about', 'leadership'],
    excerpt: "Concise professional bio highlighting Annie's expertise in authentic leadership."
  });

  // Create main website content
  const websiteContent = `# Annie's Leadership Coaching

## Hero Section
Unlock Your Authentic Leadership Potential

${insights[1]} Let me help you discover and leverage your unique strengths to create lasting impact.

[Book a Discovery Call]

## My Story
### The Journey to Authentic Leadership

I'm a leadership coach and speaker who believes in the power of authentic self-expression. ${insights[0]} This journey has shaped not only my approach to leadership but also how I help others find their path.

${insights[1]} This pivotal realization became the foundation of my coaching philosophy. Through years of experience, I've discovered that true leadership isn't about following someone else's blueprint—it's about embracing what makes you unique and using that to inspire others.

${insights[2]} Now, I dedicate my work to helping others discover and embrace their authentic leadership style, creating ripples of positive change in their organizations and communities.

### My Approach
I believe that true leadership emerges when we:
• Embrace our unique perspectives
• Trust our inner wisdom
• Show up authentically
• Create space for others to do the same

## Services

### 1. One-on-One Leadership Coaching
Personalized guidance to help you:
• Discover your authentic leadership style
• Build confidence in your unique approach
• Create meaningful impact in your way

### 2. Group Programs
Transform your team through:
• Authentic leadership development
• Team dynamics workshops
• Communication mastery

### 3. Speaking Engagements
Inspiring talks on:
• Finding your authentic voice
• Leading with purpose
• Building genuine connections

## Values & Approach
${styleProfile.themes.slice(0, 5).map(theme => `• ${theme}`).join('\n')}

## Speaking Style
${styleProfile.voice.slice(0, 5).map(trait => `• ${trait}`).join('\n')}

## Testimonial Section
"${insights[2]}"
- Recent Client

## Call to Action
Ready to begin your authentic leadership journey?
[Schedule Your Free Discovery Call]

## Blog Section
Latest insights on authentic leadership, personal growth, and creating meaningful impact.
[View All Posts]`;

  // Save main website content with 'website' section
  await writeContent('output_website.md', websiteContent, {
    section: 'website',  // Using 'website' for the main website content
    title: "Annie's Leadership Coaching Website",
    status: 'draft',
    tags: ['website', 'services', 'leadership', 'about'],
    excerpt: "Professional website content featuring Annie's authentic leadership coaching approach, services, and story."
  });

  return { bioContent, websiteContent };
}
