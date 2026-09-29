# AMGT_CORPUS -- round 9 drain-end packet (the COO's task-order packet at drain-end; L8 hand-off input)

**By `2.0.0_SA_COO~X`, 2026-09-29 ~03:2xZ.** Round 9 (decomposition v9.0, issuance @`2da2daa9b7`) had two cells: one order
(`CRPS-k-1`) and one issuer act (`CRPS-k-2`). Both are done, and all three served acts ran under signed pairs with change
entries opened before and closed with content proof.

**R-4:** graded this round -- none by this seat (L9 is the CVO's); graded ever -- 19 of 19; endpoint denominator -- 19.

## 1. Order -- 1 of 1 complete, drained

| order | cell | worker tip | drain | this seat's own run at the tip |
|---|---|---|---|---|
| `TO-CRPS-k-1` | each case = its own columns of the scenario table, with unit and page | `3f0d4f1a92` | `19458b6130` | AC1 `8 passed`; AC2 `case_census names 95 slots 285 body 84 heading_only 0 absent 201 sum 285 ordering_held 28 ordering_violated 0 ordering_na 67 unit_carried 10`; AC3 judgment recorded for the CVO; proof VALID; corpus suite 392 passed |

## 2. The served acts, as executed

1. **The dossier rewrite (k-1's act)** -- pair COO `b98e09953e` / CTO `9ffd945889`, entry `amgt-corpus-r9-dossier-rewrite`
   (open `038e76d4da`, CLOSED `fd44f203a6`): `dossier --write --workers 10`, `names 95 written 95 existed 0`; objects
   468 -> 563; served the last write 95 of 95; `current_method_available 95 stale_pick 0`; the served case census equals the
   in-memory one. Row `Z-S54` lifts `Z-S53`.
2. **The model-block re-derive (k-2)** -- gate `amgt-combined-uu4-a2-...` CLOSED 02:11:44Z; pair COO `5151500c41` / CTO
   `0fbb50e84e`; entry `amgt-corpus-r9-model-block-rederive` (open `8dd31c0bd7`, CLOSED in this commit): 33 of 33 batches rc 0;
   97 of 97 new stamps; served blocks **51 -> 69**; `verify keys 97 match 97 mismatch 0` against the rule's expected log;
   SERVED -> ABSENT exactly **6861_JP, CAT_US, CSL_AU** (no adjusted EPS at any landed stamp; the CTO's ruling @`74e1eea534`:
   they stay ABSENT, no pull, no GAAP fallback). The stored blocks now carry the rule the served adapter already computes.
3. **The follow-on dossier rewrite (k-2's second act, same pair)** -- `names 95 written 93 existed 2`; objects 563 -> **656**.
   **A prediction miss in my COO half, not in the act:** the half expected 95 puts on the assumption that every dossier name
   has a model block. Two do not -- `BP/_LN_Equity` and `NG/_LN_Equity` -- so the re-derive moved none of their inputs and
   `write_one` took its unchanged branch as written; they serve their `/2` object from act 1 (`stale_pick 0`). The CTO half
   repeated the 95; the leg's proof states the miss.

## 3. The one real run of each outcome

- **Cases, served** (`evidence/r9_real_run_read_dossier.txt`, read by this seat after act 1): ADBE_US_Equity Price 2026
  `416 / 233 / 143` at `16.0x / 9.0x / 6.0x`, unit null; AZN_LN_Equity `227.08 / 131.91 / 45.24` at `25.0x / 17.0x / 12.0x`,
  unit U+00A3 (pound); citation page 0; method `amgt-corpus-dossier/2`.
- **Model blocks, served** (`evidence/r9_k2_blocks_after.txt`): the newest block per key read from S3, 97 of 97 equal to
  `case_rule.compute_cases` over the landed raw.

## 4. Rows -- dispositions for the L9

| row | class / standing | disposition asked |
|---|---|---|
| `Z-W1-S9` | ARMED -> held by `Z-S53` | CLOSE: the served cases are the table by case (s.2 item 1) |
| `Z-S53` | INERT (hold) | CLOSE: lifted by `Z-S54` |
| `Z-S54` | INERT | the lift carrier |
| `Z-W1-S11` | INERT | CLOSE: the lone currency-symbol line read as the preceding value's unit; a date footer ends the table |
| `Z-W1-S12` | INERT | OPEN -> enrichment: 6 of 34 tables unreadable (EPS row 14 of 15 values in the extraction): 8035_JP, BZLFY_US, HEI_US, SNPS_US, TSM_US, V_US |
| `Z-S51` | INERT | CLOSE: the re-derive ran under the new rule, 97 of 97 verified |
| `Z-W3-S6` | INERT | CLOSE on the CTO's ruling @`74e1eea534` |
| `Z-S55` | INERT (the CTO's) | READ: `cases-report` grades the underscore key form ABSENT instead of refusing; this seat's runs used the Bloomberg form (97 of 97 keys round-trip key -> ticker -> key) |

## 5. Judgment criteria owed to `3.0.0_SA_CVO~Z` at L9

- **`k-1` AC3** -- *does each served case read as that case, in the team's numbers, with its unit?* -- graded on names from more
  than one currency. The artifact is the served table (656 objects; `read_dossier` any name). Currencies carried: U+00A3
  (AZN), U+20AC (ML), `$` (BP, CPA, ORA, SAP, SHOP, SPOT, TTE, UNVGY); 18 of the 28 readable tables carry no symbol (e.g.
  ADBE). ORA_FP reads `$` because the team wrote `$`.

## 6. Enrichment candidates for the round-9 analysis

1. **The six unreadable tables (`Z-W1-S12`).** The extraction drops one Base EPS value per name; a table rule that reads the
   pdf page by position (or an extraction fix) would serve them.
2. **`cases-report`'s silent ABSENT on the underscore key form (`Z-S55`)** -- a refusal would make the trap loud.
3. **A pair's expected count must be read per name from the join, not from the table's size** (s.2 item 3): a note for this
   seat's halves, not a cell.

## 7. Bounds and residue

- No vendor or gateway call. Served-plane writes this round: 95 + 93 dossier objects, 97 model blocks; no delete.
- Worktrees `/c/tmp/wk-crps7-5`, `/c/tmp/wk-crps8-1..3`, `/c/tmp/wk-crps9-1` (branches merged) hold only their workers'
  untracked `.scratch/`; removal is a forced (recursive) delete and waits on the operator's word, as do the `%TEMP%` dirs.

-- `2.0.0_SA_COO~X`
