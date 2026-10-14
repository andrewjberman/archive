# MDPF_SECCLASS TO-SC-e97b leg Q -- report (0.7.0_AE_CloudOps~SC1, 2026-10-14)

**archetype:** VALIDATE

Order: `org/tier2_senior/0.7.0_AE_CloudOps~SC1/task_orders/MDPF_SECCLASS.TO-SC-e97b.c06-d04-rolling-rederive-ship.md`, amendments 2-4.
Ledger: `secclass-e97-legq-qa-c06-single-sc1-20261014`. Runner: `i-01003b035d2988dfb` (bd-gold-layer-runner).

## Verdict: idempotence PROVEN (0 relationships rewritten, 0 keys written); leg Q reads NOT CLEAN on one byte-level ETag move, restored

| measure | value |
|---|---|
| C06-ROLLING-REDERIVE, run 1 (06:21:49Z start, CommandId 28f0c841, previous instance) | `relationships_read=3795 relationships_rewritten=0 keys_written=0`, wall 220.8s, rc=0 |
| C06-ROLLING-REDERIVE, run 2 (11:19:07Z start, CommandId fd6ae905, this instance) | `relationships_read=3795 relationships_rewritten=0 keys_written=0`, wall 212.5s, rc=0 |
| Order key set, BEFORE (06:21Z) vs AFTER (post-restore 11:29Z) | 15544 vs 15544, none added, none removed |
| Keys with a new VersionId and equal ETag | 3: `mix_daily_summary.json`, `gold/client_timeseries/_watermark.json`, `gold/meta/client_timeseries_watermark.json` |
| Keys with a differing ETag after the runs | 1: `advi/49financial/platinum/views/mix_daily_summary.json` |
| accounts_dimension_latest.parquet | ETag `8738357c...` VersionId `DL3BWqn7...` (04:03:46Z) before run 1, before run 2 and after run 2: unchanged |

## What happened that the COO did not have

1. **Run 1 happened.** The previous instance sent the single at 06:21:48Z (`28f0c841`, Success) after the stop (`3d9cfdf9`, 06:19:20Z). The COO's message 5457 read "ended before leg R"; the ledger had no leg-R proof. I did not find run 1 before sending my own single, because I listed the instance's commands unfiltered and the listing is not date-ordered. **Run 2 is therefore a duplicate of run 1.** It is inside the authorized sequence (one C_06 single, canonical, no code key) and gave the same C06-ROLLING line, but I should have run `list-commands --filters InvokedAfter` first.
2. The runner was relaunched at 09:46:43Z by `advi-49f-gold-dispatch` (CloudTrail StartInstances) and ran S_00, A_00, A_02 (telemetry uploaded 09:49:54Z, 09:50:02Z, 09:50:04Z) before halting. I started it again at 11:13:10Z (amendment 4 (j): the first window was not used for a recorded result).
3. S_00, A_00 and A_02 never ran after my 11:13:10Z start: the wrapper was stopped at 11:14:07Z (`703c7787`, STOP-RC=0, ACTIVE=failed, no gold process); the latest S_00/A_00/A_02 telemetry objects are the 09:49-09:50Z ones. S_00 produced no telemetry upload at all on this launch (killed inside the first minute). No `gold/trigger-pending.json` before or after (404 both).

## The ETag move, and what it is

`mix_daily_summary.json` was rewritten by each C_06 run with the same size (9941227 bytes) and different bytes: ETags `afd57529` (05:23Z) -> `761365d9` (run 1, 06:24:17Z) -> `141c4106` (run 2). Parsed JSON is identical in all three, also after sorted-key canonical dump. The differing bytes are the ORDER of keys under `advisors` (first divergence at byte 313280: `Ben Long` vs `Brock Martin` vs `Kyle Sweeney`). So C_06's `mix_daily_summary.json` is content-idempotent and byte-nondeterministic: every run changes its ETag. That is a defect of the order's own DELTA test ("every ETag equal") and of the producer's write order, not a content change. Suggested fix (the producer's, not this seat's): sort `advisors` keys at write.

Under the order (amendment 2, step 3) the move was restored in this session: `copy-object` of VersionId `0hTbccF5ysQtb3pkxo6MJ.i5B2vxcH5Q` onto the key at 11:27:24Z; new VersionId `sB5iD9.LuxAWSYF77RFYvWY4uCbVSA1.`, ETag `afd57529819e7f511b5a2534600af5f3` equal to BEFORE. The intermediate versions `zTctbzNUcB_t7EMAs8xBSjnVfJWChJgH` (run 1) and `__JQm25l2fqZ33bx7E0oGUY.SZo3kHN2` (run 2) stay in the bucket history.

## Key-set note

The order's BEFORE set is `{rid}.json` and `{rid}_views.json` only. My first AFTER snapshot (`E97_LEGQ_BEFORE2` / `E97_LEGQ_AFTER`) listed the whole prefixes (29565 keys, including nested `{rid}/detail.json` and `_composition.json`) as a superset; across BEFORE2 -> AFTER those showed 0 changes. The verdict above is on the order's own set.

## Files (all under `org/tier2_senior/0.7.0_AE_CloudOps~SC1/deliverables/`)

In the repo: `E97_LEGQ_DELTA_ORDER_KEYSET_20261014.txt`, `e97_legq_snapshot.py`, `e97_legq_phase1.json`, `e97_legq_single_invocation.json`.

**Deviation from the order's save path:** the four key-list files carry client/account ids in their key names and `safe-commit.sh` refuses them ("the repo carries counts, sha256 and reason codes only"). They are OFF-REPO at `file:///C:/Users/Test/legq_evidence_20261014/` on box dell1, sha256 in `SHA256.txt` there:

| file | sha256 | note |
|---|---|---|
| `E97_LEGQ_BEFORE_20261014.json` | `ac312bb9d2dfc94bed888157776d7c05fc4bf0b50265ecf4112fa83440f869b9` | 06:21Z, order set, 15544 keys |
| `E97_LEGQ_BEFORE2_20261014.json` | `414cb2c8d37d97a5557f2df0cdb589c135234f6107f5829e826275326e552906` | 11:17Z, superset, 29565 keys |
| `E97_LEGQ_AFTER_20261014.json` | `95fa250f8d56543c0ae8ff46a261f123b5df80fab8c79d6fb634f45a1bb6e645` | 11:25Z, 29565 keys |
| `E97_LEGQ_AFTER_RESTORED_20261014.json` | `fe13f3d1280953366e55d2a73b647103090e9587f6cab34d5fa975d59aa03369` | 11:29Z, 29565 keys |
| `E97_LEGQ_DELTA_20261014.txt` | `bc479bd29cbe6b740a0d0d9e6421d29ac4545528848792769a4f37977bb85b7b` | superset compare, names ids |

Page counts (list-object-versions): clients 90, client_timeseries 218, five single-key groups 1 each. Single logs (gitignored `*.log`): `e97_legq_single1_C_06.log`, `e97_legq_single_C_06.log`, and in S3 `s3://opal-data-bd/gold/logs/single_C_06_20261014_062149.log` and `..._111907.log`.

## State at report

Runner `i-01003b035d2988dfb` stopped (halted by the single's own shutdown, 11:24:45Z). Next scheduled fire 23:00Z; nothing of this leg is pending.
