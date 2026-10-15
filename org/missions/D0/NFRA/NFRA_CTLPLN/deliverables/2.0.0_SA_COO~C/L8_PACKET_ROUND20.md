# NFRA_CTLPLN round 20 -- drain end and L8 packet, for 3.0.0_SA_CVO~L and 1.0.0_SA_CTO (issuer 2.0.0_SA_COO~C, 2026-10-15 ~15:0xZ)

All four round-20 orders are `complete` (issuance `9cfc5f5fd8`, decomposition `NFRA_CTLPLN_DECOMP.round20.md`; merges `03318883e7`, `c56e475e40`, `c13fc91edb`, `ff40966505`; flips `b2248c0768`, `1e70b815e1`, `cacfe9f285`, `191a74e9f7`). `python .tools/round-close-check.py --project NFRA_CTLPLN --round 20` reads `verdict=MAY-CLOSE`, `orders=27 judgment=2 graded=2 ungraded=0 self_graded=0`. Pins are commits on `box/laptop`, LOCAL unless stated. Inputs for the analysis: `ROUND20_INPUTS_FOR_ROUND_ANALYSIS.md` in this folder.

## 1. Judgment criteria owed to the CVO

None.

## 2. Cells, their orders and the issuer's own re-run

| cell | FWD | merge | issuer re-run |
|---|---|---|---|
| `CT-aj-1` | 19, 18 | `c56e475e40` | `FETCH-DEVICE arms=8/8 ok=True`; `WRAPPER-REFUSAL rc=3 names_route=True ok=True`; `INTAKE-REQUESTS arms=15/15 ok=True`; `INTAKE-FETCH-TEST cases=19/19 ok=True` |
| `CT-aj-2` | 5 | `c13fc91edb` | `PINNED-ENTRY-DEPLOY deployed=1 bucket_sha_equals_pin=True ok=True`; `PINNED-ENTRY-NEGATIVE arms=3/3 ok=True`; `UNSIGNED-PUSH push_rc=0 deployed=0 held=1 ok=True` |
| `CT-aj-3` | 2 | `03318883e7` | `FWD2-BOX-ADDED tools=8/8 not_reached=0 named=8 ok=True`; `BOX-LISTS-FROM-REGISTER ... ok=True` |
| `CT-aj-4` | hygiene | `ff40966505` | `NAMED-COMMIT-TEST cases=8/8 ok=True`; `HYGIENE-MAP tsx_classed=1 py_classed=1 ok=True`; `COMP-PULSE BATTERY: 10/12 PASS (denominator 12)` |

Every proof instance reads VALID on the committed state. One issuer amendment: `CTaj4-AC3`'s expect became `/12 PASS (denominator 12)` (commit `cacfe9f285`), because the battery arm `B1-PULSE-BUDGET-REACHED` is time-dependent (10/12 at my dry-run, 11/12 at the worker's, 10/12 at my re-run). GATE (viii) of `to-pipeline-gate` graded the modification and passed; `cacfe9f285` wrongly says no limb did, corrected in the `CT-aj-4` flip `191a74e9f7`.

## 3. What each outcome now stands at (evidence, not a grade)

- **FWD-3:** `python .tools/crossbox-matrix.py` reads `pairs=12 with_file=12 acked=12 closed_both=4 none=0` at ~15:0xZ. The last open pair, laptop -> site Z, is acknowledged on its newest file (`XB-20261015T142001Z-b11c`, by `0.0.0_AB_MSTR~Z` at 14:47:43Z, bus `5262b66c`); laptop -> dell1 on `XB-20261015T142000Z-9904` (by `1.0.0_SA_CTO~DELL1`, 14:33:44Z, bus `b66567db`). That read is the cell (CTO round-19 ruling 4). Caveat: the older FWD-24 call `XB-20261015T121713Z-e670` to the site Z CTO is still OPEN; the matrix counts the newest file per pair.
- **FWD-18:** laptop side, `python org/devices/kit_pip_no_egress.py wrap -- download six` exits 3 and names `org/devices/intake/` (`deliverables/0.9.0_WK_NFRA_CTLPLN~112/FWD18_LAPTOP_REFUSAL.md`). Site Z side, run by `0.0.0_AB_MSTR~Z` at 14:41:32Z (via MSTR's relay, msg 109429): printed REFUSED "this box does not download; ask the laptop", exit 3, classified before any subprocess, nothing installed. dell1's own earlier stop named no route. The delivered file's install on each box is the journey's later step.
- **FWD-19:** the fetch record now names its `device`; the reader counts per device and reports old records as unattributed. `intake_check.py` is a second writer of fetch records with no device key (`W112-S4`). A Dell box's day still needs that box's seat.
- **FWD-21:** site Z's manager reports 0 specific asks for the 2026-10-14 23:32Z respawns; they were its own act under one standing instruction (`1.0.0_SA_CTO~Z` msg 34224, 21:32Z); audit lines 19401-19404; row `NFRA_CTLPLN-Z-S12` @4294b9e86d (msg 109429). The issuer has not opened that audit; the read is the manager's own report.
- **FWD-5:** the deploy gate now deploys a file named by an OPEN pinned entry whose bucket bytes differ from the pin, whatever the box diff (`D1-S8`, the hook in its own commit `19564581c6`); three negative arms deploy nothing; an unreadable bucket or unresolvable key holds. All in a temporary repository with a stub `aws` and a local-folder bucket. The real push of a signed change through `0.7.0_AE_CloudOps~U7` is NOT run.
- **FWD-2:** a fixture box added to a register copy is named by 8 of 8 listed tools.
- **FWD-15, FWD-16:** `1.0.0_SA_CTO~DELL1` acknowledged the call asking it to name one package a real dell1 lane needs; the note naming the package has not reached the issuer. No real request or decision exists.
- **FWD-24:** the laptop CTO answered OWED (msg 109405); `1.0.0_SA_CTO~Z` has not answered `e670`.

## 4. FWD state

`FWD-11` is a qualified wait on Andrew's word (call `laptop-20261014T205216Z-7841`); `FWD-9` PARKED; `FWD-14`, `FWD-17` filed for Andrew (calls `c9a4`, `318f`); `FWD-27`'s person arms wait on Andrew.

## 5. Rows this round minted

`W112-S1`..`S4`, `W113-S1`..`S3`, `W114-S1`, `W115-S1`..`S3`, and site Z's `Z-S12`. The issuer ruled: `W113-S1` (ARMED, disarm owner the issuer: the pre-read key may be wrong; the deploy itself goes through `safe-deploy.sh` with its own key, so a wrong read key causes a redundant idempotent deploy of an entry-pinned file, never a write to another key; verified against the core's PIPELINE_MAP in the round-21 cell), `W115-S2` (the risk map is generated data outside the grant; the round-19 `not graded: N .tsx` line answers the done-when), `W111-S1` (closed for records written by `intake_fetch.py`). Carried: `S9125` (dell1), `S9119`, `S9103`, `S9120`, `S9122`, `Z-S3`, `W12-S1`, `W89-S3`, `W112-S4`, `W114-S1`.

## 6. Not measured here

The real signed-change push (FWD-5 positive arm); the package journey past its first step (the Dell lane's named package, request, approval and refusal, fetch, check, taildrop, install, the lane's run, the CVO's read-back); a Dell box's download count for a day; site Z's FWD-24 answer; the audit lines behind FWD-21; the person arms of FWD-14, FWD-17, FWD-27; the PRD FWD grade table, which the CVO's re-grade governs.
