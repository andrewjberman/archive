# pipeline-override: MDPF_CANON round 10 -- the round-10 issuance is closed to new order files (ONE ISSUER PER ROUND), so the CN-r-2 apply rides one ADHOC order in the CloudOps folder, the same shape as ADHOC.canon-r9-trend-publish-tonight. DRAFT: not committed, no GO issued.
<task_order id="ADHOC.canon-r10-publisher-latest-read-deploy">
<to_id>ADHOC.canon-r10-publisher-latest-read-deploy</to_id>
<issued_by>2.0.0_SA_COO~D1</issued_by>
<issued_to>0.7.0_AE_CloudOps~DELL1</issued_to>
<date>2026-10-15</date>
<status>staged</status>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<priority>P2 (CTO round-9 analysis item 2; STAGED until the CN-r-2 build is drained and the issuer's GO names the pin)</priority>

<title>MDPF_CANON CN-r-2: apply ONE added inline policy (s3:GetObject on opal-data-portal-v2/platinum/mdpf/*) to opal-assets-mdpf-egress-publisher-role by targeted safe-apply, run the publisher ONCE, and prove the unchanged branch fires (published=0 unchanged=18)</title>
<context>
THE CHANGE: `infra/aws/terraform/opal-assets/mdpf_egress_publisher.tf` gains `module.mdpf_publisher_live_serve_read_policy_name` and `aws_iam_role_policy.mdpf_egress_publisher_live_serve_read` (Allow, `s3:GetObject`, `arn:aws:s3:::opal-data-portal-v2/platinum/mdpf/*`, no Condition, not gated). The plan must read exactly 1 to add (the module is data only), 0 to change, 0 to destroy. The merged commit is named in the GO.

WHY: the role is denied GetObject on `platinum/mdpf/*`, so the publisher cannot read its pointer `platinum/mdpf/_manifests/latest.json` (the manifest records the denial as `prior_pointer_note`) nor re-hash the served object, and every run republishes all 18 pairs and the 4 history leaves. The grant is on the whole prefix, not on `latest.json` alone: a pointer-only grant leaves the Tax-extended pairs on the repair path. It is the prefix the role already writes.

NOT IN THIS ORDER: any gold write, any change of the schedule, the Tax switch, the lambda code or the lambda environment. The role's write, list, Gold and Tax-control policies stay byte-equal.

EXPECTED OUTCOME OF THE ONE RUN: `published=0 unchanged=18 failed=0` and no S3 write under `platinum/mdpf/`, PROVIDED no gold object or Tax control moved since the pointer was last written. If a pair published, read why from the manifest row before calling it a failure: a moved input publishes for a true reason (report which pair and which input).
</context>

<scope>
1. **PRECONDITIONS, read first; any false means do nothing and report which:**
   a. The issuer's GO citing this order and the pin (a commit hash) is in hand. Without it the order is `staged`; on the GO flip `<status>` to `pending`.
   b. The pin is an ancestor of your box branch, measured with a positive control (`git merge-base --is-ancestor <pin> HEAD` rc 0, and a known non-ancestor rc 1), and `git show <pin>:infra/aws/terraform/opal-assets/mdpf_egress_publisher.tf` carries the resource `mdpf_egress_publisher_live_serve_read`.
   c. The check passes on the pin's tree: `python <the checks dir named in the GO>/r10_cn_r_2.py statement|rest|eval` reads 5 of 5, 4 of 4, 5 of 5.
   d. A clean opal-assets pre-plan: `safe-apply` plan with NO other change pending in `infra/aws/terraform/opal-assets` (the only plan diff is this policy). Any other diff: STOP and report it.
   e. A NEVER-2 ledger entry in `org/critical_paths/change_management/` is OPENED before the apply, and no other deploy is in flight: read `org/critical_paths/.open_deploys/` in EVERY live worktree (`git worktree list --porcelain`, then `git -C <wt> ls-tree -r --name-only HEAD org/critical_paths/.open_deploys/`), union them, print the per-tree denominator.
   f. No other publisher or gold run is in flight or due inside the window: read the publisher's schedule and the last invocation time (a run between the apply and your proof run is acceptable but must be read, not assumed).
2. **ORDER OF ACTS:**
   a. **Before print (the positive and negative controls).** Print the role's inline policies (names and statements) and simulate with the context keys the simulator names (the bare call returns NOT-DECIDABLE without an `s3:prefix` context): GetObject on `latest.json` and on `platinum/mdpf/global/category-views.json` must be DENIED now; GetObject on the Gold read prefix and the Tax control key must be ALLOWED (controls). Read `latest.json`'s head: print its VersionId and LastModified, and the 18 served keys' current VersionIds (these are the baseline for 2.f).
   b. **Plan.** Targeted saved plan: `-target=module.mdpf_publisher_live_serve_read_policy_name -target=aws_iam_role_policy.mdpf_egress_publisher_live_serve_read` through `safe-apply`'s own limb. It must read `Plan: 1 to add, 0 to change, 0 to destroy`. Anything else: STOP.
   c. **Apply** the saved plan by `safe-apply` (never a bare `terraform apply`).
   d. **After print.** Re-print the role's policies; the new statement is present and the other three are byte-equal to the before print. Simulate again: GetObject on `latest.json` and the served keys ALLOWED; GetObject on `json/mdpf/x`, `platinum/etfs/x`, `platinum/_staging/mdpf/x` and the bucket `opal-data-mdpf` (outside the Gold/Tax keys) DENIED; PutObject on `platinum/mdpf/x` unchanged ALLOWED; DeleteObject DENIED. Print the number of probes.
   e. **ONE publisher hand-run**, with the schedule's own input (read the rule target's input, never typed from memory). Read the result line.
   f. **The proof read.** (i) the run's summary reads `published=0 unchanged=18 failed=0` (or each published pair is explained by a moved input, named); (ii) the manifest's `prior_pointer_note` is null; (iii) every pair row reads `unchanged`; (iv) the 18 served keys' VersionIds equal the 2.a baseline, 18 of 18 (a changed VersionId means a republish happened: report it); (v) `latest.json`'s VersionId equal or advanced, stated.
   g. Close the ledger entry.
3. **ROLLBACK (same session, loud):** remove the added resource by targeted `safe-apply` of the prior commit (the role returns to three policies), re-print the policies, close the ledger as ROLLED BACK. Rollback restores today's behaviour (the 18-of-18 republish), which is the current state and harms nothing. A partial apply is never left: finish or roll back.
4. Report to `2.0.0_SA_COO~D1`: the pin, the plan line, the apply result, the before and after policy prints, the run summary line, the five proof reads with denominators, and the ledger path. Message under 150 words; the detail in the ledger file.
</scope>

<paths>
org/critical_paths/change_management/
org/critical_paths/.open_deploys/
org/tier2_senior/0.7.0_AE_CloudOps~DELL1/
</paths>

<proof_of_spec>
<expected_criteria>C1,C2,C3</expected_criteria>
<criterion id="C1" judgment="false">
  <invocation>the targeted saved plan, then the apply by safe-apply, then the role's policy documents printed before and after, with the simulator run with its context keys</invocation>
  <expect>Plan: 1 to add, 0 to change, 0 to destroy; after the apply the role holds four inline policies, the new one is the single GetObject on arn:aws:s3:::opal-data-portal-v2/platinum/mdpf/*, the other three are byte-equal to the before print; GetObject on latest.json and on the served keys flips DENIED to ALLOWED; the negative controls (json/mdpf, platinum/etfs, platinum/_staging/mdpf, opal-data-mdpf, DeleteObject) stay DENIED; PutObject on platinum/mdpf stays ALLOWED; probe count printed</expect>
</criterion>
<criterion id="C2" judgment="false">
  <invocation>one publisher invoke with the schedule's input, then the result line, the manifest prior_pointer_note and the per-pair rows</invocation>
  <expect>published=0 unchanged=18 failed=0 (or each published pair explained by a named moved input); prior_pointer_note is null; every pair row reads unchanged</expect>
</criterion>
<criterion id="C3" judgment="false">
  <invocation>head-object on the 18 served keys before (2.a) and after (2.f), compared by VersionId</invocation>
  <expect>18 of 18 VersionIds equal (no served byte moved); denominator printed; a differing key reported with its reason</expect>
</criterion>
</proof_of_spec>
</task_order>
