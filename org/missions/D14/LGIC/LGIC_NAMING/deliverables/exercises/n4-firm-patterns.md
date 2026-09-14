# N4 -- one pattern per firm

**Cell:** LGIC_NAMING `LN-f-1` (PRD candidate N4, serves FWD-3), task order `LGIC_NAMING.TO-LN-f-1`, written by
`0.9.0_WK_LGIC_NAMING~1` on branch `wk-lgic-naming-1-1` at base `3d671ff59c`.

**Inputs, all read at that base:**
- `org/missions/D14/LGIC/LGIC_NAMING/deliverables/GRADING_RULE.md` (LN-g-1, merged @`ce7349b7cc`), cited by its step ids;
- `org/standards/NAMING_SCHEMA.json` v1.4, cited as `DATA.<field>`;
- `infra/logic/05_IDENTITY_SPINE.md` v0.1, s.3 FIRMS, cited as SEED;
- `LGIC_NAMING_PRD.md` v1.4, S3-S5;
- `org/missions/D14/LGIC/LGIC_NAMING/deliverables/2.0.0_SA_COO~G/fixed_inputs/LIVE_NAMES.json`, vintage *"Built from the
  estate as of 2026-09-14 12:13:53 UTC"*, `by_type.IAM_ROLE`.

---

## 1. The four patterns

| firm key (SEED, `DATA.firm_forms`) | pattern over canonical role names | as an IAM `ArnLike` value |
|---|---|---|
| `49financial` | `*-49f-*-role` | `arn:aws:iam::313476888478:role/*-49f-*-role` |
| `inflection` | `*-inf-*-role` | `arn:aws:iam::313476888478:role/*-inf-*-role` |
| `cottonwood` | `*-cot-*-role` | `arn:aws:iam::313476888478:role/*-cot-*-role` |
| `demo` | `*-demo-*-role` | `arn:aws:iam::313476888478:role/*-demo-*-role` |

**How each is written from S3-S5.**
- **S3** gives the shape: `{system}-{scope}-{function}[-{qualifier}]-{last}`, and `{last}` for an IAM_ROLE is `role`
  (`DATA.kind.by_type.IAM_ROLE`). `{function}` is not optional, so at least one token sits between scope and `role`.
- **S4** fixes the spelling in the scope slot: the SHORT form, IAM principals included. So the scope token is `49f`,
  `inf`, `cot` or `demo`, and never `49financial`, `inflection`, `cottonwood` or `bd`.
- **S5** omits the scope of a shared resource. An unscoped principal therefore matches no firm's pattern, which is what
  the schema intends (S5: "an unscoped principal is legitimate under this schema").

The leading `*` is the system slot: one token (`advi`, `blackdiamond`, `opal`), two tokens for `seeking-alpha`, or the
placeholder `{system}` where the name does not carry its system (GRADING_RULE R1.d, row `LGIC_NAMING-W1-S3`). The
account id is V8 (`GRADING_RULE.md` V8).

**Why no pattern catches another firm's form: the rule does this, not the glob.** `ArnLike` has only `*` and `?`, so
the glob cannot pin the firm token to the second slot. The no-cross property comes from the grammar of a canonical form:
- R4 moves every V4 token into the scope slot, so in a canonical form a firm's short token appears exactly once,
  between two hyphens, right after the system;
- R4 RAISEs a name that carries two different firms, so no canonical form carries two firm tokens;
- R3 turns every `bd` into `blackdiamond` or `49f`, so no `bd` is left.

**The bound.** Each pattern is sound over CANONICAL names only. Over a name that is not canonical, a firm token outside
the scope slot is caught, and a firm token in first position is missed (it has no hyphen before it). Applied to the
LIVE names of this population as they stand today, the four patterns catch 12 of the 68 attributed roles, each by its
own firm's pattern: `advi-49f-*` (2), `bd-49f-*` (6), `bd-cot-keepalive-role`, `wsb-49f-*`, `wsd-49f-*` and
`opal-assets-mirror-cot-scheduler-role`. The other 56 are missed. Most have the firm token first, and
`irpt-core-firm-*` and the five `opal-*` guards and parities do not end in `role`. That count is context: the order
asks for patterns over canonical forms, and an `ArnLike` condition written today with these patterns would reach 12 of
the 68.

## 2. The population, and how it was graded

**Population.** The live `IAM_ROLE` names in `LIVE_NAMES.json` that carry a firm alias token (`bd`, `49f`,
`49financial`, `inf`, `inflection`, `cot`, `cottonwood`, `demo`) after splitting on `-` and `_`:
**69 of 240** live roles. Each one was graded by GRADING_RULE as an IAM_ROLE: G2.2 (no `AWS`/`Amazon` prefix),
G3 (kebab tokens, lowercase), then R1-R6 with kind `role`, then G6.

**Result: 68 attributed, 1 excluded** (68 + 1 = 69).

| firm | attributed | CONFORMANT | ALIAS | OUT-OF-PATTERN | of which carry `{system}` |
|---|---|---|---|---|---|
| `49financial` | 24 | 2 | 6 | 16 | 14 |
| `inflection` | 31 | 0 | 0 | 31 | 27 |
| `cottonwood` | 12 | 0 | 1 | 11 | 6 |
| `demo` | 1 | 0 | 0 | 1 | 1 |
| **total** | 68 | 2 | 7 | 59 | 48 |

**What decided each attribution.**
- **`bd` next to a firm token is the vendor** (R3): `bd-49f-*` (6) grade ALIAS to `blackdiamond-49f-*`,
  `bd-cot-keepalive-role` grades ALIAS to `blackdiamond-cot-keepalive-role`, and `cot-bd-session-trigger-lambda-role`
  grades OUT-OF-PATTERN to `blackdiamond-cot-session-trigger-lambda-role`. The firm is the adjacent token.
- **`bd` with no firm token next to it is the firm 49 Financial** (R3; CENSUS s.1 item 4, `bd-allocations`): the
  12 `bd-*` roles with no adjacent firm. `bd` as the firm is V3, so R1.d looks for a later V1 token. There is none, so
  the canonical form is `{system}-49f-...-role`. **The attribution does not depend on this reading.** If the registry
  later reads these 12 as the vendor, their canonical forms become `blackdiamond-49f-...-role`. Only the system slot
  changes; the firm stays 49financial and `*-49f-*-role` still catches them.
- **A firm in first position is not the system** (R1.d, S6): the 28 `inf-*`, 6 `cot-*`, 1 `demo-*` and 2
  `wsb-49f-*`/`wsd-49f-*` roles. Only `inf-api-eclipse-role` has a later V1 token, so its canonical form is
  `eclipse-inf-api-role`. The rest carry `{system}`.
- **A system first, the firm elsewhere** (R4 moves it; S4 shortens it): `irpt-core-firm-49financial`,
  `irpt-core-firm-inflection` and `irpt-core-firm-cottonwood` become `irpt-{49f|inf|cot}-core-firm-role`, with `role`
  appended by R6. `opal-assets-mirror-cot-scheduler-role` becomes `opal-cot-assets-mirror-scheduler-role`. R2 keeps
  `opal` as the system because `assets` is in neither V1 nor V2. Its name suggests that it mirrors shared assets data
  for Cottonwood; that reading is INFERRED from the name and was not measured. `cot` is the only firm token it
  carries, and R4 makes that token its scope, so it is attributed to cottonwood.
- **No kind in the last slot** (R6): `opal-{49f,inf,cot}-served-guard` and `opal-{inf,cot}-value-parity` get `role`
  appended. The firm token already sits in the scope slot.

## 3. Excluded

One role, and it is excluded for a reason other than the one the order's shape anticipates.
`wp5-49f-feeder-scheduler-role` carries `49f`, so it names 49 Financial. GRADING_RULE **RAISEs** it at R1.f: its first
token `wp5` is in no vocabulary. It is not a V1 system, and V3 lists `wsb` and `wsd` as workstream codes but not
`wp5`. A RAISE carries no canonical form, so no pattern can be tested against it. The order's shape has two
dispositions: attributed, which needs a canonical form, and excluded, whose reason is "no firm's principal". This role
fits neither. It is listed under `excluded` with that stated, and the mismatch is row `LGIC_NAMING-W1-S5`. Its live
name already matches `*-49f-*-role` as written.

## 4. The record

`patterns`, `attributed`, `excluded` and `denominator`, in the shape the order names. Within each firm, names are
in the order `LIVE_NAMES.json` lists them.

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
 "excluded": [
  {
   "name": "wp5-49f-feeder-scheduler-role",
   "reason": "RAISE, not a canonical form: GRADING_RULE.md R1.f -- first token wp5 is in no vocabulary (not a V1 system; V3 names the workstream codes wsb and wsd, not wp5), so the rule places no system slot and gives no canonical form a pattern can be tested on. It is NOT claimed to be no firm's principal: its 49f token names 49 Financial, and its live name already matches *-49f-*-role. The order's shape has no slot for a RAISE (row LGIC_NAMING-W1-S5)."
  }
 ],
 "denominator": {
  "iam_roles_live": 240,
  "with_a_firm_alias_token": 69,
  "attributed": 68,
  "excluded": 1
 }
}
```
