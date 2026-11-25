First run the `milestone` skill for `<project>` (`/milestone <project>`). If the skill is not installed, read `<absolute path of PRODUCT.md>` and `<absolute path of WORKING.md>`.

# <Milestone name> — Verification: rerun done criteria · check the diff · <what to watch especially this time>

- Workspace: **read** the worktrees below and run commands there. **Do not change code.** Create verification temp files, screenshots and reports only under `<absolute path of the output folder>/verify/`
  - <repo>: `<absolute worktree path>` · branch `<feature branch>-m<n>` (base `origin/<feature branch>` = <commit>)
  - In repos that commit build output, do not run build or codegen commands in the worker's worktree. Check out a separate copy with `git worktree add --detach <path under the verify folder> <branch>`, run them there, and `git worktree remove` it when done
- Implementation briefs: <absolute paths of briefs/ files>
- Frozen contracts: <absolute paths of contracts/ files. "None" if none>
- Cost cap: <amount if paid APIs are called again. Otherwise "None">

## 1. Rerun the done criteria

Rerun every row of the done criteria tables in the implementation briefs, and this milestone's done criteria in `PRODUCT.md`. Do not trust a "pass" the implementing worker reported.

| Command or check | Expected result |
|---|---|
| `<command>` | <expected result> |

## 2. Quality judgment

<This milestone's rows from the Quality bar in `PRODUCT.md`. Judge items the grading model flagged as ambiguous yourself, against the source. Delete this section if none>

## 3. Check the diff

Read the diff from the base to `<feature branch>-m<n>` and check:

- whether contract paths, fields, statuses and error codes match across repos
- whether any behavior differs from Current decisions in `PRODUCT.md` or from Build in the briefs
- whether anything outside May change was changed

## 4. Look hard at

<What is easy to break in this milestone: security, edge cases. Point to code, and reproduce where you can>

## Do not touch

- Source, commits and branches of the worktrees under verification (findings go in the report only)
- The project docs and contracts in `<docs folder>`
- <external services and DBs read-only, no production resources, etc.>

## If blocked

- Paste the original output of environment problems (ports, login, tokens, installs) into the report and continue with the other rows.
- Do not use `--no-verify`, `git stash`, `git checkout .`, `git reset --hard` or force push. Do not push or merge.

## Report when done

Write the full report to `<absolute path of the output folder>/verify/REPORT.md`, and only a summary in the `worker_done` message. On re-verification, add a section to the same file.

1. Each done criterion: the command run, a summary of the raw result, and a verdict (pass / fail / could not check)
2. Quality judgment table and paths to the evidence files
3. Diff and section 4 findings (by severity, file:line, evidence, how to reproduce)
4. Screenshot paths
5. Anything that looks inconsistent with the project docs or contracts
