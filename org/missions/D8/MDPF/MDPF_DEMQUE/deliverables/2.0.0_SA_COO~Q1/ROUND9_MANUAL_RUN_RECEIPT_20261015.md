# The first run under the active-set gate: receipt (2.0.0_SA_COO~Q1, 2026-10-15 ~9:15 PM ET)

Run: scheduled task `Opal MDPF_DEMQUE daily draw`, started BY HAND with `schtasks /Run` at 7:54 PM ET (23:54:42Z) on Andrew's word ("do yahoo runs now"); same wrapper, same log (`.git/demque-daily-draw.log` from line 141), schedule unchanged. It finished at about 9:08 PM ET with `OK: daily draw complete`, exit 0. Covered by the signed never-widen pair (COO half @5e62883899, CTO half @55b747d57c): the same code writing the same keys; the stop (a non-zero exit or a write outside the table) did not fire.
Read AFTER it finished, read-only: the log summary line, `~/.opal/demque/pacer.json`, S3 `list_object_versions` under `yahoo/global/silver/price_history/` against `STORE_BASELINE_AFTER_2026-10-14_RUN_VERSIONS.csv` (538 names), and the stored index object itself. Next base: `STORE_BASELINE_AFTER_2026-10-15_RUN_VERSIONS.csv` (696 names, same columns). Check script: `scratchpad/receipt_check.py` (not committed; its output is quoted here).

## 1. What the run did (measured)

| item | value | source |
|---|---|---|
| Yahoo requests (pacer, local day 2026-10-15) | 400 of 400; no pushback; factor 1.0 | `pacer.json` |
| new names written (first pull, LOCKED) | 158 | summary `stored` reason `ok` |
| incremental APPENDED | 6; 3 of them without a relock (a trade predates the stored window), listed | summary `incremental` |
| held (HELD_RESTATEMENT) | 0 | summary |
| not stored (REJECTED, nothing written) | 102: 66 `PRICE_MISMATCH`, 36 `LOW_TRADE_AGREEMENT` | summary `stored` |
| V2-held entries skipped by the Yahoo gate | 815 | summary `skipped_excluded` |
| index rows | 696 (was 538; +158) | summary, index object |
| unresolved rows | 508 (was 271) | summary |
| ledger uploaded | `yahoo/global/bronze/demand_ledger/dt=2026-10-15/ledger.jsonl` | log |

## 2. The run's claim against the store (the check that matters)

| check | result |
|---|---|
| keys the run says it wrote (incremental) | 9; actual changes on the 538 baseline names: 6 `lock.json` and 3 `prices.parquet` = 9, each on a name in the run's appended list; 0 changed outside it |
| new names | 158, each with all four files (`prices`, `splits`, `dividends`, `lock`): 632 new keys; equals the run's 158 `ok` |
| keys outside the pair's table | none: the only other changed keys are `index/index.parquet` and `index/index.csv` |
| V2-held names touched | 0 among the 538 baseline names; 0 among the 158 new names |
| `use_class` on the stored index | 528 `NOT_FOR_ACTIVE`, 168 `INACTIVE_USE`; 0 rows whose label disagrees with V2 membership (the 168 are the 10 inactive names already stored plus the 158 new ones) |
| `porting_verdict` | 696 `UNVERIFIED` (no verdicts file) |

## 3. A trap in my own check

My first read of the index called `price_store.index(root)` with no V2 set, which is the fail-closed default (every row `NOT_FOR_ACTIVE`), and it briefly looked like the run had written the fallback. The stored object was read directly and is correct. A reader checking `use_class` reads the S3 object, not `index()` without its `active` argument.

## 4. What this means for the backfill

The 400-request day drew the standing request, then backfill files 01 and 02 (`PARTIAL`: 615,301 and 249,943 cells), none of files 03 and 04. 102 of the 267 names the run processed were rejected by the identity lock (`REJECTED`), so about 38 percent of the names a night reaches do not write; they enter the unresolved list as the lock rule says (no looser rule, CTO msg 5411). At about 270 names a night, the 1,071 symbolled names are about four nights at the cap, not three.

Push state: LOCAL (box/dell1), not pushed by this seat.
