# ADVI_PERFRP.TO-R1-AE — AC5 (PRF-inv-5): the FIRM PIN at IAM

**Seat:** `0.7.0_AE_CloudOps~G` · **TO:** `ADVI_PERFRP.TO-R1-AE` · **Cell:** `PRF-inv-5` (IAM half)
**Run-ahead authorization:** `2.0.0_SA_COO` 66725 item 4 — AC5 may run before the start condition
(read-only simulate, no emission dependency, every later cell rests on its result).
**Measured:** 2026-08-24, this session. **Repo HEAD at measurement:** `f696acb8f8`.

---

## The principal, and why it is this one

`PRF-inv-5` names "the runner/publisher role for 49F". Resolved by reading the chain's own
Terraform rather than assuming:

`infra/aws/terraform/opal-assets/advi_49f_floor.tf:44-46` states it in the file's own header —
*"the CHAIN's data-plane surface (B1-B7) is NOT here — it landed on **bd-exporter-ec2-role** in
bd-pipeline/iam.tf (advi-49f-chain-access, ledger 20260819T1314Z). This file carries only the
floor's OWN plumbing."*

The floor's own roles are **not** the data-plane principal:
`advi-49f-floor-scheduler-role` holds InvokeFunction + DLQ SendMessage only, and
`advi-49f-gold-dispatch-role` holds ec2:StartInstances / Describe / SSM on one instance id
(`i-01003b035d2988dfb`, `bd-gold-layer-runner`) plus its own log group. Neither writes S3.

**Principal under test:** `arn:aws:iam::313476888478:role/bd-exporter-ec2-role`
(live `get-role`, created 2026-01-09T00:41:34Z).

---

## Instrument hygiene — the three false-deny modes, each closed BEFORE the verdicts

CLAUDE.md Rule 22a names three ways `simulate-principal-policy` returns a false deny. Each was
closed explicitly, not assumed away.

**Mode 1 — 2+ `--resource-arns` in one call flips held ones to `implicitDeny`.**
CLOSED: every simulate below is **one `--resource-arns`, one action, its own invocation**. The
positive control is a **separate invocation** from every negative — a positive control run in the
same call as the target is disarmed by this exact mode.

**Mode 2 — an unset `--context-entries` makes a conditioned statement evaluate as a deny that is
byte-identical to a real one.**
CLOSED BY CENSUS, not by assumption. All **15** inline policies on the role were read and every
statement inspected for a `Condition` block. **9 conditioned statements exist**; every one of them
keys on **`s3:prefix`**, which applies to `ListBucket` only, and every one is an **Allow**. The
sole statement that can grant `s3:PutObject` on the twin prefix — `advi-49f-publisher-platinum-put`
/ Sid `AdviPublisherScopedPut` — carries **no Condition**, and the sole S3 Deny —
`cross-firm-bucket-deny` / Sid `DenyCrossFirmCotBucket` — carries **no Condition**. So no unset
context entry can manufacture a false deny *for a PutObject test on these ARNs*.
⚠ **Scope of that clearance:** it holds for `s3:PutObject`. A future **`s3:ListBucket`** test on
this role **will** need `--context-entries s3:prefix=...`, because those nine statements are
exactly the ones that would then be in play. Recorded so the clearance is not carried across
actions it does not cover.

**Mode 3 — a NONEXISTENT action name also returns `implicitDeny`, so a typo is indistinguishable
from a missing grant.**
CLOSED ON THE DISCRIMINATING ORACLE, and never on simulate. `aws accessanalyzer validate-policy`,
run in **two isolated invocations**:

| policy document | findings | verdict |
|---|---|---|
| `s3:PutObject` (the action under test) | **0** | action name is REAL |
| `s3:ZzzNoSuchActionName9999` (planted mutant) | **1** | `ERROR INVALID_ACTION — The action s3:ZzzNoSuchActionName9999 does not exist.` |

The mutant **FIRED**. The oracle discriminates; a clean result on the real action is therefore
evidence and not a brick.

---

## The four verdicts — one resource per call, each its own invocation

Action `s3:PutObject` throughout. Principal `bd-exporter-ec2-role`.

| # | resource ARN (exactly one per call) | decision | matched statements |
|---|---|---|---|
| **1 — POSITIVE CONTROL** | `arn:aws:s3:::opal-data-portal-v2/platinum/advi/49financial/leaderboard.json` | **allowed** | 1 — `role_bd-exporter-ec2-role_advi-49f-publisher-platinum-put` |
| **2 — cross-firm cot** | `arn:aws:s3:::opal-data-cot/gold/canonical/role_aua/2026-08-21.parquet` | **explicitDeny** | 1 — `role_bd-exporter-ec2-role_cross-firm-bucket-deny` |
| **3 — cross-firm inf** | `arn:aws:s3:::opal-data-inf/platinum/firm/header_metrics.json` | **implicitDeny** | **0** |
| **4 — scoping control** | `arn:aws:s3:::opal-data-portal-v2/platinum/mdpf/model_portfolios.json` | **implicitDeny** | **0** |

**The instrument discriminates.** It returned three different answers across four inputs, and each
verdict names the statement that produced it (or names none). This is not an undiscriminating tool
agreeing with itself.

**Test 4 is the one the criterion did not ask for and is worth keeping.** Same bucket, one prefix
over, zero matched statements: **at the measurement instant below, the publisher grant evaluated as
prefix-scoped rather than bucket-wide.** On that evidence the "one producer per served key" boundary
was real *at IAM* and not merely by convention in the publisher — which matters because `publish_one`
also hard-asserts the prefix in code (`d_publisher_port.py:422`), and two independent belts is the
correct posture for a served key.

⛔ **VINTAGE — AND THE REPO HEAD ABOVE DOES NOT VINTAGE THE CLAIMS ON THIS PAGE THAT MATTER MOST.**
Every IAM verdict here is a fact about the **AWS account**, not about the repo. There is no ref that
pins a policy: a `get-role-policy` result can change with nobody editing this file, this TO, or any
commit. So the four decisions, the "prefix-scoped" reading, and the "both grants exist in Terraform"
line are **MEASUREMENTS TAKEN AT 2026-08-24 (this session), NOT STANDING PROPERTIES OF THE ROLE.**
They are stated in the past tense deliberately. **Anyone relying on them re-runs the reproduction
block at the bottom rather than citing this page** — that is one command per claim and it is the only
thing that makes them current.
*Recorded because this page is re-derived by CVO under s.14(c), and an evidence artifact that reads as
a standing property is the "moment encoded as a mechanism" class landing on the exact document a
verifier trusts. Found by applying that class's own discriminator to my own artifact: could this
change without anyone editing the sentence that asserts it? For every IAM line here, yes.*

---

## ⛔ TWO DELTAS AGAINST MY OWN ACCEPTANCE CRITERION — both measured, neither adjudicated here

**Delta 1 — the criterion understates the cot posture.** AC5 as written expects
*"cot-key simulate → implicitDeny"*. The measured decision is **`explicitDeny`**, and the
difference is not cosmetic:

- **`implicitDeny`** = *no statement grants this*. One later `Allow` anywhere on the role silently
  permits it, and nothing flags the change.
- **`explicitDeny`** = *a statement forbids this*. An explicit Deny **cannot be overridden** by any
  Allow, at any time, from any policy.

So the cot pin is **stronger than the criterion claims**. A reviewer checking AC5 literally would
read `explicitDeny != implicitDeny` and could record a FAIL on a control that is in fact
**better** than specified. Reported so the criterion's wording, not the estate's posture, is what
gets corrected.

**Delta 2 — `cot` and `inf` are named together in the cell and they do not behave alike.**
`PRF-inv-5` says *"DENIED on a cot/inf key"*, one phrase covering both. Measured, they are on
different footings:

- **cot → `explicitDeny`**, matched `cross-firm-bucket-deny`. A hard pin.
- **inf → `implicitDeny`, 0 matched statements.** There is **no Deny belt for `opal-data-inf` on
  this role**. Nothing grants it today, so the behaviour is correct *today*; but it rests on
  **absence of grant**, not on a prohibition.

This is confirmed on the **DESIRED** plane too, so it is a design asymmetry and not live drift:
`comp-iam role bd-exporter-ec2-role` parses **33 statements**, of which **exactly one is a Deny** —
Statement 18, `s3:*` on `arn:aws:s3:::opal-data-cot` + `/*`. There is no inf counterpart in
Terraform either.

**Why it is worth a line rather than a shrug:** CLAUDE.md NEVER#2 reads *"NEVER reference another
firm's bucket from a pipeline tree (bd↔cot↔inf) — gate-blocked at commit **and IAM Deny at
runtime**."* On this role the "IAM Deny at runtime" half is true for **cot** and is **not** true
for **inf** — inf is held by the commit gate and by there being no grant, which are real controls,
but they are not the one the law names. Whether that gap should be closed by adding an inf Deny
belt is an IAM change and a law question. **I have changed nothing and am not proposing an edit
here** — surfaced to COO/CVO, action theirs.

---

## Grounding, per Rule 22a — all three planes, none substituting for another

| plane | evidence |
|---|---|
| **DESIRED** (Terraform) | `comp-iam role bd-exporter-ec2-role` — Statement 32 `Allow s3:PutObject` on `arn:aws:s3:::opal-data-portal-v2/platinum/advi/49financial/*`; Statement 18 `Deny s3:*` on `opal-data-cot`(+`/*`). Both grants **exist in code** — this is **not** the live-grant-with-no-Terraform class (MSTR spawn brief; a grant absent from TF is a deletion scheduled for the next apply of that root). |
| **APPLIED** (live primitive) | `aws iam get-role-policy` on both policies, read in full and quoted above; `aws iam list-role-policies` = 15 inline (materialized, not `--query length`); `list-attached-role-policies` = 2 managed. |
| **EXERCISED** | the four `simulate-principal-policy` invocations above + the two `validate-policy` invocations, each isolated. |

**comp-iam's own disclosure is recorded rather than swallowed**, because it bears directly on why
the live primitive was required: its header prints
*"DENY-OVERLAY INCOMPLETE: 2 deny statement(s) unparsed (`for_each` — `role = each.value` not
resolved) … Among these are the cross-firm Deny belts. Asking this tool about a Deny it never
parsed returns SILENCE, and silence must not be read as allowed."*
It also reports **24 policy blocks NOT ATTACHED** — statements it has never seen. The cot Deny
*was* visible in this role's parse (Statement 18), but that is a fact I measured, not one the tool
guaranteed. **The `explicitDeny` verdict is the live simulate's, not comp-iam's.**

## Determinism

Two same-input runs of test 2, compared: `explicitDeny` / matched
`role_bd-exporter-ec2-role_cross-firm-bucket-deny` on both. **STABLE.**

## What this evidence does NOT establish

- It does **not** prove the publisher can write a **new** PERFRP key. The positive control used
  `leaderboard.json`, an **existing** twin. New leaf names are covered by the grant's `/*` wildcard
  on the same prefix, but that is an inference from the policy text and it becomes an
  **AC2** measurement once DS names the leaves — one simulate per new key, positive control in a
  separate invocation. Not claimed here.
- It does **not** exercise a real `PutObject`. A simulate is an authorization evaluation, not a
  write; AC1's D5 exercise is where a byte actually moves.
- It says nothing about `s3:ListBucket` (see Mode 2 scope note) or about any principal other than
  `bd-exporter-ec2-role`.

## Reproduction

```bash
ROLE=arn:aws:iam::313476888478:role/bd-exporter-ec2-role
# each of these is its OWN invocation, ONE --resource-arns:
aws iam simulate-principal-policy --policy-source-arn "$ROLE" --action-names s3:PutObject \
  --resource-arns arn:aws:s3:::opal-data-portal-v2/platinum/advi/49financial/leaderboard.json
aws iam simulate-principal-policy --policy-source-arn "$ROLE" --action-names s3:PutObject \
  --resource-arns arn:aws:s3:::opal-data-cot/gold/canonical/role_aua/2026-08-21.parquet
aws iam simulate-principal-policy --policy-source-arn "$ROLE" --action-names s3:PutObject \
  --resource-arns arn:aws:s3:::opal-data-inf/platinum/firm/header_metrics.json
aws iam simulate-principal-policy --policy-source-arn "$ROLE" --action-names s3:PutObject \
  --resource-arns arn:aws:s3:::opal-data-portal-v2/platinum/mdpf/model_portfolios.json
# action-name validity -- NEVER via simulate:
aws accessanalyzer validate-policy --policy-type IDENTITY_POLICY --policy-document file://<doc>
```

**VERDICT: AC5 PASS**, with the cot decision **stronger** than the criterion states and the
`cot`/`inf` asymmetry surfaced as a separate finding.
