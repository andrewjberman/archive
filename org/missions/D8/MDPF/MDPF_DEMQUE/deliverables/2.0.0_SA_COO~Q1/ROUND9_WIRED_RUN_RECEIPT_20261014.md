# The first WIRED Yahoo run: receipt read against the version baseline (2.0.0_SA_COO~Q1, 2026-10-15 ~03:50Z)

Run: scheduled task `Opal MDPF_DEMQUE daily draw`, 22:30 ET 2026-10-14 (02:30:02Z 2026-10-15), the first night with the Yahoo incremental path wired (t-58, pair A), the `porting_verdict` column (t-59), the share-class symbol form (t-62) and the B1 builder changes merged. Log `.git/demque-daily-draw.log` from the line `=== 2026-10-15T02:30:02Z demque daily draw task (dell1)` to `OK: daily draw complete`. Pacer attempts 02:33:21Z to 03:29:53Z.
Read AFTER the run finished (`OK: daily draw complete`, ledger uploaded to `yahoo/global/bronze/demand_ledger/dt=2026-10-14/ledger.jsonl`). Read-only: the log, the run's own summary line, the pacer state and S3 `list_object_versions` under `yahoo/global/silver/price_history/`. Andrew's "Go" (2026-10-14 ~20:5xZ) authorized this read.
Comparison base: `STORE_BASELINE_AFTER_2026-10-13_RUN_VERSIONS.csv` (483 names, every store key's S3 version id after the 10-13 run). Next night's base: `STORE_BASELINE_AFTER_2026-10-14_RUN_VERSIONS.csv` (538 names, same columns, written from the same listing).

## 1. What the run did (measured)

| item | value | source |
|---|---|---|
| names processed (a stored record each) | 297 | the run's `stored` list; equals the 297 symbols the pacer shows OK this run |
| incremental, APPENDED | 181 | `incremental.appended` |
| of which appended WITH the combined-history relock | 131 (all LOCKED) | `stored`: incremental APPENDED, relocked true |
| of which appended WITHOUT a relock (a trade predates the stored window) | **50** | `incremental.appended_without_relock`, listed in the receipt as pair A condition 2 requires |
| held, HELD_RESTATEMENT | 15 listed: 14 failed the combined-history relock (`REJECTED:LOW_TRADE_AGREEMENT`) and wrote nothing; 1 is a duplicate pass (see 3) | `incremental.held_restatement` |
| new names written (first pull, LOCKED) | 55 | `stored`: reason `ok` |
| not stored (REJECTED, nothing written) | 46: 39 `LOW_TRADE_AGREEMENT`, 7 `PRICE_MISMATCH` | `stored` |
| index rows | 538 (was 483: +55) | the run's summary line |
| unresolved rows | 271 (was 225) | the run's summary line |
| keys the run says it wrote | 363 (181 prices + 181 lock + 1 dividends + 0 splits) | `incremental.keys_written` |
| Yahoo requests (pacer) | 319 of the 400 daily cap; no pushback; 297 OK, 20 FAILED_EMPTY, 2 repeat attempts | `~/.opal/demque/pacer.json` |

## 2. The run's own claim against the store (the check that mattered)

For the 483 baseline names, the store's latest S3 version of each of four files, against the baseline:

| file | the run says it wrote | actually changed | claimed, not changed | changed, not claimed |
|---|---|---|---|---|
| `prices.parquet` | 181 | 181 | 0 | 0 |
| `lock.json` | 181 | 181 | 0 | 0 |
| `splits.parquet` | 0 | 0 | 0 | 0 |
| `dividends.parquet` | 1 (`693475105`) | 1 | 0 | 0 |

The other 302 baseline names are byte-for-byte untouched (same version ids). Of the 14 names held on the combined-history relock (`00141B204`, `14064D865`, `412295701`, `464287473`, `464287481`, `464287630`, `464287648`, `4812A1373`, `693390882`, `77958B402`, `922042718`, `922042858`, `92647K309`, `92828R610`): **none changed**. The store holds 55 names the baseline did not (all 55 listed by the run as stored `ok`) plus the `index` key. Denominator: 483 names x 4 files = 1,932 version ids compared, 2,154 (name, file) rows listed in all.

## 3. Wrinkles found, none a defect of the signed pairs

- **`084670702` (the BRKB / Berkshire B CUSIP) is in both lists.** It was APPENDED once (80 new rows, relocked LOCKED, prices and lock written) and then listed HELD_RESTATEMENT with `an appended row is not dated after the stored max 2026-10-14`, written false. Two pulls of the same security under two symbol spellings: `BRK-B` at 02:33:41Z (80 rows, the extension) and `BRKB` at 03:27:29Z (7,657 rows, a queued job); the second found nothing newer and wrote nothing, which is the intended behaviour. The name had been in the 22 empty symbols on 10-13, so this is the first live evidence that `DQ-t-62` works (inferred from the pacer and the stored record; I did not read the fetch code path again). Cost: one duplicate Yahoo request.
- **The queue ran to exhaustion, not to the cap.** 317 distinct symbols attempted: 297 OK, 20 FAILED_EMPTY; 773 of the 794 symbols the pacer knows are now OK, and the 21 that are not are all FAILED_EMPTY (delisted names, and money-market symbols `FZAXX`, `FIGXX`, `VMMXX` where yfinance says `Period 'max' is invalid, must be one of: 1d, 5d`). Last night the run hit 398 of 400 requests; tonight 319. The three P1 jobs read PARTIAL because of those permanent failures, not because the budget ran out.
- **The ledger's quote no longer compares with the draw.** The standing extension is quoted at 687,960 cells (the full history of 195 symbols) and drew 1,646 (the last five trading days). A reader of `cells_drawn / cells_quoted` sees 0.2 percent; it is the incremental path working, not a shortfall. The other jobs: IRPT P1 12,501 of 81,270 (PARTIAL), R4-P1-SLICE-1 3,322 of 516,900 (PARTIAL), R2-PILOT-50 0 of 172,350 (PARTIAL, nothing left to pull).
- **Residuals unchanged from the round-9 findings:** 50 names appended without a relock (pair A's named residual, now listed nightly); the 14 stuck names still ride the filed Bloomberg request `MDPF_SECHIST-CARD-A-B1-YAHOO-FAILED-14`.

## 4. For the CTO's round-9 analysis (enrichment candidates, not built)

1. The money-market symbols whose `period='max'` is invalid (`FZAXX`, `FIGXX`, `VMMXX`): a pull-shape defect, three symbols a night.
2. The quote for a standing request should price the incremental window, so the ledger's quoted-versus-drawn ratio reads as intended.
3. Two spellings of one security (`BRK-B`, `BRKB`) cost two requests: key the pacer on the dash form.
4. With the queue exhausted at 319 of 400, about 80 requests a night of Yahoo budget now go unused; the unresolved set (271 rows, +46) is the next demand.

Push state of this file: LOCAL (box/dell1).
