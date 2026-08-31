#!/usr/bin/env python3
"""Build the TO-CARD-R-W1-CCY proof of spec.

criterion_verbatim is EXTRACTED from the face's bytes (now attribute-form after the issuer's
6a0e8e85de repair), never retyped.

Run:  python org/tier2_senior/0.8.0_AE_CloudComp/deliverables/D11_CARDS/build_w1ccy_proof.py
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
FACE = ROOT / ("org/tier2_senior/0.8.0_AE_CloudComp/task_orders/"
               "NFRA_SUBSTRATECARDING.TO-CARD-R-W1-CCY.carding.md")
CARDS = ROOT / "org/tier2_senior/0.8.0_AE_CloudComp/deliverables/D11_CARDS"
SCHEMA = ROOT / "org/standards/SUBSTRATE_CARD.v3.1.schema.json"
OUT = ROOT / ("org/tier2_senior/0.8.0_AE_CloudComp/deliverables/"
              "NFRA_SUBSTRATECARDING.TO-CARD-R-W1-CCY_PROOF_OF_SPEC.json")
PEND = "PENDING-THIS-COMMIT"
RECEIPT = "3 of 8 wave-1 / 35 remainder"

DEN = {
    "W1-CCY-AC1": ("8 wave-1 rungs enumerated from the census sec 5; 3 of them owned by this lane. "
                   "Receipt on every artifact: " + RECEIPT),
    "W1-CCY-AC2": "3 of 3 subjects re-carded by reading the subject; 0 migrator runs, 0 fields copied from a v1 card",
    "W1-CCY-AC3": "6 of 6 v1 cards in this lane's D11_CARDS directory owner-resolved on 2 independent carriers; 3 of 6 resolve to this lane",
    "W1-CCY-AC4": ("3 of 3 owned subjects VALID against SUBSTRATE_CARD.v3.1 (positive control), "
                   "7 of 7 mutants REFUSED; " + RECEIPT + " -- partial for the class, complete for this face's scope"),
}

EVIDENCE = {
    "W1-CCY-AC1": (
        "ENUMERATED FROM THE CENSUS AT ITS PIN, not from any list retyped downstream: "
        "`git show 9b2c687dc8:org/tier1_exec/1.0.0_SA_CTO~Y/deliverables/"
        "D11_SUBSTRATECARDING_COVERAGE_CENSUS_20260829.md`, 11,395 bytes, sha256 "
        "83ef53654e82648bb1bd63f0ff5c45d064d775627b4e252d8ba62d8be7a96767. Sec 5 names the eight: "
        "C0, C1, C2, C3.i-as-built, D1, D2, D3, comp-similar -- 'all at schema_version 1, none at "
        "v3.1 ... carry no trust.key.key_expression (the field does not exist in v1). A vintage "
        "gap, not an absence.' RECONCILE PASSES IN BOTH DIRECTIONS: every subject on this face is a "
        "member of the census's 8, and no census member owned by this lane is missing from the face. "
        "The 35 is DERIVED from the census's own sec-6 table rather than carried from the dispatch: "
        "20 (no card anywhere, resolvable) + 7 (carded in a carrier the v3.1 census does not read) + "
        "8 (carded at v1 only) = 35. Sec 6's own stated denominators: cards 81 files (72 + 8 + 1); "
        "wave-1 8."
    ),
    "W1-CCY-AC2": (
        "NO MIGRATOR WAS WRITTEN OR RUN, and the reading was done at the SUBJECT rather than at the "
        "old card. Each rail was read from its home -- "
        "org/modules/graph/NFRA_ONTOLOGY_RULE_BANK.yaml#dynamic_rails.<rail> @5fc45ad69d, file "
        "sha256 d8ce6588dd68495978181b5d566a9e86f4d3e5912ce364e6f3c9ea7e9c30f249, `git status "
        "--porcelain` EMPTY so the worktree bytes equal the committed bytes and the read carries a "
        "vintage. THE PROOF THAT THIS WAS A RE-READ AND NOT A COPY IS THAT THE THREE KEY EXPRESSIONS "
        "CAME OUT DIFFERENT IN KIND, which a mechanical fill could not have produced: D1 yields a "
        "computable mapping-key expression over edge_grain_binding (basis measured); D2 yields NULL "
        "with basis ABSENT, because a path is a transitive closure with no stored identity; D3 "
        "yields a type-space expression over obligation_types (basis measured) while its INSTANCE "
        "space has no key grammar at all. A migrator filling a required field would have produced "
        "three expressions of the same shape and manufactured one for D2. The v1 cards were opened "
        "only to check for drift, never as input."
    ),
    "W1-CCY-AC3": (
        "OWNER MEASURED ON TWO INDEPENDENT CARRIERS, because the directory is wider than the face: "
        "D11_CARDS holds SIX v1 cards, not three. Carrier 1 is the card's own `carded_by` field (a "
        "self-report); carrier 2 is git's authorship of the commit that first added the file "
        "(`git log --diff-filter=A`, oldest). They agree 6 of 6: C0/C1/C2 -> 0.8.0_AE_CloudComp~X "
        "@7bb29e2514, D1/D2/D3 -> 0.8.0_AE_CloudComp~Y @c43050e9bb. A self-report and an external "
        "record agreeing is corroboration; two reads of the same field would have been repetition. "
        "C0/C1/C2 are the peer lane's and were NOT touched, though they sit in this lane's own "
        "deliverables tree. Every card names its owner in all seven row-level `owner` fields."
    ),
    "W1-CCY-AC4": (
        "3 of 3 owned subjects VALID against org/standards/SUBSTRATE_CARD.v3.1.schema.json, "
        "sha256 19a3547047b750c8c1493eef4515824d847ae4016510245fad87ee4d3b790d5c, schema_version "
        "const 3.1 -- NOT the legacy SUBSTRATE_CARD.schema.json (const 1). key_expression basis: "
        "D1 measured, D2 absent (NULL payload), D3 measured -- inside the enum the schema narrows "
        "to, and v3.1's own prohibition on 'inferred' for a key expression is one of the mutants "
        "below. NEGATIVE CONTROL, 7 arms, ALL REFUSED, each a failure this contract exists to "
        "catch: key_expression basis 'inferred'; schema_version 1; a NULL key_expression claimed as "
        "measured; key_expression removed; substrate question 7 removed; an off-enum basis; prose "
        "jammed back into a joinable id. THE BATTERY IS ONLY MEANINGFUL BECAUSE THE BASE IS GREEN, "
        "and the base was NOT green on the first run -- the schema refused all three cards for "
        "writing composes/invents/projection_of/co_resident_stores as descriptive strings instead "
        "of {id, note} joinable refs, and refused five ids again for carrying parentheticals. Both "
        "were repaired before this line was written. PARTIAL IS REPORTED AS PARTIAL: this face is "
        "3 of the class's 8; the other 5 belong to other lanes and are not claimed here."
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
        raise SystemExit(f"FAIL: face criteria {sorted(oracles)} != evidence {sorted(EVIDENCE)}")

    acceptance = [
        {
            "criterion_id": cid,
            "criterion_verbatim": oracles[cid]["oracle"],
            "method": "schema_validation",
            "invocation": ("python -c jsonschema Draft202012Validator over "
                           "org/standards/SUBSTRATE_CARD.v3.1.schema.json, plus `git show "
                           "<pin>:<path>` reads of the census and each rail at its home"),
            "output_evidence": EVIDENCE[cid],
            "denominator": DEN[cid],
            "status": "PASS",
        }
        for cid in sorted(oracles, key=lambda c: int(c.rsplit("AC", 1)[1]))
    ]

    arts = [
        {
            "path_or_key": f"org/tier2_senior/0.8.0_AE_CloudComp/deliverables/D11_CARDS/{n}.v3.1.json",
            "kind": "config_data",
            "commit_or_etag": PEND,
            "deployed_state": "COMMITTED-NOT-DEPLOY-SCOPE",
            "deploy_evidence": (f"Re-carded at v3.1 by reading the subject. VALID against "
                                f"SUBSTRATE_CARD.v3.1. Receipt: {RECEIPT}."),
            "artifact_covered_by": ["W1-CCY-AC1", "W1-CCY-AC2", "W1-CCY-AC3", "W1-CCY-AC4"],
        }
        for n in ("D1", "D2", "D3")
    ]
    arts.append({
        "path_or_key": ("org/tier2_senior/0.8.0_AE_CloudComp/deliverables/D11_CARDS/"
                        "build_w1ccy_proof.py"),
        "kind": "script",
        "commit_or_etag": PEND,
        "deployed_state": "COMMITTED-NOT-DEPLOY-SCOPE",
        "deploy_evidence": "Proof builder; criterion_verbatim extracted from the face's bytes.",
        "artifact_covered_by": ["W1-CCY-AC1", "W1-CCY-AC2", "W1-CCY-AC3", "W1-CCY-AC4"],
    })

    proof = {
        "schema_version": "1.0",
        "to_id": "NFRA_SUBSTRATECARDING.TO-CARD-R-W1-CCY",
        "firm": "FABRIC",
        "phase": "NON-BUILD-OTHER",
        "assignee": "0.8.0_AE_CloudComp~Y",
        "decomp_ref": {
            "doc": ("workflows/atom_decomposition/runs/nfra-substratecarding/"
                    "20260829T1129Z/rectangle.final.certified.json"),
            "vintage_commit": "603f5546dc",
            "to_ref": ("org/tier2_senior/0.8.0_AE_CloudComp/task_orders/"
                       "NFRA_SUBSTRATECARDING.TO-CARD-R-W1-CCY.carding.md"),
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
                    "Seven mutations of the REAL delivered cards through the same validator that "
                    "admitted them, each a failure this contract exists to catch: key_expression "
                    "basis 'inferred' (v3.1's own narrowing); schema_version 1 (the legacy contract "
                    "the issuer misrouted to and corrected @6a0e8e85de); a NULL key_expression "
                    "claimed as measured; key_expression removed; substrate question 7 "
                    "(distinguishable_from_true_negative) removed; an off-enum basis value; prose "
                    "jammed back into a joinable id. Paired with the three unmutated cards as the "
                    "positive control."),
                "expected": "All seven REFUSED; the three real cards VALID.",
                "observed": (
                    "7 of 7 REFUSED; positive control 3 of 3 VALID. STATED BECAUSE IT MATTERS: the "
                    "first run of this battery reported 5 of 5 refused while the base was REFUSED "
                    "on all three cards -- a battery from a failing base means nothing, and the "
                    "summary line asserting 'all three VALID' was hardcoded rather than derived "
                    "from the result. Both were corrected: the cards were repaired to the "
                    "joinable_ref contract and the verdict line is now computed from the "
                    "validator's own output."),
                "status": "FIRED-AS-EXPECTED",
            },
            "determinism": {
                "status": "N/A-WITH-REASON",
                "method": ("The cards are HAND-AUTHORED, not generated -- that is the TO's central "
                           "requirement (AC2: no migrator). There is no build step to re-run, so a "
                           "determinism control has no subject. The reproducible half is the "
                           "VALIDATION, which is deterministic and re-runnable against a pinned "
                           "schema digest."),
                "observed": ("Schema digest 19a3547047b750c8c1493eef4515824d847ae4016510245fad87ee"
                             "4d3b790d5c stable across runs; validation verdict 3 of 3 VALID "
                             "reproduces."),
            },
        },
        "declared_exclusions": [
            {"item": "C0, C1, C2 -- the other three v1 cards in this lane's own D11_CARDS directory.",
             "reason": ("Owner resolves to 0.8.0_AE_CloudComp~X on both carriers (carded_by field "
                        "and git creator @7bb29e2514). AC3 binds a card to the lane that authored "
                        "the rung; proximity in the filesystem is not ownership.")},
            {"item": "C3.i-as-built and comp-similar -- the remaining two of the census's 8.",
             "reason": "Not in this lane's directory and not on this face; other lanes' subjects."},
            {"item": "Any v1 -> v3.1 migrator, including a helper filling only mechanical fields.",
             "reason": ("AC2's STOP clause. A migrator manufactures key_expression, basis and "
                        "provenance values v1 never asked its author for -- a value with no "
                        "measurement behind it carrying the authority of a schema-conformant field.")},
            {"item": "Re-running comp-kuzu to refresh the rails' embedded counts.",
             "reason": ("Out of scope for a carding TO, and re-stamping the rail is the rail "
                        "owner's act. The consequence is carried honestly instead: D1 and D2's "
                        "coverage rows are basis 'held', not 'measured'.")},
            {"item": "The 5 remaining wave-1 rungs' cards.",
             "reason": f"Not this face's scope. Receipt is stated as {RECEIPT}, never as complete."},
        ],
        "surprises": [
            ("OBSERVATION / INERT (3.0.0_SA_CVO~X, cc 2.0.0_SA_COO~X): VERIFIER FINDING CCY-F1, "
             "RAISED AGAINST cfec0a63e3 AND REPAIRED. All three cards self-adjudicated "
             "forward_disposition -- standing 'keep', set_by 0.8.0_AE_CloudComp~Y, the carding lane "
             "deciding what becomes of its own subject. I verified the finding AT SOURCE rather than "
             "on the sender's word (the message carried a sender-unverified flag, which is the "
             "expected condition for a codex seat with no broker row, not a reason to doubt it): the "
             "v3.1 schema's set_by description reads '⛔ MUST NOT be the carding lane for its own "
             "subject -- describing and deciding are different acts and the carding seat has a stake "
             "in the second', and the block description carries Andrew-direct 2026-08-26 putting the "
             "disposition AFTER carding, born UNDECIDED. THE FINDING IS CORRECT. All three blocks "
             "restored to standing 'undecided', set_by null, basis 'absent', evidence naming the "
             "owed second pass; card substance and verdicts (D1/D2 QUALIFIED, D3 INCOMPLETE) "
             "preserved; 3 of 3 still VALID. MY DEFECT, NAMED: I read the schema's SHAPE -- required "
             "fields, enums, types -- and skipped the DESCRIPTIONS, which is where this contract "
             "keeps its law. The prohibition is prose-only and unenforced, so schema-valid did not "
             "make the values lawful, and my own validator could not have caught it."),
            ("OBSERVATION / INERT (3.0.0_SA_CVO~X, cc 2.0.0_SA_COO~X): THE THREE RAILS GAVE THREE "
             "DIFFERENT KINDS OF KEY ANSWER, and D2's is the one worth the issuer's attention: "
             "key_expression is NULL with basis ABSENT because a path is a transitive closure with "
             "no stored identity, and no minting rule is declared anywhere in the rail. Two "
             "consumers cannot agree on which path they are discussing without inventing a handle. "
             "That is a real gap in the rail, surfaced rather than papered over with a plausible "
             "expression -- and it is exactly what a migrator would have manufactured."),
            ("OBSERVATION / INERT (3.0.0_SA_CVO~X, cc 2.0.0_SA_COO~X): D3 IS CARDED INCOMPLETE, NOT "
             "QUALIFIED. Its type space is fully measured (4 of 4 tokens, computable expression) "
             "but its instance population is ZERO and the declared instance home -- ESTATE WS-E1's "
             "registry -- does not exist. A consumer cannot use the rail today except to refuse. "
             "The live consequence: every completeness or freshness question over the estate "
             "resolves against an absent contract right now, and a consumer defaulting "
             "absent-to-satisfied gets universal false compliance. Owner of the remedy is the "
             "ESTATE WS-E1 lane, not this one."),
            ("OBSERVATION / INERT (3.0.0_SA_CVO~X, cc 2.0.0_SA_COO~X): MY OWN FIRST VALIDATION RUN "
             "PRINTED A FALSE SUMMARY. It reported 'all three real cards VALID (positive control)' "
             "as a hardcoded string while the validator had just REFUSED all three, and it then "
             "reported a 5-of-5 mutant battery from that failing base. Caught by reading the rows "
             "above the summary. Recorded because it is the same defect class this project keeps "
             "finding in other carriers -- a summary line that asserts rather than derives -- and a "
             "self-report is the one place it is least likely to be audited."),
        ],
        "session_log": ("org/tier2_senior/0.8.0_AE_CloudComp/logs/2026-08-30/ (written at session "
                        "close, with a mandatory Compiler Tools section)"),
        "compiler_tools": [
            {"tool": "comp-to",
             "invocation": "comp-to NFRA_SUBSTRATECARDING.TO-CARD-R-W1-CCY",
             "result": "PASS -- bound and read back BEFORE the first tool run of this TO."},
            {"tool": "git show (pinned read)",
             "invocation": "git show 9b2c687dc8:<census>; git log/status on the rule bank",
             "result": ("PASS. The census was read through its pin and hashed. The subject was read "
                        "from the worktree WITH both `git log -1` and `git status --porcelain` "
                        "printed beside it, per the vintage lesson banked earlier this session -- "
                        "the file is clean, so the worktree bytes equal the committed bytes.")},
            {"tool": "jsonschema (2020-12)",
             "invocation": "Draft202012Validator over SUBSTRATE_CARD.v3.1 + 7 planted mutants",
             "result": ("CAUGHT TWO REAL DEFECTS IN MY OWN CARDS: descriptive strings where the "
                        "contract requires {id, note} joinable refs, then five ids still carrying "
                        "parentheticals (the schema enforces this with a pattern, not just prose). "
                        "3 of 3 VALID after repair; 7 of 7 mutants refused.")},
            {"tool": "PyYAML",
             "invocation": "yaml.safe_load of NFRA_ONTOLOGY_RULE_BANK.yaml; key enumeration per rail",
             "result": ("PASS. Also the instrument for the D2 absence proof -- flattening "
                        "node_bindings yields 71 node tokens, 0 containing 'PATH', with S3_BUCKET / "
                        "S3Key as the positive control. A FIRST ATTEMPT searched the top level of "
                        "node_bindings, whose keys are ROLES not node types; its positive control "
                        "returned no S3 token either, which is how the wrong-plane search was caught "
                        "before it became evidence.")},
        ],
    }

    OUT.write_text(json.dumps(proof, indent=1) + "\n", encoding="utf-8")
    sd = hashlib.sha256(SCHEMA.read_bytes()).hexdigest()
    print(f"OK: wrote {OUT.relative_to(ROOT)}")
    print(f"OK: {len(acceptance)} criteria, oracles EXTRACTED from the face")
    print(f"OK: contract sha256 {sd}")
    print(f"OK: receipt {RECEIPT}")


if __name__ == "__main__":
    main()
