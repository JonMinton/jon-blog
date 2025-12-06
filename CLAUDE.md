# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## SAFETY: Branch Check

**CRITICAL SAFETY REQUIREMENT:** Before making any changes to files, commits, or running commands that modify the repository:

1. Check the current git branch with `git branch --show-current`
2. **NEVER work directly on the `main` branch**
3. If on `main`, STOP and ask the user to switch to a feature branch first
4. Only proceed with file modifications when on a branch other than `main`

This is a safety aspect of the workflow to prevent accidental changes to the production branch.

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
