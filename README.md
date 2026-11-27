# agent-skills

Agent skills for Claude Code, Codex and other coding agents, installed with the [skills CLI](https://github.com/vercel-labs/skills).

| Skill | What it does |
|---|---|
| [`milestone`](skills/milestone/SKILL.md) | Runs multi-session, multi-repo work from one set of project docs split into milestones, with Orca workers doing the implementation |

## milestone

For work too big for one session: a new project, a feature that spans repos, or a refactor. `init` turns a design doc into project docs — `PRODUCT.md` as the single source of truth, plus `WORKING.md`, `DECISIONS.md` and `BLOCKED.md` — and cuts the work into milestones. For each milestone, a coordinator session writes briefs, runs one Orca worker per repo, and has a separate worker verify the result before anything is merged.

### Requirements

- [Orca](https://orca.dev).
- Optional: [Codex](https://github.com/openai/codex), used as the verification worker. Without it, a fresh worker verifies instead.

### Install

```bash
npx skills add serile/agent-skills --skill milestone -g
```

Then run `/milestone setup` once per machine. It checks each item and asks before changing anything:

- Installs Orca's `orca-cli` and `orchestration` skills, which the coordinator uses to run workers.
- For Claude Code, adds two settings that keep workers from filling their context: `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=50`, so sessions compact at about half their context, and the `scripts/orca-send-guard.py` hook, which blocks `orca orchestration send` to a worker whose context is 50% or more full. `CONTEXT_GUARD_PERCENT` changes that limit; a worker it cannot measure (a Codex worker, an Orca error) is let through.
- Optionally writes the Orca task delegation guideline — when agents hand everyday, non-milestone work to Orca worktrees, and how they clean up after a merge — into your global `CLAUDE.md` or `AGENTS.md`, or into one project's `CLAUDE.local.md`.
- Reports Orca repos whose worktree base is a local branch, or whose setup script in the Orca app hides the repo's `orca.yaml`.

Update with `npx skills update milestone -g`, then rerun `/milestone setup` to bring the guideline up to date. Do not edit the installed copy; updates overwrite it.

### Usage

```text
/milestone setup                                 set up this machine: Orca skills, worker context settings, delegation guideline
/milestone init <project> [design doc path …]   create the project docs and milestones, then wait for approval
/milestone start <project> <n>                   start milestone n
/milestone end <project> <n>                     close milestone n after you have checked the results
/milestone resume <project>                      take over a milestone after the coordinator session broke off or was cleared
/milestone <project>                             read the project docs (worker briefs start with this)
```

While a milestone runs, the coordinator keeps a one-page state board, `STATE.md`, in the milestone's output folder: the Orca Run ID, where the milestone is, which brief each worker runs and what it is waiting for, and the next step. It is overwritten, never appended, and deleted at `end`. `resume` rebinds the Run, rereads worker status and mail from Orca, and carries on from there.

### What stays on your machine

- `~/.agents/milestone/projects.md` — your project registry. Created on first run; `init` adds a row per project, including Extra permissions: what the agent may do without asking in that project.
- What `setup` added, in the files you chose: the delegation guideline block (between `milestone-orca` markers) and the Claude Code settings.
- Output folder — worker reports, verification results, baselines and each running milestone's `STATE.md`. `~/.gstack/projects/<workspace>/` if you use gstack, otherwise `~/.agents/milestone/artifacts/<workspace>/`.

### Language

The skill is written in English. Project docs and briefs are written in the language you work in.

### Default permissions

Without asking, the agent commits and pushes on the project's feature branch once the done criteria pass, and commits the project docs. When you close a milestone with `end`, it removes that milestone's merged worktrees and their local branches (including the starting branches Orca creates with each worktree); remote branches stay. It asks before merging into default branches, opening PRs, deploying to production, creating repos or changing external services. See section 4 of [SKILL.md](skills/milestone/SKILL.md).

## License

[MIT](LICENSE)
