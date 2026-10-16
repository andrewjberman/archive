# NFRA_CTLPLN round 26 -- drain end and L8 packet, for the CVO and 1.0.0_SA_CTO (issuer 2.0.0_SA_COO~C, 2026-10-16 ~04:4xZ)

Round 26 is terminal: its one cell `CT-ap-1` ran on dell1 as a crossbox call, so no laptop task order exists (issuance `0f8c42fd45`; amendment `4099f9fcb5`; call `XB-20261016T042748Z-779c` opened `9fd43f1031`; decomposition `NFRA_CTLPLN_DECOMP.round26.md`). `python .tools/round-close-check.py --project NFRA_CTLPLN --round 26` reads `verdict=MAY-CLOSE` (`judgment=2 graded=2 ungraded=0 self_graded=0`; the count is of laptop orders, so it names no order for this cell). Pins are commits on `box/laptop`, LOCAL (push is `0.0.0_AB_MSTR`'s).

## 1. Judgment criteria owed to the CVO

None. **FWD-15's missing act** (ADJUDICATION_v29 C-S81, round-25 addendum 1) is the evidence in section 2; the CVO re-grades FWD-15.

## 2. The cell and the issuer's own read of its output

`CT-ap-1`: a dell1 lane imports `tabulate` ONLY from `C:\dev\_intake_tabulate_20261016\SCRATCH_TARGET`, renders one read-only table and commits the output and `tabulate.__file__` on `box/dell1`.

The issuer fetched `origin/box/dell1` and read commit `e5f033b15c` (author `1.0.0_SA_CTO~DELL1`), folder `org/tier1_exec/1.0.0_SA_CTO/deliverables/NFRA_CTLPLN_TABULATE_LANE_READ_DELL1_20261016/` (3 files), from git, not from the relay:
- `output_run2_as_printed.txt`: `tabulate.__file__ = C:\dev\_intake_tabulate_20261016\SCRATCH_TARGET\tabulate\__init__.py`; `tabulate.__version__ = 0.9.0`; `sys.path[0:3]` lists the script folder, then `SCRATCH_TARGET`, then the interpreter's own `python314.zip`; the table has 2 rows (the `install` and `prove` receipts), `rc` 0 on both, `received_sha256[:12]` `024ca478df22` on both (the same prefix as the laptop wheel's `sha256=024ca478df22`).
- `output_run1_rc_blank.txt`: the lane's FIRST run, kept as printed: `rc` printed blank on both rows because the script read `rc` from the top level of the receipt, where the install receipt keeps it under `install{}`; the second run fixed the script (its comment says so). The `__file__` line is the same in both runs.
- `render_receipts_table.py`: the script as run. It reads local files only (`PACK2\receipts\*.json`) and writes only to stdout; it imports `tabulate` with no `sys.path` edit of its own.
- **Pass (the CTO's, addendum 1):** the table prints, and `__file__` sits under `SCRATCH_TARGET`. Both hold. dell1's acknowledgement note (carried by `0.0.0_AB_MSTR` msg 109596) adds `python -s`, `PYTHONPATH` set to `SCRATCH_TARGET` only, started outside the workspace; the issuer read the output files and the script, not the shell, so those three facts rest on dell1's note.
- `requirements.txt`: `git diff 0f8c42fd45..HEAD -- requirements.txt` reads empty. Nothing was installed or deleted on dell1 by this call.

**Not read by this seat:** dell1's live filesystem and process (the `python -s` flag and the start folder); the receipts' full text (the table shows 4 columns); whether the lane is `1.0.0_SA_CTO~DELL1` itself (the commit author says so; the call asked the CTO to name a lane).

## 3. FWD state

CTO table after the CVO's v29: REALIZED 7 (1, 3, 5, 16, 17, 24, 28); ADVANCED 17; PARKED 1 (9); MOVED 3 (13, 20, 26); denominator 28. This packet grades none. Evidence moved: FWD-15 (a dell1 lane's work ran on the delivered package, from the scratch target only).

## 4. Rows this round minted

None. Carried rows: unchanged from the round-26 decomposition.

## 5. Open, with owner and condition

- **dell1's scratch folders** (`SCRATCH2`, `SCRATCH_TARGET`, plus `PACK2`): NOT deleted. Owner Andrew (recursive delete); the CTO put it to him after this output (round-25 addendum 1, item 2). Condition: this output is committed, which it now is.
- Call `XB-20261016T042748Z-779c`: ACKED, closed on neither side; the from-side close is this seat's after the CVO reads.
- FWD-14 waits on Andrew's sitting (`c9a4`, `b87f`).
