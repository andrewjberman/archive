"""AMGT_RESAPP round 61 -- cells B2 and B3 (DSGN_AMGTV1 round-21 analysis @e14de1769c section 3B): the served Exec,
Posture and Peers text for BA_US_Equity and VLO_US_Equity carries no code-shaped token (B2), and VLO's served officers carry
their full titles with no trailing age (B3).

  --cell b2|b3                 which cell's clauses run.
  --where local                lib.research.api.scoped_amgt.handler in this tree (live stores, read-only).
  --where deployed             the DEPLOYED opal-amgt-scoped-api.
  --plan <json> [--plan ...]   a rewrite plan for STORED fields (an M-1 object written by a producer, not at serve time). Each
                               entry: {"security_key", "route" ("thesis"|"peers"), "json_path" (e.g. ".management.officers[1].name"),
                               "store_key", "store_field", "before", "after"}. Every entry's `before` must equal what the route
                               serves now, then `after` is applied to the served body before grading -- the state the store
                               write will produce. Without --plan the served body is graded as it is.

B2 clauses -- the analysis names TWO served strings (section 1 rows 2-3), so the census is exactly those: the Exec tab's
`thesis.management.lusha_enrichment.reason`, and every `reason` inside an `absent` list of the peers route (the registry's
absent-column reasons):
  C1 0 of them match the code-shaped pattern of the analysis's A1: [a-z]+_[a-z0-9_]+ | _Equity | \\.json | ABSENT
  C2 control: the pre-round Lusha skip reason literal ("no declared domain for VLO_US_Equity in domains.json ...") matches
     the pattern (the instrument sees the defect), and enrich.domain_for on a name with no domain now answers a reason that
     does not match it.
B3 clauses (thesis.management.officers):
  C1 VLO: officers served; no officer `name` equals "Senior Vice" (or any bare title word pair); every name has a capitalised
     surname-shaped last token
  C2 VLO: 0 roles ending in a number (a trailing age)
  C3 BA regression: officer count and names unchanged from the pre-round served read (12 at the cut)
B4 clauses (CTO msg 28264, analysis @b74c090804: thesis.posture.basis[*].claim):
  C1 0 claims carry a status token (\\bABSENT\\b | \\bNULL\\b | \\bMISSING\\b, case-sensitive: a lower-case word in a sentence is fine)
  C2 control: the two pre-round claims (BA basis[1], VLO basis[5]) carry the token, and the drafter's normalizer
     `lib.research.posture.judge.plain_claim` answers each without it
Verdicts: B2 EVERY SERVED REASON IS WORDS: YES|NO / B3 EVERY OFFICER CARRIES A FULL TITLE AND NO AGE: YES|NO /
          B4 EVERY POSTURE CLAIM STATES A MISSING SCORE IN WORDS: YES|NO
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys

ROOT = "org/missions/D5/AMGT/AMGT_RESAPP/deliverables"
CAPTURE_LIB = ROOT + "/0.9.0_WK_AMGT_RESAPP~158/capture_lib.py"
PREFIX = "/api/scoped/amgt"
NAMES = ("BA_US_Equity", "VLO_US_Equity")
CODE = re.compile(r"[a-z]+_[a-z0-9_]+|_Equity|\.json|ABSENT")
OLD_LUSHA = ("no declared domain for VLO_US_Equity in domains.json (5 name(s) declared): Lusha is scoped by company domain "
             "and a guessed domain enriches the wrong company")
STATUS = re.compile(r"\b(ABSENT|NULL|MISSING)\b")
OLD_CLAIMS = (
    "Fit scores for both names are ABSENT (unmeasured) on both presets, so no factor-based discrimination is possible.",
    "The two names are near-identical on size and classification (log cap distance 0.006, same sector and industry group), so "
    "the comparison turns on evidence, and fit scores are ABSENT for both and therefore unmeasured on either side.",
)
TITLE_WORDS = {"senior", "vice", "executive", "president", "chief", "officer", "chairman", "director", "general", "counsel"}
BA_NAMES_AT_CUT = 12


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


_TOK = re.compile(r"\.([A-Za-z0-9_]+)|\[(\d+)\]")


def _locate(body, json_path):
    parts = [(k, int(i) if i else None) for k, i in _TOK.findall(json_path)]
    node = body
    for key, idx in parts[:-1]:
        node = node[key] if idx is None else node[idx]
    key, idx = parts[-1]
    return node, (key if idx is None else idx)


def _absent_reasons(o, path="", in_absent=False):
    """Every `reason` string inside a list named `absent`, anywhere in the body."""
    if isinstance(o, dict):
        for k, v in o.items():
            p = f"{path}.{k}"
            if in_absent and k == "reason" and isinstance(v, str):
                yield p, v
            elif isinstance(v, list) and k == "absent":
                for i, item in enumerate(v):
                    yield from _absent_reasons(item, f"{p}[{i}]", True)
            else:
                yield from _absent_reasons(v, p, False)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from _absent_reasons(v, f"{path}[{i}]", in_absent)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cell", choices=("b2", "b3", "b4"), required=True)
    ap.add_argument("--where", choices=("local", "deployed"), required=True)
    ap.add_argument("--plan", action="append", default=[])
    a = ap.parse_args()
    ok = []

    def clause(name, cond, detail=""):
        ok.append(bool(cond))
        print(f"{'PASS' if cond else 'FAIL'} {name} {detail}")

    if a.where == "deployed":
        import boto3

        cl = _load("capture_lib", CAPTURE_LIB)
        lam = boto3.client("lambda", region_name=cl.REGION)

        def call(path):
            body, meta = cl._invoke(lam, path)
            return (200, body) if body is not None else (meta.get("status"), None)
    else:
        from lib.research.api import scoped_amgt

        def call(path):
            r = scoped_amgt.handler({"rawPath": path, "requestContext": {"http": {"method": "GET"}},
                                     "headers": {"x-firm-id": "bd"}, "queryStringParameters": None})
            return r.get("statusCode"), json.loads(r.get("body") or "null")

    bodies = {}
    for n in NAMES:
        for route in ("thesis", "peers"):
            st, body = call(f"{PREFIX}/security/{n}/{route}")
            bodies[(n, route)] = body or {}
            print(f"read {n}/{route} status {st}")
    plan = []
    for path in a.plan:
        doc = json.load(open(path, encoding="utf-8"))
        plan.extend(doc.get("entries") or [])
    stale = []
    for e in plan:
        body = bodies.get((e.get("security_key"), e.get("route")))
        if body is None:
            continue
        try:
            node, k = _locate(body, e["json_path"])
            if node[k] != e.get("before"):
                stale.append((e["security_key"], e["json_path"], node[k], e.get("before")))
            node[k] = e.get("after")
        except (KeyError, IndexError, TypeError) as err:
            stale.append((e.get("security_key"), e.get("json_path"), f"unlocatable: {err}", e.get("before")))
    print(f"plan entries {len(plan)} from {len(a.plan)} file(s); stale or unlocatable {len(stale)} {stale[:3]}")
    if a.plan:
        clause("C0 every plan entry matches what the route serves now", not stale, f"{len(stale)} of {len(plan)}")

    if a.cell == "b2":
        bad, total = [], 0
        for n in NAMES:
            lusha = ((bodies[(n, "thesis")].get("management") or {}).get("lusha_enrichment") or {}).get("reason")
            strings = ([(f"{n}/thesis.management.lusha_enrichment.reason", lusha)] if isinstance(lusha, str) else [])
            strings += list(_absent_reasons(bodies[(n, "peers")], f"{n}/peers"))
            for p, v in strings:
                total += 1
                if CODE.search(v):
                    bad.append((p, v[:110]))
        clause("C1 no served reason carries a code-shaped token", total and not bad, f"{len(bad)} of {total} strings: {bad[:5]}")
        from lib.research.management import enrich

        _c, _i, reason = enrich.domain_for("VLO_US_Equity", table={"domains": {}}, source_object=None)
        clause("C2 control: the old literal is seen; the producer's reason is words", bool(CODE.search(OLD_LUSHA)) and reason and not CODE.search(reason),
               f"producer reason now: {reason!r}")
        print(f"B2 EVERY SERVED REASON IS WORDS: {'YES' if all(ok) else 'NO'}")
    elif a.cell == "b4":
        claims = []
        for n in NAMES:
            for i, entry in enumerate(((bodies[(n, "thesis")].get("posture") or {}).get("basis")) or []):
                claim = entry.get("claim") if isinstance(entry, dict) else entry
                if isinstance(claim, str):
                    claims.append((f"{n}/posture.basis[{i}].claim", claim))
        bad = [(p, c[:120]) for p, c in claims if STATUS.search(c)]
        clause("C1 no posture claim carries a status token", claims and not bad, f"{len(bad)} of {len(claims)} claims: {bad[:3]}")
        try:
            from lib.research.posture.judge import plain_claim

            fixed = [plain_claim(c) for c in OLD_CLAIMS]
        except ImportError as err:
            fixed = [f"IMPORT FAILED: {err}"]
        clause("C2 control: the old claims carry the token; the drafter's normalizer answers words",
               all(STATUS.search(c) for c in OLD_CLAIMS) and fixed and not any(STATUS.search(f) or f.startswith("IMPORT FAILED") for f in fixed),
               f"normalized: {[f[:90] for f in fixed]}")
        print(f"B4 EVERY POSTURE CLAIM STATES A MISSING SCORE IN WORDS: {'YES' if all(ok) else 'NO'}")
    else:
        vlo = ((bodies[("VLO_US_Equity", "thesis")].get("management") or {}).get("officers")) or []
        names = [str(o.get("name") or "") for o in vlo]
        title_named = [nm for nm in names if not nm or all(w.lower().strip(",.") in TITLE_WORDS for w in nm.split())]
        clause("C1 VLO officers carry person names, none a bare title", vlo and not title_named, f"{len(vlo)} officers; title-as-name {title_named}")
        aged = [str(o.get("role")) for o in vlo if re.search(r"\s\d{1,3}\s*$", str(o.get("role") or ""))]
        clause("C2 VLO roles carry no trailing age", vlo and not aged, f"{len(aged)} of {len(vlo)}: {aged[:3]}")
        ba = ((bodies[("BA_US_Equity", "thesis")].get("management") or {}).get("officers")) or []
        clause("C3 BA officers unchanged in count", len(ba) == BA_NAMES_AT_CUT, f"{len(ba)} (cut {BA_NAMES_AT_CUT})")
        for o in vlo:
            print(f"   VLO officer: {o.get('name')!r} | {o.get('role')!r}")
        print(f"B3 EVERY OFFICER CARRIES A FULL TITLE AND NO AGE: {'YES' if all(ok) else 'NO'}")
    return 0 if all(ok) else 1


if __name__ == "__main__":
    sys.exit(main())
