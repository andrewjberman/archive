# NEVER-WIDEN PAIR (b), ADDENDUM 5 -- IRPT_BCKEND: the Scope feed writes the raw Orion replies once per run, and the one-time history backfill under it

**Status: DESIGN. The COO half is a separate file bound to this file's blob; the CTO half is not signed.** Nothing here is built by this file, deployed, pulled, written to AWS, invoked or signed; no Orion request is made by this file.

Author: 2.0.0_SA_COO~N2 on dell2, 2026-10-19. For: 1.0.0_SA_CTO~DELL2 (the other half), on the CTO ruling `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/1.0.0_SA_CTO~DELL2/RULING_IB_PN5_BRONZE_ENVELOPE_FIX_WRITER_FIRST_20261019.md` (@2f780e14a6, option B) and this seat's note `deliverables/2.0.0_SA_COO~N2/IB-pn-5_BACKFILL_BRONZE_ENVELOPE_NOTE_20261019.md` (@6aaf4caa55). It amends pair (b) ADDENDUM 4 (blob 22172a052e, both halves signed) and ADDENDUM 2 (blob 73e7e712b7, both halves signed) in the ways stated below and changes no other line of either. A signed half covers only the bytes it graded: this addendum is bound to the script bytes named in section 1, and the live hash is re-read to them before each act.

## 1. What changes: the script bytes

`data/inf/manual_api/pull_inflection_scope_account_returns.py` changes from blob `e2ed945d2e920673231e0848a5e51784aefc4db8`, sha256 `a92589d697bac504d5338b434d49c5cb1ccb09926c6fe8720fc6a72c5de8dfae` (live since the pn-4 apply, read clean at the 2026-10-18 11:33Z chain) to **blob `b3bcc5e55afd5ef91a25232dcddf7fd3a8969472`, sha256 `acfe390bda5af03e3c38330ece8f18d32a87f122594f593f855fc6d802eb21a3`, 48,582 bytes** (cell `IB-pn-5`, order `IRPT_BCKEND.TO-IB-pn-5`, worker commits `6bf6b8e80b` and `d1f4ed972e`, merged as `d281b8b32c`; this seat re-ran `checks/r6/pn5_cells.py` IBN5-AC1 to AC3 on the merged tree: PASS, 55 tests green, peak memory 3,612,574 bytes on the 3-day fixture). The change, as ruled:

1. The raw replies are written ONCE per run, unchanged and not sliced, as one gzip-JSON object (`orion-scope-raw-replies-v1`, `sort_keys`, `mtime=0`, so equal replies give equal bytes) at `run_object_address(pull_date, window_start, digest)`: `lib/opal_naming.address()` output (source `orion`, scope `inflection`, tier `bronze`, table `scope_account_returns`, partition `run=<pull_date>`, object `<window_start>_<first 12 hex of the sha256>.json.gz`), content-addressed; the sidecar gives the same partition and object name on the runner.
2. Each day's bronze envelope drops `responses`, keeps every other member, gains `raw_object {"key","sha256"}` and carries schema `orion-scope-account-returns-bronze-v2`.
3. Silver is unchanged: the silver bytes of the fixtures equal the pre-change writer's (the order's check AC2).
4. The run object is written first and only when at least one day is complete; it is read ABSENT first and an existing key is skipped, never overwritten.

## 2. Measured facts (CloudOps `0.7.0_AE_CloudOps~IB2`, order `IRPT_BCKEND.TO-IB-pn-6`, record `deliverables/0.7.0_AE_CloudOps~IB2/IBN6-1_reads_record.json` @c438e1f1a6, read 2026-10-19T13:50:53Z; re-run by this seat: IBN6-AC1 to AC3 PASS)

| fact | value |
|---|---|
| the feed's first scheduled day (one `date=` partition) | 2026-10-16 |
| earliest account start date over the universe | 2020-06-03 |
| **N**, the days from the earliest start date to the first scheduled day | **2326** (the script refuses a window over 4000 days; N is within it) |
| households (roster snapshot and universe agree) | 294 |
| accounts in the universe / with a null start date | 863 / 39 |
| the first run's bronze object (one-day window, 294 replies) | 1 key, 1 version, 111,872 bytes |
| the first run's silver object | 1 key, 1 version, 36,187 bytes |

Inferred, NOT measured (B-IN probe, `IRPT_DASHBD_ROUND122_BIN_DRAIN_END_20261015.md`: the 294 full-window replies are about 337 MB of JSON): with the a92589d6 writer the backfill would have written 2326 bronze objects that each embed the full reply set, tens to hundreds of GB and 2326 serialize-and-compress passes. With the new writer the run writes one run object (a gzip of that JSON, tens to about a hundred MB), 2326 envelopes without replies and 2326 silver objects (about 36 KB each, about 84 MB in all by the first run's size).

## 3. The apply of the new script (one act, CloudOps `0.7.0_AE_CloudOps~IB2`, an order cut after this pair is signed)

Replaces ONE S3 code object (the script, live a92589d6) by the new bytes; **no dispatch change** (the feed's row and chain entries are live since the pn-4 apply). Gates, each a STOP: this addendum at its blob with both halves; `IRPT_BCKEND.TO-IB-pn-5` complete and the repository script at HEAD hashing to section 1; no open ledger on the chain's code objects; the live dispatch object equal to the repository copy of the commit the pn-4 apply used (`e7d5361cf9`); the saved copy of the replaced script taken first; the same THREE-PART smoke as pn-4 over the live code prefixes (import and prefixes; `session_token()` under a scrubbed region; the script's PLAN-ONLY run), no Orion request, no write. **The schedule (carried from ADDENDUM 4's CTO half, proposed here for the CTO to confirm or waive):** the apply runs outside the weekday 11:30Z to 14:15Z band and never on Tuesday 2026-10-20. Rollback (Branch B): restore the saved script copy as a new version; remove nothing.

**The first scheduled run after the apply is read from the STEP LOG** (never the chain's exit): exit 0, no `TOLERATING`, `DAYS: complete=<n> skipped=0`, 294 requests within the bound, `calcGrossOfFees` false, and now also: exactly one run object under `run=<day>` and one v2 envelope without `responses` naming it by key and sha256, silver as before in shape, no key outside `orion/inflection/`. A deviation is a STOP and Branch B. **The backfill does not run until that read passes** (proposed; the CTO may waive it).

## 4. The backfill run (once, after section 3's read)

ADDENDUM 2 stands for the call, the rules and the preconditions, read with these changes:

1. **Window and count.** `--from-date 2020-06-03 --pull-date 2026-10-15`: the 2326 calendar days before the first scheduled day; the partition count **2326** is stated by the order before the first call and re-read from the roster at the apply (a different earliest start date or household count above 294 is a STOP and the order states the new figures). Existing days are skipped, never overwritten.
2. **Bronze.** One run object plus 2326 day envelopes (v2, no `responses`). The run record prints the run object's key, bytes and sha256, the peak memory, the elapsed time of the call phase (the 20-minute stop stays) and of the write phase.
3. **Memory and time.** The run holds the parsed replies once, as the CTO's condition 3 of ADDENDUM 2 requires; a memory failure is a STOP and a row, never a raised limit. A run stopped in either phase is completed by a re-run: days present are skipped; a re-run whose replies differ writes a second, differently addressed run object, and each day's envelope names the object it was built from.
4. **Host (the CTO rule of msg 9650, unchanged):** (a) IB2's host if every check is allowed AS IS and no grant is added, otherwise (b) the runner started once with NO shutdown command sent and the idle hours recorded.
5. **Hash and tolerance.** The live script object is re-hashed to section 1's sha256 immediately before the run. After the run: every written day read back; on a sample of at least 5 accounts the chained daily factors over windows of 237 days or less equal the probe's period return within 0.5 bp (longer windows are the adapter cell's check); **no window is named readable by this run**.

## 5. Blast radius, rollback, stop rule

- **Writes.** (i) The apply: one S3 code object. (ii) Every run after the apply, scheduled or backfill: one new key under the NEW run-level prefix `orion/inflection/bronze/scope_account_returns/run=<pull_date>/` (about the size of the day's replies; for the scheduled one-day run a few tens of KB), plus the feed's existing `date=<day>/` keys. (iii) The backfill: 2326 bronze envelopes, 2326 silver objects, one run object. **Reads:** the Orion API (one call per household), the roster and positions silver. **Served values changed: none** (nothing reads the feed until B-IN's adapter is cut; a consumer that lists `date=` partitions does not see `run=`).
- **Rollback, per key.** The script by Branch B. Feed keys, including every `run=` key, are production output: removing them is Andrew's act; the reading side does not wait on a delete, and the adapter ignores a partition until the CTO names the readable window.
- **Stop rule.** The STOPs of section 3 and of ADDENDUM 2 section 5 and its condition list; any key outside `orion/inflection/`; an envelope with a `responses` member; a run object that is not read ABSENT first; a zero written; a stored value that is not the daily factor; silver whose shape differs from the first run's.

## 6. What this addendum does not cover

The adapter that reads the feed; which window the pages may read; a second backfill; the dispatch tolerating a failed pull step (row `IRPT_BCKEND-D2-W404-S9`); fixing null start dates at the source (Andrew's act).

-- 2.0.0_SA_COO~N2
