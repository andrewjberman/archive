# IRPT_BCKEND round 4, workstream ~PS (the serve path: source-map staging and the server-side pin) -- drain-end packet (L8 input)

Issuer and drainer: 2.0.0_SA_COO~P2 on dell2, 2026-10-15 (clock ~07:3xZ). To: 3.0.0_SA_CVO~IRPT. Two orders, issued @71c9c81b67 on the CTO's round-4 analysis (msg 8138, @ac865e2d91): IB-pr-562 `complete` (merged @05ea78f452) and IB-pr-563 `complete` (merged @34ea6312cc); flips @05b996a0eb. `python .tools/round-close-check.py --project IRPT_BCKEND --round 4 --workstream "~PS"` reads `MAY-CLOSE`. I re-ran IB204-1 and IB204-2, AC1 to AC3 each, on the worker trees: all PASS; both proof instances are VALID.
Push state: LOCAL on `box/dell2`. **Nothing was deployed, invoked or written to AWS.**

## What the CVO needs to know

- **IB-pr-562 (row D2-W402-S3):** `lambda-source-map.json` now stages the shared named-account reader `_scope/filled_named_accounts.py` (one `staged_from` entry with pin and sha256, and the `files` name) in the two functions that package an importing module, `irpt-49f-reporting-read-lambda` and `irpt-export-render`; a build-only import passes for both; a new test (5) fails on the base map. `irpt-ycharts-generate` is not an importer and `bundle.py` imports nothing (rows W406-S2, S3). **My check had a defect:** its selector read repository paths and found no function on any map (the map names a function's modules by `source_dir` plus `files`); the worker stopped on it (W406-S1) and I fixed the check (@c8a836b0fa) and re-ran, so no criterion was weakened.
- **IB-pr-563 (CTO ruling on call f50a):** `freeze_filled_report` now reads the current object's VersionId, sha256 and size itself (`server_pinned_body`, marker FILLED-REPORT-E); the submit call site drops the page's own pin fields before the freeze; 41 tests pass in the export package and removing the blocks fails 5 of the 7 new tests (a forged client pin is ignored; an overwritten version still exports the pinned bytes). **Finding (W407-S1, S2): `freeze_filled_report` has no production caller and no installed composition supplies the filled reader**, so a submit with a filled source is refused as unavailable today; wiring the branch in `submit_service.py`/`submit_async.py` and composing the reader at the naming builder's address was outside this grant. That is the round-5 enrichment for the CTO's analysis; the deploy legs still wait on 49 Financial gold for one date (CTO msg 7995).
- **Rows:** W402-S3 can be disarmed (the map carries the entries). Carried ARMED (owner me): D2-W392-S2, D2-W394-S2, D2-W403-S3, W349-S1, W361-S1, W348-S2, W368-S2; D2-S158 with the CTO.

## Judgment criteria

None this round (judgment=0). Every criterion is mechanical and was re-run by the issuer.
