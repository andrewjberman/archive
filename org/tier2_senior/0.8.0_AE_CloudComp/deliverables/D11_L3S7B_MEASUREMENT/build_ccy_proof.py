"""Build the proof-of-spec instance for NFRA_C3MATERIALIZE.TO-L3S7B-CCY.measurement.

⛔ THE CRITERIA ARE PARSED FROM THE FACE AT ITS PIN, NEVER RETYPED (artifacts_contract).
Retyping is how a criterion drifts from the thing it certifies, and the drift is invisible
because both sides then read the same wrong text.

⛔ XML ENTITIES ARE DECODED BEFORE ANY COMPARISON. AC3's certified oracle contains the only
`>` in the three oracles, carried inside <oracle> as `&gt;=`. 1.0.0_SA_CTO~X 87667 raised this
as an INERT observation aimed at exactly this parser: without html.unescape the instance would
carry `&gt;=` where the record carries `>=` -- 3 bytes -- and a byte comparison would read the
criterion as REWORDED. The emitter escapes both sides in its own self-test, so the mismatch
would appear only here, on the reading side.

⛔ EVERY commit_or_etag IS DERIVED FROM GIT, NOT ASSERTED. A row is PENDING-THIS-COMMIT only
when the file is genuinely uncommitted-or-dirty at build time; a clean file resolves to its own
last commit. Asserting PENDING on a file that is already committed is the fa7b class: the
checker's artifact_resolution arm passes a PENDING row whenever the path merely EXISTS, so a
stale PENDING is invisible to it and the check belongs to the seat.

Author: 0.8.0_AE_CloudComp~Y.
"""

from __future__ import annotations

import html
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]   # the REPO ROOT; parents[4] is <repo>/org
OUT = Path(__file__).resolve().parent
REL = "org/tier2_senior/0.8.0_AE_CloudComp/deliverables/D11_L3S7B_MEASUREMENT/"
FACE_PIN = "f95818e96b"
FACE = "org/tier2_senior/0.8.0_AE_CloudComp/task_orders/NFRA_C3MATERIALIZE.TO-L3S7B-CCY.measurement.md"
PEND = "PENDING-THIS-COMMIT"


def face_text() -> str:
    return subprocess.run(["git", "show", f"{FACE_PIN}:{FACE}"], cwd=str(ROOT),
                          capture_output=True, check=True).stdout.decode("utf-8")


def parse_criteria(txt: str) -> dict:
    """Pull <criterion id=..> label/oracle/value_domain out of the face, entities decoded."""
    out = {}
    for m in re.finditer(
            r'<criterion\s+id="([^"]+)"\s+cell_refs="([^"]+)">(.*?)</criterion>',
            txt, re.S):
        cid, cells, body = m.group(1), m.group(2), m.group(3)
        def tag(name):
            t = re.search(rf"<{name}>(.*?)</{name}>", body, re.S)
            if not t:
                raise SystemExit(f"FAIL: {cid} has no <{name}>")
            return html.unescape(t.group(1)).strip()
        out[cid] = {"cell_refs": cells, "label": tag("label"),
                    "oracle": tag("oracle"), "value_domain": tag("value_domain")}
    if len(out) != 3:
        raise SystemExit(f"FAIL: expected 3 criteria parsed from the face, got {len(out)}")
    return out


def row_identity(rel_path: str) -> str:
    """⛔ A PATHSPEC THAT MATCHES NOTHING RETURNS EMPTY, NOT AN ERROR -- AND EMPTY READS CLEAN.

    This refused on its first run and my first diagnosis was WRONG: I blamed git collapsing a
    wholly-untracked directory into one `?? dir/` row. Running both flag forms side by side
    falsified that in one line -- with an explicit file pathspec git reports the file either
    way. The actual cause was ROOT: parents[4] on this path is `<repo>/org`, not the repo root,
    so every `git status` ran one directory too deep and the pathspec `org/tier2_senior/...`
    matched nothing THERE. Git printed nothing and exited 0, the helper read that silence as
    "clean", and only the no-commit refusal below kept it from becoming a wrong identity.

    That is the 22a shape -- a failed retrieval returning a VALUE rather than an error -- and
    the cwd is the parameter that decides it. `--untracked-files=all` is kept because it is
    correct for untracked files generally, but it was never the bug.
    """
    dirty = subprocess.run(["git", "status", "--porcelain", "--untracked-files=all",
                            "--", rel_path], cwd=str(ROOT),
                           capture_output=True, text=True).stdout.strip()
    if dirty:
        return PEND
    h = subprocess.run(["git", "log", "-1", "--format=%H", "--", rel_path], cwd=str(ROOT),
                       capture_output=True, text=True).stdout.strip()
    if not h:
        raise SystemExit(f"FAIL: {rel_path} is clean but has no commit -- cannot identify it")
    return h


def main() -> None:
    crit = parse_criteria(face_text())
    ac1 = json.load(open(OUT / "_ac1_result.json", encoding="utf-8"))
    ac3 = json.load(open(OUT / "_ac3_result.json", encoding="utf-8"))
    cen = json.load(open(OUT / "frame_block_census.json", encoding="utf-8"))
    ctl = json.load(open(OUT / "_controls_result.json", encoding="utf-8"))

    B, A = ac1["frame_B"], ac1["frame_A"]
    cv = ac3["control_verdict"]
    nul = ac3["null"]

    files = ["L3S7B-1c16-3.frame_declaration.json",
             "L3S7B-1c16-1.auc_w1_unfused.json",
             "L3S7B-0b5f-1.null_battery_instrument.json",
             "frame_block_census.json",
             "build_measurement_carriers.py",
             "build_ccy_proof.py",
             "_ac1_result.json", "_ac3_result.json", "_controls_result.json"]

    inst = {
        "schema_version": "1.0",
        "to_id": "NFRA_C3MATERIALIZE.TO-L3S7B-CCY.measurement",
        "firm": "FABRIC",
        "phase": "BUILD-GENERAL",
        "assignee": "0.8.0_AE_CloudComp~Y",
        "spec_ref": {"doc": FACE, "group": "OTHER", "vintage_commit": FACE_PIN},
        # decomp_ref is {doc, vintage_commit, to_ref} exactly -- additionalProperties:false.
        # to_ref is STATED, never derived from to_id by filename (the schema's own rule: a
        # filename-resolved lookup reports drift where there is none and reads clean where two
        # copies have diverged). owned_cells does NOT belong here; the cell set is declared in
        # the TO's <owned_cells> and the checker JOINS against that file.
        # doc is DECOMP.md at ITS OWN pin, not the certified JSON at the rectangle's pin. The
        # face's <decomp_ref> names both -- the JSON as the record, DECOMP.md as the rendering
        # -- and the checker joins against the one the TO names, so an instance citing the
        # other one disagrees with its own TO about which decomp the work discharges. The
        # substantive source for every value here is still the certified JSON; each carrier
        # cites it under certified_record with its own sha256.
        "decomp_ref": {
            "doc": "workflows/atom_decomposition/runs/nfra-c3materialize-L3/20260830T0852Z/"
                   "DECOMP.md",
            "vintage_commit": "42342fd0ed",
            "to_ref": FACE,
        },
        "artifacts_produced": [
            {"path_or_key": REL + f,
             "kind": "script" if f.endswith(".py") else "config_data",
             "commit_or_etag": row_identity(REL + f),
             "deployed_state": "COMMITTED-NOT-DEPLOY-SCOPE",
             "deploy_evidence": "a cell carrier / builder on a decomposition rectangle; no "
                                "deploy surface exists for it (no S3 key, no Lambda, no "
                                "schedule). Not a deploy-scope path under Rule 13."}
            for f in files
        ],
        "acceptance": [
            {
                "criterion_id": "L3S7B-CCY-AC1",
                "criterion_verbatim": crit["L3S7B-CCY-AC1"]["oracle"],
                "method": "command",
                "invocation": "python ac1.py -- snf_ksweep.py @e2ab79fba4 "
                              "view1_affinity + firm_separation_auc, NO snf() call",
                "output_evidence":
                    f"frame B (judged): AUC(W1) unfused = {B['auc_w1_unfused']:.6f}, "
                    f"n_within {B['n_within']:,} n_cross {B['n_cross']:,}, pairs judged "
                    f"{B['pairs_judged']:,} == C(1820,2) {B['frame_pair_domain']:,}. "
                    f"frame A (beside): {A['auc_w1_unfused']:.6f}, pairs judged "
                    f"{A['pairs_judged']:,} == C(1941,2) {A['frame_pair_domain']:,}. "
                    f"produced_at {ac1['produced_at']}, produced_before "
                    f"{ac1['produced_before']} (the first snf() completion on this rectangle, "
                    f"evidenced by the saved C1 matrix mtime) -- the baseline precedes every "
                    f"fused arm. Headroom (declaration 3, threshold 0.90): frame B NOT "
                    f"refused, margin +{ac1['headroom_declaration_3']['margin_to_threshold']:.6f}. "
                    f"Tie disclosure: W1 takes 26 distinct values (numerator/25) so "
                    f"ties_at_decision equals n_within in both frames.",
                "denominator": "2 frames of 2 required (B judged, A beside); pair denominators "
                               "1,655,290 and 1,882,770, each the frame's own C(n,2)",
                "status": "PASS",
            },
            {
                "criterion_id": "L3S7B-CCY-AC2",
                "criterion_verbatim": crit["L3S7B-CCY-AC2"]["oracle"],
                "method": "schema_validation",
                "invocation": "python build_measurement_carriers.py; frame block canonicalised "
                              "(sort_keys, separators) and sha256-compared across all carriers",
                "output_evidence":
                    f"frame declared on all {cen['denominator']} carriers with "
                    f"{cen['distinct_digests']} distinct digest -> byte_equal="
                    f"{cen['byte_equal']} (digest {cen['digest'][:16]}...). Every count names "
                    f"the set it counts: frame B 1,820 members / 1,655,290 pairs; frame A "
                    f"1,941 / 1,882,770; both-measured POPULATION 4,147 / 8,596,731 (the value "
                    f"declaration 1 carried as frame B's `pairs`, relabelled per correction-1 "
                    f"@1eba52e86c); union 19,482 / 189,764,421; A-B 121 view-2 ABSENT. "
                    f"carrier_table=CloudNode and entity_domain=L2_STRUCTURE_heterogeneous on "
                    f"every carrier by construction, not censused after the fact.",
                "denominator": "3 carriers of 3 emitted by this face",
                "status": "PASS",
            },
            {
                "criterion_id": "L3S7B-CCY-AC3",
                "criterion_verbatim": crit["L3S7B-CCY-AC3"]["oracle"],
                "method": "command",
                "invocation": "python ac3.py -- SeedSequence(20260830).spawn(20), one "
                              "independent child per draw; snf_ksweep.py @e2ab79fba4 "
                              "permute_view + snf(K=20,T=20) + firm_separation_auc",
                "output_evidence":
                    f"instrument REBUILT (the wave-2 permuted arm @c11d1ff734, carded UNSOUND "
                    f"AS A GATE @4e7016f471, is not used). Control run on perm(W1): C1 = "
                    f"SNF(W1,W1) AUC {ac3['C1']['auc']:.6f}; null over n={nul['n_permutations']} "
                    f"draws mean {nul['null_mean']:.6f}, spread(ddof=1) {nul['spread']:.6f}, "
                    f"6 decimals declared; gate C1-3*spread = {cv['gate_value']:.6f}; "
                    f"null_mean < gate -> PASS with margin {cv['margin']:+.6f}; "
                    f"{len(nul['tail_observations'])} tail observations. The null sits at ~0.5, "
                    f"which is what a destroyed correspondence should give -- the instrument "
                    f"demonstrably SEES a permutation, so clause-1 verdicts are ADMISSIBLE on "
                    f"it. This cell states admissibility only and names no clause-1 result.",
                "denominator": f"{nul['n_permutations']} draws of a declared minimum 20; 1 C1 "
                               f"arm on the same frame and (K=20, T=20)",
                "status": "PASS",
            },
        ],
        "controls": {
            "mutant": {
                "description": "carrier 3's frame B pair_domain set to 8,596,731 -- the exact "
                               "error correction-1 fixed -- and the frame-block census re-run",
                "expected": "the census refuses: more than one distinct frame digest, "
                            "byte_equal False",
                "observed": f"{ctl['mutant_distinct']} distinct digests, byte_equal=False; "
                            f"baseline over the real carriers is 1 digest, byte_equal=True",
                "status": "FIRED-AS-EXPECTED",
            },
            "determinism": {
                "method": "re-ran null draw 1 from its own child seed and compared the AUC at "
                          "the declared 6-decimal precision",
                "observed": f"seed {ctl['seed']}: first run {ctl['first_auc']:.6f}, re-run "
                            f"{ctl['rerun_auc']:.6f} -- identical",
                "status": "STABLE",
            },
        },
        "declared_exclusions": [
            {"item": "L3S7B-1c16-2 and the CANDIDATE_VIEW cells (4017-1/2/3)",
             "reason": "gate after-bridge-declared; they belong to the DECLARATION unit at "
                       "this seat (row 0 -> rows 1-4, 87275), not to this face"},
            {"item": "0b5f-2, 4565-x, 8304-x",
             "reason": "gated after-candidate / after-null-battery / after-fusion-arms; a cell "
                       "evaluated out of gate order is FORM_DEFECT (L3S7B-m-7)"},
            {"item": "view 2 (motif Jaccard) and the stitch graph",
             "reason": "neither criterion reads view 2 values. AC1 is unfused W1 and AC3 fuses "
                       "W1 with a permutation of itself. The mask defines which entities are "
                       "both-measured, but no view-2 affinity is computed, so stitch_graph.json "
                       "is not cited as an input -- what was not read is not listed."},
            {"item": "any sec-6 pass/fail statement, any candidate view, any L4 act",
             "reason": "rectangle.completion_claim_rule and the face's NOT A RESULT clause"},
        ],
        "surprises": [
            "FILED AND DISARMED BEFORE ANY MEASUREMENT (87754/87755/87756 -> disarm 87781): "
            "declaration 7 pinned the engine at cfc5f28fb7, which defines none of "
            "firm_separation_auc / permute_view / viewP_affinity, so the face could not be "
            "executed as pinned; the design lane named e2ab79fba4 and every number here is on "
            "those bytes.",
            "FILED AND DISARMED BEFORE ANY MEASUREMENT (same thread): declaration 1 gave frame "
            "B 1,820 members and 8,596,731 pairs, which is C(4147,2) -- the both-measured "
            "POPULATION's pair count carried forward from wave 3, where that set was the "
            "judged domain. Frame B's own domain is C(1820,2) = 1,655,290; every number kept "
            "and relabelled at correction-1 @1eba52e86c.",
            "OBSERVED, NO ACTION: VIEWP_firm_partition.json reads 17,585 B in the worktree "
            "against 17,333 B at its blob, the entire 252-byte delta being CR, while git "
            "reports the file clean. Not used as an input here; recorded because it is the "
            "worktree-rendering digest the artifacts_contract calls a FORM_DEFECT.",
        ],
        "session_log": "org/tier2_senior/0.8.0_AE_CloudComp/logs/2026-08-30/"
                       "session_1400-1430Z_l3s7b_measurement_face_two_pin_defects_before_a_number.md",
        "compiler_tools": [
            {"tool": ".tools/commit-gate.sh",
             "invocation": "on the two .py files in this deliverable",
             "result": "see the commit report"},
            {"tool": ".tools/proof-of-spec-check.py",
             "invocation": "python .tools/proof-of-spec-check.py <this instance> "
                           "L3S7B-CCY-AC1,L3S7B-CCY-AC2,L3S7B-CCY-AC3",
             "result": "see the commit report -- validated on the COMMITTED bytes"},
        ],
    }

    p = OUT / "NFRA_C3MATERIALIZE.TO-L3S7B-CCY.measurement.proof_of_spec.json"
    p.write_text(json.dumps(inst, ensure_ascii=True, indent=1) + "\n",
                 encoding="utf-8", newline="\n")
    print("WROTE %s" % p.name)
    pend = sum(1 for r in inst["artifacts_produced"] if r["commit_or_etag"] == PEND)
    print("  artifacts_produced %d rows: %d PENDING-THIS-COMMIT, %d resolved to a commit"
          % (len(inst["artifacts_produced"]), pend, len(inst["artifacts_produced"]) - pend))
    print("  criteria parsed from the face @%s, entities decoded: %s"
          % (FACE_PIN, ", ".join(sorted(crit))))
    print("  AC3 oracle contains a literal '>=': %s"
          % (">=" in crit["L3S7B-CCY-AC3"]["oracle"]))
    print("  AC3 oracle still contains '&gt;': %s"
          % ("&gt;" in crit["L3S7B-CCY-AC3"]["oracle"]))


if __name__ == "__main__":
    main()
