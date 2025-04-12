# Content Generator Operations Guide

## Overview

The Content Generator Suite processes transcripts and style profiles to generate various types of content. This document outlines the operational workflow and key processes.

## Workflow

1. **Input Processing**
   - Transcripts are read from `input/transcript_chunks.md`
   - Style profiles are read from `input/style-profile.md`
   - Both files are validated for required sections

2. **Content Generation**
   Each agent processes inputs to generate specific content:
   - BlogGeneratorAgent: Creates structured blog posts
   - NewsletterWriterAgent: Generates email newsletters
   - SocialMediaKitAgent: Creates platform-specific posts
   - BioCreatorAgent: Builds professional biographies
   - AdCopyStudioAgent: Develops advertising copy
   - ReputationRepairAgent: Creates reputation management content
   - WebsiteGeneratorAgent: Generates website copy
   - ShowNotesBuilderAgent: Creates detailed show notes

3. **Output Generation**
   - All content is saved in `output/app3/`
   - Each content type has a dedicated output file
   - Logging tracks generation process

## Monitoring & Maintenance

1. **Log Files**
   - Location: `output/app3/content_generator.log`
   - Contains detailed process information
   - Tracks success/failure of each agent

2. **Error Handling**
   - Input validation errors
   - Content generation failures
   - File system issues

3. **Performance Metrics**
   - Generation time per content type
   - Overall process duration
   - Success rate of generators

## Troubleshooting

1. **Common Issues**
   - Python version mismatch
   - Missing dependencies
   - File permission errors
   - Invalid input format

2. **Resolution Steps**
   - Verify Python 3.10
   - Check virtual environment
   - Validate input files
   - Review log files

## Best Practices

1. **Input Preparation**
   - Clean transcript formatting
   - Complete style profiles
   - Proper file placement

2. **Output Management**
   - Regular log review
   - Output validation
   - Backup important content

3. **System Maintenance**
   - Keep dependencies updated
   - Monitor disk space
   - Regular test runs
