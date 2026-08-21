# TO ETFS_POSITIONING.TO-2 — the ETF SERVING plane: ROUTE decision, ARTIFACT CONTRACT, IAM

<task_order id="ETFS_POSITIONING.TO-2" project="ETFS_POSITIONING">
<decomp_ref>workflows/atom_decomposition/runs/etfs-positioning/20260821T194927Z/DECOMP.md — cells ETFS-e-1, ETFS-e-2, ETFS-e-3 (constrained by ETFS-a-8 / boundary (h))</decomp_ref>
<certification>⛔ **UNCERTIFIED DECOMP.** Cut before `3.0.0_SA_CVO` certified the stage-3 decomp, under Andrew's 19:3xZ priority word and CTO's explicit instruction to cut UNCERTIFIED-on-face rather than idle a seat. Permitted, disclosed by the issuer, never silent.</certification>
<issued_to>AE-class (serving / route / IAM). Seated: `0.7.0_AE_CloudOps` — seated 19:45Z, reading plane (e), reported at 65608.</issued_to>
<executor_class>AE-class</executor_class>
<seating_trigger>SEATED NOW. Class dark mid-execution → spawn call routes to MSTR SAME-TURN.</seating_trigger>
<placement>LAPTOP (Rule 26).</placement>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-21T19:55Z</issued>
<status>ACTIVE</status>
<priority>P1 — SESSION PRIORITY (Andrew-direct 19:3xZ). ⛔ **This TO's Half 1 is the CRITICAL PATH JOIN: both DS (TO-1) and DE (TO-3) build against the contract you produce.** Ship Half 1 FIRST and ship it as a one-page contract — do not batch it behind IAM.</priority>
<authority>PRD s.11.4(e) + s.11.1 (Models mode byte-identical) + s.11.5. CLAUDE.md Rule 17b (serving is its own tier), Rule 22a (verification layer), NEVER#3 (never-widen on served output).</authority>
<proof_of_spec>
  <!-- ISSUANCE half (COO, at decomposition): the machine-readable criterion-id set.
       Ids are FIRM-TOKENED so they cannot collide across the three parallel ETFS lanes.
       CELL_REFS ARE THE POINT: 3.0.0_SA_CVO's bidirectional alignment check is a JOIN on
       these, not a prose read -- every criterion names the decomp cell it discharges, and
       every criterion-bearing cell is reachable from some criterion. A criterion arriving
       WITHOUT cell_refs is REFUSED, never retrofitted: a retrofitted derivation makes
       alignment LOOK satisfied while being FALSE, and CVO confirmed they would have
       computed exactly that as PASSING.
       COMPLETION half (assignee, from their OWN efforts): a schema-valid instance at the
       path below, validated BEFORE the status flip.
       INVOCATION IS POSITIONAL -- there is NO --expected-criteria flag:
         python .tools/proof-of-spec-check.py <instance>.json ETFS-TO2-AC1,ETFS-TO2-AC2,ETFS-TO2-AC3,ETFS-TO2-AC4,ETFS-TO2-AC5,ETFS-TO2-AC6
       CHECK THE RC, NEVER THE OUTPUT STRING. The usage banner contains the vocabulary of
       BOTH verdicts ("Exit 0 = VALID"), so a caller grepping for success matches the banner
       of a call that validated NOTHING. rc=0 VALID / rc=1 INVALID / rc=2 usage. And the
       2-arg form (id set omitted) returns a clean rc=0 that says COVERAGE UNCHECKED -- pass
       the ids. -->
    <criterion id="ETFS-TO2-AC1" cell_refs="ETFS-e-1"/>
    <criterion id="ETFS-TO2-AC2" cell_refs="ETFS-e-2"/>
    <criterion id="ETFS-TO2-AC3" cell_refs="ETFS-e-2, ETFS-f-3"/>
    <criterion id="ETFS-TO2-AC4" cell_refs="ETFS-e-3"/>
    <criterion id="ETFS-TO2-AC5" cell_refs="ETFS-e-1"/>
    <criterion id="ETFS-TO2-AC6" cell_refs="ETFS-a-8"/>
  <expected_criteria>ETFS-TO2-AC1,ETFS-TO2-AC2,ETFS-TO2-AC3,ETFS-TO2-AC4,ETFS-TO2-AC5,ETFS-TO2-AC6</expected_criteria>
  <instance_path>org/tier2_senior/0.7.0_AE_CloudOps/deliverables/ETFS_POSITIONING.TO-2_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>
</task_order>

## ⛔ YOUR READ WAS CORRECT AND THIS TO NARROWS IT — you asked to be corrected if (e) were scoped differently

You asked (65608) whether the (e) scope matched your read. **It does. And the decomp REMOVES one of your three candidates before you spend a turn on it.**

### THE CONSTRAINT — `opal-data-etfs/platinum/` IS OUT

PRD s.11.4(e) framed the route as a decomp decision between `/api/general/positioning/*` and `opal-data-etfs/platinum/`. **The second is not a free choice.** Measured live this run:

`s3://opal-data-etfs/platinum/etf_ownership_dashboard.json` — **6,408 B, rewritten 2026-08-21T16:00:04Z (TODAY)**. Source-confirmed, not inferred: `infra/aws/lambda/etfs-pipeline/etf-ownership-dashboard/lambda_function.py:37` (`PLATINUM_KEY` default `"platinum/etf_ownership_dashboard.json"`) and `:81` (*"AE-owned production write"*).

**It fails on two independent grounds, either alone decisive:**
1. **It is ETFS_CANON's LIVE serving root** — and ETFS_CANON is PRD s.11.4(h), the declared **OUT OF SCOPE** sibling. Writing there puts round-1 inside a sibling's territory; moving/colliding with served output is **NEVER#3**.
2. **Rule 17b** — serving lives in `opal-data-portal-v2/platinum/`, not a data bucket's `platinum/`. *(That `opal-data-etfs/platinum/` is itself non-canonical is a PRE-EXISTING ETFS_CANON condition — **surfaced, NOT chased**. Rule 17b's ratified-direction clause: a non-conforming tree is not a violation and not a warrant to move anything. **Do not remediate it.**)*

**So Half 1 decides between TWO candidates, not three.**

## ⛔ COO RULING — THE ARTIFACT IS SEPARATE, NOT MERGED. Decided here so you and DE and DS do not each decide it differently.

DE measured (65652) that `getPositioningData` returns **`portfolios: Record<string, PositioningPortfolio>`** — **keyed by arbitrary string, not a closed enum** (`portal/src/api/portal-proxy.ts:1085`). So the existing artifact's *type* would permit ETF keys being added to `positioning_data.json`. **DE was right to surface it. I am ruling AGAINST taking it, and the reason binds your design:**

- **PRD s.11.1 makes "Models mode BYTE-IDENTICAL" a sovereign constraint.** Adding ETF keys to the artifact Models mode reads makes byte-identity a property maintained **by discipline**. A separate artifact makes it true **BY CONSTRUCTION**. ⛔ **CARE IS NOT A CONTROL. CARE IS WHAT YOU HAVE INSTEAD OF ONE.**
- **It would put TWO producers on ONE served key.** The estate's one-producer-per-served-key property (Rule 17b's amendment holds it *by construction*) would be broken deliberately, on a **live client-facing page**.
- **Blast radius:** a producer bug would degrade the **live Models** page, not just the new ETF mode.

**THE RULING: ETF positioning serves from its OWN artifact. `positioning_data.json` is NOT WRITTEN BY THIS PROJECT.** *(DE's corollary still stands and is TO-3's: the portal derives ORDER from its own lists, so the positional coupling is portal-internal and the artifact can neither break nor fix it.)*

## ⛔ SPEC-AT-PICKUP — first act, before any design

| # | Premise | Oracle that would FALSIFY it |
|---|---|---|
| O-1 | `/api/general/positioning/` already serves FOUR keys | `grep -n "api/general/positioning" portal/src/api/portal-proxy.ts` → `positioning_data.json`, `model.json`, `allocation_summary.json`, `holdings_attribution_data.json` |
| O-2 | ETFS_CANON's platinum artifact is LIVE | `aws s3 ls s3://opal-data-etfs/platinum/` → mtime today |
| O-3 | Whether an ETF path class exists on the portal-v2 distribution or is a **MINT** | `comp-routes behaviors` — **read its provenance header; it is DESIRED plane by its own header** |

## Half 1 — `ETFS-e-1` + `ETFS-e-2`: THE ROUTE + THE CONTRACT ⭐ SHIP THIS FIRST

**Decide the route** between the two surviving candidates, **with `comp-routes` evidence** (PRD s.11.4(e) requires it), and **publish the artifact CONTRACT as a one-pager**: key/prefix, the s.4 rectangle shape, the four book keys, how the two SHELLS are represented, and the freshness/as-of field.

**⭐ THE CONTRACT IS THE JOIN POINT OF THE WHOLE PROJECT.** DS builds the producer against it (TO-1) and DE builds the portal reader against it (TO-3), **in parallel, without waiting for the artifact to exist**. That parallelism is what makes "DONE RIGHT NOW" reachable. **Ship the contract as soon as it is decided — a paragraph and a JSON skeleton beats a polished document an hour later.**

**Carry this limitation into the contract (decomp L-3):** publish-layer S3 keys are the **~11% generative class** — only ~11% of in-scope key call sites NAME their key (1 of 112 in the publish/serving layer). **A token census will not find your consumers. Do not rest the contract on one.**

## Half 2 — `ETFS-e-3`: IAM

Reader/writer pair for the chosen prefix. **You stated this discipline unprompted at 65608 and it is recorded here so it binds the CELL, not the seat:**

- **`comp-iam` is a FLOOR, never a verdict** — it models `(action)`, never `(action, resource)`. A role holding `s3:GetObject` on ANY bucket reports `[GRANTED]` for a call to EVERY other. **Treat its operation list as a floor; SILENCE IS THE DEFECT, and never read it as a deletion warrant.**
- A **NEW prefix** is verified on the live primitive: `aws iam simulate-principal-policy --policy-source-arn <role> --action-names <action> --resource-arns <ONE exact key>`.
- ⛔ **ONE `--resource-arns` PER CALL** — 2+ flips the held ones to `implicitDeny`.
- ⛔ **The positive control runs as a SEPARATE INVOCATION** — mode (1) silently disarms the very control you are leaning on. *A positive control is only a control if it runs in isolation from the target.*
- ⛔ **NEVER use `simulate-principal-policy` to check whether an action NAME is real** — a nonexistent action returns `implicitDeny`, **indistinguishable from a missing grant**, and sends you hunting a policy gap that does not exist. The discriminating oracle is `aws accessanalyzer validate-policy`.
- Pass `--context-entries` for any conditioned statement (no context → `implicitDeny`, byte-identical to a real deny).

## Acceptance criteria — every criterion carries `cell_refs`

| id | criterion | cell_refs | grounding layer |
|---|---|---|---|
| **ETFS-TO2-AC1** | Route DECIDED between the two surviving candidates, **with `comp-routes` evidence cited** and the provenance header read | `ETFS-e-1` | DESIRED + APPLIED |
| **ETFS-TO2-AC2** | ⭐ **CONTRACT PUBLISHED** — key/prefix, s.4 shape, four books, shell representation, as-of field. Sent to DS + DE the turn it exists | `ETFS-e-2` | DECLARATIVE |
| **ETFS-TO2-AC3** | Contract states **explicitly** that `positioning_data.json` is NOT written by this project and Models-mode bytes are untouched | `ETFS-e-2`, `ETFS-f-3` | DECLARATIVE |
| **ETFS-TO2-AC4** | IAM delta named: what is granted, what a NEW prefix needs — on the **live primitive**, ONE `--resource-arns` per call, positive control in a SEPARATE invocation | `ETFS-e-3` | APPLIED |
| **ETFS-TO2-AC5** | If a CF path class is a **MINT**, say so plainly (mint ≠ gap) | `ETFS-e-1` | APPLIED |
| **ETFS-TO2-AC6** | **NO write, move, or delete touches `opal-data-etfs/platinum/`** or any ETFS_CANON artifact | `ETFS-a-8` | APPLIED |

## Your two queued items — ordering CONFIRMED, neither dropped

You proposed ordering both behind the ETF read. **Confirmed, and your reasoning was right:** P4I-3 executes nothing either way (the flip it serves is held on both of Andrew's conditions), and the 04:00Z producer census blocks no one. **Both stay yours, neither is dropped, both are AFTER this TO.** No further ask needed from you on either.

## Surprise channel · Reporting

`3.0.0_SA_CVO` owns the channel. **OBSERVATION never interrupts** (one line, keep working); **BLOCKING** routes same-turn to me, cc CVO; **ARMED** needs a named disarm owner same-turn, and DISARMED ≠ REMEDIATED. **Mid-round the spec is FROZEN.**
**STATUS MOVES WITH THE ACT, BY YOU, SAME TURN.** Status is CELL-level — `ETFS-e-1`, `-e-2`, `-e-3` complete independently.
**EVERY REPORT OF A COMMIT STATES ITS PUSH STATE** — never bare "landed."
⛔ **Never compose a report of a completed act in the same tool call as the command that produces it.**
