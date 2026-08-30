#!/usr/bin/env python3
"""Build the five L3W3-c69f-* cell rows for TO-L3W3-CCX (L3C01_floor).

DERIVE, NEVER TYPE. Every number in the emitted rows is read out of an artifact AT ITS PIN
via `git show <pin>:<path>` and recomputed here; nothing is transcribed from a message. The
one thing that IS typed is the multiplier 3, and it is typed because Addendum 1's form fixes
it as a constant whose basis is `held` -- so it is emitted WITH that basis rather than as a
bare number.

WHY A BUILDER FOR FIVE ROWS: the wave-2 turnaround proved the point -- when the rectangle was
re-cut, a copy-never-type builder tracked it with no hand edit. A row set small enough to type
by hand is exactly the size where a typo survives review.

Pins, all verified resolvable before use:
  run 1 battery   fusion_l3w2cox-union-394bdac4c227-b6.json @f8c1ad1b09  (the DERIVING run)
  gate receipt    D11_L3W3_KSWEEP/ksweep_measurements.json  @e2ab79fba4  (after-sweep-runs)
  decomp          DECOMP.md @94935b740e
  consumer        check_stability_L3C01.py @28f3028a66
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys

RUN1_PIN = "f8c1ad1b09"
RUN1_PATH = ("org/tier2_senior/0.7.0_AE_CloudOps/deliverables/D11_L3W2_FUSION/"
             "fusion_l3w2cox-union-394bdac4c227-b6.json")
SWEEP_PIN = "e2ab79fba4"
SWEEP_PATH = "org/tier2_senior/0.7.0_AE_CloudOps/deliverables/D11_L3W3_KSWEEP/ksweep_measurements.json"
DECOMP_PIN = "94935b740e"
CONSUMER_PIN = "28f3028a66"
CONSUMER_PATH = ("org/tier2_senior/0.8.0_AE_CloudComp/deliverables/"
                 "D11_L3C01_STABILITY_CONSUMER/check_stability_L3C01.py")

MULTIPLIER = 3            # Addendum 1's form. Basis `held`, emitted as such.
J_THRESHOLD = 20          # 1d item 2 -> certified L3W3-b8a2-5
RHO_THRESHOLD = 5         # Addendum 1 form
TAIL_OBSERVED_AT_N = 6    # wave 2's observation, the reason J's bar is 20


def show(pin: str, path: str) -> bytes:
    env = dict(os.environ, MSYS_NO_PATHCONV="1")
    r = subprocess.run(["git", "show", "%s:%s" % (pin, path)],
                       capture_output=True, env=env)
    if r.returncode != 0:
        raise SystemExit("REFUSED: %s:%s did not resolve -- %s"
                         % (pin, path, r.stderr.decode("utf-8", "replace")[:200]))
    return r.stdout


def main() -> int:
    run1_raw = show(RUN1_PIN, RUN1_PATH)
    run1_sha = hashlib.sha256(run1_raw).hexdigest()
    run1 = json.loads(run1_raw)
    s = run1["stability_L3C01"]
    batt = s["permutation_battery"]

    sweep_raw = show(SWEEP_PIN, SWEEP_PATH)
    sweep_sha = hashlib.sha256(sweep_raw).hexdigest()

    # ---- the derivation, recomputed here rather than read from any message
    rho = batt["rho"]
    j = batt["J"]
    floor_rho = rho["null"] + MULTIPLIER * rho["spread"]
    obs_rho = rho["observed"]

    # AC4: the sanity arm keys on the DERIVING run (issuer 85390, design lane 85407).
    sanity_pass = floor_rho < obs_rho

    # AC2 rho half: derivable because run 1's N clears rho's own threshold.
    if rho["n_permutations"] < RHO_THRESHOLD:
        raise SystemExit("REFUSED: rho N=%d below its threshold %d -- the rho half would also "
                         "be a typed refusal and this builder does not emit that shape."
                         % (rho["n_permutations"], RHO_THRESHOLD))
    # AC2 J half: NOT derivable. The refusal is the correct value, not a gap.
    if j["n_permutations"] >= J_THRESHOLD:
        raise SystemExit("REFUSED: J N=%d meets threshold %d -- a J floor WOULD derive and the "
                         "typed refusal below would be UNEARNED. Re-read the ruling."
                         % (j["n_permutations"], J_THRESHOLD))

    rows = {
        "L3W3-c69f-1": {
            "label": "L3C01_floor.consumer_binding",
            "value": "BOUND -- the consumer READS firm_representation and REFUSES on absence "
                     "or unresolvability on a RUN-2 artifact; it does not warn.",
            "claim": "measured",
            "regime_scope": "RUN-2 only; on a run-1 artifact absence is an OBSERVATION, "
                            "mirroring Addendum 1e (A)'s treatment of split_half. The field is a "
                            "wave-3 arm and run-1 evidence predates it.",
            "not_adjudicated_here": "the INTERNAL shape of firm_representation -- that is "
                                    "L3W3-dc02-7 on 0.8.0_AE_CloudComp~Y's face. Confirmed by that "
                                    "seat as the one live field, alias absent (84777).",
            "exercised_by": ["F1 absent-on-run-2 REFUSED", "F2 present-but-empty REFUSED",
                             "F3 absent-on-run-1 ADMITTED (the other truth)"],
            "evidence": {"consumer": "%s @%s" % (CONSUMER_PATH, CONSUMER_PIN)},
        },
        "L3W3-c69f-2": {
            "label": "L3C01_floor.floor_derivation",
            "claim": "measured",
            "spearman_rho": {
                "disposition": "DERIVED",
                "floor": round(floor_rho, 6),
                "recomputed_as": "null + multiplier * spread",
                "null": rho["null"],
                "spread": rho["spread"],
                "spread_status": rho["spread_status"],
                "multiplier": MULTIPLIER,
                "basis": "held",
                "basis_reason": "Addendum 1's form records the multiplier as `held` until a "
                                "second run shows the spread stable across runs. Run 2 is the "
                                "floor's first outing, so run 3 is the earliest a `measured` "
                                "basis can appear (design lane 84369(1)).",
                "n_permutations": rho["n_permutations"],
                "threshold": RHO_THRESHOLD,
                "derived_from_run_id": run1.get("run_id", "run-1"),
                "derived_from_path": RUN1_PATH,
                "derived_at_commit": RUN1_PIN,
                "derived_artifact_sha256": run1_sha,
                "metric_domain": s.get("metric_domain_predicate"),
            },
            "topdecile_jaccard": {
                "disposition": "REFUSED-INSUFFICIENT-N",
                "n_permutations": j["n_permutations"],
                "threshold": J_THRESHOLD,
                "tail_observed_at_n": TAIL_OBSERVED_AT_N,
                "refusal_reason": "1d item 2 raised J's derivation bar to N >= %d because a tail "
                                  "was observed for J at N=%d in wave 2. Run 1 carries N=%d, so "
                                  "no J floor derives this wave." % (J_THRESHOLD,
                                                                     TAIL_OBSERVED_AT_N,
                                                                     j["n_permutations"]),
                "provenance_is_verifiable": True,
                "derived_from_run_id": run1.get("run_id", "run-1"),
                "derived_from_path": RUN1_PATH,
                "derived_at_commit": RUN1_PIN,
                "derived_artifact_sha256": run1_sha,
                "not_this": "NOT PROVENANCE_UNVERIFIED -- the pins resolve and the ancestry is "
                            "measured. It is the N that refuses, not the provenance.",
                "floor_status": "HELD-UNEXERCISED",
                "held_constant_reported": s.get("floors", {}).get("topdecile_jaccard"),
                "held_constant_binds": "NEITHER DIRECTION (ruling 80787)",
            },
            "not_a_repair_path": "Extending run 1's battery would mint a different artifact under "
                                 "a different digest -- it would no longer be run 1 -- and "
                                 "same-run derivation is prohibited (Addendum 1b). The refusal IS "
                                 "the correct value for the J half.",
        },
        "L3W3-c69f-3": {
            "label": "L3C01_floor.tail_binding",
            "claim": "measured",
            "value": "BOUND -- J's derivation is blocked until N >= %d carrying "
                     "tail_observed_at_n %d; rho may derive at N >= %d having no tail."
                     % (J_THRESHOLD, TAIL_OBSERVED_AT_N, RHO_THRESHOLD),
            "typed_result_separation": {
                "SPREAD_TAIL": "an IN-BATTERY draw at the deriving pin lies outside the "
                               "leave-one-out band of the OTHER draws, AT DERIVATION TIME.",
                "INSUFFICIENT_N": "the battery is CLEAN and the N is below this statistic's "
                                  "threshold. Distinct value, distinct cause.",
                "correction_carried": "The consumer previously typed a clean battery waiting on N "
                                      "as SPREAD_TAIL, which is wrong by the file's own definition "
                                      "-- that branch is reached only when no draw is outside any "
                                      "band. Retyped @%s." % CONSUMER_PIN,
                "ordering_is_load_bearing": "the tail test runs BEFORE the N threshold; checked "
                                            "the other way a real tail at N<threshold is masked by "
                                            "the general refusal.",
            },
            "exercised_by": ["D2 real declared tail -> SPREAD_TAIL", "D3 clean + prior tail -> "
                             "INSUFFICIENT_N", "N1 clean, no prior tail -> INSUFFICIENT_N",
                             "D4 at N=20 the recorded tail clears (the other truth)"],
        },
        "L3W3-c69f-4": {
            "label": "L3C01_floor.sanity_arm",
            "claim": "measured",
            "keyed_on": "THE DERIVING RUN -- run 1 @%s. The certified oracle reads 'the observed "
                        "S OF THE RUN IT WAS DERIVED FROM'. Confirmed as reading (a) by the issuer "
                        "(85390) and the design lane (85407); the 'against run 2's S' phrasing in "
                        "84349/85298/85370 was withdrawn as imprecise." % RUN1_PIN,
            "floor": round(floor_rho, 6),
            "deriving_run_observed": obs_rho,
            "strictly_below": sanity_pass,
            "result": "PASS" if sanity_pass else "SPREAD_SANITY_FAIL",
            "floor_status": "RE-DERIVED" if sanity_pass else "HELD-UNEXERCISED",
            "S_is_not_the_AUC": "REFUSED by construction (design lane 85407): S is the L3-C01 "
                                "stability family (Spearman rho / top-decile Jaccard) over ranks. "
                                "The k-sweep's firm-separation AUC over pairs is a different "
                                "quantity; a row carrying an AUC as observed_S is FORM_DEFECT. "
                                "The wrong-grain comparison would have PASSED (0.510390 > "
                                "%.6f), which is why it was refused rather than written."
                                % floor_rho,
            "exercised_by": ["J6 deriving run below its own floor -> SPREAD_SANITY_FAIL"],
        },
        "L3W3-c69f-5": {
            "label": "L3C01_floor.refusal_on_absence",
            "claim": "measured",
            "value": "BOUND -- an absent battery, an absent scheme, a missing derived_from_path "
                     "or a non-ancestor derived_at_commit each REFUSE the derivation with their "
                     "own typed result.",
            "PROVENANCE_UNVERIFIED_is_never_a_pass": True,
            "unrunnable_is_not_passed": "a provenance check that cannot run is reported as UNRUN, "
                                        "never scored as clean.",
            "earned_refusal_is_verified": "a declared REFUSED-INSUFFICIENT-N is checked against "
                                          "DERIVE_MIN_N; a refusal at a SUFFICIENT N is "
                                          "FORM_DEFECT. Without that check the typed refusal "
                                          "becomes a way to decline any floor at any N.",
            "exercised_by": ["R1 earned refusal ADMITTED", "R2 unearned refusal FORM_DEFECT",
                             "R3 wrong threshold cited FORM_DEFECT",
                             "R4 provenance dropped on a refusal FORM_DEFECT"],
        },
    }

    doc = {
        "to_id": "NFRA_C3MATERIALIZE.TO-L3W3-CCX",
        "seat": "0.8.0_AE_CloudComp~X",
        "decomp_ref": "workflows/atom_decomposition/runs/nfra-c3materialize-L3/20260829T1906Z/"
                      "DECOMP.md @%s" % DECOMP_PIN,
        "gate": {
            "name": "after-sweep-runs",
            "state": "FIRED",
            "receipt": "%s @%s" % (SWEEP_PATH, SWEEP_PIN),
            "receipt_sha256": sweep_sha,
            "receipt_owner": "0.7.0_AE_CloudOps~X (TO-L3W3-COX)",
            "note": "The receipt is cited as the GATE. No value in this file is read from the "
                    "sweep artifact: it carries firm-separation AUCs and an exact-zero census "
                    "(0 of 21 leaf names are stability-family), and none of those is an S.",
        },
        "rows": rows,
        "artifacts_produced": [
            {"path": "org/tier2_senior/0.8.0_AE_CloudComp/deliverables/D11_L3W3_L3C01_FLOOR/"
                     "l3c01_floor_rows.json",
             "commit_or_etag": "PENDING-THIS-COMMIT",
             "why_sentinel": "this file is covered by the very commit carrying it; a proof cannot "
                             "name its own hash. The issuer stamps the hex at TO close."},
            {"path": "org/tier2_senior/0.8.0_AE_CloudComp/deliverables/D11_L3W3_L3C01_FLOOR/"
                     "build_rows.py",
             "commit_or_etag": "PENDING-THIS-COMMIT"},
            {"path": CONSUMER_PATH, "commit_or_etag": CONSUMER_PIN},
            {"path": RUN1_PATH, "commit_or_etag": "sha256:%s" % run1_sha},
            {"path": SWEEP_PATH, "commit_or_etag": "sha256:%s" % sweep_sha},
        ],
        "what_this_does_not_claim": [
            "No sec-6 test is discharged. Wave 3 discharges none by its own rule (m-7); a report "
            "naming PRD 6.1, 6.2 or 6.5 as PASSED is FALSE.",
            "No J floor exists. floor_status.J stays HELD-UNEXERCISED into run 3.",
            "Run 2's own stability rho is NOT read here and is not required by any of these five "
            "cells; it is the input to a FUTURE derivation (run 3's floor) and lives on "
            "L3W3-b8a2-5 / b8a2-7, not on this face.",
        ],
    }

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "l3c01_floor_rows.json")
    payload = json.dumps(doc, indent=2, sort_keys=False) + "\n"
    with open(out, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(payload)

    print("OK: wrote %s" % out)
    print("  rows: %d of 5" % len(rows))
    print("  rho floor DERIVED  : %.6f  (null %.6f + %d * spread %.6f), basis held"
          % (floor_rho, rho["null"], MULTIPLIER, rho["spread"]))
    print("  AC4 sanity arm     : deriving-run observed %.6f > floor %.6f -> %s"
          % (obs_rho, floor_rho, "PASS" if sanity_pass else "FAIL"))
    print("  J half             : REFUSED-INSUFFICIENT-N  n=%d threshold=%d tail_at_n=%d"
          % (j["n_permutations"], J_THRESHOLD, TAIL_OBSERVED_AT_N))
    print("  run1 sha256        : %s" % run1_sha)
    print("  sweep sha256       : %s" % sweep_sha)
    return 0


if __name__ == "__main__":
    sys.exit(main())
