# Requires: playwright, drissionpage, beautifulsoup4, pandas
# Install:
#   pip install playwright drissionpage beautifulsoup4 pandas
#   playwright install
#
# Run:
#   python crawl_mit_blogs.py
#
# Output: blogs.csv

import asyncio
import re
from pathlib import Path
from urllib.parse import urljoin

import pandas as pd
from bs4 import BeautifulSoup

# ---------- Helpers ----------

def parse_article(html: str):
    soup = BeautifulSoup(html, "html.parser")
    # Title
    title_el = soup.select_one("h1, h1.entry-title")
    title = title_el.get_text(strip=True) if title_el else ""
    # Author
    author_el = soup.select_one('[rel="author"], .author, .byline a, .post-author a')
    author = author_el.get_text(strip=True) if author_el else ""
    # Time
    time_el = soup.select_one("time, .post-date, .entry-date")
    time = time_el.get_text(strip=True) if time_el else ""
    # Comment count
    cc_el = soup.select_one(".comments-link, .comment-count, a[href*='#comments']")
    comment_count = ""
    if cc_el:
        m = re.search(r"(\d+)", cc_el.get_text(" ", strip=True))
        if m:
            comment_count = m.group(1)
    # Content & images
    article = soup.select_one("article, .post, .entry-content")
    if not article:
        article = soup
    # paragraphs text
    paras = [p.get_text(" ", strip=True) for p in article.select("p")]
    content = "\n\n".join([p for p in paras if p])
    # images
    imgs = [img.get("src") or img.get("data-src") for img in article.select("img")]
    imgs = [u for u in imgs if u]
    return title, author, comment_count, time, content, imgs

# ---------- Playwright flow ----------
async def crawl_with_playwright(base_url="https://mitadmissions.org/blogs/"):
    from playwright.async_api import async_playwright
    rows = []
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(base_url, wait_until="domcontentloaded")

        # Collect first N article links from listing
        links = await page.eval_on_selector_all(
            "a[href*='/blogs/']",
            "els => Array.from(new Set(els.map(e => e.href))).slice(0, 20)"
        )
        # Filter to post detail pages (heuristic)
        links = [u for u in links if re.search(r"/blogs/\d{4}/", u)]
        links = links[:12]

        for url in links:
            await page.goto(url, wait_until="domcontentloaded")
            html = await page.content()
            title, author, cc, time, content, imgs = parse_article(html)
            rows.append({
                "Title": title,
                "Author": author,
                "Comment Count": cc,
                "Time": time,
                "Article Content": content,
                "Images In Article": ";".join(imgs)
            })
        await browser.close()
    return rows

# ---------- DrissionPage flow ----------
def crawl_with_drissionpage(base_url="https://mitadmissions.org/blogs/"):
    from DrissionPage import ChromiumPage
    import time as _time

    page = ChromiumPage()
    page.get(base_url)

    # Collect links
    els = page.eles("a[href*='/blogs/']")
    links = []
    for el in els[:200]:
        href = el.attr("href")
        if href and re.search(r"/blogs/\d{4}/", href):
            links.append(href)
    # dedupe & limit
    seen = set()
    links2 = []
    for u in links:
        if u not in seen:
            seen.add(u)
            links2.append(u)
    links = links2[:12]

    rows = []
    for url in links:
        page.get(url)
        _time.sleep(0.4)
        html = page.html
        title, author, cc, time, content, imgs = parse_article(html)
        rows.append({
            "Title": title,
            "Author": author,
            "Comment Count": cc,
            "Time": time,
            "Article Content": content,
            "Images In Article": ";".join(imgs)
        })
    page.quit()
    return rows

async def main():
    rows_p = await crawl_with_playwright()
    rows_d = crawl_with_drissionpage()

    # merge & dedupe by Title
    df = pd.DataFrame(rows_p + rows_d).drop_duplicates(subset=["Title"])
    out = Path("blogs.csv")
    df.to_csv(out, index=False, encoding="utf-8")
    print(f"Wrote {out.resolve()} with {len(df)} rows.")

if __name__ == "__main__":
    asyncio.run(main())
