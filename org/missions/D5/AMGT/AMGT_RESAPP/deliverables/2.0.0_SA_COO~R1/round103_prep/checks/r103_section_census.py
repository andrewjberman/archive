"""AMGT_RESAPP round-103 PREP -- FWD-40 (a): the per-name SECTION CENSUS read from the SERVED payloads (PRD v0.44).

  PYTHONPATH=<repo root> python r103_section_census.py --selftest
  PYTHONPATH=<repo root> python r103_section_census.py --where deployed [--names K1,K2] [--workers 4] [--out FILE.json]

For every resolved name (the dossier's resolved security keys, the same 95 `r98_thesis_fullbody_compare.py` reads) and each route the Security Analysis page calls once a name is
chosen (overlay, thesis, peers, coverage, versions, ledger; Lambda invoke, GET only), every TOP-LEVEL section of the body is classed:
    FILLED       the section carries content (a non-meta value that is not null, empty or an absence status);
    REASONED     the section is empty or an absence status AND a stated reason sits with it (`<key>_absent_reason`, `<key>_reason`, or a non-empty `reason` / `*_reason` /
                 `empty_reason` string inside the section);
    UNEXPLAINED  empty with no stated reason: FWD-40 (a)'s defect class.
Alongside, BROKEN-VALUE CANDIDATES (a candidate, never a verdict: FWD-40 (a) grades a hit CONFIRMED by a screenshot read): a string leaf under a RENDERED key (text, sentence, reason,
label, name, title, heading, description, note, notice, caption, headline, or a key ending _reason / _sentence / _label / _text / _name) that matches the ui-walk `raw-code` pattern
(an underscore-joined identifier) or one of its placeholder words (not supplied, unavailable, value pending, withheld, n/a, unknown, illustrative sample).
The population is printed beside the census: resolved names, the pack prefixes under `packs/`, and each difference NAMED.

Verdict: `R103 SECTION CENSUS: RAN <read> of <names> names (<failed> read failures)` -- the census REPORTS; the grade of FWD-40 (a) is the CVO's.
`--selftest`: six arms on synthetic bodies, `R103 CENSUS ARMS: YES|NO`.
"""
import argparse
import concurrent.futures
import json
import re
import sys

ROUTES = ("overlay", "thesis", "peers", "coverage", "versions", "ledger")
FN = "opal-amgt-scoped-api"
PREFIX = "/api/scoped/amgt"
META = {"status", "basis", "source", "source_name", "marked", "as_of", "generated", "generated_at", "schema_version", "generation", "generation_id", "security_key", "field", "axis",
        "identity_status", "window", "order", "complete", "states", "key_forms", "denominators", "count", "total"}
ABSENT_WORDS = re.compile(r"^(absent|empty|unavailable|not[_ ].*|no[_ ].*|withheld|missing|unresolved|none|n/?a|error|stale|refused|unknown)$", re.I)
RENDERED_KEYS = {"text", "sentence", "reason", "label", "name", "title", "heading", "description", "note", "notice", "caption", "headline", "display_name"}
RENDERED_SUFFIX = ("_reason", "_sentence", "_label", "_text", "_name")
RAW_CODE = re.compile(r"\b[A-Za-z][A-Za-z0-9]*(?:_[A-Za-z0-9]+)+\b")
PLACEHOLDERS = [(re.compile(p, re.I), n) for p, n in ((r"\bnot supplied\b", "not-supplied"), (r"\bunavailable\b", "unavailable"), (r"\bvalue pending\b", "value-pending"),
                                                       (r"^\s*unknown\s*$", "unknown"), (r"\bwithheld\b", "withheld"), (r"\bn/a\b", "n-a"), (r"illustrative sample", "sample-content"))]
URLISH = re.compile(r"(https?://|www\.|\.com\b|\.org\b|/)")


def _empty(v):
    return v is None or v == "" or v == [] or v == {}


def _reason_in(node):
    if isinstance(node, dict):
        for k, v in node.items():
            if (k == "reason" or k.endswith("_reason")) and isinstance(v, str) and v.strip():
                return True
    return False


def classify(body, key):
    """FILLED | REASONED | UNEXPLAINED for one top-level section `key` of a body dict."""
    value = body.get(key)
    reason = body.get(key + "_absent_reason") or body.get(key + "_reason")
    if isinstance(reason, str) and reason.strip():
        reason = True
    else:
        reason = False
    if isinstance(value, dict):
        status = value.get("status")
        content = any(not _empty(v) for k, v in value.items() if k not in META and k != "reason" and not k.endswith("_reason"))
        absent = isinstance(status, str) and bool(ABSENT_WORDS.match(status.strip()))
        if content and not absent:
            return "FILLED"
        return "REASONED" if (reason or _reason_in(value)) else "UNEXPLAINED"
    if _empty(value):
        return "REASONED" if reason else "UNEXPLAINED"
    return "FILLED"


def _rendered(k):
    return k in RENDERED_KEYS or k.endswith(RENDERED_SUFFIX)


def candidates(node, path=""):
    """[(path, kind, sample)] for string leaves under rendered keys."""
    out = []
    if isinstance(node, dict):
        for k, v in node.items():
            p = path + "." + str(k)
            if isinstance(v, str) and _rendered(str(k)):
                if RAW_CODE.search(v) and not URLISH.search(v):
                    out.append((p, "raw-code", v[:90]))
                for rx, name in PLACEHOLDERS:
                    if rx.search(v):
                        out.append((p, name, v[:90]))
            else:
                out.extend(candidates(v, p))
    elif isinstance(node, list):
        for i, v in enumerate(node[:200]):
            out.extend(candidates(v, "%s[%d]" % (path, i)))
    return out


def read(lam, key, route):
    event = {"rawPath": "%s/security/%s/%s" % (PREFIX, key, route), "queryStringParameters": None, "requestContext": {"http": {"method": "GET"}}, "headers": {"x-firm-id": "opal"}}
    r = json.loads(lam.invoke(FunctionName=FN, Payload=json.dumps(event).encode())["Payload"].read())
    try:
        return r.get("statusCode"), json.loads(r.get("body") or "{}")
    except ValueError:
        return r.get("statusCode"), {}


def one(lam, key):
    rows = {}
    for route in ROUTES:
        status, body = read(lam, key, route)
        sections = {k: classify(body, k) for k in body if not str(k).endswith("_absent_reason")} if isinstance(body, dict) else {}
        cands = candidates(body) if isinstance(body, dict) else []
        rows[route] = {"status": status, "sections": sections, "candidates": cands}
    return key, rows


def selftest():
    arms = []

    def arm(name, ok):
        arms.append(ok)
        print("   %s %s" % ("PASS" if ok else "FAIL", name))

    arm("A1 a filled list is FILLED", classify({"items": [1]}, "items") == "FILLED")
    arm("A2 an empty list with a `_absent_reason` is REASONED", classify({"price": None, "price_absent_reason": "no px"}, "price") == "REASONED")
    arm("A3 an empty list with NO reason is UNEXPLAINED (the negative control)", classify({"items": []}, "items") == "UNEXPLAINED")
    arm("A4 a dict with status absent and an inner reason is REASONED; the same without a reason is UNEXPLAINED",
        classify({"d": {"status": "absent", "reason": "none held"}}, "d") == "REASONED" and classify({"d": {"status": "absent"}}, "d") == "UNEXPLAINED")
    arm("A5 a raw code under a rendered key is a candidate; the same string under a key-like field is not",
        [c[1] for c in candidates({"label": "cash_mv", "security_key": "VLO_US_Equity"})] == ["raw-code"])
    arm("A6 a placeholder word is a candidate; a url is not a raw code",
        [c[1] for c in candidates({"text": "value pending", "note": "see http://a.b/c_d"})] == ["value-pending"])
    body = {"price": {"px_end": 1.0}, "price_absent_reason": None}
    arm("A7 a null `<key>_absent_reason` companion is not itself a section",
        sorted(k for k in body if not k.endswith("_absent_reason")) == ["price"] and classify(body, "price") == "FILLED")
    ok = all(arms)
    print("arms passed %d of %d" % (sum(arms), len(arms)))
    print("R103 CENSUS ARMS: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--where", default="deployed")
    ap.add_argument("--names")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--out")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    import boto3

    from lib.research.corpus import dossier
    from lib.research.harvest import store

    client = store._default_client()
    resolved = sorted(dossier._resolved_security_keys(client=client))
    packs = set()
    pager = client.get_paginator("list_objects_v2")
    for page in pager.paginate(Bucket=store.HARVEST_BUCKET, Prefix="packs/", Delimiter="/"):
        for cp in page.get("CommonPrefixes", []) or []:
            packs.add(cp["Prefix"].split("/")[1])
    print("POPULATION resolved=%d pack_prefixes=%d" % (len(resolved), len(packs)))
    print("  resolved NOT in packs/ (%d): %s" % (len(set(resolved) - packs), sorted(set(resolved) - packs)))
    print("  packs/ NOT in resolved (%d): %s" % (len(packs - set(resolved)), sorted(packs - set(resolved))))
    names = a.names.split(",") if a.names else resolved
    lam = boto3.client("lambda", region_name="us-east-1")
    result, failed = {}, []
    with concurrent.futures.ThreadPoolExecutor(max_workers=a.workers) as pool:
        futs = {pool.submit(one, lam, k): k for k in names}
        for fut in concurrent.futures.as_completed(futs):
            try:
                key, rows = fut.result()
                result[key] = rows
            except Exception as exc:  # a failed read is counted and named, never dropped
                failed.append("%s: %s %s" % (futs[fut], type(exc).__name__, str(exc)[:80]))
    tally = {}
    unexplained, cand_rows, bad_status = [], [], []
    for key in sorted(result):
        for route, row in result[key].items():
            if row["status"] != 200:
                bad_status.append((key, route, row["status"]))
            for sec, state in row["sections"].items():
                tally.setdefault((route, sec), {"FILLED": 0, "REASONED": 0, "UNEXPLAINED": 0})[state] += 1
                if state == "UNEXPLAINED":
                    unexplained.append((key, route, sec))
            for c in row["candidates"]:
                cand_rows.append((key, route) + tuple(c))
    print("SECTIONS (route.section: FILLED / REASONED / UNEXPLAINED over %d names)" % len(result))
    for (route, sec), t in sorted(tally.items()):
        print("  %-10s %-34s %3d / %3d / %3d" % (route, sec, t["FILLED"], t["REASONED"], t["UNEXPLAINED"]))
    print("UNEXPLAINED %d: %s" % (len(unexplained), unexplained[:40]))
    print("STATUS not 200 %d: %s" % (len(bad_status), bad_status[:40]))
    groups = {}
    for key, route, path, kind, sample in cand_rows:
        g = groups.setdefault((route, re.sub(r"\[\d+\]", "[]", path), kind, sample[:60]), set())
        g.add(key)
    print("BROKEN-VALUE CANDIDATES %d hits in %d patterns (a candidate is not a verdict; the screenshot read confirms):" % (len(cand_rows), len(groups)))
    for (route, path, kind, sample), names_hit in sorted(groups.items(), key=lambda kv: -len(kv[1]))[:50]:
        print("  %-9s %-52s %-12s on %3d names  %r" % (route, path[:52], kind, len(names_hit), sample))
    if a.out:
        json.dump({"names": sorted(result), "failed": failed, "resolved": resolved, "packs": sorted(packs), "result": result}, open(a.out, "w", encoding="utf-8"), default=str)
    print("R103 SECTION CENSUS: RAN %d of %d names (%d read failures)" % (len(result), len(names), len(failed)))
    for f in failed[:10]:
        print("  FAILED %s" % f)
    return 0 if len(result) == len(names) else 1


if __name__ == "__main__":
    sys.exit(main())
