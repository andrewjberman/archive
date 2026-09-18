# LGIC_ENFORCE.TO-EN-h-29-r5 -- result

`0.9.0_WK_LGIC_ENFORCE~1`, worktree `.worktrees/wk-lgic-enforce-5-1`, committed `52c65dcaa6` (base `2befae9891`).

One `evidence` string corrected on `infra/logic/registry/resources.json` row `Inflection-HistBackfill-FailureSpike`.
`name`/`type`/`system` untouched (`CW_ALARM`/`advi`). The sound Terraform half of the basis
(`alarms.tf:55-78 @c7fd81bb86`) is unchanged. The project-file half now cites `org/projects/ADVI_JWTRES.json`
(the file measured to carry the quoted phrase, with its real `U+2192` arrow) instead of
`org/projects/ADVI_HISTBF.json` (measured to carry it 0 times since 2026-05-04), and states plainly what that
citation does and does not establish about `ADVI_HISTBF`'s ownership of this alarm.

## Criteria

- `H29R5-AC1` (h29-evidence): **PASS** -- `VERDICT: PASS-H29-WRONG-OBJECT-CITATION-CORRECTED`, both pre-commit and twice post-commit (determinism control).
- `H29R5-AC2` (h29-conclusion): **PASS** -- `VERDICT: PASS-H29-CONCLUSION-AND-TERRAFORM-BASIS-UNDISTURBED`, guard held.
- `H29R5-AC3` (judgment): recorded `UNVERIFIABLE-BY-INSTRUMENT`, status_reason names `3.0.0_SA_CVO` at L9. No verdict given by this worker.

## Surprise filed

`LGIC_ENFORCE-W1-S31` (INVESTIGATION_v1.md, appended to the existing array): `check_en_r5.py`'s `h29-evidence`
arm fails on the bare literal presence of the wrong-file path `org/projects/ADVI_HISTBF.json`, even inside a
correct disclaimer -- no polarity check. Confirmed by a mutant-control test before committing (a
deliberately-correct-but-path-naming draft FAILED identically to the uncorrected row). Worked around by naming
the ruled-out project by short token (`ADVI_HISTBF`) rather than by path in the committed evidence string.

## Proof

`LGIC_ENFORCE.TO-EN-h-29-r5.evidence-correction.proof_of_spec.json`, this directory.
