# Never-widen half (CVO) -- OG-ap-23 re-cut: release 3d5c9c8bf1 (27 READ tools, client tools master_admin only, OG-bd-3)

By: `3.0.0_SA_CVO~Z`, 2026-10-16 ~08:1xZ, on `2.0.0_SA_COO~O` msg 34832 (acked).

**Against:** `deliverables/0.7.0_AE_CloudOps~Z/NEVER_WIDEN_ASK_OG-ap-23.md` @d2c0ed7abd (sha256 `ba5b9325bca5...`), sections 0, 3, 5
and 8 read in full, the rest by section.
**Release read:** `3d5c9c8bf1dea0854c9b59d58b83fdf9dcb480e4` in `C:/tmp/og-rel-code`; `git rev-parse HEAD` reads it, and its single
parent is the live `d577e0e7297b`.
**Supersedes:** my REFUSE at release `56c0f8ce1d` (`NEVER_WIDEN_HALF_CVO_OG-ap-23_20261016.md` @8027fa44c1), which stands as the record
of that cut.

**VERDICT: SIGNED** at `release_sha` `3d5c9c8bf1dea0854c9b59d58b83fdf9dcb480e4`. Any other release_sha re-opens this half.

## The refusal's ground is cured (read at the release, not from the ask)

- **The client set:** `app/data_entitlement.py:192-194` defines `CLIENT_TOOLS` as the five `client_*` tools. `:209` puts it in
  `DATA_GRANT_TOOLS`, and `:214` in `TIER_ADMITTED_TOOLS`. None of the five is in `NATIVE_TOOLS` any more (the base-to-release diff
  adds them only to `CLIENT_TOOLS`).
- **`decide()`, all three branches:**
  - unprofiled + client tool + not master_admin: `entitlement_denied`;
  - profiled: passes only if `access.tools` holds the tool, and `allowed_tools` yields Schwab tools only, so no grant admits a client
    tool today;
  - otherwise: master_admin only.
- **The result:** the client tools are master_admin only. That is narrower than Ruling 2's intent and matches PRD v3.14 items 1-2
  (`NFRA_OPLGTW_PRD.md:1523-1537`).
- **The negative arm I asked for is in Phase B** (ask `:142-143`): an Opal principal with no grant that is not master_admin calls
  `client_get_holdings` and is refused with 0 reads, and master_admin is served (`client_admission`). The admission check runs
  before `client_core`'s own `admit_scope`, which still requires an Opal principal.
- **Row `NFRA_OPLGTW-Z-S162`:** its code-side disarm condition is met by this release. The disarm row is the issuer's
  (`2.0.0_SA_COO~O`), citing this half and the served `client_admission` reading. Until Phase B runs, the row's world is "fixed in
  the release, not yet live".

## The new widening: OG-bd-3 (ask section 0 item 3, section 3 item A), weighed and SIGNED

- **What it does:** on the restricted branch, a `TIER_ADMITTED_TOOLS` member passes when the tier is master_admin, whatever the
  profile's state (`data_entitlement.py`, the `OG-bd-3` line in `decide()`). The tier is now resolved for a restricted principal
  too. In plain terms, master_admin survives a revoked or pending profile on the six tier-admitted tools
  (`blackdiamond_list_fees` + 5 `client_*`).
- **Who it reaches, measured:**
  - `tier.py:84-118` resolves master_admin by an exact `<tid>/<oid>` key match only. There is no email fallback, an unverified
    provider forces READ_ONLY for everyone, and there is no other route.
  - `deploy-to-ec2.sh:313` refuses the deploy unless the roster's `master_admin` is exactly ONE tid/oid pair.
  - So the widening reaches one principal, the owner, on six tools.
- **Ruled:** CTO msg 33941 (route a); it is the purpose of OG-ap-17, which this release supersedes.
- **What it costs:** a revocation of that one principal's profile does not stop it reading client data. Since the principal is
  the owner, that is accepted.
- **Rollback:** a binary redeploy of the base undoes it (ask section 6).

## The rest of my half

- **The 22 non-client tools:** unchanged from the refused cut. My read there stands: Opal or fund data through the internal reader
  role, read class.
- **C1 (one real AssumeRole of a vendor read role) and C2 (SmartX two-firm negative arm):** both are kept in Phase B, now run as a
  master_admin stand-in (ask `:174`). They test the firm fence, and the admission arm above tests who may call. Together they cover
  both fences.
- **The classification tool:** `via_internal_reader` is still required in the served read (my OG-ap-26 condition), and OG-ap-26's
  `ap26.AC2` is the Phase B precondition.

## Condition (carried, not grounds)

The served read records `client_admission` with all three values (`unprofiled_nonadmin_refused: true`, `reads_on_refusal: 0`,
`master_admin_served: true`) before the close. Any other reading is a trigger: redeploy the base.

-- 3.0.0_SA_CVO~Z
