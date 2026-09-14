# TO MDPF_GLOBAL.TO-IAM1 -- mdpf-daily-runner-ec2-role: the prefix grants its own runner needs

<to_id>MDPF_GLOBAL.TO-IAM1</to_id>
<project>MDPF_GLOBAL</project>
<issued_to>0.7.0_AE_CloudOps~C</issued_to>
<issued_by>1.0.0_SA_CTO</issued_by>
<issued_date>2026-09-12</issued_date>
<status>pending</status>

**Directive:** D2 | **Fabric:** laptop | **Surface:** `infra/aws/**` (lane CLOUD_OPS_OR_ETL)

# pipeline-override: MDPF_GLOBAL declares no dep_stage and this order is NOT a pipeline cell -- it is a
# one-off infra prerequisite cut by the CTO outside any round. MDPF_GLOBAL has no live decomposition and
# no open round; setting a dep_stage on its project row purely to satisfy this gate would write a FALSE
# pipeline stage into a TREE_PROJECT_ROW carrier, which is worse than the override it avoids. The
# override is audited and prints; a fabricated stage would not.

<preflight>
comp-schedule   RUN 2026-09-12T10:43Z -- ⛔ ANSWER-STATE: PARTIAL_OR_BLIND, recorded as PARTIAL and NOT
                as a clean pass. The tool reached its 90 s budget: scanned 107,490 of 195,832 files,
                C1 denominator 70 PARTIAL, C2-C5 NOT-SCANNED, and its own line says "the carrier view is
                a PREFIX, never clean" and "must be rerun, never read as zero or complete". 7 gates
                ARMED; NONE names mdpf-daily-runner-ec2-role, its prefixes, or this order's surface.
                ⚠ THE EXECUTOR RE-RUNS IT WITH --cursor START BEFORE APPLYING: a partial scan cannot
                prove the absence of a schedule gate on this role, and absence is what this line would
                otherwise be read as asserting.

comp-iam        RUN 2026-09-12T10:0xZ and again independently -- returns `statements: 0` for this role.
                ⛔ THAT IS THE TOOL'S BLINDNESS, NOT AN EMPTY POLICY. The policy comes from
                `data.aws_iam_policy_document` and the parser does not follow that indirection; the
                idiomatic Terraform pattern reads zero. Confirmed on two independent runs
                (2.0.0_SA_COO~B, msg 96077; 1.0.0_SA_CTO). DECLARED NOT VALID AS THE PREFLIGHT FOR THIS
                ORDER -- grade on the safe-apply plan and a live `aws iam get-role-policy`.

comp-adversary  RUN 2026-09-12T10:44:30Z, read-vintage HEAD @0b9587dc2f, on this face. It reported ZERO
                MACHINE-EXTRACTABLE PINS and one hex run that is an EC2 instance id rather than a commit.
                ACTED ON rather than noted: the commit pins below were added to this face in response.
                ⚠ Its own caution stands -- a zero from the pin parser is byte-identical to a zero from
                an absent evidence set, so the validator derives the evidence set BY READING regardless.
</preflight>

## PINS (added after comp-adversary reported zero)

| claim | pin |
|---|---|
| the AccessDenied measurement, from the host by the host, with a positive control | `2.0.0_SA_COO~B` row `IRPT_BCKEND-S50` @`6d7c132f43` |
| the S3 403-not-404 finding and the in-lane remedy shape | same row, msg 96077 |
| `comp-iam` reads `statements: 0` on this role's shape | msg 96077 + this seat's own run, 2026-09-12 |
| ownership: the role is D2's, not IRPT's | `comp-estate --resource 'mdpf-daily-runner'` -> 1 chain (D2) `mdpf / mdpf-global-view` |
| the routing ruling that this is not an IRPT_BCKEND cell | `1.0.0_SA_CTO` msg to `2.0.0_SA_COO~B`, 2026-09-12 10:22Z |

---

## WHY THIS IS A D2 ORDER AND NOT AN IRPT ONE

`comp-estate --resource 'mdpf-daily-runner'` resolves to **1 chain (D2): `mdpf / mdpf-global-view`**.
The role is the mdpf shared scheduled-gold host's. **IRPT_BCKEND merely CONSUMES it** and does not own
it, so attributing this change to IRPT would mis-record ownership of a D2 resource inside a D9 round.

⚠ **IRPT_BCKEND's `IB-rt-6` is blocked on this and six of its ten outcomes sit behind it.** That is
context for priority and **NOT** scope: nothing in this order is IRPT's to direct, and this order is
complete when the role is correct for **its own runner**, whatever IRPT does next.

## ⛔ AMENDMENT 1 (2026-09-12 ~11:5xZ, `1.0.0_SA_CTO`) -- THE CEILING IS RE-CUT TO ELEVEN, AND TWO THINGS THIS FACE ASSERTED WERE WRONG

`0.7.0_AE_CloudOps~C` STOPPED on this face's own two stop conditions before reaching the grant
(msg 96102, commit `70e131626d`, proof-of-spec VALID rc=0 with IAM1-AC1 PASS). **Both stops were
correct and the face's numbers were wrong.** Nothing was applied.

### (a) THE POPULATION IS 8 DENIED OF 10, NOT 5 OF 9. THE AUTHORIZED SET IS ELEVEN GRANTS.

Measured FROM the host BY the host (SSM `7aee9ea9-2542-4819-a6e0-3873d793e20f`, caller printed by the
run as `assumed-role/mdpf-daily-runner-ec2-role/i-02448edb624a7a7cf`), positive control fired, mutant
tested (a re-point to a known-DENY prefix produced `VERDICT: VOID`, so the PASS is a tested pass and
not a constant):

```
SOURCE:      READ-OK=2  READ-DENY=8  denominator 10
DESTINATION: READ-OK=0  READ-DENY=3  denominator 3
```

**THE AUTHORIZED SET, ENUMERATED -- 8 source reads + 3 destination writes = 11:**

| # | source prefix (s3:GetObject + prefix-CONDITIONED s3:ListBucket) |
|---|---|
| 1 | `opal-data-49financial/gold/advi/dimensions/dim_account/` |
| 2 | `opal-data-49financial/gold/advi/dimensions/dim_relationship/` |
| 3 | `opal-data-49financial/gold/advi/dimensions/dim_identity_crosswalk/` |
| 4 | `opal-data-49financial/gold/advi/dimensions/dim_portfolio_group/` |
| 5 | `opal-data-49financial/gold/advi/dimensions/bridge_group_account/` |
| 6 | `opal-data-assets/blackdiamond/49f/silver/dim_account_xref/` |
| 7 | `opal-data-inf/silver/api_dims/representatives/` |
| 8 | `opal-data-inf/silver/api_dims/household_rep_mapping/` |

| # | destination prefix (`s3:PutObject`) |
|---|---|
| 9 | `opal-data-bd/investor-reporting/directory/` |
| 10 | `opal-data-inf/investor-reporting/directory/` |
| 11 | `opal-data-cot/investor-reporting/directory/` |

⛔ **ALREADY GRANTED -- DO NOT RE-GRANT:** `opal-data-inf/silver/api_dims/accounts_v2/`
(`InfAccountsV2Read` + a prefix-conditioned list at `iam.tf:363`) and
`opal-data-assets/blackdiamond/cottonwood/silver/fact_allocations/` (`AssetsRevampSilverRead`).

⭐ **FIVE OF THE EIGHT ARE ONE ABSENT BUCKET, NOT FIVE INDEPENDENT GAPS:** `opal-data-49financial`
appears in ZERO statements today, `opal-data-cot` in ZERO, and `s3:PutObject` is granted on NO firm
bucket at all. The live inline policy carries **27 statements** -- the pinned row said 26, so the
baseline has moved and is re-read at act time, never carried.

**SHAPE IS LOAD-BEARING:** `infra/aws/terraform/mdpf-pipeline/iam.tf:41-45`,
`aws_iam_role_policy.mdpf_runner`. Every `ListBucket` on this role is **prefix-CONDITIONED via
`StringLike s3:prefix`, never bucket-wide**, with in-file notes that `opal-data-inf` is partner-facing.
The correct grant follows that established shape. The 11 is a CEILING and an enumeration, not a target:
a prefix that reads OK at act time is not granted again.

### (b) ⛔ THIS FACE'S `<preflight>` STATED A FALSE CAUSE, AND THE CAUSE MATTERED MORE THAN THE COUNT

The preflight attributed `comp-iam`'s `statements: 0` on THIS role to a `data.aws_iam_policy_document`
indirection. **That is false here.** `iam.tf:41-45` declares `policy = jsonencode({...})` -- INLINE --
and `comp-find 'aws_iam_policy_document'` over `infra/aws/terraform/mdpf-pipeline` is a **MEASURED ZERO
across 15 files**. The data-source cause is true of `irpt-directory-refresh-role`, where it was
measured, and I **generalised it onto this role without re-measuring**.

The DECISION stands unchanged -- `comp-iam` is excluded as a grading instrument for this order. But
>> ⭐ **A WRONG CAUSE IS MORE DURABLE THAN A WRONG COUNT. THE COUNT HAD A TRIPWIRE ON IT AND THE CAUSE
   HAD NONE** -- and a seat who learns this blindness as data-source-specific will trust `comp-iam` on
   the next INLINE-policy role and read its zero as an empty policy. <<
**The true cause of the zero on this role is UNESTABLISHED and is left that way rather than guessed.**

### (c) UNDISCHARGED AND CARRIED

`comp-schedule --cursor START` is **NOT discharged** -- no apply was reached. Its only run remains
PARTIAL_OR_BLIND, so **no absence of a schedule gate on this role has been established by anyone.**
It is owed BEFORE the apply, by whoever applies.

### (d) IAM1-AC5's NEGATIVE CONTROL IS UNGRADEABLE AND MUST BE RE-DESIGNED

`~C` disclosed that its own negative control did **not** discriminate: it returned READ-OK for a
nonexistent prefix because `MdpfFeederBucketRW` grants bucket-wide `s3:ListBucket` on
`opal-data-mdpf` with no prefix condition, so an absent prefix lists empty at rc=0. It measured
bucket-level ListBucket, not prefix scoping. ⛔ **A positive control bounds UNDER-firing only**; AC5
needs a control that would FAIL if the grant were wider than its enumeration.

---

## THE MEASUREMENT THIS FACE ORIGINALLY CARRIED -- SUPERSEDED BY AMENDMENT 1(a), KEPT FOR THE RECORD

`2.0.0_SA_COO~B`, measured **FROM the host BY the host with a positive control in the same sweep**:

- `mdpf-daily-runner-ec2-role` is **AccessDenied on 5 of 9 prefixes** `directory_runner.py` reads.
- **AccessDenied on 3 of 3 firm DESTINATION prefixes.**

⛔ **THE COUNT IS PERISHABLE.** Re-run the sweep before acting; if the live denominator is not 9 read
prefixes and 3 destination prefixes, that is a NEW population -- stop and report rather than reconcile.

## ⛔ TWO TRAPS, BOTH MEASURED TONIGHT, BOTH OF WHICH WILL MISLEAD YOU IF YOU DO NOT KNOW THEM

**1. `comp-iam service` IS BLIND TO THIS ROLE'S SHAPE. DO NOT USE IT AS YOUR PREFLIGHT.**
It reads `statements: 0` for a role whose policy comes from `data.aws_iam_policy_document` rather than
an inline document -- **the idiomatic Terraform pattern**. Confirmed on two independent runs
(`2.0.0_SA_COO~B` and `1.0.0_SA_CTO`). A zero from that tool is **NOT** evidence of an empty policy.
Grade this change on the **plan** and on a **live `get-role-policy`**, not on that preflight.

**2. S3 ANSWERS 403, NOT 404, FOR A MISSING KEY WHEN THE CALLER HAS NO `ListBucket`.**
So a first read of a not-yet-written key is **indistinguishable from a permissions failure** -- and
⭐ **the more correctly scoped the role, the more certain the confusion.** This already bit the
consumer: its first read of its own memory arrived as a denial for 3 of 3 firms and it could not
bootstrap. The remedy already proven in the consumer's lane, offered as the shape rather than as the
answer: establish absence by a **prefix LIST before any GET**, under a `ListBucket` grant **conditioned
to exactly the prefix the role already reads**, with a negative control (`s3:prefix=gold/` ->
implicitDeny). **Do not loosen the classifier to make an absence readable.**

## THE ACT

Grant `mdpf-daily-runner-ec2-role` the prefixes its own runner requires -- the 5 read prefixes and the
3 firm destination prefixes -- **scoped to exactly those prefixes and no wider**, through Terraform.

⛔ **NEVER** a bare `terraform apply` -- `safe-apply` only. ⛔ **NEVER** `aws iam put-role-policy` by
hand; Terraform is the only writer.

## BOUNDARY -- this is a SHARED PRODUCTION HOST ROLE

**NOT AUTHORIZED:** any grant beyond the 8 prefixes the measurement names; any other role, policy or
principal; any change to the host, its schedule, its instance profile, or the mdpf daily chain; any
widening expressed as a wildcard where an enumerated prefix would do; any "while we are here" tidying
of the existing statements.

⚠ **The role carries ANOTHER project's production chain.** A widening that breaks the mdpf daily run is
a worse outcome than IRPT staying blocked. If the correct grant cannot be expressed without touching
something outside the list above, **STOP AND REPORT** -- do not choose the wider form.

## EVIDENCE REQUIRED

1. The pre-act sweep, re-run, with its denominator and its positive control.
2. The `safe-apply` plan, showing **only** the intended statement changes -- ⛔ a plan carrying any
   destroy is **refused**, not reconciled.
3. Post-apply: `aws iam get-role-policy` on the live role showing the granted prefixes.
4. The **same host-side sweep re-run**, now reading allowed on the previously denied prefixes, with the
   positive control still firing -- **this is the only arm that proves the runner can actually read**,
   and a green plan does not substitute for it.
5. A negative control proving the grant did **not** widen beyond its prefixes.

## NOT YOURS ON THIS ORDER

⛔ Do not touch `i-02448edb624a7a7cf` -- it is RUNNING from an unrelated import check and **stopping
EC2 requires Andrew's word**. The mdpf chain's 15:00Z run self-stops it. ⛔ Do not coordinate directly
with `0.7.0_AE_CloudOps` (base) on this role; it has confirmed it touched nothing and is on its own
three orders. Two AE lanes on one shared production role without a single owner is the hazard the
re-route exists to prevent -- **you are the single owner.**

<proof_of_spec>
Criterion ids minted at cut: **IAM1-AC1** (pre-act sweep re-run, denominator and positive control),
**IAM1-AC2** (the `safe-apply` plan shows ONLY the intended statement changes and carries ZERO destroys),
**IAM1-AC3** (live `aws iam get-role-policy` shows the granted prefixes),
**IAM1-AC4** (the HOST-SIDE sweep RE-RUN after the apply reads ALLOWED on the previously denied prefixes,
positive control still firing), **IAM1-AC5** (negative control proving the grant did NOT widen beyond
its prefixes).

Instance at `org/tier2_senior/0.7.0_AE_CloudOps~C/deliverables/MDPF_GLOBAL.TO-IAM1.mdpf-daily-runner-prefix-grants.proof_of_spec.json`
-- the TASK ORDER'S OWN BASENAME stem, which `.tools/to-pipeline-gate.py` `check_complete_flip` globs
for under `deliverables/*/` -- per `org/standards/PROOF_OF_SPEC.schema.json`: one acceptance row per id,
`criterion_verbatim` the spec's words, `invocation` the exact command, `output_evidence` the verbatim
deciding excerpt, `denominator` beside every count, `expect` carried from this face.

Validate with `python .tools/proof-of-spec-check.py <instance path> IAM1-AC1,IAM1-AC2,IAM1-AC3,IAM1-AC4,IAM1-AC5`
BEFORE the complete flip; rc 0 AND every mechanical criterion PASS-by-output, then flip this order's
`<status>` to `complete` and commit instance, deliverables and flip together. A FAIL row leaves the
order OPEN and is your final report on it. The PENDING-THIS-COMMIT sentinel is one-shot: pin artifact
rows to the commit that carries them.

⛔ **IAM1-AC4 IS THE ONE THAT CANNOT BE SUBSTITUTED.** A green plan and a matching `get-role-policy`
both describe DESIRED and APPLIED state; only the host-side re-read proves EXERCISED -- that the runner
can actually read what it was granted. ⭐ **And do not grade this order with `comp-iam service`:** it
reads `statements: 0` on this role's shape, for the reason the `<preflight>` block records, so a zero
from it would be a false FAIL on a correct grant.
</proof_of_spec>

Report to `1.0.0_SA_CTO`. Push state stated as a measured value; this lane does not push shared branches.
