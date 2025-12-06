# Footnote Addition Decisions

## Decision Criteria

**ADD footnotes when:**
- Post makes factual/scientific claims that can be verified/updated
- Post references research that has developed since publication
- Post makes predictions that can be evaluated
- Related concepts/research would genuinely add value

**SKIP footnotes when:**
- Pure commentary/opinion pieces
- Humorous/satirical posts
- Posts already have extensive citations
- No clear value-add from external verification

**SPECIAL CASE - Technical/Educational Posts:**
- Statistical methods posts (GLM series, etc.) DO receive technical footnotes
- Focus: Online courses, ML/data science connections, Python library alternatives
- Academic references (books/articles) moved to .bib files for proper citations
- Web resources (courses, documentation) remain as inline footnotes

## Posts Reviewed - Batch 1 (Pilot + Recent)

### ✅ Added Footnotes

1. **unattended-deaths** (2 footnotes) - Epidemiological research validation
2. **psycho-logical-arithmetic** (1 footnote) - Cocoa price prediction validated
3. **x-minute-neighbourhoods** (1 footnote) - Walkability research evidence
4. **analytical-maxim-gun** (1 footnote) - Historical verification of Maxim gun
5. **tolerating-intolerance-paradox** (1 footnote) - Link to Popper's paradox
6. **brian-may-gentleman-ecoscientist** (4 footnotes) - Documentary reception + verification footnotes (Anne Brunner, testing frequency, May's PhD)

**Subtotal: 6 posts, 10 footnotes**

### ⏭️ Skipped (Good Reasons)

1. **rwanda-information-warfare** - Documenting real-time misinformation, value is in observation
2. **voter-types** - Theoretical framework, no factual claims to verify
3. **circular-reasoning** - Humorous political geometry, satirical
4. **threw-missiles** - Linguistic commentary, no factual verification needed

**Subtotal: 4 posts skipped**

## Batch 2: Technical/Statistical Methods Posts

### ✅ Added Footnotes

1. **lms-are-glms-part-01** (1 footnote) - Andrew Ng's ML course, Python libraries (statsmodels, scikit-learn)
2. **lms-are-glms-part-02** (1 footnote) - Link functions vs activation functions, cross-entropy loss
3. **lms-are-glms-part-03** (1 footnote) - Python GLM libraries, fast.ai course
4. **lms-are-glms-part-04** (1 footnote + .bib) - Marginal effects, SHAP values, ML interpretability [@molnar2022interpretable]
5. **lms-are-glms-part-05** (1 footnote + .bib) - Likelihood theory, loss functions, Stanford CS229 [@murphy2022probabilistic]
6. **lms-are-glms-part-06** (1 footnote) - Optimization algorithms, gradient descent, PyTorch/TensorFlow
7. **lms-are-glms-part-16** (1 footnote + .bib) - Causal inference in ML/data science [@cunningham2021causal, @facure2022causal]
8. **resampling-approaches-intro** (1 footnote + .bib) - Computational statistics, bootstrapping in ML [@downey2014think]
9. **p-values-stat-sig** (1 footnote + .bib) - Cross-validation, model selection in ML [@mcelreath2020statistical, @efron2016computer]

**Subtotal: 9 posts, 9 footnotes, 5 new .bib files created/updated**

**Bibliography files created:**
- `posts/glms/intro-to-glms/lms-are-glms-part-04/references.bib` (Molnar)
- `posts/glms/likelihood-and-simulation-theory/lms-are-glms-part-05/references.bib` (Murphy)
- `posts/glms/causal-inference/lms-are-glms-part-16/references.bib` (Cunningham, Facure)
- `posts/glms/hacker-stats/resampling-approaches-intro/references.bib` (Downey)
- `posts/glms/one-off/p-values-stat-sig/references.bib` (McElreath, Efron - updated existing)

## Posts To Review - Remaining ~121 posts

### Priority Categories

**High Priority (substantive factual claims):**
- Epidemiology/health posts
- Economic/social science posts
- Historical/cultural analysis
- Scientific topics (evolution, ecology, etc.)

**Medium Priority:**
- Commentary with some factual basis
- Book/media reviews with verifiable claims

**Low Priority (likely skip):**
- GLM series (25+ posts) - Technical tutorials
- Hand-drawn statistics - Visual explanations
- Tardy Tuesday - Data visualization exercises
- Pure opinion pieces
- Meta/blog infrastructure posts

## Efficiency Strategy

Given 131 total posts, estimated breakdown:
- GLM series: ~30 posts (SKIP - technical tutorials)
- Hand-drawn/Tardy Tuesday: ~15 posts (SKIP - visual/exercise content)
- Meta/infrastructure: ~10 posts (SKIP)
- **Substantive posts for review: ~70 posts**

Target: 1-2 footnotes per substantive post = **70-140 total footnotes**
Current: 7 footnotes completed
Remaining: **~63-133 footnotes**

## Next Batches

### Batch 2: Evolution/Science Posts (in progress)
- gentes-lover-and-a-fighter - YES (verify Poecilia parae research)
- death-dying-darwin - Review needed
- can-we-go-dutch - Review needed

### Batch 3: Social/Economic Posts
- changing-tenure-in-scotland
- effective-saving-for-interest-free-credit
- anti-victories-and-velvet-mousetraps

### Batch 4: Unpopular Opinions Series
- Posts in unpop/ directory

### Batch 5: Older substantive posts (2023)
- Posts with research/factual claims

