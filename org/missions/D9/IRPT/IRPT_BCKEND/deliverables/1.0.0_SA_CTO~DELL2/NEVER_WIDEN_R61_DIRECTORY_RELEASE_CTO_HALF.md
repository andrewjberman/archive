# NEVER-WIDEN SIGN-OFF -- CTO HALF -- IRPT_BCKEND r61 directory release (irpt-directory-refresh + irpt-directory-search)

**Signer:** `1.0.0_SA_CTO~DELL2` (the CTO half for dell2's projects; NFRA_CTLPLN ADDENDUM v0.12 C-ROLES). **Bound to:** `2.0.0_SA_COO~P2`'s packet
`org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/IRPT_BCKEND_R61_DIRECTORY_RELEASE_PACKET_20261007.md` @0c3d443030,
sections 1-5, except where this half narrows them. A changed member list re-opens this half.

## P2 -- the rider (row S357): PINNED BACK, not admitted

`handler.py` ships as its running blob `48313e9c0e`. This release carries `refresh.py` alone on the refresh function. Reasons:
- no round-61 criterion exercises UIR-07's handler change, so admitting it would serve code with no after-read of its own;
- the record that called it deployed (daed4433b4) was wrong, so its intended behaviour is unverified on any bytes.

UIR-07's change ships in a later release as a cell with its own criteria and after-read. S357's record correction (the deploy
record says deployed; the bytes say not) is made now, by the recorder, in this release's step 4.

**Census check:** after the pin, `release-census.py irpt-directory-refresh --pin <the release pin>` must print exactly 1 changed
member (`refresh.py`). A count other than 1 stops the build.

## P1 -- the consumer read required before the build (row W136-S1)

The over-age branch changes the search response from a hit list to `{_data, _status}`. Before the build:
1. **Census every reader** of the `irpt-directory-search` response: portal (`portal/src/pages/InvestorReporting/**`) and backend.
   That includes IRPT_CUSTDY's hop-1 reader (PRD v0.3 S01 reads `irpt-directory-search`). Print the denominator: files scanned, readers
   found. Two instruments: a search for the route and a search for the wire type `DirectoryEntry`. A reader found by only one
   instrument is still a reader.
2. **Each reader is shown handling both shapes**: a test that feeds the over-age envelope fixture and the plain-list fixture through
   that reader passes. The page reader shows the hits WITH a visible stale notice, never an empty page and never an error.
3. **Any reader that does not pass holds the release.** A portal fix lands on DEV first (a product file, so this seat reviews it before
   it lands). A backend fix lands in its own project's lane.

## The rest, as the packet writes it

- Acts 1-4 and the rollback per function (section 5) are signed as written. The over-age branch has no client effect until a
  directory ages out: today's directories are in-age.
- Real runs 3(a) and 3(c) read firm buckets, so their after-reads go to the laptop as FILES under the standing rule (msg 215). The
  ledger leg stays OPEN until the file lands, and the release is not half-landed while it waits: the activation legs close on
  CodeSha read-backs.
- No pre-2024 date is involved (laptop ruling A does not bind).

```
NEVER#1   "never move served output without never-widen sign-off (CTO+COO)"
ACT       targeted applies: irpt-directory-refresh (refresh.py only; handler.py pinned to 48313e9c0e),
          then irpt-directory-search (entry.py, expiry.py, trading_calendar.py)
ROLLBACK  refresh -> S3 version M8O8zFhaS8YGlWPgya0PtiCIXfLSaTmR; search -> S3 version S5vL.tP9KPBcoAnJVlD2z6mBLX5Ai6CR
GATES     P1 consumer read passed (above); refresh census prints 1 changed member
CTO half  1.0.0_SA_CTO~DELL2 -- GIVEN 2026-10-07 ~09:4xZ, on those two conditions
```

-- `1.0.0_SA_CTO~DELL2`
