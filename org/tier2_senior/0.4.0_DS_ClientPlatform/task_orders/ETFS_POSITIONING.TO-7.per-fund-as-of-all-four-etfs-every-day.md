# TO ETFS_POSITIONING.TO-7 — PER-FUND AS-OF: "all 4 ETFs every day"

<issued_to>`0.4.0_DS_ClientPlatform~F` — **ADDRESSED 2026-08-28 ~01:5xZ by `2.0.0_SA_COO~Z` (issuer). THIS TO HAD NO ASSIGNEE FOR THREE DAYS.** DS half (the producer) first; the DE half (serving surface) is sequenced behind it and is NOT addressed here. Letter measured free: the 388-line spawn audit carries `~L ~P ~Q ~W ~Z` for this base and nothing else. ⛔ **Rule 27 forbids folding it into a live DS lane — `~L` is on `ETFS_SATELLITES`, `~Q` on `ETFS_INGEST`; `ETFS_POSITIONING` is a third project.**</issued_to>
<executor_class>DS-class (producer) — the DE half follows</executor_class>
<status>complete -- ⭐ **CERTIFIED. THE CERTIFICATE EXISTS AND IS ON ORIGIN.** `cvoZ_ETFS_POSITIONING_TO7_TO11DE_CERTIFICATION_20260828.md` @`37a69dcdf7`, verdict **CERTIFIED -- 7 of 7**. Located 15:1xZ by `3.0.0_SA_CVO~Z`; VERIFIED at this seat by containment against `origin/SITEZ` with a SOUND negative control (`origin/CLOUD` tip NOT contained, so the test demonstrably returns NO). ⛔ **THIS FACE PREVIOUSLY READ 'awaiting certification' AND WAS STALE -- the certificate POSTDATES it and nobody updated the face.** ROOT: the face and the certificate are TWO DURABLE RECORDS OF ONE FACT WITH NO NAMED PRIMARY -- the certifier writes one and cannot write the other, the issuer owns the face and has no trigger to return, so they diverge from minute one in the direction of 'outstanding'. Corrected by `2.0.0_SA_COO~Z` as ISSUER. ⚠ **BOUND, STATED BY ITS MEASURER AND NOT PAPERED OVER: this establishes A CERTIFICATE EXISTS for the criteria as they read AT CERTIFICATION TIME. It does NOT establish that no criterion was ADDED to this face afterwards -- that needs a per-face criterion-set diff, NOT RUN.**</status>
<priority>P1 — **ANDREW-DIRECT basis.** Inside D4's completion set (`ETFS_POSITIONING`). ⚠ Does not change D4's bar, which remains his smoke test; it changes how close D4 is to meeting it.</priority>

⚠ **HEADER TAGS ADDED 2026-08-28 by `2.0.0_SA_COO~Z`. THE ABSENCE OF THEM WAS ITSELF THE DEFECT:** this TO was authored in the older markdown-header format, carries no `<issued_to>`, and therefore renders in `.tools/to-check.py` as **`[??]` with `(unassigned)`** — *it was invisible as an owned item to the instrument every seat is told to run.* **A TO that no index can attribute is a TO nobody is accountable for**, and that is the mechanism by which an Andrew-direct order sat three days in plain sight.

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
| **`POS-TO7-AC1`** | **Each book resolves and renders its OWN latest available holdings**, with its own `data_as_of`. ⛔ **AND THAT DATE IS READ FROM THE ROWS, NEVER DERIVED FROM THE PARTITION NAME.** *(Amended 00:24Z on `Z-S29` / `3.0.0_SA_CVO~Z`: as first written this criterion was **SATISFIED BY A PARTITION-DERIVED DATE** — it would have PASSED while the defect stood. Gold currently writes `"data_as_of": as_of` — the RUN's value — and reads silver's row-level as-of **ZERO** times, against a positive control showing it reads **EIGHT** other silver columns by name.)* | `ETFS-d-1` | **EXERCISED (row-sourced, prove the provenance)** |
| **`POS-TO7-AC2`** | ⛔ **The global selector is UNCHANGED in behaviour for funds that already worked.** PFDE/PFOE resolve to exactly what they resolve to today — **prove it, do not assert it.** | `ETFS-d-1` | **EXERCISED (before/after)** |
| **`POS-TO7-AC3`** | **The artifact carries `data_as_of` PER BOOK** and the contract records that it may differ across books in one payload. | `ETFS-e-2` | **SOURCE + artifact** |
| **`POS-TO7-AC4`** | ⛔ **A BOOK-LEVEL as-of is DISPLAYED beside each book.** The page-level `useYangDataAsOf('positioning', …)` is the **wrong grain** and must not be stretched to carry it. **State what you built and why the hook was not reused** (rung 2 requires saying why not). | `ETFS-f-1` | **EXERCISED (rendered)** |
| **`POS-TO7-AC5`** | **`ETFS-f-3` holds: Models mode BYTE-IDENTICAL.** The `isEtfs ? null : dataAsOf` ternary is *in the mode switch* — **the Models branch must be provably untouched.** | `ETFS-f-1` | **EXERCISED (byte-verified)** |
| **`POS-TO7-AC6`** | ⛔ **NEGATIVE CONTROL: a fund with NO holdings at any date.** Show it still renders as a labelled shell with an honest empty as-of — **not omitted, and not silently borrowing another book's date.** | `ETFS-d-1` | **EXERCISED (fixture)** |
| **`POS-TO7-AC7`** | ⛔ **GOLD READS `data_as_of` FROM THE SILVER ROWS. The run's `as_of` is a SELECTION KEY, NEVER A PROVENANCE STAMP.** Measured now: `:649 "data_as_of": as_of` — the run value — `data_as_of` occurs **exactly once** in the gold file and it is a **WRITE**; `as_of_basis` occurs **zero** times. **POSITIVE CONTROL: gold reads EIGHT silver columns by name** (`holding_ticker`, `is_cash`, `security_name`, `cusip`, `weight_pct`, `market_value`, `shares`, `price`) — **so it CAN read row columns and DOES NOT read this one.** `as_of_basis` propagates too. | `ETFS-d-1`, `ETFS-e-2` | **SOURCE + EXERCISED** |

> **AC6 is the load-bearing one.** Per-fund as-of makes "each book finds its own latest" the rule —
> **and the failure mode of that rule is a book with nothing to find quietly inheriting a neighbour's
> date.** That renders perfectly and is a lie about provenance, the day after Andrew ruled on
> provenance.

> ⛔ **`POS-TO7-AC7` IS THE ONE THAT MAKES ANDREW'S RULING REAL, AND IT IS SEPARABLE FROM AC1.**
> AC1 decides **WHICH** partition each book uses; AC7 decides **WHERE THE DATE VALUE COMES FROM.**
> **A perfect per-fund implementation that still stamps each book's partition name satisfies AC1 and
> leaves the provenance defect standing** — which is exactly how one criterion comes to stand in for
> another. ⛔ **Until AC7 lands, *"maintained from bronze ingestion onward"* is unimplemented at the
> only layer the page reads, and `ETFS_INGEST.TO-7`'s silver fix — however perfect — is INVISIBLE at
> platinum.**

## LANES and sequencing

> ⛔ **RETRACTED 00:07Z BY ITS AUTHOR — DO NOT SEQUENCE OFF THE STRUCK TEXT BELOW.**
> This TO carried, from 00:06Z to 00:24Z: *"if only one lands before 13:00Z, land the RE-DERIVE, not
> per-fund as-of"*, on the grounds that per-fund as-of alone would make DIVZ/IDVZ *"more visible AND
> still wrong."* **`1.0.0_SA_CTO~Z` retracted it on `Z-S29`: that scenario CANNOT OCCUR ON EITHER
> BRANCH.** If `bbg/2026-08-24/` lands, as_of = 08-24, all four books fill and the served date
> **matches the provider's own bronze `Date`** — correct with no re-derive and no per-fund as-of. If
> it does not land, as_of = 08-21, TrueShares has **zero** rows — shells, **nothing to mislabel.**
> **The preference rested on a third branch that does not exist.**
> ✅ **THE RE-DERIVE IS DE-URGENTED off the 13:00Z clock — still correct, still wanted, no longer
> racing.** ✅ **Per-fund as-of STANDS as a requirement, DEMOTED from an emergency** — Andrew's *"all
> 4 ETFs every day"* still needs it on any day the funds' available dates genuinely diverge.


- **`0.4.0_DS_ClientPlatform~F`** — AC1/AC2/AC3/**AC6**/**AC7**, `data/etfs/scripts/gold/etf_positioning_gold.py`
  (Rule 13: yours end-to-end). ⚠ **RE-ADDRESSED 2026-08-28 ~04:2xZ by `2.0.0_SA_COO~Z` (issuer).**
  This line read ~~`0.4.0_DS_ClientPlatform~Z`~~, which is **DEAD** (not among the 15 registered).
  The `<issued_to>` face was corrected to `~F` at ~01:5xZ and **this body line was not** — the TO
  disagreed with itself for two and a half hours, and a reader staffing off the body would have
  addressed a corpse.
  ⚠ **`AC7` ADDED TO THIS LINE 2026-08-28 ~04:2xZ by `2.0.0_SA_COO~Z` (issuer), surfaced by
  `0.4.0_DS_ClientPlatform~F` (12686). IT WAS A DECLARED CRITERION ASSIGNED TO NOBODY.**
  `POS-TO7-AC7` appeared **4 times** — criteria table, prose, the proof-of-spec command, and
  `<expected_criteria>` — and **0 times** in this LANES block (control: `AC6` appears in both).
  **It was added by the 00:24Z `Z-S29` amendment and this block predates it, so the two carriers
  never met.** ⚠ **NOT open work** — that seat has already discharged and filed it; the assignment
  is recorded so a newly-seated lane and `3.0.0_SA_CVO~Z` do not read an unowned criterion as
  unstaffed. ⛔ **I edited this exact block minutes earlier and did not catch it: I corrected the
  two names in front of me and never asked whether the criteria SET was covered.**
- **`0.4.0_DE_ClientPlatform~C`** — AC4/AC5. ⛔ **AC4 is a PRECONDITION of AC1 reaching users**, not a
  follow-up: shipping four differently-dated books with no visible date is worse than today.
  ⛔ **RE-ADDRESSED 2026-08-28 ~04:2xZ by `2.0.0_SA_COO~Z` (issuer). This half had NO ELIGIBLE
  EXECUTOR and that is why it never moved.** It read ~~`0.4.0_DE_ClientPlatform~Z`~~ — a **LIVE**
  lane, but one working `ETFS_INGEST`, so **Rule 27 (one instance, one project) BARS it from
  `ETFS_POSITIONING`.** ⭐ **That seat declined correctly rather than crossing the fence** (its own
  words: *"NOT POS-TO7-AC4/AC5, which remain seated to this serial, undischarged, and untaken under
  Rule 27"*) — **the block was the ASSIGNMENT, not the seat.**
  **`~C` is chosen on the `~Q` precedent this office already set:** it is LIVE (`last_seen`
  04:16:34Z), holds **NOTHING** open (measured, with a positive control that the same filter finds
  ten other lanes), and its own project work `D1_CATVIEWS.TO-Q1-DE` is **`complete` and CERTIFIED
  5/5**. **Rule 27 holds: `~C` moves to `ETFS_POSITIONING` holding nothing else.** No spawn needed.
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
         python .tools/proof-of-spec-check.py <instance>.json POS-TO7-AC1,POS-TO7-AC2,POS-TO7-AC3,POS-TO7-AC4,POS-TO7-AC5,POS-TO7-AC6,POS-TO7-AC7
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
  <expected_criteria>POS-TO7-AC1,POS-TO7-AC2,POS-TO7-AC3,POS-TO7-AC4,POS-TO7-AC5,POS-TO7-AC6,POS-TO7-AC7</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/ETFS_POSITIONING.TO-7_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

## Why this composes with his provenance ruling rather than competing with it

He ruled at ~23:0xZ that **the provider's as-of IS the provenance stamp, maintained from bronze
onward.** **Per-fund as-of is that ruling carried to the serving layer — one date per book, from the
provider, shown.** ⭐ **A single global as-of is precisely the thing that FORCES us to discard one
provider's honest date in favour of another's.** The two rulings are one requirement at two layers.
