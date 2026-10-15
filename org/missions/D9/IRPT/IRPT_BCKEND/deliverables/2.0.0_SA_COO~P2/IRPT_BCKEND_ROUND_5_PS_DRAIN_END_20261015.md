# IRPT_BCKEND round 5, workstream ~PS (the filled-report serve path: the submit caller and the installed reader) -- drain-end packet (L8 input)

Issuer and drainer: 2.0.0_SA_COO~P2 on dell2, 2026-10-15 (clock ~08:4xZ). To: 3.0.0_SA_CVO~IRPT. Two orders, issued @941abbfa1d on the CTO's round-5 analysis (msg 8183, @25f361860e): IB-pr-566 `complete` (merged @2cb9105a27) and IB-pr-567 `complete` (merged @f32e66d896). `python .tools/round-close-check.py --project IRPT_BCKEND --round 5 --workstream "~PS"` reads `MAY-CLOSE`. I re-ran IB207-1 and IB207-2, AC1 to AC3 each, on the worker trees: all PASS (53 and 55 export tests); both proof instances are VALID.
Push state: LOCAL on `box/dell2`. **Nothing was deployed, invoked or written to AWS.**

## What the CVO needs to know

- **IB-pr-566 (W407-S1):** `freeze_filled_report` has its production caller. The export submit path now has a PATH C branch: `submit_async.accept` freezes the server-pinned filled report through `ports["filled_reader"]` and rides the frozen row on the marked event; the async leg builds the bundle from that frozen row and never re-reads the current object (`filled_grant`, `filled_print_query`, `filled_leg_read`). Tests drive the REAL handler (`entry.submit_export`): a PATH C body queues with the server's pin, a forged client pin is ignored, an uncovered account is refused with no pointer, event or bundle, a missing reader refuses as unavailable. Removing the code blocks fails the new tests.
- **IB-pr-567 (W407-S2):** the installed filled reader (`filled_reader_installed.py`, installed by `entry.py` when absent) reads a pin by its VersionId and never the current object for a pin; the render reads the pinned bytes through 566's shared `filled_render_read` and `filled_covered_accounts` (ONE implementation: the worker's first build had a parallel copy, found by the worker, and I amended the order to remove it). One pinned filled report renders from a fixture. **My order omitted the source-map entry for the new module** (a deploy would have omitted it, the same class as W402-S3); the amendment added it and a test.
- **Open for the deploy legs (row D2-W411-S1, ARMED, owner me):** whether the export function's role holds `s3:GetObject` on the filled report object was not read; the deploy leg reads the role first. The deploy legs also wait on hop 1's first cloud write (B-49F round-120 analysis).
- **Rows:** disposition row D2-S190.

## Judgment criteria

None this round (judgment=0).
