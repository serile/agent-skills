# Create the project docs (`init <project> [design doc path …]`)

`<project>` is a short lowercase English name (`coupon`, `core-ui-refactor`). It names the docs folder, branches and output folder. It cannot be `setup`, `init`, `start`, `end` or `resume`, the skill's verbs. If it is already in the registry (`~/.agents/milestone/projects.md`), or the design doc already starts with a "The current source of truth is …" line (a design doc that has moved to other project docs), stop and ask.

## 1. Is this the right tool

Use it only when the work spans two or more sessions, two or more repos, or needs product decisions along the way. If none applies, say "this is better done without milestones" and stop.

## 2. Read the input

The input is the design docs passed as arguments, the records they point to (canvases, decision records, research docs), and what the user wrote in this conversation. Treat design docs the same wherever they came from. Do not research the web or code anew, and do not reopen decisions already made. When records contradict each other without saying which replaces which, do not pick; list them (section 7).

Move design doc content like this.

| Design doc content | Goes to |
|---|---|
| Change logs, update blocks | They win over the body, in date order. What a later record changed goes into Current decisions, and why into `DECISIONS.md`. Do not carry over old decisions (they stay in the design doc) |
| Problem, target users, success criteria | `PRODUCT.md` Goals, three lines |
| Rejected approaches, and constraints that mean "we won't" | Out of scope |
| Chosen approach | Current decisions |
| Proposals and things left undecided | If technical, Current decisions as a "starting proposal" (workers may change it). If customers or operators see it, treat it as a decision for a person (next row) |
| Decisions needed, open questions | Product decisions for a person go to `BLOCKED.md`. Things that measuring or looking into will settle go to "M<n> to-do" of the milestone that needs them, or to Deferred if not needed soon |
| Dependencies, things to wait for | Human prerequisites of the first milestone that needs them |
| Reviewer comments marked as blocking | Judge whether the current body resolves them. If not, split them as in the "Decisions needed" row |
| Evidence, facts, numbers, market research, schedule estimates, non-blocking review comments | Do not carry over. They stay in the design doc; briefs point to it by path and section under Facts to know |
| Observations about people, assignments, rollout plans | Do not carry over. A rollout plan that is an open product decision goes to the "Decisions needed" row |

If the input is too thin to write the goals and the first milestone's result, stop and say what is missing.

## 3. Fit the kind of work

- **New project** (a new app or server appears): fill every section of `PRODUCT.md`.
- **Feature** (finishes inside an existing service): Goals, Out of scope, milestones and Related repos carry the weight. Current decisions lists only what differs from the existing service.
- **Refactor:** in place of Goals, write what is wrong now, how far the change goes, and what must not change. Propose the target structure yourself and show it at approval. Cut milestones as "same visible behavior, changed structure" steps, and write done criteria as "matches the baseline" plus "what disappeared (files, dependencies, duplication)". `start` measures the baseline.

## 4. Decide where things live

- **Docs folder:** somewhere that does not follow branches. If the workspace root is a git repo, use `docs/<project>/` on its default branch; otherwise ask the user. Never inside a project code repo. Every session reads it through the absolute path of this original checkout.
- **Related repos:** for each repo write the absolute path, what it owns, its rule files (`CLAUDE.md`, `AGENTS.md`), feature branch, whether Orca knows it (`orca repo list --json`), and what must be on which branch before a worker can start. Read-only reference repos and non-repo dependencies (another team's work, etc.) go in too, saying so under what it owns. Repos not registered in Orca, or not created yet, go into the prerequisites of the first milestone that needs them.
- **Feature branch:** follow the repo's rules (e.g. `feature/<project>`). If repos differ, write each in the Related repos table and put the most common one in the registry. Workers work on `<feature branch>-m<n>` under it, one per milestone.
- **Output folder:** for things that are not committed, such as worker reports, evaluation results and baselines. The default is named after the workspace that holds the docs folder: `~/.gstack/projects/<workspace folder name>/`, or `~/.agents/milestone/artifacts/<workspace folder name>/` when `~/.gstack/` does not exist. Each milestone gets `<project>-m<n>-<YYYYMMDD>/` under it.

## 5. Create the docs

Copy this skill's `templates/` into the docs folder.

| Template | File to create |
|---|---|
| `PRODUCT.md` | `PRODUCT.md` (150 lines max, keep cells and bullets short) |
| `DECISIONS.md`, `BLOCKED.md`, `WORKING.md` | Same name |
| `history.md` | Not created — `start` creates `history/m<n>.md` per milestone |
| `STATE.md` | Not created — `start` creates it in each milestone's output folder |
| `orca-delegation.md` | Not created — `setup` writes it into the user's own instruction file |
| `brief.md`, `brief-verify.md` | `briefs/_template.md`, `briefs/_verify-template.md` |
| `projects.md` | Not created — it is the registry template (SKILL.md section 1) |

- In the brief templates, fill only the per-project slots (project name, docs path, feature branch, output folder) and leave the per-milestone slots as they are.
- Current decisions holds only what is valid now, in the present tense. Do not pile up change blocks.
- Decisions from the input that are still valid go into the topic tables of `DECISIONS.md` with date and source (only those that need a reason, per `WORKING.md` rule 5).
- `BLOCKED.md` holds only product decisions for a person (what, who decides, which milestone it blocks). Logged is the date the issue was first recorded. `PRODUCT.md` holds no open decisions.
- `start` creates `contracts/`.

## 6. Cut milestones

- Name each one as an outcome sentence ("Reviews show up on the operator screen"), not as a feature bundle ("Operator screen and import").
- Size each so one coordinator session can finish it (usually about a day). Do not aim for a particular count.
- Make the first one the thinnest: one flow working end to end, like one input → stored → one screen, ideally within two repos and not blocked by open decisions.
- Write done criteria as commands the agent runs, with expected results. If no command exists yet, write the behavior to check and the expected result; `start` turns it into a command in the brief.
- Results that need quality judgment (AI output, screen quality, etc.) get numeric pass thresholds and a scoring method (rule check, model grading, person) in the Quality bar section. If the input has no numbers, propose them from test results and mark them "init proposal". Without a bar, agents end up grading themselves.
- For each milestone, write the execution plan (which repo's workers, in what order) and the human prerequisites (repos, Orca registration, DB, deploy jobs, external accounts, keys).
- Do not schedule.
- To-dos tied to a date, time or waiting period (external review, etc.) go to "M<n> to-do (first)", not to Deferred.

## 7. Show and wait

Show only the following and wait for approval. Before approval, do not implement and do not do section 8.

- `PRODUCT.md` Goals and Out of scope
- The milestone table (with the target structure proposal for a refactor)
- Open decisions that block the first milestone, and its human prerequisites (for the other open decisions, just say how many are in `BLOCKED.md`)
- Quality bar numbers marked "init proposal"
- Records that contradict each other
- An Extra permissions proposal: what could be done without asking in this project (dev deploys, publishing package dev builds, etc.). Record only what the user picks.

## 8. Once approved

1. Add one line at the top of the design doc: "The current source of truth is `<absolute path of PRODUCT.md>` (since YYYY-MM-DD). This document is the record up to then." Do not edit the design doc after that.
2. If memory holds this project's design, shrink it to one pointer: "<project> work starts with `/milestone <project>`".
3. Add a row to the registry (`~/.agents/milestone/projects.md`). Never edit files inside this skill folder. Under External docs, list the documents `end` keeps in sync (a project page in an internal docs tool, Claude Docs, etc.; leave it empty if none).
4. Commit and push the docs folder.
5. Say "Next: `/milestone start <project> 1`".
