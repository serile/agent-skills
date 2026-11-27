---
name: milestone
description: Run multi-session, multi-repo work (a new project, a feature in an existing service, or a refactor) from one set of project docs split into milestones, with Orca workers doing the implementation. Arguments — `init <project> [design doc paths]` creates the project docs, `start <project> <n>` starts a milestone, `end <project> <n>` closes one, `resume <project>` takes over a milestone after its coordinator session broke off or was cleared, and `<project>` alone reads the project docs. Also run it when the first line of a worker brief says to.
---

# Milestones

## Language

This skill is written in English, but the documents it creates follow the user. Write project docs, briefs, reports and registry rows in the language the user works in, translating template headings and status values too. When reading those files, find sections, columns and status values by meaning, not by exact text. Talk to the user in their language.

## 1. Find the project

Read the project registry, `~/.agents/milestone/projects.md`. It belongs to each person, so it never lives in this skill folder. If it does not exist, copy this skill's `templates/projects.md` there. Each row holds one project's docs folder, feature branch, output folder, external docs and extra permissions.

The first argument is a verb when it is `init`, `start`, `end` or `resume`; otherwise it is the project name.

- `init <project> [design doc path …]`: read `references/init.md` and follow it. Skip section 2.
- Otherwise, if `<project>` is not in the registry, stop and ask. With no argument, list the registered projects and ask.

## 2. Read the project docs and state three lines

Read `PRODUCT.md` and `WORKING.md` in the project's docs folder through the absolute path in the registry (the original checkout). Do not read copies inside worktrees. These two files win over every other document (design docs, external docs, memory). If you were given a worker brief, read it too.

Then tell the user three lines. The current milestone is the row whose status is Active, or else the first row that is not Done.

```
Current milestone: <name>
Done criteria: <summary of the done criteria in PRODUCT.md>
To finish this session: <concrete>
```

Then branch on the arguments.

- `<project>` alone: carry on with what you were given; a worker follows its brief. If you are a coordinator and the current milestone's output folder (`<project>-m<n>-*` under the registry's output folder) has a `STATE.md`, the milestone is mid-flight: say that `/milestone resume <project>` takes over its coordination, and wait.
- `start <project> <n>` (`2` or `M2`): read `references/start.md` and follow it.
- `end <project> <n>`: read `references/end.md` and follow it.
- `resume <project>`: read `references/resume.md` and follow it.

## 3. Session roles

- **Worker** (a session that received a brief, or whose prompt carries an Orca Task and Dispatch ID): do not spawn workers. Follow the worker duties in the `orchestration` skill (questions, final report), and only read the project docs. Put anything that should change in your report.
- **Coordinator** (any other session): the only session that edits the project docs. It does not implement; it runs workers with the `orchestration` skill. Before assigning workers, run that skill to read the guide for the installed Orca version, and follow its flow (register tasks, assign workers, questions and answers, final reports). Do not substitute your own subagents (the Agent tool).
- **Giving a worker more work.** Before you `send` a worker anything new (a fix, a follow-up, a next step), measure its context with `python3 <this skill folder>/scripts/context-usage.py --dispatch <dispatch_id>`. It assumes a 1M-token window; pass `--window` for a model with another window. Send to that worker only when the new work builds on what it just did and the result is under 50%. At 50% or more, or when the script reports unknown (a Codex worker, a missing transcript), start a fresh worker in the same worktree once the old one has settled. Hand it the brief, the previous worker's report and the new instructions as files, and tell it to continue on the existing branch instead of creating it.

## 4. Default permissions (on top of WORKING.md)

- **Do without asking:** commit and push on the project's feature branch (and branches under it) once the done criteria pass. Commit and push changes inside the docs folder to its repo. At `end`, remove the milestone's merged worktrees and their local branches (`references/end.md` step 5). Whatever the registry's Extra permissions column lists.
- **Ask first:** merging into a default branch (dev, main), opening PRs, production deploys, creating GitHub repos, changing external service settings, and any dev deploy or package publish not listed under Extra permissions.
- When a product decision is needed (anything customers or operators see or go through, money, legal), write it in `BLOCKED.md` and keep working on something else. Stop and ask only when everything left is blocked.
- Never print secrets (keychain, `.env`, API keys, tokens). Production databases are read-only.
