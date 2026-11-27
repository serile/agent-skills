# M<n> state

The coordinator's state board, read by `/milestone resume <project>`. Overwrite it whenever the state changes; never append. It holds only what Orca and git cannot tell: worker status is read live from Orca, and decisions, rulings and checks go where `WORKING.md` says.

Updated: <YYYY-MM-DD HH:MM>
Orca Run: <Run ID> (objective `<project> M<n>`)
Phase: <where the milestone is, e.g. contracts frozen ✓ → implementation ✓ → verification round 1: 2 findings → fixes → verification round 2>

## Workers

| Repo | Brief | Task · Dispatch | Worktree · branch | Waiting for |
|---|---|---|---|---|

## Next

- Next step: <one to three lines>
- Findings not yet ruled on: <none, or the list>
- Questions to answer: <none, or the list>
