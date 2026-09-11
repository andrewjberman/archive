# IB-s-5 RESULT -- THE FIRM DESTINATION POLICY AND THE INGESTION GATE

**TO:** `IRPT_BCKEND.TO-IB-s-5` | **worker:** `0.9.0_WK_IRPT_BCKEND~1` | **branch:** `wk-irpt_bckend-1-1`
**base commit:** `6800337403` (HEAD of `CLOUD` at hand-off, carrying the merged core root and key grammar)
**This cell APPLIED infrastructure.** 13 resources added, 0 changed, 0 destroyed, under a change-management
entry opened before the act and closed and committed before the grading reads.

## Criteria

| id | verdict | invocation | deciding line |
|---|---|---|---|
| `S5-AC1` | **PASS-by-output** | `timeout 300 python org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~1/battery_ib_s_5.py` | rc=0, `arms: 6 of 6 evaluated; arms holding: 6 of 6; assertions failed: 0` then `IBS5-POLICY-BOUND` |
| `S5-AC2` | **PASS-by-output** | `timeout 120 .tools/terraform.exe -chdir=infra/aws/terraform/investor-reporting/core plan -no-color -input=false -lock=false` | rc=0, `No changes. Your infrastructure matches the configuration.` |
| `S5-AC3` | **RECORDED (judgment)** -- no verdict | evidence assembled for `3.0.0_SA_CVO` at L9 | in the proof-of-spec instance under `UNVERIFIABLE-BY-INSTRUMENT` |

Transcripts committed beside this file: `IB-s-5_S5-AC1_battery_output.txt`, `IB-s-5_S5-AC2_plan_output.txt`.

## What was applied

`safe-apply` rc=0: **`Apply complete! Resources: 13 added, 0 changed, 0 destroyed.`** The pre-apply plan read
`13 to add, 0 to change, 0 to destroy` -- no IB-s-17 resource (bucket, tables, queues, key) is in this act's
blast radius.

- **IAM** 3 firm execution role stubs (`irpt-core-firm-49financial/cottonwood/inflection`) + 1 quarantine
  role stub, trust to `lambda.amazonaws.com` only. 3 scoped policies, each granting `s3:GetObject`/
  `PutObject`/conditioned `ListBucket` on `firms/<that firm>/*` alone, attached only to that firm's own role.
  1 write-only quarantine policy scoped to `quarantine/*`, zero access to any `firms/*` prefix.
- **POLICY** `firm_destination_policy.json` generated (`local_file`, same pattern IB-s-17 used for
  `layout.json`): `policy_version` `"1"`, `owner` `"0.7.0_AE_CloudOps"`, 3 firms each with `sender_domain`
  read from the registry, `execution_role`, the shared tables/queues by name, and 6 destination kinds
  rendered from the SAME locals `layout.json` itself renders from -- so the two documents cannot disagree
  about *where* evidence lives, only about *who* may write there.

**The gates that ran.** Same discipline as IB-s-17: halt-gate scanned the issuer's inbox (`2.0.0_SA_COO~B`,
a worker has no inbox); `comp-tagauthz` PASSED (0 candidate `aws_instance` resources); tombstone-gate CLEAN
on 13 creates vs 7 tombstones. No override used anywhere.

## The mechanism, and what the red-first mutants found in it

**`bind_firm()` is a closed four-branch outcome**, and its two hazard arms are checked in a specific order:
`display_from_used != False` (the spoofing signal) is checked FIRST and independent of `verified`, because a
spoofing claim is a finding about the evidence regardless of what else it says; then a non-`VERIFIED` verdict;
then a `VERIFIED` verdict resting on an unrecognized method (the contradiction arm); then domain lookup, with
Opal's own domain (`opalinvest.com`, cited from the PRD's B6 fixtures row) the one case that reaches
`Unresolved` rather than `Quarantined`.

**`BoundRequest` wraps `keys.TenantBinding` (IB-s-17) rather than reinventing immutability** -- the estate
already had the mechanism this class needs. A red-first mutant on `BoundRequest.__setattr__` exposed that
this reuse creates a SECOND, independent protection on `.firm_id` specifically (the property itself has no
setter), so disabling `__setattr__` alone left the criterion's own three attempts (set/rebind/delete)
**still raising** -- a weak mutant that didn't discriminate the mechanism it targeted. Fixed by adding a
fourth attempt against `_binding`, an actual `__slots__` member with no property protecting it, which DOES
discriminate: 4 of 4 mutation attempts now correctly fail when `__setattr__`'s raise is disabled.

**A second red-first mutant crashed the battery instead of failing it.** Disabling the spoofing check let a
spoofed fixture bind successfully; the battery's arm (c) then unconditionally read `outcome.reason` (a field
`Quarantined`/`Unresolved` carry and `BoundRequest` does not), crashing with an `AttributeError` before
printing a controlled failure. Fixed to report the unexpected bind as data (`"BOUND to firm_id=... -- THIS
FIXTURE SHOULD NEVER HAVE BOUND"`) rather than crash on it. All 4 of 4 mutants now fire cleanly and restore
byte-for-byte.

## Rows filed

- `IRPT_BCKEND-W1-S6` (OBSERVATION, INERT) -- the preflight named `comp-iam service irpt-core` and
  `comp-iam gaps` as the Phase 1/2 reads for this cell's role. Both ran post-apply and see nothing:
  `comp-iam stats` reads `IAM roles parsed: 191`, unchanged before and after, while the SAME apply's own
  `comp-tagauthz` sweep (a live `iam:GetAccountAuthorizationDetails` call) counts 231 roles, confirming the
  four are real and live. `comp-iam`'s static census walks backward from a Lambda/EC2 service definition to
  its role; a role stub with no compute resource assuming it yet has no entry point into that walk. Not a
  gap finding -- an absence from the tool's population. This cell's own claims are verified by other
  instruments instead (`get-role` for the trust policy, `terraform plan` for the full IAM documents).

## Bounds observed

The mailbox was not read and no request was created -- all sender evidence in this cell is fixtures. No
existing role was widened: the four roles are new, trust-policy-only stubs. `example-firm.com` was planted
and correctly resolved to `Quarantined` (an unregistered domain that is not Opal's own), matching the order's
own bound ("a domain that is not in the registry is not a firm, even if it looks like one").
No monitor, alarm, SNS or SES send. No credential in any artifact. No served output touched -- the only
writes are this cell's own new IAM resources, the generated policy document, and this worker's deliverables.
Every path written is inside the order's `<paths>` grant. No existing surprise row edited. `.tools/
commit-gate.sh` rc=0 on all four `.py` files. Every invocation ran under `timeout`.
