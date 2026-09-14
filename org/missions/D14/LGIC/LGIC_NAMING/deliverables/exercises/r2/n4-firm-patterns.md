# N4 -- one pattern per firm, with a RAISE disposition (round 2)

**Cell:** LGIC_NAMING `LN-f-1`, round 2 (PRD candidate N4, serves FWD-3), task order `LGIC_NAMING.TO-LN-f-1-r2`, written by
`0.9.0_WK_LGIC_NAMING~4` on branch `wk-lgic-naming-2-4`, cut from CLOUD @`619dec559f`.

**What round 2 changes.** Round 1 (`deliverables/exercises/n4-firm-patterns.md`) met FWD-3 with one qualification: its
output shape had two dispositions, so `wp5-49f-feeder-scheduler-role`, whose grade is a RAISE, was filed under `excluded`
(row `LGIC_NAMING-W1-S5`). This record adds the third disposition, `raise` (the row's option b; round-1 analysis s.1
FWD-3 and s.7 item 6). That role now sits under `raise` with the step that raised it, and `excluded` is empty.

**Inputs, all read at @`619dec559f`:**
- `org/missions/D14/LGIC/LGIC_NAMING/deliverables/GRADING_RULE.md` (LN-g-1, last changed @`51b0952d71`), cited by step id;
- `org/standards/NAMING_SCHEMA.json` **v1.6**, cited as `DATA.<field>`;
- `infra/logic/05_IDENTITY_SPINE.md` v0.1, s.3 FIRMS, cited as SEED;
- `LGIC_NAMING_PRD.md` v1.6, S3-S6 and S10;
- `org/missions/D14/LGIC/LGIC_NAMING/deliverables/2.0.0_SA_COO~G/fixed_inputs/LIVE_NAMES.json`, vintage *"Built from the
  estate as of 2026-09-14 12:13:53 UTC"*, `by_type.IAM_ROLE`;
- round 1's `deliverables/exercises/n4-firm-patterns.md`, the starting point.

---

## 1. The four patterns

| firm key (SEED, `DATA.firm_forms`) | pattern over canonical role names | as an IAM `ArnLike` value |
|---|---|---|
| `49financial` | `*-49f-*-role` | `arn:aws:iam::313476888478:role/*-49f-*-role` |
| `inflection` | `*-inf-*-role` | `arn:aws:iam::313476888478:role/*-inf-*-role` |
| `cottonwood` | `*-cot-*-role` | `arn:aws:iam::313476888478:role/*-cot-*-role` |
| `demo` | `*-demo-*-role` | `arn:aws:iam::313476888478:role/*-demo-*-role` |

**How each is written from S3-S5** (unchanged from round 1; v1.6 moved none of these clauses).
- **S3** gives the shape `{system}-{scope}-{function}[-{qualifier}]-{last}`. For an IAM_ROLE, `{last}` is `role`
  (`DATA.kind.by_type.IAM_ROLE` = `["role"]` at v1.6). `{function}` is not optional, so at least one token sits between
  the scope and `role`.
- **S4** fixes the spelling in the scope slot. It is the SHORT form, IAM principals included: `49f`, `inf`, `cot` or
  `demo`, never `49financial`, `inflection`, `cottonwood` or `bd` (`DATA.resource.scope_form` = `SHORT`).
- **S5** omits the scope of a shared resource, so an unscoped principal matches no firm's pattern. That is what the
  schema intends (S5: "an unscoped principal is legitimate under this schema").

The leading `*` is the system slot. It holds one token (`advi`, `blackdiamond`, `eclipse`, `irpt`, `opal`), or the
placeholder `{system}` where the name does not carry its system. That placeholder is GRADING_RULE R1.d, and at v1.6
it is `DATA.grade.placeholder` (PH1): "a typed gap, never a guess", filled from LGIC_ENFORCE's resource-to-system rows.
The account id is `GRADING_RULE.md` V8.

**Why no pattern catches another firm's form: the grammar does this, not the glob.** `ArnLike` has only `*` and `?`, so
the glob cannot pin the firm token to the second slot. The no-cross property comes from the grammar of a canonical form:
- R4 moves every V4 token into the scope slot. In a canonical form, a firm's short token therefore appears exactly
  once, between two hyphens, right after the system.
- R4 RAISEs a name that carries two different firms, so no canonical form carries two firm tokens.
- R3 turns every `bd` into `blackdiamond` or `49f`, so no `bd` is left.

**The bound.** Each pattern is sound over CANONICAL names only. Applied to the LIVE names of this population as they
stand, the four patterns catch **12 of the 68** attributed roles, each by its own firm's pattern:
`advi-49f-*` (2), `bd-49f-*` (6), `wsb-49f-*`, `wsd-49f-*`, `bd-cot-keepalive-role` and
`opal-assets-mirror-cot-scheduler-role`. Most of the other 56 put the firm token first, so no hyphen comes before it.
`irpt-core-firm-*` and the five `opal-*` guards and parities do not end in `role`. The live name of the one RAISE
(`wp5-49f-feeder-scheduler-role`) also matches `*-49f-*-role`. None of the 171 live roles outside the population
matches any of the four patterns. These counts are context: the order asks for patterns over canonical forms, and no
condition is written or applied here (PRD S13).

## 2. The population, and how it was graded

**Population.** These are the live `IAM_ROLE` names in `LIVE_NAMES.json` that carry a firm alias token (`bd`, `49f`,
`49financial`, `inf`, `inflection`, `cot`, `cottonwood`, `demo`) after splitting on `-` and `_`: **69 of 240** live
roles. Each was graded by GRADING_RULE as an IAM_ROLE in the rule's order: G1 (IAM_ROLE is a RESOURCE-grammar type);
G2.2 (no name begins `AWS` or `Amazon`); G3 (every name is already lowercase kebab); R1-R6 with kind `role`; then G6.

**Result: 68 attributed, 0 excluded, 1 raise** (68 + 0 + 1 = 69).

| firm | attributed | CONFORMANT | ALIAS | OUT-OF-PATTERN | of which carry `{system}` |
|---|---|---|---|---|---|
| `49financial` | 24 | 2 | 6 | 16 | 14 |
| `inflection` | 31 | 0 | 0 | 31 | 27 |
| `cottonwood` | 12 | 0 | 1 | 11 | 6 |
| `demo` | 1 | 0 | 0 | 1 | 1 |
| **total** | 68 | 2 | 7 | 59 | 48 |

**Two methods.** Round 1 graded the 69 by hand and checked them with its own script. This round re-derived every
grade with a new scratch script that encodes R1-R6 and G6, with V1-V4 transcribed from GRADING_RULE.md and the kind
lists read from the v1.6 data file (`.scratch/f1r2_grade.py`, not committed). The new script's output was compared
with round 1's record. They agree on **68 of 68** attributions: same firm, same canonical form, 0 differences. The
script RAISEs the same one name, at R1.f. I traced by hand the cases the prose below names (the `bd` readings,
`inf-api-eclipse-role`, the `irpt-core-firm-*` and `opal-*` forms, and `wp5`), not all 69.

**What decided each attribution** (as in round 1, re-read at v1.6).
- **`bd` next to a firm token is the vendor** (R3). The 6 `bd-49f-*` roles grade ALIAS to `blackdiamond-49f-*`, and
  `bd-cot-keepalive-role` grades ALIAS to `blackdiamond-cot-keepalive-role`. `cot-bd-session-trigger-lambda-role` grades
  OUT-OF-PATTERN to `blackdiamond-cot-session-trigger-lambda-role`: R1.d finds the vendor reading of `bd` as the first
  later V1 token. In each case the firm is the adjacent token.
- **`bd` with no firm token next to it is the firm 49 Financial** (R3; CENSUS s.1 item 4, `bd-allocations`). This covers
  the 12 `bd-*` roles with no adjacent firm. `bd` read as the firm is V3, so R1.d looks for a later V1 token. There is
  none, so each canonical form is `{system}-49f-...-role`. The order's own paraphrase of this step reads differently
  (row `LGIC_NAMING-W4-S1`); this record follows R3's text.
- **A firm in first position is not the system** (R1.d, S6). This covers the 28 `inf-*`, 6 `cot-*` and 1 `demo-*` roles,
  plus `wsb-49f-*` and `wsd-49f-*` (workstream codes, V3). Only `inf-api-eclipse-role` has a later V1 token, so its
  canonical form is `eclipse-inf-api-role`. The rest carry `{system}`.
- **A system first, the firm elsewhere** (R4 moves it; S4 shortens it). `irpt-core-firm-49financial`,
  `irpt-core-firm-inflection` and `irpt-core-firm-cottonwood` become `irpt-{49f|inf|cot}-core-firm-role`, with `role`
  appended by R6. `opal-assets-mirror-cot-scheduler-role` becomes `opal-cot-assets-mirror-scheduler-role`. R2 keeps
  `opal` as the system because `assets` is in neither V1 nor V2. That the role mirrors shared assets data for Cottonwood
  is INFERRED from its name and was not measured.
- **No kind in the last slot** (R6). `opal-{49f,inf,cot}-served-guard` and `opal-{inf,cot}-value-parity` get `role`
  appended. The firm token already sits in the scope slot.

## 3. Raise

One role. `wp5-49f-feeder-scheduler-role` names 49 Financial by its `49f` token, and GRADING_RULE **RAISEs** it at
**R1.f**: its first token `wp5` is in no vocabulary. It is not a V1 system and not a V2 token. V3 lists the workstream
codes `wsb` and `wsd`, not `wp5`. The role is not a LAMBDA_LAYER, so R1.e does not apply. By `DATA.grade.unplaceable`
(v1.6), "a token no registry row resolves" is a defect in the rule, the data file or the registry, never a verdict. A
RAISE carries no canonical form, so there is nothing to test a pattern against. It therefore appears under `raise`
with its step, and not under `attributed` or `excluded`.

Round 1's row names the other remedy, not chosen here: (a) the rule's owner adds `wp5` to V3 as a workstream code (S6:
never a system). The canonical form would then be `{system}-49f-wp5-feeder-scheduler-role`, which `*-49f-*-role`
catches.

**Excluded: none.** None of the 69 roles is shown to be no firm's principal. Every one either carries a firm token
that R4 places in the scope slot, or RAISEs.

## 4. What NAMING_SCHEMA v1.6 moves here, and what it does not

**Measured.** I diffed NAMING_SCHEMA v1.4 (@`e04b802fe9`, the version GRADING_RULE.md cites) against v1.6 at
@`619dec559f`, top-level field by field. The changed fields are `aws_fixed`; `grade.placeholder`;
`iam_policy.purpose_slot`; `key.partition` and `key.scope_rule`; `kind.closed_at_l4`; `resource.function` and
`resource.qualifier`; `secret.purpose`; and `system.vendor_through_tiers`. The version, `ratified_by` and changelog
lines also changed.

**No attribution moves.** The fields that decide a firm are unchanged between v1.4 and v1.6: `firm_forms`,
`refused_tokens`, `resource.scope_form`, `resource.scope_when_shared`, `kind.by_type` and `system.reserved`. So is
GRADING_RULE.md's text. The patterns and all 69 dispositions are therefore unchanged from round 1. The fields that did
change reach this population as follows:
- `grade.placeholder` (PH1) makes the 48 `{system}` forms typed gaps, filled from LGIC_ENFORCE's registry rows. It
  confirms them and changes none.
- `system.vendor_through_tiers` (SY1) decides a system from what a resource builds. A grade of `(name, type)` cannot read
  that, so the slot stays `{system}` under PH1.
- `aws_fixed` (AW1) names no IAM_ROLE, and no name in the population begins `AWS` or `Amazon`.
- `key.*`, `secret.purpose` and `iam_policy.purpose_slot` do not apply to an IAM_ROLE.

**Where v1.6 and the rule's text part.** `resource.function` (FN1) says "an agent noun is always written as its verb"
and "a kind word ... is never written in the function slot". GRADING_RULE R5 reads the function as "free vocabulary",
and R6 keeps another type's kind in the function. By R5/R6, **31 of the 68** canonical forms carry a kind word
(`lambda` 18, `runner` 6, `api` 5, `layer` 4, `task` 1) in the function slot. Many forms also carry agent nouns
(`exporter`, `scheduler`, `processor`, `checker`). Under FN1, `advi-49f-floor-scheduler-role` (CONFORMANT by the rule)
and `bd-49f-runner-role` (ALIAS) would read differently. This record follows GRADING_RULE.md, as the order's J1 names,
and the divergence is row `LGIC_NAMING-W4-S2`. Only the function slot is at stake. The firm, the scope slot and every
pattern's catch are indifferent to it.

## 5. The record

`patterns`, `attributed`, `excluded`, `raise` and `denominator`, in the shape the order names. Within each firm, names
are in the order `LIVE_NAMES.json` lists them.

```json
{
 "patterns": {
  "49financial": "*-49f-*-role",
  "inflection": "*-inf-*-role",
  "cottonwood": "*-cot-*-role",
  "demo": "*-demo-*-role"
 },
 "attributed": {
  "49financial": [
   {
    "name": "advi-49f-floor-scheduler-role",
    "canonical": "advi-49f-floor-scheduler-role"
   },
   {
    "name": "advi-49f-gold-dispatch-role",
    "canonical": "advi-49f-gold-dispatch-role"
   },
   {
    "name": "bd-49f-auto-login-role",
    "canonical": "blackdiamond-49f-auto-login-role"
   },
   {
    "name": "bd-49f-etf-ownership-daily-role",
    "canonical": "blackdiamond-49f-etf-ownership-daily-role"
   },
   {
    "name": "bd-49f-fees-runner-role",
    "canonical": "blackdiamond-49f-fees-runner-role"
   },
   {
    "name": "bd-49f-keepalive-role",
    "canonical": "blackdiamond-49f-keepalive-role"
   },
   {
    "name": "bd-49f-runner-role",
    "canonical": "blackdiamond-49f-runner-role"
   },
   {
    "name": "bd-49f-session-trigger-role",
    "canonical": "blackdiamond-49f-session-trigger-role"
   },
   {
    "name": "bd-allocation-checker-lambda-role",
    "canonical": "{system}-49f-allocation-checker-lambda-role"
   },
   {
    "name": "bd-allocation-processor-role",
    "canonical": "{system}-49f-allocation-processor-role"
   },
   {
    "name": "bd-daily-trigger-lambda-role",
    "canonical": "{system}-49f-daily-trigger-lambda-role"
   },
   {
    "name": "bd-exporter-ec2-role",
    "canonical": "{system}-49f-exporter-ec2-role"
   },
   {
    "name": "bd-gold-detail-generator-role",
    "canonical": "{system}-49f-gold-detail-generator-role"
   },
   {
    "name": "bd-gold-eventbridge-step-functions-role",
    "canonical": "{system}-49f-gold-eventbridge-step-functions-role"
   },
   {
    "name": "bd-gold-layer-lambda-role",
    "canonical": "{system}-49f-gold-layer-lambda-role"
   },
   {
    "name": "bd-gold-step-functions-role",
    "canonical": "{system}-49f-gold-step-functions-role"
   },
   {
    "name": "bd-merge-daily-lambda-role",
    "canonical": "{system}-49f-merge-daily-lambda-role"
   },
   {
    "name": "bd-pipeline-task-role",
    "canonical": "{system}-49f-pipeline-task-role"
   },
   {
    "name": "bd-processor-lambda-role",
    "canonical": "{system}-49f-processor-lambda-role"
   },
   {
    "name": "bd-silver-merge-role",
    "canonical": "{system}-49f-silver-merge-role"
   },
   {
    "name": "irpt-core-firm-49financial",
    "canonical": "irpt-49f-core-firm-role"
   },
   {
    "name": "opal-49f-served-guard",
    "canonical": "opal-49f-served-guard-role"
   },
   {
    "name": "wsb-49f-model-aua-daily-role",
    "canonical": "{system}-49f-wsb-model-aua-daily-role"
   },
   {
    "name": "wsd-49f-partner-held-etf-daily-role",
    "canonical": "{system}-49f-wsd-partner-held-etf-daily-role"
   }
  ],
  "inflection": [
   {
    "name": "inf-accounts-v2-daily-role",
    "canonical": "{system}-inf-accounts-v2-daily-role"
   },
   {
    "name": "inf-api-assets-v2-lambda-role",
    "canonical": "{system}-inf-api-assets-v2-lambda-role"
   },
   {
    "name": "inf-api-eclipse-role",
    "canonical": "eclipse-inf-api-role"
   },
   {
    "name": "inf-api-positions-role",
    "canonical": "{system}-inf-api-positions-role"
   },
   {
    "name": "inf-api-reps-role",
    "canonical": "{system}-inf-api-reps-role"
   },
   {
    "name": "inf-api-txn-role",
    "canonical": "{system}-inf-api-txn-role"
   },
   {
    "name": "inf-assets-trigger-lambda-role",
    "canonical": "{system}-inf-assets-trigger-lambda-role"
   },
   {
    "name": "inf-billing-daily-role",
    "canonical": "{system}-inf-billing-daily-role"
   },
   {
    "name": "inf-bronze-complete-emitter-role",
    "canonical": "{system}-inf-bronze-complete-emitter-role"
   },
   {
    "name": "inf-bronze-runner-ec2-role",
    "canonical": "{system}-inf-bronze-runner-ec2-role"
   },
   {
    "name": "inf-bronze-trigger-lambda-role",
    "canonical": "{system}-inf-bronze-trigger-lambda-role"
   },
   {
    "name": "inf-ec2-launch-monitor-lambda-role",
    "canonical": "{system}-inf-ec2-launch-monitor-lambda-role"
   },
   {
    "name": "inf-ec2-retry-launch-lambda-role",
    "canonical": "{system}-inf-ec2-retry-launch-lambda-role"
   },
   {
    "name": "inf-etf-ownership-daily-role",
    "canonical": "{system}-inf-etf-ownership-daily-role"
   },
   {
    "name": "inf-eventbridge-ssm-role",
    "canonical": "{system}-inf-eventbridge-ssm-role"
   },
   {
    "name": "inf-exporter-ec2-role",
    "canonical": "{system}-inf-exporter-ec2-role"
   },
   {
    "name": "inf-gold-layer-ec2-role",
    "canonical": "{system}-inf-gold-layer-ec2-role"
   },
   {
    "name": "inf-gold-layer-lambda-role",
    "canonical": "{system}-inf-gold-layer-lambda-role"
   },
   {
    "name": "inf-gold-qa-runner-ec2-role",
    "canonical": "{system}-inf-gold-qa-runner-ec2-role"
   },
   {
    "name": "inf-gold-trigger-lambda-role",
    "canonical": "{system}-inf-gold-trigger-lambda-role"
   },
   {
    "name": "inf-jwt-trigger-lambda-role",
    "canonical": "{system}-inf-jwt-trigger-lambda-role"
   },
   {
    "name": "inf-nna-partition-checker-lambda-role",
    "canonical": "{system}-inf-nna-partition-checker-lambda-role"
   },
   {
    "name": "inf-otp-relay-lambda-role",
    "canonical": "{system}-inf-otp-relay-lambda-role"
   },
   {
    "name": "inf-performance-daily-role",
    "canonical": "{system}-inf-performance-daily-role"
   },
   {
    "name": "inf-silver-aggregator-lambda-role",
    "canonical": "{system}-inf-silver-aggregator-lambda-role"
   },
   {
    "name": "inf-silver-chain-lambda-role",
    "canonical": "{system}-inf-silver-chain-lambda-role"
   },
   {
    "name": "inf-tax-daily-role",
    "canonical": "{system}-inf-tax-daily-role"
   },
   {
    "name": "inf-unified-account-dim-daily-role",
    "canonical": "{system}-inf-unified-account-dim-daily-role"
   },
   {
    "name": "irpt-core-firm-inflection",
    "canonical": "irpt-inf-core-firm-role"
   },
   {
    "name": "opal-inf-served-guard",
    "canonical": "opal-inf-served-guard-role"
   },
   {
    "name": "opal-inf-value-parity",
    "canonical": "opal-inf-value-parity-role"
   }
  ],
  "cottonwood": [
   {
    "name": "bd-cot-keepalive-role",
    "canonical": "blackdiamond-cot-keepalive-role"
   },
   {
    "name": "cot-bd-session-trigger-lambda-role",
    "canonical": "blackdiamond-cot-session-trigger-lambda-role"
   },
   {
    "name": "cot-etf-ownership-daily-role",
    "canonical": "{system}-cot-etf-ownership-daily-role"
   },
   {
    "name": "cot-exporter-ec2-role",
    "canonical": "{system}-cot-exporter-ec2-role"
   },
   {
    "name": "cot-gold-layer-ec2-role",
    "canonical": "{system}-cot-gold-layer-ec2-role"
   },
   {
    "name": "cot-rebalancer-runner-role",
    "canonical": "{system}-cot-rebalancer-runner-role"
   },
   {
    "name": "cot-satellites-registry-producer-role",
    "canonical": "{system}-cot-satellites-registry-producer-role"
   },
   {
    "name": "cot-session-scheduler-role",
    "canonical": "{system}-cot-session-scheduler-role"
   },
   {
    "name": "irpt-core-firm-cottonwood",
    "canonical": "irpt-cot-core-firm-role"
   },
   {
    "name": "opal-assets-mirror-cot-scheduler-role",
    "canonical": "opal-cot-assets-mirror-scheduler-role"
   },
   {
    "name": "opal-cot-served-guard",
    "canonical": "opal-cot-served-guard-role"
   },
   {
    "name": "opal-cot-value-parity",
    "canonical": "opal-cot-value-parity-role"
   }
  ],
  "demo": [
   {
    "name": "demo-transform-runner-ec2-role",
    "canonical": "{system}-demo-transform-runner-ec2-role"
   }
  ]
 },
 "excluded": [],
 "raise": [
  {
   "name": "wp5-49f-feeder-scheduler-role",
   "step": "R1.f",
   "why": "t1 wp5 is in no vocabulary of GRADING_RULE.md: not a V1 system, not a V2 token, not V3 (whose workstream codes are wsb and wsd only), and the type is not LAMBDA_LAYER, so R1.e does not apply. The system slot cannot be placed, and a token no registry row resolves is a defect in the rule, the data file or the registry (DATA.grade.unplaceable, v1.6), never a verdict. No canonical form exists for a pattern to be tested on. The firm is legible (49f names 49financial), and the live name matches *-49f-*-role (row LGIC_NAMING-W1-S5, option b)."
  }
 ],
 "denominator": {
  "iam_roles_live": 240,
  "with_a_firm_alias_token": 69,
  "attributed": 68,
  "excluded": 0,
  "raise": 1
 }
}
```
