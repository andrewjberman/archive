"""Local canonical session-harvester -> HTTP-consumer iteration.

Run a round, inspect the saved responses and notes, add exact-hash reviews, then
run the next round. No browser article extraction and no cloud session writes.
"""

import argparse
import datetime as dt
import hashlib
import importlib
import json
from pathlib import Path
import re
import time
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup
from harvest_local_session import harvest

ROOT = Path(__file__).resolve().parents[4]
SCRIPTS = Path(__file__).resolve().parent
ORDER = ("sa", "ft", "wsj", "bbg")
COMPANY = {
    "BA": "Boeing",
    "COST": "Costco",
    "HD": "Home Depot",
    "INTU": "Intuit",
    "VLO": "Valero",
    "HAL": "Halliburton",
    "KMB": "Kimberly-Clark",
}
METHOD = "canonical-harvest-rest-v1"


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)


def read(path, default):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default


def client(pub):
    return importlib.import_module(({"bbg": "bloomberg"}.get(pub, pub)) + "_rest_fetch")


def session(pub, args, folder):
    m = client(pub)
    cache = args.out / "sessions" / (pub + ".json")
    saved = read(cache, None)
    if saved is None:
        bundle = harvest(pub, folder / "auth", args.max_steps, args.trace_hold)
        saved = {
            "bundle": bundle,
            "auth_evidence": read(folder / "auth/auth-evidence.json", {}),
        }
        write(cache, saved)
    evidence = saved["auth_evidence"]
    if not evidence.get("network_auth_corroborated"):
        raise ValueError(
            "Uncorroborated session cannot enter the canonical reliability test"
        )
    write(folder / "auth-source.json", evidence)
    s = m.build_session(bundle=saved["bundle"])
    return s[0] if pub == "sa" else s


def clean_sa(record):
    a = record.get("attributes") or {}
    soup = BeautifulSoup(a.get("content") or "", "html.parser")
    for node in soup.select(
        "script, style, noscript, #more-links, .signup_widget_placeholder"
    ):
        node.decompose()
    blocks = [
        n.get_text(" ", strip=True)
        for n in soup.select("p, li, h2, h3, blockquote, table")
        if not n.find_parent(["li", "blockquote", "table"])
    ]
    text = "\n\n".join(x for x in blocks if x)
    return {
        "url": urljoin(
            "https://seekingalpha.com", record.get("links", {}).get("self", "")
        ),
        "title": a.get("title"),
        "published": a.get("publishOn") or a.get("published_on"),
        "text": text,
        "body_source": "sa_rest_fetch.news.attributes.content",
    }


def assess(record, ticker):
    text = record.get("text") or ""
    title = record.get("title") or ""
    issues = []
    if record.get("completeness") in ("partial_body", "missing_body"):
        issues.append(record["completeness"])
    if len(text.split()) < 120 or len(text.split("\n\n")) < 3:
        issues.append("short_or_partial_body")
    if not title or not record.get("published"):
        issues.append("missing_metadata")
    if COMPANY[ticker].casefold() not in (title + " " + text).casefold():
        issues.append("company_not_mentioned")
    if re.search(r"<[/A-Za-z][^>]*>|@media|function\s*\(|__NEXT_DATA__", text):
        issues.append("markup_or_code")
    if "earnings call insights" in title.lower():
        issues.append("generated_summary")
    record.update(
        body_sha256=hashlib.sha256(text.encode()).hexdigest(),
        words=len(text.split()),
        issues=issues,
        content_status="candidate" if not issues else "rejected",
    )
    return record


def collect(pub, ticker, args, folder, result):
    m = client(pub)
    s = None
    try:
        if pub != "wsj":
            s = session(pub, args, folder)
        result["transport"] = {
            "sa": "curl_cffi_residential_proxy",
            "ft": "curl_cffi_residential_proxy",
            "wsj": "brightdata_web_unlocker_one_shotter",
            "bbg": "curl_cffi_native",
        }[pub]
        if pub == "sa":
            account = m.check(s)
            result["rest_authorized"] = bool(account.get("authorized"))
            if not result["rest_authorized"]:
                raise m.NotAuthorized(
                    "Freshly harvested session did not authorize REST account check"
                )
            payload = m.news(s, ticker, limit=args.candidates)
            write(folder / "news-response.json", payload)
            records = [clean_sa(r) for r in payload.get("data", [])]
            for record in records:
                yield record
        elif pub == "ft":
            exchange = "NSQ" if ticker in ("COST", "INTU") else "NYQ"
            url = f"https://markets.ft.com/data/equities/tearsheet/summary?s={ticker}:{exchange}"
            html = m.get_html(s, url, m.BASE)
            (folder / "discovery-response.html").write_text(html, encoding="utf-8")
            soup = BeautifulSoup(html, "html.parser")
            urls = []
            for a in soup.select(".o-teaser__heading a[href]"):
                link = urljoin(url, a["href"]).split("?")[0]
                if (
                    urlparse(link).hostname == "www.ft.com"
                    and re.fullmatch(r"/content/[0-9a-f-]{36}", urlparse(link).path)
                    and link not in urls
                ):
                    urls.append(link)
            result["discovered_urls"] = urls
            for ix, link in enumerate(urls[: args.candidates]):
                yield m.article(
                    s,
                    link.rsplit("/", 1)[-1],
                    response_path=folder / f"response-{ix:02d}.html",
                )
                time.sleep(m.PACE_SECONDS)
        elif pub == "wsj":
            payload = m.extract_ticker_news(ticker)
            write(folder / "discovery-response.json", payload)
            if not payload.get("found_on_attempt"):
                raise ValueError(
                    "Ticker feed absent from Unlocker snapshot; coverage unmeasured"
                )
            articles = payload["news_node"]["data"]["data"]["news"]["articles"]
            urls = list(
                dict.fromkeys(
                    a["url"]
                    for a in articles
                    if urlparse(a.get("url", "")).hostname == "www.wsj.com"
                )
            )
            result["discovered_urls"] = urls
            for ix, link in enumerate(urls[: args.candidates]):
                try:
                    yield m.article(
                        link, response_path=folder / f"response-{ix:02d}.html"
                    )
                except Exception as exc:
                    status = re.search(r"-> (\d{3})", str(exc))
                    yield {
                        "url": link,
                        "title": None,
                        "text": "",
                        "published": None,
                        "error_type": type(exc).__name__,
                        "http_status": int(status[1]) if status else None,
                    }
                time.sleep(m.PACE_SECONDS)
        else:
            response = m.ticker(s, ticker + ":US")
            result["ticker_http_status"] = response.status_code
            write(
                folder / "endpoint-gap.json",
                {
                    "ticker_status": response.status_code,
                    "article_body_api": "not_implemented_in_canonical_consumer",
                    "news_params": "full_observed_request_not_yet_captured",
                    "next_step": "Capture authenticated browser network request, then implement HTTP replay.",
                },
            )
            result["notes"].append(
                "Canonical Bloomberg client has no article-body API; no browser-content fallback."
            )
    finally:
        if s is not None:
            s.close()


def reconcile(state, out):
    reviews = read(out / "review.json", {})
    windows = {pub: [] for pub in ORDER}
    qualified = {}
    for row in state["rounds"]:
        for pub in ORDER:
            result = row["results"].get(pub, {})
            accepted = []
            for a in result.get("attempts", []):
                review = reviews.get(a["review_key"], {})
                # Re-read saved bytes: a stale recorded hash cannot authorize a changed body.
                record = read(out / a["review_key"], {})
                digest = hashlib.sha256(record.get("text", "").encode()).hexdigest()
                if (
                    a.get("content_status") == "candidate"
                    and review.get("complete")
                    and review.get("relevant")
                    and digest == a.get("body_sha256") == review.get("body_sha256")
                    and not any(
                        x["url"] == a["url"] or x["body_sha256"] == digest
                        for x in accepted
                    )
                ):
                    accepted.append(a)
            result["accepted"] = accepted[:5]
            result["passed"] = len(accepted) >= 5
            windows[pub] = (
                (windows[pub] + [row["ticker"]])[-3:] if result["passed"] else []
            )
            if len(windows[pub]) == 3 and len(set(windows[pub])) == 3:
                qualified[pub] = list(windows[pub])
            if result:
                write(
                    out
                    / f"round-{row['round']:03d}-{row['ticker']}"
                    / pub
                    / "result.json",
                    result,
                )
    state["qualifications"] = qualified
    state["target_measured"] = all(pub in qualified for pub in ORDER)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out",
        type=Path,
        default=ROOT / ".runtime/codex-seats/4.0.0_SA_CRO~W/harvest-rest-iteration",
    )
    parser.add_argument("--tickers", nargs="+", choices=COMPANY, default=list(COMPANY))
    parser.add_argument("--rounds", type=int, default=1)
    parser.add_argument("--candidates", type=int, default=20)
    parser.add_argument("--max-steps", type=int, default=10)
    parser.add_argument("--trace-hold", action="store_true")
    parser.add_argument("--review-only", action="store_true")
    args = parser.parse_args()
    args.out = args.out.resolve()
    args.out.mkdir(parents=True, exist_ok=True)
    path = args.out / "state.json"
    state = read(path, {"method": METHOD, "rounds": []})
    if state.get("method") != METHOD:
        raise ValueError("Output directory belongs to a different collection method")
    if args.review_only:
        reconcile(state, args.out)
        write(path, state)
        print(json.dumps({k: state[k] for k in ("qualifications", "target_measured")}))
        return
    for _ in range(args.rounds):
        if state["rounds"] and not state["rounds"][-1].get("finished"):
            row = state["rounds"][-1]
        else:
            n = len(state["rounds"]) + 1
            ticker = args.tickers[(n - 1) % len(args.tickers)]
            if state["rounds"] and ticker == state["rounds"][-1]["ticker"]:
                raise ValueError("Next round requires a different ticker")
            row = {"round": n, "ticker": ticker, "results": {}}
            state["rounds"].append(row)
        for pub in ORDER:
            if pub in row["results"]:
                continue
            folder = args.out / f"round-{row['round']:03d}-{row['ticker']}" / pub
            folder.mkdir(parents=True, exist_ok=True)
            result = {
                "method": METHOD,
                "attempts": [],
                "notes": [],
                "started_at": dt.datetime.now(dt.timezone.utc).isoformat(),
                "client_sha256": hashlib.sha256(
                    Path(client(pub).__file__).read_bytes()
                ).hexdigest(),
            }
            print(
                json.dumps(
                    {
                        "event": "publisher_start",
                        "publisher": pub,
                        "ticker": row["ticker"],
                    }
                ),
                flush=True,
            )
            try:
                for ix, record in enumerate(
                    collect(pub, row["ticker"], args, folder, result)
                ):
                    record = assess(record, row["ticker"])
                    target = folder / f"article-{ix:02d}.json"
                    write(target, record)
                    result["attempts"].append(
                        {
                            k: record[k]
                            for k in (
                                "url",
                                "title",
                                "body_sha256",
                                "words",
                                "issues",
                                "content_status",
                            )
                        }
                    )
                    result["attempts"][-1]["review_key"] = target.relative_to(
                        args.out
                    ).as_posix()
                    write(folder / "result.json", result)
            except Exception as exc:
                result["error_type"] = type(exc).__name__
                status = re.search(r"-> (\d{3})", str(exc))
                if status:
                    result["http_status"] = int(status[1])
                # Never echo provider exception bodies or account responses.
                if type(exc).__name__ in ("ReHarvestRequired", "NotAuthorized"):
                    cache = args.out / "sessions" / (pub + ".json")
                    if cache.exists():
                        archive = folder / "failed-session.json"
                        archive.write_bytes(cache.read_bytes())
                        cache.unlink()
                    result["notes"].append(
                        "Next publisher round must run the canonical session harvester again."
                    )
            row["results"][pub] = result
            write(folder / "result.json", result)
            write(path, state)
            print(
                json.dumps(
                    {
                        "event": "publisher_finished",
                        "publisher": pub,
                        "candidates": sum(
                            a["content_status"] == "candidate"
                            for a in result["attempts"]
                        ),
                        "error_type": result.get("error_type"),
                        "notes": result["notes"],
                    }
                ),
                flush=True,
            )
        row["finished"] = True
        reconcile(state, args.out)
        write(path, state)
        if state["target_measured"]:
            break


if __name__ == "__main__":
    main()
