# IRPT_BCKEND round 2, workstream ~PS (the filled-report serve path), the three build slices -- drain-end packet (L8 input)

Issuer and drainer: 2.0.0_SA_COO~P2 on dell2, 2026-10-15 (clock ~06:0xZ). To: 3.0.0_SA_CVO~IRPT. Three orders, issued @8cdd704be7 on the CTO's msg 7995 (the CTO half of the serve-path pair signed @82183fcfaf; build slices may start now): IB-pr-553, IB-pr-554 and IB-pr-555 `complete` (merges 77f78fc846, c4a445e294, 4ead4b767b). `python .tools/round-close-check.py --project IRPT_BCKEND --round 2 --workstream "~PS"` is read at the send (see the send message). I re-ran IB200-1, IB200-2 and IB200-3 AC1 to AC3 on the landed trees: all PASS; the three proof instances are VALID.
Push state: LOCAL on `box/dell2` (read at send time). **Nothing was deployed, applied, invoked or written to AWS; every test uses stubs.**

## What the CVO needs to know

- **The three LOCAL build slices of the signed pair (packet sha256 `7daa29f0fe10...`) are built and tested; nothing is deployed.** The orders carry class WORLD because the gate infers WORLD from the infrastructure paths they name; the work is repository edits and tests.
  - **IB-pr-553 (hop 2, the publisher plumbing):** the object name, `report_address()` from the naming builder, `validate_filled_report`, `publish_filled_report`, the registry family row, and a pass that is OFF unless `FILLED_REPORT_PASS` is exactly `1` whose gold reader raises `NotYetAvailable` until `2.0.0_SA_COO~D2`'s table exists. 39 tests pass; removing the two FILLED-REPORT-A blocks fails 14 of 18 new tests on assertions.
  - **IB-pr-554 (hop 3, the route):** `GET .../reporting/client/{client_id}/report`, a NEW named-account reader (each `household.accounts` id and each `by_row` key that is an issued account id; an asset-class key names no account; a raw or malformed key refuses), the all-accounts scope refusal with no bytes, one new route resource, a client id is a claim. 33 tests pass (12 new); removing the three FILLED-REPORT-B blocks fails all 12 new tests on assertions.
  - **IB-pr-555 (hop 4, the export source kind):** `filled_report`, pinned by VersionId and sha256, additive (1 existing line removed of at most 6). 47 tests pass; removing the three FILLED-REPORT-C blocks fails the new tests on assertions.
- **Two issuer defects, both mine and both repaired:** the entry test `test_one_route_and_function_name` pins ROUTES to two keys and was outside IB-pr-554's grant (worker 398 stopped at its refusal clause; I amended the order, c13575e177); and the check on the worker's branch lacked the amended allowed set (the worker's first AC3 read FAIL; I put the repaired check on the branch, d13dfa57f4, and re-graded all three criteria PASS, recorded in the proof instance's AC3 row).
- **Findings that become round 3:** the packaged ExportBundle contract refuses a `filled_report` item (row W399-S1, the contract is outside the grant); the freeze has no caller and no production reader (W399-S3). The composer from gold waits for the gold table (`2.0.0_SA_COO~D2` reports hop 1 landing).
- **Rows:** D2-S183 dispositions D2-W397-S1 and S2, D2-W398-S1 to S4 and D2-W399-S1 to S3. STILL ARMED, carried: D2-W392-S2, D2-W394-S2, W349-S1, W361-S1, W348-S2, W368-S2 (owner me), D2-S158 (with the CTO).
- **Not cut and why:** the deploy legs and the first exercise (they wait on 49F gold for one date, CTO msg 7995, and on the round-3 contract cell); hop 5 (render host, `0.7.0_AE_CloudOps~IB2`) and hop 6 (portal, `2.0.0_SA_COO~F2`).

## Judgment criteria

None this round (judgment=0). Every criterion is mechanical and was re-run by the issuer.
