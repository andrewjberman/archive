#!/usr/bin/env python3
"""Wall Street Journal REST consumer -- no login, no session to park. Standing reference for
AMGT_RESAPP, mirroring sa_rest_fetch.py / ft_rest_fetch.py's shape and ROE.

MEASURED CONTRACT (4.0.0_SA_CRO~Z, 2026-09-10):
  1. Auth mechanism: NONE. Bright Data's Web Unlocker (zone=one_shotter) defeats WSJ's bot-wall
     cookielessly and returns public-page HTML. This is the SAME call the estate's production
     fetch_wsj.py already makes; this module just packages it standalone.
  2. WSJ has NO Seeking-Alpha-style dedicated per-security report. What it DOES have:
         https://www.wsj.com/market-data/quotes/{TICKER}
     -- a real, fully public per-ticker page (its own embedded state literally tags the visitor
     "user_type": "nonsubscriber"), loads fine over the Web Unlocker. Its React/Redux state
     (window.__STATE__) sometimes embeds a genuine per-ticker news array under a key shaped
         data["quotes_latestNews_{\"ticker\":\"RTX\",...}"].data.data.news
     -- MEASURED PRESENT on one fetch with real structure, ABSENT on a repeat fetch of the exact
     same URL seconds later. This is a timing/hydration race in Bright Data's static snapshot,
     not a stable feature -- extract_ticker_news() below retries with a stated cap and reports
     honestly whether it found the key, never treating an absence as an empty feed.
  3. `wsj.com/search?query=...` is a near-empty client-rendered shell over plain REST (measured:
     252 bytes, no visible text) -- it needs a real browser; do not build on it as a REST source.

ROE (inherited unchanged): observe-act-only; never log a fetched credential (none apply here --
WSJ needs none); the Bright Data API key is read from Secrets Manager and never printed.

C-VENDOR-EGRESS: an external vendor call needs Andrew's explicit per-use word. The 2026-09-10
word covered that day's investigation. A SCHEDULED consumer built on this module needs its own.

Usage:
  python wsj_rest_fetch.py listing home markets economy business finance   # article links, per fetch_wsj.py's own listing set
  python wsj_rest_fetch.py article <url>                                   # one article, full text
  python wsj_rest_fetch.py quote RTX                                      # market-data quote page + ticker news (best-effort)
Options:  --out <dir>   write each payload as JSON
Env:      SA_SECRETS_DIR=<dir>  read secret_*.json from disk instead of Secrets Manager (dev only)
"""
import html as htmlmod
import json
import os
import re
import sys
import time

import requests

ENDPOINT = "https://api.brightdata.com/request"
ZONE = "one_shotter"
PACE_SECONDS = 1.5

# The estate's own committed pattern (tools/astn_wsjft/configs/sources.json) -- cited, not
# reinvented; matches WSJ's URL shape as of the 2026-06-25 measurement and re-confirmed live today.
ARTICLE_LINK_PATTERN = r"^https://www\.wsj\.com/(articles|economy|finance|world|business|politics|markets|tech|health|science)/[^?#]+-[0-9a-f]{6,}"
EXCLUDE_LINK_PATTERN = r"(/livecoverage/|/video/|/podcasts/|/buyside/|utm_|/author/|/sports/|/style/|/arts-culture/)"
LISTING_URLS = {
    "home": "https://www.wsj.com",
    "markets": "https://www.wsj.com/news/markets",
    "economy": "https://www.wsj.com/economy",
    "business": "https://www.wsj.com/news/business",
    "finance": "https://www.wsj.com/finance",
}


def _secret(name):
    d = os.environ.get("SA_SECRETS_DIR")
    if d:
        with open(os.path.join(d, "secret_" + name.replace("/", "_") + ".json"), encoding="utf-8") as fh:
            return fh.read().strip()
    import boto3
    return boto3.client("secretsmanager", region_name="us-east-1").get_secret_value(SecretId=name)["SecretString"]


def strip_html(t):
    return re.sub(r"\s+", " ", re.sub("<[^>]+>", " ", htmlmod.unescape(t or ""))).strip()


def web_unlocker(url):
    key = _secret("brightdata-api-key").strip()
    body = json.dumps({"zone": ZONE, "url": url, "format": "raw"}).encode()
    r = requests.post(ENDPOINT, data=body, headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"}, timeout=150)
    if r.status_code != 200:
        raise RuntimeError(f"Web Unlocker GET {url} -> {r.status_code}: {r.text[:200]}")
    if len(r.text) < 200:
        raise RuntimeError(f"Web Unlocker GET {url} -> 200 but {len(r.text)}-byte body -- treat as a REFUSAL, not empty content")
    return r.text


def listing(section):
    """Copied verbatim from fetch_wsj.py's article_links() -- stdlib regex, no bs4 (EXTEND, never
    rebuild: the extraction logic already exists and is proven; this just packages it standalone
    for a reference script that lives outside the ASTN_WSJFT tree)."""
    url = LISTING_URLS.get(section, section if section.startswith("http") else section)
    html = web_unlocker(url)
    pat = re.compile(ARTICLE_LINK_PATTERN)
    exc = re.compile(EXCLUDE_LINK_PATTERN)
    found, seen = [], set()
    for m in re.finditer(r'href="([^"]+)"', html):
        u = htmlmod.unescape(m.group(1)).split("?")[0]
        if pat.match(u) and not exc.search(u) and u not in seen:
            seen.add(u)
            found.append(u)
    return {"section": section, "url": url, "article_urls": found}


def article(url, *, response_path=None):
    """Keep canonical Unlocker transport; normalize only the returned article body."""
    html = web_unlocker(url)
    if response_path is not None:
        from pathlib import Path
        Path(response_path).write_text(html, encoding="utf-8")
    return parse_article(html, url)


def parse_article(html, url):
    from bs4 import BeautifulSoup

    ogt = re.search(r'(?is)property="og:title"\s+content="([^"]+)"', html) or re.search(r"(?is)<title[^>]*>(.*?)</title>", html)
    title = htmlmod.unescape(ogt.group(1)).strip() if ogt else ""
    pub = re.search(r'(?is)property="article:published_time"\s+content="([^"]+)"', html) or re.search(r'(?is)"datePublished"\s*:\s*"([^"]+)"', html)
    published = pub.group(1).strip() if pub else None
    boilerplate = re.compile(
        r"(subscriber agreement|dow jones reprint|complete digital access|pay a year upfront|"
        r"for help please visit|cancel anytime during your trial|all rights reserved|"
        r"sign in|create an account|this copy is for your personal)", re.IGNORECASE,
    )
    soup = BeautifulSoup(html, "html.parser")
    body = soup.select_one('article .crawler section')
    paras = []
    if body:
        for node in body.select("script, style, noscript, button, form"):
            node.decompose()
        for node in body.select("p, h2, h3, li, blockquote, table"):
            if node.find_parent(["li", "blockquote", "table"]):
                continue
            t = node.get_text(" ", strip=True)
            if t and not boilerplate.search(t):
                paras.append(t)
    text = "\n\n".join(paras)
    expected_words = None
    state_node = soup.select_one("#__NEXT_DATA__")
    if state_node:
        try:
            props = json.loads(state_node.string)["props"]["pageProps"]
            expected_words = props["articleData"]["meta"]["metrics"].get("wordCount")
        except (TypeError, ValueError, KeyError):
            pass
    completeness = "requires_review" if body else "missing_body"
    if isinstance(expected_words, (int, float)) and expected_words > len(text.split()) * 1.3:
        completeness = "partial_body"
    return {"url": url, "title": title, "published": published, "text_chars": len(text), "text": text,
            "body_source": "web_unlocker_html.article.crawler.section",
            "expected_word_count": expected_words, "completeness": completeness}


def extract_balanced(text, start_marker):
    i = text.index(start_marker) + len(start_marker)
    while text[i] != "{":
        i += 1
    depth = 0
    j = i
    in_str = False
    esc = False
    q = ""
    while j < len(text):
        c = text[j]
        if in_str:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == q:
                in_str = False
        else:
            if c in ('"', "'"):
                in_str = True
                q = c
            elif c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    return text[i:j + 1]
        j += 1
    raise ValueError("unbalanced braces from " + start_marker)


def extract_ticker_news(ticker, max_attempts=3, *, response_dir=None):
    """MEASURED INTERMITTENT: the market-data quote page's window.__STATE__ sometimes carries a
    per-ticker news array and sometimes does not, on an identical URL fetched seconds apart --
    Bright Data's static snapshot appears to race the page's own async hydration. Retries up to
    max_attempts and reports which attempt (if any) found it; NEVER claims absence proves no feed
    exists, and never fabricates a result on a miss."""
    url = f"https://www.wsj.com/market-data/quotes/{ticker.upper()}"
    diagnostics = []
    for attempt in range(1, max_attempts + 1):
        html = web_unlocker(url)
        diagnostic = {"attempt": attempt, "bytes": len(html), "state_marker_present": "window.__STATE__" in html}
        diagnostics.append(diagnostic)
        if response_dir is not None:
            from pathlib import Path
            folder = Path(response_dir)
            folder.mkdir(parents=True, exist_ok=True)
            (folder / f"quote-attempt-{attempt}.html").write_text(html, encoding="utf-8")
        try:
            blob = extract_balanced(html, "window.__STATE__ =")
            d = json.loads(blob)
        except Exception as exc:
            diagnostic["parse_error_type"] = type(exc).__name__
            time.sleep(PACE_SECONDS)
            continue
        keys = [k for k in d.get("data", {}) if k.startswith("quotes_latestNews_")]
        diagnostic["news_key_count"] = len(keys)
        if keys:
            news = d["data"][keys[0]]
            return {"ticker": ticker.upper(), "url": url, "found_on_attempt": attempt, "attempts": attempt,
                    "state_key": keys[0], "news_node": news, "diagnostics": diagnostics}
        time.sleep(PACE_SECONDS)
    return {"ticker": ticker.upper(), "url": url, "found_on_attempt": None, "attempts": max_attempts,
            "diagnostics": diagnostics,
            "note": "quotes_latestNews_ key not present in window.__STATE__ on any attempt -- "
                    "a timing/hydration race in the Unlocker's snapshot, not proof the feed is absent"}


def quote(ticker):
    url = f"https://www.wsj.com/market-data/quotes/{ticker.upper()}"
    html = web_unlocker(url)
    title_m = re.search(r"<title[^>]*>(.*?)</title>", html, re.S | re.I)
    nonsub = '"user_type": "nonsubscriber"' in html or '"user_type":"nonsubscriber"' in html
    news = extract_ticker_news(ticker)
    return {"ticker": ticker.upper(), "url": url, "title": (title_m.group(1).strip() if title_m else None),
            "bytes": len(html), "publicly_readable_as_nonsubscriber": nonsub, "news": news}


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    verb = argv[1]
    args = [a for a in argv[2:] if not a.startswith("--")]
    out = argv[argv.index("--out") + 1] if "--out" in argv else None
    results = {}
    try:
        if verb == "listing":
            for sec in args:
                r = listing(sec)
                results[sec] = r
                print(f"OK: {sec:<10} article urls: {len(r['article_urls'])}")
                time.sleep(PACE_SECONDS)
        elif verb == "article":
            for url in args:
                r = article(url)
                results[url] = r
                print(f"OK: {url[:70]} title={r['title']!r} text_chars={r['text_chars']}")
                time.sleep(PACE_SECONDS)
        elif verb == "quote":
            for tk in args:
                r = quote(tk)
                results[tk] = r
                nk = r["news"].get("found_on_attempt")
                print(f"OK: {tk.upper()} bytes={r['bytes']} nonsubscriber={r['publicly_readable_as_nonsubscriber']} "
                      f"news_found_on_attempt={nk} of {r['news']['attempts']}")
                time.sleep(PACE_SECONDS)
        else:
            print("ERROR: unknown verb %r" % verb)
            return 2
    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {e}")
        return 1
    if out:
        os.makedirs(out, exist_ok=True)
        for k, v in results.items():
            safe = re.sub(r"[^A-Za-z0-9._-]", "_", k)[:80]
            p = os.path.join(out, f"{verb}.{safe}.json")
            with open(p, "w", encoding="utf-8", newline="\n") as fh:
                json.dump(v, fh, indent=1)
            print("OK: wrote %s" % p)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
