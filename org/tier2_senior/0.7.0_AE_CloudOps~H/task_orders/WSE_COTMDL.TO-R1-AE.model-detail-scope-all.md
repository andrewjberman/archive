# TASK ORDER — WSE_COTMDL.TO-R1-AE · MODEL_DETAIL_SCOPE -> "all"

**to:** `0.7.0_AE_CloudOps~H` · **issuer:** `2.0.0_SA_COO` · **cut:** 2026-08-25 ~09:15Z
**project:** `WSE_COTMDL` · **ONE PROJECT, ONE INSTANCE** (Andrew-direct 2026-08-24 seating rule)
**authorization:** `1.0.0_SA_CTO` ~06:0xZ — forward-only, already-implemented branch.

⛔ **NOT IN THIS TO — READ BEFORE `list_task_orders`.** `WSE_COTMDL.WS5.iam-infra-scoped-role-eventbridge.md` is a
**DIFFERENT SCOPE** (scoped IAM role + EventBridge) that shares this project code and **is NOT your assignment.**
`list_task_orders` **NEVER VALIDATES THE LANE SUFFIX** — a fabricated lane returns the base serial's identical **25
pending TOs**, while a fabricated *base* correctly returns "not found" (control pair, `0.0.0_AB_MSTR` 69893). **There
is no query that returns only your lane.** **If you are building an IAM role, you are on the wrong task order.**
**THIS TO IS YOUR ASSIGNMENT IN FULL: the `MODEL_DETAIL_SCOPE` env-var apply, forward-only, and nothing else.**

<decomp_ref>
workflows/atom_decomposition/runs/cotmdl-model-scope-all/20260825T091500Z/DECOMP.md — cells
COT-a-1, COT-a-2, COT-a-3, COT-a-4, COT-b-1, COT-b-2, COT-b-3, COT-b-4, COT-c-1,
COT-inv-1, COT-inv-2, COT-inv-3, COT-inv-4
</decomp_ref>

<decomp_context>
`COT-e-1` — the 08-21 backfill — is **EXCLUDED BY DETERMINATION** and is NOT in this TO. This change is FORWARD-ONLY.
Whether current Opal-membership may be applied to the 08-21 canonical date, or 08-21 needs a re-pull at `all` scope,
is **AN OPEN CALL AT ANDREW** and a separately authorized act. Rule 24(iv): it does not move on this apply.
</decomp_context>

<proof_of_spec>
  <!-- Positional: python .tools/proof-of-spec-check.py <instance>.json COTR1AE-AC1,COTR1AE-AC2,COTR1AE-AC3,COTR1AE-AC4,COTR1AE-AC5,COTR1AE-AC6 ; check the rc. -->
  <criterion id="COTR1AE-AC1" cell_refs="COT-a-1"/>
  <criterion id="COTR1AE-AC2" cell_refs="COT-a-2, COT-a-3, COT-a-4"/>
  <criterion id="COTR1AE-AC3" cell_refs="COT-b-1, COT-b-2"/>
  <criterion id="COTR1AE-AC4" cell_refs="COT-b-3, COT-b-4"/>
  <criterion id="COTR1AE-AC5" cell_refs="COT-inv-1, COT-inv-2, COT-inv-3"/>
  <criterion id="COTR1AE-AC6" cell_refs="COT-inv-4, COT-c-1"/>
  <instance_path>org/tier2_senior/0.7.0_AE_CloudOps~H/deliverables/WSE_COTMDL.TO-R1-AE_PROOF_OF_SPEC.json</instance_path>
  <expected_criteria>COTR1AE-AC1,COTR1AE-AC2,COTR1AE-AC3,COTR1AE-AC4,COTR1AE-AC5,COTR1AE-AC6</expected_criteria>
  <alignment_denominators>cells in this TO: 13 (a 4 · b 4 · c 1 · inv 4); criteria: 6; every criterion carries >=1
cell_ref; every one of the 13 cells is reachable from >=1 criterion. Unmapped cells 0; untraceable criteria 0.
Decomp total 14; surface (e) = 1, excluded by determination and named in decomp_context so the difference is visible.
</alignment_denominators>
</proof_of_spec>

---

## WHY THIS IS THE PRIORITY, IN HIS WORDS

**Andrew-direct 2026-08-25 ~08:5xZ, VERBATIM:** *"I'm fine with it on PROD, let's just get the data part sorted."*
He released the BRANCH half of his PERFRP condition and **kept the DATA half**. `1.0.0_SA_CTO` measured that the data
part is **blocked on a SEAT, not a decision** — no AE-class lane was free, and this TO exists so that the moment one
is, the work has an acceptance surface waiting rather than a briefing.

⛔ **THE PUBLISH GATE IS UNTOUCHED BY THIS TO.** Nothing here publishes, and zero PERFRP leaves served remains correct.

---

## THE MECHANISM, SOURCE-CONFIRMED @f26f4668d8 — DO NOT RE-DERIVE IT

```
infra/aws/terraform/opal-assets/cot_rebalancer_runner.tf:154   MODEL_DETAIL_SCOPE = "opal_closure"
infra/aws/lambda/cot-pipeline/cot-rebalancer-runner/lambda_function.py:70   default "opal_closure"
                                                            :300  if MODEL_DETAIL_SCOPE == "all":  <- IMPLEMENTED
                                                            :393  manifest emits rebalancer_model_detail {count, scope}
```
**ONE TERRAFORM LINE. NOT A CODE CHANGE.** The `all` branch exists and is tested.

**WHY THE CLOSURE SCOPE IS STRUCTURALLY WRONG, not merely narrow:** the walk seeds on `_is_opal(name)` and descends
into children of models already pulled — **a model whose NAME is not Opal-ish but which HOLDS an Opal constituent is
undiscoverable by construction.** Measured: **30 of 64** roster models; both Anna accounts (**$46,436,739.80**) missing.

⛔ **THE PULL IS PER-DATE. Every day at `opal_closure` writes a partition permanently carrying 30 of 64.**

---

## ACCEPTANCE CRITERIA

| id | criterion | cells | grounding |
|---|---|---|---|
| **COTR1AE-AC1** | **MEASURED BEFORE, denominators printed:** the TF literal at a NAMED REF · the **APPLIED** env from `aws lambda get-function-configuration` (desired is not applied) · `rebalancer_model_detail.{count,scope}` from the most recent emitted manifest. **A before-number is what makes the after-number a finding.** | `COT-a-1` | MEASURED |
| **COTR1AE-AC2** | TF `:154` -> `"all"`, **committed before apply** (Rule 2). ⛔ **`.tools/safe-apply.sh` — NEVER bare `terraform apply`; Rule 26 puts the apply on THIS device, run by the seat that built it.** Plan read before. ⛔ **AMENDED ~09:5xZ ON `0.7.0_AE_CloudOps~H`'s SURPRISE (69998): THE POST-APPLY RE-PLAN IS `0-DIFF ON THE TARGETED RESOURCE`, WITH THE NON-MINE PENDING CHANGES NAMED AND COUNTED — NOT A BLANKET 0-DIFF.** The `opal-assets` workspace carries **3 committed-but-unapplied changes belonging to other lanes** (49F/TAXSMA IAM; an MDPF grant + producer prefix repoint, a matched pair). **Apply `-target=module.cot_rebalancer_runner.aws_lambda_function.this` — your one resource, nothing else.** A blanket 0-diff is UNAVAILABLE here and demanding one would force either a false report or a failed criterion on a seat doing the right thing. **Report `0 to add, 3 to change` with the three named; that IS the passing form.** *Do not apply or revert another lane's pending change in either direction.* ⛔ **RESOLVE the terraform binary — `.tools/terraform.exe` does NOT exist on every device.** Then the **APPLIED** read shows `MODEL_DETAIL_SCOPE=all` on the live function. | `COT-a-2/3/4` | APPLIED |
| **COTR1AE-AC3** | ⛔ **EXERCISED ON THE NEXT *SCHEDULED* RUN — an ad-hoc run is a QA instrument and NEVER production evidence.** Manifest `scope == "all"` AND `count` **>** the AC1 before-count, **reported WITH its denominator (64 roster models) and the delta named.** A bare count is not a result; a residual below 64 is **itemised**, never left as "the rest". | `COT-b-1/2` | EXERCISED |
| **COTR1AE-AC4** | ⛔ **THE FALSIFYING CASE AND THE MUTANT, BOTH.** The two Anna accounts' models are PRESENT — they are why the defect was found, and their absence falsifies the fix whatever the count says. AND a **MUTANT run forced back to `opal_closure` produces the LOWER count** — run BOTH ways. **An after-number with no before and no mutant is consistent with the env var having done nothing.** | `COT-b-3/4` | EXERCISED |
| **COTR1AE-AC5** | ⛔ **NO alert / alarm / SNS / SES / notification / freshness-checker / monitor** (standing moratorium). **NO shadow path, NO parallel emitter, NO standing comparator** (complete veto — build correctly once and port; an ad-hoc QA read is run-and-read, nothing standing). **NO served output moved — NEVER#3 does not attach to a producer env var**, stated positively so it is not re-derived under time pressure. | `COT-inv-1/2/3` | SOURCE |
| **COTR1AE-AC6** | ⛔ **NEVER#6: a deploy-completion ledger entry OPENED AT DEPLOY-START and CLOSED with per-leg proof** (`.tools/deploy_ledger.py`). *An entry opened and never written back reads identically to a stranded deploy — measured on the ETFS promote this same morning.* Every claim at a NAMED REF; timestamps from an offset-bearing formatter (`%aI` / `s3api` UTC), **never a typed `Z`**. | `COT-inv-4`, `COT-c-1` | SOURCE + APPLIED |

---

## WHAT WOULD FALSIFY THE WHOLE THING

**AC4's mutant.** If the mutant produces the SAME count, `MODEL_DETAIL_SCOPE` is not the operative control and the
30-of-64 has another cause. **That is a FINDING, not a failure — report it and STOP. Do not go looking for a second
knob to turn until the first is understood.**

## SURPRISE CHANNEL (Rule 27)

Mid-round the spec is FROZEN. The only legal off-spec act is to SURFACE a surprise: one line by MCP to
`3.0.0_SA_CVO`, cc the issuer. **Executing seats do not write `org/surprise_channel/**` — CVO files it.**
OBSERVATION never interrupts; BLOCKING routes same-turn to me for spec amendment; **any ARMED item disarms SAME-TURN
via a named owner, and DISARMED IS NOT REMEDIATED.**
