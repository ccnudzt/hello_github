#!/usr/bin/env python3
"""
Fetch GitHub Trending Repositories (This month, All languages) – Top 3
and write the results to docs/trending-monthly-top3.md
"""

import sys
import os
from datetime import datetime, timezone

import requests
from bs4 import BeautifulSoup

TRENDING_URL = "https://github.com/trending?since=monthly"
OUTPUT_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "docs",
    "trending-monthly-top3.md",
)
TOP_N = 3
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}


def fetch_trending(top_n: int = TOP_N):
    """Fetch trending repositories and return a list of (name, url, description) tuples."""
    try:
        response = requests.get(TRENDING_URL, headers=HEADERS, timeout=30)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        print("ERROR: Request timed out after 30 seconds.", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.HTTPError as exc:
        print(
            f"ERROR: Received HTTP error {exc.response.status_code} from GitHub Trending.",
            file=sys.stderr,
        )
        sys.exit(1)
    except requests.RequestException as exc:
        print(f"ERROR: Failed to fetch GitHub Trending page: {exc}", file=sys.stderr)
        sys.exit(1)

    soup = BeautifulSoup(response.text, "lxml")

    # Each trending repo is inside an <article class="Box-row"> element
    articles = soup.select("article.Box-row")
    if not articles:
        print(
            "ERROR: Could not find any repository entries on the page. "
            "The page structure may have changed.",
            file=sys.stderr,
        )
        sys.exit(1)

    repos = []
    for article in articles[:top_n]:
        # Repo name link: <h2><a href="/owner/repo">
        name_tag = article.select_one("h2 a")
        if name_tag is None:
            print("WARNING: Skipping an entry – could not find name/link.", file=sys.stderr)
            continue
        href = name_tag.get("href", "").strip()
        # href is like "/owner/repo"
        repo_url = f"https://github.com{href}"
        repo_name = href.lstrip("/")  # "owner/repo"

        # Description: GitHub renders it in a <p> with class "col-9"
        desc_tag = article.select_one("p.col-9")
        description = desc_tag.get_text(strip=True) if desc_tag else ""

        repos.append((repo_name, repo_url, description))

    if not repos:
        print("ERROR: Parsed zero repositories – check HTML selectors.", file=sys.stderr)
        sys.exit(1)

    return repos


def write_markdown(repos, output_path: str = OUTPUT_FILE):
    """Write the results to a Markdown file."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        "# GitHub 当月热榜 Top 3 仓库\n",
        f"> 数据来源：[GitHub Trending (This month)]({TRENDING_URL})  \n",
        f"> 最后更新：{now}\n",
        "\n",
        "| 排名 | 仓库 | 简介 |\n",
        "| ---- | ---- | ---- |\n",
    ]
    for rank, (name, url, desc) in enumerate(repos, start=1):
        lines.append(f"| {rank} | [{name}]({url}) | {desc} |\n")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.writelines(lines)

    print(f"Written {len(repos)} entries to {output_path}")
    for rank, (name, url, _) in enumerate(repos, start=1):
        print(f"  {rank}. {name} — {url}")


def main():
    repos = fetch_trending(TOP_N)
    write_markdown(repos, OUTPUT_FILE)


if __name__ == "__main__":
    main()
