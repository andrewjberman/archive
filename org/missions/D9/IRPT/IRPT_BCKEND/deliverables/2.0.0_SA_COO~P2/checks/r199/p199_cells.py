"""IRPT_BCKEND round 199 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- the check of one order.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
It reuses the round-196 helpers (checks/r196/p196_cells.py, committed beside it).

  IB199-1  IB-pr-549  READ: the Orion Inflection gap (2026-07-01 and 2026-09-28): the pull path, why the scheduled pull skipped them, and the re-pull method (READ ONLY)
    AC1  both dates are trading days and every bronze and silver partition the re-pull would write reads EMPTY beforehand (counts, measured)
    AC2  the pull path is named stage by stage (producer file:line the check reads at HEAD, identifier on the line, trigger words), and the skip cause carries its claim
    AC3  the proposed re-pull method writes only the two dates' keys under the Orion Inflection prefixes, with read-back and per-key rollback, executed false; notes, counters 0, no long digit run

  IB199-2  IB-pr-549  the holdings-producer release APPLIED under the signed pair IB-pr-532 packet v3, per-firm pins (see p199_apply.py)
  IB199-3  IB-pr-551  hops 2-4 of the filled-report serve path as ONE never-widen pair: the design record and the packet (see p199_serve.py)
  IB199-4  IB-pr-552  READ: the Orion raw producer, every day the mirror silently dropped, the re-pull cost per feed, the 6 AM ET fold design (see p199_orion2.py)
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "r196"))
sys.path.insert(0, str(HERE.parent / "r193"))
sys.path.insert(0, str(HERE))
import p196_cells as P6  # noqa: E402
import p199_apply as PA  # noqa: E402
import p199_serve as PS  # noqa: E402
import p199_orion2 as PO  # noqa: E402

D = P6.D
REC = D + "0.9.0_WK_IRPT_BCKEND~394/IB199-1_orion_gap_read.json"
DATES = ("2026-07-01", "2026-09-28")
EMPTY_KEYS = ("bronze_positions", "bronze_performance", "bronze_transactions", "silver_fact_positions", "silver_fact_performance", "silver_fact_transactions")
KINDS = ("vendor_pull", "bronze_write", "silver_convert", "trigger")
CLAIMS = ("measured", "inferred", "absent")
PREFIX = "s3://opal-data-assets/orion/inflection/"
fail, load, is_int, counters, no_long_digits, git_show = P6.fail, P6.load, P6.is_int, P6.counters, P6.no_long_digits, P6.git_show


def c1():
    r = load(REC)
    if not re.fullmatch(r"[0-9a-f]{40}", str(r.get("base_commit", ""))):
        fail("base_commit must be a 40-hex commit")
    dates = r.get("dates")
    if not isinstance(dates, dict) or sorted(dates) != sorted(DATES):
        fail("dates must hold exactly %s" % ", ".join(DATES))
    for d in DATES:
        x = dates[d]
        if x.get("trading_day") is not True or x.get("claim") != "measured":
            fail("%s: a measured trading day" % d)
        e = x.get("empty_beforehand")
        if not isinstance(e, dict) or sorted(e) != sorted(EMPTY_KEYS):
            fail("%s: empty_beforehand needs exactly %s" % (d, ", ".join(EMPTY_KEYS)))
        for k in EMPTY_KEYS:
            if not is_int(e[k]) or e[k] != 0:
                fail("%s: %s must read 0 (the partition is empty before any re-pull), reads %r" % (d, k, e[k]))
    print("OK: both dates are trading days and every target partition reads empty")


def c2():
    r = load(REC)
    stages = (r.get("pull_path") or {}).get("stages")
    if not isinstance(stages, list) or not stages:
        fail("pull_path.stages is required")
    kinds = {s.get("kind") for s in stages}
    if "silver_convert" not in kinds or not kinds <= set(KINDS):
        fail("stages must include silver_convert and use kinds %s" % "/".join(KINDS))
    for s in stages:
        if s.get("claim") not in CLAIMS or not isinstance(s.get("trigger"), str) or len(s["trigger"]) < 15:
            fail("each stage needs a claim (%s) and trigger words" % "/".join(CLAIMS))
        if s["claim"] == "measured":
            m = re.fullmatch(r"(.+):(\d+)", s.get("producer") or "")
            src = git_show("HEAD", m.group(1)) if m else None
            ident = s.get("identifier")
            if not m or src is None or not isinstance(ident, str) or not ident:
                fail("a measured stage needs producer path:line at HEAD and the identifier on that line")
            lines = src.decode("utf-8", "replace").splitlines()
            if int(m.group(2)) > len(lines) or ident not in lines[int(m.group(2)) - 1]:
                fail("stage %s: %s does not hold %r" % (s.get("kind"), s["producer"], ident))
    c = r.get("skip_cause") or {}
    if c.get("claim") not in CLAIMS or not isinstance(c.get("statement"), str) or len(c["statement"]) < 40:
        fail("skip_cause needs a claim (%s) and a statement" % "/".join(CLAIMS))
    ev = c.get("evidence")
    if c["claim"] != "absent" and (not isinstance(ev, list) or len(ev) < 2 or not all(isinstance(x, str) and len(x) > 20 for x in ev)):
        fail("a cause that is not 'absent' needs at least two evidence lines")
    print("OK: the pull path stage by stage and the skip cause with its claim")


def c3():
    r = load(REC)
    m = r.get("repull_method") or {}
    writes = m.get("writes")
    if not isinstance(writes, list) or not writes:
        fail("repull_method.writes must list the key prefixes")
    for w in writes:
        if not isinstance(w, str) or not w.startswith(PREFIX) or not any(d in w or d.replace("-", "") in w for d in DATES):
            fail("every write prefix must sit under %s and name one of the two dates: %r" % (PREFIX, w))
    if m.get("executed") is not False or m.get("writes_only_the_two_dates") is not True:
        fail("the method is proposed only (executed false) and writes only the two dates")
    for k in ("read_back", "rollback_per_key"):
        if not isinstance(m.get(k), str) or len(m[k]) < 30:
            fail("repull_method.%s must be stated" % k)
    if not is_int(m.get("vendor_calls_needed")) or m["vendor_calls_needed"] < 0:
        fail("vendor_calls_needed must be a count")
    counters(r)
    no_long_digits(json.dumps(r))
    print("OK: the method writes only the two dates, read-back and rollback stated, counters 0")


CHECKS = {"IB199-1-AC1": c1, "IB199-1-AC2": c2, "IB199-1-AC3": c3, **PA.CHECKS, **PS.CHECKS, **PO.CHECKS}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CHECKS:
        print("usage: p199_cells.py <repo_root> <%s>" % "|".join(CHECKS))
        sys.exit(2)
    P6.ROOT, P6.CID = Path(sys.argv[1]).resolve(), sys.argv[2]
    PA.sync()
    CHECKS[sys.argv[2]]()
    print("%s PASS" % sys.argv[2])
