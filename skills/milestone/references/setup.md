# Set up this machine (`setup`)

Prepares this machine for Orca workers: what the milestone skill needs, plus an optional guideline that tells agents when to hand everyday work to Orca worktrees. No project is involved. It is safe to rerun: a rerun brings each item up to date and skips what is already done. Never change anything outside the items below.

## 1. Check (read only)

Look at each item, then show one table: item, current state, what setup would do.

| Item | Check | Done when |
|---|---|---|
| Orca CLI | `orca --version` | It runs. If it does not, stop: Orca must be installed, and this session should run in an Orca terminal |
| Orca skills | `orca skills install --skill orca-cli --skill orchestration --dry-run --json` | Every op in the plan is `keep` |
| Delegation guideline | Section 3: where the guideline is now | A marked block holds the latest template |
| Worker context settings (Claude Code only) | Section 4 | Both entries are present |
| Orca repos | `orca repo list --json` | Section 5 finds nothing to report |

## 2. Ask once

Ask about everything that is not done in one round (Claude Code: one AskUserQuestion call; other agents ask in the conversation and wait). Explain each item in a sentence, including what changes on disk.

- **Orca skills** missing or outdated: install / skip. Installing runs `orca skills install --skill orca-cli --skill orchestration`, which links the copies into each detected agent's skills folder.
- **Delegation guideline:** where to put it (section 3) / skip.
- **Each missing worker context setting** (section 4): add / skip. They take effect in sessions started afterwards.

## 3. Delegation guideline

The source is this skill's `templates/orca-delegation.md`. Write it as is, except: replace `<milestone skill folder>` with this skill folder's absolute path, written as `~/…` when it is under the home folder, and use the heading level of the target file's other top sections (`#` or `##`).

**Where it can go**

| Choice | Claude Code | Codex |
|---|---|---|
| Global, every project (recommended) | `$CLAUDE_CONFIG_DIR/CLAUDE.md`, else `~/.claude/CLAUDE.md` | `$CODEX_HOME/AGENTS.md`, else `~/.codex/AGENTS.md` |
| This project only | `CLAUDE.local.md` at the root of the current git repo | Not offered: Codex has no personal per-project file |

Never write it into a project's `CLAUDE.md` or `AGENTS.md`: those are shared with the team, and this guideline is a personal choice. If the user picks This project and `git check-ignore CLAUDE.local.md` says the file is not ignored, warn that it would be committed and offer Global instead.

**Find what is there first,** in both the global and the project file:

- A marked block (`<!-- milestone-orca:start` … `<!-- milestone-orca:end -->`): this is an update. Replace only that block with the latest template, without asking where.
- An unmarked `Orca Task Delegation` section (up to the next heading of the same or a higher level), or an `orca-dispatch` block (`<!-- orca-dispatch:start` … `<!-- orca-dispatch:end -->`) that older setups wrote into `CLAUDE.local.md`: name it in the question. If the new block goes into the same file, it replaces that text in place. If it goes elsewhere, ask whether to remove the old text, so the guideline is not loaded twice.
- If the old text has rules the template does not (for example, rules for one workspace), show them and ask whether to keep them right after the block. Do not drop them silently.

Write only the block (and the old text you were told to replace or remove). Keep everything else in the file as it is. With nothing to replace, append the block at the end. Create the file if it is missing.

## 4. Worker context settings (Claude Code only)

Two entries in `$CLAUDE_CONFIG_DIR/settings.json`, else `~/.claude/settings.json`. They keep Orca workers from filling their context. Skip this section for other agents.

| Entry | What it does | Done when |
|---|---|---|
| `"CLAUDE_AUTOCOMPACT_PCT_OVERRIDE": "50"` in `env` | Sessions compact at about half their context instead of near the end. It applies to every Claude Code session on the machine, the coordinator included | `env` has the key, with any value |
| The `orca-send-guard.py` PreToolUse hook | Blocks `orca orchestration send` to a worker whose context is 50% or more full and tells the agent to start a fresh worker | `hooks.PreToolUse` has an entry whose command contains `orca-send-guard.py` |

- If `env` has the key with another value, keep it and report the value.
- To add, merge into the file: keep every other key and hook (Orca and other tools write their own hooks here), append to `env` and to the `hooks.PreToolUse` array, and check that the file still parses as JSON. If it does not parse before you start, do not edit it; put the entries in the report instead.
- The hook entry, with the command pointing at this skill folder's `scripts/orca-send-guard.py` (written with `$HOME` when it is under the home folder):
  ```json
  {
    "matcher": "Bash",
    "hooks": [
      {
        "type": "command",
        "command": "python3 \"$HOME/.agents/skills/milestone/scripts/orca-send-guard.py\"",
        "timeout": 30
      }
    ]
  }
  ```

## 5. Orca repos (report only)

From `orca repo list --json`, report two kinds of registered repos. Do not change them; give the user commands or steps instead.

- **Worktree base is a local branch** (`worktreeBaseRef` is a bare name such as `dev` or starts with `refs/heads/`): Orca then creates worktrees from stale, unpulled commits without fetching. `origin/<branch>` and `refs/remotes/origin/<branch>` are both remote and fine. Give `orca repo set-base-ref --repo path:<absolute repo path> --ref origin/<branch>`.
- **Worktree base not set** (`worktreeBaseRef` is empty): give the same command, with the branch the repo's work starts from.
- **Setup script in the Orca app settings** (`hookSettings.scripts.setup` is not empty) while the repo has an `orca.yaml`: the app setting makes Orca ignore `orca.yaml`. Tell the user to clear that repo's setup field in Orca's settings screen.

## 6. Report

A table of each item: done before / added or updated (with the file path) / skipped / could not be done (with why). Then say that the guideline and settings apply to agent sessions started after this.
