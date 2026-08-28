# TO D1_CATVIEWS.TO-S1-DE — PER-CLIENT ROW SUPPRESSION AT L1/L2 (RENDER-SIDE)

<id>D1_CATVIEWS.TO-S1-DE.per-client-row-suppression</id>
<decomp_ref>workflows/atom_decomposition/runs/d1-catviews/20260824T195537Z/DECOMP.md — `D1-h-p1` (**L0 presence predicate**: *"the node's served AUM at the firm's as-of > 0 … drive the block with one node at 0 and assert the tile is ABSENT, not empty"*) extended to L1/L2, and `D1-h-v3` (L2 drill). **NO new cell** — this is `D1-h-p1`'s predicate applied one and two levels down.</decomp_ref>
<issued_to>`0.4.0_DE_ClientPlatform~Z` — **BUILT AND COMPLETE.** That lane built this TO and its guard SELF-ARMS on the served values the moment they appear (no flip, no code change). The lane was then KILLED 2026-08-28 ~19:4xZ by `2.0.0_SA_COO~Z` on **Andrew-direct** (*"kill the idle tier2 lanes, need to clean up here"*) — **idle because its remaining criterion is EVENT-GATED, with zero uncommitted work in its tree, verified before the kill.** ⛔ **DO NOT RE-SPAWN A DE LANE FOR THIS TO.** No build act is outstanding; `TS1-AC2` discharges at the next ~13:00Z fire. ⚠ ~~NO LIVE DE LANE — seating is `0.0.0_AB_MSTR~Z`'s act~~ **STRUCK: seating is the COO's act since Andrew's 15:32Z word, and the phrase read as an instruction to spawn a lane for work that was already built.**</issued_to>
<issued_by>2.0.0_SA_COO~Z</issued_by>
<issued>2026-08-28T15:0xZ</issued>
<status>pending -- ⛔ **THE HARD DEPENDENCY IS DISCHARGED AND A DE LANE IS LIVE. RECONCILED 2026-08-28 ~19:3xZ by `2.0.0_SA_COO~Z` (issuer); BOTH CLAIMS BELOW WENT FALSE AND THE FACE KEPT SAYING THEM.** (1) `D1_CATVIEWS.TO-M1-DS` **HAS LANDED** — build `a5227cf161` + instance `c5b405f643`, both ON `origin/SITEZ`, and `a5227cf161` is an ancestor of the DEPLOYED gold-lambda pin `70a0828226` (17:28:29Z), verified with a negative control that demonstrably returns NO. (2) `0.4.0_DE_ClientPlatform~Z` **IS LIVE** and reports this TO **BUILT**, with its guard self-arming on the served values the moment they appear — no flip, no code change, nothing for a seat to remember. ⚠ **REMAINING GATE IS AN EVENT, NOT A SEAT:** the dollar values are in the DEPLOYED bytes but no fire has emitted a new object, so the served plane still reads `as_of 2026-08-27` with 0 of 15 L2 members carrying an `aum` (measured through the dev proxy on a real bearer, all four scopes). ⛔ **CORRECTED 2026-08-28 ~19:5xZ by `2.0.0_SA_COO~Z`: ~~four criteria, one event~~ WAS WRONG ON BOTH COUNTS. THERE ARE THREE TIMES ACROSS TWO EventBridge PLANES**, censused on both APIs:
> ```
> RULES plane      13:00Z  etf-positioning-producer-daily -> etf-positioning-producer   -> INGEST-TO10-AC3  (D4)
> SCHEDULER plane  13:30Z  mdpf-scheduled-floor           -> mdpf-gold-lambda           -> CATV-TOV1-AC7
>                          (⛔ TM1-AC1 MOVED OUT OF THIS ROW 2026-08-28 ~20:4xZ by 2.0.0_SA_COO~Z on
>                           0.4.0_DS_ClientPlatform~Z's catch: its own text reads "carries a dollar value
>                           on the SERVED artifact", so it belongs at 13:50Z. The L2 values are PRODUCED
>                           at 13:30Z but only REACH the served object when the publisher copies them.)
>                  13:40Z  mdpf-accrual-bridge-daily      -> mdpf-accrual-trigger
>                  13:50Z  opal-assets-mdpf-portal-publisher-daily -> ...-portal-publisher -> **THIS TO's TS1-AC2**
> ```
> ⭐ **`TS1-AC2` IS THE LATEST OF ALL OF THEM — it needs the SERVED object, which the PUBLISHER writes at ~13:50Z, not the gold floor at 13:30Z.** Scoring it at 13:30Z reads the pre-publish object and returns the OLD values, which would look like the fix failing. ⚠ **`list-rules` STRUCTURALLY CANNOT SEE a Scheduler entry** — a single-plane census is how one number stood in for three. The gold-lambda's deployed `LastModified` is `2026-08-28T17:28:29Z`, so the 13:30Z fire runs the repinned bytes. ⛔ No ad-hoc run to beat it. ⚠ **ORIGINAL FOLLOWS, APPENDED NOT REPLACED.** ~~CUT, UNSEATED and BLOCKED. HARD DEPENDENCY: `D1_CATVIEWS.TO-M1-DS` MUST LAND FIRST.~~</status>
<priority>P1 — Andrew has asked for this TWICE.</priority>

<authority>
**ANDREW-DIRECT ~14:0xZ, VERBATIM** (typos his, preserved):
> *"Also sometng Iwould recommend is that named constituents at L1 and L2 only appear if there is AUM
> associated. if I am a client that does not have any Opal Fixed Income, i should not even se Opal
> Fixed Income in Custom Models."*

**ANDREW-DIRECT ~14:2xZ — THE PLANE, VERBATIM:**
> *"in my opinion, the easiest way to do that, is simply dont display a row if its not populate"*
> *"that is the architecturally simple decision"*

**ANDREW-DIRECT ~15:0xZ — RE-ASKED, WITH THE WORKED CASE:**
> *"Also need the edits i asked for regarding what cards/rows surface per client. Opal Fixed Income for
> example is only invested in by Cottonwood, we do not need to show that for Inflection in their Custom
> Models."*

**AND THE NULL/ZERO OVERRULE ~14:0xZ, VERBATIM:**
> *"A null is a 0 in this case, if only practically, think about the end user. There may be a null
> because that model doesnt exist for them, so if your solution to this is throw a noisey client-facing
> error about Type 2 errors and unknown denominators, as a non-technical audient and also human being,
> that would be massive inapproprirate"*
</authority>

## 1. ⛔ THE PLANE IS **RENDER-SIDE**, AND THE SEQUENCE IS KEPT SO NOBODY RE-LITIGATES IT
```
OPEN            "a per-client zero is a RENDER-time fact"                (1.0.0_SA_CTO~Z, 13177)
PRODUCER-SIDE   "the artifact is the trust boundary"                     (13201) -- WITHDRAWN by author
RENDER-SIDE     ANDREW, 13206.   >> THIS ONE IS LIVE. <<
```
⛔ **DO NOT BUILD PRODUCER-SIDE SUPPRESSION.** The withdrawn ruling's own diagnosis: *"I applied a
cross-tenant threat model to a single-tenant surface."* Audience is **Opal staff and advisors only**
(Andrew, 14:2xZ) — firm-scoped artifact, that firm's own data.

## 2. ACCEPTANCE CRITERIA

| id | criterion |
|---|---|
| `TS1-AC1` | ⛔ **NULL AND ZERO BOTH SUPPRESS.** A named L1/L2 constituent with null OR zero AUM **is not there**: no card, no row, no badge, no `unavailable` treatment, **no explanatory text**. ⛔ **`predicate === 'unavailable'` MUST NOT be routed to for this** — `PredicateUnavailable` renders *"Fee split unavailable at this scope"* and that sentence must never reach a reader whose only "defect" is not owning the product. |
| `TS1-AC2` | **HIS WORKED CASE IS THE ACCEPTANCE TEST, BOTH DIRECTIONS.** `Opal Fixed Income` **RENDERS for Cottonwood** and **IS ABSENT for Inflection** under `Custom Models`. ⛔ **Exhibit BOTH — an absence with no positive control proves nothing.** |
| `TS1-AC3` | **A RENDERED BEFORE AND AFTER, both READ by the executing agent.** ⚠ **The canvas is SILVER** — light text or ghost-white controls outside a dark Panel is the #1 recurring portal defect. **Check it by looking, not by a class-name grep.** |
| `TS1-AC4` | ⛔ **NO L0 REGRESSION.** L0 zero-suppression **already works** (`D1-h-p1`, measured on his screenshots: no `Alternatives` card, no `SMA` card). **Show the L0 set is unchanged** — `Models` / `Client` for cottonwood. **This TO extends a live mechanism; it must not re-implement or displace it.** |
| `TS1-AC5` | ⛔ **THE SUM-PRESERVING CHECK IS INTERNAL QA ONLY.** Suppressing a true zero is sum-preserving; suppressing an unknown is not. **If a parent stops reconciling after suppression, something non-zero was suppressed.** ⛔ **This NEVER becomes a client-facing banner** — it is a pipeline signal, invisible to the reader. |
| `TS1-AC6` | **TYPESCRIPT CLEAN** — `tsc -b`, zero errors. ⛔ **`commit-gate` reads `.py`/`.sh`/`.tf` and will print "checked 0 of N files" on a frontend diff; that line is NOT evidence of a clean gate.** |

## 3. ⛔⛔ THE HARD DEPENDENCY — READ BEFORE STARTING

**EVERY L2 NODE UNDER `Models` RENDERS `--` TODAY.** `Primary` ($178.36M) and `Custom` ($8.43M) carry
money; their children carry none.
>> ⛔ **SHIPPING THIS TO AGAINST TODAY'S DATA HIDES THE ENTIRE L2 LAYER.** `Custom` and `Primary` would
   expand to nothing. **`D1_CATVIEWS.TO-M1-DS` MAPS THE VALUES; THIS TO SUPPRESSES WHAT IS THEN
   GENUINELY ZERO. That order is not a preference.**
⚠ **AND THIS IS THE CASE WHERE NULL REALLY IS NOT ZERO** — those L2 nodes are **unmapped**, not empty.
**Andrew's ruling still governs the RENDER (the client is never told which); the distinction lives in
the pipeline's own counts.** Both are true and they do not conflict.

## 4. ⛔ WHAT THIS TO CANNOT REACH — do not mark it closed by shipping this
The **888-char `predicate_reason`** on the `Client` node **is NOT touched by this rule, because that
row IS populated** (`Client` = $294.91M). Engineer-facing prose inside a populated node is not an empty
row. ⛔ **TWO ITEMS, TWO REMEDIES.** That one is producer-side — measured: `CategoryViewTree.tsx:212`
renders only the amber TITLE; the body is the emitter's own field, **so no portal change can reach it
at all.**

## 5. NOT YOURS
⛔ The L2 value mapping (`TO-M1-DS`, DS-class) · the `predicate_reason` remedy (producer-side) ·
the **PROD promote** — **Andrew's word, per promote, no standing authorization.**

<proof_of_spec>
  <criterion id="TS1-AC1" cell_refs="D1-h-p1"/>
  <criterion id="TS1-AC2" cell_refs="D1-h-p1,D1-h-v3"/>
  <criterion id="TS1-AC3" cell_refs="D1-h-v3"/>
  <criterion id="TS1-AC4" cell_refs="D1-h-p1"/>
  <criterion id="TS1-AC5" cell_refs="D1-h-p1"/>
  <criterion id="TS1-AC6" cell_refs="D1-h-v3"/>
  <expected_criteria>TS1-AC1,TS1-AC2,TS1-AC3,TS1-AC4,TS1-AC5,TS1-AC6</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DE_ClientPlatform/deliverables/D1_CATVIEWS.TO-S1-DE_PROOF_OF_SPEC.json</instance_path>
  <alignment_denominators>cells declared: 2 (D1-h-p1, D1-h-v3); criteria: 6. FORWARD — 6 of 6 carry >=1 cell_ref. BACKWARD — 2 of 2 reachable (D1-h-p1 from AC1/AC2/AC4/AC5; D1-h-v3 from AC2/AC3/AC6). Unmapped 0; untraceable 0. NO cell added: `D1-h-p1` already declares the presence predicate at L0 and its oracle is "assert the tile is ABSENT, not empty" — this TO applies that same predicate one and two levels down, on the sovereign's word.</alignment_denominators>
</proof_of_spec>
