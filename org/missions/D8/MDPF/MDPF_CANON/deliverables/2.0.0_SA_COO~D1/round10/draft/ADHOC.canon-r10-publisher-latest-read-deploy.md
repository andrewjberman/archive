# pipeline-override: MDPF_CANON round 10 -- the round-10 issuance is closed to new order files (ONE ISSUER PER ROUND), so the CN-r-2 apply rides one ADHOC order in the CloudOps folder, the same shape as ADHOC.canon-r9-trend-publish-tonight. STAGED: behind the never-widen pair (both halves) and the issuer's GO naming the pin.
<task_order id="ADHOC.canon-r10-publisher-latest-read-deploy">
<to_id>ADHOC.canon-r10-publisher-latest-read-deploy</to_id>
<issued_by>2.0.0_SA_COO~D1</issued_by>
<issued_to>0.7.0_AE_CloudOps~DELL1</issued_to>
<date>2026-10-15</date>
<status>staged</status>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<priority>P2 (CTO round-9 analysis item 2; STAGED until both halves of NEVER_WIDEN_PAIR_R10_CN_R_2.md are signed and the issuer's GO names the pin)</priority>

<title>MDPF_CANON CN-r-2: apply ONE added inline policy (s3:GetObject on opal-data-portal-v2/platinum/mdpf/*) to opal-assets-mdpf-egress-publisher-role by targeted safe-apply, run the publisher ONCE, and prove the unchanged branch fires (published=0 unchanged=18)</title>
<context>
THE CHANGE: `infra/aws/terraform/opal-assets/mdpf_egress_publisher.tf` gains `module.mdpf_publisher_live_serve_read_policy_name` and `aws_iam_role_policy.mdpf_egress_publisher_live_serve_read` (Allow, `s3:GetObject`, `arn:aws:s3:::opal-data-portal-v2/platinum/mdpf/*`, no Condition, not gated). The plan must read exactly 1 to add (the module is data only), 0 to change, 0 to destroy. Pin: `3df2f0851a1eda3eb1c2e0ed00e66281e7697c1e` or a descendant carrying that file byte-equal; the GO names the commit. The pair: `org/missions/D8/MDPF/MDPF_CANON/deliverables/2.0.0_SA_COO~D1/round10/NEVER_WIDEN_PAIR_R10_CN_R_2.md`.

WHY: the role is denied GetObject on `platinum/mdpf/*`, so the publisher cannot read its pointer `platinum/mdpf/_manifests/latest.json` (the manifest records the denial as `prior_pointer_note`) nor re-hash the served object, and every run republishes all 18 pairs and the 4 history leaves. The grant is on the whole prefix, not on `latest.json` alone: a pointer-only grant leaves the Tax-extended pairs on the repair path. It is the prefix the role already writes. Measured by the issuer on 2026-10-15: the prefix holds 566 objects (22 served keys, `_manifests/latest.json`, 99 dated manifests, 444 archive copies), 5,839,823 B; the 22 served keys are the 18 pairs plus the 4 `category-views-history.json` leaves.

NOT IN THIS ORDER: any gold write, any change of the schedule, the Tax switch, the lambda code or the lambda environment. The role's write, list, Gold and Tax-control policies stay byte-equal.

EXPECTED OUTCOME OF THE ONE RUN: `published=0 unchanged=18 failed=0` and no served-key write under `platinum/mdpf/`, PROVIDED no gold object or Tax control moved since the pointer was last written. If a pair published, read why from the manifest row before calling it a failure: a moved input publishes for a true reason (report which pair and which input).
</context>

<scope>
1. **PRECONDITIONS, read first; any false means do nothing and report which:**
   a. The issuer's GO citing this order and the pin (a commit hash) is in hand, and both halves of the pair are signed (the CTO half at `org/missions/D8/MDPF/MDPF_CANON/ledger/NEVER_WIDEN_R10_PUBLISHER_CN_R_2_CTO_HALF.md`). Without them the order is `staged`; on the GO flip `<status>` to `pending`.
   b. The pin is an ancestor of your box branch, measured with a positive control (`git merge-base --is-ancestor <pin> HEAD` rc 0, and a known non-ancestor rc 1), and `git show <pin>:infra/aws/terraform/opal-assets/mdpf_egress_publisher.tf` carries the resource `mdpf_egress_publisher_live_serve_read`.
   c. The check passes on the pin's tree: `python <the checks dir named in the GO>/r10_cn_r_2.py statement|rest|eval` reads 5 of 5, 4 of 4, 5 of 5.
   d. A clean opal-assets pre-plan: `safe-apply` plan with NO other change pending in `infra/aws/terraform/opal-assets` (the only plan diff is this policy). Any other diff: STOP and report it.
   e. A NEVER-2 ledger entry in `org/critical_paths/change_management/` is OPENED before the apply, and no other deploy is in flight: read `org/critical_paths/.open_deploys/` in EVERY live worktree (`git worktree list --porcelain`, then `git -C <wt> ls-tree -r --name-only HEAD org/critical_paths/.open_deploys/`), union them, print the per-tree denominator.
   f. **GAP RULE.** Read the gold rule `mdpf-scheduled-floor` (13:30Z daily, 2026-10-15) and the publisher rule's schedule (13:50Z; `latest.json` last written 2026-10-15T13:51:01Z) and each lambda's last invocation. The apply and the hand-run both start and finish outside 13:00Z-14:10Z, and no gold or publisher run is in flight. A run between the apply and your proof run must be read, not assumed.
2. **ORDER OF ACTS:**
   a. **Before print (the positive and negative controls).** Print the role's inline policies (names and statements) and simulate with `comp-iam simulate opal-assets-mdpf-egress-publisher-role s3:GetObject <arn> --context s3:prefix=string:platinum/mdpf/ --control-arn arn:aws:s3:::opal-data-assets/portal/gold/mdpf/global/aggregate-aua-timeseries/x.json` (without the context the simulator returns NOT-DECIDABLE, and without the control arn DENIED-UNPROVEN rc 2): GetObject on `latest.json`, on `platinum/mdpf/global/category-views.json`, on `json/mdpf/x`, on `platinum/etfs/x` and on `platinum/_staging/mdpf/x` must read DENIED, control-proven, now (the issuer read these on 2026-10-15); the control arn and PutObject on `platinum/mdpf/global/x.json` read allowed. Read `latest.json`'s head: print its VersionId and LastModified, and the 22 served keys' current VersionIds (these are the baseline for 2.f). The 22 are `platinum/mdpf/<scope>/<type>.json` for the keys the list under `platinum/mdpf/` returns outside `_manifests/` and `archive/`; print the count (expect 22) and stop if it differs.
   b. **Plan.** Targeted saved plan: `-target=module.mdpf_publisher_live_serve_read_policy_name -target=aws_iam_role_policy.mdpf_egress_publisher_live_serve_read` through `safe-apply`'s own limb. It must read `Plan: 1 to add, 0 to change, 0 to destroy`. Anything else: STOP.
   c. **Apply** the saved plan by `safe-apply` (never a bare `terraform apply`).
   d. **After print.** Re-print the role's policies; the new statement is present and the other three inline policies are byte-equal to the before print. Simulate again with the same context and control: GetObject on `latest.json` and the served keys ALLOWED; GetObject on `json/mdpf/x`, `platinum/etfs/x`, `platinum/_staging/mdpf/x` DENIED, control-proven; PutObject on `platinum/mdpf/x` unchanged ALLOWED. DeleteObject on `platinum/mdpf/x` is reported as read (the GetObject control does not prove a Delete deny: state it as implicitDeny, UNPROVEN by this instrument, never as a proven deny). Print the number of probes.
   e. **ONE publisher hand-run**, with the schedule's own input (read the rule target's input, never typed from memory). Read the result line.
   f. **The proof read.** (i) the run's summary reads `published=0 unchanged=18 failed=0` (or each published pair is explained by a moved input, named); (ii) the manifest's `prior_pointer_note` is null; (iii) every pair row reads `unchanged`; (iv) the 22 served keys' VersionIds equal the 2.a baseline, 22 of 22 (a changed VersionId means a republish happened: report it with its reason); (v) `latest.json`'s VersionId equal or advanced, stated.
   g. Close the ledger entry.
3. **ROLLBACK (same session, loud):** remove the added resource by targeted `safe-apply` of the prior commit for that file (the role returns to three inline policies), re-print the policies, close the ledger as ROLLED BACK. Rollback restores today's behaviour (the 18-of-18 republish), which is the current state and harms nothing. A partial apply is never left: finish or roll back. A served key the hand-run changed is restored only by copy-object of its recorded prior VersionId; nothing is deleted.
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
  <invocation>the targeted saved plan, then the apply by safe-apply, then the role's policy documents printed before and after, with comp-iam simulate run with its s3:prefix context and its --control-arn</invocation>
  <expect>Plan: 1 to add, 0 to change, 0 to destroy; after the apply the role holds four inline policies, the new one is the single GetObject on arn:aws:s3:::opal-data-portal-v2/platinum/mdpf/*, the other three are byte-equal to the before print; GetObject on latest.json and on the served keys flips DENIED to ALLOWED; GetObject on json/mdpf, platinum/etfs and platinum/_staging/mdpf stays DENIED (control-proven); PutObject on platinum/mdpf stays ALLOWED; DeleteObject stated as implicitDeny and unproven; probe count printed</expect>
</criterion>
<criterion id="C2" judgment="false">
  <invocation>one publisher invoke with the schedule's input, then the result line, the manifest prior_pointer_note and the per-pair rows</invocation>
  <expect>published=0 unchanged=18 failed=0 (or each published pair explained by a named moved input); prior_pointer_note is null; every pair row reads unchanged</expect>
</criterion>
<criterion id="C3" judgment="false">
  <invocation>head-object on the 22 served keys before (2.a) and after (2.f), compared by VersionId</invocation>
  <expect>22 of 22 VersionIds equal (no served byte moved); denominator printed; a differing key reported with its reason</expect>
</criterion>
</proof_of_spec>
</task_order>
