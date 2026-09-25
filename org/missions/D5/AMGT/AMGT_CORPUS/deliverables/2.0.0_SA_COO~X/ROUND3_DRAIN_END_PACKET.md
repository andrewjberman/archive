# AMGT_CORPUS -- round 3 drain-end packet (the COO's task-order packet at drain-end; L8 hand-off input)

**FINAL, 2026-09-25 ~02:2xZ, by `2.0.0_SA_COO~X`** (draft @`0d67f8b268`). Every drain act that can run this round has run;
three are blocked by defects rowed for the round-3 analysis (section 5). L8 hand-off to `3.0.0_SA_CVO~Z` follows this commit.

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

1. **The 40-name FIRE -- DONE, 36 of 40.** Pre-flight held it once (Z-S21, 20 twins predicted; fix `9ec1226a01`). Pair COO
   `8bd8ba7e2b`/`498c9aeb01`, CTO `af08f78a9b`, vendor limb released on Andrew-direct R-21 (msg 25761). ONE run @`505fc14404`:
   bloomberg_calls 36, pool_puts 1; crosswalk 09-24 versions 24 -> 25, UNRESOLVED 40 -> 4, twins 0, multi-claimed 0, 214 of 214.
2. **The RE-MINT -- DONE, 94 of 94.** The 4 skipped on keyless rows (Z-S23) + AMD (added from its own workbook, 41-row table)
   + the 16 lost forms (Z-S24), after three builder limbs by `2.0.0_SA_COO~Z` (`e772a89bad`, `74e6a76e5c`, `b58d5c1d53`). The
   pre-flight was widened to drive the producer's skip rule and census each folder's own form. Pair COO `ae79d37b0c` + A1
   `9e2d8ab2c2` (the key moved to 09-25 past midnight), CTO `35e4cb93ef` + A1 `2a336885fb`. ONE run @`c79872b0ff`: 5 calls, 1 put,
   new key `crosswalk/v1/2026-09-25.json` (before-state re-measured ABSENT): 94 of 94 live folders MEASURED with their own
   form, twins 0, multi-claimed 0 of 564, 234 of 234 prior keys. Re-ingest: **resolved_folders 94, unresolved files 0.**
   Z-S23/Z-S24 disarmed by Z-S31.
3. **The FWD-12 PULL -- NOT REALIZED.** First run passed security keys, not Bloomberg identifiers: every response empty; its
   derive served empty blocks to 31 names for ~7 minutes, rolled back by copy-forward 31 of 31 (Z-S26, incident, this seat's
   act). The terminal then went down behind its updater (Z-S27); after a human sign-in the corrected re-pull brought refdata and
   bestdata but history `{}` for every key -- e-2 grew the historical request 23 -> 39 fields and the client drops a
   request-level error (Z-S29; field limit inferred). No derive ran on it. Served Model state: 31 restored, 58 honest-empty (0
   figures). Ledger entry closed as run-and-rolled-back @`932b3ffeb2`.
4. **The PRODUCTION SEQUENCE -- BLOCKED at step 1.** After the re-ingest, extract refused a write-once collision on Copa's
   duplicate PDF (Z-S30, the Z-S17 class); steps 2-10 skipped, nothing partial served. The earlier post-fire run (steps 1-8
   over 73 folders) completed and was stopped by this seat's own timeout inside the dossier step.
5. **The COO's one real run of each outcome:** the served crosswalk census and the re-ingest above (identity outcome); the
   Model block and dossier outcomes have no real run to show this round (items 3-4).

## 3. Rows filed this round -- dispositions for the L9

| row | class / standing | one line | for the CVO |
|---|---|---|---|
| Z-S21 | OBSERVATION / INERT | pre-flight held the fire before any write | adjudicate |
| Z-S22 | OBSERVATION / INERT | disarm carrier: Z-S17, W3-S3, W3-S4, W2-S5, W4-S3, W3-S5, W1-S6, W2-S6 | adjudicate the eight on it |
| Z-S23 | OBSERVATION / ARMED (legacy) | 4 skipped on keyless rows | disarmed by Z-S31 |
| Z-S24 | OBSERVATION / ARMED (legacy) | 16 ENRICH folders lost their form | disarmed by Z-S31 |
| Z-S26 | OBSERVATION / **ARMED** | INCIDENT: keys passed as identifiers, 31 served empty ~7 min, rolled back; 58 honest-empty | adjudicate; disarms with Z-S29's remedy |
| Z-S29 | OBSERVATION / **ARMED** | history `{}`: 39-field request, client drops the error | enrichment |
| Z-S30 | OBSERVATION / **ARMED** | extract body carries the filename; Copa's duplicate PDF stops the sequence | enrichment |
| Z-S31 | OBSERVATION / INERT | disarm carrier for Z-S23, Z-S24 (94 of 94) | adjudicate |
| Z-S25, Z-S27, Z-S28 | `1.0.0_SA_CTO~Z`'s rows | purpose number; terminal recovery ladder | as filed |
| W1-S5, W2-S4 | worker rows, INERT | as filed | adjudicate |

## 4. Judgment criteria owed to `3.0.0_SA_CVO~Z` at L9

None cut this round: each of the five orders carries three mechanical criteria. The round's served effects (the crosswalk,
the Model block, the dossiers) are graded at L9 on the COO's real runs in section 2 item 5.

## 5. Enrichment candidates for the round-3 analysis (`1.0.0_SA_CTO~Z`), from this seat's record

1. **Z-S29 (FWD-12):** split `model_block_pull`'s historical request to at most 25 fields and merge by date; make
   `blp_client.historical_data` surface a responseError instead of returning `{}`; then ONE pull + derive under the signed
   pair, verified by FY rows > 0 per key. Carries Z-S26's 58 honest-empty blocks to real ones.
2. **Z-S30 (FWD-19 extraction half):** the extract body must be a function of its key, and a content-duplicate pair must
   resolve to one extract; then the whole sequence for the 41 newly inducted names.
3. **Pre-flights drive the REQUEST path and census what the READER resolves by** (Z-S23, Z-S24); the widened script is the
   pattern.
4. **A verify leg checks CONTENT, not presence** (Z-S26: 89 of 89 raw objects existed and all were empty).
5. **Run pre-flights on committed bytes only** (two readings came from a peer's uncommitted edit in the shared tree).
6. **`induction_run` writes its read-back into the worker's folder**, which the issuer cannot commit; moved by hand twice.

## 6. Bounds and residue

AMGT only; no library write; no S3 delete; no shared push (`0.0.0_AB_MSTR~Z` integrates). Residue: the 58 new model blocks,
once derived, have an S3 delete as their only rollback (disclosed in the derive pair).
