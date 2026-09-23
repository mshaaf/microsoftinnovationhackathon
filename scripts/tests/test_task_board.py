from scripts.task_board import parse_frontmatter


def test_parse_frontmatter_reads_task_fields_and_empty_dependencies():
    content = """---
id: P0-01
title: "Repo skeleton, Makefile, task board"
phase: 0
lane: shared
status: in_progress
owner: "luna-s1"
depends_on: []
---
Task body.
"""

    task = parse_frontmatter(content)

    assert task == {
        "id": "P0-01",
        "title": "Repo skeleton, Makefile, task board",
        "phase": 0,
        "lane": "shared",
        "status": "in_progress",
        "owner": "luna-s1",
        "depends_on": [],
    }
