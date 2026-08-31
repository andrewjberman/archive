"""AC11 discharge harness -- join each grain leaf to its membership sidecar.

ISSUER RULING (2.0.0_SA_COO 84321): the `.verification.json` sidecar IS AC11's read
path. It is a BUILD artifact beside the leaf, not a served object, so reading it needs
no serve word and touches nothing behind arm-(a). AC11 flips only on the MEASURED join.

DESIGN NOTES, each one paid for by a miss in this investigation:

1. PRINT THE DOC'S REAL TOP-LEVEL KEYS BEFORE ASSERTING ON ANY.
   0.4.0_DS_ClientPlatform~V's first probe asserted on `_account_ids` and an `entries`
   array. The emitted key is `membership` and there is no `entries` array, so the probe
   returned a clean, confident, WRONG absence -- a wrong accessor and a genuine absence
   are byte-identical in that output.

2. RE-ASSERT THE CROSS-TIE; NEVER READ `cross_tie_asserted_at_emit`.
   That field is the producer describing its own act. Under the one-self-report limit it
   may corroborate and never substitute. This harness recomputes len(membership[key])
   against the leaf's own `accounts` count and ignores the producer's flag entirely.

3. THE CORPUS IS THE WHOLE DIRECTORY.
   My own 84233 filtered `verification` out of the file list and then ran a "positive
   control" INSIDE the filtered corpus, which could only ever agree with the error. The
   file list here is unfiltered and the split is PRINTED, not assumed.

4. KEY SETS ARE COMPARED IN BOTH DIRECTIONS.
   An absence is directional: leaf-not-in-sidecar and sidecar-not-in-leaf are different
   defects and either is a real finding per the ruling.

5. NEGATIVE CONTROL RUNS EVERY TIME.
   A join test that cannot fail is not a control. Arm N corrupts one count and one key
   in memory and requires both to be caught.
"""
import json
import os
import sys

BASE = "org/tier2_senior/0.4.0_DS_ClientPlatform~V/deliverables/emissions/"
SIDECAR_SUFFIX = ".verification.json"

# leaf basename -> the grain whose entries carry an `accounts` count
PAIRS = [
    "perfrp_book_advisor",
    "perfrp_book_advisor_floor_aligned",
    "perfrp_gainloss_relationship",
    "perfrp_gainloss_account",
    "perfrp_performance_relationship",
]


def load(name):
    with open(os.path.join(BASE, name), encoding="utf-8") as f:
        return json.load(f)


def join_one(stem, verbose=True, corrupt=None):
    """Return (ok, report_dict). `corrupt` injects a fault for the negative control."""
    leaf = load(stem + ".json")
    side = load(stem + SIDECAR_SUFFIX)

    if verbose:
        print("  sidecar REAL top-level keys:", sorted(side.keys()))

    membership = side.get("membership")
    if not isinstance(membership, dict):
        return False, {"fatal": "no `membership` dict on the sidecar"}

    membership = dict(membership)  # local copy; never mutate the loaded artifact
    entries = {e["key"]: e for e in leaf["entries"]}

    if corrupt == "count":
        k = next(iter(membership))
        membership[k] = membership[k] + ["INJECTED-EXTRA-ID"]
    elif corrupt == "key":
        membership.pop(next(iter(membership)))

    leaf_keys, side_keys = set(entries), set(membership)
    only_leaf = leaf_keys - side_keys
    only_side = side_keys - leaf_keys

    mismatches = []
    for k in leaf_keys & side_keys:
        declared = entries[k].get("accounts")
        actual = len(membership[k])
        if declared != actual:
            mismatches.append((k, declared, actual))

    ids_total_resummed = sum(len(v) for v in membership.values())

    rep = {
        "leaf_entries": len(entries),
        "sidecar_keys": len(membership),
        "matched": len(leaf_keys & side_keys),
        "only_leaf": len(only_leaf),
        "only_sidecar": len(only_side),
        "count_mismatches": len(mismatches),
        "ids_resummed": ids_total_resummed,
        "ids_total_field": side.get("ids_total"),
        "sample_mismatch": mismatches[:3],
        "sample_only_leaf": sorted(only_leaf)[:3],
        "sample_only_sidecar": sorted(only_side)[:3],
    }
    ok = not only_leaf and not only_side and not mismatches
    return ok, rep


def main():
    files = sorted(f for f in os.listdir(BASE) if f.endswith(".json"))
    side = [f for f in files if SIDECAR_SUFFIX in f]
    print("CORPUS (unfiltered, split PRINTED not assumed):")
    print("  %d .json total = %d served leaf + %d sidecar" % (len(files), len(files) - len(side), len(side)))
    print()

    all_ok = True
    for stem in PAIRS:
        print("== %s ==" % stem)
        ok, rep = join_one(stem)
        if "fatal" in rep:
            print("  FATAL:", rep["fatal"])
            all_ok = False
            continue
        print(
            "  leaf entries=%d  sidecar keys=%d  matched=%d  only_leaf=%d  only_sidecar=%d"
            % (rep["leaf_entries"], rep["sidecar_keys"], rep["matched"], rep["only_leaf"], rep["only_sidecar"])
        )
        print(
            "  accounts-count vs len(membership[key]): %d MISMATCH of %d joined"
            % (rep["count_mismatches"], rep["matched"])
        )
        print(
            "  ids re-summed BY THIS HARNESS = %d ; doc's own ids_total field = %s (field NOT trusted, compared)"
            % (rep["ids_resummed"], rep["ids_total_field"])
        )
        if rep["sample_mismatch"]:
            print("  sample mismatches (key, declared, actual):", rep["sample_mismatch"])
        if rep["sample_only_leaf"]:
            print("  sample only-in-leaf:", rep["sample_only_leaf"])
        if rep["sample_only_sidecar"]:
            print("  sample only-in-sidecar:", rep["sample_only_sidecar"])
        print("  ARM:", "PASS" if ok else "FAIL")
        print()
        all_ok = all_ok and ok

    print("== NEGATIVE CONTROL (a join test that cannot fail is not a control) ==")
    neg_ok = True
    for fault in ("count", "key"):
        ok, _ = join_one(PAIRS[2], verbose=False, corrupt=fault)
        fired = not ok
        print("  inject %-6s -> harness reports %s  [%s]" % (fault, "FAIL" if fired else "PASS", "control FIRES" if fired else "CONTROL DID NOT FIRE"))
        neg_ok = neg_ok and fired
    print()

    print("RESULT: join %s ; negative control %s" % ("PASS" if all_ok else "FAIL", "FIRES" if neg_ok else "DEAD"))
    return 0 if (all_ok and neg_ok) else 1


if __name__ == "__main__":
    sys.exit(main())
