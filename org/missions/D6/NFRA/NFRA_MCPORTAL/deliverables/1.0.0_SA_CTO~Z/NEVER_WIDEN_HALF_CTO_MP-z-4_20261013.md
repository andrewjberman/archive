# CTO half -- NFRA_MCPORTAL MP-z-4: one `dynamodb:Scan` on `gateway-access-state-table` for `opal-gateway-role`

**Signer:** `1.0.0_SA_CTO~Z`, 2026-10-13 ~13:5xZ. **Ask:** `0.7.0_AE_CloudOps~MQ` msg 33631;
`org/missions/D6/NFRA/NFRA_MCPORTAL/deliverables/0.7.0_AE_CloudOps~MQ/NEVER_WIDEN_ASK_MP-z-4.md` @a667941f52 (read whole
with `git show`). **Serves:** PRD v0.7 FWD-20, the gateway breakdown's "current state of entitlements", which Andrew made
MCPORTAL's first outcome (record `ANDREW_DIRECT_20261012_205xZ_SITEZ_PORTFOLIO_SEVEN_PROJECT_RULINGS.md`, item 2).

## VERDICT: SIGNED, for exactly the ask's section 6 sentence

> `opal-gateway-role` may LIST `gateway-access-state-table` -- one `dynamodb:Scan`, unprojected and unconditioned, on that
> one table ARN. It may not write it, delete from it, reach any other table, or reach any index.

This IS a widening, and the ask names it as one. It is a LIST delta over a table the role already READS item by item, and
this seat signs it because Andrew's FWD-20 needs that list.

## Read by this seat, live

| read | result |
|---|---|
| `opal-gateway-role` inline `opal-gateway-access-state-runtime` | `AccessStateStrongRead`: `dynamodb:GetItem` on `table/gateway-access-state-table`, **no Condition**. So every item is already readable by key, as the ask states (section 1.2). `AccessStateRuntimeWritesRuntimeKeysOnly`: Put, Update and Delete under `LeadingKeys RUNTIME#*`. Both are untouched by this act |
| `describe-table gateway-access-state-table` | **0 GSI, 0 LSI.** The statement names no index ARN, and none exists to be reached |
| the planned document (ask section 2.2) | one statement, one action (`dynamodb:Scan`), one resource (the table ARN); no Condition, NotAction or NotResource. Plan `1 to add, 0 to change, 0 to destroy`, under `-target` and a saved plan |

## Both branches

- **Applied (A):** AC1 shows the exact document, and the 4 isolated simulate arms read: Scan on this table allowed;
  Scan on `mcportal-grant-changes-table` allowed (the pre-existing control); Scan on `opal-users-v2` implicitDeny;
  GetItem on this table allowed. The refused arm is read together with the allowed ones.
- **Fails mid-act (B):** a single `delete-role-policy` on `gateway-access-state-principal-scan-policy`. The act writes
  no data, so nothing is lost.

## Conditions

- **CTO-1:** the grant lives in its own file and its own policy name, never folded into
  `opal-gateway-access-state-runtime`, so the rollback stays a single call.
- **CTO-2:** a future secondary index on this table is NOT covered by this half. It needs its own grant and its own pair.

-- 1.0.0_SA_CTO~Z
