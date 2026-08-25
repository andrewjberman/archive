"""POSITIVE CONTROL for the GLD-f-1 harness: prove it CAN return PASS.

WHY THIS EXISTS. Every run of `gldrns_f1_scheduled_read.py` so far has returned rc=1 --
correctly, because the live frontier is the pre-remedy partition where twr_daily refuses
7,335 of 7,335 rows. That is a NEGATIVE control and it is only half of one.

  A HARNESS THAT HAS ONLY EVER FAILED HAS NOT BEEN SHOWN TO BE ABLE TO PASS.

If the AC7 checks were broken in a way that makes them ALWAYS fail -- a wrong column
name, an inverted comparison, a scoped set that is empty by construction -- the live
runs would look EXACTLY as they look now, and I would carry that into 12:45Z and report
a real remedy as a failure. That is the false-outage direction, on the artifact carrying
Andrew's publish evidence, which is the most expensive place in the estate to be wrong.

THE FRAME IS POST-REMEDY SHAPED, and that is the second thing this exercises. The mirror
remedy produces MIXED partitions: 13 columns carrying the four TWR operands, most rows
computing, a residue still refusing. The live 9-column frontier CANNOT reach that path,
so the harness's operand branch and its scoped-zero arithmetic have never run against
the shape they were written for.

WHAT THIS IS NOT: it is not evidence about the live plane and not AC7 evidence. It is
evidence about THE INSTRUMENT. The fixture is synthetic and says nothing about whether
the 12:45Z run will succeed.
"""
from __future__ import annotations

import sys

import pandas as pd

sys.path.insert(0, "org/tier2_senior/0.4.0_DS_ClientPlatform~G/deliverables")
import gldrns_f1_scheduled_read as h  # noqa: E402  the SUBJECT -- imported, never re-typed

D = "2026-08-24"
PREV = "2026-08-21"

# A post-remedy MIXED partition. Deliberately NOT all-computed: AC3 forbids the remedy
# manufacturing a BMV, so a healthy run still carries refusals -- they must simply all
# be accounts absent at D-1.
BOTH_DAYS = ["A%03d" % i for i in range(6)]      # present at D and D-1 -> must COMPUTE
D_ONLY = ["N%03d" % i for i in range(2)]         # new at D -> REFUSED-NO-BMV is CORRECT
ZERO_BMV = ["Z%03d" % i for i in range(2)]       # present both days, BMV == 0 -> its own status


def _frame(date):
    if date != D:
        raise AssertionError("fixture asked for an unexpected date: %s" % date)
    rows = []
    for a in BOTH_DAYS:
        rows.append({"account_id": a, "status": "OK", "r_net": 0.0012})
    for a in ZERO_BMV:
        rows.append({"account_id": a, "status": "UNCOMPUTABLE-ZERO-BMV", "r_net": None})
    for a in D_ONLY:
        rows.append({"account_id": a, "status": "REFUSED-NO-BMV", "r_net": None})
    df = pd.DataFrame(rows)
    # the four operands the remedy restores -- a 13-col MIXED shape, not the live 9
    for c in ("bmv", "emv", "cf_net", "cf_gross"):
        df[c] = 1.0
    for c in ("business_date", "r_gross", "flow_convention", "schema_version",
              "source_pipeline", "_ingested_at"):
        df[c] = "x"
    return df


def _fixture(prefix, date):
    if "twr_daily" in prefix:
        return _frame(date)
    if "dim_calendar" in prefix:
        return pd.DataFrame([{"trading_day": D, "prev_trading_day": PREV}])
    if "canonical_valuation" in prefix:
        accts = (BOTH_DAYS + ZERO_BMV + D_ONLY) if date == D else (BOTH_DAYS + ZERO_BMV)
        return pd.DataFrame([{"account_id": a, "net_mv_plus_cash": 1000.0} for a in accts])
    raise AssertionError("fixture asked for an unexpected prefix: %s" % prefix)


def main() -> int:
    print("POSITIVE CONTROL -- can the GLD-f-1 harness return PASS at all?")
    print("subject: gldrns_f1_scheduled_read.py | fixture: SYNTHETIC post-remedy MIXED partition")
    print("=" * 100)
    print("\nTHE FIXTURE, and why each population is here")
    print("   present at BOTH D and D-1, computing ....... {:>2}  <- AC7's scoped denominator".format(
        len(BOTH_DAYS)))
    print("   present at BOTH, BMV == 0 .................. {:>2}  <- UNCOMPUTABLE-ZERO-BMV,".format(
        len(ZERO_BMV)))
    print("                                                     must NOT be driven to zero")
    print("   new at D, absent at D-1 .................... {:>2}  <- REFUSED-NO-BMV, CORRECTLY".format(
        len(D_ONLY)))
    print("   twr columns .................................. 13  <- the shape the live 9-col")
    print("                                                     frontier cannot reach")

    # STUB THE DISPATCH RECORD TOO. Section 8b (added after this control was written)
    # reads LIVE SSM, and the live history currently shows the last dispatch Failed --
    # so without this stub the positive control fails on a REAL fact about the world
    # rather than on the fixture, and STOPS BEING A POSITIVE CONTROL AT ALL.
    # A NEW CHECK SILENTLY INVALIDATED AN EXISTING CONTROL, and the only reason it was
    # caught is that this file was re-run after the harness changed. A control is not
    # a write-once artifact; it has to be re-exercised whenever its subject moves.
    real_disp = h._dispatch_record
    h._dispatch_record = lambda limit_pages=20: {
        "pages": 1, "exhausted": True, "total_commands": 1, "chain_dispatches": 1,
        "recent": [{"at_utc": "2026-08-25T12:45:41Z", "status": "Success",
                    "comment": "advi 49f dispatch src=" + h.SCHEDULED_SRC,
                    "scheduled": True}]}
    real_part, real_read = h._partitions, h._read
    h._partitions = lambda prefix: [PREV, D]
    h._read = _fixture
    h._manifest = lambda prefix, date: {
        "bmv_source": "canonical_valuation date=%s" % PREV,
        "status_census": _frame(D)["status"].value_counts().to_dict(),
    }
    try:
        rc = h.main()
    finally:                                    # restore, always -- a leaked patch would
        h._partitions, h._read = real_part, real_read   # poison every later call in-process
        h._dispatch_record = real_disp

    print("\n" + "=" * 100)
    print("HARNESS rc = %d" % rc)
    ok = rc == 0
    print("[%s] the harness CAN return PASS on a healthy post-remedy partition"
          % ("PASS" if ok else "FAIL"))
    if not ok:
        print("     -> the AC7 checks do NOT pass on a frame built to satisfy them.")
        print("        That is an INSTRUMENT defect, and it would have presented at 12:45Z")
        print("        as a failed remedy. This is exactly what this control exists to catch.")
    print("\nSCOPE: this is evidence about the INSTRUMENT, not about the live plane.")
    print("  It says nothing about whether the 12:45Z run will succeed, and it is NOT")
    print("  AC7 evidence. The negative control (live pre-remedy partition, rc=1 on the")
    print("  two AC7 limbs) and this positive control together show the checks can move")
    print("  in BOTH directions -- which is the only condition under which either verdict")
    print("  means anything.")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
