"""AMGT_RESAPP round 77 -- the served shape the redeploy (AMGT-ba-20) must show, beyond r77_ba11's five clauses.

  python r77_served_shape.py --where local|deployed

No build cell's own check reads these on the function AFTER the hookups are live, so the issuer wrote one:
  C1 GET /freshness?view=page answers 200 with ONLY covered rows (95), each carrying the served stale flag and keyed date,
     and the body is under 150,000 bytes (the default body is 2.89 MB);
  C2 the page view's stale count is printed, and at least one row reads not stale (ruling 1: a flag on every row says nothing);
  C3 the page view's lists statement names the owner (the owner line contains "Andrew"). `local` SKIPS this clause and says so:
     the two list files are packaged into the artifact's data/ folder and are absent from a source tree;
  C4 the plain GET /freshness is unchanged in shape: 302 rows and a `reads` block (r75 c59 compares its rows);
  C5 ruling 7 on /thesis: ASML_NA_Equity's driver chart is ABSENT with refused True and a plain reason, and its segment
     breakdown serves no rows with a reason; BA_US_Equity keeps a served chart with points and segment rows (the control);
  C6 /thesis carries `passage_coverage` on BA_US_Equity with one or more sections, and on a name with no filing a plain reason.
Verdict: R77 SERVED SHAPE: YES|NO (exit 0|1). Read-only: GET-shaped direct invokes.
"""
from __future__ import annotations

import argparse
import json
import sys

FN = "opal-amgt-scoped-api"
PREFIX = "/api/scoped/amgt"


def _event(path, query=None):
    return {"rawPath": path, "requestContext": {"http": {"method": "GET"}}, "headers": {"x-firm-id": "opal"},
            "queryStringParameters": query}


def _segments(bundle):
    """The served segment breakdown: the first dict in the /thesis body carrying both `rows` and `source`."""
    stack = [bundle]
    while stack:
        node = stack.pop()
        if isinstance(node, dict):
            if "rows" in node and "source" in node and "reason" in node:
                return node
            stack.extend(node.values())
        elif isinstance(node, list):
            stack.extend(node)
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--where", choices=("local", "deployed"), required=True)
    a = ap.parse_args()
    ok = []

    def clause(name, cond, detail=""):
        ok.append(bool(cond))
        print(f"{'PASS' if cond else 'FAIL'} {name} {detail}")

    if a.where == "deployed":
        import boto3

        lam = boto3.client("lambda", region_name="us-east-1")

        def raw(event):
            return json.loads(lam.invoke(FunctionName=FN, Payload=json.dumps(event).encode())["Payload"].read())
    else:
        from lib.research.api import scoped_amgt

        def raw(event):
            return scoped_amgt.handler(event)

    def body(path, query=None):
        r = raw(_event(path, query))
        text = r.get("body") or "{}"
        try:
            return r.get("statusCode"), json.loads(text), len(text.encode("utf-8"))
        except (ValueError, TypeError):
            return r.get("statusCode"), {}, len(text)

    code, page, size = body(f"{PREFIX}/freshness", {"view": "page"})
    rows = page.get("rows") or []
    flagged = [r for r in rows if isinstance(r.get("stale"), bool)]
    dated = [r for r in rows if "keyed_date" in r]
    stale = [r for r in flagged if r["stale"]]
    print(f"   page view: status {code}; {size} B; rows {len(rows)}; with a stale flag {len(flagged)}; with keyed_date {len(dated)}; "
          f"stale {len(stale)}; not stale {len(flagged) - len(stale)}; reads present {'reads' in page}")
    clause("C1 the page view serves only covered rows with the flag and the keyed date, under 150,000 B",
           code == 200 and len(rows) == 95 and len(flagged) == 95 and len(dated) == 95 and size < 150000 and "reads" not in page,
           f"{len(rows)} rows {size} B")
    clause("C2 at least one row reads not stale", len(flagged) - len(stale) >= 1, f"stale {len(stale)} of {len(flagged)}")
    lists = page.get("lists") or {}
    owner_line = lists.get("owner_line") if isinstance(lists, dict) else None
    print(f"   owner line: {owner_line!r}; out of date: {(lists.get('out_of_date') if isinstance(lists, dict) else None)!r}")
    if a.where == "local":
        print("SKIP C3 the owner line names the owner -- the list files are packaged data, absent from a source tree")
    else:
        clause("C3 the owner line names the owner", isinstance(owner_line, str) and "Andrew" in owner_line, repr(owner_line))

    code, full, fsize = body(f"{PREFIX}/freshness")
    clause("C4 the plain /freshness is unchanged in shape", code == 200 and len(full.get("rows") or []) == 302 and "reads" in full,
           f"status {code}; rows {len(full.get('rows') or [])}; {fsize} B")

    code_a, asml, _ = body(f"{PREFIX}/security/ASML_NA_Equity/thesis")
    code_b, ba, _ = body(f"{PREFIX}/security/BA_US_Equity/thesis")
    ca, cb = asml.get("thesis_driver_chart") or {}, ba.get("thesis_driver_chart") or {}
    sa, sb = _segments(asml) or {}, _segments(ba) or {}
    print(f"   ASML NA: chart status {ca.get('status')!r} refused {ca.get('refused')!r} points {len(ca.get('points') or [])} "
          f"reason {str(ca.get('plain_reason'))[:70]!r}; segment rows {len(sa.get('rows') or [])} reason {str(sa.get('reason'))[:70]!r}")
    print(f"   BA: chart status {cb.get('status')!r} points {len(cb.get('points') or [])}; segment rows {len(sb.get('rows') or [])}")
    clause("C5 ASML NA's share-capital chart and segments are refused with a reason; BA keeps both",
           code_a == 200 and code_b == 200 and ca.get("status") == "ABSENT" and ca.get("refused") is True
           and bool(ca.get("plain_reason")) and not (ca.get("points") or []) and not (sa.get("rows") or []) and bool(sa.get("reason"))
           and len(cb.get("points") or []) >= 1 and len(sb.get("rows") or []) >= 1)

    cov = ba.get("passage_coverage") or {}
    code_n, amd, _ = body(f"{PREFIX}/security/AMD_US_Equity/thesis")
    covn = amd.get("passage_coverage") or {}
    print(f"   BA passage_coverage: sections {len(cov.get('sections') or [])} not_covered {len(cov.get('not_covered') or [])}; "
          f"AMD: sections {len(covn.get('sections') or [])} reason {str(covn.get('reason'))[:70]!r}")
    clause("C6 /thesis carries passage_coverage: sections on BA, a plain reason on a name with no filing",
           len(cov.get("sections") or []) >= 1 and code_n == 200 and (len(covn.get("sections") or []) >= 1 or bool(covn.get("reason"))))

    yes = all(ok)
    print("R77 SERVED SHAPE: " + ("YES" if yes else "NO"))
    return 0 if yes else 1


if __name__ == "__main__":
    sys.exit(main())
