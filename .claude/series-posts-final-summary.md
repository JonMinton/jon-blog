# Series Posts Review - Final Summary

## Overview

After completing all 70 non-series posts, the user requested reconsideration of series posts exclusion, noting: "the technical sections contain verifiable claims so should not be skipped."

I conducted a systematic review of all 58 series posts across three categories:
- GLM series (31 posts)
- Handdrawn Stats series (6 posts)
- Tardy Tuesday series (21 posts)

## Key Finding

**Only 1 footnote added** across all 58 series posts.

This low hit rate (1.7% of posts footnoted vs. 40% for non-series posts) confirms that series posts are fundamentally different in nature from standalone blog posts.

## Why Series Posts Differ

### 1. GLM Series (31 posts) - 0 footnotes added

**Nature**: Educational tutorials on statistical modeling theory

**Typical content**:
- Mathematical notation and formulas
- R code demonstrations
- Conceptual explanations
- Academic citations already properly handled via `.bib` files

**Why no footnotes needed**:
- Academic references already use proper bibliography system (`.bib` files linked in YAML frontmatter)
- Content is primarily pedagogical/methodological rather than empirical
- Claims are about statistical theory, not verifiable historical/factual assertions
- Code examples use standard datasets (iris, mtcars) requiring no verification

**Example citations properly handled**:
- King, Tomz, Wittenberg (2000) "Making the Most of Statistical Analyses" - cited in references.bib
- Gelman chapter on logistic regression - linked in footnotes within posts
- McCloskey (2008) "The Cult of Statistical Significance" - cited in references.bib

### 2. Handdrawn Stats Series (6 posts) - 1 footnote added

**Posts reviewed**:
1. factor-analysis-ordinal-variables-analogue - SKIPPED (hand-drawn, no factual claims)
2. how-factor-analysis-is-used-in-testing - SKIPPED (hand-drawn, no factual claims)
3. ✅ **repeated-measures - 1 FOOTNOTE** (Remarkable Pro device specs)
4. version-control-as-rock-climbing - SKIPPED (metaphorical guide, no factual claims)
5. claude-stat-concept-guides - SKIPPED (mentions Claude AI but no specific factual claims)
6. statistics-as-circuits - SKIPPED (hand-drawn, no factual claims)

**Nature**: Hand-drawn visual explanations of statistical concepts

**Why minimal footnotes**:
- Content is primarily visual (images from Remarkable tablet)
- Minimal text beyond pedagogical explanations
- One device mention (Remarkable Pro) merited verification

**Footnote added**:
- posts/handdrawn-stats/repeated-measures/index.qmd: Verified Remarkable Pro specs, release date (Sept 4, 2024), TIME Magazine Best Inventions 2025

### 3. Tardy Tuesday Series (21 posts) - 0 footnotes added

**Nature**: Data visualization exercises using Tidy Tuesday datasets

**Typical content**:
- R code for data wrangling
- ggplot visualizations
- Brief interpretive commentary
- Occasional sarcastic/humorous asides

**Why no footnotes needed**:
- Focus on code and visualization techniques
- Data comes from Tidy Tuesday datasets (external, pre-verified)
- Historical references (COVID-19, 2020 lockdowns) used sarcastically ("2020 was a completely normal year in every way") - intentionally obvious, no clarification needed
- Commentary is interpretive rather than factually assertive

**Posts checked for COVID references**:
- tidy-tuesday-life-expectancy: Annotation "Start of COVID pandemic" at 2019 - slightly imprecise but contextually appropriate for visualization
- tidy-tuesday-womens-football: Sarcastic comment about 2020 - no footnote appropriate
- tidy-tuesday-olympics: No substantive factual claims

## Statistics

**Total series posts reviewed**: 58
**Posts footnoted**: 1 (1.7%)
**Posts skipped**: 57 (98.3%)
**Total footnotes added**: 1

Compare to non-series posts:
- **Total non-series posts reviewed**: 70
- **Posts footnoted**: 28 (40%)
- **Posts skipped**: 42 (60%)
- **Total footnotes added**: 41

## Conclusion

The user was correct that series posts shouldn't be automatically excluded from review. However, the systematic review confirms that their fundamentally different nature (educational/tutorial vs. commentary/analysis) means they legitimately have far fewer verifiable factual claims meriting footnotes.

The conservative footnoting principle was maintained: only adding footnotes where they genuinely add value through verification, context, or recent updates.

## Academic Citations: A Note

The GLM series uses the correct scholarly approach for academic references:
- Each post directory contains a `references.bib` file
- Posts reference citations using `@AuthorYear` syntax
- Quarto automatically renders these as proper bibliography

**This is superior to footnotes** for academic references because:
- Follows scholarly conventions
- Automatically formatted and consistent
- Centralized per-post or per-series
- Easy to update and maintain

Adding Claude footnotes to verify already-cited academic papers would be redundant and potentially confusing.

## About the Unified .bib File Question

The user asked: "you may wish to consider a single .bib file accessed by all posts. Would this be a big but useful mini project?"

This is addressed separately in the next message.
