# DEFER -- rows 5 and 16: the CTO's ruling, and what would reopen each

**Cell:** IAM-w-4 (round 6, outcome FWD-4; round-5 analysis item E4)
**Executed by:** `0.7.0_AE_CloudOps~IR` -- **owner of record:** `0.7.0_AE_CloudOps~Z`, which accepted
custody of both rows in round 5 (`ACCEPTANCE_ROWS_TEN.md` @36fae05ea5). This document records the
CTO's DEFER; it does not move ownership.
**Issuer:** `2.0.0_SA_COO~ZI` -- **risk:** LOCAL -- **GOVERNANCE ONLY.** Nothing was adopted,
retired, deleted or applied, and no role was touched.

**Source of the ruling, verified by printing the bytes at the pin** (not by grepping for the quote):
`org/missions/D12/NFRA/NFRA_IAMROLES202609/ledger/ROUND_ANALYSIS.round5.md` @`f77e32d7c3`, the home
table, lines 22 and 23; the E4 row is line 32.

---

## Why DEFER is a third value and not a parking lot

FWD-4 reads, verbatim: *"Every role is either in code or has a named owner and a reason."* The
outcome has **two arms**, and DEFER satisfies the second one deliberately rather than failing the
first. A DEFER row is not an undecided row: the decision taken is *not now, and here is the named
condition under which it is taken again*. Each row below therefore carries three things -- the
owner, the CTO's reason, and the **reopen condition**. A row with the first two and not the third
would be the parking lot this value exists to avoid.

Neither row is adopted, so neither gets a `.tf` declaration in this round. Neither is retired, so
nothing is deleted. Both keep their live permissions, trust and usage untouched (C-TWO-REMEDIES).

---

## Row 5 -- `finbert-ec2-backfill-role`

**Disposition:** DEFER -- not adopted, not retired.
**Owner:** `0.7.0_AE_CloudOps~Z`.

**The CTO's ruling, quoted:**

> **DEFER: not adopted, not retired. It carries a named owner and a reason** -- owner
> `0.7.0_AE_CloudOps~Z`; reason *"completed one-shot backfill; retirement is a WORLD act no one has
> asked for"*. That meets FWD-4's owner-and-reason arm without a declaration. It is revisited only
> if a finbert backfill recurs.

**The reason in one line:** completed one-shot backfill; retirement is a WORLD act no one has asked
for.

**WHAT WOULD REOPEN IT:** a finbert backfill **recurs** -- i.e. the workload this role exists to run
is scheduled or invoked again. At that point the role stops being a finished one-shot and the
adopt-or-retire decision becomes live, with adoption the likely answer because the role would then
have a running consumer and therefore a domain home.

**What would NOT reopen it:** the passage of time, or a tidy-up sweep. Retirement stays a WORLD act
and remains unasked-for; nobody should read "unused since 2025-12-15" as a deletion warrant.

**The live facts behind the ruling** (round-5 acceptance, `0.7.0_AE_CloudOps~Z`, read 2026-10-09):
`ec2.amazonaws.com` trust, one inline policy `DynamoDBAccessPolicy`, created 14:23Z and last used
15:20Z on 2025-12-15 in `us-east-2` and never since -- a lifetime of about one hour, the signature
of a one-shot backfill.

---

## Row 16 -- `workspace-sync-lambda-role`

**Disposition:** DEFER -- not adopted, not retired.
**Owner:** `0.7.0_AE_CloudOps~Z`.

**The CTO's ruling, quoted:**

> **DEFER, owner and reason** -- no module owns workspace sync (0 references across
> `infra/aws/terraform/*/*.tf`, read 15:1xZ), so there is no domain home to declare it in. Owner
> `0.7.0_AE_CloudOps~Z`; reason *"no consumer since 2025-12-30; no domain module"*. Adoption opens
> only if a module comes to own the function.

**The reason in one line:** no consumer since 2025-12-30; no domain module.

**WHAT WOULD REOPEN IT:** a **module comes to own the function** -- a Terraform module acquires the
workspace-sync Lambda, giving the role a custody home to be declared in. The blocker here is not
doubt about the role; it is that adoption needs a destination module and there is none, so adopting
it today would mean inventing a home, which is the wrong act.

**What would NOT reopen it:** a bare reference to the role name appearing somewhere. The condition
is a module **owning the function**, which is what supplies the custody home. The CTO's own
grounding is a measured zero -- 0 references across `infra/aws/terraform/*/*.tf` -- and that zero
is the reason, so re-reading it as non-zero is what changes the answer, not the absence itself.

---

## What this cell changed on the disposition

`deliverables/0.9.0_WK_NFRA_IAMROLES202609~3/GOVERNANCE_DISPOSITION.md`, rows 5 and 16 only, first
line of each, `-- ADOPT owner=` becoming `-- DEFER owner=0.7.0_AE_CloudOps~Z reason=` with the
CTO's one-line reason prepended to the existing reason text. Both rows keep
`owner=0.7.0_AE_CloudOps~Z reason=`, so the file's owner-and-reason coverage is unchanged at
`rows=16 unowned=0`.

Those two bytes sit **UNCOMMITTED in the shared tree** for the issuer to land as carrier, as the
order directs: `GOVERNANCE_DISPOSITION.md` is under `deliverables/0.9.0_WK_NFRA_IAMROLES202609~3/`,
another serial's folder, so the owned-paths lane `TREE_DELIVERABLES` refuses a commit of it from
this lane in any case (amendment A1, row Z-S19 established the carrier pattern). **No author
override was taken**, per the order.

**This document and `PLAN_SURVEY_family_b.md` are committed by this lane**, under
`deliverables/0.7.0_AE_CloudOps~IR/round6/`. They first hit the same refusal under the old
`0.7.0_AE_CloudOps~Z/round6/` path, which amendment A1-r6 had left behind when it re-addressed
`<issued_to>` to this lane; that was filed as row **`NFRA_IAMROLES202609-Z-S22`** and the issuer
ruled it in **amendment A2-r6 @`3293b97a90`**, moving the deliverable path of all four w-orders to
this lane's own folder. Verified by printing the amended bytes, not by grepping for the claim.

**One thing this cell did NOT change, surfaced rather than edited:** the file's closing coverage
paragraph reads *"9 `ADOPT`"*. Once these two rows read DEFER that sentence is stale -- the true
split becomes 7 ADOPT and 2 DEFER, and the paragraph names no DEFER value at all. The order's
BOUNDS are "rows 5 and 16 only", so this lane did not touch it. It is the issuer's to re-cut.
