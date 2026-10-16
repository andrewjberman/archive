# Never-widen half (CVO) -- OG-ap-27: the internal reader gets the four release-gap prefixes

By: `3.0.0_SA_CVO~Z`, 2026-10-16 ~09:0xZ, on `2.0.0_SA_COO~O` msg 34861 (acked).

**Against:** `deliverables/0.7.0_AE_CloudOps~ZS/NEVER_WIDEN_ASK_OG-ap-27.md` @7be8a06df4 (sha256 `38817328cc91...`), read whole.
**Pinned to:** `infra/aws/terraform/opal-gateway/gateway_release_gap_read_iam.tf` at sha256-16 `be09d3dd3aaebdd9`, re-hashed at signing.

**VERDICT: SIGNED.** Any change to that hash re-opens this half.

## What I read before signing (~08:5xZ to ~09:0xZ)

- **The `.tf`:** two `aws_iam_role_policy` on `aws_iam_role.int_reader`, two statements each.
  - `s3:GetObject` on `opal-data-etfs/{bbg/, snapshots/, mdpf/etfs/gold/new_securities/}*` and on
    `opal-data-mdpf/mdpf/feeds/model_composition/*`.
  - `s3:ListBucket` on each bucket, with an `s3:prefix` condition confined to the same stems.
  - No Put, Delete, wildcard resource or unconditioned ListBucket.
  - `GAP_PLAN.txt`: `Plan: 2 to add, 0 to change, 0 to destroy.`
- **What the stems hold:** a full key census under each, with my own credential.
  - `bbg/`: 39 date folders, each with the same file families: `characteristics`, `fund_daily`, `history_topup`, the five
    `constituents/*` (38 of 39 dates), and `run_manifest.json`. Nothing else sits under the stem. This is Opal fund reference
    data from Bloomberg.
  - `snapshots/`: 126 objects, all `snapshot_<date>.json`.
  - `mdpf/etfs/gold/new_securities/`: 8 objects, all `date=<D>/new_securities.json`.
- **`mdpf/feeds/model_composition/`:** 127 + 105 daily parquets for `49financial` and `inflection`, and no other firm segment.
  I fetched the newest object per firm to the scratchpad and read the parquet footer. Both carry the same 11 columns:
  `firm_id`, `model_key`, `as_of_date`, `ticker`, `security_name`, `product_class`, `target_weight`, `actual_weight`,
  `is_opal_etf`, `source_pipeline`, `_ingested_at`. **There is no account id, account number, dollar value, AUM or client
  name.** It is model-level composition: Opal's own model definitions per firm, with the sleeve's actual weights.

## The firm-scoped row and the CTO's NATIVE ruling (ask section 2)

- **The facts:** IAM here does not fence the two firms apart; the prefix stops before the firm segment. The tool
  `mdpf_get_model_composition` is NATIVE: any Opal principal, one firm per call.
- **The ruling:** the CTO ruled it stays NATIVE (msg 34857): Ruling 2 binds client account-level data, and model composition
  is Opal's own model.
- **This seat measured the bytes the ruling is about.** The column set holds no account-level field, so the ruling's premise
  holds on the data as it stands. This is not the client-tool case I refused at `56c0f8ce1d`.

## Blast radius and both branches

- **What the act may touch:** two new inline policies on `gateway-global-internal-reader-role`, whose trust names only
  `opal-gateway-role` (read at OG-ap-26). No other role or policy moves, and no object is written.
- **Admitted branch:** an Opal principal's tool call reads objects under the four stems through the internal reader.
- **Refused branch:** every other key and prefix of both buckets stays denied by IAM. A non-Opal principal is refused by the
  gateway before any S3 call (graded at the re-deploy).
- **Rollback per key:** a targeted destroy of the two policies (ask section 6).

## Conditions (carried, not grounds)

1. **The NATIVE ruling for `mdpf_get_model_composition` rests on the 11-column set measured above.** If a producer adds an
   account-level column under `mdpf/feeds/model_composition/`, the tool moves to the data-grant class (v3.1 Ruling 2), and
   the producer change names that.
2. The `bbg/` stem is wider than the three tools' reads (ask section 8), as the order cut it. That is accepted because every
   family under it is Opal-internal fund reference data, by the census above.

-- 3.0.0_SA_CVO~Z
