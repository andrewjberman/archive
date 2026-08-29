"""SOURCE_BASIS exercise -- the carve-out/additive plug. NO S3, NO network.

THE ACCEPTANCE IS `CLIENT DOES NOT MOVE` (1.0.0_SA_CTO~Z 16047), NOT "SMA went up":
a criterion that checks SMA increased passes the BROKEN version too, because the broken
version increases SMA by taking the money out of Client.

DATE-INDEPENDENT: every amount is a synthetic parameter. No production figure is pinned,
so this scores identically at any as_of.

⛔ THE IDENTITY IS A REGRESSION ROW, NEVER A PROGRESS ROW (3.0.0_SA_CVO~Z 15942): it is
assembled FROM the source_basis labels and re-satisfies exactly under a WRONG assignment
in either direction. It proves the arithmetic, which nobody doubts. The PROGRESS row is
the negative control: the refused shape must produce a DIFFERENT Client.
"""
import os
import sys

sys.path.insert(0, os.path.join("data", "mdpf", "scripts", "gold"))

MODEL = 600.0
NON_MODEL = 400.0
CARVE = 100.0    # divz -- inside non_model
ADDITIVE = 60.0  # tax  -- outside it (0833)


def ts(with_tax, carried_basis="additive"):
    """49financial-shaped by_model. `divz`/`opal_div_sma` is the carve-out cohort."""
    # a Models cohort is REQUIRED for the fixture to be self-consistent: the gold plane
    # asserts sum(peers) == total_aua, so model_aua must actually be represented.
    bm = {"opal_short_term": {"model_value": [MODEL]},
          "opal_div_sma": {"model_value": [CARVE]}}
    if with_tax:
        e = {"model_value": [ADDITIVE]}
        if carried_basis is not None:
            e["source_basis"] = carried_basis
        bm["tax"] = e
    return {
        "as_of_last": "2026-08-27",
        "opal_aggregate_aua": [MODEL + NON_MODEL],
        "non_model_aua": [NON_MODEL],
        "by_model": bm,
    }


def show(title, rows):
    print("=" * 80)
    print(title)
    print("=" * 80)
    ok = True
    for n, p, d in rows:
        print("  {0:<54} {1}   {2}".format(n, "PASS" if p else "FAIL", "" if p else d))
        ok = ok and p
    return ok


def peers(cv):
    return {k: v.get("aum") for k, v in cv["nodes"].items()}


def main():
    import mdpf_category_registry as R
    import mdpf_gold_consolidator as C

    base = C._shape_category_views(ts(False), "49financial")
    withtax = C._shape_category_views(ts(True), "49financial")

    b, w = peers(base), peers(withtax)
    # `total_aua` is not echoed on the emitted object, so the served PEER SUM is the
    # instrument for it. That is not a workaround -- the gold-plane assertion inside
    # build_category_views is `sum(TOP_LEVEL_PEERS) == total_aua`, so a peer sum that
    # moved by the additive amount IS the total having moved by it, already checked
    # against the total by the producer itself.
    b_sum = round(sum(v for v in b.values() if v is not None), 2)
    w_sum = round(sum(v for v in w.values() if v is not None), 2)

    print("BASELINE (no additive member)  peers:", b, " sum:", b_sum)
    print("WITH TAX (additive, carried)   peers:", w, " sum:", w_sum)
    print()

    after = show("AFTER -- an ADDITIVE member arrives", [
        ("A1 CLIENT DOES NOT MOVE  <-- THE acceptance",
         round(w["Client"], 2) == round(b["Client"], 2),
         "Client {0} -> {1}".format(b["Client"], w["Client"])),
        ("A2 SMA grows by EXACTLY the additive amount",
         round(w["SMA"] - b["SMA"], 2) == round(ADDITIVE, 2),
         "delta {0}".format(round(w["SMA"] - b["SMA"], 2))),
        ("A3 the served peer sum grows by EXACTLY that amount",
         round(w_sum - b_sum, 2) == round(ADDITIVE, 2),
         "delta {0}".format(round(w_sum - b_sum, 2))),
        ("A4 Models untouched", round(w["Models"], 2) == round(b["Models"], 2),
         "{0} -> {1}".format(b["Models"], w["Models"])),
    ])

    print()
    # the REFUSED shape, same fixture: treat tax as a carve-out and net it.
    refused_client = round(NON_MODEL - (CARVE + ADDITIVE), 2)
    correct_client = round(NON_MODEL - CARVE, 2)
    ctl = show("NEGATIVE CONTROL -- the REFUSED shape must give a DIFFERENT Client", [
        ("C1 refused (net everything) Client != correct Client",
         refused_client != correct_client,
         "both {0}".format(correct_client)),
        ("C2 the instrument DISCRIMINATES the two shapes",
         round(w["Client"], 2) == correct_client
         and round(w["Client"], 2) != refused_client,
         "got {0}, correct {1}, refused {2}".format(w["Client"], correct_client,
                                                    refused_client)),
    ])
    print("     refused shape would report Client {0} vs correct {1} -- a silent "
          "{2} reclassification".format(refused_client, correct_client,
                                        round(correct_client - refused_client, 2)))

    print()
    # guard arms
    def raises(fn):
        try:
            fn()
            return False
        except SystemExit:
            return True
        except ValueError:
            return True

    guards = show("GUARDS -- each must REFUSE, and each is reachable", [
        ("G1 additive member with NO carried basis -> REFUSED",
         raises(lambda: C._shape_category_views(ts(True, carried_basis=None),
                                                "49financial")),
         "accepted an uncarried additive value"),
        ("G2 carried basis CONTRADICTS the registry -> REFUSED",
         raises(lambda: C._shape_category_views(ts(True, carried_basis="carve_out"),
                                                "49financial")),
         "accepted a contradicting claim"),
        ("G3 sma_members_with_basis rejects a typo'd basis",
         raises(lambda: R.sma_members_with_basis("carveout")),
         "returned empty instead of raising"),
    ])

    print()
    reg = show("REGISTRY -- the axis is declared, complete, and never defaulted", [
        ("R1 every SMA member carries a valid basis",
         all(sb in R.SMA_BASIS_VALUES for (*_x, sb) in R.SMA_MEMBERS),
         "some member lacks one"),
        ("R2 tax is the ONLY additive member today",
         R.sma_members_with_basis(R.SMA_BASIS_ADDITIVE) == ("tax",),
         "got {0}".format(R.sma_members_with_basis(R.SMA_BASIS_ADDITIVE))),
        ("R3 carve-outs are the other five",
         len(R.sma_members_with_basis(R.SMA_BASIS_CARVE_OUT)) == 5,
         "got {0}".format(R.sma_members_with_basis(R.SMA_BASIS_CARVE_OUT))),
        ("R4 verified coverage is 3 of 6 (CVO 15942 denominator)",
         len(R.SMA_BASIS_VERIFIED) == 3 and len(R.SMA_MEMBERS) == 6,
         "verified {0} of {1}".format(len(R.SMA_BASIS_VERIFIED), len(R.SMA_MEMBERS))),
        ("R5 sma_basis_of returns None for a NON-SMA member (not on this axis)",
         R.sma_basis_of("opal_short_term") is None, "returned a basis"),
    ])

    print()
    print("=" * 80)
    sound = after and ctl and guards and reg
    print("VERDICT")
    print("  AFTER            : {0}".format(after))
    print("  NEGATIVE CONTROL : {0}   (the load-bearing arm)".format(ctl))
    print("  GUARDS           : {0}".format(guards))
    print("  REGISTRY         : {0}".format(reg))
    print("  INSTRUMENT SOUND : {0}".format(sound))
    return 0 if sound else 1


if __name__ == "__main__":
    raise SystemExit(main())
