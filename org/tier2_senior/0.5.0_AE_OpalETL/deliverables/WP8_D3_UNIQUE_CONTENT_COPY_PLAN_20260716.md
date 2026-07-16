# WP8-DECOM D3 -- the 01_raw unique-content copy plan (at CTO's gate)

**Filed by:** 0.5.0_AE_OpalETL, 2026-07-16 ~20:2xZ. **Status: PLAN -- execution gated on CTO's GO.**
Composes with V2-5 (bronze closeout certificate): the post-copy census and the certificate are
the same evidence worn two ways -- one run emits both (per CTO 201227Z).

## 1. What was measured tonight (read-only; denominators printed; instrument in session scratchpad)

- **01_raw/ = 7,222 objects / 195.21 GB.** All 7,222 parse to `CRS{YYYYMMDD}.{TYPE}` flat names
  (0 unparsed) -- UNZIPPED as-delivered CRS files from the pre-SI2 OneDrive delivery era.
- **Monolith 0824 bronze = 6,257 objects**, all parse to `{type}/{date}/...` (0 unparsed) --
  the SI2-era tree is *.zip* deliveries plus the already-recovered UNZIPPED rld/tcf 2023 history.
- **Format confound named:** raw ETag-membership reads 6,909/7,222 "unique" -- FALSE lens. The two
  eras carry the same logical content in different byte formats (unzipped vs zipped), and 3,679 of
  01_raw's ETags are multipart-shape besides. The trustworthy lens is logical `(type, date)`:
- **THE TRUE GAP: 988 logical (type,date) pairs in 01_raw with NO monolith equivalent** --
  one contiguous band, 2024-01-12..2024-07-05: ult/rps/uln/upn/upt 120 dates each,
  trn/sec/acc 119 each, tnn 31. rld/tcf/tcfx/rly/rty/rlw: fully covered (0 missing -- the
  earlier recovered-history backfill did its job).
- **bronze/ (rps mirror) = 338 objects / 19.42 GB** -- derivative of 01_raw per the census;
  verify-membership then no separate copy (S1 disposition stands).

## 2. The copy (per the CTO backfill ruling: FULL history, byte-for-byte)

- **Motion:** server-side `CopyObject` (no download leg), `s3://opal-data-schwab/01_raw/CRS{D}.{T}`
  -> `s3://opal-data-assets/schwab/08242234/bronze/{t}/{D}/CRS{D}.{T}` -- the exact shape the
  recovered rld 2023 history already established monolith-side (unzipped flat file under the
  typed/dated prefix; both formats legitimately coexist under 17a: each is raw as-delivered
  from its own delivery era).
- **Idempotent, never-overwrite:** manifest-driven. Skip when target key exists AND ties
  (ETag-exact, or size-tie + sampled-MD5 for multipart shapes). **A target key present but
  NOT tied = STOP and surface -- never overwrite.** Re-runs converge to 0 pending.
- **SSE:** bucket default AES256, NO producer SSE header (13a-reversed posture).
- **Additive-only:** object puts into the existing grammar; no policy / notification / TF /
  scheduler touch anywhere. Nothing races L5b or the automatic chain (distinct key spaces:
  the chain writes zips under account-prefixed names; this writes `CRS*` flats).
- **Denominators enumerated at run time** (13b): the manifest is re-listed at execution, never
  reused from tonight's snapshot.

## 3. Verification (13c, three tiers, never loosened silently) == the V2-5 certificate evidence

1. **Keys:** post-copy ListObjectsV2 census -- every manifest key present; only-legacy = 0.
2. **Size:** size-tie on all 7,222.
3. **Content:** ETag-exact where shapes match; the multipart class closes on sampled true-MD5
   (sample >= 10, positive control run as a SEPARATE invocation before targets).
4. **Logical-coverage close (the certificate's headline):** re-run the (type,date) instrument --
   monolith coverage must be a SUPERSET of 01_raw's; the 988-pair gap reads 0.
5. **rps-mirror membership:** each of the 338 bronze/ ETags is a member of the 01_raw set
   (or size+sampled-MD5 for shape mismatches) -- proves derivative status, closes its cell.

## 4. Explicitly NOT in this plan

The ruling-pending prefixes (02_anonymized / 03_mappings [P2-sensitive] / 03_silver / _archive /
backfill / 01_raw_quartz_validation) -- dispositions remain at CTO. Bridge retirement, L5b, D1/D2
gates: untouched. The delete motion: Andrew's final word only.

## 5. Cost/duration estimate

195 GB server-side copy, 7,222 objects; all under the 5 GB single-CopyObject ceiling
(largest MEASURED: CRS20251231.RLY at 0.333 GB) -- single-pass, no multipart-copy leg needed; est. wall-clock
tens of minutes with modest parallelism. Zero egress.
