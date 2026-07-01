from __future__ import annotations

import json
import re
from collections import defaultdict
from datetime import date
from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "papers.json"
ANALYSES_FILE = ROOT / "data" / "analyses.json"
DOCS_DIR = ROOT / "docs"
PAPERS_DIR = DOCS_DIR / "papers"
TOPICS_DIR = DOCS_DIR / "topics"


def load_papers() -> list[dict]:
    with DATA_FILE.open("r", encoding="utf-8") as file:
        papers = json.load(file)
    return sorted(papers, key=lambda paper: paper.get("date", ""), reverse=True)


def load_analyses() -> dict[str, dict]:
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
    return slug.strip("-") or "topic"


def front_matter(title: str, layout: str = "default") -> str:
    return f"---\nlayout: {layout}\ntitle: {title}\n---\n\n"


def list_items(values: list[str]) -> str:
    if not values:
        return "<p>原文信息不足</p>"
    items = "\n".join(f"<li>{escape(str(value))}</li>" for value in values)
    return f"<ul>{items}</ul>"


def analysis_markdown(record: dict | None) -> str:
    if not record:
        return ""

    analysis = record.get("analysis", {}).get("analysis", {})
    if not analysis:
        return ""

    priority = escape(analysis.get("reading_priority", ""))
    priority_reason = escape(analysis.get("priority_reason", ""))

    return "\n".join(
        [
            '<section class="ai-notes">',
            "<h3>AI Notes</h3>",
            f"<p><strong>文章做了什么：</strong>{escape(analysis.get('what_was_done', '原文信息不足'))}</p>",
            f"<p><strong>为什么做：</strong>{escape(analysis.get('why_it_was_done', '原文信息不足'))}</p>",
            f"<p><strong>怎么做：</strong>{escape(analysis.get('how_it_was_done', '原文信息不足'))}</p>",
            f"<p><strong>做得怎么样：</strong>{escape(analysis.get('how_well_it_worked', '原文信息不足'))}</p>",
            "<h4>主要结论</h4>",
            list_items(analysis.get("main_conclusions", [])),
            "<h4>亮点和创新点</h4>",
            list_items(analysis.get("highlights_and_innovations", [])),
            "<h4>局限性</h4>",
            list_items(analysis.get("limitations", [])),
            "<h4>可能的发展方向</h4>",
            list_items(analysis.get("future_directions", [])),
            "<h4>注意事项</h4>",
            list_items(analysis.get("cautions", [])),
            f"<p><strong>关键词：</strong>{escape(', '.join(analysis.get('keywords', [])) or '原文信息不足')}</p>",
            f"<p><strong>适合读者：</strong>{escape(', '.join(analysis.get('suitable_for', [])) or '原文信息不足')}</p>",
            f"<p><strong>阅读优先级：</strong>{priority}。{priority_reason}</p>",
            "</section>",
        ]
    )


def paper_markdown(paper: dict, analyses: dict[str, dict]) -> str:
    title = escape(paper.get("title", "Untitled paper"))
    authors = escape(", ".join(paper.get("authors", [])) or "Unknown authors")
    keywords = escape(", ".join(paper.get("keywords", [])) or "None")
    topics = escape(", ".join(paper.get("topics", [])) or "Uncategorized")
    doi = escape(paper.get("doi", ""))
    url = paper.get("url") or (f"https://doi.org/{doi}" if doi else "")
    elsevier_abstract = (
        paper.get("content", {})
        .get("elsevier", {})
        .get("abstract", "")
    )
    abstract = escape(paper.get("abstract") or elsevier_abstract)
    date_text = escape(paper.get("date", "Unknown date"))
    journal = escape(paper.get("journal", "Journal of the Mechanics and Physics of Solids"))
    volume = escape(paper.get("volume", ""))
    article_number = escape(paper.get("article_number", ""))

    journal_bits = [journal]
    if volume:
        journal_bits.append(f"Volume {volume}")
    if article_number:
        journal_bits.append(f"Article {article_number}")

    link = f'<p><a href="{escape(url)}">Publisher Link</a></p>' if url else ""
    analysis = analysis_markdown(analyses.get(paper.get("doi", "").lower()))

    return "\n".join(
        [
            '<article class="paper">',
            f"<h2>{title}</h2>",
            f'<p class="meta"><strong>Authors:</strong> {authors}</p>',
            f'<p class="meta"><strong>Date:</strong> {date_text}</p>',
            f'<p class="meta"><strong>Journal:</strong> {" - ".join(journal_bits)}</p>',
            f'<p class="meta"><strong>DOI:</strong> {doi}</p>',
            f'<p class="meta"><strong>Keywords:</strong> {keywords}</p>',
            f'<p class="meta"><strong>Topics:</strong> {topics}</p>',
            "",
            f"<p>{abstract}</p>" if abstract else "",
            link,
            analysis,
            "</article>",
            "",
        ]
    )


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def render_index(papers: list[dict], analyses: dict[str, dict]) -> None:
    latest = papers[:10]
    content = [
        front_matter("Latest JMPS Papers"),
        "# Latest JMPS Papers",
        "",
        f"Last updated: {date.today().isoformat()}",
        "",
        "Recent papers tracked from Journal of the Mechanics and Physics of Solids.",
        "",
    ]
    content.extend(paper_markdown(paper, analyses) for paper in latest)
    write_file(DOCS_DIR / "index.md", "\n".join(content))


def render_monthly_archives(papers: list[dict], analyses: dict[str, dict]) -> None:
    by_month: dict[str, list[dict]] = defaultdict(list)
    for paper in papers:
        month = paper.get("date", "unknown")[:7]
        by_month[month].append(paper)

    archive_index = [
        front_matter("Paper Archive"),
        "# Paper Archive",
        "",
    ]

    for month in sorted(by_month.keys(), reverse=True):
        filename = f"{month}.md"
        link = f"/papers/{month}.html"
        archive_index.append(f"- [{month}]({{{{ '{link}' | relative_url }}}})")
        page = [
            front_matter(f"JMPS Papers - {month}"),
            f"# JMPS Papers - {month}",
            "",
        ]
        page.extend(paper_markdown(paper, analyses) for paper in by_month[month])
        write_file(PAPERS_DIR / filename, "\n".join(page))

    write_file(PAPERS_DIR / "index.md", "\n".join(archive_index))


def render_topic_pages(papers: list[dict], analyses: dict[str, dict]) -> None:
    by_topic: dict[str, list[dict]] = defaultdict(list)
    for paper in papers:
        for topic in paper.get("topics", ["uncategorized"]):
            by_topic[topic].append(paper)

    topic_index = [
        front_matter("Topics"),
        "# Topics",
        "",
    ]

    for topic in sorted(by_topic.keys(), key=str.lower):
        slug = slugify(topic)
        filename = f"{slug}.md"
        link = f"/topics/{slug}.html"
        topic_index.append(f"- [{topic}]({{{{ '{link}' | relative_url }}}})")
        page = [
            front_matter(f"Topic - {topic}"),
            f"# {topic}",
            "",
        ]
        page.extend(paper_markdown(paper, analyses) for paper in by_topic[topic])
        write_file(TOPICS_DIR / filename, "\n".join(page))

    write_file(TOPICS_DIR / "index.md", "\n".join(topic_index))


def main() -> None:
    papers = load_papers()
    analyses = load_analyses()
    render_index(papers, analyses)
    render_monthly_archives(papers, analyses)
    render_topic_pages(papers, analyses)
    print(f"Rendered {len(papers)} papers into {DOCS_DIR}")


if __name__ == "__main__":
    main()
