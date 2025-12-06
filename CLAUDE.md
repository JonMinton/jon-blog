# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## SAFETY: Branch Check and Sync

**CRITICAL SAFETY REQUIREMENT - Run at the start of EVERY session:**

At the beginning of each session, Claude Code agents MUST:

1. **Check current branch:**
   ```bash
   git branch --show-current
   ```

2. **Verify branch is experimental/claude:**
   - If on `main`: STOP immediately and inform the user they are on main
   - Ask user if they want to switch to `experimental/claude` or if they explicitly intend to work on main
   - **NEVER make file changes on main** unless user explicitly confirms

3. **If on experimental/claude, sync with main to prevent merge conflicts:**
   ```bash
   git fetch origin
   git merge origin/main
   ```
   - This is AUTOMATIC and should be done proactively without asking
   - Inform the user: "Syncing experimental/claude with main to prevent merge conflicts..."
   - If merge conflicts occur during sync, report them to the user
   - If sync succeeds, report: "✓ Branch synced with main"

4. **Only then proceed with normal work**

**Why this matters:** Syncing at the start of each session prevents the experimental/claude branch from diverging from main, which causes painful merge conflicts later. This two-line command prevents hours of merge conflict resolution.

**Exception:** If user explicitly states they are working on main and know what they're doing, skip the sync step but still warn about working on main.

## Merge Workflow: experimental/claude → main

**To minimize merge conflicts when merging experimental/claude to main:**

1. **Before starting new work on experimental/claude:**
   ```bash
   git checkout experimental/claude
   git fetch origin
   git merge origin/main
   ```
   This keeps experimental/claude in sync with main.

2. **When committing from experimental/claude:**
   - Commit source file changes (.qmd, .md, .R files)
   - Avoid running `quarto render` before committing if possible
   - If you must render, that's okay - just be aware it may cause merge conflicts

3. **When merging to main (user handles this, but context is useful):**
   - Most conflicts will be in auto-generated files (docs/*, _freeze/*)
   - For conflicts in source files (.qmd): prefer the experimental/claude version
   - For conflicts in generated files: accept experimental/claude version, then re-render on main
   - Use `git checkout --theirs <file>` to accept experimental/claude version

4. **After merging to main:**
   - Run `quarto render` on main branch to regenerate docs/ with merged content
   - This ensures rendered output matches the merged source files

## Project Overview

This is Jon Minton's personal Quarto blog - a static website built with Quarto that outputs to GitHub Pages. The blog covers diverse topics including statistics, data science, AI, pop culture analysis, and social commentary.

## Building and Rendering

**Preview the blog locally:**
```bash
quarto preview
```

**Render the full site:**
```bash
quarto render
```

The rendered site outputs to the `docs/` directory (configured in `_quarto.yml`), which is served by GitHub Pages.

**Pre-render automation:**
The `pre-render.R` script runs automatically before each render (configured in `_quarto.yml`). It:
- Executes `calculate-wordcount.R` to count total words across all `.qmd` files
- Updates the subtitle in `index.qmd` with the current word count
- Captures warnings to `render_warnings.log`

**Monitoring long-running renders:**
When `quarto render` is run in the background, use these **safe** methods to check progress without interrupting the process:

1. **Check process table (safest):**
   ```bash
   ps aux | grep -E "quarto|render" | grep -v grep
   ```
   This only reads system info and won't interrupt the process.

2. **Check background task output:**
   Use the `BashOutput` tool with the background task ID. This reads buffered output without sending signals to the process.

**AVOID:** Calling the `BashOutput` tool excessively or asking about progress too frequently, as this can sometimes interrupt the render process. Check progress sparingly (e.g., every few minutes for long renders).

## Project Structure

```
.
├── _quarto.yml           # Main Quarto configuration
├── posts/                # All blog posts, organized by topic
│   ├── glms/            # Multi-part GLM statistics series
│   ├── unpop/           # Pop culture analysis posts
│   ├── tardy-tuesday/   # Tidy Tuesday data visualizations
│   ├── handdrawn-stats/ # Hand-drawn statistics illustrations
│   └── [topic]/index.qmd
├── docs/                 # Rendered output (GitHub Pages)
├── index.qmd            # Homepage with post listing
├── about.qmd            # About page
└── *.qmd                # Top-level pages (glms.qmd, tardy-tuesday.qmd, etc.)
```

**Post organization:**
- Each post lives in `posts/[category]/[post-name]/index.qmd`
- Multi-part series organized in subdirectories (e.g., `glms/intro-to-glms/lms-are-glms-part-01/`)
- YAML frontmatter required: title, author, date, categories

## Blog Post Conventions

**YAML frontmatter structure:**
```yaml
---
title: Post Title
subtitle: Optional subtitle (if needed)
author: Jon Minton
date: YYYY-MM-DD
categories: [category1, category2, tag3]
---
```

**Internal linking:**
- Use relative paths from the post location: `../other-post/index.qmd`
- For posts in nested directories: `../../category/post/index.qmd`
- Common pattern: Link to related posts in the same series or topic area

**Markdown formatting:**

**CRITICAL - List formatting:** Bullet point lists in `.qmd` files MUST have blank lines before and after the entire list block, or they will not render properly. This is a common source of rendering errors.

Correct format:
```markdown
Here is some text before the list.

- Item one
- Item two
- Item three

Here is text after the list.
```

Incorrect format (will break rendering):
```markdown
Here is some text before the list.
- Item one
- Item two
- Item three
Here is text after the list.
```

Other formatting rules:
- Paragraph breaks require blank lines between paragraphs (markdown standard)
- Use `**bold**` for emphasis in bullet points when needed
- Links: `[Link text](url)` for external, `[Link text](../path/index.qmd)` for internal

**Images and media:**
- Store in the same directory as the post's `index.qmd`
- Reference with relative paths: `![Alt text](filename.jpg)`

**Footnotes:**

Quarto supports standard Markdown footnote syntax with two-part format:
- Reference in text: `Some text here[^id]`
- Definition elsewhere: `[^id]: Footnote content here`

**CRITICAL - Footnote ID Convention:**
- **ALWAYS use descriptive IDs** for Claude-generated footnotes
- Format: `[^claude-shorttopic]` (e.g., `[^claude-ml]`, `[^claude-pvalues]`)
- **NEVER use sequential numbers** ([^1], [^2]) for Claude footnotes - this creates collision risk with existing footnotes
- User's original footnotes may use numbers - descriptive IDs prevent conflicts

Example correct usage:
```markdown
The GLM framework applies to many models.[^claude-ml]

[^claude-ml]: **Note from Claude:** This concept is taught in Andrew Ng's ML course...
```

Footnotes can include bibliography citations using `@citationkey` format if the post has a `bibliography: references.bib` entry in the YAML frontmatter. See `.claude/footnote-rendering-fix.md` for full details on the footnote rendering fix and conventions.

## Themes and Styling

The blog uses dual themes configured in `_quarto.yml`:
- Light: cosmo
- Dark: slate
- Custom CSS: `styles.css`

## R Integration

This is primarily an R-based blog with Quarto. R scripts handle word counting and pre-render automation. Posts may contain R code chunks with statistical analyses and visualizations.

## Content Categories

The blog has several major content areas linked in the navbar:
- **Statistical Theory and Applications** (glms.qmd): GLM series and statistical tutorials
- **Tardy Tuesday** (tardy-tuesday.qmd): Tidy Tuesday data visualization challenges
- **Hand-drawn Statistics** (hand-drawn-statistics.qmd): Visual explanations of stats concepts
- **Unpopular Opinions** (unpop.qmd): Pop culture and media analysis

## Common Workflow Patterns

**Creating a new post:**
1. Create directory: `posts/[category]/[post-name]/`
2. Add `index.qmd` with proper YAML frontmatter
3. Add any images/assets to the same directory
4. Render to preview: `quarto preview`

**Editing existing posts:**
- Posts are in `posts/**/**/index.qmd`
- After editing, render to see changes
- Word count updates automatically on next render via pre-render script

**Working with series posts:**
The GLM series follows a numbered pattern (`lms-are-glms-part-XX`) within subdirectories by topic area. When adding to a series, maintain the numbering convention and place in the appropriate subdirectory.
