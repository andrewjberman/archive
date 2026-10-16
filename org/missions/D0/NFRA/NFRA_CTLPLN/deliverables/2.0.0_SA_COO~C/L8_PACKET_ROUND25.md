# NFRA_CTLPLN round 25 -- drain end and L8 packet, for the CVO and 1.0.0_SA_CTO (issuer 2.0.0_SA_COO~C, 2026-10-16 ~04:1xZ)

Round 25 is terminal: its two cut orders are `complete` (issuance `e9b01f6def`, no order at the cut; amendments `dde9454f6b` and `ce28147b01`; decomposition `NFRA_CTLPLN_DECOMP.round25.md`; merges `5834b9f30e`, `8114177059`; flips `66837d94dc`, `070b24cddc`). `python .tools/round-close-check.py --project NFRA_CTLPLN --round 25` reads `verdict=MAY-CLOSE`, `judgment=2 graded=2 ungraded=0 self_graded=0`. Pins are commits on `box/laptop`, LOCAL (push is `0.0.0_AB_MSTR`'s). Inputs for the analysis: `ROUND25_INPUTS_FOR_ROUND_ANALYSIS.md` in this folder.

## 1. Judgment criteria owed to the CVO

None on the two orders. **FWD-17's evidence** (the CTO's relay, msg 109581): Andrew heard the check-8 record of the `tabulate` intake (checked, and not ruled out) and said, verbatim, "thats good, i approve of this"; record `org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261016_034xZ_ALL_19_CALLS_RECS_APPROVED_C02C_POSTPONED.md`, addendum @ba2e7f6545; laptop call `318f` closed. This seat has not read that addendum; it is carried as the CTO relayed it. The CVO grades it.

## 2. Cells, their orders and the issuer's own re-run

| cell | FWD | merge | issuer re-run (main tree, after the merge) |
|---|---|---|---|
| `CT-ao-1` | 16 | `5834b9f30e` | `JOURNEY-FETCH wheels=1 file=tabulate-0.9.0-py3-none-any.whl device=laptop sha256=024ca478df22 requests=4 ok=True`; `JOURNEY-CHECK checks_run=7 failed=0 check8=AWAITING released=False ok=True` (at the merge); proof VALID |
| `CT-ao-2` | 15, 16 | `8114177059` | `JOURNEY-RELEASE released=1 check8=SIGNED ... ok=True`; `JOURNEY-PACK files=4 manifest_ok=True ... ok=True`; `JOURNEY-TAILDROP files_sent=4 failed=0 target=dell1 ok=True`; proof VALID |

## 3. The drive and the one real run (the real entry point, on dell1)

FWD-16's absent-package arm was driven deliberately (CTO round-24 ruling 1), with one test act:
- `requirements.txt` (98 lines, 93 non-empty) did not name `tabulate`; `intake_request.py status --name tabulate --version 0.9.0` read `UNKNOWN`. Request `REQ-20261016T025712Z-tabulate` filed by this lane.
- **Status reads:** 1 of 3 `REQUESTED` (02:57Z, before the decision); 2 of 3 `APPROVED` by `1.0.0_SA_CTO` at 02:59:56Z; 3 of 3 `polars==1.12.0` `REFUSED` (16:33:46Z, 2026-10-15). The status verb is read-only, so each read is the verb's own output at that time.
- Checks 1-7 passed (check 5 not applicable), the CTO signed check 8 (@9aed0e1263) naming the accepted risks; the wheel was released, packed (4 files, local `verify` ok) and Taildropped to dell1 (4 sends, each exit 0 at 03:40-03:41Z).
- **dell1's own receipts, read by this seat from `origin/box/dell1` commit `c25860a18b`**, folder `org/tier1_exec/1.0.0_SA_CTO/deliverables/NFRA_CTLPLN_TABULATE_INTAKE_DELL1_RECEIPTS_20261016/`: terminal outputs `INTAKE-VERIFY pack=PACK2 wheels=1 verified=1 checked=1 stray=0 ok=True`; `INTAKE-PROVE device=dell1 python=3.14.7 wheels=1 installed=1 imported=1 import_missing_dep=0 failed=0 refused=0 ok=True`; `INTAKE-INSTALL ... installed=0 ... dry_run=True ok=True`; `INTAKE-INSTALL ... installed=1 refused=0 target_form=target dry_run=False ok=True`. The install receipt's `received_sha256` is `024ca478df22e934...1948f`, EQUAL to the laptop's wheel; its pip command is `-m pip install --no-index --no-deps --target C:\dev\_intake_tabulate_20261016\SCRATCH_TARGET ...`, rc 0, and its `pip_log` names `...install-pip.dell1.log` with SHA-256 `cd6e3557...6cb9` and 676 bytes: the issuer hashed the committed log and read 676 bytes and the same SHA-256; the prove receipt names `...prove-pip.dell1.log` at 697 bytes and SHA-256 `49006dd4...32cd`, and the issuer's hash of that committed log reads the same. Both pip logs carry `env_pins=PIP_NO_INDEX=1 PIP_DISABLE_PIP_VERSION_CHECK=1 PIP_CONFIG_FILE=nul`. The logs show `inherited_pip_vars_removed=PIP_NO_INDEX`: dell1's parent environment held that variable and the tool removed it before pinning its own.
- `requirements.txt`: `git diff e9b01f6def..HEAD -- requirements.txt` reads empty; the file still has 98 lines.
- Organic ask: dell1 (049f), dell2 (e2a3, answer file on `box/dell2` not yet in CLOUD, read as MSTR quoted it) and site Z (ae75) each answered NONE; the three calls are closed from the issuing side (`4ea99db2b8`).

**Not read by this seat:** dell1's live filesystem (no scratch state read); the stand-in lane's stated read (the table itself) was not run, because the drive asked only for the route; the `e2a3` answer file.

## 4. FWD state

CTO table entering the round (round-24 analysis section 1): REALIZED 5 (1, 3, 5, 24, 28); ADVANCED 19; PARKED 1 (9); MOVED 3 (13, 20, 26). This packet grades none. Evidence moved: FWD-15 (dell-side receipt from dell1 itself with the pip log and a matching SHA-256), FWD-16 (not approved, then approved, then a real delivery of an absent package), FWD-17 (Andrew's approval of the intake record).

## 5. Rows this round minted and the rulings on them

`W126-S1` (the commit gate's client-data check, WARN-only; closed by the CTO's acceptance, round-24 ruling 5). `W128-S1` (the check record at the order's base read check 8 awaiting, so the worker re-ran `check` with the CTO's signature; OBSERVATION, INERT; the same re-run was the duckdb batch's step). No new armed row. Carried rows: unchanged from the round-24 decomposition.

## 6. Open, with owner and condition

- **dell1's scratch folders** `SCRATCH2` and `SCRATCH_TARGET` are NOT deleted: dell1's note holds the recursive delete for Andrew's word (CLAUDE.md, human confirmation for recursive deletion). Owner `1.0.0_SA_CTO~DELL1`; condition: Andrew's word. The scratch holds a pure-Python package, outside any git tree.
- The call `XB-20261016T034630Z-a0a3` is ACKED and not closed on either side; the from-side close is this seat's, after the CVO reads.
- FWD-14 waits on Andrew's sitting (`c9a4`, `b87f`).
