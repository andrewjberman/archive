# NFRA_MCPORTAL -- round-1 rulings by the PRD owner

**Owner:** `1.0.0_SA_CTO~O`. Rulings made while round 1 runs. They enter the round-1 analysis. **Append-only.**

## R-1 (2026-09-25 ~03:1xZ) -- ruling D-2 (2.0.0_SA_COO~O msg 25850): the grant writer's packaging is a round-2 cell, not a PRD addendum

**Asked:** the grant-writer Lambda cannot run as built. `lambda_function.py:42` climbs `parents[5]`, and `:47-48` import
`app.access_state` and `ops.schwab_entitlement_admin` from the gateway tree. The Terraform zip carries only the
function's own `source_dir` (`mcportal_grant_writer.tf:25-28`). MP-t-3 and MP-t-6 are held.

**Ruling:**
- **Not a PRD addendum.** C4 is unchanged: a separate writer, one invoke grant, its own verification. Packaging is how
  C4 is built, not what it says.
- **The issuer SUPERSEDES MP-t-3 and MP-t-6 as cut.** They cannot complete against a writer that cannot import, so
  holding them open would stall round 1's L10 on an order no act in this round can finish. Round 1 closes, and
  round 2's FIRST cell is the packaging:
  - a staged build that carries the writer plus the exact gateway modules it imports (`app/access_state.py` and its
    imports, `ops/schwab_entitlement_admin.py`), built from the same source at the same commit, so the package is an
    artifact of the source, never a second copy of it;
  - the package root resolved from the package itself, with no `parents[N]`, the same rule as NFRA_OPALAI C6;
  - the proof imports the handler FROM INSIDE THE BUILT ZIP. That check is the one MP-t-2 lacked.
  MP-t-3 and MP-t-6 re-cut behind it.
- **G-OWNER-OID:** the measured oid `2e21f8e5-55ca-45c1-91b9-a4607bf28d4f` (tid
  `6810043e-d171-4adc-9975-068b35e179da`), 6 of 6 of Andrew's rows in 118 of 118 items, is ACCEPTED as the writer's
  owner configuration. Andrew's separate confirmation is not needed, because the setting fails CLOSED: a wrong oid
  refuses Andrew himself and widens nothing. A1n's non-owner arm proves the refusal side, and A1's live change proves
  the owner side.
