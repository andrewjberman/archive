# Never-widen CTO half -- resident r34s (Multi-Comp portfolio path from the common window start; report presentation fixes)

**Seat:** 1.0.0_SA_CTO~DELL2, 2026-10-21 ~08:5xZ.
**Packet:** `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~G2/NEVER_WIDEN_PACKET_RESIDENT_R34S_MULTICOMP_PORTFOLIO_PATH_AND_REPORT_PRESENTATION_20261021.md`
- git blob `c5148a9c27c5c674e1e14e624549fe62d94a0c88`, sha256 `d6809f3b00da67fd404f3bd3a51f269c2bd6caa072ccc5cc958de94bfdc0be17`, commit 155e876231.
- Package pin 5fd1e793f2, tar sha256 fa9506817742..., 5 members change against r34r, 0 added or removed.

## What was read here
- **The defect, measured by exact reproduction** (G2 msgs 11929, 11933):
  - 7J's portfolio row equals the filed amounts bought at 2016-10-20, the start of the 10-year price window, then rebased at the common window start 2024-04-30.
  - By then SPY had drifted to 60.1 against a filed 44.
- **The fix:** `buy_and_hold_from` buys the filed amounts at the common window start, in `_compare_stage` only. It is graded by `ar_window_checks.py`, which fails at the base and passes at the pin.
- **The Overview path is unchanged.** Run 7f reproduces exactly, and its caption already states its semantics.
- **Presentation:**
  - the false "no row has a value" sentence is removed;
  - the n/a periods are named in words;
  - the comparison elements are kept together on a page;
  - `{portfolio_name}` now prints as "Your portfolio".
- **Unmoved:** registry, bindings (package_pin only), run.json, lease, budget and tiers.

## Both branches
- **V2S OK:** r34s runs. Run 7K (Multi-Comp, new holdings) is the live proof. G2 reads its PDF against an independent recomputation: the portfolio row must reproduce, and the false sentence and the raw placeholder must be gone.
- **Not OK:** roll back to r34r and report. No retry.

## Conditions on the apply
- Y2's residue-delete order (TO-RUN-RESIDUE-DELETE-7E7J) is CLOSED first, and nothing else is open on IB2.
- Outside 11:30Z to 14:15Z.
- Andrew is told the Multi-Comp sample is superseded once 7K's read passes, never before.

## Signature
SIGNED, CTO half, bound to the packet blob and sha256 above.
