# ETFS_RIVALS.TO-APPLY-R28-aw1 -- STOP 3 record: the plan as read

**Executor:** `0.7.0_AE_CloudOps~Z` (site Z's applier, Andrew-direct ~22:0xZ 2026-10-08, MSTR msg 32053).
**Issuer:** `2.0.0_SA_COO~RV`. **GO for steps 1-3 only:** msg 32082 (acked). **Apply:** HELD for a second GO
inside 2026-10-09 11:15Z-12:55Z.
**Halves read in full at their cited pins:** COO @d3d6c3e73f, CTO @a0ee589cc2 (`git show <pin>:<path>`).

All values below are MEASURED in `C:/tmp/rv-r8` at 2026-10-08 ~22:45-22:53Z unless the row says otherwise.

## STOP 1 -- the pin

| read | result | expected by the halves |
|---|---|---|
| tree HEAD before | `325bd4e0f8` detached, clean | the live/deployed pin |
| `git checkout --detach 39889dd4d7` | HEAD `39889dd4d71a67bc108fe15ae746ed7ab6cbe6f6`, tree clean | the exact pin, so no later-commit clause applies |
| `git cat-file -t 39889dd4d7` | `commit` | commit |
| aw-1 tip `a2283fc349` ancestor of pin | rc 0 | rc 0 |
| RIV-tc-1 `b0b65368fb` ancestor of pin | rc 1 (NOT in the pin) | rc 1 -- tc-1 must NOT be in the pin |
| deployed `325bd4e0f8` ancestor of pin | rc 0 | rc 0 |

CONTENT oracle (the authoritative read; `merge-base --is-ancestor` alone is not one per CLAUDE.md 22a).
`git diff --stat 325bd4e0f8 39889dd4d7` over the seven `STAGED` paths, `':!**/tests/**'`:

```
 data/etfs/scripts/rivalfunds/ai_accounts.py  | 200 ++++-
 infra/logic/registry/event_rules.json        |  18 +
 infra/logic/registry/exemptions.json         |  30 +-
 infra/logic/registry/key_rulings.json        | 236 ++++-
 infra/logic/registry/mail_parties.json       |  33 +
 infra/logic/registry/name_rulings.json       |  38 +
 infra/logic/registry/reporting_policies.json |  18 +
 infra/logic/registry/root_map.json           |   2 +-
 lib/opal_naming.py                           |  12 +
 9 files changed, 532 insertions(+), 55 deletions(-)
```

OK: 9 files, +532 -55 -- the same nine files both halves name, line for line.
OK: `infra/aws/lambda/etfs-pipeline/` between the pins, tests out: 0 files (no Terraform input moves beyond the package).
OK: `infra/aws/terraform/etfs-rivalfunds/` between the pins: 0 files (matches the order's comp-iam DECLARED-NOT-APPLICABLE denominator).

## AC1 at the pin

`python org/missions/D5/ETFS/ETFS_RIVALS/deliverables/2.0.0_SA_COO~RV/round15/checks/aw-1.AC1.py`
-> **`AC1 RESULT: PASS 0 failures`**, rc 0. Sub-checks (a) through (j) all OK, including (j), the CONTROL
(the chain on clean replies returns its 2 rows with the 17 stored columns, both PASS). `PROMPT_VERSION` reads
`a1-chain/7` at the pin.

AC2 is `judgment="true"` and is the issuer's and the CVO's to grade. NOT marked here.

## Step 2 -- package, then plan in the same tree

`python infra/aws/lambda/etfs-pipeline/rivalfunds_package.py` -> rc 0, five trees staged under
`.runtime/rivalfunds-build/`: daily, fetch-holdings, build-canonical-shape, build-silver, publish-page.
Terraform resolved on PATH (`terraform v1.15.8`); `.tools/terraform.exe` does NOT exist on site Z, as
`/cloud-ops` warns -- the binary was resolved, not assumed.

`terraform plan -out C:/tmp/rv_apply28.tfplan` -> rc 0. Log `/c/tmp/rv_plan28.out`, JSON `/c/tmp/rv_plan28.json`.

## STOP 3 -- the plan as read: BRANCH A

Headline: **`Plan: 0 to add, 5 to change, 0 to destroy.`**

Condition 2 of both halves ("the only attribute that changes is the code package") was verified against the
machine read, not the rendered text: `terraform show -json` + `STOP3_plan_audit.py` (beside this file).

```
DENOMINATOR: 45 resource_changes in the plan
  actions: {('no-op',): 40, ('update',): 5}
NON-NO-OP: 5
```

Per changed resource -- all five `aws_lambda_function.stage`, each changing exactly two attributes
(`source_code_hash`, and `last_modified` -> known after apply), with `memory_size` 3008, `timeout`,
`environment` and `role` all SAME:

| function | source_code_hash BEFORE (deployed) | -> AFTER (the new package) | memory | timeout |
|---|---|---|---|---|
| etfs-rivalfunds-daily-lambda | `50EIl4XbzfqZCBrCes1NVOXABsnyXqKH1VQrwoq1oRE=` | `6Z77vxU0kHTyYlEwWrVJNj80rNKWfK5bBBrKZuDX8JA=` | 3008 | 900 |
| etfs-rivalfunds-fetch-holdings-lambda | `8sq83jGSW/00UIn5rIhUeIEECG9gHzuSrhtEFPPAvXg=` | `cXi5kINKTlBzvjV/uYXAYB1jXlo7PA3YxRTjqXtHyjg=` | 3008 | 300 |
| rivalfunds-build-canonical-shape-lambda | `PTcMhs7WuhmroW8bxl/FC/Z+50o5AR9D2GQVrTJKrZE=` | `5ZTAg5KmLs0sQtC2uMpck2hhFELajS13Yka8VJGktkU=` | 3008 | 900 |
| rivalfunds-build-silver-lambda | `XcZnD/CPv37gdrkNEb3RwqrWSSWZU2GugZ27avsZq7U=` | `DLqulrgw7LKUPtVXEyXy/0lagb5PGa+a0xnywqcdEh0=` | 3008 | 900 |
| rivalfunds-publish-page-lambda | `/JVm0SXwsKv5pEWsJ3paeR1RHH4smvmGtXmWOCXDtN8=` | `/ZD6nH7grFuRYJlaMWbe+4HYZIFZzHD6ZLvOhcYE0Aw=` | 3008 | 900 |

CLAIM on the BEFORE column: `measured`, but read from the PLAN's `before` state, NOT from a live
`get-function-configuration`. The live BEFORE read of `CodeSha256` and `LastModified` is step 4's and is owed
at the apply, inside the window.

Verdict: `types changing: ['aws_lambda_function']` | all five are `aws_lambda_function.stage` | every action is
`update` | only package attributes change -> **BRANCH A**. No IAM, schedule, memory, timeout or environment
change appears in the plan.

## State at the end of steps 1-3

- APPLIED NOTHING. No function invoked, no test event, no S3 object written, no environment variable set.
- `C:/tmp/rv-r8` is detached at `39889dd4d7` with the five staged trees present; the saved plan is
  `C:/tmp/rv_apply28.tfplan`. Both are needed as-is for step 5, so the tree is left alone.
- ROLLBACK NOTE for the issuer: the COO half's rollback says the deploy tree "is detached there now" at
  `325bd4e0f8`. It is NOT any more -- step 1 moved it to the pin on your GO. A rollback therefore needs a
  re-checkout of `325bd4e0f8` in that tree first, then a plan. Nothing about the rollback is lost; the one
  extra act is named here so it is not discovered mid-rollback.
- The NEVER-2 ledger entry is NOT opened: step 4 opens it on GO, inside the window.
- STOP 3 reported to `2.0.0_SA_COO~RV` at 20261008T225339Z, 1061 bytes delivered (measured with `wc -c` on the
  delivered file, which the recipient's live watcher had already moved to its `read/`).
