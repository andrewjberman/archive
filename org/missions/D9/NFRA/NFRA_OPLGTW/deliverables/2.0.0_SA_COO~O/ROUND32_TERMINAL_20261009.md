# NFRA_OPLGTW round 32 -- TERMINAL at the drain (2.0.0_SA_COO~O, 2026-10-09 ~15:5xZ)

`python .tools/round-close-check.py --project NFRA_OPLGTW --round 32` (fixed matcher @0cba1a01be):
`orders=14 complete=14 proof_ok=14 judgment=2 graded=0 ungraded=2 verdict=REFUSED` -- the two judgment criteria below are
the CVO's at L9, and they are the only thing between this round and its close.

## The orders (14 of 14 complete, every proof instance structurally valid)

| order | what it delivered | drained |
|---|---|---|
| OG-sf-1, OG-rf-1, OG-cm-1, OG-md-1, OG-sc-1, OG-en-1, OG-cc-1 | r29's build cells, the 08403355 enumerate, the closure census | before 2026-10-09 07Z |
| OG-tg-1 (r30 cell) | Opal-users Teams gate, sender identity, concierge mirror | fd8e329416 |
| OG-bf-1 | 13-month completion records, both masters, 512 of 512 qualified | 4d3f416b4e |
| OG-tm-1 | 08403355 on the daily schedule; first pull 10:45Z, 22 of 22 dates qualified | 0912929684 |
| OG-da-1 | data_refresh admission fails closed (deployed; qa-scratch clone pinned, A1) | 47c6a98f49 (applier) |
| OG-ap-1, OG-ap-2 | the 08403355 apply; the 49F dispatcher date gate | before 07Z |
| OG-ap-3 | r29 deployed, 91811b648a, verify 5/5, md5 98/98 | fab015fa54 (applier) |
| OG-rl-15 | r29 served read, Alyssa's 13-month grant (rev 3 -> 4), release drained back (A8) | 347b4f3764 |

## The one real run of each outcome (read, not predicted)

- **r29 served:** `RL15_READ.json` through the INSTALLED code, SSM 9f50157b: asker SAFE, SendGate present,
  calendar_months max 13, contract 1.4, 4 of 4 domain entries, 0 concierge families revoked, 0 grants written.
- **13 months for Alyssa:** `RL15_GRANTS.json`, SSM 426082eb: one principal changed, 274 available dates per master and
  dataset.
- **08403355 daily:** `tm1.sh AC2` read 22 completion records, 22 qualified with every named object at its VersionId.
- **Completion-record backfill:** `bf1.sh AC1` and `AC2`: 273 of 273 window dates qualified per master; 2048 served
  objects predate the backfill.

## Owed to `3.0.0_SA_CVO~Z` at L9 (judgment, never self-graded)

1. **OG-bf-1 AC3** -- did what the backfill caused downstream match the signed ask? The consumer's own log, read
   by the worker: `/aws/lambda/advi-49f-gold-dispatch`, 2026-10-09T05:48:03Z..06:40:00Z, 1537 events, START 256,
   SKIP "not the production T-1 ... historical record, not dispatched" 256, `dispatched doc=` 0, ERROR 0. Instance:
   `deliverables/0.9.0_WK_NFRA_OPLGTW~41/NFRA_OPLGTW.TO-OG-bf-1.closure-marker-backfill-13m.proof_of_spec.json`.
2. **OG-da-1 AC3** -- does each of the 6 caller roles in `deliverables/0.7.0_AE_CloudOps~Z/da1_callers.json` read
   ADMITTED in `/aws/lambda/opal-data-refresh-api`'s own log on its first real call after the deploy (2026-10-09
   07:59:39Z)? At the applier's close, 0 of 6 roles had called; the read is the CVO's, now. Instance:
   `deliverables/0.7.0_AE_CloudOps~Z/NFRA_OPLGTW.TO-OG-da-1.*.proof_of_spec.json`.

## Rows from this round, for the compile

Z-S72 (da-1 second reader, disarmed by A1), Z-S73 (round-close-check matcher, fixed), Z-S74 / Z-S75 (r29 halt gate on
the sparse release worktree; A2 wrong, A3 right), Z-W41-S4/S5, Z-W43-S7 (13-month read ~4 min/master cold, ARMED).

## Not in round 32 (round 33 workstreams, in flight)

OG-bh-1 (08403355 full history; batches 4-9 resumed with RPS-drift dates held), OG-pn-1 (RPS pin), OG-tl-1 / OG-ap-4
(transcript allowlist, deploying), OG-ab-1 / OG-ab-2 (E2; .xlsx releases alone), OG-pf-1 (r30).

-- 2.0.0_SA_COO~O
