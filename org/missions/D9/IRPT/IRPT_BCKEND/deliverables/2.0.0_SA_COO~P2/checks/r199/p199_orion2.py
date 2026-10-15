"""IRPT_BCKEND round 199 (workstream ~P) -- the Orion raw-producer read check IB199-4 (IB-pr-552), imported by p199_cells.py.

  IB199-4  IB-pr-552  READ: the raw producer of the Orion Inflection .jsonl.gz feeds, every day the mirror silently dropped, the re-pull cost per feed, and the 6 AM ET fold design
    AC1  the raw producer located (a site read at HEAD) or absent with the search stated; the dropped-day census per feed carries its denominator
    AC2  the re-pull cost per feed (requests, pacing, hours) and the fold design (schedule, builder names, trading-day frontier), the account-performance feed folded
    AC3  the mirror defect stated, notes, counters 0, no long digit run
"""
import json
import re

import p196_cells as P6  # noqa: E402

D = P6.D
REC = D + "0.9.0_WK_IRPT_BCKEND~396/IB199-4_orion_raw_producer_read.json"
FEEDS = ("positions", "transactions", "performance")
CLAIMS = ("measured", "inferred", "absent")
fail, load, is_int, counters, no_long_digits, git_show = P6.fail, P6.load, P6.is_int, P6.counters, P6.no_long_digits, P6.git_show


def c1():
    r = load(REC)
    if not re.fullmatch(r"[0-9a-f]{40}", str(r.get("base_commit", ""))):
        fail("base_commit must be a 40-hex commit")
    p = r.get("raw_producer") or {}
    if p.get("claim") not in CLAIMS or not isinstance(p.get("statement"), str) or len(p["statement"]) < 40:
        fail("raw_producer needs a claim (%s) and a statement" % "/".join(CLAIMS))
    ev = p.get("evidence")
    if not isinstance(ev, list) or len(ev) < 2 or not all(isinstance(x, str) and len(x) > 20 for x in ev):
        fail("raw_producer needs at least two evidence lines (for 'absent': what was searched and where)")
    if p["claim"] == "measured":
        s = p.get("site") or {}
        src = git_show("HEAD", s.get("path", "")) if s.get("path") else None
        if src is None or not is_int(s.get("line")) or not isinstance(s.get("identifier"), str) or not s["identifier"]:
            fail("a measured producer needs a site path, line and identifier at HEAD")
        lines = src.decode("utf-8", "replace").splitlines()
        if s["line"] < 1 or s["line"] > len(lines) or s["identifier"] not in lines[s["line"] - 1]:
            fail("site %s:%s does not hold %r" % (s["path"], s["line"], s["identifier"]))
    cen = (r.get("parquet_census") or {}).get("feeds")
    if not isinstance(cen, dict) or sorted(cen) != sorted(FEEDS):
        fail("parquet_census.feeds must hold %s" % ", ".join(FEEDS))
    for f in FEEDS:
        c = cen[f]
        keys = ("source_keys_total", "jsonl_gz_days", "parquet_only_days", "silently_dropped_days")
        if not all(is_int(c.get(k)) and c[k] >= 0 for k in keys) or not isinstance(c.get("denominator_note"), str) or len(c["denominator_note"]) < 20:
            fail("%s: the census needs %s as counts and a denominator note" % (f, ", ".join(keys)))
        if c["silently_dropped_days"] > c["parquet_only_days"] or c["parquet_only_days"] > c["source_keys_total"]:
            fail("%s: dropped <= parquet-only <= total source keys" % f)
    if cen["positions"]["parquet_only_days"] < 2:
        fail("positions: the two known gap days (2026-07-01, 2026-09-28) are parquet-only, so at least 2")
    print("OK: the raw producer, the dropped-day census with denominators")


def c2():
    r = load(REC)
    cost = r.get("cost") or {}
    if sorted(cost) != sorted(FEEDS):
        fail("cost must hold %s" % ", ".join(FEEDS))
    for f in FEEDS:
        c = cost[f]
        if not is_int(c.get("requests")) or c["requests"] < 0 or c.get("claim") not in CLAIMS or not isinstance(c.get("pacing"), str) or len(c["pacing"]) < 15:
            fail("%s: cost needs requests, pacing words and a claim" % f)
        if not isinstance(c.get("hours"), (int, float)) or isinstance(c.get("hours"), bool) or c["hours"] < 0:
            fail("%s: cost needs hours" % f)
    fd = r.get("fold_design") or {}
    for k in ("schedule", "builder_names", "trading_day_frontier"):
        if not isinstance(fd.get(k), str) or len(fd[k]) < 20:
            fail("fold_design.%s must be stated" % k)
    if "opal_naming" not in fd["builder_names"]:
        fail("fold_design.builder_names must come from lib/opal_naming.py name()/address(), not typed")
    if not isinstance(fd.get("covers_feeds"), list) or not set(FEEDS) <= set(fd["covers_feeds"]):
        fail("fold_design.covers_feeds must include the three feeds")
    i2 = r.get("i2_feed") or {}
    if i2.get("claim") not in CLAIMS or not isinstance(i2.get("statement"), str) or len(i2["statement"]) < 30:
        fail("i2_feed: the account-performance feed ~I2 may add must be stated, with a claim")
    print("OK: the re-pull cost per feed, the fold design, the ~I2 feed")


def c3():
    r = load(REC)
    m = r.get("mirror_defect") or {}
    if m.get("claim") not in CLAIMS or not isinstance(m.get("statement"), str) or len(m["statement"]) < 40:
        fail("mirror_defect must state whether a format the mirror ignores is a defect to fix at the mirror, with a claim")
    counters(r)
    no_long_digits(json.dumps(r))
    print("OK: the mirror defect, notes, counters 0")


CHECKS = {"IB199-4-AC1": c1, "IB199-4-AC2": c2, "IB199-4-AC3": c3}
