"""AMGT_RESAPP round 45, AMGT-tt-3 AC1 -- the AC4 sample is chosen against the criterion's FULL clause set.
Reads deliverables/0.9.0_WK_AMGT_RESAPP~164/AC4_SAMPLE.json: {"members": [...]}, each member carrying security_key, clauses (a subset
of "a" named currency, "b" same value on both surfaces, "c" reads as a price), crncy, base_line (the served export's Base case line),
px_last, ratio, fixture (a repo path). Requires: the members' clauses cover a, b and c; at least 3 members and 2 currencies; at least
one member from the round-43 first-mint names; every member naming b or c carries px_last > 0, ratio == value / px_last, and a fixture
whose _provenance.captured_at is at or after 2026-09-26T11:28:27Z (the rs-2 deploy) and whose code_sha256 is a string; the fixture
carries the six route keys ui-contract-check.mjs reads, and its thesis's model_cases.base is SERVED at the member's value.
usage (repo root): python <this>"""
import json
import re
import sys
from pathlib import Path

P = Path("org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~164/AC4_SAMPLE.json")
FIRST_MINT = {"AMD_US_Equity", "GOOGL_US_Equity", "LLY_US_Equity", "PWR_US_Equity", "UNH_US_Equity"}   # round 43 rr-1's five
ROUTES = ["/api/scoped/amgt/security/BA_US_Equity/thesis", "/api/scoped/amgt/watchlist",
          "/api/scoped/amgt/lead-panel/rankings/trending/chatter", "/api/scoped/amgt/lead-panel/timeseries/trending/chatter",
          "/api/scoped/amgt/security/BA_US_Equity/overlay", "/api/scoped/amgt/security/BA_US_Equity/peers"]
if not P.exists():
    print("FAIL: no sample at %s" % P)
    sys.exit(1)
members = json.loads(P.read_text(encoding="utf-8")).get("members") or []
bad, clauses, crncys, first = [], set(), set(), 0
for m in members:
    k = m.get("security_key") or "?"
    cl = set(m.get("clauses") or [])
    clauses |= cl
    crncys.add(m.get("crncy"))
    first += k in FIRST_MINT
    mv = re.search(r"SERVED -- ([-0-9.e]+) ", m.get("base_line") or "")
    if not mv:
        bad.append("%s: base_line carries no SERVED value" % k)
        continue
    val = float(mv.group(1))
    if cl & {"b", "c"}:
        px = m.get("px_last")
        if not isinstance(px, (int, float)) or px <= 0:
            bad.append("%s: exercises %s with no px_last" % (k, sorted(cl)))
        elif abs((m.get("ratio") or 0) - val / px) > 1e-6:
            bad.append("%s: ratio %s != value/px_last %s" % (k, m.get("ratio"), val / px))
        fx = Path(m.get("fixture") or "")
        if not fx.is_file():
            bad.append("%s: no fixture at %s" % (k, fx))
            continue
        d = json.loads(fx.read_text(encoding="utf-8"))
        prov = d.get("_provenance") or {}
        if str(prov.get("captured_at") or "") < "2026-09-26T11:28:27Z" or not isinstance(prov.get("code_sha256"), str):
            bad.append("%s: fixture provenance %r predates the rs-2 deploy or names no code_sha256" % (k, prov))
        miss = [r for r in ROUTES if r not in d]
        if miss:
            bad.append("%s: fixture lacks %s" % (k, miss))
        base = (((d.get(ROUTES[0]) or {}).get("model_cases") or {}).get("base") or {})
        if base.get("status") != "SERVED" or abs(float(base.get("value") or 0) - val) > 1e-9:
            bad.append("%s: fixture base %r does not serve the member's value %s" % (k, base.get("value"), val))
print("members %d; clauses covered %s; currencies %d; first-mint members %d; defects %d" % (
    len(members), sorted(clauses), len(crncys - {None}), first, len(bad)))
for b in bad[:12]:
    print("  " + b)
ok = len(members) >= 3 and {"a", "b", "c"} <= clauses and len(crncys - {None}) >= 2 and first >= 1 and not bad
sys.exit(0 if ok else 1)
