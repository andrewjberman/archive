# NFRA_CTLPLN round 24 -- drain end and L8 packet, for the CVO and 1.0.0_SA_CTO (issuer 2.0.0_SA_COO~C, 2026-10-16 ~02:4xZ)

Round 24 is terminal: its one cut order `TO-CT-an-1` is `complete` (issuance `67d0509936`; decomposition `NFRA_CTLPLN_DECOMP.round24.md`; merge `79ee07a0b7`; flip `2a7e490280`). `python .tools/round-close-check.py --project NFRA_CTLPLN --round 24` reads `verdict=MAY-CLOSE`, `orders=24 judgment=2 graded=2 ungraded=0 self_graded=0`. Pins are commits on `box/laptop`, LOCAL (push is `0.0.0_AB_MSTR`'s). The cell's worker `~126` died with the prior session after committing code and tests; this seat re-seated the slot on the same branch to write and commit the proof instance. Inputs for the analysis: `ROUND24_INPUTS_FOR_ROUND_ANALYSIS.md` in this folder.

## 1. Judgment criteria owed to the CVO

None.

## 2. Cell, order and the issuer's own re-run

| cell | FWD | merge | issuer re-run (main tree, after the merge) |
|---|---|---|---|
| `CT-an-1` | 15 | `79ee07a0b7` | `CTan1-AC1` `PIP-LOG arms=7/7 ok=True`; `CTan1-AC2` `INTAKE-RECEIVE-TEST cases=34/34 ok=True` (base 32); proof instance VALID (`proof-of-spec-check`, violations=0); `py_compile` clean |

Diff paths of the branch (`67d0509936..74aeadbbab`): `.tools/tests/test_round24_pip_log.py`, `org/devices/intake/intake_receive.py`, `org/devices/intake/test_intake_receive.py`, the proof instance, `INVESTIGATION_v1.md`; all inside the order's `<paths>` and its deliverables folder.

## 3. The one real run

The tool's own CLI on a synthetic pack, parent `PIP_INDEX_URL` and `PIP_FIND_LINKS` set to canary values: `CT-an-1_REAL_RUN_round24.txt` in this folder. `verify`, `prove` and `install --target` each read ok=True. `prove` wrote `<wheel>.prove-pip.laptop.log` and `install` wrote `<wheel>.install-pip.laptop.log`; each receipt's `pip_log` carries the log's file name, SHA-256 and byte count. Each log records the command (`--no-index --no-deps`), the three pinned variables, `inherited_pip_vars_removed=PIP_FIND_LINKS,PIP_INDEX_URL` (names only) and pip's own output; none holds `127.0.0.1`, the canary folder or a `Looking in indexes` line. LIMIT, as the code says: the log is the command, the environment and what pip printed, not a network trace. Synthetic wheel only; no real package and no dell-side run.

## 4. FWD state

CTO table entering the round (round-23 analysis section 1): this packet grades none. `CT-an-1` moves FWD-15's tool half; dell1 receives the change only after it pulls.

## 5. Rows this round minted and the rulings on them

`W126-S1` (the commit gate's client-data check reports NOT checked on this box; OBSERVATION, ARMED). `0.0.0_AB_MSTR` msg 109561: the WARN is the ruled WARN-only state (Andrew 2026-10-09; the laptop list set aside 2026-10-14 by the CTO's ruling), the same condition adjudicated NOT_A_DEFECT on another box (`COMM_ASSIST` `ADJUDICATION_v10.md` D2-S2). Nothing owed by this seat. Carried rows: unchanged from the round-23 packet section 5.

## 6. Not measured here

The FWD-16 absent-package arm (no driver exists, below); dell1's own `verify`/`prove`/`install` output; FWD-14 (waits on Andrew's sitting); the CVO's read-back of this round.
