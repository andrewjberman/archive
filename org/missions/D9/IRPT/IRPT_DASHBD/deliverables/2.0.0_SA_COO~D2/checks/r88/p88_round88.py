"""IRPT_DASHBD round 88 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2 msg 6931, round-88 analysis section 4 item 2: the tie-out against Black Diamond decided by COMPUTING
both flow-timing conventions, not by a statement.

Cell: DB-b-166 (LOCAL, read-only, zero vendor calls, zero secret reads, no served byte moves).
  (a) bd_default  Black Diamond's published default (learn.bdreporting.com article 97): a positive net addition is weighted at the START of its day, a withdrawal or a day with no
                  net addition at the END: HPR = (EMV - BMV - NA) / (BMV + NA) if NA > 0, else (EMV - BMV - NA) / BMV.
  (b) end         every flow at the END of its day (the served behaviour; the vendor's on-request alternative "All End of Day Cash Flows").
The declared decision rule is in the criterion below and is not the worker's to change.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  DB88-1-AC1  <worker folder>/FLOW_CONVENTION_TIEOUT.json: tolerance_pp 0.35; conventions bd_default and end each stated with a rule and a source, bd_default citing article 97;
              code {file, sha256, tracked} where the file exists under org/missions/D9/IRPT/IRPT_DASHBD/ and hashes to the stated sha256; population {flow_segments int > 0,
              contested_51 51}; crosstab_flow and crosstab_contested_51 {both, only_bd_default, only_end, neither} summing to their populations; controls: the existing reader's
              START convention closes 50 of the contested 51 and END 0 of the 51 (reproduced by this cell's machinery); verdict in {BD_DEFAULT, END, BOTH_TIE_INDISTINGUISHABLE,
              MIXED_NEITHER_DECIDES} equal to the one the declared rule gives from crosstab_flow; a BOTH or MIXED verdict names a surprise_row; negative_arm true exactly
              when the convention not chosen misses at least one flow segment the chosen one hits (for BOTH and MIXED the arm is false); reads {vendor_calls 0, secret_reads 0,
              s3_writes 0}; served_values_changed false; no run of 8 or more digits anywhere in the record (counts only, no account id).
DECLARED RULE (flow-bearing segments that are gradable): BD_DEFAULT iff only_end == 0 and only_bd_default >= 1; END iff only_bd_default == 0 and only_end >= 1;
BOTH_TIE_INDISTINGUISHABLE iff both are 0 (the window cannot tell them apart: widen it); MIXED_NEITHER_DECIDES iff both are above 0.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

REC = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~132/FLOW_CONVENTION_TIEOUT.json"
PROJ = "org/missions/D9/IRPT/IRPT_DASHBD/"
KEYS = ("both", "only_bd_default", "only_end", "neither")
VERDICTS = ("BD_DEFAULT", "END", "BOTH_TIE_INDISTINGUISHABLE", "MIXED_NEITHER_DECIDES")


def is_int(v):
    return isinstance(v, int) and not isinstance(v, bool) and v >= 0


def rule_verdict(c):
    a, e = c["only_bd_default"], c["only_end"]
    if e == 0 and a >= 1:
        return "BD_DEFAULT"
    if a == 0 and e >= 1:
        return "END"
    if a == 0 and e == 0:
        return "BOTH_TIE_INDISTINGUISHABLE"
    return "MIXED_NEITHER_DECIDES"


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else "DB88-1-AC1"

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % cid)
        sys.exit(1)

    p = root / REC
    if not p.is_file():
        fail("no %s" % REC)
    raw = p.read_bytes().decode("utf-8")
    r = json.loads(raw)
    # a sha256 (64 hex characters) is a hash, not an identifier, and can hold a long digit run by chance: drop 64-hex tokens, then scan
    if re.search(r"\d{8,}", re.sub(r"\b[0-9a-f]{64}\b", "", raw)):
        fail("the record holds a run of 8 or more digits (counts only; no account id)")
    if r.get("tolerance_pp") != 0.35:
        fail("tolerance_pp %r" % r.get("tolerance_pp"))
    cv = r.get("conventions") or {}
    for k in ("bd_default", "end"):
        c = cv.get(k) or {}
        if not str(c.get("rule") or "").strip() or not str(c.get("source") or "").strip():
            fail("conventions.%s needs a rule and a source" % k)
    if "article/97" not in str(cv["bd_default"]["source"]):
        fail("conventions.bd_default.source must cite learn.bdreporting.com article/97")
    code = r.get("code") or {}
    f = str(code.get("file") or "")
    if not f.startswith(PROJ) or code.get("tracked") is not True or not re.fullmatch(r"[0-9a-f]{64}", str(code.get("sha256") or "")):
        fail("code %r" % code)
    if not (root / f).is_file() or hashlib.sha256((root / f).read_bytes()).hexdigest() != code["sha256"]:
        fail("code file missing or its sha256 differs from the record")
    pop = r.get("population") or {}
    if not is_int(pop.get("flow_segments")) or pop["flow_segments"] < 1 or pop.get("contested_51") != 51:
        fail("population %r" % pop)
    cf, c51 = r.get("crosstab_flow") or {}, r.get("crosstab_contested_51") or {}
    for name, c, n in (("crosstab_flow", cf, pop["flow_segments"]), ("crosstab_contested_51", c51, 51)):
        if any(not is_int(c.get(k)) for k in KEYS) or sum(c[k] for k in KEYS) != n:
            fail("%s %r does not sum to %d" % (name, c, n))
    ctl = r.get("controls") or {}
    if ctl.get("start_within_contested_51") != 50 or ctl.get("end_within_contested_51") != 0:
        fail("controls %r: the reader's known 50 of 51 under START and 0 of 51 under END must reproduce" % ctl)
    v = r.get("verdict")
    if v not in VERDICTS or v != rule_verdict(cf):
        fail("verdict %r; the declared rule gives %s from %r" % (v, rule_verdict(cf), cf))
    if v in ("BOTH_TIE_INDISTINGUISHABLE", "MIXED_NEITHER_DECIDES") and not str(r.get("surprise_row") or "").strip():
        fail("a %s verdict must name its surprise_row" % v)
    want_neg = v in ("BD_DEFAULT", "END")
    if r.get("negative_arm") is not want_neg:
        fail("negative_arm %r, expected %r for verdict %s" % (r.get("negative_arm"), want_neg, v))
    rd = r.get("reads") or {}
    if rd.get("vendor_calls") != 0 or rd.get("secret_reads") != 0 or rd.get("s3_writes") != 0:
        fail("reads %r" % rd)
    if r.get("served_values_changed") is not False:
        fail("served_values_changed %r" % r.get("served_values_changed"))
    print("OK: %d flow-bearing segments; verdict %s (only_bd_default %d, only_end %d, both %d, neither %d); controls reproduce 50 and 0 of the contested 51"
          % (pop["flow_segments"], v, cf["only_bd_default"], cf["only_end"], cf["both"], cf["neither"]))
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
