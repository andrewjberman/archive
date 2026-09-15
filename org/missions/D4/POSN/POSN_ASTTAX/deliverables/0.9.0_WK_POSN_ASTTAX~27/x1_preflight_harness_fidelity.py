#!/usr/bin/env python3
"""POSN_ASTTAX.TO-X1-1 / AT7-s-1 -- PREFLIGHT ITEM 1.

The order's comp-adversary names this uncovered: "if the fake table's
update_item ignores SET semantics (replaces the item), the harness itself
would clobber management_style and the negative control would not
discriminate; measure the harness first".

THIS MEASURES IT, on a throwaway row, before anything else runs. It imports
V3's harness by path (never re-derives it) and asserts the bytes of BOTH
files by sha256, as V3 did.

NO seeder bytes execute here and no network client is ever constructed.
"""
import hashlib
import importlib.util
import io
import os
import sys

ROOT = os.getcwd()
DELIV = "org/missions/D4/POSN/POSN_ASTTAX/deliverables"
V3_HARNESS = os.path.join(ROOT, DELIV, "0.9.0_WK_POSN_ASTTAX~21",
                          "v3_mutant_control_re.py")
V3_SHA256 = "6342be43813fff1f8bce87bf47982d926ea67706381a591ea8876fdb48e0daf9"
MACHINERY = os.path.join(ROOT, ".scratch", "u3_ac1_before_control.py")
MACHINERY_SHA256 = ("ae72cab7dfbeb62f9acb2e6e15347672"
                    "a478adce3c0421e12e49750c7bf13aca")


def sha256_of(path):
    return hashlib.sha256(io.open(path, "rb").read()).hexdigest()


def main():
    print("=" * 100)
    print("X1 PREFLIGHT ITEM 1 -- DOES THE HARNESS FAKE TABLE HONOUR SET SEMANTICS?")
    print("=" * 100)

    got_m = sha256_of(MACHINERY)
    got_v = sha256_of(V3_HARNESS)
    print("  machinery   : %s" % MACHINERY)
    print("                sha256 %s" % got_m)
    print("                asserted == %s : %s" % (MACHINERY_SHA256,
                                                   got_m == MACHINERY_SHA256))
    assert got_m == MACHINERY_SHA256, "machinery bytes changed"
    print("  V3 harness  : %s" % V3_HARNESS)
    print("                sha256 %s" % got_v)
    print("                asserted == %s : %s" % (V3_SHA256, got_v == V3_SHA256))
    assert got_v == V3_SHA256, "V3 harness bytes changed"

    spec = importlib.util.spec_from_file_location("v3h", V3_HARNESS)
    v3h = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(v3h)
    ac1 = v3h.ac1
    print("  imported    : v3h.ScratchTableWithGet (adds get_item to ac1.ScratchTable)")
    print("                ac1.ScratchTable / ac1.make_fake_boto3 / ac1.YANG_TABLE=%r"
          % ac1.YANG_TABLE)

    # ---- the throwaway row --------------------------------------------------
    t = v3h.ScratchTableWithGet(ac1.YANG_TABLE)
    throwaway = {
        "ticker": "ZZTEST",
        "asset_class": "structured",
        "sub_asset_class": "Hedge",
        "name": "Throwaway Probe Row",
        "management_style": "active",
        "sector": "Broad",
        "last_updated": "2026-09-12T00:00:00Z",
        "updated_by": "posn-asttax-retag",
    }
    t.store["ZZTEST"] = dict(throwaway)
    print("")
    print("  THROWAWAY ROW BEFORE (%d field(s)):" % len(throwaway))
    for k in sorted(throwaway):
        print("    %-18s %r" % (k, throwaway[k]))

    # the seeder's EXACT Yang SET clause, three owned + two audit fields
    t.update_item(
        Key={"ticker": "ZZTEST"},
        UpdateExpression=("SET asset_class = :ac, sub_asset_class = :sac, "
                          "#n = :n, last_updated = :ts, updated_by = :ub"),
        ExpressionAttributeNames={"#n": "name"},
        ExpressionAttributeValues={
            ":ac": "fixed_income",
            ":sac": "Volatility",
            ":n": "TrueShares Quarterly Bear Hedge ETF",
            ":ts": "2026-09-15T13:30:00+00:00",
            ":ub": "canonical_si_seed",
        },
    )
    after = dict(t.store["ZZTEST"])
    print("")
    print("  THROWAWAY ROW AFTER the seeder's exact SET clause (%d field(s)):"
          % len(after))
    for k in sorted(after):
        print("    %-18s %r" % (k, after[k]))

    # ---- the verdict, as values --------------------------------------------
    unwritten = sorted(set(throwaway) - {"asset_class", "sub_asset_class", "name",
                                         "last_updated", "updated_by"})
    print("")
    print("  FIELDS OUTSIDE THE SET CLAUSE, by subtraction from the row's %d field(s):"
          % len(throwaway))
    print("    %r  (denominator %d of %d)" % (unwritten, len(unwritten),
                                              len(throwaway)))
    survived = [k for k in unwritten if after.get(k) == throwaway[k]]
    print("    SURVIVED %d of %d: %r" % (len(survived), len(unwritten), survived))
    merged = (len(survived) == len(unwritten)
              and after["asset_class"] == "fixed_income"
              and after["name"] == "TrueShares Quarterly Bear Hedge ETF")
    print("")
    print("  MEASURED: update_item %s"
          % ("MERGES into the existing item (DynamoDB SET semantics) -- the "
             "instrument\n            can carry an unowned field across a write, so "
             "X1-AC2's negative\n            control CAN discriminate. No extension "
             "of the harness is needed."
             if merged else
             "REPLACES the item -- the harness would clobber\n            "
             "management_style itself and the negative control would NOT "
             "discriminate.\n            THE HARNESS MUST BE EXTENDED IN THIS "
             "WORKER'S OWN COPY."))
    print("  source of the behaviour: ac1.ScratchTable.update_item -- "
          "'item = self.store.setdefault(key, dict(Key))' then per-clause "
          "'item[attr] = values[rhs]'")
    print("  (a merge into the existing dict; no rebind, no clear)")
    print("=" * 100)
    return 0 if merged else 1


if __name__ == "__main__":
    sys.exit(main())
