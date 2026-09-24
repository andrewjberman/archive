# AMGT_CORPUS -- round 3 drain-end packet (the COO's task-order packet at drain-end; L8 hand-off input)

**DRAFT, 2026-09-24 ~22:0xZ, by `2.0.0_SA_COO~X`.** Section 1 is final. Section 2's last three drain duties are in
flight; this file is updated in place as each lands, and the L8 hand-off to `3.0.0_SA_CVO~Z` follows the last.

## 1. Orders -- terminal state per task order (5 of 5 issued, 5 of 5 complete, all drained)

Issuance @`6108b0d804` off decomposition v3.0 @`d63cdd71ca`. Every grade below is this seat's own run at the worker's tip
before the drain.

| order | cell | worker | close commit | drain into CLOUD | grade at the drain |
|---|---|---|---|---|---|
| `TO-CRPS-e-2` Model-block pull gains the 22 mnemonics | e-2 | `~4` | 77fea54b48 | `bb6b1f2f25` | HIST 23->39, FORECAST 5->11, 66 distinct, 66 basis; dry run carries the 22; 3-security cap refuses 4 |
| `TO-CRPS-e-3` sector template body a function of its key | e-3 | `~3` (worker-light) | 4d196099bc | `1266b834ec` | 2 of 2; `--write` rc 0 over 218 reports, 9 objects written once, a second run all existed |
| `TO-CRPS-e-4` production-sequence runner | e-4 | `~1` | dcfb64fbac | `5637be19e9` | 9 of 9; `--list` states the ruled 10-step order; citation `types.ts:973` live |
| `TO-CRPS-e-1` curated evidence table | e-1 | `~2` | 77782b0da1 | `21e624a003` | 9 passed; dry run population 41 evidenced 40 called 40, bloomberg_calls 0; fire refused without the env gate |
| `TO-CRPS-e-5` served-as-empty-shell disposition | e-5 | `~1` | 9cc0599acc | `dae976b3b0` | 5 passed; census 94 = 44 dossier-served + 9 served-as-empty-shell + 41 unresolved; never-prose named 12 |

All five instances `proof-of-spec-check` VALID rc 0. Worktrees `/c/tmp/wk-crps3-{1..4}` removed, branches deleted.
Issuer amendments during the round (stated in their commits): `c1437f9864` (e-1's evidence table read against the served
pool before spawn), `03baefb8af` (AC1 expect admits `, N deselected`; the decomposition's cells prefixed `CRPS-e-<n>`),
`beaf092dc3` (e-4 AC3 reads `types.ts` from the main worktree). No gate limb graded these modifications (none of the five
declares `<placeholders>`).

## 2. The drain duties (decomposition v3.0 s.5), as executed

1. **The 40-name FIRE -- DONE, 36 of 40 landed.** Pre-flight caught 20 twin records before any write (row Z-S21, the fix
   `2.0.0_SA_COO~Z` @`9ec1226a01`); pair COO @`8bd8ba7e2b`/`498c9aeb01`, CTO `ledger/` @`af08f78a9b`, vendor limb released
   on Andrew-direct R-21 (msg 25761). ONE run @`505fc14404`: batch_calls 1, pool_puts 1, bloomberg_calls 36; served key
   versions 24 -> 25; records 254 -> 238, MEASURED 214 -> 234, UNRESOLVED 40 -> 4; twins 0, multi-claimed 0 of 545 forms,
   214 of 214 prior keys, 36 of 40 landed exactly as called. Two gaps, both rowed and both fixed on the identity surface:
   Z-S23 (4 skipped on keyless rows, @`e772a89bad`) and Z-S24 (16 ENRICH folders lost their form, @`74e6a76e5c`).
2. **The RE-MINT -- IN FLIGHT.** The 4 + AMD (added to the table from its own workbook) + the 16 forms, one put. Pair COO
   half @`2a3319e5ae` (AMD amendment to follow); CTO half owed; a third builder limb (ENRICH with no record to retire adds
   the folder's form) asked of `2.0.0_SA_COO~Z`. Target: 94 of 94 folders MEASURED, resolved at ingest.
3. **The FWD-12 PULL -- DONE (pull); DERIVE held on its pair.** Change-management entry
   `amgt-corpus-fwd12-model-block-pull-20260924` @`9361723c96`. 30 of 30 batches rc 0; 89 of 89 keys landed raw, read back on
   S3 (L1, L2 closed). Derive moves served `derived/model_block` (31 of 89 keys replaced as newest, 58 new; four readers):
   pair COO half @`2a3319e5ae`, CTO half owed; L3 open.
4. **The PRODUCTION SEQUENCE -- running** through the runner after the re-ingest (resolved_folders 73; the 16 + 4 + AMD
   follow the re-mint): `evidence/production_sequence_after_fire40_20260924T212840Z.log`. It runs again after the re-mint
   and after the derive (dossier Model rows carry the 22).
5. **The COO's one real run of each outcome at close:** owed after 2-4.

## 3. Rows filed this round -- dispositions for the L9

| row | class / standing | one line | for the CVO |
|---|---|---|---|
| Z-S21 | OBSERVATION / INERT | pre-flight held the fire before any write (20 twins predicted) | adjudicate |
| Z-S22 | OBSERVATION / INERT | owner's disarm carrier for Z-S17, W3-S3, W3-S4, W2-S5, W4-S3, W3-S5, W1-S6, W2-S6 | may adjudicate the eight on it |
| Z-S23 | OBSERVATION / **ARMED** | 4 folders skipped as already-registered on keyless rows | disarms at the re-mint |
| Z-S24 | OBSERVATION / **ARMED** | 16 ENRICH folders lost their association form; ingest read 73 | disarms at the re-mint + re-ingest |
| W1-S5, W2-S4 | worker rows, INERT | as filed | adjudicate |

## 4. Judgment criteria owed to `3.0.0_SA_CVO~Z` at L9

None cut this round: each of the five orders carries three mechanical criteria. The round's served effects (the crosswalk,
the Model block, the dossiers) are graded at L9 on the COO's real runs in section 2 item 5.

## 5. Enrichment candidates for the round-3 analysis (`1.0.0_SA_CTO~Z`), from this seat's record

1. **A pre-flight must drive the producer's REQUEST path, not only its builder.** Synthetic rows skipped
   `_find_existing` and missed Z-S23; the widened script now calls it.
2. **A pre-flight must census what the downstream READER resolves by.** Twins and multi-claimed forms were zero while 16
   folders lost the form the ingest reads (Z-S24); the script now censuses `crosswalk.harvester_key` per folder.
3. **Run a pre-flight on committed bytes only.** Two readings came from a peer's uncommitted edit in the shared tree; the
   cited run prints `git status` of the imported package beside its verdict.
4. **The worker-deliverables default of `induction_run`** writes its read-back into the worker's folder, which the issuer
   cannot commit (owned-paths clause 4); the issuer moved it by hand.

## 6. Bounds and residue

AMGT only; no library write; no S3 delete; no shared push (`0.0.0_AB_MSTR~Z` integrates). Residue: the 58 new model blocks,
once derived, have an S3 delete as their only rollback (disclosed in the derive pair).
