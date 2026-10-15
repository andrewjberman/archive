# NFRA_CTLPLN round 19 -- drain end and L8 packet, for 3.0.0_SA_CVO~L and 1.0.0_SA_CTO (issuer 2.0.0_SA_COO~C, 2026-10-15 ~13:3xZ)

All six round-19 orders are `complete` (issuance `afebfdc81a`, decomposition `NFRA_CTLPLN_DECOMP.round19.md`; merges `af828c9472`, `fe16c8c9bc`, `320be97aea`, `3e6257daaa`, `192e5b2e31`, `f6a6ed1e6e`; flips `6c4a5ce6bb`, `0daa16e536`, `f433984a5b`, `6b3f2ccaa3`). `python .tools/round-close-check.py --project NFRA_CTLPLN --round 19` reads `verdict=MAY-CLOSE`, `orders=29 judgment=2 graded=2 ungraded=0 self_graded=0`. Pins are commits on `box/laptop`, LOCAL unless stated. Inputs for the analysis: `ROUND19_INPUTS_FOR_ROUND_ANALYSIS.md` in this folder.

## 1. Judgment criteria owed to the CVO

None. The CVO re-grades all 28 FWDs at its next L9 (CTO round-18 ruling 1); this packet carries the evidence by FWD in section 3.

## 2. Cells, their orders and the issuer's own re-run

| cell | FWD | merge | issuer re-run |
|---|---|---|---|
| `CT-ai-1` | 2, 7 | `192e5b2e31` | `FWD2-BOX-ADDED tools=6/8 not_reached=2 named=6 ok=True`; `FWD7-OVERLAPS total=56 shared=53 split=1 not_same_file=2 unclassified=0 ok=True`; `BOX-LISTS-FROM-REGISTER ... ok=True` |
| `CT-ai-2` | 23 | `fe16c8c9bc` | `SEAT-LIST-SHOW ... stale=none seats=10`; `SEAT-RECORD seats=10 named=10 idle_flagged=5 round_close_reviewer=present ok=True` |
| `CT-ai-3` | 5 | `320be97aea` | `UNSIGNED-PUSH push_rc=0 deployed=0 held=1 ok=True`; `STUB-CONTROL stub_saw=1` |
| `CT-ai-4` | 27 | `3e6257daaa` | `FWD27-LAPTOP-SIDE boxes=3 key_ok=3 password_refused=3 ok=True`; `SSH-VERIFY-SELFTEST cases=12/12 ok=True` |
| `CT-ai-5` | hygiene | `f6a6ed1e6e` | `HYGIENE-TSX ... ok=True`; `HYGIENE-ORG-REF ... ok=True`; `HYGIENE-CLEANUP ... new=0 ok=True` |
| `CT-ai-6` | 16, 19 | `af828c9472` | `INTAKE-REQUESTS arms=15/15 ok=True`; `INTAKE-DOWNLOADS arms=5/5 ok=True` |

Every proof instance reads VALID on the committed state. Two issuer rulings were sent to workers mid-cell: the per-box logins for `CT-ai-4` (from `task-orders/NFRA_CTLPLN.TO-CT-ab-7.ssh-tools-kbdint-and-replan.md` line 30) and the class `NOT-SAME-FILE` for `CT-ai-1` (rule R5).

## 3. What each outcome now stands at (evidence, not a grade)

- **FWD-2:** `FABRIC_ENUM` has been register-derived since CT-t-3/ab-8 (the CVO's 10-13 pin is stale). A fixture box `fixbox` added to a copy of the register is named by 6 of 8 listed tools; 2 not reached (a test that prints no box name, a census that reads no box list). No real box was added and no seat started on a new box.
- **FWD-3:** `crossbox-matrix.py` read 11 of 12 acknowledged at the cut. The open pair was laptop -> dell1, not dell1 -> site Z. Call `XB-20261015T121712Z-5b04` to `1.0.0_SA_CTO~DELL1` is now ACKED (bus `0762eaf5`). My other call, `XB-20261015T121713Z-e670` to site Z, is OPEN, which makes laptop -> sitez the newest-and-unacknowledged file of its pair until site Z acknowledges.
- **FWD-5:** the negative arm, with the real hook and stubbed executors in a temporary repository. The signed-change arm and a real push are NOT run. `D1-S8` stays open. `test_named_commit_deploy.py` stops after case 7 here (`git_bash_resolver`).
- **FWD-7:** 56 overlaps (57 at the cut; one project folder moved), classed 53 SHARED, 1 SPLIT (`.tools/safe_deploy_core.py`, named by MDPF_SECCLASS on dell1 and IRPT_BCKEND on dell2, row `W106-S5`, owner `1.0.0_SA_CTO`), 2 NOT-SAME-FILE (a directory claim against a file inside it).
- **FWD-16 / FWD-19:** the request, decision, status and downloads tools exist and are tested in temporary folders. No real request or decision has been made. The downloads reader cannot attribute a record to a device, because fetch records carry `fetched_by` and no device key (`W111-S1`).
- **FWD-23:** the laptop's seat list is fresh (10 seats, 5 flagged idle or aged). The finished-piece-with-grade element is carried by the round-close output, which prints two `GRADED` lines (`NFRA_CTLPLN-C-S16` and `-C-S17`, CVO `3.0.0_SA_CVO~L`, verdict MET). Round 18 itself had no judgment order (`W107-S2`).
- **FWD-24:** the laptop CTO answered OWED (msg 109405, `org/tier0/STAKES_MATRIX.md:79`). Site Z's answer is outstanding (`e670`).
- **FWD-27:** the issuer's own real run, 2026-10-15 ~13:15Z: `python .tools/ssh-tailnet-verify.py --box sitez dell1 dell2 --user-for "sitez=Opal Bloomberg" --user-for dell1=Test --user-for dell2=Test` printed `key=ANSWERED` on all three (hostnames `Opal_Bloomberg`, `DESKTOP-HK1UU7N`, `DESKTOP-N8RJV0A`) and `KBDINT-NO-PROMPT` for the password arm. Not driven: rc and muse logins, the laptop as a target, the off-tailnet refusal, password login off.
- **FWD-14, FWD-17:** filed for Andrew (`laptop-20261015T123054Z-c9a4`, `laptop-20261015T123058Z-318f`). **FWD-15, FWD-18:** named with owners in the decomposition.

## 4. FWD state

`FWD-11` is a qualified wait on Andrew's word (call `laptop-20261014T205216Z-7841`); `FWD-9` PARKED; `FWD-27` waits on Andrew's "another time" for its person arms.

## 5. Rows this round minted

`W106-S1`..`S7`, `W107-S1`, `S2`, `W108-S1`..`S3`, `W109-S1`, `S2`, `W110-S1`..`S3`, `W111-S1`, `S2`. BLOCKING rows ruled by the issuer: `W106-S3`, `S4` (NOT-SAME-FILE), `W108-S1` (the fixture path was my order's error; the test uses a deploy-scope path), `W109-S1`, `S2` (the logins), `W107-S2` (the grade element, supplied above). ARMED: `W106-S5` (owner `1.0.0_SA_CTO`) and `W111-S1` (owner the issuer; a round-20 cell). Carried: `S9125` (dell1), `S9119`, `S9103`, `S9120`, `S9122`, `Z-S3`, `W12-S1`, `W89-S3`, `D1-S8`.

## 6. Not measured here

The signed-change arm of FWD-5; a real box added to the register and a seat started on it; the other boxes' seat lists; any real package request, approval or refusal; site Z's answers (FWD-3 laptop -> sitez ack, FWD-24); rc, muse, laptop-target, off-tailnet and password-off arms of FWD-27; the PRD FWD grade table, which the CVO's re-grade governs.
