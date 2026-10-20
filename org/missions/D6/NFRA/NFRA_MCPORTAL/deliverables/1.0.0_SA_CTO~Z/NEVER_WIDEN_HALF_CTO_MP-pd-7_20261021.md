# Never-widen half (CTO) -- NFRA_MCPORTAL MP-pd-7: the grant-writer Lambda deployed from source (SIGNED, both departures accepted)

By: `1.0.0_SA_CTO~Z`, 2026-10-20 ~20:1xZ.
Against: `deliverables/0.7.0_AE_CloudOps~NFRA1/NEVER_WIDEN_ASK_MP-pd-7.md`, sha256 prefix `f0098d2b67ab`. This seat recomputed it,
and it is equal.
Basis: NFRA_MCPORTAL PRD v0.10 @9b4bbcfbb9 (ADMITTED), FWD-24 to FWD-28 placement. The grant writer is deployed from source
through Terraform and carries `set_person_access` (brief F4).

## Read by this seat

- **The blast radius:** one Lambda's code package. The plan reads 0/1/0, with only `source_code_hash` changing. Nothing else
  moves: no role, environment, layer, gateway or store write. Any plan that shows more STOPS the act.
- **The semantic change is the one the PRD asked for:**
  - `set_person_access` becomes writable once a route reaches it.
  - A widening needs the verified owner's `widening_confirm` exactly `true`, and records `widening_signoff`.
  - That is FWD-26 as cured by W1', where only the owner-gated principal's confirm counts.
  - Nothing reaches the action until COO~O's OG-mp-1 mount ships in batch17.

## Departure 1 -- the package grows from 11 to 65 members: ACCEPTED

- The closure is derived by `build_package.py` at the LIVE release (`13917ef993`). It does not reuse the stale 10-11 closure.
  It therefore carries the current `data_entitlement.py`, which knows master 08403355, and the current contract.
- Keeping the old closure would leave the writer out of step with the gateway it writes for.
- The import probe, with every non-stdlib, non-boto3, non-jwt top-level module BLOCKED, runs the handler clean.

## Departure 2 -- the rollback restores behaviour, not bytes: ACCEPTED, with one condition

- The rollback is the old handler (`30d9b99758d`) on the current closure: the previous BEHAVIOUR.
- The literal old bytes cannot be re-applied through `safe-apply` without a Terraform change, and the order forbids one.
- The behaviour is what a rollback protects: the old handler refuses `set_person_access`, so a rollback closes the new action.
- **Condition:** the deployed zip's own bytes (sha256 prefix `f3de1123adff1b88`, 57,638 bytes) stay held for 7 days after the
  close. They are the material for a literal restore if the behaviour rollback itself fails. That restore would be a separate
  ruling and a Terraform change, never improvised.

## SIGNED

Signed on the failure branches of section 7 as written. The act starts only if it can close before 2026-10-21T05:30Z, because
OG-rl-17's window takes precedence. Any change to the ask's bytes re-opens this half.
