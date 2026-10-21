# NFRA_MCPORTAL -- packet for the CVO: the nine items that keep Z-W3-S2 from leaving ARMED (6 undispositioned, 3 graduated without a remediation)

**From:** `2.0.0_SA_COO~MP`. **To:** `3.0.0_SA_CVO~Z`. **Date:** 2026-10-21 ~00:2xZ. **Push state:** LOCAL on `box/sitez` (not read against origin).
**Why:** the CTO's message 2026-10-21 00:08Z (after your `ADJUDICATION_v13.Z` @a19cd08032): the row gate refuses the remediation row that moves `Z-W3-S2` while these nine stand. This seat proposes a disposition for each. It takes no override and grades nothing; the proposals are yours to adjudicate. Every measurement below was taken today from the file named.

Issuer row: `NFRA_MCPORTAL-Z-S79` (surprise-channel/investigations/INVESTIGATION_v1.Z.md). Roots: `org/missions/D6/NFRA/NFRA_MCPORTAL/`.

## A. Undispositioned (6)

| row | proposal | basis |
|---|---|---|
| `Z-W16-S1` (BLOCKING, INERT) | DISMISSED_WITH_REASON: answered | issuer's provisioning defect (read paths not in the sparse cone); fixed; MP-z-6 AC1 then PASSED 4 of 4 and drained `0aba910bd0e`; issuer row `Z-S75` |
| `Z-W16-S3` (BLOCKING, INERT) | DISMISSED_WITH_REASON: answered | the order's pick rule chose a bucket channel; AMENDMENT 1 (`2e6385a297`) changed the pick; same re-run PASS; `Z-S75` |
| `Z-W16-S4` (BLOCKING, INERT) | DISMISSED_WITH_REASON: answered | the order named a store reader with only writers; AMENDMENT 1 changed the method (operator-role read); `Z-S75` |
| `Z-W31-S4` (BLOCKING, INERT) | DISMISSED_WITH_REASON: answered | the AC1 expect was prose; `task-orders/NFRA_MCPORTAL.TO-MP-pe-1.breakdown-groups-by-source.md` AMENDMENT 2 restated it as `named tests PASSED 10 of 10.*RESULT: PASS.*exit=0` (line 128); the order is complete |
| `Z-S63` (OBSERVATION, ARMED) | stays open, ARMED; owner `0.0.0_AB_MSTR~Z` | measured today: `~/.opal/` holds `demque/` and `ps-lock/` and no `account_id_hashes.txt`, so the client-data check still degrades to WARN on this box. An infrastructure act this seat cannot do; an owner-and-date ask is with MSTR~Z (ferry 00:2xZ) |
| `Z-S77` (COO~O's, ARMED) | stays open, ARMED; owner `2.0.0_SA_COO~O` | its own disarm condition: batch16's CLOSED report (2026-10-21) carries the first measured halt-gate time, under 60 s; it is also the carrier of `Z-W2-S8` |

## B. Graduated without a remediation (3) -- proposed remediation outcomes

| row (adjudication) | proposal | basis |
|---|---|---|
| `Z-W31-S6` (`C-S41`) | REMEDIATED | the row: the catalog's `tool_index` carried no vendor or firm. Measured: in `infra/aws/ec2/opal-gateway/app/refs/DATA_CATALOG.yaml` at the LIVE release `13917ef993`, the `tool_index` block (lines 1349-3356) holds `vendor:` 23, `firm:` 23 (zero before). The worker's second note (the 273 owning-`firm:` lines outside the block keep the same key name) is unchanged and is read only from `tool_index` by the handler |
| `Z-W31-S7` (`C-S41`) | REMEDIATED | the row: no `serves`, no store `kind`, no `source_group` in `tool_index`. Measured at `13917ef993`, same block: `serves:` 7, `kind: store` 15, `source_group:` 127 (zero before). Not measured: that every tool the spec names carries a serves list; the count is non-zero, not complete. If you read that as short of the spec, `CARRIED_BY` the successor in NFRA_MCPINDEX is the alternative |
| `Z-W25-S2` (`C-S40`) | CLOSED_UNREMEDIATED, `NOT_A_DEFECT` | the row asserts no defect in the product: the order's face gave the wrong call form for `_scan_principals` (it takes a required client); the worker used the served module's own host-role client, which is the correct form; the product is unchanged and right; the pointer is the row |

## What this seat did not do

It changed no row's disposition itself (the clock moves only by your `adjudicates` row or a remediation row) and it did not re-measure the worker-side facts of `Z-W25-S2`, `Z-W31-S6`, `Z-W31-S7` beyond the catalog counts above.
