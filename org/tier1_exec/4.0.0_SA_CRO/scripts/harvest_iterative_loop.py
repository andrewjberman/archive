"""Local headful publication loop. Raw content and browser state stay in .runtime.

Run one complete round, inspect notes, change strategy, then resume. A successful
round needs five distinct scoped article bodies per publisher. The state records
per-publisher and joint consecutive-ticker streaks. Never counts a page shell.
"""

import argparse
import datetime as dt
import hashlib
import importlib.util
import json
import pathlib
import re
import subprocess
import sys
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parents[4]
SCRIPTS = pathlib.Path(__file__).resolve().parent
ORDER = ["sa", "ft", "wsj", "bbg"]
BASE = {
    "sa": "https://seekingalpha.com",
    "ft": "https://www.ft.com",
    "wsj": "https://www.wsj.com",
    "bbg": "https://www.bloomberg.com",
}
REVISION = "headful-dom-v6"
SOURCE_BYTES = pathlib.Path(__file__).read_bytes()
SOURCE_SHA256 = hashlib.sha256(SOURCE_BYTES).hexdigest()
COMPANY = {
    "BA": "Boeing",
    "COST": "Costco",
    "HD": "Home Depot",
    "INTU": "Intuit",
    "VLO": "Valero",
    "HAL": "Halliburton",
    "KMB": "Kimberly-Clark",
}
SELECTORS = {
    "sa": [
        '[data-test-id="content-container"]',
        '[data-test-id="article-content"]',
        '[itemprop="articleBody"]',
    ],
    "ft": ['[data-component="article-content-body"]'],
    "wsj": [
        '[data-testid="article-body"]',
        '[class*="articleBody"]',
        '[class*="article-content"]',
        "article .crawler section",
    ],
    "bbg": [
        '[data-component="article-body"]',
        '[class*="body-content"]',
        '[class*="BodyContent"]',
        '[data-component="body"]',
    ],
}


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)


def load_client(pub):
    name = {"bbg": "bloomberg"}.get(pub, pub) + "_rest_fetch"
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / (name + ".py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def seed(context, pub):
    if pub == "wsj":
        return
    m = load_client(pub)
    b = json.loads(m._secret(m.SESSION_SECRET_ID))
    cookies = (
        b.get("all_cookies")
        if pub != "ft"
        else [
            {"name": k, "value": v, "domain": ".ft.com", "path": "/"}
            for k, v in b.items()
        ]
    )
    selected = []
    for c in cookies:
        if not any(
            d in c.get("domain", "")
            for d in ["seekingalpha.com", "ft.com", "bloomberg.com"]
        ):
            continue
        v = {
            k: c[k]
            for k in ["name", "value", "domain", "path", "secure", "httpOnly"]
            if k in c
        }
        v.setdefault("path", "/")
        selected.append(v)
    context.add_cookies(selected)


def listing_url(pub, ticker, exchange):
    return {
        "sa": f"{BASE[pub]}/symbol/{ticker}/news",
        "ft": f"https://markets.ft.com/data/equities/tearsheet/summary?s={ticker}:{exchange}",
        "wsj": f"{BASE[pub]}/market-data/quotes/{ticker}",
        "bbg": f"{BASE[pub]}/quote/{ticker}:US",
    }[pub]


def article_url(pub, url):
    p = urlparse(url)
    host = p.hostname or ""
    path = p.path
    if pub == "sa":
        return host == "seekingalpha.com" and bool(
            re.match(r"/(news|article)/\d+", path)
        )
    if pub == "ft":
        return host == "www.ft.com" and bool(
            re.fullmatch(r"/content/[a-f0-9-]{36}", path)
        )
    if pub == "wsj":
        return (
            host == "www.wsj.com"
            and bool(re.search(r"-[a-f0-9]{8,}$", path))
            and not any(x in path for x in ["/video/", "/livecoverage/", "/buyside/"])
        )
    return host == "www.bloomberg.com" and bool(
        re.match(r"/(news|opinion|features)/articles/", path)
    )


def snapshot(page, folder, label):
    html = page.content()
    (folder / (label + ".html")).write_text(html, encoding="utf-8")
    page.screenshot(
        path=str(folder / (label + ".png")),
        mask=[page.locator('input[type="password"]')],
        timeout=15000,
    )
    return html


def navigate(page, url):
    ref = (
        page.url
        if page.url.startswith("http")
        else "https://" + urlparse(url).netloc + "/"
    )
    r = page.goto(url, referer=ref, wait_until="commit", timeout=45000)
    try:
        page.wait_for_load_state("domcontentloaded", timeout=20000)
    except Exception:
        # The response can render while a third-party script delays the event.
        # Subsequent DOM/content checks, not this timeout, decide acceptance.
        pass
    page.wait_for_timeout(5000)
    return r.status if r else None


def resolve_hold(page, notes, trace_dir=None):
    """Use the repository's existing local handler only on an observed challenge."""
    if not re.search(
        r"(?i)press.{0,8}hold|human verification|unusual activity|access to this page",
        page.title() + " " + page.locator("body").inner_text(),
    ):
        return
    from press_and_hold_lib import press_and_hold_adaptive

    for attempt in range(2):
        target = None
        for frame in page.frames:
            for locator in [
                frame.get_by_role("button", name=re.compile("Press.*Hold", re.I)),
                frame.get_by_text(re.compile("^Press.*Hold$", re.I)),
            ]:
                try:
                    if locator.count() and locator.first.is_visible():
                        target = locator.first.bounding_box()
                        break
                except Exception:
                    pass
            if target:
                break
        if not target:
            notes.append(
                "Challenge observed; no visible hold control could be localized."
            )
            break
        try:
            press_and_hold_adaptive(
                page,
                target["x"] + target["width"] / 2,
                target["y"] + target["height"] / 2,
                target,
                lambda message: notes.append(message),
                max_hold_s=12.0 if trace_dir else 8.0,
                trace_dir=(trace_dir / f"attempt-{attempt}") if trace_dir else None,
                release_on_pixel_peak=not bool(trace_dir),
            )
        finally:
            page.mouse.up()
        page.wait_for_timeout(5000)
        if not re.search(
            r"(?i)press.{0,8}hold|access to this page has been denied|unusual activity",
            page.locator("body").inner_text(),
        ):
            notes.append("Challenge no longer visible after hold.")
            break


def discovery(page, pub):
    if pub == "wsj":
        try:
            m = load_client(pub)
            state = json.loads(m.extract_balanced(page.content(), "window.__STATE__ ="))
            nodes = [
                v
                for k, v in state.get("data", {}).items()
                if k.startswith("quotes_latestNews_")
            ]
            articles = [
                a
                for n in nodes
                for a in n.get("data", {})
                .get("data", {})
                .get("news", {})
                .get("articles", [])
            ]
            return [
                {
                    "url": a["url"],
                    "title": a.get("headline", ""),
                    "provider": a.get("provider"),
                }
                for a in articles
                if a.get("provider") == "The Wall Street Journal"
                and article_url(pub, a.get("url", ""))
            ]
        except Exception:
            return []
    selector = ".o-teaser__heading a[href]" if pub == "ft" else "a[href]"
    anchors = page.locator(selector).evaluate_all(
        "(els)=>els.map(a=>({url:a.href,title:a.innerText}))"
    )
    links = []
    seen = set()
    for a in anchors:
        url = a["url"].split("?")[0].split("#")[0]
        if article_url(pub, url) and url not in seen:
            seen.add(url)
            links.append({"url": url, "title": a["title"]})
    return links


def extract(page, pub, ticker):
    html = page.content()
    soup = BeautifulSoup(html, "html.parser")
    for e in soup(
        ["script", "style", "noscript", "svg", "nav", "footer", "button", "form"]
    ):
        e.decompose()
    for e in soup.select(
        '.newsletter-signup,.n-content-recommended,.recommended,.event-promo,[data-component*="newsletter"],[data-component*="recommended"],[data-testid="byline"],[data-testid="utility-bar"]'
    ):
        e.decompose()
    title = soup.find("meta", property="og:title")
    title = (
        title.get("content", "")
        if title
        else (soup.title.get_text(" ", strip=True) if soup.title else "")
    )
    canonical = soup.find("link", rel="canonical")
    canonical = canonical.get("href") if canonical else page.url
    published = soup.find("meta", property="article:published_time")
    published = published.get("content") if published else None
    if not published:
        m = re.search(r'"datePublished"\s*:\s*"([^"<>]+)"', html)
        published = m.group(1) if m else None
    body = None
    selector = None
    for sel in SELECTORS[pub]:
        el = soup.select_one(sel)
        if el is not None and len(el.get_text(" ", strip=True)) > 100:
            body = el
            selector = sel
            break
    paragraphs = (
        [p.get_text(" ", strip=True) for p in body.find_all(["p", "h2", "h3", "li"])]
        if body
        else []
    )
    paragraphs = [p for p in paragraphs if p]
    text = "\n\n".join(paragraphs)
    visible = page.locator("body").inner_text(timeout=10000)
    barrier = bool(
        re.search(
            r"(?i)subscribe to (read|continue)|to continue reading|already a subscriber\?\s*sign in|unusual activity|press & hold|access to this page has been denied",
            visible,
        )
    )
    issues = []
    if not body:
        issues.append("no_scoped_article_body")
    if len(text.split()) < 120 or len(paragraphs) < 3:
        issues.append("insufficient_substantive_body")
    if barrier:
        issues.append("access_or_subscription_barrier")
    if re.search(r"\.css-|var\(--|function\s*\(|<[/A-Za-z]", text):
        issues.append("markup_or_code")
    if not published:
        issues.append("missing_publication_time")
    if not title or "subscribe to read" in title.lower():
        issues.append("missing_or_barrier_title")
    if not re.search(
        r"\b" + re.escape(COMPANY[ticker]) + r"\b", title + " " + text, re.I
    ):
        issues.append("no_company_mention")
    return {
        "url": canonical,
        "title": title,
        "published_at": published,
        "body_text": text,
        "paragraphs": paragraphs,
        "selector": selector,
        "content_status": "candidate" if not issues else "rejected",
        "issues": issues,
        "body_sha256": hashlib.sha256(text.encode()).hexdigest(),
        "words": len(text.split()),
        "fetched_at": now(),
        "visible_body_chars": len(visible),
    }


def sa_browser_news(page, ticker, folder):
    """Documented JSON news endpoint, fetched by the real headful browser session."""
    slug = ticker.lower()
    path = f"/api/v3/symbols/{slug}/news?filter[since]=0&filter[until]=0&id={slug}&include=author,primaryTickers,sentiments&page[size]=20"
    reply = page.evaluate(
        """async path => { const r=await fetch(path,{credentials:'include',headers:{Accept:'application/json'}}); return {status:r.status,body:await r.text()}; }""",
        path,
    )
    write(folder / "news-api-response.json", reply)
    if reply["status"] != 200:
        raise RuntimeError("Browser news API HTTP " + str(reply["status"]))
    data = json.loads(reply["body"])
    records = []
    for row in data.get("data", []):
        a = row.get("attributes", {})
        soup = BeautifulSoup(a.get("content", ""), "html.parser")
        for e in soup(["script", "style", "noscript", "figure"]):
            e.decompose()
        for e in soup.select("#more-links,.signup_widget_placeholder"):
            e.decompose()
        paragraphs = [
            e.get_text(" ", strip=True) for e in soup.find_all(["p", "li", "h2", "h3"])
        ]
        paragraphs = [p for p in paragraphs if p]
        text = "\n\n".join(paragraphs)
        url = row.get("links", {}).get("self", "")
        url = BASE["sa"] + url if url.startswith("/") else url
        issues = []
        if len(text.split()) < 120 or len(paragraphs) < 3:
            issues.append("insufficient_substantive_body")
        if not article_url("sa", url):
            issues.append("missing_canonical_article_url")
        if not a.get("publishOn"):
            issues.append("missing_publication_time")
        if re.search(
            r"\.css-|var\(--|<[/A-Za-z]|subscribe to (read|continue)", text, re.I
        ):
            issues.append("code_or_barrier")
        if not re.search(
            r"\b" + re.escape(COMPANY[ticker]) + r"\b",
            a.get("title", "") + " " + text,
            re.I,
        ):
            issues.append("no_company_mention")
        records.append(
            {
                "url": url,
                "title": a.get("title"),
                "published_at": a.get("publishOn"),
                "body_text": text,
                "paragraphs": paragraphs,
                "selector": "browser-fetch:news-api:data.attributes.content",
                "content_kind": "publisher_news",
                "content_status": "candidate" if not issues else "rejected",
                "issues": issues,
                "body_sha256": hashlib.sha256(text.encode()).hexdigest(),
                "words": len(text.split()),
                "fetched_at": now(),
                "article_id": row.get("id"),
            }
        )
    return records


def reconcile(state, out):
    """Only explicit agent reviews of the exact saved body can advance a streak."""
    reviews = (
        json.loads((out / "review.json").read_text())
        if (out / "review.json").exists()
        else {}
    )
    state["reviews"] = reviews
    state["streaks"] = {p: 0 for p in ORDER}
    state["joint_streak"] = 0
    state["qualifications"] = {}
    windows = {pub: [] for pub in ORDER}
    for row in state["rounds"]:
        for pub, r in row["results"].items():
            accepted = []
            for a in r["attempts"]:
                review = reviews.get(a.get("review_key"), {})
                if (
                    a.get("content_status") != "candidate"
                    or not review.get("complete")
                    or not review.get("relevant")
                    or review.get("body_sha256") != a.get("body_sha256")
                ):
                    continue
                if any(
                    x["url"] == a["url"] or x["body_sha256"] == a["body_sha256"]
                    for x in accepted
                ):
                    continue
                accepted.append(a)
                if len(accepted) == 5:
                    break
            r["accepted"] = accepted
            r["passed"] = len(accepted) == 5
            state["streaks"][pub] = state["streaks"][pub] + 1 if r["passed"] else 0
            windows[pub] = (
                (windows[pub] + [{"round": row["round"], "ticker": row["ticker"]}])[-3:]
                if r["passed"]
                else []
            )
            if len(windows[pub]) == 3 and len({w["ticker"] for w in windows[pub]}) == 3:
                state["qualifications"][pub] = list(windows[pub])
            write(
                out / f"round-{row['round']:03d}-{row['ticker']}" / pub / "result.json",
                r,
            )
        state["joint_streak"] = (
            state["joint_streak"] + 1
            if all(r["passed"] for r in row["results"].values())
            else 0
        )
    state["target_measured"] = all(pub in state["qualifications"] for pub in ORDER)
    return state


def run_publisher(pw, args, state, pub, ticker, round_number):
    folder = args.out / f"round-{round_number:03d}-{ticker}" / pub
    folder.mkdir(parents=True, exist_ok=True)
    result = {
        "publisher": pub,
        "ticker": ticker,
        "round": round_number,
        "revision": REVISION,
        "script_sha256": SOURCE_SHA256,
        "started_at": now(),
        "accepted": [],
        "attempts": [],
        "notes": [],
    }
    launch = {
        "channel": "chrome",
        "headless": False,
        "args": ["--no-first-run", "--disable-blink-features=AutomationControlled"],
    }
    if args.proxy and pub in ["sa", "bbg"]:
        px = json.loads(load_client(pub)._secret("astn/brightdata/residential-proxy"))
        launch["proxy"] = {
            "server": f"http://{px['host']}:{px['port']}",
            "username": px["username"]
            + "-country-"
            + px.get("country", "us")
            + "-session-harvest"
            + pub,
            "password": px["password"],
        }
        result["egress"] = "existing_residential_proxy"
    else:
        result["egress"] = "native"
    browser = pw.chromium.launch(**launch)
    state_path = args.out / "sessions" / (pub + ".json")
    if pub == "sa" and args.refresh_sa:
        auth_dir = folder / "session-refresh"
        auth_dir.mkdir(exist_ok=True)
        original = SCRIPTS / "sa_harvest_session.py"
        copied = auth_dir / original.name
        copied.write_bytes(original.read_bytes())
        driver = auth_dir / "run.py"
        driver.write_text(
            "import runpy, sys\n"
            + "sys.path.insert(0, "
            + repr(str(SCRIPTS))
            + ")\n"
            + "sys.argv = ["
            + repr(str(copied))
            + ", '--max-steps', '10']\n"
            + "runpy.run_path("
            + repr(str(copied))
            + ", run_name='__main__')\n",
            encoding="utf-8",
        )
        with (auth_dir / "run.log").open("w", encoding="utf-8") as log:
            proc = subprocess.run([sys.executable, str(driver)], stdout=log, stderr=log)
        result["session_refresh"] = {
            "exit_code": proc.returncode,
            "source_sha256": hashlib.sha256(original.read_bytes()).hexdigest(),
            "cloud_park": False,
        }
        bundles = sorted(auth_dir.glob("sa_session_*.json"))
        if proc.returncode == 0 and bundles:
            bundle = json.loads(bundles[-1].read_text())
            write(state_path, {"cookies": bundle["all_cookies"], "origins": []})
            result["notes"].append("Fresh local SA session used; no cloud parking.")
    opts = {
        "viewport": {"width": 1366, "height": 900},
        "locale": "en-US",
        "timezone_id": "America/New_York",
        "ignore_https_errors": bool(args.proxy and pub in ["sa", "bbg"]),
    }
    if state_path.exists():
        opts["storage_state"] = str(state_path)
    context = browser.new_context(**opts)
    context.add_init_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined});"
    )
    if not state_path.exists():
        seed(context, pub)
    page = context.new_page()
    page.set_default_timeout(15000)
    result["request_failures"] = []
    page.on(
        "requestfailed",
        lambda request: result["request_failures"].append(
            {
                "host": urlparse(request.url).hostname,
                "resource_type": request.resource_type,
                "failure": request.failure,
            }
        ),
    )
    try:
        status = navigate(
            page,
            listing_url(pub, ticker, "NSQ" if ticker in ["COST", "INTU"] else "NYQ"),
        )
        resolve_hold(
            page, result["notes"], folder / "hold-listing" if args.trace_hold else None
        )
        if (
            pub == "bbg"
            and "unusual activity" not in page.locator("body").inner_text().lower()
        ):
            status = navigate(
                page, BASE[pub] + "/search?query=" + COMPANY[ticker].replace(" ", "%20")
            )
            resolve_hold(
                page,
                result["notes"],
                folder / "hold-search" if args.trace_hold else None,
            )
        result["listing_http"] = status
        result["listing_title"] = page.title()
        snapshot(page, folder, "listing")
        api_records = sa_browser_news(page, ticker, folder) if pub == "sa" else None
        links = (
            [{"url": r["url"], "title": r["title"]} for r in api_records]
            if api_records is not None
            else discovery(page, pub)
        )
        if pub == "ft":
            try:
                # GET form action/name observed in the company page's own search form.
                navigate(
                    page, BASE[pub] + "/search?q=" + COMPANY[ticker].replace(" ", "%20")
                )
                snapshot(page, folder, "search")
                extra = discovery(page, pub)
                seen = {a["url"] for a in links}
                links.extend(a for a in extra if a["url"] not in seen)
                result["notes"].append(
                    f"Company-page links supplemented by {len(extra)} browser search links."
                )
            except Exception as exc:
                result["notes"].append("FT search supplement: " + type(exc).__name__)
        if pub == "wsj" and not links:
            for retry in range(2):
                page.mouse.wheel(0, 1800)
                page.wait_for_timeout(5000)
                if retry:
                    page.reload(wait_until="domcontentloaded", timeout=45000)
                    page.wait_for_timeout(5000)
                links = discovery(page, pub)
                snapshot(page, folder, f"listing-retry-{retry}")
                if links:
                    break
            result["notes"].append(
                f"Ticker news after hydration retries: {len(links)} links."
            )
            if not links and args.discovery_fallback:
                m = load_client(pub)
                fallback = m.extract_ticker_news(ticker)
                write(folder / "legacy-news-discovery.json", fallback)
                articles = (
                    fallback.get("news_node", {})
                    .get("data", {})
                    .get("data", {})
                    .get("news", {})
                    .get("articles", [])
                )
                articles.sort(key=lambda a: bool(a.get("subscriber")))
                links = [
                    {
                        "url": a["url"],
                        "title": a.get("headline", ""),
                        "provider": a.get("provider"),
                    }
                    for a in articles
                    if a.get("provider") == "The Wall Street Journal"
                    and article_url(pub, a.get("url", ""))
                ]
                result["notes"].append(
                    f"Existing Unlocker client supplied {len(links)} ticker-linked WSJ URLs; article fetch remains headful browser."
                )
        if pub == "wsj" and args.search_wsj:
            try:
                navigate(
                    page,
                    BASE[pub] + "/search?query=" + COMPANY[ticker].replace(" ", "%20"),
                )
                page.wait_for_timeout(5000)
                snapshot(page, folder, "search")
                anchors = page.locator("a[href]").evaluate_all(
                    "els => els.map(a => ({url:a.href,title:a.innerText}))"
                )
                seen = {a["url"] for a in links}
                extra = []
                for a in anchors:
                    url = a["url"].split("?")[0].split("#")[0]
                    if (
                        article_url(pub, url)
                        and url not in seen
                        and re.search(
                            r"\b" + re.escape(COMPANY[ticker]) + r"\b", a["title"], re.I
                        )
                    ):
                        seen.add(url)
                        extra.append(
                            {
                                "url": url,
                                "title": a["title"],
                                "provenance": "headful_company_search",
                            }
                        )
                links.extend(extra)
                result["notes"].append(
                    f"Headful WSJ search supplied {len(extra)} additional company-headline URLs."
                )
            except Exception as exc:
                result["notes"].append(
                    "WSJ browser search supplement: " + type(exc).__name__
                )
        result["discovered_links"] = links
        if pub == "ft":
            links.sort(
                key=lambda a: (
                    not bool(
                        re.search(
                            r"\b" + re.escape(COMPANY[ticker]) + r"\b",
                            a.get("title", ""),
                            re.I,
                        )
                    )
                )
            )
        if not links:
            result["notes"].append(
                "No article links discovered; inspect listing screenshot/HTML and choose next-round strategy."
            )
        for ix, link in enumerate(links[: args.candidates]):
            review_path = args.out / "review.json"
            if review_path.exists():
                state["reviews"] = json.loads(review_path.read_text())
            result["accepted"] = []
            for prior in result["attempts"]:
                review = state.get("reviews", {}).get(prior.get("review_key"), {})
                if (
                    prior.get("content_status") == "candidate"
                    and review.get("complete")
                    and review.get("relevant")
                    and review.get("body_sha256") == prior.get("body_sha256")
                    and not any(
                        a["url"] == prior["url"]
                        or a["body_sha256"] == prior["body_sha256"]
                        for a in result["accepted"]
                    )
                ):
                    result["accepted"].append(prior)
            if len(result["accepted"]) >= 5:
                break
            item = {"requested_url": link["url"], "listing_title": link["title"]}
            try:
                if api_records is not None:
                    record = api_records[ix]
                    item["http"] = 200
                else:
                    item["http"] = navigate(page, link["url"])
                    resolve_hold(
                        page,
                        result["notes"],
                        folder / f"hold-article-{ix:02d}" if args.trace_hold else None,
                    )
                    snapshot(page, folder, f"article-{ix:02d}")
                    record = extract(page, pub, ticker)
                write(folder / f"article-{ix:02d}.json", record)
                item.update(
                    {
                        k: record[k]
                        for k in [
                            "url",
                            "title",
                            "published_at",
                            "selector",
                            "content_status",
                            "issues",
                            "body_sha256",
                            "words",
                        ]
                    }
                )
                # Candidate means structural checks passed. Agent content/relevance review is
                # required in review.json before an article advances the reliability streak.
                item["review_key"] = (
                    f"round-{round_number:03d}-{ticker}/{pub}/article-{ix:02d}.json"
                )
                review = state.get("reviews", {}).get(item["review_key"], {})
                if (
                    record["content_status"] == "candidate"
                    and review.get("complete")
                    and review.get("relevant")
                    and review.get("body_sha256") == item["body_sha256"]
                    and not any(
                        x["url"] == item["url"]
                        or x["body_sha256"] == item["body_sha256"]
                        for x in result["accepted"]
                    )
                ):
                    result["accepted"].append(item)
            except Exception as exc:
                item.update(error_type=type(exc).__name__)
            result["attempts"].append(item)
            write(folder / "result.json", result)
            print(
                json.dumps(
                    {
                        "event": "article",
                        "round": round_number,
                        "publisher": pub,
                        "ticker": ticker,
                        "index": ix,
                        **{
                            k: item.get(k)
                            for k in ["content_status", "issues", "words", "error_type"]
                        },
                    }
                ),
                flush=True,
            )
            if len(result["attempts"]) >= 3 and all(
                "access_or_subscription_barrier" in a.get("issues", [])
                and not a.get("words")
                for a in result["attempts"][-3:]
            ):
                result["notes"].append(
                    "Three consecutive blocked bodies; defer this strategy to next round."
                )
                break
        state_path.parent.mkdir(parents=True, exist_ok=True)
        context.storage_state(path=str(state_path))
    except Exception as exc:
        result["notes"].append("Publisher operation failed: " + type(exc).__name__)
        try:
            snapshot(page, folder, "failure-page")
            result["failure_page_title"] = page.title()
        except Exception:
            pass
        status = re.search(r"HTTP (\d{3})", str(exc))
        if status:
            result["error_http"] = int(status.group(1))
    finally:
        state_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            context.storage_state(path=str(state_path))
        finally:
            browser.close()
    result["finished_at"] = now()
    result["passed"] = len(result["accepted"]) == 5
    write(folder / "result.json", result)
    print(
        json.dumps(
            {
                "event": "publisher_finished",
                "round": round_number,
                "publisher": pub,
                "ticker": ticker,
                "links": len(result.get("discovered_links", [])),
                "candidates": sum(
                    a.get("content_status") == "candidate" for a in result["attempts"]
                ),
                "accepted": len(result["accepted"]),
                "notes": result["notes"],
            }
        ),
        flush=True,
    )
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--out",
        type=pathlib.Path,
        default=ROOT / ".runtime/codex-seats/4.0.0_SA_CRO~W/harvest-iteration",
    )
    ap.add_argument(
        "--tickers",
        nargs="+",
        default=["BA", "COST", "HD", "INTU", "VLO", "HAL", "KMB"],
    )
    ap.add_argument("--rounds", type=int, default=1)
    ap.add_argument("--candidates", type=int, default=10)
    ap.add_argument("--review-only", action="store_true")
    ap.add_argument("--proxy", action="store_true")
    ap.add_argument("--discovery-fallback", action="store_true")
    ap.add_argument("--refresh-sa", action="store_true")
    ap.add_argument("--trace-hold", action="store_true")
    ap.add_argument("--search-wsj", action="store_true")
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    revision_dir = args.out / "revisions"
    revision_dir.mkdir(exist_ok=True)
    (revision_dir / (SOURCE_SHA256 + ".py")).write_bytes(SOURCE_BYTES)
    sp = args.out / "state.json"
    state = (
        json.loads(sp.read_text())
        if sp.exists()
        else {
            "rounds": [],
            "streaks": {p: 0 for p in ORDER},
            "joint_streak": 0,
            "reviews": {},
        }
    )
    if (args.out / "review.json").exists():
        state["reviews"] = json.loads((args.out / "review.json").read_text())
    if args.review_only:
        reconcile(state, args.out)
        write(sp, state)
        print(
            json.dumps(
                {
                    "streaks": state["streaks"],
                    "joint_streak": state["joint_streak"],
                    "target_measured": state["target_measured"],
                }
            )
        )
        return
    with sync_playwright() as pw:
        for _ in range(args.rounds):
            n = len(state["rounds"]) + 1
            ticker = args.tickers[(n - 1) % len(args.tickers)]
            if state["rounds"] and ticker == state["rounds"][-1]["ticker"]:
                raise ValueError("Consecutive rounds require different tickers")
            row = {"round": n, "ticker": ticker, "results": {}}
            for pub in ORDER:
                row["results"][pub] = run_publisher(pw, args, state, pub, ticker, n)
                state["streaks"][pub] = (
                    state["streaks"][pub] + 1 if row["results"][pub]["passed"] else 0
                )
                write(args.out / "in-progress.json", row)
            state["joint_streak"] = (
                state["joint_streak"] + 1
                if all(r["passed"] for r in row["results"].values())
                else 0
            )
            state["rounds"].append(row)
            reconcile(state, args.out)
            write(sp, state)
            if state["target_measured"]:
                print(
                    "TARGET_MEASURED: three consecutive tickers, five reviewed distinct articles per publisher",
                    flush=True,
                )
                break
    print(
        json.dumps(
            {"streaks": state["streaks"], "joint_streak": state["joint_streak"]}
        ),
        flush=True,
    )


if __name__ == "__main__":
    raise SystemExit(
        "Retired browser-content experiment. Use harvest_rest_loop.py for the "
        "canonical session-harvester -> HTTP-consumer workflow. Existing experimental "
        "artifacts remain available for audit and do not qualify REST reliability."
    )
