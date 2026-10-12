"""IRPT_DASHBD round 77 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2's ROUND-76 ANALYSIS @d70feb6d15, items 1 (second half), 3 and 4.

Items 1 (first half) and 2 were issued as round 76 on the CTO's msg 5721 (DB-b-144, DB-b-143).
Cells: DB-b-145 (item 1) the scripts that produced figures the records quote are tracked in the project's folder, or the figure is
listed as withdrawn; DB-b-146 (item 3, row D2-W113-S3) the shared code table's class for the one fee row, beside the method's rule;
DB-b-147 (item 4) what CONTESTED still means for the 51 and what would close each.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  DB77-1-AC1  ~118/FIGURE_PRODUCERS.json: figures (1 or more) each {record, figure, producer_origin, state TRACKED or WITHDRAWN};
              a TRACKED figure names tracked_as (files that exist under the worker's folder) each with a sha256 equal to the file's;
              a WITHDRAWN figure carries why; scanned {files, long_digit_runs 0}; no tracked script file holds a run of 8+ digits
              (the private evidence folder's own name excepted).
  DB77-2-AC1  ~119/FEE_ROW_CLASS.json: table {file or address, how_read}; row_class (non-empty) or "NOT_ESTABLISHED" with why;
              method_rule {file, line, quote}; agree (true / false / "NOT_ESTABLISHED"); false carries a row id; client_figures 0;
              s3_writes 0; no long digit run.
  DB77-3-AC1  ~120/CONTESTED_51_MEANING.json: denominator 51; groups [{meaning, segments, what_would_close_it}] summing to 51;
              flow_reproduces {segments_all_days_to_the_cent, segments_not} summing to 51; tieout_state {total 244, classed,
              contested, unclassed} summing to 244, called_closed false; proposal (a sentence) and proposal_is_a_ruling false.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

M = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
RUN = re.compile(r"\d{8,}")
PRIVATE_FOLDER = "_irpt_private_evidence_20261009"


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
        print("%s FAIL" % (cid or "DB77"))
        sys.exit(1)

    def record(rel):
        p = root / (M + rel)
        if not p.is_file():
            fail("no record %s" % rel)
        return json.loads(p.read_bytes().decode("utf-8"))

    if cid == "DB77-1-AC1":
        folder = root / (M + "0.9.0_WK_IRPT_DASHBD~118")
        r = record("0.9.0_WK_IRPT_DASHBD~118/FIGURE_PRODUCERS.json")
        figs = r.get("figures") or []
        if not figs:
            fail("no figures")
        tracked = withdrawn = 0
        for f in figs:
            if not str(f.get("record") or "").strip() or not str(f.get("figure") or "").strip() or not str(f.get("producer_origin") or "").strip():
                fail("a figure lacks its record, its text or its producer's origin")
            if f.get("state") == "TRACKED":
                ta = f.get("tracked_as") or []
                if not ta:
                    fail("a TRACKED figure names no file")
                for t in ta:
                    fp = folder / str(t.get("file") or "")
                    if not fp.is_file():
                        fail("tracked file %r is not in the worker's folder" % t.get("file"))
                    raw = fp.read_bytes()
                    if hashlib.sha256(raw).hexdigest() != t.get("sha256"):
                        fail("tracked file %r does not hash to its sha256" % t.get("file"))
                    # the private evidence folder's own name carries a date; it is a path, not client data
                    if RUN.search(raw.decode("utf-8", errors="replace").replace(PRIVATE_FOLDER, "")):
                        fail("tracked file %r holds a run of 8 or more digits" % t.get("file"))
                tracked += 1
            elif f.get("state") == "WITHDRAWN":
                if not str(f.get("why") or "").strip():
                    fail("a WITHDRAWN figure gives no why")
                withdrawn += 1
            else:
                fail("figure state %r" % f.get("state"))
        sc = r.get("scanned") or {}
        if not isinstance(sc.get("files"), int) or sc.get("long_digit_runs") != 0:
            fail("scanned %r" % sc)
        print("OK: %d figure(s): %d with their producer tracked in the tree, %d withdrawn; no tracked script holds a long digit run"
              % (len(figs), tracked, withdrawn))
    elif cid == "DB77-2-AC1":
        r = record("0.9.0_WK_IRPT_DASHBD~119/FEE_ROW_CLASS.json")
        t = r.get("table") or {}
        mr = r.get("method_rule") or {}
        if not str(t.get("how_read") or "").strip() or not str(mr.get("file") or "").strip() or not mr.get("line") or not str(mr.get("quote") or "").strip():
            fail("table.how_read or the method's rule (file, line, quote) is missing")
        rc = r.get("row_class")
        ag = r.get("agree")
        if not str(rc or "").strip() or ag not in (True, False, "NOT_ESTABLISHED"):
            fail("row_class %r, agree %r" % (rc, ag))
        if (rc == "NOT_ESTABLISHED") != (ag == "NOT_ESTABLISHED"):
            fail("row_class and agree must both be NOT_ESTABLISHED or neither")
        if rc == "NOT_ESTABLISHED" and not str(r.get("why") or "").strip():
            fail("NOT_ESTABLISHED without why")
        if ag is False and not str(r.get("row") or "").strip():
            fail("a disagreement names no row")
        if r.get("client_figures") != 0 or r.get("s3_writes") != 0:
            fail("client_figures %r, s3_writes %r" % (r.get("client_figures"), r.get("s3_writes")))
        hits = long_digit_runs(r)
        if hits:
            fail("the record holds a run of 8 or more digits at %s" % hits[:3])
        print("OK: the code table's class for the fee row: %s; agrees with the method's rule: %s" % (rc, ag))
    elif cid == "DB77-3-AC1":
        r = record("0.9.0_WK_IRPT_DASHBD~120/CONTESTED_51_MEANING.json")
        g = r.get("groups") or []
        if r.get("denominator") != 51 or not g:
            fail("denominator %r or no groups" % r.get("denominator"))
        for x in g:
            if not str(x.get("meaning") or "").strip() or not isinstance(x.get("segments"), int) or x["segments"] < 1 or not str(x.get("what_would_close_it") or "").strip():
                fail("a group lacks its meaning, a positive count or what would close it")
        if sum(x["segments"] for x in g) != 51:
            fail("the groups sum to %d, not 51" % sum(x["segments"] for x in g))
        fr = r.get("flow_reproduces") or {}
        if not isinstance(fr.get("segments_all_days_to_the_cent"), int) or not isinstance(fr.get("segments_not"), int) \
                or fr["segments_all_days_to_the_cent"] + fr["segments_not"] != 51:
            fail("flow_reproduces %r" % fr)
        ts = r.get("tieout_state") or {}
        parts = [ts.get("classed"), ts.get("contested"), ts.get("unclassed")]
        if ts.get("total") != 244 or any(not isinstance(x, int) for x in parts) or sum(parts) != 244 or ts.get("called_closed") is not False:
            fail("tieout_state %r" % ts)
        if not str(r.get("proposal") or "").strip() or r.get("proposal_is_a_ruling") is not False:
            fail("proposal missing, or presented as a ruling")
        print("OK: the 51 in %d group(s); the flow reproduces to the cent on every day in %d; the tie-out is not closed"
              % (len(g), fr["segments_all_days_to_the_cent"]))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
