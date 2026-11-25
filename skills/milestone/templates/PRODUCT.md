# <Project name> — Source of truth

This file is the single source of truth for <project name>. Working rules are in `WORKING.md`, the reasons behind decisions in `DECISIONS.md`, milestone records (verification rulings, checks) in `history/`, and open decisions and blockers in `BLOCKED.md`. Updated: <YYYY-MM-DD>.

## Goals

<!-- New project or feature: three lines on who it is for and what success looks like. Refactor: what is wrong now / how far the change goes / what must not change -->

1. 
2. 
3. 

## Out of scope

- 

## Current decisions

Only what is valid now, in the present tense. When something changes, overwrite it and fix its row in `DECISIONS.md` too.

- **<Topic>:** <decision>

## Open decisions

Open decisions and blockers live in one place, `BLOCKED.md`.

## Milestones

Status: Planned · Active <date> · Done <date> (remaining work) · Blocked (<reason>)

| # | Name | End-to-end result | Done criteria (run by the agent) | Execution plan | Human prerequisites | Status |
|---|---|---|---|---|---|---|
| M1 | | | | | | Planned |

<!-- To-dos tied to a date, time or waiting period: "M<n> to-do (first): …" -->
<!-- Things to look into or settle in that milestone: "M<n> to-do: …" -->
<!-- Carried over from an earlier milestone: "Carry into M<n> (from M<previous>, date): …" -->

## Quality bar

<!-- Only for results that need quality judgment (AI output, screen quality, etc.). Delete this section if there are none -->

| Milestone | Metric | Pass threshold (number) | Test set | Scoring (rule check · model grading · person) |
|---|---|---|---|---|

## Deferred

- 

## Related repos

| Repo | Absolute path | Owns | Rule files | Feature branch | Orca | Worker start condition (on the default branch) |
|---|---|---|---|---|---|---|
| <repo holding the project docs> | <absolute path> | Project docs `<docs folder>` (coordinator edits only) | `CLAUDE.md` | — | — | Workers read only |
