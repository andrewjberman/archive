# MDPF_TAXSMA.TO-TX-m-1 -- result record

**Worker** `0.9.0_WK_MDPF_TAXSMA~2` · **cell** `TX-m-1` (PRD surface S03, FWD-1/3) · **branch**
`wk-mdpf_taxsma-1-2c` in `C:/tmp/wk-taxsma-2c` · **cut base** `fa353c4c29` (the COO's drain commit for
`TX-b-2`, the input cell). **Spec:** the PRD @671925aecc and `org/standards/MDPF_TAXSMA_DATA_CONTRACT.json`
v0.5.0 (`status_axes`, `membership`, `valuation.history_fields` siblings), whose enumerations are the only
vocabulary used. **Input:** `TX-b-2`'s typed Silver builder (`data/mdpf/scripts/silver/taxsma_workbook.py`,
drained @fa353c4c29), whose `read_parquet_bytes`/`LocalSilverStore` this cell reuses directly; this cell
never imports `taxsma_snapshot` (the Bronze acquirer, TX-b-1) or references a `BronzeStore` of any kind.

Every value below names its instrument, the UTC time it was measured and its denominator.

## 1. What was built

| Path | What | Instrument / evidence |
|---|---|---|
| `data/mdpf/scripts/gold/taxsma_membership.py` (new) | S03: reads the S19 Silver parquet + file metadata only, classifies every row into one `business_status`, computes `business_active_accounts` with its 3 nulling arms, emits append-only OBSERVE_TRADED/OBSERVE_INACTIVE dispositions (idempotent, order-conflict-aware, UTC-dated), reads manual/legacy dispositions as inert evidence, resolves a valuation date's membership status, and computes the dispositions key at the ONE `address()` call site | `git status --porcelain` (untracked pre-commit), this record's own reads |
| `data/mdpf/tests/taxsma/test_taxsma_membership.py` (new) | 29 tests, `test_ac1_` .. `test_ac23_`, one or more per criterion; synthetic Silver snapshots and `LocalDispositionStore`/`LocalSilverStore` only, no `taxsma_snapshot` import anywhere | `py -3.12 -m pytest ... -q`: `29 passed in 0.60s` |
| `org/missions/D8/MDPF/MDPF_TAXSMA/deliverables/0.9.0_WK_MDPF_TAXSMA~2/probes/tx_m_1.py` (new) | the criterion probe: one AC per invocation, fresh subprocess, vacuous-pass refused | 23 of 23 `AC1`..`AC23` invocations below |

**Design decisions this cell makes that the contract does not fix (declared, not hidden -- see module
docstring "DESIGN DECISIONS" and s.3 below):**
- `status_axes.business_status` also names `REMOVED_UNCONFIRMED` (an unresolved prior traded removal/rekey,
  a reconciliation-level outcome `TX-m-2` can see and this single-snapshot cell cannot); `classify_rows`
  never returns it.
- Per-row classification only escalates a NO to `INACTIVE_CONFIRMED` when the caller supplies a
  `previously_traded` lookup (the disposition store's own open-interval state); the bare stateless call the
  full-sheet AC2/AC3 fixtures use classifies every first-seen NO as `UNTRADED`.
- This cell's own light, structural account-identity check (`normalize_account_key`) is NOT the full
  custodian/master reconciliation match `TX-m-2` performs; it exists only to decide CONFLICT-vs-TRADED_CLAIM
  and the AC8 nulling arm, and this cell reads no custodian, master, BD-enrollment or value source at all
  (AC5, verified by both a fixture count and an AST/token call-site census).

## 2. Criteria -- 23 of 23 PASS by output

Instrument: `cd C:/tmp/wk-taxsma-2c && timeout 120 py -3.12 org/missions/D8/MDPF/MDPF_TAXSMA/deliverables/0.9.0_WK_MDPF_TAXSMA~2/probes/tx_m_1.py AC<n>`,
run at HEAD `fa353c4c29` (2 of the 2 files under test dirty -- new, pre-commit; the same 2 files, unstaged,
committed in this order's own commit below), 2026-09-21T04:54Z. Each run prints its vintage, its measurement,
its denominator and exactly one `VERDICT:` line; rc 0 on all 23.

| Criterion | Deciding measurement | Denominator |
|---|---|---|
| AC1 | no Bronze module/store token anywhere in the module under test; a harness holding only a `LocalSilverStore` (no `LocalBronzeStore`/`BronzeStore` object exists in the test) still classifies (`business_active_accounts=1`, `freshness=CURRENT`) | 2 of 2 sub-tests passed |
| AC2 | 7-row fixture (traded, funded-but-untraded, prospect, blank, total, 2 conflicting-duplicate) -> counts `{'TRADED_CLAIM': 1, 'UNTRADED': 1, 'PROSPECT': 1, 'BLANK': 2, 'CONFLICT': 2}` | sums to 7 of 7 rows, each in exactly one `business_status` |
| AC3 | 13 `Traded` fixture values (trim/casefold variants of yes/no/blank, plus a garbage string, a bare letter, an INTEGER/BOOLEAN/FLOAT scalar) parsed to the expected label | 13 of 13 cases matched |
| AC4 (difference) | before=0; engaged (Traded No->Yes) -> 1 (+1); disengaged (Ready flip only, Traded unchanged) -> 0 (unchanged); confirmed the module contains no `AUM`/funded-balance token at all (not a shipped business column) | before/engaged/disengaged: 0/1/0 |
| AC5 | 2-key fixture (2 distinct validated YES keys, 1 NO) -> `business_active_accounts=2`; AST import census + 9-token source scan for custodian/master/BD-enrollment/value-source references | 0 of 9 forbidden tokens present; 2 of 2 sub-tests passed |
| AC6 | 2 rows sharing 1 full key, both YES -> both `business_status=CONFLICT`, count=1, no nulling reason | 1 count, 2 of 2 rows CONFLICT |
| AC7 | a YES row with a structurally invalid identity -> `business_status=CONFLICT` (never `PROSPECT`), `traded_label=YES` retained, reason `INVALID_ACCOUNT` | 1 of 1 fixture row |
| AC8 | 3 nulling arms, each its own test: invalid identity on a YES claim -> null + `INVALID_ACCOUNT`; unknown Traded on an identified account -> null + `TRADED_STATUS_UNVERIFIED`; nonempty UNRECOGNIZED row -> null + `MEMBERSHIP_CONFLICT` | 3 of 3 arms produced `None` (never a smaller positive number) |
| AC9 | a raising `get_body` -> null + `STALE` + `SOURCE_UNAVAILABLE`, last-good (7, "2026-09-15") carried forward; non-parquet bytes -> null + `STALE` + `SOURCE_SCHEMA_INVALID`, last-good (4, "2026-09-14") carried forward, never an empty/zero census | 2 of 2 failure arms, both carried last-good forward |
| AC10 | a first-observed YES at `2026-09-16T14:00:00Z` -> 1 `OBSERVE_TRADED` event, `effective_date=2026-09-16`, `membership_date_basis=FIRST_OBSERVED_UTC`, `actor=S03_MEMBERSHIP_SERVICE`; `is_open=True` | 1 of 1 event emitted |
| AC11 (difference) | engaged: explicit NO on 2026-09-12 closes exclusively that day (`is_open` False; date-status `OBSERVED_TRADED` on 09-11, `OBSERVED_INACTIVE` on 09-12 itself); disengaged: blank/invalid Traded on the same later date emits no event, `is_open` stays True | before/engaged/disengaged: open->closed vs open->open |
| AC12 | YES(01-01) -> NO(02-01) -> YES(03-01) on one key -> 2 `OBSERVE_TRADED` events retained at both `2026-01-01` and `2026-03-01` (the earlier interval is kept, not overwritten); `is_open=True` | 2 of 2 OBSERVE_TRADED events present |
| AC13 | `Inception Date`/`Last Trade Date` each set to `2020-01-01` on a YES row observed at `2026-09-10` -> `effective_date=2026-09-10` in both arms; AST subscript census over the whole module finds 0 reads of `Inception Date`/`Last Trade Date`/`source_modified_at`; `effective_date()`'s only parameter is `source_observed_at` | 0 of 3 forbidden-field subscript reads; 2 of 2 field arms unmoved |
| AC14 | `2026-09-16T00:30:00Z` -> `effective_date=2026-09-16` (never `2026-09-15`); an explicit `-04:00` offset still resolves to its UTC calendar date (`2026-09-16T20:30:00-04:00` -> `2026-09-17`) | 2 of 2 timestamp arms UTC-dated |
| AC15 (difference) | engaged: account observed only once (day 2026-09-10) -> `2026-09-05` (before it) is `UNVERIFIED` + `TRADED_HISTORY_UNVERIFIED`; disengaged: an earlier complete open(09-01)/close(09-03) cycle before a later reopening(09-10) -> `2026-09-05` reads `OBSERVED_INACTIVE` | before-first-observation=`UNVERIFIED`; covered-by-earlier-NO=`OBSERVED_INACTIVE` |
| AC16 | the same classifications processed twice (two calls standing in for two run UUIDs, since the module accepts no run_uuid parameter at all) -> 1 event total, second call returns `[]`, `source_event_id` identical, date unmoved; module source contains no `run_uuid` token | 1 of 1 event (not 2) |
| AC17 | an in-order YES(09-01)/NO(09-10) cycle closes the account (`is_open=False`); a late-arriving OLDER snapshot (YES at 09-05, between the two) is retained with `TRADED_EVENT_ORDER_CONFLICT` and `is_open` stays `False` (unchanged) | 1 of 1 conflict-flagged event; current state unmoved |
| AC18 | two accepted automatic events at the identical `source_observed_at` with differing `traded_value` -> `DispositionConflictError` raised (proven both via the emission pipeline and a direct manufactured-conflict store append) | 1 of 1 conflict raised |
| AC19 | YES at 09:00Z and NO at 15:00Z on the same UTC calendar day -> both events retained (2 of 2), both dated `2026-09-16`, `is_open=False` (the later, 15:00Z, NO governs) | 2 of 2 events retained |
| AC20 | each of the 3 `MANUAL_DISPOSITION_KINDS` (`CORRECT_IDENTITY`, `CONFIRM_TRANSFER`, `RESOLVE_STRATEGY`) appended alone (no source YES) -> `is_open=False` in every case | 3 of 3 manual kinds non-activating |
| AC21 | a legacy `CONFIRM_EFFECTIVE_MEMBERSHIP` record appended -> retained in `events_for` (historical evidence) but `is_open=False` and `resolve_date_status` reads `UNVERIFIED`+`TRADED_HISTORY_UNVERIFIED` (the legacy record carries no automatic evidence) | 1 of 1 legacy record inert |
| AC22 | `dispositions_address()` resolves to `s3://.../dispositions.json`; exactly 1 `address()` call site in the whole module, AST-located inside `dispositions_address`; resolved value equals a direct `address("mdpf","49financial","state","taxsma_membership","dispositions.json")` call | 1 of 1 call site |
| AC23 | AST call-name/call-attr census: 0 of 10 forbidden write-call tokens (workbook/BD-roster/trade/order/access-grant) present; 0 `put_object` call sites anywhere in the module (`S3DispositionStore.append` itself refuses); no `httpx`/`requests` import, no `graph.microsoft.com` or live SharePoint site identifier in source | 0 of 10 forbidden calls; 0 write call sites |

**Controls.**
- **MUTANT** (AC18): removed the `LocalDispositionStore.append` conflict-detection branch (a second
  accepted event at an existing `source_observed_at` with a differing `traded_value` fell through to a
  silent append instead of raising) -- `test_ac18_two_conflicting_snapshots_at_one_observed_at_refused`
  FAILED (`Failed: DID NOT RAISE <class 'taxsma_membership.DispositionConflictError'>`), probe printed
  `VERDICT: FAIL-TXM1-AC18`. Reverted; re-run: `1 passed`, `VERDICT: PASS-TXM1-AC18`. FIRED-AS-EXPECTED.
- **DETERMINISM**: AC1 run twice back to back; outputs diffed with the `vintage:`/`elapsed:` lines and
  pytest's own embedded per-run timing (`in 0.6Xs`) stripped from each side -- identical apart from that
  timing noise. STABLE.

## 3. Bounds and exclusions

- No egress: no call to a live route, Microsoft Graph or SharePoint (no `httpx`/`requests` import, no
  `graph.microsoft.com` or live site identifier in source or tests); no `S3DispositionStore`,
  `S3SilverStore` or `S3BronzeStore` constructed by any test (`test_no_live_route_or_s3_call_site_is_executed_in_this_test_module`).
  No real S3 write; `S3DispositionStore.append`/`events_for` raise `NotImplementedError` -- a later release
  cell's to build and prove live, never this one's.
- No private data: fixture account numbers are synthetic, already-normalized ten-digit `00`-prefixed forms
  (`0000012345`, `0000099999`, `0000055555`, `0000011111`); no client name, real account number, balance,
  token or credential appears in the module, tests or this record.
- The dispositions key is `address()` output at exactly one call site (`dispositions_address`, AC22).
- Full custodian/master/strategy reconciliation (`TX-m-2`), case evidence (`TX-m-3`), dated valuation
  (`TX-m-4`), and the pipeline wiring that invokes S03 on a successful S19 build are out of this cell's
  scope; declared in the proof-of-spec instance.

## 4. Surprises

None filed. Every criterion as written was met without a route this order does not name; no premise failed
and no needed path was missing from the grant.
