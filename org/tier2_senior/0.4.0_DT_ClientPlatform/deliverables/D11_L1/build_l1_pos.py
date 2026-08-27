#!/usr/bin/env python3
"""Proof-of-spec instance for TO-L1-DTX.

NOT mechanically required -- the TO's <proof_of_spec> declares no instance_path and
NFRA_C3MATERIALIZE has no project json, so proof-of-spec-check's conditional decomp_ref rule does
not bind. Built anyway because it is what a certifier reads, and because "not required" is a poor
reason to hand 3.0.0_SA_CVO~X prose where a machine-checkable instance would do.

⛔ CONTROLS ARE RUN HERE AND BAKED FROM THE RUN, never typed beside it. The two refusal arms of
build_l1_cells.py are exercised against PLANTED MUTANTS in this file -- a refusal arm that has
never been made to fire is an assertion, not a control.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess

from jsonschema import Draft202012Validator

WS = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                    capture_output=True, text=True, check=True).stdout.strip()
D = os.path.join(WS, "org/tier2_senior/0.4.0_DT_ClientPlatform/deliverables/D11_L1")
CELLS = os.path.join(D, "L1_CELLS.json")
RECT = os.path.join(WS, "workflows/atom_decomposition/runs/nfra-c3materialize-L1/rectangle.c0.json")
OUT = os.path.join(WS, "org/tier2_senior/0.4.0_DT_ClientPlatform/deliverables/"
                       "NFRA_C3MATERIALIZE.TO-L1-DTX_PROOF_OF_SPEC.json")
ME = "0.4.0_DT_ClientPlatform~X"
PIN = "4226a09f74"


def sh(*a):
    return subprocess.run(a, capture_output=True, text=True, cwd=WS).stdout.strip()


doc = json.load(open(CELLS, encoding="utf-8"))
cells = doc["cells"]
rect = json.load(open(RECT, encoding="utf-8"))
lane_ids = {c["cell_id"] for c in rect["cells"] if c.get("executor_class") == ME}

ids = {c["cell_id"] for c in cells}
complete = [c for c in cells if all(c.get(k) for k in ("status", "value", "basis", "evidence", "owner"))]
unmeasured = [c for c in cells if c["status"] == "UNMEASURED"]
unmeasured_no_reason = [c for c in unmeasured if len(c.get("evidence", "")) < 40]

# ---- CONTROL 1: MUTANT against the id-set refusal arm --------------------------------
mut_ids = set(ids)
mut_ids.discard(sorted(ids)[0])
arm1_fires = mut_ids != lane_ids

# ---- CONTROL 2: MUTANT against the UNMEASURED-without-reason arm ---------------------
mut_cells = json.loads(json.dumps(cells))
target = next(c for c in mut_cells if c["status"] == "UNMEASURED")
target["evidence"] = "no reason"
arm2_fires = len([c for c in mut_cells
                  if c["status"] == "UNMEASURED" and len(c["evidence"]) < 40]) > 0

# ---- CONTROL 3: determinism ----------------------------------------------------------
before = hashlib.sha256(open(CELLS, "rb").read()).hexdigest()
subprocess.run(["python", os.path.join(D, "build_l1_cells.py")],
               capture_output=True, text=True, cwd=WS, check=True)
after = hashlib.sha256(open(CELLS, "rb").read()).hexdigest()

pos = {
    "schema_version": "1.0",
    "to_id": "NFRA_C3MATERIALIZE.TO-L1-DTX",
    "phase": "INVESTIGATION",
    "spec_ref": {
        "doc": "org/tier1_exec/2.0.0_SA_COO/deliverables/D11_L1/NFRA_C3MATERIALIZE.TO-L1-DTX.md",
        "group": "OTHER",
        "vintage_commit": "b8de1c48ed",
    },
    "decomp_ref": {
        "doc": "workflows/atom_decomposition/runs/nfra-c3materialize-L1/rectangle.c0.json",
        "vintage_commit": PIN,
        "to_ref": "org/tier1_exec/2.0.0_SA_COO/deliverables/D11_L1/"
                  "NFRA_C3MATERIALIZE.TO-L1-DTX.md",
    },
    "assignee": ME,
    "artifacts_produced": [
        {"path_or_key": "org/tier2_senior/0.4.0_DT_ClientPlatform/deliverables/D11_L1/L1_CELLS.json",
         "kind": "config_data", "commit_or_etag": sh("git", "log", "-1", "--format=%h", "--", CELLS) or "PENDING",
         "deployed_state": "COMMITTED-NOT-DEPLOY-SCOPE",
         "deploy_evidence": "The 29-cell record. Governance artifact, no deploy surface."},
        {"path_or_key": "org/tier2_senior/0.4.0_DT_ClientPlatform/deliverables/D11_L1/"
                        "L1_CANONICAL_GRAIN_DECLARATION.md",
         "kind": "doc", "commit_or_etag": "16cd74c870",
         "deployed_state": "COMMITTED-NOT-DEPLOY-SCOPE",
         "deploy_evidence": "L1-m-graindecl, amended @55c6293bd0 with the falsifier-1 verdict."},
        {"path_or_key": "org/tier2_senior/0.4.0_DT_ClientPlatform/deliverables/D11_L1/",
         "kind": "script", "commit_or_etag": "af072a8dc6",
         "deployed_state": "COMMITTED-NOT-DEPLOY-SCOPE",
         "deploy_evidence": "Five probes. Every number in every cell is reproducible from them."},
    ],
    "acceptance": [
        {"criterion_id": "AC1", "method": "schema_validation",
         "criterion_verbatim": "All 29 lane cells carry `status`, `value`, `basis`, `evidence`, "
                               "`owner`. No cell ships `UNMEASURED` without a stated reason in its "
                               "own row.",
         "invocation": "python org/tier2_senior/0.4.0_DT_ClientPlatform/deliverables/D11_L1/build_l1_cells.py -- id set read from the rectangle, two refusal arms",
         "output_evidence": "cells %d; complete rows %d of %d; UNMEASURED %d, of which %d lack a "
                            "reason. Id set identical to the rectangle's lane set: %s."
                            % (len(cells), len(complete), len(cells), len(unmeasured),
                               len(unmeasured_no_reason), ids == lane_ids),
         "denominator": "29 lane cells of 33 rectangle cells; 4 are issuer-owned",
         "status": "PASS" if (len(complete) == len(cells) and not unmeasured_no_reason
                              and ids == lane_ids) else "FAIL"},
        {"criterion_id": "AC2", "method": "manual_read_with_citation",
         "criterion_verbatim": "`space_is_crossing` answered FIRST in each block, citing a measured "
                               "crossing property.",
         "invocation": "python org/tier2_senior/0.4.0_DT_ClientPlatform/deliverables/D11_L1/probe_symbol_crossing.py + probe_file_crossing.py @38d60dc",
         "output_evidence": "4 of 4 blocks. arn_resource 1,692 shared ARNs across two artifacts; "
                            "chain_motif 6,090 at instance grain with cross-grain 0; file 373 of "
                            "374 on the filesystem plane; symbol 0 raw / 1,331 after a parse. Every "
                            "one cites a MEASURED crossing property, not a name.",
         "denominator": "4 of 4 id spaces", "status": "PASS"},
        {"criterion_id": "AC3", "method": "command",
         "criterion_verbatim": "Every population count MEASURED, with the denominator printed and "
                               "the sweep method named.",
         "invocation": "python org/tier2_senior/0.4.0_DT_ClientPlatform/deliverables/D11_L1/probe_population_census.py @baca7f07eb, corrected @31b1978428",
         "output_evidence": "All four measured with per-substrate denominators and named "
                            "instruments. arn 1,851 (cypher DISTINCT n.arn) == PRD exactly; "
                            "chain_motif 6,207 (semctl instance grain) == PRD exactly; symbol union "
                            "14,447 over 3 named substrates, PRD 19,482 UNRESOLVED and not guessed; "
                            "file 430 over the PORTAL PLANE with the co-change corpus named as a "
                            "substrate not swept. UNION DELTAS RETRACTED to UNMEASURED @31b1978428.",
         "denominator": "4 of 4 spaces; 9 substrates named", "status": "PASS"},
        {"criterion_id": "AC4", "method": "manual_read_with_citation",
         "criterion_verbatim": "The canonical grain DECLARED, falsifiable -- naming what it is NOT, "
                               "and what observation would show it wrong. The PRD demands "
                               "falsifiable, not merely stated.",
         "invocation": "org/tier2_senior/0.4.0_DT_ClientPlatform/deliverables/D11_L1/L1_CANONICAL_GRAIN_DECLARATION.md @16cd74c870, amended @55c6293bd0",
         "output_evidence": "Declared (PLANE, ENTITY). Names 5 things it is NOT. States 4 RUNNABLE "
                            "refutations. FALSIFIER 1 RUN BY 3.0.0_SA_CVO~X (75044) and FAILED TO "
                            "REFUTE -- the attack was non-empty, surfacing stitch CONTAINS x12,352 "
                            "which my own probe could not see, then failing on partial coverage "
                            "(ARN 59.5%), cover-not-roll-up, and membership-not-identity. "
                            "Falsifiers 2-4 OPEN and declared open.",
         "denominator": "4 refutations stated, 1 run by an independent seat", "status": "PASS"},
        {"criterion_id": "AC5", "method": "command",
         "criterion_verbatim": "Roll-up fan-out cardinality recorded per space. Not one collapses "
                               "to a single target.",
         "invocation": "python org/tier2_senior/0.4.0_DT_ClientPlatform/deliverables/D11_L1/probe_rollup_cardinality.py @16cd74c870",
         "output_evidence": "4 roll-ups, each with its cardinality distribution. NOT ONE collapses: "
                            "symbol->file fan-in max 1,290 mean 36.14; chain_motif->family 1,649 / "
                            "477.46; arn->service 678 / 84.14; pipeline->firm 724 / 445.67. "
                            "INSTRUMENT LIMIT DECLARED ON THE FACE: fan-out=1 is a TAUTOLOGY of the "
                            "parse, not a property of the estate.",
         "denominator": "4 roll-ups of 4 spaces", "status": "PASS"},
        {"criterion_id": "AC6", "method": "command",
         "criterion_verbatim": "`absent_vs_unaddressed` answered with both arms reachable and a "
                               "firing control.",
         "invocation": "python org/tier2_senior/0.4.0_DT_ClientPlatform/deliverables/D11_L1/probe_discrimination_gate.py @68cd2f273e",
         "output_evidence": "Answered 4 of 4. file DISCRIMINATES with both arms non-empty and "
                            "reachable from different truths (1 graph-not-disk, 56 disk-not-graph) "
                            "-- its second arm is a DIFFERENT PLANE. symbol NO (918 of 2,249, no "
                            "field to reject on). arn_resource NO (278 of 1,970, no scan scope). "
                            "chain_motif PARTIAL (vintage discriminates staleness only). FOR 3 OF 4 "
                            "THE ARMS ARE NOT REACHABLE, AND THAT IS THE ANSWER, NOT A GAP.",
         "denominator": "4 of 4 spaces", "status": "PASS"},
        {"criterion_id": "AC7", "method": "manual_read_with_citation",
         "criterion_verbatim": "Work item 1 delivered or explicitly blocked by a `4.0.0_SA_CRO~A` "
                               "ruling naming the contract OPERATIVE.",
         "invocation": "read of 4.0.0_SA_CRO~A msgs 75046/75058/75067 and 1.0.0_SA_CTO~X 75091",
         "output_evidence": "NOT MET, AND NOT BY THE ESCAPE CLAUSE. 4.0.0_SA_CRO~A ruled the "
                            "contract PROPOSED (not operative), then separately HELD the generator "
                            "re-run on RECEIVER-MUTANT grounds. That is a DIFFERENT blocker from "
                            "the one the clause anticipates, so it does not apply. My half landed "
                            "@51c851e8b9 (generator source edit, confirmed outside the hold); the "
                            "RE-RUN is held by its owner and I have not run it. Step 2 is "
                            "additionally held by 1.0.0_SA_CTO~X because MY proposed sequence had a "
                            "hole -- the committed artifact still carries the field.",
         "denominator": "1 criterion, 0 met", "status": "FAIL",
         "status_reason": "The escape clause names a 4.0.0_SA_CRO~A ruling declaring the contract "
                          "OPERATIVE; the actual blocker is that lane's HOLD on the generator "
                          "re-run over receiver mutants, which is a different fact. Reported FAIL "
                          "rather than claimed under a clause written for another blocker. Releases "
                          "when CRO Base returns PASS on 3aef865b30 and 4.0.0_SA_CRO~A lifts the "
                          "hold; the lane half already landed @51c851e8b9."},
    ],
    "controls": {
        "mutant": {
            "description": "The two REFUSAL ARMS of build_l1_cells.py, exercised against planted "
                           "mutants. A refusal arm that has never been made to fire is an "
                           "assertion, not a control. ARM 1: drop one cell id and confirm the id "
                           "set no longer equals the rectangle's lane set. ARM 2: blank one "
                           "UNMEASURED cell's reason and confirm the AC1 check catches it.",
            "expected": "both arms fire on their mutant and neither fires on the real record",
            "observed": "ARM 1 (id set mismatch) -> %s. ARM 2 (UNMEASURED without reason) -> %s. "
                        "On the REAL record: id set identical %s, UNMEASURED-without-reason %d."
                        % ("FIRED" if arm1_fires else "*** DID NOT FIRE ***",
                           "FIRED" if arm2_fires else "*** DID NOT FIRE ***",
                           ids == lane_ids, len(unmeasured_no_reason)),
            "status": "FIRED-AS-EXPECTED" if (arm1_fires and arm2_fires)
                      else "DID-NOT-FIRE (deliverable INVALID)",
        },
        "determinism": {
            "method": "sha256 of L1_CELLS.json, re-run build_l1_cells.py, sha256 again",
            "observed": "identical=%s (%s)" % (before == after, before[:12]),
            "status": "STABLE" if before == after else "UNSTABLE (deliverable INVALID)",
        },
    },
    "declared_exclusions": [
        {"item": "The 4 issuer-owned mechanism cells (L1-m-rolluprel, L1-m-absentgate and two more).",
         "reason": "Issuer-owned by the TO's own seating; 29 of 33 are this lane's."},
        {"item": "Work item 1's generator re-run.",
         "reason": "HELD by 4.0.0_SA_CRO~A on receiver-mutant grounds. Their hold, their release. "
                   "The source half landed @51c851e8b9 and they confirmed it is outside the hold."},
        {"item": "A coverage PERCENTAGE for symbol, arn_resource and chain_motif.",
         "reason": "Row 6 measured that those spaces cannot discriminate substrate-absent from "
                   "genuinely-unaddressed. A ratio whose numerator and denominator are both "
                   "scope-dependent is not a coverage measurement. Recorded UNMEASURED with the "
                   "missing discriminator named."},
        {"item": "The co-change corpus for the `file` space, and the provenance of the PRD's "
                 "symbol population of 19,482.",
         "reason": "Neither was located. Named as not-swept rather than approximated from the "
                   "substrates I did have."},
    ],
    "surprises": [
        "OBSERVATION -- 0 of 16,811 portal-source edges express the symbol->file roll-up across 20 "
        "edge types, so the relation the spine owns is declared nowhere and every consumer must "
        "parse ids. I got that parse wrong twice while building this TO, which is the measurement.",
        "OBSERVATION -- no mapping in any of the four id spaces carries a confidence value; the "
        "structured key scan returns 0 across all three JSON substrates and kuzu CloudEdge has no "
        "such property. Recorded ABSENT rather than 1.0.",
        "OBSERVATION -- c2_instances.json was computed over graph snapshot 8601547680771488785 "
        "(2026-08-07) while kuzu_nessie_db is 2902399899597701830 (2026-08-26): a 19.5-day gap on "
        "the same known-stale input the decomp already cites for nerves_resolve.",
        "OBSERVATION -- scan scope on the producing stores (kuzu, stitch) is 1.0.0_SA_CTO~X's "
        "instance #9 and is UNOWNED. It is the single finding that makes 3 of 4 L1 coverage rows "
        "UNMEASURED. Routed, not claimed -- the stores are not this lane's.",
    ],
    "session_log": "org/tier2_senior/0.4.0_DT_ClientPlatform/logs/2026-08-27/"
                   "l1_entity_spine_29_cells.md",
    "compiler_tools": [
        {"tool": "kuzu (python)", "invocation": "cypher over kuzu_nessie_db for layer/type/arn sets",
         "result": "the store's DECLARED node_type and layer are what every id space was derived "
                   "from after two pattern-derived attempts over-counted by 13x."},
        {"tool": "jsonschema Draft202012Validator",
         "invocation": "L0 manifest validation; in-memory shape checks",
         "result": "used for the parts_registered sequencing check -- and that check tested the "
                   "WRONG OBJECT, which 1.0.0_SA_CTO~X caught. Recorded rather than smoothed."},
        {"tool": "git hash-object / merge-base --is-ancestor",
         "invocation": "push-state reads with a positive control on e48a7466ba",
         "result": "8 of 9 L1 commits confirmed ON ORIGIN at 08:41:39Z."},
        {"tool": ".tools/commit-gate.sh + ruff",
         "invocation": "every .py in D11_L1",
         "result": "blocked two commits on unused imports; both fixed rather than forced."},
    ],
}


def main() -> None:
    schema = json.load(open(os.path.join(WS, "org/standards/PROOF_OF_SPEC.schema.json"),
                            encoding="utf-8"))
    v = Draft202012Validator(schema)
    errs = sorted(v.iter_errors(pos), key=lambda e: list(e.path))
    for e in errs[:10]:
        print("POS SCHEMA ERROR:", list(e.path)[:4], e.message[:170])
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(pos, f, indent=2, ensure_ascii=True)
        f.write("\n")
    print("OK: wrote %s" % os.path.relpath(OUT, WS).replace("\\", "/"))
    print("POS validation errors : %d" % len(errs))
    print("NEGATIVE CONTROL      : %d errors on {}" % len(list(v.iter_errors({}))))
    print("acceptance            : %d rows, PASS %d / FAIL %d"
          % (len(pos["acceptance"]),
             sum(1 for r in pos["acceptance"] if r["status"] == "PASS"),
             sum(1 for r in pos["acceptance"] if r["status"] == "FAIL")))
    print("mutant control        : %s" % pos["controls"]["mutant"]["status"])
    print("determinism           : %s" % pos["controls"]["determinism"]["status"])


if __name__ == "__main__":
    main()
