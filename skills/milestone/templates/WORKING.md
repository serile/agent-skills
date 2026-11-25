# <Project name> working rules

Every session doing <project name> work (the coordinator, Orca workers, sessions opened in other repos) follows the same rules. Only rules the whole team can see belong here.

## Project docs

| File | Purpose | How it changes |
|---|---|---|
| `PRODUCT.md` | Goals, current decisions, milestones, quality bar, deferred items, related repos. **The single source of truth** | Only the coordinator edits it. Changed decisions are overwritten |
| `DECISIONS.md` | Decisions valid now and why, by topic. What we do is in `PRODUCT.md`; why we chose it is here | When a decision is made, add one row (one-sentence decision, one-sentence reason) to its topic table. When a decision changes, rewrite its row and move the old row verbatim to Superseded decisions in `history/m<n>.md` |
| `history/m<n>.md` | Milestone record — verification rulings, dev environment checks (build numbers, hashes), superseded decisions verbatim | The coordinator only appends to it during the milestone. Not read during work; open it only to trace how an old decision came about |
| `BLOCKED.md` | What is blocked and who must unblock it. Open product decisions live here too | Add a row when blocked; when resolved, mark it Resolved with the date |
| `contracts/` | Contracts between repos (APIs, event formats, shared enums) | The coordinator freezes them when a milestone starts. Workers do not edit them |
| `briefs/` | Worker briefs | The coordinator writes them in the `_template.md` and `_verify-template.md` formats |

Absolute path: `<absolute path of the docs folder>`

## Rules

1. **When a session starts,** read `PRODUCT.md` and state three lines: current milestone / done criteria / what this session will finish.
2. **`PRODUCT.md` is the only source of truth.** Design docs and external docs (internal docs tools, Claude Docs, etc.) are synced only when a milestone ends. If they differ, `PRODUCT.md` is right.
3. **Only the coordinator edits the project docs.** Workers only read them and put anything that should change in their report.
4. **Do not ask about side issues.** Add one line to Deferred in `PRODUCT.md` and keep going. Report them together when the milestone ends.
5. **Make reversible technical decisions yourself** and record them in `DECISIONS.md`. Ask only about product decisions (anything customers or operators see or go through, money, legal).
   - `DECISIONS.md` holds only what someone would need a reason for before changing it later: product decisions, things decided against, behavior matched to external systems (external APIs, other teams' services), and hard-to-reverse technical decisions (data shape, storage, security, infrastructure, contracts between repos). Do not record implementation details the code or contracts already show, schedule shifts, or progress notes.
   - Verification rulings and dev environment checks go in `history/m<n>.md`. If a ruling yields a rule that stays valid, add just that rule to `DECISIONS.md` as one row.
6. **When blocked,** write it in `BLOCKED.md` (what, who must decide, which milestone it blocks) and continue with the next unblocked work. Stop and ask only when everything left is blocked.
7. **Before editing files in another repo,** read that repo's root `CLAUDE.md` and `AGENTS.md`. Its rules are not loaded automatically when you edit it from elsewhere.
8. **Do not reopen settled decisions.** If there is evidence a decision should be reversed, write it in `BLOCKED.md` with the evidence and ask.

## Running milestones

- The coordinator only coordinates; per-repo Orca workers implement. Hand each worker the **absolute path** of its brief in `briefs/`.
- Freeze anything that crosses repos in `contracts/` first, then run the workers in parallel.
- A separate Codex worker verifies, not the worker that implemented (if Codex is unavailable, a fresh worker other than the implementer). It reruns the done criteria itself and checks the diff against `PRODUCT.md`, the contracts and the briefs.
- No progress reports along the way. Report once at the end: done criteria results / summary of changes / what was added to or changed in `DECISIONS.md` / deferred items / `BLOCKED.md` / things for a person to check.
- When a milestone ends, update its status in `PRODUCT.md`, make sure no ruling, check or superseded rows remain in `DECISIONS.md` (move any to `history/m<n>.md`), bring external docs up to date in one pass, and commit and push the project docs.

## Branches

- <Project name> code lives on `<feature branch>` in each repo. Never commit directly to the default branch.
- For each milestone, workers create `<feature branch>-m<n>` from `origin/<feature branch>`, and the coordinator merges it into `<feature branch>` once verification passes.
- Orca worktrees branch off the default branch set in that repo's Orca project settings. If a worker needs something that is not on the default branch, list it under Prerequisites in the brief.
