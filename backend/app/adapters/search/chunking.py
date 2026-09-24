"""Turns fixtures/kb/*.md into citable chunks. Shared by mock search and `make index`."""

import re
from pathlib import Path

import yaml

KB_DIR = Path(__file__).resolve().parents[4] / "fixtures" / "kb"
MAX_CHARS = 1200
FRONT_MATTER_KEYS = ("url", "title", "agency", "lang", "topic", "fetched_at")


def _split_long(text: str) -> list[str]:
    parts, current = [], ""
    for paragraph in text.split("\n\n"):
        while (
            len(paragraph) > MAX_CHARS
        ):  # ponytail: hard cut only for one giant paragraph
            cut = paragraph.rfind(" ", 0, MAX_CHARS) or MAX_CHARS
            parts.append(paragraph[:cut].strip())
            paragraph = paragraph[cut:].strip()
        if current and len(current) + len(paragraph) + 2 > MAX_CHARS:
            parts.append(current)
            current = paragraph
        else:
            current = f"{current}\n\n{paragraph}" if current else paragraph
    return [p for p in [*parts, current] if p]


def chunk_markdown(text: str, source: str = "kb") -> list[dict]:
    match = re.match(r"---\n(.*?)\n---\n(.*)", text, re.DOTALL)
    if not match:
        raise ValueError(f"{source}: missing front matter")
    meta = yaml.safe_load(match.group(1))
    missing = [k for k in FRONT_MATTER_KEYS if not meta.get(k)]
    if missing:
        raise ValueError(f"{source}: front matter missing {missing}")
    meta = {k: str(meta[k]) for k in FRONT_MATTER_KEYS}
    chunks = []
    for section in re.split(r"(?m)^(?=## )", match.group(2)):
        if not section.strip():
            continue
        for part in _split_long(section.strip()):
            chunks.append({**meta, "id": f"{source}-{len(chunks)}", "content": part})
    return chunks


def load_kb(kb_dir: Path = KB_DIR) -> list[dict]:
    chunks = []
    for path in sorted(kb_dir.glob("*.md")):
        if path.name.lower() == "readme.md":
            continue
        chunks += chunk_markdown(
            path.read_text(encoding="utf-8"), path.stem.replace(".", "-")
        )
    return chunks
