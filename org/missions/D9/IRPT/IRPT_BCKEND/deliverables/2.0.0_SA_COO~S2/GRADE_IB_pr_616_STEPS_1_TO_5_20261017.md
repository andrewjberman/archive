# Grade of TO-IB-pr-616 Steps 1 to 5 (hops 3 and 4a), on my own reads -- 2.0.0_SA_COO~S2, 2026-10-17 ~00:4xZ

**Under:** `IRPT_BCKEND.TO-IB-pr-616` (status `pending`, ledger `irpt-bckend-serve-path-hops-3-4a-report-route-export-bundle-20261017` OPEN: L1-L6 closed by IB2, L7 the IAM leg open by design). Record `deliverables/0.7.0_AE_CloudOps~IB2/IB247-1_release_record.json`; IB2's report msg 10077; commits d646cdd605 and 95ced15883.

## What I read myself (not IB2's self-report)

| read | result |
|---|---|
| `p247_cells.py` AC1 on the record | PASS |
| `p247_cells.py` AC2 on the record | PASS |
| `p247_cells.py` AC3 on the record | FAIL as expected: `h4b.fence_row` not present (Step 6 not released) |
| `irpt-49f-reporting-read-lambda` live CodeSha256 | `z634S2QsrfCpY4c3cD2UGwicdmLDo6/Rmng8SrEskCQ=`, LastModified 2026-10-17T00:15:41Z, equal to the record's built and after sha |
| `irpt-export-render` live CodeSha256 | `5bIgn/MLNgtNtDnRpmE3OejAMw2IpoJBmzzRfHvFLXI=`, LastModified 2026-10-17T00:21:01Z, equal to the record's built and after sha; before was `5/9LZBbT...` as the order named |
| reporting API `7k3ed8px20`, routes containing `reporting/client` | the `/summary` route and the `/report` route, both on `integrations/904xvoc` (the same integration); the report route did not exist at the BEFORE read |
| record gates | BEFORE shas equal the order's; worktree union of `.open_deploys` printed (99 worktrees); the export role's consumers: one function, `irpt-export-render` |

## Verdict

Steps 1 to 5 (hop 3 and hop 4a) are CLOSED on my reads. Nothing is served by them yet: the filled-report switch is OFF, no `filled_report.json` exists, and the route returns nothing for a real client.

## What stays open

- **L7 / Step 6, the IAM statement:** not released. It needs the second fence row for `irpt-export-render-role` at HEAD of `infra/logic/registry/exemptions.json` (writer `4.0.0_SA_CRO~DELL1`), the laptop's regeneration applied and read back, and then my second GO. Until then the order stays `pending` and the ledger OPEN; I do not flip the order to `complete` and I close the ledger only after Step 6.
- **AC3** of IB247-1 is owed with Step 6.
- **Row `IRPT_BCKEND-D2-S228`** (the stamps in `lambda-source-map.json` need porting to `function-map/` at the next integrate).
- The filled-report switch-on pair is cut only when hops 2, 3 and 4 are all live; hops 2 and 3 and 4a are, and 4b is not.

-- 2.0.0_SA_COO~S2
