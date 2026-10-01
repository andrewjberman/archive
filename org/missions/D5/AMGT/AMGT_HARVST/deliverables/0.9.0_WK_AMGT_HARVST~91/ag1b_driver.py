"""HVST-ag-1 (round 34, FWD-11): wsj THEN barrons, a fresh-profile in-profile Dow Jones sign-in (verification.renew) under
ONE InputSourceMonitor window. Up to 3 fresh-profile attempts per publisher, at most 15 requests per publisher.
A challenge is never forced: if none is met the record says "none". Credentials are never printed."""
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[7]
sys.path.insert(0, str(ROOT))
from lib.opal_data_harvest import tab_transport, verification  # noqa: E402
from lib.opal_data_harvest.input_source import InputSourceMonitor  # noqa: E402

OUT = Path(__file__).resolve().parent
PROFILES = OUT / "r34-profiles"
ORIGINS = {"wsj": "https://www.wsj.com", "barrons": "https://www.barrons.com"}
CAP, ATTEMPTS = 5, 2

state = {"pub": None, "n": {"wsj": 0, "barrons": 0}, "log": []}
solves = []


class CapReached(Exception):
    pass


def bump(kind, detail):
    pub = state["pub"]
    if state["n"][pub] >= CAP:
        raise CapReached("request cap %d reached for %s" % (CAP, pub))
    state["n"][pub] += 1
    state["log"].append({"pub": pub, "n": state["n"][pub], "kind": kind, "detail": detail})


_orig_get = tab_transport.TabSession.get


def counted_get(self, url, *a, **k):
    bump("fetch", url.split("?")[0][-80:])
    r = _orig_get(self, url, *a, **k)
    state["log"][-1]["status"] = r.status_code
    return r


tab_transport.TabSession.get = counted_get
_orig_solve = verification.solve


def recording_solve(*a, **k):
    out = _orig_solve(*a, **k)
    solves.append(dict(out))
    return out


verification.solve = recording_solve


def attempt(pub, k, monitor):
    root = PROFILES / pub / ("a%d" % k)
    rec = {"profile_root": str(root.relative_to(OUT)), "attempt": k, "requests_before": state["n"][pub]}
    tab = None
    del solves[:]
    try:
        bump("navigate", ORIGINS[pub] + " (TabSession open)")
        tab = tab_transport.TabSession(pub, root, ORIGINS[pub])
        page = tab.page
        orig_goto = page.goto

        def counted_goto(url, *a, **kw):
            bump("navigate", url.split("?")[0][-80:])
            return orig_goto(url, *a, **kw)

        page.goto = counted_goto
        renewal = verification.renew(tab, pub, monitor=monitor)
        rec["renewal"] = {k2: v for k2, v in renewal.items() if k2 not in ("before_sha256", "after_sha256")}
    except CapReached as exc:
        rec["error"] = str(exc)
    except BaseException as exc:  # noqa: BLE001 -- recorded, never a retry loop
        rec["error"] = ("%s: %s" % (type(exc).__name__, str(exc).splitlines()[0] if str(exc) else ""))[:240]
    finally:
        if tab is not None:
            try:
                tab.close()
            except Exception as exc:  # noqa: BLE001
                rec["close_error"] = str(exc)[:120]
    rec["solves"] = list(solves)
    rec["requests_after"] = state["n"][pub]
    return rec


results = {}
t0 = time.time()
with InputSourceMonitor() as monitor:
    for pub in ("wsj",):
        state["pub"] = pub
        attempts = []
        for k in range(4, 4 + ATTEMPTS):
            if state["n"][pub] >= CAP:
                break
            rec = attempt(pub, k, monitor)
            attempts.append(rec)
            print("%s attempt %d: error=%s solves=%s requests=%d" % (pub, k, rec.get("error"),
                  [(s.get("challenge_met"), s.get("path"), s.get("passed")) for s in rec["solves"]], state["n"][pub]), flush=True)
            if any(s.get("passed") and s.get("path") not in (None, "none") for s in rec["solves"]):
                break
            if not rec.get("error") or "Timeout" not in rec["error"] or rec["requests_after"] > 3:
                break
            time.sleep(20)
        results[pub] = {"attempts": attempts, "requests": state["n"][pub]}
        (OUT / ("ag1b_%s_result.json" % pub)).write_text(json.dumps(results[pub], indent=1, default=str), encoding="utf-8")
        print("%s DONE at %s" % (pub, monitor.now()), flush=True)
        print("%s LAST REQUEST AT %s" % (pub, monitor.now()), flush=True)
detail = {"monitor": monitor.record(), "results": results, "request_log": state["log"]}
(OUT / "ag1b_detail.json").write_text(json.dumps(detail, indent=1, default=str), encoding="utf-8")
print("MONITOR", json.dumps(monitor.record()))
