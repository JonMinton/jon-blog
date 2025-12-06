# Permanent Merge Conflict Solution (2025-12-06)

## What Was Done

Added volatile auto-generated files to `.gitignore` and removed them from version control to permanently prevent timestamp-based merge conflicts between `experimental/claude` and `main`.

## Files Added to .gitignore

```
_freeze/
docs/search.json
docs/sitemap.xml
```

## Why This Works

### Problem
These files change on every `quarto render`:
- **_freeze/**: Quarto's computational cache (timestamps, execution results)
- **docs/search.json**: Search index with timestamps
- **docs/sitemap.xml**: Site map with lastmod timestamps

When both `experimental/claude` and `main` rendered at different times, Git saw different timestamps as conflicts.

### Solution
- Files are now ignored by Git (not tracked)
- Generated fresh on each render
- No more timestamp conflicts during merges

## What's Still Tracked

Important rendered assets remain in version control:
- `docs/**/*.html` (all rendered HTML pages)
- `docs/**/*.png` (all images)
- `docs/**/*.jpg` (all images)

These are needed for GitHub Pages deployment.

## Impact on Workflow

### No change required for:
- `quarto preview` - works the same
- `quarto render` - still generates all files locally
- GitHub Pages - still deploys correctly (renders regenerate search/sitemap)

### What's different:
- `_freeze/`, `docs/search.json`, `docs/sitemap.xml` won't appear in `git status`
- Merging from experimental/claude to main: **no more timestamp conflicts**
- Repository is ~51,000 lines smaller (389 files removed)

## Testing

After this change:
1. ✅ Merge conflict resolved (timestamp conflicts in index.html, sitemap.xml)
2. ✅ Files added to .gitignore
3. ✅ 389 cache/volatile files removed from tracking
4. ✅ Repository size reduced
5. ✅ Committed successfully

## Future Merges

When merging `experimental/claude → main`:
- Timestamp conflicts: **eliminated**
- Source file conflicts: may still occur (handle with `git checkout --theirs` as documented in `.claude/merge-conflict-prevention.md`)
- After merge: run `quarto render` on main to regenerate fresh cache/search/sitemap

## Related Documentation

- [.claude/merge-conflict-prevention.md](.claude/merge-conflict-prevention.md) - Full merge conflict prevention strategies
- [.claude/session-startup-checklist.md](.claude/session-startup-checklist.md) - Session startup sync protocol
- [CLAUDE.md](../CLAUDE.md) - Project instructions including session startup

## Commit Reference

Commit: `d785898` (2025-12-06)
Message: "Prevent future merge conflicts by ignoring volatile files"
