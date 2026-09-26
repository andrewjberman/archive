# AMGT_CORPUS -- round 6 drain-end packet (the COO's task-order packet at drain-end; L8 hand-off input)

**By `2.0.0_SA_COO~X`, 2026-09-26.** Five orders issued, five complete, five drained, each re-graded by this seat at the
worker's tip before its merge. The drain acts of decomposition v6.0 s.5 ran except one, which this seat HELD on a measured
defect (s.2 item 3, row `Z-S45`). Every verify leg read CONTENT on the store or at the bytes. Work paused 14:4xZ-16:18Z on
Andrew-direct "pause" (relayed by `0.0.0_AB_MSTR~Z`); the subagent work finished inside the pause on Andrew's word "Finish
your work with your subagents, then pause", and the drain acts below ran after his "resume tier 1".

**R-4:** graded this round -- none by this seat (L9 is the CVO's); graded ever -- 19 of 19 (the CTO's 19-outcome coverage read
@`95b6f068ed`, 10 REALIZED after correction A2 @`2dae84b5a9`); endpoint denominator -- 19. This round adds EVIDENCE on five
outcomes: FWD-9, FWD-12 (AC4's workbook half), FWD-14, FWD-17 (b), FWD-18 (data half).

## 1. Orders -- 5 of 5 issued, 5 of 5 complete, all drained (issuance @`e52d265f5c`, decomposition v6.0 @`4115b38e7b`, corrected @`d2ee564a64` and @`8d7ef31385`)

| order | cell | worker | worker tip | drain | this seat's own run at the tip |
|---|---|---|---|---|---|
| `TO-CRPS-h-1` | dossier newest = last write | `~1` worker-light | `7adb677b72` | `dd82056420` | AC1 `4 passed`; AC2 `read_dossier serves the last write 95 of 95`; AC3 `312 passed`; proof VALID |
| `TO-CRPS-h-2` | ratio census + workbook side-by-side | `~2` worker | `bbd15e187e` | `6d18367755` | AC1 `h2 OK census_rows 97 bins_sum 97 keys_with_block 97 workbook_names 53 rows_without_coord 0`; AC2 `h2 determinism identical sha 4639ea944625`; AC3 `h2 floor LN 9 US 16 ASIA 7 refused_in_census 20 of 20`; proof VALID; AC4 judgment below |
| `TO-CRPS-h-3` | FWD-9 third state | `~3` worker-light | `02ae5ab468` | `f5bf53d464` | AC1 `9 passed`; AC2 `tristate library 0 unresolved 4 clear 43 write_like_calls 47`; AC3 `317 passed`; census rc 1 (predicate not weakened); proof VALID |
| `TO-CRPS-h-4` | FWD-14 fence triple | `~4` worker-light | `01f9c49f93` | `90fec781ba` | AC1 `6 passed`; AC2 `fence14 resolved 83 ambiguous 0 empty-or-workbook-only 12 sum 95 outside-fence 0 folders_read 95`; AC3 `314 passed`; proof VALID |
| `TO-CRPS-h-5` | FWD-18 terms (data half) | `~5` worker | `3f328d0ee0` | `b8798b1548` | AC1 `12 passed`; AC2 `pillars 5 with_terms 5 kpi_rows 25 with_terms 25` (AZN_LN_Equity, in memory); AC3 `320 passed`; proof VALID; AC4 judgment below |

Push state at packet time: `dd82056420`, `f5bf53d464`, `90fec781ba`, `b8798b1548` on origin (in origin/CLOUD `7c7a781ee0`,
ls-remote read ~16:05Z); `6d18367755` and every later commit LOCAL. This lane does not push.

## 2. The drain acts, as executed

1. **Every merge** through `safe-merge.sh` on a clean index (retrying only on its staged-changes precondition), the row gate
   and the pipeline gate grading each merged index; the worker's suite re-run at its tip before each merge (s.1).
2. **h-1's exercised arm -- FWD-17 (b) READ ON THE SERVED TABLE.** Before-state at 16:23:45Z (HEAD `174790d015`, the fixed
   reader): IMB_LN_Equity 5 objects, served `as_of=2026-09-25.fc1e3a62101e4598.json`, fresh inputs == served inputs True.
   `dossier --write --security-key IMB_LN_Equity` (write_one twice) printed `unchanged inputs_sha16 fc1e3a62101e4598 wrote 0`
   both times. After: IMB 5 objects, newest write `2026-09-25T21:45:30Z` unchanged; table `partitions 95 objects 373`,
   `rewrites_on_unchanged_inputs 37` unchanged, `read_dossier serves the last write 95 of 95`. DELTA=0 on the store, so no
   pair was owed. Row `Z-S44` disarms `Z-S41` and lifts `Z-S42` (@`66cc58f4a1`). Evidence
   `evidence/fwd17b_imb_write_twice_20260926.txt`.
3. **h-5's served rewrite -- HELD, NOT RUN.** Before opening the pair, the producer's own rule was read: continuation objects
   are named `sha16({method_version, inputs})`, so METHOD_VERSION /2 writes a new object for every name, but both readers
   (`continuation.read_latest`, `substrate._pick_stored`) take the FIRST sorted key whose `inputs` match, and `inputs` does
   not carry the method version. Read-only census over the 95 resolved names: the readers would serve /2 (with terms) on
   **49** and keep serving /1 (no terms) on **46**. Row `Z-S45` (BLOCKING, ARMED) disarmed same turn by `Z-S46` (this seat
   holds `continuation --write`; it is the only writer) @`070cf35da9`. Evidence
   `evidence/continuation_v2_pick_census_20260926.txt`. The dossier rewrite that would follow is held with it.
4. **h-3 and h-4 close runs** on CLOUD HEAD `070cf35da9` (`evidence/round6_close_runs_20260926.txt`): `files_scanned 43`,
   `library_write_calls 0`, `tristate library 0 unresolved 4 clear 43 write_like_calls 47`, the four `unresolved_site` lines
   (all `induction_run.py` :462 :464 :688 :690), both positive controls flagged, census rc 1; coverage dry run `fence
   dossier-served 83 resolved-but-no-prose 12 unresolved-with-reason 0 sum 95 folders_read 95` and `fence14 resolved 83
   ambiguous 0 empty-or-workbook-only 12 sum 95 outside-fence 0 folders_read 95`. No coverage vintage was written: the dry
   run is the real run of the census and nothing it counts has moved.

## 3. Rows -- dispositions for the L9

| row | class / standing | disposition asked |
|---|---|---|
| `Z-S41` | OBSERVATION, ARMED -> disarmed by `Z-S44` | CLOSE: read_dossier serves the last write; the exercised arm wrote 0 twice |
| `Z-S42` | OBSERVATION, INERT (hold) | CLOSE: hold lifted by `Z-S44` |
| `Z-S43` | OBSERVATION, INERT | CLOSE: FWD-2's one bronze-without-silver is the Copa Holdings byte-identical pair |
| `Z-S44` | OBSERVATION, INERT | the disarm/lift carrier |
| `Z-S45` | BLOCKING, ARMED -> held by `Z-S46` | OPEN: needs a reader build (round 7) |
| `Z-S46` | OBSERVATION, INERT (hold) | OPEN until `Z-S45` closes |
| `Z-W2-S10` | OBSERVATION (worker ~2) | READ: three SERVED Base cases (6861_JP, CAT_US, CSL_AU) sit in pre-CRPS-g-1 blocks with no band or currency fields; this seat read them IN BAND (1.257, 0.597, 1.390) but their unit cannot be confirmed from fields the block does not carry |

## 4. Judgment criteria owed to `3.0.0_SA_CVO~Z` at L9

- **h-2 AC4 (FWD-12, the workbook half the round-5 slug left UNGRADED).** Evidence:
  `deliverables/0.9.0_WK_AMGT_CORPUS~2/CASE_EVIDENCE_ROUND6.md` (+ `.json`, producer `case_evidence.py`, deterministic).
  Bins over 97 block keys: `<0.33` 1, `0.33-0.5` 0, `0.5-1.0` 13, `1.0-1.5` 22, `1.5-2.0` 13, `2.0-2.5` 1, `2.5-3.0` 2,
  `3.0-3.5` 1, `>=3.5` 3, `unconverted` 14, `not-computable` 27. Nearest the 3.0 ceiling: below SAN_FP 2.566, ZTS_US 2.522;
  above NFLX_US 3.043, NOW_US 4.453, GPN_US 5.170, CELH_US 23.021. The accept side now has TWO cases in 2.5-3.0 and none in
  0.33-0.5. Workbook cells are laid out by coordinate, never selected. Sample floor (R-1): London 9, US 16, Asia 7 names
  with workbooks; every refused key (20 of 20) in the census.
- **h-5 AC4 (FWD-18 data half).** The criterion reads "on the issuer's served rewrite", which is HELD (s.2 item 3). What exists
  to judge is the in-memory build: AZN_LN_Equity's five pillars carry their heading as the first term, and one also carries a
  KPI term (`dividend`); 25 of 25 KPI rows carry terms. This seat's reading, for the grader: the rule is honest and thin --
  most pillar texts name no KPI-lexicon term, so most terms are the heading alone.

## 5. Enrichment candidates for the round-6 analysis

1. **The continuation readers' method-version preference (`Z-S45`).** Both first-match readers prefer the object whose
   `method_version` is current among input-equal objects, the last write breaking any tie; then the h-5 rewrite and the
   dossier rewrite under a pair. Until then FWD-18's data half is built and not served.
2. **The three pre-guard served Base cases (`Z-W2-S10`).** A re-derive of 6861_JP, CAT_US and CSL_AU under the g-1 guard
   would give them band and currency fields; they read in band today.
3. **FWD-9's four unresolved sites** (`induction_run.py` deliverables_dir writes). The census now names them; whether they
   can reach the library is a read of their callers, for the grader or a cell.
4. **FWD-18 terms richness**, if the grader finds heading-only terms too thin: a wider named vocabulary is a ruling, not a
   worker's choice.

## 6. Bounds and residue

- No vendor or gateway call this round. No S3 delete. The only served-plane act was h-1's exercised arm, DELTA=0.
- Worktrees `C:/tmp/wk-crps6-1..5` and branches `wk-amgt_corpus-6-1..5` remain (all merged); removal deletes the workers'
  scratch and waits on the operator's word.
- FWD-10, FWD-11 and FWD-15 were not cells (their render halves sit on AMGT_RESAPP; FWD-11's obligation is owned there by
  FWD-31 @`c2c6c507d6`). FWD-12 limb 3's data half is MET per correction A2 @`2dae84b5a9`; its render half is AMGT_RESAPP FWD-24.

-- `2.0.0_SA_COO~X`
