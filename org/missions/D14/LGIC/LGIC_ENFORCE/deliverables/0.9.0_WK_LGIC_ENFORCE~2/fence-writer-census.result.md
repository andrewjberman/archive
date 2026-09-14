# RESULT -- LGIC_ENFORCE.TO-EN-c-2, the fence-writer census

**Worker:** `0.9.0_WK_LGIC_ENFORCE~2`. **Worktree:** `wk-lgic-enforce-1-2`, branch `wk-lgic-enforce-1-2`, cut from CLOUD
@fd9c9ca174. **Deliverable:** `org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/FENCE_WRITER_CENSUS.md`. **Proof:**
`LGIC_ENFORCE.TO-EN-c-2.fence-writer-census.proof_of_spec.json`, beside this file. This file is the session log.

## 0. Verdict

**5 of 5 mechanical criteria PASS by output.** The order has no judgment criterion.

| Criterion | Verdict line | rc |
|---|---|---|
| C2-AC1 | `VERDICT: PASS-FOUR-BUCKETS` | 0 |
| C2-AC2 | `VERDICT: PASS-TOKENS` (203 principal rows, none without a token) | 0 |
| C2-AC3 | `VERDICT: PASS-WINDOW` (2026-09-14T02:33:09Z to 2026-09-14T20:00:52Z) | 0 |
| C2-AC4 | `VERDICT: PASS-STATED` | 0 |
| C2-AC5 | `VERDICT: PASS-DENOMINATORS` (`MISMATCHED: []`) | 0 |

## 1. The bar

- **Branch and tree.** `git rev-parse --abbrev-ref HEAD` printed `wk-lgic-enforce-1-2`, HEAD `fd9c9ca174`, then `TREE-OK`.
  Every path the order names exists in the worktree.

## 2. The order's premises, re-grounded against live state

| Premise | Read | Holds? |
|---|---|---|
| Read logging on the four buckets was validated @231cd62ec5 at 02:33:09Z | `git show --stat 231cd62ec5`: `2026-09-13T22:33:09-04:00` = 2026-09-14T02:33:09Z | yes |
| The org trail logs these buckets `ReadOnly` at `cloudtrail-organization-trail.tf:73` | line 73 is `read_write_type = "ReadOnly"`; live `get-event-selectors` shows a ReadOnly selector on exactly the four buckets | yes |
| `item2e`'s WriteOnly events show `platinum/firm/` writers | the trail is live (`IsLogging` true) and WriteOnly, but on `opal-data-bd`, `-inf` and `-cot` only; its header still says "NOT YET APPLIED" | partly: row `LGIC_ENFORCE-W2-S3` |
| `comp-iam role <name>` gives the grant half per principal | 0 of 94 roles resolved | no: row `LGIC_ENFORCE-W2-S1` |
| "role-side belts" | the term is used, not defined, in the PRD (`:203`). The Terraform uses it for a role-side explicit Deny (92 hits over `infra/aws/terraform`) | read that way; placement is row `LGIC_ENFORCE-W2-S4` |
| PRD `:206`: `bd-gold-layer-runner` is a legacy principal | it is an EC2 host; its role is `bd-exporter-ec2-role` | no: row `LGIC_ENFORCE-W2-S2` |

## 3. What was run

All AWS reads were read-only, through the `aws` shim.

1. **Authorization dump.** `aws iam get-account-authorization-details` returned 250 roles, 7 users, 1 group and 56
   managed policies. A different instrument agrees: `list-roles` 250 and `list-users` 7, and 48 of 48 attached
   managed-policy ARNs resolve in the dump.
2. **Bucket policies.** `aws s3api get-bucket-policy` on 4 of 4 buckets. Bucket regions: all `us-east-1`.
3. **Trail state.** `aws cloudtrail describe-trails` (2 trails), plus `get-trail-status` and `get-event-selectors` on
   both.
4. **Log download.** `aws s3 cp --recursive` of both trails' `us-east-1/2026/09/14/` prefixes, from 20:00:52Z to
   20:01:32Z: 2169 org-trail files and 112 served-trail files.
5. **Grant census.** `.scratch/c2/grants.py` (scratch, not committed). For each bucket it keeps every role or user
   whose policies carry an Allow covering any `s3:` action on the bucket or its objects, and records each
   identity-policy Deny that names the bucket.
6. **Seen census.** `.scratch/c2/trail.py` (scratch). It reads the S3 data events on the four buckets from 02:33:09Z
   on:
   - org trail: 146,273 events, 0 writes;
   - served trail: 2333 WriteOnly events on `platinum/firm/`.
7. **`comp-iam roles`.** 209 Terraform roles, each with its `source:` file.
8. **`comp-iam role <name>`.** Run for 94 roles: 94 of 94 printed "No role matching". The control
   `comp-iam role FredMacroIngestionLambdaRole` resolves.
9. **The OAI reader.** One raw record read. The one seen reader with no identity grant is `userIdentity` type
   `AWSAccount`, principalId `AIDAJ3ELLOIDNV4A5IWRG`, accountId `CloudFront`. It is the OAI `E139998VWH0PD`, which
   `AllowScopedAdvisorOAI` names in the bd, inf and cot bucket policies.
10. **`bd-gold-layer-runner`.** `ec2 describe-instances` and `iam get-instance-profile` resolve it to host
    `i-01003b035d2988dfb` (stopped), instance profile `bd-exporter-profile`, role `bd-exporter-ec2-role`.
11. **Build.** `.scratch/c2/build_census.py` (scratch) writes the census: the prose half, a generated summary table,
    then ONE ```json fence.
12. **Criteria.** The five criterion invocations, each as the order names it, each under `timeout 120`.

## 4. Numbers

| Bucket | granted | seen | belt_only |
|---|---|---|---|
| opal-data-bd | 46 | 13 | 47 |
| opal-data-inf | 51 | 32 | 18 |
| opal-data-cot | 30 | 11 | 47 |
| opal-data-49financial | 16 | 4 | 13 |

- **Every seen principal is also granted,** 60 of 60 seen rows, once the OAI is mapped.
- **On `opal-data-49financial`, 2 of the 16 granted principals are literal:** `bd-exporter-ec2-role` and
  `opal-advi-stitch-landing-role`. The other 14 reach it by wildcard.
- **Tokens by the resource grammar:** 10 of 203 principal rows carry a firm token. The other 193 read `none`, and
  `token_basis` states why for each.

## 5. Controls

- **Mutant.** Two mutations of the written census:
  - one `opal-data-bd` granted row dropped with its denominator left at 46: `MISMATCHED: ['opal-data-bd.granted']`,
    `VERDICT: FAIL-DENOMINATORS`, rc=1;
  - one token blanked: `VERDICT: FAIL-TOKENS`, rc=1.

  Restored by a rebuild that is byte-identical to run 1. Both criteria then read PASS again.
- **Determinism.** Two builds from the same inputs are byte-identical: 290,337 bytes, `cmp` clean.
- **Negative control on the reading.** The org trail's 146,273 in-window data events contain 0 writes, as its ReadOnly
  selector predicts.

## 6. Rows filed

All four are in `surprise-channel/investigations/INVESTIGATION_v1.md`, as `OBSERVATION`, `INERT`, `UNDER_INVESTIGATION`:

- **`LGIC_ENFORCE-W2-S1`.** `comp-iam role` resolved 0 of 94.
- **`LGIC_ENFORCE-W2-S2`.** `bd-gold-layer-runner` is a host, not a principal.
- **`LGIC_ENFORCE-W2-S3`.** No write to `opal-data-49financial` is observed at all, and item2e's header is stale.
- **`LGIC_ENFORCE-W2-S4`.** Belt-only principals and the 49financial bucket-policy Deny sit beside `granted`, not in it.

## 7. Limits

- **Unobserved writes.** Writes outside `platinum/firm/` are not observed, and on `opal-data-49financial` no write is
  observed at all.
- **Window end.** The last minutes before 20:00:52Z may be under-read: the newest delivered event is at 19:55:00Z.
- **What a grant means here.** A grant is an identity-policy Allow as written. Permissions boundaries, SCPs and
  statement conditions are not intersected with it: a conditioned Allow is still listed, and marked `conditioned`.
- **Not read.** Bucket and object ACLs, and S3 access points.
- **Tokens.** Read by the rule in the census's section 4. `lib/opal_naming.py` (EN-b-1) is not at this HEAD, so no
  builder graded them.
