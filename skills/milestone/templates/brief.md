First run the `milestone` skill for `<project>` (`/milestone <project>`). If the skill is not installed, read `<absolute path of PRODUCT.md>` and `<absolute path of WORKING.md>`.

# <Milestone name> — <repo name>: <one line on what this brief covers>

- Workspace: <Orca worktree or repo absolute path> · branch `<feature branch>-m<n>`
- Prerequisites: as soon as you start, `git fetch origin && git checkout -b <feature branch>-m<n> origin/<feature branch>`. <Anything else that must be on which branch of which repo. Omit if none>
- Parallel workers: <other brief file names and where they meet (contracts). "None" if none>
- Frozen contracts (do not edit): <absolute paths of contracts/ files. "None" if none>
- Cost cap: <amount if paid APIs are used. Otherwise "None">
- Report file: `<absolute path of the output folder>/<short repo name>/REPORT.md`

## Goal

<One or two sentences on what works when this is done. Describe behavior, not documents>

## Facts to know

<Facts this work needs, with paths: earlier milestone results, test results, failure cases, tools to use. Delete this section if none>

## Build

1. <…>

## Done criteria

<Only what the agent can run and check itself. Pair each command with its expected result>

| Command or check | Expected result |
|---|---|
| `<command>` | <exit 0, N rows, what shows on screen, etc.> |

## May change

- <paths>

## Do not touch

- The project docs and contracts in `<docs folder>` (put changes in your report)
- <other paths, settings, other repos, production resources>

## Decide without asking

- Reversible technical choices (names, internal structure, minor library choices). List them under Decisions made in your report.
- <anything specially allowed for this work>

## If blocked

- If a product decision is needed, do not stop: note it under Blocked in your report and do the next unblocked work.
- Do not work around permission, secret or external account problems. Paste the original error into the report (with secrets removed).
- Do not use `--no-verify`, forced lockfile updates, `git stash`, `git checkout .`, `git reset --hard` or force push.
- Push, merge or publish only when this brief says so.

## Report when done

Write the full report to the report file, and only a summary in the `worker_done` message.

- Each row of the done criteria table: the command run and a summary of the raw result (pass / fail)
- Commit hashes and the list of changed files
- Decisions made (→ the coordinator moves them into `DECISIONS.md`)
- Blocked (→ `BLOCKED.md`)
- Side findings (→ Deferred in `PRODUCT.md`)
- Anything that looks inconsistent with the project docs or contracts
