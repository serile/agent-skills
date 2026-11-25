# agent-skills

Agent skills for Claude Code, Codex and other coding agents, installed with the [skills CLI](https://github.com/vercel-labs/skills).

| Skill | What it does |
|---|---|
| [`milestone`](skills/milestone/SKILL.md) | Runs multi-session, multi-repo work from one set of project docs split into milestones, with Orca workers doing the implementation |

## milestone

For work too big for one session: a new project, a feature that spans repos, or a refactor. `init` turns a design doc into project docs — `PRODUCT.md` as the single source of truth, plus `WORKING.md`, `DECISIONS.md` and `BLOCKED.md` — and cuts the work into milestones. For each milestone, a coordinator session writes briefs, runs one Orca worker per repo, and has a separate worker verify the result before anything is merged.

### Requirements

- [Orca](https://orca.dev) with its `orca-cli` and `orchestration` skills:
  ```bash
  orca skills install --skill orca-cli --skill orchestration
  ```
- Optional: [Codex](https://github.com/openai/codex), used as the verification worker. Without it, a fresh worker verifies instead.

### Install

```bash
npx skills add serile/agent-skills --skill milestone -g
```

Update with `npx skills update`. Do not edit the installed copy; updates overwrite it.

### Usage

```text
/milestone init <project> [design doc path …]   create the project docs and milestones, then wait for approval
/milestone start <project> <n>                   start milestone n
/milestone end <project> <n>                     close milestone n after you have checked the results
/milestone <project>                             resume
```

### What stays on your machine

- `~/.agents/milestone/projects.md` — your project registry. Created on first run; `init` adds a row per project, including Extra permissions: what the agent may do without asking in that project.
- Output folder — worker reports, verification results and baselines. `~/.gstack/projects/<workspace>/` if you use gstack, otherwise `~/.agents/milestone/artifacts/<workspace>/`.

### Language

The skill is written in English. Project docs and briefs are written in the language you work in.

### Default permissions

Without asking, the agent commits and pushes on the project's feature branch once the done criteria pass, and commits the project docs. When you close a milestone with `end`, it removes that milestone's merged worktrees and local worker branches; remote branches stay. It asks before merging into default branches, opening PRs, deploying to production, creating repos or changing external services. See section 4 of [SKILL.md](skills/milestone/SKILL.md).

## License

[MIT](LICENSE)
