#!/usr/bin/env python3
"""Claude Code PreToolUse hook: 컨텍스트가 찬 Orca 워커에게 `orca orchestration send` 로 일을 더 보내는 것을 막는다.

settings.json 에 이렇게 건다:
  "hooks": { "PreToolUse": [ { "matcher": "Bash", "hooks": [ { "type": "command",
    "command": "python3 \"$HOME/.agents/skills/milestone/scripts/orca-send-guard.py\"", "timeout": 30 } ] } ] }

- 명령에 `orchestration send` 와 `--to dispatch:<id>` 가 둘 다 있을 때만 잰다. 다른 Bash 명령은 바로 통과한다.
- 잰 값이 기준(기본 50%, CONTEXT_GUARD_PERCENT 로 바꿈) 이상이면 막고, 이유를 Claude 에게 돌려준다.
- 잴 수 없으면 (Codex 워커, orca 오류, 시간 초과) 막지 않는다. 그때 판단은 milestone 스킬 규칙에 맡긴다.
- 명령 앞에 CONTEXT_GUARD_SKIP=1 을 붙이면 통과한다. 아직 일하는 워커에게 짧게 방향만 바로잡을 때 쓴다.
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path

SEND = re.compile(r"orchestration\s+send\b")
TARGET = re.compile(r"--to[=\s]+[\"']?dispatch:([A-Za-z0-9_-]+)")
SKIP = re.compile(r"(^|[\s;&|(])CONTEXT_GUARD_SKIP=1(\s|$)")
# hook 전체 timeout(30초) 안에 끝나도록 워커 하나당 측정 시간을 묶는다
MEASURE_TIMEOUT_SECONDS = 25


def measure(dispatch_id: str):
    script = Path(__file__).with_name("context-usage.py")
    try:
        out = subprocess.run(
            [sys.executable, str(script), "--dispatch", dispatch_id, "--json"],
            capture_output=True, text=True, timeout=MEASURE_TIMEOUT_SECONDS,
        )
        return json.loads(out.stdout)
    except (OSError, subprocess.TimeoutExpired, json.JSONDecodeError):
        return None


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return
    if data.get("tool_name") != "Bash":
        return
    command = (data.get("tool_input") or {}).get("command") or ""
    if not SEND.search(command) or SKIP.search(command):
        return
    dispatch_ids = list(dict.fromkeys(TARGET.findall(command)))
    if not dispatch_ids:
        return

    limit = int(os.environ.get("CONTEXT_GUARD_PERCENT") or 50)
    full = []
    for dispatch_id in dispatch_ids:
        result = measure(dispatch_id)
        if result and result.get("known") and result.get("percent", 0) >= limit:
            full.append((dispatch_id, result))
    if not full:
        return

    lines = [
        f"- dispatch:{d}: {r['tokens']:,} tokens, {r['percent']}% of a {r['window']:,}-token window"
        for d, r in full
    ]
    reason = "\n".join([
        f"Blocked: this sends more work to an Orca worker whose context is at or above {limit}%.",
        *lines,
        "Start a fresh worker in the same worktree once this one has settled, and hand it the brief,"
        " this worker's report and the new instructions as files"
        " (milestone skill, \"Giving a worker more work\").",
        "Only for a short course correction to a worker that is still running,"
        " rerun the same command prefixed with CONTEXT_GUARD_SKIP=1.",
    ])
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }))


if __name__ == "__main__":
    main()
