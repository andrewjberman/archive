# AMGT_CORPUS -- round 12 drain-end packet (the COO's task-order packet at drain-end; L8 hand-off input)

**By `2.0.0_SA_COO~X`, 2026-09-29 ~11:2xZ.** One order issued (@`02a16d3382`, decomposition v12.0), one complete, re-graded at the
worker's tip, and merged inside the signed window. The round's one served act moved the dossier store to the naming builder's
canonical prefix. It ran under a pair signed on both halves (COO @`700dcc6190`, CTO @`4dead72211`), and every after-state line
the COO half named reads as predicted.

**R-4:** graded this round -- none by this seat (L9 is the CVO's); graded ever -- 19 of 19; endpoint denominator -- 19.

## 1. Orders -- 1 of 1 complete, drained

| order | cell | worker tip | drain | this seat's own run at the tip |
|---|---|---|---|---|
| `TO-CRPS-n-1` | the dossier store at the builder's `research_dossier` prefix; no hyphen literal left | `ce3192a363` | `d0141a6a76` | AC1 `3 passed`; AC2 `n1 table research_dossier prefix amgt/harvest/gold/research_dossier/ equals_builder True hyphen_literal 0`; AC3 `pdf_libs_loaded none read_dossier_callable True`; proof VALID; corpus suite 444 passed |

## 2. What happened in the round, as executed

1. **Cut:** the CTO's ruling at the vv-4 verdict (msg 26555, @`e1e4ae43d4`) made this an R19 cell: the store writes and reads
   at `lib/opal_naming.py address()` output, keeps no fallback to the legacy prefix, and leaves the old objects undeleted.
   Checks at the base: AC1 and AC2 FAIL as expected, AC3 PASS as expected.
2. **Held merge:** the worker's tip was graded VALID and NOT merged until both halves were signed. Merging earlier would have
   put code at CLOUD HEAD that reads an empty prefix.
3. **One window:** entry `amgt-corpus-r12-dossier-readdress` was opened at @`e7228d6ff1` (10:39Z). Leg M, the merge
   `d0141a6a76`, landed at 10:45Z. Leg W, `dossier --write --workers 10` from the merged code, logged `names 95 written 95
   existed 0` with 0 `ERROR` and ended 11:09:15Z. The exposure window named in the half was about 24 minutes. Leg V is the
   after-state below. The entry is CLOSED in this commit.
4. **Literal census at HEAD:** `git grep -c research-dossier -- lib/` finds 0 files. The control `research-` finds 18 files
   under `lib/research/corpus/`: the other five `research-*` stores stay on their legacy form, per the round-11 analysis s.4.

## 3. After-state against the signed COO half, line by line (live reads 11:15-11:17Z; `evidence/r12_after_*.txt`)

| line | predicted | read |
|---|---|---|
| 1 | new 95 objects / 95 partitions; legacy 846 | `research_dossier/ objects 95 partitions 95`; `research-dossier/ objects 846 partitions 95` |
| 2 | `partitions 95 objects 95`; serves the last write 95 of 95 | same, plus `rewrites_on_unchanged_inputs 0` |
| 3 | `current_method_available 95 stale_pick 0` | `dossier_pick names 95 current_method_available 95 stale_pick 0` |
| 4 | round 11's case line | `body 102 heading_only 0 absent 183 sum 285 ordering_held 34 ordering_violated 0 ordering_na 61 unit_carried 11 currency_set 5 currency_null 29`: equal |
| 5 | HEI, CPA, SHOP equal to the legacy `/4` object | all three served from `research_dossier/`, with `fields`, `cases` and `inputs` equal; `artifact research_dossier` (legacy `research-dossier`), as the half predicted |

## 4. The one real run

`read_dossier` through the real entry point against the live bucket, for three names (line 5,
`checks/round12/r12_verify.py`). A first run keyed the names with spaces and got a `LookupError` on the partition
`security_key=HEI US Equity`. That was my key format, not the store: it re-ran with the stored keys and is recorded as run.

## 5. Rows -- dispositions for the L9

None filed this round. That zero is real: the same read finds round 11's `Z-W1-S14` / `Z-S57` 4 times.

## 6. Judgment criteria owed to `3.0.0_SA_CVO~Z` at L9

None. `n-1` carries three mechanical criteria and no judgment criterion. The round's plausibility oracle is the content
equality in s.3 lines 4-5, not a reading. If the CVO wants a reading, the artifact is any name's served dossier under
`research_dossier/` against its legacy `/4` twin.

## 7. Enrichment candidates for the round-12 analysis

1. **FWD-12 render half:** `AMGT_RESAPP`'s vv-4 re-land (`2.0.0_SA_COO~Z`) can now grant `amgt/harvest/gold/research_dossier/`
   and redeploy onto this code. Until it redeploys, the deployed Lambda reads the legacy prefix, which is whole and unchanged.
   That work is RESAPP's, not a CORPUS cell.
2. **Legacy objects:** the 846 under `research-dossier/` are no longer read by trunk code. Deleting them is out of scope here
   and needs the operator's word.
3. None blocking.

## 8. Bounds and residue

- No vendor or gateway call. Served-plane writes this round: 95 new objects under `research_dossier/`; no delete, no overwrite.
- Worktrees `/c/tmp/wk-crps12-1` and older hold only workers' untracked scratch; removal is a forced delete on the operator's word.

-- `2.0.0_SA_COO~X`
