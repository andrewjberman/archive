# NEVER-WIDEN SIGN-OFF -- CTO HALF -- IRPT_DASHBD DB-b-34: `irpt-49f-reporting-gold-lambda` also writes `account_class_daily`

**Signer:** `1.0.0_SA_CTO~DELL2` (NFRA_CTLPLN ADDENDUM v0.12 C-ROLES). **Bound to:** the packet
`org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~19/NEVER_WIDEN_PACKET_ACCOUNT_CLASS_DAILY_RELEASE.md`, all sections
as written at REMEDIATION_v8 @372500963a. A changed member list, a changed pin set or a plan other than the one stated re-opens this half.

## Signed, as the packet's "CTO half" section defines it

- **Blast radius:** one NEW prefix (`.../gold/account_class_daily/`, empty today); the returns prefix written byte-identically
  (sha256 `11453fc7...ae2e1` both ways, `RELEASE_LOCAL_RUN.json`); one table read by key (`dynamodb:GetItem` on
  `etf-classifications`, a cross-firm registry with no client data). No delete, scan, or write to any table.
- **Writers counted:** one rule (`emit_class_day`), two paths (the schedule and the bounded backfill event). The manual path creates no
  state the schedule cannot reach.
- **Both branches** are read from the producer's rule: A lands both tables. B refuses the class day by name, still writes returns,
  and the next fire's catch-up retries it.
- **Rollback per key** as written. The class-prefix rollback needs an S3 delete, which is Andrew's word (CLAUDE.md Agent Autonomy);
  it is not covered here and is listed if ever needed.
- **Reads the TABLE, not the seed module:** `etf_classifications_dynamodb.py`, per this seat's round-21 correction. The sample
  unclassified share is 0.153% against the module's 1.804%.

## Conditions on the apply

1. Preconditions 1 and 2 are met by the deploying lane: the three `staged_from` pins land together (pins 1 and 3 never apart), and
   the plan read is exactly 0 to add, 1 to change (the role policy) and 0 to destroy, plus the code hash. Any other plan stops the
   apply.
2. The apply runs from dell2 once terraform is on the box (the kit, laptop 106173). This is not an emergency, so no laptop applier
   is used.
3. A1-A5 are read on the first fire. A3's firm-wide unclassified share is printed and recorded (W19-S5 closes on it).

## W19-S1 (separate from this act)

`etf_classifications_dynamodb.py` returns `None` on a read error, and every caller other than this producer reads that as "no item".
It is a fail-open-to-unclassified for those callers. This producer is not affected: it raises `ClassTableUnreadable`. The client is
shared across projects, so the fix (raise on error and distinguish "absent") is routed to its owner. It is not part of this release.

```
NEVER#1   "never move served output without never-widen sign-off (CTO+COO)"
ACT       targeted safe-apply of infra/aws/terraform/investor-reporting/reporting-gold/ with the rebuilt artifact
CTO half  1.0.0_SA_CTO~DELL2 -- GIVEN 2026-10-07 ~13:0xZ, on conditions 1-3
```

-- `1.0.0_SA_CTO~DELL2`
