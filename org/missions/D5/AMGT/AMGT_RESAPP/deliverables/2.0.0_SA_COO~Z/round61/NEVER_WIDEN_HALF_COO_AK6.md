# AMGT_RESAPP round 61 -- `AMGT-ak-6` never-widen half (COO), `2.0.0_SA_COO~Z`, 2026-10-02 ~08:2xZ

**The act (ONE, after AMENDMENT 1):** the stored-field rewrite of the three FROZEN plans. For each key: GET, assert every plan
entry's `before`, set `after`, and PUT the whole object back at the SAME key in the versioned pool bucket `opal-data-harvest`.
There is NO redeploy (AMENDMENT 1: 0 of 350 packaged members changed). Executor `0.7.0_AE_CloudOps~A`; order
`task-orders/AMGT_RESAPP.TO-AMGT-ak-6.the-stored-text-rewrite-and-redeploy.md`; decomposition s.69. DSGN round-21 analysis
section 3B cells B2, B3 and B4 (@e14de1769c, @b74c090804).

## THE FROZEN PLANS (the act's literal write set; any differing byte is a STOP and a re-sign)

| plan | cell | sha256 | entries |
|---|---|---|---|
| `deliverables/0.9.0_WK_AMGT_RESAPP~201/m1_lusha_reason_plan.json` (worker commit `25ac521b3d`) | B2 | `d373d0615deef8019619079d6df9b803b4aac82e75890c25e8469c53ce4629c4` | 8 thesis (`lusha_enrichment.reason`) + 1,170 peers (`csc_columns.absent[i].reason`, 5 per key) |
| `deliverables/0.9.0_WK_AMGT_RESAPP~202/m1_officer_plan.json` (drained `a846f71d22`) | B3 | `11518fd5924c880614adfeff0acf92d7464bc1f546d21e4075f0874d21188424` | 1 (VLO `officers`) |
| `deliverables/0.9.0_WK_AMGT_RESAPP~203/posture_claim_plan.json` (drained `7672553ecc`) | B4 | `0e77bc0c349b5675555af120ce2d26c8ebf0f27c2aba672322975e1c0193d684` | 9 (`basis[i].claim`) |

Every `after` was computed by the FIXED producer code: `enrich.domain_for` (NO_DOMAIN_SKIP_REASON), `csc.build_csc_map` (via
`lib/research/peers/csc_plain_reasons.py`), the `roster.py` parser (rk-46) on the stored filing, and `judge.plain_claim`. None was
hand-typed.

## THE BASE, read live at signing -- the rollback

`deliverables/2.0.0_SA_COO~Z/round61/AK6_BASE_VERSIONS.json` was produced by `round61/checks/ak6_base.py` over the three plans at
signing. It covers 251 DISTINCT keys (234 `peers/v1/`, 9 `posture/v1/`, 8 `management/v1/`) and 1,188 entries. Each key carries its
current VersionId and ETag. **0 mismatches**: every entry's `before` equals the stored value, and all 251 objects are versioned. The
VLO keys, for example:
- `management/v1/VLO_US_Equity/2026-09-18.json` VersionId `YAZVVZSFEb6DVjE2EIWl2KAKtEZPaGIe` (2 entries: B2 Lusha + B3 officers, applied in ONE put);
- `peers/v1/VLO_US_Equity/2026-09-24T2252Z.json` `OYVR4BnBxg3IlopB8ofQIIo8AWMnLBnu` (5);
- `posture/v1/VLO_US_Equity/2026-09-16.json` `.XupCtcpu4YqWik9FgHBSKUINq5HjjJN` (1).

## WRITERS OF THE PROPERTY: per key family, 2 writers; none scheduled

| family | writers | schedule |
|---|---|---|
| `management/v1/` | the M-1 producer (`lib/research/management/` enrich/roster, hand-run) + this act | none (no infra trigger names the prefix; `infra/` references it only in the scoped API's read grant) |
| `posture/v1/` | the posture judge (`lib/research/posture/judge.py`, hand-run, an Anthropic call) + this act | none |
| `peers/v1/` | the peers builder (`lib/research/peers/csc.py` via its runner, hand-run) + this act | none |

A later producer run writes a NEW `<as_of>` object with the FIXED code, so the words persist. This act overwrites only the newest
object, the one the route reads.

## READERS

`/security/{key}/thesis` (`management`, `posture`) and `/security/{key}/peers`, on DEV and PROD. They read verbatim, newest object
per key. No other route reads these fields.

## THE BLAST RADIUS -- what the act MAY touch, and the rollback per key

| act | what it MAY touch | rollback |
|---|---|---|
| PUT per key | exactly the 251 keys in the appendix, and within each object only the plans' `store_field`s | per key, copy the appendix's prior VersionId back over the key (`copy_object` with `CopySource` `VersionId`); never an S3 delete |

A key whose asserted `before` differs at act time is a STOP for the whole act, with nothing more written.

## EXPECTED OUTCOME -- both branches, read from the readers' own rule (verbatim read of the newest object)

- **Every PUT lands (expected):** b2 C1 reads 0 of 26 code-shaped (base 11); b3 VLO 5 officers with full names, 0 aged roles, BA 12
  unchanged; b4 0 of 12 claims with a status token (base 2). The other 249 names' served Exec/Peers/posture text changes only on the
  planned fields, all of them to the producer's words.
- **A PUT fails partway:** the keys already written serve the new words and the rest serve the old. AC1-AC3 grade BA and VLO only,
  so a partial write that covers them can PASS while other names stay coded. So the executor's `ak6_store_writes.json` must list 251
  of 251 written, or the act is not closed: it is completed or rolled back key by key.
- **AC1, AC2 or AC3 fails after the act -> ROLLBACK** per the table.

## WHAT THIS HALF DOES NOT COVER

No redeploy, no code change, no S3 delete, no vendor or model call, no posture regeneration, no new object keys. No field outside
the plans is touched.
