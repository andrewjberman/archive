"""C6-KERNEL K6 -- every acquisition emits a C1-envelope Observation_Record.

VALIDATED AGAINST THE RATIFIED SCHEMA, not inspected by eye. The C1 envelope
(observation_record.schema.json) is the authority; conformance is a schema_validation
result, not a source read.

WHY plane=EXERCISED / substrate=codebase HERE: this exercise runs FIXTURE transitions
behind the build-staging fence and touches no cloud substrate. Emitting APPLIED/aws would
assert a plane the measurement never stood on. The pair is a PARAMETER; an activated call
site (Andrew's worded act only) passes APPLIED/aws.

Run:  python exercise_k6_observation.py
Exit: 0 iff every emitted record validates AND the negative control fails validation.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from transition_kernel import (
    Checkpoint,
    InadmissibleRow,
    ResidueVector,
    TransitionManifest,
    TransitionUnit,
)

SCHEMA = (Path(__file__).resolve().parents[4] / "tier1_exec" / "4.0.0_SA_CRO~A"
          / "deliverables" / "NFRA_EPISTEMY.C1-ENVELOPE" / "schemas"
          / "observation_record.schema.json")


def _manifest() -> TransitionManifest:
    return TransitionManifest(
        transition_id="k6-fixture",
        targets=("scratch://fixture/a",),
        action_classes=("write",),
        checkpoints=(Checkpoint("leg1", "checkpoint 1"), Checkpoint("leg2", "checkpoint 2")),
        envelope=ResidueVector(axes={"objects_written": 10.0}),
        recovery_capacity=100.0,
        policy_epoch="epoch-fixture-0",
        knowledge_basis="kb-fixture-0",
        harm_model="hm-stamp-only",
    )


def main() -> int:
    print("=" * 84)
    print("K6 -- Observation_Record emission, validated against the RATIFIED C1 envelope")
    print("=" * 84)

    if not SCHEMA.is_file():
        print(f"FAIL: ratified schema NOT FOUND at {SCHEMA}")
        print("      Refusing to validate against a locally-invented shape.")
        return 1
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    print(f"  schema: {SCHEMA}")
    print(f"  ratified plane enum    : {schema.get('properties', {}).get('plane', {}).get('enum')}")
    print(f"  ratified substrate enum: {schema.get('properties', {}).get('substrate', {}).get('enum')}")

    try:
        import jsonschema
    except ImportError:
        print("FAIL-LOUD: jsonschema not installed -- conformance UNVERIFIABLE by this instrument.")
        print("           (An import guard answers COMPLETION, never PRESENCE -- so this is a")
        print("            refusal, not a pass.)")
        return 1

    validator = jsonschema.Draft7Validator(schema)

    # --- run a 2-leg fixture transition; each measurement is an acquisition -------------
    tu = TransitionUnit(_manifest())          # defaults: EXERCISED / codebase
    tu.run_leg("leg1", act=lambda: None, residue_axis="objects_written",
               measure_fn=lambda: 2.0, method="fixture count")
    tu.run_leg("leg2", act=lambda: None, residue_axis="objects_written",
               measure_fn=lambda: 3.0, method="fixture count")

    # a REFUSED acquisition must ALSO emit -- otherwise the stream is a census of survivors
    try:
        tu.ledger.record_measurement("leg3", "objects_written", 9.0, "asserted by hand")
    except InadmissibleRow:
        pass

    obs = tu.ledger.observations()
    rows = tu.ledger.rows()
    print(f"\n  ledger rows (successful measurements): {len(rows)}")
    print(f"  Observation_Records emitted          : {len(obs)}   <- 2 KNOWN + 1 UNKNOWN(refused)")

    if len(obs) != 3:
        print(f"FAIL: expected 3 emitted records (2 KNOWN + 1 refused), got {len(obs)}")
        return 1

    ok = 0
    for i, rec in enumerate(obs):
        errs = sorted(validator.iter_errors(rec), key=str)
        state = rec["substantive_result"]["state"]
        if errs:
            print(f"  [FAIL] record {i} ({state}): {errs[0].message[:90]}")
        else:
            ok += 1
            print(f"  [OK  ] record {i}: plane={rec['plane']} substrate={rec['substrate']} "
                  f"state={state} value={rec['substantive_result']['value']} "
                  f"hash={rec['request_hash'][:26]}...")

    # --- the honesty rule: a REFUSED acquisition must be UNKNOWN with a reason ----------
    refused = [r for r in obs if r["substantive_result"]["state"] == "UNKNOWN"]
    honest = bool(refused) and all(
        r["substantive_result"]["value"] is None and r["substantive_result"]["reason"]
        for r in refused)
    print(f"\n  refused acquisition -> UNKNOWN + value None + reason present: {honest}")

    # --- NEGATIVE CONTROL: a record with an off-enum plane MUST fail validation ---------
    bad = json.loads(json.dumps(obs[0]))
    bad["plane"] = "FIXTURE"          # not in the ratified enum
    bad_errs = sorted(validator.iter_errors(bad), key=str)
    discriminates = bool(bad_errs)
    print(f"  NEGATIVE CONTROL (plane='FIXTURE') rejected: {discriminates}"
          + (f" -- {bad_errs[0].message[:70]}" if bad_errs else " *** VALIDATOR IS BLIND ***"))

    # --- the digest home: prove it came from C10, not a local sha256 --------------------
    same_request_same_hash = obs[0]["request_hash"] == tu.ledger._request_hash(
        {"leg_id": "leg1", "axis": "objects_written", "method": "fixture count",
         "instrument": "transition_kernel.TransitionUnit", "version": "0.1.0-staged"})
    print(f"  request_hash reproduces through the NORMATIVE home (C10 _request_hash): "
          f"{same_request_same_hash}")

    print("\n" + "=" * 84)
    print(f"  records valid against ratified C1 schema : {ok}/{len(obs)}")
    print(f"  honesty rule on refused acquisition      : {honest}")
    print(f"  validator discriminates (negative control): {discriminates}")
    print(f"  digest via normative home                 : {same_request_same_hash}")
    print("=" * 84)

    if ok == len(obs) and honest and discriminates and same_request_same_hash:
        print("RESULT: PASS -- K6 emission conformant, plane/substrate honest for a fixture run.")
        return 0
    print("RESULT: FAIL")
    return 1


if __name__ == "__main__":
    sys.exit(main())
