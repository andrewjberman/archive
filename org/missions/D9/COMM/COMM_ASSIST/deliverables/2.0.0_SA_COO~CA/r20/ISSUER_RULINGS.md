# COMM_ASSIST round 20 -- the issuer's rulings on what surfaced (2.0.0_SA_COO~CA, laptop, 2026-10-15)

Each ruling cites the commit or read that carries it. A worker row is the worker's: the issuer rules inside its own decomposition and the CVO grades at the compile.

## Rows from the round's workers and seats

Denominator: `COMM_ASSIST-W3*` and `COMM_ASSIST-D2-*` ids in `surprise-channel/investigations/INVESTIGATION_v1.md` (one file). Worker ~30 (CA-l-2) filed no row: no `COMM_ASSIST-W30` id is in that file.

| row | what | ruling | carried by |
|---|---|---|---|
| W31-S1 (BLOCKING, INERT) | worker ~31 found that CAl3-AC3 (the round-19 check `check_l3_batch.py`) fails any change outside four allowed files, so the three sibling test repairs the order requires made it print `ok=False arms=7 of 8` | ISSUER CRITERION DEFECT, mine: a control that could not pass. The worker was right to refuse and not widen the old check. AC3 was re-pointed to the new `r20/checks/check_k2_reader.py` and the order completed with all three criteria PASS | amendment `3653bad156`; CA-l-3 merged `863dc0f739`, complete `eedbf3e881` |
| D2-S2 (ARMED, owner `0.0.0_AB_MSTR`) | the commit gate's client-data check printed WARN on dell2: the hashed account-id list is absent at `C:\Users\Test\.opal\account_id_hashes.txt`, so commit `5bab1a0866` was not checked for client account ids | the same condition as `COMM_ASSIST-W21-S1` and `COMM_ASSIST-W29-S2`, which the CTO's round-18 ADDENDUM 1 (`16e5520ca8`) closed AS BY DESIGN on Andrew's 2026-10-09 word (the check stays WARN-only; the list is deliberately not built). Not a hazard of this round: the commit holds ten evidence files (command outputs, status words, file names, row counts) and no item text. Named for the CVO's compile so it closes with W21-S1 | this file |
| W29-S2 (carried from round 19) | the same absent list on the laptop | closed by design with W21-S1, as in `r19/ISSUER_RULINGS.md` | this file |

## Rulings made inside the round (not rows)

1. **The C1 static scan found two names outside the 12-name manifest.** `check_m4_scan.py` found `root_map.json` and `name_rulings.json` named only inside `opal_naming.py` functions reachable only from `main()` or the `census` family, behind `import opal_naming_rootcheck` at lines 3505 and 3810 (an unpackaged module). The CTO ruled (a) EXCLUDE: both are CLI-only and unreachable from the packaged handlers. The scan implements the ruling (`M4-SCAN ok=True named=14 manifest=12 outside=2 excluded=2`). Carried by `e8367a0075` and the CTO half `0a5a028e6b`.
2. **The round-19 premise was wrong.** Each mail is its own state object (`mail_poll.py:132`, `ldo.send("mail:<mid>")`), so `state["pending"]` is per message and the round-19 `pending_list` fixed a defect that never existed live. Raised with the CTO, who agreed and ruled to leave the code; removal rides the next deploy that touches `mail_requests.py` (ADDENDUM 2 `283c35e975`).
3. **The dell2 pick-up was a read-only crossbox order** (as CA-j-15 was), because `org/devices/crossbox/**` is the manager lane `0.0.0_AB_MSTR`: MSTR committed and sent XB-20261015T072147Z-4a82; the laptop side closed at `5bbfad9003`.
4. **CA-l-2 was declared WORLD, edit only.** The gate infers a risk floor of WORLD for an `infra/` path, so the LOCAL declaration was refused and corrected at the cut.

## Defects of the issuer's own this round

1. CAl3-AC3 was an uncheckable control (W31-S1 above). Cost: one refused order, one amendment, one close-out session. Remedy: the issuer runs every criterion's invocation against the scratch reference before the cut, not only the ones it expects to fail at the base.
2. The round-19 premise that mail objects share one pending slot was never measured against `mail_poll.py` before the cut. Cost: one deployed code path that is harmless and unneeded. Remedy: a premise about a data shape is read from the writer's source line before it becomes a cell.
3. Two clock words (`~02:5xZ` for the real ~01:3x-01:4xZ) written in the round-19 record were corrected at `603acb636a`.
4. Workers ~27 and ~28 (round 19) ended on an API monthly spend limit; the lane was continued by close-out sessions after the issuer measured each worktree.
