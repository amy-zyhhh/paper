from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from env_loader import load_dotenv


ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "papers.json"
ELSEVIER_ARTICLE_URL = "https://api.elsevier.com/content/article/doi/{doi}"

load_dotenv()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Enrich papers.json with abstracts from Elsevier."
    )
    parser.add_argument("--limit", type=int, default=5, help="Maximum papers to request.")
    parser.add_argument(
        "--offset",
        type=int,
        default=0,
        help="Start at this index in data/papers.json.",
    )
    parser.add_argument(
        "--doi",
        action="append",
        default=[],
        help="Only enrich this DOI. Can be used multiple times.",
    )
    parser.add_argument(
        "--journal",
        default="",
        help="Only enrich papers whose journal name matches this value.",
    )
    parser.add_argument(
        "--api-key",
        default=os.environ.get("ELSEVIER_API_KEY", ""),
        help="Elsevier API key. Defaults to ELSEVIER_API_KEY environment variable.",
    )
    parser.add_argument(
        "--insttoken",
        default=os.environ.get("ELSEVIER_INSTTOKEN", ""),
        help="Optional Elsevier institution token.",
    )
    parser.add_argument(
        "--include-raw",
        action="store_true",
        help="Store the raw Elsevier JSON response under content.elsevier.raw.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Request data and print a summary without writing papers.json.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Re-fetch papers that already have Elsevier enrichment data.",
    )
    parser.add_argument(
        "--retry-errors",
        action="store_true",
        help="Retry papers that previously returned an Elsevier error.",
    )
    return parser.parse_args()


def clean_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        value = " ".join(clean_text(item) for item in value)
    elif isinstance(value, dict):
        for key in ["$", "_", "text", "para", "ce:para", "simple-para"]:
            if key in value:
                return clean_text(value[key])
        value = " ".join(clean_text(item) for item in value.values())
    text = html.unescape(str(value))
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def load_papers() -> list[dict[str, Any]]:
    with DATA_FILE.open("r", encoding="utf-8") as file:
        data = json.load(file)
    if not isinstance(data, list):
        raise SystemExit(f"{DATA_FILE} must contain a JSON array.")
    return data


def save_papers(papers: list[dict[str, Any]]) -> None:
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(papers, file, ensure_ascii=False, indent=2)
        file.write("\n")


def request_elsevier(doi: str, api_key: str, insttoken: str = "") -> dict[str, Any]:
    encoded_doi = urllib.parse.quote(doi, safe="")
    url = ELSEVIER_ARTICLE_URL.format(doi=encoded_doi)
    url = f"{url}?httpAccept=application/json"
    headers = {
        "Accept": "application/json",
        "X-ELS-APIKey": api_key,
        "User-Agent": "jmps-literature-tracker/0.1",
    }
    if insttoken:
        headers["X-ELS-Insttoken"] = insttoken

    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=45) as response:
        return json.loads(response.read().decode("utf-8"))


def find_first(node: Any, keys: set[str]) -> Any:
    if isinstance(node, dict):
        for key, value in node.items():
            if key in keys and value not in (None, "", [], {}):
                return value
        for value in node.values():
            found = find_first(value, keys)
            if found not in (None, "", [], {}):
                return found
    elif isinstance(node, list):
        for item in node:
            found = find_first(item, keys)
            if found not in (None, "", [], {}):
                return found
    return None


def find_all(node: Any, keys: set[str]) -> list[Any]:
    values = []
    if isinstance(node, dict):
        for key, value in node.items():
            if key in keys and value not in (None, "", [], {}):
                values.append(value)
            values.extend(find_all(value, keys))
    elif isinstance(node, list):
        for item in node:
            values.extend(find_all(item, keys))
    return values


def flatten_keywords(value: Any) -> list[str]:
    keywords = []
    for raw in find_all(value, {"author-keyword", "keyword", "idxterm"}):
        if isinstance(raw, list):
            candidates = raw
        else:
            candidates = [raw]
        for candidate in candidates:
            text = clean_text(candidate)
            if text and len(text) <= 120:
                keywords.append(text)
    return sorted(set(keywords), key=str.lower)


def extract_sections(payload: dict[str, Any], max_chars: int = 12000) -> list[dict[str, str]]:
    sections = []
    raw_sections = find_all(payload, {"section", "ce:section"})
    for section in raw_sections:
        if not isinstance(section, dict):
            continue
        title = clean_text(
            section.get("section-title")
            or section.get("ce:section-title")
            or section.get("title")
        )
        text = clean_text(section)
        if title and text:
            sections.append({"title": title, "text": text[:max_chars]})
    return sections[:20]


def extract_elsevier_content(
    payload: dict[str, Any],
    include_raw: bool,
) -> dict[str, Any]:
    response = payload.get("full-text-retrieval-response", payload)
    coredata = response.get("coredata", {}) if isinstance(response, dict) else {}

    abstract = clean_text(
        coredata.get("dc:description")
        or find_first(response, {"dc:description", "description", "abstract", "ce:abstract"})
    )
    content = {
        "source": "elsevier",
        "retrieved_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "abstract": abstract,
    }
    keywords = flatten_keywords(response)
    if keywords:
        content["keywords"] = keywords
    if include_raw:
        content["raw"] = payload
    return content


def journal_matches(paper: dict[str, Any], journal: str) -> bool:
    if not journal:
        return True
    names = [
        str(paper.get("journal", "")),
        str(paper.get("container_title", "")),
    ]
    return any(journal.lower() in name.lower() for name in names)


def has_elsevier_result(paper: dict[str, Any], retry_errors: bool) -> bool:
    content = paper.get("content", {})
    if content.get("elsevier"):
        return True
    if content.get("elsevier_error") and not retry_errors:
        return True
    return False


def selected_papers(
    papers: list[dict[str, Any]],
    args: argparse.Namespace,
) -> tuple[list[dict[str, Any]], dict[str, int]]:
    if args.doi:
        wanted = {doi.lower() for doi in args.doi}
        candidates = [paper for paper in papers if str(paper.get("doi", "")).lower() in wanted]
    else:
        candidates = papers[args.offset :]

    selected = []
    stats = {
        "candidates": 0,
        "skipped_journal": 0,
        "skipped_existing": 0,
        "selected": 0,
    }
    for paper in candidates:
        stats["candidates"] += 1
        if not journal_matches(paper, args.journal):
            stats["skipped_journal"] += 1
            continue
        if not args.overwrite and has_elsevier_result(paper, args.retry_errors):
            stats["skipped_existing"] += 1
            continue
        selected.append(paper)
        stats["selected"] += 1
        if not args.doi and len(selected) >= args.limit:
            break
    return selected, stats


def main() -> int:
    args = parse_args()
    if not args.api_key:
        print(
            "Missing Elsevier API key. Set $env:ELSEVIER_API_KEY or pass --api-key.",
            file=sys.stderr,
        )
        return 2

    papers = load_papers()
    targets, stats = selected_papers(papers, args)
    print(
        "[ELSEVIER QUEUE]"
        f" candidates={stats['candidates']},"
        f" selected={stats['selected']},"
        f" skipped_existing={stats['skipped_existing']},"
        f" skipped_journal={stats['skipped_journal']}"
    )
    if not targets:
        print("[SKIP] No papers selected for Elsevier. Existing enrichment/error records were skipped.")
        return 0

    updated = 0
    for index, paper in enumerate(targets, start=1):
        doi = str(paper.get("doi", "")).strip()
        if not doi:
            continue

        print(f"[ELSEVIER {index}/{len(targets)}] START {doi}")
        try:
            payload = request_elsevier(doi, args.api_key, args.insttoken)
            content = extract_elsevier_content(
                payload,
                include_raw=args.include_raw,
            )
        except urllib.error.HTTPError as error:
            paper.setdefault("content", {})["elsevier_error"] = {
                "status": error.code,
                "reason": error.reason,
                "retrieved_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
            }
            print(f"[ELSEVIER {index}/{len(targets)}] ERROR HTTP {error.code}: {error.reason}")
            if not args.dry_run:
                save_papers(papers)
                print(f"[WRITE] Saved progress after Elsevier error to {DATA_FILE}")
            continue
        except Exception as error:
            paper.setdefault("content", {})["elsevier_error"] = {
                "status": "error",
                "reason": str(error),
                "retrieved_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
            }
            print(f"[ELSEVIER {index}/{len(targets)}] ERROR request failed: {error}")
            if not args.dry_run:
                save_papers(papers)
                print(f"[WRITE] Saved progress after Elsevier error to {DATA_FILE}")
            continue

        paper.setdefault("content", {})["elsevier"] = content
        if content.get("abstract") and not paper.get("abstract"):
            paper["abstract"] = content["abstract"]
        if content.get("keywords"):
            paper["elsevier_keywords"] = content["keywords"]

        updated += 1
        print(
            f"[ELSEVIER {index}/{len(targets)}] OK"
            f" abstract={'yes' if content.get('abstract') else 'no'},"
            f" keywords={len(content.get('keywords', []))}"
        )
        if not args.dry_run:
            save_papers(papers)
            print(f"[WRITE] Saved progress: Elsevier data for {doi} to {DATA_FILE}")
        time.sleep(0.25)

    if args.dry_run:
        print("[DRY-RUN] papers.json was not changed.")
    else:
        print(f"[WRITE] Final paper count: {len(papers)} records in {DATA_FILE}")

    print(f"[ELSEVIER SUMMARY] enriched={updated}, selected={len(targets)}, skipped_existing={stats['skipped_existing']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
