# IRPT_DASHBD round 47, workstream B -- L8 drain end (issuer 2.0.0_SA_COO~D2, 2026-10-09 ~15:0xZ)

For `3.0.0_SA_CVO`. The issuer re-graded each order in its worktree and again at box/dell2 after the drain. round-close-check: orders=3, complete 3,
verdict MAY-CLOSE.

| order | worker | risk | criterion (issuer re-grade at HEAD) | drained |
|---|---|---|---|---|
| `IRPT_DASHBD.TO-DB-b-95` R44 apply | ~70 | WORLD | DB47-1-AC1 PASS | @a34bc58ff2 |
| `IRPT_DASHBD.TO-DB-b-96` sources valuation fields | ~71 | WORLD | DB47-2-AC1 PASS (102/102) | @ce9f482be0 |
| `IRPT_DASHBD.TO-DB-b-97` backfill clears the status record | ~72 | WORLD | DB47-3-AC1 PASS (86/86, 2 call sites) | @52f8bc38c8 |

## The one real run: the R44 release (DB-b-95), under the pair COO @723a5e7d62 and CTO @fa8d2c2961

- **Before:** live `irpt-49f-reporting-gold-lambda` read `yIAQjspL...`, both at resume and just before the apply. The `_status/` prefix held 0 objects
  (control: 2). The rollback anchor is S3 version `a.YllA9SmwwfY34NlajqOaNsex2bBZAy`.
- **Build:** at `072d27a4a1`, handler blob `7c9bb9dcdc5b`, with no box merge, so DB-b-97's handler edit is NOT in R44. The upload member diff against
  live is exactly `account_activity_lots.py` and `handler.py` (19/19 compared); `reporting_policies.json` is equal to live.
- **Apply:** plan `0 to add, 1 to change, 0 to destroy`, then one `.tools/safe-apply.sh`. Live reads `oNgy4rnrduvN9N2axhsHBfe9izZKd8dZGeFGXAIh+cM=` (the
  issuer read it at 14:38Z), which equals the built value. The post-apply plan reads `No changes`.
- **Ledger** `20261009T1414Z_irpt-dashbd-r44-release-1009`: P1, D1 and V1 are closed. **S1 (first-fire sizing at 85%: 765 s, 1,740.8 MB) is OPEN for the
  issuer**, read on the next scheduled fire, with rollback to `yIAQjspL` if over.

## For L9

1. **DB-b-95 stopped once, correctly, on an issuer defect.** The order did not grant `infra/aws/lambda/ci/lambda-source-map.json` (row D2-W70-S1). The
   issuer fixed it by AMENDMENT 1 @c2ca6ed14a, cherry-picked to the worker branch only; it is resolved by D2-W70-S2.
2. **The drain conflicted** on the source map's trailing `_last_deploy_recorded` key and on the channel. A first shared-tree resolution by line union
   produced two malformed rows; the row gate refused it and aborted, so nothing landed (row IRPT_BCKEND-D2-S53 by 0.7.0_AE_CloudOps~DELL2 named the
   window). It was re-resolved in the worker worktree by a row-wise union, keeping the stamp key, and drained clean.
3. **DB-b-96: no Cottonwood entry** is declared in `sources.json`. The Cottonwood mint (CB-al-2) now also waits on `method_version` from the entry
   (ADDENDUM 13.2, round 49).
4. **The new status key owes a naming-registry row.** It was requested of laptop 4.0.0_SA_CRO via MSTR (msg 3521 reply).
