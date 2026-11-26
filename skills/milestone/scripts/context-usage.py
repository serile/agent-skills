#!/usr/bin/env python3
"""Claude Code 세션이 지금 컨텍스트를 얼마나 쓰고 있는지 대화 기록(JSONL)에서 잰다.

마지막 응답의 입력 토큰(input + cache_creation + cache_read)이 지금 컨텍스트 크기다.
Claude Code 는 창 크기를 대화 기록에 남기지 않아서, 퍼센트는 --window 로 받은 창 크기로 계산한다.

  context-usage.py                     이 세션 (CLAUDE_CODE_SESSION_ID)
  context-usage.py --dispatch <id>     Orca 워커 (worker-read 로 대화 기록을 찾는다)
  context-usage.py --session <id>      세션 id
  context-usage.py --transcript <path> 대화 기록 파일

종료 코드: 0 = 쟀다, 2 = 알 수 없다 (Claude Code 워커가 아님, 기록을 못 찾음 등).
"""

import argparse
import json
import os
import shlex
import subprocess
import sys
import time
from pathlib import Path

DEFAULT_WINDOW = 1_000_000
# 메시지 id 로 기록을 찾을 때 프로젝트 폴더 밖까지 뒤지는 범위 (최근 수정된 파일만)
FALLBACK_SCAN_DAYS = 7


def projects_dir() -> Path:
    base = os.environ.get("CLAUDE_CONFIG_DIR") or str(Path.home() / ".claude")
    return Path(base) / "projects"


def project_slug(path: str) -> str:
    # Claude Code 는 작업 폴더 경로의 영숫자가 아닌 글자를 '-' 로 바꿔 프로젝트 폴더 이름을 만든다
    return "".join(c if c.isalnum() else "-" for c in path)


def unknown(reason: str, as_json: bool) -> None:
    if as_json:
        print(json.dumps({"known": False, "reason": reason}))
    else:
        print(f"context: unknown ({reason})")
    sys.exit(2)


def newest_first(paths):
    return sorted(paths, key=lambda p: p.stat().st_mtime, reverse=True)


def find_by_session(session_id: str):
    hits = list(projects_dir().glob(f"*/{session_id}.jsonl"))
    return newest_first(hits)[0] if hits else None


def find_by_message(message_id: str, workspace_path):
    # fork 된 세션은 옛 메시지를 복사해 가지므로, 같은 id 가 여러 파일에 있으면 가장 최근 파일을 쓴다
    needle = message_id.encode()
    root = projects_dir()
    if workspace_path:
        local = root / project_slug(workspace_path)
        for f in newest_first(local.glob("*.jsonl")) if local.is_dir() else []:
            if needle in f.read_bytes():
                return f
    cutoff = time.time() - FALLBACK_SCAN_DAYS * 86400
    recent = [f for f in root.glob("*/*.jsonl") if f.stat().st_mtime >= cutoff]
    for f in newest_first(recent):
        if needle in f.read_bytes():
            return f
    return None


def resolve_dispatch(dispatch_id: str, as_json: bool) -> Path:
    orca = shlex.split(os.environ.get("ORCA_CLI_COMMAND") or "orca")
    cmd = orca + [
        "orchestration", "worker-read", "--dispatch", dispatch_id,
        "--source", "transcript", "--limit", "1", "--json", "--full",
    ]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.TimeoutExpired) as e:
        unknown(f"could not run orca: {e}", as_json)
    try:
        data = json.loads(out.stdout)
    except json.JSONDecodeError:
        unknown(f"orca worker-read failed: {(out.stderr or out.stdout).strip()[:300]}", as_json)
    if not data.get("ok"):
        unknown(f"orca worker-read failed: {json.dumps(data.get('error'))[:300]}", as_json)
    result = data.get("result") or {}
    provider = result.get("provider")
    if provider != "claude":
        unknown(f"worker agent is {provider!r}, not Claude Code", as_json)
    messages = (result.get("transcript") or {}).get("messages") or []
    if not messages or not messages[-1].get("id"):
        unknown("worker transcript has no messages yet", as_json)
    workspace_id = ((result.get("projection") or {}).get("workspace") or {}).get("id") or ""
    workspace_path = workspace_id.split("::")[-1] if "::" in workspace_id else None
    path = find_by_message(messages[-1]["id"], workspace_path)
    if not path:
        unknown("transcript file not found on this machine", as_json)
    return path


def measure(path: Path):
    last_tokens = None
    model = None
    compactions = 0
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            # json 파싱 전에 글자로 먼저 걸러서 큰 기록도 빠르게 읽는다
            if "compact_boundary" in line:
                try:
                    o = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if o.get("type") == "system" and o.get("subtype") == "compact_boundary":
                    compactions += 1
                continue
            if '"usage"' not in line or '"assistant"' not in line:
                continue
            try:
                o = json.loads(line)
            except json.JSONDecodeError:
                continue
            if o.get("type") != "assistant" or o.get("isSidechain"):
                continue
            msg = o.get("message") or {}
            usage = msg.get("usage") or {}
            tokens = sum(
                usage.get(k) or 0
                for k in ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens")
            )
            # 오류 응답 같은 합성 메시지는 사용량이 0 이라 건너뛴다
            if tokens <= 0 or msg.get("model") == "<synthetic>":
                continue
            last_tokens = tokens
            model = msg.get("model")
    return last_tokens, model, compactions


def main() -> None:
    ap = argparse.ArgumentParser(description="Measure a Claude Code session's current context size.")
    group = ap.add_mutually_exclusive_group()
    group.add_argument("--dispatch", help="Orca worker dispatch id")
    group.add_argument("--session", help="Claude Code session id")
    group.add_argument("--transcript", help="path to a transcript .jsonl")
    ap.add_argument(
        "--window", type=int,
        default=int(os.environ.get("CONTEXT_WINDOW_TOKENS") or DEFAULT_WINDOW),
        help=f"context window in tokens (default: $CONTEXT_WINDOW_TOKENS or {DEFAULT_WINDOW:,})",
    )
    ap.add_argument("--json", action="store_true", help="print JSON")
    args = ap.parse_args()

    if args.transcript:
        path = Path(args.transcript).expanduser()
        if not path.is_file():
            unknown(f"no such file: {path}", args.json)
    elif args.dispatch:
        path = resolve_dispatch(args.dispatch, args.json)
    else:
        session_id = args.session or os.environ.get("CLAUDE_CODE_SESSION_ID")
        if not session_id:
            unknown("no session id: pass --session, --dispatch or --transcript", args.json)
        path = find_by_session(session_id)
        if not path:
            unknown(f"no transcript for session {session_id}", args.json)

    tokens, model, compactions = measure(path)
    if tokens is None:
        unknown(f"no model response in {path} yet", args.json)
    percent = round(tokens * 100 / args.window)
    if args.json:
        print(json.dumps({
            "known": True, "tokens": tokens, "window": args.window, "percent": percent,
            "compactions": compactions, "model": model, "transcript": str(path),
        }))
    else:
        print(
            f"context: {tokens:,} tokens of a {args.window:,} window ({percent}%)"
            f" · compactions: {compactions} · model: {model} · transcript: {path}"
        )
    if tokens > args.window:
        print("warning: tokens exceed the window; pass the model's real window with --window", file=sys.stderr)


if __name__ == "__main__":
    main()
