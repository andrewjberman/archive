# RESULT -- LGIC_ENFORCE.TO-EN-t-1, the Terraform-label census

**Worker:** `0.9.0_WK_LGIC_ENFORCE~3`, branch `wk-lgic-enforce-1-3` off CLOUD @`fd9c9ca174`.
**Proof instance:** `LGIC_ENFORCE.TO-EN-t-1.tf-label-census.proof_of_spec.json`, beside this file.

## What landed

- `org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/TF_LABEL_CENSUS.md`: prose, then one fenced json block.
  Denominator `{"tf_files": 468, "labels": 2035, "name_attributes": 1332}`, with the two lists kept separate.
- `instrument/` in this folder: `tfscan.py` (a stdlib Terraform block scanner), `census.py` (GRADING_RULE.md by its
  written steps, the Terraform-type map and static resolution) and `writer.py` (writes the census). Re-run it from the
  worktree root with `python org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~3/instrument/writer.py`.
- Four rows on the project channel: `LGIC_ENFORCE-W3-S1` to `S4`.

## Which grader was used

`grade()` (EN-b-1, `lib/opal_naming.py`) is absent at the base, so GRADING_RULE.md was applied by its written steps
(G1, G2, G3, then R/S/L/B/K, then G6), hand-coded. The self-test over the rule's own worked cases: **38 of 38 graded
cases agree**. The 5 key cases of the K4a/K5/K6 forms are not coded, and 0 of the 1,332 Terraform names needed them.

## Counts

| list | CONFORMANT | ALIAS | OUT-OF-PATTERN | RAISE | NOT-GRADED | total |
|---|---|---|---|---|---|---|
| labels | 1 | 0 | 659 | 1289 | 86 | 2035 |
| name attributes | 189 | 24 | 670 | 442 | 7 | 1332 |

Name values: 1,208 literal, 100 resolved in their own directory (inferred), 24 not resolvable.

## Criteria (all mechanical)

- `T1-AC1` PASS by output: `LABELS: 2035  NAME ATTRIBUTES: 1332` / `VERDICT: PASS-REPORTED-APART`, rc 0.
- `T1-AC2` PASS by output: `DENOMINATOR: {'tf_files': 468, 'labels': 2035, 'name_attributes': 1332}  tracked .tf files at HEAD: 468` / `VERDICT: PASS-DENOMINATORS`, rc 0.
- `T1-AC3` PASS by output: `ROWS: 3367  WITHOUT A VERDICT: 0` / `VERDICT: PASS-GRADED`, rc 0.

## Controls

- **Mutant:** FIRED 3 of 3. The denominator 2035 -> 2036 gave FAIL-DENOMINATORS, a blanked verdict gave FAIL-UNGRADED, and
  the renamed list key gave FAIL-NOT-APART, each rc 1. After the restore, the sha256 equals run 1 and all three pass.
- **Determinism:** STABLE. Two writer runs give the same sha256, `00a84976a86d2543438cf682aa93001432d030912905df1c3a0e3820eeffe5fd`.
- **Grader spot-check on real output,** before any criterion ran, found two step-order defects in the hand-coding. The B
  steps read the name before G3 normalisation (`opal_data_demo` fell to B4), and G3 was decided before G1 on unresolved
  values (2 Route 53 names came out RAISE instead of NOT-GRADED). Both are fixed and re-verified.

## Rows

- `LGIC_ENFORCE-W3-S1` (OBSERVATION, INERT): no Terraform type is a node type, and the order gives no map; the census used its own.
- `LGIC_ENFORCE-W3-S2` (OBSERVATION, INERT): 124 name values are expressions; 100 were resolved statically and 24 were not.
- `LGIC_ENFORCE-W3-S3` (OBSERVATION, INERT): `role_name` is on no resource block, and names passed to modules are outside the census.
- `LGIC_ENFORCE-W3-S4` (OBSERVATION, INERT): the rule is v1.4-vintage against schema v1.6, which moves 2 G2.3 names; FN1-FN4 are absent from the rule.

## Not claimed

- The Terraform-type map and the static resolution are readings, not rulings.
- Label verdicts are the rule applied outside the schema's domain, because the order says so.
- Nothing live was read and no Terraform ran.
