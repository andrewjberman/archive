# AMGT_CORPUS -- round 15 drain-end packet (the COO's packet at drain-end; L8 hand-off input)

**By `2.0.0_SA_COO~X`, 2026-09-29 ~21:5xZ.** The issuance @`ca6e2ef4f2` (decomposition v15.0) cut the round-14 analysis's two
enrichment items (@`c2e8fc74f6`) with `fanout: 0 of 2 chains`. No worker order was cut, for two reasons:
- q-1 was resolved at L5 by the issuer's measurement.
- q-2 is the issuer's served act under a signed pair.

**R-4:** graded this round: none by this seat. Graded ever: 19 of 19. Endpoint denominator: 19.

## 1. Cells

| cell | disposition | evidence |
|---|---|---|
| `CRPS-q-1` (`Z-W4-S5`, slash-key read path) | RESOLVED AT L5, no build | `evidence/r15_q1_slash_read.txt` (21:42:14Z) |
| `CRPS-q-2` (crosswalk row for Hitachi 6501 JP) | LANDED under pair COO `ca6e2ef4f2` / CTO `411236c2b7`; entry `amgt-corpus-r15-hitachi-crosswalk` CLOSED 3 of 3 | `evidence/r15_q2_{dryrun,before,run,after}.txt` |

**q-1:**
- `read_dossier("BP/_LN_Equity")` and `read_dossier("NG/_LN_Equity")` each return their served object under the writer's
  slash-safe partition.
- All 95 partitions, decoded through `crosswalk.security_key_from_slash_safe`, read `read_ok 95 fail 0 slash_keys 2`.
- Negative control: the partition form passed as a key raises `SlashSafeKeyError`.
- The 93-of-95 count in `Z-W4-S5` came from p-4's sweep passing partition names as keys. It was never a read-path defect.

**q-2** (entry `126b55bf26` opened -> CLOSED):
- **STOP limb 1** (21:54:22Z): 5 pool keys; `2026-09-29.json` absent.
- **R** (21:54:45-21:54:49Z):
  - `RAW LANDED bronze/identity/security_key=6501_JP_Equity/20260929T215447Z.json`.
  - `MEASURED 6501_JP_Equity 'HITACHI LTD' ... AGREES`, `bloomberg_calls 1`. This is one scripted call under R-21
    `b390c36444`.
  - `OK uploaded crosswalk/v1/2026-09-29.json 599016 B records 237 UNRESOLVED 0 pool_puts 1`.
- **G:** `registrations.json` committed at `7581890b07`, 71 rows.
- **V** (21:55:20Z):
  - 6 pool keys, the latest today's.
  - Record diff against `2026-09-25.json`: `added 1 removed 0 changed 0 added_keys ['6501_JP_Equity'] other_jp_moved 0 of 6`.
  - Backlog census: `folders 96 resolved 96 unresolved 0 ambiguous 0 hitachi 6501_JP_Equity`.

## 2. The one real run (FWD-4's organic arm, `evidence/r15_q2_after.txt`)

`induction_request.run()` from HEAD read `backlog_folders 96`, `unresolved_in_universe 0 of 96`, `picked NONE population is
empty`, `vendor_calls 0`, `s3_writes 0`, `poison_positive_control raised 4 of 4`. The output file went to a scratch
directory, which was removed afterwards.

With Hitachi resolved, the library has no unresolved folder, so the organic arm has no candidate today. The two limbs (WILL-ADD,
REFUSES-ambiguous) were driven in round 14 (p-2) on planted folders.

## 3. Rows -- dispositions for the L9

| row | state | note |
|---|---|---|
| `Z-W4-S5` | answered by q-1's measurement | the sweep's decoding, not the read path |
| `Z-S58` | answered by q-2 | Hitachi now resolves; FWD-4's organic population is 0 of 96 |

No new row this round.

## 4. Judgment criteria owed to `3.0.0_SA_CVO~Z` at L9

- **The identity choice:** `6501 JP` was read from the folder's own name, because no ONE PAGER workbook exists, then measured by
  the call. The CTO half AGREED it (s.1).
- **q-1's L5 resolution:** no build was owed, and a test would be coverage only.

## 5. Enrichment candidates for the round-15 analysis

- None from this project's own surfaces.
- The six render outcomes remain with AMGT_RESAPP round 50, and this project re-grades them on the deployed function once they
  land (round-14 analysis, ruling 7).
- A standing mechanism is the analysis's call, not this seat's: every library folder newer than the crosswalk gets its row as
  it arrives. Today it was a manual act.

## 6. Bounds and residue

- One served write under the pair, and one scripted Bloomberg call (R-21).
- No worktrees this round. Operator cleanup is carried from round 14: the checkouts `wk-crps14-*` and `wk-crps10/12/13-1`, and
  the system-temp `amgt_corpus*` entries. Each waits on Andrew's word.
