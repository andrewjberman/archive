# MDPF_CANON round 10 -- never-widen pair for CN-r-2: ONE added inline policy on `opal-assets-mdpf-egress-publisher-role` (`s3:GetObject` on `opal-data-portal-v2/platinum/mdpf/*`), so the publisher can read its pointer and the served keys and the unchanged branch fires

**COO half DRAFT, UNSIGNED; CTO half OWED.** Drafted by a fork of `2.0.0_SA_COO~D1` on 2026-10-15 and to be read and signed by the issuer. Every claim is labelled MEASURED (read or run in this session), INFERRED (read from code or a record, not run) or UNVERIFIED. Nothing here is deployed.
**Deployer:** `0.7.0_AE_CloudOps~DELL1`, on `ADHOC.canon-r10-publisher-latest-read-deploy` (beside this file, STAGED).
**Halves:** CTO half = `1.0.0_SA_CTO~DELL1`, to be recorded at `ledger/NEVER_WIDEN_R10_PUBLISHER_CN_R_2_CTO_HALF.md`; COO half = this lane.
**Rulings this pair carries:** the CTO round-9 analysis item 2 (`ledger/ROUND_ANALYSIS.round9.md` section 4): "one read-only IAM element is added, so the unchanged branch fires"; decomposition v10 (the grant covers the served prefix and not `latest.json` alone, because the publisher also re-hashes the served keys).
**Pin:** `3df2f0851a1eda3eb1c2e0ed00e66281e7697c1e` (the CN-r-2 drain merge), or a descendant carrying `infra/aws/terraform/opal-assets/mdpf_egress_publisher.tf` byte-equal to it (read by content: `git show <pin>:<path>`). MEASURED: `3df2f0851a` is an ancestor of origin's `box/dell1` head `5ed48abca1c0cb41291fade6917f4f83e253def5` (`git ls-remote` read, `git merge-base --is-ancestor` rc 0; negative control `786f33b5a8` into `3df2f0851a` rc 1). The status flip `786f33b5a8` is also an ancestor.

## 1. The change (MEASURED: `git diff 3df2f0851a^1 3df2f0851a`, one Terraform file, +24 lines, no deletion)

```
module "mdpf_publisher_live_serve_read_policy_name" { source = "../modules/opal_name"; system = "mdpf"; function = "publisher-live-serve-read"; kind = "policy" }
resource "aws_iam_role_policy" "mdpf_egress_publisher_live_serve_read" {
  name = module.mdpf_publisher_live_serve_read_policy_name.name
  role = aws_iam_role.mdpf_egress_publisher.id
  policy = { Sid "ReadLiveServedMdpf", Effect Allow, Action ["s3:GetObject"],
             Resource "arn:aws:s3:::opal-data-portal-v2/platinum/mdpf/*" }   # no Condition
}
```

- Not gated by `count` or `for_each`; the existing write policy `mdpf_egress_publisher_live_serve` (Put on the same prefix, List with `s3:prefix` condition) is untouched. Expected plan: **1 to add, 0 to change, 0 to destroy** (the module is data only). The role is `opal-assets-mdpf-egress-publisher-role`.
- Criteria on the merged tree: `r10_cn_r_2.py` statement 5/5, rest 4/4, eval 5/5 (re-run by the issuer, `786f33b5a8`).
- Role policies BEFORE (INFERRED from the `.tf`, the order's step 2.a prints the live ones): managed `AWSLambdaBasicExecutionRole` attachment; inline `..._scoped` (Get on `opal-data-assets/portal/gold/mdpf/*`, Put on `platinum/_staging/mdpf/*`, two List); `..._live_serve` (Put and conditioned List on `platinum/mdpf/*`); `..._taxsma_control` (Get on the one control key). After: those plus the new inline policy (four inline).

## 2. Blast radius: what the grant can reach (MEASURED, read-only, 2026-10-15 ~15:5xZ)

`aws s3api list-objects-v2 --bucket opal-data-portal-v2 --prefix platinum/mdpf/` (auto-paginated, counted client-side): **566 objects, 5,839,823 B**. Versioning on the bucket: Enabled. By class (denominator 566):

| class | objects | bytes | what it is |
|---|---|---|---|
| served keys, `<scope>/<type>.json` | 22 | 1,983,911 | 18 (scope,type) pairs + 4 `category-views-history.json` leaves: 49financial 5, cottonwood 6, global 6, inflection 5 |
| `_manifests/latest.json` | 1 | 6,936 | the pointer; VersionId `2PNZ5kd6oNj4nnkoquO0dW4sCn.3BUbj`, written 2026-10-15T13:51:01Z (the 13:50Z publisher fire) |
| `_manifests/<date>/<ts>.json` | 99 | 960,262 | dated run manifests |
| `archive/...` | 444 | 2,888,714 | dated copies of earlier served bodies |

(Sum check: 22 + 1 + 99 + 444 = 566; 49financial 5 + cottonwood 6 + global 6 + inflection 5 = 22.) **Every one of the 566 objects is one the role can already WRITE (Put on `platinum/mdpf/*`) and the data class is the served, client-facing MDPF aggregate plane that the portal already reads; no PII, no raw source data, no other tenant's bucket.** INFERRED from the key names and the write policy; the content class of `archive/` was not opened.

What the grant does NOT reach (the order's step 2.d simulates each with a passing positive control): `opal-data-portal-v2/json/mdpf/*`, `platinum/etfs/*`, `platinum/_staging/mdpf/*` (the role writes staging but still cannot read it back), the bucket `opal-data-mdpf`, any Delete, any List beyond the existing statement. The ARN is a literal prefix, so `platinum/mdpfX` does not match (`platinum/mdpf/*` needs the slash).

**Writers of the property "this role can read `platinum/mdpf/*`". N = 1.** The new `aws_iam_role_policy.mdpf_egress_publisher_live_serve_read`. MEASURED by reading the policy statements in the `.tf` (above): the other three inline policies grant Get on `portal/gold/mdpf/*` (a different bucket) and on the one Tax control key only. No managed policy on the role grants S3 (INFERRED: the one attachment is the Lambda basic-execution policy). The order's before-print confirms the live set.
**Readers of that capability:** the publisher lambda only (the role's single trust). INFERRED from `assume_role_policy` in the `.tf` (`lambda.amazonaws.com`).

## 3. Expected behaviour, both branches (read from the publisher's rule)

- **Branch A (a grant makes the reads succeed; the designed path).** The publisher reads `latest.json` as `prior_pointer`, then for each pair compares the gold body hash with the served body: a pair whose hash is unchanged is `unchanged` and NOT written. If no gold input moved since the pointer was written, the run reads `published=0 unchanged=18 failed=0`, no S3 write under `platinum/mdpf/` except possibly the manifest and `latest.json` per the publisher's own rule (the order's proof reads whether `latest.json`'s VersionId advanced and states it either way), `prior_pointer_note` is null. If a gold input moved, that pair publishes for a true reason (the order requires naming it). This branch is a function of data, not of the grant.
- **Branch B (the grant does not take effect or is too narrow).** IAM changes propagate in seconds; if the first run still reads `prior_pointer_note` set, every pair republishes (today's behaviour: 18 of 18, with the same bytes). That is the CURRENT state and harms nothing: a republish of a data-identical body writes a new VersionId of equal bytes. The failure of the proof is stated, the policy is left (it is harmless) or rolled back at the CTO's word; a partial state is not possible, because the apply is one resource.
- **The publisher on a read error that is NOT AccessDenied.** The publisher's existing fall-back (the repair path) republishes; the proof then reads published>0. No behaviour is added by this change.

## 4. Rollback, per key

1. Remove the one added resource: targeted `safe-apply` of the commit BEFORE `3df2f0851a` for that file (the role returns to three inline policies); re-print policies; ledger CLOSED as ROLLED BACK. Recorded before the apply: the role's three prior policy documents (byte-equal check in the order).
2. There is no data to roll back: the apply writes no S3 object and changes no object. The ONE publisher hand-run of the order may write: if a pair publishes (Branch A with a moved input, or Branch B), its prior VersionId is recorded by the order's step 2.a baseline (the 22 served keys + `latest.json`) and the served key's prior version can be restored by copy-object by VersionId. A delete needs a human's word.
3. The gap rule keeps the rollback unambiguous: no scheduled gold or publisher fire is inside the window, so any VersionId change in the window is the hand-run's, nothing else.

## 5. Sequencing and the gap rule

- Schedule (MEASURED from the records of this session; the order re-reads the rule targets): gold lambda `mdpf-scheduled-floor` `cron(30 13 * * ? *)`; the publisher fires at 13:50Z (the manifest `latest.json` was written 2026-10-15T13:51:01Z). **The order starts and finishes outside 13:00Z-14:10Z.** Today's 13:30Z and 13:50Z fires are done (MEASURED: `latest.json` written 13:51:01Z); the order may start any time after the CTO and COO halves and the GO, and must finish before 13:00Z on the following day or wait until after 14:10Z.
- Starts only on (i) the CTO half signed, (ii) the COO half signed, (iii) the issuer's written GO naming the pin; the deploy order is `staged` until then.
- No open deploy sentinel names the role, `mdpf_egress_publisher.tf` or the publisher lambda (the order re-reads `org/critical_paths/.open_deploys/` in every live worktree). The CN-r-1 gold deploy is a different order and function; it must not overlap the 13:30Z fire; the two orders do not share a resource, and the CTO may sequence them either way (they do not touch the same object).

## 6. Pre-change decision on `latest.json` (MEASURED: `comp-iam simulate`, APPLIED plane, 2026-10-15)

Role `opal-assets-mdpf-egress-publisher-role`, `--context s3:prefix=string:platinum/mdpf/`, positive control `--control-arn arn:aws:s3:::opal-data-assets/portal/gold/mdpf/global/aggregate-aua-timeseries/x.json` (the control returned `allowed`, so the instrument can say yes):

| action / resource | decision |
|---|---|
| GetObject `opal-data-portal-v2/platinum/mdpf/_manifests/latest.json` | **DENIED (implicitDeny), control-proven** |
| GetObject `.../platinum/mdpf/global/category-views.json` | DENIED, control-proven |
| GetObject `.../json/mdpf/x` | DENIED, control-proven |
| GetObject `.../platinum/etfs/x` | DENIED, control-proven |
| GetObject `.../platinum/_staging/mdpf/x` | DENIED, control-proven |
| GetObject `opal-data-assets/portal/gold/mdpf/global/aggregate-aua-timeseries/x.json` (control) | allowed |
| PutObject `.../platinum/mdpf/global/x.json` (control) | allowed |
| DeleteObject `.../platinum/mdpf/global/x.json` | NOT-DECIDABLE (the GetObject control does not prove a Delete deny; implicitDeny read) |

**Without the `s3:prefix` context the simulator returns NOT-DECIDABLE for every row (a conditioned List statement is unevaluated), and without `--control-arn` it returns DENIED-UNPROVEN (rc 2): the order must pass both. The DeleteObject row stays UNPROVEN by this instrument; the order's after-print states it as such and does not claim a proven deny.** A simulation is not an exercised read; the one publisher run is the runtime proof.

## 7. Acceptance after the act (the issuer reads; never a leg of the CloudOps order)

1. The ledger and the before/after policy prints: four inline policies after, three byte-equal to before, plan line `1 to add, 0 to change, 0 to destroy`.
2. The after-print simulation: GetObject on `latest.json` and the served keys ALLOWED; the negative controls of section 6 DENIED; Put ALLOWED.
3. The publisher run: `published=0 unchanged=18 failed=0` or each published pair explained; `prior_pointer_note` null; the 22 served keys' VersionIds equal the baseline (22 of 22, or each differing key reported with its reason).
4. At the NEXT scheduled gold + publisher fire (2026-10-16 13:30Z / 13:50Z) the same read: unchanged branch fires for pairs whose gold body is data-identical (not "18 of 18" unless nothing moved).

## 8. What the COO half asks the CTO half to read

1. **Section 2:** the grant is the whole served prefix (566 objects), the same prefix the role already writes. Accept the whole-prefix grant (decomposition v10) or narrow to `_manifests/latest.json` plus the 22 served keys by exact ARN?
2. **Section 6:** the DeleteObject deny is NOT proven by the simulator; accept as stated.
3. **Section 3, Branch B:** accept that a non-taking grant leaves today's harmless republish and the policy in place.
4. **Section 5:** the gap rule (no start inside 13:00Z-14:10Z) and the independence from the CN-r-1 gold deploy.

## COO half -- SIGNED by 2.0.0_SA_COO~D1, 2026-10-15 ~16:0xZ

Read in full. Re-measured by the issuer at signing: `3df2f0851a` is an ancestor of origin `box/dell1` `4339774d12` (rc 0); the 566-object count and the DENIED decision on `latest.json` are the drafter's reads, re-run by CloudOps in the order's before-print (leg L1) before any act. Signature is this line in the commit by `2.0.0_SA_COO~D1`.

## CTO half -- OWED (`1.0.0_SA_CTO~DELL1`)

Sign, or refuse naming what is missing; a signature is a line in a commit by that seat, and no message carries it.
