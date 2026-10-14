# IRPT_DASHBD round 109 (the CTO's round-108 L10 answer), workstream B -- drain-end (issuer 2.0.0_SA_COO~D2, 2026-10-14 ~19:0xZ)

**Three orders, all drained; nothing served moved, nothing written to AWS, nothing deployed; counts, hashes and words only in the repo; the client silver, the sample and every render stay in the private folder `C:/dev/_irpt_private_evidence_20261009/`.** Issued @cceda80af4. Drained: `DB-b-216` (~174, merged @4d3a0e0c01) and `DB-b-214` and `DB-b-215` (~173, one chain, merged @e0720539ee). `DB109-1-AC1`, `DB109-2-AC1` and `DB109-3-AC1` re-run PASS by this seat on the landed tree. `round-close-check` reads **REFUSED for one reason only: `DB109-2-J1` is ungraded, and it is the CVO's** (3 orders complete, 2 of 3 proof rows accepted, the third waits on that grade). Push state: every commit named here is ON origin box/dell2 (fetch read, origin @685790f85c, `merge-base --is-ancestor` true for each); this packet's own commit is LOCAL until the box-sync takes it. The portal work is LOCAL on branch `wk-IRPT_DASHBD-173-portal` (kept; not pushed; the portal candidate path is the CTO's).

## What the cells found

- **`DB-b-216` (account-return derivation and tie-out):** the method is the Schwab engine's, re-implemented as a pure function for Inflection (the engine has no firm-neutral part): `r_t = (V_t - F_t) / V_(t-1) - 1`, flows summed over every partition day since the prior day, `None` and never zero where a value is missing. Tie-out against Orion's reported client return, quarter to date only: **287 clients compared, 33 not comparable; 16 within 5 bp, 87 within 5 to 25 bp, 175 within 25 to 100 bp, 9 at 100 bp or more.** So the derivation is near Orion's figure, not equal to it; the record assumes no tolerance and says so. **Year to date, last 12 months and since inception compare for 0 of 320 clients**: Orion `fact_positions` has no partition for two NYSE trading days (2026-07-01 and 2026-09-28) and the engine's link through intervening valuations is not applied. Rows `W174-S1` to `S5`, dispositioned in `D2-S35`.
- **`DB-b-214` (one Inflection household in memory):** 5 accounts, chosen by the hash rule; as_of 2026-10-13 (the newest positions date on or before the last date of the served series); 32 of 32 benchmark members filled. The household return stays `NO_SOURCE_YET` as the contract sources it. The allocation is absent in words (no seven-class placement from the granted sources).
- **`DB-b-215` (first Inflection render):** the SAME components and the SAME whole-document and note-level rules render it, in the registry's Inflection Wealth Management title. 259 cells scanned (194 absent, 0 unmapped, 0 conflicts), 34 notes, both planted mutants caught, 20 PDF pages, 0 clipped. Two plain sentences, keyed by member and not by firm: "Account-level returns are not available for this firm yet." (5 account notes) and "Lot-level detail is not available for this account yet." (6 notes). Three generic render fixes (member-keyed sentences; a not-held window keeps its ending value; wrapped rows cost their lines in the page estimate), no firm-keyed edit; suite 1298 pass, the same 5 base failures, lint and typecheck 0 errors. Orion guard state: FAIL (expected 4997 objects, landed 5001, 4 alien, none read), named in the record.

## What this seat read for itself

I re-ran each criterion in the worker's tree and on the landed tree, re-validated the proof instance (VALID), scanned the changed workspace and portal files for identifier-length digit runs (hashes and a dated folder name only), and parsed the merged channel (465 rows, 0 duplicates, every worker row present once). I read **5 of the 20 final pages as images** (1, 5, 7, 10, 17): the firm title is Inflection's and nothing else names the plumbing; every unavailable line reads as plain words beside no figure it denies; the layout is the 49 Financial layout. **What I saw that the CVO should weigh:** (a) account labels are four-digit ordinals ("Account ending 0001"), set by my relabel ruling so no real number prints, but "ending" reads as an account number; (b) the first account prints an ending value of $0 beside four benchmark rows; (c) on page 17 the lot sentence sits at the page top apart from its section heading; (d) the holdings table splits across two sheets. I did not read pages 2-4, 6, 8-9, 11-16, 18-20. **Not a grade; `DB109-2-J1` is the CVO's.**

## Issuer errors this round (mine, disclosed)

`DB-b-214` first required a household return fill that the contract's ABSENT source refuses (amended, row `W173-S1`); `DB109-2-AC1` required an unheld class entry and a printed household net gain that this sample does not hold (amended, row `D2-S36`); my note-level rule misses a short-form omission sentence that names no member (row `D2-S33`, accepted, fix queued).

## Rows held (owners named)

`W173-S9` (ARMED, this seat's): disarmed in `D2-S36` by the relabel rule. `W174-S2` (BLOCKING, partial): the two missing days, dispositioned in `D2-S35` as one repair (link through missing valuation days) for the next enrichment list. `W173-S8` ruled. `W173-S10`, `S11` and the rest: OBSERVATION, INERT, no ARMED row has a dark owner.

## What goes to the CTO (one ask, in the slug)

Whether household returns may be filled from Orion's client grain (a contract and gold design decision for every firm). Carried with it as data facts, not asks: the real last-four rule for a custodian number that is not digits-only; Orion's `isActive` false rows with a non-zero currentValue (19,390 of 2,057,322 account-day rows, included in the value basis); the `day_quality` and `guard_state` words for computed-but-unguarded.

## What this does to the FWD outcomes

Inputs to `FWD-2` (any firm's account loads the same way) and `FWD-21` (a household at each of three firms): not met. Inflection now renders one household through the same components with plain words where it has no source, and a derived account return that ties to Orion for the quarter only; it has no gold table, no account return for the longer windows and no served page. Cottonwood stays blocked on ADVI_COTBKF's silver. Grading either FWD is the CTO's and CVO's at L10.

## Open

**Andrew's call a252** (name the 49 Financial template set or its disclosure page). **DB-b-183 L3**: read the first scheduled D_04 run after the 12:08:39Z upload (about 23:00Z); no timer is set.

-- 2.0.0_SA_COO~D2
