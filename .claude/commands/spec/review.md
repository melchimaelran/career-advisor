---
allowed-tools: Bash(cat:*), Bash(test:*), Bash(ls:*)
description: Review current specification phase or implementation
---

## Context

Active spec: !`cat spec/.current-spec 2>/dev/null || echo "none"`
Requirements approved: !`test -f spec/$(cat spec/.current-spec 2>/dev/null)/.requirements-approved && echo "Yes" || echo "No"`
Design approved: !`test -f spec/$(cat spec/.current-spec 2>/dev/null)/.design-approved && echo "Yes" || echo "No"`
Tasks approved: !`test -f spec/$(cat spec/.current-spec 2>/dev/null)/.tasks-approved && echo "Yes" || echo "No"`
Spec files: !`ls -1 spec/$(cat spec/.current-spec 2>/dev/null)/ 2>/dev/null | grep -E "(requirements|design|tasks)\.md"`

## Your Task

If active spec is "none": tell user to run `/spec:switch <spec-name>` to select one.

**If all three phases approved (requirements Yes, design Yes, tasks Yes) → Implementation Review:**
1. Read the full specification: requirements.md, design.md, tasks.md
2. Inspect the code changes implementing this spec (use git or grep as needed)
3. Verify compliance:
   - **Requirements:** checklist — is each requirement met?
   - **Design:** does implementation match the architecture and component choices?
   - **Tasks:** is every task completed and correct?
4. Deliver summary: deviations, bugs, areas for improvement, or confirmation

**If any phase NOT approved → Specification Review:**
1. Show approval status for each phase
2. Identify the first unapproved document (requirements → design → tasks)
3. Display its current content
4. Provide a review checklist:
   - Complete, clear, and unambiguous?
   - Meets all criteria for its type?
   - Missing elements or potential issues?
5. Remind user to run `/spec:approve <phase>` when satisfied