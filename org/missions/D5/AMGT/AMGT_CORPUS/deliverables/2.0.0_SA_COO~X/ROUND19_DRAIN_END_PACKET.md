# AMGT_CORPUS -- round 19 drain-end packet (the COO's packet at drain-end; L8 hand-off input)

**By `2.0.0_SA_COO~X`, 2026-09-30 ~02:4xZ.** Two orders were issued in ONE issuance (decomposition v19.0, `49d41f0c2b`,
merged `65f1025c46`) on `1.0.0_SA_CTO~Z`'s round-18 analysis (`62ccfcb8d2`). Both are complete, re-graded at each worker's tip
by this seat, and merged; the one hookup that belongs to no cell landed after both. `u-3` (the r-1 re-sign) is BLOCKED on
AMGT_RESAPP (s.3).

**R-4:** graded this round: none by this seat. Graded ever: 19 of 19. Endpoint denominator: 19.

## 1. Orders -- 2 of 2 complete, drained

| order | cell | worker tip | drain | this seat's own run at the tip |
|---|---|---|---|---|
| `TO-CRPS-u-1` | scalar unit/sign readers honour a per-security exception or non-MEASURED status (`Z-W2-S13`) | `e37c984564` | `186d1cc8da` | proof VALID; AC1 `u1 reader best_sales_6501 unit UNRESOLVED sign UNRESOLVED control_8035 unit MILLIONS sign POSITIVE module_in_toplevel yes`; AC2 `u1 served best_sales_6501 FY1 value 11962163.4 served_unit_class UNRESOLVED reader_unit_class UNRESOLVED agree yes`; AC3 `7 passed` |
| `TO-CRPS-u-2` | the `build_unit_map` CLI builds from the producer's header preparation (`Z-W2-S14`) | `6e708d2f5c` | `db3344a99c` | proof VALID; AC1 `u2 replay rc 0 shared_changed 0 shared_removed 0 type_changed 0 hitachi_reproduced 214 of 214 non6501_added 0`; AC2 `14 passed`; the worker's mutant control (the prior file) read 209 of 214 |

**The hookup** (`ff1a0f531d`, this seat): `model_block_pull._ensure_unit_map` now calls `build_unit_map.prepare_header` in place
of its inline CIE_DES_BULK join and bestdata FY1 merge. Parity on Hitachi's raw (stamp `20260929T232729Z`): 27 keys, the old
inline preparation equals `prepare_header` (True), the raw header is unmutated (True).

**Merges.** Both merges were clean through `safe-merge.sh` (4 staged paths each; no channel conflict; no rows minted).

## 2. The one real run (`evidence/r19_real_run.txt`, CLOUD `ff1a0f531d`, 02:37:04Z)

- u-1's probe on the merged tree: 6501's BEST_SALES reads UNRESOLVED on the committed map; the control 8035 still reads
  `MILLIONS` / `POSITIVE`. The served Hitachi block's FY1 BEST_SALES unit is UNRESOLVED and agrees with the fixed reader.
- u-2's replay at HEAD after the hookup: 214 of 214 reproduced, 0 shared / removed / type change, 0 non-6501 addition.
- Drain hygiene: `py_compile` OK, ruff py39 clean, 20 passed over the five research suites (readers, split, exceptions, CLI
  header, admit).

**Ruling 1's branch.** The served block and the fixed reader agree, so the served block stands and no re-derive is owed. The
fix protects the next derive of Hitachi, which under the old reader would have served MEASURED `MILLIONS`.

## 3. `u-3` -- BLOCKED on AMGT_RESAPP r51 cell 1, named

`lib/research/identity/crosswalk.py`'s newest commit is still `6a940b02b8` at `ff1a0f531d`; the union has not moved into
`write_pool`. The `admit` step (round 18) is merged, so u-3's other dependency is met. Nothing is registered.

## 4. Rows -- dispositions for the L9

| row | state | note |
|---|---|---|
| `Z-W2-S13` | answered | the readers honour the exception and the pre-exception status form (u-1) |
| `Z-W2-S14` | answered | one header preparation for both entry points; 214 of 214 (u-2 + the hookup) |
| `Z-W1-S18` | routed | AMGT_RESAPP's file (analysis ruling 3); u-1's probe carries a `module_in_toplevel` guard for it |
| `Z-S63`, `Z-S66` | ARMED, carried | u-3 waits on AMGT_RESAPP r51 cell 1 |
| `Z-S64` | carried | the migration item (round-17 ruling 3) |

No new row this round.

## 5. Judgment criteria owed to `3.0.0_SA_CVO~Z` at L9

- None on the orders (both all-mechanical). For the CVO's read: the reader also honours a non-MEASURED per-security status
  without an `exception` key. The issuer ruled that at L5 because the committed map's 6501 entry predates the exception shape;
  an `exception`-only reader would still have served `MILLIONS`.

## 6. Enrichment candidates for the round-19 analysis

1. `u-3` carries on AMGT_RESAPP r51 cell 1.
2. `build_unit_map.py`'s `Path.write_text(..., newline=)` finding from u-2: `model_block_pull._ensure_unit_map` still writes
   the map with `Path.write_text(..., newline="\n")`, which Python 3.9 rejects (the `newline` keyword arrived in 3.10). The
   runtime here is newer, so it is INERT today; the code's stated floor is 3.9.

## 7. Bounds and residue

- No served write, no S3 write and no vendor call this round (the replay used a temp map; the probe made one S3 GET).
- Drained worktrees `wk-crps19-1/2`: their removal waits on Andrew's word, like the carried ones.
