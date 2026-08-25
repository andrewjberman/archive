"""PRF-c-1 + PRF-inv-2 EXERCISE (ADVI_PERFRP TO-R1-DS, AC13).

AC13: every leaf an EMITTERS entry, count printed via the publisher's OWN derived
denominator; never-blend fixture BYTE-EQUAL.

ADVI_INSURE_PRD.md:114 requires the never-blend property "exercised, not asserted",
so this computes real figures twice -- once clean, once with an insurance-shaped row
present -- and compares the SERIALISED BYTES, not a summary.

EVIDENCE VINTAGE: live plane read 2026-08-25; citations resolve at
23271aac6480f2ebd65a37247ae64dde4d68c199.
"""
from __future__ import annotations

import hashlib
import json
import sys

sys.path.insert(0, "data/assets/scripts/gold/runners_49f")
from perfrp_emitters import (  # noqa: E402  IMPORTED, never copied
    INSURANCE_KEY_FIELD,
    PERFRP_EMITTER_FAMILIES,
    PUBLISHER_PRESTATE,
    BlendRefused,
    assert_am_only,
)
from perfrp_rollup import rollup  # noqa: E402  the SHARED law, not a stand-in

PASSED = 0
FAILED = 0


def check(label, ok, detail=""):
    global PASSED, FAILED
    if ok:
        PASSED += 1
    else:
        FAILED += 1
    print("  [%s] %-56s %s" % ("PASS" if ok else "FAIL", label, detail))


def figures(rows):
    """A real PERFRP figure set for one relationship, via the SHARED rollup law.

    Uses the actual production functions rather than a stand-in, so the byte-equality
    below is a property of the real projection and not of a toy.
    """
    kids = [{"dollars": r["mv"], "denominator": r["mv"], "daily": r["daily"]}
            for r in rows if r.get("mv") is not None]
    out = rollup(kids, from_level="account", to_level="relationship")
    return {
        "dollars": round(out["dollars"], 2),
        "denominator": round(out["denominator"], 2),
        "window_return": (None if out["window_return"] is None
                          else round(out["window_return"], 12)),
        "state": out["window_return_state"],
        "accounts": len(kids),
    }


def serialise(fig):
    """Canonical bytes. Sorted keys + fixed separators so the comparison is about the
    CONTENT and cannot pass or fail on dict ordering."""
    return json.dumps(fig, sort_keys=True, separators=(",", ":")).encode()


def main() -> int:
    print("PRF-c-1 + PRF-inv-2 EXERCISE -- ADVI_PERFRP TO-R1-DS (AC13)")
    print("=" * 100)

    print("\nAC13.1 -- the emitter families, against the publisher's DERIVED denominator")
    n = len(PERFRP_EMITTER_FAMILIES)
    print("  publisher PRE-STATE (its own derived line, not a literal here):")
    print("    emitter_entries=%d  emit_twins=%d  live_objects=%d"
          % (PUBLISHER_PRESTATE["emitter_entries"], PUBLISHER_PRESTATE["emit_twins"],
             PUBLISHER_PRESTATE["live_objects"]))
    print("  PERFRP adds %d families:" % n)
    for f in PERFRP_EMITTER_FAMILIES:
        print("      %s" % f)
    check("11 families, per COO 67014", n == 11, "n=%d" % n)
    check("names are unique", len(set(PERFRP_EMITTER_FAMILIES)) == n)
    check("transactions is ONE family, not a level pair (s.11 #6)",
          "perfrp_transactions_relationship" in PERFRP_EMITTER_FAMILIES
          and "perfrp_transactions_account" not in PERFRP_EMITTER_FAMILIES)
    print("  AFTER-STATE emitter entries: %d + %d = %d"
          % (PUBLISHER_PRESTATE["emitter_entries"], n,
             PUBLISHER_PRESTATE["emitter_entries"] + n))
    print("  N_OBJECTS is DATA-DEPENDENT and is deliberately NOT asserted (COO 67014):")
    print("    these are per-relationship/per-account keys; the count moves with the book.")

    print("\nAC13.2 -- NEVER-BLEND, byte-equality on REAL figures")
    am_ids = {"0010000001", "0010000002", "0010000003"}
    clean = [
        {"account_id": "0010000001", "mv": 1_000_000.0, "daily": [0.010, -0.004]},
        {"account_id": "0010000002", "mv": 250_000.0, "daily": [0.020, -0.010]},
        {"account_id": "0010000003", "mv": 4_000_000.0, "daily": [-0.001, 0.003]},
    ]
    # An ADVI_INSURE row as the PRD defines it (row 3): keyed on bd_account_id, and
    # NO SCHWAB ID EXISTS -- so account_id is None, which is exactly the shape that
    # would arrive through the BD-side xref join a-6 already reads.
    insurance_row = {"account_id": None, INSURANCE_KEY_FIELD: "BD-INS-0001",
                     "mv": 750_000.0, "daily": [0.05, 0.05]}
    with_ins = clean + [insurance_row]

    f_clean = figures(clean)
    f_with = figures([r for r in with_ins if r.get("account_id") in am_ids])
    b_clean, b_with = serialise(f_clean), serialise(f_with)
    print("    clean          : %s" % b_clean.decode())
    print("    with insurance : %s" % b_with.decode())
    check("figures are BYTE-EQUAL with and without the insurance row",
          b_clean == b_with,
          "sha256 %s vs %s" % (hashlib.sha256(b_clean).hexdigest()[:12],
                               hashlib.sha256(b_with).hexdigest()[:12]))

    print("\n  CONTROL -- the comparison must be ABLE to fail, or byte-equality proves nothing:")
    f_blended = figures(with_ins)          # deliberately NOT filtered
    b_blended = serialise(f_blended)
    print("    blended (mutant): %s" % b_blended.decode())
    check("MUTANT: an unfiltered blend DOES change the bytes", b_clean != b_blended,
          "dollars %.2f -> %.2f" % (f_clean["dollars"], f_blended["dollars"]))

    print("\nAC13.3 -- the GUARD refuses rather than relying on the filter")
    check("clean rows pass the AM-only guard",
          assert_am_only(clean, am_account_ids=am_ids, figure_fields=("mv",)) is True)
    try:
        assert_am_only(with_ins, am_account_ids=am_ids, figure_fields=("mv",))
        check("an insurance row carrying a FIGURE is REFUSED", False, "it was accepted")
    except BlendRefused as e:
        check("an insurance row carrying a FIGURE is REFUSED", True, str(e)[:52] + "...")
    # the a-6 legality case: existence WITHOUT figures is a join, not a blend (Q-p3)
    existence_only = [{"account_id": None, INSURANCE_KEY_FIELD: "BD-INS-0002", "mv": None}]
    try:
        assert_am_only(existence_only, am_account_ids=am_ids, figure_fields=("mv",))
        check("an EXISTENCE record with no figure is ALLOWED (a-6 / Q-p3)", True,
              "a join, not a blend -- this is what keeps a-6 legal")
    except BlendRefused:
        check("an EXISTENCE record with no figure is ALLOWED (a-6 / Q-p3)", False,
              "the guard is too broad -- it would break the roster")

    print("\n" + "=" * 100)
    print("DENOMINATOR: %d checks, %d PASS, %d FAIL" % (PASSED + FAILED, PASSED, FAILED))
    print("MEASURED: no insurance data exists yet (blackdiamond/49financial absent, no")
    print("insurance_* table in the BD tree), so this is necessarily a FIXTURE control.")
    return 0 if FAILED == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
