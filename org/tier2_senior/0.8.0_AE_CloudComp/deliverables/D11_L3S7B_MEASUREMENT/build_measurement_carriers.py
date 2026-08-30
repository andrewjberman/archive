"""Emit the three cell carriers for NFRA_C3MATERIALIZE.TO-L3S7B-CCY.measurement.

WHAT THIS FILE IS. The face @f95818e96b owns three certified cells at gate `now`:
L3S7B-1c16-3 (frame declaration), L3S7B-1c16-1 (the unfused AUC(W1) baseline) and
L3S7B-0b5f-1 (the REBUILT clause-1 instrument exercised on perm(W1) as its own control).
This module writes one carrier per cell and a frame-block census proving the frame is
byte-equal on all three, which is what L3S7B-1c16-3's value_domain asks for.

WHY A DRIVER OF MY OWN AND NOT run_sweep.py -- STATED BECAUSE IT LOOKS LIKE A DEPARTURE
AND IS NOT. Declaration 7 fixes the IMPLEMENTATION (the engine). run_sweep.py is the wave-3
runner; it computes AUC on FUSED output and permutes view 2 once at a fixed seed. Neither of
this face's measurements exists in it: AC1 is the UNFUSED AUC(W1) (no snf() call at all), and
AC3 requires an instrument that is REBUILT rather than reused, with n >= 20 independently
seeded draws. So the engine's functions are called at their pinned bytes and the driver is
this file, committed beside the carriers. No number from any other implementation crosses in
(1i(ii)): every value below comes from snf_ksweep.py @e2ab79fba4.

⛔ ORDER IS LOAD-BEARING AND IS RECORDED, NOT ASSERTED. AC1 must be produced BEFORE any fused
arm exists on this rectangle, and AC3's control needs C1 = SNF(W1, W1), which IS a fused arm.
So AC1 ran first at 14:14:51Z and the first snf() call on this rectangle completed at
14:15:46Z; that second timestamp is AC1's produced_before and it is evidenced by the mtime of
the saved C1 matrix, not by this file's say-so.

PINS CORRECTED BEFORE ANY MEASUREMENT (1.0.0_SA_CTO~X disarm 87781, correction-1 @1eba52e86c):
the face's declaration 7 pinned the engine at cfc5f28fb7, which defines NONE of
firm_separation_auc / permute_view / viewP_affinity; the fixed implementation for sec-7b is
snf_ksweep.py @e2ab79fba4 + run_sweep.py @e2ab79fba4, one revision. Declaration 1's frame-B
`pairs` 8,596,731 is C(4147,2), the both-measured POPULATION's pair count; frame B's own pair
domain is C(1820,2) = 1,655,290. Both corrected at the record; every number kept and named for
the set it counts. Consumers cite BOTH pins, which every carrier below does.

Author: 0.8.0_AE_CloudComp~Y.  TO: NFRA_C3MATERIALIZE.TO-L3S7B-CCY.measurement.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]   # the REPO ROOT; parents[4] is <repo>/org
OUT = Path(__file__).resolve().parent
FACE_PIN = "0684a3e11a"
FACE_SHA = "9d9bd7559577f9cc"  # first 16 hex of the record-successor face
ENGINE_PIN = "e2ab79fba4"
ENGINE_SHA = "86ae5ca5f72ed8748cc035535ac6ea8db02fb5c47d0fe7391562400b25f58374"

# ---------------------------------------------------------------------------
# THE FRAME BLOCK -- one object, embedded identically in all three carriers.
# Every count names the set it counts (correction-1; the artifacts_contract's
# "every count prints what it is a count of, with its denominator").
# ---------------------------------------------------------------------------
FRAME = {
    "judged_frame": "B",
    "B": {
        "role": "judged",
        "members": 1820,
        "predicate": "view 1 AND view 2 MEASURED (both-measured) AND in the firm cohort",
        "pair_domain": 1655290,
        "pair_domain_is": "C(1820,2) -- frame B's own pairs",
        "basis": "measured",
    },
    "A": {
        "role": "reported beside B, never carried from or to B (1k(iii))",
        "members": 1941,
        "predicate": "the full firm cohort",
        "pair_domain": 1882770,
        "pair_domain_is": "C(1941,2) -- frame A's own pairs",
        "basis": "measured",
    },
    "both_measured_population": {
        "role": "NOT a frame -- the population from which B is drawn; named because its pair "
                "count was carried into frame B's block in the record and is corrected here",
        "members": 4147,
        "predicate": "view 1 AND view 2 MEASURED over the full 19,482 population",
        "pair_domain": 8596731,
        "pair_domain_is": "C(4147,2) -- the value declaration 1 carried as frame B's `pairs`",
        "basis": "measured",
    },
    "union_pair_domain": {
        "members": 19482,
        "pair_domain": 189764421,
        "pair_domain_is": "C(19482,2) -- the L2 STRUCTURE population's pairs",
        "basis": "measured",
    },
    "A_minus_B": {
        "members": 121,
        "predicate": "cohort members that are view-2 ABSENT",
        "basis": "measured",
    },
    "carrier_table": "CloudNode",
    "entity_domain": "L2_STRUCTURE_heterogeneous",
    "corrected_by": {
        "record": "DESIGN_DECLARATIONS_AT_THE_CUT_1.0.0_SA_CTO~X.correction-1.json",
        "pin": "1eba52e86c",
        "field": "1_frame.B.pairs -- was 8596731 (C(4147,2)), frame B's own is 1655290",
    },
}


def canonical(obj) -> str:
    """One serialisation for every carrier, so byte-equality is a property of the bytes."""
    return json.dumps(obj, ensure_ascii=True, sort_keys=True, separators=(",", ":"))


def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def blob_sha256(pin: str, rel: str) -> str:
    """sha256 of the BLOB AT THE PIN -- never the worktree.

    The artifacts_contract calls a worktree-rendering digest a FORM_DEFECT on a certified row
    (1l(iii)), and this box checks out CRLF: VIEWP_firm_partition.json reads 17,585 B in the
    worktree against 17,333 B at its blob, the whole 252-byte delta being CR. Measured, not
    assumed.
    """
    raw = subprocess.run(["git", "show", f"{pin}:{rel}"], cwd=str(ROOT),
                         capture_output=True, check=True).stdout
    return hashlib.sha256(raw).hexdigest()


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


DELIV = "org/tier2_senior/0.7.0_AE_CloudOps/deliverables/"
SCRATCH = ("C:/Users/ANDREW~1/AppData/Local/Temp/claude/"
           "C--Users-AndrewBerman-Desktop-ajb-workspace/"
           "b3cf19c0-4b0d-4065-b24b-caf9685c8a2a/scratchpad/")


def inputs_block() -> list:
    """Every input row carries digest_of (1l(vi)). Only what was actually read is listed."""
    return [
        {
            "role": "fixed implementation (engine) -- the ONLY source of every number here",
            "path": DELIV + "D11_L3W3_KSWEEP/snf_ksweep.py",
            "pin": ENGINE_PIN,
            "digest_of": "blob-at-pin",
            "sha256": ENGINE_SHA,
            "functions_called": ["load_view1_partitions", "view1_affinity",
                                 "firm_separation_auc", "permute_view", "snf",
                                 "exact_zero_count"],
            "contains_census": "all six present at this pin; at cfc5f28fb7 three of them are "
                               "absent (firm_separation_auc 0, permute_view 0, viewP_affinity "
                               "0; positive control snf 1). CVO 87774: a pin row carries "
                               "CONTAINS beside ON_ORIGIN or it is not a measured pin.",
            "basis": "measured",
        },
        {
            "role": "view 1 source -- the served factorized consensus (25 partitions)",
            "path": "s3://opal-313476888478-globgrph/c3materialize-b4/out/eb009c01-.../"
                    "W_STRUCTURE_FACTORIZED.json",
            "digest_of": "served-object",
            "sha256": "e91d69910fc9d4eabb58eedb8a73165476225ab838977e8d6c16604af3f5e19a",
            "bytes": 2662267,
            "identity_check": "equals the digest the engine's own docstring declares for this "
                              "artifact -- checked, not assumed",
            "basis": "measured",
        },
        {
            "role": "both-measured mask (defines the both-measured population)",
            "path": DELIV + "D11_L3W2_FUSION/mask_carrier_union.json",
            "pin": "1f5d4f6136",
            "digest_of": "blob-at-pin",
            "sha256": "a3354b0e8ddc3a67c20fa39333b3268da598fce3f1b14adc82818b6fab8eb7dd",
            "basis": "measured",
        },
        {
            "role": "firm cohort (defines frame A and the firm labels the AUC separates on)",
            "path": DELIV + "D11_L3W2_FUSION/firm_cohort_shared.json",
            "pin": "9f8a1f13e6",
            "digest_of": "blob-at-pin",
            "sha256": "ad361014a7da885037421da005011c32b28cfb37f64da8feafad1cba95db3f19",
            "basis": "measured",
        },
        {
            "role": "L2 view artifacts -- the STRUCTURE entity ordering the mask indexes into",
            "path": SCRATCH + "L2_VIEW_ARTIFACTS.json",
            "digest_of": "content-addressed",
            "sha256": "9ca36c50e588b7f911826eb7b73e069ed172509dfea3ea5842778e265a83800c",
            "bytes": 10352399,
            "named_gap": "UNTRACKED and device-local: retrievable here by digest, not "
                         "re-derivable from git at any pin. Same class as the portal graph "
                         "(87247/87275); recorded, not silently relied on.",
            "basis": "measured",
        },
    ]


def declarations_block() -> list:
    return [
        {
            "record": "DESIGN_DECLARATIONS_AT_THE_CUT_1.0.0_SA_CTO~X.json",
            "pin": "e04cad153a",
            "digest_of": "blob-at-pin",
            "sha256": "7dd15d6bea1a4923a6bac0e1f0d7cb517b83c2fbfdafaffcc1366b021baa09fb",
            "binds": "declaration 1 (frame), 4 (null battery form), 7 (fixed implementation)",
        },
        {
            "record": "DESIGN_DECLARATIONS_AT_THE_CUT_1.0.0_SA_CTO~X.correction-1.json",
            "pin": "1eba52e86c",
            "digest_of": "blob-at-pin",
            "sha256": "46a11b15295b9008ae3536f014b4c2546dcb8b5bfe15354adae4f29d539cc3a2",
            "corrects": ["7_fixed_implementation.engine.pin cfc5f28fb7 -> e2ab79fba4",
                         "1_frame.B.pairs 8596731 -> 1655290 (the 8596731 relabelled to the "
                         "both-measured population)"],
        },
    ]


def envelope(cell_id: str, label: str, criterion: str) -> dict:
    return {
        "schema": "D11.L3S7B.cell_carrier.v1",
        "cell_id": cell_id,
        "label": label,
        "criterion": criterion,
        "plane": "SINGLE_VIEW_BASELINE" if cell_id.startswith("L3S7B-1c16")
                 else "NULL_BATTERY",
        "sequence_gate": "now",
        "owner": "0.8.0_AE_CloudComp~Y",
        "face": {"id": "NFRA_C3MATERIALIZE.TO-L3S7B-CCY.measurement",
                 "pin": FACE_PIN, "sha256_first16": FACE_SHA},
        "certified_record": {
            "record": "rectangle.final.certified.json",
            "pin": "97ccacce00",
            "digest_of": "blob-at-pin",
            "sha256": "e1b4c434ef3f0f408bdc8744259a431393797f578a22e23c4d789cc4c21941b4",
        },
        "design_declarations": declarations_block(),
        "carrier_table": FRAME["carrier_table"],
        "entity_domain": FRAME["entity_domain"],
        "frame": FRAME,
        "inputs": inputs_block(),
        "not_a_result": "nothing here names any sec-6 test passed or failed "
                        "(rectangle.completion_claim_rule); no candidate view is admitted, "
                        "built or run; no L4 act.",
    }


def main() -> None:
    ac1 = json.load(open(OUT / "_ac1_result.json", encoding="utf-8"))
    ac3 = json.load(open(OUT / "_ac3_result.json", encoding="utf-8"))

    # ---- L3S7B-1c16-3 : the frame declaration (written FIRST) ----
    c3 = envelope("L3S7B-1c16-3", "single_view_baseline.frame_declaration",
                  "L3S7B-CCY-AC2")
    c3["value"] = {
        "declared": FRAME,
        "byte_equal_on_every_carrier": True,
        "census": "frame_block_census.json -- the canonical serialisation of `frame` from all "
                  "three carriers, compared by sha256",
        "basis": "measured",
    }
    c3["produced_at"] = ac1["produced_at"]

    # ---- L3S7B-1c16-1 : the unfused baseline ----
    c1 = envelope("L3S7B-1c16-1", "single_view_baseline.auc_w1_unfused", "L3S7B-CCY-AC1")
    c1["value"] = {
        "frame_B_judged": {
            "auc_w1_unfused": ac1["frame_B"]["auc_w1_unfused"],
            "members": ac1["frame_B"]["members"],
            "pairs_judged": ac1["frame_B"]["pairs_judged"],
            "pairs_judged_is": "n_within + n_cross, every pair of frame B",
            "n_within": ac1["frame_B"]["n_within"],
            "n_cross": ac1["frame_B"]["n_cross"],
            "frame_pair_domain": ac1["frame_B"]["frame_pair_domain"],
            "pairs_judged_equals_frame_pair_domain":
                ac1["frame_B"]["pairs_judged_equals_domain"],
            "auc_denominator": "n_within * n_cross (Mann-Whitney)",
            "ties_at_decision": ac1["frame_B"]["ties_at_decision"],
            "basis": "measured",
        },
        "frame_A_beside": {
            "auc_w1_unfused": ac1["frame_A"]["auc_w1_unfused"],
            "members": ac1["frame_A"]["members"],
            "pairs_judged": ac1["frame_A"]["pairs_judged"],
            "n_within": ac1["frame_A"]["n_within"],
            "n_cross": ac1["frame_A"]["n_cross"],
            "frame_pair_domain": ac1["frame_A"]["frame_pair_domain"],
            "pairs_judged_equals_frame_pair_domain":
                ac1["frame_A"]["pairs_judged_equals_domain"],
            "ties_at_decision": ac1["frame_A"]["ties_at_decision"],
            "carried": "NEVER carried to or from B (1k(iii)) -- reported beside",
            "basis": "measured",
        },
        "fusion": "NONE. W1 is passed directly to firm_separation_auc; snf() is not called on "
                  "this criterion at all.",
        "implementation_pin": ENGINE_PIN,
        "produced_before": ac1["produced_before"],
        "produced_before_is": "the ISO completion of the FIRST snf() call on this rectangle, "
                              "evidenced by the mtime of the saved C1 matrix; AC1's own "
                              "produced_at is " + ac1["produced_at"] + ", which precedes it",
        "tie_mass_disclosure": {
            "distinct_w1_values": 26,
            "why": "W1(i,j) = numerator/25 with numerator in 0..25, so the unfused baseline is "
                   "measured on a 26-valued scale. ties_at_decision equals n_within in BOTH "
                   "frames for that reason -- expected quantisation, not an anomaly. Rank AUC "
                   "is not tie-invariant (the engine's own warning), so the tie count travels "
                   "beside the value rather than being left for a reader to rediscover.",
            "basis": "measured",
        },
        "headroom_declaration_3": {
            "threshold": ac1["headroom_declaration_3"]["threshold"],
            "threshold_source": "declaration 3 read at e04cad153a: distance 0.1, "
                                "refusal_threshold 0.9 -- the design lane's number, not mine",
            "tested": "AUC(W1) on frame B; no V exists on this rectangle "
                      "(candidate typed NONE), so AUC(W1) alone is tested",
            "auc_B": ac1["headroom_declaration_3"]["auc_B"],
            "frame_B_refused": ac1["headroom_declaration_3"]["frame_B_refused"],
            "margin_to_threshold": ac1["headroom_declaration_3"]["margin_to_threshold"],
            "reading": "frame B is NOT refused for the 6.3 re-run: 0.742864 sits 0.157136 "
                       "below the declared 0.90. Had it exceeded, that would have been a "
                       "FINDING on this face and never a value to move.",
            "basis": "measured",
        },
        "basis": "measured",
    }
    c1["produced_at"] = ac1["produced_at"]

    # ---- L3S7B-0b5f-1 : the rebuilt instrument + its own control ----
    cb = envelope("L3S7B-0b5f-1", "null_battery.instrument_rebuilt", "L3S7B-CCY-AC3")
    cb["value"] = {
        "instrument": ac3["instrument"],
        "instrument_source_pin": ENGINE_PIN,
        "instrument_source_sha256": ENGINE_SHA,
        "K": ac3["K"],
        "T": ac3["T"],
        "C1": ac3["C1"],
        "null": ac3["null"],
        "control_verdict": ac3["control_verdict"],
        "reading": "the rebuilt instrument SEES a permutation: the null sits at "
                   f"{ac3['null']['null_mean']} against C1 {ac3['C1']['auc']}, "
                   f"{ac3['control_verdict']['margin']} clear of the C1 - 3*spread gate, with "
                   "0 tail observations. A null at ~0.5 is what a destroyed correspondence "
                   "should give, which is the sanity signal the arm exists to produce. "
                   "Clause-1 verdicts are therefore ADMISSIBLE on this instrument -- this "
                   "cell states admissibility only and names no clause-1 result.",
        "basis": "measured",
    }
    cb["produced_at"] = ac3["produced_at"]

    written = []
    for obj, name in ((c3, "L3S7B-1c16-3.frame_declaration.json"),
                      (c1, "L3S7B-1c16-1.auc_w1_unfused.json"),
                      (cb, "L3S7B-0b5f-1.null_battery_instrument.json")):
        p = OUT / name
        p.write_text(json.dumps(obj, ensure_ascii=True, indent=1) + "\n",
                     encoding="utf-8", newline="\n")
        written.append(name)
        print("WROTE %s" % name)

    # ---- the frame-block census the value_domain asks for ----
    digests = {}
    for name in written:
        obj = json.loads((OUT / name).read_text(encoding="utf-8"))
        digests[name] = sha256_text(canonical(obj["frame"]))
    uniq = sorted(set(digests.values()))
    census = {
        "schema": "D11.L3S7B.frame_census.v1",
        "question": "is the frame block byte-equal on every carrier this face emits?",
        "method": "canonical JSON (sort_keys, separators (,:), ensure_ascii) of each "
                  "carrier's `frame`, compared by sha256",
        "denominator": len(written),
        "carriers": digests,
        "distinct_digests": len(uniq),
        "byte_equal": len(uniq) == 1,
        "digest": uniq[0] if len(uniq) == 1 else None,
        "basis": "measured",
    }
    (OUT / "frame_block_census.json").write_text(
        json.dumps(census, ensure_ascii=True, indent=1) + "\n",
        encoding="utf-8", newline="\n")
    print("WROTE frame_block_census.json -- %d carriers, %d distinct digest(s), byte_equal=%s"
          % (census["denominator"], census["distinct_digests"], census["byte_equal"]))
    if not census["byte_equal"]:
        raise SystemExit("FAIL: the frame block is NOT byte-equal across carriers")


if __name__ == "__main__":
    main()
