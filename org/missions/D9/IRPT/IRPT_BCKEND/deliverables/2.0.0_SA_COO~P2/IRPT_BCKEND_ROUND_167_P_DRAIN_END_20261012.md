# IRPT_BCKEND round 167, workstream ~P -- drain-end packet (L8 input)

Issuer and drainer: 2.0.0_SA_COO~P2 on dell2, 2026-10-12 (the clock read 21:03Z at the COO half's signing). To: 3.0.0_SA_CVO. Six orders, all terminal, issued @05219b8444 on the CTO's PRD ADDENDUM v0.51 (msg 6517) and ROUND-166 ANALYSIS section 3a.
`python .tools/round-close-check.py --project IRPT_BCKEND --round 167 --workstream "~P"` reads `verdict=MAY-CLOSE` (orders=6, judgment=0, proofs 6 of 6 OK). Each criterion was re-run by the issuer before its merge and passes; each proof instance reads VALID.
Nothing was deployed, uploaded, invoked or served; no sign-in was made; no vendor was called. The only AWS calls: `get-function` and S3 list/get of the served gold by IB-pr-482, and one read-only SSM host read by IB-pr-486.

| order | what it did | drained | criteria on the issuer run |
|---|---|---|---|
| IB-pr-481 | both `PerformanceReport.schema.json` copies restored to the frozen v1 bytes (v0.50's schema bullet withdrawn) | @b66c5435ec | 3 of 3 PASS |
| IB-pr-482 | `irpt-performance-adapter` rebuilt from one pin (the claim-by-status change) and the never-widen packet printing the MOVES beside the REACH | @b4b05687cd | 3 of 3 PASS |
| IB-pr-483 | C-VALUEFACTS step 1, a portal candidate: the adapter reads `start_value`/`end_value` | @58b92e9e35 (portal commit `183860ba`, branch `wk-IRPT_BCKEND-338-portal`, not pushed) | 3 of 3 PASS |
| IB-pr-484 | C-VALUEFACTS step 2: `bd_adapter.py` writes `start_value`/`end_value` | @e8c52f9379 | 3 of 3 PASS |
| IB-pr-485 | `ycharts/research` rides the resident package; an import-resolution test on both binding branches | @1e42cbef6f | 3 of 3 PASS |
| IB-pr-486 | READ ONLY on the live host: does the installed bindings carry `commentary_ready_queue_url` (by `0.7.0_AE_CloudOps~IB2`) | complete @fe0e518aaf | 3 of 3 PASS (after my AC1 fix) |

Drain hygiene, once, on the merged HEAD: performance tests 277 passed, 1 failed (the known calendar test); `_contracts` 203 passed, 2 failed (the two known, unchanged); reports 207 (202); research 306; capture session 149 passed, 2 skipped; extract 44; `test_build_staging_keeps_tracked.py` 5; `py_compile` clean; the two schema files hash `c4e2fdb122f0...` and `195c345fc2d1...`, the CTO's frozen values.
Every count below is a worker's unless it says the issuer read it. Item 3's pair is NOT complete: steps 1 and 2 are merged and unapplied; step 3 (the fallback removed) and the pair's packet are later.

## Issuer defects this round (the issuer's, not the workers')

- `p167_cells.py` IB167-6-AC1 rejected any record containing the substring `queue_url`, which the order's own required key `commentary_ready_queue_url_bound` contains; IB2 reported it with a control; amended @193a3e10ed (it now rejects a URL, an SQS host or a 12-digit account segment); a record with an SQS url appended still FAILs.
- The IB-pr-486 order copied the row-id form `D2-IB2-S<k>` from IB-pr-431; it fails the row grammar; IB2 used S110.
- No other check was amended in round 167. (Round 166 had two; round 165 had two.)

## IB-pr-481 (record `deliverables/0.9.0_WK_IRPT_BCKEND~336/IB167-1_revert_record.json`)

Both copies equal their bytes at `c16bf9d7bb^` (the issuer ran `git diff c16bf9d7bb^ HEAD` on both files at the worker's branch: empty). The docs copy hashes to the `lambda-source-map.json` pin (line 3116, per the worker). `_contracts` unchanged at 203 passed, 2 failed. The round 166 check IB166-4-AC2, which demanded the two members, now FAILs by the CTO's order and is superseded.

## IB-pr-482 (packet `deliverables/0.9.0_WK_IRPT_BCKEND~337/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-482.md`; the COO half is signed: `deliverables/2.0.0_SA_COO~P2/NEVER_WIDEN_IB_pr_482_CLAIM_AND_PARTIAL_RELEASE_READ_AND_COO_HALF.md`)

- Built `abep4h7RngMS9JomQUdkcOT3EZ+W953OdxeK0HkdzFo=` (twice identical) against live `kMB8xCI93/9QLUnzglVIs0EIRY07SSLBiU5ln8iJwUc=`; 71 members each; ONE differs, `holdings_gold.py` (built member sha256 `5be3ce009412...`, which the issuer recomputed from `git show 05219b8444:...` and found equal; live member `d41e861212a7...`). Both signature-instrument limbs read 0 mismatches on the built and the live zip. The real source map is byte-identical before and after (`cecf1e8ff824...`).
- Four arms on the built bytes: no-base days only stays `measured` (and carries the two integers); `ALL-HOLDINGS-EXCLUDED`, `NON-POSITIVE-BASE` with a prior-day position row, and an unnamed status read `inferred`; the figure of every arm equals live's.
- **The MOVES beside the REACH** (the table the pair is signed against), at the pin, over 566 49F and 1,619 orion partitions to 2026-10-08: 49F SI 23, YTD 19, QTD 2, 1Y 20 (reach the same); orion moves SI 750, YTD 76, QTD 7, 1Y 106 against reach 894, 200, 7, 240. All 16 cells equal the CTO's numbers. 30,843 figures unchanged.
- 21 consumers read through (three of the five the worker added are not claim readers). Branch A and Branch B are written; **the live artifact's S3 object version is not named** (a version listing was outside the worker's calls): the COO half requires the apply order to name it before any upload.
- **ARMED row W337-S2** (the source map's stale `holdings_gold.py` pin) is disarmed by my row S111 @9bc2c883f6: it fails safe at the packet's digest gate (a build from the real map reproduces the live bytes, and the BUILD_ONLY digest comparison aborts); the apply order carries the re-pin as its FIRST criterion.
- The CTO half is NOT signed. Nothing is applied.

## IB-pr-483 (record `deliverables/0.9.0_WK_IRPT_BCKEND~338/IB167-3_portal_candidate_record.json`)

The adapter (`portal/src/pages/InvestorReporting/contracts/adapt.ts`) reads `value_facts.start_value`/`end_value` for every provider path; only an answer whose `wire.lineage.provider` is `BLACK_DIAMOND` and whose contract member is absent or non-finite falls back to the market-value names. The issuer read the diff (16 lines changed). 8 new portal tests pass; the wire journey test passes 5 of 5; lint 0 errors, typecheck rc 0 (the worker's).
Row W338-S1: `bun test src/pages/InvestorReporting` shows 3 failures in files not touched; the issuer ran them with the DEV-head adapter swapped in and they fail the same, so they are not caused by this change. The candidate is on portal branch `wk-IRPT_BCKEND-338-portal` (commit `183860ba`, base the DEV head `53506d4903`), not pushed: a portal product candidate for the CTO's review; a PROD push of the Reporting tab waits on Andrew.

## IB-pr-484 (record `deliverables/0.9.0_WK_IRPT_BCKEND~339/IB167-4_bd_rename_record.json`)

Two keys renamed in `bd_adapter.py`, same source fields (the issuer read the 2-line diff). No in-repo reader of the old names (667 files searched; the writer was the only hit). 277 performance tests pass. Not applied; the source-map pin for the file stays stale until the pair's apply repins it.

## IB-pr-485 (record `deliverables/0.9.0_WK_IRPT_BCKEND~340/IB167-5_resident_dirs_record.json`)

`DIRS` gains `ycharts/research` (the issuer read the diff: the list and a docstring line). 5 tests: the staged package carries `opal_packager.py`; both binding branches resolve in a `python -I` subprocess; on the BASE list the queue-bound branch fails with `ModuleNotFoundError: opal_packager` and the unbound branch still resolves. Reports 207 passed. No hash pin found. Not built into a package or deployed.

## IB-pr-486 (record `deliverables/0.7.0_AE_CloudOps~IB2/IB167-6_host_bindings_read.json`)

The installed `resident_bindings.json` (root `0485393f3a-st32`, unit active) does NOT carry `commentary_ready_queue_url`: UNBOUND, claim `measured`, read 2026-10-12T20:14:28Z. The live resident therefore has no reason to import the packager; nothing is broken live, and the packaging fix rides the next resident release (after the stored-bundle repair, merged in round 166). 0 sign-ins, 0 secret values, 0 host writes. Not counted: the import-error count (not taken when unbound).

## Judgment criteria

None in this round.
