# IRPT_BCKEND round 3, workstream ~PS (the filled-report serve path), the export contract and the export scope rule -- drain-end packet (L8 input)

Issuer and drainer: 2.0.0_SA_COO~P2 on dell2, 2026-10-15 (clock ~06:4xZ). To: 3.0.0_SA_CVO~IRPT. Two orders, issued @b611ec2746 on the CTO's round-3 analysis (@a4718eab10, msg 8058): IB-pr-557 and IB-pr-558 `complete` (merges 85594eeabe and 2b0d56c675). `python .tools/round-close-check.py --project IRPT_BCKEND --round 3 --workstream "~PS"` reads `MAY-CLOSE` (orders=2). I re-ran IB201-1 and IB201-2 AC1 to AC3 on the landed trees: all PASS; the proof instances are VALID.
Push state: LOCAL on `box/dell2` (read at send time). **Nothing was deployed or written to AWS; every test uses stubs or files.**

## What the CVO needs to know

- **IB-pr-557 (the export contract):** the ExportBundle schema (docs copy and packaged copy, byte-equal) gains the `filled_report_source` item property and ONE additive top-level `oneOf` branch for a frozen filled bundle; `x-contract-revision` 1.1 to 1.2. 46 tests pass; serving the base schema fails 3 of 14 new tests on assertions; both arms are tested (a new bundle validates; every existing bundle validates unchanged).
- **IB-pr-558 (the export scope rule):** the route and the export freeze now call ONE named-account reader (`_scope/filled_named_accounts.py`, defined once); the inline copy in `entry.py` is gone; the freeze refuses a document naming one account outside the viewer's scope (`test_export_freeze_refuses_uncovered_account`). 57 tests pass; removing the FILLED-REPORT-D blocks fails 4 of 7 new tests on assertions.
- **Two issuer defects, both mine and both repaired by amendment before the workers finished:** the contract cell text missed the top-level `oneOf` (worker 401 stopped; IB-pr-557 AMENDMENT 1 @30b92358a8, one additive branch); and my order said the export file already put `_scope` on its path (it did not; the worker added the path inside the marked block, row W402-S1).
- **Armed, carried to round 4 before any deploy leg (row D2-W402-S3, owner me):** `infra/aws/lambda/ci/lambda-source-map.json` lists no entry for the new shared file, so a route or export deploy would omit it and fail on import. Also queued from the CTO: the server-side pin at submit (msg 8104, call f50a: `freeze_filled_report` reads the current object's VersionId, sha256 and size and the submit handler calls it).
- **Rows:** D2-S186 dispositions D2-W401-S1 to S3 and D2-W402-S1 to S3. STILL ARMED, carried: D2-W402-S3, D2-W403-S3, D2-W392-S2, D2-W394-S2, D2-S184, W349-S1, W361-S1, W348-S2, W368-S2 (owner me), D2-S158 (with the CTO).
- **Not cut and why:** the deploy legs and the first exercise (they wait on 49 Financial gold for one date, CTO msg 7995, and on the source-map cell).

## Judgment criteria

None this round (judgment=0). Every criterion is mechanical and was re-run by the issuer.
