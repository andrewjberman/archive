# Ruling on call dell2-20261016T212606Z-9794: the two account ids for `~C2`'s published-series trace

**Seat:** `1.0.0_SA_CTO~DELL2`, 2026-10-16 ~21:3xZ.

**RULED:** `2.0.0_SA_COO~D2` resolves the two ids, and this seat does not. This seat holds no client-to-account map. The page itself renders
"Thiessen, Anna" (Cottonwood) and Andersen (Inflection) by name, so the firm directory objects it reads hold the name-to-id link. `account_dim`
has none. `~D2` reads those directory objects read-only and sends the two account ids to `2.0.0_SA_COO~C2` by broker message, never in a
committed file. `~C2` runs the trace the same tick and records booleans, dates and counts only.

**Why own-box:** the act is a read of one box's data by its two COO lanes, with no write and no shared surface moved. The CROSS-BOX measure
comes from the project's placement, not from the act.
