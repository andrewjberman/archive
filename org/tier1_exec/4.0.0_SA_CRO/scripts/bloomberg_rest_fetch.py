#!/usr/bin/env python3
"""Bloomberg.com REST consumer -- rides the PARKED session (bloomberg/session), never logs in inline.
Standing reference for AMGT_RESAPP, mirroring sa_rest_fetch.py / ft_rest_fetch.py's shape and ROE.

DISCOVERED 2026-09-11 (4.0.0_SA_CRO~Z) by network-sniffing a real authenticated browser session
navigating to a quote page -- not guessed. Of ~110 XHR/fetch calls observed, three are Bloomberg's
own first-party data APIs (the rest is ad-tech/analytics noise):
  1. GET login.bloomberg.com/user-info?withSubscriberData=false&activeSubscriptionsOnly=false
     -- session/auth check, same role as SA's `check` verb.
  2. GET www.bloomberg.com/nemo-next/api/tickers?ids={TICKER}:{EXCHANGE}
     -- per-symbol quote lookup (the "individual symbol search" Andrew asked to test). Bloomberg's
     own page called this 5 times for RTX across exchange suffixes (US, CI, SW, AV, DC) discovered
     from ITS OWN internal ticker-resolution, not guessed by us.
  3. GET www.bloomberg.com/bazaar/api/chart-news/{TICKER}:{EXCHANGE}?targetDate=...&dateRange=1D&
     endDate=...&name={NAME}
     -- per-ticker news tied to the chart widget, seen fire multiple times in one real page load
     with DIFFERENT targetDate/endDate pairs each time and at least one further parameter
     (truncated in the sniff log as "sta...", not yet captured in full). MEASURED: a hand-built
     call with a naive now-minus-1-day targetDate/endDate returned 404, and two follow-up live
     sniffs (including scrolling + hovering the chart) did not reproduce the call firing again --
     its exact trigger and full parameter set are NOT YET PROVEN. This is a NOT-FOUND-AT-THIS-CUT,
     not a claim the endpoint doesn't exist (same honest shape as ft_rest_fetch.py's own
     news_tab-not-found note) -- a later pass with the vendor word can capture the full request
     via CDP/HAR rather than a truncated response-log line.

ROE (inherited unchanged): observe-act-only; a credential, cookie or session VALUE is never logged
or printed. The only artifacts written are the fetched payloads the caller asks for.

C-VENDOR-EGRESS: an external vendor call needs Andrew's explicit per-use word; each live call this
file made was inside a same-terminal "run it" during this investigation. A SCHEDULED consumer built
on this module needs its own word.

Usage:
  python bloomberg_rest_fetch.py check                     # is the parked session authorized
  python bloomberg_rest_fetch.py ticker RTX:US              # per-symbol lookup
  python bloomberg_rest_fetch.py news RTX:US "RTX CORP"     # per-ticker news, last 1 day
Options:  --out <dir>   write each payload as JSON
Env:      SA_SECRETS_DIR=<dir>  read secret_*.json from disk instead of Secrets Manager (dev only)
"""
import datetime
import json
import os
import sys

from curl_cffi import requests as creq

BASE = "https://www.bloomberg.com"
LOGIN_BASE = "https://login.bloomberg.com"
SESSION_SECRET_ID = "bloomberg/session"


def _secret(name):
    d = os.environ.get("SA_SECRETS_DIR")
    if d:
        with open(os.path.join(d, "secret_" + name.replace("/", "_") + ".json"), encoding="utf-8") as fh:
            return fh.read().strip()
    import boto3
    return boto3.client("secretsmanager", region_name="us-east-1").get_secret_value(SecretId=name)["SecretString"]


def build_session():
    bundle = json.loads(_secret(SESSION_SECRET_ID))
    s = creq.Session(impersonate="chrome", timeout=30, verify=False)
    for c in bundle["all_cookies"]:
        s.cookies.set(c["name"], c["value"], domain=c.get("domain"), path=c.get("path", "/"))
    s.headers.update({
        "User-Agent": bundle.get("user_agent") or "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json, text/plain, */*",
    })
    print(f"OK: parked session loaded, captured_at={bundle.get('captured_at')}", flush=True)
    return s


def check(s):
    r = s.get(f"{LOGIN_BASE}/user-info", params={"withSubscriberData": "true", "activeSubscriptionsOnly": "false"},
               headers={"Referer": f"{BASE}/"})
    print(f"OK: HTTP {r.status_code} bytes={len(r.content)}")
    return r


def ticker(s, symbol):
    r = s.get(f"{BASE}/nemo-next/api/tickers", params={"ids": symbol},
               headers={"Referer": f"{BASE}/quote/{symbol}"})
    print(f"OK: {symbol} HTTP {r.status_code} bytes={len(r.content)}")
    return r


def news(s, symbol, name):
    now = datetime.datetime.utcnow()
    since = now - datetime.timedelta(days=1)
    r = s.get(f"{BASE}/bazaar/api/chart-news/{symbol}", params={
        "targetDate": since.strftime("%Y-%m-%dT%H:%M:00Z"),
        "dateRange": "1D",
        "endDate": now.strftime("%Y-%m-%dT%H:%M:00.000Z"),
        "name": name.replace(" ", "+"),
    }, headers={"Referer": f"{BASE}/quote/{symbol}"})
    print(f"OK: {symbol} news HTTP {r.status_code} bytes={len(r.content)}")
    return r


def _write(out_dir, name, r):
    if not out_dir:
        return
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"{name}.json")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(r.text)
    print(f"OK: wrote {path} ({len(r.content)} bytes)")


if __name__ == "__main__":
    A = sys.argv
    out_dir = A[A.index("--out") + 1] if "--out" in A else None
    verb = A[1] if len(A) > 1 else ""
    s = build_session()
    if verb == "check":
        r = check(s)
        print(r.text[:2000])
    elif verb == "ticker":
        symbol = A[2]
        r = ticker(s, symbol)
        print(r.text[:2000])
        _write(out_dir, f"ticker_{symbol.replace(':', '_')}", r)
    elif verb == "news":
        symbol, name = A[2], A[3]
        r = news(s, symbol, name)
        print(r.text[:2000])
        _write(out_dir, f"news_{symbol.replace(':', '_')}", r)
    else:
        print(f"ERROR: unknown verb {verb!r}")
        sys.exit(1)
