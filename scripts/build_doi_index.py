from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PAPERS_FILE = ROOT / "data" / "papers.json"
INDEX_FILE = ROOT / "data" / "doi_index.json"


def load_papers() -> list[dict[str, Any]]:
    if not PAPERS_FILE.exists():
        return []
    with PAPERS_FILE.open("r", encoding="utf-8") as file:
        data = json.load(file)
    if not isinstance(data, list):
        raise SystemExit(f"{PAPERS_FILE} must contain a JSON array.")
    return data


def journal_name(paper: dict[str, Any]) -> str:
    return str(paper.get("journal") or paper.get("container_title") or "").strip()


def build_index(papers: list[dict[str, Any]]) -> dict[str, Any]:
    items: dict[str, dict[str, str]] = {}
    for paper in papers:
        doi = str(paper.get("doi", "")).strip().lower()
        if not doi:
            continue
        items[doi] = {
            "doi": doi,
            "date": str(paper.get("date", "") or ""),
            "journal": journal_name(paper),
            "issn": ", ".join(str(value) for value in paper.get("issn", []) if value)
            if isinstance(paper.get("issn"), list)
            else str(paper.get("issn", "") or ""),
            "title": str(paper.get("title", "") or ""),
        }
    return {
        "updated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "count": len(items),
        "items": dict(sorted(items.items())),
    }


def main() -> int:
    papers = load_papers()
    index = build_index(papers)
    INDEX_FILE.parent.mkdir(parents=True, exist_ok=True)
    with INDEX_FILE.open("w", encoding="utf-8") as file:
        json.dump(index, file, ensure_ascii=False, indent=2)
        file.write("\n")
    print(f"[DOI INDEX] Wrote {index['count']} DOI records to {INDEX_FILE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
