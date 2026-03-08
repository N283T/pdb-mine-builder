#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "httpx",
#     "beautifulsoup4",
# ]
# ///
"""Fetch all SQL examples from pdbj.org/help/mine-sql-ex* pages."""

import json
import re
import sys
from pathlib import Path

import httpx
from bs4 import BeautifulSoup

BASE_URL = "https://pdbj.org/help/mine-sql-ex{num:03d}"
OUTPUT_FILE = Path(__file__).parent.parent / "scripts" / "pdbj_examples_raw.json"
MAX_CONSECUTIVE_404 = 5


def fetch_example(client: httpx.Client, num: int) -> dict | None:
    """Fetch a single example page and extract title + SQL."""
    url = BASE_URL.format(num=num)
    try:
        resp = client.get(url, params={"lang": "ja"})
        if resp.status_code == 404:
            return None
        resp.raise_for_status()
    except httpx.HTTPStatusError:
        return None

    soup = BeautifulSoup(resp.text, "html.parser")

    # Extract title - usually in the main content area
    title = ""
    # Try <h2> or <h3> inside main content
    main = soup.find("div", class_="main") or soup.find("main") or soup
    for tag in main.find_all(["h1", "h2", "h3", "h4"]):
        text = tag.get_text(strip=True)
        # Skip navigation-like headers
        if text and len(text) > 10 and "PDBj" not in text and "Mine" not in text:
            title = text
            break

    # If no good header found, look for the first substantial paragraph
    if not title:
        for p in main.find_all("p"):
            text = p.get_text(strip=True)
            if len(text) > 20:
                title = text
                break

    # Extract SQL query from <pre>, <code>, or <textarea>
    sql = ""
    # Try textarea first (common for SQL forms)
    textarea = soup.find("textarea")
    if textarea:
        sql = textarea.get_text(strip=True)

    # Try <pre> tags
    if not sql:
        for pre in soup.find_all("pre"):
            text = pre.get_text(strip=True)
            if any(kw in text.upper() for kw in ["SELECT", "WITH", "INSERT"]):
                sql = text
                break

    # Try <code> tags
    if not sql:
        for code in soup.find_all("code"):
            text = code.get_text(strip=True)
            if any(kw in text.upper() for kw in ["SELECT", "WITH"]):
                sql = text
                break

    # Try finding SQL in any text node that looks like SQL
    if not sql:
        all_text = soup.get_text()
        # Look for SELECT ... FROM pattern
        match = re.search(
            r"((?:SELECT|WITH)\s+.+?(?:FROM|LIMIT)\s+\S+(?:\s+.+?)*?)(?:\n\n|\Z)",
            all_text,
            re.DOTALL | re.IGNORECASE,
        )
        if match:
            sql = match.group(1).strip()

    if not sql:
        print(f"  WARNING: No SQL found for ex{num:03d}", file=sys.stderr)

    # Get full page text for context
    page_text = soup.get_text(separator="\n", strip=True)

    return {
        "number": num,
        "url": url,
        "title": title,
        "sql": sql,
        "page_text": page_text[:2000],  # Truncate for reference
    }


def main():
    results = []
    consecutive_404 = 0

    with httpx.Client(follow_redirects=True, timeout=30.0) as client:
        num = 1
        while consecutive_404 < MAX_CONSECUTIVE_404:
            print(f"Fetching ex{num:03d}...", end=" ")
            result = fetch_example(client, num)

            if result is None:
                print("404")
                consecutive_404 += 1
            else:
                print(f"OK - {result['title'][:50]}...")
                results.append(result)
                consecutive_404 = 0

            num += 1

    print(f"\nTotal examples found: {len(results)}")
    print(f"Range: ex001 to ex{results[-1]['number']:03d}")

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(json.dumps(results, ensure_ascii=False, indent=2))
    print(f"Saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
