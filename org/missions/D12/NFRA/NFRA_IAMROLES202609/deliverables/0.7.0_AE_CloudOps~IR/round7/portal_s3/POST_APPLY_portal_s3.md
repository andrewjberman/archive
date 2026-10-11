# POST_APPLY -- NFRA_IAMROLES202609.TO-IAM-x-5 PHASE B: `opal-portal-s3-read` NARROWED

**Cell:** IAM-x-5 (round 7, E5, the round's MOST URGENT). **Executed by:** `0.7.0_AE_CloudOps~IR`.
**Authority:** GO `2.0.0_SA_COO~ZI` msg 33256. Halves: COO @`541e951458`, CTO @`55aca92d76`, both read as FILES
at HEAD before anything moved, beside a positive control proving an absent half reads absent.
**Measured:** 2026-10-11, apply at `11:14:40Z`, returned `11:15:57Z`.

> **THIS IS THE LARGEST PERMISSION NARROWING OF THE PROJECT.** Twelve ARNs left a statement granting
> `GetObject` + `PutObject` + **`DeleteObject`** + `ListBucket`, on a role **12 Lambda functions assume**, and
> every one of the twelve named a **GLOBAL S3 bucket name that does not exist** -- so until this apply, whoever
> created any of those six names in any AWS account would have received READ, WRITE and DELETE through a
> production role. Nothing was added; no trust, tag, attachment or other policy moved.

---

## 1. THE REQUIRED LINE

```
POST-APPLY-PLAN: shared-infra: 0 to add, 0 to change, 0 to destroy
```

Terraform renders a clean plan as a sentence, so its verbatim output is quoted beside the canonical line rather
than silently reshaped:

```
$ terraform -chdir=infra/aws/terraform/shared-infra plan ... -target=aws_iam_role_policy.opal_portal_s3_read
No changes. Your infrastructure matches the configuration.
```

Apply verbatim: `Apply complete! Resources: 0 added, 1 changed, 0 destroyed.`

## 2. THE PLAN THAT WAS APPLIED, GRADED BEFORE THE APPLY

Saved with `-out`; the apply ran that file. Graded from `terraform show -json` per `resource_change` **and per
ARN**, because a policy is ONE opaque string attribute and `1 to change` would read identically if an action had
been dropped or a LIVE ARN removed.

| graded property | measured |
|---|---|
| `resource_changes` / non-no-op | 2 / **1** |
| non-no-op addresses that are NOT the target | **`[]`** |
| adds / destroys | **0 / 0** |
| attributes that differ | **1** (`policy`) |
| `name` / `role` / `id` | all **byte-identical** |
| statements / `Sid` | 1 -> 1 / `S3ReadWrite` -> `S3ReadWrite` |
| **actions** | **identical, all four** |
| ARNs | **16 -> 4** |
| **ARNs ADDED** | **0** |
| ARNs REMOVED | **exactly the 12** |

### 2a. THE EDIT'S OWN BLAST RADIUS WAS MEASURED, NOT ASSERTED

```
diff hunks: 1          lines: 13 removed, 1 added          terraform fmt -check: rc=0
```

**The hunk count is load-bearing.** The trailing-comma fix on the last kept ARN was applied with a **global**
regex, in a file that declares many policies, so "it only touched my block" is a claim that needs measuring. One
hunk is that measurement. The 13th removal plus the 1 addition are `opal-data-news-v2/*` rewritten without its
comma; the net is exactly 12 ARNs gone. The heredoc still parses as JSON.

Committed BEFORE the import/apply at `0daa084a68`, per A4-r6 and row `Z-S27`.

## 3. LIVE, AGAINST THE COMMITTED ROLLBACK

The rollback was saved in PHASE A and **proven equal to a FRESH live re-fetch**, not to the file being written --
canonical `sort_keys` compare **True**. Comparing a saved file to itself would prove nothing, and that ordering
is the whole value of the check.

| | before (the rollback) | after (live) |
|---|---|---|
| ARNs | **16** | **4** |
| removed | -- | **exactly the 12**, enumerated in the ledger |
| **added** | -- | **0** |
| kept | -- | `opal-data-portal-v2` + `/*`, `opal-data-news-v2` + `/*` |
| statements / `Sid` | 1 / `S3ReadWrite` | 1 / `S3ReadWrite` |
| actions | 4 | **the same 4** |

### 3a. "EVERY OTHER POLICY BYTE-IDENTICAL" -- measured across all 18, not assumed

The COO half permits only this one document to move. All **18** of the role's inline policy documents were
hashed BEFORE the apply (`sha256` of `sort_keys` JSON) and re-hashed after:

```
18 compared -> 17 BYTE-IDENTICAL, 1 changed
CHANGED: opal-portal-s3-read   aa0fa4e08bdf82dd -> 87ca089e25ba4213      <- the signed one, and only it
policy COUNT: 18 before, 18 after                                        <- nothing added or dropped
```

The role itself is untouched: trust still `lambda.amazonaws.com`, **0 tags** before and after, **0 attached
managed policies** before and after.

`AC2`'s own invocation reads **`dead=0 live=4`**.

## 4. THE LAST GUARD -- a KEPT grant exercised with a WRITE, after the change

The CTO half keeps one condition: *"ONE real invocation of a portal function on this role, read AFTER the change
(the log plane, since `RoleLastUsed` lags), succeeded."*

**Met on the strongest available oracle -- not merely that the role is assumable, but that the SURVIVING grant
still works:**

```
/aws/lambda/opal-trending-topics-portal-publisher
START RequestId: 37131e0c-f0ea-4c7d-9289-0c5e570236bf   epoch 1791717640947 = 2026-10-11T11:20:40Z
  Dest:  s3://opal-data-portal-v2/json/trending/latest.json        <- one of the four KEPT ARNs
  Retrieved 19 trending topics from DynamoDB
  Publishing to portal bucket...
  OK: Published successfully!
  File size: 87.6 KB
```

against an apply that **returned at 11:15:57Z**. That is a real `s3:PutObject` to a kept bucket completing after
the twelve ARNs were removed. **Errors in the window: 0**, over
`?AccessDenied ?NoSuchBucket ?Traceback ?Forbidden ?"An error occurred"` -- and an `AccessDenied` is precisely
what a damaged grant would have printed, so the zero carries its cause.

**Corroborated on a second function, deliberately cited second:** `opal-portal-authorizer` shows **239** START
events after the apply with **0** error-pattern matches, which proves the role remains assumable at production
volume. It is the weaker oracle because an authorizer need not touch S3 at all.

> **`RoleLastUsed` WAS DELIBERATELY NOT USED.** IAM last-used data lags up to four hours -- measured on x-1 row 6
> earlier in this same session, where it still read pre-apply while the consumer had demonstrably run. The log
> plane is the only near-real-time read, and the half says so itself.

**Branch B did not fire. The rollback was available throughout and was not run.**

## 5. THE POST-DRAIN SHARED-TREE PLAN

```
UNTARGETED-MODULE-PLAN: infra/aws/terraform/shared-infra: No changes. Your infrastructure matches the configuration.
```

rc=0, 0 planned-action addresses, 0 destroys, 0 replaces -- **fully absorbed with no residue**, which is stronger
than the leg required (it required only `0 to destroy`). Run in the **SHARED tree** after the drain at
`bfc71ac6a1`, not in the worktree that made the change, because the claim is about the repository every other
seat reads.

**The half bound the PLAN SHAPE directly rather than "breakglass adds unchanged", and that was the right call:**
`restricted_breakglass` appears here only as two `Refreshing state...` lines with **0 planned actions**, because
its owner applied the pair at 09:05:05Z (row `Z-S40`). Row 6's pair *had* bound the stale "2 to add UNCHANGED"
clause and it was unsatisfiable before that act began; the x-5 half avoided inheriting it because PHASE A's
survey flagged the staleness.

## 6. THE COVERAGE GAP I REPORTED, CLOSED BY THE CTO

PHASE A reported **1 of 12** functions' deployed code uncensused: `opal-session-analytics`, whose source-map
entry names `dist/index.mjs` with no `dist/` in the repo (a bun artifact built at deploy). I checked that with a
forward-slash path specifically because a mixed separator on this device can make a present file read absent --
it was genuinely not there, and I reported the gap rather than letting the function's zero stand unqualified.

`1.0.0_SA_CTO~Z` closed it the right way: downloaded the bundle via `get-function` `Code.Location` into a scratch
directory, **never executed it**, searched its 70,108 bytes and found **all six dead names at 0**, with a
positive control (`opal-sessions`, `opal-portal-api`, `opal-portal-auth` all found) proving the search reads the
bundle. **The census is 12 of 12, env and deployed code, every dead name 0.**

## 7. THE LEDGER, AND THE CLOSE THE TOOL WILL NOT COMMIT

`iamroles-r7-narrow-portal-s3`, opened at `11:02:33Z` BEFORE the first act with **4** legs -- TF, LIVEDIFF,
REPLAN, INVOCATION -- each `proof_required` written at open time as a falsifiable condition. All four closed on
live reads.

**The close was checked rather than trusted, and it needed committing by hand again:** immediately after
`deploy_ledger.py close`, the entry read `CLOSED -- nothing stranded` on disk and **`**Status:** OPEN` at HEAD**.
The tool auto-commits `open` and says so in its own output, but it does not commit `close-leg` or `close`. This
is the second time today (x-1 row 6 was `c0b5dc0c63`), and the COO half for this cell cites that fix by name,
which is why the check ran at all.

## 8. WHAT THIS CELL DID NOT SETTLE

- **Whether `DeleteObject` belongs in a policy named `opal-portal-s3-read` at all.** The module's own comment at
  `opal-portal-lambda-role.tf:382` already flags the name-vs-grant drift and records why it was left (renaming an
  inline policy is a destroy-plus-create on a live authorizer role). Out of BOUNDS here.
- **Whether any of the six buckets is meant to exist.** `opal-market-data-v2` is DECLARED in
  `market-overview/s3.tf:6`, so Terraform's own intent is that it exist -- which makes "recreate the bucket" and
  "remove the grant" opposite answers for that one name, and `RULINGS_LEDGER.jsonl:44` carries a prior
  `DELETE-GATED` ruling on it. Removing the grant is correct for closing the squatting hazard and does not
  settle the product question. Six buckets may not share one answer.
- **`opal-data-smartx`'s DynamoDB table**, which is live and referenced by `opal-portal-data-proxy`. This S3
  grant never reached it; the name collision is recorded because it is what made PHASE A's substring census lie.

**PHASE B ENDS HERE.**
