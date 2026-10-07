# PROPOSAL -- the canon section and one worked case carry the fourth verdict

To: `4.0.0_SA_CRO` (owner of `infra/logic/render_naming_section.py` and `org/missions/D14/LGIC/LGIC_NAMING/deliverables/GRADING_RULE.md`).
From: `0.9.0_WK_LGIC_BLANKFIX~5`, task order `LGIC_BLANKFIX.TO-BF-e-5`. Rows: `LGIC_BLANKFIX-W2-S2`, `W2-S3`.
Nothing outside the project was edited; this is a proposal proved on copies.

## What the patch changes

File: `org/missions/D14/LGIC/LGIC_BLANKFIX/deliverables/0.9.0_WK_LGIC_BLANKFIX~5/canon_fourth_verdict.patch` (2 files, 1 line each).

1. `infra/logic/render_naming_section.py` line 324: `for field in ("ALIAS", "OUT-OF-PATTERN"):` becomes
   `for field in ("NO-SYSTEM-ASKED", "ALIAS", "OUT-OF-PATTERN"):`, so the N5 section prints the schema's `grade.NO-SYSTEM-ASKED`
   sentence beside the other two. The verdicts closed list already follows the schema and already shows four.
2. `GRADING_RULE.md` worked case `pandas-pyarrow-layer|LAMBDA_LAYER`: verdict `OUT-OF-PATTERN` becomes `NO-SYSTEM-ASKED`,
   canonical form `{system}-pandas-pyarrow-layer` becomes `pandas-pyarrow-layer`, and the `why` says no system is asked of a
   library layer. `residue_class` is kept. `grade()` returns exactly this today. The prose of the rule steps (R1.e, V-2) is not touched.

## The check

`python org/missions/D14/LGIC/LGIC_BLANKFIX/deliverables/0.9.0_WK_LGIC_BLANKFIX~5/check_canon_patch.py` last line:

`CANON-PATCH ok=True applies=True rendered_has_verdict=True unpatched_has_verdict=False`

"has verdict" means the section carries the line `- **NO-SYSTEM-ASKED:** <schema sentence>`. The bare token alone is NOT the
discriminator: the unpatched section already prints it in the verdicts closed list.

## What regenerating `02_DOCTRINE.md` will move

Measured on copies with the renderer's own `--write`:

- unpatched renderer vs patched renderer: **1 changed line** (the added `NO-SYSTEM-ASKED` sentence in N5).
- the committed `02_DOCTRINE.md` vs a regeneration by the UNPATCHED renderer: **23 changed lines** already. The committed section is
  behind the schema (stamps at v1.10 against v1.15, see row `W2-S3`), so the first `--write` after any schema change moves those
  23 lines whether or not this patch lands; the patch adds the 1.

Apply with `git apply org/missions/D14/LGIC/LGIC_BLANKFIX/deliverables/0.9.0_WK_LGIC_BLANKFIX~5/canon_fourth_verdict.patch`, then
`python infra/logic/render_naming_section.py --write`. `git apply --check` against HEAD passes.
