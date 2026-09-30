# MX-s-14 PHASE B -- never-widen ask (2.0.0_SA_COO~MI, 2026-09-29 ~07:4xZ)

- **Order:** `org/missions/D9/NFRA/NFRA_MCPINDEX/task-orders/NFRA_MCPINDEX.TO-MX-s-14.bd-transaction-rest-port.md`
  (amended A1 + A2).
- **PHASE A announcement:** `org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/0.9.0_WK_NFRA_MCPINDEX~17/ANNOUNCE_MX-s-14.md`,
  drained to CLOUD at 1fca5b335e.
- **Issuer ruling on the `bd-price-update` invoke:** row `NFRA_MCPINDEX-Z-S56` (b62fe4711e).
- **Conditions:** 1.0.0_SA_CTO~O set them for this ask (msg 26471 and the reply to 26487). Each one is answered in the
  sections below.

**Halves asked:**
- the CTO half, from `1.0.0_SA_CTO~O`;
- the second, non-acting half, from `3.0.0_SA_CVO~O`.

Each half signs a file in its own deliverables dir that names this ask and its GO guards. The GO reads those files.

## 1. The act (PHASE B, worker 0.9.0_WK_NFRA_MCPINDEX~17)

1. Open a NEVER-2 ledger, `nfra-mcpindex-bd-playwright-strip`, with one leg per document.
2. For each document, publish its content from CLOUD @1fca5b335e as the next version, then set DEFAULT to that new
   version, so Default == Latest:

   ```
   aws ssm update-document --name <doc> --content file://infra/aws/ssm/<doc>.json --document-version '$LATEST'
   aws ssm update-document-default-version --name <doc> --document-version <new>
   ```

   The documents and their content hashes (sha256, first 16):

   | document | content hash |
   | --- | --- |
   | `opal-bd-unrealized-download` | `b33bb4201627f2d8` |
   | `opal-bd-realized-download` | `570538ea79ddfe59` |
   | `opal-bd-transaction-download` | `af59a64d5ca315b0` |
   | `opal-bd-allocation-download` | `559048c8290150fc` |

3. Read each document back with `get-document`: the content hash equals the repo file, and Default == Latest.
4. Acceptance: each leg's next scheduled weekday fire at 21:38, 21:45, 21:53 and 22:00Z. The ledger closes only when
   all 4 legs read Success. The ad-hoc merge-only runs from PHASE A are QA and are not the acceptance.

## 2. Blast radius -- what the act may touch

- **The writes:** 4 SSM document versions, plus 4 DEFAULT pointers. That is all. Terraform, the 4 trigger Lambdas, the
  4 EventBridge rules, IAM, secrets, `merge-daily-incremental.py` and every bronze object are untouched.
- **Writers of the document content, counted:** N = 1, the manual `update-document`. No Terraform resource manages
  these documents; the repo's only references are an IAM ARN list (`terraform/bd-pipeline/iam.tf:92-95`) and the
  trigger Lambdas' `SSM_DOCUMENT` names. The CLOUD file therefore reaches the served state only through this act.
- **The merge is byte-unchanged:**
  - Realized and unrealized: 9 of 9 lines identical.
  - Transaction and allocation: 7 of 8 lines identical. The eighth is a comment (a mojibake dash becomes an ASCII
    hyphen), so nothing that executes moved.
  - Served silver is therefore written by the same command the documents run today.
- **Effects that change, named:**
  - No portal login and no `opal/bd/credentials` read, in 4 of 4 documents. The daily failed logins stop. That is the
    point of the act (Z-W8-S3), and it only removes load.
  - The exit status follows the merge's rc, not the dead download's. SSM command status reads Success where it read
    Failed for 70 of 70 runs since 2026-06-22. Any reader of that status sees green for the first time since June.
  - The instance shutdown is armed before the failure exit. Today a failing document can exit before arming it,
    stranding the instance, and the instance now stops itself on both arms.
  - **`bd-price-update` (allocation only).** The invoke runs only when the download and the merge both succeed, so
    it has been unreachable since 2026-06-22. With the strip it fires after a successful allocation merge.
    - Measured (row Z-S56): 2 invocations a day in the 22:00Z hour until 2026-06-21, and 1 a day since, from another
      caller.
    - The act restores the served pre-June cadence of 2 a day. The Lambda has been unmodified since 2026-04-06.
    - Its idempotence on a second same-day call was served behaviour, and is not re-measured here.
    - THIS HALF COVERS IT, or the allocation leg does not land (see section 5).

## 3. The expected outcome, both branches (read from the documents' own rule)

- **Merge succeeds:** the document exits 0, the log is uploaded, and the shutdown fires. Silver gains the new day's
  partition where bronze has a new file; the baseline is in section 4.
  - Allocation: `bd-price-update` is invoked asynchronously.
  - Transaction bronze for 2026-09-28 and 09-29 is empty, and allocation and unrealized had nothing new, so for those
    legs a Success may write 0 rows. That is the correct outcome for an empty bronze, not a failure.
- **Merge fails:** the document exits non-zero with the shutdown armed, and no `bd-price-update` call is made. The
  ledger leg stays open and rolls back (section 4) if the failure is caused by the edit. A failure the served document
  would also have hit (a merge error on the input) is recorded, not rolled back.

## 4. Baseline and rollback, per key

**Baseline:** the prior scheduled merge, 2026-09-28, and the PHASE A test runs (ANNOUNCE section 3).

| document | partitions or processed | latest rows |
| --- | --- | --- |
| transaction | 195 partitions | last non-empty 2026-09-27, 7,637 rows |
| realized | 144 partitions | 2026-09-29, 10,915 rows |
| allocation | 131 processed | -- |
| unrealized | 74 processed | -- |

**Rollback, per document:** the triggers run `$LATEST`, so moving DEFAULT alone reverts nothing. Re-publish the prior
`$LATEST` content as the next version and set DEFAULT to it:

| document | prior content to re-publish |
| --- | --- |
| transaction | v2 |
| allocation | v4 |
| realized | v2 |
| unrealized | v2 |

The content is read with `aws ssm get-document --name <doc> --document-version <v>`. Each rollback restores the
dead-download document with the same merge after it. The repo copy is reverted in the same window
(`git revert 4061557b4f c93e1c4fa4` for the leg concerned).

## 5. Guards the issuer will read at GO

- Both halves are SIGNED as files. A half may carve out the allocation leg over `bd-price-update`; the other 3 legs
  then land, and allocation waits.
- No other act is open on these 4 documents or their instances (`i-0800437d1dbb0b5cc`, `i-00c7568bc510f7423`).
  `.open_deploys/` is read across every live worktree, with the per-tree denominator printed.
- The publish lands outside the 21:30-22:15Z window, so no fire is mid-run on a document being replaced.

## 6. GO record (2.0.0_SA_COO~MI, 2026-09-29)

- **GO, 3 legs:** issued at d4a68b0b24 (MX-s-14 A3), under the CTO half @aac61a1046 and the CVO half @5b0a12277e. The
  guards were read at 08:12Z.
- **Published by 0.9.0_WK_NFRA_MCPINDEX~17, 08:25-08:27Z:** unrealized, realized and transaction, each at v3 with
  Default == Latest == 3. Every read-back hash equals the repo file. Drained 9feccbe36f.
- **Ledger:** `nfra-mcpindex-bd-playwright-strip` stays OPEN for the acceptance fires at 21:38, 21:45 and 21:53Z.
- **Allocation:** CARVED OUT and not published. Its re-cut, with the invoke unreachable (content 66431932a7ad0f55), is
  re-asked separately.
