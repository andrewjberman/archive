# ADVI_BILLING round 3 -- drain-end read (issuer `2.0.0_SA_COO~B2`, 2026-10-09 ~10:1xZ)

On CTO ADDENDUM 3 @7f414eb19e. **Orders:** 3 of 3 complete and merged:
- AB-r-1 @41087e4406, with the portal change landed on DEV;
- AB-r-2 (workstream EDGEPROBE3, `0.7.0_AE_CloudOps~AB2`), ledger closed @8cab625508;
- AB-r-3 @9828e7761f.

`round-close-check --round 3`: MAY-CLOSE (3 orders, 3 proofs OK, 0 judgment criteria).

| item | outcome | measured |
|---|---|---|
| FWD-3 empty states | **on portal DEV @6d383958** (CTO-approved msg 3067, landed by MSTR~DELL2 msg 3073) | The CTO refused the first candidate 09bc05e9 because an absent field read as "none". The issuer's repair: only `[]` / an exact 0 read "none"; a null or absent value reads "not computed for this quarter". bun 7/7, tsc clean. |
| FWD-3 real render (for the CVO) | rendered on DEV 6d383958 with the served object | LOC `/advisor-intelligence`, CANVAS `rgb(244, 246, 250)`. Both accounts of `z08219260` show "No money moved in or out this quarter" and "Nothing excluded" (the object carries `flows_in_period: []` and `excluded_value: 0`). Also shown: household fee, per-account schedule, days, both components with reasons, 10 steps, and source notes. The fee panel passes the colour law. The real PNG is private on dell2 at `C:/dev/advi_billing_private/r3_close/r3_realrun_fee_panel.png` (sha256 `8e941d5e...`). The invented-data render `r3_fixture_fee_panel.png` sits beside this record. |
| D2-S3 cross-firm arm | **EXERCISED, refused** | An Inflection admin token with complete claims: the edge admits it (`index.mjs:468-470`) and `advi-49f-billing-read-lambda` refuses with `401 {"error": "Access denied to this firm"}` (`entry.py:135-136`). The CTO's PROD precondition (msg 2995 item 3) now reads complete. |
| E2 release packet | **handed to site Z** (MSTR to MSTR, msg 3083) | The tool is registered and outside the safe-tool set; the IAM grant is one `s3:PutObject` on the builder's `fee_statement` prefix (targeted plan 1/0/0); env line and packet `0.9.0_WK_ADVI_BILLING~7/RELEASE_PACKET_E2.md`. INTERIM from site Z (msg 3098): REC TAKE, sequenced after r29 (11:00Z) and MX-r-9, with the ruling from `1.0.0_SA_CTO~Z`. Site Z builds the required carry (row D2-W7-S1: `destructive_ops.py` / `data_entitlement.py` entries) and the deploy line, and `AE~Z` applies under its own pair. |

**Rows this round:** D2-W7-S1 (BLOCKING for the release, carried by site Z) and D2-W7-S2..S4 (OBSERVATION: the env line lives in `deploy-to-ec2.sh`; a whole-root plan cannot run from dell2; the HCL derives the address from the registry tier-home rule). AB-r-1 and AB-r-2 filed no new row; D2-S3 can be dispositioned.

**Armed rows whose owner I could not seat:** none.

**What remains for the endpoint (the issuer's reading):**
- FWD-1 is REALIZED on Andrew's PROD push, since the page is client-facing; the CTO puts that to him now that the precondition holds.
- E2 lands once site Z deploys: the issuer then lands the Q3 2026 statement with the tool, writes its silver, and re-emits `fee_quarter` v2 for `z08219260` under a pair.
- FWD-2, FWD-4, FWD-5 and FWD-6 have not started.
