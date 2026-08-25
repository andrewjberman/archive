# TO ETFS_INGEST.TO-4 — the `convert_trueshares()` holdings FEED (`INGEST-T2-1`) + implementing TO-2's ruled conventions

<task_order id="ETFS_INGEST.TO-4" project="ETFS_INGEST">
<decomp_ref>workflows/atom_decomposition/runs/etfs-ingest/20260824T2010Z/DECOMP.md @fcdf042972 (CERTIFIED vintage) — cell `INGEST-T2-1`. It IMPLEMENTS the conventions ruled under `ETFS_INGEST.TO-2` (`CONV-1` `CONV-2` `CONV-3` `T2-3` `T2-4`, delivered @80c36267a1, proof-of-spec VALID, RAVC-4 validated at the COO seat) — **those cells are DISCHARGED as rulings and are CITED here, not re-covered.**</decomp_ref>
<certification>✅ **CERTIFIED** — `3.0.0_SA_CVO~Z` @422bdb431b, bound to **`@fcdf042972` and no other vintage**. ⛔ Reduced-cohort run, one independent perspective; premise-oracle verification was **a SAMPLE, not a census** (3 of 36).</certification>
<issued_to>DS-class. Seated: `0.4.0_DS_ClientPlatform~Z`.</issued_to>
<executor_class>DS-class</executor_class>
<seating_trigger>SEATED. ⛔ **SEQUENCED BEHIND `ETFS_INGEST.TO-3`** (one thing at a time in this lane, as you have been running it) **AND BEHIND `0.0.0_AB_MSTR~Z`'s A5 fix** — see the hard dependency below.</seating_trigger>
<placement>**SITE Z** (Rule 26). ⚠ **LANE, CHECKED AGAINST THE AUTHORITY RATHER THAN ASSUMED:** this TO touches **both** `data/assets/scripts/silver/` **and** `infra/aws/lambda/etfs-pipeline/`. I expected the second to be AE-only under Rule 13 and it is **not** — `.owned-paths.yaml:1661-1663` puts `infra/aws/lambda/etfs-pipeline/**` on lane **`POD4_OR_AE`**, note: *"DS authors producer code, AE deploys; longest-match overrides the `infra/aws/**` AE-only rule."* **So both halves are yours to author. AE still deploys.** *(I nearly surfaced a lane conflict that does not exist; reading `.owned-paths.yaml` instead of my summary of Rule 13 is what settled it.)</placement>
<issued_by>2.0.0_SA_COO~Z</issued_by>
<issued>2026-08-24T21:3xZ</issued>
<status>complete -- both halves delivered by 0.4.0_DS_ClientPlatform~Z (vendor @e442e30964, unified @d7aa525fa9); proof-of-spec VALID rc=0; CONV-1 re-ruled mid-build per CTO~Z 5380; awaiting RAVC step-4</status>
<priority>P1 — this is the cell that actually **fills the DIVZ/IDVZ vendor-silver tier**. TO-1 gave us the unified rows; this gives us the Rule-17-strict vendor rows and puts the ruled conventions into code.</priority>
<authority>Andrew-direct 2026-08-24 word (1) *"design the structure in a manner that renders a consistent output shape"* and word (4) *"ground-up, in pattern ingestion and processing (bronze and silver) layers… from their idiosyncratic shapes, to unified parquet"*. Conventions ruled under TO-2. CLAUDE.md **Rule 17** (silver = dedup + dtype ONLY; never slim, never fillna/dropna/business-filter), **Rule 15** (`from __future__ import annotations`), **Rule 13** + `.owned-paths.yaml:1661` (lane).</authority>
</task_order>

## ⛔ THE HARD DEPENDENCY — DO NOT LAND THIS BEFORE THE A5 FIX

`Z-S14`: `etf_daily_pull.py:88`'s bare `~h["is_cash"]` **raises TypeError** on a null-bearing column.
`0.0.0_AB_MSTR~Z` owns the fix under **A5**, executing after tonight's 22:00Z fire.

**Two separate things, and conflating them is the trap:**
- **Tonight's fire already arms it** via the TO-1 deploy writing TrueShares rows into
  `opal-data-etfs/silver/holdings/`. **That is not yours and you cannot prevent it.**
- **THIS TO changes what that artifact CONTAINS** (the unified row half). **Landing it before the
  consumer is adapted compounds a live break instead of a known one.**

⚠ **The vendor-silver half is a DIFFERENT artifact** —
`opal-data-assets/trueshares/{fund}/silver/fact_holdings/…` — and has **no found in-repo consumer**
(F5: 22 hits / 27,945 files, all converter/schema). **So the vendor half carries no consumer risk and
the unified half carries all of it.** Sequence accordingly, and **state in your report which half you
landed first and why.**

## WHAT YOU RULED, AND WHICH FILE EACH RULING LANDS IN

| ruling (TO-2) | lands in |
|---|---|
| `cash_basis` {`vendor-flag` \| `vendor-blank` \| `vendor-silent`} | the **unified row** (Lambda `HOLDINGS_COLUMNS:156`) |
| `id_kind` {`cusip` \| `bbgid` \| `vendor-sentinel` \| `unclassified`}, cusip by **CHECK DIGIT** | the **unified row** |
| pct-points declared; conservation a **MANIFEST field at (fund × date) grain**, tolerance **0.10** derived from max 0.07/144 | the **manifest**, deliberately NOT a row column |
| `as_of_basis` {`issuer-holdings-file` \| `issuer-page-netassets` \| `run-date`} + an explicit **`run_date`** column | the **unified row** |
| superset **17 + 4 = 21**, additive-only, vendor columns **ISSUER-NAMESPACED** | the **unified row** |
| the `holdings` feed, Rule 17 strict, vendor columns verbatim | **`convert_trueshares()`** + `etf_schemas` |

⛔ **YOUR OWN Z-S16 FINDING IS THE ONE TO BUILD AGAINST:** the two issuers reach `date` by **different
KINDS of source** (`:612` a holdings-file date vs `:526` a net-assets-page as-of), flowing into one
column with **no marker** — one column, two grains. **`as_of_basis` is what makes that difference
declared, and T2-3's superset is what restores the TrueShares sheet's own discarded `Date`.** You
checked that the two remedies compose; this TO is where that composition gets built.

## Acceptance criteria

| id | criterion | cell_refs | grounding layer |
|---|---|---|---|
| **`INGEST-TO4-AC1`** | **`convert_trueshares()` gains a `holdings` FEED** — **a new feed in the EXISTING converter, NEVER a new converter** (build-ladder rung 2, MSTR~Z's rung-2 finding, adopted) — with its shape **DECLARED in `etf_schemas.py`** per that file's explicit-schema law. **Rule 17 STRICT: vendor columns VERBATIM (names and order as landed), plus deterministic additive only.** ⛔ **Do NOT widen `PATHFINDER_FUNDS`** — the scope asymmetry is a FIELD, not a defect | `INGEST-T2-1` | **SOURCE** |
| **`INGEST-TO4-AC2`** | **The five ruled conventions are IN CODE** — `cash_basis`, `id_kind`, `as_of_basis`, the explicit `run_date` column, and the 21-column issuer-namespaced superset. **Cite the TO-2 deliverable section each one implements.** ⛔ **If implementation forces a change to any ruling, STOP and route it to me — do NOT re-rule it mid-build** (the spec is frozen; a surprise item is the legal write) | `INGEST-T2-1` | **SOURCE** |
| **`INGEST-TO4-AC3`** | ⛔ **EXERCISED ON THE DISCRIMINATING ROWS, and you already know which they are.** `SALXX` (TrueShares cash, `is_cash` null → `cash_basis: vendor-silent`) · a filepoint **BLANK** MoneyMarketFlag (→ `vendor-blank`, NOT `vendor-flag`) · the PFDE **BBGID** `BBG01Y2F01K3` (→ `id_kind: bbgid`) · **`CASHEUR`** (→ `unclassified`, and **NOT** a cash sentinel — measured `is_cash=False`, so calling it one would assert what the vendor DENIED) · a row where the issuer date ≠ the run date (→ both `as_of_basis` and `run_date` legible) | `INGEST-T2-1` | **EXERCISED** |
| **`INGEST-TO4-AC4`** | ⛔ **THE CHECK-DIGIT RULE GETS ITS INJECTION TEST, because you established that live data CANNOT falsify it.** 7,674/7,674 nine-char values pass, so a length-only rule returns identical output. **Show the mutant** (a valid CUSIP with a corrupted check digit reclassifies; the length-only rule still says `cusip`). ⛔ **AND USE A MEASURED CONSTANT, NOT A REMEMBERED ONE** — your own positive control failed OPEN on a remembered CUSIP that was a different real CUSIP with its own valid check digit | `INGEST-T2-1` | **EXERCISED (injection)** |
| **`INGEST-TO4-AC5`** | **Rule 17 compliance, stated per change:** no field slimmed, no `fillna`/`dropna`, no business-row filter, no judgment at silver. ⛔ **The conservation check is a MANIFEST FIELD, NEVER A FILTER** — and note PFOE carries a **NEGATIVE** `weight_pct` (min −0.02), so a non-negativity assumption is wrong and dropping that row would be exactly the forbidden filter | `INGEST-T2-1` | **SOURCE + DATA** |
| **`INGEST-TO4-AC6`** | **Sequencing declared, not implied:** state whether MSTR~Z's A5 fix had landed when you landed the unified-row half, **measured** (`grep -n "fillna(False)" integrations/bloomberg/pipeline/etf_daily_pull.py`), and which half you landed first. **If A5 has not landed, land the VENDOR half only and say so** | `INGEST-T2-1` | **SOURCE** |

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>comp-blast convert_trueshares</run>
      <expect>Consumers of the vendor-silver ETF trees. F5 measured 22 hits / 27,945 files, all converter/schema — expect NO found in-repo consumer outside those.</expect>
      <if_mismatch>A consumer you did not expect changes the risk profile of the vendor half. STOP and surface to COO~Z.</if_mismatch>
    </step>
    <step>
      <run>⛔ **comp-pipescript io is NOT AVAILABLE for this tree and I am not mandating it.** You measured it two ways on TO-2 (`--pipeline etfs` rc=2 invalid choice; `--pipeline all` rc=1 unknown script, explicitly not a bd fallback). **Do NOT substitute `--pipeline bd-gold`** — it returns a confident answer about the WRONG TREE.</run>
      <expect>Nothing. Enumerate the unified row's consumers by reading instead: the three live readers are `etf_daily_pull.py:88` (universe derivation), `etf_constituents_pull.py:213` (leg 2), and the TO-1 gold producer.</expect>
      <if_mismatch>A fourth consumer means the superset's additive-safety argument needs re-checking — it rests on every consumer NAMING its columns and none selecting `*`.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>bash .tools/commit-gate.sh (every .py touched)</run>
      <expect>PASS — py_compile + ds-precommit-check AST/silver-ids + ruff. `from __future__ import annotations` on every silver file (Rule 15).</expect>
      <if_mismatch>STOP. `--force` does NOT bypass a gate FAILURE.</if_mismatch>
    </step>
    <step>
      <run>the AC3 discriminating-row exercise + the AC4 injection, rc WITHOUT a pipe</run>
      <expect>Each convention returns the right value on the row chosen to break it; the mutant reclassifies.</expect>
      <if_mismatch>Do not commit. A convention validated only on rows it was written from is a test that cannot fail.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>read the newest silver/holdings partition after the next 22:00Z fire</run>
      <expect>DIVZ/IDVZ rows present carrying the new columns with legible `cash_basis` / `id_kind` / `as_of_basis` / `run_date`.</expect>
      <if_mismatch>Surface to COO~Z. The unified row is the artifact three live consumers read.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

## RULED 22:2xZ -- CONV-1 FORK RESOLVED: (a) BLANK IS THE VENDOR'S NEGATIVE. + AC7.

`0.4.0_DS_ClientPlatform~Z` STOPPED MID-BUILD per AC2 and falsified their own CONV-1 ruling with a measurement. **That is AC2 working exactly as written, and the stop was correct.**

**EVIDENCE, widened at the COO seat from their n=1 to n=15 before ruling** -- *a single file cannot distinguish "this vendor never writes N" from "today's file happens to have none", and the fork turns entirely on which is true*:
```
DENOMINATOR 41 holdings CSVs in bronze (full pagination) - sampled the 15 newest
every file: rows=114  Y=4  blank=110  N=0  other=0
TOTAL 1,710 rows - Y=60 - blank=1,650 - *** N=0 *** - other=0
DISTINCT VALUES EVER OBSERVED: ['', 'Y']
POSITIVE CONTROL Y=60 non-zero -> the column IS parsed, so N=0 is a real absence
BOUND: 15 of 41 files. The older 26 were NOT sampled.
```

**RULED (a):** `cash_basis: vendor-flag` for all 114 filepoint rows; `is_cash` unchanged; **ZERO rows change.** `vendor-blank` stays in the enum for a future vendor with a genuinely optional cell.
**Three grounds:** the encoding is MEASURED, so reading blank as "no" is **DECODING a presence flag** (silver's job), not adjudicating an ambiguous null (not silver's job) - (b) would flip 110 rows to NULL and **A5's `fillna(False)` would coerce them straight back at the one consumer fixed tonight**, ceremony with no benefit - and **the value-name argument is DS~Z's own**: `vendor-blank` reads *"the vendor did not say"*, which for a presence-flag encoding **is false**. Rule 24(iii) inside a value's wording, the same class they rejected `name-inferred` for.

| id | criterion | cell_refs | grounding |
|---|---|---|---|
| **`INGEST-TO4-AC7`** | **THE CONVERTER REFUSES LOUDLY on any `MoneyMarketFlag` value outside `{'', 'Y'}`**, naming the offending value and row. Exercise it with an injected third value. | `INGEST-T2-1` | **EXERCISED** |

> **WHY AC7 EXISTS AND IS NOT OPTIONAL: I RULED (a) FROM AN INFERENCE ABOUT A VENDOR'S BEHAVIOUR, AND VENDORS CHANGE.** If filepoint ever writes `'N'`, or starts leaving genuinely-unknown cells blank, **(a) silently becomes wrong and the rows keep reading False with nothing to say otherwise.** *A ruling resting on a measured constant must fail loud when the constant moves -- otherwise I have installed an unmeasured exact constant that fails open and looks principled.*

⚠ **AC7 IS A RUNTIME REFUSAL, NOT ALERT MACHINERY** -- no alarm, no SNS, no monitor, no freshness checker. Same shape as `_assert_write_boundary`: a guard in the code path, which the standing moratorium has never touched.

<proof_of_spec>
  <!-- ISSUANCE half (COO~Z). POSITIONAL — no --expected-criteria flag:
         python .tools/proof-of-spec-check.py <instance>.json INGEST-TO4-AC1,INGEST-TO4-AC2,INGEST-TO4-AC3,INGEST-TO4-AC4,INGEST-TO4-AC5,INGEST-TO4-AC6
       ⛔ CHECK THE RC, NEVER THE OUTPUT STRING; take it WITHOUT A PIPE. Coverage diff is BIDIRECTIONAL.
       ⚠ The checker's `firm` enum has NO ETFS value (['49F','INF','COT','MDPF','FABRIC']) — a Rule 24(i)
       CE failure inside the gate that enforces Rule 24. You entered FABRIC on TO-2 and DECLARED it;
       do the same here and keep declaring it until the enum is fixed. It is routed to CTO~Z as gate
       owner; neither of us edits a gate. -->
  <criterion id="INGEST-TO4-AC1" cell_refs="INGEST-T2-1"/>
  <criterion id="INGEST-TO4-AC2" cell_refs="INGEST-T2-1"/>
  <criterion id="INGEST-TO4-AC3" cell_refs="INGEST-T2-1"/>
  <criterion id="INGEST-TO4-AC4" cell_refs="INGEST-T2-1"/>
  <criterion id="INGEST-TO4-AC5" cell_refs="INGEST-T2-1"/>
  <criterion id="INGEST-TO4-AC6" cell_refs="INGEST-T2-1"/>
  <criterion id="INGEST-TO4-AC7" cell_refs="INGEST-T2-1"/>
  <expected_criteria>INGEST-TO4-AC1,INGEST-TO4-AC2,INGEST-TO4-AC3,INGEST-TO4-AC4,INGEST-TO4-AC5,INGEST-TO4-AC6,INGEST-TO4-AC7</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/ETFS_INGEST.TO-4_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

## Premise oracles — run at pickup

| premise | the read that falsifies it |
|---|---|
| `convert_trueshares()` handles `netassets_page` only | `grep -n "netassets_page\|holdings" data/assets/scripts/silver/etf_conversion.py` → `:216` def, `:222` the single feed |
| the vendor-silver holdings tree is empty | `aws s3 ls s3://opal-data-assets/trueshares/DIVZ/silver/ ` → no `fact_holdings` — ⛔ **pair with the sibling that must be NON-empty**, `…/silver/fact_netassets_page/` → populated |
| the A5 fix state | `grep -n "fillna(False)" integrations/bloomberg/pipeline/etf_daily_pull.py` → present = landed, absent = **land the vendor half only** |
| the unified row is 17 columns today | read the newest `silver/holdings/*.parquet` column list |
| PFOE carries a negative weight | `df[df.fund_ticker=='PFOE'].weight_pct.min()` → **−0.02** |

## Standing constraints

- **Rule 17 / 17a / 17b.** Silver never slims and never judges. **The cash INFERENCE stays in gold**
  (`etf_positioning_gold.py:480-483 infer_is_cash`), which is precisely why `cash_basis` records
  **who said what** and not **what we concluded**.
- **Lane:** both halves are yours to AUTHOR (`.owned-paths.yaml:1661`, `POD4_OR_AE`). **AE deploys.**
  You do not apply.
- **No shadow path, no parallel emitter, no standing comparator.** Extend the converter; do not mint
  a second grammar beside it.
- **No alarm, no SNS, no SES, no monitor.**
- **Commit to your own lane; do NOT push.** Report as **"landed LOCAL @hash, rides integration"**.
- **Read the number, then write the sentence.**
- **Surprise channel:** `org/surprise_channel/ETFS_INGEST/` (`3.0.0_SA_CVO~Z`), coordinate `-Z-S{n}`.
  Mid-round the spec is **FROZEN** — route, do not adjudicate. **A ruling that implementation
  contradicts is a surprise item, not a re-ruling.**
- **Status moves with the act, by you, in the same turn.**

## What this closes

`INGEST-T2-1` is the last unblocked cell in the T0→T2 span. With it landed, the chain from **issuer
raw → bronze → vendor silver → unified silver** is complete and in pattern for **all four** ETFs, and
the remaining round-1 surface is gold (`TO-3` + `ETFS_POSITIONING.TO-5`'s apply) and the frontend
(`TO-5`). ⛔ **It does NOT discharge Andrew's condition (i)** — *"the pipeline COMPLETE with the full
data structure for daily Bloomberg data for ALL ETFs"* is judged on the SCHEDULED chain end to end,
and the promote word remains his.
