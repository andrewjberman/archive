"""Open-backlog counter: TWO numbers, never one.

WHY THIS EXISTS. "How many armed rows do I own?" got four different answers in one
session -- 26, 14, 4, 8 -- and at every pass the seat believed it had the denominator.
Each pass differed because a different subset of disposals happened to be machine-findable.

RULING R-14 settles both halves:
  * The disarm CLOCK is the REMEDIATION row's `disarm.state`, written by 3.0.0_SA_CVO at
    L9 as ARMED and advanced to DISARMED by the named owner. That is the one carrier with
    a consumer.
  * An ISSUER's mid-round disarm row is EVIDENCE that the hazard is dead. It is read when
    the CVO graduates the item. IT CLOSES NOTHING BY ITSELF.

So the honest mid-round figure is printed as a partition, never as one number:

    DISMISSED  adjudicated DISMISSED_WITH_REASON -- no remediation row, NO CLOCK BY DESIGN
    LIVE       filed ARMED, not dismissed, and the remediation clock does not read DISARMED
    PENDING    among those LIVE, the ones carrying an issuer's disarm EVIDENCE awaiting L9

NEVER ONE NUMBER MIXING THESE. A single figure either overstates the live set (counting
rows whose evidence is already filed, or rows already dismissed) or understates it
(treating an issuer's evidence as a closure, which R-14 says it is not).

R-14 named LIVE and PENDING. DISMISSED is a third category this tool added on its FIRST
REAL RUN, because without it the count read LIVE 21 where 6 of those had been dismissed by
the CVO's own adjudication row and will never receive a remediation clock -- only a
GRADUATED item does. Reported to 1.0.0_SA_CTO as a refinement of R-14, not a departure:
it splits a category rather than collapsing one, which is the ruling's own principle.

An issuer's disarm row is FOUND by its citation: R-14 requires the target in
`grounding.evidence[]` as `<channel file>@<commit>#<FULL-ID>`. This matches on the FULL id
only -- a bare short id is a defect by that ruling and is deliberately NOT matched here, so
the count surfaces the defect instead of hiding it.

LIMITS:
  1. A row with NO remediation row at all has no clock yet -- it has not reached L9. It
     counts as LIVE, which is correct, and the output says so rather than implying the
     CVO is late.
  2. It reads the channel documents, not the gate. For the DISPOSITION question (a
     different question from hazard standing) call surprise-row-gate's `_resolve_latest`.
  3. Scoped to one owner by prefix, because "mine" is the question an issuer asks.

USAGE
    python <this> --project LGIC_ENFORCE
    python <this> --project LGIC_CANON --owner 2.0.0_SA_COO
    python <this> --selftest
"""

import argparse
import glob
import io
import json
import os
import re
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), *([os.pardir] * 8)))
_FENCE_RE = re.compile(r"```json\s*(.*?)```", re.S)


def load_rows(path):
    try:
        text = io.open(path, encoding="utf-8", errors="replace").read()
    except OSError:
        return []
    rows = []
    for block in _FENCE_RE.findall(text):
        try:
            rows.extend(json.loads(block))
        except ValueError:
            continue
    return rows


def cited_targets(rows):
    """Full ids cited as `...#<FULL-ID>` in any row's grounding.evidence[].

    FULL ID ONLY, on purpose: R-14 calls a bare short id a defect, so matching one here
    would hide the very defect the ruling names.
    """
    out = {}
    for r in rows:
        ev = (r.get("grounding") or {}).get("evidence") or []
        for e in ev:
            for m in re.finditer(r"#([A-Z][A-Z0-9_]*-(?:[CW]\d*-)?S\d+)\b", str(e)):
                out.setdefault(m.group(1), set()).add(r.get("id"))
    return out


def run(project, owner):
    base = os.path.join(REPO, "org", "missions", "D14", "LGIC", project, "surprise-channel")
    inv, rem, allrows = {}, {}, []
    for p in sorted(glob.glob(os.path.join(base, "*", "*.md"))):
        rows = load_rows(p)
        allrows.extend(rows)
        bucket = rem if "remediation" in p.replace("\\", "/").lower() else inv
        for r in rows:
            if r.get("id") and r.get("id") not in bucket:
                bucket[r["id"]] = r

    mine = sorted(i for i, r in inv.items()
                  if r.get("hazard_standing") == "ARMED"
                  and str(r.get("disarm_owner", "")).startswith(owner))
    cited = cited_targets(allrows)

    # An item DISMISSED at adjudication never receives a remediation row -- only a
    # GRADUATED one does -- so it has NO CLOCK BY DESIGN and is not live. Counting it
    # LIVE overstated this project by 6 on the first real run, which is why this exists.
    adjudged = {}
    for r in allrows:
        for t in (r.get("adjudicates") or []):
            adjudged[t] = (r.get("disposition"), r.get("id"))

    live, pending, noclock, dismissed = [], [], [], []
    for i in mine:
        d = (rem.get(i) or {}).get("disarm")
        if isinstance(d, dict) and d.get("state") == "DISARMED":
            continue
        verdict, by = adjudged.get(i, (None, None))
        if verdict == "DISMISSED_WITH_REASON" and i not in rem:
            dismissed.append((i, by))
            continue
        live.append(i)
        if i in cited:
            pending.append(i)
        if not isinstance(d, dict):
            noclock.append(i)

    print("project %s, owner prefix %s" % (project, owner))
    print("  filed ARMED (a FILED count, frozen at authorship -- never the live figure): %d" % len(mine))
    print("")
    print("  DISMISSED %d  adjudicated DISMISSED_WITH_REASON, so no remediation row and NO CLOCK BY DESIGN" % len(dismissed))
    print("  LIVE     %d   clock does NOT read DISARMED" % len(live))
    print("  PENDING  %d   of those LIVE, carrying an issuer's disarm EVIDENCE awaiting L9" % len(pending))
    print("")
    for i in live:
        tag = "evidence filed by %s" % ",".join(sorted(x for x in cited[i] if x)) if i in pending else "no disarm evidence"
        clock = "no remediation row yet (not through L9)" if i in noclock else "clock ARMED"
        print("    %-24s %-34s %s" % (i, tag, clock))
    print("")
    print("  of the LIVE rows, %d have NO remediation row at all -- they have not reached L9,"
          % len(noclock))
    print("  which is a position in the loop, not a late seat.")
    print("")
    if dismissed:
        print("  DISMISSED at adjudication (no clock will ever be written for these):")
        for i, by in dismissed:
            print("    %-24s dismissed by %s" % (i, by))
        print("")
    print("R-14: an issuer's disarm row is EVIDENCE, never a clock. The clock is the")
    print("remediation row's disarm.state, advanced by the named owner.")
    return 0


def selftest():
    ok = True
    rows = [{"id": "X-S1", "grounding": {"evidence": [
        "INVESTIGATION_v1.md@abc1234567#X_PRJ-S9 -- disarmed here"]}}]
    c = cited_targets(rows)
    a1 = "X_PRJ-S9" in c
    print("CITATION  a full id in the citation form is found: %s" % a1)
    ok = ok and a1

    bare = [{"id": "X-S2", "grounding": {"evidence": ["disarms S9, see above"]}}]
    a2 = cited_targets(bare) == {}
    print("BARE ID   a bare short id is NOT matched (R-14 calls it a defect): %s" % a2)
    ok = ok and a2

    w = [{"id": "X-S3", "grounding": {"evidence": ["INVESTIGATION_v1.md@dead123456#X_PRJ-W1-S4"]}}]
    a3 = "X_PRJ-W1-S4" in cited_targets(w)
    print("WORKER ID a worker-shaped id (W1-S4) is found: %s" % a3)
    ok = ok and a3

    a4 = cited_targets([{"id": "X-S5"}]) == {}
    print("NO EVIDENCE a row with no grounding yields nothing, no crash: %s" % a4)
    ok = ok and a4

    a5 = load_rows(os.path.join(REPO, "no", "such", "file.md")) == []
    print("MISSING   an absent channel file returns empty, not an exception: %s" % a5)
    ok = ok and a5

    print("SELFTEST: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--project")
    ap.add_argument("--owner", default="2.0.0_SA_COO")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.project:
        ap.error("--project is required unless --selftest")
    return run(a.project, a.owner)


if __name__ == "__main__":
    sys.exit(main())
