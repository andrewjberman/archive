#!/usr/bin/env python3
"""HVST-w-5 AC1 -- ONE /user-info call and ONE search/query call on the PARKED bbg session.

Rides org/tier1_exec/4.0.0_SA_CRO/scripts/bloomberg_rest_fetch.py (check, search) on the session
`bloomberg/session`. It never logs in, never starts a browser, never calls a vision model.
`lib.opal_data_harvest` is NOT imported (its 403 path would open a headed Chrome press-and-hold).

Andrew's word (org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20260928_1805Z_OPEN_CALLS_FOUR_RULINGS.md
ruling 2): one bounded run, diagnostic only, no data written, no retry. Mechanical guards here:
  * a recording proxy REFUSES a second call to the same host+path and any third call;
  * a live run REFUSES to start if ac1_capture.json or a ledger '## CALL 1' entry already exists;
  * HVST_W5_STUB=1 swaps the network for a canned response and writes to .scratch only (debug arm).
A credential, cookie or session VALUE is never printed or written: cookie NAMES/COUNTS only.
"""
import datetime
import hashlib
import importlib.util
import json
import os
import re
import sys
import time
from pathlib import Path
from urllib.parse import urlparse

HERE = Path(__file__).resolve().parent
DELIV = HERE.parent
REPO = HERE.parents[7]
assert (REPO / "org").is_dir() and (REPO / ".tools").is_dir(), REPO
STUB = os.environ.get("HVST_W5_STUB") == "1"
SEAT = "0.9.0_WK_AMGT_HARVST~37"
QUERY = "Lenovo"
if STUB:
    OUT_DIR = REPO / ".scratch" / "w5_stub"
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    CAPTURE = OUT_DIR / "ac1_capture.json"
    LEDGER = OUT_DIR / "VENDOR_CALLS_STUB.md"
else:
    CAPTURE = DELIV / "ac1_capture.json"
    LEDGER = REPO / "org/missions/D5/AMGT/AMGT_HARVST/ledger/VENDOR_CALLS_0.9.0_WK_AMGT_HARVST_37.md"
FETCH = REPO / "org/tier1_exec/4.0.0_SA_CRO/scripts/bloomberg_rest_fetch.py"

LEDGER_HEAD = """# VENDOR CALL LEDGER -- `0.9.0_WK_AMGT_HARVST~37`, AMGT_HARVST (task order `HVST-w-5`)

**Why this file exists.** The ledger is a condition of Andrew's word (ANDREW_DIRECT_20260928_1805Z ruling 2), not
paperwork. Same shape as `VENDOR_CALLS_0.9.0_WK_AMGT_HARVST_22.md` beside it.

**No entry here covers spend, a contract, an entitlement or a hold-lift.** No re-authentication, browser or
vision call is covered or was reached.

---
"""


def _load_fetch():
    spec = importlib.util.spec_from_file_location("bloomberg_rest_fetch", FETCH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class _StubResp:
    def __init__(self, status, body, headers):
        self.status_code, self.content, self.headers = status, body, headers
        self.text = body.decode("utf-8", "replace")

    def json(self):
        return json.loads(self.text)


class _StubSession:
    """Debug arm only: no network. /user-info -> 200, search/query -> canned 535-byte PX-shaped 403."""
    def __init__(self):
        self.cookies, self.headers = {}, {}

    def get(self, url, **kw):
        if "user-info" in url:
            return _StubResp(200, b'{"userId":"x"}', {"content-type": "application/json"})
        body = (b'{"appId":"PX0000","jsClientSrc":"/x/init.js","firstPartyEnabled":true,"vid":"'
                + b"a" * 36 + b'","uuid":"' + b"b" * 36 + b'","hostUrl":"/x/xhr","blockScript":"/x/captcha.js"}')
        return _StubResp(403, body, {"content-type": "application/json", "set-cookie": "_pxhd=SECRET; Path=/"})


class Recorder:
    """Delegating session proxy: records every GET, refuses a repeat of host+path and any third call."""
    def __init__(self, inner):
        self.inner, self.calls, self._seen = inner, [], set()

    def get(self, url, **kw):
        u = urlparse(url)
        key = (u.hostname, u.path)
        if key in self._seen or len(self.calls) >= 2:
            raise RuntimeError(f"REFUSED: second call to {key} / call #{len(self.calls) + 1} exceeds the word")
        self._seen.add(key)
        t0 = time.perf_counter()
        at = datetime.datetime.now(datetime.timezone.utc)
        r = self.inner.get(url, **kw)
        self.calls.append({"host": u.hostname, "path": u.path, "params": sorted((kw.get("params") or {}).keys()),
                           "at": at.isoformat(), "elapsed_ms": round((time.perf_counter() - t0) * 1000),
                           "response": r})
        return r

    def __getattr__(self, name):
        return getattr(self.inner, name)


def _structure(text):
    """Volatile-token-normalised form: uuids, long hex/base64 runs and digits collapsed, so two bodies
    that differ only in per-request ids hash equal."""
    t = re.sub(r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}", "<uuid>", text)
    t = re.sub(r"[A-Za-z0-9+/=_-]{24,}", "<tok>", t)
    return re.sub(r"\d+", "<n>", t)


MARKERS = ["px-captcha", "_px", "perimeterx", "px-cloud", "captcha", "blockScript", "appId", "jsClientSrc",
           "Are you a robot", "human", "cloudflare", "akamai", "datadome", "access denied", "<html", "<title"]


def classify(r):
    text = r.text
    hdrs = {}
    set_cookie_names = []
    items = r.headers.items() if hasattr(r.headers, "items") else []
    for k, v in items:
        lk = k.lower()
        if lk == "set-cookie":
            set_cookie_names += [c.split("=", 1)[0].strip() for c in str(v).split("\n")]
            hdrs[lk] = "<names only: %s>" % ",".join(c.split("=", 1)[0].strip() for c in str(v).split("\n"))
        elif lk in ("cookie", "authorization"):
            hdrs[lk] = "<redacted>"
        else:
            hdrs[lk] = str(v)[:240]
    out = {
        "status": r.status_code, "bytes": len(r.content), "headers": hdrs, "set_cookie_names": set_cookie_names,
        "content_type": hdrs.get("content-type"),
        "title": (re.findall(r"<title>(.*?)</title>", text, re.S) or [None])[0],
        "markers_present": [m for m in MARKERS if m.lower() in text.lower()],
        "body_sha256": hashlib.sha256(r.content).hexdigest(),
        "body_structure_sha256": hashlib.sha256(_structure(text).encode()).hexdigest(),
        "is_535_bytes": len(r.content) == 535,
    }
    try:
        j = json.loads(text)
        out["json_top_level_keys"] = sorted(j.keys()) if isinstance(j, dict) else f"<{type(j).__name__}>"
        if isinstance(j, dict) and "results" in j:
            out["json_results_len"] = len(j["results"])
            out["json_total"] = j.get("total")
    except Exception:
        out["json_top_level_keys"] = None
    if r.status_code != 200 and len(r.content) <= 20000:
        out["body_text_retained"] = text          # a refusal page/challenge JSON, no credential in it
    else:
        out["body_text_retained"] = None          # a 200 payload is data: shape only, never retained
    return out


def main():
    if not STUB:
        if CAPTURE.exists():
            print("REFUSED: ac1_capture.json already exists -- a second live run exceeds the word")
            return 2
        if LEDGER.exists() and "## CALL 1" in LEDGER.read_text(encoding="utf-8"):
            print("REFUSED: ledger already holds CALL 1 -- a second live run exceeds the word")
            return 2
    mod = _load_fetch()
    now = datetime.datetime.now(datetime.timezone.utc)
    if STUB:
        bundle = {"captured_at": (now - datetime.timedelta(hours=5)).isoformat(),
                  "all_cookies": [{"name": "_pxhd", "value": "V", "domain": ".bloomberg.com", "expires": -1},
                                  {"name": "session_id", "value": "V", "domain": ".bloomberg.com"}],
                  "user_agent": "stub"}
        inner = _StubSession()
    else:
        bundle = json.loads(mod._secret(mod.SESSION_SECRET_ID))          # the transport's own designed read
        inner = mod.build_session(bundle=bundle)                          # prints captured_at
    ca = bundle.get("captured_at")
    try:
        cdt = datetime.datetime.fromisoformat(str(ca).replace("Z", "+00:00"))
        if cdt.tzinfo is None:
            cdt = cdt.replace(tzinfo=datetime.timezone.utc)
        age_h = round((now - cdt).total_seconds() / 3600, 2)
    except Exception:
        age_h = None
    cookies = bundle.get("all_cookies", [])
    names = sorted({c["name"] for c in cookies})
    px = [{"name": c["name"], "domain": c.get("domain"), "expires": c.get("expires")} for c in cookies
          if c["name"].lower().startswith("_px") or "px" in c["name"].lower()]
    print(f"session captured_at={ca} age_hours_at_call={age_h}")
    print(f"session bundle top-level keys={sorted(bundle.keys())}")
    print(f"session cookie count={len(cookies)} distinct names={len(names)}")
    print(f"session cookie names={names}")
    print(f"px-class cookies (name/domain/expires only)={px}")

    s = Recorder(inner)
    result = {"seat": SEAT, "stub": STUB, "query": QUERY, "session_captured_at": ca, "session_age_hours": age_h,
              "cookie_count": len(cookies), "cookie_names": names, "px_cookies": px, "calls": []}

    # ---- CALL A: /user-info (the transport's own check) ----
    r1 = mod.check(s)
    c1 = classify(r1)
    print("--- /user-info ---")
    print(json.dumps({k: v for k, v in c1.items() if k != "body_text_retained"}, indent=1))

    # ---- CALL B: search/query "Lenovo" -- non-200 CAUGHT, never retried ----
    search_error = None
    try:
        mod.search(s, QUERY)
    except RuntimeError as e:
        search_error = str(e)
    rec = s.calls[1]
    c2 = classify(rec["response"])
    print("--- search/query ---")
    print(f"search() raised={search_error!r}")
    print(json.dumps({k: v for k, v in c2.items() if k != "body_text_retained"}, indent=1))
    for rc, c in zip(s.calls, (c1, c2)):
        result["calls"].append({"host": rc["host"], "path": rc["path"], "params": rc["params"], "at": rc["at"],
                                "elapsed_ms": rc["elapsed_ms"], "classification": c})
    result["search_raised"] = search_error
    result["stored_403_bytes_expected"] = 535

    browser = [m for m in ("playwright", "selenium", "pyppeteer", "undetected_chromedriver") if m in sys.modules]
    vision = [m for m in ("openai", "anthropic", "moonshot", "kimi") if m in sys.modules]
    login_paths = [c["path"] for c in s.calls if c["path"] != "/user-info" and "search/query" not in c["path"]]
    hosts = sorted({c["host"] for c in s.calls})
    result["measured"] = {"browser_started": bool(browser), "login_attempted": bool(login_paths) or
                          "lib.opal_data_harvest" in sys.modules, "vision_call": bool(vision) or
                          any(not h.endswith("bloomberg.com") for h in hosts),
                          "calls_made": len(s.calls), "hosts_contacted": hosts,
                          "lib_opal_data_harvest_imported": "lib.opal_data_harvest" in sys.modules}
    CAPTURE.write_text(json.dumps(result, indent=1) + "\n", encoding="utf-8")
    print(f"calls_made: {len(s.calls)} (hosts {hosts})")
    print(f"browser_started: {result['measured']['browser_started']}")
    print(f"login_attempted: {result['measured']['login_attempted']}")
    print(f"vision_call: {result['measured']['vision_call']}")

    # ---- ledger CALL 1, same run, printed as written ----
    ts = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    end = datetime.datetime.now(datetime.timezone.utc).strftime("%H:%M:%SZ")
    st2 = c2["status"]
    entry = f"""
## CALL 1 -- bloomberg.com, {ts} -> {end}

| field | value |
|---|---|
| seat | `{SEAT}` (worker of `2.0.0_SA_COO~H`, task order `HVST-w-5`, AC1) |
| vendor | bloomberg (`www.bloomberg.com`, `login.bloomberg.com`) |
| endpoint class | REST: `GET login.bloomberg.com/user-info` (session check) and `GET www.bloomberg.com/nemo-next/api/search/query?query={QUERY}` |
| mechanism | `python org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~37/scripts/ac1_one_call_pair.py` -- imports `check` and `search` from `org/tier1_exec/4.0.0_SA_CRO/scripts/bloomberg_rest_fetch.py` (curl_cffi chrome impersonation) on the parked session `bloomberg/session`; `lib.opal_data_harvest` NOT imported; a recording proxy refuses any repeat call |
| agent-turn fetch? | **NO.** Scripted transport run from a command line; the worker constructed no HTTP client and pasted no payload. The script printed classifications only; no 200 body is retained or printed |
| scope | exactly {len(s.calls)} calls: 1 x `/user-info`, 1 x `search/query` (query `{QUERY}`); no retry, no second security |
| authorization | Andrew-direct 2026-09-28 ~18:05Z, `org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20260928_1805Z_OPEN_CALLS_FOUR_RULINGS.md` ruling 2, verbatim answer "2.) Rec approved." -- `w-5` YES, one bounded run, diagnostic only, no data written, scripted producer, ledgered by the seat that runs it. Spend, contracts, entitlements and hold-lifts NOT covered |
| credential used | the PARKED session envelope in AWS Secrets Manager `bloomberg/session` (GetSecretValue, the transport's designed read); captured_at `{ca}`, age at call {age_h} h, {len(cookies)} cookies; VALUES never printed or written |
| re-auth fired? | **NO -- measured.** login_attempted={result['measured']['login_attempted']}, browser_started={result['measured']['browser_started']}, vision_call={result['measured']['vision_call']}; only the two recorded calls reached the network (hosts {hosts}) |
| result | `/user-info` HTTP {c1['status']} ({c1['bytes']} B); `search/query` HTTP {st2} ({c2['bytes']} B, title {c2['title']!r}, markers {c2['markers_present']}, 535-byte body: {c2['is_535_bytes']}) |
| bytes retained | `ac1_capture.json`: status/bytes/header names+values (set-cookie names only)/classification for both calls; the refusal body text ONLY if non-200 (it is a bot-wall page, not data); NO 200 body |
| S3 written | none |
| spend | none |
| evidence | `org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~37/ac1_capture.json`, `ac1_output.txt` |
"""
    if not LEDGER.exists():
        LEDGER.write_text(LEDGER_HEAD, encoding="utf-8")
    with LEDGER.open("a", encoding="utf-8") as fh:
        fh.write(entry)
    print("=== LEDGER CALL 1 AS WRITTEN (%s) ===" % LEDGER.name)
    print(entry)
    return 0


class _Tee:
    def __init__(self, a, path):
        self.a, self.f = a, open(path, "w", encoding="utf-8")

    def write(self, x):
        self.a.write(x)
        self.f.write(x)

    def flush(self):
        self.a.flush()
        self.f.flush()


if __name__ == "__main__":
    _out = (REPO / ".scratch" / "w5_stub" / "ac1_output.txt") if STUB else (DELIV / "ac1_output.txt")
    _out.parent.mkdir(parents=True, exist_ok=True)
    if not STUB and CAPTURE.exists():
        print("REFUSED: ac1_capture.json already exists -- a second live run exceeds the word")
        sys.exit(2)
    sys.stdout = _Tee(sys.stdout, _out)
    sys.exit(main())
