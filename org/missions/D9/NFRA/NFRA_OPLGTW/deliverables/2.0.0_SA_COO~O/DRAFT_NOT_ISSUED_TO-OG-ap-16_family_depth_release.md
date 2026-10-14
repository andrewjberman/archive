# DRAFT, NOT ISSUED -- `OG-ap-16` -- APPLY: OG-cd-1's FWD-20 cadence/depth read on the gateway (its read grant, the release, the route)

Status: DRAFT by `2.0.0_SA_COO~O`, 2026-10-13 ~23:5xZ. This is work-ahead on an empty drive tick, done around OG-ap-14's
block. It is cut at the round-37 analysis's recut (or as a round-37 recut cell if the CTO names it there), and only then
gets its checks, written and dry-run at the base. Its write surfaces and criteria below are the cut's starting point,
not a grant.

## Facts it rests on (measured 2026-10-13)

- **The code:** OG-cd-1 drained @4de09d2d86. Build commits `046bc2be02` (module, refs file, tests, IAM file, ask),
  `1653c34232` (live read re-run), `2b000fea49` (denominator_source fix). Gateway paths: `app/family_depth.py`,
  `app/refs/silver_families.json`, `tests/test_og_cd1.py`. Terraform: `infra/aws/terraform/opal-gateway/family_depth_read_iam.tf`.
- **The ask:** `deliverables/0.9.0_WK_NFRA_OPLGTW~65/NEVER_WIDEN_ASK_OG-cd-1.md`; halves `1.0.0_SA_CTO~Z` + `2.0.0_SA_COO~O`.
- **The ONE grant:** `gateway-family-depth-read-policy` (builder output) on `opal-gateway-role`:
  - `events:DescribeRule` on the `opal-assets-silver-*-sweep-daily` rules;
  - `s3:GetObject` on `opal-data-assets/*/meta/backfill-status.json`;
  - `s3:ListBucket` on `opal-data-assets`, conditioned to silver prefixes.
  It plans 1 add, 0 change, 0 destroy.
- **The route:** ONE line in `app/admin_api.py`,
  `Route("/gateway/families", family_depth.families, methods=["GET"])` behind `owner_gate.owner_only`. It is the
  issuer's hookup at the release; the file is NFRA_MCPORTAL's, so the line is named in the pair and taken with
  `2.0.0_SA_COO~MP`'s word.
- **Gateway queue:** MX-r-11 v2 (NFRA_MCPINDEX) -> OG-ap-14 (r30) -> OG-hv-2 (harvest) -> THIS -> MP-n-4.

## Shape (same as OG-ap-14 and OG-hv-2; applier `0.7.0_AE_CloudOps~Z`)

- **PHASE A** (after OG-hv-2's ledgers close): read the live ref from EC2_MANIFEST plus one host md5 read; re-cut
  `rel-nfra-oplgtw-cd` at it, taking OG-cd-1's gateway hunks plus the one route line; re-generate
  `silver_families.json` with `python -m app.family_depth --generate`, and show it byte-equal to the committed one or
  name the drift; run `test_og_cd1.py`; targeted plan of the one policy; write the ask (re-pinned to the release). STOP.
- **PHASE B** (on the GO naming both halves): ledger `nfra-oplgtw-family-depth-read-grant`, then apply the policy and
  run a simulate (allowed on one backfill-status key, implicitDeny on a non-meta key). Then ledger
  `nfra-oplgtw-gateway-release-cd`, deploy, and read back.
- **The served read:** ONE owner-gated GET of `/gateway/families` through the INSTALLED code, writing `AP16_SERVED.json`
  with: families >= 7; claim-less values 0; schwab schedule equal to a live `describe-rule`; schwab frontier equal to
  the live backfill-status. Runbook 7.2 and EC2_MANIFEST move to the release.
- **Criteria (to write at the cut, at most three):**
  - AC1, the re-cut carries only OG-cd-1 + the route line (the ap14.AC1 containment method);
  - AC2, landed, closed, recorded and served;
  - AC3 (judgment, `3.0.0_SA_CVO~Z`), NFRA_MCPORTAL's page shows the read. That is MCPORTAL's display cell, so
    record it as owed.

## Open before the cut

- **2.0.0_SA_COO~MP's word on the route line** in their `admin_api.py`. One ask, sent at the cut, not now: the round is
  frozen, and the ask is cheap once the release is next in the queue.
