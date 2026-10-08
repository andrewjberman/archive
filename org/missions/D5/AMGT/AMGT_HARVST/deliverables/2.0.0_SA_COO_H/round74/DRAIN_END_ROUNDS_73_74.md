# AMGT_HARVST -- drain end, rounds 73 and 74 (issuer `2.0.0_SA_COO~H`, 2026-10-08 ~23:0xZ)

## Orders (5 of 5 terminal)

| order | cell | result | merge |
|---|---|---|---|
| `bq-1` | R26(a) lower-case alias read | YES, "target" pairs TGT; 3 passed | drained @afd20e8eac |
| `bq-2` | acceptance on the searched strings (R25/R27, AMENDMENT 1: the union) | 12 passed; SUPERSET 242 of 242; CHANGED 158; ONE-WORD FORMS 67 | HELD (section 86: after gold, own pair, not while a leg runs from the shared tree) |
| `br-1` | R30 capital-initial alias rule (+ the issuer's exact-stored-alias clause) | 7 passed; R30 REMOVES 280 of 46,066 tested (16 securities); SENTENCE-INITIAL 3 of 40; CVO 30 of 30 wrong, bar met (msg 32051) | HELD (own pair, serves after rebuild #11) |
| `br-2` | FWD-18 cycle runner | 12 passed; dry run 4 plans, NETWORK CALLS 0; FT refused | drained @5a2d54eb4a |
| `br-3` | FWD-18 at-log-on installer | -Plan REGISTERED NOTHING, TIMELIMIT PT0S; TASK ABSENT | drained @ef68288dee |

## Rows

- Z-W120-S3 (ARMED, owner this seat): disarmed at HEAD @928dbc98e7 (the three record scripts refuse to write a live
  collector pointer); carrier row Z-S105, DISMISSED_WITH_REASON. comp-surprise `--armed` read 1 before it.
- Z-W126-S1: a stale identity-file pin in `test_bc1_legal_names.py` after the pointer move; fixed @543548f46c (the
  fourth such pin, all mine).
- Z-W127-S1 ruled (`--idle-seconds` accepted); Z-W128-S1 INERT (the checker reads `expect` as a regex); Z-W125-S5 ruled.

## Served state

- Gold rebuild #10 (R28, frozen list): act 2 killed in its gate by `0.0.0_AB_MSTR~Z`'s process GC at 21:48:25Z (my
  detached launch; nothing written); act 3 relaunched in-session 22:08:24Z; GATE HOLDS (mention 48,358 -> 52,282, gone 3
  named, lost 0, unexplained 0; daily other 0); the build step writing the two parts is running. Ledger
  `harvst-gold-rebuild10-act2-m-20261008`, L1 closed.
- Collector ledger `harvst-collector-242-and-the-eight-m-20261008` CLOSED @7e1509b798.
- Seeking Alpha r47 backfill: 126+ of 242 pairs; relaunched in-session 22:10:03Z after the same GC.

## What the analysis has to place (no recommendation is a ruling)

1. **FWD-18 activation vs the merge holds.** A runner that never ends means "not merged while a leg runs from the shared
   tree" never lifts for `bq-2`. The runner is meant to run from a PINNED checkout, so a shared-tree merge cannot reach
   it; the hold could be re-read as "not while a leg runs from the tree being merged into". Mine to amend for `bq-2`
   (section 86 is my decomposition); flagged because it decides when WSJ stops discarding articles.
2. **The `sa` overlap.** The r47 backfill (Andrew 2026-10-06, depth to 2026-01-01) and the runner's `sa` cycle (FWD-18,
   since yesterday) would ask Seeking Alpha twice at once. Options: activate the runner on bbg, wsj and barrons now and
   add `sa` when the backfill ends; or end the backfill. The second is not this seat's.
3. **Merge order (R26):** gold first (`br-1`, after rebuild #11's list-move pair), then acceptance (`bq-2`). Rebuild #11
   (AIG and both OMAB lines, ten titles each to the CVO) is uncut.
4. **Next enrichment:** FWD-18 hop 3, the page that says when a publisher did not run, once cycle records exist.
