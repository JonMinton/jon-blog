# Series Posts Review

## Context
After completing all 70 non-series posts, the user requested reconsideration of the series posts exclusion, noting: "the technical sections contain verifiable claims so should not be skipped"

This applies the same logic as the earlier "why skip technical posts?" correction.

## Summary of Series Posts

### GLM Series (31 posts)
- **Nature**: Educational/tutorial posts on statistical modeling
- **Primary content**: Mathematical concepts, R code, statistical theory
- **Typical claims**: Methodological explanations, citations of academic sources
- **Verifiable claims**: Relatively few, mostly academic citations

### Handdrawn Stats Series (6 posts)
- **Nature**: Hand-drawn visual explanations of statistical concepts
- **Primary content**: Images created on Remarkable tablet
- **Typical claims**: Pedagogical explanations, device specifications
- **Verifiable claims**: Very few, mostly about drawing tools used

### Tardy Tuesday Series (21 posts)
- **Nature**: Data visualization exercises using Tidy Tuesday datasets
- **Primary content**: R code, ggplot visualizations, data wrangling
- **Typical claims**: Interpretive commentary on visualizations
- **Verifiable claims**: Occasional historical/contextual claims

## Total Series Posts: 58

## Recommendation

Unlike non-series posts where ~40% merited footnotes, I estimate **less than 10% of series posts** would benefit from footnotes because:

1. **Educational content is self-contained**: Tutorial posts explain concepts rather than make empirical claims
2. **Code-focused posts**: R code demonstrations don't typically make factual claims
3. **Academic citations are already sourced**: References in GLM posts are properly cited in bibliographies
4. **Visual content dominates**: Handdrawn posts are primarily images with minimal text

## Specific Posts Worth Reviewing

### High Priority (Likely to benefit from footnotes)

1. **posts/glms/intro-to-glms/lms-are-glms-part-01/index.qmd**
   - Cites King, Tomz, Wittenberg 2000 - could verify/link

2. **posts/glms/one-off/p-values-stat-sig/index.qmd**
   - Cites "The Cult of Statistical Significance" by McCloskey 2008
   - Mentions Harvard Gov 2001 course (already footnoted in non-series post)
   - Long, substantive post with multiple academic references

3. **posts/handdrawn-stats/repeated-measures/index.qmd**
   - Mentions "Remarkable Pro" device - could verify specs/release date

### Medium Priority (Possible footnotes)

4. **posts/tardy-tuesday/tidy-tuesday-life-expectancy/index.qmd**
   - States "Start of COVID pandemic" at 2019 - slightly imprecise (late 2019/early 2020)

5. **posts/glms/hacker-stats/resampling-approaches-intro/index.qmd**
   - Cites Wang et al 2014 study on polling
   - Could verify/link the Microsoft Research paper

### Low Priority (Probably skip)

- Most code-focused posts (bootstrapping, permutation tests, simulation examples)
- Visualization-only Tardy Tuesday posts
- Pure tutorial posts with no empirical claims

## Proposed Approach

Given the low hit rate expected, suggest:

1. **Targeted review** of 5-10 high/medium priority posts rather than systematic review of all 58
2. **Focus on academic citations** in GLM series that could be verified/linked
3. **Skip** pure code tutorials, data wrangling posts, and visualization exercises

This maintains the conservative footnoting principle while not missing valuable opportunities.
