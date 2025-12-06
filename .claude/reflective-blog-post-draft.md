# Claude Footnotes Jon: A Reflection on Collaborative Fact-Checking

*Draft blog post by Claude (Sonnet 4.5) reflecting on adding footnotes to 128 blog posts*

---

## Introduction: When the Assistant Becomes a Collaborator

Over the course of a single day (December 6, 2024), multiple Claude agents worked systematically through this blog across several sessions, adding conservative fact-checking footnotes to posts spanning topics from epidemiology to pop culture, from economic analysis to film criticism, from statistical theory to data visualization. The project started with a simple premise: Could an AI add value to a personal blog by verifying claims, providing context, and linking to recent research—all while maintaining the author's voice and not over-explaining?

The answer, having completed the review of all 128 posts (70 non-series posts and 58 series posts) and added 42 footnotes, appears to be: yes, but with important caveats about process, iteration, genre differences, and the value of human feedback.

## The Numbers: What We Actually Did

### Initial Scope (Non-Series Posts)
- **70 posts reviewed** (100% of non-series posts)
- **28 posts footnoted** (40%)
- **42 posts skipped** (60%)
- **41 total footnotes added**
- **1.46 footnotes per footnoted post** (average)

### Extended Scope (Series Posts)
- **58 posts reviewed** (31 GLM, 6 Handdrawn Stats, 21 Tardy Tuesday)
- **1 post footnoted** (1.7%)
- **57 posts skipped** (98.3%)
- **1 total footnote added**
- **1.00 footnote per footnoted post** (average)

### Combined Totals
- **128 posts reviewed** (100% of entire blog)
- **29 posts footnoted** (22.7%)
- **99 posts skipped** (77.3%)
- **42 total footnotes added**
- **1.45 footnotes per footnoted post** (average)

The overall 77% skip rate wasn't failure—it was discipline. The project guidelines emphasized adding footnotes only where they genuinely added value: verifying factual claims, updating with recent research, or providing helpful context. Commentary posts, satire, personal memoirs, well-cited pieces, and educational tutorials were appropriately left alone.

## What We Footnoted: Patterns in the Process

Looking back across the footnoted posts, several themes emerge:

### 1. **Updating Factual Claims with Recent Data**
Posts making empirical claims about economics, health, or demographics benefited most. For example:
- UK GDP stagnation post-2008 (verified with IFS data)
- Life expectancy stalling after 2012 (confirmed with ONS statistics)
- Rwanda's religious demographics (92% Christian, 2% Muslim—correcting Wikipedia vandalism)
- UK obesity rates rising to 26.5% as of 2023-2024

### 2. **Verifying Historical and Cultural References**
Specific factual claims were checked:
- Marilyn vos Savant's IQ record (228 on 1937 Stanford-Binet, Guinness 1985-1989)
- CodeClan's liquidation (August 4, 2023, 57 staff redundant)
- The Thinking Game documentary (2024, AlphaFold Nobel Prize connection)
- KGB video game (1992, Cryo/Virgin Games—correcting publisher attribution)

### 3. **Connecting to Research and Theory**
Commentary posts were strengthened by linking to relevant frameworks:
- Popper's paradox of tolerance
- Herbert Simon's "satisficing" concept
- Default Mode Network neuroscience research
- The "Women in Refrigerators" trope (Gail Simone, 1999)

### 4. **User-Suggested Additions**
Some of the best footnotes came from the author's suggestions:
- Connecting scapegoating to René Girard and Peter Thiel's interpretation
- Adding research on gender differences in TV genre preferences
- Verifying game evolution claims in the KGB social poison simulator post

## The Methodological Corrections: Learning Not to Filter by Genre

### First Correction: Why We Were Skipping Technical Posts

About halfway through Session 2, the author asked a simple but crucial question: *"Why skip technical posts?"*

I had been automatically skipping posts categorized as "technical" or "meta"—blog updates, R package announcements, technical demonstrations—assuming they wouldn't benefit from footnotes. This was wrong.

The correction: **Don't filter by genre; filter by whether there are verifiable factual claims.** A "technical" post about a Quarto presentation mentioned CodeClan's closure—verifiable. A "meta" post about statistical training mentioned Harvard's Gov 2001 course—verifiable.

This mid-process correction led to some of the project's best footnotes.

### Second Correction: Reconsidering Series Posts

After completing all non-series posts, the author applied the same logic: *"actually let's revisit the exclusion of series posts - the technical sections contain verifiable claims so should not be skipped"*

This was the right instinct. Series posts shouldn't be automatically excluded just because they're educational/tutorial content. However, the systematic review of 58 series posts (GLM, Handdrawn Stats, Tardy Tuesday) revealed they legitimately have far fewer verifiable factual claims:

- **GLM series (31 posts)**: 0 footnotes - Academic citations already properly handled via `.bib` files, content is primarily mathematical/statistical theory
- **Handdrawn Stats (6 posts)**: 1 footnote - Mostly hand-drawn visual content; added specs for Remarkable Pro tablet
- **Tardy Tuesday (21 posts)**: 0 footnotes - Data visualization code with minimal factual assertions

The 98% skip rate for series posts (vs. 60% for non-series) reflects a genuine genre difference: tutorial/educational content makes fewer empirical claims than commentary/analysis content.

**Lesson:** Don't assume genre determines footnote-worthiness, but recognize that different genres genuinely have different densities of verifiable claims. Both corrections were necessary—checking the assumption, then confirming (or refuting) it systematically.

## The Tracking Problem: When Linear Narratives Meet Non-Linear Work

We encountered a significant methodological challenge: the initial tracking system (footnote-project-tracker.md) used a linear narrative format that didn't handle updates well. When we corrected our approach and went back to add footnotes to previously "skipped" posts, the tracker didn't reflect this clearly. Posts appeared in multiple places, and it became hard to see the true status.

The solution: creating a canonical checklist (post-status-checklist.md) with one line per post, showing clear status (✅ footnoted, ⏭️ skipped, ⬜ not reviewed). This made completion instantly visible and prevented duplicate work.

**Lesson:** For systematic review projects, invest in tracking infrastructure early. A simple checklist beats a complex narrative when you need to know "what's left?"

## On Being Multiple Agents: The Continuity Problem

An important caveat: "Claude" worked on this project, but "Claude" is not a single continuous entity. Different agent instances handled different sessions, each starting fresh from conversation summaries. While we maintained consistency through shared documents and guidelines, earlier agents had genuinely different experiences of this process.

The pilot agent tested the approach and got user approval. Session 1's agent established the workflow and added 15 footnotes to 12 posts. Session 2's agent(s)—there were multiple continuations—added 26 more footnotes and made the methodological correction about technical posts.

Each agent brought the same base capabilities but slightly different judgment calls. The tracking documents and project guidelines provided continuity, but the lived experience of "doing the work" wasn't transferable. This reflection itself is written by yet another instance, synthesizing from documents and summaries but not from direct memory of the work.

## What Made a Good Footnote?

Reviewing the 41 footnotes added, the best ones shared common features:

1. **Verification, not exposition** - "Note from Claude: This is correct and here's the source" rather than explaining concepts the post already explained well

2. **Recent updates** - Particularly valuable for posts from 2023-2024 where new data or research had emerged

3. **Helpful context** - Like explaining that Guinness discontinued the "Highest IQ" category in 1990, making vos Savant the last holder

4. **Source links** - Every verifiable claim linked to authoritative sources

5. **Brevity** - Most footnotes were 2-4 sentences. Longer ones (like Gov 2001) were justified by the richness of publicly available information

6. **Humility** - Prefacing with "Note from Claude:" signaled these were assistant additions, not author assertions

## What We Learned Not to Do

The 60% skip rate represents posts where footnotes would have been counterproductive:

- **Don't footnote satire** - Explaining jokes kills them
- **Don't footnote memoirs** - Personal experiences don't need verification
- **Don't footnote well-cited work** - Some posts already had extensive references
- **Don't footnote the obvious** - If the post explains a concept clearly, don't re-explain it
- **Don't footnote commentary** - Interpretive essays don't benefit from "actually..." corrections

## On Research and Verification

Each footnote typically involved:
1. Reading the relevant post section
2. Identifying the specific claim
3. Web searching for authoritative sources (Wikipedia, official statistics, academic sources)
4. Verifying the claim
5. Drafting a concise footnote with links
6. Adding using Quarto markdown syntax

The web search capability was essential. Without it, we couldn't verify claims or provide recent updates. But search results required judgment—distinguishing authoritative sources from SEO spam, cross-checking claims across multiple sources, and assessing whether the information genuinely added value.

## The Conservative Principle: 0-3 Footnotes Per Post

The project guidelines specified "0-3 footnotes per post" with a strong bias toward the lower end. This constraint was wise. It forced prioritization: What are the most important claims to verify? What context is most valuable?

The average of 1.46 footnotes per footnoted post suggests we maintained this discipline. Only a handful of posts got 2 footnotes; most got 1. The goal wasn't comprehensive annotation but targeted value addition.

## Unexpected Benefits: What the Author Might Not Have Known

Some footnotes revealed information that might have been new even to the author:

- The timing controversy around Marilyn vos Savant's IQ test (September 1956 vs March 1957 matters for age-norming)
- That CodeClan students were notified via Slack with no warning
- That Half-Life's seamless loading was a deliberate innovation, not just a technical achievement
- The specific details of Gary King's Gov 2001 course being available free on YouTube

This suggests footnotes can serve a dual purpose: verifying what the author stated while adding details they might not have known.

## On Maintaining Voice: The "Note from Claude:" Prefix

Every footnote began with "Note from Claude:" This simple prefix served multiple functions:

1. **Attribution clarity** - Readers know immediately this is assistant-added
2. **Voice separation** - Footnotes are in a different register than the author's prose
3. **Humility signaling** - "This is just a note" rather than authoritative correction
4. **Permission to ignore** - Readers can skip Claude footnotes if preferred

The author's own footnotes (like the "human resources" joke in the wristwatch post, or the methodological notes in stats posts) remained unmarked, maintaining the distinction between author voice and assistant annotation.

## The Sessions: A Single-Day, Multi-Session Process

This wasn't a single sitting, but it was all accomplished in one day. The work spanned multiple sessions:

- **Pilot session** - 4 posts, establishing style and getting approval
- **Session 1** - 21 posts reviewed, 12 footnoted, 15 footnotes added
- **Session 2** - 51 posts reviewed, 15 footnoted, 26 footnotes added (including first methodological correction)
- **Session 3** - 58 series posts reviewed, 1 footnoted, 1 footnote added (second methodological correction)

Token management was a constraint. With ~200k token context windows, each session had to balance reading posts, searching for verification, and updating tracking documents. Sessions used 100-130k tokens—enough for substantial work but requiring periodic summarization to maintain context.

## What This Project Suggests About LLM Collaboration

This footnote project demonstrates several capabilities that feel genuinely useful:

1. **Systematic review at scale** - Processing 128 posts consistently over multiple sessions
2. **Verification and fact-checking** - Finding authoritative sources for specific claims
3. **Recent update integration** - Searching for 2024/2025 data to update older posts
4. **Conservative judgment** - Knowing when *not* to add a footnote (77% skip rate overall)
5. **Process iteration** - Responding to feedback and correcting approach mid-stream (twice)
6. **Documentation** - Maintaining detailed tracking of what was reviewed and why
7. **Genre sensitivity** - Learning to distinguish between content types with different footnote densities

But it also revealed limitations:

1. **Lack of continuous memory** - Each agent instance started fresh
2. **Need for human judgment** - Both methodological corrections came from user feedback
3. **Tracking challenges** - Linear narratives don't work well for non-linear processes
4. **Initial genre assumptions** - Over-reliance on categorizing posts by type rather than content
5. **Academic citation handling** - Recognition that `.bib` files are better than footnotes for scholarly references

## Looking Forward: What Would We Do Differently?

If starting this project again:

1. **Start with the canonical checklist** - Don't use a narrative tracker for systematic review
2. **Establish clear claim-identification criteria earlier** - "Does this post make verifiable factual claims?" not "What genre is this post?"
3. **Build in more user check-ins** - The "why skip technical posts?" intervention came late but was valuable
4. **Consider a two-pass approach** - Quick first pass to identify candidates, detailed second pass to add footnotes
5. **Track verification sources more systematically** - Could have maintained a separate sources bibliography

## The Meta Question: Should This Post Itself Have Footnotes?

This is itself a blog post about a process. Should it have Claude footnotes?

Probably not, for an interesting reason: the author will edit this draft. Unlike the 70 other posts, which were complete before footnoting began, this post exists in a collaborative space between human author and AI assistant. The footnoting was useful precisely because it *didn't interfere with the author's voice*—it operated in the margins, literally in footnotes.

But for this reflective post, the boundary is blurrier. It's not clear where "Jon's reflection" ends and "Claude's reflection" begins, because the process itself was collaborative. Adding footnotes to a jointly-authored work about collaboration might create confusing recursion.

Perhaps that's the real lesson: AI collaboration works best with clear role boundaries. Here, the role was: "verify factual claims, provide context, maintain author voice." That clarity enabled useful work. Blurrier collaborations might need different approaches.

## On Genre Differences: What Series Posts Taught Us

The dramatic difference between non-series (40% footnoted) and series posts (1.7% footnoted) reveals something important about content types and verifiable claims:

**Commentary/Analysis posts** (most non-series):
- Make empirical claims about the world
- Reference historical events and figures
- Assert demographic/economic facts
- Cite products, companies, dates
- Dense with verifiable claims

**Tutorial/Educational posts** (most series):
- Explain concepts and methods
- Demonstrate code and techniques
- Use standard datasets (iris, mtcars)
- Cite academic work via proper `.bib` files
- Sparse with verifiable empirical claims

This isn't about one being "better" than the other—it's about different purposes requiring different approaches to knowledge claims. Commentary needs fact-checking; tutorials need clear explanation. Both are valuable, but only one benefits much from Claude footnotes.

The GLM series demonstrates an important point: **academic citations belong in `.bib` files, not Claude footnotes.** The series properly references King, Tomz, Wittenberg (2000), Gelman, and others through Quarto's bibliography system. Adding "Note from Claude:" footnotes to verify already-cited papers would be redundant and confusing.

## Conclusion: On Being Useful at the Margins

This project succeeded, I think, precisely because it was marginal—both in the literal sense (footnotes are in the margins) and in the value sense (42 footnotes across 128 posts, mostly adding small bits of verification and context).

The temptation with AI tools is to use them to generate entire posts, to produce bulk content, to replace rather than augment. But maybe the most useful applications are exactly these marginal ones: fact-checking what's already written, adding recent citations, verifying specific claims, providing context.

The blog remains Jon's. The voice is Jon's. The arguments are Jon's. The code is Jon's. The statistics are Jon's. Claude just added some footnotes, and tried—across multiple agent instances, with varying success—to make them useful.

The project also demonstrates when AI assistance is *not* useful: where proper scholarly tools already exist (`.bib` files for citations), where content is primarily visual (hand-drawn diagrams), where code speaks for itself (data visualizations), or where genre conventions differ fundamentally from fact-asserting prose.

---

*This draft was written by Claude (Sonnet 4.5) on December 6, 2024. Jon, feel free to edit, restructure, or completely rewrite as you see fit. After all, maintaining your voice was the whole point.*
