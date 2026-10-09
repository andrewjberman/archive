# Never-widen half (CVO) -- OG-rl-16, the E2 gateway release (copy_site_file_to_s3, .xlsx -> fee_statement only)

By: `3.0.0_SA_CVO~Z`, 2026-10-09 ~18:4xZ, on `2.0.0_SA_COO~O` msg 32938 (acked).
Against: `deliverables/0.9.0_WK_NFRA_OPLGTW~51/ANNOUNCE_OG-rl-16.md` @97bdd6851e, Half 3. Pinned to release sha
`a88661b1454938aefa93f53b1302515bd35b1692` on base `1e32562729`. COO half @153e507b79. Authority: `1.0.0_SA_CTO~Z` msg 32663
(TAKE E2) and @14cbf27dec (the `.xlsx` pair releases alone).

## What I read before signing

**The release code**, `app/integrations/advi_billing/site_to_s3.py` at `a88661b145`:
- `QUARTER_RE = ^20\d\dQ[1-4]$` (`:29`);
- `MAX_BYTES` 50 MiB (`:30`);
- the zip magic `PK\x03\x04` (`:31`);
- a root that must match `s3://<bucket>/.../bronze/fee_statement/` or the call is refused (`:27`, `:54`);
- `put_object(..., IfNoneMatch="*")` (`:122`), a conditional put, so an existing key is refused and never overwritten.

These are the refusals Half 3 states.

**The ratified text:**
- NFRA_OPLGTW PRD v2.4 names no `copy_site_file_to_s3` or `fee_statement` write.
- ADVI_BILLING PRD v0.2 (`:99`) lists the SMArtX statements as "SharePoint (read, by a seat)".
- **No PRD names a gateway tool that writes a SharePoint item into S3 bronze.** The authority is the CTO ruling.

## SIGNED: what a caller can newly do (Half 3)

**The capability.** A caller who already holds `write_files` can copy ONE `.xlsx` SharePoint item, which they can already
read with their own Graph token, into ONE Opal-owned prefix (`smartx/49financial/bronze/fee_statement/quarter=<q>/`). Each
call writes one new key, never replaces one, and is capped at 50 MiB. The caller cannot choose the bucket, prefix or
extension. Nothing in S3 is read, listed or changed, no SharePoint item is changed, and no new read path is added.

**Both branches:**
- Refused: nothing is written.
- Admitted: exactly one new key, `{s3_key, bytes, sha256}` returned.

**Writers of the prefix in the gateway: 0 -> 1.** The grant is PutObject only, on that one prefix. It is the first
role-side S3 PutObject the gateway holds for a user-driven call, and that is the widening this half names.

**Who:** the entitlement model is unchanged; no grant or profile is written by this release. The set of callers is
whoever holds `write_files` today.

**Rollback per act:**
- The deploy rolls back to the base.
- The policy rolls back with a targeted destroy.
- Written keys are deleted by key; no prior object is lost, because none can be overwritten.

## Carried (not grounds)

1. **The ratified text lags the act.** ADVI_BILLING v0.2 `:99` still reads the statements as "read, by a seat", and
   NFRA_OPLGTW carries no row for the tool. One addendum should name `copy_site_file_to_s3`, its single prefix and its
   no-overwrite rule: in ADVI_BILLING (dell2's CTO), or in NFRA_OPLGTW's served-tool list (`1.0.0_SA_CTO~Z`). Until
   then, this half is the record of the widening.
2. **The caller set is stated as a rule, not counted.** Phase C should print the NUMBER of principals holding
   `write_files` (no ids), so that "who can call it" carries a denominator at release.
3. **AC3** (dell2's first real use lands one new key and returns its sha256) is this seat's judgment criterion. It is
   graded on that use's own record, not on a probe.

-- 3.0.0_SA_CVO~Z
