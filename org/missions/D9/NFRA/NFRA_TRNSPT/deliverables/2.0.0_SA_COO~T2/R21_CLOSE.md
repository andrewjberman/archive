# NFRA_TRNSPT round 21 -- close record: the first scheduled meeting landed wiped; the silver-only reader is live; the gateway may write the deck (2.0.0_SA_COO~T2, dell2, 2026-10-09)

Issuance `da995dba71` (decomposition `decompositions/NFRA_TRNSPT_DECOMP_R21.md`, CTO ADDENDUM 12 + 12.1). Amendments: AMENDMENT 1 @f613876eed,
AMENDMENT 2 (park) @68750c9d95, AMENDMENT 3 @c1ef86dfb7. `round-close-check --round 21` MAY-CLOSE.

| cell | merged / act | what exists |
|---|---|---|
| TR-m-21 (D2-S12) | 4e29ac38d5 | `lambda-source-map.json` maps the 3 `aws_lambda_function` resources of the transcripts root (live sha + deployed commit for the two pulls; commentary marked not yet applied) |
| TR-g-21 (D2-S12) | tag on origin | `transcripts-v1.0.0` -> 4e29ac38d5 (annotated fe3e0aad38), pushed by 0.0.0_AB_MSTR~DELL2 |
| TR-r-21 (FWD-5) | 7a834056a8, AMEND 1 7c5ea4b740, AMEND 2 365a08577e | silver-only reader role: GetObject on Teams + outlook silver, research_meeting DENIED (D2-W2-S10 ruled by D2-S13), decrypt-only key statement via S3, trust = the raw-tier readers (CTO ruling 3248) |
| TR-a-21 (FWD-5) | TO-APPLY-s21 complete 483697155e | applied by laptop 0.7.0_AE_CloudOps~TRL 14:07:33Z (3/1/0, key diff only SilverReaderDecryptOnly); issuer proof `R21_SILVER_READER_PROOF.json` @f8a19f80e4: silver 200, bronze AccessDenied, research AccessDenied |
| TR-k-21 (FWD-6) | b74b1e45bd | `GatewayWritesTranscripts`: GenerateDataKey + Encrypt for the gateway role (via the opal-gateway root's output, no typed ARN), via S3 to this bucket; no decrypt |
| TR-ka-21 (FWD-6) | TO-APPLY-ka21 complete (proof @a3e5c43506) | applied by ~TRL 16:44:04Z (0/1/0, key 5 -> 6 Sids, added only that statement); issuer live read: 6 Sids, both conditions. Step 1 found NO S3 write grant for the gateway role on this bucket; the prefix grant is site Z's OG-ab-2 |
| TR-p-21 (FWD-1/2/3) | `R21_FIRST_SCHEDULED_LANDING.json` @7cdd125f18 | D2-S11 re-probe 3/4 admitted (row D2-S14); the 16:00Z SCHEDULED fire landed 1 monday_meeting bronze -> silver: 436 rows, 98 held out, residual re-wipe 0, planted control discriminates, wall-clock 'absent' (interim). The 17:00Z fire landed nothing new (no re-land) |

**Rows:** D2-S12 closed by TR-m/g-21. D2-W2-S10 ARMED, disarmed same turn by D2-S13. D2-S11's host-allowlist half resolved by D2-S14. W1-S9 OBSERVATION (naming gate refused a `pipeline` field; dropped).

**Carried / open:**
- **FWD-1/2/3:** graded at this round's analysis on the CVO slug (CTO fold @4d1a177002); the research meeting is the one excluded case
  (organizer grant, Andrew).
- **FWD-5:** grades on Andrew's own read through the role.
- **FWD-6:** TR-d-20 PARKED until site Z's OG-ab-2 (generalised site_to_s3 + its PutObject on the market_update prefix) lands the deck;
  un-park on its sha256.
- **FWD-8:** a18's admitted read is at site Z (Opal_Terminal). Its refused half is measured on dell2 (AccessDenied).
- **FWD-9:** IRPT_ANLREQ TO-APPLY-t1 is applying (step A landed; A2's registry row ACTIVE @103902e75d).
- **Wall-clock:** site Z's metadata route (@7f58eb8f77).
