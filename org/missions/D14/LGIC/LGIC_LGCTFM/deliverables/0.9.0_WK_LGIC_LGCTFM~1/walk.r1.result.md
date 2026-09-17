# LT-e-1 round 1 result -- `0.9.0_WK_LGIC_LGCTFM~1` on `LGIC_LGCTFM.TO-LT-e-1-r1`

**Cell:** `LT-e-1`. **Artifacts:** `lib/opal_lgctfm.py` (new, the `walk` verb),
`infra/logic/10_LEGACY_TRANSFORM.md` (new, the method document) and
`.claude/skills/lgctfm/SKILL.md` (new, the skill), plus the GRADED RUN's own output
`org/missions/D14/LGIC/LGIC_LGCTFM/deliverables/0.9.0_WK_LGIC_LGCTFM~1/walk/{contract.json,PLANT.json}`,
all committed at `d64df250db` on branch `wk-lgic-lgctfm-1-1`.

## What the engine does

`python lib/opal_lgctfm.py walk --subject <key> --seed <bucket> [--seed ...] --out <dir>` follows
DEC-3's order, read-only: reads `infra/logic/06_CONFORMANCE_LEDGER.md` for context (the walk's own
buckets come from `--seed`, never re-derived); walks the AWS live plane with
`.tools/comp-find --corpus aws '\b(?:<seed>|...)\b' --all`; census's BOTH trigger APIs with
`org/modules/graph/comp_trigger.py --list --json` and keeps a trigger if its EventPattern text names a
seed bucket OR its own name carries a firm shortcode (`opal-data-bd` -> `bd`, mechanically stripped,
never read from the round's fixed-input control); reads declaration off a preloaded
`infra/aws/**/*.tf` text corpus; reads `mark` off `infra/logic/registry/scopes.json` (Rule 30's "one
home" for a bucket's alias/routed state), `infra/logic/registry/remediations.json` and
`org/missions/D14/LGIC/LGIC_NAMING/deliverables/LEGACY_SERVED_PATHS.json`. Every `current` field is a
cell `{value, status, evidence: {instrument, blind_spot, ...}}`; `desired` stays `{}` on every row this
round (the worker face's own permission: "`desired` may be absent until LT-e-2"). One resource is
planted outside both instruments' scope and surfaces with every `current` cell `UNMEASURED`.

## The graded run

`--subject 49financial --seed opal-data-bd --seed opal-data-inf --seed opal-data-cot --out
.../deliverables/0.9.0_WK_LGIC_LGCTFM~1/walk` -- never fed `SUBJECT_CONTROL.json`. 276 rows (incl. 1
planted), 1656 current-half cells. The AWS-plane pull found 249 hits across 6 of the 33 node types
(`CLOUDFRONT_DISTRIBUTION` 1, `EVENT_RULE` 11, `IAM_POLICY` 3, `S3Key` 228 -> 205 rows after
name-keyed dedup, `S3_BUCKET` 3, `S3_BUCKET_POLICY` 3) at a MEASURED denominator of 2575 nodes
scanned; the trigger census found 58 relevant `EVENT_RULE` (of 144 events-rules census'd) and 2
relevant `SCHEDULE` (of 23 schedulers census'd), 49 of those 60 not already present from the AWS-plane
pull. The 11 `EVENT_RULE` names the AWS-plane pull found independently and the 11 the trigger-plane
pull found by EventPattern-text match are the SAME 11 names -- two independent instruments
corroborating each other on the control's own sample set.

## Criterion-by-criterion

All eight mechanical criteria run against
`org/missions/D14/LGIC/LGIC_LGCTFM/deliverables/2.0.0_SA_COO~G/fixed_inputs/r1/check_lt_r1.py`
(read-only fixed input, not edited).

- **E1R1-AC1** `e1-control`: all 17 of the control's named members (3 `S3_BUCKET`, 3
  `S3_BUCKET_POLICY`, 11 `EVENT_RULE`) present as rows with the correct `node_type`. PASS.
- **E1R1-AC2** `e1-triggers`: `trigger_denominator.list_rules` (58) and `.list_schedules` (2) both
  MEASURED, both `>= 1`, both via `comp-trigger`. PASS.
- **E1R1-AC3** `e1-cells`: 0 of 1656 current/desired cells across 276 non-FORK rows defective. PASS.
- **E1R1-AC4** `e1-plant`: the planted row (`opal-data-bd-s3-notify-planted-test-queue`) carries an
  `UNMEASURED` current cell (all 6 of them, by construction). PASS.
- **E1R1-AC5** `e1-method`: all 7 required terms (walk order, fork test, twin, tension, plan, mark,
  coverage hole) present in a heading. PASS.
- **E1R1-AC6** `e1-skill`: frontmatter `name: lgctfm` present; body invokes `lib/opal_lgctfm.py`. PASS.
- **E1R1-AC7** `e1-stdlib`: 0 of 8 top-level imports outside stdlib + `lib/`. PASS.
- **E1R1-AC8** `e1-ascii`: 0 of 23788 bytes non-ASCII. PASS.
- **E1R1-AC9**: JUDGMENT, no verdict from this worker; recorded `UNVERIFIABLE-BY-INSTRUMENT`,
  `status_reason` naming `3.0.0_SA_CVO` at L9. `infra/logic/10_LEGACY_TRANSFORM.md`'s "Walk order" and
  "Coverage hole" sections are the record for that adjudication.

## Controls

**Mutant:** the committed `walk/contract.json`'s `cot-bronze-complete` row (one of the control's 17
required members) was deleted and `e1-control` re-run: flipped PASS (17 of 17) to FAIL (16 of 17,
naming the missing member). The file was restored via `git checkout --` and `e1-control` re-run:
returned to PASS at 17 of 17, matching the original. FIRED-AS-EXPECTED.

**Determinism:** `e1-cells` run twice against the committed, unmodified `walk/contract.json`; outputs
byte-identical both times (`diff` empty).

## Coverage holes, named not hidden

`infra/logic/10_LEGACY_TRANSFORM.md`'s own "Coverage hole" section: trigger relevance is a
name/pattern heuristic, not a Lambda-source trace (a schedule whose name carries no firm shortcode and
whose only bucket reference lives in its Lambda's own source is invisible to this walk);
`current.live` is `UNMEASURED`/`NOT_MEASURABLE` for nearly every row (no direct S3 `HeadObject` sweep
was run); `S3Key` rows dedupe by name across buckets (205 of 228 live hits become rows); the portal
submodule is not checked out in this worktree, so `client_facing` for non-bucket rows falls back to
`LEGACY_SERVED_PATHS.json` membership alone; the plant is fictional by construction, not a claim about
real AWS state.

## Commits

- `d64df250db` `build(LGIC_LGCTFM.TO-LT-e-1-r1, 0.9.0_WK_LGIC_LGCTFM~1): the LT-e-1 walk -- lib/opal_lgctfm.py
  walk verb, the method document and the skill` -- `lib/opal_lgctfm.py`,
  `infra/logic/10_LEGACY_TRANSFORM.md`, `.claude/skills/lgctfm/SKILL.md`,
  `org/missions/D14/LGIC/LGIC_LGCTFM/deliverables/0.9.0_WK_LGIC_LGCTFM~1/walk/{contract.json,PLANT.json}`.

No surprise row filed: nothing in this cell diverged from its order, the record, or the fixed-input
checker. The naming-gate WARN on the planted resource's name (out-of-pattern by construction, WARN
window only) is expected -- the plant is deliberately not a real, grammar-conformant resource.
