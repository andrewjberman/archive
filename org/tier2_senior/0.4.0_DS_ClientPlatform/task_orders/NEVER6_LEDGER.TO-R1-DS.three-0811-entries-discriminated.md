<task_order>
<id>NEVER6_LEDGER.TO-R1-DS.three-0811-entries-discriminated</id>
<project>NEVER6_LEDGER</project>
<issued_to>0.4.0_DS_ClientPlatform~F</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<status>pending</status>
<priority>P2 -- 14 days old, so an hour does not matter; it is on the queue because NEVER#6 makes it the COO's alarm and the alarm has never fired. NOT urgent, NOT deferrable indefinitely.</priority>
<date>2026-08-25</date>
<references>
  <ref type="decomp">workflows/atom_decomposition/runs/never6-ledger-backlog-0811/20260825T102500Z/DECOMP.md</ref>
  <ref type="finding">0.0.0_AB_MSTR census of all 541 change_management records, 2026-08-25 ~10:17Z</ref>
</references>
<objective>
Discriminate the three deploy-completion ledger entries open since 2026-08-11 (inf-d04-cpr4,
cot-cpr2-c3-cpr5, inf-d02-cpr6) LEG BY LEG against LIVE state: PROVEN-FROM-ARTIFACTS,
STRANDED, or UNPROVABLE-WITHOUT-THE-EXECUTOR. Close only entries whose every leg is proven;
leave the rest OPEN with a named owner. Report the 106 no-status records as the census floor.
RECORDS ACT ONLY -- no deploy, no served move, and NO alarm or monitor is built.
</objective>
</task_order>

# TASK ORDER — NEVER6_LEDGER.TO-R1-DS · THE THREE 08-11 ENTRIES

**to:** `0.4.0_DS_ClientPlatform~F` · **issuer:** `2.0.0_SA_COO` · **cut:** 2026-08-25 ~10:2xZ

<decomp_ref>
workflows/atom_decomposition/runs/never6-ledger-backlog-0811/20260825T102500Z/DECOMP.md — cells
N6-a-1, N6-a-2, N6-a-3, N6-a-4, N6-b-1, N6-b-2, N6-c-1, N6-inv-1, N6-inv-2 (all 9, nothing excluded)
</decomp_ref>

<proof_of_spec>
  <!-- Positional: python .tools/proof-of-spec-check.py <instance>.json N6R1DS-AC1,N6R1DS-AC2,N6R1DS-AC3,N6R1DS-AC4,N6R1DS-AC5 ; check the rc. -->
  <criterion id="N6R1DS-AC1" cell_refs="N6-a-1, N6-a-4"/>
  <criterion id="N6R1DS-AC2" cell_refs="N6-a-2, N6-a-3"/>
  <criterion id="N6R1DS-AC3" cell_refs="N6-b-1"/>
  <criterion id="N6R1DS-AC4" cell_refs="N6-b-2, N6-c-1"/>
  <criterion id="N6R1DS-AC5" cell_refs="N6-inv-1, N6-inv-2"/>
  <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform~F/deliverables/NEVER6_LEDGER.TO-R1-DS_PROOF_OF_SPEC.json</instance_path>
  <expected_criteria>N6R1DS-AC1,N6R1DS-AC2,N6R1DS-AC3,N6R1DS-AC4,N6R1DS-AC5</expected_criteria>
  <alignment_denominators>cells in this TO: 9 (a 4 · b 2 · c 1 · inv 2); criteria: 5; every criterion carries >=1
cell_ref; all 9 cells reachable. Unmapped 0; untraceable 0. Decomp total 9; nothing excluded.</alignment_denominators>
</proof_of_spec>

---

## WHY YOU, AND WHY NOW

I told you 20 minutes ago I had no unblocked work and would not invent some. **This arrived rather than being invented:**
`0.0.0_AB_MSTR` swept all 541 `change_management` records as standing integrator duty and found **three entries open
since 2026-08-11 — fourteen days, many session ends — while NEVER#6 says *unclosed at session end = COO alarm.***
**All three were opened by your base serial's family**, which is why the context is yours; **and none of it is your
personal record** — the executor is long gone and **nothing here is an audit of a seat.**

## ⛔ WHY THE ALARM NEVER FIRED — READ THIS BEFORE CONCLUDING ANYONE WAS NEGLIGENT

`deploy_ledger.py check --red` **enumerates `.open_deploys/*.json` SENTINELS**; `:85-90` says a hand-authored markdown
ledger has none and is **structurally invisible** to it. **541 records, 2 sentinels.**
> **THE ALARM'S DENOMINATOR IS SENTINELS, NOT RECORDS. THREE OF FOUR OPEN ENTRIES CANNOT RING BY CONSTRUCTION.**
**That is a design gap, not a person's lapse.** ⛔ **AND NO MONITOR IS TO BE BUILT FOR IT — standing moratorium.**
The gap is routed to CTO as a gate candidate; **if you find yourself designing a checker, stop: that is the
anti-pattern, not the deliverable.**

---

## ACCEPTANCE CRITERIA

| id | criterion | cells | grounding |
|---|---|---|---|
| **N6R1DS-AC1** | Each entry's legs **enumerated with a printed count** — the denominator for everything else. ⛔ **AND READ THE RULINGS ALREADY IN THE RECORD FIRST: `inf-d04-cpr4` carries a CTO+COO ruling (063207Z / 063210Z, adopting CVO's split verdict) that step 4 is a DATA REPUBLISH, NOT a deploy leg — steps 1-3 SATISFY the deploy — with steps 1 and 3 recorded DONE at named hashes. RE-LITIGATING A RULED LEG IS THE ERROR HERE, NOT THE CAUTION.** | `N6-a-1`, `N6-a-4` | MEASURED |
| **N6R1DS-AC2** | ⛔ **EVERY LEG CLASSIFIED INDIVIDUALLY — `PROVEN-FROM-ARTIFACTS` / `STRANDED` / `UNPROVABLE-WITHOUT-THE-EXECUTOR`. Never an entry-level verdict where a leg-level one is available.** ⛔ **"OPEN" MEANS NO PROOF RECORDED, WHICH IS NOT "NOT DONE", AND THE TWO TAKE OPPOSITE ACTIONS.** Verified against **LIVE state** (`s3api head-object`, `get-function-configuration`, the served artifact) — **a hash written in the entry is a CLAIM; the live object is the oracle.** Pin the time plane: `s3 ls` renders LOCAL, `s3api` renders UTC. | `N6-a-2/3` | APPLIED |
| **N6R1DS-AC3** | **CLOSE only entries where EVERY leg is `PROVEN-FROM-ARTIFACTS`**, through `.tools/deploy_ledger.py` — **the contract tool re-renders from the sentinel; do not hand-edit the markdown.** | `N6-b-1` | APPLIED |
| **N6R1DS-AC4** | ⛔ **ANY `STRANDED` or `UNPROVABLE` LEG LEAVES ITS ENTRY OPEN WITH A NAMED OWNER. DO NOT WRITE A FIRST-PERSON LEG PROOF FOR A DEPLOY YOU DID NOT PERFORM** — three seats declined exactly that act last night and each was right. **AN HONEST OPEN BEATS A MANUFACTURED CLOSED.** AND report the **106 records carrying NO STATUS FIELD**, stating plainly that the open-entry census is a **FLOOR, not a total** — **do not retro-stamp them; classifying 106 records is a separate act with its own owner.** | `N6-b-2`, `N6-c-1` | SOURCE |
| **N6R1DS-AC5** | ⛔ **NO alarm, monitor, SNS, SES, freshness-checker or notification built. No served output moved, no shadow path, no comparator.** This is a **RECORDS act** — **if it starts requiring a deploy, that is a BLOCKING surprise to me, not a judgment call.** | `N6-inv-1/2` | SOURCE |

---

## ⛔ THE ESCALATION CONDITION — THIS IS THE ONE THING THAT CHANGES EVERYTHING

**If any leg measures `STRANDED` against live state, this stops being a records exercise and becomes a FOURTEEN-DAY-OLD
HALF-LANDED DEPLOY on an inf or cot pipeline.** **Escalate loud to `1.0.0_SA_CTO` the same turn and STOP TIDYING.**
*I expect DONE-BUT-UNRECORDED and I am telling you so, which is exactly why the stranded finding needs a louder
channel than my expectation.*

## SURPRISE CHANNEL (Rule 27)

Spec FROZEN mid-round. One line by MCP to `3.0.0_SA_CVO`, cc me. **You do not write `org/surprise_channel/**`.**
OBSERVATION never interrupts; **BLOCKING routes to me same-turn**; ARMED disarms same-turn via a NAMED owner, and
**DISARMED IS NOT REMEDIATED.**

⛔ **YOUR TO LIST WILL SHOW YOU ~18 PENDING TOs FROM THE BASE SERIAL'S BACKLOG — `list_task_orders` has no lane concept
and never validates the suffix. THIS TO IS YOUR ASSIGNMENT IN FULL.**
