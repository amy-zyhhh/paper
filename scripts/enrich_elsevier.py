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


ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "papers.json"
FULL_TEXT_DIR = ROOT / "private" / "full_text"
ELSEVIER_ARTICLE_URL = "https://api.elsevier.com/content/article/doi/{doi}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Enrich papers.json with abstracts and content metadata from Elsevier."
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
        "--include-full-text",
        action="store_true",
        help="Store available full text returned by the API. Use only for private/local notes.",
    )
    parser.add_argument(
        "--save-full-text",
        action="store_true",
        help="Save available full text to private/full_text instead of embedding it in papers.json.",
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
    include_full_text: bool,
    include_raw: bool,
) -> dict[str, Any]:
    response = payload.get("full-text-retrieval-response", payload)
    coredata = response.get("coredata", {}) if isinstance(response, dict) else {}

    abstract = clean_text(
        coredata.get("dc:description")
        or find_first(response, {"dc:description", "description", "abstract", "ce:abstract"})
    )
    keywords = flatten_keywords(response)
    sections = extract_sections(response)
    original_text = clean_text(response.get("originalText", ""))

    content = {
        "source": "elsevier",
        "retrieved_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "abstract": abstract,
        "keywords": keywords,
        "sections": sections,
        "has_full_text": bool(original_text or sections),
        "available_text_chars": len(original_text),
    }
    if include_full_text and original_text:
        content["full_text"] = original_text
    if include_raw:
        content["raw"] = payload
    return content


def safe_filename(doi: str) -> str:
    filename = doi.lower()
    filename = re.sub(r"[^a-z0-9]+", "_", filename)
    return filename.strip("_") or "paper"


def save_full_text_file(doi: str, title: str, full_text: str) -> str:
    FULL_TEXT_DIR.mkdir(parents=True, exist_ok=True)
    path = FULL_TEXT_DIR / f"{safe_filename(doi)}.txt"
    content = "\n".join(
        [
            title,
            doi,
            "",
            full_text,
        ]
    )
    path.write_text(content, encoding="utf-8")
    return str(path.relative_to(ROOT))


def selected_papers(papers: list[dict[str, Any]], args: argparse.Namespace) -> list[dict[str, Any]]:
    if args.doi:
        wanted = {doi.lower() for doi in args.doi}
        return [paper for paper in papers if str(paper.get("doi", "")).lower() in wanted]
    return papers[args.offset : args.offset + args.limit]


def main() -> int:
    args = parse_args()
    if not args.api_key:
        print(
            "Missing Elsevier API key. Set $env:ELSEVIER_API_KEY or pass --api-key.",
            file=sys.stderr,
        )
        return 2

    papers = load_papers()
    targets = selected_papers(papers, args)
    if not targets:
        print("No papers selected.")
        return 0

    updated = 0
    for index, paper in enumerate(targets, start=1):
        doi = str(paper.get("doi", "")).strip()
        if not doi:
            continue

        print(f"[{index}/{len(targets)}] {doi}")
        try:
            payload = request_elsevier(doi, args.api_key, args.insttoken)
            content = extract_elsevier_content(
                payload,
                include_full_text=args.include_full_text,
                include_raw=args.include_raw,
            )
            if args.save_full_text:
                original_text = clean_text(
                    payload.get("full-text-retrieval-response", {}).get("originalText", "")
                )
                if original_text:
                    content["full_text_path"] = save_full_text_file(
                        doi,
                        str(paper.get("title", "")),
                        original_text,
                    )
        except urllib.error.HTTPError as error:
            paper.setdefault("content", {})["elsevier_error"] = {
                "status": error.code,
                "reason": error.reason,
                "retrieved_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
            }
            print(f"  Elsevier returned HTTP {error.code}: {error.reason}")
            continue
        except Exception as error:
            paper.setdefault("content", {})["elsevier_error"] = {
                "status": "error",
                "reason": str(error),
                "retrieved_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
            }
            print(f"  Request failed: {error}")
            continue

        paper.setdefault("content", {})["elsevier"] = content
        if content.get("abstract") and not paper.get("abstract"):
            paper["abstract"] = content["abstract"]
        if content.get("keywords"):
            paper["elsevier_keywords"] = content["keywords"]

        updated += 1
        print(
            "  ok:"
            f" abstract={'yes' if content.get('abstract') else 'no'},"
            f" keywords={len(content.get('keywords', []))},"
            f" sections={len(content.get('sections', []))},"
            f" full_text_chars={content.get('available_text_chars', 0)}"
        )
        time.sleep(0.25)

    if not args.dry_run:
        save_papers(papers)
        print(f"Updated {DATA_FILE}")
    else:
        print("Dry run only; papers.json was not changed.")

    print(f"Elsevier-enriched records: {updated}/{len(targets)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
