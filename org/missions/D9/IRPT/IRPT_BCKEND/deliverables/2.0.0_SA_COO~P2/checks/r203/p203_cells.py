"""IRPT_BCKEND workstreams ~PO round 4 and ~PY round 1 (issuer 2.0.0_SA_COO~P2) -- the checks of two READ cells.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.

  IB203-1  IB-pr-560  the Orion pairs RE-CUT (CTO msg 8127): (b) re-time the existing inf-gold-trigger into the 06:00 New York fold (no new function, no port; the silver steps stay
           chained); (a) re-run the 36 absent days through the chain's own pull steps; the manual CLIs' bronze writes retired with a message naming the chain; design record and packet
    AC1  (b): the files to change read at HEAD, the re-timing, the T-1 completeness read (measured-complete time), the CLI retirement, no new function, the silver steps chained
    AC2  (a): the 36 days and keys per feed, each read ABSENT first, through the chain's pull steps, ABSENT-AT-SOURCE, read-back, rollback, the blast radius
    AC3  the packet with its phrases and both halves UNSIGNED, the LOCAL build slices, notes, counters 0, no long digit run
  IB203-2  IB-pr-561  the IB-pr-456 release rebuilt on the live R29c bytes (CTO msg 8116): irpt-ycharts-generate's candidate rebuilt from current trunk, the pre-apply digest restated, no silent revert of release 29
    AC1  the live digest (5TRFZf6G...) and the rebuilt candidate, moved members counted with their denominator
    AC2  release 29's L3 members are not moved (no silent revert), the three ENDPOINT members compared by hash, resign needed exactly when an ENDPOINT member moved
    AC3  the restated pre-apply digest, notes, counters 0, no long digit run
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "r196"))
sys.path.insert(0, str(HERE.parent / "r200"))
import p196_cells as P6  # noqa: E402
import p200_orion as PO  # noqa: E402

D = P6.D
REC1 = D + "0.9.0_WK_IRPT_BCKEND~404/IB203-1_orion_recut_design.json"
PKT1 = D + "0.9.0_WK_IRPT_BCKEND~404/ORION_RECUT_PAIRS_PACKET_V2.md"
REC2 = D + "0.9.0_WK_IRPT_BCKEND~405/IB203-2_ycharts_generate_rebuild.json"
LIVE_DIGEST = "5TRFZf6Grgd9V9jWBVu2QDPRVbgfWBjsuuw8rtf8hRA="
R29C_MEMBERS = ("generate_installed.py", "uploads.py", "ordinary_viewer.py", "interactive_access.py")
ENDPOINT_MEMBERS = ("submission.py", "acceptance.py", "AnalysisSubmissionRequest.schema.json")
FEEDS = PO.FEEDS
fail, load, is_int, counters, no_long_digits = P6.fail, P6.load, P6.is_int, P6.counters, P6.no_long_digits


def text(x, n, what):
    PO.text(x, n, what)


# ----------------------------------------------------------------------------- IB203-1
def o1():
    r = load(REC1)
    if not re.fullmatch(r"[0-9a-f]{40}", str(r.get("base_commit", ""))):
        fail("base_commit must be a 40-hex commit")
    b = r.get("pair_b") or {}
    files = b.get("files")
    if not isinstance(files, list) or not files:
        fail("pair_b.files must name the files to change")
    for f in files:
        PO.site_ok(f, "pair_b")
    text(b.get("retiming"), 40, "pair_b.retiming (inf-gold-trigger moves into the 06:00 New York fold)")
    if "inf-gold-trigger" not in b["retiming"] or "06:00" not in b["retiming"]:
        fail("pair_b.retiming must name inf-gold-trigger and the 06:00 New York fold")
    if b.get("new_function") is not False or b.get("port") is not False:
        fail("pair_b.new_function and pair_b.port must read false: consolidate, never build alongside")
    if b.get("silver_steps_chained") is not True:
        fail("pair_b.silver_steps_chained must be true (the silver steps stay chained)")
    c = b.get("t1_completeness") or {}
    if c.get("claim") not in PO.CLAIMS:
        fail("t1_completeness.claim must be measured, inferred or absent")
    text(c.get("statement"), 40, "t1_completeness.statement (is Orion's T-1 complete by 06:00 New York; if not, the earliest measured-complete time and why)")
    if not isinstance(c.get("evidence"), list) or len(c["evidence"]) < 2:
        fail("t1_completeness needs at least two evidence lines")
    if not re.search(r"\d{1,2}:\d{2}", c["statement"]):
        fail("t1_completeness.statement must name a clock time (the earliest measured-complete time or 06:00)")
    cli = b.get("cli_retirement")
    text(cli, 40, "pair_b.cli_retirement")
    if "chain" not in cli.lower() or not re.search(r"exit", cli, re.I):
        fail("pair_b.cli_retirement must say each manual CLI exits with a message that names the chain")
    sb = b.get("schedule_builder_output")
    text(sb, 20, "pair_b.schedule_builder_output")
    if "opal_naming" not in sb:
        fail("any NEW schedule name is the builder's output (opal_naming)")
    text(b.get("trading_day_frontier"), 20, "pair_b.trading_day_frontier")
    print("OK: pair (b) as a re-timing, no new function, T-1 completeness, the CLIs retired")


def o2():
    r = load(REC1)
    a = r.get("pair_a") or {}
    feeds = a.get("feeds")
    if not isinstance(feeds, dict) or sorted(feeds) != sorted(FEEDS):
        fail("pair_a.feeds must hold %s" % ", ".join(FEEDS))
    for f in FEEDS:
        x = feeds[f]
        days = x.get("days")
        if not isinstance(days, list) or len(set(days)) != len(days) or not all(isinstance(d, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", d) for d in days):
            fail("%s: days must be distinct ISO dates" % f)
        want = {"positions": 7, "transactions": 7, "performance": 22}[f]
        if len(days) != want:
            fail("%s: %d absent trading days expected, %d listed" % (f, want, len(days)))
        keys = x.get("keys")
        if not isinstance(keys, list) or len(keys) != len(days) or not all(isinstance(k, str) and k.startswith("s3://opal-data-inf/bronze/%s/" % f) and k.endswith(".jsonl.gz") for k in keys):
            fail("%s: one flat .jsonl.gz key under s3://opal-data-inf/bronze/%s/ per day" % (f, f))
        if not is_int(x.get("requests")) or x["requests"] < 0:
            fail("%s: requests must be a count" % f)
        text(x.get("chain_step"), 6, f + ".chain_step (the chain's own pull step name)")
    if a.get("absent_beforehand_read_at_act") is not True or a.get("through_chain_steps") is not True:
        fail("every key is read ABSENT before writing, and the re-run goes through the chain's own pull steps")
    for k, n in (("read_back", 30), ("rollback_per_key", 30), ("absent_at_source_policy", 40)):
        text(a.get(k), n, "pair_a." + k)
    if "ABSENT-AT-SOURCE" not in a["absent_at_source_policy"] or "empty key" not in a["absent_at_source_policy"].lower():
        fail("absent_at_source_policy must say ABSENT-AT-SOURCE is recorded and an empty key is never written")
    bl = r.get("blast_radius") or {}
    if not isinstance(bl.get("writes"), list) or not bl["writes"] or not isinstance(bl.get("reads"), list) or bl.get("new_iam") not in (True, False):
        fail("blast_radius needs writes, reads and new_iam")
    if bl.get("served_values_changed") is not False or bl.get("other_dates_touched") is not False:
        fail("blast_radius.served_values_changed and other_dates_touched must read false")
    print("OK: pair (a) through the chain's own steps, per feed, ABSENT first, ABSENT-AT-SOURCE")


def o3():
    r = load(REC1)
    f = P6.ROOT / PKT1
    if not f.is_file():
        fail("no packet at %s" % PKT1)
    t = f.read_text(encoding="utf-8")
    low = t.lower()
    if len(t) < 6000:
        fail("the packet must be at least 6,000 characters")
    for need in ("never-widen", "pair (a)", "pair (b)", "blast radius", "rollback", "stop rule", "re-timing", "inf-gold-trigger", "no shadow", "supersede", "coo half", "cto half"):
        if need not in low:
            fail("the packet does not carry %r" % need)
    if len(re.findall(r"unsigned", low)) < 2:
        fail("both halves must read UNSIGNED")
    sl = r.get("build_slices")
    if not isinstance(sl, list) or len(sl) < 1:
        fail("build_slices needs at least one proposed LOCAL cell")
    for s in sl:
        if s.get("risk") != "LOCAL" or not isinstance(s.get("cell"), str) or not isinstance(s.get("files"), list) or not s["files"]:
            fail("each build slice is a LOCAL cell with the files it writes")
    counters(r)
    no_long_digits(json.dumps(r))
    no_long_digits(t)
    print("OK: the packet, both halves unsigned, the build slices, counters 0")


# ----------------------------------------------------------------------------- IB203-2
def y1():
    r = load(REC2)
    if not re.fullmatch(r"[0-9a-f]{40}", str(r.get("base_commit", ""))):
        fail("base_commit must be a 40-hex commit")
    if r.get("function") != "irpt-ycharts-generate" or r.get("live_codesha256") != LIVE_DIGEST:
        fail("function irpt-ycharts-generate with the live CodeSha256 %s (release 29 leg L3)" % LIVE_DIGEST)
    c = r.get("candidate") or {}
    if not isinstance(c.get("codesha256"), str) or not re.fullmatch(r"[A-Za-z0-9+/]{43}=", c["codesha256"]):
        fail("candidate.codesha256 must be a base64 SHA-256")
    if c["codesha256"].startswith("AHxuDf7h"):
        fail("the candidate must be REBUILT, not the stale IB-pr-456 build")
    if not is_int(c.get("moved_count")) or not is_int(c.get("total_members")) or not 0 <= c["moved_count"] <= c["total_members"] or c["total_members"] < 20:
        fail("candidate.moved_count of total_members (the denominator) must be counts")
    if not isinstance(c.get("moved_members"), list) or len(c["moved_members"]) != c["moved_count"]:
        fail("candidate.moved_members must list exactly moved_count members")
    print("OK: the live digest, the rebuilt candidate, the moved members with their denominator")


def y2():
    r = load(REC2)
    moved = {Path(m).name for m in (r.get("candidate") or {}).get("moved_members", [])}
    hit = sorted(moved & set(R29C_MEMBERS))
    if hit:
        fail("the candidate moves release 29's L3 members %r: a silent revert of live code" % hit)
    if r.get("r29c_members_preserved") is not True:
        fail("r29c_members_preserved must be true")
    em = r.get("endpoint_members")
    if not isinstance(em, dict) or sorted(em) != sorted(ENDPOINT_MEMBERS):
        fail("endpoint_members must hold %s" % ", ".join(ENDPOINT_MEMBERS))
    anyc = False
    for k, v in em.items():
        a, b = v.get("sha256_at_signing"), v.get("sha256_now")
        if not (isinstance(a, str) and isinstance(b, str) and re.fullmatch(r"[0-9a-f]{64}", a) and re.fullmatch(r"[0-9a-f]{64}", b)):
            fail("%s: both hashes must be sha256 hex" % k)
        if v.get("changed") is not (a != b):
            fail("%s: changed must equal (hashes differ)" % k)
        anyc = anyc or (a != b)
    if r.get("endpoint_bytes_moved") is not anyc or r.get("resign_needed") is not anyc:
        fail("endpoint_bytes_moved and resign_needed must both equal whether any ENDPOINT member's hash moved (%s)" % anyc)
    print("OK: no silent revert of release 29; ENDPOINT members compared by hash; re-sign exactly when one moved")


def y3():
    r = load(REC2)
    d = r.get("pre_apply_digest_restated")
    if d != LIVE_DIGEST:
        fail("pre_apply_digest_restated must be the live digest %s" % LIVE_DIGEST)
    counters(r)
    no_long_digits(json.dumps(r))
    print("OK: the pre-apply digest restated, notes, counters 0")


CHECKS = {"IB203-1-AC1": o1, "IB203-1-AC2": o2, "IB203-1-AC3": o3, "IB203-2-AC1": y1, "IB203-2-AC2": y2, "IB203-2-AC3": y3}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CHECKS:
        print("usage: p203_cells.py <repo_root> <%s>" % "|".join(CHECKS))
        sys.exit(2)
    P6.ROOT, P6.CID = Path(sys.argv[1]).resolve(), sys.argv[2]
    CHECKS[sys.argv[2]]()
    print("%s PASS" % sys.argv[2])
