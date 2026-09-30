# AMGT_CORPUS -- round 14 drain-end packet (the COO's task-order packet at drain-end; L8 hand-off input)

**By `2.0.0_SA_COO~X`, 2026-09-29 ~21:2xZ.** Five orders were issued in one issuance (@`a592fb2bf0`, decomposition v14.0). All
five are complete, re-graded at each worker's tip by this seat, and merged. The round carried ONE served write under a signed
pair (p-5). The site-Z crash at 15:34Z killed the first spawn of p-1/p-2/p-3/p-5 with 0 commits. They were re-dispatched at
~18:4xZ under the post-crash restart (`ANDREW_DIRECT_20260929_183xZ_SELF_DRIVE_AMGT_FABRIC_OPS.md`). Steps 1+2 of the
post-crash edict are recorded in `org/tier1_exec/2.0.0_SA_COO~X/drive_log_20260929T18Z.md`.

**R-4:** graded this round: none by this seat (L9 is the CVO's; the round-14 analysis grades). Graded ever: 19 of 19. Endpoint
denominator: 19.

## 1. Orders -- 5 of 5 complete, drained

| order | cell | worker tip | drain | this seat's own run at the tip |
|---|---|---|---|---|
| `TO-CRPS-p-1` | FWD-9 inside its mkdtemp bound | `5c2951a388` | `975dbcd17f` | proof VALID; AC1 `4 passed`; AC3 `code_census rc 0 library_write_calls 0 temp_new_entries 0`; AC2 `negative_control rc 0 ingest_rc 0 put_performed 0 temp_new_entries 1` (see row `Z-W1-S17` below) |
| `TO-CRPS-p-2` | FWD-4 planted drive | `bf0860c49e` | `15fd9e4123` | proof VALID; AC1 `fwd4 will_add_before_add True ambiguous_refused True vendor_calls 0 s3_writes 0 poison_positive 4 of 4`; AC2 `7 passed`; AC3 `paths_outside_grant 0` |
| `TO-CRPS-p-3` | FWD-17 scratch drive | `986c886b9a` | `49d84a344c` | proof VALID; AC1 `fwd17 new_report_id16_beside_old True inputs_sha16_changed True newer_pillars_served True prior_as_of_reads True unchanged_rebuild_wrote 0`; AC2 `445 passed`; AC3 `paths_outside_grant 0` |
| `TO-CRPS-p-5` | ML_FP pillar body, Z-W1-S16 | `a53f4c4bfc` | `34bbf74213` | proof VALID; AC1 `44 passed`; AC2 `p5 ML_FP_Equity pillars 5 empty_text 0 \| IMB_LN_Equity pillars 6 empty_text 0 \| ADBE_US_Equity pillars 2 empty_text 0`; AC3 `455 passed` |
| `TO-CRPS-p-4` | six render-owned fences on the deployed function | `ae9748bf1f` | `eb36437bcf` | proof VALID; AC1 `outcomes 6 of 6 rows_valid 6 entry_named True deployed_read True` / `VALID`; AC2 `fence_quotes_verbatim 6 of 6`; AC3 `paths_outside_grant 0` |

**Mid-round acts by the issuer:**
- **p-1 AC2 temp entry.** The one entry was `amgt_corpus_census_ni2_stj4`. It persisted with its positive-control plants,
  which the fixed arm removes. It was written by the unfixed code in the sibling `wk-crps14-5r` suite, whose
  `readonly_proof.py` had 0 rmtree calls at the time. This is the case row `Z-W1-S17` names, so the order was graded VALID.
- **p-5 AMENDMENT 1** @`af9e934ae2`, on the worker's ARMED row `Z-W5-S5`. The first pass (`708242756c`) served ML_FP ABSENT.
  This seat re-read the extract `362ec404b3d2eba8` (lines 675-688): five bold-first, period-led pillars with bodies. The CTO's
  round-13 ruling routes a source that has text to the reader repair, so AC2 was pinned to `pillars 5`. The first worker was
  not resumable, so a fresh `~5` built the repair on the same branch.
- **p-4's spawn was held on both triggers.** The first ww-1 entry closed ABANDONED NOT-STARTED (`8d79cf769c`); its restart
  closed at `4a5eeb4458`. p-4 was spawned at 20:45Z, after the restart closed and after p-5's served act, so it read the final
  served state.

## 2. The served act (p-5) -- change entry `amgt-corpus-r14-continuation-v3`, CLOSED 4 of 4 @`247d2dace6`

Pair: COO `69e88e71ad` and CTO `9e1da13005`. CTO condition 1 was met: the ww-1 restart's V1 leg closed at 19:56:38Z, before the
merge. Condition 2 held: no consumer ran between legs M and C.
- **M:** merge `34bbf74213`. Six foreign 4.0.0_SA_CRO~Z paths rode the `--continue` (row `Z-S59`).
- **C:** `continuation --write` wrote 95 of 95, 0 ERROR. The table went 225 -> 320 objects (`evidence/r14_continuation_write.log`).
- **D:** `dossier --write --workers 10` wrote 95 of 95, 0 ERROR. The table went 95 -> 190 objects (`evidence/r14_dossier_write.log`).
- **V** (`evidence/r14_after.txt`):
  - ML_FP serves 5 pillars with 0 empty.
  - IMB_LN (6) and ADBE_US (2) are unchanged.
  - `current_method_available 95 stale_pick 0`.
  - `case_census` equals round 12's line.
  - A field diff of each new object against its predecessor, over 95 of 95 names: only `thesis_pillars` changed, on
    ML_FP_Equity.

## 3. The measurement (the workers'; each is the clause as written, not a grade)

| FWD | this round's instrument | reads |
|---|---|---|
| FWD-4 | p-2 planted drive through `induction_request.run` | WILL-ADD printed before any add; the ambiguous name REFUSED; transport refused; poison 4 of 4. The organic arm (Hitachi) still reads NO_EVIDENCE (`Z-S58`). |
| FWD-9 | p-1 arm on the whole library | the real negative control ran inside ONE mkdtemp directory, asserted removed (`scratch_removed True`); `stored 356 existed 356 read_failed 0`, actual S3 puts 0 |
| FWD-17 | p-3 drive over the real stage functions with `StubS3Client` | a new report_id16 lands beside the old; inputs_sha16 changes; newer pillars served; prior as_of still reads; unchanged rebuild wrote 0. Two seams were stubbed (typed CLI, dossier clock; `Z-W3-S8`). |
| FWD-10, 11, 12, 15, 16, 18 | p-4 on the deployed `opal-amgt-scoped-api` (CodeSha256 `lg6NJ2JL...`, 19:18:58Z) | **6 of 6 unmet, owner AMGT_RESAPP.** /thesis passes only `model.team_cases` from the dossier (33 of 33 per case equal); pillars 0 of 157, management 0 of 46, fund/position 0 of 46, terms 0 of 157; portal DEV `ac8265668d` renders the Base case only |

## 4. The one real run (`evidence/r14_real_run.txt`, CLOUD `eb36437bcf`, 21:13:29Z)

This seat invoked the deployed /thesis route (read-only, through AMGT_RESAPP's capture library):
- **ML_FP_Equity:** dossier `as_of=2026-09-29.d667004f7e2ea259.json` carries 5 pillars; /thesis returned 200 with 0 of 5 pillar
  leads and team_cases base/downside/upside.
- **IMB_LN_Equity:** dossier carries 6 pillars; /thesis returned 200 with 0 of 6 pillar leads.
- This equals p-4's rows. The data half this project owns is served in the store; the render half is AMGT_RESAPP's.

## 5. Rows -- dispositions for the L9

| row | class / standing | disposition asked |
|---|---|---|
| `Z-W1-S17` | OBSERVATION, INERT: `temp_new_entries` counts the shared temp dir, so sibling worktrees on unfixed code bleed into it | for the analysis. The source stops once every worktree holds `975dbcd17f`. 93+ legacy `amgt_corpus*` entries sit in system temp for operator cleanup. |
| `Z-W3-S8` | OBSERVATION, INERT: typed `--write` and the dossier clock were stubbed in the FWD-17 drive | for the analysis: whether the CLI limb needs its own exercise |
| `Z-W5-S4` | OBSERVATION, INERT: the order said the key excludes METHOD_VERSION; the code includes it | ruled in the pair (every name moves key; landed) |
| `Z-W5-S5` | ARMED -> DISARMED by `Z-S60` | closed: ML_FP serves 5 pillars |
| `Z-W5-S6` | OBSERVATION, INERT: the served lead drops the trailing period (colon precedent) | no change ruled by this seat |
| `Z-W4-S5` | OBSERVATION, INERT: `BP/` and `NG/` partitions raise SlashSafeKeyError through `read_dossier` by partition name, so the sweep reads 93 of 95 | for the analysis: a key-encoding repair cell, or accepted |
| `Z-S59` | OBSERVATION, INERT: `safe-merge --continue` named 6 concurrently-staged foreign paths and still committed them | for the analysis: route to the tool's owner |
| `Z-S60` | the disarm above | -- |

## 6. Judgment criteria owed to `3.0.0_SA_CVO~Z` at L9

None on the orders. The judgment calls made:
- **p-1:** AC2 was accepted with `temp_new_entries 1`, attributed to the sibling (issuer's call).
- **p-4:** FWD-12 is graded unmet because its render clause shows only Base, although team_cases are served 33 of 33.
- **p-5:** a lead's trailing period is stripped (`Z-W5-S6`).

## 7. Enrichment candidates for the round-14 analysis

1. **The Hitachi 6501 JP crosswalk row** (1.0.0_SA_CTO~Z msg 26708; AMGT_RESAPP `ROUND_ANALYSIS.round48.md` s.2 ruling 3). The
   folder is newer than crosswalk/v1's vintage and has no identity.
2. **The six AMGT_RESAPP render acts:** one served-reader change passing the dossier's pillars, management, posture, model rows
   and terms through /thesis, plus the portal render. These belong to that project's rounds.
3. **`Z-W4-S5`:** the slash-key read path for `BP/` and `NG/`.
4. **`Z-W3-S8`:** the typed `--write` CLI limb, if the analysis wants it driven.

## 8. Bounds and residue

- One served write, under the pair above. No vendor or gateway call. Lambda reads were invocations of the /thesis route only.
- Worktrees: `wk-crps14-1/2/3/4/5r` are drained, and each branch is merged. `wk-crps14-5` is crash damage, and
  `wk-crps10-1/12-1/13-1` belong to closed rounds. Removing any of these checkouts, and the system-temp `amgt_corpus*`
  entries, waits on Andrew's word.
