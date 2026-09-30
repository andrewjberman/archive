"""AMGT_RESAPP round 52, AMGT-ab-3 -- every PAGE-SHAPED RESAPP outcome is mapped to the DSGN_AMGTV1 outcome that now owns its capability,
or to NONE with an ask (CTO round-51 ruling 4; fork F5 @ac5433b35b: RESAPP keeps the payloads, DSGN owns presentation).
Reads `deliverables/0.9.0_WK_AMGT_RESAPP~187/PAGE_FWD_MAP_ROUND52.json`: {"rows": [ {resapp_fwd, resapp_quote, dsgn_fwd | null,
dsgn_quote | null, relation, ask | null}, ... ]} and checks, against the two PRDs:
  - FWD-21, 22, 23, 27, 28, 29 each have exactly one row (other page-shaped outcomes may be added, each row graded the same way);
  - `resapp_quote` is VERBATIM (whitespace-normalised) in prd/AMGT_RESAPP_PRD.md, `dsgn_quote` VERBATIM in the DSGN_AMGTV1 PRD, and
    `dsgn_fwd` is an FWD id the DSGN PRD states;
  - `relation` in {covers, partly-covers, none}; a `none` or `partly-covers` row carries a non-empty `ask` (what DSGN would own, or the
    one line saying which capability is no longer promised) -- never retired silently.
usage: python <this>   (from the repo root)"""
import json
import re
import sys

MAP = "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~187/PAGE_FWD_MAP_ROUND52.json"
RESAPP = "org/missions/D5/AMGT/AMGT_RESAPP/prd/AMGT_RESAPP_PRD.md"
DSGN = "org/missions/D13/DSGN/DSGN_AMGTV1/prd/DSGN_AMGTV1_PRD.md"
REQUIRED = ["FWD-21", "FWD-22", "FWD-23", "FWD-27", "FWD-28", "FWD-29"]
RELATIONS = {"covers", "partly-covers", "none"}


def norm(s):
    return re.sub(r"\s+", " ", str(s or "")).strip()


def main():
    try:
        rows = json.load(open(MAP, encoding="utf-8")).get("rows") or []
    except FileNotFoundError:
        print("no %s" % MAP)
        print("EVERY PAGE-SHAPED OUTCOME HAS AN OWNER OR AN ASK: NO")
        return 1
    rp, dp = norm(open(RESAPP, encoding="utf-8").read()), open(DSGN, encoding="utf-8").read()
    dsgn_ids = set(re.findall(r"FWD-\d+", dp))
    dp = norm(dp)
    bad, seen = [], {}
    for r in rows:
        f = r.get("resapp_fwd")
        seen[f] = seen.get(f, 0) + 1
        if not norm(r.get("resapp_quote")) or norm(r.get("resapp_quote")) not in rp:
            bad.append("%s resapp_quote not verbatim" % f)
        rel = r.get("relation")
        if rel not in RELATIONS:
            bad.append("%s relation %r" % (f, rel))
        if rel in ("covers", "partly-covers"):
            if r.get("dsgn_fwd") not in dsgn_ids:
                bad.append("%s dsgn_fwd %r not in the DSGN PRD" % (f, r.get("dsgn_fwd")))
            if not norm(r.get("dsgn_quote")) or norm(r.get("dsgn_quote")) not in dp:
                bad.append("%s dsgn_quote not verbatim" % f)
        if rel in ("none", "partly-covers") and not norm(r.get("ask")):
            bad.append("%s %s without an ask" % (f, rel))
    for f in REQUIRED:
        if seen.get(f) != 1:
            bad.append("%s has %d rows" % (f, seen.get(f, 0)))
    for b in bad[:10]:
        print("  BAD", b)
    counts = {k: sum(1 for r in rows if r.get("relation") == k) for k in sorted(RELATIONS)}
    print("rows %d (required 6 covered: %d); relations %s" % (len(rows), sum(1 for f in REQUIRED if seen.get(f) == 1), counts))
    ok = not bad
    print("EVERY PAGE-SHAPED OUTCOME HAS AN OWNER OR AN ASK: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
