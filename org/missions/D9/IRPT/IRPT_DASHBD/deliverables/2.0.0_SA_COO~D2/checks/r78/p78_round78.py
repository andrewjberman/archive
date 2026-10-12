"""IRPT_DASHBD round 78 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2 rulings msg 5835 and msg 5827.

Cells: DB-b-148 the Rule 24 proposal for the tie-out's reconcile and timing classes (four postulates, a word-boundary census of each
new token, the 51 placed by subtraction, and for the 3 whether any timing closes); DB-b-149 the two price paths that take a median
over un-deduplicated rows: what each serves and to whom, and whether the median moves on one day when ids are counted once;
DB-b-150 the ids that repeat inside ONE portfolio group in the original store: counts by cause, or stated unexplained.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  DB78-1-AC1  ~121/TIMING_CLASSES_PROPOSAL.json: is_a_proposal true; axes (2) each {name, domain, values (2 or more)}; postulates has
              mece, same_grain, intent_coherence, state_coherence, each {finding, evidence}; token_census one entry per NEW token
              {token, pattern, files_scanned (int > 0), hits (int)}; placement {total 51, cells [{reconciles, timing, segments}]}
              summing to 51 with uncovered 0; the_three {any_timing_closes (bool), segments 3, stay_contested (bool)}.
  DB78-2-AC1  ~122/PRICE_PATHS_MEDIAN.json: paths (2) each {file, line, serves, to_whom, scheduled (bool)}; day; medians {compared
              (int), moved (int), unmoved (int)} with moved + unmoved == compared, or measured false with a reason; no price or
              amount value in the record; s3_writes 0; no string holds a run of 8 or more digits.
  DB78-3-AC1  ~123/SAME_GROUP_REPEATS.json: day; denominator (int > 0, the ids repeating inside one group); causes [{cause, ids,
              rule}] and unexplained {ids, why} summing to the denominator; s3_writes 0; no long digit run.
"""
import json
import re
import sys
from pathlib import Path

M = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
RUN = re.compile(r"\d{8,}")


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
        print("%s FAIL" % (cid or "DB78"))
        sys.exit(1)

    def record(rel):
        p = root / (M + rel)
        if not p.is_file():
            fail("no record %s" % rel)
        return json.loads(p.read_bytes().decode("utf-8"))

    if cid == "DB78-1-AC1":
        r = record("0.9.0_WK_IRPT_DASHBD~121/TIMING_CLASSES_PROPOSAL.json")
        if r.get("is_a_proposal") is not True:
            fail("is_a_proposal %r" % r.get("is_a_proposal"))
        axes = r.get("axes") or []
        if len(axes) != 2 or any(not str(a.get("name") or "").strip() or not str(a.get("domain") or "").strip() or len(a.get("values") or []) < 2 for a in axes):
            fail("axes: exactly two, each with a name, a declared domain and two or more values")
        po = r.get("postulates") or {}
        for k in ("mece", "same_grain", "intent_coherence", "state_coherence"):
            v = po.get(k) or {}
            if not str(v.get("finding") or "").strip() or not str(v.get("evidence") or "").strip():
                fail("postulate %s lacks its finding or evidence" % k)
        tc = r.get("token_census") or []
        new = sorted({str(v) for a in axes for v in a["values"] if str(v) in set(r.get("new_tokens") or [])})
        if not r.get("new_tokens") or sorted(str(t.get("token")) for t in tc) != sorted(set(str(x) for x in r["new_tokens"])):
            fail("token_census does not hold one entry per new token")
        for t in tc:
            if not str(t.get("pattern") or "").strip() or not isinstance(t.get("files_scanned"), int) or t["files_scanned"] < 1 or not isinstance(t.get("hits"), int):
                fail("token %r lacks its pattern, its denominator or its hit count" % t.get("token"))
        pl = r.get("placement") or {}
        cells = pl.get("cells") or []
        if pl.get("total") != 51 or pl.get("uncovered") != 0 or sum(c.get("segments", 0) for c in cells) != 51 \
                or any(not str(c.get("reconciles") or "").strip() or not str(c.get("timing") or "").strip() for c in cells):
            fail("placement does not place 51 of 51")
        th = r.get("the_three") or {}
        if th.get("segments") != 3 or not isinstance(th.get("any_timing_closes"), bool) or not isinstance(th.get("stay_contested"), bool):
            fail("the_three %r" % th)
        print("OK: a proposal over two axes with the four postulates; %d new token(s) censused (%d in the axes); 51 of 51 placed; the three: a timing closes %s"
              % (len(tc), len(new), th["any_timing_closes"]))
    elif cid == "DB78-2-AC1":
        r = record("0.9.0_WK_IRPT_DASHBD~122/PRICE_PATHS_MEDIAN.json")
        ps = r.get("paths") or []
        if len(ps) != 2:
            fail("%d path(s), want 2" % len(ps))
        for p in ps:
            if not str(p.get("file") or "").strip() or not p.get("line") or not str(p.get("serves") or "").strip() \
                    or not str(p.get("to_whom") or "").strip() or not isinstance(p.get("scheduled"), bool):
                fail("path %r lacks its line, what it serves, to whom, or scheduled" % p.get("file"))
        m = r.get("medians") or {}
        if m.get("measured") is False:
            if not str(m.get("reason") or "").strip():
                fail("medians not measured and no reason")
            tail = "not measured"
        else:
            if any(not isinstance(m.get(k), int) for k in ("compared", "moved", "unmoved")) or m["moved"] + m["unmoved"] != m["compared"] \
                    or not str(r.get("day") or "").strip():
                fail("medians %r or day missing" % m)
            tail = "%d median(s) compared on one day, %d moved" % (m["compared"], m["moved"])
        if r.get("s3_writes") != 0:
            fail("s3_writes %r" % r.get("s3_writes"))
        hits = long_digit_runs(r)
        if hits:
            fail("the record holds a run of 8 or more digits at %s" % hits[:3])
        print("OK: two price paths traced to what they serve; %s" % tail)
    elif cid == "DB78-3-AC1":
        r = record("0.9.0_WK_IRPT_DASHBD~123/SAME_GROUP_REPEATS.json")
        d = r.get("denominator")
        cs = r.get("causes")
        un = r.get("unexplained") or {}
        if not isinstance(d, int) or d < 1 or not isinstance(cs, list) or not isinstance(un.get("ids"), int) or not str(r.get("day") or "").strip():
            fail("denominator, causes, unexplained.ids or day missing")
        for c in cs:
            if not str(c.get("cause") or "").strip() or not isinstance(c.get("ids"), int) or c["ids"] < 1 or not str(c.get("rule") or "").strip():
                fail("a cause lacks its name, a positive id count or its rule")
        if sum(c["ids"] for c in cs) + un["ids"] != d:
            fail("causes and unexplained sum to %d, not %d" % (sum(c["ids"] for c in cs) + un["ids"], d))
        if un["ids"] and not str(un.get("why") or "").strip():
            fail("unexplained ids with no why")
        if r.get("s3_writes") != 0:
            fail("s3_writes %r" % r.get("s3_writes"))
        hits = long_digit_runs(r)
        if hits:
            fail("the record holds a run of 8 or more digits at %s" % hits[:3])
        print("OK: %d id(s) repeating inside one group: %d cause(s) holding %d, %d unexplained" % (d, len(cs), d - un["ids"], un["ids"]))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
