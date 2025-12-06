# Known Render Warnings

This file tracks known warnings that appear during `quarto render` that can be safely ignored or need investigation.

## Current Warnings (as of 2025-12-06)

### Duplicate note reference in lms-are-glms-part-02

**Warning:**
```
[WARNING] Duplicate note reference '1' at line 96 column 1
```

**File:** `posts/glms/intro-to-glms/lms-are-glms-part-02/index.qmd`

**Status:** ✅ SAFE TO IGNORE (likely stale cache)

**Details:**
- This warning appeared after we converted Claude footnotes to descriptive IDs
- We changed the Claude footnote from [^1] to [^claude-activations]
- Investigation shows only ONE [^1] definition (the original user footnote on line 58)
- The warning is likely from Quarto's cached state from before the fix

**Verified footnote structure:**
- Line 56: `[^1]` reference in text (for the masochistic base R graphics comment)
- Line 58: `[^1]: Using some base R graphics...` (definition)
- Line 90: `[^claude-activations]` reference in text (for the ML/activation functions comment)
- Line 94: `[^claude-activations]: **Note from Claude:**...` (definition)

**Verification:**
```bash
grep -n "\[^1\]" posts/glms/intro-to-glms/lms-are-glms-part-02/index.qmd
# Returns only 2 lines (reference and definition) ✓
```

**Resolution:** Warning should disappear after Quarto cache is cleared or on next clean render. The file is correct.

---

## Guidelines for Future Warnings

### When to document a warning here:

1. **Persistent warnings** that appear across multiple renders
2. **Unexplained warnings** that don't match the code
3. **Warnings we've decided to ignore** (with rationale)

### When to fix immediately:

1. **Duplicate footnote references** - these usually mean footnotes won't render
2. **Missing file references** - broken links
3. **Bibliography errors** - citations won't work

### When to ignore:

1. **Package version warnings** (e.g., "package built under R version X.X.X")
2. **libxml version warnings** (system library mismatch)
3. **Cosmetic warnings** that don't affect output

---

## How to Investigate Footnote Warnings

If you see a "Duplicate note reference" warning:

1. **Find the file and line number** from the warning
2. **Search for all instances** of that footnote number:
   ```bash
   grep -n "\[^N\]" path/to/file.qmd
   ```
3. **Check for:**
   - Multiple `[^N]:` definitions (should be only ONE)
   - References without definitions
   - Definitions without references

4. **Fix by:**
   - Removing duplicate definitions
   - Renumbering conflicting footnotes
   - Using descriptive IDs for Claude footnotes ([^claude-*])

---

## Historical Issues (Resolved)

### Footnote rendering failures (2025-12-06) - ✅ RESOLVED

**Problem:** 9 GLM posts had Claude footnotes that weren't rendering

**Root cause:**
1. Stale rendered output
2. Duplicate footnote numbers ([^1], [^4] used by both user and Claude)

**Solution:** Converted all Claude footnotes to descriptive IDs

**Files affected:** See `.claude/footnote-rendering-fix.md` for complete list

**Prevention:** Always use `[^claude-*]` format for Claude footnotes

---

## Quick Reference: Footnote Best Practices

**DO:**
- Use `[^claude-topic]` for all Claude-generated footnotes
- Verify footnote appears in rendered output after adding
- Run `quarto render` to check for warnings

**DON'T:**
- Use numbered IDs like `[^1]`, `[^2]` for Claude footnotes
- Add footnote definitions without corresponding references
- Ignore "Duplicate note reference" warnings
