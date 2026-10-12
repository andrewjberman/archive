"""IRPT_DASHBD round 80 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2 msg 5878 (the severity read) and msg 5886 (the first axis renamed).

Cells: DB-b-154 how many of the 34 moved medians of 2026-10-09 are the final served price, how many of those assets are held on a
served account-day, the two over 1 percent by the same test, and whether the script path runs today; DB-b-155 the proposal's first
axis renamed for what it measures, two tokens with their census, none containing RECONCILES.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  DB80-1-AC1  ~125/MOVED_MEDIANS_SEVERITY.json: day; moved 34; final_served {count (int) or "NOT_ESTABLISHED", outranked_by_yahoo,
              outranked_by_override, basis}; held_on_served_account_day {count or "NOT_ESTABLISHED", basis}; over_one_percent
              {moved 2, final_served, held, basis}; script_path_runs_today {answer (true / false / "NOT_ESTABLISHED"), basis};
              where final_served.count is an int, count + outranked_by_yahoo + outranked_by_override + not_placed == 34;
              s3_writes 0; no string holds a run of 8 or more digits.
  DB80-2-AC1  ~121/TIMING_CLASSES_PROPOSAL.json: is_a_proposal true; the first axis is renamed (its name and its 2 values do not
              contain RECONCILES); new_tokens holds no token containing RECONCILES; token_census holds one entry per new token
              {token, pattern, files_scanned > 0, hits}; placement still sums to 51 with uncovered 0 and no cell names a
              RECONCILES token; superseded_tokens lists the two retired tokens with the ruling that retired them.
"""
import json
import re
import sys
from pathlib import Path

M = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
RUN = re.compile(r"\d{8,}")
NE = "NOT_ESTABLISHED"


def long_digit_runs(obj, name=""):
    hits = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if not str(k).endswith("sha256"):
                hits += long_digit_runs(v, name + "/" + str(k))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            hits += long_digit_runs(v, "%s/%d" % (name, i))
    elif isinstance(obj, str) and RUN.search(obj):
        hits.append(name)
    return hits


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "DB80"))
        sys.exit(1)

    def record(rel):
        p = root / (M + rel)
        if not p.is_file():
            fail("no record %s" % rel)
        return json.loads(p.read_bytes().decode("utf-8"))

    def count_or_ne(v):
        return (isinstance(v, int) and not isinstance(v, bool) and v >= 0) or v == NE

    if cid == "DB80-1-AC1":
        r = record("0.9.0_WK_IRPT_DASHBD~125/MOVED_MEDIANS_SEVERITY.json")
        if not str(r.get("day") or "").strip() or r.get("moved") != 34:
            fail("day %r, moved %r (want 34)" % (r.get("day"), r.get("moved")))
        fs = r.get("final_served") or {}
        if not count_or_ne(fs.get("count")) or not str(fs.get("basis") or "").strip():
            fail("final_served needs a count (or NOT_ESTABLISHED) and its basis")
        if isinstance(fs.get("count"), int):
            parts = [fs.get(k) for k in ("outranked_by_yahoo", "outranked_by_override", "not_placed")]
            if any(not isinstance(p, int) for p in parts) or fs["count"] + sum(parts) != 34:
                fail("final_served: count + outranked_by_yahoo + outranked_by_override + not_placed must be 34")
        h = r.get("held_on_served_account_day") or {}
        if not count_or_ne(h.get("count")) or not str(h.get("basis") or "").strip():
            fail("held_on_served_account_day needs a count (or NOT_ESTABLISHED) and its basis")
        o = r.get("over_one_percent") or {}
        if o.get("moved") != 2 or not count_or_ne(o.get("final_served")) or not count_or_ne(o.get("held")) or not str(o.get("basis") or "").strip():
            fail("over_one_percent needs moved 2, final_served, held and its basis")
        s = r.get("script_path_runs_today") or {}
        if s.get("answer") not in (True, False, NE) or not str(s.get("basis") or "").strip():
            fail("script_path_runs_today needs an answer and its basis")
        if r.get("s3_writes") != 0:
            fail("s3_writes %r" % r.get("s3_writes"))
        hits = long_digit_runs(r)
        if hits:
            fail("the record holds a run of 8 or more digits at %s" % hits[:3])
        print("OK: of 34 moved medians, final served %s, held on a served account-day %s; over 1 percent: final %s, held %s; the script path runs today: %s"
              % (fs["count"], h["count"], o["final_served"], o["held"], s["answer"]))
    elif cid == "DB80-2-AC1":
        r = record("0.9.0_WK_IRPT_DASHBD~121/TIMING_CLASSES_PROPOSAL.json")
        if r.get("is_a_proposal") is not True:
            fail("is_a_proposal %r" % r.get("is_a_proposal"))
        axes = r.get("axes") or []
        if len(axes) != 2:
            fail("%d axes, want 2" % len(axes))
        first = [a for a in axes if "TIMING" not in str(a.get("name") or "").upper()]
        if len(first) != 1:
            fail("want exactly one axis that is not the TIMING axis")
        a = first[0]
        vals = [str(v) for v in (a.get("values") or [])]
        if "RECONCILES" in str(a.get("name") or "").upper() or len(vals) != 2 or any("RECONCILES" in v.upper() for v in vals):
            fail("the first axis keeps RECONCILES in its name or values, or does not hold exactly 2 values: %r %r" % (a.get("name"), vals))
        new = [str(t) for t in (r.get("new_tokens") or [])]
        if not new or any("RECONCILES" in t.upper() for t in new) or any(v not in new for v in vals):
            fail("new_tokens holds a RECONCILES token or lacks the two renamed values")
        tc = r.get("token_census") or []
        if sorted(str(t.get("token")) for t in tc) != sorted(set(new)):
            fail("token_census does not hold one entry per new token")
        for t in tc:
            if not str(t.get("pattern") or "").strip() or not isinstance(t.get("files_scanned"), int) or t["files_scanned"] < 1 or not isinstance(t.get("hits"), int):
                fail("token %r lacks its pattern, its denominator or its hit count" % t.get("token"))
        pl = r.get("placement") or {}
        cells = pl.get("cells") or []
        if pl.get("total") != 51 or pl.get("uncovered") != 0 or sum(c.get("segments", 0) for c in cells) != 51:
            fail("placement does not place 51 of 51")
        if any("RECONCILES" in str(v).upper() for c in cells for k, v in c.items() if k != "of_which"):
            fail("a placement cell still names a RECONCILES token")
        sup = r.get("superseded_tokens") or {}
        if sorted(sup.get("tokens") or []) != ["RECONCILES_NO", "RECONCILES_YES"] or not str(sup.get("retired_by") or "").strip():
            fail("superseded_tokens must list RECONCILES_YES and RECONCILES_NO and the ruling that retired them")
        print("OK: the first axis is %s with values %s; %d new token(s) censused; 51 of 51 placed" % (a["name"], vals, len(tc)))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
