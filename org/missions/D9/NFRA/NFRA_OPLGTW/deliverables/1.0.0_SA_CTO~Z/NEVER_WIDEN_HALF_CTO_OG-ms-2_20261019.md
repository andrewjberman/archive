# Never-widen half (CTO) -- OG-ms-2: Alyssa gains Schwab master 08403355 (Tax SMA) at its full current accounts (SIGNED)

By: `1.0.0_SA_CTO~Z`, 2026-10-19 ~21:3xZ.
Against: `deliverables/0.7.0_AE_CloudOps~NFRA1/NEVER_WIDEN_ASK_OG-ms-2.md`, sha256 prefix `30351bdddf2d`. This seat recomputed it,
and it is equal.
COO half: `deliverables/2.0.0_SA_COO~O/NEVER_WIDEN_HALF_COO_OG-ms-2_20261019.md` (msg 36131).
Basis:
- Andrew-direct ~19:55Z: "she needs the 0840 master too added to her entitlements" (laptop @3c6ce94b4f);
- his ~17:2xZ "Schwab should automatically cover the full accounts" (@65a05f6658).

## Read by this seat

- **The widening, stated plainly:** ONE principal (Alyssa) gains ONE master, 08403355, at its 30 current accounts. Those are the
  distinct `dim_balance` accounts at 2026-10-16, the latest complete marker, which is T-1 for Monday 10-19.
  - `changed_keys` reads `["accounts", "masters"]` and nothing else.
  - Her two existing masters are unchanged (7,599 and 7,690 accounts).
  - The datasets, columns and the 13-month window are the same.
  - The operations exclude download.
  - Andrew's grant is untouched.
- **08403355 is the only 0840 prefix** under `schwab/` (Phase A, read). All four datasets have data at 2026-10-16.

## The sequencing risk, and why the COO's conditions cover it

The LIVE gateway (`6d1b5dcb64`) rejects a grant that names 08403355 as Malformed. Activating this grant before `OG-rz-2`'s
release would therefore deny ALL of her Schwab access. The COO half's conditions close that risk, and this half binds them:
- **J2:** Phase B runs only after ledger `batch15` reads CLOSED;
- **J4:** the read-back `decide()` runs against the DEPLOYED tree;
- **J5:** a `batch15` rollback reverts this grant FIRST.

## SIGNED

Signed on J2, J4 and J5 as written. Any change to the ask's bytes re-opens this half.
