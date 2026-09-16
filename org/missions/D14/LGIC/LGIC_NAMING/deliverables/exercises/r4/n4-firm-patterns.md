# N4 -- one pattern per firm, with a RAISE disposition (round 4)

**Cell:** LGIC_NAMING `LN-f-1`, round 4 (decomposition v6), task order `LGIC_NAMING.TO-LN-f-1-r4`, written by
`0.9.0_WK_LGIC_NAMING~4` on branch `wk-lgic-naming-4-4`, cut from CLOUD @`5e908a4929`.

**What round 4 changes.** Round 3 re-graded round 2's `attributed` forms against R5's one FN1d subtraction and
found no change (GRADING_RULE.md "FORMS CHANGED BY THE v1.7 STEPS: 0 of 68"). This round re-grades the whole
population against GRADING_RULE.md as re-cut to NAMING_SCHEMA v1.9 at this order's base, and adds the
requirement round 2 and round 3 did not carry: **every attributed canonical form that still carries a
placeholder is ALSO listed under `raise`, with the grading step and the registry row that would place it**
(round-3 analysis s.1 FWD-5 and s.3 items 3 and 4; row `LGIC_NAMING-W4-S1`).

**Inputs, all read at this order's base `@5e908a4929`:**
- `org/missions/D14/LGIC/LGIC_NAMING/deliverables/GRADING_RULE.md`, re-cut in round 4 (`LN-g-1`), which grades
  against `org/standards/NAMING_SCHEMA.json` v1.9;
- `lib/opal_naming.py`'s `grade()` (`LN-g-2`), called directly rather than hand-graded, and every attributed
  canonical form below equals its output at this tree (`F1R4-AC2`);
- `infra/logic/registry/systems.json` (V1), `scopes.json` (V4) and `refused_keys`/`unresolved` (V2/V3), as
  `lib/opal_naming.py` loads them at run time -- **this is the registry `LGIC_ENFORCE` `EN-r-2` just landed**
  (commit `72d636db4f`): 7 new system rows (`agentbus`, `cmtque`, `estate`, `firmsep`, `globgrph`, `bloomberg`,
  `msci`) and 93 tokens placed under `refused_keys` (`workstream_code`, `generic_noun`, `purpose_word`),
  including `wp5`, which round 2 could not place;
- `org/missions/D14/LGIC/LGIC_NAMING/deliverables/2.0.0_SA_COO~G/fixed_inputs/LIVE_NAMES.json`, vintage
  "Built from the estate as of 2026-09-14 12:13:53 UTC", `by_type.IAM_ROLE` -- unchanged from round 2;
- round 2's `deliverables/exercises/r2/n4-firm-patterns.md`, the starting point for the four patterns.

---

## 1. The population

**69 of 240** live `IAM_ROLE` names carry a firm alias token (`bd`, `49f`, `49financial`, `inf`, `inflection`,
`cot`, `cottonwood`, `demo`) after splitting on `-` and `_` -- unchanged from round 2 and round 3 (`LIVE_NAMES.json`
has not moved). Every one is graded here with `lib/opal_naming.py`'s `grade(name, "IAM_ROLE")` directly, not by
hand, and `F1R4-AC2` checks the two agree.

**Result: 69 attributed, 0 excluded, 0 names where `grade()` itself RAISEs.** That last number is new: round 2's
one `grade()`-RAISE, `wp5-49f-feeder-scheduler-role` (unplaceable at R1.f, no vocabulary held `wp5`), now
resolves, because `EN-r-2` placed `wp5` under `refused_keys.workstream_code` beside `wsb` and `wsd`. R1.d then
reads it exactly as it already read `wsb-49f-*` and `wsd-49f-*`: a workstream code is not the system (V3), the
scope is `49f`, and no later token is a V1 system, so the canonical form carries `{system}` and the role is
attributed, not raised by `grade()`.

| firm | attributed | CONFORMANT | ALIAS | OUT-OF-PATTERN, no `{system}` | of which carry `{system}` |
|---|---|---|---|---|---|
| `49financial` | 25 | 2 | 8 | 0 | 15 |
| `inflection` | 31 | 0 | 4 | 0 | 27 |
| `cottonwood` | 12 | 0 | 6 | 0 | 6 |
| `demo` | 1 | 0 | 0 | 0 | 1 |
| **total** | 69 | 2 | 18 | 0 | 49 |

**No exclusions.** As in round 2: every one of the 69 carries a firm token R4 places in the scope slot (`bd`
read by R3's adjacency test, never a second firm), so none is "no firm's principal."

## 2. What decided each attribution (re-read at v1.9, registry at `72d636db4f`)

Unchanged in substance from round 2 (GRADING_RULE.md's R1--R4 did not move on these clauses between v1.6 and
v1.9; only R5's one FN1d subtraction and G2's `aws_fixed` exclusion moved, and round 3 measured FN1d changes
nothing here):
- **`bd` next to a firm token is the VENDOR `blackdiamond`** (R3, quoted in this order's WORKER FACE, row
  `LGIC_NAMING-W4-S1`): the 6 `bd-49f-*` roles and `bd-cot-keepalive-role` ALIAS to `blackdiamond-{49f|cot}-...`;
  `cot-bd-session-trigger-lambda-role` (the vendor reads either side of the scope) grades OUT-OF-PATTERN to
  `blackdiamond-cot-session-trigger-lambda-role`.
- **`bd` with no adjacent firm token is the FIRM 49 Financial** (R3): the 12 remaining `bd-*` roles grade
  `{system}-49f-...-role` -- R1.d finds no later V1 token, so the system slot is the placeholder.
- **A firm in first position is not the system** (R1.d, S6): the 27 remaining `inf-*` roles, the 6 remaining
  `cot-*` roles, `demo-transform-runner-ec2-role`, `wp5-49f-feeder-scheduler-role`, `wsb-49f-model-aua-daily-role`
  and `wsd-49f-partner-held-etf-daily-role` all carry `{system}`. `inf-api-eclipse-role` is the one exception:
  its later token `eclipse` is a V1 vendor row, so it grades `eclipse-inf-api-role` with no placeholder.
- **A system first, the firm elsewhere** (R4 moves it; S4 shortens it): `irpt-core-firm-{49financial|cottonwood|
  inflection}` become `irpt-{49f|cot|inf}-core-firm-role`; `opal-assets-mirror-cot-scheduler-role` becomes
  `opal-cot-assets-mirror-scheduler-role`. `irpt` and `opal` (R2, reserved) are both already systems, so none of
  these six carry a placeholder.
- **No kind in the last slot** (R6): `opal-{49f,inf,cot}-served-guard` and `opal-{inf,cot}-value-parity` get
  `role` appended; `opal` is the system already, so no placeholder.

## 3. Raise: every placeholder, none filled

**49 of the 69 attributed canonical forms carry `{system}`** (round 2: 48 of 68 -- the one addition is
`wp5-49f-feeder-scheduler-role`, moved from `grade()`-RAISE to attributed-with-placeholder by `EN-r-2`'s
classification, never by a system-token match). **Every one of the 49 is listed below, and none is filled**,
because `infra/logic/registry/` carries no resource-to-system rows to fill from.

**Measured, not assumed.** `infra/logic/registry/` holds exactly five files at this tree --
`exemptions.json`, `remediations.json`, `scopes.json`, `systems.json`, `tiers.json` -- and `git ls-tree -r HEAD`
finds no `resources.json`. `NAMING_SCHEMA.json`'s own `grade.placeholder` text names the one mechanism that
fills `{system}`: "{system} from the identity registry's resource-to-system rows (LGIC_ENFORCE)". That file
is `LGIC_ENFORCE` cell `EN-r-4`'s own deliverable (task order `LGIC_ENFORCE.TO-EN-r-4-r2`, `<status>pending</status>`
at this tree) -- it is not among this order's two landed dependencies (`EN-r-2` and the G-V19 group), and it has
not run. So the 49 gaps cannot be filled here, and per `CLAUDE.md` Rule 30 ("a missing registry row is a row to
add, never a guess") and this order's own instruction, each is RAISED rather than guessed. Row `LGIC_NAMING-W4-S3`
records that this is MORE raises than round 2 carried (round 2's file raised only `wp5`, 1 of 69; this round's
`f1-gaps` criterion requires all 49), the opposite of the order's own hint -- the order itself says not to carry
round 2's numbers forward, and this is why.

Each raise entry below names the grading step (`R1.d` in every case, via `R3`'s `bd`-as-firm reading for the 12
`bd-*` names and via `refused_keys.workstream_code` for `wp5`/`wsb`/`wsd`), why the system cannot be read from the
name's own tokens, and the `resources.json` row that is owed and does not exist. No system is guessed for any
of the 49.

## 4. The four patterns, unchanged from round 2

`ArnLike`-shaped globs over CANONICAL role names, one per firm:

| firm key | pattern | as an IAM `ArnLike` value |
|---|---|---|
| `49financial` | `*-49f-*-role` | `arn:aws:iam::313476888478:role/*-49f-*-role` |
| `inflection` | `*-inf-*-role` | `arn:aws:iam::313476888478:role/*-inf-*-role` |
| `cottonwood` | `*-cot-*-role` | `arn:aws:iam::313476888478:role/*-cot-*-role` |
| `demo` | `*-demo-*-role` | `arn:aws:iam::313476888478:role/*-demo-*-role` |

**Why unchanged.** S3 (shape), S4 (SHORT scope spelling) and S5 (an unscoped principal matches no firm's
pattern) did not move between v1.6 and v1.9, and R4 still puts exactly one firm's SHORT token immediately after
the system, whether that system is a real token or the placeholder `{system}` (a placeholder writes no token and
removes nothing, R5). So every one of the 69 canonical forms -- placeholder or not -- still carries its firm's
short token in the same position, and the glob still catches it. **Measured over this round's 69 canonical
forms:** each firm's pattern catches every one of that firm's attributed forms (`F1R4-AC4`), and no pattern
catches another firm's form (`F1R4-AC5`) -- verified directly with `fnmatch.fnmatchcase`, the module the order's
checker uses, zero misses and zero cross-catches.

## 5. The record

`patterns`, `attributed`, `excluded`, `raise` and `denominator`, in the shape the order names. Within each
firm, names are in the order `LIVE_NAMES.json` lists them (unchanged from round 2).

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
    "name": "wp5-49f-feeder-scheduler-role",
    "canonical": "{system}-49f-wp5-feeder-scheduler-role"
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
   "name": "bd-allocation-checker-lambda-role",
   "step": "R1.d",
   "why": "R1.d: the name's first token resolves to the firm scope (directly, or via R3's bd-as-firm reading when bd carries no adjacent firm token; or via V3's workstream-code reading for wp5/wsb/wsd, refused_keys.workstream_code, infra/logic/registry/systems.json). No later token in the name is a REGISTRY systems.json V1 key, so the system slot cannot be read from the name's own tokens. DATA.grade.placeholder names the registry's resource-to-system rows as the only fill (NAMING_SCHEMA.json v1.9 grade.placeholder; GRADING_RULE.md R1.d, row LGIC_NAMING-W1-S3): which system this specific role's resource BUILDS (SY1, system.vendor_through_tiers) is not something grade(name, type) can read.",
   "missing_row": "infra/logic/registry/resources.json has no row for {\"name\": \"bd-allocation-checker-lambda-role\", \"type\": \"IAM_ROLE\"} -- the file itself does not exist in this tree. LGIC_ENFORCE cell EN-r-4 (task order LGIC_ENFORCE.TO-EN-r-4-r2) is the cell that mints it; its <status> is pending and it is not among this order's landed dependencies (EN-r-2 and the G-V19 group). No system is guessed here."
  },
  {
   "name": "bd-allocation-processor-role",
   "step": "R1.d",
   "why": "R1.d: the name's first token resolves to the firm scope (directly, or via R3's bd-as-firm reading when bd carries no adjacent firm token; or via V3's workstream-code reading for wp5/wsb/wsd, refused_keys.workstream_code, infra/logic/registry/systems.json). No later token in the name is a REGISTRY systems.json V1 key, so the system slot cannot be read from the name's own tokens. DATA.grade.placeholder names the registry's resource-to-system rows as the only fill (NAMING_SCHEMA.json v1.9 grade.placeholder; GRADING_RULE.md R1.d, row LGIC_NAMING-W1-S3): which system this specific role's resource BUILDS (SY1, system.vendor_through_tiers) is not something grade(name, type) can read.",
   "missing_row": "infra/logic/registry/resources.json has no row for {\"name\": \"bd-allocation-processor-role\", \"type\": \"IAM_ROLE\"} -- the file itself does not exist in this tree. LGIC_ENFORCE cell EN-r-4 (task order LGIC_ENFORCE.TO-EN-r-4-r2) is the cell that mints it; its <status> is pending and it is not among this order's landed dependencies (EN-r-2 and the G-V19 group). No system is guessed here."
  },
  {
   "name": "bd-daily-trigger-lambda-role",
   "step": "R1.d",
   "why": "R1.d: the name's first token resolves to the firm scope (directly, or via R3's bd-as-firm reading when bd carries no adjacent firm token; or via V3's workstream-code reading for wp5/wsb/wsd, refused_keys.workstream_code, infra/logic/registry/systems.json). No later token in the name is a REGISTRY systems.json V1 key, so the system slot cannot be read from the name's own tokens. DATA.grade.placeholder names the registry's resource-to-system rows as the only fill (NAMING_SCHEMA.json v1.9 grade.placeholder; GRADING_RULE.md R1.d, row LGIC_NAMING-W1-S3): which system this specific role's resource BUILDS (SY1, system.vendor_through_tiers) is not something grade(name, type) can read.",
   "missing_row": "infra/logic/registry/resources.json has no row for {\"name\": \"bd-daily-trigger-lambda-role\", \"type\": \"IAM_ROLE\"} -- the file itself does not exist in this tree. LGIC_ENFORCE cell EN-r-4 (task order LGIC_ENFORCE.TO-EN-r-4-r2) is the cell that mints it; its <status> is pending and it is not among this order's landed dependencies (EN-r-2 and the G-V19 group). No system is guessed here."
  },
  {
   "name": "bd-exporter-ec2-role",
   "step": "R1.d",
   "why": "R1.d: the name's first token resolves to the firm scope (directly, or via R3's bd-as-firm reading when bd carries no adjacent firm token; or via V3's workstream-code reading for wp5/wsb/wsd, refused_keys.workstream_code, infra/logic/registry/systems.json). No later token in the name is a REGISTRY systems.json V1 key, so the system slot cannot be read from the name's own tokens. DATA.grade.placeholder names the registry's resource-to-system rows as the only fill (NAMING_SCHEMA.json v1.9 grade.placeholder; GRADING_RULE.md R1.d, row LGIC_NAMING-W1-S3): which system this specific role's resource BUILDS (SY1, system.vendor_through_tiers) is not something grade(name, type) can read.",
   "missing_row": "infra/logic/registry/resources.json has no row for {\"name\": \"bd-exporter-ec2-role\", \"type\": \"IAM_ROLE\"} -- the file itself does not exist in this tree. LGIC_ENFORCE cell EN-r-4 (task order LGIC_ENFORCE.TO-EN-r-4-r2) is the cell that mints it; its <status> is pending and it is not among this order's landed dependencies (EN-r-2 and the G-V19 group). No system is guessed here."
  },
  {
   "name": "bd-gold-detail-generator-role",
   "step": "R1.d",
   "why": "R1.d: the name's first token resolves to the firm scope (directly, or via R3's bd-as-firm reading when bd carries no adjacent firm token; or via V3's workstream-code reading for wp5/wsb/wsd, refused_keys.workstream_code, infra/logic/registry/systems.json). No later token in the name is a REGISTRY systems.json V1 key, so the system slot cannot be read from the name's own tokens. DATA.grade.placeholder names the registry's resource-to-system rows as the only fill (NAMING_SCHEMA.json v1.9 grade.placeholder; GRADING_RULE.md R1.d, row LGIC_NAMING-W1-S3): which system this specific role's resource BUILDS (SY1, system.vendor_through_tiers) is not something grade(name, type) can read.",
   "missing_row": "infra/logic/registry/resources.json has no row for {\"name\": \"bd-gold-detail-generator-role\", \"type\": \"IAM_ROLE\"} -- the file itself does not exist in this tree. LGIC_ENFORCE cell EN-r-4 (task order LGIC_ENFORCE.TO-EN-r-4-r2) is the cell that mints it; its <status> is pending and it is not among this order's landed dependencies (EN-r-2 and the G-V19 group). No system is guessed here."
  },
  {
   "name": "bd-gold-eventbridge-step-functions-role",
   "step": "R1.d",
   "why": "R1.d: the name's first token resolves to the firm scope (directly, or via R3's bd-as-firm reading when bd carries no adjacent firm token; or via V3's workstream-code reading for wp5/wsb/wsd, refused_keys.workstream_code, infra/logic/registry/systems.json). No later token in the name is a REGISTRY systems.json V1 key, so the system slot cannot be read from the name's own tokens. DATA.grade.placeholder names the registry's resource-to-system rows as the only fill (NAMING_SCHEMA.json v1.9 grade.placeholder; GRADING_RULE.md R1.d, row LGIC_NAMING-W1-S3): which system this specific role's resource BUILDS (SY1, system.vendor_through_tiers) is not something grade(name, type) can read.",
   "missing_row": "infra/logic/registry/resources.json has no row for {\"name\": \"bd-gold-eventbridge-step-functions-role\", \"type\": \"IAM_ROLE\"} -- the file itself does not exist in this tree. LGIC_ENFORCE cell EN-r-4 (task order LGIC_ENFORCE.TO-EN-r-4-r2) is the cell that mints it; its <status> is pending and it is not among this order's landed dependencies (EN-r-2 and the G-V19 group). No system is guessed here."
  },
  {
   "name": "bd-gold-layer-lambda-role",
   "step": "R1.d",
   "why": "R1.d: the name's first token resolves to the firm scope (directly, or via R3's bd-as-firm reading when bd carries no adjacent firm token; or via V3's workstream-code reading for wp5/wsb/wsd, refused_keys.workstream_code, infra/logic/registry/systems.json). No later token in the name is a REGISTRY systems.json V1 key, so the system slot cannot be read from the name's own tokens. DATA.grade.placeholder names the registry's resource-to-system rows as the only fill (NAMING_SCHEMA.json v1.9 grade.placeholder; GRADING_RULE.md R1.d, row LGIC_NAMING-W1-S3): which system this specific role's resource BUILDS (SY1, system.vendor_through_tiers) is not something grade(name, type) can read.",
   "missing_row": "infra/logic/registry/resources.json has no row for {\"name\": \"bd-gold-layer-lambda-role\", \"type\": \"IAM_ROLE\"} -- the file itself does not exist in this tree. LGIC_ENFORCE cell EN-r-4 (task order LGIC_ENFORCE.TO-EN-r-4-r2) is the cell that mints it; its <status> is pending and it is not among this order's landed dependencies (EN-r-2 and the G-V19 group). No system is guessed here."
  },
  {
   "name": "bd-gold-step-functions-role",
   "step": "R1.d",
   "why": "R1.d: the name's first token resolves to the firm scope (directly, or via R3's bd-as-firm reading when bd carries no adjacent firm token; or via V3's workstream-code reading for wp5/wsb/wsd, refused_keys.workstream_code, infra/logic/registry/systems.json). No later token in the name is a REGISTRY systems.json V1 key, so the system slot cannot be read from the name's own tokens. DATA.grade.placeholder names the registry's resource-to-system rows as the only fill (NAMING_SCHEMA.json v1.9 grade.placeholder; GRADING_RULE.md R1.d, row LGIC_NAMING-W1-S3): which system this specific role's resource BUILDS (SY1, system.vendor_through_tiers) is not something grade(name, type) can read.",
   "missing_row": "infra/logic/registry/resources.json has no row for {\"name\": \"bd-gold-step-functions-role\", \"type\": \"IAM_ROLE\"} -- the file itself does not exist in this tree. LGIC_ENFORCE cell EN-r-4 (task order LGIC_ENFORCE.TO-EN-r-4-r2) is the cell that mints it; its <status> is pending and it is not among this order's landed dependencies (EN-r-2 and the G-V19 group). No system is guessed here."
  },
  {
   "name": "bd-merge-daily-lambda-role",
   "step": "R1.d",
   "why": "R1.d: the name's first token resolves to the firm scope (directly, or via R3's bd-as-firm reading when bd carries no adjacent firm token; or via V3's workstream-code reading for wp5/wsb/wsd, refused_keys.workstream_code, infra/logic/registry/systems.json). No later token in the name is a REGISTRY systems.json V1 key, so the system slot cannot be read from the name's own tokens. DATA.grade.placeholder names the registry's resource-to-system rows as the only fill (NAMING_SCHEMA.json v1.9 grade.placeholder; GRADING_RULE.md R1.d, row LGIC_NAMING-W1-S3): which system this specific role's resource BUILDS (SY1, system.vendor_through_tiers) is not something grade(name, type) can read.",
   "missing_row": "infra/logic/registry/resources.json has no row for {\"name\": \"bd-merge-daily-lambda-role\", \"type\": \"IAM_ROLE\"} -- the file itself does not exist in this tree. LGIC_ENFORCE cell EN-r-4 (task order LGIC_ENFORCE.TO-EN-r-4-r2) is the cell that mints it; its <status> is pending and it is not among this order's landed dependencies (EN-r-2 and the G-V19 group). No system is guessed here."
  },
  {
   "name": "bd-pipeline-task-role",
   "step": "R1.d",
   "why": "R1.d: the name's first token resolves to the firm scope (directly, or via R3's bd-as-firm reading when bd carries no adjacent firm token; or via V3's workstream-code reading for wp5/wsb/wsd, refused_keys.workstream_code, infra/logic/registry/systems.json). No later token in the name is a REGISTRY systems.json V1 key, so the system slot cannot be read from the name's own tokens. DATA.grade.placeholder names the registry's resource-to-system rows as the only fill (NAMING_SCHEMA.json v1.9 grade.placeholder; GRADING_RULE.md R1.d, row LGIC_NAMING-W1-S3): which system this specific role's resource BUILDS (SY1, system.vendor_through_tiers) is not something grade(name, type) can read.",
   "missing_row": "infra/logic/registry/resources.json has no row for {\"name\": \"bd-pipeline-task-role\", \"type\": \"IAM_ROLE\"} -- the file itself does not exist in this tree. LGIC_ENFORCE cell EN-r-4 (task order LGIC_ENFORCE.TO-EN-r-4-r2) is the cell that mints it; its <status> is pending and it is not among this order's landed dependencies (EN-r-2 and the G-V19 group). No system is guessed here."
  },
  {
   "name": "bd-processor-lambda-role",
   "step": "R1.d",
   "why": "R1.d: the name's first token resolves to the firm scope (directly, or via R3's bd-as-firm reading when bd carries no adjacent firm token; or via V3's workstream-code reading for wp5/wsb/wsd, refused_keys.workstream_code, infra/logic/registry/systems.json). No later token in the name is a REGISTRY systems.json V1 key, so the system slot cannot be read from the name's own tokens. DATA.grade.placeholder names the registry's resource-to-system rows as the only fill (NAMING_SCHEMA.json v1.9 grade.placeholder; GRADING_RULE.md R1.d, row LGIC_NAMING-W1-S3): which system this specific role's resource BUILDS (SY1, system.vendor_through_tiers) is not something grade(name, type) can read.",
   "missing_row": "infra/logic/registry/resources.json has no row for {\"name\": \"bd-processor-lambda-role\", \"type\": \"IAM_ROLE\"} -- the file itself does not exist in this tree. LGIC_ENFORCE cell EN-r-4 (task order LGIC_ENFORCE.TO-EN-r-4-r2) is the cell that mints it; its <status> is pending and it is not among this order's landed dependencies (EN-r-2 and the G-V19 group). No system is guessed here."
  },
  {
   "name": "bd-silver-merge-role",
   "step": "R1.d",
   "why": "R1.d: the name's first token resolves to the firm scope (directly, or via R3's bd-as-firm reading when bd carries no adjacent firm token; or via V3's workstream-code reading for wp5/wsb/wsd, refused_keys.workstream_code, infra/logic/registry/systems.json). No later token in the name is a REGISTRY systems.json V1 key, so the system slot cannot be read from the name's own tokens. DATA.grade.placeholder names the registry's resource-to-system rows as the only fill (NAMING_SCHEMA.json v1.9 grade.placeholder; GRADING_RULE.md R1.d, row LGIC_NAMING-W1-S3): which system this specific role's resource BUILDS (SY1, system.vendor_through_tiers) is not something grade(name, type) can read.",
   "missing_row": "infra/logic/registry/resources.json has no row for {\"name\": \"bd-silver-merge-role\", \"type\": \"IAM_ROLE\"} -- the file itself does not exist in this tree. LGIC_ENFORCE cell EN-r-4 (task order LGIC_ENFORCE.TO-EN-r-4-r2) is the cell that mints it; its <status> is pending and it is not among this order's landed dependencies (EN-r-2 and the G-V19 group). No system is guessed here."
  },
  {
   "name": "wp5-49f-feeder-scheduler-role",
   "step": "R1.d",
   "why": "R1.d: the name's first token resolves to the firm scope (directly, or via R3's bd-as-firm reading when bd carries no adjacent firm token; or via V3's workstream-code reading for wp5/wsb/wsd, refused_keys.workstream_code, infra/logic/registry/systems.json). No later token in the name is a REGISTRY systems.json V1 key, so the system slot cannot be read from the name's own tokens. DATA.grade.placeholder names the registry's resource-to-system rows as the only fill (NAMING_SCHEMA.json v1.9 grade.placeholder; GRADING_RULE.md R1.d, row LGIC_NAMING-W1-S3): which system this specific role's resource BUILDS (SY1, system.vendor_through_tiers) is not something grade(name, type) can read.",
   "missing_row": "infra/logic/registry/resources.json has no row for {\"name\": \"wp5-49f-feeder-scheduler-role\", \"type\": \"IAM_ROLE\"} -- the file itself does not exist in this tree. LGIC_ENFORCE cell EN-r-4 (task order LGIC_ENFORCE.TO-EN-r-4-r2) is the cell that mints it; its <status> is pending and it is not among this order's landed dependencies (EN-r-2 and the G-V19 group). No system is guessed here."
  },
  {
   "name": "wsb-49f-model-aua-daily-role",
   "step": "R1.d",
   "why": "R1.d: the name's first token resolves to the firm scope (directly, or via R3's bd-as-firm reading when bd carries no adjacent firm token; or via V3's workstream-code reading for wp5/wsb/wsd, refused_keys.workstream_code, infra/logic/registry/systems.json). No later token in the name is a REGISTRY systems.json V1 key, so the system slot cannot be read from the name's own tokens. DATA.grade.placeholder names the registry's resource-to-system rows as the only fill (NAMING_SCHEMA.json v1.9 grade.placeholder; GRADING_RULE.md R1.d, row LGIC_NAMING-W1-S3): which system this specific role's resource BUILDS (SY1, system.vendor_through_tiers) is not something grade(name, type) can read.",
   "missing_row": "infra/logic/registry/resources.json has no row for {\"name\": \"wsb-49f-model-aua-daily-role\", \"type\": \"IAM_ROLE\"} -- the file itself does not exist in this tree. LGIC_ENFORCE cell EN-r-4 (task order LGIC_ENFORCE.TO-EN-r-4-r2) is the cell that mints it; its <status> is pending and it is not among this order's landed dependencies (EN-r-2 and the G-V19 group). No system is guessed here."
  },
  {
   "name": "wsd-49f-partner-held-etf-daily-role",
   "step": "R1.d",
   "why": "R1.d: the name's first token resolves to the firm scope (directly, or via R3's bd-as-firm reading when bd carries no adjacent firm token; or via V3's workstream-code reading for wp5/wsb/wsd, refused_keys.workstream_code, infra/logic/registry/systems.json). No later token in the name is a REGISTRY systems.json V1 key, so the system slot cannot be read from the name's own tokens. DATA.grade.placeholder names the registry's resource-to-system rows as the only fill (NAMING_SCHEMA.json v1.9 grade.placeholder; GRADING_RULE.md R1.d, row LGIC_NAMING-W1-S3): which system this specific role's resource BUILDS (SY1, system.vendor_through_tiers) is not something grade(name, type) can read.",
   "missing_row": "infra/logic/registry/resources.json has no row for {\"name\": \"wsd-49f-partner-held-etf-daily-role\", \"type\": \"IAM_ROLE\"} -- the file itself does not exist in this tree. LGIC_ENFORCE cell EN-r-4 (task order LGIC_ENFORCE.TO-EN-r-4-r2) is the cell that mints it; its <status> is pending and it is not among this order's landed dependencies (EN-r-2 and the G-V19 group). No system is guessed here."
  },
  {
   "name": "inf-accounts-v2-daily-role",
   "step": "R1.d",
   "why": "R1.d: the name's first token resolves to the firm scope (directly, or via R3's bd-as-firm reading when bd carries no adjacent firm token; or via V3's workstream-code reading for wp5/wsb/wsd, refused_keys.workstream_code, infra/logic/registry/systems.json). No later token in the name is a REGISTRY systems.json V1 key, so the system slot cannot be read from the name's own tokens. DATA.grade.placeholder names the registry's resource-to-system rows as the only fill (NAMING_SCHEMA.json v1.9 grade.placeholder; GRADING_RULE.md R1.d, row LGIC_NAMING-W1-S3): which system this specific role's resource BUILDS (SY1, system.vendor_through_tiers) is not something grade(name, type) can read.",
   "missing_row": "infra/logic/registry/resources.json has no row for {\"name\": \"inf-accounts-v2-daily-role\", \"type\": \"IAM_ROLE\"} -- the file itself does not exist in this tree. LGIC_ENFORCE cell EN-r-4 (task order LGIC_ENFORCE.TO-EN-r-4-r2) is the cell that mints it; its <status> is pending and it is not among this order's landed dependencies (EN-r-2 and the G-V19 group). No system is guessed here."
  },
  {
   "name": "inf-api-assets-v2-lambda-role",
   "step": "R1.d",
   "why": "R1.d: the name's first token resolves to the firm scope (directly, or via R3's bd-as-firm reading when bd carries no adjacent firm token; or via V3's workstream-code reading for wp5/wsb/wsd, refused_keys.workstream_code, infra/logic/registry/systems.json). No later token in the name is a REGISTRY systems.json V1 key, so the system slot cannot be read from the name's own tokens. DATA.grade.placeholder names the registry's resource-to-system rows as the only fill (NAMING_SCHEMA.json v1.9 grade.placeholder; GRADING_RULE.md R1.d, row LGIC_NAMING-W1-S3): which system this specific role's resource BUILDS (SY1, system.vendor_through_tiers) is not something grade(name, type) can read.",
   "missing_row": "infra/logic/registry/resources.json has no row for {\"name\": \"inf-api-assets-v2-lambda-role\", \"type\": \"IAM_ROLE\"} -- the file itself does not exist in this tree. LGIC_ENFORCE cell EN-r-4 (task order LGIC_ENFORCE.TO-EN-r-4-r2) is the cell that mints it; its <status> is pending and it is not among this order's landed dependencies (EN-r-2 and the G-V19 group). No system is guessed here."
  },
  {
   "name": "inf-api-positions-role",
   "step": "R1.d",
   "why": "R1.d: the name's first token resolves to the firm scope (directly, or via R3's bd-as-firm reading when bd carries no adjacent firm token; or via V3's workstream-code reading for wp5/wsb/wsd, refused_keys.workstream_code, infra/logic/registry/systems.json). No later token in the name is a REGISTRY systems.json V1 key, so the system slot cannot be read from the name's own tokens. DATA.grade.placeholder names the registry's resource-to-system rows as the only fill (NAMING_SCHEMA.json v1.9 grade.placeholder; GRADING_RULE.md R1.d, row LGIC_NAMING-W1-S3): which system this specific role's resource BUILDS (SY1, system.vendor_through_tiers) is not something grade(name, type) can read.",
   "missing_row": "infra/logic/registry/resources.json has no row for {\"name\": \"inf-api-positions-role\", \"type\": \"IAM_ROLE\"} -- the file itself does not exist in this tree. LGIC_ENFORCE cell EN-r-4 (task order LGIC_ENFORCE.TO-EN-r-4-r2) is the cell that mints it; its <status> is pending and it is not among this order's landed dependencies (EN-r-2 and the G-V19 group). No system is guessed here."
  },
  {
   "name": "inf-api-reps-role",
   "step": "R1.d",
   "why": "R1.d: the name's first token resolves to the firm scope (directly, or via R3's bd-as-firm reading when bd carries no adjacent firm token; or via V3's workstream-code reading for wp5/wsb/wsd, refused_keys.workstream_code, infra/logic/registry/systems.json). No later token in the name is a REGISTRY systems.json V1 key, so the system slot cannot be read from the name's own tokens. DATA.grade.placeholder names the registry's resource-to-system rows as the only fill (NAMING_SCHEMA.json v1.9 grade.placeholder; GRADING_RULE.md R1.d, row LGIC_NAMING-W1-S3): which system this specific role's resource BUILDS (SY1, system.vendor_through_tiers) is not something grade(name, type) can read.",
   "missing_row": "infra/logic/registry/resources.json has no row for {\"name\": \"inf-api-reps-role\", \"type\": \"IAM_ROLE\"} -- the file itself does not exist in this tree. LGIC_ENFORCE cell EN-r-4 (task order LGIC_ENFORCE.TO-EN-r-4-r2) is the cell that mints it; its <status> is pending and it is not among this order's landed dependencies (EN-r-2 and the G-V19 group). No system is guessed here."
  },
  {
   "name": "inf-api-txn-role",
   "step": "R1.d",
   "why": "R1.d: the name's first token resolves to the firm scope (directly, or via R3's bd-as-firm reading when bd carries no adjacent firm token; or via V3's workstream-code reading for wp5/wsb/wsd, refused_keys.workstream_code, infra/logic/registry/systems.json). No later token in the name is a REGISTRY systems.json V1 key, so the system slot cannot be read from the name's own tokens. DATA.grade.placeholder names the registry's resource-to-system rows as the only fill (NAMING_SCHEMA.json v1.9 grade.placeholder; GRADING_RULE.md R1.d, row LGIC_NAMING-W1-S3): which system this specific role's resource BUILDS (SY1, system.vendor_through_tiers) is not something grade(name, type) can read.",
   "missing_row": "infra/logic/registry/resources.json has no row for {\"name\": \"inf-api-txn-role\", \"type\": \"IAM_ROLE\"} -- the file itself does not exist in this tree. LGIC_ENFORCE cell EN-r-4 (task order LGIC_ENFORCE.TO-EN-r-4-r2) is the cell that mints it; its <status> is pending and it is not among this order's landed dependencies (EN-r-2 and the G-V19 group). No system is guessed here."
  },
  {
   "name": "inf-assets-trigger-lambda-role",
   "step": "R1.d",
   "why": "R1.d: the name's first token resolves to the firm scope (directly, or via R3's bd-as-firm reading when bd carries no adjacent firm token; or via V3's workstream-code reading for wp5/wsb/wsd, refused_keys.workstream_code, infra/logic/registry/systems.json). No later token in the name is a REGISTRY systems.json V1 key, so the system slot cannot be read from the name's own tokens. DATA.grade.placeholder names the registry's resource-to-system rows as the only fill (NAMING_SCHEMA.json v1.9 grade.placeholder; GRADING_RULE.md R1.d, row LGIC_NAMING-W1-S3): which system this specific role's resource BUILDS (SY1, system.vendor_through_tiers) is not something grade(name, type) can read.",
   "missing_row": "infra/logic/registry/resources.json has no row for {\"name\": \"inf-assets-trigger-lambda-role\", \"type\": \"IAM_ROLE\"} -- the file itself does not exist in this tree. LGIC_ENFORCE cell EN-r-4 (task order LGIC_ENFORCE.TO-EN-r-4-r2) is the cell that mints it; its <status> is pending and it is not among this order's landed dependencies (EN-r-2 and the G-V19 group). No system is guessed here."
  },
  {
   "name": "inf-billing-daily-role",
   "step": "R1.d",
   "why": "R1.d: the name's first token resolves to the firm scope (directly, or via R3's bd-as-firm reading when bd carries no adjacent firm token; or via V3's workstream-code reading for wp5/wsb/wsd, refused_keys.workstream_code, infra/logic/registry/systems.json). No later token in the name is a REGISTRY systems.json V1 key, so the system slot cannot be read from the name's own tokens. DATA.grade.placeholder names the registry's resource-to-system rows as the only fill (NAMING_SCHEMA.json v1.9 grade.placeholder; GRADING_RULE.md R1.d, row LGIC_NAMING-W1-S3): which system this specific role's resource BUILDS (SY1, system.vendor_through_tiers) is not something grade(name, type) can read.",
   "missing_row": "infra/logic/registry/resources.json has no row for {\"name\": \"inf-billing-daily-role\", \"type\": \"IAM_ROLE\"} -- the file itself does not exist in this tree. LGIC_ENFORCE cell EN-r-4 (task order LGIC_ENFORCE.TO-EN-r-4-r2) is the cell that mints it; its <status> is pending and it is not among this order's landed dependencies (EN-r-2 and the G-V19 group). No system is guessed here."
  },
  {
   "name": "inf-bronze-complete-emitter-role",
   "step": "R1.d",
   "why": "R1.d: the name's first token resolves to the firm scope (directly, or via R3's bd-as-firm reading when bd carries no adjacent firm token; or via V3's workstream-code reading for wp5/wsb/wsd, refused_keys.workstream_code, infra/logic/registry/systems.json). No later token in the name is a REGISTRY systems.json V1 key, so the system slot cannot be read from the name's own tokens. DATA.grade.placeholder names the registry's resource-to-system rows as the only fill (NAMING_SCHEMA.json v1.9 grade.placeholder; GRADING_RULE.md R1.d, row LGIC_NAMING-W1-S3): which system this specific role's resource BUILDS (SY1, system.vendor_through_tiers) is not something grade(name, type) can read.",
   "missing_row": "infra/logic/registry/resources.json has no row for {\"name\": \"inf-bronze-complete-emitter-role\", \"type\": \"IAM_ROLE\"} -- the file itself does not exist in this tree. LGIC_ENFORCE cell EN-r-4 (task order LGIC_ENFORCE.TO-EN-r-4-r2) is the cell that mints it; its <status> is pending and it is not among this order's landed dependencies (EN-r-2 and the G-V19 group). No system is guessed here."
  },
  {
   "name": "inf-bronze-runner-ec2-role",
   "step": "R1.d",
   "why": "R1.d: the name's first token resolves to the firm scope (directly, or via R3's bd-as-firm reading when bd carries no adjacent firm token; or via V3's workstream-code reading for wp5/wsb/wsd, refused_keys.workstream_code, infra/logic/registry/systems.json). No later token in the name is a REGISTRY systems.json V1 key, so the system slot cannot be read from the name's own tokens. DATA.grade.placeholder names the registry's resource-to-system rows as the only fill (NAMING_SCHEMA.json v1.9 grade.placeholder; GRADING_RULE.md R1.d, row LGIC_NAMING-W1-S3): which system this specific role's resource BUILDS (SY1, system.vendor_through_tiers) is not something grade(name, type) can read.",
   "missing_row": "infra/logic/registry/resources.json has no row for {\"name\": \"inf-bronze-runner-ec2-role\", \"type\": \"IAM_ROLE\"} -- the file itself does not exist in this tree. LGIC_ENFORCE cell EN-r-4 (task order LGIC_ENFORCE.TO-EN-r-4-r2) is the cell that mints it; its <status> is pending and it is not among this order's landed dependencies (EN-r-2 and the G-V19 group). No system is guessed here."
  },
  {
   "name": "inf-bronze-trigger-lambda-role",
   "step": "R1.d",
   "why": "R1.d: the name's first token resolves to the firm scope (directly, or via R3's bd-as-firm reading when bd carries no adjacent firm token; or via V3's workstream-code reading for wp5/wsb/wsd, refused_keys.workstream_code, infra/logic/registry/systems.json). No later token in the name is a REGISTRY systems.json V1 key, so the system slot cannot be read from the name's own tokens. DATA.grade.placeholder names the registry's resource-to-system rows as the only fill (NAMING_SCHEMA.json v1.9 grade.placeholder; GRADING_RULE.md R1.d, row LGIC_NAMING-W1-S3): which system this specific role's resource BUILDS (SY1, system.vendor_through_tiers) is not something grade(name, type) can read.",
   "missing_row": "infra/logic/registry/resources.json has no row for {\"name\": \"inf-bronze-trigger-lambda-role\", \"type\": \"IAM_ROLE\"} -- the file itself does not exist in this tree. LGIC_ENFORCE cell EN-r-4 (task order LGIC_ENFORCE.TO-EN-r-4-r2) is the cell that mints it; its <status> is pending and it is not among this order's landed dependencies (EN-r-2 and the G-V19 group). No system is guessed here."
  },
  {
   "name": "inf-ec2-launch-monitor-lambda-role",
   "step": "R1.d",
   "why": "R1.d: the name's first token resolves to the firm scope (directly, or via R3's bd-as-firm reading when bd carries no adjacent firm token; or via V3's workstream-code reading for wp5/wsb/wsd, refused_keys.workstream_code, infra/logic/registry/systems.json). No later token in the name is a REGISTRY systems.json V1 key, so the system slot cannot be read from the name's own tokens. DATA.grade.placeholder names the registry's resource-to-system rows as the only fill (NAMING_SCHEMA.json v1.9 grade.placeholder; GRADING_RULE.md R1.d, row LGIC_NAMING-W1-S3): which system this specific role's resource BUILDS (SY1, system.vendor_through_tiers) is not something grade(name, type) can read.",
   "missing_row": "infra/logic/registry/resources.json has no row for {\"name\": \"inf-ec2-launch-monitor-lambda-role\", \"type\": \"IAM_ROLE\"} -- the file itself does not exist in this tree. LGIC_ENFORCE cell EN-r-4 (task order LGIC_ENFORCE.TO-EN-r-4-r2) is the cell that mints it; its <status> is pending and it is not among this order's landed dependencies (EN-r-2 and the G-V19 group). No system is guessed here."
  },
  {
   "name": "inf-ec2-retry-launch-lambda-role",
   "step": "R1.d",
   "why": "R1.d: the name's first token resolves to the firm scope (directly, or via R3's bd-as-firm reading when bd carries no adjacent firm token; or via V3's workstream-code reading for wp5/wsb/wsd, refused_keys.workstream_code, infra/logic/registry/systems.json). No later token in the name is a REGISTRY systems.json V1 key, so the system slot cannot be read from the name's own tokens. DATA.grade.placeholder names the registry's resource-to-system rows as the only fill (NAMING_SCHEMA.json v1.9 grade.placeholder; GRADING_RULE.md R1.d, row LGIC_NAMING-W1-S3): which system this specific role's resource BUILDS (SY1, system.vendor_through_tiers) is not something grade(name, type) can read.",
   "missing_row": "infra/logic/registry/resources.json has no row for {\"name\": \"inf-ec2-retry-launch-lambda-role\", \"type\": \"IAM_ROLE\"} -- the file itself does not exist in this tree. LGIC_ENFORCE cell EN-r-4 (task order LGIC_ENFORCE.TO-EN-r-4-r2) is the cell that mints it; its <status> is pending and it is not among this order's landed dependencies (EN-r-2 and the G-V19 group). No system is guessed here."
  },
  {
   "name": "inf-etf-ownership-daily-role",
   "step": "R1.d",
   "why": "R1.d: the name's first token resolves to the firm scope (directly, or via R3's bd-as-firm reading when bd carries no adjacent firm token; or via V3's workstream-code reading for wp5/wsb/wsd, refused_keys.workstream_code, infra/logic/registry/systems.json). No later token in the name is a REGISTRY systems.json V1 key, so the system slot cannot be read from the name's own tokens. DATA.grade.placeholder names the registry's resource-to-system rows as the only fill (NAMING_SCHEMA.json v1.9 grade.placeholder; GRADING_RULE.md R1.d, row LGIC_NAMING-W1-S3): which system this specific role's resource BUILDS (SY1, system.vendor_through_tiers) is not something grade(name, type) can read.",
   "missing_row": "infra/logic/registry/resources.json has no row for {\"name\": \"inf-etf-ownership-daily-role\", \"type\": \"IAM_ROLE\"} -- the file itself does not exist in this tree. LGIC_ENFORCE cell EN-r-4 (task order LGIC_ENFORCE.TO-EN-r-4-r2) is the cell that mints it; its <status> is pending and it is not among this order's landed dependencies (EN-r-2 and the G-V19 group). No system is guessed here."
  },
  {
   "name": "inf-eventbridge-ssm-role",
   "step": "R1.d",
   "why": "R1.d: the name's first token resolves to the firm scope (directly, or via R3's bd-as-firm reading when bd carries no adjacent firm token; or via V3's workstream-code reading for wp5/wsb/wsd, refused_keys.workstream_code, infra/logic/registry/systems.json). No later token in the name is a REGISTRY systems.json V1 key, so the system slot cannot be read from the name's own tokens. DATA.grade.placeholder names the registry's resource-to-system rows as the only fill (NAMING_SCHEMA.json v1.9 grade.placeholder; GRADING_RULE.md R1.d, row LGIC_NAMING-W1-S3): which system this specific role's resource BUILDS (SY1, system.vendor_through_tiers) is not something grade(name, type) can read.",
   "missing_row": "infra/logic/registry/resources.json has no row for {\"name\": \"inf-eventbridge-ssm-role\", \"type\": \"IAM_ROLE\"} -- the file itself does not exist in this tree. LGIC_ENFORCE cell EN-r-4 (task order LGIC_ENFORCE.TO-EN-r-4-r2) is the cell that mints it; its <status> is pending and it is not among this order's landed dependencies (EN-r-2 and the G-V19 group). No system is guessed here."
  },
  {
   "name": "inf-exporter-ec2-role",
   "step": "R1.d",
   "why": "R1.d: the name's first token resolves to the firm scope (directly, or via R3's bd-as-firm reading when bd carries no adjacent firm token; or via V3's workstream-code reading for wp5/wsb/wsd, refused_keys.workstream_code, infra/logic/registry/systems.json). No later token in the name is a REGISTRY systems.json V1 key, so the system slot cannot be read from the name's own tokens. DATA.grade.placeholder names the registry's resource-to-system rows as the only fill (NAMING_SCHEMA.json v1.9 grade.placeholder; GRADING_RULE.md R1.d, row LGIC_NAMING-W1-S3): which system this specific role's resource BUILDS (SY1, system.vendor_through_tiers) is not something grade(name, type) can read.",
   "missing_row": "infra/logic/registry/resources.json has no row for {\"name\": \"inf-exporter-ec2-role\", \"type\": \"IAM_ROLE\"} -- the file itself does not exist in this tree. LGIC_ENFORCE cell EN-r-4 (task order LGIC_ENFORCE.TO-EN-r-4-r2) is the cell that mints it; its <status> is pending and it is not among this order's landed dependencies (EN-r-2 and the G-V19 group). No system is guessed here."
  },
  {
   "name": "inf-gold-layer-ec2-role",
   "step": "R1.d",
   "why": "R1.d: the name's first token resolves to the firm scope (directly, or via R3's bd-as-firm reading when bd carries no adjacent firm token; or via V3's workstream-code reading for wp5/wsb/wsd, refused_keys.workstream_code, infra/logic/registry/systems.json). No later token in the name is a REGISTRY systems.json V1 key, so the system slot cannot be read from the name's own tokens. DATA.grade.placeholder names the registry's resource-to-system rows as the only fill (NAMING_SCHEMA.json v1.9 grade.placeholder; GRADING_RULE.md R1.d, row LGIC_NAMING-W1-S3): which system this specific role's resource BUILDS (SY1, system.vendor_through_tiers) is not something grade(name, type) can read.",
   "missing_row": "infra/logic/registry/resources.json has no row for {\"name\": \"inf-gold-layer-ec2-role\", \"type\": \"IAM_ROLE\"} -- the file itself does not exist in this tree. LGIC_ENFORCE cell EN-r-4 (task order LGIC_ENFORCE.TO-EN-r-4-r2) is the cell that mints it; its <status> is pending and it is not among this order's landed dependencies (EN-r-2 and the G-V19 group). No system is guessed here."
  },
  {
   "name": "inf-gold-layer-lambda-role",
   "step": "R1.d",
   "why": "R1.d: the name's first token resolves to the firm scope (directly, or via R3's bd-as-firm reading when bd carries no adjacent firm token; or via V3's workstream-code reading for wp5/wsb/wsd, refused_keys.workstream_code, infra/logic/registry/systems.json). No later token in the name is a REGISTRY systems.json V1 key, so the system slot cannot be read from the name's own tokens. DATA.grade.placeholder names the registry's resource-to-system rows as the only fill (NAMING_SCHEMA.json v1.9 grade.placeholder; GRADING_RULE.md R1.d, row LGIC_NAMING-W1-S3): which system this specific role's resource BUILDS (SY1, system.vendor_through_tiers) is not something grade(name, type) can read.",
   "missing_row": "infra/logic/registry/resources.json has no row for {\"name\": \"inf-gold-layer-lambda-role\", \"type\": \"IAM_ROLE\"} -- the file itself does not exist in this tree. LGIC_ENFORCE cell EN-r-4 (task order LGIC_ENFORCE.TO-EN-r-4-r2) is the cell that mints it; its <status> is pending and it is not among this order's landed dependencies (EN-r-2 and the G-V19 group). No system is guessed here."
  },
  {
   "name": "inf-gold-qa-runner-ec2-role",
   "step": "R1.d",
   "why": "R1.d: the name's first token resolves to the firm scope (directly, or via R3's bd-as-firm reading when bd carries no adjacent firm token; or via V3's workstream-code reading for wp5/wsb/wsd, refused_keys.workstream_code, infra/logic/registry/systems.json). No later token in the name is a REGISTRY systems.json V1 key, so the system slot cannot be read from the name's own tokens. DATA.grade.placeholder names the registry's resource-to-system rows as the only fill (NAMING_SCHEMA.json v1.9 grade.placeholder; GRADING_RULE.md R1.d, row LGIC_NAMING-W1-S3): which system this specific role's resource BUILDS (SY1, system.vendor_through_tiers) is not something grade(name, type) can read.",
   "missing_row": "infra/logic/registry/resources.json has no row for {\"name\": \"inf-gold-qa-runner-ec2-role\", \"type\": \"IAM_ROLE\"} -- the file itself does not exist in this tree. LGIC_ENFORCE cell EN-r-4 (task order LGIC_ENFORCE.TO-EN-r-4-r2) is the cell that mints it; its <status> is pending and it is not among this order's landed dependencies (EN-r-2 and the G-V19 group). No system is guessed here."
  },
  {
   "name": "inf-gold-trigger-lambda-role",
   "step": "R1.d",
   "why": "R1.d: the name's first token resolves to the firm scope (directly, or via R3's bd-as-firm reading when bd carries no adjacent firm token; or via V3's workstream-code reading for wp5/wsb/wsd, refused_keys.workstream_code, infra/logic/registry/systems.json). No later token in the name is a REGISTRY systems.json V1 key, so the system slot cannot be read from the name's own tokens. DATA.grade.placeholder names the registry's resource-to-system rows as the only fill (NAMING_SCHEMA.json v1.9 grade.placeholder; GRADING_RULE.md R1.d, row LGIC_NAMING-W1-S3): which system this specific role's resource BUILDS (SY1, system.vendor_through_tiers) is not something grade(name, type) can read.",
   "missing_row": "infra/logic/registry/resources.json has no row for {\"name\": \"inf-gold-trigger-lambda-role\", \"type\": \"IAM_ROLE\"} -- the file itself does not exist in this tree. LGIC_ENFORCE cell EN-r-4 (task order LGIC_ENFORCE.TO-EN-r-4-r2) is the cell that mints it; its <status> is pending and it is not among this order's landed dependencies (EN-r-2 and the G-V19 group). No system is guessed here."
  },
  {
   "name": "inf-jwt-trigger-lambda-role",
   "step": "R1.d",
   "why": "R1.d: the name's first token resolves to the firm scope (directly, or via R3's bd-as-firm reading when bd carries no adjacent firm token; or via V3's workstream-code reading for wp5/wsb/wsd, refused_keys.workstream_code, infra/logic/registry/systems.json). No later token in the name is a REGISTRY systems.json V1 key, so the system slot cannot be read from the name's own tokens. DATA.grade.placeholder names the registry's resource-to-system rows as the only fill (NAMING_SCHEMA.json v1.9 grade.placeholder; GRADING_RULE.md R1.d, row LGIC_NAMING-W1-S3): which system this specific role's resource BUILDS (SY1, system.vendor_through_tiers) is not something grade(name, type) can read.",
   "missing_row": "infra/logic/registry/resources.json has no row for {\"name\": \"inf-jwt-trigger-lambda-role\", \"type\": \"IAM_ROLE\"} -- the file itself does not exist in this tree. LGIC_ENFORCE cell EN-r-4 (task order LGIC_ENFORCE.TO-EN-r-4-r2) is the cell that mints it; its <status> is pending and it is not among this order's landed dependencies (EN-r-2 and the G-V19 group). No system is guessed here."
  },
  {
   "name": "inf-nna-partition-checker-lambda-role",
   "step": "R1.d",
   "why": "R1.d: the name's first token resolves to the firm scope (directly, or via R3's bd-as-firm reading when bd carries no adjacent firm token; or via V3's workstream-code reading for wp5/wsb/wsd, refused_keys.workstream_code, infra/logic/registry/systems.json). No later token in the name is a REGISTRY systems.json V1 key, so the system slot cannot be read from the name's own tokens. DATA.grade.placeholder names the registry's resource-to-system rows as the only fill (NAMING_SCHEMA.json v1.9 grade.placeholder; GRADING_RULE.md R1.d, row LGIC_NAMING-W1-S3): which system this specific role's resource BUILDS (SY1, system.vendor_through_tiers) is not something grade(name, type) can read.",
   "missing_row": "infra/logic/registry/resources.json has no row for {\"name\": \"inf-nna-partition-checker-lambda-role\", \"type\": \"IAM_ROLE\"} -- the file itself does not exist in this tree. LGIC_ENFORCE cell EN-r-4 (task order LGIC_ENFORCE.TO-EN-r-4-r2) is the cell that mints it; its <status> is pending and it is not among this order's landed dependencies (EN-r-2 and the G-V19 group). No system is guessed here."
  },
  {
   "name": "inf-otp-relay-lambda-role",
   "step": "R1.d",
   "why": "R1.d: the name's first token resolves to the firm scope (directly, or via R3's bd-as-firm reading when bd carries no adjacent firm token; or via V3's workstream-code reading for wp5/wsb/wsd, refused_keys.workstream_code, infra/logic/registry/systems.json). No later token in the name is a REGISTRY systems.json V1 key, so the system slot cannot be read from the name's own tokens. DATA.grade.placeholder names the registry's resource-to-system rows as the only fill (NAMING_SCHEMA.json v1.9 grade.placeholder; GRADING_RULE.md R1.d, row LGIC_NAMING-W1-S3): which system this specific role's resource BUILDS (SY1, system.vendor_through_tiers) is not something grade(name, type) can read.",
   "missing_row": "infra/logic/registry/resources.json has no row for {\"name\": \"inf-otp-relay-lambda-role\", \"type\": \"IAM_ROLE\"} -- the file itself does not exist in this tree. LGIC_ENFORCE cell EN-r-4 (task order LGIC_ENFORCE.TO-EN-r-4-r2) is the cell that mints it; its <status> is pending and it is not among this order's landed dependencies (EN-r-2 and the G-V19 group). No system is guessed here."
  },
  {
   "name": "inf-performance-daily-role",
   "step": "R1.d",
   "why": "R1.d: the name's first token resolves to the firm scope (directly, or via R3's bd-as-firm reading when bd carries no adjacent firm token; or via V3's workstream-code reading for wp5/wsb/wsd, refused_keys.workstream_code, infra/logic/registry/systems.json). No later token in the name is a REGISTRY systems.json V1 key, so the system slot cannot be read from the name's own tokens. DATA.grade.placeholder names the registry's resource-to-system rows as the only fill (NAMING_SCHEMA.json v1.9 grade.placeholder; GRADING_RULE.md R1.d, row LGIC_NAMING-W1-S3): which system this specific role's resource BUILDS (SY1, system.vendor_through_tiers) is not something grade(name, type) can read.",
   "missing_row": "infra/logic/registry/resources.json has no row for {\"name\": \"inf-performance-daily-role\", \"type\": \"IAM_ROLE\"} -- the file itself does not exist in this tree. LGIC_ENFORCE cell EN-r-4 (task order LGIC_ENFORCE.TO-EN-r-4-r2) is the cell that mints it; its <status> is pending and it is not among this order's landed dependencies (EN-r-2 and the G-V19 group). No system is guessed here."
  },
  {
   "name": "inf-silver-aggregator-lambda-role",
   "step": "R1.d",
   "why": "R1.d: the name's first token resolves to the firm scope (directly, or via R3's bd-as-firm reading when bd carries no adjacent firm token; or via V3's workstream-code reading for wp5/wsb/wsd, refused_keys.workstream_code, infra/logic/registry/systems.json). No later token in the name is a REGISTRY systems.json V1 key, so the system slot cannot be read from the name's own tokens. DATA.grade.placeholder names the registry's resource-to-system rows as the only fill (NAMING_SCHEMA.json v1.9 grade.placeholder; GRADING_RULE.md R1.d, row LGIC_NAMING-W1-S3): which system this specific role's resource BUILDS (SY1, system.vendor_through_tiers) is not something grade(name, type) can read.",
   "missing_row": "infra/logic/registry/resources.json has no row for {\"name\": \"inf-silver-aggregator-lambda-role\", \"type\": \"IAM_ROLE\"} -- the file itself does not exist in this tree. LGIC_ENFORCE cell EN-r-4 (task order LGIC_ENFORCE.TO-EN-r-4-r2) is the cell that mints it; its <status> is pending and it is not among this order's landed dependencies (EN-r-2 and the G-V19 group). No system is guessed here."
  },
  {
   "name": "inf-silver-chain-lambda-role",
   "step": "R1.d",
   "why": "R1.d: the name's first token resolves to the firm scope (directly, or via R3's bd-as-firm reading when bd carries no adjacent firm token; or via V3's workstream-code reading for wp5/wsb/wsd, refused_keys.workstream_code, infra/logic/registry/systems.json). No later token in the name is a REGISTRY systems.json V1 key, so the system slot cannot be read from the name's own tokens. DATA.grade.placeholder names the registry's resource-to-system rows as the only fill (NAMING_SCHEMA.json v1.9 grade.placeholder; GRADING_RULE.md R1.d, row LGIC_NAMING-W1-S3): which system this specific role's resource BUILDS (SY1, system.vendor_through_tiers) is not something grade(name, type) can read.",
   "missing_row": "infra/logic/registry/resources.json has no row for {\"name\": \"inf-silver-chain-lambda-role\", \"type\": \"IAM_ROLE\"} -- the file itself does not exist in this tree. LGIC_ENFORCE cell EN-r-4 (task order LGIC_ENFORCE.TO-EN-r-4-r2) is the cell that mints it; its <status> is pending and it is not among this order's landed dependencies (EN-r-2 and the G-V19 group). No system is guessed here."
  },
  {
   "name": "inf-tax-daily-role",
   "step": "R1.d",
   "why": "R1.d: the name's first token resolves to the firm scope (directly, or via R3's bd-as-firm reading when bd carries no adjacent firm token; or via V3's workstream-code reading for wp5/wsb/wsd, refused_keys.workstream_code, infra/logic/registry/systems.json). No later token in the name is a REGISTRY systems.json V1 key, so the system slot cannot be read from the name's own tokens. DATA.grade.placeholder names the registry's resource-to-system rows as the only fill (NAMING_SCHEMA.json v1.9 grade.placeholder; GRADING_RULE.md R1.d, row LGIC_NAMING-W1-S3): which system this specific role's resource BUILDS (SY1, system.vendor_through_tiers) is not something grade(name, type) can read.",
   "missing_row": "infra/logic/registry/resources.json has no row for {\"name\": \"inf-tax-daily-role\", \"type\": \"IAM_ROLE\"} -- the file itself does not exist in this tree. LGIC_ENFORCE cell EN-r-4 (task order LGIC_ENFORCE.TO-EN-r-4-r2) is the cell that mints it; its <status> is pending and it is not among this order's landed dependencies (EN-r-2 and the G-V19 group). No system is guessed here."
  },
  {
   "name": "inf-unified-account-dim-daily-role",
   "step": "R1.d",
   "why": "R1.d: the name's first token resolves to the firm scope (directly, or via R3's bd-as-firm reading when bd carries no adjacent firm token; or via V3's workstream-code reading for wp5/wsb/wsd, refused_keys.workstream_code, infra/logic/registry/systems.json). No later token in the name is a REGISTRY systems.json V1 key, so the system slot cannot be read from the name's own tokens. DATA.grade.placeholder names the registry's resource-to-system rows as the only fill (NAMING_SCHEMA.json v1.9 grade.placeholder; GRADING_RULE.md R1.d, row LGIC_NAMING-W1-S3): which system this specific role's resource BUILDS (SY1, system.vendor_through_tiers) is not something grade(name, type) can read.",
   "missing_row": "infra/logic/registry/resources.json has no row for {\"name\": \"inf-unified-account-dim-daily-role\", \"type\": \"IAM_ROLE\"} -- the file itself does not exist in this tree. LGIC_ENFORCE cell EN-r-4 (task order LGIC_ENFORCE.TO-EN-r-4-r2) is the cell that mints it; its <status> is pending and it is not among this order's landed dependencies (EN-r-2 and the G-V19 group). No system is guessed here."
  },
  {
   "name": "cot-etf-ownership-daily-role",
   "step": "R1.d",
   "why": "R1.d: the name's first token resolves to the firm scope (directly, or via R3's bd-as-firm reading when bd carries no adjacent firm token; or via V3's workstream-code reading for wp5/wsb/wsd, refused_keys.workstream_code, infra/logic/registry/systems.json). No later token in the name is a REGISTRY systems.json V1 key, so the system slot cannot be read from the name's own tokens. DATA.grade.placeholder names the registry's resource-to-system rows as the only fill (NAMING_SCHEMA.json v1.9 grade.placeholder; GRADING_RULE.md R1.d, row LGIC_NAMING-W1-S3): which system this specific role's resource BUILDS (SY1, system.vendor_through_tiers) is not something grade(name, type) can read.",
   "missing_row": "infra/logic/registry/resources.json has no row for {\"name\": \"cot-etf-ownership-daily-role\", \"type\": \"IAM_ROLE\"} -- the file itself does not exist in this tree. LGIC_ENFORCE cell EN-r-4 (task order LGIC_ENFORCE.TO-EN-r-4-r2) is the cell that mints it; its <status> is pending and it is not among this order's landed dependencies (EN-r-2 and the G-V19 group). No system is guessed here."
  },
  {
   "name": "cot-exporter-ec2-role",
   "step": "R1.d",
   "why": "R1.d: the name's first token resolves to the firm scope (directly, or via R3's bd-as-firm reading when bd carries no adjacent firm token; or via V3's workstream-code reading for wp5/wsb/wsd, refused_keys.workstream_code, infra/logic/registry/systems.json). No later token in the name is a REGISTRY systems.json V1 key, so the system slot cannot be read from the name's own tokens. DATA.grade.placeholder names the registry's resource-to-system rows as the only fill (NAMING_SCHEMA.json v1.9 grade.placeholder; GRADING_RULE.md R1.d, row LGIC_NAMING-W1-S3): which system this specific role's resource BUILDS (SY1, system.vendor_through_tiers) is not something grade(name, type) can read.",
   "missing_row": "infra/logic/registry/resources.json has no row for {\"name\": \"cot-exporter-ec2-role\", \"type\": \"IAM_ROLE\"} -- the file itself does not exist in this tree. LGIC_ENFORCE cell EN-r-4 (task order LGIC_ENFORCE.TO-EN-r-4-r2) is the cell that mints it; its <status> is pending and it is not among this order's landed dependencies (EN-r-2 and the G-V19 group). No system is guessed here."
  },
  {
   "name": "cot-gold-layer-ec2-role",
   "step": "R1.d",
   "why": "R1.d: the name's first token resolves to the firm scope (directly, or via R3's bd-as-firm reading when bd carries no adjacent firm token; or via V3's workstream-code reading for wp5/wsb/wsd, refused_keys.workstream_code, infra/logic/registry/systems.json). No later token in the name is a REGISTRY systems.json V1 key, so the system slot cannot be read from the name's own tokens. DATA.grade.placeholder names the registry's resource-to-system rows as the only fill (NAMING_SCHEMA.json v1.9 grade.placeholder; GRADING_RULE.md R1.d, row LGIC_NAMING-W1-S3): which system this specific role's resource BUILDS (SY1, system.vendor_through_tiers) is not something grade(name, type) can read.",
   "missing_row": "infra/logic/registry/resources.json has no row for {\"name\": \"cot-gold-layer-ec2-role\", \"type\": \"IAM_ROLE\"} -- the file itself does not exist in this tree. LGIC_ENFORCE cell EN-r-4 (task order LGIC_ENFORCE.TO-EN-r-4-r2) is the cell that mints it; its <status> is pending and it is not among this order's landed dependencies (EN-r-2 and the G-V19 group). No system is guessed here."
  },
  {
   "name": "cot-rebalancer-runner-role",
   "step": "R1.d",
   "why": "R1.d: the name's first token resolves to the firm scope (directly, or via R3's bd-as-firm reading when bd carries no adjacent firm token; or via V3's workstream-code reading for wp5/wsb/wsd, refused_keys.workstream_code, infra/logic/registry/systems.json). No later token in the name is a REGISTRY systems.json V1 key, so the system slot cannot be read from the name's own tokens. DATA.grade.placeholder names the registry's resource-to-system rows as the only fill (NAMING_SCHEMA.json v1.9 grade.placeholder; GRADING_RULE.md R1.d, row LGIC_NAMING-W1-S3): which system this specific role's resource BUILDS (SY1, system.vendor_through_tiers) is not something grade(name, type) can read.",
   "missing_row": "infra/logic/registry/resources.json has no row for {\"name\": \"cot-rebalancer-runner-role\", \"type\": \"IAM_ROLE\"} -- the file itself does not exist in this tree. LGIC_ENFORCE cell EN-r-4 (task order LGIC_ENFORCE.TO-EN-r-4-r2) is the cell that mints it; its <status> is pending and it is not among this order's landed dependencies (EN-r-2 and the G-V19 group). No system is guessed here."
  },
  {
   "name": "cot-satellites-registry-producer-role",
   "step": "R1.d",
   "why": "R1.d: the name's first token resolves to the firm scope (directly, or via R3's bd-as-firm reading when bd carries no adjacent firm token; or via V3's workstream-code reading for wp5/wsb/wsd, refused_keys.workstream_code, infra/logic/registry/systems.json). No later token in the name is a REGISTRY systems.json V1 key, so the system slot cannot be read from the name's own tokens. DATA.grade.placeholder names the registry's resource-to-system rows as the only fill (NAMING_SCHEMA.json v1.9 grade.placeholder; GRADING_RULE.md R1.d, row LGIC_NAMING-W1-S3): which system this specific role's resource BUILDS (SY1, system.vendor_through_tiers) is not something grade(name, type) can read.",
   "missing_row": "infra/logic/registry/resources.json has no row for {\"name\": \"cot-satellites-registry-producer-role\", \"type\": \"IAM_ROLE\"} -- the file itself does not exist in this tree. LGIC_ENFORCE cell EN-r-4 (task order LGIC_ENFORCE.TO-EN-r-4-r2) is the cell that mints it; its <status> is pending and it is not among this order's landed dependencies (EN-r-2 and the G-V19 group). No system is guessed here."
  },
  {
   "name": "cot-session-scheduler-role",
   "step": "R1.d",
   "why": "R1.d: the name's first token resolves to the firm scope (directly, or via R3's bd-as-firm reading when bd carries no adjacent firm token; or via V3's workstream-code reading for wp5/wsb/wsd, refused_keys.workstream_code, infra/logic/registry/systems.json). No later token in the name is a REGISTRY systems.json V1 key, so the system slot cannot be read from the name's own tokens. DATA.grade.placeholder names the registry's resource-to-system rows as the only fill (NAMING_SCHEMA.json v1.9 grade.placeholder; GRADING_RULE.md R1.d, row LGIC_NAMING-W1-S3): which system this specific role's resource BUILDS (SY1, system.vendor_through_tiers) is not something grade(name, type) can read.",
   "missing_row": "infra/logic/registry/resources.json has no row for {\"name\": \"cot-session-scheduler-role\", \"type\": \"IAM_ROLE\"} -- the file itself does not exist in this tree. LGIC_ENFORCE cell EN-r-4 (task order LGIC_ENFORCE.TO-EN-r-4-r2) is the cell that mints it; its <status> is pending and it is not among this order's landed dependencies (EN-r-2 and the G-V19 group). No system is guessed here."
  },
  {
   "name": "demo-transform-runner-ec2-role",
   "step": "R1.d",
   "why": "R1.d: the name's first token resolves to the firm scope (directly, or via R3's bd-as-firm reading when bd carries no adjacent firm token; or via V3's workstream-code reading for wp5/wsb/wsd, refused_keys.workstream_code, infra/logic/registry/systems.json). No later token in the name is a REGISTRY systems.json V1 key, so the system slot cannot be read from the name's own tokens. DATA.grade.placeholder names the registry's resource-to-system rows as the only fill (NAMING_SCHEMA.json v1.9 grade.placeholder; GRADING_RULE.md R1.d, row LGIC_NAMING-W1-S3): which system this specific role's resource BUILDS (SY1, system.vendor_through_tiers) is not something grade(name, type) can read.",
   "missing_row": "infra/logic/registry/resources.json has no row for {\"name\": \"demo-transform-runner-ec2-role\", \"type\": \"IAM_ROLE\"} -- the file itself does not exist in this tree. LGIC_ENFORCE cell EN-r-4 (task order LGIC_ENFORCE.TO-EN-r-4-r2) is the cell that mints it; its <status> is pending and it is not among this order's landed dependencies (EN-r-2 and the G-V19 group). No system is guessed here."
  }
 ],
 "denominator": {
  "iam_roles_live": 240,
  "with_a_firm_alias_token": 69,
  "attributed": 69,
  "excluded": 0,
  "raise": 49,
  "placeholders_filled": 0,
  "placeholders_raised": 49
 }
}
```
