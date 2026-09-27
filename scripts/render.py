"""Placeholder rendering shared by spawn.py and upstream.py.

Placeholders look like {{NAME}}. Rendering a template with a value map
replaces every known placeholder; an unknown one left in the output is an
error, because a `{{TITLE}}` that reaches a generated repo is a bug nobody
would notice until a customer reads it. The exception is the double-brace
syntax that legitimately survives, listed in KEEP: Astro/JSX expressions
never use it, but the launch checklist mentions `{{...}}` placeholders in
legal pages as text.
"""

from __future__ import annotations

import re
from pathlib import Path

PLACEHOLDER = re.compile(r"\{\{([A-Z0-9_]+)\}\}")
KEEP = {"..."}  # `{{...}}` in prose that talks about placeholders


def render(text: str, values: dict[str, str], where: str = "") -> str:
    def sub(match: re.Match[str]) -> str:
        key = match.group(1)
        if key not in values:
            raise SystemExit(f"unknown placeholder {{{{{key}}}}} in {where}")
        return values[key]

    return PLACEHOLDER.sub(sub, text)


def leftovers(text: str) -> list[str]:
    return sorted({m.group(1) for m in PLACEHOLDER.finditer(text)} - KEEP)


def is_text(path: Path) -> bool:
    try:
        path.read_bytes().decode("utf-8")
        return True
    except UnicodeDecodeError:
        return False


def reverse(text: str, values: dict[str, str]) -> str:
    """Put placeholders back: the longest values first, so `acme-ops` is
    caught before `acme`. Only values long enough to be unambiguous."""
    pairs = sorted(((v, k) for k, v in values.items() if len(v) >= 4), key=lambda p: -len(p[0]))
    for value, key in pairs:
        text = text.replace(value, "{{" + key + "}}")
    return text
