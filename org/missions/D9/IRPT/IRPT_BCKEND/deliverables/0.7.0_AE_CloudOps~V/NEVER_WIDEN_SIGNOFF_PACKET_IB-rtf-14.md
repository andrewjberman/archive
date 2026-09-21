# NEVER-WIDEN SIGN-OFF PACKET -- IRPT_BCKEND.TO-IB-rtf-14 (the export role reads the receipt it serves)

**Seat:** `0.7.0_AE_CloudOps~V` | **Worktree:** `/c/tmp/wk-irpt-6-ae1` | **Order:** `org/missions/D9/IRPT/IRPT_BCKEND/task-orders/IRPT_BCKEND.TO-IB-rtf-14.the-export-role-reads-the-receipt-it-serves.md` @`19ccf82226` | **GO:** msg 98314

---

## 0. WHAT THIS PACKET ASKS THE TWO HALVES TO SIGN

**NO GRANT. NO PLAN CHANGE. NOTHING IS APPLIED.**

This is the order's own second branch, taken on measurement rather than on preference: *"OR, if (a)(iv)
shows the receipt is absent, NO grant and instead a ROW for the CTO ... the packet states which."*
**(a)(iv) shows the receipt is absent, and the measurement goes further than the branch anticipated:
the address the code reads is not merely empty, it is OUTSIDE THE EVIDENCE BUCKET'S DECLARED LAYOUT
AND NO WRITER IN THE CORPUS PRODUCES IT.** Signing a grant for it would widen an IAM role onto an
undeclared prefix of a shared evidence bucket in order to reach an object that does not and cannot
exist.

A half that signs this packet is signing **that no change is made**, that the export root stays at
**no-op**, and that the two defects are routed as rows rather than patched by a grant. **If either
half disagrees, the act it is refusing is the NON-act** -- say so and the seat re-cuts.

Rows filed with this packet: **`IRPT_BCKEND-S105`** (the address) and **`IRPT_BCKEND-S106`** (the
error-class mapping). Both `disarm_owner: 1.0.0_SA_CTO`; both remedies are source changes this order
bars in terms.

---

## 1. THE CAUSE, MEASURED -- arm (a)

**Identity line, arm (a)(i), (a)(ii), (a)(iv):** ran as `arn:aws:iam::313476888478:user/Andrew_Berman`
-- a configuration and document claim, NEVER a served behaviour.
**Identity line, arm (a)(iii)(A):** the INVOKE runs the deployed function AS ITS OWN ROLE
(`irpt-export-render-role`); the operator identity only issues the invoke.
**Identity line, arm (a)(iii)(B):** real S3 wire responses, one UNSIGNED (anonymous) and one operator,
parsed by the botocore the deployed bytes use.

### (i) The key the code builds, against the ARNs the role holds

| | |
|---|---|
| template (`export/entry.py:63-64` @HEAD) | `investor-reporting/export/{firm}/{export_id}/receipt.json` |
| deployed override `IRPT_EXPORT_RECEIPT_KEY` | **UNSET** -- the default above is what the function uses |
| bucket (`IRPT_EVIDENCE_BUCKET`) | `opal-data-ycharts` |
| concrete key, the export id rtf-12's arm (f) sent | `s3://opal-data-ycharts/investor-reporting/export/49financial/EXP-5db0796cbfcffc3c0c1d5291/receipt.json` |
| the role's policies / resource ARNs (live `get-role-policy`) | 4 policies, **15** resource ARNs, of which **7** carry `s3:GetObject` |
| `fnmatch` of the concrete key against each of the 7 | **0 match** |
| **verdict** | **OUTSIDE** |

`export/iam.tf:85-125` Sid `ReadWriteExportsPrefixOnly` =
`arn:aws:s3:::${local.evidence_bucket}/firms/*/generations/*/attempts/*/exports/*`.

> **THE FACE'S OWN PARENTHETICAL IS CONTRADICTED AND IT IS RECORDED RATHER THAN QUIETLY CORRECTED.**
> (a)(i) says the concrete key is `firms/<firm>/...`. It is not: the code builds
> `investor-reporting/export/...`. The face's premise was that the key sits inside the evidence
> layout and merely misses the grant's deeper segments. **The measured key is in a different address
> space entirely**, which is what turns branch (b) from "one ARN correction" into "no grant".

### (ii) `simulate-principal-policy` -- one resource per call, both controls

| action | resource | the role | positive control (`user/Andrew_Berman`) | negative control (`opalinvest-auth-lambda-role`) |
|---|---|---|---|---|
| `s3:GetObject` | the concrete key | **implicitDeny** | allowed | implicitDeny |
| `s3:ListBucket` (ctx `s3:prefix`) | `arn:aws:s3:::opal-data-ycharts` | **implicitDeny** | allowed | implicitDeny |
| `kms:Decrypt` (ctx `kms:ViaService`) | `.../key/7f4d3042-10d8-49a7-b55e-3c963cea8111` | **allowed** | allowed | implicitDeny |

Controls behaved as expected **6 of 6**. The role is denied on **2 of 3** actions.

> **A CORRECTION TO THIS SEAT'S OWN EARLIER MEASUREMENT.** An earlier pass recorded `kms:Decrypt` as
> `implicitDeny` for this role and carried that into the rtf-12 record's remedy notes. **That was the
> instrument, not the world:** the statement is conditioned on `kms:ViaService`, and a simulate call
> with no `--context-entries` returns `implicitDeny` byte-identically to a real deny (the documented
> false-deny mode 2). With the context supplied the same call returns **allowed**. **KMS IS NOT PART
> OF THIS DEFECT** and any remedy that touches the KMS grant is widening for nothing.

### (iii) The swallowed exception -- what CANNOT be printed, and what replaces it

**It cannot be printed verbatim from the live path, and the reason is structural, not effort:**

- `irpt-export-render-role`'s trust policy names `lambda.amazonaws.com` **only**, so this seat cannot
  assume it (`sts:AssumeRole` -> AccessDenied for `user/Andrew_Berman`). **The order's literal
  instrument -- "the recorder-patched diagnostic pair AS THE ROLE" -- is not available on this role**,
  and saying so is part of the answer.
- The boundary records internal errors to a **None sink (S91)**, so the class is not recoverable from
  the served answer or from CloudWatch either.

**Two instruments that CAN run, and together they close the question anyway:**

**(A) The live invoke pair, as the deployed role** -- the discriminator that the failure IS the read:

| arm | result |
|---|---|
| the S3 receipt read, as deployed | StatusCode 200, `public_reason_code` **UNEXPECTED**, `firm_id` present |
| `receipt_fixture {}` (the read bypassed) | StatusCode 200, no refusal code, `firm_id` present |

**(B) The REAL WIRE classes, measured on the same object** -- an UNSIGNED request reproduces the exact
403 the role receives, and the requester does not change how botocore parses it:

| request | HTTP | code | class |
|---|---|---|---|
| UNSIGNED (anonymous), the concrete key | **403** | `AccessDenied` | `botocore.errorfactory.AccessDenied` |
| operator, the concrete key | **404** | `NoSuchKey` | `botocore.errorfactory.NoSuchKey` |
| UNSIGNED, a key inside the grant | 403 | `AccessDenied` | `botocore.errorfactory.AccessDenied` |
| operator, a key inside the grant | 200 | -- | (positive control: the object reads) |

The handler's own test is `exc.__class__.__name__ in ("NoSuchKey", "ClientError")`
(`export/entry.py:100-103`). So: **`NoSuchKey` maps to `ExportRefused` -> NOT_FOUND; `AccessDenied`
does not match either name, propagates, and is served as UNEXPECTED.** That is the whole of S104's
operator-vs-role asymmetry, with no code difference between the two paths.

> **AND ONE INSTRUMENT IN THIS PACKET WAS WRONG BEFORE THE WIRE CORRECTED IT.** A hand-built stub
> raising `botocore.exceptions.ClientError` with an `AccessDenied` error code, through the deployed
> bytes, maps to `ExportRefused` and reads **GREEN**. **A stub asserts the class its author assumed;
> botocore's errorfactory mints a MODELED class per error code and raised a different one.** Both arms
> were run and they DISAGREE. The wire arm is the true one, and the stub arm is kept in the record
> because a packet that showed only the stub would have signed a grant to fix a mapping bug.

### (iv) The receipt object itself

| prefix listed (operator, who holds ListBucket) | KeyCount |
|---|---|
| the concrete key's own prefix | **0** |
| `investor-reporting/export/` (the template's WHOLE root) | **0** |
| `firms/` (the policy's prefix) | 2 -- both `firms/49financial/generations/GENRT8PROOF/attempts/1/exports/<rev>/bundle.json` |

**THE CASE THAT HOLDS: ABSENT.** Not "absent for this export id" -- absent for the entire address
space the reader builds.

---

## 2. THE WRITERS (W) -- the census the branch turns on

**Denominator: 38,705 tracked + 281 untracked files in this worktree.**

- **Sites that build a `receipt.json` OBJECT KEY: 3** -- `ycharts/generate/job.py:477-479` and
  `:324-326`, and `intake/poller.py:418-420`. **All three** build it through
  `_keys` / `destination_for` / `s3_evidence_key`, i.e. under `firms/{firm_id}/...`.
- **Sites that write the export's own evidence: 1** -- `export/handler.py:126-130`, which writes
  `keys.s3_evidence_key(tenant, "generations", [generation_id, "attempts", attempt, "exports",
  export_revision, "bundle.json"])` -- **the grant's exact shape**, and the two live objects above.
- **Writers of `investor-reporting/export/{firm}/{export_id}/receipt.json`: ZERO.**

**And the address is not declared.** `infra/aws/terraform/investor-reporting/core/layout.json` -- the
Terraform-generated declaration whose own `_meta` says *"IB-s-5 binds the FirmDestinationPolicy and
the per-firm IAM conditions to THIS declaration"* -- declares **three** prefix families, all
`firms/{firm_id}/...` (`generations`, `intake`, `requests`), plus `quarantine/`.
`_keys/keys.py:109-113` holds the same three as the runtime source, cross-checked by
`verify_against_layout()`. **`investor-reporting/export/` is in neither.**

---

## 3. BOTH BRANCHES, AND WHAT EACH ONE DOES NOT DO

**BRANCH 1 -- THE GRANT (the order's first branch). NOT TAKEN.**
The narrowest form would be one `s3:GetObject` resource ARN,
`arn:aws:s3:::opal-data-ycharts/investor-reporting/export/*/*/receipt.json`, added to
`export/iam.tf`'s evidence policy, `kms:ViaService` untouched, no bucket-wide or `kms:*` wildcard.
**What it WOULD do:** convert the served answer from UNEXPECTED to a truthful NOT_FOUND, because the
role would then receive `NoSuchKey` (404) instead of `AccessDenied` (403), and `NoSuchKey` IS in the
handler's name list.
**What it would NOT do, and why it is refused:**
1. it grants read on a prefix **outside `layout.json`**, contradicting the declaration every other
   per-firm IAM condition on this bucket is derived from;
2. it grants read to an address **no writer produces** -- a permanent grant for a permanently empty
   prefix, which no later least-privilege audit can distinguish from a live need;
3. **it would close the visible symptom while leaving S106 fully armed** -- any future denial on this
   route still serves UNEXPECTED, because the mapping bug is untouched. That is the masking shape,
   and buying a truthful answer with an IAM grant is exactly the trade the never-widen rule exists to
   refuse.

**BRANCH 2 -- NO GRANT, TWO ROWS. TAKEN.**
**What it does:** leaves IAM exactly as signed at rtf-12, routes S105 (the address) and S106 (the
mapping) to `1.0.0_SA_CTO` with measured mechanisms and measurable disarm conditions.
**What it does NOT do, stated plainly so no half signs a cure it is not getting:** **the route still
answers UNEXPECTED after this packet.** Nothing is repaired today. The served plane is unchanged from
the rtf-12 post-apply state, which is the state both halves already signed.

---

## 4. CROSS-FIRM

**The template carries the firm segment:** `investor-reporting/export/{firm}/{export_id}/receipt.json`,
and `_load_receipt`'s own docstring binds it -- *"THE PREFIX IS BUILT FROM THE BOUND FIRM, NEVER FROM
THE REQUEST ... a caller holding another firm's export id reads a key that does not exist rather than
another firm's receipt."* The seat verified that in the source: `key = RECEIPT_KEY_TEMPLATE.format(
firm=tenant, ...)` where `tenant` is the resolved scope's firm, not an event field.

**The honest qualifier, because this packet signs a blast radius and not a hope:** `opal-data-ycharts`
is the **shared** evidence bucket for all three client firms, and the role is multi-tenant by design
(one function serves every firm). The existing evidence ARN is already firm-WILDCARDED
(`firms/*/generations/...`), so **on this bucket the per-firm fence is the KEY the code builds from
the bound principal, not the resource ARN** -- the same mechanism divergence S97 recorded for the
directory prefix. **That is a property of the WRITERS and of the runtime binding, not of IAM**, and a
grant signed under branch 1 would have inherited it. Under branch 2 nothing changes, so the
denominator of roles reaching any prefix of this bucket is unchanged at today's value.

---

## 5. ROLLBACK

**There is nothing to roll back: no change is applied.** The rollback the order specifies
(*revert + re-apply, verified by `implicitDeny` again*) is recorded here as the procedure that WOULD
apply had branch 1 been taken, and the verification instrument is already exercised and reproducible:
`simulate-principal-policy` on the concrete key, one resource per call, with the
`user/Andrew_Berman` positive control run as a SEPARATE invocation -- today it returns
**implicitDeny / allowed**, which is both the pre-state and the post-rollback expectation.

---

## 6. THE PLAN -- the export root

`.tools/terraform.exe -chdir=infra/aws/terraform/investor-reporting/export plan -input=false -no-color -lock=false`

```
No changes. Your infrastructure matches the configuration.
```

| | |
|---|---|
| resource_changes | **10** |
| actions | **no-op: 10** |
| **to destroy** | **0** |
| canonical digest (sha256 of resource_changes sorted by address) | `d9639bcb795496494f8d380a7d99e93c1997b69d6e49eef65f266ea1c0109fd5` |

**This digest is the packet's discriminator: it is the plan of a root with NOTHING proposed.** If a
later pass re-cuts this packet WITH a grant, this digest MUST change; if it has not changed, nothing
was added.

---

## 7. WHAT THE HALVES ARE SIGNING

1. **No IAM statement, resource ARN or condition is added, removed or modified.** The export root
   stays at `no-op` 10 of 10, 0 to destroy, digest `d9639bcb...`.
2. **The blast radius of this act is EMPTY**, because the act is the non-act. The served plane stays
   exactly as rtf-12 left it: the scope resolves on 8 of 8 counted requests; this route answers
   UNEXPECTED; S103 and S104's symptoms are unchanged.
3. **The two defects are routed, not fixed:** S105 (address undeclared, zero writers) and S106
   (error-class mapping serves an untrue answer), both to `1.0.0_SA_CTO`, both source changes barred
   by this order's bounds.
4. **The one thing a half should push back on:** if either half judges that branch 1's grant IS worth
   signing despite `layout.json` and the zero-writer census -- say so, and the seat re-cuts the packet
   with the ARN, a new plan and a new digest. **That is a re-signature, not an amendment.**

**Prepared by `0.7.0_AE_CloudOps~V`. NO APPLY WILL BE ATTEMPTED under this packet in either branch:
under branch 2 there is nothing to apply, and under a re-cut branch 1 the halves must be at HEAD
naming the new blob first.**
