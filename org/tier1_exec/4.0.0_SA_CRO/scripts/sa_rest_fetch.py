#!/usr/bin/env python3
"""Seeking Alpha REST consumer -- rides the PARKED session, never logs in inline.

Measured contract (4.0.0_SA_CRO~Z, 2026-09-10; see
org/tier1_exec/4.0.0_SA_CRO/deliverables/AMGT_RESAPP_SEEKING_ALPHA_AUTH_INVESTIGATION_20260910.md):

  1. The jar MUST carry the browser-minted PerimeterX cookies (_px3, _pxvid, pxcts, _pxde) as well as
     the identity four (user_id, session_id, user_remember_token, user_cookie_key). Identity alone =>
     403. This is why the session is HARVESTED in a real browser (sa_harvest_session.py) and parked.
  2. Every request MUST carry a per-page Referer. Without it the API answers 200 with a 2-byte body.
  3. The fetch MUST egress through the residential proxy. This estate's native/datacenter IP served
     ~10 calls and was then PerimeterX-blocked for every call, including ones that had just worked.
  4. A 403 whose body contains "blockScript" is the RE-HARVEST signal (the PX cookies aged out), NOT
     an authentication failure. Callers distinguish the two: re-running the harvester fixes the first
     and nothing fixes the second but a new credential.

  ticker -> sa_id -> report:  GET /api/v3/symbols/{ticker} -> data.id
                              GET /api/v3/virtual_analysts/{sa_id}

ROE (inherited from bd_49f_auto_login.js): observe-act-only; a credential, cookie or session VALUE is
never logged or printed. The only artifacts written are the fetched payloads the caller asks for.

C-VENDOR-EGRESS: an external vendor call needs Andrew's explicit per-use word. The 2026-09-10 word
covered that day's investigation. A SCHEDULED consumer built on this module needs its own.

Usage:
  python sa_rest_fetch.py report RTX AAPL MSFT          # the virtual_analyst_report payload per ticker
  python sa_rest_fetch.py symbol RTX                    # the symbol record (carries sa_id)
  python sa_rest_fetch.py analysis RTX --limit 5        # recent analysis list
  python sa_rest_fetch.py article 4940348               # one article, full body for a paying user
  python sa_rest_fetch.py check                         # account info: is the parked session still authorized
Options:  --out <dir>   write each payload as JSON      --no-proxy   egress natively (expect PX blocks)
Env:      SA_SECRETS_DIR=<dir>  read secret_*.json from disk instead of Secrets Manager (dev only)
"""

import json
import os
import random
import re
import sys
import time

BASE = "https://seekingalpha.com"
SESSION_SECRET_ID = "seeking-alpha/session"
PROXY_SECRET_ID = "astn/brightdata/residential-proxy"
IDENTITY_COOKIE = "user_id"
# contracts.json sa auth_check: GET /api/v3/account/{user_id}/info -- {user_id} is the value of the
# parked bundle's `user_id` cookie (bundle["all_cookies"]); check() never uses a literal account id.
USER_ID_SHAPE = re.compile(r"^[A-Za-z0-9_-]{1,64}$")
PACE_SECONDS = 1.5


class ReHarvestRequired(RuntimeError):
    """The PerimeterX cookies in the parked bundle have aged out -- re-run sa_harvest_session.py."""


class NotAuthorized(RuntimeError):
    """The parked session is not an authorized user -- the credential or subscription is the problem."""


def _secret(name):
    d = os.environ.get("SA_SECRETS_DIR")
    if d:
        with open(
            os.path.join(d, "secret_" + name.replace("/", "_") + ".json"),
            encoding="utf-8",
        ) as fh:
            return fh.read().strip()
    import boto3

    return (
        boto3.client("secretsmanager", region_name="us-east-1")
        .get_secret_value(SecretId=name)["SecretString"]
        .strip()
    )


def bundle_user_id(cookies):
    """The account id the parked bundle carries: the value of its `user_id` cookie. Raises
    NotAuthorized when no such cookie has a usable value (the message never holds a value)."""
    ids = {str(c.get("value")) for c in cookies if c.get("name") == IDENTITY_COOKIE and c.get("value")}
    if len(ids) != 1:
        raise NotAuthorized(
            "parked bundle carries %d distinct non-empty %s values, need exactly 1" % (len(ids), IDENTITY_COOKIE)
        )
    user_id = ids.pop()
    if not USER_ID_SHAPE.match(user_id):
        raise NotAuthorized("parked bundle %s value is not a plain account id" % IDENTITY_COOKIE)
    return user_id


def build_session(use_proxy=True, *, bundle=None):
    """A curl_cffi session carrying the parked jar, Chrome TLS impersonation, and the proxy egress."""
    from curl_cffi import requests as cr

    if bundle is None:
        bundle = json.loads(_secret(SESSION_SECRET_ID))
    cookies = bundle["all_cookies"]
    names = {c["name"] for c in cookies}
    if IDENTITY_COOKIE not in names:
        raise NotAuthorized(
            "parked bundle carries no %s cookie -- it was not harvested logged-in"
            % IDENTITY_COOKIE
        )
    # BUG FIXED 2026-09-10 (found while building the FT/WSJ standing scripts, never caught here
    # because this function was never exercised end-to-end after commit): Bright Data's proxy
    # SSL-bumps traffic, which curl_cffi's default strict cert verification rejects outright
    # (CertificateVerifyError) -- every scratch prototype during the original investigation had
    # verify=False; this committed version never did, so a real run through the proxy would have
    # failed here on its first call.
    kwargs = {"impersonate": "chrome", "timeout": 70, "verify": False}
    if use_proxy:
        px = json.loads(_secret(PROXY_SECRET_ID))
        user = "%s-country-%s-session-sa%d" % (
            px["username"],
            px.get("country", "us"),
            random.randint(100000, 999999),
        )
        url = "http://%s:%s@%s:%s" % (user, px["password"], px["host"], px["port"])
        kwargs["proxies"] = {"http": url, "https": url}
    s = cr.Session(**kwargs)
    for c in cookies:
        try:
            s.cookies.set(
                c["name"],
                c["value"],
                domain=c.get("domain", "seekingalpha.com").lstrip("."),
                path=c.get("path", "/"),
            )
        except Exception:
            pass
    if bundle.get("user_agent"):
        s.headers.update({"User-Agent": bundle["user_agent"]})
    s.sa_user_id = bundle_user_id(cookies)
    return s, bundle["captured_at"]


def _headers(referer_path):
    return {
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": BASE + referer_path,
    }


def get_json(s, path, referer_path):
    """One authenticated GET. Raises ReHarvestRequired on a PerimeterX challenge."""
    r = s.get(BASE + path, headers=_headers(referer_path))
    head = (r.text or "")[:250]
    if r.status_code == 403 and "blockScript" in head:
        raise ReHarvestRequired(
            "PerimeterX challenge on %s -- re-run sa_harvest_session.py --park" % path
        )
    if r.status_code != 200:
        raise RuntimeError(
            "GET %s -> %d (%d bytes)" % (path, r.status_code, len(r.text or ""))
        )
    if len(r.text or "") < 10:
        raise RuntimeError(
            "GET %s -> 200 but %d-byte body; a missing Referer produces exactly this"
            % (path, len(r.text or ""))
        )
    return r.json()


def symbol(s, ticker):
    j = get_json(s, "/api/v3/symbols/%s" % ticker, "/symbol/%s" % ticker)
    d = j.get("data") or {}
    return {
        "ticker": ticker,
        "sa_id": d.get("id"),
        "attributes": d.get("attributes") or {},
    }


def news(s, ticker, limit=20):
    """Per-symbol news JSON; route measured in the later harvest consumer check."""
    symbol_name = ticker.lower()
    return get_json(
        s,
        f"/api/v3/symbols/{symbol_name}/news?filter[since]=0&filter[until]=0"
        f"&id={symbol_name}&include=author,primaryTickers,sentiments&page[size]={limit}",
        f"/symbol/{ticker.upper()}/news",
    )


def report(s, ticker, sa_id=None):
    """The virtual_analyst_report payload -- the modal's data, which its HTML does not carry."""
    if sa_id is None:
        sa_id = symbol(s, ticker)["sa_id"]
        time.sleep(PACE_SECONDS)
    j = get_json(
        s,
        "/api/v3/virtual_analysts/%s" % sa_id,
        "/symbol/%s/virtual_analyst_report" % ticker,
    )
    a = (j.get("data") or {}).get("attributes") or {}
    return {
        "ticker": ticker,
        "sa_id": sa_id,
        "created_at": a.get("createdAt"),
        "previous_report_date": a.get("previousReportDate"),
        "enough_analysis": a.get("enoughAnalysis"),
        "section_highlight": a.get("sectionHighlight"),
        "response_content": a.get("responseContent"),
        "ratings_response": a.get("ratingsResponse"),
        "provenance": {
            "source": "seekingalpha.com/api/v3/virtual_analysts",
            "claim": "measured",
            "basis": "Seeking Alpha generated report; adopt its basis, never restate as our own",
        },
    }


def analysis(s, ticker, limit=10):
    p = (
        "/api/v3/symbols/%s/analysis?filter[until]=0&filter[related]=false&id=%s"
        "&include=author,primaryTickers,sentiments&lang=en&page[number]=1&page[size]=%d"
        % (ticker.lower(), ticker.lower(), limit)
    )
    j = get_json(s, p, "/symbol/%s/analysis" % ticker)
    return [
        {
            "id": d.get("id"),
            "title": (d.get("attributes") or {}).get("title"),
            "published_on": (d.get("attributes") or {}).get("publishOn"),
        }
        for d in (j.get("data") or [])
    ]


def article(s, article_id):
    j = get_json(
        s, "/api/v3/articles/%s?include=author" % article_id, "/article/%s" % article_id
    )
    a = (j.get("data") or {}).get("attributes") or {}
    return {
        "id": article_id,
        "title": a.get("title"),
        "published_on": a.get("publishOn"),
        "is_paywalled": a.get("isPaywalled"),
        "is_locked_pro": a.get("isLockedPro"),
        "content": a.get("content"),
    }


def check(s):
    """Is the parked session still an authorized paying user? The account endpoint is the oracle."""
    user_id = getattr(s, "sa_user_id", None)
    if not isinstance(user_id, str) or not USER_ID_SHAPE.match(user_id):
        raise NotAuthorized("session carries no %s -- no account id to check" % IDENTITY_COOKIE)
    j = get_json(
        s, "/api/v3/account/%s/info?include=proSubscription" % user_id, "/symbol/RTX"
    )
    d = j.get("data") or {}
    if d.get("type") != "authorizedUser":
        raise NotAuthorized("account endpoint returned data.type=%r" % d.get("type"))
    subs = [
        i.get("attributes")
        for i in (j.get("included") or [])
        if "ubscription" in str(i.get("type"))
    ]
    return {
        "authorized": True,
        "user_id": (d.get("attributes") or {}).get("userId"),
        "subscriptions": subs,
    }


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    verb = argv[1]
    args = [a for a in argv[2:] if not a.startswith("--")]
    out = argv[argv.index("--out") + 1] if "--out" in argv else None
    limit = int(argv[argv.index("--limit") + 1]) if "--limit" in argv else 10
    s, captured_at = build_session(use_proxy="--no-proxy" not in argv)
    print(
        "OK: parked session captured_at=%s egress=%s"
        % (captured_at, "native" if "--no-proxy" in argv else "residential-proxy")
    )
    results = {}
    try:
        if verb == "check":
            results["check"] = check(s)
            print(
                "OK: authorized=%s subscriptions=%s"
                % (
                    results["check"]["authorized"],
                    json.dumps(results["check"]["subscriptions"]),
                )
            )
        elif verb == "report":
            for tk in args:
                r = report(s, tk.upper())
                results[tk.upper()] = r
                print(
                    "OK: %-6s sa_id=%-7s created=%s report_chars=%d ratings_chars=%d"
                    % (
                        tk.upper(),
                        r["sa_id"],
                        r["created_at"],
                        len(r["response_content"] or ""),
                        len(r["ratings_response"] or ""),
                    )
                )
                time.sleep(PACE_SECONDS)
        elif verb == "symbol":
            for tk in args:
                r = symbol(s, tk.upper())
                results[tk.upper()] = r
                print(
                    "OK: %-6s sa_id=%s name=%s"
                    % (tk.upper(), r["sa_id"], r["attributes"].get("companyName"))
                )
                time.sleep(PACE_SECONDS)
        elif verb == "analysis":
            for tk in args:
                r = analysis(s, tk.upper(), limit)
                results[tk.upper()] = r
                print(
                    "OK: %-6s %d article(s): %s"
                    % (tk.upper(), len(r), ", ".join(str(x["id"]) for x in r))
                )
                time.sleep(PACE_SECONDS)
        elif verb == "article":
            for aid in args:
                r = article(s, aid)
                results[aid] = r
                print(
                    "OK: article %s paywalled=%s lockedPro=%s content_chars=%d title=%s"
                    % (
                        aid,
                        r["is_paywalled"],
                        r["is_locked_pro"],
                        len(r["content"] or ""),
                        r["title"],
                    )
                )
                time.sleep(PACE_SECONDS)
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
            p = os.path.join(out, "%s.%s.json" % (verb, k))
            with open(p, "w", encoding="utf-8", newline="\n") as fh:
                json.dump(v, fh, indent=1)
            print("OK: wrote %s" % p)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
