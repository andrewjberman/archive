# CHECKPOINT -- 2.0.0_SA_COO~Z -- AMGT_RESAPP -- wound down 2026-09-26 ~22:0xZ on Andrew's word

The successor issuer of AMGT_RESAPP (any `2.0.0_SA_COO` lane on site Z) starts here. Everything below is LOCAL on CLOUD; the push is
`0.0.0_AB_MSTR~Z`'s. The broker's MCP send was DOWN fabric-wide from ~17:0xZ (`0.0.0_AB_MSTR~Z` inbox file 20260926T171529Z): peers
are reached by WRITING a file into `org/mcp/inbox/<base>/~<lane>/` in the `# Message from` shape.

## 1. WHERE THE PROJECT STANDS

- **Round 44** CLOSED by the CTO (`ledger/ROUND_ANALYSIS.round44.md` @799381448c). Its "95 of 95" is CORRECTED by row Z-S289: the OK
  predicate never tested missing absences (86 of 95 names dropped one posture line). Z-S268's graduation is the CVO's to reconsider.
- **Round 45** issued @897d9b4a7d (decomposition s.53, four orders):

| order | holder | state | pin |
|---|---|---|---|
| tt-1 the export carries every page absence; the verdict counts a dropped one | ~163 | COMPLETE, VALID, drained | @00ffce7fbf (portal 4e29386e, UNPUBLISHED) |
| tt-2 the redeploy | `0.7.0_AE_CloudOps~A` | **IN FLIGHT** -- NEVER-2 entry `20260926T2128Z_amgt-tt-2-the-redeploy` opened @ee87bf1506, 10 legs | halves: COO @52128e2a19, CTO @392fee249c |
| tt-3 the AC4 sample, chosen against its clauses | ~164 | COMPLETE, VALID, drained | @c8e0b03ee0 |
| tt-4 the unmarked + carried rows, measured | ~165 | COMPLETE, VALID, drained | @f7e8a62fdd |

- **Issuer evidence committed:** round-45 render on 5174 of tt-3's three post-deploy fixtures, PASS 3 of 3 names, POSITIVE CONTROL 18 of
  18 states, AMD's served base case observed on the page (clause (b)) -- `round45/real-run-*` + `real-run.CONTROL.txt` @5b68ded8e9.

## 2. WHAT THE SUCCESSOR DOES NEXT, IN ORDER

1. **Read tt-2's report.** It lands as a FILE in `org/mcp/inbox/2.0.0_SA_COO/~Z/` (the GO asked for that). Grade its instance with
   `.tools/proof-of-spec-check.py`, confirm the NEVER-2 entry is CLOSED on the TRUNK (not a worktree union), and flip tt-2's `<status>` as
   issuer if the lane has not. Do NOT /unstick the lane (the CTO withdrew that ask at 21:45Z; it was working).
2. **The issuer's real run of FWD-30:** `bash round45/checks/tt-2.AC2.sh`, but save the TSV + log under `round45/close-run/` with a
   PROVENANCE naming the new CodeSha256 and read_at. The falsifiers: abs_missing 86 -> 0 over the live library; and tt-1 AC2 (the planted
   control) still NOT OK on both pinned pre-fix exports.
3. **Packet** `round45/DRAIN_END_PACKET.md`, hand to `3.0.0_SA_CVO~Z` (by file while the broker send is down). Judgment criterion owed:
   tt-3 AC2 -- read `deliverables/0.9.0_WK_AMGT_RESAPP~164/AC4_SAMPLE.json` beside `round45/real-run-*/model.png`.
4. **Portal gitlink:** portal DEV holds tt-1's harness commit 4e29386e UNPUBLISHED; the outer gitlink stays at the published 1e02be40
   (the gitlink-publication check). Ask `0.0.0_AB_MSTR~Z` to publish DEV, then move the gitlink in a follow-up commit.
5. **Round 46 cut** from the CTO's round-45 analysis. Already asked for (CTO file 21:05Z): **a full FWD-1..FWD-31 outcome pass** as a
   cell, run AFTER tt-2's served sweep (model: AMGT_CORPUS CRPS-i-5). Also: the order template must NOT tell a worker to commit the
   portal gitlink (row Z-S290, disarming Z-W163-S1); FWD-24 (the team's cited cases, 34 of 95 dossiers); the stale "methodology to be
   discussed" served reason; raw float repr in served values.

## 3. RESIDUE -- what was cleaned, what is left and why

- **Cleaned:** worker worktrees `/c/tmp/wk-amgt-44-161/162` and `/c/tmp/wk-amgt-45-163/164/165` removed (branches merged on CLOUD).
  All session work committed (this checkpoint's commit is the last).
- **Left for a person (recursive deletes need human approval):** `C:/tmp/amgt-r42-cache`, `-cache2`, `-close`, `C:/tmp/amgt-r43-cache`,
  `C:/tmp/amgt-r43-live95`, `/tmp/tmp.5dHqjUoZQw`. **KEEP `C:/tmp/amgt-r44-close`**: round 45's tt-1 AC1 reads it as its fixed capture.
- **Left for 0.0.0_AB_MSTR~Z:** `org/mcp/BROKER_CLEANUP_FIX_20260926_MSTRZ.patch` (untracked; the fix itself landed @113834f73f).
- **Seats this issuer launched:** `0.7.0_AE_CloudOps~A` is LIVE and executing tt-2 -- not killed; it releases after its report.

## 4. OTHER ACTS THIS SESSION (outside the round)

- `org/mcp/broker.py` stale-cleanup fix @113834f73f, on `0.0.0_AB_MSTR~Z`'s handoff (lane-barred BASE_EXEC); both arms exercised on a
  copy of broker.db. Takes effect on the broker's next restart.
- Rows filed: Z-S289 (round-44 claim correction), Z-S290 (W163-S1 disarm act).

## 5. LESSONS WORTH CARRYING

- A retry loop that waits for a clean index must not leave its OWN failed attempt staged: this seat's did, and blocked every drain on
  the shared tree for ~20 min. Unstage on failure, and name files (safe-commit refuses a directory pathspec).
- A verdict that passes on an absence needs a planted control that makes it FAIL, or its pass is indistinguishable from a blind
  instrument (round 44's 95 of 95; the CTO's /login census).
- A never-widen half written before the producer lands is a prediction until the issuer re-reads it against the landed rule
  (round 45: branch (ii) was incomplete and was amended).
- Timestamps: the CTO's files carry hand-set names (18:30Z on a message the device clock read at ~17:3xZ); row Z-S289's `surfaced_at`
  18:40Z inherits that error, and the true time was ~17:4xZ.
