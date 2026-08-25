# TO ETFS_INGEST.TO-2 — THE CANONICAL CONSTITUENT ROW: the four conventions, as Rule-24 value-enum acts

<task_order id="ETFS_INGEST.TO-2" project="ETFS_INGEST">
<decomp_ref>workflows/atom_decomposition/runs/etfs-ingest/20260824T2010Z/DECOMP.md @babfb23e8c — cells `INGEST-T2-3` (the superset row), `INGEST-T2-4` (the as-of convention), `INGEST-CONV-1` (cash line), `INGEST-CONV-2` (identifier spine), `INGEST-CONV-3` (weight units + conservation). Run manifest `run.json` @796c92888c.</decomp_ref>
<certification>⛔ **CUT AHEAD OF CERTIFICATION AND CARRIED "UNCERTIFIED DECOMP" ON ITS FACE — that was the legal shape and it was correct.** ✅ **THE DECOMP IS NOW CERTIFIED**: `3.0.0_SA_CVO~Z`, certificate `org/tier1_exec/3.0.0_SA_CVO/deliverables/laneZ_ETFS_INGEST_STAGE3_DECOMP_CERTIFICATION_20260824.md` @422bdb431b, **BOUND TO ONE VINTAGE — `@fcdf042972` AND NO OTHER** (the certifier verified their certified pin byte-identical to that commit, sha256 `1bc5eba5de…`, 480 lines, rather than assuming it; the three earlier commits are explicitly NOT covered and two of them FAIL the cells→criteria direction). ⛔ **THE SIGNATURE DOES NOT CLOSE THE COHORT GAP:** this remains a **REDUCED-COHORT** run — **one independent perspective, the author's**. *A certifier is the second reader, not the cohort;* nobody has independently re-enumerated the operative surfaces. **Premise-oracle verification was a SAMPLE, NOT A CENSUS: 3 of 36 re-run verbatim, 3 of 3 reproducing. The other 33 are unverified and the certificate does not assert them.**</certification>
<issued_to>DS-class (data scripts / schema / silver conventions). Executor-class declared to `1.0.0_SA_CTO~Z` (msg 4909); spawn ask routed to `0.0.0_AB_MSTR~Z`. **Seat may not exist when you read this — the TO does not wait on the seat and the seat does not act without a GO.**</issued_to>
<executor_class>DS-class</executor_class>
<seating_trigger>FIRED at the declaration. Nothing gates this TO — C2 and C3 are ruled, and none of these five cells depends on the TO-1 deploy.</seating_trigger>
<placement>**SITE Z** (Rule 26; D4 is SITEZ until the project is done). **Rule 13 lane split holds: you author `data/**`, AE-class applies.** No apply crosses a fabric.</placement>
<issued_by>2.0.0_SA_COO~Z</issued_by>
<issued>2026-08-24T20:2xZ</issued>
<status>complete — delivered by 0.4.0_DS_ClientPlatform~Z; proof-of-spec VALID (rc=0); awaiting COO~Z RAVC step-4 validation</status>
<priority>P1 — **this IS his central design ask.** *"work to design the structure in a manner that renders a consistent output shape."* Everything downstream of silver inherits whatever you decide here.</priority>
<authority>Andrew-direct 2026-08-24 word (1): *"design the structure in a manner that renders a consistent output shape"*; word (4): *"from their idiosyncratic shapes, to unified parquet"*. PRD `docs/architecture/ETFS_INGEST_PRD.md` §5 (the canonical row, v0.1 record + the conventions it owes) and §6 T5. CLAUDE.md **Rule 24** (four postulates, at AUTHORING, binding every value enumeration), **Rule 17** (silver = dedup + dtype only; NEVER slim fields, NEVER fillna/dropna/business-filter), **Rule 17a** (bronze stays raw), **Rule 17b** (serving is platinum).</authority>
</task_order>

## ⛔ WHAT THIS TO IS — AND WHAT IT IS NOT

**This is a SCHEMA-AUTHORING task order. It is not a converter edit.** Its deliverable is **four
ruled conventions with their four-postulate records**, plus the superset-row decision that frames
them. **The code that implements them is `ETFS_INGEST.TO-4`** (the `convert_trueshares()` holdings
feed) and is deliberately a separate TO.

> **THE SPLIT IS THE POINT, and the decomp made it for a reason it has already paid for once:** folded
> into a converter edit, a vocabulary act becomes an implementation detail decided by whoever happens
> to be writing the code at the time. **That is the axis-flattening Rule 24's 2026-08-20 widening was
> written against** — *"OUTCOME ARRAYS, TYPED-RESULT SETS AND PREDICATES ARE SCHEMAS, and they escape
> the gate PRECISELY BECAUSE THEY DO NOT READ AS SCHEMAS."* A `cash_basis` field with three allowed
> values reads like bookkeeping. **It is an enum.**

## THE BASE — an ADOPTION with declared gaps, not a mint (build-ladder rung 2)

The 17-column `HOLDINGS_COLUMNS` shape **already exists and both issuers already normalize into it**
(`lambda_function.py:159`; filepoint maps at `:624-633`, TrueShares at `:464-473`). **Do not mint a
new shape.** ⚠ **Adoption is still an authoring act** — the four-postulate test applies to what you
adopt, not only to what you invent.

**Measured on the live artifact** (`silver/holdings/2026-08-23.parquet`, read directly at the COO
seat, 2026-08-24 — **re-derive rather than inherit**):

```
114 rows   PFDE 90 / PFOE 24 / DIVZ 0 / IDVZ 0     source_system=etf_netassets_watch 114/114
is_cash    False 110 / True 4                       weight_pct sums  PFDE 100.01 / PFOE 99.99
17 cols: date fund_key fund_ticker holding_ticker cusip security_name shares price market_value
         weight_pct is_cash fund_net_assets fund_shares_outstanding source source_system
         data_as_of _ingested_at
```

## THE FOUR CONVENTIONS — each a Rule-24 act, each with what is MEASURED today

| cell | convention | measured today | what you owe |
|---|---|---|---|
| **`INGEST-CONV-1`** | **CASH LINE** | filepoint sets `is_cash` from `MoneyMarketFlag=Y` → **4 of 114 True**; TrueShares declares `is_cash=None` (unknown, correctly, per Rule 17). ⛔ **AMENDED 20:5xZ — THE ISSUED TEXT SAID "both issuers carry a `SALXX` line" AND THAT IS FALSE.** DS~Z measured **SALXX = 0 of 114 silver rows**; the four `True` rows are **FXFXX ×2 and a literal Cash&Other ×2**. `SALXX` is the **TrueShares** cash line — "both" was true of **DIVZ+IDVZ (two FUNDS)**, never of the two ISSUERS. *Traced: MSTR~Z's brief said "both" meaning the two funds; the PRD rendered it "both issuers"; I copied the PRD. **Each hop was a faithful copy and the referent silently widened.*** ⛔ **AND IT CHANGES YOUR DENOMINATOR: a cash convention written against "the SALXX line" covers ZERO of today's 114 live rows.** | A **provenance** enum — e.g. `cash_basis ∈ {vendor-flag, name-inferred, none}` — so a NULL that means *"the vendor did not say"* is distinguishable from a FALSE that means *"the vendor said no"*. ⛔ **THE INFERENCE ITSELF STAYS IN GOLD** (Rule 17: null-meaning judgment is gold-tier). Silver records **who said what**, never **what we concluded** |
| **`INGEST-CONV-2`** | **IDENTIFIER SPINE** | `cusip` populated on every row of both issuers (oracle CSVs: 44/44 and 30/30). **IDVZ's lines are US-listed ADR tickers** (`BBSEY`, `BNPQY` …). ⛔ **PFDE carries a Bloomberg ID `BBG01Y2F01K3` IN THE `CUSIP` COLUMN** — measured, row 1 of `constituents_issuer_fill.csv`, the TPG line | `cusip` is the spine, **plus an `id_kind` (or a validated-CUSIP rule) so a BBGID can never masquerade as a CUSIP.** Bloomberg resolution for the enrich leg goes **through the spine, not the ticker** — the ADR ticker resolves, but to the ADR line, not the local line |
| **`INGEST-CONV-3`** | **WEIGHT UNITS + CONSERVATION** | silver is **pct-points** (`%` stripped at normalize); sums PFDE 100.01 / PFOE 99.99, and the issuer CSVs 99.80 / 99.51 | Declare **pct-points** at silver. Declare the sum-vs-100 check **as a MANIFEST FIELD, NEVER A FILTER** (a filter is a business-row-filter and Rule 17 forbids it at silver). ⛔ **DO NOT REGULARISE AGAINST PLATINUM:** `holdings[].weight` there is a **FRACTION** while the book percentages that aggregate those same weights are **PERCENT**. That asymmetry is deliberate, it preserves Models byte-parity, and DS correctly refused to tidy it once already (ETFS_POSITIONING Amendment F) |
| **`INGEST-T2-4`** | **AS-OF** | ⛔ **AMENDED 20:5xZ — IT IS TWO CLOCKS, NOT FOUR READINGS, AND DS~Z'S FRAMING IS BETTER THAN MINE.** Source-confirmed in the deployed converter: `:612` reads the ISSUER's own `Date`, and `date` / `data_as_of` are **ONE VALUE STORED TWICE** (`:902` / `:917`, same expression; measured EQUAL 114/114 — they *cannot* disagree). So there is an **ISSUER clock** (`date` == `data_as_of` == the issuer's Date) and a **RUN clock** (`_ingested_at` + the object key, date-parts equal 114/114). The key-vs-column divergence I measured is REAL and reproduces — it is a **filepoint forward-dated effective Date**, not a defect. | ⛔ **THE OWED DELIVERABLE IS RE-POINTED. "The issuer's date stored verbatim beside it" is ALREADY SATISFIED, twice over — do not build it. THE REAL GAP IS ITS MIRROR: NO COLUMN CARRIES THE RUN DATE.** It survives only as a timestamp string and in the object key, and **all three consumers read ROWS, not keys — so a consumer holding a dataframe cannot recover which run produced it.** That is what T2-4 owes. |

## `INGEST-T2-3` — THE SUPERSET ROW (the decision that frames all four)

**The tension, stated exactly:** his *"unified parquet"* at SILVER meets **Rule 17's "silver never
slims fields."** Today's 17-column shape **DROPS vendor columns** — `SharesOutstanding`,
`CreationUnits`, `MoneyMarketFlag` (filepoint); `Net Assets`, `Account` (TrueShares).

**THE PRD'S RECOMMENDATION, WHICH YOU MAY OVERTURN WITH EVIDENCE:** the unified row is a **SUPERSET**
— canonical spine columns (deterministically derived, both-store) **+ every vendor column verbatim,
null where a vendor lacks it** — and **every judgment field stays gold.** That satisfies both his word
and Rule 17 with no second path.

⚠ **`opal-data-etfs/silver/holdings/` HAS THREE LIVE CONSUMERS** (the L1 universe derivation at
`etf_daily_pull.py:88`, the constituents leg 2, the TO-1 gold producer). **A superset ADDS columns,
which is additive and safe; it is NOT a warrant to move, rename, or re-tier that artifact.** If your
design implies a move, **stop and route it to me** — that is a NEVER#3-adjacent act, not a schema choice.

## Acceptance criteria

| id | criterion | cell_refs | grounding layer |
|---|---|---|---|
| **`INGEST-TO2-AC1`** | **A four-postulate record per convention — FOUR separate records, not one covering four axes.** Each names its **axis**, its **grain**, its **ONE intent**, and its **state frame**; the **CE half is tested against a DECLARED LAYER you name explicitly**, then you hunt the uncovered member. ⛔ **Rule 24(iii) applies INSIDE a value's wording** — a value whose adjective asserts something the axis does not measure fails even when the cross-value test passes | `CONV-1`, `CONV-2`, `CONV-3`, `T2-4` | **SOURCE** — the record is the artifact |
| **`INGEST-TO2-AC2`** | **A token-hygiene census per proposed value name**, word-boundary, **`comp-find -i`** (⛔ case-sensitive by default, and this estate CAPITALISES its load-bearing words — a case-sensitive census drops exactly the rulings). **Print the denominator.** A value name that collides with an existing ratified term is a **re-coin**, not a mint — check `comp-estate --definitions` first (build-ladder rung 2, one layer up) | all four | **SOURCE** |
| **`INGEST-TO2-AC3`** | **The superset-row decision, RULED with evidence** — adopt the PRD's recommendation or overturn it. Enumerate **every vendor column dropped today**, per issuer, **with a denominator** (the vendor header vs `HOLDINGS_COLUMNS`). State explicitly whether the shape is additive-only | `T2-3` | **DATA** — the vendor headers + the live parquet |
| **`INGEST-TO2-AC4`** | ⛔ **EXERCISED ON REAL ROWS, NOT ON THE SPEC.** For each convention, show it produces the right answer on **at least one row that discriminates**: the `SALXX` line (CONV-1), the **PFDE TPG BBGID row** (CONV-2), a full fund's weight sum (CONV-3), a row where `date` ≠ `_ingested_at`'s date (T2-4). ⛔ **A convention validated only against rows it was written from is a test that cannot fail** | all five | **EXERCISED** |
| **`INGEST-TO2-AC5`** | **Rule 17 compliance stated per convention:** no field slimmed, no `fillna`/`dropna`, no business-row filter, no judgment at silver. Where a convention *records* a judgment made elsewhere, say where that judgment lives. **No new gate, no alarm, no monitor** | all five | **SOURCE** |

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>comp-estate --definitions</run>
      <expect>The RATIFIED term registry. Every value name you propose is checked against it BEFORE minting.</expect>
      <if_mismatch>A name that already exists as a ratified term is a re-coin — adopt the existing term or state why a new one is needed. Build-ladder rung 2 applies to vocabulary, not only to code.</if_mismatch>
    </step>
    <step>
      <run>comp-find -i "&lt;each proposed value name&gt;"</run>
      <expect>A printed DENOMINATOR and a band breakdown per name.</expect>
      <if_mismatch>⛔ Use `-i`. A case-sensitive census over these records misses the emphatic, decision-carrying lines and keeps the incidental prose — measured at 46% missed on a 3-file corpus. And an UNDERCOUNT is the dangerous case: comp-find guards a ZERO with a warning and names `-i` itself, but a PARTIAL case-miss returns a confident non-zero count with no caveat at all.</if_mismatch>
    </step>
    <step>
      <run>comp-pipescript io etf_positioning_gold.py --pipeline etfs</run>
      <expect>COLUMN GAPS + the portal consumers of the gold row — so a silver convention change is checked against what already reads downstream. `--pipeline` is REQUIRED; flagless is rc=2 REFUSED.</expect>
      <if_mismatch>STOP. A new or renamed silver column with an unexamined downstream consumer is the cross-domain case; surface to COO~Z before writing.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>bash .tools/commit-gate.sh (every .py touched)</run>
      <expect>PASS — py_compile + ds-precommit-check + ruff. Every gold/silver/bronze .py begins with `from __future__ import annotations` (Rule 15).</expect>
      <if_mismatch>STOP. `--force` does NOT bypass a gate FAILURE.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>the AC4 discriminating-row exercise, re-run against the committed spec</run>
      <expect>Each convention returns the right answer on the row chosen to break it.</expect>
      <if_mismatch>Surface to COO~Z. A convention that only works on the rows it was authored from is not ruled, it is fitted.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<proof_of_spec>
  <!-- ISSUANCE half (COO~Z). POSITIONAL invocation — there is NO --expected-criteria flag:
         python .tools/proof-of-spec-check.py <instance>.json INGEST-TO2-AC1,INGEST-TO2-AC2,INGEST-TO2-AC3,INGEST-TO2-AC4,INGEST-TO2-AC5
       ⛔ CHECK THE RC, NEVER THE OUTPUT STRING (the usage banner contains "Exit 0 = VALID", so a grep
       for a success string passes on a call that validated nothing), and take the rc WITHOUT A PIPE.
       The coverage diff is BIDIRECTIONAL. -->
  <criterion id="INGEST-TO2-AC1" cell_refs="INGEST-CONV-1, INGEST-CONV-2, INGEST-CONV-3, INGEST-T2-4"/>
  <criterion id="INGEST-TO2-AC2" cell_refs="INGEST-CONV-1, INGEST-CONV-2, INGEST-CONV-3, INGEST-T2-4"/>
  <criterion id="INGEST-TO2-AC3" cell_refs="INGEST-T2-3"/>
  <criterion id="INGEST-TO2-AC4" cell_refs="INGEST-CONV-1, INGEST-CONV-2, INGEST-CONV-3, INGEST-T2-4, INGEST-T2-3"/>
  <criterion id="INGEST-TO2-AC5" cell_refs="INGEST-CONV-1, INGEST-CONV-2, INGEST-CONV-3, INGEST-T2-4, INGEST-T2-3"/>
  <expected_criteria>INGEST-TO2-AC1,INGEST-TO2-AC2,INGEST-TO2-AC3,INGEST-TO2-AC4,INGEST-TO2-AC5</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/ETFS_INGEST.TO-2_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

## Premise oracles — run these at pickup

| premise | the one-line read that falsifies it |
|---|---|
| the 17-column shape is what silver carries | read the newest `silver/holdings/*.parquet`; column list == `HOLDINGS_COLUMNS` |
| `is_cash` is vendor-flagged for one issuer only | `is_cash` value counts → **4 True / 110 False**, all from filepoint rows |
| a BBGID sits in the CUSIP column | `head -2` the newest `constituents_issuer_fill.csv` → the TPG line's `cusip` = `BBG01Y2F01K3` |
| three date semantics disagree | one silver row's `date` vs `data_as_of` vs `_ingested_at` vs the object key |
| the artifact has three live consumers | `etf_daily_pull.py:88`, `etf_constituents_pull.py:213`, the TO-1 gold producer |

## Standing constraints

- **Rule 13:** you author `data/**`; **AE-class deploys.** Do not apply anything.
- **Rule 17 / 17a / 17b** bind every line of this. **Silver never slims, never judges.**
- **Do NOT edit `PATHFINDER_FUNDS`** — the scope asymmetry (filepoint = one file both funds;
  TrueShares = per fund) is a **FIELD, not a defect**.
- **Do NOT move, rename, or re-tier `opal-data-etfs/silver/holdings/`** — three live consumers. A
  design implying a move routes to me.
- **Commit to your own lane; do NOT push** (integrator-only, LD-0367). **Report as "landed LOCAL
  @hash, rides integration", never a bare "landed".**
- **Read the number, then write the sentence** — never compose a report of a completed act in the
  same tool call as the command that produces it.
- **Surprise channel:** `org/surprise_channel/ETFS_INGEST/` (`3.0.0_SA_CVO~Z`), coordinate `-Z-S{n}`.
  **OBSERVATION never interrupts; BLOCKING routes same-turn to me, cc CVO~Z; anything ARMED names a
  disarm owner same-turn. DISARMED ≠ REMEDIATED.** Mid-round the spec is **FROZEN** — route, do not
  adjudicate.
- **Status moves with the act, by you, in the same turn.**

## What this TO unblocks

`ETFS_INGEST.TO-4` (the `convert_trueshares()` holdings feed) implements CONV-1..3 and T2-4 — it is
**deliberately downstream of your rulings**, so the code is written against a decided shape rather
than deciding it. `INGEST-T3-6` (the gold row) is a **SECOND Rule-24 act at a DIFFERENT GRAIN** and
**may not share an axis with yours**; it is a separate cell and will be a separate TO.
