# MDPF_CANON round 2 -- CLOSE (2.0.0_SA_COO~D1, dell1, 2026-10-09 ~23:1xZ)

Round 2 is the enrichment list of the round-1 analysis (`ledger/ROUND_ANALYSIS.round1.md` @409182ae5a section 3). Items 2-4 were
cut as four cells. Items 1 and 5 are an issuer read of the 2026-10-10 13:30Z daily write: not a cell, and not yet owed (section 4).

| item | value |
|---|---|
| issuance | @5f2c367568: decomposition v2, 4 cells, risk WORLD |
| amendments | @8a4ef42ee6 (issuer's ARN scanner, row W7-S1); @6f0b43bb0f (serial-folder paths, row W5-S1; PRD v2.10 @b3259175a5). Gate limb: none (modifications) |
| `CN-b-1` reader census (M1) | ~4 (re-seated), `f918c9205a`, drained @3c7fdcf16d. `r2_checks.py census` 4/4, proof VALID |
| `CN-b-2` global basis (M7, FWD-3) | ~5, `dcaf2f5e62`, drained @f93eccd490. `r2_checks.py basis` 3/3, proof VALID |
| `CN-b-3` publisher python3.11 + pyarrow layer (M5) | ~6, `25c1b3b6a4`, drained @9c36cacc05. `r2_checks.py publisher` 3/3, fmt clean, proof VALID |
| `CN-b-4` composite grant on builder output (W1-S1) | ~7, `2fb91b7b78`, drained @63b47dc1d4. `r2_checks.py builder` 3/3, `r1_iam.py` 6/6, proof VALID |
| deploy | CloudOps ~DELL1 `ADHOC.canon-r2-publisher-layer-and-builder-grant` @43bd5a8356, COMPLETE @446b5db1a6, C1-C6 PASS, ledger CLOSED |

At HEAD @77a321b160: census 4 of 4, basis 3 of 3, publisher 3 of 3, builder 3 of 3, r1_iam 6 of 6.
`round-close-check.py --round 2`: 4 of 4 complete, proof_ok 4, verdict REFUSED (4 AC3 judgment criteria ungraded; this packet asks for them).

## The real runs (what each AC3 is graded on)

- **CN-b-1 AC3:** `deliverables/0.9.0_WK_MDPF_CANON~4/READER_CENSUS.md`. It has 51 rows, and all 138 `path:line` cells resolve at HEAD.
  The worker's disclosed gaps:
  - the archive and docs hits are grouped as history;
  - config is cited 47 times against IV.2's floor of 50 (a grouping, not missing sites);
  - the bronze count moved 310 -> 313 (sibling scratch files);
  - the portal front-end was unseen in its worktree (row W4-S1).

  Row **S8** (@77a321b160) closes that last limb from the main tree's portal pin c96efe17. The stale key's readers sit only in
  `portal/src/api` (`portal-proxy.ts:338`, `endpoints/aum.ts:328,449`), and no page calls them. The key has dead readers and no
  live consumer.
- **CN-b-2 AC3:** `deliverables/0.9.0_WK_MDPF_CANON~5/X2_GLOBAL_BASIS.md`, with headings Aggregation level, Minimum firm count, and Why no
  per-firm or per-account row survives. The ledger X2 row cites it (`infra/logic/06_CONFORMANCE_LEDGER.md`). The grade asks whether the
  minimum firm count is read from the producer.
- **CN-b-3 AC3:** one ad-hoc publisher invocation in the scheduler's own event shape (`{}`, read from
  `aws_scheduler_schedule.mdpf_publisher_daily`).
  - Response: published 18, failed [], all_present true.
  - **DELTA=0** across 125,721 data-bearing values in 18 leaves; the 18 `_provenance.written_at` values were excluded.
  - Plan: 2 of 46 attributes moved (runtime, layers). All 15 forbidden attributes are unchanged, `source_code_hash` and `environment`
    among them.
  - Live: python3.11, the layer read by name, CodeSha256 unchanged.
- **CN-b-4 AC3:** the targeted plan read "No changes" (rc=0), with a positive control: the target resolved, and the planfile holds it
  as one of 5 no-ops with 0 changes. The rendered policy matches before and after as parsed JSON. Not applied, as the order requires.

## For the CTO at L10 (not this packet's ask)

- **W1-S1, the letter of the ruling.** The ruling asked for a registry row making the builder tier-aware for `global`. CN-b-4 found that
  the builder already carries `scope_bucket["mdpf"] = "opal-data-mdpf"` (`modules/opal_name/generated_locals.tf`), so the grant now
  reads builder output with no new row. `scope_bucket["global"]` still gives `opal-data-portal-v2`. A consumer that keys the composite
  by `"global"` would still get the platinum bucket.
- **PRD path wording.** M1/M7's root `deliverables/` paths can be written by no lane. v2.10 moved them to the serial folders.

## Carried (not this round's acts)

1. **The 2026-10-10 13:30Z daily write** (enrichment items 1 and 5). Read at the tick after the fire:
   - the four types x four scopes at their `address()` paths are written;
   - prior partitions are unchanged;
   - global is byte-identical to its legacy figures;
   - the first `account_units` partitions exist for 49financial, inflection and global.

   That read grades CN-a-2 AC3 and FWD-1 REALIZED. It is the producer's own clock (CTO's word in the round-1 analysis section 1), and
   the backfill already drove the writer on demand.
2. M3's full-history clause, M4, M6, M8, and M11-M17 follow the PRD's arc. M9 and M10 wait on ADVI_FIRMBKTS.
