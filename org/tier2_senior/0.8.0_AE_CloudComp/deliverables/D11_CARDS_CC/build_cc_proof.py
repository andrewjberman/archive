#!/usr/bin/env python3
"""Build the TO-CARD-R-CC proof of spec.

criterion_verbatim is EXTRACTED from the face's bytes, never retyped.

Run:  python org/tier2_senior/0.8.0_AE_CloudComp/deliverables/D11_CARDS_CC/build_cc_proof.py
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
FACE = ROOT / ("org/tier2_senior/0.8.0_AE_CloudComp/task_orders/"
               "NFRA_SUBSTRATECARDING.TO-CARD-R-CC.carding.md")
CARDS = ROOT / "org/tier2_senior/0.8.0_AE_CloudComp/deliverables/D11_CARDS_CC"
SCHEMA = ROOT / "org/standards/SUBSTRATE_CARD.v3.1.schema.json"
OUT = ROOT / ("org/tier2_senior/0.8.0_AE_CloudComp/deliverables/"
              "NFRA_SUBSTRATECARDING.TO-CARD-R-CC_PROOF_OF_SPEC.json")
PEND = "PENDING-THIS-COMMIT"
RECEIPT = "4 of 20 uncarded / 35 remainder"
FILES = ("code_heat_emit", "cse_producers_nightly", "emit_fedobs_snap", "ms_cloud_extract")

DEN = {
    "CC-AC1": "2 load-bearing writers named by the oracle; 0 of them on this face; 1 gate receipt cited",
    "CC-AC2": "20 uncarded = 19 manifest writers (census sec 3) + rebuild.tmp.SET (sec 2); 4 of the 19 owned here. Receipt: " + RECEIPT,
    "CC-AC3": "4 cards x 7 questions x 3 grains = 84 rows; rows 5/6/7 measured or honestly absent on 4 of 4 cards",
    "CC-AC4": "4 of 4 cards written from a read of the writer; 0 generated from a manifest entry; 3 of 4 DISAGREE with the manifest's write-path count, in three different directions",
    "CC-AC5": "4 of 4 at this face's grain; 4 of 20 at the class grain. The oracle's 20 of 20 is a CLASS figure and is not this face's to claim",
}

EVIDENCE = {
    "CC-AC1": (
        "DISCHARGED BY CITATION, NOT BY RE-CARDING, and the issuer confirmed that reading at 85553. "
        "The oracle names derive_stitch.py and kuzu_nessie_load.py as carded FIRST and the gate on "
        "the rest. NEITHER IS ON THIS FACE: both are TO-CARD-R-AE cards 1-2 at 0.7.0_AE_CloudOps~K, "
        "PASSED by 3.0.0_SA_CVO~X at 03:22Z and 03:27Z, cards @d31070ec0b and @d7f74b7a59. The face's "
        "own <sequenced_after> records the gate OPEN since 03:27Z. So the cell is satisfied by citing "
        "that receipt: the class cell is shared across faces and the gate it names is open. A face "
        "re-carding another lane's subjects to satisfy a cell it holds would manufacture a second "
        "carrier for those two writers -- the exact defect the carding project exists to remove."
    ),
    "CC-AC2": (
        "ENUMERATED FROM THE CENSUS AT ITS PIN: git show 9b2c687dc8:org/tier1_exec/1.0.0_SA_CTO~Y/"
        "deliverables/D11_SUBSTRATECARDING_COVERAGE_CENSUS_20260829.md, 11,395 bytes, sha256 "
        "83ef53654e82648bb1bd63f0ff5c45d064d775627b4e252d8ba62d8be7a96767. Sec 3 lists 19 UNCARDED "
        "writers (32 resolvable generator paths named by the manifest, 13 already carded); sec 6 "
        "composes the 20 as those 19 plus kuzu_nessie_db.rebuild.tmp.SET from sec 2, which AC2 names "
        "explicitly because a subject that looks like a temp artifact is the one a reader drops. All "
        "FOUR of this face's subjects appear in sec 3's table by name and were checked individually. "
        "RECONCILE PASSES. The 35 on the receipt is derived from sec 6's own table (20 no-card + 7 "
        "cells-only + 8 v1-only), not carried from the dispatch. AND THE CENSUS'S FLOOR NOTE IS "
        "CARRIED RATHER THAN FLATTENED: it says the 19 are counted at FILE grain and each may split "
        "into more than one WRITE PATH, so 19 is a floor. This face measured that split on four "
        "writers and it is the dominant effect -- see AC4."
    ),
    "CC-AC3": (
        "ALL 7 QUESTIONS ACROSS 3 GRAINS ON 4 OF 4 CARDS, with 5/6/7 answered rather than hand-waved. "
        "Every row carries basis + evidence + owner. The hard rows, per card: COVERAGE -- three of "
        "four carry denominator null with a MEASURED absence reason naming what would have to be run "
        "to get one, and code_heat's names the trap explicitly (its source asserts a 374/374 "
        "join-coverage figure that is NOT the writer's output cardinality). KEY -- code_heat's "
        "graph_path is measured and its stability is called UNSTABLE because the key is a file path; "
        "cse's event_id is measured AND exercised by the subject itself as its own dedup spine; "
        "fedobs's four convention columns are measured with the producer_ref 12-char truncation named "
        "as non-injective; ms_cloud's key_is_stable is 'unknown' and HELD because item-id stability "
        "across move/rename is Microsoft's guarantee, not one this card can assert. FAILURE MODE -- "
        "distinguishable_from_true_negative is answered yes/yes/NO/yes, and the one NO is the "
        "sharpest finding on the face: emit_fedobs_snap prints the SAME line for a broken producer "
        "and an absent signal. A FULL 7-ROW FLOOR AUDIT runs over all cards (scalar == min of "
        "basis_by_field, measured > held > inferred > absent): 0 violations. The schema mechanises "
        "that rule on trust.key ONLY, so the other six rows are covered by this audit -- which is "
        "what caught ms_cloud's artifact.location scalar before presentation."
    ),
    "CC-AC4": (
        "NO CARD WAS GENERATED. Each writer was read at its own commit with git status confirming a "
        "clean worktree, so each read carries a vintage: code_heat_emit @c934701a67 (14,812 B / 298 "
        "L), cse_producers_nightly @9369f74518 (22,210 B / 448 L), emit_fedobs_snap @85a4b4e006 "
        "(7,626 B / 153 L), ms_cloud_extract @f861a238e6 (31,519 B / 656 L). "
        "THE PROOF THAT THESE ARE READINGS AND NOT MANIFEST RESTATEMENTS IS THAT THREE OF FOUR "
        "DISAGREE WITH THE MANIFEST, IN THREE DIFFERENT DIRECTIONS -- an outcome a generator cannot "
        "produce, because a generator's cards agree with their source by construction: "
        "(1) code_heat_emit -- TWO write paths, manifest names one. The parquet at warehouse/"
        "code_heat/ is a second published surface beside the code_heat_snap staging path. "
        "(2) cse_producers_nightly -- SIX write paths, manifest names one: the cse append, done/, "
        "rejected/, last_run.json, last_append.json and the 4-table marker. "
        "(3) emit_fedobs_snap -- ONE write path, matching. The undercount is a property of particular "
        "writers, not of the manifest as such, and this card is the control that shows it. "
        "(4) ms_cloud_extract -- ZERO write paths. A token census over its 656 lines returns "
        "put_object 0 / boto3 0 / 'import s3' 0 / 'open(' 0 / 'write(' 0 / to_parquet 0, with a "
        "positive control on the same instrument ('^def ' -> 18). It mutates the caller's dict and "
        "returns; ms_heat_snap appears 0 times in it and 12 times in snap_store.py, which registers "
        "and appends that surface. The reading consistent with the evidence is that the manifest's "
        "generation.materializer is not uniformly at (file, write-path) grain -- for that part it "
        "names a DATA ORIGIN upstream of the byte-writer. I did not trace this module's MS nodes to "
        "ms_heat_snap rows and say so on the card rather than asserting the link."
    ),
    "CC-AC5": (
        "UNCOMPUTABLE-BY-CONSTRUCTION AT THE ORACLE'S GRAIN, WITH BOTH NUMERATORS PRINTED, per the "
        "issuer's 85553 instruction and the 0.4.0_DS_ClientPlatform~V precedent CVO~X accepted at "
        "85289. The oracle says '20 of 20 at v3.1 with the two load-bearing writers landed and "
        "verified first'. That is a CLASS figure spanning every face in the wave; this face carries 4 "
        "subjects. FACE GRAIN: 4 of 4 delivered, each VALID against SUBSTRATE_CARD.v3.1 (sha256 "
        "19a3547047b750c8c1493eef4515824d847ae4016510245fad87ee4d3b790d5c, const 3.1), each rc=0 on "
        ".tools/substrate-card-check.py, each with three shaped negatives returning rc=1 -- "
        "self-adjudicated set_by, key_expression basis 'inferred', question 7 removed. rc read PER "
        "ARM: rc=1 is INVALID and rc=2 is READ-ERROR, a distinction an rc!=0 test loses and one my "
        "own control hit early on a mutant file that had silently failed to write. CLASS GRAIN: 4 of "
        "20, plus the two load-bearing gate cards and DS~V's -- the class total is the issuer's "
        "aggregation across faces and is never a face's claim. PARTIAL IS REPORTED AS PARTIAL: this "
        "face is complete at its own grain and incomplete at the class's, and both numbers are on "
        "every artifact rather than one standing in for the other."
    ),
}


def face_oracles() -> dict[str, dict[str, str]]:
    text = FACE.read_text(encoding="utf-8")
    out = {}
    for m in re.finditer(
        r'<criterion id="([^"]+)"[^>]*>\s*<label>([^<]*)</label>\s*<oracle>(.*?)</oracle>',
        text, re.S,
    ):
        cid, label, oracle = m.groups()
        out[cid] = {"label": label.strip(), "oracle": " ".join(oracle.split())}
    return out


def main() -> None:
    oracles = face_oracles()
    if set(oracles) != set(EVIDENCE):
        raise SystemExit(f"FAIL: face {sorted(oracles)} != evidence {sorted(EVIDENCE)}")

    acceptance = [
        {
            "criterion_id": cid,
            "criterion_verbatim": oracles[cid]["oracle"],
            "method": "schema_validation",
            "invocation": ("python .tools/substrate-card-check.py <card> plus a Draft202012Validator "
                           "pass over SUBSTRATE_CARD.v3.1, a 3-arm shaped-negative battery per card, "
                           "and a 7-row floor audit; inputs read via git show <pin>:<path>"),
            "output_evidence": EVIDENCE[cid],
            "denominator": DEN[cid],
            "status": "UNCOMPUTABLE-BY-CONSTRUCTION" if cid == "CC-AC5" else "PASS",
            **({"status_reason": (
                "The oracle's '20 of 20' is a CLASS-grain figure over every face in the wave; this "
                "face carries 4 subjects. Written with both numerators (4 of 4 face, 4 of 20 class) "
                "per the issuer's 85553 direction and the DS~V precedent; the class total is the "
                "issuer's aggregation, never a face's claim.")} if cid == "CC-AC5" else {}),
        }
        for cid in sorted(oracles, key=lambda c: int(c.rsplit("AC", 1)[1]))
    ]

    arts = [
        {
            "path_or_key": f"org/tier2_senior/0.8.0_AE_CloudComp/deliverables/D11_CARDS_CC/{n}.v3.1.json",
            "kind": "config_data",
            "commit_or_etag": PEND,
            "deployed_state": "COMMITTED-NOT-DEPLOY-SCOPE",
            "deploy_evidence": (f"Carded at v3.1 from a read of the writer at its own pin. VALID; "
                                f"substrate-card-check rc=0. Receipt: {RECEIPT}."),
            "artifact_covered_by": ["CC-AC2", "CC-AC3", "CC-AC4", "CC-AC5"],
        }
        for n in FILES
    ]
    arts.append({
        "path_or_key": ("org/tier2_senior/0.8.0_AE_CloudComp/deliverables/D11_CARDS_CC/"
                        "build_cc_proof.py"),
        "kind": "script",
        "commit_or_etag": PEND,
        "deployed_state": "COMMITTED-NOT-DEPLOY-SCOPE",
        "deploy_evidence": "Proof builder; criterion_verbatim extracted from the face's bytes.",
        "artifact_covered_by": ["CC-AC1", "CC-AC2", "CC-AC3", "CC-AC4", "CC-AC5"],
    })

    proof = {
        "schema_version": "1.0",
        "to_id": "NFRA_SUBSTRATECARDING.TO-CARD-R-CC",
        "firm": "FABRIC",
        "phase": "NON-BUILD-OTHER",
        "assignee": "0.8.0_AE_CloudComp~Y",
        "decomp_ref": {
            "doc": ("workflows/atom_decomposition/runs/nfra-substratecarding/"
                    "20260829T1129Z/rectangle.final.certified.json"),
            "vintage_commit": "603f5546dc",
            "to_ref": ("org/tier2_senior/0.8.0_AE_CloudComp/task_orders/"
                       "NFRA_SUBSTRATECARDING.TO-CARD-R-CC.carding.md"),
        },
        "spec_ref": {
            "doc": "org/standards/SUBSTRATE_CARD.v3.1.schema.json",
            "group": "OTHER",
            "vintage_commit": "6a0e8e85de",
        },
        "artifacts_produced": arts,
        "acceptance": acceptance,
        "controls": {
            "mutant": {
                "description": (
                    "Three shaped negatives per card, 12 arms across the face, each a failure the "
                    "v3.1 contract exists to catch: a self-adjudicated forward_disposition set_by "
                    "(the CCY-F1 class, now mechanised in .tools/substrate-card-check.py), a "
                    "key_expression whose basis is 'inferred' (v3.1's own narrowing), and substrate "
                    "question 7 removed. Paired with the four unmutated cards as the positive "
                    "control. A FULL 7-ROW FLOOR AUDIT runs beside them because the schema mechanises "
                    "the floor rule on trust.key only."),
                "expected": "All 12 arms rc=1 INVALID; the four real cards rc=0 VALID; floor audit 0.",
                "observed": (
                    "12 of 12 REFUSED at rc=1; 4 of 4 cards VALID at rc=0; floor audit 0 violations "
                    "across 7 cards x 7 rows. rc READ PER ARM, not as non-zero: rc=1 is INVALID and "
                    "rc=2 is READ-ERROR, and an early control of mine returned rc=2 on a mutant file "
                    "that had silently failed to write -- an rc!=0 test would have scored that "
                    "instrument failure as a firing control. The floor audit earned its place: it "
                    "caught ms_cloud_extract's artifact.location scalar (held where the floor was "
                    "absent) before presentation, on a row the validator does not check."),
                "status": "FIRED-AS-EXPECTED",
            },
            "determinism": {
                "status": "N/A-WITH-REASON",
                "method": ("The cards are HAND-AUTHORED from readings of the subjects, which is the "
                           "TO's central requirement (AC4: no card without a reading). There is no "
                           "build step to re-run, so a determinism control has no subject. The "
                           "reproducible half is the VALIDATION, which is deterministic against a "
                           "pinned schema digest."),
                "observed": ("Schema digest 19a3547047b750c8c1493eef4515824d847ae4016510245fad87ee4"
                             "d3b790d5c stable across runs; 4 of 4 VALID reproduces."),
            },
        },
        "declared_exclusions": [
            {"item": "derive_stitch.py and kuzu_nessie_load.py -- AC1's two load-bearing writers.",
             "reason": ("TO-CARD-R-AE cards 1-2 at 0.7.0_AE_CloudOps~K, both PASSED by CVO~X. AC1 is "
                        "discharged on this face by citing that gate receipt; re-carding them here "
                        "would manufacture a second carrier.")},
            {"item": "The other 15 of the census's 20 uncarded subjects.",
             "reason": f"Not this face's scope. Receipt is stated as {RECEIPT}, never as complete."},
            {"item": "Running any of the four writers to obtain a coverage denominator.",
             "reason": ("Out of scope for a carding read, and three of the four require the live "
                        "plane (Nessie in-VPC, the MS gateway, or the served fedobs artifact). The "
                        "consequence is carried honestly instead: those denominators are null with "
                        "measured absence reasons, and the row scalars take the floor.")},
            {"item": "Tracing ms_cloud_extract's MS_CLOUD nodes through to ms_heat_snap rows.",
             "reason": ("Would require carding derive_runner and snap_store, neither of which is on "
                        "this face. The link is recorded as UNVERIFIED on the card rather than "
                        "asserted or denied.")},
            {"item": "Any change to the manifest, the census, or the writers themselves.",
             "reason": "The writers are SUBJECTS to be read. No deploy, no infra change, per the face."},
        ],
        "surprises": [
            ("OBSERVATION / INERT (3.0.0_SA_CVO~X, cc 2.0.0_SA_COO~X): THE MANIFEST'S materializer "
             "FIELD IS NOT AT A UNIFORM GRAIN, measured across four writers in one directory. Two "
             "undercount (2 and 6 write paths against 1 named), one matches, and one names a file "
             "with ZERO write primitives while the surface is registered and appended by "
             "snap_store.py. The census's own FLOOR note anticipated the undercount half; the "
             "zero-writer half is the other direction and is not anticipated anywhere I found. This "
             "is offered as a reading of the evidence, not as a defect claim against the manifest -- "
             "the honest statement is that generation.materializer sometimes names a data ORIGIN "
             "rather than a byte-WRITER, and a consumer counting writers from it gets a number whose "
             "grain varies by row."),
            ("OBSERVATION / INERT (3.0.0_SA_CVO~X, cc 2.0.0_SA_COO~X): TWO MIRROR-IMAGE TRIGGER TRAPS "
             "ON ONE FACE, both mine and both caught. cse_producers_nightly.py was FALSE-ZEROED by a "
             "FILE-name-shaped token ('cse_producers' against the live 'globgrph-cse-producer'), "
             "which would have carded a nightly Fargate task as a manual CLI. emit_fedobs_snap.py was "
             "FALSE-POSITIVED by a RESOURCE-name-shaped token ('fedobs' matched the producer family), "
             "and I asserted that error to two seats and into a PASSED card before the terraform "
             "settled it: the rule targets ['python', '/app/fedobs_observe.py'], a different "
             "component. THE RULE THAT COVERS BOTH: a trigger census must resolve WHAT THE RULE "
             "TARGETS -- which lives in the task definition's command -- never what shares its "
             "prefix. A file's name and a resource's name are different identifiers."),
            ("OBSERVATION / INERT (3.0.0_SA_CVO~X, cc 2.0.0_SA_COO~X): THE FLOOR RULE IS ENFORCED ON "
             "ONE ROW OF SEVEN, AND THE OTHER SIX ARE WHERE MY VIOLATIONS WERE. The schema's own "
             "clause says it mechanises only the basis='measured' case on trust.key, 'the one that "
             "over-promises a consumer', and states the full ordering is not machine-enforceable. "
             "Across this session I wrote three floor violations: one on trust.key (caught by the "
             "schema), one on trust.coverage in two cards (caught by CVO~X's ruling), and one on "
             "artifact.location (caught by the 7-row audit I built after that ruling). The audit is "
             "eight lines and now runs per card. Offered because the next lane will write the same "
             "shape and the validator will not tell them."),
        ],
        "session_log": ("org/tier2_senior/0.8.0_AE_CloudComp/logs/2026-08-30/ (written at session "
                        "close, with a mandatory Compiler Tools section)"),
        "compiler_tools": [
            {"tool": "comp-to",
             "invocation": "comp-to NFRA_SUBSTRATECARDING.TO-CARD-R-CC",
             "result": "PASS -- bound and read back before the first tool run of this TO."},
            {"tool": "git show (pinned read) + git status",
             "invocation": "git show 9b2c687dc8:<census>; per-subject git log -1 and git status --porcelain",
             "result": ("PASS. The census was read through its pin and hashed. Each subject was read "
                        "from the worktree WITH both its log line and its status printed beside it, "
                        "so every read carries a vintage. Also the instrument that settled the fedobs "
                        "misattribution: the DECLARED plane (terraform) names what the rule targets.")},
            {"tool": "comp-find",
             "invocation": "--corpus aws for the trigger census; scoped pathspecs for the repo plane",
             "result": ("PARTIAL. It found the live SCHEDULE and EVENT_RULE resources and its "
                        "denominators are printed. TWO LIMITS MEASURED: an unscoped content query "
                        "over 136k files exceeded 120s twice and had to be scoped to a pathspec, and "
                        "--corpus aws timed out at 110s on a later run -- 3.0.0_SA_CVO~X reported the "
                        "same 90s failure independently and fell back to a direct read of the same "
                        "substrate.")},
            {"tool": ".tools/substrate-card-check.py",
             "invocation": "per card, plus 3 shaped negatives per card",
             "result": ("PASS, 4 of 4 rc=0 and 12 of 12 negatives rc=1. This checker exists because "
                        "of CCY-F1, a defect of mine on the previous TO; it now mechanically refuses "
                        "the self-adjudication I committed there.")},
            {"tool": "jsonschema (2020-12) + a 7-row floor audit",
             "invocation": "Draft202012Validator over SUBSTRATE_CARD.v3.1; scalar == min(basis_by_field) per row",
             "result": ("PASS after repair. The schema caught one floor violation on trust.key; the "
                        "audit caught one on artifact.location that the schema does not check.")},
        ],
    }

    OUT.write_text(json.dumps(proof, indent=1) + "\n", encoding="utf-8")
    print(f"OK: wrote {OUT.relative_to(ROOT)}")
    print(f"OK: {len(acceptance)} criteria, oracles EXTRACTED from the face")
    print(f"OK: contract sha256 {hashlib.sha256(SCHEMA.read_bytes()).hexdigest()}")
    print(f"OK: receipt {RECEIPT}")
    for a in acceptance:
        print(f"   {a['criterion_id']}  status={a['status']}")


if __name__ == "__main__":
    main()
