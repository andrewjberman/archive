"""IRPT_BCKEND workstream ~PO round 2 -- the Orion pairs check IB200-4 (IB-pr-556), imported by p200_cells.py.

  IB200-4  IB-pr-556  the Orion pairs: (b) the scheduled producer PORTED into the 6 AM ET fold (no second producer beside the manual CLI) and (a) the 7-day positions
           re-pull through (b)'s code path: the design record and ONE packet, both halves UNSIGNED (READ ONLY)
    AC1  the live daily writer located or absent with the search stated; pair (b): the files to change (each site read at HEAD), the port, the CLI's retirement, the schedule name from the builder, the trading-day frontier
    AC2  pair (a): every absent trading day of the three feeds (7, 7 and 22) with its flat key, absent beforehand, through (b)'s path, requests and pacing per feed, read-back, rollback per key, ABSENT-AT-SOURCE; the scope feed addendum; the blast radius
    AC3  the packet with its phrases and both halves UNSIGNED, the LOCAL build slices, notes, counters 0, no long digit run
"""
import json
import re

import p196_cells as P6  # noqa: E402

D = P6.D
REC = D + "0.9.0_WK_IRPT_BCKEND~400/IB200-4_orion_pairs_design.json"
PKT = D + "0.9.0_WK_IRPT_BCKEND~400/ORION_PAIRS_PACKET_V1.md"
DAYS = ("2026-07-01", "2026-07-03", "2026-07-04", "2026-07-05", "2026-08-06", "2026-09-28", "2026-09-29")  # positions (CTO msg 8014)
TXN_DAYS = ("2026-07-01", "2026-07-13", "2026-07-14", "2026-07-15", "2026-08-06", "2026-09-28", "2026-09-29")  # transactions (row D2-W396-S4)
FEEDS = ("positions", "transactions", "performance")
CLAIMS = ("measured", "inferred", "absent")
KEYPFX = "s3://opal-data-inf/bronze/positions/"
fail, load, is_int, counters, no_long_digits, git_show = P6.fail, P6.load, P6.is_int, P6.counters, P6.no_long_digits, P6.git_show


def site_ok(f, what):
    if not isinstance(f, dict) or not f.get("path") or not is_int(f.get("line")) or not isinstance(f.get("identifier"), str) or not f["identifier"]:
        fail("%s: each file needs path, line and the identifier on that line" % what)
    src = git_show("HEAD", f["path"])
    if src is None:
        fail("%s: %s does not exist at HEAD" % (what, f["path"]))
    lines = src.decode("utf-8", "replace").splitlines()
    if f["line"] < 1 or f["line"] > len(lines) or f["identifier"] not in lines[f["line"] - 1]:
        fail("%s: %s:%s does not hold %r" % (what, f["path"], f["line"], f["identifier"]))


def text(x, n, what):
    if not isinstance(x, str) or len(x) < n:
        fail("%s must be stated (%d+ characters)" % (what, n))


def c1():
    r = load(REC)
    if not re.fullmatch(r"[0-9a-f]{40}", str(r.get("base_commit", ""))):
        fail("base_commit must be a 40-hex commit")
    w = r.get("live_writer") or {}
    if w.get("claim") not in CLAIMS:
        fail("live_writer.claim must be measured, inferred or absent")
    text(w.get("statement"), 40, "live_writer.statement")
    ev = w.get("evidence")
    if not isinstance(ev, list) or len(ev) < 2 or not all(isinstance(x, str) and len(x) > 20 for x in ev):
        fail("live_writer needs at least two evidence lines (for 'absent': what was searched and where)")
    b = r.get("pair_b") or {}
    files = b.get("files")
    if not isinstance(files, list) or not files:
        fail("pair_b.files must name the files to change")
    for f in files:
        site_ok(f, "pair_b")
    text(b.get("port"), 40, "pair_b.port (what is ported from the manual CLI into the scheduled function)")
    cli = b.get("cli_disposition")
    text(cli, 30, "pair_b.cli_disposition")
    if not re.search(r"retire|repoint", cli, re.I):
        fail("pair_b.cli_disposition must say the manual CLI is retired or repointed in the same pair")
    if b.get("no_second_producer") is not True:
        fail("pair_b.no_second_producer must be true (no shadow pipeline)")
    sb = b.get("schedule_builder_output")
    text(sb, 20, "pair_b.schedule_builder_output")
    if "opal_naming" not in sb:
        fail("the schedule and function names are the builder's output (opal_naming), never typed")
    text(b.get("trading_day_frontier"), 20, "pair_b.trading_day_frontier")
    print("OK: the live writer, pair (b) with sites read at HEAD, the CLI retired or repointed")


def c2():
    r = load(REC)
    a = r.get("pair_a") or {}
    feeds = a.get("feeds")
    if not isinstance(feeds, dict) or sorted(feeds) != sorted(FEEDS):
        fail("pair_a.feeds must hold %s (CTO msg 8031: every absent trading day across three feeds)" % ", ".join(FEEDS))
    for f in FEEDS:
        x = feeds[f]
        days = x.get("days")
        if not isinstance(days, list) or not all(isinstance(d, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", d) for d in days) or len(set(days)) != len(days):
            fail("%s: days must be distinct ISO dates" % f)
        if f == "positions" and list(days) != list(DAYS):
            fail("positions: the seven dropped days %s" % ", ".join(DAYS))
        if f == "transactions" and list(days) != list(TXN_DAYS):
            fail("transactions: the seven absent trading days %s" % ", ".join(TXN_DAYS))
        if f == "performance" and (len(days) != 22 or not {"2026-07-01", "2026-09-28"} <= set(days)):
            fail("performance: the 22 absent trading days, including 2026-07-01 and 2026-09-28")
        keys = x.get("keys")
        if not isinstance(keys, list) or len(keys) != len(days) or not all(isinstance(k, str) and k.startswith("s3://opal-data-inf/bronze/%s/" % f) and k.endswith(".jsonl.gz") for k in keys):
            fail("%s: one flat .jsonl.gz key under s3://opal-data-inf/bronze/%s/ per day" % (f, f))
        for k, d in zip(keys, days):
            if d not in k and d.replace("-", "") not in k:
                fail("%s: key %s does not name its day %s" % (f, k, d))
        if not is_int(x.get("requests")) or x["requests"] < 0:
            fail("%s: requests must be a count" % f)
        text(x.get("pacing"), 20, f + ".pacing")
    if a.get("absent_beforehand_read_at_act") is not True or a.get("through_b_code_path") is not True:
        fail("every key is read ABSENT before writing, and the re-pull writes through (b)'s code path")
    for k, n in (("read_back", 30), ("rollback_per_key", 30), ("absent_at_source_policy", 40)):
        text(a.get(k), n, "pair_a." + k)
    if "ABSENT-AT-SOURCE" not in a["absent_at_source_policy"] or "never write an empty key" not in a["absent_at_source_policy"].lower():
        fail("absent_at_source_policy must say ABSENT-AT-SOURCE with the response status is recorded and an empty key is never written")
    sf = r.get("scope_feed_addendum") or {}
    text(sf.get("statement"), 40, "scope_feed_addendum.statement")
    for w in ("NO_GROUP", "GROUP_NO_SERIES"):
        if w not in json.dumps(sf):
            fail("scope_feed_addendum must name the absent form %s" % w)
    if sf.get("fee_basis") != "UNPROVEN":
        fail("scope_feed_addendum.fee_basis stays UNPROVEN until a fee window ties it")
    site_ok(sf.get("one_account_limit_site"), "scope_feed_addendum.one_account_limit_site")
    bl = r.get("blast_radius") or {}
    if not isinstance(bl.get("writes"), list) or not bl["writes"] or not isinstance(bl.get("reads"), list) or bl.get("new_iam") not in (True, False):
        fail("blast_radius needs writes, reads and new_iam")
    if bl.get("served_values_changed") is not False or bl.get("other_dates_touched") is not False:
        fail("blast_radius.served_values_changed and other_dates_touched must read false")
    print("OK: pair (a) per-feed days and keys, ABSENT-AT-SOURCE, the scope feed addendum, blast radius")


def c3():
    r = load(REC)
    f = P6.ROOT / PKT
    if not f.is_file():
        fail("no packet at %s" % PKT)
    t = f.read_text(encoding="utf-8")
    low = t.lower()
    if len(t) < 6000:
        fail("the packet must be at least 6,000 characters")
    for need in ("never-widen", "pair (a)", "pair (b)", "blast radius", "rollback", "stop rule", "opal_naming", "trading-day frontier", "no shadow", "coo half", "cto half"):
        if need not in low:
            fail("the packet does not carry %r" % need)
    if len(re.findall(r"unsigned", low)) < 2:
        fail("both halves must read UNSIGNED")
    sl = r.get("build_slices")
    if not isinstance(sl, list) or len(sl) < 2:
        fail("build_slices needs at least two proposed LOCAL cells")
    for s in sl:
        if s.get("risk") != "LOCAL" or not isinstance(s.get("cell"), str) or not isinstance(s.get("files"), list) or not s["files"]:
            fail("each build slice is a LOCAL cell with the files it writes")
    counters(r)
    no_long_digits(json.dumps(r))
    no_long_digits(t)
    print("OK: the packet, both halves unsigned, the build slices, counters 0")


CHECKS = {"IB200-4-AC1": c1, "IB200-4-AC2": c2, "IB200-4-AC3": c3}
