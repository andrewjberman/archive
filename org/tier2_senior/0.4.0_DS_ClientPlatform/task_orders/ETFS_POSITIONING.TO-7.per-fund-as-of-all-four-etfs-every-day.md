# TO ETFS_POSITIONING.TO-7 — PER-FUND AS-OF: "all 4 ETFs every day"

**Issued:** 2026-08-25T00:00Z by `2.0.0_SA_COO~Z`
**Executor class:** DS (producer) + DE (serving surface) — **two lanes, sequenced, see LANES**
**Basis:** **ANDREW-DIRECT ~23:5xZ**, relayed verbatim by `1.0.0_SA_CTO~Z` (5918), who ruled the
remedy. **Cells:** `ETFS-d-1` (the projection producer) · `ETFS-e-2` (artifact contract) ·
`ETFS-f-1` (the Models↔ETFs mode switch).
**Supersedes nothing already cut.** `ETFS_INGEST.TO-7` corrects a **wrong** date; **this stops us
discarding a right one.** Different defects, different code, both live.

## HIS WORD, VERBATIM

```
"It is not a problem if we are showing 08-21 data and not 08-24, the issue is that we have data for
PFDE and PFOE being presented but we are not presenting DIVZ and IDVZ data, so the question is what
is missing, do we not have 08-21 data and holdings from Trueshares? is the mapping not set up
properly because the holdings have a different process of ingestion? That is what needs to be
figured out. We should be able to display data for all 4 ETFs every day"
```

⭐ **Note what he explicitly took OFF the table: *"It is not a problem if we are showing 08-21 data
and not 08-24."* Staleness is not the complaint. ABSENCE is.**

## ANSWERED BEFORE THIS TO WAS CUT (`1.0.0_SA_CTO~Z`, measured)

- **"Do we not have 08-21 TrueShares holdings?"** — **No, and we never did.** Bronze holds
  `trueshares/{DIVZ,IDVZ}/bronze/holdings/20260824/` **only**; silver 08-19…08-23 carry **0**
  TrueShares rows each. **Capture began 22:00Z tonight.** ⛔ **Not retroactively capturable** — the
  source is a **point-in-time export** of the fund page. There is no 08-21 file to fetch.
- **"Is the mapping wrong because ingestion differs?"** — **The ingestion differs; the mapping does
  not.** TrueShares rows arrive correctly shaped (29+44, weights 99.80/99.51, normalised into the
  same silver shape). **They simply only started arriving tonight.**

## ⛔ THE DEFECT IS DESIGN, NOT TIMING — AND NO AMOUNT OF WAITING FIXES IT

```
etf_positioning_gold.py:279  def resolve_as_of(...)        -> ONE as_of for the whole run
                       :556  def build_tables(as_of: dt.date, universe: list[str], holdings, ...)
                       :577      for code in universe:     -> ALL FOUR books at that single date
```
>> **ANY FUND WHOSE HISTORY STARTS LATER THAN THE SELECTED AS-OF IS EMPTY BY CONSTRUCTION.** Today
the selector correctly chose 08-21, and at 08-21 TrueShares **does not exist and never will**.
**"All 4 ETFs every day" is unreachable under a single global as-of — permanently, not just tonight.**

⛔ **DO NOT "FIX" THIS BY LOOSENING THE SELECTOR TO PICK 08-24 GLOBALLY.** That keys PFDE/PFOE to a
date whose bbg characteristics do not exist and **breaks the two funds that currently work.**
**The selector is correct. The SINGULARITY is the defect.**

## ⭐ AND THE SERVING HALF IS A GRAIN MISMATCH — measured at this seat, and it is not "a missing surface"

```
portal/src/pages/Positioning/shared/etfAdapter.ts:131
    as_of_date: book.data_as_of ?? null          <- ALREADY PER-BOOK. The data grain is right.
portal/src/pages/Positioning/Positioning.tsx:148
    useYangDataAsOf('positioning', isEtfs ? null : dataAsOf)   <- NULL, in the MODE TERNARY
portal/src/hooks/useDataSource.ts:61-75
    registerYangTimestamp(source, ...) / getYangTimestamp(source)   <- keyed by SOURCE only
```
>> **THE ADAPTER IS PER-BOOK; THE DISPLAY HOOK IS PER-SOURCE.** `useYangDataAsOf` can hold **one**
timestamp for `'positioning'` — **so it structurally cannot express four books at four dates.**
**This is not "turn the existing surface on." The existing surface is the wrong GRAIN** (Rule 24(ii)),
and a per-fund as-of needs a **book-level** date beside each book, not a page-level one.
⚠ **INFERRED, MARKED AS SUCH:** the `isEtfs ? null` looks like it exists *because* ETFs never had a
coherent single page-level date — consistent with the singularity defect. **I have not read a comment
or commit saying so and I am not asserting it.** `0.4.0_DE_ClientPlatform~Z` owns that read.
⛔ **AND THE ORDER MATTERS: four books at possibly different dates WITH NO DATE SHOWN is worse than
today.** The surface is a **precondition** of the producer change reaching users, not a follow-up.

## Acceptance criteria

| id | criterion | cell_refs | grounding layer |
|---|---|---|---|
| **`POS-TO7-AC1`** | **Each book resolves and renders its OWN latest available holdings**, with its own `data_as_of`. Today: PFDE/PFOE @ 08-21, DIVZ/IDVZ @ 08-24 — **all four present.** | `ETFS-d-1` | **EXERCISED** |
| **`POS-TO7-AC2`** | ⛔ **The global selector is UNCHANGED in behaviour for funds that already worked.** PFDE/PFOE resolve to exactly what they resolve to today — **prove it, do not assert it.** | `ETFS-d-1` | **EXERCISED (before/after)** |
| **`POS-TO7-AC3`** | **The artifact carries `data_as_of` PER BOOK** and the contract records that it may differ across books in one payload. | `ETFS-e-2` | **SOURCE + artifact** |
| **`POS-TO7-AC4`** | ⛔ **A BOOK-LEVEL as-of is DISPLAYED beside each book.** The page-level `useYangDataAsOf('positioning', …)` is the **wrong grain** and must not be stretched to carry it. **State what you built and why the hook was not reused** (rung 2 requires saying why not). | `ETFS-f-1` | **EXERCISED (rendered)** |
| **`POS-TO7-AC5`** | **`ETFS-f-3` holds: Models mode BYTE-IDENTICAL.** The `isEtfs ? null : dataAsOf` ternary is *in the mode switch* — **the Models branch must be provably untouched.** | `ETFS-f-1` | **EXERCISED (byte-verified)** |
| **`POS-TO7-AC6`** | ⛔ **NEGATIVE CONTROL: a fund with NO holdings at any date.** Show it still renders as a labelled shell with an honest empty as-of — **not omitted, and not silently borrowing another book's date.** | `ETFS-d-1` | **EXERCISED (fixture)** |

> **AC6 is the load-bearing one.** Per-fund as-of makes "each book finds its own latest" the rule —
> **and the failure mode of that rule is a book with nothing to find quietly inheriting a neighbour's
> date.** That renders perfectly and is a lie about provenance, the day after Andrew ruled on
> provenance.

## LANES and sequencing

- **`0.4.0_DS_ClientPlatform~Z`** — AC1/AC2/AC3/AC6, `data/etfs/scripts/gold/etf_positioning_gold.py`
  (Rule 13: yours end-to-end).
- **`0.4.0_DE_ClientPlatform~Z`** — AC4/AC5. ⛔ **AC4 is a PRECONDITION of AC1 reaching users**, not a
  follow-up: shipping four differently-dated books with no visible date is worse than today.
- **`1.0.0_SA_CTO~Z`** — the design ruling is already yours and is recorded above.
- **`3.0.0_SA_CVO~Z`** — closes on AC1+AC4 together, **never AC1 alone.**

## Standing constraints

- **Do NOT loosen the as-of selector to a later global date.** Named above; it breaks the working funds.
- **Do NOT backfill TrueShares history.** It is a point-in-time export; there is nothing to fetch,
  and a re-fetch now would write **today's** holdings under an **earlier** partition name — the
  hazard `1.0.0_SA_CTO~Z` ruled on for `ETFS_INGEST.TO-7` AC3.
- **No producer→serving coupling shortcuts**, no shadow path, no comparator (standing veto).
- **No alarms, monitors, SES or freshness checkers** (standing moratorium).

<proof_of_spec>
  <!-- ISSUANCE half (COO~Z). POSITIONAL — no --expected-criteria flag:
         python .tools/proof-of-spec-check.py <instance>.json POS-TO7-AC1,POS-TO7-AC2,POS-TO7-AC3,POS-TO7-AC4,POS-TO7-AC5,POS-TO7-AC6
       CHECK THE RC, NEVER THE OUTPUT STRING; take it WITHOUT A PIPE. Coverage diff is BIDIRECTIONAL.
       The checker's `firm` enum still has no ETFS value — enter FABRIC and DECLARE it. Routed to
       CTO~Z as gate owner; neither lane edits a gate.
       TWO LANES, ONE CONTRACT: the instance is not complete until BOTH lanes have filed. AC4 filed
       alone, or AC1 filed alone, is a PARTIAL — do not let a per-lane pass read as a TO pass. -->
  <criterion id="POS-TO7-AC1" cell_refs="ETFS-d-1"/>
  <criterion id="POS-TO7-AC2" cell_refs="ETFS-d-1"/>
  <criterion id="POS-TO7-AC3" cell_refs="ETFS-e-2"/>
  <criterion id="POS-TO7-AC4" cell_refs="ETFS-f-1"/>
  <criterion id="POS-TO7-AC5" cell_refs="ETFS-f-1, ETFS-f-3"/>
  <criterion id="POS-TO7-AC6" cell_refs="ETFS-d-1"/>
  <expected_criteria>POS-TO7-AC1,POS-TO7-AC2,POS-TO7-AC3,POS-TO7-AC4,POS-TO7-AC5,POS-TO7-AC6</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/ETFS_POSITIONING.TO-7_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

## Why this composes with his provenance ruling rather than competing with it

He ruled at ~23:0xZ that **the provider's as-of IS the provenance stamp, maintained from bronze
onward.** **Per-fund as-of is that ruling carried to the serving layer — one date per book, from the
provider, shown.** ⭐ **A single global as-of is precisely the thing that FORCES us to discard one
provider's honest date in favour of another's.** The two rulings are one requirement at two layers.
