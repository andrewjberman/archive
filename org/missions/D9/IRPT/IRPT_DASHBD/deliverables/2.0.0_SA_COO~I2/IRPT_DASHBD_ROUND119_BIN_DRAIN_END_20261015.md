# IRPT_DASHBD round 119 (the CTO's B-IN analysis, msg 8048), workstream B-IN (Inflection) -- drain-end (issuer 2.0.0_SA_COO~I2, 2026-10-15 ~05:1xZ)

**One order (a WORLD vendor read), drained; ONE GET; no write to AWS, nothing deployed; the whole-firm roster stays in the private folder; counts, verdict words and field names only in the repo.** Issued @cca2e77e03 (merged @a69db7d3ec). Drained: `DB-i-7` (~307, @37b3a966f3). On the landed tree `DBI119-1-AC1` PASSES and the proof instance reads VALID. `round-close-check --project IRPT_DASHBD --round 119` reads **MAY-CLOSE** (1 order, 0 judgment criteria). Push state: LOCAL on box/dell2, not read against origin.

## What the read found

**One GET, not three:** GET 1 (the pull's own `NewPortfolio` request, `isActive=true`) returned HTTP 200 with 3,040 rows and **held all three accounts**, so GET 2 and GET 3 were not due and were not made. The credential is accepted again (a third time).

- **The missing account is NOT an inactive account.** It is in Orion's active whole-firm account list. The omission is in Scope, not in the account list.
- **No exclusion-type flag differs.** Missing against present: 7 differing field paths; the performance-relevant names are `accountStartDate`, `accountStartValue` and `modelName`; exclusion-type paths: none; boolean differences: none. Series-less against present: 18 differing paths, the same three relevant names, none exclusion-type. The checker's verdict for both is `STATUS_OR_DATE_DIFFERS`, not `FLAG_DIFFERS`.
- **The three names carry a pattern the worker did not name (read privately by this seat; relations and nulls only, no value).** In Orion's own record the MISSING account has `accountStartDate` **null** and `accountStartValue` **null**, and no `modelName`. The SERIES-LESS account has a start date and a positive start value but **no `modelName`**. The PRESENT account has all three. So the visible pattern is: no start date and no start value at the source, then no Scope group at all; a start date but no model, then a group without a series over Q3 (the series appeared over YTD).
- **That is an inference, claim `inferred`, not a cause.** Three accounts of one household cannot prove why Scope omits an account. It is a testable hypothesis, and the roster gives its denominator: of the 980 Inflection accounts in the private dimension, **863 are in Orion's active roster** (117 are not; that is a third coverage class not read here). Among the 863, **40 have a null `accountStartDate` and `accountStartValue` and every one of the 40 also has no model**, and **132 more have a start date but no model** (172 without a model in all).

## What this seat read for itself

I re-ran the criterion in the worker's tree (PASS), re-validated the proof instance (VALID), merged through `safe-merge.sh` (row gate clean), scanned the record, script and proof for identifier-length digit runs (none) and read the three records' nulls and the roster counts from the private body myself, printing no value. **Not a grade.**

## Issuer errors this round

None found. (Earlier rounds' disclosures stand in their packets.)

## Rows held (owners named)

`W307-S1` (INERT): the GET's header names were re-cased by the request builder; the GET returned 200 and nothing was repaired. **`D2-S60` (ARMED, owner this seat; the CTO's row) is partly met and stays ARMED:** its disarm needs (1) this read to name a flag or record `NOT_DETERMINED`, which it does (no flag differs; the cause stays undetermined), AND (2) `~P2`'s feed (IB-pr-556) to carry the account as `ABSENT` `NO_GROUP` with no household-level aggregate built from the feed's account rows. Half (2) is `~P2`'s and has not landed; `D2-S61` records half (1). The commit gate's account-id check did not run (`W182-S1`'s condition).

## What goes to the CTO

1. **The ruling's "if a flag explains the omission, the feed's reason class gains it" does not apply as worded** (no flag differs), but the read gives the feed a better reason class than `NOT_DETERMINED`, on a stated inference: **`NO_START_DATE_AT_SOURCE`** for an account whose Orion record has a null `accountStartDate`, and **`NO_MODEL_AT_SOURCE`** for one with a start date and no `modelName`. The feed can take it from the `NewPortfolio` roster the pull already lands (`accounts_v2`), joined on the account id, with no further vendor call. The page words can then say "no start date recorded for this account" instead of "not available".
2. **This may be a fix at the source, not a vendor question:** a null start date and a missing model are fields set in Orion by Inflection's own operations. For the CTO's decision: ask Inflection's operations (an Opal-side act, not a vendor contact) to set the start date and model on the 40 accounts with no start date, then re-read Scope. The 117 accounts of the dimension that are not in the active roster are a separate class and are not explained here.
3. **A test the CTO may want before the feed relies on the inference:** one probe (a WORLD read, two Scope calls) on a household whose accounts include one with a null start date and one with no model, to see whether the pattern holds on a second household. I would not run it unless the CTO wants the reason classes stated as measured; as inferred they can ship.

## What this does to the FWD outcomes

Inputs to `FWD-2` for Inflection: not met. The account pages stay "Account-level returns are not available for this firm yet." until `~P2`'s feed lands and the B-IN adapter reads it.

## Open

**Andrew:** nothing from this workstream. **This seat:** the adapter cell waits on `~P2`'s feed landing its first bronze and silver; the next B-IN cut waits on the CTO's round-120 B-IN analysis or on that landing.

-- 2.0.0_SA_COO~I2
