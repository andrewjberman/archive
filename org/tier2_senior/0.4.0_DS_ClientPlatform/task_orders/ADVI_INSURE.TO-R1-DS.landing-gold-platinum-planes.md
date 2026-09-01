<task_order>
<id>ADVI_INSURE.TO-R1-DS.landing-gold-platinum-planes</id>
<project>ADVI_INSURE</project>
<issued_to>0.4.0_DS_ClientPlatform~R</issued_to>
<!-- RE-SEATED 2026-08-26 ~19:1xZ by 2.0.0_SA_COO (issuer). Prior: ~J (NOT LIVE).
     ⛔ THIS RE-SEAT MAKES THE RECORD MATCH WORK THAT WAS ALREADY AUTHORISED AND ALREADY DONE.
     0.4.0_DS_ClientPlatform~R has carried this project all day ON RULINGS. CORRECTED 2026-08-26 ~20:1xZ
     BY THE ISSUER: this line first read "AC1 closed, AC2 closed" and THAT WAS FALSE ON AC1 AND
     IMPRECISE ON AC2 -- it contradicted lines 94-112 of this same file, which correctly report AC1 as
     DISTINGUISHED / APPLIED-GATED (INS-b-2 satisfied; INS-b-1 + INS-inv-4 genuinely gated on an unseated
     producer). A TO FACE THAT CONTRADICTS ITSELF IS WORSE THAN EITHER HALF ALONE, and I introduced it.
     THE ACCURATE FORM: the ISSUER has ruled criteria closed IN MESSAGES; THIS FILE'S ARRAY CANNOT SAY SO --
     0 of 1,067 criterion rows estate-wide carry a CLOSED value (census 0.4.0_DS_ClientPlatform~R
     @4776a2305c, re-run 19:59:01Z, control PASS=999). The ruling vocabulary and the status enum share no
     value, so the array is NOT to be edited to match my rulings -- that authorization is WITHDRAWN (73382).
     Rulings of record: stamp-amendment spec @211b4ae752, design-doc fifth row @06ff6bbb2f (on origin/CLOUD)
     -- while
     `to-check.py --assignee 0.4.0_DS_ClientPlatform~R` returned total=0 over 2,115 files, because
     every act was authorised by a MESSAGE and no TO ever moved to that serial.
     THE TWO INSTRUMENTS FAIL TOWARD OPPOSITE ERRORS ON THE SAME BASE AT THE SAME MOMENT: the broker's
     rollup over-reports that lane at 4, the assignee scan under-reports it at 0, and the true answer
     is NEITHER -- one project, carried on rulings, invisible to both. Surfaced by ~R with a positive
     control (same command, ~J -> total=1, so the zero is measured and not a matcher artifact). -->
<issued_by>2.0.0_SA_COO</issued_by>
<status>pending</status>
<!-- seat RELEASED 2026-08-28 17:4xZ by 2.0.0_SA_COO (78492, reversible); open set gated on INS-a-5's
     first fire; re-seat on that fire or Andrew's word. AC1/AC5/AC6 PASS, AC2/AC3 APPLIED-GATED,
     AC4 SHUT. Status stays `pending` deliberately -- a released seat is not a closed TO. -->
<!-- ⛔ MEASURED STATE RE-READ 2026-09-01 ~11:2xZ BY 0.4.0_DS_ClientPlatform~R (re-seated). THE NOTE
     ABOVE IS THREE DAYS STALE AND ITS OWN RE-SEAT CONDITION HAS BEEN MET: it gates the open set on
     "INS-a-5's first fire", and INS-a-5 has now fired on FOUR consecutive scheduled 04:35Z days
     (bronze present for 2026-08-29/30/31 and 09-01; 23 bronze keys walked under
     blackdiamond/49financial/bronze/, denominator printed).
     ⛔ NOTHING HERE RULES A CRITERION. Criterion status is the ISSUER's and 73382 stands. This
     records WHAT IS TRUE ON THE WORLD so the next seat does not re-derive it; instruments named.

     AC1  PASS STANDS -- and it is no longer only a ruling, it is EXERCISED. The deployed converter
          `opal-assets-silver-bd49finsurance` fired on TWO consecutive scheduled days and wrote silver
          at the ruled `fact_*` grammar: date=2026-08-31 (33,165 B / 12,271 B) and date=2026-09-01
          (33,052 B @04:35:15Z / 12,275 B @04:35:22Z). Rule 17a RE-MEASURED BY ME on the live plane:
          `.parquet` under `bronze/` = 0 of 23 keys. POSITIVE CONTROL: the same matcher returns 7 over
          the 14-key silver set, so that zero is ABSENCE and not a dead matcher. The 77/77/77 row
          agreement is RELAYED from 0.7.0_AE_CloudOps~R 91452 -- measured by that seat, not by me.
     ⚠ AC1 CARRIES A COVERAGE HOLE ITS PASS DOES NOT COVER, AND THE PASS IS NOT FALSIFIED BY IT: AC1
          was ruled on "3 of 3 CONVERTIBLE at the grammar" -- a CAPABILITY claim, not a COVERAGE one.
          THREE convertible bronze days have NO silver: 2026-08-28, 08-29, 08-30. CAUSE MEASURED, not
          inferred: the converter's own deploy landed 2026-08-30T08:06:05Z, AFTER all three. (08-27
          detailsearch is a FOURTH absence and is DESIGNED -- 50 of a vendor-attested 77, held
          UNCONVERTED-REFUSED by the completeness control.) A backfill is the ISSUER's call, not this
          seat's: spec is FROZEN mid-round and writing production silver is not a QA act.

     AC2  ⛔ THE GATE OPENED AND THE LIMB IS UNBUILT -- the one state change that matters. AC2's
          APPLIED limb was gated behind AC1's applied limb; THAT GATE OPENED 2026-08-31T04:35Z.
          MEASURED: `gold/advi/insurance/insurance_nav_current/` holds EXACTLY ONE partition,
          date=2026-08-25, LastModified 2026-08-27T19:12:18Z, ETag 3dd4f7e0c6f922ee4aed045e111a2d40 --
          an AD-HOC QA artifact, and ad-hoc artifacts are NEVER production evidence (CLAUDE.md s.5).
          The producer `data/assets/scripts/gold/bd49f_insurance_nav_current.py` is ABSENT FROM THE
          DEPLOYED CHAIN ROSTER -- measured on the `_code/` the SSM document `advi-49f-chain-dispatch`
          actually syncs (`s3://opal-data-49financial/_code/chain_49f_entrypoint.py`, 33,416 B), NOT on
          the repo copy. That roster carries a00-a07, b00-b03, c00-c02, c04 and `d_publisher_port.py`,
          and no insurance stage. POSITIVE CONTROL: the same read enumerated all of those, so the
          absence is measured. CONSEQUENCE: gold is SEVEN DAYS STALE against a source landing daily.

     AC3  UNCHANGED, AND CORRECTLY SO. The AFTER half is still not takeable -- nothing insurance-derived
          has entered the AM serve. ⚠ FLAGGED: the BEFORE baseline lives in the DEAD ~J TREE at
          `org/tier2_senior/0.4.0_DS_ClientPlatform~J/deliverables/AC3_AM_BYTE_IDENTITY_BASELINE_BEFORE.json`
          -- the re-seat moved `instance_path` and this file did not travel with it. The one artifact
          that CANNOT be re-taken later is the one sitting in the tree nothing points at.

     AC4  STILL SHUT, and the world agrees: `platinum/advi/` on `opal-data-49financial` = 0 keys.
          ⚠ BUT THIS FACE'S OWN AC4 INSTRUMENT NO LONGER RESOLVES. The block below cites
          `advi-49f-publisher` State=DISABLED (0.7.0_AE_CloudOps~K, 2026-08-26). THAT FUNCTION DOES NOT
          EXIST: a census of ALL 200 Lambda functions in the account returns no such name. POSITIVE
          CONTROL: the same matcher returns `opal-assets-silver-bd49finsurance` and
          `advi-49f-gold-dispatch`, so it is not failing toward zero. The live emitter is
          `d_publisher_port.py`, invoked INSIDE the deployed chain at :351. ⛔ THE SOVEREIGN GATE IS
          UNAFFECTED -- a gate is a WORD, not a resource state, and nothing here loosens it -- but a
          hold that names a SUBJECT rather than a PROPERTY goes unsatisfiable when the substrate
          shifts, so AC4's re-read instruction needs RE-POINTING by the issuer.

     AC5 / AC6  UNCHANGED. SOURCE-grounded; no re-measurement owed and none taken.

     STATUS STAYS `pending`. Not mine to move, and the enum still cannot express issuer-ruled closure
     (0 of 1,067 criterion rows estate-wide carry a CLOSED value, census @4776a2305c). -->

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
  <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform~R/deliverables/ADVI_INSURE.TO-R1-DS_PROOF_OF_SPEC.json</instance_path>
  <!-- RE-POINTED with the re-seating; it named the dead ~J tree. -->
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

## ⛔⛔ AMENDED ~12:5xZ ON `0.4.0_DS_ClientPlatform~J`'s BLOCKING SURPRISE — AC1/AC2 ARE DEPENDENCY-GATED, NOT FAILED

**Their measurement, and it is the right shape: 480,954 keys FULLY WALKED across FOUR NAMED TREES, `insurance`-bearing
= 0, with a POSITIVE CONTROL (`allocation` = 416 over the same walked set) proving the matcher discriminates.**
`blackdiamond/49financial/` **does not exist** — only `49f` (285 keys) and `cottonwood` (3,370) are live under
`blackdiamond/`.

⛔ **THE DEFECT IS MINE AND IT IS THE SAME ONE FIVE TIMES TODAY: I EXCLUDED SURFACE (a) TO `0.6.0_AE_PartnerETL` AND
NAMED NO SEAT AND NO SEQUENCE.** AC1's grounding is **APPLIED** (*keys exist, head-object*), and Rule 17a says bronze
is **RAW API BYTES PER RUN** — **so AC1 is satisfiable only by fabricating raw vendor bytes, which is the one thing
that rule forbids. A criterion reachable only by the prohibited act is unreachable.**

**RULED:**
- **`INSR1DS-AC1` (the LANDING plane) is `UNCOMPUTABLE-BY-DEPENDENCY` until surface (a) lands.** Not failed, not
  deferred by choice — **gated on a producer that is not seated.** Dependency NAMED: `INS-a-1..3`,
  `0.6.0_AE_PartnerETL`, the bd49f REST vehicle's insurance leg. **Seat requested; sequence stated so it is not
  re-derived.**
- ⛔ **AMENDED 2026-08-25 ~21:0xZ BY THE ISSUER — `INSR1DS-AC1` SPLITS. It reports as `DISTINGUISHED / APPLIED-GATED`,
  NOT as a flat `UNCOMPUTABLE-BY-DEPENDENCY`.** Raised by `0.4.0_DS_ClientPlatform~J` (71424) and the ruling is theirs;
  I am only signing it. **THE DEFECT WAS MINE AND IT IS THE ONE I ALREADY STATED AS LAW ON AC2 AT 70416:** *a criterion
  carrying two grounding layers cannot take one status honestly.* **AC2 GOT THE SPLIT. AC1 DID NOT — I FIXED THE
  INSTANCE AND NOT THE CLASS, which is the identical failure this project's own CVO P1 recorded against me on
  `INS-inv-2` less than 24h earlier.** Third instance of that shape at this seat; the remedy is the split, not more care.
    - **`DISTINGUISHED`** — **`INS-b-2`** (the two prefixes NAMED and distinguished). Grounding layer **SOURCE**, and
      its oracle is a **NAMING act, not a byte property**, so surface (a) never gated it. **ALREADY SATISFIED, evidence
      already committed inside AC1's own `output_evidence`:** `49f` 285 keys, `cottonwood` 3,370,
      `blackdiamond/49financial` absent (0), both live spellings named with counts, leaf-name collision resolved.
      **No new measurement is owed.**
    - **`APPLIED-GATED`** — **`INS-b-1`** + **`INS-inv-4`**. Grounding layer **APPLIED**; genuinely unreachable until
      `INS-a-1..3` / `0.6.0_AE_PartnerETL` lands. The dependency above still binds these two and ONLY these two.
  ⚠ **AC1's `status_reason` never mentioned `INS-b-2` — it reasoned only about raw-byte availability and Rule 17a,
  i.e. about `b-1` and `inv-4`. A SATISFIED CELL WAS RIDING A GATED VERDICT AND THE VERDICT'S OWN PROSE SHOWED IT.**
  ⛔ **NO SCHEMA CHANGE: 6 criteria, `cell_refs` unchanged, alignment denominators unchanged.** This rules how AC1
  REPORTS, not what it covers. `0.4.0_DS_ClientPlatform~J` correctly refused to amend the instance themselves — a
  criterion's status is the ISSUER's ruling and rewriting it at the executing seat is scope adjudication in the
  widening direction. **They were right to ask and right not to act.**
- ⛔ **SILVER GRAMMAR RULED 2026-08-25 ~23:4xZ BY THE ISSUER, on `0.4.0_DS_ClientPlatform~J`'s BLOCKING
  surprise (71849).** AC1's row reads `blackdiamond/49financial/silver/insurance_*`. **THE RULED FORM IS
  THE FRAMEWORK'S:**
  `blackdiamond/49financial/silver/{_fact_table(...)}/date={D}/data.parquet` via `silver_key()` —
  e.g. `.../silver/fact_insurance_relationshipaccountdetailsearch/date=2026-08-25/data.parquet`.
    - **THE TWO AUTHORITIES GOVERN DIFFERENT GRAINS AND DO NOT ACTUALLY COLLIDE.** PRD s.11 **Ruling 1
      (Andrew-approved) rules THE TREE** — `blackdiamond/49financial/`, with `49f/` recorded as the
      legacy alias. `insurance_*` in that sentence is **ILLUSTRATIVE OF THE TABLE, not a ruling on the
      table-segment convention.** `data/assets/scripts/silver/silver_registry.py` — "the ONE conversion
      framework" — rules **THE TABLE SEGMENT** (`_fact_table()`, `FACT_NAMING_CHANNEL_WIDE = True` at
      `:67`). **Both are satisfied by the same key.** No ruling is overridden.
      ⚠ **LIMIT OF THIS READING, STATED:** if Andrew intended Ruling 1 to fix the TABLE NAME as well as
      the tree, this is wrong and one line from him corrects it. The ruling is read at the grain its own
      words settle; it is not widened.
    - **MEASURED (`~J`, denominator printed):** 12,522 keys under `blackdiamond/` walked client-side, 18
      distinct silver table segments — **`fact_*` 16 tables / 1,006 keys · BARE 2 tables / 60 keys.**
      POSITIVE CONTROL `/silver/fact_` → 1,006 FIRES. CROSS-SOURCE CONTROL under `schwab/` (the ruled
      family) → 13,545 of 38,435 FIRES. ⚠ The two bare ones are named `dim_*` — **GOLD VOCABULARY IN A
      SILVER PATH** — read as an anomaly, not a counter-convention.
    - ⛔ **AND WRITING THE LITERAL FORM WOULD HAVE MADE THIS THE ONLY PRODUCER ON THIS SOURCE OUTSIDE THE
      FRAMEWORK** — the one-producer-one-home defect, minted fresh by this TO.
    - ⛔ **THE PARKED CELL IS CASHED.** `silver_registry.py:61-65`: *"CHANNEL-WIDE extension
      (orion/eclipse/blackdiamond/etf/smartx) is PARKED to an open contract cell settling before those
      families' first deploy (COO, V2-8 AMENDMENT-3 @ca90ae9dd)."* **THIS IS THAT FAMILY'S FIRST DEPLOY.**
      RULED: `FACT_NAMING_CHANNEL_WIDE = True` **STANDS** for the blackdiamond family. **No code change** —
      the constant already defaults True and 16 tables already ride it; what was missing was the ruling.
      `~J` declined to cash it themselves: *"a seat could easily treat it as settled and proceed."*
      **A DEFAULT THAT HAPPENS TO BE CORRECT IS NOT A DECISION.**
  **No cell_ref, criterion id, alignment denominator or acceptance row count changed** — the DESTINATION
  GRAMMAR is corrected.
- ⛔ **`INSR1DS-AC2` (the GOLD TABLE) SPLITS, and I am correcting my own first wording of this amendment, which said
  AC1 *and* AC2 were gated and then listed AC2's own cells as reachable four lines later — a contradiction inside one
  edit.** **Its DESIGN limb — schema, partition grammar, spine-key set — IS DELIVERABLE NOW.** **Its APPLIED limb —
  rows actually written — is dependency-gated with AC1.** Report it as **DESIGN-COMPLETE / APPLIED-GATED**, never as
  a single verdict: *a criterion carrying two grounding layers cannot take one status honestly.*
- ⛔ **DO NOT MINT PLACEHOLDER OR SYNTHETIC BYTES UNDER `bronze/` TO MAKE A CRITERION GO GREEN. Rule 17a exists so
  whatever the raw feed carried stays recoverable; a fabricated bronze partition destroys that permanently and would
  read as a PASS.**
- **`blackdiamond/49financial/` being a MINT is correct and expected** — the grammar ruling stands; a prefix that does
  not exist yet is not a defect, it is unbuilt.

**WHAT IS REACHABLE NOW AND IS YOURS TO PROCEED ON, WITHOUT ANY INSURANCE BYTE:**
| reachable | why it needs no bytes |
|---|---|
| **`INS-c-1/c-2/c-3` — the gold table DESIGN**, schema, partition grammar, spine-key set, and the **forbidden-field census** (no analytics / returns / series) | a schema is authored, not measured |
| **`INS-f-1` — the pattern record** Cottonwood reuses | a document, and `INS-inv-2` (no cot prefix) is checkable today |
| ⛔ **`INS-inv-1` — THE BYTE-IDENTITY BASELINE ON EVERY EXISTING AM FIGURE, TAKEN NOW** | **this is worth MORE before the change than after. A before-measurement taken after the fact is not a baseline.** |
| **`INS-d-2`** — stating positively that this MINTS a key rather than moving one | a NEVER#3 determination, not a write |

---

## ACCEPTANCE CRITERIA

| id | criterion | cells | grounding |
|---|---|---|---|
| **INSR1DS-AC1** | **Landing in the canonical grammar: `blackdiamond/49financial/bronze/insurance_*` (RAW API bytes per run) and `.../silver/insurance_*` (parquet).** ⛔ **Rule 17a: NO parquet under `bronze/` — coercing schema at ingest destroys bronze's one job. Rule 17: silver is DEDUP + DTYPE ONLY — no field slimming, no fillna, no business-row filter.** ⛔ **`49financial` and `49f` are BOTH live spellings in this estate — name which tree you wrote to and which join dims you read; a leaf-name collision here is silent.** | `INS-b-1/2`, `INS-inv-4` | APPLIED |
| **INSR1DS-AC2** | **ONE additive current-state gold table** in `opal-data-49financial/gold/advi/` (candidate `insurance_nav_current/date={D}/`), **one row per insurance account per `asOfDate`**, ⛔ **carrying the spine keys (account → relationship → advisor → firm from `a00`/`a01`) SO EVERY AGGREGATION IS A JOIN, NEVER A COMPUTATION IN THE FRONTEND.** | `INS-c-1/2` | APPLIED |
| **INSR1DS-AC3** | ⛔ **NO analytics fields, NO returns, NO series — a schema census against the forbidden set, printed.** *A snapshot plane that grows a series has become an AM calculation.* **AND the byte-identity control on every existing AM figure, measured BEFORE and AFTER.** | `INS-c-3`, `INS-inv-1` | EXERCISED |
| **INSR1DS-AC4** ⛔ **BLOCKED -- SOVEREIGN, AND IT IS NOT A SEPARATE "FREEZE" (2.0.0_SA_COO ruling 2026-08-26 ~19:1xZ).**
This criterion emits through `d_publisher_port.py` under `platinum/advi/49financial/`. **That publisher is held by
Andrew-direct 2026-08-21T19:18Z** -- the 49F flip waits on BOTH source gaps AND schedule. **MEASURED TONIGHT by
`0.7.0_AE_CloudOps~K`: `advi-49f-publisher` State=DISABLED BY CONTRACTED DESIGN, `OPAL_ADVI_PUBLISH_GRANT` unset, and
at least three of four source-gap rows open or unknown. BOTH conditions must clear; neither is sufficient.**
>> **SO AC4 IS BEHIND THE *SAME* SOVEREIGN GATE AS `0.7.0_AE_CloudOps~K`'s AC1(2)/AC3/AC6 on ADVI_PERFRP -- one gate,
>> two TOs, and it was being carried in two places as two different unknowns.** AC3 rides it too (it re-takes at
>> emission). **A publish is the ACT, not a test of it: Andrew's drive-now law licenses ad-hoc QA and does NOT reach
>> this.** AC4 stays shut; the executing lane owes nothing on it and should not re-ask per tick. | **ONE json under `platinum/advi/49financial/`, emitted by `d_publisher_port.py`** so it joins the twin set and rides the publisher's activation. ⛔ **ONE PRODUCER PER SERVED KEY — verify no second writer exists for that key.** *Live counter-example in this estate: `D_01` and `D_04` both write `platinum/firm/partner_analytics_*.json` with disagreeing `CacheControl`, resolved only by write order.* **NEVER#3 does NOT attach — you are MINTING a key, not moving one; state that positively.** | `INS-d-1/2`, `INS-inv-6` | APPLIED |
| **INSR1DS-AC5** | ⛔ **bd↔cot SEPARATION IS ABSOLUTE — 49F TREE ONLY.** The pattern record names the structure Cottonwood reuses (grammar, gold table shape, platinum key form, class-axis value) **with NO shared code, NO shared keys, NO cot prefix anywhere in it.** | `INS-inv-2`, `INS-f-1` | SOURCE |
| **INSR1DS-AC6** | ⛔ **NO alarm / SNS / SES / monitor / freshness-checker; NO shadow path, NO parallel emitter, NO standing comparator.** **AND: the Advisor tab and Distribution tab are OUT CATEGORICALLY** — if any cell of yours touches `DistributionTab` or the Advisor tab, you are outside the TO. | `INS-inv-3/5` | SOURCE |

---

## SURPRISE CHANNEL (Rule 27)

Spec FROZEN mid-round. One line by MCP to `3.0.0_SA_CVO`, **cc me** — **and NOT to `4.0.0_SA_CRO`.** You do not write
`org/surprise_channel/**`; CVO files it. OBSERVATION never interrupts; **BLOCKING routes to me same-turn**; ARMED
disarms same-turn via a NAMED owner, and **DISARMED IS NOT REMEDIATED.**

⛔ **YOUR TO LIST WILL SHOW ~18 PENDING TOs FROM THE BASE SERIAL'S BACKLOG — `list_task_orders` has no lane concept and
never validates the suffix. THIS TO IS YOUR ASSIGNMENT IN FULL.**

---
## ⚖ D2 LOCK-IN RIDER — COO, 2026-08-27 (CVO 76086, additive; no clause above is altered)
The proof-of-spec instance is validated **BY RC** (never an output string), and the validator
invocation + its TRUE rc are recorded as evidence **IN the instance**. The GO for this TO pairs
only AFTER `3.0.0_SA_CVO` cert step-zero (cert-before-GO); the re-seat is the S4 word @1d761ded1f.
FIRST ACT on GO: resume at the a-2 occupancy census (D2 brief @e4f7ecbfdc, P2 source step).
