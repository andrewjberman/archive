# NEVER-WIDEN SIGNOFF PACKET -- IRPT_BCKEND IB-pr-519 (round 185, workstream ~P)

Order: IRPT_BCKEND.TO-IB-pr-519 (issued by 2.0.0_SA_COO~P2, CTO round-185 analysis item 2, RE 7262). Worker: 0.9.0_WK_IRPT_BCKEND~368.
Scope: census and rebuild of `irpt-export-render` against its CURRENT live bytes, with ONE staged contract re-pinned
(`docs/contracts/investor-reporting/v1/ExportReceipt.schema.json`, v1.1 to v1.2), and a dry-run count of the stored receipts.
BUILD ONLY. Nothing was uploaded, applied, deployed, invoked or signed in, and the backfill tool was never run with `--apply`.
The source-map edit was made in the worktree only, uncommitted, and was reverted (sha256 equal before and after).

Base commit (worker HEAD before the first commit of this order): afa744802ee2dc3fb839dfc1b197306bc331909f.
Pin commit (last commit changing the schema): e8005582a1fde9bf21f70b49f8b773e356a394e7. Old pin: 8d08ee54e488e74ef5bc9f4ba715e0a3cad776f5.

## The served change, in words

The receipt read of `irpt-export-render` (`GET /api/scoped/investor-reporting/export/{exportId}`) passes for a receipt that
carries `facts.covered_account_ids`. Today the live function refuses that receipt: its packaged schema is v1.1 and
`facts` has `additionalProperties` false, so the read fails with "Additional properties are not allowed". The re-pin makes
the packaged schema v1.2. Under v1.2 the read still REFUSES a receipt that lacks the field (fail closed), unless the branch
below says otherwise. No code path changes. The only changed member is the schema.

Never refuse a receipt that exists today, and how this release keeps that rule: the evidence store holds ONE receipt, and it
already carries the field, so the v1.2 read admits it (it is refused today, so the release makes it readable). The dry-run
census counted zero receipts lacking the field and zero unreadable or denied objects. Branch `none_needed` therefore applies.
If a receipt lacking the field appears before the apply, Branch A runs the backfill first (`backfill_first`), so the re-pin
never goes live over a receipt it would refuse. The UNFILLABLE count is zero, so the optional-member branch is not reached.

## Live and built sha256

- Live (CodeSha256 K74JEIjw0NKmy4YfEo7Sb7LcRxEII+/yaYtaKJ3qnD8=, hex 2bbe091088f0d0d2a6cb861f128ed26fb2dc47110823eff2698b5a289dea9c3f),
  read 2026-10-13, LastModified 2026-10-13T12:43:58Z, CodeSize 419460, 66 members. Equal to the source map artifact_sha256 and to
  the bytes fetched to scratch.
- Built (BUILD_ONLY, packed twice, byte-identical; base64 5/9LZBbTEWOfrnNZufc6Mqz5pbDxTxYAxpWcZVURGs4=), hex
  e7ff4b6416d311639fae7359b9f73a32acf9a5b0f14f1600c6959c6555111ace, 66 members.
- Members: 65 identical to live, 1 changed (below). Only-in-built and only-in-live: none.

## The one changed member

`irpt_contracts/ExportReceipt.schema.json`. Built member sha256 118a3575eaf20ff6ffb37d387b0cb3d4bd5e1a4d42ce68c86c07919bc968b4c7,
equal to the repo blob at the pin e8005582a1 (verified by content). Live member sha256 5a7bda2ecddd81eb91423ee1acf4d86b8bca4b3c515dff97e8028420320d69ba
(the blob at the old pin 8d08ee54e4). The old-to-new schema diff is the v1.2 change and nothing else: `revision` 1.1 to 1.2,
the `revision_note` extended, the `covered_account_ids` property added, and its entry added to `required`.

## Source-map row diff (NOT committed by this order)

One `staged_from` row of `irpt-export-render`: `pin` 8d08ee54e4 to e8005582a1, `sha256` 5a7bda2ecddd to 118a3575eaf2. The apply
seat commits this row together with the release. Saved as IB185-1_source_map_row_diff.txt in this folder. The source map was
restored: sha256 f80454ce2367e876617eddfb54d4b06023af517c60ff2f60200c3e777aae0bc3 before and after.

## Signature and attribute instrument (AMENDMENT 1 rule)

Built zip: 1 signature mismatch. Live zip: 1 signature mismatch, the identical line:
`MISMATCH: served:1026 calls interactive_access.InteractiveAccess -- unknown keyword(s) ['profile_reader']`.
The built count does not exceed the live count, and every built line is a live line. Attribute mismatches: 0 on each zip.

This is a LATENT defect carried by the live function, not created by this release. The call sits in `served.py`
`_handle_prospect` (the prospect CREATE_INPUT path, line 1026 at pin 564e604838). The issuer's reachability read: the function's
own operations (`export/entry.py` lines 447-455: submit, receipt, download, custody-report read and persist) never route
there. Row IRPT_BCKEND-D2-W368-S2 stays ARMED, owner the issuer. This release does not repair it. It is a condition of this
packet: no change to `served.py` ships with the apply.

## Open ledgers and sequencing

Deploy ledgers under `org/critical_paths/change_management/` that name `irpt-export-render`: 49 of 1859 files read. All 49
read Status CLOSED. Open markers naming the function: 0 of 788 marker files, across 54 readable worktrees. One worktree
listed by `git worktree list` (C:/dev/wk-irpt-anlreq-104) has no directory on disk and could not be read (row S5). The
source map's own `deploy_ledger` cites a CLOSED ledger that does not name the function (row IRPT_BCKEND-D2-W368-S3).
Sequencing: no open ledger or open marker names the function, so the apply waits on no ledger. A marker found OPEN at a
stale worktree HEAD is a stale view (NEVER-2): its owner closes it SUPERSEDED, and this release closes nothing.

## Branch A -- land digest-gated (never a mint)

1. Rebuild with the release source map. Compare the rebuilt sha256 with the signed built digest e7ff4b64...555111ace
   (base64 5/9LZBbTEWOfrnNZufc6Mqz5pbDxTxYAxpWcZVURGs4=). On any difference ABORT.
2. Upload the built zip under its digest to opal-313476888478-lambda-artifacts (the build script, not this packet).
3. Terraform path `infra/aws/terraform/investor-reporting/export/lambda.tf`, module `irpt_export_render`: the change is
   `s3_object_version` and `source_code_hash` only. Plan to a planfile showing 1 change and 0 to destroy.
4. `bash .tools/safe-apply.sh` on that planfile.
5. Backfill step: NOT needed under branch `none_needed`. Under `backfill_first` the backfill tool's dry-run counts are re-read,
   the tool runs with `--apply` under its own signed pair, and it runs BEFORE the re-pin goes live.
6. Gates before the apply: both halves signed at these packet bytes; the ledgers above CLOSED; the live CodeSha256 equal to the
   start value K74JEIjw0NKmy4YfEo7Sb7LcRxEII+/yaYtaKJ3qnD8=.

## Branch B -- restore the live version (rollback)

The live version is the S3 object version `_LGUODZLsTpblhaTy2ODlBjRnwdx6cW1` of `investor-reporting/irpt-export-render.zip` in
opal-313476888478-lambda-artifacts (IsLatest, ContentLength 419460, content-sha256 metadata K74JEIjw0NKm... equal to the live
CodeSha256). Named by a read-only version list and head-object now; re-read at the apply before any upload. Rollback per key:
`s3_object_version` back to that id, `source_code_hash` back to the live value, and the source-map row back to pin
8d08ee54e4 and sha256 5a7bda2ecddd81eb91423ee1acf4d86b8bca4b3c515dff97e8028420320d69ba.

Receipts under Branch B: no receipt is backfilled under branch `none_needed`, so none is written. The one stored receipt
already carries the field; the live v1.1 schema refuses it today, and Branch B returns to that exact state. Branch B refuses
no receipt that is readable today. It does not refuse the carrying receipt newly. If a backfill had run, the carrying receipts
would keep the extra field, which the live v1.1 schema refuses; that case would be the CTO's and CVO's ruling, not this packet's.

## Red list

`deliverables/0.9.0_WK_IRPT_BCKEND~278/IB117-1_red_list.json` names two target prefixes: `infra/aws/lambda/investor-reporting/_contracts/`
and `docs/contracts/investor-reporting/`. The changed member's repo path `docs/contracts/investor-reporting/v1/ExportReceipt.schema.json`
lies under the second prefix, so it INTERSECTS the red list. The list's `red_test_operations` is `analysis-request-original`. No red
test or red operation names the export receipt: the two failed nodes are the route-response-contract test and the
`analysis-request-original` control. The red list's stop flag is not raised by this member, but the intersection is stated here.

## Consumers (one read-through each)

- The portal's export status read `investor-reporting.ts getExportReceipt` and the poll `submit.ts pollExportReceipt`, named by the
  order. Each reads the receipt through the function's route; each is read through once by the apply seat, not here.

## Receipt counts and the branch

The backfill tool was run in its default `--dry-run` mode only (no `--apply`), with its census written to scratch. It listed one
receipt across the evidence bucket's firms. A cross-check of the bucket's objects under the documented prefix found 47 objects
and one `receipt.json` key. Counts: `receipts_total` 1, `receipts_with_field` 1, `receipts_lacking_field` 0,
`unreadable_or_denied` 0. FILLED 1 (already carries the list), UNFILLABLE 0, DENIED 0. Branch: `none_needed`, because no
receipt lacks the field and none is unreadable. No firm key or export id appears in any tracked file.

## After-read the CTO set

After the apply: one NEW export reaches a readable status on DEV, and the ONE pre-existing receipt (the receipt counted above)
is still readable, now through the v1.2 read. This is a person's read on DEV; no seat can sign in to make it.

## The pair (both UNSIGNED)

- COO half: `2.0.0_SA_COO~P2` -- UNSIGNED at these packet bytes.
- CTO half: `1.0.0_SA_CTO~DELL2` -- UNSIGNED at these packet bytes.

Both halves are signed at these packet bytes before Branch A may run. Any change to these bytes re-opens both halves.
