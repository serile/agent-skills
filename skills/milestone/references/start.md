# Start a milestone (`start <project> <n>`)

`<n>` comes as `2` or `M2`. Read the name, result, done criteria, execution plan and prerequisites from the `| M<n> |` row of the milestone table in `PRODUCT.md`. If the number is not in the table, stop and ask. If the previous milestone is not Done, say so and ask.

The output folder is `<project>-m<n>-<YYYYMMDD>/` under the registry's output folder. Worker reports, evaluation results and baselines go there.

1. **State the three lines** (SKILL.md section 2) and set this milestone's status to "Active <date>".
2. **Check what comes first.** Pull "M<n> to-do (first)" and "Carry into M<n>" into this milestone's scope. Do nothing tied to a date or time before that time, and hold back the steps that depend on it.
3. **Show the human prerequisites.** List the prerequisites only the user can do (accounts, repos, keys, permissions, external settings). Do not copy them from the doc; check the real state (installs, keychain, repos, Orca registration, accounts, permissions) and mark what is already done and what you can do instead. Start once the user says they are done.
4. **For a refactor milestone, measure the baseline first.** Before running workers, measure what the done criteria compare (test count, typecheck, lint error count, bundle size, screenshots of key screens, etc.) and put it in the output folder's `baseline/`.
5. **Keep going until the done criteria pass.**
   - The coordinator only coordinates; per-repo Orca workers implement (SKILL.md section 3). Write briefs in the docs folder's `briefs/` as `m<n>-<short repo name>.md` in the `_template.md` format, and hand each worker the absolute path of its brief. With two or more workers in one repo, split May change so they do not overlap; if they must overlap, run them in sequence.
   - The worker branch is `<feature branch>-m<n>`, and the brief says it starts from `origin/<feature branch>` (Orca worktrees branch off the default branch). If the repo has no feature branch yet, the coordinator creates it from the default branch and pushes it.
   - If the done criteria in `PRODUCT.md` describe only behavior, turn them into commands and expected results in the brief.
   - Freeze anything that crosses repos (API contracts, event formats, shared enums) in `contracts/` first, then run the workers in parallel.
   - Briefs for workers that call paid APIs state a cost cap.
   - A separate Codex worker verifies, not the worker that implemented (if Codex is unavailable, a fresh worker other than the implementer). Its brief is `m<n>-verify.md` in the `_verify-template.md` format. Have it rerun the done criteria and check the diff against `PRODUCT.md`, the contracts and the briefs.
   - The coordinator rules on verification findings (fix, temporary exception, approved after the fact). Send fixes back to the implementing worker, or to a fresh worker when its context is too full (SKILL.md section 3, "Giving a worker more work"), and have them verified again; record rulings in the docs folder's `history/m<n>.md` (create it from this skill's `templates/history.md` if missing). If a ruling yields a rule that stays valid, add just that rule to `DECISIONS.md` as one row.
   - Dev environment checks (build numbers, hashes, test data) also go in `history/m<n>.md`. Whether they also go in `DECISIONS.md` follows `WORKING.md` rule 5; when a decision changes, rewrite its row and move the old row verbatim to Superseded decisions in `history/m<n>.md`.
   - When it passes, merge the worker branch into that repo's feature branch and push, then remove the merged worktree with `orca worktree rm`.
   - Commit and push changes to the project docs (contracts, briefs, rulings) as they happen.
   - No progress reports along the way.
6. **Report once at the end**, and write the same content to `REPORT.md` in the output folder.
   - For each done criterion, the command run and the result (numbers, output summary, screenshot paths)
   - Summary of changes (repo, branch, commits)
   - What was added to or changed in `DECISIONS.md`. Group temporary exceptions and after-the-fact approvals (Verification rulings in `history/m<n>.md`) separately
   - Deferred items. Group separately anything that was in this milestone's result but got dropped
   - BLOCKED: open rows blocking this milestone, and newly added rows
   - For the user to check: 3–5 things only a person can judge (where to go and what to try)

   Updating the status in `PRODUCT.md` and syncing external docs happen when the user confirms with `end`.
