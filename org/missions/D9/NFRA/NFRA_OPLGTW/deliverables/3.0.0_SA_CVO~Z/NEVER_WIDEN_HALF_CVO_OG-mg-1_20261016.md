# Never-widen half (CVO) -- OG-mg-1: R1 (Andrew's profile) and R2 (the Bloomberg mirror)

By: `3.0.0_SA_CVO~Z`, 2026-10-16 ~11:2xZ, on `2.0.0_SA_COO~O` msg 34941 (acked).

**Against:** `deliverables/0.7.0_AE_CloudOps~Z/NEVER_WIDEN_ASK_OG-mg-1.md` @a8798df9d0 (sha256 `757f5146afee...`), read whole,
re-issued at the live release `3d5c9c8bf1`.

**R1: SIGNED. R2: SIGNED.** Each is bound to ask sha `757f5146afee`, and any other ask hash re-opens both.

## What I read

- **Before state:** the ask's re-read, 1714 items, 17 POLICY# partitions, 4 `principal_profile` and 4 `data_entitlement`.
  - Exactly one active profile exists (Alyssa's), so R1 and R2 each read NONE.
  - This seat's own scan at ~04:5xZ today agrees independently: 17 POLICY items, and exactly ONE `POLICY#<tid>#<oid>`
    principal holds a profile or a grant. The other three profile keys are og-i1 probes (`NFRA_OPLGTW-Z-S160`).
  - Neither Andrew's nor the concierge's principal holds a profile today.
- **Width:**
  - Contract-maximal: 2 masters, 4 `dim_*` datasets, 4 operations, a 13-month rolling window.
  - R2's scope equals R1's with zero differing keys.
  - The contract's `forbidden_field_classes` (raw account id, account title, tax id, mailing address, hidden operands) bind
    both through `validate_candidate`. `prepare()` accepted both.
- **Fee access:** the master_admin tier carries it through a profile (OG-bd-3, live, which I read at its `decide()` line in
  my OG-ap-23 re-cut half). So R1 removes nothing from Andrew.
- **Writer:** one module (`ops/schwab_entitlement_admin.py`). The rollback is `revoke`, a tombstone; the role has no
  DeleteItem.

## The blast radius, stated as signed

- **R1:** Andrew's own principal gains the Schwab data-grant family at full contract width. The owner reads his firms' Schwab
  data, and nothing else changes.
- **R2, read plainly:**
  - The `opalbloomberg` concierge principal gains the same Schwab family, including `download_filtered`.
  - The concierge answers Teams requests from any `@opalinvest.com` user, and since v2.3 it is unscoped.
  - So after R2, **any Opal user who asks the concierge on Teams can have Schwab client account data read for them**,
    without a data grant of their own.
  - That stands in tension with v3.1 Ruling 2's principle ("being an Opal user is not enough for client data").
  - **I sign it because Andrew's own words cover it exactly.** v2.3, Andrew-direct 2026-10-09: "opal-gateway-bbg should be
    an exact copy of opal-gateway for now ... eventually we will make rules but not yet". v2.3 item 1 adds "every account in
    every served source", with the Opal-users-only gate as its condition (item 4, shipped in r30).
  - I do not narrow his word. The tension is carried to the CTO as a decision for the "rules" he deferred, not as a refusal.
- **Rollback per record:** `revoke`, which leaves "revoked at revision 1" in the store, not an absence. Signed knowingly.

## Conditions (carried, not grounds)

1. **The R2 read-back includes the gate.** The Opal-users-only gate's A32 arms (an external sender absent from the poll; a send
   into a mixed chat refused) must still hold on the live release `3d5c9c8bf1` at the act. R2 is safe only behind that gate.
2. **AC3 of OG-ap-14** stays the BBGTerminal seat's own 8-tool re-exercise after these writes. Graded by this seat on its record.

## Off this ask (filed as its own row): a ratified no-download with no carrier

PRD v2.2 item 4 keeps "Alyssa's no-download" (Andrew ~19:2xZ: "no downloads needed yet"), and v2.3's Unchanged list
repeats it. The ask's section 3 measured that her live grant's `operations` holds `download_filtered`, and that no
profile, grant or contract field carries a no-download. The ratified rule is therefore not enforced. That is filed as
`NFRA_OPLGTW-Z-S173` for the CTO to rule (enforce it, or record that Andrew's "not needed yet" was never a prohibition). It
does not bear on R1 or R2, which mirror Andrew, not Alyssa's restriction.

-- 3.0.0_SA_CVO~Z
