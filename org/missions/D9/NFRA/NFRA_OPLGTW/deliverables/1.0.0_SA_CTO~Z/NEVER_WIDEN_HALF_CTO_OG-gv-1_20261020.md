# Never-widen half (CTO) -- OG-gv-1: Andrew's Schwab grant moves to the master-wide scope (SIGNED, email_deny handling: option 2)

By: `1.0.0_SA_CTO~Z`, 2026-10-20 ~13:4xZ.
Against: `deliverables/0.7.0_AE_CloudOps~NFRA1/NEVER_WIDEN_ASK_OG-gv-1.md`, sha256 prefix `637db69736ab`. This seat recomputed it,
and it is equal.
COO half: `deliverables/2.0.0_SA_COO~O/NEVER_WIDEN_HALF_COO_OG-gv-1_20261020.md` @9adb63850e.
Basis: Andrew-direct ~17:2xZ 10-19, "Schwab should automatically cover the full accounts ... there shouldnt be a persisted list"
(@65a05f6658); CTO round-46 analysis, rank 6.

## Read by this seat

- **The widening:** one principal (the owner) moves from stored account lists (7,477 and 7,559) to `["*"]` on the same two
  masters, resolved at read time by OG-rt-1's code.
  - `changed_keys` reads `['accounts']`.
  - No master, dataset, operation, column or date window is added.
  - The download operation is unchanged.
  - This is exactly his word.
- **The release order:** OG-rl-18 must be CLOSED and live first. An older gateway reads `["*"]` as Malformed and denies all of
  his Schwab access. A batch17 rollback reverts this grant first. Both are bound as section 3 and section 6 write them.

## The email_deny handling: OPTION 2

Option 2: a master-admin exemption on the legacy `/callback` consent branch, in its own small release, BEFORE the activation.

- **Why not option 1 (accept the 403).** `/callback` is `token_broker.redeem_consent`, the owner's consent sign-in. Accepting a
  403 there puts a lockout of the owner on a path whose next use this seat cannot predict, for example a re-consent after a
  token lapse.
  - The browser routes already exempt a master admin before the store is read (OG-en-14).
  - The same exemption on `/callback` makes the two e-mail paths consistent, and costs one guarded check.
- **Why not option 3.** It leaves his stored list in place, against his word.
- **Why not option 4.** It changes the shared operator tool for every future grant, which is a wider change than this needs.

**Conditions for the exemption release:**
- It exempts the master-admin tier only.
- A non-admin principal with a deny record still answers 403 on `/callback`, proved by a test.
- It ships under its own never-widen ask. It may ride OG-rl-18 if that release is not yet cut; otherwise it goes alone,
  before this activation.
- Phase B of OG-gv-1 runs only when both are live.

## SIGNED

Signed with option 2 and the release-order conditions above. Any change to the ask's bytes re-opens this half.
