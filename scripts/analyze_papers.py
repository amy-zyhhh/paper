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


ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "papers.json"
ANALYSES_FILE = ROOT / "data" / "analyses.json"
DEFAULT_OPENAI_BASE_URL = "https://llmapi.paratera.com/v1"


ANALYSIS_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "paper_info": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "title": {"type": "string"},
                "doi": {"type": "string"},
                "date": {"type": "string"},
                "authors": {"type": "array", "items": {"type": "string"}},
                "author_affiliations": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "author": {"type": "string"},
                            "affiliations": {
                                "type": "array",
                                "items": {"type": "string"},
                            },
                        },
                        "required": ["author", "affiliations"],
                    },
                },
            },
            "required": ["title", "doi", "date", "authors", "author_affiliations"],
        },
        "analysis": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "what_was_done": {"type": "string"},
                "why_it_was_done": {"type": "string"},
                "how_it_was_done": {"type": "string"},
                "how_well_it_worked": {"type": "string"},
                "main_conclusions": {"type": "array", "items": {"type": "string"}},
                "highlights_and_innovations": {"type": "array", "items": {"type": "string"}},
                "limitations": {"type": "array", "items": {"type": "string"}},
                "future_directions": {"type": "array", "items": {"type": "string"}},
                "cautions": {"type": "array", "items": {"type": "string"}},
                "keywords": {"type": "array", "items": {"type": "string"}},
                "suitable_for": {"type": "array", "items": {"type": "string"}},
                "reading_priority": {"type": "string", "enum": ["high", "medium", "low"]},
                "priority_reason": {"type": "string"},
            },
            "required": [
                "what_was_done",
                "why_it_was_done",
                "how_it_was_done",
                "how_well_it_worked",
                "main_conclusions",
                "highlights_and_innovations",
                "limitations",
                "future_directions",
                "cautions",
                "keywords",
                "suitable_for",
                "reading_priority",
                "priority_reason",
            ],
        },
    },
    "required": ["paper_info", "analysis"],
}


PROMPT_TEMPLATE = """你是一名力学方向的研究助理，擅长阅读专业论文。请基于我提供的论文全文或可用文本，生成一份中文文献分析笔记。

要求：
1. 只根据提供的文本回答，不要编造文本中没有的信息。
2. 如果某一项信息在文本中不充分，请明确写“原文信息不足”。
3. 区分作者明确陈述的内容和你基于文本做出的合理推断。
4. 回答要面向研究人员，准确、简洁、有技术含量。
5. 不要大段翻译原文，不要摘录长段原文。
6. 保留必要的英文术语，例如 phase-field, homogenization, finite deformation, crystal plasticity 等。
7. 输出必须是 JSON，不要添加 JSON 之外的解释文字。
8. 如果作者单位信息缺失，请在 author_affiliations 中写“原文信息不足”。

请按照以下 JSON 结构输出：

{
  "paper_info": {
    "title": "论文标题",
    "doi": "DOI",
    "date": "发表日期或在线发表日期",
    "authors": [
      "作者 1",
      "作者 2"
    ],
    "author_affiliations": [
      {
        "author": "作者名",
        "affiliations": [
          "单位 1",
          "单位 2"
        ]
      }
    ]
  },
  "analysis": {
    "what_was_done": "文章做了什么工作？概括研究对象、核心问题和主要任务。",
    "why_it_was_done": "为什么要做这个工作？说明研究背景、已有方法的不足、科学或工程动机。",
    "how_it_was_done": "怎么做的？总结理论模型、实验方法、数值方法、数据来源、验证方式等。",
    "how_well_it_worked": "做得怎么样？总结主要性能、验证结果、对比结果、适用范围。如果原文没有充分评价，请说明。",
    "main_conclusions": [
      "主要结论 1",
      "主要结论 2",
      "主要结论 3"
    ],
    "highlights_and_innovations": [
      "亮点或创新点 1",
      "亮点或创新点 2",
      "亮点或创新点 3"
    ],
    "limitations": [
      "局限性 1",
      "局限性 2"
    ],
    "future_directions": [
      "可能的发展方向 1",
      "可能的发展方向 2"
    ],
    "cautions": [
      "阅读或使用该工作的注意事项 1",
      "注意事项 2"
    ],
    "keywords": [
      "关键词 1",
      "关键词 2",
      "关键词 3"
    ],
    "suitable_for": [
      "适合关注该方向的读者或研究问题"
    ],
    "reading_priority": "high / medium / low",
    "priority_reason": "为什么给出这个阅读优先级。"
  }
}

论文信息如下：

标题：
{title}

DOI：
{doi}

日期：
{date}

作者：
{authors}

作者单位：
{author_affiliations}

摘要：
{abstract}

全文或正文片段：
{full_text}
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analyze locally saved JMPS full text with the OpenAI API."
    )
    parser.add_argument("--limit", type=int, default=1, help="Maximum papers to analyze.")
    parser.add_argument("--offset", type=int, default=0, help="Start at this paper index.")
    parser.add_argument("--doi", action="append", default=[], help="Analyze this DOI only.")
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
        "--max-chars",
        type=int,
        default=60000,
        help="Maximum full-text characters sent per paper.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Re-analyze papers that already have an analysis.",
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


def author_affiliations(paper: dict[str, Any]) -> list[dict[str, Any]]:
    details = paper.get("author_details", [])
    if not details:
        return [
            {"author": author, "affiliations": ["原文信息不足"]}
            for author in paper.get("authors", [])
        ]
    output = []
    for detail in details:
        affiliations = detail.get("affiliations") or ["原文信息不足"]
        output.append({"author": detail.get("name", ""), "affiliations": affiliations})
    return output


def local_full_text_path(paper: dict[str, Any]) -> Path | None:
    path = (
        paper.get("content", {})
        .get("elsevier", {})
        .get("full_text_path", "")
    )
    if not path:
        return None
    return ROOT / path


def paper_text(paper: dict[str, Any], max_chars: int) -> str:
    path = local_full_text_path(paper)
    if path and path.exists():
        return path.read_text(encoding="utf-8", errors="replace")[:max_chars]
    content = paper.get("content", {}).get("elsevier", {})
    full_text = content.get("full_text", "")
    if full_text:
        return full_text[:max_chars]
    return (paper.get("abstract") or content.get("abstract") or "")[:max_chars]


def make_prompt(paper: dict[str, Any], max_chars: int) -> str:
    replacements = {
        "{title}": paper.get("title", ""),
        "{doi}": paper.get("doi", ""),
        "{date}": paper.get("date", ""),
        "{authors}": ", ".join(paper.get("authors", [])),
        "{author_affiliations}": json.dumps(
            author_affiliations(paper),
            ensure_ascii=False,
            indent=2,
        ),
        "{abstract}": paper.get("abstract", ""),
        "{full_text}": paper_text(paper, max_chars),
    }
    prompt = PROMPT_TEMPLATE
    for placeholder, value in replacements.items():
        prompt = prompt.replace(placeholder, value)
    return prompt


def request_openai(prompt: str, model: str, api_key: str, base_url: str) -> dict[str, Any]:
    chat_url = f"{base_url.rstrip('/')}/chat/completions"
    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": prompt,
            }
        ],
        "temperature": 0.2,
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
    return json.loads(text)


def selected_papers(papers: list[dict[str, Any]], args: argparse.Namespace) -> list[dict[str, Any]]:
    if args.doi:
        wanted = {doi.lower() for doi in args.doi}
        return [paper for paper in papers if str(paper.get("doi", "")).lower() in wanted]
    return papers[args.offset : args.offset + args.limit]


def main() -> int:
    args = parse_args()
    if not args.api_key and not args.dry_run:
        print("Missing OpenAI API key. Set OPENAI_API_KEY or pass --api-key.", file=sys.stderr)
        return 2

    papers = load_json_array(DATA_FILE)
    analyses = load_json_array(ANALYSES_FILE)
    by_doi = {str(item.get("doi", "")).lower(): item for item in analyses}

    targets = selected_papers(papers, args)
    completed = 0
    for index, paper in enumerate(targets, start=1):
        doi = str(paper.get("doi", "")).lower()
        if not doi:
            continue
        if doi in by_doi and not args.overwrite:
            print(f"[{index}/{len(targets)}] {doi} already analyzed; skipping.")
            continue

        prompt = make_prompt(paper, args.max_chars)
        print(f"[{index}/{len(targets)}] analyzing {doi} ({len(prompt)} prompt chars)")
        if args.dry_run:
            print(prompt[:1200])
            print("...")
            continue

        try:
            analysis = request_openai(prompt, args.model, args.api_key, args.base_url)
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
            "analyzed_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
            "analysis": analysis,
        }
        by_doi[doi] = record
        completed += 1
        time.sleep(0.5)

    if not args.dry_run:
        save_json(ANALYSES_FILE, sorted(by_doi.values(), key=lambda item: item.get("date", ""), reverse=True))
        print(f"Saved {len(by_doi)} analyses to {ANALYSES_FILE}")
    print(f"New analyses: {completed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
