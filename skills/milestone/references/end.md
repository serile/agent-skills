# Close a milestone (`end <project> <n>`)

This means the user has checked the M<n> results. Work from the `| M<n> |` row of the milestone table in `PRODUCT.md`.

1. **Check whether it can close.** If any of the following exist, do not change the status. Show the list and ask whether to wait until they are resolved or to close with them moved to remaining work.
   - Rows in `BLOCKED.md` that block M<n> and are still Open
   - Done criteria in the output folder's `REPORT.md` with no result or a failure. If there is no `REPORT.md`, ask for the final report to be pasted

   If the user chooses to close with remaining work, add a line under Verification rulings in `history/m<n>.md`.
2. Set M<n>'s status in `PRODUCT.md` to "Done <date>". Note any remaining work (moved in step 1, or tied to a date) in the same cell. If `DECISIONS.md` still has this milestone's ruling or check rows, or superseded rows, move them to `history/m<n>.md` (`WORKING.md` rule 5).
3. Bring the documents in the registry's External docs column (a project page in an internal docs tool, a Claude Docs design doc, etc.) up to date with this milestone. If that tool has a writing guide, read it first. Skip this if the column is empty.
4. Commit and push the changes in the docs folder.
5. **Clean up this milestone's worktrees and branches.** `end` is the user's go-ahead, so do not ask again.
   - Targets: Orca worktrees (`orca worktree list --limit 10000 --json`) whose branch is `<feature branch>-m<n>` or starts with `<feature branch>-m<n>-`, or whose path a brief of this milestone or its `STATE.md` named, and temporary worktrees this milestone's sessions left in the related repos (`git worktree list`: detached checkouts under the output folder or a scratchpad). Leave other milestones' and other projects' worktrees alone.
   - Check each one after `git fetch --prune`: no uncommitted changes (throwaway files such as test logs may go), no unpushed commits, and its HEAD is in `origin/<feature branch>` or the default branch (`git merge-base --is-ancestor`). If a check fails, keep it and say why. Also keep any worktree whose worker you still need to message; removing a worktree closes its worker's terminal.
   - Remove Orca worktrees with `orca worktree rm --worktree "id:<id>" --json` (`--force` only when the leftovers are throwaway files) and temporary ones with `git worktree remove <path>` in their repo. Do not pass `--delete-branch`: on a worktree that has the feature branch checked out, Orca may delete the feature branch as merged.
   - Then, in each related repo, delete two kinds of local branches: the worker branches (`<feature branch>-m<n>` or `<feature branch>-m<n>-*`), and the starting branch Orca created with each removed worktree (`<prefix>/<worktree name>`, the prefix coming from Orca's branch prefix setting). Workers move to the worker branch as soon as they start, so the starting branch is left unused. Note the worktree names before removing the worktrees.
   - Try `git branch -d` first. If it refuses, delete with `-D` only when `git rev-list --count <branch> --not --remotes=origin` is 0 after `git fetch --prune`: everything is on the remote, so nothing is lost (`-d` refuses a branch with no upstream unless the checked-out branch contains it). Otherwise keep it and say so. Never delete the feature branch or a default branch. Leave remote branches alone; other people and the docs may still refer to them.
   - Delete `STATE.md` from the milestone's output folder; `REPORT.md` keeps the outcome.
   - Include what was removed and what was kept, with reasons, when you report the close.
6. Show the Deferred list. Propose moving what belongs in the next milestone to "Carry into M<next>" in `PRODUCT.md`.
7. Propose the next milestone's plan, including its execution plan and human prerequisites, and say "Next: `/milestone start <project> <next>`". If this was the last milestone, show the remaining BLOCKED and Deferred items, and ask whether to merge the feature branch into the default branch.
