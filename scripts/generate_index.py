#!/usr/bin/env python3
"""
generate_index.py
-----------------
Reads all notebooks in notebooks/ and regenerates docs/index.md
with an up-to-date table of contents.

Usage:
    python scripts/generate_index.py
"""

import json
import re
from pathlib import Path


def extract_metadata(nb_path: Path) -> dict:
    """Extract title, level, domain, and key concepts from a notebook's first cell."""
    with open(nb_path) as f:
        nb = json.load(f)

    metadata = {
        "title": nb_path.stem,
        "domain": "Classical Mechanics",
        "level": "Intermediate",
        "concepts": "",
    }

    for cell in nb["cells"]:
        if cell["cell_type"] == "markdown":
            src = "".join(cell["source"])
            # Extract H1 title
            m = re.search(r'^# (.+?)$', src, re.MULTILINE)
            if m:
                metadata["title"] = m.group(1).split(':')[0].strip()
            # Extract bold domain/level line
            m = re.search(r'\*\*MechanicsDSL Notebook \d+\*\* \| (.+?) \| (.+?)(?:\n|$)', src)
            if m:
                metadata["domain"] = m.group(1).strip()
                metadata["level"] = m.group(2).strip()
            break

    return metadata


def main():
    root = Path(__file__).parent.parent
    notebooks = sorted((root / "notebooks").glob("*.ipynb"))

    rows = []
    for nb in notebooks:
        num = nb.stem.split("_")[0]
        meta = extract_metadata(nb)
        rows.append(
            f"| {num} | [{meta['title']}](notebooks/{nb.name}) "
            f"| {meta['domain']} | {meta['level']} | |"
        )

    table = "\n".join([
        "| # | Notebook | Domain | Level | Key Concepts |",
        "|---|----------|--------|-------|--------------|",
    ] + rows)

    index_path = root / "docs" / "index.md"
    content = index_path.read_text()

    # Replace existing table
    new_content = re.sub(
        r'\| # \| Notebook.*?(?=\n##|\Z)',
        table + "\n\n",
        content,
        flags=re.DOTALL,
    )

    index_path.write_text(new_content)
    print(f"Updated {index_path} with {len(notebooks)} notebooks.")


if __name__ == "__main__":
    main()
