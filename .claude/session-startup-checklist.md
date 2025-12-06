# Session Startup Checklist

## For Jon (User) - Quick Reference

When starting a new Claude Code session on this project:

**Default expectation:** You should be on `experimental/claude` branch

**If Claude reports you're on `main`:**
- This is unusual - did you intend to work on main?
- If NO: Switch to experimental/claude: `git checkout experimental/claude`
- If YES: Tell Claude explicitly "I'm working on main intentionally"

**Claude will automatically run at session start:**
```bash
git fetch origin
git merge origin/main
```

This keeps your experimental branch in sync and prevents merge conflicts.

---

## For Claude Agents - Automatic Session Startup

**FIRST THING in every session (before any other work):**

```bash
# 1. Check branch
BRANCH=$(git branch --show-current)

# 2. If on main, STOP and alert user
if [ "$BRANCH" = "main" ]; then
  echo "⚠️  WARNING: You are on the main branch"
  echo "Did you intend to work on main? (Most work should be on experimental/claude)"
  # WAIT for user confirmation before proceeding
fi

# 3. If on experimental/claude, auto-sync
if [ "$BRANCH" = "experimental/claude" ]; then
  echo "Syncing experimental/claude with main to prevent merge conflicts..."
  git fetch origin
  git merge origin/main

  if [ $? -eq 0 ]; then
    echo "✓ Branch synced with main"
  else
    echo "⚠️  Merge conflicts during sync - please review"
    # Report conflicts to user
  fi
fi
```

**After this check completes successfully, proceed with normal session work.**

---

## Why This Matters

**Problem:** When experimental/claude diverges from main (because main has new commits), merging back becomes painful with conflicts in:
- Auto-generated files (docs/*, _freeze/*)
- Modified source files (.qmd)

**Solution:** Sync experimental/claude with main at the START of each session, before making any changes.

**Result:** When you eventually merge experimental/claude → main, git sees a clean merge (or fast-forward) because experimental/claude is already up-to-date with main.

---

## Visual Diagram

**WITHOUT startup sync:**
```
main:              A --- B --- C --- D
                        \
experimental/claude:     X --- Y --- Z
                                    \
                                     CONFLICT when merging!
```

**WITH startup sync:**
```
main:              A --- B --- C --- D
                                    \
experimental/claude:                 D' --- X --- Y --- Z
                                                         \
                                                          Clean merge!
```

Where `D'` is the result of syncing main into experimental/claude.

---

## Expected Session Flow

1. **User opens new session**
2. **Claude automatically checks branch and syncs**
3. **Claude reports:** "✓ On experimental/claude, synced with main"
4. **Normal work begins** - editing files, commits, etc.
5. **User merges to main** (outside Claude session or with explicit instruction)
6. **No conflicts!** Because branches were kept in sync

---

## Manual Commands (for reference)

If you need to run these manually:

```bash
# Check what branch you're on
git branch --show-current

# Switch to experimental/claude
git checkout experimental/claude

# Sync with main
git fetch origin
git merge origin/main

# If there are conflicts during sync:
git status  # See what's conflicted
# Resolve conflicts, then:
git add .
git commit -m "Merge main into experimental/claude"
```

---

## Exception Cases

**"I want to work on main for deployment/hotfix"**
- Tell Claude: "I'm working on main intentionally"
- Claude will skip the branch switch and sync
- Claude will still warn before making changes

**"experimental/claude has conflicts when syncing"**
- This means main has changes that conflict with experimental/claude
- Resolve conflicts before continuing work
- Better to resolve NOW than during eventual merge to main

**"I want a different branch"**
- Tell Claude: "Switch to branch X" or "I'm on branch X intentionally"
- Claude will adapt workflow accordingly
