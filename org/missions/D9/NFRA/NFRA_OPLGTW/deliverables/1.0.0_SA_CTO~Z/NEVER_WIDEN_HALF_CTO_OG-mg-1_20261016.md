# NEVER-WIDEN HALF -- CTO -- NFRA_OPLGTW.TO-OG-mg-1 (two grant writes: R1 Andrew's profile, R2 the Bloomberg mirror)

**Half:** `1.0.0_SA_CTO~Z`. **Verdict: R1 SIGNED; R2 SIGNED**, 2026-10-16 ~11:1xZ, at ask sha256 `757f5146afee` (re-hashed at signing),
re-issued at live release `3d5c9c8bf1`.
**Ask:** `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z/NEVER_WIDEN_ASK_OG-mg-1.md`, read whole (msg 34940).

## R1 -- Andrew's master-admin principal (pk `a18b74486b`): SIGNED

- **Before:** no profile and no grant.
- **The write:** profile revision 1 and grant revision 1, `restricted`, with the contract-maximal Schwab scope (2 masters,
  4 datasets, 4 operations, 13 months).
- **Who gains:** only the principal of the man who owns the data. OG-bd-3 (live) keeps his fee access by tier, so nothing is
  lost (`MG1_FEE_ACCESS.txt`, 11 of 11).

## R2 -- the Bloomberg concierge (pk `3c1d2597c9`): SIGNED

- **The grounding is Andrew's own word,** PRD v2.3 item 1 (2026-10-09, verbatim in
  `ANDREW_DIRECT_20261009_032xZ_OPAL_GATEWAY_BBG_MIRRORS_OPALGATEWAY.md`): "opal-gateway-bbg should be an exact copy of
  opal-gateway for now".
- **Scope:** equal to R1's, with zero differing keys.
- **Bound by item 4's Opal-users-only gate** (OG-tg-1, shipped in r30, ledger CLOSED), the coupling v2.3 requires.

## Both

- **Rollback:** `revoke`, which writes a tombstone; this role cannot DeleteItem.
- **Writer:** one module.
- **Contract:** the forbidden field classes bind every principal at the contract level.

## Finding carried, which signing does not fix

Section 3 measures that **Alyssa's live grant includes `download_filtered`**, and that no per-principal no-download restriction
exists anywhere in the store. PRD v2.3 "Unchanged" lists "Alyssa's grant and her no-download". So the PRD and the live store
disagree on a client-data permission of a real principal. It is routed to `2.0.0_SA_COO~O` as a surprise row, and told to
Andrew. Neither R1 nor R2 depends on it: they mirror Andrew, whose access is full.

## Note on AC3

Section 5 expects the BBGTerminal's 8 denied non-Schwab tools to read ALLOWED after these writes. A Schwab-family grant does not
obviously admit `opal_discover` or `ycharts_freshness`; the ask itself makes a denial a BLOCKING row. That AC is the CVO's to grade.
