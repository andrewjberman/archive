"""AMGT-ak-6 -- the per-entry SERVED cross-check: every plan entry for a graded name reads its
`after` on the live route.

Why this exists. Three instruments cover different things and none covers this one:
  - `ak6_verify.py` C2 proves the STORED field equals `after` for all 1,188 entries. Stored, not
    served.
  - `b_served_text.py` C1/C2/C3 prove no served string carries a code-shaped token, a bare title,
    a trailing age or a status token. That is a PATTERN over the served text, not an identity.
  - `b_served_text.py` C0 would compare served against the plan per entry, but it is guarded by
    `if a.plan:` and compares against `before`, then patches memory -- it is the PRE-act
    simulation path. The TO's literal post-act invocation passes no `--plan`, so C0 is SKIPPED
    (not failed, and not vacuously passed: no C0 verdict is emitted at all).

So the link "the object I wrote is the text the route returns", per entry, is unproven by the
criteria. This closes it for the graded names, and prints the denominator it is scoped to.

  --name <KEY> ...   default BA_US_Equity, VLO_US_Equity
"""
from __future__ import annotations

import argparse
import importlib.util
import io
import json

ROOT = "org/missions/D5/AMGT/AMGT_RESAPP/deliverables"
GRADER = ROOT + "/2.0.0_SA_COO~Z/round61/checks/b_served_text.py"
PLANS = ["C:/tmp/ak6_b2_plan.json",
         ROOT + "/0.9.0_WK_AMGT_RESAPP~202/m1_officer_plan.json",
         ROOT + "/0.9.0_WK_AMGT_RESAPP~203/posture_claim_plan.json"]


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", action="append")
    a = ap.parse_args()
    names = a.name or ["BA_US_Equity", "VLO_US_Equity"]

    g = _load("b_served_text", GRADER)
    import boto3
    cl = _load("capture_lib", g.CAPTURE_LIB) if hasattr(g, "CAPTURE_LIB") else None
    lam = boto3.client("lambda", region_name=(cl.REGION if cl else "us-east-1"))

    bodies = {}
    for n in names:
        for route in ("thesis", "peers"):
            body, meta = cl._invoke(lam, "%s/security/%s/%s" % (g.PREFIX, n, route))
            bodies[(n, route)] = body or {}
            print("read %s/%s status %s" % (n, route, 200 if body is not None else meta.get("status")))

    entries = []
    for p in PLANS:
        entries += json.load(io.open(p, encoding="utf-8")).get("entries") or []
    scoped = [e for e in entries if e.get("security_key") in names]
    print("DENOMINATOR: %d plan entr(ies) total; %d for %s -- this check is scoped to those, and "
          "says NOTHING about the other %d" % (len(entries), len(scoped), names, len(entries) - len(scoped)))

    ok, bad, unloc = 0, [], []
    for e in scoped:
        body = bodies.get((e["security_key"], e.get("route")))
        if body is None:
            unloc.append((e["security_key"], e.get("route"), "no body"))
            continue
        try:
            node, k = g._locate(body, e["json_path"])
            served = node[k]
        except (KeyError, IndexError, TypeError) as err:
            unloc.append((e["security_key"], e["json_path"], "unlocatable: %s" % err))
            continue
        if served == e.get("after"):
            ok += 1
        elif served == e.get("before"):
            bad.append((e["security_key"], e["json_path"], "still serving BEFORE"))
        else:
            bad.append((e["security_key"], e["json_path"], "serves neither before nor after"))

    print("served EQUALS after : %d of %d" % (ok, len(scoped)))
    print("served still BEFORE  or other: %d %s" % (len(bad), bad[:6]))
    print("unlocatable on the route     : %d %s" % (len(unloc), unloc[:6]))
    verdict = len(scoped) > 0 and ok == len(scoped) and not bad and not unloc
    print("AK6 SERVED-EQUALS-AFTER (scoped to %s): %s" % (",".join(names), "YES" if verdict else "NO"))
    return 0 if verdict else 1


if __name__ == "__main__":
    raise SystemExit(main())
