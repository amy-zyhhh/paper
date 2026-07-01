from __future__ import annotations

import json
import re
from collections import defaultdict
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "papers.json"
DOCS_DIR = ROOT / "docs"
PAPERS_DIR = DOCS_DIR / "papers"
TOPICS_DIR = DOCS_DIR / "topics"


def load_papers() -> list[dict]:
    with DATA_FILE.open("r", encoding="utf-8") as file:
        papers = json.load(file)
    return sorted(papers, key=lambda paper: paper.get("date", ""), reverse=True)


def slugify(value: str) -> str:
    slug = value.lower().strip()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    return slug.strip("-") or "topic"


def front_matter(title: str, layout: str = "default") -> str:
    return f"---\nlayout: {layout}\ntitle: {title}\n---\n\n"


def paper_markdown(paper: dict) -> str:
    authors = ", ".join(paper.get("authors", [])) or "Unknown authors"
    keywords = ", ".join(paper.get("keywords", [])) or "None"
    topics = ", ".join(paper.get("topics", [])) or "Uncategorized"
    doi = paper.get("doi", "")
    url = paper.get("url") or (f"https://doi.org/{doi}" if doi else "")
    abstract = paper.get("abstract", "")
    date_text = paper.get("date", "Unknown date")
    journal = paper.get("journal", "Journal of the Mechanics and Physics of Solids")
    volume = paper.get("volume", "")
    article_number = paper.get("article_number", "")

    journal_bits = [journal]
    if volume:
        journal_bits.append(f"Volume {volume}")
    if article_number:
        journal_bits.append(f"Article {article_number}")

    link = f"[Publisher Link]({url})" if url else ""

    return "\n".join(
        [
            '<article class="paper">',
            f"## {paper.get('title', 'Untitled paper')}",
            "",
            f'<p class="meta"><strong>Authors:</strong> {authors}</p>',
            f'<p class="meta"><strong>Date:</strong> {date_text}</p>',
            f'<p class="meta"><strong>Journal:</strong> {" - ".join(journal_bits)}</p>',
            f'<p class="meta"><strong>DOI:</strong> {doi}</p>',
            f'<p class="meta"><strong>Keywords:</strong> {keywords}</p>',
            f'<p class="meta"><strong>Topics:</strong> {topics}</p>',
            "",
            abstract,
            "",
            link,
            "</article>",
            "",
        ]
    )


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def render_index(papers: list[dict]) -> None:
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
    content.extend(paper_markdown(paper) for paper in latest)
    write_file(DOCS_DIR / "index.md", "\n".join(content))


def render_monthly_archives(papers: list[dict]) -> None:
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
        page.extend(paper_markdown(paper) for paper in by_month[month])
        write_file(PAPERS_DIR / filename, "\n".join(page))

    write_file(PAPERS_DIR / "index.md", "\n".join(archive_index))


def render_topic_pages(papers: list[dict]) -> None:
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
        page.extend(paper_markdown(paper) for paper in by_topic[topic])
        write_file(TOPICS_DIR / filename, "\n".join(page))

    write_file(TOPICS_DIR / "index.md", "\n".join(topic_index))


def main() -> None:
    papers = load_papers()
    render_index(papers)
    render_monthly_archives(papers)
    render_topic_pages(papers)
    print(f"Rendered {len(papers)} papers into {DOCS_DIR}")


if __name__ == "__main__":
    main()
