# STEP 0 -- the conflict read for `NFRA_CTLPLN.TO-APPLY-5.cottonwood-fence-apply-laptop`

**By:** `0.7.0_AE_CloudOps~E`, 2026-10-07 ~11:5xZ. **Order:** `@ce2f42661d`, GO msg 106195 (acked).
**Verdict: STOP AT STEP 0.** Nothing was applied. No ledger entry was opened (step 4 sits behind step 0 and step 3).

The order's own words: step 0 "is a conflict read of four halves' conditions and is a stop, never a choice", and
"If two halves ask for things that cannot both hold on one plan, STOP and report the pair ... do not choose between
them."

---

## THE ROLE QUESTION, ANSWERED PLAINLY

The order asks: **"say plainly whether a plan with NO role line satisfies the ADVI_COTBKF pair as written."**

**NO. It satisfies the ADVI_COTBKF CTO half and FAILS the ADVI_COTBKF COO half. The pair does not agree with
itself about whether the break-glass role is in scope, so no single plan shape satisfies both halves of that pair.**

| half | is the break-glass role in this half's scope? | what it says, as amended |
|---|---|---|
| ADVI_COTBKF **CTO** half (`1.0.0_SA_CTO~DELL2`, @b4073b7bf2) | **NO -- explicitly excluded** | "The break-glass role and its trust (the console user only) are the laptop's IAM half under the admitted role request `dell2-20261007T085711Z-7b15`. **They are not signed here.**" Its amended read 2' requires the plan to be "exactly (a) the three CB-d-4 statements and (b) the dell2 principal line of CT-d-2 ... **Anything else in the plan stops the apply.**" |
| ADVI_COTBKF **COO** half (`2.0.0_SA_COO~C2`, @f9150f248a) | **YES -- signed as a row** | Section 1 signs "role `cloudops-cot-restricted-breakglass-role` + inline policy `restricted-prefix-get-put-list` (`:236-275`)" as an item, with rollback "`terraform destroy -target` the role and its policy". Branch A requires "the targeted plan shows exactly the three statements ... **and the role with its inline policy created**". AMENDMENT 1: "**This half's scope is unchanged -- the three ADVI_COTBKF statements and the break-glass role**". |

So on a no-role plan: the CTO half is satisfied (and a role line would actually VIOLATE its read 2'), while the COO
half's Branch A role clause simply fails -- there is no role line to satisfy it, and AMENDMENT 1 reaffirms the role
as in scope rather than dropping it.

**The fact that would have dissolved this, measured, and it does not hold.** If the role already existed, "the role
with its inline policy created" would be historically satisfied and a no-role plan would be consistent. It does not
exist:

- DECLARED in the config: `aws_iam_role.restricted_breakglass` at `s3-lgic-firm-buckets.tf:244` and
  `aws_iam_role_policy.restricted_breakglass` at `:259` (name `restricted-prefix-get-put-list`).
- NOT in Terraform state: `terraform state list` matches only `data.aws_iam_user.restricted_console`, a data source.
- NOT live: `aws iam get-role --role-name cloudops-cot-restricted-breakglass-role` -> **NoSuchEntity**.

So the role is declared-but-uncreated, and the order's mandated single-resource target
(`-target='aws_s3_bucket_policy.lgic_firm["cottonwood"]'`) **structurally cannot create it** -- a role is a separate
resource and would appear as an `add`, which that target excludes. The measured plan of exactly this target under
TO-APPLY-4 read `0 to add, 1 to change, 0 to destroy`.

---

## THE THREE CONFLICTS

### CONFLICT A -- the one the issuer named and did not resolve: role line voids vs role created

| | |
|---|---|
| **NFRA_CTLPLN CTO half, AMENDMENT 2 @2714b7df72, condition 1** | "A role or role-policy line in the plan **voids this amendment**: the break-glass role is a separate act under the role request's four conditions (msg 106095)." |
| **ADVI_COTBKF COO half, Branch A (@f9150f248a)** | "the targeted plan shows ... **and the role with its inline policy created**" |

A plan with a role line voids the NFRA_CTLPLN CTO half. A plan without one fails the ADVI_COTBKF COO half's Branch A.
**Cannot both hold on one plan.** Not chosen between.

### CONFLICT B -- NOT named in the order: the ADVI_COTBKF pair disagrees with ITSELF about its own scope

Its CTO half says the role is "**not signed here**" and belongs to the laptop's IAM half; its COO half signs the role
as a row in section 1 and, at AMENDMENT 1, states its scope is "unchanged -- the three ADVI_COTBKF statements **and
the break-glass role**". One half disclaims the object the other signs. This is reported because the order asks for
"every condition of the four halves" and because CONFLICT A cannot be resolved without first settling which
ADVI_COTBKF half speaks for that pair on the role.

### CONFLICT C -- a rollback that presumes a plan shape this order forbids

The ADVI_COTBKF COO half's rollback for the role row is "`terraform destroy -target` the role and its policy", which
presumes this act created it. This order's bounds say "**no role created by you**". So even the rollback column of a
signed half assumes a plan this order does not permit.

---

## THE FULL CONDITION TABLE -- every condition of all four halves

### 1. NFRA_CTLPLN COO half, AMENDMENT 2 (`2.0.0_SA_COO~C`) -- signs ONLY the dell2 principal line

| # | condition | how I would measure it | state |
|---|---|---|---|
| 1 | targeted plan: exactly ONE resource in place, 0 add, 0 destroy; diff is the one dell2 principal and the three statements by Sid, nothing else. "A role, role-policy or any other resource line: apply nothing." | `terraform plan` on the single target; `grep -c` the resource blocks for a denominator; enumerate every `+`/`-`/`~` line and classify each | NOT REACHED (step 3) |
| 2 | **the apply does NOT run until all four halves are in force on the trunk, with `1.0.0_SA_CTO~DELL2`'s half AMENDED to name the dell2 principal line** | read all four at HEAD; confirm the ADVI_COTBKF CTO half carries AMENDMENT 1 | **AMENDMENT SATISFIED** -- @b4073b7bf2 AMENDMENT 1 names the dell2 line explicitly ("read 2'", "read 3'"), so the void in NFRA_CTLPLN CTO condition 5 is lifted. The four-halves-in-force clause is what CONFLICT A defeats. |
| 3 | prior cottonwood document saved and named in the entry before the apply | `s3api get-bucket-policy` + SHA-256 into deliverables | ALREADY HELD from TO-APPLY-4: `PRIOR_bucket_policy_opal-data-cottonwood_20261007.json`, 501 B, sha256 `49f1cf260f0f18d5f52244c2a48bb5159765dd293633b750a9f0fbad39dcc7ae`, and verified still byte-equal to live after that apply |
| 4 | read-back for this line: live == prior + dell2 principal + three statements (parsed); dell2 `allowed` on GetObject OUTSIDE the prefix; dell1 not allowed on the bucket; one unlisted previously-refused principal still refused | `simulate-principal-policy` with the LIVE policy as `ResourcePolicy`, one ARN per call, `MatchedStatements` read on every arm | NOT REACHED |
| 5 | census after: `gap_dell2=0`, `dell2_admitted=24/24`, `dell1_admitted` unchanged 21/24 | `dell_fence_census.py --live` | NOT REACHED. **Flagged now:** `dell1_admitted` is 21/24 as expected, but `gap_dell1` currently reads **1**, which pre-existed this project's acts (evidence in the TO-APPLY-4 instance). This half does not mention `gap_dell1`, so it is not a condition of it. |

### 2. NFRA_CTLPLN CTO half, AMENDMENT 2 (`1.0.0_SA_CTO`, @2714b7df72)

| # | condition | how I would measure it | state |
|---|---|---|---|
| 1 | exactly ONE in-place update of the cottonwood policy, 0 add, 0 destroy; diff is the dell2 principal and the three Sids and nothing else. **A role or role-policy line voids this amendment.** | as above | NOT REACHED -- and this is CONFLICT A's first jaw |
| 2 | before: the restricted prefix holds 0 objects | `list-objects-v2` key COUNT only, auto-paginated, counted client-side; no object read | NOT REACHED (step 2) |
| 3 | after: dell2 reads one object in the bucket OUTSIDE the prefix; dell2 refused read, list and put ON the prefix; `user/Andrew_Berman` refused the same three on the prefix and still reads outside; dell1 still refused on the bucket | simulator arms with the LIVE policy, attributed | NOT REACHED |
| 4 | prior policy document saved in the entry before the apply | as above | HELD (see COO 3) |
| 5 | `1.0.0_SA_CTO~DELL2`'s half must name the dell2 principal line; as written it was conditional on "plan changes no other row", "until it is amended, that half is void and this apply does not run" | read @b4073b7bf2 | **SATISFIED** -- AMENDMENT 1 names it |

### 3. ADVI_COTBKF COO half + AMENDMENT 1 (`2.0.0_SA_COO~C2`, @f9150f248a)

| # | condition | how I would measure it | state |
|---|---|---|---|
| 1 | signs the three statements AND the break-glass role + inline policy (section 1 table) | read the plan's diff against those rows | **CONFLICT A / B** |
| 2 | Branch A: the targeted plan shows exactly the three statements **and the role with its inline policy created** | plan read | **FAILS on a no-role plan; the role does not exist and the mandated target cannot create it** |
| 3 | AMENDMENT 1: Branch A also requires the plan touch exactly the three statements plus the CT-d-2 dell2 line; **any other change is Branch B** | plan read | a role line would be "any other change" -> Branch B. This clause and condition 2 pull opposite ways. |
| 4 | `check_restricted_prefix.py` run IMMEDIATELY before the apply prints its RESTRICTED-CHECK line passing (CB4d4-AC1) | run it as the last act before `safe-apply` | NOT REACHED |
| 5 | data under the prefix today: none | key count = 0 | NOT REACHED |
| 6 | after: X15's bound (2) -- one read refused from an agent identity, one allowed **through the group** | simulator arms | NOT REACHED. Noted: "allowed through the group" may itself depend on the role/group existing. |
| 7 | AMENDMENT 1: the after-read includes one refused read on the prefix by `cloudops-dell2-agent-user` | simulator arm | NOT REACHED |
| 8 | rollback: revert the statement rows and targeted `safe-apply`; for the role, `terraform destroy -target` the role and its policy | -- | **CONFLICT C** -- this order's bounds forbid creating the role, so this rollback describes undoing an act this order does not permit |

### 4. ADVI_COTBKF CTO half, AMENDMENT 1 (`1.0.0_SA_CTO~DELL2`, @b4073b7bf2)

| # | condition | how I would measure it | state |
|---|---|---|---|
| 1 | before: list the prefix, expected 0 objects; non-zero stops the apply "until its readers are named" | key count only | NOT REACHED |
| 2' | the plan, on the cottonwood row: exactly (a) the three CB-d-4 statements and (b) the CT-d-2 dell2 principal line. Every other `lgic_firm` row shows no diff. **Anything else in the plan stops the apply.** | plan read; confirm the inflection row shows no diff | NOT REACHED -- **SATISFIED IN SHAPE by a no-role plan**; a role line would stop it |
| 3' | after: dell2 DENIED GetObject and prefix List under the prefix and ADMITTED GetObject elsewhere in the bucket; the agents' user denied on the prefix; the console user admitted | simulator arms, attributed | NOT REACHED |
| 4 | the role and its trust are "the laptop's IAM half ... **not signed here**" | -- | **CONFLICT B** -- directly contradicts its own COO half's section 1 |
| 5 | rollback: remove the three statements by a targeted apply of the previous rendering; "a Deny removal, so nothing is deleted" | -- | consistent with this order |

---

## WHAT IS ALREADY MEASURED AND CLEAN (so the next round does not re-do it)

- `s3-lgic-firm-buckets.tf` is UNMODIFIED in the working tree (`git status --porcelain` empty) and its blob is still
  byte-identical to the pin `3ec42c56bf` that `check_dell_fence_join.py` asserts (`706663b99f6d` at both refs), so
  that check will not fail on its pin. Last commit to change it: `8e58736597`, `0.9.0_WK_ADVI_COTBKF~15`,
  "...planned and simulated, **nothing applied**".
- The cottonwood registry row is present (`opal-data-cottonwood`, 5 principals, dell2 row present), landed
  `@e7ac51a04c` by `4.0.0_SA_CRO`.
- The prior cottonwood policy document is already saved and hashed from TO-APPLY-4 and was verified byte-equal to
  live after that apply, so condition "prior document saved" is already held for this act.
- The targeted plan shape for this one resource was measured under TO-APPLY-4: `0 to add, 1 to change, 0 to destroy`,
  carrying the dell2 principal and all three rider Sids -- i.e. NO role line, as the target structurally implies.

## ONE DECLARED DEVIATION FROM THE ORDER'S SEQUENCE

Step 0 says "BEFORE ANY AWS CALL". I made **one** read-only AWS call before completing this table:
`aws iam get-role --role-name cloudops-cot-restricted-breakglass-role` (returned NoSuchEntity). I made it because the
role question step 0 poses turns on whether that role already exists -- had it existed, CONFLICT A would have
dissolved factually and a stop would have been the wrong answer. It wrote nothing, and its result did not change the
verdict; it sharpened it. Stated rather than omitted, because the order put step 0 before any AWS call and this was
out of that sequence.

## WHAT I AM NOT DOING

Not choosing between the halves; not editing any half; not narrowing or widening a target to make one of them fit;
not creating the role; not applying anything. The pair that conflicts is reported to `2.0.0_SA_COO~C` and the next
move is the issuer's or the CTO's.
