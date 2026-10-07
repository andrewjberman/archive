# NEVER-WIDEN SIGN-OFF -- COO HALF -- IRPT_DASHBD DB-b-34: `irpt-49f-reporting-gold-lambda` also writes `account_class_daily`

**Signer:** `2.0.0_SA_COO~D2`, the issuer of IRPT_DASHBD on dell2. **Bound to:** the packet
`org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~19/NEVER_WIDEN_PACKET_ACCOUNT_CLASS_DAILY_RELEASE.md` as merged at
@d48052d79b and compiled at REMEDIATION_v8 @372500963a, and to the CTO half
`deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_ACCOUNT_CLASS_DAILY_RELEASE_CTO_HALF.md` @9816b17511. A changed member list, pin set or plan
re-opens this half, as it re-opens the CTO's.

## Signed, as the packet's "COO half" section defines it

- **Blast radius, read from the act:** the targeted safe-apply of `infra/aws/terraform/investor-reporting/reporting-gold/` with the
  rebuilt artifact. It writes ONE new prefix (`s3://opal-data-49financial/irpt/49financial/gold/account_class_daily/`, builder output
  `address("irpt","49financial","gold","account_class_daily","date=<D>")`), rewrites the returns prefix byte-identically (sha256
  11453fc7...ae2e1 both ways, the before side on the base handler and base `sources.json`), and reads `etf-classifications` by key only.
  The role policy is the one changed resource; the schedule is unchanged.
- **Writers of the new prefix, counted:** 1 rule (`emit_class_day`), 2 paths (the schedule with its catch-up, and the bounded backfill
  event). Both are read from the handler at @d48052d79b; neither path reaches a state the other cannot.
- **Both branches:** A, the first fire writes the class table for its days with the identity holding; B, a class day is refused by name,
  the returns table is still written, and the next fire's catch-up retries it (rows W19-S4, W19-S6, resolved by S29 @c4c454a03b).
- **Rollback per key:** the prior Lambda version and the prior role policy are restored by re-applying the root at the base pins. Removing
  the class prefix's objects is an S3 delete, which is outside this half and needs Andrew's word (CLAUDE.md Agent Autonomy).

## What this seat does, and in what order

1. The deploying lane sets the three `staged_from` pins in `infra/aws/lambda/ci/lambda-source-map.json` together (account_class_daily.py;
   etf_classifications_dynamodb.py packaged flat; sources.json re-pinned), at @d48052d79b with their sha256, and rebuilds the artifact.
   This seat routes that act to the lane and does not set the pins itself.
2. This seat reads the plan. It applies only on exactly 0 to add, 1 to change (the role policy) and 0 to destroy, plus the code hash. Any
   other plan stops the apply.
3. This seat applies ONCE from the saved plan, from dell2, when the terraform kit is on the box (CTO condition 2). The change-management
   entry is opened in `org/critical_paths/change_management/` at the start and closed on completion.
4. This seat reads A1-A5 on the first fire, and records A3's firm-wide unclassified share (W19-S5 closes on it).

```
NEVER#1   "never move served output without never-widen sign-off (CTO+COO)"
ACT       targeted safe-apply of infra/aws/terraform/investor-reporting/reporting-gold/ with the rebuilt artifact
CTO half  1.0.0_SA_CTO~DELL2 -- GIVEN @9816b17511 on conditions 1-3
COO half  2.0.0_SA_COO~D2   -- GIVEN 2026-10-07 ~13:1xZ, on the same conditions and the order above
```

-- `2.0.0_SA_COO~D2`
