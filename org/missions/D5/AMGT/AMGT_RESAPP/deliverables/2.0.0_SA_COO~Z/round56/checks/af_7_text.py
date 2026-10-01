"""AMGT_RESAPP round 56 -- AMGT-af-7 AC2: no served reason reads as a status token (CONTRACT s.4).

Live, read-only: calls lib.research.api.scoped_amgt.handler locally for the overlay, thesis, print and
coverage routes of three names (BA_US_Equity, ASML_NA_Equity, AMZN_US_Equity), walks every response,
and collects every string value under a key whose name ends in `reason`. A value FAILS when it carries
a status token the page must never show: ABSENT, REFUSED, NOT_SERVED, "not served", "unsupported".
A third clause: a posture whose verdict is `absent` (ASML at the cut) carries `absent_reason` in plain words
(no status token, no internal label such as R-1, no null/None). A second clause reads BA_US_Equity's research-pack claims across thesis, print and overlay: a reason
saying there is no research pack FAILS if any of those responses serves a pack-derived field
(`drafted_sections`, `posture` verdict, or model `header_figures`) for the same name.

Verdict: EVERY SERVED REASON IS PLAIN WORDS AND BA'S PACK CLAIMS AGREE: YES|NO
"""
from __future__ import annotations

import json
import re
import sys

NAMES = ("BA_US_Equity", "ASML_NA_Equity", "AMZN_US_Equity")
LEAVES = ("overlay", "thesis", "print", "coverage")
TOKEN = re.compile(r"\bABSENT\b|\bREFUSED\b|\bNOT_SERVED\b|(?i:not served|unsupported)")
JARGON = re.compile(r"\b[A-Z]-\d\b|\bnull\b|\bNone\b")
NO_PACK = re.compile(r"no research pack", re.IGNORECASE)


def _call(path):
    from lib.research.api import scoped_amgt

    ev = {"rawPath": path, "requestContext": {"http": {"method": "GET"}},
          "headers": {"x-firm-id": "bd"}, "queryStringParameters": None}
    r = scoped_amgt.handler(ev)
    try:
        return r.get("statusCode"), json.loads(r.get("body") or "null")
    except ValueError:
        # a non-JSON body (the print route renders HTML): reasons there are graded by its text
        body = r.get("body") or ""
        return r.get("statusCode"), {"_html_reason": body} if TOKEN.search(body) else {}


def _walk(o, path=""):
    if isinstance(o, dict):
        for k, v in o.items():
            p = f"{path}.{k}"
            if isinstance(v, str) and k.lower().endswith("reason"):
                yield p, v
            else:
                yield from _walk(v, p)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from _walk(v, f"{path}[{i}]")


def _strings(o, path=""):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from _strings(v, f"{path}.{k}")
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from _strings(v, f"{path}[{i}]")
    elif isinstance(o, str):
        yield path, o


def _has_pack_fields(body):
    s = json.dumps(body or {})
    return any(k in s for k in ('"drafted_sections": [{', '"verdict": "')) or bool((body or {}).get("header_figures"))


def main():
    from lib.research.api import scoped_amgt as s

    bad, total = [], 0
    bodies = {}
    for n in NAMES:
        for leaf in LEAVES:
            st, body = _call(f"{s.ROUTE_PREFIX}/security/{n}/{leaf}")
            bodies[(n, leaf)] = body
            for p, v in _walk(body):
                total += 1
                if TOKEN.search(v):
                    bad.append((n, leaf, p, v[:90]))
    # AMGT-ah (row Z-S330): the denominator names the (name, route) pairs that carried reason strings, not the route list's length
    carried = sorted({(n, leaf) for (n, leaf), body in bodies.items() if any(True for _ in _walk(body))})
    print(f"denominator: {total} served reason string(s) across {len(carried)} of {len(NAMES) * len(LEAVES)} (name, route) pairs "
          f"that carried any (the print route serves a PDF and is skipped)")
    ok1 = not bad
    print(f"{'PASS' if ok1 else 'FAIL'} C1 no served reason carries a status token -- {len(bad)} bad")
    for b in bad[:12]:
        print("   ", b)
    ba = [(leaf, p, v) for (n, leaf), body in bodies.items() if n == "BA_US_Equity" for p, v in _strings(body) if NO_PACK.search(v)]
    served_pack = [leaf for (n, leaf), body in bodies.items() if n == "BA_US_Equity" and _has_pack_fields(body)]
    ok2 = not (ba and served_pack)
    print(f"{'PASS' if ok2 else 'FAIL'} C2 BA research-pack claims agree -- 'no research pack' at {[(leaf_, p) for leaf_, p, _ in ba][:4]}; "
          f"pack-derived fields served by {served_pack}")
    post = []
    for n in NAMES:
        pz = (bodies.get((n, "overlay")) or {}).get("posture") or {}
        if str(pz.get("verdict", "")).lower() == "absent":
            ar = str(pz.get("absent_reason") or "")
            post.append((n, bool(ar) and not TOKEN.search(ar) and not JARGON.search(ar), ar[:90]))
    ok3 = bool(post) and all(x[1] for x in post)
    print(f"{'PASS' if ok3 else 'FAIL'} C3 a posture with verdict absent carries a plain-words absent_reason -- {post}")
    verdict = ok1 and ok2 and ok3
    print(f"EVERY SERVED REASON IS PLAIN WORDS AND BA'S PACK CLAIMS AGREE: {'YES' if verdict else 'NO'}")
    return 0 if verdict else 1


if __name__ == "__main__":
    sys.exit(main())
