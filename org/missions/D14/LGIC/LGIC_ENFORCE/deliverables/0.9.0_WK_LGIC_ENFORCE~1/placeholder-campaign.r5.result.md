# LGIC_ENFORCE.TO-EN-c-28-r5 -- result

Commit: `43194e7a28d21c8a09976a5e50f94165e1d64fae` (LOCAL, branch `wk-lgic-enforce-5-4`).

population_at_start (fresh parse of NAMING_CENSUS_REPORT.r4.md): **1411**
population_at_close (fresh parse of NAMING_CENSUS_REPORT.r5.md): **1370**
resolved: **41** census rows across **25** distinct resources (each measured from a declared Terraform
source citing a project already governing an existing sibling `infra/logic/registry/resources.json` row
for the same Terraform root).
carded: **1370**, each with `owner: 2.0.0_SA_COO~G` and one of three reasons -- `TIMEBOXED_R33` (1134),
`NON_SYSTEM_PLACEHOLDER_TOKEN` (235), `TYPE_MISMATCH_NEEDS_CONFIRMATION` (1).

| Criterion | Verdict | Evidence line |
|---|---|---|
| C28R5-AC1 | PASS | `VERDICT: PASS-C28-START-POPULATION-MEASURED` |
| C28R5-AC2 | PASS | `VERDICT: PASS-C28-EVERY-PLACEHOLDER-ROW-RESOLVED-OR-CARDED` |
| C28R5-AC3 | PASS | `VERDICT: PASS-C28-DENOMINATOR-RE-MEASURED-AT-WRITE-TIME` |
| C28R5-AC4 | PASS | `VERDICT: PASS-C28-APPLIED-FENCE-UNCHANGED` (guard, exemptions.json untouched) |
| C28R5-AC5 | PASS | `VERDICT: PASS-C28-R33-TIMEBOX-RESPECTED` (stopped_on_timebox=true, delta filed) |
| C28R5-AC6 | PASS | `VERDICT: PASS-C28-NO-JUDGED-ROW-GRADED-AGAINST-A-TEMPLATE` |
| C28R5-AC7 | UNVERIFIABLE-BY-INSTRUMENT | judgment, oracle 3.0.0_SA_CVO at L9 |

Mutant control (c28-covered, carded[0].owner deleted): FAIL as expected; restored byte-identical; PASS
re-confirmed twice. Determinism: every mechanical arm re-run >=2x post-commit, identical output each time.

Full proof: `LGIC_ENFORCE.TO-EN-c-28-r5.placeholder-campaign.proof_of_spec.json` (this folder).
