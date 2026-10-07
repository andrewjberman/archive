# The pool crosswalk rebuild's difference, explained -- a READ-ONLY act (`2.0.0_SA_COO~Z`, 2026-10-07 ~09:5xZ)

Step 1 of CTO ruling msg 30760 on row `AMGT_RESAPP-Z-S363`. Nothing was written to the store and no Bloomberg call was made.

**What was compared.** The served object `s3://opal-data-harvest/crosswalk/v1/2026-09-29.json` (newest of 6 keys, 237 records)
against an in-memory build by `add_security._build_document(<today UTC>, ...)` over the 71 rows of
`lib/research/identity/registrations.json` at HEAD, with NO new row. Per-record JSON comparison, key by `security_key`.

## The answer in one paragraph

Every difference traces to TWO input changes and nothing else. (1) The identity universe input moved from
`universe/v1/2026-09-16.json` to `universe/v1/2026-10-06.json` (written 2026-10-06 04:10:10Z; 3 keys under that prefix). The
newer file writes each name's `ticker` WITHOUT the " Equity" suffix and carries a longer `resolution_reason`; it holds 302 names
against 250 (243 keyed against 192; 51 keys added, 0 removed). (2) The coverage list's path moved from a worker folder to
`lib/research/identity/data/universe.json`. No `security_key`, `bloomberg`, `association_keys`, `exchange`, `model_key`,
`resolution` VALUE or `source_row.folder` changes on any of the 237 records.

## The three fields, by cause

| field | records changed (of 237) | cause | the change |
|---|---|---|---|
| `raw_identifier` | 158 | cause 1 | 158 of 158 are the universe-sourced records; 158 of 158 follow one pattern: the served value equals the rebuilt value plus " Equity" (`2602335D US Equity` -> `2602335D US`). 0 follow any other pattern. |
| `source_row.bloomberg_ticker` (`value`, `evidence`, `resolved_at`) | 158 | cause 1 | the same 158; `value` loses " Equity", `evidence` gains the newer file's added sentences (a second SEC ticker-table read of 2026-09-22, and the holdings-line join) |
| `source_row.coverage_source` | 191 | cause 2 | the path string only |
| `provenance.source_row` | 191 | cause 2 | the path string only |
| `provenance.resolution` | 158 | cause 1 | the longer reason text |
| `provenance.resolves_coverage_record` | 40 | cause 2 | the path string inside the sentence |
| `provenance.bloomberg`, `provenance.raw_identifier` | 33 each | cause 2 | the path string; `provenance.bloomberg` also reads "normalised to upper case only" where the served text reads "normalised" (a wording change in the builder since 2026-09-29, not traced to a commit here) |
| any other field | 0 | -- | -- |
| `source_row.folder` | 0 | -- | unchanged on all 237 |

Records changed in any field: 231 of 237. Records equal after replacing only the moved coverage path: 73 of 231; the other 158
are the universe-sourced records of cause 1.

## The 5 added records

`BE_US_Equity`, `DG_US_Equity`, `ED_US_Equity`, `GEV_US_Equity`, `MRNA_US_Equity`. Each is `MEASURED`, sourced
`s3://opal-data-harvest/universe/v1/2026-10-06.json :: names[]`, resolved "through the Positioning chain" on the
`bbg/<date>/characteristics` plane: they are names the Opal ETF books hold that the newer universe file added. Denominators
served -> rebuilt: `universe_names` 250 -> 302, `universe_registered` 158 -> 163, `universe_existing` 33 -> 79,
`universe_refused` 59 -> 60, `records` 237 -> 242, `research_folders_live` 96 -> 97. Keys only in the served object: 0.

(The same five are among the 15 names the MDPF_SECHIST history backfill plans. That is a coincidence of source, both read the ETF
books; it is noted, not relied on.)

## Readers of the three fields (non-test code; one search over `*.py`, `*.ts`, `*.tsx`, `*.js` repo-wide, then each hit read)

| reader | reads | project | does the rebuild change what it reads? |
|---|---|---|---|
| `lib/research/api/name_search.py:33` | `source_row.folder` | RESAPP (the `/resolve` route) | NO: folder unchanged on 237 of 237 |
| `lib/research/identity/coverage_residue.py:151`, `covered_keyed.py:30` | `source_row.folder` | RESAPP | NO |
| `lib/research/identity/build_universe.py:788-798` | `source_row.folder`, `provenance.resolution`, and `raw_identifier` only as the fallback when `bloomberg` is empty | RESAPP | `bloomberg` is empty on 0 of 237 served and 0 of 242 rebuilt records, so the fallback is not taken; `provenance.resolution` text it copies is longer on 158 records |
| `lib/research/corpus/backlog.py:60-61` | `source_row.bloomberg_ticker` status and evidence, from a `resolve()` hit | CORPUS | YES on the 158: the evidence text is longer and `value` loses " Equity". Whether backlog compares `value` to anything was NOT traced |
| `lib/research/posture/membership.py:147-320`, `posture/comparable.py:207-218`, `peers/engine.py:265-286` | a `raw_identifier` key on their OWN identity dicts | RESAPP | NOT settled here: these build the key from the form or ticker they were handed (`form.get("raw_identifier") or key`, `"raw_identifier": ticker`). Whether a pool record's `raw_identifier` flows into `form` or `result` was not traced end to end |
| `portal/src/pages/SecurityAnalysis/types.ts:503` | `identity.raw_identifier?` (optional, a type) | DSGN page | follows the row above; the page component that renders it was not read |
| `lib/research/identity/positioning_chain.py`, `filings/analyze.py` | a local argument or variable of the same name | -- | NO: not the pool record's field |
| HARVST: `lib/opal_data_harvest/depth_census.py` names the crosswalk | not opened line by line | HARVST | row `AMGT_HARVST-Z-S95` (filed 09:05Z by `2.0.0_SA_COO~H`) reads the research-folder name from the crosswalk: `source_row.folder`, unchanged on 237 of 237. The 5 added records carry no folder |

Denominator of the search: 114 files repo-wide name `raw_identifier` or `source_row`; the hits outside `lib/research/` and the
one portal type are other projects' own fields of the same name (rival funds, investor reporting) and were not opened.

## What this read does NOT settle

1. Whether `raw_identifier` on a pool record reaches the peers or posture identity dict and the page (the three rows above).
2. Whether CORPUS's backlog compares `bloomberg_ticker.value` to a suffixed form.
3. Whether the five added names are wanted in the pool, and who produced `universe/v1/2026-10-06.json` and why its `ticker`
   form changed. That file's producer was not identified here.
4. The Lambda packages: `opal-amgt-scoped-api` reads the pool at request time; which fields its packaged code reads was taken
   from the repo files above at HEAD, not from the deployed artifact.

## Recommendation for step 2 (the re-mint's pair)

The re-mint is safe on the keyed fields (0 changes) and the folder (0 changes). The two open questions that bound its blast
radius are items 1 and 2. They are one trace each; the re-mint half should carry both answers, or a five-name before/after read
of `/overlay` peers and of the CORPUS backlog on universe-sourced names.

## ADDENDUM 1 (~10:0xZ) -- the two traces this read left open, both run

**Trace 1: does a pool record's `raw_identifier` reach the peers and posture identity? YES for peers, NO for posture; nothing
compares it and the page does not render it.**
- `crosswalk.resolve()` returns the pool record's own `raw_identifier` on a hit (`lib/research/identity/crosswalk.py:1234`).
  Exercised on the served object: `resolve("2602335D_US_Equity")` and `resolve("AMD_US_Equity")` each return `MEASURED`,
  `matched_as model_key`, `raw_identifier "<root> US Equity"`.
- `lib/research/peers/engine.py:265` copies that value into the peer's identity dict. So after a re-mint, a universe-sourced peer's
  `identity.raw_identifier` reads `<root> US` where it reads `<root> US Equity` today, on up to 158 names.
- `lib/research/posture/membership.py:147-176` and `posture/comparable.py:207-218` set `raw_identifier` to the key or the ticker
  they were handed, never to the pool record's value. Unaffected.
- Uses of the value: the three hits in `peers/engine.py` are assignments; no comparison on `raw_identifier` was found in
  `lib/research` non-test code. In `portal/src` the name appears ONCE, the optional type field at
  `pages/SecurityAnalysis/types.ts:503`; no component reads it. So the change is carried in the served JSON and shown nowhere.

**Trace 2: does the CORPUS backlog compare `bloomberg_ticker.value`? NO.** `lib/research/corpus/backlog.py:57-62` reads
`bloomberg_ticker` status and evidence only to word the reason of a hit that has NO `security_key`. The 158 changed records are
all `MEASURED` with a key, so that branch is not reached for them; `value` is never read there.

**One served change the first read under-stated: the 5 added names become resolvable.** On the served object
`resolve("BE_US_Equity")` reads `UNRESOLVED` (and `CSCO_US_Equity`, a name outside both objects, reads `UNRESOLVED` as the
control). After a re-mint BE, DG, ED, GEV and MRNA resolve `MEASURED`. Wherever one of the five appears as a peer or a comparable
member, its identity moves from unresolved to keyed. That is the intended effect of the newer universe input, and it is the one
visible change of the re-mint.

**One more read: `python -m lib.research.identity.crosswalk --as-of 2026-10-07 --disclosure`** (read-only by its own contract)
prints `folders_in_records 96 research_folders_live 97 snapshot_input_names 89 snapshot_stale_against_live True`: one live
research folder is not in the coverage snapshot the build reads. The re-mint does not add it; it is named so the half does not
claim the pool is current against the folders.
