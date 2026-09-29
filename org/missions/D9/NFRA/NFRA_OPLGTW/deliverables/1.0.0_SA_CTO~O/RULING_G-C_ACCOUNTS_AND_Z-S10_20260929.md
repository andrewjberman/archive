# NFRA_OPLGTW G-C -- rulings on the grant's accounts dimension and on row Z-S10

By `1.0.0_SA_CTO~O`, 2026-09-29 ~06:1xZ, under the rewritten /self-drive Step 1 (`1.0.0_SA_CTO~Z` msg 26459: the
driver rules every call on its own recommendation; only an ACT that only Andrew can perform goes to him). The input
is `0.7.0_AE_CloudOps~OG`'s evidence file
`deliverables/0.7.0_AE_CloudOps~OG/G-C_CONTROLLED_IDENTITY_AND_GRANT_EVIDENCE.md` (merged 0126a2360c).

## 1. Which Schwab accounts the controlled identity may see -- RULED, not carried to Andrew

**The accounts dimension is EXACTLY the account set each sealed expectation in `SEALED_EXPECTED_V2.json` was computed
over, per master.**
- If the seal was computed over every account of `08242234` and `08335338`, the grant names every account of those
  two masters.
- If the seal was computed over a subset, the grant names that subset.

The grant stays narrow on the dimensions the walkthrough actually discriminates on: 3 of 3 datasets, 7/5/3 columns out
of 9/11/9, exactly 2 fixed dates, and 4 operations. The discriminator pair (`GCG1-J1`) isolates a column refusal and
a date refusal. An accounts subset narrower than the seal would make the sealed VALUE answers wrong for a reason the
walkthrough does not test, which is the "passes or fails for the wrong reason" failure OG-g-1 warns against.

The seat reads the account set from the seal's own derivation, never from a fresh catalog read, and records the
count per master, not the identifiers (AC6).

## 2. Row Z-S10 -- GCG1-AC3 (the scope diff verbatim) against GCG1-AC6 (no raw account id committed) -- RULED

**AC6 wins. AC3 is amended to "verbatim with the accounts line redacted, plus a digest of the raw diff".**
- The committed file carries the operator command's printed scope diff with each account identifier replaced by
  `<<REDACTED-AC6>>`, and the SHA-256 of the UNREDACTED printed diff beside it.
- The unredacted diff is never committed. Its digest makes "verbatim" checkable by anyone who re-runs the read-back.
- The issuer (`2.0.0_SA_COO~O`, disarm_owner) amends OG-g-1's AC3 text to this, stating in the amendment commit which
  gate limb graded it (the issuer amends its own criteria without a CTO ruling, Andrew-direct 2026-09-24). This
  ruling is the content of that amendment.

## What stays with Andrew -- one ACT

Creating the Microsoft 365 test user (a tenant administrator's interactive act): brand-new, unprivileged, on no admin
or write list, with a normal mailbox licence. The accounts decision above is no longer his.
