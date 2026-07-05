from __future__ import annotations

import json
import re
import shutil
from collections import defaultdict
from datetime import date
from html import escape
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "papers.json"
ANALYSES_FILE = ROOT / "data" / "analyses.json"
DOCS_DIR = ROOT / "docs"
PAPERS_DIR = DOCS_DIR / "papers"
TOPICS_DIR = DOCS_DIR / "topics"
ASSETS_DIR = DOCS_DIR / "assets"

ZH_LATEST = "\u6700\u65b0\u6587\u732e"
ZH_INDEX = "\u6587\u732e\u7d22\u5f15"
ZH_TOPICS = "\u4e3b\u9898\u5206\u7c7b"
ZH_SEARCH = "\u641c\u7d22"
ZH_AUTHOR = "\u4f5c\u8005"
ZH_DATE = "\u65e5\u671f"
ZH_JOURNAL = "\u671f\u520a"
ZH_KEYWORDS = "\u5173\u952e\u8bcd"
ZH_TOPIC = "\u4e3b\u9898"
ZH_ABSTRACT = "\u6458\u8981"
ZH_AI = "AI \u5206\u6790"
ZH_BACK_INDEX = "\u8fd4\u56de\u6587\u732e\u7d22\u5f15"
ZH_PUBLISHER = "\u51fa\u7248\u793e\u9875\u9762"
ZH_NO_INFO = "\u539f\u6587\u4fe1\u606f\u4e0d\u8db3"
ZH_NO_ABSTRACT = "\u6682\u65e0\u6458\u8981\u6216 AI \u5206\u6790\u3002"


def load_papers() -> list[dict[str, Any]]:
    with DATA_FILE.open("r", encoding="utf-8") as file:
        papers = json.load(file)
    return sorted(papers, key=lambda paper: paper.get("date", ""), reverse=True)


def load_analyses() -> dict[str, dict[str, Any]]:
    if not ANALYSES_FILE.exists():
        return {}
    with ANALYSES_FILE.open("r", encoding="utf-8") as file:
        analyses = json.load(file)
    return {
        analysis.get("doi", "").lower(): analysis
        for analysis in analyses
        if analysis.get("doi")
    }


def slugify(value: str) -> str:
    slug = value.lower().strip()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    return slug.strip("-") or "item"


def journal_name(paper: dict[str, Any]) -> str:
    return str(paper.get("journal") or paper.get("container_title") or "Unknown Journal")


def journal_slug(paper: dict[str, Any]) -> str:
    return slugify(journal_name(paper))


def paper_slug(paper: dict[str, Any]) -> str:
    doi = str(paper.get("doi", ""))
    if doi:
        return slugify(doi)
    return slugify(str(paper.get("title", "paper")))


def paper_month(paper: dict[str, Any]) -> str:
    date_text = str(paper.get("date", ""))
    if len(date_text) >= 7:
        return date_text[:7]
    return "unknown"


def paper_detail_path(paper: dict[str, Any]) -> Path:
    return PAPERS_DIR / journal_slug(paper) / paper_month(paper) / f"{paper_slug(paper)}.md"


def paper_detail_url(paper: dict[str, Any]) -> str:
    return f"/papers/{journal_slug(paper)}/{paper_month(paper)}/{paper_slug(paper)}.html"


def front_matter(title: str, layout: str = "default") -> str:
    return f"---\nlayout: {layout}\ntitle: {json.dumps(title, ensure_ascii=False)}\n---\n\n"


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def clean_generated_pages() -> None:
    PAPERS_DIR.mkdir(parents=True, exist_ok=True)
    TOPICS_DIR.mkdir(parents=True, exist_ok=True)
    for path in PAPERS_DIR.glob("*.md"):
        path.unlink()
    for path in PAPERS_DIR.iterdir():
        if path.is_dir():
            shutil.rmtree(path)
    for path in TOPICS_DIR.glob("*.md"):
        path.unlink()


def text_from_analysis(record: dict[str, Any] | None, key: str) -> str:
    if not record:
        return ""
    return str(record.get("analysis", {}).get("analysis", {}).get(key, "") or "")


def list_from_analysis(record: dict[str, Any] | None, key: str) -> list[str]:
    if not record:
        return []
    values = record.get("analysis", {}).get("analysis", {}).get(key, [])
    if isinstance(values, list):
        return [str(value) for value in values if value]
    if values:
        return [str(values)]
    return []


def abstract_text(paper: dict[str, Any]) -> str:
    elsevier_abstract = (
        paper.get("content", {})
        .get("elsevier", {})
        .get("abstract", "")
    )
    return str(paper.get("abstract") or elsevier_abstract or "")


def short_description(paper: dict[str, Any], analysis: dict[str, Any] | None) -> str:
    what = text_from_analysis(analysis, "what_was_done")
    if what:
        return what
    abstract = abstract_text(paper)
    if abstract:
        return abstract
    return ZH_NO_ABSTRACT


def truncate(text: str, max_chars: int = 360) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 1].rstrip() + "..."


def paper_meta_html(paper: dict[str, Any]) -> str:
    authors = escape(", ".join(paper.get("authors", [])) or "\u672a\u77e5\u4f5c\u8005")
    doi = escape(str(paper.get("doi", "")))
    date_text = escape(str(paper.get("date", "\u672a\u77e5\u65e5\u671f")))
    journal = escape(journal_name(paper))
    volume = escape(str(paper.get("volume", "")))
    article_number = escape(str(paper.get("article_number", "")))
    keywords = escape(", ".join(paper.get("keywords", [])) or "None")
    topics = escape(", ".join(paper.get("topics", [])) or "Uncategorized")

    journal_bits = [journal]
    if volume:
        journal_bits.append(f"Volume {volume}")
    if article_number:
        journal_bits.append(f"Article {article_number}")

    return "\n".join(
        [
            f'<p class="meta"><strong>{ZH_AUTHOR}\uff1a</strong>{authors}</p>',
            f'<p class="meta"><strong>{ZH_DATE}\uff1a</strong>{date_text}</p>',
            f'<p class="meta"><strong>{ZH_JOURNAL}\uff1a</strong>{" - ".join(journal_bits)}</p>',
            f'<p class="meta"><strong>DOI\uff1a</strong>{doi}</p>',
            f'<p class="meta"><strong>{ZH_KEYWORDS}\uff1a</strong>{keywords}</p>',
            f'<p class="meta"><strong>{ZH_TOPIC}\uff1a</strong>{topics}</p>',
        ]
    )


def list_items(values: list[str]) -> str:
    if not values:
        return f"<p>{ZH_NO_INFO}</p>"
    items = "\n".join(f"<li>{escape(value)}</li>" for value in values)
    return f"<ul>{items}</ul>"


def analysis_html(record: dict[str, Any] | None) -> str:
    if not record:
        return ""
    analysis = record.get("analysis", {}).get("analysis", {})
    if not analysis:
        return ""
    return "\n".join(
        [
            '<section class="ai-notes">',
            f"<h2>{ZH_AI}</h2>",
            f"<p><strong>\u6587\u7ae0\u505a\u4e86\u4ec0\u4e48\uff1a</strong>{escape(analysis.get('what_was_done', ZH_NO_INFO))}</p>",
            f"<p><strong>\u4e3a\u4ec0\u4e48\u505a\uff1a</strong>{escape(analysis.get('why_it_was_done', ZH_NO_INFO))}</p>",
            f"<p><strong>\u600e\u4e48\u505a\uff1a</strong>{escape(analysis.get('how_it_was_done', ZH_NO_INFO))}</p>",
            f"<p><strong>\u505a\u5f97\u600e\u4e48\u6837\uff1a</strong>{escape(analysis.get('how_well_it_worked', ZH_NO_INFO))}</p>",
            "<h3>\u4e3b\u8981\u7ed3\u8bba</h3>",
            list_items(list_from_analysis(record, "main_conclusions")),
            "<h3>\u4eae\u70b9\u548c\u521b\u65b0\u70b9</h3>",
            list_items(list_from_analysis(record, "highlights_and_innovations")),
            "<h3>\u5c40\u9650\u6027</h3>",
            list_items(list_from_analysis(record, "limitations")),
            "<h3>\u53ef\u80fd\u7684\u53d1\u5c55\u65b9\u5411</h3>",
            list_items(list_from_analysis(record, "future_directions")),
            "<h3>\u6ce8\u610f\u4e8b\u9879</h3>",
            list_items(list_from_analysis(record, "cautions")),
            f"<p><strong>{ZH_KEYWORDS}\uff1a</strong>{escape(', '.join(list_from_analysis(record, 'keywords')) or ZH_NO_INFO)}</p>",
            f"<p><strong>\u9002\u5408\u8bfb\u8005\uff1a</strong>{escape(', '.join(list_from_analysis(record, 'suitable_for')) or ZH_NO_INFO)}</p>",
            f"<p><strong>\u9605\u8bfb\u4f18\u5148\u7ea7\uff1a</strong>{escape(str(analysis.get('reading_priority', '')))}\u3002{escape(str(analysis.get('priority_reason', '')))}</p>",
            "</section>",
        ]
    )


def paper_list_item(paper: dict[str, Any], analyses: dict[str, dict[str, Any]]) -> str:
    title = escape(str(paper.get("title", "Untitled paper")))
    detail_url = paper_detail_url(paper)
    analysis = analyses.get(str(paper.get("doi", "")).lower())
    description = escape(truncate(short_description(paper, analysis)))
    authors = escape(", ".join(paper.get("authors", [])) or "\u672a\u77e5\u4f5c\u8005")
    date_text = escape(str(paper.get("date", "\u672a\u77e5\u65e5\u671f")))
    doi = escape(str(paper.get("doi", "")))
    journal = escape(journal_name(paper))
    priority = escape(text_from_analysis(analysis, "reading_priority"))
    priority_html = f'<span class="badge">\u9605\u8bfb\u4f18\u5148\u7ea7\uff1a{priority}</span>' if priority else ""

    return "\n".join(
        [
            '<article class="paper-summary">',
            f'<h2><a href="{{{{ \'{detail_url}\' | relative_url }}}}">{title}</a></h2>',
            f'<p class="meta"><strong>{ZH_AUTHOR}\uff1a</strong>{authors}</p>',
            f'<p class="meta"><strong>{ZH_JOURNAL}\uff1a</strong>{journal}</p>',
            f'<p class="meta"><strong>{ZH_DATE}\uff1a</strong>{date_text}</p>',
            f'<p class="meta"><strong>DOI\uff1a</strong>{doi}</p>',
            f"<p>{description}</p>",
            priority_html,
            "</article>",
            "",
        ]
    )


def render_paper_detail(paper: dict[str, Any], analyses: dict[str, dict[str, Any]]) -> None:
    title = str(paper.get("title", "Untitled paper"))
    publisher_url = paper.get("url") or f"https://doi.org/{paper.get('doi', '')}"
    abstract = abstract_text(paper)
    analysis = analyses.get(str(paper.get("doi", "")).lower())
    content = [
        front_matter(title),
        f"# {escape(title)}",
        "",
        paper_meta_html(paper),
        "",
        f'<p><a href="{{{{ \'/papers/\' | relative_url }}}}">{ZH_BACK_INDEX}</a></p>',
        "",
    ]
    if publisher_url:
        content.append(f'<p><a href="{escape(str(publisher_url))}">{ZH_PUBLISHER}</a></p>')
        content.append("")
    if abstract:
        content.extend([f"## {ZH_ABSTRACT}", "", f"<p>{escape(abstract)}</p>", ""])
    ai_notes = analysis_html(analysis)
    if ai_notes:
        content.extend([ai_notes, ""])
    write_file(paper_detail_path(paper), "\n".join(content))


def render_index(papers: list[dict[str, Any]], analyses: dict[str, dict[str, Any]]) -> None:
    latest = papers[:12]
    journals = sorted({journal_name(paper) for paper in papers})
    content = [
        front_matter(ZH_LATEST),
        f"# {ZH_LATEST}",
        "",
        f"\u6700\u540e\u66f4\u65b0\uff1a{date.today().isoformat()}",
        "",
        "\u8fd9\u91cc\u5217\u51fa\u6700\u8fd1\u8ffd\u8e2a\u7684\u8bba\u6587\u3002\u70b9\u51fb\u6807\u9898\u8fdb\u5165\u8be6\u60c5\u9875\uff0c\u67e5\u770b\u6458\u8981\u548c AI \u5206\u6790\u3002",
        "",
        f"\u5f53\u524d\u5171\u8ffd\u8e2a {len(papers)} \u7bc7\u8bba\u6587\uff0c\u8986\u76d6 {len(journals)} \u4e2a\u671f\u520a\u3002",
        "",
    ]
    content.extend(paper_list_item(paper, analyses) for paper in latest)
    write_file(DOCS_DIR / "index.md", "\n".join(content))


def render_monthly_archives(papers: list[dict[str, Any]], analyses: dict[str, dict[str, Any]]) -> None:
    by_journal_month: dict[str, dict[str, list[dict[str, Any]]]] = defaultdict(lambda: defaultdict(list))
    journal_names: dict[str, str] = {}
    for paper in papers:
        slug = journal_slug(paper)
        journal_names[slug] = journal_name(paper)
        by_journal_month[slug][paper_month(paper)].append(paper)

    archive_index = [
        front_matter(ZH_INDEX),
        f"# {ZH_INDEX}",
        "",
        "\u6240\u6709\u8ffd\u8e2a\u8bba\u6587\u6309\u671f\u520a\u548c\u6708\u4efd\u5206\u7ec4\u3002\u6bcf\u6761\u8bb0\u5f55\u90fd\u94fe\u63a5\u5230\u5355\u7bc7\u8bba\u6587\u8be6\u60c5\u9875\u3002",
        "",
    ]
    for journal in sorted(by_journal_month.keys(), key=lambda slug: journal_names[slug].lower()):
        archive_index.extend(["", f"## {escape(journal_names[journal])}", ""])
        for month in sorted(by_journal_month[journal].keys(), reverse=True):
            filename = f"{journal}-{month}.md"
            link = f"/papers/{journal}-{month}.html"
            count = len(by_journal_month[journal][month])
            archive_index.append(f"- [{month} ({count})]({{{{ '{link}' | relative_url }}}})")
            page = [
                front_matter(f"{journal_names[journal]} - {month}"),
                f"# {escape(journal_names[journal])} - {month}",
                "",
                f"\u5171 {count} \u7bc7\u8bba\u6587\u3002",
                "",
            ]
            page.extend(paper_list_item(paper, analyses) for paper in by_journal_month[journal][month])
            write_file(PAPERS_DIR / filename, "\n".join(page))
    write_file(PAPERS_DIR / "index.md", "\n".join(archive_index))


def render_topic_pages(papers: list[dict[str, Any]], analyses: dict[str, dict[str, Any]]) -> None:
    by_topic: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for paper in papers:
        for topic in paper.get("topics", ["uncategorized"]):
            by_topic[topic].append(paper)
    topic_index = [front_matter(ZH_TOPICS), f"# {ZH_TOPICS}", ""]
    for topic in sorted(by_topic.keys(), key=str.lower):
        slug = slugify(topic)
        filename = f"{slug}.md"
        link = f"/topics/{slug}.html"
        topic_index.append(f"- [{escape(topic)} ({len(by_topic[topic])})]({{{{ '{link}' | relative_url }}}})")
        page = [
            front_matter(f"{ZH_TOPIC} - {topic}"),
            f"# {escape(topic)}",
            "",
            f"\u5171 {len(by_topic[topic])} \u7bc7\u8bba\u6587\u3002",
            "",
        ]
        page.extend(paper_list_item(paper, analyses) for paper in by_topic[topic])
        write_file(TOPICS_DIR / filename, "\n".join(page))
    write_file(TOPICS_DIR / "index.md", "\n".join(topic_index))


def analysis_search_text(record: dict[str, Any] | None) -> str:
    if not record:
        return ""
    analysis = record.get("analysis", {}).get("analysis", {})
    parts: list[str] = []
    for value in analysis.values():
        if isinstance(value, list):
            parts.extend(str(item) for item in value)
        else:
            parts.append(str(value))
    return " ".join(parts)


def render_search_index(papers: list[dict[str, Any]], analyses: dict[str, dict[str, Any]]) -> None:
    records = []
    for paper in papers:
        doi = str(paper.get("doi", "")).lower()
        analysis = analyses.get(doi)
        records.append(
            {
                "title": paper.get("title", ""),
                "authors": paper.get("authors", []),
                "date": paper.get("date", ""),
                "journal": journal_name(paper),
                "doi": paper.get("doi", ""),
                "url": paper_detail_url(paper),
                "abstract": abstract_text(paper),
                "keywords": paper.get("keywords", []),
                "topics": paper.get("topics", []),
                "ai_text": analysis_search_text(analysis),
                "description": truncate(short_description(paper, analysis), 280),
            }
        )
    write_file(DOCS_DIR / "search-index.json", json.dumps(records, ensure_ascii=False, indent=2) + "\n")


def render_search_page() -> None:
    content = [
        front_matter(ZH_SEARCH),
        f"# {ZH_SEARCH}",
        "",
        '<div class="search-panel">',
        '<input id="search-input" class="search-input" type="search" placeholder="输入标题、作者、关键词、主题、DOI 或 AI 分析内容">',
        '<div class="search-modes" role="radiogroup" aria-label="搜索模式">',
        '<label><input type="radio" name="search-mode" value="global" checked> 全局搜索</label>',
        '<label><input type="radio" name="search-mode" value="keyword"> 关键词/主题</label>',
        '<label><input type="radio" name="search-mode" value="author"> 作者</label>',
        "</div>",
        '<p id="search-count" class="meta">请输入搜索词。</p>',
        "</div>",
        '<div id="search-results"></div>',
        '<script src="{{ \'/assets/search.js\' | relative_url }}"></script>',
        "",
    ]
    write_file(DOCS_DIR / "search.md", "\n".join(content))


def main() -> None:
    papers = load_papers()
    analyses = load_analyses()
    clean_generated_pages()
    for paper in papers:
        render_paper_detail(paper, analyses)
    render_index(papers, analyses)
    render_monthly_archives(papers, analyses)
    render_topic_pages(papers, analyses)
    render_search_index(papers, analyses)
    render_search_page()
    print(f"Rendered {len(papers)} papers into {DOCS_DIR}")


if __name__ == "__main__":
    main()
