from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from env_loader import load_dotenv


ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "papers.json"
ANALYSES_FILE = ROOT / "data" / "analyses.json"
DEFAULT_OPENAI_BASE_URL = "https://llmapi.paratera.com/v1"
ANALYSIS_TYPE = "abstract_translation"

load_dotenv()


PROMPT_TEMPLATE = """你是一名力学方向的学术翻译助手。请只根据我提供的英文摘要，将其翻译成准确、自然、适合研究人员阅读的中文。

要求：
1. 只翻译摘要，不要扩展、总结、解释或添加原文没有的信息。
2. 保留必要英文术语，例如 phase-field, homogenization, finite deformation, crystal plasticity 等。
3. 数学符号、缩写、材料名、方法名和专有名词应尽量保持准确。
4. 输出必须是 JSON，不要添加 JSON 之外的解释文字。

请按照以下 JSON 结构输出：
{
  "abstract_translation": "中文摘要翻译"
}

论文标题：
{title}

DOI：
{doi}

英文摘要：
{abstract}
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Translate paper abstracts with an OpenAI-compatible API."
    )
    parser.add_argument("--limit", type=int, default=1, help="Maximum papers to translate.")
    parser.add_argument("--offset", type=int, default=0, help="Start at this paper index.")
    parser.add_argument("--doi", action="append", default=[], help="Translate this DOI only.")
    parser.add_argument(
        "--journal",
        default="",
        help="Only translate papers whose journal name matches this value.",
    )
    parser.add_argument(
        "--model",
        default=os.environ.get("OPENAI_MODEL", "DeepSeek-V3.2-Thinking"),
        help="OpenAI-compatible model name. Defaults to OPENAI_MODEL or DeepSeek-V3.2-Thinking.",
    )
    parser.add_argument(
        "--api-key",
        default=os.environ.get("OPENAI_API_KEY", ""),
        help="OpenAI API key. Defaults to OPENAI_API_KEY.",
    )
    parser.add_argument(
        "--base-url",
        default=os.environ.get("OPENAI_BASE_URL", DEFAULT_OPENAI_BASE_URL),
        help="OpenAI-compatible API base URL. Defaults to https://llmapi.paratera.com/v1.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Re-translate abstracts that already have a translation.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Build prompts without API calls.")
    return parser.parse_args()


def load_json_array(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)
    if not isinstance(data, list):
        raise SystemExit(f"{path} must contain a JSON array.")
    return data


def save_json(path: Path, data: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
        file.write("\n")


def abstract_text(paper: dict[str, Any]) -> str:
    elsevier_abstract = (
        paper.get("content", {})
        .get("elsevier", {})
        .get("abstract", "")
    )
    return str(paper.get("abstract") or elsevier_abstract or "").strip()


def journal_matches(paper: dict[str, Any], journal: str) -> bool:
    if not journal:
        return True
    names = [
        str(paper.get("journal", "")),
        str(paper.get("container_title", "")),
    ]
    return any(journal.lower() in name.lower() for name in names)


def has_translation(record: dict[str, Any] | None) -> bool:
    if not record:
        return False
    if record.get("analysis_type") != ANALYSIS_TYPE:
        return False
    return bool(str(record.get("abstract_translation", "")).strip())


def make_prompt(paper: dict[str, Any]) -> str:
    replacements = {
        "{title}": str(paper.get("title", "")),
        "{doi}": str(paper.get("doi", "")),
        "{abstract}": abstract_text(paper),
    }
    prompt = PROMPT_TEMPLATE
    for placeholder, value in replacements.items():
        prompt = prompt.replace(placeholder, value)
    return prompt


def request_openai(prompt: str, model: str, api_key: str, base_url: str) -> dict[str, Any]:
    chat_url = f"{base_url.rstrip('/')}/chat/completions"
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1,
        "response_format": {"type": "json_object"},
    }
    request = urllib.request.Request(
        chat_url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        body = json.loads(response.read().decode("utf-8"))

    text = (
        body.get("choices", [{}])[0]
        .get("message", {})
        .get("content", "")
    )
    if not text:
        raise ValueError("OpenAI response did not contain output text.")
    data = json.loads(text)
    if "abstract_translation" not in data and "translation" in data:
        data["abstract_translation"] = data["translation"]
    if not str(data.get("abstract_translation", "")).strip():
        raise ValueError("OpenAI response did not contain abstract_translation.")
    return data


def selected_papers(
    papers: list[dict[str, Any]],
    args: argparse.Namespace,
    by_doi: dict[str, dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, int]]:
    if args.doi:
        wanted = {doi.lower() for doi in args.doi}
        candidates = [paper for paper in papers if str(paper.get("doi", "")).lower() in wanted]
    else:
        candidates = papers[args.offset :]

    selected = []
    stats = {
        "candidates": 0,
        "skipped_missing_doi": 0,
        "skipped_missing_abstract": 0,
        "skipped_journal": 0,
        "skipped_translated": 0,
        "selected": 0,
    }
    for paper in candidates:
        stats["candidates"] += 1
        doi = str(paper.get("doi", "")).lower()
        if not doi:
            stats["skipped_missing_doi"] += 1
            continue
        if not journal_matches(paper, args.journal):
            stats["skipped_journal"] += 1
            continue
        if not abstract_text(paper):
            stats["skipped_missing_abstract"] += 1
            continue
        if has_translation(by_doi.get(doi)) and not args.overwrite:
            stats["skipped_translated"] += 1
            continue
        selected.append(paper)
        stats["selected"] += 1
        if not args.doi and len(selected) >= args.limit:
            break
    return selected, stats


def main() -> int:
    args = parse_args()
    if not args.api_key and not args.dry_run:
        print("Missing OpenAI API key. Set OPENAI_API_KEY or pass --api-key.", file=sys.stderr)
        return 2

    papers = load_json_array(DATA_FILE)
    analyses = load_json_array(ANALYSES_FILE)
    by_doi = {str(item.get("doi", "")).lower(): item for item in analyses if item.get("doi")}

    targets, stats = selected_papers(papers, args, by_doi)
    print(
        "[AI QUEUE]"
        f" candidates={stats['candidates']},"
        f" selected={stats['selected']},"
        f" skipped_translated={stats['skipped_translated']},"
        f" skipped_journal={stats['skipped_journal']},"
        f" skipped_missing_abstract={stats['skipped_missing_abstract']},"
        f" skipped_missing_doi={stats['skipped_missing_doi']}"
    )
    completed = 0
    if not targets:
        print("[SKIP] No papers selected for abstract translation. Existing translations were skipped.")

    for index, paper in enumerate(targets, start=1):
        doi = str(paper.get("doi", "")).lower()
        prompt = make_prompt(paper)
        print(f"[AI {index}/{len(targets)}] START {doi} ({len(prompt)} prompt chars)")
        if args.dry_run:
            print(prompt[:1200])
            print("...")
            continue

        try:
            result = request_openai(prompt, args.model, args.api_key, args.base_url)
        except urllib.error.HTTPError as error:
            detail = error.read().decode("utf-8", errors="replace")
            print(f"OpenAI HTTP {error.code}: {detail}", file=sys.stderr)
            return 1
        except Exception as error:
            print(f"OpenAI request failed: {error}", file=sys.stderr)
            return 1

        record = {
            "doi": doi,
            "title": paper.get("title", ""),
            "date": paper.get("date", ""),
            "model": args.model,
            "analysis_type": ANALYSIS_TYPE,
            "analyzed_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
            "abstract": abstract_text(paper),
            "abstract_translation": str(result["abstract_translation"]).strip(),
        }
        by_doi[doi] = record
        completed += 1
        print(f"[AI {index}/{len(targets)}] OK {doi}")
        save_json(ANALYSES_FILE, sorted(by_doi.values(), key=lambda item: item.get("date", ""), reverse=True))
        print(f"[WRITE] Saved progress: {len(by_doi)} translation records to {ANALYSES_FILE}")
        time.sleep(0.5)

    if args.dry_run:
        print("[DRY-RUN] No translations were written.")
    else:
        print(f"[WRITE] Final translation count: {len(by_doi)} records in {ANALYSES_FILE}")
    print(f"[AI SUMMARY] new={completed}, selected={len(targets)}, skipped_translated={stats['skipped_translated']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
