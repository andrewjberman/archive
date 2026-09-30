# AMGT_CORPUS -- round 17 drain-end packet (the COO's packet at drain-end; L8 hand-off input)

**By `2.0.0_SA_COO~X`, 2026-09-30 ~00:2xZ.** The issuance @`1d58fd0c2e` (decomposition v17.0, fanout 1 of 2) cut two cells:
- `s-1`: the model-block census, then Hitachi's model-block act, under a pair. **Drained and landed.**
- `s-2`: the r-1 re-sign. **Blocked** on AMGT_RESAPP (section 3).

**R-4:** graded this round: none by this seat. Graded ever: 19 of 19. Endpoint denominator: 19.

## 1. Orders -- 1 of 1 complete, drained

| order | cell | worker tip | drain | this seat's own run at the tip |
|---|---|---|---|---|
| `TO-CRPS-s-1` | the model-block census (read-only) | `56b9492b20` | `01682baecd` | proof VALID; AC1 `s1 census names 96 present 95 absent 1 rows_valid 96 hitachi absent`; AC2 `s1 producer writer integrations/bloomberg/research/model_block_pull.py invoked_by_n 4 population_source_named True admits_new_registrations False evidence_n 6`; AC3 `paths_outside_grant 0`; own S3 list: `6501_JP_Equity` 0 objects, `BP/_LN_Equity` 6 (literal `/`) |

## 2. The served act -- Hitachi's model block, entry `amgt-corpus-r17-hitachi-model-block` CLOSED 4 of 4

Pair: COO `6e7bdec3bd`, CTO `c58e96e867`, CTO ruling (b) `ab489143c2`. Run from the clean checkout `wk-crps17-1`.
- **P** (23:27Z): `model_block_pull pull --securities "6501 JP Equity"`. Three raw objects under stamp `20260929T232729Z`:
  refdata 1179 B, histdata 11153 B, bestdata 2098 B.
- **D** (23:28Z): `derive` gave `derived/model_block/6501_JP_Equity/20260929T232834Z/model_block.json`, with 11 FY rows, 389
  figures and 69 unresolved.
  - Sources: bloomberg-dapi 357, BBG 34, SA_FALLBACK 0. The fallback read "no Bloomberg gap -- nothing to fill", so SA was
    never called (CTO condition 1).
- **V:** the census re-run over the live library reads `folders 96 present 96 absent 0`.
- **F:**
  - The producer's unit-map merge changed SHARED field entries (row `Z-S65`): 4 fields flip `unit_status`/`sign_status` from
    MEASURED to UNRESOLVED-ON-6501, and 1 field changes type from scalar to dict. It was withheld under stop limb 3.
  - CTO ruled (b): Hitachi's per-security entries only. Built at `6077a2d939`: 214 additions, all 6501-scoped; 0 changed,
    0 removed, 0 type changes. BEST_SALES unit and sign were skipped because they are scalar fields.
  - The shared tree's 05:42:34Z residue (`field_map.json` +NVDA and `AMGT_CORPUS~1/ingest_run.json`, one pre-crash test run) was
    restored to HEAD by 1.0.0_SA_CTO~Z on Andrew's approval (`ANDREW_DIRECT_20260930_001xZ_OPEN_CALLS_RECS_APPROVED.md`). The
    backup is at `.runtime/crash-investigation-20260929/uncommitted-backups/`. `git stash` was refused by the hook, correctly.
  - Merged at `ead621d685`, and re-verified on CLOUD with the same diff.
- **Correction for the record:** commit `b3cafa00f3`'s subject reads "ledger-hold". No hold was set; the ledger refuses HOLD
  while an apply leg is open, so that commit carries evidence only.

## 3. `s-2` -- BLOCKED on AMGT_RESAPP, named

AMGT_RESAPP `yy-6` (`6a940b02b8`, merged) makes only `crosswalk.main --write-pool` union-first. The other `crosswalk/v1` writer,
`add_security` (`add_security.py:366` build, `:401` put), is the scheduled fire's path and still builds without `served=`.
- Census: 14 `write_pool` / `build_crosswalk` call sites, of which exactly 2 build `crosswalk/v1` (row `Z-S66`).
- 1.0.0_SA_CTO~Z AGREED the hold (msg 26799, `1b2294bbd6`). The union moves into `write_pool` itself as RESAPP's next cell
  (2.0.0_SA_COO~Z).
- `r-1` re-signs once that cell drains, with the fork test run through `add_security` on both sides.
- Nothing is registered.

## 4. Rows -- dispositions for the L9

| row | state | note |
|---|---|---|
| `Z-S63` | ARMED | half-closed by yy-6; `Z-S66` names the remaining path |
| `Z-S64` | INERT | the model-block writer bypasses `slash_safe_key` (`BP/` is stored under a literal `/`); carried to round 18 (CTO) |
| `Z-S65` | ARMED | `build_unit_map`'s merge recomputes shared field aggregates when one name's unit is ambiguous; carried to round 18 (CTO) |
| `Z-S66` | ARMED | `add_security` builds without `served=`; routed to AMGT_RESAPP (CTO) |

## 5. Judgment criteria owed to `3.0.0_SA_CVO~Z` at L9

The residue attribution: "most likely this seat's prior-session drain test run". It rests on the mtime (one process, 34 ms
apart), the timing (inside 2.0.0_SA_COO~X's round-10 drain, 05:41-05:46Z) and the content (+NVDA, a non-library name). No
process trace exists.

## 6. Enrichment candidates for the round-17 analysis

1. **The model-block admission:** a caller that pulls newly registered names. `admits_new_registrations False` today; every
   caller names tickers by hand.
2. **`Z-S65`:** `build_unit_map` should never downgrade a shared field on one ambiguous name.
3. **`Z-S64`:** the model-block key form.
4. **`s-2`** carries forward on RESAPP's `write_pool` union.

## 7. Bounds and residue

- **Served writes:** Hitachi's 3 raw objects plus 1 derived model block, under the pair. `field_map.json` additions are on CLOUD.
- **Vendor calls:** the Bloomberg DAPI calls of one pull (R-21, scripted); the Seeking Alpha fallback made 0.
- **Drained worktrees** `wk-crps16-1` and `wk-crps17-1`: their removal, like the carried ones, waits on Andrew's word.
