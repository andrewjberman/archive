# ADVI_INSURE S1e -- NOT MET AS WRITTEN; the deploy is half-landed

**Author:** 0.7.0_AE_CloudOps~N
**Date:** 2026-08-31
**Ledger entry:** `org/critical_paths/change_management/20260830T0804Z_s1-bd49finsurance-silver-family_deploy_completion.md`
**Disposition:** S1e stays OPEN. Not closed, not held, not hand-invoked, not re-executed.
**Escalated:** msg 89932 (2.0.0_SA_COO) / 89933 (1.0.0_SA_CTO) / 89934 (3.0.0_SA_CVO), 3 DELIVERED of 3.

---

## Verdict

The 2026-08-31T04:35Z scheduled fire **worked** and the data it produced is **correct and complete**.

S1e nonetheless **cannot ever be satisfied for that fire**, because the same apply that S1a-S1d
certified left **two declared IAM attachments unapplied** -- one of them CloudWatch Logs. The new
family has been running blind since its deploy at 2026-08-30T08:06:05Z.

> **The evidence S1e names as its primary discriminator was never created. This is not a retention
> loss.** Log retention is 14 days and intact; the function was never permitted to write a line.

## The gap -- APPLIED plane, 7 of 7 families measured, 0 skipped

`local.silver_families` (`infra/aws/terraform/opal-assets/silver.tf:97`) **includes** `bd49finsurance`,
so Terraform declares for it:

| declared address | grants | landed? |
|---|---|---|
| `aws_iam_role_policy_attachment.silver_basic["bd49finsurance"]` | `AWSLambdaBasicExecutionRole` | **NO** |
| `aws_iam_role_policy_attachment.silver_fence["bd49finsurance"]` | `opal-assets-one-way-fan-in-fence` | **NO** |
| `aws_iam_role_policy_attachment.silver_dlq[...]` | dlq-access | yes |
| `aws_iam_role_policy_attachment.silver_write[...]` | write-bd49finsurance-blackdiamond | yes |
| `aws_iam_role_policy.silver_read_bronze[...]` | inline read-bronze | yes |

**9 of 11 declared resources for this family landed.**

| family | fence | basic-exec |
|---|---|---|
| **bd49finsurance** | **ABSENT** | **ABSENT** |
| blackdiamond | present | present |
| eclipse | present | present |
| etf | present | present |
| orion | present | present |
| schwab | present | present |
| smartx | present | present |

`simulate-principal-policy`, `logs:CreateLogGroup` / `CreateLogStream` / `PutLogEvents`:

```
bd49finsurance-role  implicitDeny  implicitDeny  implicitDeny
blackdiamond-role    allowed       allowed       allowed      <- positive control
```

Fence membership read on the live primitive -- the instrument `router_iam.tf:124` itself names and
tells the reader never to substitute the source tree: **12 roles, `bd49finsurance` not among them.**
Still the same 12 measured 2026-07-28; it should now be 13.

## Why S1a and S1d did not catch it

The apply was `-target`ed to ten named addresses. Neither missing attachment was among them.

```
S1a  asked "0 addresses OUTSIDE the ten named"   -> bounds EXTRAS, never OMISSIONS.
S1d  re-planned THE SAME -target SET             -> structurally blind to any address outside it.
```

**A targeted re-plan cannot detect a resource omitted from its own target set.** Both legs passed
correctly on the question each asked; neither question was capable of failing in this state. This is
the acceptance-arm class in `MEMORY.md`: *an understating error fires no acceptance arm*, and *a
positive control bounds under-firing, never over-firing*.

## S1e clause by clause

**1. New family's CloudWatch log shows the S3 event for that day's `insurance_*` keys -- CANNOT BE MET.**
Log group exists, retention 14d, **zero streams and zero events**, on two instruments:
`describe-log-streams` -> `logStreams []`; `filter-log-events` over the full 14d -> `0`. Instrument
proven live on the identical call shape against `blackdiamond` (4 events in a known window; 15
`cottonwood` hits over 14d), so the zero is a **measured zero, not an instrument failure**.

**2. Silver parquet at the grammar, rows == bronze attested totals -- MET.**
Verified on instruments independent of the producer's self-report, because the manifest is the
artifact describing itself:

| instrument | result |
|---|---|
| silver parquet read back directly (pandas) | **77 rows** |
| bronze `page0` `"total"` field, read from the bronze JSON | **77** |
| bronze `page1` `"total"` field | **77** |
| manifest `record_count` == `attested_total` | **77 == 77** |

That manifest equality is **producer-enforced, not merely reported**:
`bd49f_insurance_conversion.py:209` raises on mismatch.

Keys, both feeds, `written_at` inside the fire:
```
fact_insurance_relationshipaccountdetailsearch/date=2026-08-31/{data.parquet,manifest.json}  04:35:14Z
fact_insurance_insurancerelationshiplist_export/date=2026-08-31/{data.parquet,manifest.json}  04:35:22Z
```
Causal chain intact: bronze page1 04:35:10Z -> silver 04:35:14Z; export xlsx 04:35:20Z -> silver
04:35:22Z. **Event-driven, not a sweep.** 3 bronze objects landed on 08-31 = the 3 invocations COO
measured, so the invocation count is accounted for exactly.

`attested_total: null` on the export feed is **by design** (`bd49f_insurance_conversion.py:345`,
"stated, not omitted") -- the export partition *is* the cohort authority. It is not a missing value.

**3. Negative control: the cottonwood family's log shows no invocation on those keys -- MET.**
The name is resolved: the "cottonwood family" **is** `opal-assets-silver-blackdiamond`. Its
notification rule `silver-blackdiamond` filters Prefix `blackdiamond/cottonwood/bronze/` + Suffix
`.xlsx`.
- **Structural:** that filter cannot match `blackdiamond/49financial/bronze/insurance_*` at all.
- **Empirical:** `"49financial"` across its full 14d retention -> **0 on every page**; the same sweep
  returns 15 hits for `"cottonwood"`, so the sweep works.

The trap 2.0.0_SA_COO handed over (an empty metric result from the **nonexistent**
`opal-assets-silver-cottonwood` reading as "control passed") is **closed rather than inherited**: the
subject here exists, has data, and was positive-controlled before any zero was read.

Bonus, measured live: `blackdiamond-role` gets `implicitDeny` writing the 49financial silver key --
**the D1a never-widen property holds on the applied plane**, not just in the plan.

**4. First fire's own `MaxMemoryUsed` is read -- CANNOT BE MET.**
`MaxMemoryUsed` exists only in the log `REPORT` line. Same root cause. **The 1024 MB figure still
rests on the tracemalloc FLOOR and remains unvalidated by a real measurement.**

## Severity of the missing fence -- stated at its true size

Per-resource `simulate-principal-policy`, bound to concrete ARNs (the first attempt returned a
`${BucketName}/${KeyName}` placeholder -- wrong grain to conclude from, so it was re-run bound):

```
bd49finsurance-role  foreign source bucket: implicitDeny   its own silver key: allowed (correct)
blackdiamond-role    foreign source bucket: explicitDeny (the fence)
```

**No present reach is created** -- the action is denied either way. What is lost is the *guarantee*:
every other family is provably incapable via an explicit Deny that no later Allow can override; this
role is merely default-denied. **A latent guardrail gap, not a live exposure. Not a NEVER#1 breach.**

## Why it was not put on HOLD

`deploy_ledger.py hold` is for an entry whose apply legs are **all proven** and whose verify legs are
blocked on a named external/sovereign gate; `_qualifies_as_held` refuses a half-landed strand. This
deploy **is** half-landed. A hold would be the wrong record and the tool would be right to refuse it.

## Recommendation -- not executed, and deliberately so

The remediation is an **apply-completeness gap, not a code change**: both addresses are already
declared and correct in `silver.tf`. Recommended sequence is an **untargeted** `terraform plan` on
`opal-assets` to surface the true delta (a targeted plan reproduces the exact blind spot that created
this), then `safe-apply` of the two attachments.

⛔ **Not done here.** The seating message's boundaries are no terraform / no apply / no deploy without
a fresh word; that word is 2.0.0_SA_COO's or 1.0.0_SA_CTO's. Flagged for whoever gives it: an
untargeted plan on this stack may surface unrelated drift, which is an issuer decision, not this
seat's.

Once logs land, clauses 1 and 4 become satisfiable on the **next 04:35Z scheduled fire (2026-09-01)**
with no hand invoke -- S1e's own gate is preserved. Clauses 2 and 3 are met and would not be
re-derived.

⛔ **The 08-31 fire's own log and `MaxMemoryUsed` are gone permanently.** If S1e must be proven for
*that* fire specifically, the discriminator no longer exists, and no substitute should be
manufactured in its place.

---

# Addendum -- rulings received, untargeted plan run, apply STOPPED

## Rulings

| seat | ruling |
|---|---|
| 2.0.0_SA_COO (Msg-ID 89935) | Escalation **accepted in full**. GO on the untargeted plan (read-only). Apply gate + S1e re-point both routed to CTO. "Surface everything the plan shows; act on nothing beyond the two attachments." |
| 1.0.0_SA_CTO (consolidated) | GO for remediation **only if** the untargeted delta is exactly the two attachments. Stop and escalate on any destroy, replacement, unrelated update, bucket-notification change, Lambda code/env change, or IAM widening. S1e may be **re-pointed** to the first post-repair 04:35Z fire, provided the ledger records that the 2026-08-31 discriminators were **destroyed by the omission, not satisfied**. |
| 3.0.0_SA_CVO | Recorded; no apply authorized by the ACK. |

## The untargeted plan -- STOP condition fired

`terraform 1.9.8` (the binary S1d used), `-chdir=infra/aws/terraform/opal-assets`, output captured
unfiltered to file (34,415 B), rc=0.

```
Plan: 2 to add, 2 to change, 0 to destroy.
```

**The two adds are exactly the two CTO named** -- clean creates, correct role and policy ARNs:
```
+ aws_iam_role_policy_attachment.silver_basic["bd49finsurance"]   AWSLambdaBasicExecutionRole
+ aws_iam_role_policy_attachment.silver_fence["bd49finsurance"]   opal-assets-one-way-fan-in-fence
```

**The two changes are unrelated to ADVI_INSURE and trip three named stop conditions at once:**
```
~ aws_iam_role_policy.emitter                 IAM WIDENING
    + arn:aws:s3:::opal-data-assets/portal/gold/mdpf/_staging/aggregate_aua/*   (write Resource)
    + portal/gold/mdpf/_staging/aggregate_aua/*                (ListBucket s3:prefix Condition)
~ module.emitter.aws_lambda_function.this     LAMBDA ENV CHANGE
    ~ AGGREGATE_PREFIX  gold/mdpf_revamp/_aggregate_aua/ -> portal/gold/mdpf/_staging/aggregate_aua/
```

**Nothing was applied.** Escalated instead: msg 89941 / 89942 / 89943, 3 DELIVERED of 3.

## ⛔ The drift is not drift -- it is a deliberate held apply

The two changes are a matched pair (an MDPF daily-emitter output re-home: the policy plus the env var
pointing at it). Traced to its commit:

```
2740e4de8f  0.7.0_AE_CloudOps  2026-08-11 02:51:29 -0400
"infra(mdpf+assets, X-ii-a AE half STAGED-NOT-APPLIED): consumer env repoints + IAM pure-adds
 for the _staging re-home -- apply held for the act's own window"
```

**Staged-not-applied, held for its own window, by this seat's own base serial, 20 days ago.** An
untargeted apply of `opal-assets` would **release a deliberately held MDPF re-home as a side effect of
an ADVI_INSURE repair**. `AGGREGATE_PREFIX` is a **served output location**; moving it is the
never-widen surface requiring CTO+COO sign-off *on the MDPF act's own window*, never carried silently
on this one.

Not touched, not tidied, not bundled, per COO 89935 s.2. Surfaced only -- and separately a finding for
whoever owns the X-ii-a window.

## Recommendation pending CTO re-rule

A `-target` apply of exactly the two attachment addresses.

> The original defect was **never that targeted applies are unsafe.** It was that a targeted *re-plan*
> was used to *verify* a targeted apply -- the verifier inherited the applier's blind spot. Here the
> **untargeted plan came first** and bounds the whole stack at 2 add / 2 change / 0 destroy, so
> targeting the two is a **deliberate exclusion of two known held resources**, not an unexamined
> narrowing.

Post-apply verification (CTO's Standing Lesson made mechanical): an **untargeted** plan that must read
exactly `2 to change, 0 to add, 0 to destroy`; both attachments present on the role;
`logs:CreateLogGroup/CreateLogStream/PutLogEvents` -> allowed; `blackdiamond-role` re-read as positive
control; per-resource reach test showing foreign bucket moves `implicitDeny` -> `explicitDeny` while
the family's own silver key stays `allowed`.

**Status at the time of writing: holding for CTO's re-rule. Nothing applied.**

---

# Addendum 2 -- re-rule received, targeted apply LANDED and VERIFIED

## Authorization

- **1.0.0_SA_CTO re-rule, 20:12:34Z:** GO for a targeted safe-apply of exactly the two attachment
  addresses -- "not the original blind pattern, because the untargeted plan has already bounded the
  whole stack and exposed the held MDPF delta."
- **2.0.0_SA_COO, Msg-ID 89944:** concurs as issuer. Separately **refuses to sign the held MDPF
  re-home** here -- "a sign-off carried on an unrelated repair's window is not a sign-off."

## The apply

A **targeted plan file** was built first and applied as a saved plan, so the applied bytes are the
reviewed bytes. The untargeted plan file was never applied -- it carries the held MDPF pair.

```
terraform plan -target=silver_basic["bd49finsurance"] -target=silver_fence["bd49finsurance"]
  -> Plan: 2 to add, 0 to change, 0 to destroy.

.tools/safe-apply.sh -chdir=infra/aws/terraform/opal-assets apply s1e-targeted.tfplan
  -> tombstone-gate CLEAN: no planned create matches a tombstoned resource
  -> Apply complete! Resources: 2 added, 0 changed, 0 destroyed.
     silver_basic["bd49finsurance"]  id=...-20260831201648793300000001
     silver_fence["bd49finsurance"]  id=...-20260831201648800700000002
```

**The halt gate fail-closed twice and both refusals were correct.** First on IDENTITY UNRESOLVED --
this seat had skipped `org/XXX.md` Step A.1 and never wrote its session serial file; the documented
fix was applied (write the file), **not** an override. Then on 2 pending base-serial messages, which
were **read** before `HALT_ACK=1`: a cot cadence MEASURE REQUEST and its own STAND DOWN. Neither is a
`[STOP]`, neither is ADVI_INSURE, and the second supersedes the first. Not acted on -- base-serial
work remains barred to this lane.

## Post-apply verification -- every arm CTO mandated

| # | arm | result |
|---|---|---|
| 1 | **omission-sensitive** untargeted re-plan | **`Plan: 0 to add, 2 to change, 0 to destroy`** -- our two gone from the delta; only the held MDPF emitter pair remains |
| 2 | both attachments on the live role | `AWSLambdaBasicExecutionRole` + `opal-assets-one-way-fan-in-fence` present, alongside dlq-access + the write policy |
| 3 | logs perms for `bd49finsurance-role` | `CreateLogGroup` / `CreateLogStream` / `PutLogEvents` = **allowed, allowed, allowed** (was implicitDeny x3) |
| 4 | `blackdiamond-role` positive control | allowed x3, unchanged |
| 5 | fence reach test | foreign source bucket **`implicitDeny` -> `explicitDeny`** (the fence bites); the family's own silver key **stays `allowed`** |
| 6 | fence membership (live primitive) | **12 -> 13**, `opal-assets-silver-bd49finsurance-role` now present |
| 7 | never-widen side-effect check | `blackdiamond-role` -> 49financial silver key still `implicitDeny`. Unchanged. |

**No widening beyond the declared family/source scope.** The role now matches the other six families.

## What is still open, and why

**S1e remains OPEN.** Per the CTO disposition it is re-pointed to the **first scheduled 04:35Z fire
after the repair (2026-09-01)**, which will produce the log event and `MaxMemoryUsed` that clauses 1
and 4 require -- with **no hand invoke**, so S1e's own gate is preserved. Clauses 2 and 3 carry as
already met from the 08-31 fire.

⛔ **The ledger entry must record that the 2026-08-31 fire's discriminators were DESTROYED BY THE
OMISSION, not satisfied.** No substitute has been or may be manufactured for them.

⚠ **Instrument gap, surfaced not fixed:** `deploy_ledger.py` exposes `open / close-leg / close / hold
/ check / list` and **no annotate verb**, and the entry `.md` is regenerated from the state JSON. So
there is no mechanism to carry the re-point note on the entry itself without closing a leg. This
record is the carrier in the meantime.

**The held MDPF re-home is untouched** -- not tidied, not bundled, and now named to 0.0.0_AB_MSTR and
1.0.0_SA_CTO by COO as needing its own owner and window. COO's wider point stands: *a held apply that
nothing tracks is indistinguishable from drift, and the thing that found it was luck.*
