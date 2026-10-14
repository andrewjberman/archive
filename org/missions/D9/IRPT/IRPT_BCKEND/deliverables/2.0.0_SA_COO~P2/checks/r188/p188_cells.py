"""IRPT_BCKEND round 188 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of two orders.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.

  IB188-1  IB-pr-525  irpt-49f-reporting-gold-lambda CENSUSED and rebuilt against its CURRENT live bytes with the Design-B stage-selection change (IB-pr-523), BUILD ONLY, with the returns baseline and the never-widen packet
    AC1  the census: built twice identical, signature and attribute mismatches not above live's and a subset of its lines, the live sha256 equals the source map's last deployed CodeSha256, the changed members exactly handler.py, nothing uploaded, the source map untouched
    AC2  the packet: Branch A (the code release, then chunked runs), Branch B, the red list, live and built sha256, both halves, rollback, the open-ledger sequencing, the CURRENT live CodeSha256, the returns proof (hash before and after), the timeout chunking, idempotence stated
    AC3  the arms, the baseline and the ledgers: four offline arms on the BUILT zip's own handler.py, the returns baseline (partition count and a digest over key and ETag lines), the open ledgers, the bound counters
  IB188-2  IB-pr-526  the IR holdings class count: per firm, how many served holdings carry a cash-type sub_asset_class but a class other than cash (the holdings the shared cash rule would move) (READ ONLY)
    AC1  per firm the served snapshot read: found or not, its business date, its node count
    AC2  the counts: cash-subclass nodes, nodes that would move, nodes already cash, the moving tickers (public symbols), consistent with each other and with the node count
    AC3  the note and the counters: what each count rests on and what was not read, no client identifier, no long digit run, the six bound counters 0
"""
import base64
import json
import re
import sys
from pathlib import Path

PROJ = "org/missions/D9/IRPT/IRPT_BCKEND/"
D = PROJ + "deliverables/"
CENSUS = D + "0.9.0_WK_IRPT_BCKEND~372/IB188-1_release_census.json"
ARMS = D + "0.9.0_WK_IRPT_BCKEND~372/IB188-1_arms_baseline_ledgers.json"
PACKET = D + "0.9.0_WK_IRPT_BCKEND~372/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-525.md"
SRCMAP = "infra/aws/lambda/ci/lambda-source-map.json"
FN = "irpt-49f-reporting-gold-lambda"
BOUND1 = ("functions_invoked", "sign_ins_made", "aws_writes_made", "rows_written", "figures_written", "vendor_requests_sent")
REC2 = D + "0.9.0_WK_IRPT_BCKEND~373/IB188-2_holdings_class_count.json"
BOUND2 = ("functions_invoked", "sign_ins_made", "aws_writes_made", "rows_written", "figures_written", "vendor_requests_sent")
ROOT = Path(".")
CID = ""


def fail(msg):
    print("FAIL: " + msg)
    print("%s FAIL" % (CID or "IB188"))
    sys.exit(1)


def load(rel):
    f = ROOT / rel
    if not f.is_file():
        fail("no %s" % rel)
    try:
        return json.loads(f.read_text(encoding="utf-8"))
    except ValueError as e:
        fail("%s is not JSON: %s" % (rel, e))


def is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)


def is_date(x):
    return isinstance(x, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", x) is not None


def b64_of_hex(h):
    return base64.b64encode(bytes.fromhex(h)).decode()


def no_long_digits(r):
    if re.search(r"(?<![0-9a-fA-F-])\d{9,}(?![0-9a-fA-F])", json.dumps(r)):
        fail("the record carries a long digit run")


def census(arm):
    if arm == "AC1":
        rec = load(CENSUS)
        fn = rec.get("functions") or []
        if len(fn) != 1 or fn[0].get("function") != FN:
            fail("functions must hold exactly %s" % FN)
        f = fn[0]
        for k in ("built_sha256", "live_sha256"):
            if not re.fullmatch(r"[0-9a-f]{64}", str(f.get(k, ""))):
                fail("%s must be 64-hex" % k)
        cur = (load(SRCMAP).get("functions") or {}).get(FN, {}).get("artifact_sha256")
        if cur != b64_of_hex(f["live_sha256"]):
            fail("live_sha256 must equal the source map's last deployed CodeSha256 for %s (%s): the census is of a STALE live otherwise" % (FN, cur))
        if f.get("built_twice_identical") is not True:
            fail("built twice identical true is required")
        for kind in ("signature", "attribute"):
            bm, lm = f.get("built_%s_mismatched" % kind), f.get("live_%s_mismatched" % kind)
            bl, ll = f.get("%s_mismatch_lines_built" % kind), f.get("%s_mismatch_lines_live" % kind)
            if not is_int(bm) or not is_int(lm) or bm > lm or not isinstance(bl, list) or not isinstance(ll, list) or len(bl) != bm or len(ll) != lm or not set(bl) <= set(ll):
                fail("%s mismatches: built must not exceed live and every built line must be a live line" % kind)
        cm = f.get("changed_members") or []
        names = sorted(str(m.get("name", "")).split("/")[-1] for m in cm)
        if names != ["handler.py"]:
            fail("the changed members must be exactly handler.py, read %s (any other member moving is a STOP, not a widening)" % names)
        for m in cm:
            if not (re.fullmatch(r"[0-9a-f]{64}", str(m.get("built_member_sha256", ""))) and m.get("built_member_sha256") == m.get("repo_blob_sha256_at_pin")):
                fail("the built member's sha256 must equal the repo blob's at its pin")
        if rec.get("uploaded") is not False or not re.fullmatch(r"[0-9a-f]{7,40}", str(rec.get("pin_commit", ""))):
            fail("uploaded false and a pin_commit are required")
        sm = rec.get("source_map") or {}
        if not (sm.get("edited") is False and re.fullmatch(r"[0-9a-f]{64}", str(sm.get("sha256_before", ""))) and sm.get("sha256_before") == sm.get("sha256_after")):
            fail("source_map: edited false, sha256 before equal to after (handler.py is a native member: no source-map row changes)")
        print("OK: %s built twice identical against the CURRENT live; changed members %s; source map untouched" % (FN, names))
    elif arm == "AC2":
        pk = ROOT / PACKET
        if not pk.is_file():
            fail("no %s" % PACKET)
        t = pk.read_text(encoding="utf-8", errors="replace")
        for need, pat in (("Branch A", r"Branch A"), ("Branch B", r"Branch B"), ("the red list", r"(?i)red list"), ("live and built sha256", r"(?i)live.{0,40}sha256|sha256.{0,40}live"),
                          ("the COO half", r"(?i)COO half"), ("the CTO half", r"(?i)CTO half"), ("rollback", r"(?i)rollback|restore the live"),
                          ("the open-ledger sequencing", r"(?i)open (deploy )?ledger"), ("the returns proof", r"(?i)hash(es)? before and after|before and after"),
                          ("returns untouched", r"(?i)returns.{0,60}(untouched|not (written|changed|touched)|unchanged)"), ("the timeout chunking", r"(?i)timeout"),
                          ("chunks", r"(?i)chunk"), ("idempotence stated", r"(?i)idempot"), ("dry_run first", r"(?i)dry.?run"), ("the 2012 floor", r"2012")):
            if not re.search(pat, t):
                fail("the packet lacks: %s" % need)
        cur = (load(SRCMAP).get("functions") or {}).get(FN, {}).get("artifact_sha256", "")
        if cur[:12] not in t:
            fail("the packet must name the CURRENT live CodeSha256 (%s...)" % cur[:12])
        if len(t) < 4000:
            fail("the packet is shorter than 4000 characters")
        print("OK: the packet is complete and names the current live CodeSha256")
    else:
        r = load(ARMS)
        led = r.get("open_ledgers_naming_the_function")
        if not isinstance(led, list):
            fail("open_ledgers_naming_the_function must be a list (empty if none)")
        for x in led:
            if not x.get("ledger") or x.get("status") not in ("OPEN", "CLOSED", "SUPERSEDED", "HELD"):
                fail("each ledger needs a name and a status OPEN/CLOSED/SUPERSEDED/HELD")
        want = {"lots_only_no_returns_calls": "no_returns_call", "default_event_unchanged": "unchanged", "malformed_stages_refused": "refused", "scheduled_event_stages_refused": "refused"}
        arms = {a.get("arm"): a.get("verdict") for a in (r.get("arms") or [])}
        if arms != want:
            fail("arms must read %s, read %s" % (want, arms))
        if r.get("arms_run_on") != "built_zip_handler_py_bytes":
            fail("arms_run_on must read built_zip_handler_py_bytes (the arms are run on the BUILT zip's own handler.py, not on the repo file)")
        b = r.get("returns_baseline") or {}
        if not (is_int(b.get("returns_partitions")) and b["returns_partitions"] >= 0 and is_int(b.get("activity_partitions")) and b["activity_partitions"] >= 0
                and re.fullmatch(r"[0-9a-f]{64}", str(b.get("listing_digest", ""))) and str(b.get("digest_of", "")).strip() and is_date(b.get("read_on"))):
            fail("returns_baseline needs integer returns_partitions and activity_partitions, a 64-hex listing_digest, digest_of (what the digest covers) and read_on (a date)")
        no_long_digits(r)
        for k in BOUND1:
            if r.get(k) != 0:
                fail("the bound counter %s must read 0, reads %r" % (k, r.get(k)))
        print("OK: four arms on the built bytes, the returns baseline, %d ledger(s), counters 0" % len(led))


def holdings(arm):
    r = load(REC2)
    firms = r.get("firms") or {}
    if sorted(firms) != ["49financial", "cottonwood", "inflection"]:
        fail("firms must hold exactly 49financial, cottonwood and inflection")
    for k, v in firms.items():
        s = v.get("snapshot_read") or {}
        if arm == "AC1":
            if not isinstance(s.get("found"), bool):
                fail("%s: snapshot_read.found must be true or false" % k)
            if s["found"] and not (is_date(s.get("business_date")) and is_int(s.get("nodes")) and s["nodes"] >= 0):
                fail("%s: a found snapshot needs a business_date and an integer node count" % k)
            if not s["found"] and not str(s.get("reason", "")).strip():
                fail("%s: a snapshot not found needs its stated reason" % k)
        elif arm == "AC2":
            if not s.get("found"):
                for key in ("cash_subclass_nodes", "would_move", "already_cash"):
                    if v.get(key) is not None:
                        fail("%s: no snapshot was found, so %s must be null" % (k, key))
                continue
            n, c, m, a = s["nodes"], v.get("cash_subclass_nodes"), v.get("would_move"), v.get("already_cash")
            if not all(is_int(x) and x >= 0 for x in (c, m, a)):
                fail("%s: cash_subclass_nodes, would_move and already_cash must be integers >= 0" % k)
            if c != m + a or c > n:
                fail("%s: cash_subclass_nodes must equal would_move + already_cash and not exceed the node count" % k)
            tk = v.get("moving_tickers")
            if not isinstance(tk, list) or len(tk) != len(set(tk)) or any(not re.fullmatch(r"[A-Z0-9.\-]{1,12}", str(x)) for x in tk):
                fail("%s: moving_tickers must be distinct public symbols (A-Z, 0-9, dot, dash, up to 12 characters)" % k)
            if (m == 0) != (len(tk) == 0):
                fail("%s: moving_tickers must be empty exactly when would_move is 0" % k)
            if len(tk) > m:
                fail("%s: more distinct moving tickers than moving nodes" % k)
        else:
            if not str(v.get("note", "")).strip():
                fail("%s: a note stating what the counts rest on and what was not read is required" % k)
    if arm == "AC2":
        ct = r.get("canonical_table")
        if ct is not None and not (isinstance(ct, dict) and is_int(ct.get("rows")) and ct["rows"] >= 0 and is_int(ct.get("cash_subclass_rows")) and ct["cash_subclass_rows"] >= 0):
            fail("canonical_table is null (not readable, with canonical_table_absence stating why) or {rows, cash_subclass_rows} integers")
        if ct is None and not str(r.get("canonical_table_absence", "")).strip():
            fail("canonical_table is null: canonical_table_absence must state why")
    if arm == "AC3":
        no_long_digits(r)
        for k in BOUND2:
            if r.get(k) != 0:
                fail("the bound counter %s must read 0, reads %r" % (k, r.get(k)))
    print("OK: %s" % {"AC1": "snapshots read for 3 firms", "AC2": "counts consistent for 3 firms", "AC3": "notes and counters"}[arm])


def main():
    global ROOT, CID
    ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    CID = sys.argv[2] if len(sys.argv) > 2 else ""
    cell, arm = CID[:7], CID[8:]
    if arm not in ("AC1", "AC2", "AC3"):
        fail("unknown criterion %r" % CID)
    if cell == "IB188-1":
        census(arm)
    elif cell == "IB188-2":
        holdings(arm)
    else:
        fail("unknown criterion %r" % CID)
    print("%s PASS" % CID)


if __name__ == "__main__":
    main()
