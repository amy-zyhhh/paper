from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from datetime import date, timedelta, timezone, datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "papers.json"

JOURNAL_NAME = "Journal of the Mechanics and Physics of Solids"
JMPS_ISSN = "0022-5096"
CROSSREF_WORKS_URL = f"https://api.crossref.org/journals/{JMPS_ISSN}/works"

TOPIC_KEYWORDS = {
    "fracture": ["fracture", "crack", "damage", "phase-field", "phase field"],
    "plasticity": ["plasticity", "plastic", "yield", "hardening", "crystal plasticity"],
    "dislocations": ["dislocation", "dislocations", "geometrically necessary"],
    "metamaterials": ["metamaterial", "metamaterials", "architected", "lattice"],
    "homogenization": ["homogenization", "homogenisation", "effective response"],
    "computational mechanics": ["finite element", "simulation", "numerical", "computational"],
    "soft matter": ["soft solid", "soft solids", "gel", "elastomer", "hydrogel"],
    "mechanics": ["mechanics", "elasticity", "deformation", "stress", "strain"],
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch recent JMPS papers from Crossref and update data/papers.json."
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=25,
        help="Maximum number of records to request from Crossref.",
    )
    parser.add_argument(
        "--days",
        type=int,
        default=365,
        help="Only fetch papers published in the last N days. Ignored if --from-date is set.",
    )
    parser.add_argument(
        "--from-date",
        default="",
        help="Fetch papers published on or after this date, in YYYY-MM-DD format.",
    )
    parser.add_argument(
        "--until-date",
        default="",
        help="Fetch papers published on or before this date, in YYYY-MM-DD format.",
    )
    parser.add_argument(
        "--mailto",
        default=os.environ.get("CROSSREF_MAILTO", ""),
        help="Email address sent to Crossref for polite API usage.",
    )
    parser.add_argument(
        "--replace-test-data",
        action="store_true",
        help="Remove records whose source is test-data before merging real records.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Fetch and summarize results without writing data/papers.json.",
    )
    return parser.parse_args()


def validate_date(value: str, option_name: str) -> str:
    if not value:
        return ""
    try:
        return date.fromisoformat(value).isoformat()
    except ValueError:
        raise SystemExit(f"{option_name} must use YYYY-MM-DD format, got: {value}")


def request_json(url: str) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "jmps-literature-tracker/0.1 (mailto:unknown@example.com)",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def clean_text(value: Any) -> str:
    if isinstance(value, list):
        value = " ".join(str(item) for item in value if item)
    if not value:
        return ""
    text = html.unescape(str(value))
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def first_date(parts: dict[str, Any]) -> str:
    date_parts = parts.get("date-parts", [])
    if not date_parts or not date_parts[0]:
        return ""

    values = list(date_parts[0])
    if len(values) == 1:
        values.extend([1, 1])
    elif len(values) == 2:
        values.append(1)

    try:
        return date(values[0], values[1], values[2]).isoformat()
    except (TypeError, ValueError):
        return ""


def paper_date(item: dict[str, Any]) -> str:
    for key in ["published-online", "published-print", "published", "created"]:
        value = item.get(key)
        if isinstance(value, dict):
            parsed = first_date(value)
            if parsed:
                return parsed
    return ""


def authors(item: dict[str, Any]) -> list[str]:
    names = []
    for author in item.get("author", []):
        given = clean_text(author.get("given", ""))
        family = clean_text(author.get("family", ""))
        name = " ".join(part for part in [given, family] if part)
        if name:
            names.append(name)
    return names


def classify_topics(title: str, abstract: str) -> tuple[list[str], list[str]]:
    text = f"{title} {abstract}".lower()
    topics = []
    matched_keywords = []

    for topic, keywords in TOPIC_KEYWORDS.items():
        hits = [keyword for keyword in keywords if keyword in text]
        if hits:
            topics.append(topic)
            matched_keywords.extend(hits)

    if not topics:
        topics = ["mechanics"]

    return sorted(set(topics)), sorted(set(matched_keywords))


def normalize_item(item: dict[str, Any]) -> dict[str, Any] | None:
    title = clean_text(item.get("title", []))
    doi = clean_text(item.get("DOI", "")).lower()
    if not title or not doi:
        return None

    abstract = clean_text(item.get("abstract", ""))
    topics, matched_keywords = classify_topics(title, abstract)
    issued_date = paper_date(item)
    url = clean_text(item.get("URL", "")) or f"https://doi.org/{doi}"

    return {
        "title": title,
        "authors": authors(item),
        "doi": doi,
        "date": issued_date,
        "journal": JOURNAL_NAME,
        "volume": clean_text(item.get("volume", "")),
        "issue": clean_text(item.get("issue", "")),
        "article_number": clean_text(item.get("article-number", "")),
        "page": clean_text(item.get("page", "")),
        "url": url,
        "abstract": abstract,
        "keywords": matched_keywords,
        "topics": topics,
        "source": "crossref",
        "added_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    }


def build_crossref_url(
    limit: int,
    days: int,
    mailto: str,
    from_date: str = "",
    until_date: str = "",
) -> str:
    from_date = validate_date(from_date, "--from-date")
    until_date = validate_date(until_date, "--until-date")

    if not from_date:
        from_date = (date.today() - timedelta(days=days)).isoformat()

    filters = [f"from-pub-date:{from_date}", "type:journal-article"]
    if until_date:
        filters.append(f"until-pub-date:{until_date}")

    params = {
        "filter": ",".join(filters),
        "sort": "published",
        "order": "desc",
        "rows": str(limit),
        "select": ",".join(
            [
                "DOI",
                "URL",
                "title",
                "author",
                "abstract",
                "published",
                "published-online",
                "published-print",
                "created",
                "volume",
                "issue",
                "page",
                "article-number",
            ]
        ),
    }
    if mailto:
        params["mailto"] = mailto
    return f"{CROSSREF_WORKS_URL}?{urllib.parse.urlencode(params)}"


def load_existing() -> list[dict[str, Any]]:
    if not DATA_FILE.exists():
        return []
    with DATA_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def merge_papers(
    existing: list[dict[str, Any]],
    fetched: list[dict[str, Any]],
    replace_test_data: bool,
) -> tuple[list[dict[str, Any]], int]:
    if replace_test_data:
        existing = [paper for paper in existing if paper.get("source") != "test-data"]

    by_doi = {
        clean_text(paper.get("doi", "")).lower(): paper
        for paper in existing
        if clean_text(paper.get("doi", ""))
    }
    added = 0

    for paper in fetched:
        doi = paper["doi"]
        if doi in by_doi:
            current = by_doi[doi]
            current.update({key: value for key, value in paper.items() if value})
        else:
            by_doi[doi] = paper
            added += 1

    merged = sorted(by_doi.values(), key=lambda paper: paper.get("date", ""), reverse=True)
    return merged, added


def save_papers(papers: list[dict[str, Any]]) -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(papers, file, ensure_ascii=False, indent=2)
        file.write("\n")


def main() -> int:
    args = parse_args()
    url = build_crossref_url(
        args.limit,
        args.days,
        args.mailto,
        args.from_date,
        args.until_date,
    )

    try:
        payload = request_json(url)
    except Exception as error:
        print(f"Failed to fetch Crossref data: {error}", file=sys.stderr)
        return 1

    items = payload.get("message", {}).get("items", [])
    fetched = [paper for item in items if (paper := normalize_item(item))]
    existing = load_existing()
    merged, added = merge_papers(existing, fetched, args.replace_test_data)

    print(f"Fetched {len(fetched)} JMPS records from Crossref.")
    print(f"Added {added} new records; total records would be {len(merged)}.")

    if fetched:
        print("Newest fetched paper:")
        print(f"  {fetched[0]['date']} - {fetched[0]['title']}")

    if not args.dry_run:
        save_papers(merged)
        print(f"Updated {DATA_FILE}")

    time.sleep(1)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
