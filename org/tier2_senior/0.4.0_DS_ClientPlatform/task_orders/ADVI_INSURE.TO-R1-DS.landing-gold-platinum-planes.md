<task_order>
<id>ADVI_INSURE.TO-R1-DS.landing-gold-platinum-planes</id>
<project>ADVI_INSURE</project>
<issued_to>0.4.0_DS_ClientPlatform~J</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<status>pending</status>
<priority>P0 -- Andrew-direct 2026-08-25 ~12:0xZ named this project as one of two waiting on the decomp seat. PRD v0.2 approved by him ~18:3xZ 08-24; the project has been unblocked and unseated since.</priority>
<date>2026-08-25</date>
<references>
  <ref type="decomp">workflows/atom_decomposition/runs/advi-insure-snapshot-plane/20260825T122500Z/DECOMP.md</ref>
  <ref type="prd">docs/architecture/ADVI_INSURE_PRD.md (v0.2, APPROVED)</ref>
</references>
<objective>
The BACKEND planes of the 49F insurance current-value snapshot: landing (bronze raw +
silver parquet under blackdiamond/49financial/), ONE additive current-state gold table
carrying the spine keys, and ONE platinum json emitted by the D-fleet publisher. Plus the
pattern record Cottonwood reuses. FRONTEND (surface e) and the ETL VEHICLE LEG (surface a)
are excluded to their own lanes. Every existing asset-management figure stays BYTE-IDENTICAL.
</objective>
</task_order>

# TASK ORDER — ADVI_INSURE.TO-R1-DS · THE LANDING, GOLD AND PLATINUM PLANES

**to:** `0.4.0_DS_ClientPlatform~J` · **issuer:** `2.0.0_SA_COO` · **cut:** 2026-08-25 ~12:35Z
⛔ **DISTRIBUTION: NOT TO `4.0.0_SA_CRO`, AT EVERY RELAY** (PRD s.3, Andrew ~16:1xZ).

<decomp_ref>
workflows/atom_decomposition/runs/advi-insure-snapshot-plane/20260825T122500Z/DECOMP.md — cells
INS-inv-1, INS-inv-2, INS-inv-3, INS-inv-4, INS-inv-5, INS-inv-6,
INS-b-1, INS-b-2, INS-c-1, INS-c-2, INS-c-3, INS-d-1, INS-d-2, INS-f-1
</decomp_ref>

<decomp_context>
⛔ **EIGHT OF THE DECOMP'S 22 CELLS ARE EXCLUDED FROM THIS TO, TO OTHER LANES — named so the 14-vs-22 difference is
visible rather than lost:**
- **`INS-a-1..3` (3) — THE ETL VEHICLE LEG.** The bd49f REST vehicle gaining an insurance leg is `0.6.0_AE_PartnerETL`
  ground (ADVI_BDAPIMIG). **Your landing plane CONSUMES what that leg produces; you do not build it.**
- **`INS-e-1..5` (5) — THE FRONTEND PLANE.** The composition class-axis mint, `PartnerAnalytics.tsx`, the Books L4
  segment, the spine aggregation, and the three-integration-point exclusion list are DE-class.
**Both are REAL WORK, not deferred scope. If either blocks you, that is a BLOCKING surprise, not something to absorb.**
</decomp_context>

<proof_of_spec>
  <!-- Positional: python .tools/proof-of-spec-check.py <instance>.json INSR1DS-AC1,INSR1DS-AC2,INSR1DS-AC3,INSR1DS-AC4,INSR1DS-AC5,INSR1DS-AC6 ; check the rc. -->
  <criterion id="INSR1DS-AC1" cell_refs="INS-b-1, INS-b-2, INS-inv-4"/>
  <criterion id="INSR1DS-AC2" cell_refs="INS-c-1, INS-c-2"/>
  <criterion id="INSR1DS-AC3" cell_refs="INS-c-3, INS-inv-1"/>
  <criterion id="INSR1DS-AC4" cell_refs="INS-d-1, INS-d-2, INS-inv-6"/>
  <criterion id="INSR1DS-AC5" cell_refs="INS-inv-2, INS-f-1"/>
  <criterion id="INSR1DS-AC6" cell_refs="INS-inv-3, INS-inv-5"/>
  <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform~J/deliverables/ADVI_INSURE.TO-R1-DS_PROOF_OF_SPEC.json</instance_path>
  <expected_criteria>INSR1DS-AC1,INSR1DS-AC2,INSR1DS-AC3,INSR1DS-AC4,INSR1DS-AC5,INSR1DS-AC6</expected_criteria>
  <alignment_denominators>cells in this TO: 14 (inv 6 · b 2 · c 3 · d 2 · f 1); criteria: 6; every criterion carries
>=1 cell_ref; all 14 cells reachable. Unmapped 0; untraceable 0. Decomp total 22; 8 excluded to two other lanes,
named in decomp_context.</alignment_denominators>
</proof_of_spec>

---

## ⛔ THE ONE INVARIANT THAT OUTRANKS EVERYTHING ELSE HERE

**NEVER BLEND INSURANCE INTO ANY ASSET-MANAGEMENT CALCULATION.** Andrew's words are the design, not a preference:
insurance NAV sits **BESIDE** AM AUM and never inside it.
> **A BYTE-IDENTITY CONTROL ON EVERY EXISTING AM FIGURE IS AN ACCEPTANCE PROPERTY, NOT A COURTESY.**
⛔ **AND IT IS THE FALSIFIER: if any existing AM figure moves by ONE BYTE, the DESIGN is wrong — not your
implementation. REPORT AND STOP. Do not reconcile the difference.**

---

## ACCEPTANCE CRITERIA

| id | criterion | cells | grounding |
|---|---|---|---|
| **INSR1DS-AC1** | **Landing in the canonical grammar: `blackdiamond/49financial/bronze/insurance_*` (RAW API bytes per run) and `.../silver/insurance_*` (parquet).** ⛔ **Rule 17a: NO parquet under `bronze/` — coercing schema at ingest destroys bronze's one job. Rule 17: silver is DEDUP + DTYPE ONLY — no field slimming, no fillna, no business-row filter.** ⛔ **`49financial` and `49f` are BOTH live spellings in this estate — name which tree you wrote to and which join dims you read; a leaf-name collision here is silent.** | `INS-b-1/2`, `INS-inv-4` | APPLIED |
| **INSR1DS-AC2** | **ONE additive current-state gold table** in `opal-data-49financial/gold/advi/` (candidate `insurance_nav_current/date={D}/`), **one row per insurance account per `asOfDate`**, ⛔ **carrying the spine keys (account → relationship → advisor → firm from `a00`/`a01`) SO EVERY AGGREGATION IS A JOIN, NEVER A COMPUTATION IN THE FRONTEND.** | `INS-c-1/2` | APPLIED |
| **INSR1DS-AC3** | ⛔ **NO analytics fields, NO returns, NO series — a schema census against the forbidden set, printed.** *A snapshot plane that grows a series has become an AM calculation.* **AND the byte-identity control on every existing AM figure, measured BEFORE and AFTER.** | `INS-c-3`, `INS-inv-1` | EXERCISED |
| **INSR1DS-AC4** | **ONE json under `platinum/advi/49financial/`, emitted by `d_publisher_port.py`** so it joins the twin set and rides the publisher's activation. ⛔ **ONE PRODUCER PER SERVED KEY — verify no second writer exists for that key.** *Live counter-example in this estate: `D_01` and `D_04` both write `platinum/firm/partner_analytics_*.json` with disagreeing `CacheControl`, resolved only by write order.* **NEVER#3 does NOT attach — you are MINTING a key, not moving one; state that positively.** | `INS-d-1/2`, `INS-inv-6` | APPLIED |
| **INSR1DS-AC5** | ⛔ **bd↔cot SEPARATION IS ABSOLUTE — 49F TREE ONLY.** The pattern record names the structure Cottonwood reuses (grammar, gold table shape, platinum key form, class-axis value) **with NO shared code, NO shared keys, NO cot prefix anywhere in it.** | `INS-inv-2`, `INS-f-1` | SOURCE |
| **INSR1DS-AC6** | ⛔ **NO alarm / SNS / SES / monitor / freshness-checker; NO shadow path, NO parallel emitter, NO standing comparator.** **AND: the Advisor tab and Distribution tab are OUT CATEGORICALLY** — if any cell of yours touches `DistributionTab` or the Advisor tab, you are outside the TO. | `INS-inv-3/5` | SOURCE |

---

## SURPRISE CHANNEL (Rule 27)

Spec FROZEN mid-round. One line by MCP to `3.0.0_SA_CVO`, **cc me** — **and NOT to `4.0.0_SA_CRO`.** You do not write
`org/surprise_channel/**`; CVO files it. OBSERVATION never interrupts; **BLOCKING routes to me same-turn**; ARMED
disarms same-turn via a NAMED owner, and **DISARMED IS NOT REMEDIATED.**

⛔ **YOUR TO LIST WILL SHOW ~18 PENDING TOs FROM THE BASE SERIAL'S BACKLOG — `list_task_orders` has no lane concept and
never validates the suffix. THIS TO IS YOUR ASSIGNMENT IN FULL.**
