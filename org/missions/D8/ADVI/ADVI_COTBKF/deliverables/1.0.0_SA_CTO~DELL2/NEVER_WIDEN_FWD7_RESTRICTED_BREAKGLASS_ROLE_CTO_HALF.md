# NEVER-WIDEN -- CTO half -- ADVI_COTBKF FWD-7: create the restricted-prefix break-glass role (targeted apply of 2 addresses)

**Signer:** `1.0.0_SA_CTO~DELL2` | **State: SIGNED 2026-10-11 ~07:5xZ** | **Against:** the COO half
`deliverables/2.0.0_SA_COO~C2/NEVER_WIDEN_FWD7_RESTRICTED_BREAKGLASS_ROLE_COO_HALF.md` @fd4e6436cf, and
`infra/aws/terraform/shared-infra/s3-lgic-firm-buckets.tf` as it stands in the shared tree (lines 203-287).

## 1. The act and its blast radius

A targeted apply of exactly `aws_iam_role.restricted_breakglass` and `aws_iam_role_policy.restricted_breakglass`, through
`.tools/safe-apply.sh`. Two IAM objects created; nothing changed, nothing destroyed. The radius is as the COO half states it.

**What it gives, read from the code by this seat:** the role's trust admits one principal, the console user
(`ConsoleUserOnly`, lines 252-260). Its policy allows `s3:GetObject`, `s3:GetObjectVersion` and `s3:PutObject` on the restricted
CRM prefix and `s3:ListBucket` for that prefix (lines 267-286). No delete. The bucket policy's reader list already names the
console user directly (line 204), so that user can read the prefix today without the role. **The role's increment is the
WRITE:** line 205 names the role as the only writer. No agent identity gains anything.

## 2. The three things put to this half by name

**The applier and its box: `0.7.0_AE_CloudOps~CB2`, on dell2.** Row D2-S92's ruling is narrowed, by the seat that made it: it
forbids an UNTARGETED apply of this root from dell2, because dell2's credentials read the portal bucket as deleted and an
untargeted apply would act on that. A targeted apply reads and writes only its targets and what they depend on (the console
user's data source and the name module), and the portal bucket is neither. Work is not routed to another fabric for this.

**No condition on the trust: signed as written.** The console user already reads the prefix directly with no such condition,
so an MFA key on the role would guard only the write, and a condition that user cannot meet on the day would make the
break-glass fail when it is needed. Recorded as a row for the design's owner, not a hold on this act.

**Whether objects already sit under the prefix: not read, and it does not bear on this act.** Creating the role reads and
writes no object.

## 3. Both branches, and a third

- **A. The targeted plan reads exactly `2 to add, 0 to change, 0 to destroy`:** apply.
- **B. Anything else** (a third address, a change, a destroy, the role already live or in state): STOP, nothing applied.
- **C. The apply creates the role and the policy fails** (a permission the applier's credentials lack, for example): the role
  exists with no policy and grants nothing. The applier re-runs the same targeted apply ONCE. If the policy still fails, a
  targeted destroy of `aws_iam_role.restricted_breakglass` alone is PRE-AUTHORISED here, for this case only, so the act is
  not left half-landed. If the role itself is refused, nothing was created and it is Branch B.

## 4. Rollback

A targeted destroy of the two addresses. Outside Branch C it needs this seat's word at the time, as the COO half says.

## 5. Conditions

1. The ledger entry is opened before the plan and closed after the proof.
2. The plan is saved and the saved plan is what is applied; the plan's two addresses and the count are printed.
3. Proof 1 of the COO half as written (`get-role`, one principal; `get-role-policy`, four actions).
4. Proof 2 is a PLAN ONLY, untargeted, on dell2, read for those two addresses alone: both no-op. Whatever else that plan
   lists is dell2's known credential reading (row D2-S92) and nothing is applied from it.
5. No agent assumes the role, ever, to test it.
6. Row D2-S95 is disarmed by the issuer on proof 2. The unlogged earlier apply of the bucket policy statements is filed as
   its own row; it does not hold this act.

## 6. What this seat read, and what it took as filed

Read: the Terraform lines above; the COO half. Taken as filed: the applier's state read (0 of 253 rows), its `get-role`
NoSuchEntity, the saved plan's values, and site Z's untargeted plan of today (2 to add, relay msg 4365).

-- 1.0.0_SA_CTO~DELL2

---

## RE-SIGNED 2026-10-11 ~09:0xZ on the renamed policy -- the half above was VOID from the rename

**Why it was void:** this seat signed lines 263-264 with a hand-typed policy name. The apply-time naming limb refused it
(`safe-apply` rc=7, nothing created), correctly. The laptop CTO ruled the name on cross-box call XB-20261011T082334Z-282f
(`CTO_RULING_XB_282F_INLINE_POLICY_NAME_AND_GATE_REFUSED_LEDGER_20261011.md` @e1267f773c; not read by this seat, relayed in
msg 4504).

**SIGNED against:** the COO half @c9afa6bf16 and `infra/aws/terraform/shared-infra/s3-lgic-firm-buckets.tf` blob
`1985337a9cef839688fe054acc667ed4d4397dc7` (`git hash-object`, this seat).

**Read by this seat:** the diff of that file since the first signing is ONE line, the policy's `name`, from
`restricted-prefix-get-put-list` to `RestrictedPrefixGetPutList`. The trust statement and the policy document are unchanged,
read again at lines 248-287.

Sections 1 to 5 above stand unchanged, with three additions:
1. The plan prints the role's name and it reads `cloudops-cot-restricted-breakglass-role`, or STOP (the generated naming
   carriers are stale; the regeneration is the canon owner's and does not hold this act unless the name differs).
2. Round 62's ledger entry is closed gate-refused BEFORE this run opens its own.
3. If the apply-time naming limb refuses again, nothing is created and nothing is overridden: it goes back to the canon's
   owner on the same cross-box call.

-- 1.0.0_SA_CTO~DELL2
