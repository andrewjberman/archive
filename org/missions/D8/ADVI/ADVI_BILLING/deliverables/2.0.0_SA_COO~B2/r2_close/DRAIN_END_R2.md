# ADVI_BILLING round 2 -- drain-end read (issuer `2.0.0_SA_COO~B2`, 2026-10-09 ~09:3xZ)

On the CTO's round-1 analysis @ed0aad9538 + ADDENDUM 1 @e5371f3e39 + ADDENDUM 2 @abbf204c7e.

**Orders:**
- 6 of 6 complete and merged:
  - AB-e-2 @f6eedccf4d;
  - AB-e-3 @53da6fc612;
  - AB-e-4, AB-e-5, AB-e-6 @e91337d596;
  - AB-e-1, workstream EDGEPROBE, by `0.7.0_AE_CloudOps~AB2`, ledger closed @606da36dc7.
- `round-close-check --round 2`: MAY-CLOSE (6 orders, 6 proofs OK, 0 judgment criteria). The EDGEPROBE workstream reads MAY-CLOSE as well.

## Per enrichment item

| item | outcome | measured |
|---|---|---|
| E1 book check | **already enforced at the edge; no Lambda duplicate needed** | Five live GET probes for `z08219260`: in_book 200, out_of_book 403, firm_admin 200, other_firm 403, execute_api_bypass 403 (authorizer log "Origin verification FAILED", 1 of 1 event). Record `deliverables/0.7.0_AE_CloudOps~AB2/AB_E1_PROBES.json`. Per ADDENDUM 1, a refused bypass means no Lambda check. |
| E1 map gap | producer fixed (dry); **premise thinner than stated** | The 5 registered advisorKeys now enter `d08_firm_ownership_map.py`'s universe with empty lists; 0 of 144 other advisors changed. All 5 own NO household in the source, and 2 of the 5 are `firmRole` admin, who bypass the check. The served map is written by legacy `D_00.portal_aggregates.py`, not d08, so the fix moves nothing served until that cutover. Rows D2-W4-S1..S3. |
| E2 SMArtX ingest | path built (not deployed); parser built (synthetic only) | The gateway `copy_site_file_to_s3` copies to the builder's `smartx/49financial/bronze/fee_statement/` prefix only (27 tests). The parser writes silver `smartx_fee_statement` (contract 0.1.0). No real statement has run. The tool's registration line in `tools.py` is DEFERRED to its deploy act, with the deploy's `s3:PutObject` grant and the `ADVI_FEE_STATEMENT_S3_ROOT` config. |
| E3 crosswalk | **landed** | `s3://opal-data-49financial/advi/49financial/gold/household_crosswalk/date=2026-10-09/household_crosswalk.parquet`: 6,715 of 7,620 accounts and 3,146 of 3,353 client keys; allocations partition 2026-10-02 (5 trading days behind). The seam probe matches the served summary's 2 of 2 accounts. Ledger closed. |
| E2+E3 consumer | fee_quarter v2 built, dry run only | Household from the crosswalk; SMArtX rates and true-up when a silver statement exists (none yet). Contract 0.2.0, additive. The served round-1 object is unchanged. |
| E4 FWD-3 grade | **for the CVO** | The served panel is unchanged since round 1, so the real render is round 1's (`r1_close/REAL_RUN_FWD1_R1.md` @b44766f7ef; the real PNG is private on dell2, sha256 efc9ee5e...). It shows value, schedule, days, flows, exclusions and steps per account. |

## Rows needing a ruling above the issuer

1. **D2-W4-S1..S3 (E1 map gap).** Is the served regeneration under a pair still wanted? The legacy D_00 writes the map, and the 5 advisors own no household, so adding them changes only the refusal reason. The issuer's recommendation: no served regeneration now; d08 carries the fix to its cutover.
2. **D2-S3.** The other_firm probe was refused at "missing identity claims" (`index.mjs:478-492`), before firm resolution. The CROSS-FIRM arm is ABSENT, not exercised-against. Reaching it needs a probe with complete claims for another firm's mapped advisor.
3. **D2-S2.** The issuer's order named the public-key secret; the lane minted with `opal/auth/jwt-private-key`. This is the issuer's face error, recorded.

## Armed rows whose owner I could not seat

None. `D2-W2-S3` still reads ARMED in `investigations/`. Its disarm act was done in round 1 and the CVO graded round 1 ARMED 0 in `adjudications/ADJUDICATION_v1.md`.

## Enrichment candidates for round 3 (the issuer's reading; the CTO's to set)

- Deploy the gateway tool (IAM grant, config, registration) and land the Q2 and Q3 2026 SMArtX statements to bronze, then silver.
- Re-emit `fee_quarter` v2 for `z08219260` with the SMArtX rates and true-up (served, under a ledger), and test it against the real statement (row D2-W3-S3).
- The cross-firm probe arm (D2-S3).
- A schedule for the crosswalk producer.
- The PROD push of the panel. It is Andrew's word: the page is client-facing, and the CTO's precondition, the live book check, is now measured.
