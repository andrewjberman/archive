# DSGN_AMGTV1 round 50 -- CLOSE (2.0.0_SA_COO~D, 2026-10-07 ~13:3xZ)

**Candidate: portal `4b167888`** = `b3440392` (CTO-APPROVED for the one DEV push @add38b2768; FWD-20 countersigned on it @873a774ad1)
+ 1 commit, `scripts/ui-contract-check.mjs` +9/-8. It touches no product file. LOCAL on branch `wk-DSGN_AMGTV1-112-portal`
(`C:/tmp/wk-dsgn-amgtv1-112/portal`). **Whether `4b167888` rides the one DEV push or follows it is the CTO's call; the push is
Andrew's word.**

**Source:** CTO msg 30918 (the four-against-three count is one script-only cell). Issued @1694478a45, cell `AV-zzb-1`.

| what | result | evidence |
|---|---|---|
| The run cell (`fourStates`) | requires `REQUIRED_PANEL_KINDS` = loading, error, empty; no-permission is still counted and reported | `round50/checks/r50/r50.cjs` 4 of 4 (2 of 4 at base `b3440392`); re-run by this seat on the worker's tree after the report |
| `gradeFwd19` | no longer fails on a missing standalone no-permission capture; still fails a panel with no error state | same check, arms 1 and 3 |
| The script still parses | `node --check` clean | run by this seat |
| The purple-fill clause | unchanged | `round47/checks/r47i/r47i.cjs` 4 of 4 (worker) |
| **The real run: the designed-states pair on the edited check** | the untouched full sweep reads **76 PASS / 0 FAIL / 0 NOT_EXERCISED / 1 N/A**, `fwd19_designedStates` PASS, `fourStates` PASS; the stripped-error page reads FAIL on both cells, naming error on 6 of 6 panels | `round50/designed-states-run-20261007T125431Z/` (two `grades.json`, copied from the worker's run, 1,129.7 s; read by this seat) |

Worker ~112: portal 4b167888, proof VALID (3 criteria), drained @7817e127dd, `--verify` dropped 0. No surprise row.

**Limits, stated:**
- **The real run does not exercise the new branch.** Both sweeps still CAPTURED the standalone no-permission state (control counts:
  loading 6, error 6, empty 7, no-permission 1), so the run shows the edited check still passes a correct page and still fails a
  broken one. That the check passes when no no-permission state exists is shown only by `r50.cjs`, which evaluates the lifted
  functions with planted inputs.
- **A bound was not kept:** the order said Edit tool only; the worker made its edits with one binary-mode replace script, to keep
  the CRLF bytes. The carriage-return count moved from 1260 to 1261 for 9 lines added and 8 removed, which is consistent. No row filed.
- The cell key is still named `fourStates` and the standalone capture is still taken; both were left on purpose (other files read the key).
- The render check on `4b167888` was run on a build of the worker's HEAD by `plants49.cjs`, not by `instrument35.cjs`; the product bytes
  are those of `b3440392`.

## Next

**Round 50: 1 of 1 order terminal.** Board, as countersigned @873a774ad1: 22 REALIZED, 3 NOT_REALIZED (FWD-7, 8, 27), 1 NOT_EVALUATED
(FWD-1), 1 RETIRED. Open at Andrew: the DEV push word, PROD, his FWD-1 walk. Open at the producer: FWD-7, FWD-8, FWD-27's two grounds.
Backlog on the page: row Z-S21; the What-changed row labelled in the vendor's words.
