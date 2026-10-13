"""IRPT_DASHBD round 89 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2 msg 6956, round-89 analysis section 4 item 2: a stated reason for each of
the 12 segments that neither flow convention closes, from a CLOSED LIST written before the read, each reasoned segment recomputed with its cause
corrected and closing within 0.35 pp; the rest stay UNEXPLAINED, per account, with a surprise row.

Cell: DB-b-167 (LOCAL, read-only on the stored tie-out set of worker ~108, zero vendor calls, zero secret reads, no served byte moves).

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  DB89-1-AC1  <worker folder>/NEITHER_12_REASONS.json: tolerance_pp 0.35; rule {file in the worker's folder, sha256 equal to its bytes, commit 7-40 hex,
              written_before_count true}; reasons_list equal to the closed list below, in order; code {file under org/missions/D9/IRPT/IRPT_DASHBD/, sha256
              equal to its bytes, tracked true}; population {flow_segments 88, neither_segments 12, accounts int 1..12}; by_reason six ints summing to 12;
              evidence for every reason above 0 except UNEXPLAINED: {kind "count" or "day_offsets", values non-empty ints}; corrected {reasoned, closed_within_tolerance,
              demoted_to_unexplained, combined_only}: reasoned = 12 - UNEXPLAINED = closed_within_tolerance (a reason whose correction does not close the segment
              is not a reason); uncorrected_closes_among_12 0 (control); unexplained_per_account ints >= 1 summing to UNEXPLAINED, one per account; fwd8_unmet_accounts equal to
              their number; a surprise_row naming the unexplained iff UNEXPLAINED > 0; reads {vendor_calls 0, secret_reads 0, s3_writes 0}; served_values_changed false;
              on_a_copy true; no run of 8 or more digits (sha256 and commit members excepted).
"""
import hashlib
import json
import re
import sys
from pathlib import Path

PROJ = "org/missions/D9/IRPT/IRPT_DASHBD/"
FOLDER = PROJ + "deliverables/0.9.0_WK_IRPT_DASHBD~133"
REASONS = ("MISSING_PRICE", "FLOW_ABSENT_ONE_SIDE", "FLOW_ON_NON_TRADING_DAY", "INCOME_OFF_FLOW_DAY", "BD_ACCRUED_INCOME", "UNEXPLAINED")
RUN = re.compile(r"\d{8,}")


def is_int(v):
    return isinstance(v, int) and not isinstance(v, bool) and v >= 0


def long_digit_runs(obj, name=""):
    hits = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if not str(k).endswith("sha256") and str(k) != "commit":
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
        print("%s FAIL" % (cid or "DB89"))
        sys.exit(1)

    if cid != "DB89-1-AC1":
        fail("unknown criterion %r" % cid)
    folder = root / FOLDER
    p = folder / "NEITHER_12_REASONS.json"
    if not p.is_file():
        fail("no %s/NEITHER_12_REASONS.json" % FOLDER)
    r = json.loads(p.read_bytes().decode("utf-8"))
    if r.get("tolerance_pp") != 0.35:
        fail("tolerance_pp %r" % r.get("tolerance_pp"))
    ru = r.get("rule") or {}
    rf = folder / str(ru.get("file") or "")
    if not str(ru.get("file") or "").strip() or not rf.is_file():
        fail("rule.file must name a file in the worker's folder")
    if hashlib.sha256(rf.read_bytes()).hexdigest() != ru.get("sha256"):
        fail("rule.sha256 does not equal the rule file's bytes: the rule changed after it was recorded")
    if not re.fullmatch(r"[0-9a-f]{7,40}", str(ru.get("commit") or "")) or ru.get("written_before_count") is not True:
        fail("rule.commit and written_before_count true are required")
    if tuple(r.get("reasons_list") or ()) != REASONS:
        fail("reasons_list must be the closed list %r, in order" % (REASONS,))
    code = r.get("code") or {}
    f = str(code.get("file") or "")
    if not f.startswith(PROJ) or code.get("tracked") is not True or not re.fullmatch(r"[0-9a-f]{64}", str(code.get("sha256") or "")):
        fail("code %r" % code)
    if not (root / f).is_file() or hashlib.sha256((root / f).read_bytes()).hexdigest() != code["sha256"]:
        fail("code file missing or its sha256 differs from the record")
    pop = r.get("population") or {}
    if pop.get("flow_segments") != 88 or pop.get("neither_segments") != 12 or not is_int(pop.get("accounts")) or not 1 <= pop["accounts"] <= 12:
        fail("population %r (must reproduce 88 flow segments and 12 neither-closes segments)" % pop)
    br = r.get("by_reason") or {}
    if any(not is_int(br.get(k)) for k in REASONS) or sum(br[k] for k in REASONS) != 12:
        fail("by_reason %r must be six ints summing to 12" % br)
    ev = r.get("evidence") or {}
    for k in REASONS[:-1]:
        if br[k] > 0:
            e = ev.get(k) or {}
            vals = e.get("values")
            if e.get("kind") not in ("count", "day_offsets") or not isinstance(vals, list) or not vals or any(not isinstance(x, int) or isinstance(x, bool) for x in vals):
                fail("evidence for %s must be a count or day offsets from the stored rows, as ints" % k)
    un = br["UNEXPLAINED"]
    co = r.get("corrected") or {}
    if any(not is_int(co.get(k)) for k in ("reasoned", "closed_within_tolerance", "demoted_to_unexplained", "combined_only")):
        fail("corrected %r" % co)
    if co["reasoned"] != 12 - un or co["closed_within_tolerance"] != co["reasoned"]:
        fail("every reasoned segment must close within 0.35 pp when its cause is corrected: corrected %r, UNEXPLAINED %d" % (co, un))
    if co["demoted_to_unexplained"] > un or co["combined_only"] > un:
        fail("demoted_to_unexplained and combined_only are parts of UNEXPLAINED (%d)" % un)
    if r.get("uncorrected_closes_among_12") != 0:
        fail("uncorrected_closes_among_12 %r: the 12 must reproduce as not closing" % r.get("uncorrected_closes_among_12"))
    upa = r.get("unexplained_per_account")
    if not isinstance(upa, list) or any(not isinstance(x, int) or isinstance(x, bool) or x < 1 for x in upa) or sum(upa) != un or len(upa) > pop["accounts"]:
        fail("unexplained_per_account %r must be ints >= 1 summing to UNEXPLAINED %d, one per account" % (upa, un))
    if r.get("fwd8_unmet_accounts") != len(upa):
        fail("fwd8_unmet_accounts %r, expected %d" % (r.get("fwd8_unmet_accounts"), len(upa)))
    row = str(r.get("surprise_row") or "").strip()
    if (un > 0) != bool(row):
        fail("a surprise_row naming the unexplained is required exactly when UNEXPLAINED > 0 (UNEXPLAINED %d, surprise_row %r)" % (un, row))
    rd = r.get("reads") or {}
    if rd.get("vendor_calls") != 0 or rd.get("secret_reads") != 0 or rd.get("s3_writes") != 0:
        fail("reads %r" % rd)
    if r.get("served_values_changed") is not False or r.get("on_a_copy") is not True:
        fail("served_values_changed false and on_a_copy true are required")
    hits = long_digit_runs(r)
    if hits:
        fail("the record holds a run of 8 or more digits at %s" % hits[:3])
    print("OK: 12 segments over %d account(s): %s; %d reasoned and re-closed at 0.35 pp; %d UNEXPLAINED over %d account(s)"
          % (pop["accounts"], ", ".join("%s %d" % (k, br[k]) for k in REASONS), co["reasoned"], un, len(upa)))
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
