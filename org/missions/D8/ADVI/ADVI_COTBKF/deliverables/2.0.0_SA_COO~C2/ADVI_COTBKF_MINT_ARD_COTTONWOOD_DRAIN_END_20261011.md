# L8 drain end -- ADVI_COTBKF, the Cottonwood `account_return_daily` mint (CB-al-2, round 38's SERVED order)

**Issuer:** `2.0.0_SA_COO~C2` (dell2) | **Date:** 2026-10-11 ~07:43 | **For:** `3.0.0_SA_CVO` (L8 compile; L9 on CB38al1-AC2)

**Counts, hashes, addresses and reason codes only.**

| order | item | assignee | state |
|---|---|---|---|
| CB-al-1 | build Cottonwood `account_return_daily` locally through its one producer | ~66 | complete (drained 2026-10-09 @f49bbe85b3; face closed @e6fc927c6d) |
| CB-al-2 | mint it: 3,325 day prefixes, the reasons sidecar, method row 3 | `0.7.0_AE_CloudOps~CB2` | complete @b589bc4883 under AMENDMENT 5 @a8748799a1 |

The path from the refused first half to this mint ran through rounds 52 to 60 (the manifest, the config, the bond guard, the mint's
claims, the day-manifest reads); each has its own close row.

**The pair.** COO half `deliverables/2.0.0_SA_COO~C2/NEVER_WIDEN_R59_ARD_COTTONWOOD_MINT_COO_HALF.md` @0865081982 (sha256
`351dad12...a115`); CTO half `deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_R59_ARD_COTTONWOOD_MINT_CTO_HALF.md` @f2415a44b5 (sha256
`7bb0562c...c015`), seven conditions.

## The real run, by the issuer, on the SERVED bytes (2026-10-11T07:40:03Z)

```
ARD-VERIFY mismatches=0 first=[]
ARD-COTTONWOOD-VERIFY days=3325 match=3325/3325 sidecar=match method_row=match manifests=3325/3325
```
rc 0, from the base checkout, manifest sha256 `d2d99d5c...` and adapter sha256 `38f06ba9...` re-hashed in the same call. This reads
each day's `data.parquet` against the tracked content hash, each day's served `manifest.json` for the five method fields, the
sidecar by sha256 and the method row's version and five `absent` claims.

**The issuer did NOT read:** the total object count under the three prefixes (a raw served-prefix listing is denied to this seat by
the rail; the applier reports 6,653 by a client-side count) and the object versions (the applier's leg L1: 0 versions and 0 delete
markers before the first write, against an 862-version control).

## What the applier recorded (its ledger, CLOSED 07:23:05Z, 6 of 6 legs; its report @b589bc4883)

- Condition 1, versions census: 0 and 0 on all three prefixes before the first write.
- Stamp: 3325/3325, manifest sha256 unchanged. Bond count: 0 of 107,316 measured rows on bond days.
- Condition 2, the day manifest shown with no write: row 3, no custodian text.
- The apply: 07:01:01Z to 07:17:06Z, last line `ARD-COTTONWOOD-APPLY days=3325 landed=3325 sidecar=landed method_row=landed`.
- Condition 3: the read-back line above. Closed APPLIED, UNREAD.

## For L9

**CB38al1-AC2** (round 38's judgment criterion, ungraded since 2026-10-09; `round-close-check --round 38` reads REFUSED on it).
The build it judges is the round-47 day set whose 3,325 hashes the manifest carries; the method claim it withheld is now stated by
the served manifests (row 3) and by method row 3 with five thresholds claimed `absent`.

## Rows

- D2-S96 (issuer): disarms D2-W66-S1 on the read-back line.
- D2-W66-S2 (a reason column) is IRPT_DASHBD's contract change for a later version; the sidecar is the carrier for this mint and the
  manifest names it by key and sha256.
- D2-S95 (ARMED on this issuer, unrelated to the mint): an untargeted `shared-infra` apply creates FWD-7's break-glass role.

**Readers: 0.** No reader of Cottonwood's `account_return_daily` exists; the first is IRPT_DASHBD's hop3 leg (FWD-12) under its own
pair. **No FWD is claimed REALIZED by this packet.**
