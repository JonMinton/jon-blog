# Preventing Merge Conflicts: experimental/claude → main

## The Problem

When merging `experimental/claude` to `main`, conflicts occur primarily in two types of files:

1. **Auto-generated files** (docs/*, _freeze/*): These change with every `quarto render`
2. **Source files** (.qmd): When both branches modify the same content (e.g., footnotes)

## Solutions (Ranked by Effectiveness)

### 🥇 Solution 1: Keep experimental/claude synced with main (BEST)

**Before starting any new work on experimental/claude:**

```bash
git checkout experimental/claude
git fetch origin
git merge origin/main
```

**Why this works:**
- Brings any main branch changes into experimental/claude
- Future work builds on top of main's state
- Minimizes divergence between branches
- Makes eventual merge to main straightforward

**Trade-off:** Slightly more overhead, but prevents painful merge conflicts

---

### 🥈 Solution 2: Commit source files only, render on main

**Workflow:**

1. On `experimental/claude`: Make changes, commit .qmd/.md/.R files
2. **Don't run `quarto render`** before committing
3. Merge to `main`
4. On `main`: Run `quarto render` once after merge

**Why this works:**
- Eliminates conflicts in docs/* and _freeze/*
- Only source files get merged
- Single render on main creates consistent output

**Trade-off:** Can't verify rendered output on experimental/claude before merging

**Modified workflow (if you need to verify renders):**
```bash
# On experimental/claude
quarto preview    # Check locally, don't commit the render
# Make changes, commit source only
git add posts/**/*.qmd CLAUDE.md .claude/*
git commit -m "message"
```

---

### 🥉 Solution 3: Use .gitignore for volatile files

Add to `.gitignore`:
```
_freeze/
docs/search.json
docs/sitemap.xml
```

**Keep in version control:**
```
docs/**/*.html
docs/**/*.png
docs/**/*.jpg
```

**Why this works:**
- Eliminates conflicts in frequently-changing generated files
- HTML/images still versioned for GitHub Pages
- Search/sitemap regenerated on each render

**Trade-off:** Search index changes won't show in git history

---

### 🎖️ Solution 4: Use rebase instead of merge (Advanced)

```bash
# On experimental/claude, before starting work
git fetch origin
git rebase origin/main
```

**Why this works:**
- Creates linear history
- Replays experimental/claude commits on top of main
- Cleaner git history

**Trade-off:**
- More complex (conflicts resolved during rebase, not merge)
- **Never rebase if branch is pushed/shared**
- Requires understanding of git rebase

---

## Recommended Combined Approach

For your workflow, I recommend **Solution 1 + Solution 2**:

### Daily workflow:

1. **Starting new work:**
   ```bash
   git checkout experimental/claude
   git pull origin main  # Keep synced
   ```

2. **Making changes:**
   - Edit .qmd, .md, CLAUDE.md, .claude/* files
   - Use `quarto preview` to check locally (don't commit render)
   - Commit only source files:
     ```bash
     git add posts/**/*.qmd .claude/*.md CLAUDE.md
     git commit -m "Descriptive message"
     ```

3. **Before merging to main (user's responsibility):**
   - Ensure experimental/claude is current with main
   - Merge or ask Claude agent to help resolve conflicts

4. **After merging to main:**
   ```bash
   git checkout main
   quarto render
   git add docs/
   git commit -m "Regenerate docs after merge"
   ```

---

## Quick Reference: Resolving Conflicts When They Happen

If conflicts occur despite prevention:

**For source files (.qmd, .md):**
```bash
git checkout --theirs path/to/file.qmd  # Use experimental/claude version
```

**For generated files (docs/*, _freeze/*):**
```bash
git checkout --theirs path/to/file.html  # Use experimental/claude version
# Then after merge:
quarto render  # Regenerate everything on main
```

**Verify resolution:**
```bash
git status  # Should show "nothing to commit" after git add
```

---

## Why This Happened Today

The footnote merge conflict happened because:

1. Numbered footnotes ([^1], [^4]) were changed to descriptive IDs ([^claude-ml], [^claude-mle])
2. Both changes happened only on experimental/claude
3. main still had the old numbered footnotes
4. When merging, git saw different content in the same location
5. Generated files (docs/*) also conflicted because they reflected different footnote IDs

**How the new approach prevents this:**
- Syncing experimental/claude with main first means both branches share the same base
- Changes are then made on top of that shared base
- When merging back, git sees a clean fast-forward or simple merge

---

## For Future Claude Agents

When starting work on experimental/claude:

1. ✅ Always run `git pull origin main` first to sync
2. ✅ Commit source files, optionally skip committing render output
3. ✅ Document any breaking changes in commit messages
4. ✅ Test locally with `quarto preview` before committing

When asked to help with merges:

1. ✅ Accept experimental/claude version for source conflicts (`--theirs`)
2. ✅ Accept experimental/claude version for generated files, then re-render
3. ✅ Verify merge success: `git status` should be clean after resolution
