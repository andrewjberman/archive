# IRPT_ANLREQ release 28 -- ADDENDUM 1b: the synthetic internal viewer carries NO allowedFirmIds -- never-widen pair, COO half

**WRITTEN, NOT APPLIED. No order change is cut on this file until the CTO half is signed on this file's blob.**
COO half: `2.0.0_SA_COO~Y2`, dell2, 2026-10-14. CTO half: owed, by `1.0.0_SA_CTO~DELL2`, bound to this file's blob.
It amends section 3 of Addendum 1 (`NEVER_WIDEN_PAIR_ANLREQ_RELEASE28_ADDENDUM_1_D1D4_INTERNAL_VIEWER.md`, COO blob `909ca2c466`, CTO half @daf0a6043e) and nothing else. Sections 1, 2, 4 to 8 of Addendum 1 stand.

## 1. Why (RECORD, AQ2 msg 7513, read at the code)

Addendum 1 section 3 specified an internal viewer row with `allowedFirmIds ["49financial"]`. The applier `0.7.0_AE_CloudOps~AQ2` read the door before any live act: `infra/aws/lambda/investor-reporting/_authz/served.py :1079-1081` (`_create_owner`): a caller whose profile has `allowedFirmIds` containing the tenant, with NO `advisor_email` in the query, is refused (`ProspectOwnershipRefused`, answered NOT_AUTHORIZED at D1), pinned by `_authz/tests/test_served_on_behalf_create.py` `test_served_refuses_advisor_email_absent`. Naming an advisor needs a partner row, which Addendum 1 forbids. Run as written, the sitting would stop at D1 and prove nothing. When the profile has NO `allowedFirmIds` attribute, the door takes `access.prospect_owner()` (`served.py :1082`): the normal path of an Opal viewer uploading into a concrete data firm (`_scope/interactive_access.py :123-137`).

## 2. The change (and only this)

Addendum 1 section 3 reads: "... `allowedFirmIds` `["49financial"]` and nothing else". It now reads: **the users PROFILE row carries NO `allowedFirmIds` attribute at all.** Everything else in section 3 stands: the address `irpt-r28-iv-<YYYYMMDD>@opal.invalid`, written with `attribute_not_exists(PK)`, `status` the exact string `active`, the user class the authorizer reads as an INTERNAL human, no partner row, ONE RS256 token with `exp` at most 20 minutes after `iat`, held in the lane's process only, never written, never logged.

## 3. Blast radius of the change

- The row is an internal-class viewer WITHOUT a firm list, so the on-behalf firm restriction does not apply to it; the only limits on what its token can do in 20 minutes are the lane's own script and the order: the door's route, `selected_tenant=49financial`, four requests, synthetic files. No other route, no other firm, no second token (Addendum 1 section 5, order `TO-EXERCISE-R28b` bounds). The token is never written or logged and the row is deleted after `exp` and read ABSENT by the GSI and a ConsistentRead.
- Stored inputs: the same two synthetic inputs in 49financial's intake store (D2, D3), now attributed to the internal viewer's principal (a prospect owner in firm 49financial) instead of an advisor; named in the report; NOT deleted by the lane (Andrew's word).
- No authorization change is released; the row is created for the sitting and removed.

## 4. Both branches

- **D1 answers NOT_AUTHORIZED anyway:** STOP at once, remove the row, report the classifier code; no other identity is tried without a new addendum.
- **The door admits and a case answers other than expected:** as Addendum 1 section 6.

## 5. Owed

1. The CTO half on this file's blob (one line is enough).
2. After it: an amendment to `TO-EXERCISE-R28b` naming this identity (this seat cuts it).
