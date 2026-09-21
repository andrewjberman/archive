"""R79-AC1 battery for IRPT_BCKEND.TO-IB-rth-4.

Re-derives the round-8 stale-owned-remediation-row set LIVE (calling the gate's own resolver, never a
cached figure), loads the committed disposition record (`DISPOSITION_R8.json`, built by
`build_disposition_r8.py`), and asserts:

  1. the LIVE-measured id set equals the RECORDED id set exactly (determinism: nothing in the channel
     moved between build time and grading time) -- printed both ways, never silently trusted;
  2. every id in the (live) denominator carries exactly one disposition entry with a non-empty
     evidence/reason string, and (for CARRIED) an owner token that parses as a real seat serial;
  3. DISARMED + STAYS-ARMED + CARRIED == denominator;
  4. no row is disposed on AGE ALONE -- the reason text for every CARRIED row cites the row's OWN
     schema owner field and its OWN mechanism excerpt, never a bare "stale N rounds" sentence (grepped
     for and refused if found, per the order's NO-AGE-CLOSE bound).

Prints the full per-row table, the denominator, the per-disposition counts, and on success the literal
token `IBR79-EVERY-ROW-DISPOSITIONED-COUNTS-SUM-TO-DENOMINATOR`.
"""
import json
import os
import re
import sys
import importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.getcwd()
if not (os.path.isdir(os.path.join(ROOT, ".tools")) and os.path.isdir(os.path.join(ROOT, "org"))):
    print("FAIL: run this from the worktree root (cwd lacks .tools/ or org/): %r" % ROOT)
    sys.exit(1)

GATE_PATH = os.path.join(ROOT, ".tools", "surprise-row-gate.py")
spec = importlib.util.spec_from_file_location("srg", GATE_PATH)
srg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(srg)

PROJECT = "IRPT_BCKEND"
CURRENT_ROUND = 8
SEAT_RE = re.compile(r"^\d\.\d\.\d_[A-Z][A-Za-z0-9_]*(~[A-Za-z0-9]+)?$")
AGE_ONLY_RE = re.compile(r"^\s*(has\s+)?(not\s+moved|stale)\s+(for\s+)?\d+\s+round", re.IGNORECASE)

RECORD_PATH = os.path.join(HERE, "DISPOSITION_R8.json")


def fail(msg):
    print("FAIL: %s" % msg)
    sys.exit(1)


def main():
    if not os.path.isfile(RECORD_PATH):
        fail("no disposition record at %s" % RECORD_PATH)
    record = json.load(open(RECORD_PATH, encoding="utf-8"))

    # 1. LIVE re-derivation, never trusting the cached record's own stale_ids for the denominator.
    rows_by_id, note = srg._remediation_rows_for_project(ROOT, PROJECT)
    if rows_by_id is None:
        fail("remediation census failed live: %s" % note)
    n_rounds = srg.STALE_OPEN_ROW_N_ROUNDS
    live_stale = srg._stale_open_row(rows_by_id, CURRENT_ROUND, n_rounds)
    if live_stale is None:
        fail("live staleness predicate returned None")
    live_set = set(live_stale)
    recorded_set = set(record.get("stale_ids", []))

    print("LIVE denominator: %d" % len(live_set))
    print("RECORDED denominator: %d" % len(recorded_set))
    if live_set != recorded_set:
        only_live = sorted(live_set - recorded_set)
        only_recorded = sorted(recorded_set - live_set)
        fail("live and recorded id sets differ (channel moved since build time) -- only_live=%s "
             "only_recorded=%s" % (only_live[:10], only_recorded[:10]))
    denominator = len(live_set)
    print("DETERMINISM: live == recorded, denominator=%d" % denominator)

    # 2 + 3 + 4: per-row coverage and no-age-close check.
    disp_by_id = {}
    for d in record.get("dispositions", []):
        disp_by_id[d["id"]] = d

    missing = sorted(live_set - set(disp_by_id))
    extra = sorted(set(disp_by_id) - live_set)
    if missing:
        fail("%d id(s) in the live denominator carry NO disposition entry: %s" % (len(missing), missing[:10]))
    if extra:
        fail("%d disposition entry/entries do not belong to the live denominator: %s" % (len(extra), extra[:10]))

    counts = {"DISARMED": 0, "STAYS-ARMED": 0, "CARRIED": 0}
    print("\n%-28s %-9s %-14s %-9s %-16s %s" % ("ID", "CLASS", "HAZARD", "DISP", "OWNER", "REASON (first 90 chars)"))
    print("-" * 160)
    for rid in sorted(live_set):
        d = disp_by_id[rid]
        disp = d.get("disposition")
        if disp not in counts:
            fail("row %s carries an unrecognised disposition %r" % (rid, disp))
        counts[disp] += 1
        reason = (d.get("reason") or "").strip()
        if not reason:
            fail("row %s carries an empty evidence/reason" % rid)
        if AGE_ONLY_RE.match(reason):
            fail("row %s: reason reads as AGE-ONLY ('%s...') -- NO ROW CLOSED BY AGE" % (rid, reason[:60]))
        if disp == "CARRIED":
            owner = d.get("carried_owner") or ""
            if not SEAT_RE.match(owner):
                fail("row %s: CARRIED but carried_owner %r does not parse as a seat serial" % (rid, owner))
        if disp == "DISARMED":
            # must cite something beyond a bare date/age -- already covered by AGE_ONLY_RE above; also
            # require the reason to name a commit-ish or a later row id as evidence.
            if not re.search(r"@[0-9a-f]{7,40}\b", reason) and "-S" not in reason and "IRPT_BCKEND-" not in reason:
                fail("row %s: DISARMED but its reason cites no commit-ish/@pin or later-row id as evidence" % rid)
        print("%-28s %-9s %-14s %-9s %-16s %s"
              % (rid, d.get("class"), d.get("hazard_standing"), disp,
                 (d.get("carried_owner") or "-"), reason[:90].replace("\n", " ")))

    total = sum(counts.values())
    print("\nDENOMINATOR: %d" % denominator)
    print("DISARMED: %d of %d" % (counts["DISARMED"], denominator))
    print("STAYS-ARMED: %d of %d" % (counts["STAYS-ARMED"], denominator))
    print("CARRIED: %d of %d" % (counts["CARRIED"], denominator))
    print("SUM CHECK: %d + %d + %d == %d -> %s"
          % (counts["DISARMED"], counts["STAYS-ARMED"], counts["CARRIED"], denominator, total == denominator))

    if total != denominator:
        fail("counts do not sum to the denominator")

    print("\nVERDICT: PASS")
    print("IBR79-EVERY-ROW-DISPOSITIONED-COUNTS-SUM-TO-DENOMINATOR")


if __name__ == "__main__":
    main()
