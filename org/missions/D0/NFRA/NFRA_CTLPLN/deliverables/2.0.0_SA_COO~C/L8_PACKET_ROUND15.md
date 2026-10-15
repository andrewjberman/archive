# NFRA_CTLPLN round 15 -- drain end and L8 packet, for 3.0.0_SA_CVO~L and 1.0.0_SA_CTO (issuer 2.0.0_SA_COO~C, 2026-10-15 ~05:2xZ)

All three round-15 orders are `complete` (issuance `cd1e04765b`, decomposition `NFRA_CTLPLN_DECOMP.round15.md`). `python .tools/round-close-check.py --project NFRA_CTLPLN --round 15` reads `verdict=MAY-CLOSE`, `judgment=2 graded=2 ungraded=0 self_graded=0` (no judgment criterion of this round; the two are earlier `TO-APPLY` rows). Pins are commits on `box/laptop`, LOCAL unless stated. Each cell below carries the issuer's own re-run on the worker's branch, not the worker's report. The round was held from about 00:5xZ to 03:2xZ by the account spend limit; Andrew lifted it (`ANDREW_WORD_SPEND_LIMIT_LIFTED_20261015.md`, `9611167855`).

## 1. Judgment criteria owed to the CVO

None.

## 2. Cells, their orders and the issuer's own re-run

| cell | order status | merge / flip | issuer re-run |
|---|---|---|---|
| `CT-ae-1` | complete (LOCAL; kills only the processes the test starts) | `a133dfa1e5` / `ee04570c0f` | `KILL-MAINT-PLANTED cases=10/10 ok=True`; `STOP-AT-DESCENDANT cases=27/27 ok=True`; real `claude.exe` seats 8 before, 8 after; the diff touches only `.tools/kill-maint.ps1` and the new test (plus the proof instance and the rows) |
| `CT-ae-2` | complete (LOCAL) | `833f1d7bb7` / `d531251edb` | `MEASURE-INLINE-HOLIDAYS arms=5/5 ok=True`; `INLINE-HOLIDAY-SETS found=6 same_2026_2027=5 differs_2026_2027=1 unreadable=0 ok=True` |
| `CT-ae-3` | complete (WORLD by path floor, no AWS call) | `193269c452` / `0c5972dc80` | `ROUND15-BATCH arms=9/9 ok=True`; `OPEN-CALL-ACT-ROOTS arms=8/8 ok=True`; `SAFE-COMMIT-DERIVATION cases=17/17 ok=True`; the identity-root diff is empty (the search found nothing to reword) |

Every proof instance reads VALID from `proof-of-spec-check.py` on the committed state.

## 3. Real runs of the outcomes

- **`S9118` (FWD-21, FWD-25):** a planted tree holding a foreign `claude.exe` seat (serial `9.9.0_SA_TEST~PLANT`) survived a real `kill-maint.ps1 -Mode scripts -Execute -OnlyPid`; the control tree died; the audit file holds `KILL-MAINT-REFUSED ... reason=seat-boundary`. **The run found a defect:** the held-tree guard SKIPped any tree holding a `claude.exe`, so the seat-boundary refusal was never reached for a seat (row `W97-S1`). The worker's fix (`21ad9d0ca4`, in `.tools/kill-maint.ps1`) judges the boundary first for a held tree and only REFUSES; it stops nothing. `seat-boundary.ps1` is unchanged. The issuer read the diff: a refuse-only addition, no widening of what is killed.
- **Planted shape:** the recipe's literal shape (a `bash.exe` or `powershell.exe` root with a `claude.exe` child) cannot be planted as written (row `W97-S2`); the test plants a `python.exe` root with a `cmd.exe` copy named `claude.exe`. Whether that shape is the one the real reaper meets is not measured.
- **`W94-S1`:** six hand-typed holiday sets, not two. Both MDPF functions match the library for 2026-2027. The one that differs is `inf-gold-freshness-guard` (INF Lambda, no 2027 closure; first miss 2027-01-01). Routed by the CTO (msg 109290) to dell1, before 2026-12-31; row `S9125` (`c38dff9cf3`).
- No UI is touched, so no screenshot.

## 4. FWD state

`FWD-11` is a qualified wait on Andrew's word (open call `laptop-20261014T205216Z-7841`); `FWD-9` PARKED; `FWD-27` waits on Andrew's "another time".

## 5. Rows this round minted

`W97-S1`, `W97-S2`, `W98-S1..S3`, `W99-S1`, all INERT observations, plus the issuer's `S9125` (owner dell1). Dispositions are in each order's `<status_reason>`. Carried: `W99-S1` (the placement-refusal branch of the naming stage, the `W93-S1` shape, a later batch), `S9125` (dell1), `S9119`, `S9103`, `S9120`, `S9122`, `Z-S3`, `W12-S1`, `W89-S3`. `S9118` is closed by this run.

## 6. Not measured here

Any run of `kill-maint.ps1` against a real foreign seat (the test plants one); the `W99-S1` placement branch (read from source, never exercised); the PRD FWD grade table, which the CTO's coverage read governs.
