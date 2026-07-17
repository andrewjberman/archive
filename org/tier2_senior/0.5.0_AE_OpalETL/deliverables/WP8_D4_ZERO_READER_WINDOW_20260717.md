# WP8-DECOM D4 -- the zero-reader observation window (OPENED 2026-07-17)

**Filed by:** 0.5.0_AE_OpalETL. **Mechanism:** CTO ruling 20260717T164137Z = option B (S3 server
access logging on the dying bucket), three conditions folded below. **Window clock: NOT STARTED
until the self-read probe appears in delivered logs (condition 2).**

## The instrument (armed 2026-07-17 ~16:47-16:50Z)

- **Deviation from condition 1 as written, surfaced same-turn:** every existing ops/logging
  bucket is us-east-1; `opal-data-schwab` is **us-east-2**, and S3 access logging is
  same-region-only (`CrossLocationLoggingProhibitted`, measured). So the destination is a NEW
  DEDICATED telemetry bucket, not an existing one: `opal-schwab-d4-access-logs-313476888478`
  (us-east-2, PAB all-on, policy = single statement granting `logging.s3.amazonaws.com`
  PutObject on `s3-access/opal-data-schwab/*` conditioned on SourceArn=the schwab bucket +
  SourceAccount). **Temporary instrument -- deleted with the D6 motion.** The spirit of
  condition 1 holds: telemetry never touches the monolith. (A first attempt against
  `opal-cloudtrail-logs-313476888478` was fully reverted -- live sids read clean.)
- Logging config on `opal-data-schwab` (live read-back): TargetBucket = the D4 bucket,
  TargetPrefix `s3-access/opal-data-schwab/`.
- **Self-read probe (condition 2) FIRED 2026-07-17T16:49:47Z:** GetObject
  `01_raw/CRS20230117.RLD` range-64B, request-id `473HDV08DW9CZ25Y`. A Monitor polls the
  target prefix; **the window clock starts at the delivery of THIS request-id**, not at
  config-enable (config-enabled-without-delivered-probe is a DESIRED claim, 22a).

## Honest framing (condition 3, verbatim discipline)

- Server access logging is **BEST-EFFORT**. The eventual window verdict reads: **"no reads
  OBSERVED over N days (best-effort logging + IAM census both corroborate)"** -- never "zero
  reads proven". The actual CONTROL is D5's read-only + IAM flip; this window is corroboration.
- **The window measures READERS ONLY.** The SI2 automatic chain (`canonical-schwab-runner-role`)
  remains an ACTIVE WRITER by design until D2/L5b closes -- writer events in the logs are
  EXPECTED and are NOT a window breach. Probe-class reads by this lane (self-reads, D3 verify
  re-reads) are identifiable by requester role + request-id and excluded by enumeration.

## The DESIRED half (leg 1, CTO-accepted 164137Z)

Live authorization-details sweep (denominator: 209 roles + 30 local managed policies): **6
carriers** of opal-data-schwab grants -- `canonical-schwab-runner-role` (SI2 chain, expected-
active writer), `opal-schwab-monolith-remap-role` (D3 copy path), `schwab-anonymizer-lambda-role`
(02_anonymized, ruling-pending), `quartz-si2-spike-role` (quartz, ruling-pending),
`bd-exporter-ec2-role`, `MANAGED-POLICY:opal-assets-one-way-fan-in-fence` (deny fence).

## Window ruling (CTO 20260717T165744Z -- deviation APPROVED as executed)

- **N = 7 CALENDAR DAYS from the delivered-probe clock-start** ("long enough to catch any
  weekly cron reader; a monthly reader is D5's problem -- the read-only flip is the control").
- Clock-start reported to CTO with delivery evidence when req-id 473HDV08DW9CZ25Y lands.
- Cadence: daily requester-role histograms to the session record; exceptions to CTO.
