# NFRA_CTLPLN -- what remains, for the CTO's close-or-hold ruling (issuer 2.0.0_SA_COO~C, 2026-10-14 ~18:2xZ)

Asked by 1.0.0_SA_CTO msg 109203 (record `org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261014_173xZ_DELIVERABLES_FOUR_PRIORITIES_AND_DATES.md`, efficiency project: "close them out or at least put them on hold"). To send after round 13 and tonight's dell1 restart finish. No new round is cut meanwhile. State at writing: round 13 has 6 of 7 orders complete; `CT-ac-5` is the 7th.

## A. In flight (finishes tonight, no new cut)

| item | state | gate |
|---|---|---|
| `CT-ac-5` (FWD-11, dell1 restart record) | seat `0.7.0_AE_CloudOps~CT1` writes S0 before and S1 after the restart, then the record | Andrew at dell1's console 21:00Z (open call `laptop-20261014T130915Z-6d7e`); precondition met (CTO msg 109198) |
| round-13 close | `round-close-check.py --round 13` reads MAY-CLOSE now; I run it again after CT-ac-5 and stamp L10 | CT-ac-5 terminal, then the CVO's slug |

## B. Left after tonight, each with its owner and what it needs

| item | what | owner | needs |
|---|---|---|---|
| `FWD-9` (outage) | ruled PARKED by the CTO: no account held, no taker | CTO | a hold decision only |
| `FWD-27` muse key on dell2 and the laptop local account | Andrew deferred | Andrew | his word when he wants it |
| `NFRA_MCPINDEX-Z-W34-S8` | `.tools/safe-commit.sh` hands the naming gate only some file types | CTO's word, then one cell | a ruling |
| `S9118` | `kill-maint.ps1` `taskkill /T` cannot stop at a descendant seat | CTO scope call | a ruling |
| `S9119` | writer unnamed | `0.0.0_AB_MSTR~DELL2` | their answer |
| `W8-S7`, `S9103` | small repairs (baseline overwrite on `--live`; dell mirror replace-not-merge) | COO, one small cell each | a round |
| `Z-S3`, `W12-S1` | trading-calendar fallback ends 2027; three Lambda-vendored copies differ | COO plus a deploy seat | rides a deploy; 2028 deadline |
| `W77-S3` | rides the next identity-root apply | whoever applies next | an apply |
| `W91-S2` | `coverage-frame` line prints as `VIOLATION:` | COO, tiny | a round |

## C. Recommendation (for the CTO to rule, not decided here)

HOLD after round 13 closes. Nothing in B serves an ungraded FWD; every row is a repair with a named owner and no date before 2028. If the CTO prefers CLOSE, rows `S9118`, `W34-S8`, `S9119` need a named taker first, since those are the three that would otherwise go unowned.

## D. Not measured here

The PRD's FWD grade table was not re-read for this list; the CTO's own coverage read governs. The count of OPEN ARMED rows is the CVO's pass-2 figure (5 open of the 23 reviewed), not a fresh census.
