"""IRPT_DASHBD round 75 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2's ROUND-75 ANALYSIS @06b01d9b88, items 2 and 3.

Item 1 (the issuer's own five-day re-run) is the issuer's act and carries no order: deliverables/2.0.0_SA_COO~D2/RERUN_FIVE_DAYS_ROW_W111_S1.md.
Cells: DB-b-141 (row D2-W113-S2) every reader of the Black Diamond transactions copy in the repo, each read for whether it keys on the
transaction id; DB-b-142 (row D2-W113-S3) the comparison re-read at the cent, and the one fee row classed by the method's own rule.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  DB75-1-AC1  ~114/BD_TXN_READERS.json: search {method, files_searched (int > 0)}; readers (1 or more) each {file, line,
              keys_on_transaction_id (bool), sums_amounts (bool), what_it_serves}; reader_count == len(readers); not_keyed is exactly
              the files of the readers that sum amounts and do not key on the id; corrected == 0; s3_writes == 0.
  DB75-2-AC1  ~115/CENT_REREAD.json: segments {total 51, agree_at_cent, differ_at_cent} summing to 51; flow_days {total,
              differing_at_cent, reproduced_by_id_once, not_reproduced} with reproduced + not_reproduced == differing_at_cent;
              fee_row {transaction_type, method_rule {file, line, quote}, is_flow_by_the_method (bool), reason};
              tieout_state {total 244, classed, contested, unclassed} summing to 244, called_closed false; client_figures == 0;
              s3_writes == 0; no string holds a run of 8 or more digits.
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
        print("%s FAIL" % (cid or "DB75"))
        sys.exit(1)

    def record(rel):
        p = root / (M + rel)
        if not p.is_file():
            fail("no record %s" % rel)
        return json.loads(p.read_bytes().decode("utf-8"))

    if cid == "DB75-1-AC1":
        r = record("0.9.0_WK_IRPT_DASHBD~114/BD_TXN_READERS.json")
        s = r.get("search") or {}
        if not str(s.get("method") or "").strip() or not isinstance(s.get("files_searched"), int) or s["files_searched"] < 1:
            fail("search lacks its method or a positive files_searched")
        rd = r.get("readers") or []
        if not rd or r.get("reader_count") != len(rd):
            fail("readers empty, or reader_count %r is not %d" % (r.get("reader_count"), len(rd)))
        for x in rd:
            if not str(x.get("file") or "").strip() or not x.get("line") or not isinstance(x.get("keys_on_transaction_id"), bool) \
                    or not isinstance(x.get("sums_amounts"), bool) or not str(x.get("what_it_serves") or "").strip():
                fail("reader %r lacks its line, its two booleans or what it serves" % x.get("file"))
        want = sorted({str(x["file"]) for x in rd if x["sums_amounts"] and not x["keys_on_transaction_id"]})
        if sorted(set(r.get("not_keyed") or [])) != want:
            fail("not_keyed %r, the readers give %r" % (sorted(set(r.get("not_keyed") or [])), want))
        if r.get("corrected") != 0 or r.get("s3_writes") != 0:
            fail("corrected %r, s3_writes %r" % (r.get("corrected"), r.get("s3_writes")))
        print("OK: %d reader(s) of the copy over %d file(s) searched; %d sum amounts without keying on the transaction id; none corrected"
              % (len(rd), s["files_searched"], len(want)))
    elif cid == "DB75-2-AC1":
        r = record("0.9.0_WK_IRPT_DASHBD~115/CENT_REREAD.json")
        sg = r.get("segments") or {}
        if sg.get("total") != 51 or not isinstance(sg.get("agree_at_cent"), int) or not isinstance(sg.get("differ_at_cent"), int) \
                or sg["agree_at_cent"] + sg["differ_at_cent"] != 51:
            fail("segments %r" % sg)
        fd = r.get("flow_days") or {}
        for k in ("total", "differing_at_cent", "reproduced_by_id_once", "not_reproduced"):
            if not isinstance(fd.get(k), int):
                fail("flow_days.%s missing" % k)
        if fd["reproduced_by_id_once"] + fd["not_reproduced"] != fd["differing_at_cent"]:
            fail("flow_days: reproduced + not_reproduced is not differing_at_cent")
        fr = r.get("fee_row") or {}
        mr = fr.get("method_rule") or {}
        if not str(fr.get("transaction_type") or "").strip() or not str(mr.get("file") or "").strip() or not mr.get("line") \
                or not str(mr.get("quote") or "").strip() or not isinstance(fr.get("is_flow_by_the_method"), bool) or not str(fr.get("reason") or "").strip():
            fail("fee_row lacks its type, the method's rule cited by file, line and quote, the verdict or its reason")
        ts = r.get("tieout_state") or {}
        parts = [ts.get("classed"), ts.get("contested"), ts.get("unclassed")]
        if ts.get("total") != 244 or any(not isinstance(x, int) for x in parts) or sum(parts) != 244 or ts.get("called_closed") is not False:
            fail("tieout_state %r" % ts)
        if r.get("client_figures") != 0 or r.get("s3_writes") != 0:
            fail("client_figures %r, s3_writes %r" % (r.get("client_figures"), r.get("s3_writes")))
        hits = long_digit_runs(r)
        if hits:
            fail("the record holds a run of 8 or more digits at %s" % hits[:3])
        print("OK: at the cent %d of 51 segments differ on %d flow day(s); %d reproduced by counting each id once, %d not; the fee row is a flow by the method: %s"
              % (sg["differ_at_cent"], fd["differing_at_cent"], fd["reproduced_by_id_once"], fd["not_reproduced"], fr["is_flow_by_the_method"]))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
