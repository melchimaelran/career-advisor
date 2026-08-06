---
allowed-tools: Bash(ls:*), Bash(cat:*), Bash(grep:*), Bash(test:*), Bash(find:*)
description: Show all specifications and their status
---

## Gather Status Information

All specs: !`ls -d spec/*/ 2>/dev/null | sort`
Current spec: !`cat spec/.current-spec 2>/dev/null || echo "None"`

For each spec directory found above, use the Bash tool to check:
- `ls -la spec/<dir>/` — lists phase files (.md) and approval markers (.*-approved)
- `grep "^- \[" spec/<dir>/tasks.md | head -5` — task preview (if tasks.md exists)
- `grep -c "^- \["  spec/<dir>/tasks.md` — total tasks count
- `grep -c "^- \[x\]" spec/<dir>/tasks.md` — completed tasks count

## Your Task

Present a clear status report showing:
1. All specifications with their IDs and names
2. Current active spec (highlighted)
3. Phase completion status for each spec
4. Task progress percentage if applicable
5. Recommended next action for active spec
