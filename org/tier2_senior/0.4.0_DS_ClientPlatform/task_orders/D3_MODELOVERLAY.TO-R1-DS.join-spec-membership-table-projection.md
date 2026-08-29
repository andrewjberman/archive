<task_order>
<id>D3_MODELOVERLAY.TO-R1-DS.join-spec-membership-table-projection</id>
<project>D3_MODELOVERLAY</project>
<issued_to>0.4.0_DS_ClientPlatform~S</issued_to>
<!-- RE-SEATED 2026-08-26 ~19:0xZ by 2.0.0_SA_COO (issuer). Prior: 0.4.0_DS_ClientPlatform~K.
     ~K IS NOT LIVE and has not been for this session; DS base and ~J are also absent, so this P0
     was seated on a dead instance while the register carried it as pending. 0.4.0_DS_ClientPlatform~S
     is live, fresh, and holds ZERO other TOs (measured: to-check.py --assignee ~S -> total=0,
     scanned=2115), so Rule 27's one-project-per-instance holds.
     ⛔ HOW THE DEAD SEATING WENT UNNOTICED: the broker's get_agent_status "Pending task orders (N)"
     is a BASE-FOLDER ROLLUP -- every ~lane under 0.4.0_DS_ClientPlatform inherits the same four TOs
     in that field, regardless of <issued_to>. A lane reading it believes it holds work seated at a
     different instance, and an issuer reading it (as 2.0.0_SA_COO did at 73046 s.3) believes the
     work is covered. `to-check.py --assignee <lane>` reads <issued_to> and is the sound instrument.
     Found by 0.4.0_DS_ClientPlatform~S refusing to start work it could not confirm was its own. -->
<issued_by>2.0.0_SA_COO</issued_by>
<status>complete -- DELIVERED @fbf3ce7a44 (0.4.0_DS_ClientPlatform~K, 2026-08-25T09:15Z), CERTIFIED 6/6 @c0fad0b548 by 3.0.0_SA_CVO (instance 28,199 B, AC1-AC6 all PASS, VALID rc=0). R1 CLOSED. Terminal flip by the issuer 2026-08-29T15:0xZ; both pins verified on origin at this seat. Register drift surfaced by 1.0.0_SA_CTO 82889.</status>
<!-- ADVANCED 2026-08-26 ~19:3xZ by 2.0.0_SA_COO (issuer). It read `pending` while the work was
     DELIVERED @fbf3ce7a44 (0.4.0_DS_ClientPlatform~K, 2026-08-25T09:15Z) and CERTIFIED 6/6 @c0fad0b548
     (3.0.0_SA_CVO, 09:21Z). A stale `pending` is what re-seated a discharged TO onto a live lane as
     unstarted P0 work -- and it would have done it again on the next register scan.
     ⛔ THE ONE RESIDUAL IS NOT R1 WORK: the advisor level of the four-level contract is structurally
     unbuildable (is_primary NULL 29,907/29,907), ruled OUT OF R1 by 2.0.0_SA_COO 70461, and its
     unblock spec @9e86f635dc concludes the remedy is a BD vendor API write -- Andrew's call, not an
     exec act. SOVEREIGN-GATED, NOT LANE-GATED. -->
<priority>P0 -- Andrew-direct 2026-08-25 ~12:0xZ named this project as one of two waiting on the decomp seat. D3 has SIX open TOs and has not begun; surface (a) has never been blocked.</priority>
<date>2026-08-25</date>
<references>
  <ref type="decomp">workflows/atom_decomposition/runs/d3-account-model-overlay/20260825T123000Z/DECOMP.md</ref>
  <ref type="prd">docs/architecture/D3_ACCOUNT_MODEL_OVERLAY_PRD.md (v1.0 + v1.1 s4b amendment)</ref>
</references>
<objective>
The SMARTX_BD_EXACT_JOIN precondition spec (startable NOW) and the account_model_membership
gold table + producer at ACCOUNT GRAIN. AMENDED ~12:4xZ: the platinum projection (surface c)
is REMOVED to 0.7.0_AE_CloudOps per PRD s4c ruling 9, the Andrew-approved owner row. Portal
overlay UI (surface d) is excluded to a DE lane; Cottonwood's binding (e-2) is a declared
cross-project dependency on ADVI_COTKEY, not work to chase. An UNRESOLVED count
greater than zero is a PUBLISHED NUMBER, never a dropped row.
</objective>
</task_order>

# TASK ORDER — D3_MODELOVERLAY.TO-R1-DS · THE JOIN SPEC, THE MEMBERSHIP TABLE, THE PROJECTION

**to:** `0.4.0_DS_ClientPlatform~K` · **issuer:** `2.0.0_SA_COO` · **cut:** 2026-08-25 ~12:35Z

<decomp_ref>
workflows/atom_decomposition/runs/d3-account-model-overlay/20260825T123000Z/DECOMP.md — cells
D3-inv-1, D3-inv-2, D3-inv-3, D3-inv-4, D3-inv-5, D3-inv-6,
D3-a-1, D3-a-2, D3-a-3, D3-a-4, D3-b-1, D3-b-2, D3-b-3, D3-b-4, D3-e-1, D3-e-3
</decomp_ref>

<decomp_context>
⛔ **FIVE OF THE DECOMP'S 21 CELLS ARE EXCLUDED, FOR THREE DIFFERENT REASONS — named so the 16-vs-21 difference is
visible:**
- **`D3-c-1`, `D3-c-2` (2) — THE PLATINUM PROJECTION. AMENDED IN ~12:4xZ ON `~K`'s BLOCKING SURPRISE (70396).**
  **PRD s4c ruling 9 — THE ANDREW-APPROVED OWNER ROW — reads `0.7.0_AE_CloudOps (publisher key)`.** This TO had
  assigned it here and the decomp's sequencing line had said DE-class; **both were mine and both widened past his
  approved row.** ⛔ **AND A SECOND LIVE RECORD STILL CLAIMS IT: `D3_MODELOVERLAY.TO-D3.3.publisher-pair-and-platinum-key.md`,
  `<issued_to>0.4.0_DS_ClientPlatform~B</issued_to>`, `<status>staged -- GATED ON TO-D3.2 + D2 publisher active</status>`
  — routed to CTO for disposition. DISARMED IS NOT REMEDIATED.**
- **`D3-d-1`, `D3-d-2` (2) — THE PORTAL OVERLAY UI.** DE-class: the "seventy-thirty at a glance" render and the slice
  pivots. **REAL WORK, another lane. Your gold table is what it consumes.**
- **`D3-e-2` (1) — A DECLARED CROSS-PROJECT DEPENDENCY, NOT WORK.** Cottonwood's binding waits on `ADVI_COTKEY`
  (Andrew's keying investigation). Per §4b the per-partner models plane is `model_aua_positions` at account grain for
  49F + Inflection; **Cottonwood is NOT on it** (BD-side `fact_model_assignment` + `dim_model_portfolio`).
  **Enumerated so it is not discovered at integration. Do not chase it.**
</decomp_context>

<proof_of_spec>
  <!-- Positional: python .tools/proof-of-spec-check.py <instance>.json D3R1DS-AC1,D3R1DS-AC2,D3R1DS-AC3,D3R1DS-AC4,D3R1DS-AC5,D3R1DS-AC6 ; check the rc. -->
  <criterion id="D3R1DS-AC1" cell_refs="D3-a-1, D3-a-4, D3-inv-3"/>
  <criterion id="D3R1DS-AC2" cell_refs="D3-a-2, D3-a-3"/>
  <criterion id="D3R1DS-AC3" cell_refs="D3-b-1, D3-b-2, D3-inv-1"/>
  <criterion id="D3R1DS-AC4" cell_refs="D3-b-3"/>
  <criterion id="D3R1DS-AC5" cell_refs="D3-b-4, D3-inv-2, D3-inv-6"/>
  <criterion id="D3R1DS-AC6" cell_refs="D3-inv-4, D3-inv-5, D3-e-1, D3-e-3"/>
  <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform~K/deliverables/D3_MODELOVERLAY.TO-R1-DS_PROOF_OF_SPEC.json</instance_path>
  <!-- ⛔ RESTORED 2026-08-26 ~19:3xZ by 2.0.0_SA_COO. I re-pointed this at ~S and it was WRONG.
       THIS PATH HOLDS THE CVO-CERTIFIED INSTANCE: 28,199 B, AC1-AC6 all PASS, certified 6/6 VALID rc=0
       by 3.0.0_SA_CVO @c0fad0b548 against delivery @fbf3ce7a44.
       A DEAD LANE IS NOT A DEAD ARTIFACT. I reasoned dead-lane -> dead-folder -> re-point, and the
       folder held the certification. Had the seating been executed, a NEW instance would have been
       authored at the new path, proof-of-spec-check would have returned rc=0, this TO would have read
       COMPLIANT -- and the certified instance would have been SILENTLY ORPHANED with a junior one
       standing in its place. Caught by 0.4.0_DS_ClientPlatform~S refusing to start. -->
  <!-- RE-POINTED 2026-08-26 with the re-seating (~K -> ~S). It named a DEAD lane's folder: the
       proof-of-spec check would have written its instance into an abandoned tree, and the TO would
       have read compliant while its evidence landed where nobody looks. Surfaced by ~S. -->
  <expected_criteria>D3R1DS-AC1,D3R1DS-AC2,D3R1DS-AC3,D3R1DS-AC4,D3R1DS-AC5,D3R1DS-AC6</expected_criteria>
  <alignment_denominators>cells in this TO: 16 (inv 6 · a 4 · b 4 · e 2); criteria: 6; every criterion carries
>=1 cell_ref; all 16 cells reachable. Unmapped 0; untraceable 0. Decomp total 21; 5 excluded for THREE declared
reasons, named in decomp_context (AMENDED ~12:4xZ: surface (c) removed to 0.7.0_AE_CloudOps).</alignment_denominators>
</proof_of_spec>

---

## WHY THIS EXISTS, IN HIS WORDS

Andrew, S4: ***"very important that we get it to the account level… that is what's going to allow us to create those
slices of various granularity."*** A 49F advisor, via the Mike Little call: ***"a quick way to see what [model a client
is in] without having to dig… oh yeah, seventy-thirty."***
**Account grain is not a preference — it is what makes every other slice free.**

⛔ **SURFACE (a) IS STARTABLE NOW AND HAS NEVER BEEN BLOCKED. That is exactly why it has sat. Start there.**

---

## ACCEPTANCE CRITERIA

| id | criterion | cells | grounding |
|---|---|---|---|
| **D3R1DS-AC1** | **Drive the measured 99.65% end-to-end join to 100%-CLASSIFIED** across `a06`'s two universes + the BD export's Original Account Number universe + fam `col_4`. ⛔ **The run #9 baselines (joint 5,277 / fam-only 1,925 / BD-only 868) ARE A VINTAGE — re-measure and print your own with its timestamp.** ⛔ **`a06`'s LOCKSTEP caveat is NOT evidence of universe agreement: two universes moving together is not two universes matching.** | `D3-a-1/4`, `D3-inv-3` | MEASURED |
| **D3R1DS-AC2** | ⛔ **THE RESIDUAL ENUM IS A RULE 24 AUTHORING ACT AND THE PRD'S LIST IS A CANDIDATE, NOT AN ANSWER.** Finalize `{JOINED, NO_SMARTX_ALLOCATION, NOT_IN_ACCOUNT_UNIVERSE, NON_8DIGIT_KEY, OTHER_CUSTODIAN, CLOSED, UNRESOLVED}` **against MEASURED residuals**, with a **four-postulate record** (MECE · one grain · intent coherence · state coherence) + a token-hygiene census. **ADOPTING A SCHEMA AUTHORED ELSEWHERE IS ITSELF AN AUTHORING ACT.** The table design carries a **per-row, non-optional `evidence` column** — a status with no evidence is an assertion. | `D3-a-2/3` | SOURCE + Rule 24 |
| **D3R1DS-AC3** | **`account_model_membership` at ACCOUNT × MODEL × as_of**, writing `gold/advi/canonical/account_model_membership/date={D}/` parquet **+ manifest carrying BOTH coverage denominators**. **NAME the U1 model-identity source explicitly** — an unnamed source is where the grain slips. ⛔ **FULL 8-DIGIT ACCOUNT NUMBERS ALWAYS. TWO MASTERS, NOT INTERCHANGEABLE: `08335338` = ADVI/BD · `08242234` = MDPF/SmartX. NEVER the 4-digit prefix.** **Placement rides the D2-landed grammar, confirmed with the D2 owner — D3 mints no new tree.** | `D3-b-1/2`, `D3-inv-1` | APPLIED |
| **D3R1DS-AC4** | ⛔⛔ **THE PRD SAYS *"empty map partition = LOUD fail (vintages do not advance — a06 precedent)."* THAT PRECEDENT WAS MEASURED TODAY AND IT IS NOT THE ENDORSEMENT IT READS AS.** `a06` fails loud — **and it fails loud EVERY SUNDAY AND MONDAY BY CONSTRUCTION**: it takes `map_dates[-1]` with no trading-day filter, the map emits EMPTY weekend partitions (4,507 B, byte-identical, zero rows), and the map always lands ~30 min AFTER the chain fires — so `[-1]` is ALWAYS D-1. **The whole 49F gold chain has been dead two days a week; `c02_twr_daily` has not run since 08-22.** ⛔ **INHERIT THE LOUD FAIL. DO NOT INHERIT THE `[-1]` SELECTION.** Select by a **trading-day-resolved date**, or assert non-empty before aborting. **ORACLE: a weekend dry-run that does NOT abort.** | `D3-b-3` | EXERCISED |
| **D3R1DS-AC5** | ⛔ **AN `UNRESOLVED` COUNT > 0 IS A PUBLISHED NUMBER, NEVER A DROPPED ROW.** *"Perfect" = joined + explained-residual = denominator, **zero silent drops**.* **Coverage below the registered floor = PUBLISH WITH THE BREACH FLAGGED in the manifest, and the flag PROPAGATES into the served artifact's provenance block, read by the publisher pair AT EVERY RUN** — so a regression is visible at every publish, not only at a one-time acceptance pass. ⛔ **NO ALARM MACHINERY. The PRD's own phrasing is the model: *the record simply has a recurring reader.*** | `D3-b-4`, `D3-inv-2/6` | EXERCISED |
| **D3R1DS-AC6-AMENDED** | ⛔ **AMENDED ~12:4xZ ON `0.4.0_DS_ClientPlatform~K`'s BLOCKING SURPRISE (70396). THE PLATINUM PROJECTION IS REMOVED FROM THIS TO — IT IS NOT YOURS.** **PRD s4c ruling 9, THE ANDREW-APPROVED ROW (*"all recs approved"* ~19:1xZ), reads `0.7.0_AE_CloudOps (publisher key)`.** My decomp's sequencing line said DE-class and this TO assigned it to you; **both were mine and both widened past his approved owner row.** **WHAT REMAINS YOURS IN AC6:** ⛔ **17b — PLATINUM IS SERVING AND THE PUBLISHER IS THE ONLY JSON PRODUCER, so serving-shaped work does NOT go in your gold table.** That constraint binds your table whoever builds the publisher. **49F FIRST (the D2 template firm); INF/COT inherit by TEMPLATE, one implementation with firm-pinned invocations — never a fork.** **§4b's four-level additive runner contract (account / relationship-household-client / advisor / firm) is honoured at all four levels.** ⛔ **NO client-facing surface — Opal stays advisor-level.** | ~~`D3-c-1/2`~~ **STRUCK 2026-08-26** · `D3-inv-4/5`, `D3-e-1/3` | APPLIED |

---

## ⛔ WHAT WOULD FALSIFY THE WHOLE THING

**`D3-inv-2`.** If the residual classification cannot reach **joined + explained = denominator** — if rows fall out
unexplained — **the account-grain premise is not established, and every slice built above it inherits the gap
silently.** **Publish the `UNRESOLVED` count and STOP. Do not narrow the denominator until it reconciles.**

## SURPRISE CHANNEL (Rule 27)

Spec FROZEN mid-round. One line by MCP to `3.0.0_SA_CVO`, cc me. You do not write `org/surprise_channel/**`.
OBSERVATION never interrupts; **BLOCKING routes to me same-turn**; ARMED disarms same-turn via a NAMED owner, and
**DISARMED IS NOT REMEDIATED.**

⛔ **CELL-REF RULING 2026-08-26 (`2.0.0_SA_COO`, issuer), on `0.4.0_DS_ClientPlatform~S`'s read:**
the `<proof_of_spec>` block was **ALREADY CORRECT** -- `D3R1DS-AC6` carries
`cell_refs="D3-inv-4, D3-inv-5, D3-e-1, D3-e-3"` with **no c-cells** -- and `alignment_denominators`
already says 16 cells with (c) named as excluded. **The staleness was in the ACCEPTANCE TABLE row,
not the contract block**, and it is struck above. **~S's reading (prose authoritative, cell_refs
stale) was RIGHT; its location for the stale copy was one block off** -- and the machine-checked
artifact was the clean one, which is the direction that matters: `proof-of-spec-check.py` was never
going to fault this. **Surface (c) is `0.7.0_AE_CloudOps`'s per PRD s4c ruling 9 and is NOT in this
TO.**

⛔ **AND THE WARNING BELOW IS MINE, WRITTEN 2026-08-25 -- THEN I VIOLATED IT MYSELF ON 08-26.**
At 73046 s.3 I told `0.4.0_DS_ClientPlatform~S` *"you hold 4 pending TOs"* off the broker's
base-folder rollup. **I authored the caution one day earlier and did not obey it.** `~S` refused to
start work it could not confirm was its own and measured `to-check.py --assignee ~S -> total=0`.
**A warning in an artifact only protects the reader who reads it, and the author is not exempt.**

⛔ **YOUR TO LIST WILL SHOW ~18 PENDING TOs FROM THE BASE SERIAL'S BACKLOG — `list_task_orders` has no lane concept and
never validates the suffix. THIS TO IS YOUR ASSIGNMENT IN FULL.**
