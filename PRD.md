PRD — App 3: Content Generator Suite
Part of the Self Cast Studios Modular System
Version: v1.0
Status: ✅ Approved for build

🎯 Purpose
To generate diverse, platform-ready content based on the client’s personal narrative — using a structured, AI-assisted system that preserves their voice, tone, and story. App 3 will take the transcript and narrative style profile created in previous apps and output high-quality, human-like content in multiple formats.

📥 Inputs
File	Description	Source
transcript_chunks.md	Cleaned, chunked transcript of Speaker 1's narrative	App 1
style-profile.md	Narrative fingerprint (voice, tone, themes, values)	App 2
Both inputs must be passed at runtime, and loaded into memory by the app.

📤 Outputs
Seven content types will be generated from the inputs. Each agent will generate its own .md file and save it to:

bash
Copy
Edit
/output/app3/
Content Type	Output Filename	Notes
Blog Article	output_blog.md	600–900 words, thought-leadership style
Show Notes	output_show_notes.md	Podcast-style summary w/ timestamps
Newsletter	output_newsletter.md	Brief, engaging blurb with value + insight
Social Media Kit	output_social_posts.md	Multi-platform (X, FB, LinkedIn)
Personal Bio	output_bio.md	Website bio + social profile versions
Ad Copy / Intros	output_ad_copy.md	Headlines, hooks, promotional blurbs
Reputation Content	output_reputation.md	SEO support, “suppression” style content
🧠 Tier 3 AI Agents
Each agent uses both inputs and a specialized prompt (designed earlier in Tier 3) to generate human-quality content in their domain of expertise.

Agent File	Responsibility
blog_generator.py	Longform blog article
show_notes_builder.py	Podcast-style summary with highlights
newsletter_writer.py	Succinct and branded newsletter preview
social_media_kit.py	Platform-specific social posts
bio_creator.py	Bios for site + platforms
ad_copy_studio.py	Catchy headlines, blurbs, CTAs
reputation_repair.py	Suppression-oriented SEO content
Each returns a .md formatted string with clear headings.

🧱 Output Format (per agent)
All output files must:

Be saved to /output/app3/

Be valid Markdown (.md)

Start with a clear header (e.g., ## Blog Article)

Be written in the author’s voice, based on style-profile.md

🧪 Success Criteria
Goal	Required?
Accepts both input files via CLI	✅
Loads both files successfully	✅
Runs all 7 agents in correct order	✅
Saves 7 output .md files to /output/app3/	✅
Each file is clean, readable Markdown	✅
Style is consistent with style-profile.md	✅
Prints clear success confirmation	✅
🔒 Limitations
No PDF, DOCX, or HTML output in this version

No Supabase or external storage integration

No web dashboard or scheduling yet

No multi-user logic (handled in future phases)