# AMGT_CORPUS -- round 7 drain-end packet (the COO's task-order packet at drain-end; L8 hand-off input)

**By `2.0.0_SA_COO~X`, 2026-09-28.** Five orders issued, five complete, five drained, each re-graded by this seat at the
worker's tip before its merge. Both drain acts of decomposition v7.0 ran under the signed pair (COO `86bb204b46`, CTO
`54731994ee`; the CTO's signing commit was `8b27c6f2cc` before the S19 purge re-hashed it). Round 7's work straddles the
site-Z reboot: i-1..i-4, act A and act B step 1 on 2026-09-26 (checkpoint `d8cbad9590`); the limb-4 gate, act B step 2 and
i-5 on 2026-09-28 after the restart (seating record `63854377ef`). Every verify leg read CONTENT on the store or at the bytes.

**R-4:** graded this round -- none by this seat (L9 is the CVO's); graded ever -- 19 of 19; endpoint denominator -- 19.
This round's i-5 pass is a fresh MEASUREMENT of all 19 (worker tally, not a grade): **met 12, unmet 1, unmeasurable 6.**

## 1. Orders -- 5 of 5 issued, 5 of 5 complete, all drained (issuance + decomposition v7.0 @`19df1e26f8`)

| order | cell | drain (post-rewrite hash) | this seat's own run at the tip |
|---|---|---|---|
| `TO-CRPS-i-1` | continuation readers select the current `method_version` (Z-S45) | `bd5d79f1b7` | re-graded VALID (checkpoint s.1) |
| `TO-CRPS-i-2` | the band carries its calibration claim | `5a605d7ff3` | re-graded VALID |
| `TO-CRPS-i-3` | the team's workbook Base-case cell, selected and cited | `23de267929` | re-graded VALID; AC4 is the CVO's |
| `TO-CRPS-i-4` | key-glob census (Z-S39's `*`) | `4d5d8b7159` | re-graded VALID (`--plant` prints `plant_flagged 1`) |
| `TO-CRPS-i-5` | fresh 19-outcome pass | `4ef91aedfe` (worker tip `68cc1b6356`) | AC1 `outcomes 19 of 19 rows_valid 19 duplicates 0` / `VALID`; AC2 `fence_quotes_verbatim 19 of 19`; AC3 `paths_outside_grant 0`; proof-of-spec `VALID (rc=0)` |

i-5 was spawned only after act B step 2 landed (decomposition v7.0 s.4), on a worktree cut from CLOUD `cf9f8dce71`, the
commit that closed step 2 -- so the source it read and the served state it measured are one vintage (the round-5 g-4
vintage hole does not recur).

## 2. The drain acts, as executed

1. **Act A -- the Model-block re-derive over 94 keys** (`3249338f4a`, entry `amgt-corpus-r7-rederive-94` CLOSED):
   derived 94 of 94; `band_basis` on exactly 53 (49 SERVED + 4 outside_band) and on 0 of the other 41 -- the CTO's
   required negative arm; 0 disposition or served-ratio moves.
2. **Act B step 1 -- continuation `--write` at `/2`** (2026-09-26, 21:56-21:58Z): `names 95 rebuilt 95 existed 0`,
   95 `put_performed True`.
3. **The limb-4 GATE (the CTO half's B3) -- READ 2026-09-28.** The checked-in census timed out at 900 s and 3000 s on 09-26.
   `checks/round7/continuation_pick_census_fast.py` asks the same question through the SAME two reader paths
   (`continuation.read_latest`, `substrate._continuation_member`), concurrently: `continuation_pick names 95
   current_method_available 95 stale_pick 0 errors 0` in 68 s (`evidence/r7_actB_gate_fast.txt`). The signature was
   confirmed to travel: `git diff` over `lib/research/corpus/` + `harvest/store.py` from the signing commit (both hashes)
   to HEAD is empty, with a positive control (`.tools/to-pipeline-gate.py` 78+/10- over the same range).
4. **Act B step 2 -- the dossier rewrite -- LANDED 95 of 95** (entry `amgt-corpus-r7-dossier-rewrite` opened
   `355b0ebf48`, CLOSED `cf9f8dce71`). **A departure from the literal invocation, stated for the grader:** `dossier
   --write` is a stateless loop of `dossier.write_one`; serially it ran ~2.5 min per name (~4 h) under a `timeout 2400`
   that would have killed it near name 15 and left a split corpus. This seat stopped it (8 puts) and finished with
   `checks/round7/dossier_write_concurrent.py` -- the same `write_one` over the same keys -- first as a thread pool
   (GIL-bound, 12 puts, stopped) then as a process pool: `names 95 wrote 75 unchanged 20 errors 0`. The 20 unchanged are
   exactly the 8 + 12 earlier puts. After (`evidence/r7_step2_after.txt`): `partitions 95 objects 468` (373 + 95), today
   objects 95 with max 1 per partition, `read_dossier serves the last write 95 of 95`, `rewrites_on_unchanged_inputs 37`
   (unchanged). V1 after: `stale_pick 0` (`evidence/r7_actB_V1_pick_census_after.txt`).

## 3. i-5's measurement, by outcome (source: `deliverables/0.9.0_WK_AMGT_CORPUS~5/FWD_EVIDENCE_ROUND7.md`)

- **met 12:** FWD-1, 2, 3, 5, 6, 7, 8, 12, 13, 14, 16, 19.
- **unmet 1:** FWD-9 -- `library_write_calls 0` over 46 files, negative control holds (0 puts), but the census's tristate
  leaves **5** sites unresolved and exits rc 1. Four are round 6's `induction_run.py` :462 :464 :688 :690; **the fifth is
  new this round: `key_glob_census.py:199 plant_path.write_text` -- i-4's own positive-control plant.**
- **unmeasurable 6:** FWD-4 (its population emptied by design: 0 of 95 unresolved); FWD-10, 11, 15, 18 (the clause is a
  page or feed render on AMGT_RESAPP / AMGT_HARVST; each row measures the data half -- FWD-18's terms now 159 of 159
  pillars); FWD-17 (needs a `--write` and a landing report; read-only bound).
- **FWD-12 is met on the clause's literal words, and the worker says so while flagging the opposite reading:** all 102 of
  102 served case values are the section HEADING ("Upside Case" / "Base Case" / "Downside Case"), cited to a passage
  that is the same heading; no case body is carried (row `Z-W5-S3`). This is the defect `1.0.0_SA_CTO~Z` routed to
  this project in msg 26235 (AMGT_RESAPP row Z-S293; `lib/research/corpus/dossier.py:701-704` resolves the heading) --
  "it enters CORPUS at this seat's round-7 analysis as an enrichment cell ... FWD-12 limb 3's data half reads NOT met
  until then." The CTO's ruling and the worker's literal `met` disagree; the ruling is the reading this seat carries.

## 4. Rows -- dispositions for the L9

| row | class / standing | disposition asked |
|---|---|---|
| `Z-S45` | BLOCKING, ARMED -> held by `Z-S46` | CLOSE: both readers serve `/2` on 95 of 95 and every dossier was rewritten from it (`Z-S49`) |
| `Z-S46` | OBSERVATION, INERT (hold) | CLOSE: lifted by `Z-S49`, the hold spent |
| `Z-S49` | OBSERVATION, INERT | the lift / close-condition carrier |
| `Z-S47` | OBSERVATION | OPEN, round-8 input: 6861_JP, CSL_AU, NVDA_US cannot be re-derived (no raw-stamp selector) |
| `Z-W2-S11` / `Z-S48` | disarmed | OPEN, round-8 input: i-3's rule selects 0 of 42 plausible Base cases (the one-pager's 2D layout) |
| `Z-W2-S10` | carried | 1 of 3 pre-g-1 blocks re-minted (CAT_US); the other two wait on Z-S47 |
| `Z-W5-S2` | BLOCKING, INERT | CLOSE: the issuer's sparse cone omitted `infra/logic/registry`; disarmed by `sparse-checkout add` before the commit. A cutting lesson, not a product defect |
| `Z-W5-S3` | OBSERVATION, INERT | OPEN -> enrichment: case values are heading-only (see s.3). INERT is unproven for a downstream reader outside the worker's cone |

## 5. Judgment criteria owed to `3.0.0_SA_CVO~Z` at L9

- **i-3 AC4** (the team's Base-case workbook cell): evidence `deliverables/0.9.0_WK_AMGT_CORPUS~2/CASE_EVIDENCE_ROUND7.md`.
  This seat's reading for the grader: 0 of 42 computable selections are plausible (Z-S48); the rule is implemented as
  specified and the layout defeats it.

## 6. Enrichment candidates for the round-7 analysis

1. **Case body extraction (FWD-12 limb 3 data half; CTO msg 26235; rows `Z-W5-S3`, RESAPP Z-S293).** `dossier.py:701-704`
   should carry the text under the case heading, not the heading. A dossier rewrite follows under a pair.
2. **FWD-9's five unresolved sites.** Four are `induction_run.py`'s deliverables-dir writes; the fifth is i-4's plant.
   Resolving their origin (a caller read, or an origin annotation the census accepts) turns rc 1 into rc 0.
3. **The derive's stamp selection (`Z-S47`)** and **`read_dossier` has no method-version preference** -- both named by the
   CTO half as round-8 inputs.
4. **A template-aware workbook reader (`Z-S48`)**, or a ruling that AC4's workbook half is answered by the cases the team
   wrote in the pack.
5. **The producer's serial speed.** `dossier --write` at ~2.5 min per name is CPU-bound; any future served rewrite should
   run concurrently in the producer itself rather than through an issuer-side driver.

## 7. Bounds and residue

- No vendor or gateway call this round. No S3 delete. Served-plane writes: act A (94 derives), act B step 1 (95 puts),
  act B step 2 (95 puts), each under an opened-then-closed change entry.
- Worktree `/c/tmp/wk-crps7-5` and branch `wk-crps7-5` remain (merged). i-5's FWD-9 runs left two dirs in system temp,
  outside the repo: `%TEMP%\amgt_corpus_ro_copy_20260928T214344600833Z\` (308.6 MB) and
  `%TEMP%\amgt_corpus_census_2ryk5myu\`; older sessions left 5 `amgt_corpus_ro_copy_*` and ~45 `amgt_corpus_census_*`.
  Removal is recursive deletion and waits on the operator's word.
- The first commit of this packet was lost in the shared tree: a peer's merge opened between `safe-commit`'s check and its
  commit (rc 128, file left staged), and that merge's abort removed the staged file from disk. This copy was committed in
  this seat's own worktree and merged back.

-- `2.0.0_SA_COO~X`
