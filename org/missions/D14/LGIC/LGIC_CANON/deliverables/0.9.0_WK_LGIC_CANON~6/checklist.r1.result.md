# LGIC_CANON.TO-CN-o-1 -- result (cell CN-o-1, round 1)

**Worker:** 0.9.0_WK_LGIC_CANON~6 · **Issuer:** 2.0.0_SA_COO~G · **Branch:** `wk-lgic-canon-1-6`, cut from CLOUD
@`671925aecc`, in the reused directory `.worktrees/wk-lgic-canon-1-1`.
**Artifacts:**
- the new `infra/logic/10_ONBOARDING_CHECKLIST.md`, with 16 steps;
- rows `LGIC_CANON-W6-S1`, `-W6-S2` and `-W6-S3` in the channel;
- this file.

They are committed together, and the proof instance pins them by that commit.
**Nothing live moves (DEC-9).** The registry, the schema, the canon and every builder were read and not written.

## Premises re-grounded at the start

- **The base.** The canon at the base is v1.0 (`02_DOCTRINE.md` header, `RULES CARRYING ALL THREE PARTS: 21 of 21`),
  so R1..R21 are the rule ids a step may cite.
- **Rule 30** is present in the worktree's `CLAUDE.md`, as the order cites it.
- **The CONTRACTS table** of `LGIC_ENFORCE_PRD.md` (`:159-171`) has nine rows. The checker reads the same nine
  (`contract names: 9`).
- **The builders.** The docstrings of `key()`, `address()` and `name()` (`lib/opal_naming.py:1287-1353`) match the
  order's description. Neither `key()` nor `address()` takes a bucket, and `name()` takes the LONG scope and writes
  the SHORT form.
- **LGIC_ENFORCE's order statuses at the base** decide each step's `built:` line:
  - complete: `EN-r-1`, `EN-b-1`, `EN-m-1`, `EN-f-1`, `EN-f-2`, `EN-g-1`, `EN-t-2` and `EN-v-2`..`EN-v-6`;
  - pending: `EN-s-1` (both round-1 and round-2 orders), `EN-r-3-r2` (the firm-forms move), `EN-t-2-r2` (the plan
    limb) and `EN-v-1`.

  So `data/firm_registry.json`, whose view order is still pending, is not cited as a built file. `firm-config.mjs`,
  whose view order is complete, is cited instead.
- **The DEC-6 path** runs: identity row, bucket from the template, IAM under the fence, pipelines through `key()` and
  `address()`, routes, served dashboard. The 16 steps follow that path in that order.
- **Baseline before the file existed, as the negative control.** All four criteria read FAIL:
  - `FAIL-O1-NO-STEPS`
  - `FAIL-O1-RULES-NO-STEPS`
  - `FAIL-O1-BUILDERS-ABSENT` (`contract names: 9`)
  - `FAIL-O1-BUILT-NO-STEPS`

## The criteria

Every invocation is
`cd <WS> && timeout 120 python org/missions/D14/LGIC/LGIC_CANON/deliverables/2.0.0_SA_COO~G/fixed_inputs/r1/check_canon_r1.py <sub>`,
with `<WS>` = `/c/Users/AndrewBerman/Desktop/ajb_workspace/.worktrees/wk-lgic-canon-1-1`. The outputs below are from
the run on the written file before the commit. The proof instance records the re-run at the commit.

| id | sub | deciding output | rc | denominator | status |
|---|---|---|---|---|---|
| O1-AC1 | `o1-order` | `STEPS: 16 numbered [1, ..., 16]  FIRST NAMES THE IDENTITY ROW: True  LAST NAMES THE DASHBOARD: True` / `VERDICT: PASS-O1-ORDERED` | 0 | 16 of 16 steps numbered 1..16 | PASS-by-output |
| O1-AC2 | `o1-rules` | `STEPS: 16  NAMING A CANON RULE: 16` / `VERDICT: PASS-O1-RULES-NAMED` | 0 | 16 of 16 | PASS-by-output |
| O1-AC3 | `o1-builders` | `STEPS: 16  NAMING A CONTRACT: 16  (contract names: 9)` / `VERDICT: PASS-O1-BUILDERS-NAMED` | 0 | 16 of 16, against 9 contract names | PASS-by-output |
| O1-AC4 | `o1-unbuilt` | `STEPS: 16  BUILT STATE PROVED OR ITS CELL NAMED: 16` / `VERDICT: PASS-O1-BUILT-STATED` | 0 | 16 of 16 (15 `built: yes` on a path that exists, 1 `built: no EN-s-1`) | PASS-by-output |

**The mutant control** was run on the file itself and then restored; the sha256 was equal after the restore. Two lines
were changed: Step 12's rule became `R99`, and Step 13's builder and built lines became `census mode` / `no census`.
- `o1-rules` read `FAIL-O1-RULE-UNNAMED` (15 of 16).
- `o1-builders` read `FAIL-O1-BUILDER-UNNAMED` (15 of 16).
- `o1-unbuilt` read `FAIL-O1-BUILT-UNSTATED` (15 of 16).

After the restore, all three read PASS again, 16 of 16.

## What each step names

| step | what | rule | builder (CONTRACTS name) | built |
|---|---|---|---|---|
| 1 | the identity row | R2, R5, R7 | the identity registry's ROWS | yes `infra/logic/registry/scopes.json` |
| 2 | the firm list, while the schema carries it | R1 | `org/standards/NAMING_SCHEMA.json` | yes |
| 3 | masters, monolith scopes, pipeline tree | R3, R7 | the identity registry's ROWS | yes |
| 4 | regenerate the views | R1, R6 | the generated views | yes `firm-config.mjs` |
| 5 | the bucket's exemption list | R6, R7 | the fence patterns | yes `exemptions.json` |
| 6 | the bucket from the template | R1, R5, R6 | the fence patterns (the template) | yes `s3-49financial.tf` |
| 7 | resource names | R1, R7 | `lib/opal_naming.py` `name()` | yes |
| 8 | bronze and silver | R4, R9, R10 | `lib/opal_naming.py` `key()`/`address()` | yes |
| 9 | gold, state, code | R5, R11, R13, R16, R21 | `lib/opal_naming.py` `address()` | yes |
| 10 | platinum (STOP at tier-first served keys) | R6, R12, R14 | `lib/opal_naming.py` `address()` | yes |
| 11 | commit through the flagger | R1, R20 | the flagger's verdict line and kill switch | yes `.tools/naming-gate.py` |
| 12 | apply through safe-apply | R1, R18 | the flagger's verdict line and kill switch | yes `.tools/safe-apply.sh` |
| 13 | census | R1 | the census report | **no `EN-s-1`** |
| 14 | the people's sign-in (STOP for the path list) | R6 | the identity registry's ROWS | yes |
| 15 | routes | R6, R12 | the generated views | yes `firm-config.mjs` |
| 16 | the served dashboard | R6, R12, R14 | the generated views | yes `firm-config.mjs` |

## Choices left for the reviewer (CN-o-2) and L9

- **Stops routed to an owner.** Four values have no builder at this vintage: the firm's two forms, the tenant facts,
  the portal path list, and the served ownership-map key. Each is either an input from Andrew or a STOP naming its
  row. A STOP is written as mechanical: the runner stops and does not choose. Whether a STOP counts as
  "no judgement" is the reviewer's to mark.
- **Step 2 is conditional.** It keys on the `validate` WARN line recorded by `EXERCISE_FWD7.md:35`, so the step
  becomes a no-op once `EN-r-3` moves the firm list. The checklist does not need rewriting when that lands.
- **Step 3(c) is a new separation rule.** It separates a new firm's pipeline tree from every other firm, and adds the
  new firm to every existing tree's `separated_from`, reading CLAUDE.md section 5's NEVER. The existing rows are not
  all-to-all (`49financial` is separated from `cottonwood` only), so this reading is new to the registry.
- **Steps 14 and 16 cite R6.** The canon rules only the storage plane, so R6 (tenant separation) is the nearest rule
  for the sign-in and the dashboard (row W6-S2).

## Rows filed

- `LGIC_CANON-W6-S1` -- no rule or builder produces a new firm's LONG and SHORT forms; the only runbook has the
  operator choose. OBSERVATION, INERT.
- `LGIC_CANON-W6-S2` -- the sign-in acts (partner table, user rows, the portal page-access map) have no CONTRACTS
  builder and are not generated views. OBSERVATION, INERT.
- `LGIC_CANON-W6-S3` -- the served routes read tier-first keys that `key()` and `address()` cannot produce, and the
  list of legacy served paths does not exist yet. OBSERVATION, INERT.
