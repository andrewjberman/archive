#!/usr/bin/env python3
"""Financial Times REST consumer -- rides the PARKED session (astn/ft/session), never logs in
inline. Standing reference for AMGT_RESAPP, mirroring sa_rest_fetch.py's shape and ROE exactly.

MEASURED CONTRACT (4.0.0_SA_CRO~Z, 2026-09-10):
  1. FT's article pages are server-rendered HTML -- unlike Seeking Alpha, there is no separate
     JSON API discovery needed. A plain authenticated GET of an article URL returns the FULL
     paywalled body in the raw HTML (measured: 36,237 chars of visible article text, no paywall
     marker, both through the residential proxy and on native IP).
  2. GET only. The residential zone refuses every POST (policy_20130 -- the same Bright Data
     account-level restriction measured on Seeking Alpha); a login can never complete through it,
     which is why the harvest step (ft_harvest_session.py) runs on NATIVE IP and only the READS
     ride the proxy here.
  3. Per-security pages exist beyond news: markets.ft.com's equity tearsheet, keyed by
     `{TICKER}:{EXCHANGE}` (e.g. RTX:NYQ) --
         https://markets.ft.com/data/equities/tearsheet/summary?s={TICKER}:{EXCHANGE}
         https://markets.ft.com/data/equities/tearsheet/profile?s={TICKER}:{EXCHANGE}
     both load fine over plain REST with the same session. No working `/tearsheet/news?s=...`
     endpoint was found -- every URL shape tried for it returned an FT-side error page. This is a
     NOT-FOUND, not a proof it doesn't exist; a later cell with the vendor word can hunt further.
  4. ft.com's own /search endpoint is REFUSED at the proxy (a policy-shaped block), not merely
     empty -- do not treat a 402 there as "no results", it is a transport-level refusal.

ROE (inherited unchanged): observe-act-only; a credential, cookie or session VALUE is never
logged or printed. The only artifacts written are the fetched payloads the caller asks for.

C-VENDOR-EGRESS: an external vendor call needs Andrew's explicit per-use word. The 2026-09-10
word covered that day's investigation. A SCHEDULED consumer built on this module needs its own.

Usage:
  python ft_rest_fetch.py listing companies markets global-economy   # article links per section
  python ft_rest_fetch.py article <content-id>                       # one article, full body
  python ft_rest_fetch.py quote RTX NYQ                              # markets.ft.com tearsheet summary+profile
  python ft_rest_fetch.py check                                      # is the parked session still authenticated
Options:  --out <dir>   write each payload as JSON      --no-proxy   egress natively (works too for FT reads)
Env:      SA_SECRETS_DIR=<dir>  read secret_*.json from disk instead of Secrets Manager (dev only)
"""
import html as htmlmod
import json
import os
import random
import re
import sys
import time

BASE = "https://www.ft.com"
MARKETS_BASE = "https://markets.ft.com"
SESSION_SECRET_ID = "astn/ft/session"
PROXY_SECRET_ID = "astn/brightdata/residential-proxy"
IDENTITY_COOKIES = ("FTSession", "FTSession_s")
DROP_COOKIES = {"__cf_bm", "_cfuvid"}
PACE_SECONDS = 1.5

LISTING_URLS = {
    "home": "https://www.ft.com",
    "markets": "https://www.ft.com/markets",
    "companies": "https://www.ft.com/companies",
    "global-economy": "https://www.ft.com/global-economy",
}


class ReHarvestRequired(RuntimeError):
    """The parked session no longer authenticates -- re-run ft_harvest_session.py --park."""


class NotAuthorized(RuntimeError):
    """The parked bundle carries no FT identity cookie at all."""


def _secret(name):
    d = os.environ.get("SA_SECRETS_DIR")
    if d:
        with open(os.path.join(d, "secret_" + name.replace("/", "_") + ".json"), encoding="utf-8") as fh:
            return fh.read().strip()
    import boto3
    return boto3.client("secretsmanager", region_name="us-east-1").get_secret_value(SecretId=name)["SecretString"]


def strip_html(t):
    return re.sub(r"\s+", " ", re.sub("<[^>]+>", " ", htmlmod.unescape(t or ""))).strip()


def build_session(use_proxy=True):
    from curl_cffi import requests as cr
    bundle = json.loads(_secret(SESSION_SECRET_ID))
    names = set(bundle.keys())
    if not any(n in names for n in IDENTITY_COOKIES):
        raise NotAuthorized("parked bundle carries no FTSession/FTSession_s cookie -- it was not harvested logged-in")
    # Bright Data's proxy SSL-bumps traffic; curl_cffi's default strict cert verification rejects
    # that outright (measured live, same failure sa_rest_fetch.py carried uncaught until today).
    kwargs = {"impersonate": "chrome", "timeout": 70, "verify": False}
    if use_proxy:
        px = json.loads(_secret(PROXY_SECRET_ID))
        sid = f"ft{random.randint(100000, 999999)}"
        user = f"{px['username']}-country-{px.get('country', 'us')}-session-{sid}"
        url = f"http://{user}:{px['password']}@{px['host']}:{px['port']}"
        kwargs["proxies"] = {"http": url, "https": url}
    s = cr.Session(**kwargs)
    for name, value in bundle.items():
        if name in DROP_COOKIES:
            continue
        try:
            s.cookies.set(name, value, domain=".ft.com", path="/")
        except Exception:
            pass
    s.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    })
    return s


def get_html(s, url, referer):
    r = s.get(url, headers={"Referer": referer})
    if r.status_code == 402 and "Residential Failed" in (r.text or ""):
        raise RuntimeError(f"GET {url} -> 402, proxy policy refusal (POST-only class or an unlisted path), not a content answer")
    if "accounts.ft.com/login" in (r.url or ""):
        raise ReHarvestRequired(f"GET {url} redirected to the login host -- the parked session has died")
    if r.status_code != 200:
        raise RuntimeError(f"GET {url} -> {r.status_code} ({len(r.text or '')} bytes)")
    return r.text


def listing(s, section):
    url = LISTING_URLS.get(section, section if section.startswith("http") else BASE + "/" + section.lstrip("/"))
    html = get_html(s, url, BASE)
    links = sorted(set(re.findall(r'href="(/content/[0-9a-f-]{36})"', html)))
    return {"section": section, "url": url, "article_ids": [u.split("/")[-1] for u in links]}


def article(s, content_id):
    url = f"{BASE}/content/{content_id}"
    html = get_html(s, url, BASE + "/companies")
    title_m = re.search(r"<title[^>]*>(.*?)</title>", html, re.S | re.I)
    body_m = re.search(r'data-component="article-body"[^>]*>(.*?)</div>\s*</div>', html, re.S)
    text = strip_html(body_m.group(1)) if body_m else strip_html(html)
    pub_m = re.search(r'"datePublished"\s*:\s*"([^"]+)"', html)
    return {"content_id": content_id, "url": url, "title": (title_m.group(1).strip() if title_m else None),
            "published": (pub_m.group(1) if pub_m else None), "text_chars": len(text), "text": text}


def quote(s, ticker, exchange):
    """markets.ft.com equity tearsheet -- MEASURED working over plain REST for summary + profile;
    the news-tab URL shape is NOT FOUND (every guess returned an FT-side error page)."""
    key = f"{ticker.upper()}:{exchange.upper()}"
    out = {"ticker": ticker.upper(), "exchange": exchange.upper(), "key": key}
    for tab in ("summary", "profile"):
        url = f"{MARKETS_BASE}/data/equities/tearsheet/{tab}?s={key}"
        html = get_html(s, url, BASE)
        title_m = re.search(r"<title[^>]*>(.*?)</title>", html, re.S | re.I)
        out[tab] = {"url": url, "title": (title_m.group(1).strip() if title_m else None), "bytes": len(html)}
    out["news_tab"] = "NOT FOUND at this cut -- every /tearsheet/news?s=... shape tried returned an FT-side error page; not proven absent"
    return out


def check(s):
    """Is the parked session still authenticated? A listing fetch that stays off the login host is the oracle."""
    listing(s, "companies")  # raises ReHarvestRequired if redirected to login
    return {"authorized": True}


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    verb = argv[1]
    args = [a for a in argv[2:] if not a.startswith("--")]
    out = argv[argv.index("--out") + 1] if "--out" in argv else None
    s = build_session(use_proxy="--no-proxy" not in argv)
    print("OK: parked session loaded, egress=%s" % ("native" if "--no-proxy" in argv else "residential-proxy"))
    results = {}
    try:
        if verb == "check":
            results["check"] = check(s)
            print("OK: authorized")
        elif verb == "listing":
            for sec in args:
                r = listing(s, sec)
                results[sec] = r
                print(f"OK: {sec:<16} article ids: {len(r['article_ids'])}")
                time.sleep(PACE_SECONDS)
        elif verb == "article":
            for cid in args:
                r = article(s, cid)
                results[cid] = r
                print(f"OK: {cid} title={r['title']!r} published={r['published']} text_chars={r['text_chars']}")
                time.sleep(PACE_SECONDS)
        elif verb == "quote":
            ticker, exchange = args[0], args[1] if len(args) > 1 else "NYQ"
            r = quote(s, ticker, exchange)
            results[r["key"]] = r
            print(f"OK: {r['key']} summary_bytes={r['summary']['bytes']} profile_bytes={r['profile']['bytes']} news_tab={r['news_tab'][:40]}...")
        else:
            print("ERROR: unknown verb %r" % verb)
            return 2
    except ReHarvestRequired as e:
        print("BLOCKED: %s" % e)
        return 3
    except NotAuthorized as e:
        print("ERROR: not authorized: %s" % e)
        return 4
    if out:
        os.makedirs(out, exist_ok=True)
        for k, v in results.items():
            p = os.path.join(out, f"{verb}.{k}.json".replace(":", "_"))
            with open(p, "w", encoding="utf-8", newline="\n") as fh:
                json.dump(v, fh, indent=1)
            print("OK: wrote %s" % p)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
