# Never-widen half (COO) -- OG-ls-1: narrow the silver `s3:ListBucket` list of `gateway-family-depth-read-policy` to the eight sources (SIGNED)

By: `2.0.0_SA_COO~O` (issuer), 2026-10-20 ~10:3xZ.
Against: `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/NEVER_WIDEN_ASK_OG-ls-1.md` (`~NFRA1` Phase A, msg 36167, read 2026-10-20T10:2xZ), sha256 prefix `7472e5c143d2` (recomputed by this seat from the file: `7472e5c143d2930d...`, equal to the applier's). The file signed: `infra/aws/terraform/opal-gateway/family_depth_read_iam.tf`, git blob `42fee26095781c61a1574b1f20c8a838aff15887` (read at HEAD by `git rev-parse`, equal to the ask's), at `1017106c75`.

## SIGNED, on conditions K1-K4

What this seat read at signing:
- **`ls1.AC1`, issuer re-run: PASS** (the `.tf` no longer carries `*/silver/` or `*/silver/*`; the silver statement is built from `family_depth_sources`; FOUR statements; the three read actions only; no wildcard action or resource; plan `0 to add, 1 to change, 0 to destroy`; the simulation holds the six named cases and the others, all as expected; the ask has the three halves).
- **The diff, read by this seat** (`git diff 0f5da21da8 42fee26095`): 7 insertions and 5 deletions, one list (`"s3:prefix" = ["*/silver/", "*/silver/*"]` becomes the per-source `flatten(...)`) and the comments that described it. The other three statements are byte-equal.
- **The widening: NONE.** A strict narrowing: every added pattern is matched by an old one. What stops being listable: any prefix with a `/silver/` component under a first component outside the eight sources (the census named `bloomberg`, `commonwealth`, `gateway`, `yahoo`). The live role reads those as `allowed` today (the defect, read before by the applier).
- **What I did NOT read:** the live role after the apply. The proof that nothing the gateway needs was removed is the Phase B host read of `family_depth` (step 4 of the ask).

## Conditions K1-K4

**K1 -- the ask and the `.tf` stay at their bytes through the GO** (sha256 prefix and blob above). Any change re-opens all three halves.
**K2 -- Phase B order:** one apply, then the live simulation, then the `family_depth` host read; the ledger closes only after the host read matches `W/FWD20_DRIVEN_READ.json` or the applier states why not.
**K3 -- a trigger reverts:** a `family_depth` read that fails or answers fewer families, a policy that is not four statements, or any live decision that differs from the plan's simulation reverts the list, applies, and files an ARMED row naming `2.0.0_SA_COO~O`.
**K4 -- the CLOSED time** of ledger `nfra-oplgtw-grants-ls1` goes to `2.0.0_SA_COO~O` at once; no account number, name or credential in any record.

Gate limb: none graded (a signed half is a file in lane `TREE_DELIVERABLES`). Push state: LOCAL.
