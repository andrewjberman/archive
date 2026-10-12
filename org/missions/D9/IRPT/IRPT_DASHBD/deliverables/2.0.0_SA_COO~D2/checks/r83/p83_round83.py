"""IRPT_DASHBD round 83 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2's ROUND-83 ANALYSIS @3f7c91e682, section 3: the inputs to the
flow-timing addendum. Read-only; counts and basis-point bands only.

Cells: DB-b-158 (item 1) the accounts and flow-bearing days behind the 51; DB-b-159 (item 2) the size of a change of convention, per
account-day and per served window, on a copy; DB-b-160 (item 3) how the guard's flags move; DB-b-161 (item 4) what the custodian and
Black Diamond publish about when a flow arrives. Item 5 (the 39 that close under no timing) is a member of EVERY record: `the_39`.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  DB83-1-AC1  ~127/FLOWTIME_DENOMINATOR.json: segments 51; accounts (int > 0); flow_bearing_days (int > 0); closes {end, start,
              mid, both, start_only, mid_only} ints with start_only + mid_only + both <= 51; agrees_with_record (bool) with basis.
  DB83-2-AC1  ~128/CONVENTION_CHANGE_SIZE.json: served_accounts and account_days (ints > 0); on_a_copy true; daily {end_vs_start,
              end_vs_mid} each {differing_days, bands {under_1bp, from_1_to_10bp, over_10bp}} with the bands summing to
              differing_days; windows {as_of, mtd, ytd, itd} each of the three {end_vs_start, end_vs_mid} each {accounts,
              bands} with the bands summing to accounts; s3_writes 0.
  DB83-3-AC1  ~129/GUARD_INTERPLAY.json: guard_rule {file, line (int)}; flags {FLOW_UNRECONCILED, LARGE_FLOW} each {under_end,
              under_start, under_mid, end_not_start, start_not_end, end_not_mid, mid_not_end} ints, with under_end - end_not_start
              + start_not_end == under_start and the same for mid; flag_depends_on_convention (bool) with basis; s3_writes 0.
  DB83-4-AC1  ~130/PUBLISHED_FLOW_TIMING.json: parties (2: CUSTODIAN, BLACK_DIAMOND) each {party, name, convention (START / END /
              MID / OTHER / NOT_PUBLISHED), basis, sources (1 or more) each {url, retrieved_utc, found (QUOTED /
              NOTHING_ON_FLOW_TIMING), quote (non-empty when QUOTED), where}}; a convention other than NOT_PUBLISHED needs at
              least one QUOTED source; no_login true; no_account_data_sent true; searches (1 or more).
  Every record: the_39 {count 39, accrual_class 31, unclassed 8, statement (non-empty)}; no string holds a run of 8 or more digits
  (a `url` member is excepted).
"""
import json
import re
import sys
from pathlib import Path

M = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
RUN = re.compile(r"\d{8,}")
BANDS = ("under_1bp", "from_1_to_10bp", "over_10bp")
WHERE = {
    "DB83-1-AC1": "0.9.0_WK_IRPT_DASHBD~127/FLOWTIME_DENOMINATOR.json",
    "DB83-2-AC1": "0.9.0_WK_IRPT_DASHBD~128/CONVENTION_CHANGE_SIZE.json",
    "DB83-3-AC1": "0.9.0_WK_IRPT_DASHBD~129/GUARD_INTERPLAY.json",
    "DB83-4-AC1": "0.9.0_WK_IRPT_DASHBD~130/PUBLISHED_FLOW_TIMING.json",
}


def long_digit_runs(obj, name=""):
    hits = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if not str(k).endswith("sha256") and str(k) != "url":
                hits += long_digit_runs(v, name + "/" + str(k))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            hits += long_digit_runs(v, "%s/%d" % (name, i))
    elif isinstance(obj, str) and RUN.search(obj):
        hits.append(name)
    return hits


def is_int(v):
    return isinstance(v, int) and not isinstance(v, bool) and v >= 0


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "DB83"))
        sys.exit(1)

    if cid not in WHERE:
        fail("unknown criterion %r" % cid)
    p = root / (M + WHERE[cid])
    if not p.is_file():
        fail("no record %s" % WHERE[cid])
    r = json.loads(p.read_bytes().decode("utf-8"))
    t = r.get("the_39") or {}
    if t.get("count") != 39 or t.get("accrual_class") != 31 or t.get("unclassed") != 8 or not str(t.get("statement") or "").strip():
        fail("the_39 must state 39 = 31 accrual-class + 8 unclassed, with its statement")
    hits = long_digit_runs(r)
    if hits:
        fail("the record holds a run of 8 or more digits at %s" % hits[:3])

    def banded(x, total_key, what):
        b = (x or {}).get("bands") or {}
        if not is_int((x or {}).get(total_key)) or any(not is_int(b.get(k)) for k in BANDS) or sum(b[k] for k in BANDS) != x[total_key]:
            fail("%s: the three bands must be counts summing to %s" % (what, total_key))

    if cid == "DB83-1-AC1":
        c = r.get("closes") or {}
        if r.get("segments") != 51 or not is_int(r.get("accounts")) or r["accounts"] < 1 or not is_int(r.get("flow_bearing_days")) or r["flow_bearing_days"] < 1:
            fail("segments 51, accounts and flow_bearing_days are required")
        if any(not is_int(c.get(k)) for k in ("end", "start", "mid", "both", "start_only", "mid_only")) or c["start_only"] + c["mid_only"] + c["both"] > 51:
            fail("closes %r" % c)
        if not isinstance(r.get("agrees_with_record"), bool) or not str(r.get("agrees_basis") or "").strip():
            fail("agrees_with_record and its basis are required")
        print("OK: 51 segments over %d account(s) and %d flow-bearing day(s); closes END %d, START %d, MID %d, both %d; agrees with the record: %s"
              % (r["accounts"], r["flow_bearing_days"], c["end"], c["start"], c["mid"], c["both"], r["agrees_with_record"]))
    elif cid == "DB83-2-AC1":
        if not is_int(r.get("served_accounts")) or r["served_accounts"] < 1 or not is_int(r.get("account_days")) or r["account_days"] < 1:
            fail("served_accounts and account_days are required")
        if r.get("on_a_copy") is not True or r.get("s3_writes") != 0:
            fail("on_a_copy %r, s3_writes %r" % (r.get("on_a_copy"), r.get("s3_writes")))
        d = r.get("daily") or {}
        for k in ("end_vs_start", "end_vs_mid"):
            banded(d.get(k), "differing_days", "daily." + k)
        w = r.get("windows") or {}
        if not str(w.get("as_of") or "").strip():
            fail("windows.as_of is required")
        for win in ("mtd", "ytd", "itd"):
            for k in ("end_vs_start", "end_vs_mid"):
                banded((w.get(win) or {}).get(k), "accounts", "windows.%s.%s" % (win, k))
        print("OK: %d served account(s), %d account-day(s); daily returns differing END to START on %d day(s), END to MID on %d; three windows banded at %s"
              % (r["served_accounts"], r["account_days"], d["end_vs_start"]["differing_days"], d["end_vs_mid"]["differing_days"], w["as_of"]))
    elif cid == "DB83-3-AC1":
        g = r.get("guard_rule") or {}
        if not str(g.get("file") or "").strip() or not is_int(g.get("line")):
            fail("guard_rule needs its file and line")
        f = r.get("flags") or {}
        for name in ("FLOW_UNRECONCILED", "LARGE_FLOW"):
            x = f.get(name) or {}
            keys = ("under_end", "under_start", "under_mid", "end_not_start", "start_not_end", "end_not_mid", "mid_not_end")
            if any(not is_int(x.get(k)) for k in keys):
                fail("flags.%s lacks a count" % name)
            if x["under_end"] - x["end_not_start"] + x["start_not_end"] != x["under_start"] or x["under_end"] - x["end_not_mid"] + x["mid_not_end"] != x["under_mid"]:
                fail("flags.%s: the moves do not carry under_end to under_start and under_mid" % name)
        if not isinstance(r.get("flag_depends_on_convention"), bool) or not str(r.get("depends_basis") or "").strip() or r.get("s3_writes") != 0:
            fail("flag_depends_on_convention with its basis, and s3_writes 0, are required")
        print("OK: guard at %s:%d; FLOW_UNRECONCILED END %d START %d MID %d; LARGE_FLOW END %d START %d MID %d; depends on the convention: %s"
              % (g["file"], g["line"], f["FLOW_UNRECONCILED"]["under_end"], f["FLOW_UNRECONCILED"]["under_start"], f["FLOW_UNRECONCILED"]["under_mid"],
                 f["LARGE_FLOW"]["under_end"], f["LARGE_FLOW"]["under_start"], f["LARGE_FLOW"]["under_mid"], r["flag_depends_on_convention"]))
    else:
        ps = r.get("parties") or []
        if sorted(str(x.get("party")) for x in ps) != ["BLACK_DIAMOND", "CUSTODIAN"]:
            fail("parties must be exactly CUSTODIAN and BLACK_DIAMOND")
        for x in ps:
            src = x.get("sources") or []
            if not str(x.get("name") or "").strip() or x.get("convention") not in ("START", "END", "MID", "OTHER", "NOT_PUBLISHED") \
                    or not str(x.get("basis") or "").strip() or not src:
                fail("party %r lacks its name, convention, basis or a source" % x.get("party"))
            for s in src:
                if not str(s.get("url") or "").startswith("http") or not str(s.get("retrieved_utc") or "").strip() \
                        or s.get("found") not in ("QUOTED", "NOTHING_ON_FLOW_TIMING") or not str(s.get("where") or "").strip() \
                        or (s["found"] == "QUOTED" and not str(s.get("quote") or "").strip()):
                    fail("a source of %r lacks its url, time, finding, place or quote" % x.get("party"))
            if x["convention"] != "NOT_PUBLISHED" and not any(s["found"] == "QUOTED" for s in src):
                fail("party %r names a convention with no quoted source" % x.get("party"))
        if r.get("no_login") is not True or r.get("no_account_data_sent") is not True or not (r.get("searches") or []):
            fail("no_login, no_account_data_sent and the searches made are required")
        print("OK: " + "; ".join("%s (%s): %s, %d source(s)" % (x["party"], x["name"], x["convention"], len(x["sources"])) for x in ps))
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
