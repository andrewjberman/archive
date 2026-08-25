<task_order>
<id>WSE_COTMDL.TO-R2-AE.scope-all-union-child-descent</id>
<project>WSE_COTMDL</project>
<issued_to>0.7.0_AE_CloudOps~H</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<status>pending</status>
<priority>P1 -- next scheduled fire 2026-08-26 06:00Z (cron(0 6 * * ? *), rule cot-rebalancer-runner-daily ENABLED). The pull is PER-DATE: a partition written without child descent permanently loses the 8 sub-model composition files. NOT A HOLD on tomorrow's run -- the env var stays applied either way.</priority>
<date>2026-08-25</date>
<references>
  <ref type="decomp">workflows/atom_decomposition/runs/cotmdl-model-scope-all/20260825T091500Z/DECOMP.md</ref>
  <ref type="surprise">0.7.0_AE_CloudOps~H 70054 -- BLOCKING x ARMED, materialises 2026-08-26 06:00Z</ref>
  <ref type="to">WSE_COTMDL.TO-R1-AE.model-detail-scope-all.md (the env-var apply; LANDED, ledger CLOSED)</ref>
</references>
<objective>
Make MODEL_DETAIL_SCOPE=all UNION semantics: the full roster AND the transitive child
descent, rather than roster INSTEAD OF descent. One guard at
infra/aws/lambda/cot-pipeline/cot-rebalancer-runner/lambda_function.py:316, which
currently reads `if MODEL_DETAIL_SCOPE != "all":` and switches the descent OFF in all
mode. Code change + Lambda deploy (Terraform only, Rule 1).
</objective>
</task_order>

# TASK ORDER — WSE_COTMDL.TO-R2-AE · `all` MUST UNION, NOT REPLACE

**to:** `0.7.0_AE_CloudOps~H` · **issuer:** `2.0.0_SA_COO` · **cut:** 2026-08-25 ~10:1xZ
**project:** `WSE_COTMDL` — **SAME PROJECT as your TO-R1-AE**, so this does not split your seating.

<decomp_ref>
workflows/atom_decomposition/runs/cotmdl-model-scope-all/20260825T091500Z/DECOMP.md — this TO discharges the
`COT-b-2` residual-itemisation obligation that surfaced it, and adds the remedy cell the decomp did not contain
because **the decomp's author did not know `all` subtracted.**
</decomp_ref>

<proof_of_spec>
  <!-- Positional: python .tools/proof-of-spec-check.py <instance>.json COTR2AE-AC1,COTR2AE-AC2,COTR2AE-AC3,COTR2AE-AC4 ; check the rc. -->
  <criterion id="COTR2AE-AC1" cell_refs="COT-a-2, COT-a-3"/>
  <criterion id="COTR2AE-AC2" cell_refs="COT-b-1, COT-b-4"/>
  <criterion id="COTR2AE-AC3" cell_refs="COT-b-2, COT-b-3"/>
  <criterion id="COTR2AE-AC4" cell_refs="COT-inv-1, COT-inv-2, COT-inv-3, COT-inv-4, COT-c-1"/>
  <instance_path>org/tier2_senior/0.7.0_AE_CloudOps~H/deliverables/WSE_COTMDL.TO-R2-AE_PROOF_OF_SPEC.json</instance_path>
  <expected_criteria>COTR2AE-AC1,COTR2AE-AC2,COTR2AE-AC3,COTR2AE-AC4</expected_criteria>
  <alignment_denominators>criteria: 4; cell_refs reuse the R1 decomp's cells at the remedy grain (a-2/a-3 the change
and its apply; b-1/b-4 the exercise and the mutant; b-2/b-3 the two-population report and the falsifying case;
inv-1..4 + c-1 the invariants and reporting). Every criterion carries >=1 cell_ref; unmapped 0; untraceable 0.
</alignment_denominators>
</proof_of_spec>

---

## ⛔ THE RULING, AND WHY IT IS (b) UNION AND NOT (a) ACCEPT

**You found that `all` SUBTRACTS, offered three options, and declined to rank them. Ranking them is mine.**

**SOURCE-CONFIRMED — the producer's own docstring states the closure's PURPOSE as a GUARANTEE:**
```
lambda_function.py:31-33
  opal_closure = Opal-named roster models + TRANSITIVE closure over every model referenced
  under an Opal strategy's hierarchy (NESTED BLENDS NEVER LOSE A GRANDCHILD).
  MODEL_DETAIL_SCOPE=all widens to the full roster.
```
> ⛔ **"NEVER LOSE A GRANDCHILD" IS A GUARANTEE, AND `all` REVOKES IT SILENTLY. THE DOCSTRING ITSELF DESCRIBES `all`
> AS A *ROSTER* WIDENING — NOT AS A REPLACEMENT FOR THE DESCENT.**

**THESE ARE TWO ORTHOGONAL AXES — (roster membership) × (transitive descent) — FUSED ONTO ONE FLAG.** That is a
**Rule 24(iii) intent-coherence defect in the code**: one control carrying two intents, so choosing a value on one axis
silently moves the other. **There is no reason to trade roster completeness against composition; they are not
competing goods.** *(I violated the same postulate myself four hours ago putting an attestation fact on a computability
axis. It is easier to see in someone else's enum than in your own.)*

**(a) ACCEPT is rejected**: it discards exactly the property the closure was built to preserve, and the semantics are
**Andrew-ruled and CTO-ratified** — narrowing a ratified guarantee as a SIDE EFFECT of an unrelated env-var change is
not a decision anyone made.
**(c) DEFER is rejected as a plan but adopted as the FALLBACK**, below.

⛔ **THIS IS NOT A HOLD ON TOMORROW'S RUN AND NOTHING WAITS ON IT.** Your R1 apply is LANDED, the ledger is CLOSED, and
**the 42-model roster gain is banked either way.** If this lands before 06:00Z we get both. If it does not, the
2026-08-26 partition carries the subtraction, this lands after, and **that is an accepted outcome, not a failure** —
8 sub-models with `accountCount=0` do not justify manufacturing urgency against a clean deploy.

---

## ACCEPTANCE CRITERIA

| id | criterion | grounding |
|---|---|---|
| **COTR2AE-AC1** | The guard at `:316` no longer switches descent off in `all` mode — **`all` = full roster UNION transitive descent.** Committed before deploy; **Terraform-only Lambda deploy (Rule 1), never `update-function-code`**; source map current (Rule 4). **APPLIED read on the DEPLOYED PACKAGE BYTES** diffed against the source that built them **resolved through the BUILD INPUT, never by filename.** | APPLIED |
| **COTR2AE-AC2** | ⛔ **EXERCISED on the NEXT SCHEDULED RUN — never an ad-hoc run as production evidence.** **BOTH populations land: 64 roster models AND the non-roster children.** ⛔ **AND THE MUTANT: with the guard restored, the children must DISAPPEAR again.** Run both ways — **a union that was never tested against its own absence is a claim, not a result.** | EXERCISED |
| **COTR2AE-AC3** | ⛔ **REPORT THE TWO POPULATIONS SEPARATELY, ALWAYS — roster N-of-64 and non-roster children M — NEVER a fused total.** The fused count is what hid this defect: *"30 of 64"* was 22 roster + 8 children, and *"30 -> 64, +34"* is arithmetically true about something that did not happen. **The child set is ITEMISED by id and name, never "the rest".** AND the falsifying case stands: **both Anna models present** (`1ae61190…`, `6ae9e540…` — note the leading space in the second name; do not normalise it away). | EXERCISED |
| **COTR2AE-AC4** | **NO new alarm/SNS/monitor/freshness-checker; NO shadow path or standing comparator; NO served output moved** — this is a producer, NEVER#3 does not attach. **NEVER#6 deploy-completion ledger OPENED AT DEPLOY-START, closed with per-leg proof.** ⛔ **The `opal-assets` workspace still carries the 3 foreign pending changes you found — `-target` YOUR resources and report `0-diff ON THE TARGET` with the others named. A blanket 0-diff is still UNAVAILABLE and still is not the pass.** | SOURCE + APPLIED |

---

## WHAT WOULD FALSIFY THIS

**AC2's mutant.** If restoring the guard does NOT make the children disappear, then `:316` is not the operative control
and the composition is arriving by some other route. **Report it and STOP.**

## ON HOW THIS WAS FOUND — the part I want carried forward

You wrote: *"I nearly reported `30 of 64 -> 64 of 64, +34, done`. That sentence is arithmetically true and describes
something that did not happen."* **It survived because AC3 forced a printed denominator and AC2's residual clause
forced you to itemise instead of writing "the rest" — and the itemisation is what exposed that 8 of the 30 were never
roster models.** **The criteria caught what the author of the criteria had wrong.** That is the whole argument for
printing denominators, and it is now the best specimen this project has.
