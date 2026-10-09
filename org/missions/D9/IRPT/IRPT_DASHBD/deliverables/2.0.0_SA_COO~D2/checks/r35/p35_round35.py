"""IRPT_DASHBD round 35 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2's round-34 ADDENDUM 3 @fde009aab3 (on ADJUDICATION_v19): the
withheld activity-and-lot release proceeds to its never-widen pair. S31 and S33 are MET on the pandas 2.2.3 kit (7,604 accounts, 447 s,
1,500.7 of 2,048 MB); S33 holds only if the packet prints the run's refusal count as 0. S32 is MET only on ONE read the packet carries:
classify_and_sum output on 2.2.3 equal to its tested-version output on the same fixture, or the differences named. The round-26 packet
(deliverables/0.9.0_WK_IRPT_DASHBD~23/NEVER_WIDEN_PACKET_ACTIVITY_LOT_RELEASE.md) pins its file list at efeb21df71; the lots producer and
contracts changed since (DB-b-47, -48, -52, -55), so the packet is re-cut at HEAD.

Usage: python <this file> <repo_root> <criterion_id>
  DB35-1-AC1  S32_READ_E1.json: `runtime_kit` {python 3.12.x, pandas "2.2.3", numpy "1.26.4", pyarrow "14.0.2"} and `runtime_tested`
              {pandas != "2.2.3"} read from each process; `classify_and_sum` {fixture, equal (bool), differences (list)} with equal iff
              differences is empty; `returns_table` {old_pin "bc50d5711e", sha256_old_pin, sha256_head, identical (bool)} with identical
              iff the two sha256 match; `db_b_43_test` on the kit (AMENDMENT 1, issuer, 2026-10-09 ~03:1xZ): `served_default`
              {passed (int > 0), failed == 0} -- the test bodies with `future.infer_string` left at pandas 2.2.3's default, the mode the
              served runtime runs in (account_activity_lots.set_served_runtime() forces it off; the returns path never sets it) -- and
              `forced_option_on` {passed, failed, note} recorded as measured (the test forces the pandas-3 mode, experimental on 2.2.3;
              row W46-S1). Base: FAIL.
  DB35-1-AC2  `full_run` on the kit: population_count >= 7,000, accounts_run equal, `refusals` (the count of REFUSED / LOTS_SKIPPED /
              CLASS_SKIPPED lines in its log) an integer, lots_stage_completed true; `s33_holds` == (refusals == 0). Base: FAIL.
  DB35-2-AC1  the packet NEVER_WIDEN_PACKET_ACTIVITY_LOT_RELEASE_R35.md: every row of its file-list table (a line `| `<repo_path>` ... |
              `<64-hex sha256>` |`) names a file whose sha256 at HEAD equals the printed one, at least 10 rows; it carries the sections
              "Rollback, per key", "Writers of the property", "BRANCH A", "BRANCH B", and prints the refusal count beside S33 (a line
              containing "refusals" and the integer from S32_READ_E1.json full_run.refusals). Base: FAIL.
Prints "<id> PASS" or "<id> FAIL" as the last line.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

W = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~46/"
REC = W + "S32_READ_E1.json"
PACKET = W + "NEVER_WIDEN_PACKET_ACTIVITY_LOT_RELEASE_R35.md"
OLD_PIN = "bc50d5711e"
ROW = re.compile(r"^\|\s*`([^`]+)`.*\|\s*`([0-9a-f]{64})`\s*\|\s*$", re.M)


def num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "DB35"))
        sys.exit(1)

    def load(rel):
        p = root / rel
        if not p.is_file():
            fail("no %s" % rel)
        return json.loads(p.read_bytes().decode("utf-8"))

    if cid == "DB35-1-AC1":
        r = load(REC)
        k = r.get("runtime_kit") or {}
        if k.get("pandas") != "2.2.3" or k.get("numpy") != "1.26.4" or k.get("pyarrow") != "14.0.2" or not str(k.get("python") or "").startswith("3.12."):
            fail("runtime_kit %r" % k)
        t = r.get("runtime_tested") or {}
        if not t.get("pandas") or t.get("pandas") == "2.2.3":
            fail("runtime_tested %r must be a different pandas" % t)
        c = r.get("classify_and_sum") or {}
        if not c.get("fixture") or not isinstance(c.get("differences"), list) or c.get("equal") is not (len(c["differences"]) == 0):
            fail("classify_and_sum %r: equal must hold iff differences is empty" % c)
        rt = r.get("returns_table") or {}
        if not str(rt.get("old_pin") or "").startswith(OLD_PIN) or not rt.get("sha256_old_pin") or not rt.get("sha256_head") \
                or rt.get("identical") is not (rt["sha256_old_pin"] == rt["sha256_head"]):
            fail("returns_table %r" % rt)
        d = r.get("db_b_43_test") or {}
        sd, fo = d.get("served_default") or {}, d.get("forced_option_on") or {}
        if not isinstance(sd.get("passed"), int) or sd["passed"] <= 0 or sd.get("failed") != 0:
            fail("db_b_43_test.served_default %r (the served mode must pass, 0 failed)" % sd)
        if not isinstance(fo.get("passed"), int) or not isinstance(fo.get("failed"), int) or not str(fo.get("note") or "").strip():
            fail("db_b_43_test.forced_option_on %r must be recorded with a note" % fo)
        print("OK: kit pandas 2.2.3 vs tested %s: classify_and_sum equal=%s (%d difference(s)); returns old pin vs HEAD identical=%s; DB-b-43 served mode %d passed (forced pandas-3 mode: %d/%d, recorded)" % (
            t["pandas"], c["equal"], len(c["differences"]), rt["identical"], sd["passed"], fo["passed"], fo["passed"] + fo["failed"]))
    elif cid == "DB35-1-AC2":
        f = load(REC).get("full_run") or {}
        if not isinstance(f.get("population_count"), int) or f["population_count"] < 7000 or f.get("accounts_run") != f["population_count"] \
                or not isinstance(f.get("refusals"), int) or f.get("lots_stage_completed") is not True:
            fail("full_run %r" % f)
        if f.get("s33_holds") is not (f["refusals"] == 0):
            fail("s33_holds %r but refusals %d" % (f.get("s33_holds"), f["refusals"]))
        print("OK: full run on the kit: %d accounts, refusals %d -> S33 holds: %s" % (f["population_count"], f["refusals"], f["s33_holds"]))
    elif cid == "DB35-2-AC1":
        p = root / PACKET
        if not p.is_file():
            fail("no %s" % PACKET)
        text = p.read_bytes().decode("utf-8")
        rows = ROW.findall(text)
        if len(rows) < 10:
            fail("%d file-list rows with a sha256 (need >= 10)" % len(rows))
        bad = []
        for path, sha in rows:
            f = root / path
            if not f.is_file() or hashlib.sha256(f.read_bytes()).hexdigest() != sha:
                bad.append(path)
        if bad:
            fail("%d of %d file-list rows do not match HEAD's bytes: %r" % (len(bad), len(rows), bad[:5]))
        for s in ("Rollback, per key", "Writers of the property", "BRANCH A", "BRANCH B"):
            if s not in text:
                fail("section %r missing" % s)
        n = (load(REC).get("full_run") or {}).get("refusals")
        if not isinstance(n, int) or not re.search(r"refusals\D{0,40}\b%d\b" % n, text):
            fail("the packet does not print the measured refusals (%r) beside S33" % n)
        print("OK: packet file list %d of %d rows equal HEAD's bytes; sections present; refusals %d printed" % (len(rows), len(rows), n))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
