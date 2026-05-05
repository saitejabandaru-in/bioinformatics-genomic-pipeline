"""Shared command, path, and metadata utilities."""

from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence


@dataclass(frozen=True)
class CommandResult:
    command: list[str]
    returncode: int
    stdout: str
    stderr: str


def path_arg(value: str) -> Path:
    return Path(value).expanduser().resolve()


def ensure_parent(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def command_to_text(command: Sequence[str]) -> str:
    return " ".join(str(part) for part in command)


def run_command(command: Sequence[str], *, dry_run: bool = False, cwd: Path | None = None) -> CommandResult:
    command_list = [str(part) for part in command]
    if dry_run:
        return CommandResult(command_list, 0, command_to_text(command_list), "")

    completed = subprocess.run(
        command_list,
        cwd=cwd,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            f"Command failed ({completed.returncode}): {command_to_text(command_list)}\n{completed.stderr}"
        )
    return CommandResult(command_list, completed.returncode, completed.stdout, completed.stderr)


def write_json(path: Path, payload: dict) -> Path:
    ensure_parent(path).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def add_common_flags(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    parser.add_argument("--dry-run", action="store_true", help="print the generated command without running it")
    return parser


def require_inputs(paths: Iterable[Path]) -> None:
    missing = [str(path) for path in paths if not path.exists()]
    if missing:
        raise FileNotFoundError("Missing required input(s): " + ", ".join(missing))
