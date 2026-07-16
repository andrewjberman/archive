# opal-data-schwab DECOMMISSION -- the census + redirect map (Andrew-direct ~16:2xZ @ de4978e3a)

**Filed by:** 0.5.0_AE_OpalETL, 2026-07-16 ~16:4xZ. **Order (verbatim on record):** identify
everything pointing at opal-data-schwab, redirect to the correct opal-data-assets locations,
then decommission the bucket. **Execution stance:** staged -- redirect -> verify zero
readers/writers -> read-only -> the delete motion on Andrew's final go (destructive class).
Composes with WP7/L5b; nothing here races the in-flight re-points.

## 1. THE BUCKET, measured (live, ~16:3xZ; ~38,392 objects; historically ~82.8GB)

| prefix | objects | what it is | disposition class |
|---|---|---|---|
| 01_raw/ | 7,222 | the 0824 CRS delivery archive (flat names, back to ~2024) | UNIQUE pre-SI2 raw history -> COPY into monolith schwab/08242234/bronze/ per the CTO backfill ruling, then retained-read-only until delete |
| bronze/ (rps mirror) | 338 | *.RPS mirror of 01_raw | derivative of 01_raw -- no separate copy needed once 01_raw history lands |
| silver/ {ACC,TRN,ULN + scripts/} | 1,516 | UPPERCASE legacy silver + a CODE dir inside silver/ | consumers below need redirect ruling; scripts/ = stray code home to disposition |
| 03_silver/ | 1,005 | older silver generation | disposition ruling (likely superseded; verify no reader) |
| 08242234/ | 5,966 | the C3 staging tree (0824 wide pull) | ALREADY the monolith migration source -- verify copied-complete, then no action |
| 08335338/ | 6,932 | the 0833 staging tree | memory-recorded DONE into monolith (6,932, 13c-clean) -- verify tie, then no action |
| backfill/ | 6,935 | backfill staging | verify duplicated-into-monolith or unique; ruling |
| 02_anonymized/ | 3,221 | anonymized derivatives | disposition ruling (derivable? unique?) |
| 03_mappings/ | 3,193 | mapping tables -- SENSITIVE (the NFRA-P2 silent-grant finding names this prefix) | disposition ruling w/ the P2 doc's context; likely copy-to-controlled-home |
| _archive/ | 3,988 | archive | disposition ruling |
| _ops/ | 22 | **the SI2 box's Rule-12 code home (sdd-daily-pull.ps1)** -- LIVE dependency | new code home BEFORE read-only (0.6.2's surface) |
| 01_raw_quartz_validation/ | 54 | validation snapshots | disposition ruling |

**No S3 event notifications on the bucket** (measured: empty config) -- nothing event-wired to unhook.
**Bucket TF/policy:** the AES256-SSE resource-deny bucket policy (the skill's known posture);
retire with the bucket. **Audit note:** the cross-firm read-deny belt (news-pipeline/
cross-firm-bucket-read-deny.tf) enumerates opal-data-{bd,cot,inf} LITERALLY -- schwab was never
in the belt (NFRA-P2 finding), so decommission CLOSES a standing audit gap.

## 2. LIVE consumers/writers -> the redirect map

| # | pointer | redirect | vehicle | status |
|---|---|---|---|---|
| 1 | my /49-schwab-conv seven (01_raw + bronze/rps + local-OneDrive TRN) | monolith schwab/08242234/bronze/ (unzip-at-read, parameterized master) | **L5b** (pre-approved, ~A authoring next) | in flight |
| 2 | sync_schwab_onedrive_to_s3.py (writer) | retires outright (the box delivers monolith-side) | L5b retirement leg | in flight |
| 3 | SI2 box code-pull: _ops/canonical-schwab-si2/sdd-daily-pull.ps1 | new code home (opal-data-assets _ops/ or the lambda-artifacts bucket -- 0.6.2/CTO call) | 0.6.2 surface | TO ROUTE |
| 4 | B_02.canonical_lots reads silver/ULN (uppercase) -- GOLD consumer | redirect ruling: its lot source should ride the L5b-era silver (opal-data-bd/schwab/silver/uln lowercase) or monolith-derived | DS/bd lane + CTO gate | TO ROUTE |
| 5 | comp-freshness config: s3://opal-data-schwab/silver/RPS/ | update the config row to the surviving home | tooling touch (~Z/CTO) | TO ROUTE |
| 6 | PFMG_TAXSMA PRD S0.1 leans on the bucket's silver for Tax-SMA cost basis | PRD pointer update to the surviving home | ~A lane awareness | TO ROUTE |
| 7 | docs/README/guides (historical references) | sweep at read-only time; archive-grade, no data risk | batch doc pass | LAST |
| 8 | IAM grants naming the bucket (incl. the 03_mappings silent grant from NFRA-P2) | revoke at read-only | CTO/0.7.0 TF | AT READ-ONLY |

## 3. THE STAGED PLAN (gates named)

1. [L5b lands, ~A + me] consumers #1-2 die; TWO clean re-pointed cycles per the CTO clock.
2. [parallel] #3 code-home move (0.6.2) + #4 gold-consumer ruling (DS/CTO) + #5/#6 pointer updates.
3. [me, CTO gate] UNIQUE-CONTENT COPY: 01_raw full history -> monolith schwab/08242234/bronze/
   (the bridge mechanism at archive scale: ETag census, idempotent, 13c tiers) + dispositions
   for 02_anonymized / 03_mappings / 03_silver / _archive / backfill / quartz per CTO rulings.
4. [CTO] zero-reader/zero-writer verification window (access-log or IAM-simulate sweep).
5. [CTO/0.7.0] bucket -> READ-ONLY (policy) + IAM revocations.
6. [ANDREW's final go] the delete motion itself.

## 3a. VERIFY CELLS EXECUTED (successor session, 2026-07-16 ~20:1xZ -- read-only, measured)

Both staging-tree "verify, then no action" cells from S1 are now MEASURED (ListObjectsV2
key+ETag+Size both sides, relative-key join, denominators printed; script preserved in the
session scratchpad, method = the 13c tiers, never loosened silently):

- **08335338: VERIFIED-TIED.** Legacy 6,932/6,932 relative keys common; ETag exact 6,932/6,932;
  only-legacy 0. Monolith-only 40 = the NEW daily deliveries (dates 20260713-20260715 landing
  monolith-side directly -- the automatic chain, not a gap). **Disposition confirmed: no action.**
- **08242234: VERIFIED copied-complete.** Legacy 5,966/5,966 keys common; only-legacy 0.
  ETag exact 5,321/5,966; the remaining 645 are ALL multipart-vs-plain ETag shape (legacy
  multipart upload, monolith single-part), ALL size-tied, 0 true-MD5-diff candidates.
  Content-grade close on the shape class: 3 sampled pairs downloaded, legacy MD5 == monolith
  plain ETag 3/3, with a separate positive control (plain-ETag legacy object, computed==listed)
  run BEFORE the targets. Monolith-only 291 = new deliveries + recovered rld 2023 history
  (CRS2023xxxx.RLD -- the monolith is MORE complete than the legacy staging tree).
  **Disposition confirmed: no action.**

Residual on these two prefixes: none. The copy-class work remaining in S3 stage 3 is 01_raw
history + the ruling-pending prefixes (02_anonymized / 03_mappings / 03_silver / _archive /
backfill / quartz), unchanged.

## 4. What this composes with

WP7/L5b (the redirect spine), the WP7 backfill ruling (now bucket-wide), 0.6.2's SI2
decommission thread, MSTR's LCLRPO legacy dispositions (superseded-in-direction), and the
NFRA-P2 audit-gap closure. Nothing new races anything in flight.
