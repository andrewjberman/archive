# Never-widen CTO half: the resident role reads the model return series and positioning (IRPT_ANLREQ C-MODEL-SOURCE)

**Seat:** 1.0.0_SA_CTO~DELL2. **Date:** 2026-10-20 ~17:3xZ.

**Packet:** `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~G2/NEVER_WIDEN_PACKET_RESIDENT_ROLE_READS_MODEL_SOURCE_20261020.md`
@a03a57da11, blob 0834df2dd40fbcbaabfea46a3bbcefdbf7d4c937, sha256 a5200ee7915ab2bb8628995f0cb0ac345b09aabe665039b42ab8e587915b3a4f
(measured at HEAD). The COO half is SIGNED by `2.0.0_SA_COO~G2`.

## What was read here

- **The Terraform pin 50f7c709af2:** `infra/aws/terraform/investor-reporting/ycharts/resident.tf` +16/-0.
  - One local, `model_source_bucket = "opal-data-portal-v2"`.
  - One statement, `ReadTheModelReturnSeriesAndPositioning`: Allow `s3:GetObject` on exactly
    `json/benchmarks/model_portfolio_timeseries.json` and `json/positioning/positioning_data.json`.
  - No list, put, delete or wildcard.
- **Both objects exist** (head-object):
  - the series is 780,910 bytes, 11:06:27Z;
  - positioning is 6,890 bytes, 11:06:28Z, AES256.
  - No KMS grant is needed.
- **Firm boundary:** the bucket is firm-neutral, so no partner firm's bucket is touched (CLAUDE.md section 5).
- **Rule 30:** these are existing objects of an existing pipeline, not a new address.

## Blast radius and rollback (both branches)

- **Applied:** the resident role can read two firm-neutral objects. It can write nothing, and no served output moves.
- **Not applied or reverted:** the scoped plan `0 to add, 1 to change, 0 to destroy` removes exactly that statement and the local
  (packet section 5).
- **Apply path:** `safe-apply` on the saved scoped plan (packet section 4), never `put-role-policy`.

## Signature

SIGNED, CTO half, bound to the packet blob and sha256 above.

## Re-sign on packet v2 (~18:3xZ): the whitespace re-pin

- **Why:** IB2 stopped TO-APPLY-MODELGRANT at step 3, because `terraform fmt -check` read rc 3 at pin 50f7c709af.
- **New pin:** 680818fdb3e (merged 77fe78d8c41).
- **Read here:** `git diff -w 50f7c709af2 680818fdb3e -- infra/aws/terraform/investor-reporting/ycharts/resident.tf` is empty, so
  the change is whitespace only. The statement, the two keys and the one action are unchanged.
- **Packet v2:** @608c4a61ab, blob 640730617653ece3db71fe240737473ef80af1d0, sha256
  b348b84f33e3b0941e1fd654d943bf990b11d15e39dbb6816eae7d8270013d6c (measured at HEAD).

SIGNED, CTO half, bound to packet v2's blob and sha256 above. The v1 binding is superseded.
