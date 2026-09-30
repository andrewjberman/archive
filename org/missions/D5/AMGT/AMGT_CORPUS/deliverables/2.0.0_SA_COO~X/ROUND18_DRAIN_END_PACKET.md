# AMGT_CORPUS -- round 18 drain-end packet (the COO's packet at drain-end; L8 hand-off input)

**By `2.0.0_SA_COO~X`, 2026-09-30 ~01:4xZ.** Three orders were issued (decomposition v18.0; the files arrived inside
`2.0.0_SA_COO~D`'s merge `6fcaa52f79`, and the issuance was re-stated @`fba80203b5` with its fanout line, row `Z-S67`). All three
are complete, re-graded at each worker's tip by this seat, and merged. `t-4` (the r-1 re-sign) is BLOCKED on AMGT_RESAPP (s.3).

**R-4:** graded this round: none by this seat. Graded ever: 19 of 19. Endpoint denominator: 19.

## 1. Orders -- 3 of 3 complete, drained

| order | cell | worker tip | drain | this seat's own run at the tip |
|---|---|---|---|---|
| `TO-CRPS-t-1` | the model-block `admit` step | `f5b3ced671` | `c63945134b` | proof VALID; AC1 `admit population registered 96 without_block 0 pulled 0 bloomberg_calls 0`; AC2 `t1 refuses_loudly True rc_nonzero True names_surface True population_printed_first True planted_pulled 1`; AC3 `t1 scheduled_steps registration,model_block_admit`; bound 0 |
| `TO-CRPS-t-2` | `build_unit_map` per-security exceptions (`Z-S65`) | `e8e8edee63` | `c95be7d59a` | proof VALID; AC1 `t2 replay rc 0 shared_changed 0 shared_removed 0 type_changed 0 hitachi_reproduced 209 of 214 non6501_added 0`; AC2 `9 passed`; bound 0 |
| `TO-CRPS-t-3` | the model-block reader key-form census (`Z-S64`) | `164866d4db` | `74cf6a2830` | proof VALID; AC1 `t3 readers 20 rows_valid 20 all_valid True ... bp_absent 1`; AC2 `paths_outside_grant 0`; own S3 list: `BP/_LN_Equity` 6, `BP-_LN_Equity` 0 |

**Merges.** Each merge conflicted in the append-only channel. The first attempt at t-2 mis-stitched interleaved hunks; safe-merge
refused it and aborted cleanly. Every merge was then resolved by rebuilding the channel from the index stages: ours' rows plus
the branch's new rows, in order. The channel now holds 114 rows with 0 duplicates.

## 2. The one real run (`evidence/r18_real_run.txt`, CLOUD `74cf6a2830`, 01:42:15Z)

- `model_block_pull.py admit --dry-run` on the LIVE population read `admit population registered 96 without_block 0` and then
  `... pulled 0 bloomberg_calls 0`. It made an S3 list and no vendor call.
- The t-2 replay at HEAD read `shared_changed 0 shared_removed 0 type_changed 0 hitachi_reproduced 209 of 214 non6501_added 0`.
- t-3: 18 readers are raw_slash and read BP/NG OK. `/versions` and `/thesis` return 200 SERVED for BP and NG (the worker's
  reads). The one ABSENT reader is `lib/research/print/render_pack.py` `main()`, a hand-run CLI with no caller in
  lib/integrations/infra that builds `BP-_LN_Equity`, a key which has 0 objects. The served print route (`scoped_amgt.py:4480`)
  reads the raw key.

## 3. `t-4` -- BLOCKED on AMGT_RESAPP r51 cell 1, named

The union still lives only in `crosswalk.main` (yy-6 `6a940b02b8`). `add_security` builds without `served=` (row `Z-S66`). No
AMGT_RESAPP commit moving the union into `write_pool` is on CLOUD at `74cf6a2830`: `crosswalk.py`'s latest commit is still
`6a940b02b8`. `t-1` has merged, so t-4's other dependency is met. Nothing is registered.

## 4. Rows -- dispositions for the L9

| row | state | note |
|---|---|---|
| `Z-W2-S13` | ARMED | an exception under a SCALAR shared field is invisible to `model_block_pull._resolved_unit` / `_resolved_sign`, so 6501's BEST_SALES reads the shared `MILLIONS`. For the analysis: a reader cell (model_block_pull's file). |
| `Z-W2-S14` | INERT | `build_unit_map`'s CLI and the producer's `_ensure_unit_map` feed different headers, which is why the replay reproduces 209 of 214 |
| `Z-W1-S18` | ARMED | `price_axis_pull.py:97-100` puts the MAIN workspace on `sys.path` when imported, so a multi-file pytest in a worktree grades the main tree's bytes. Single-file AC scripts are unaffected. |
| `Z-W3-S9` | INERT | the only ABSENT reader (render_pack CLI) has no served surface |
| `Z-S67` | INERT | the issuance swept into a peer's merge; for safe-merge's owner |
| `Z-S64` | answered | no served reader reads BP/NG as ABSENT; carried as a migration item (round-17 ruling 3) |
| `Z-S65` | answered | `build_unit_map` no longer moves a shared field (t-2) |

## 5. Judgment criteria owed to `3.0.0_SA_CVO~Z` at L9

- t-2's "byte-equal" is graded as 0 shared/type change with 209 of 214 reproduced. The 5 are the CLI-versus-producer header
  path (`Z-W2-S14`), not the exception shape.
- t-3's ABSENT reader is judged not served: there is no caller, and the served route reads the raw key.

## 6. Enrichment candidates for the round-18 analysis

1. `Z-W2-S13`: `model_block_pull`'s unit/sign readers honour `per_security_detail[sec].exception`.
2. `Z-W1-S18`: `price_axis_pull.py`'s import-time `sys.path` injection.
3. `Z-W2-S14`: the CLI builds with the producer's header preparation.
4. `t-4` carries on RESAPP r51 cell 1.

## 7. Bounds and residue

- No served write and no vendor call this round (every admit run was `--dry-run`; the replay used a temp map).
- Drained worktrees `wk-crps18-1/2/3`: their removal waits on Andrew's word, like the carried ones.
