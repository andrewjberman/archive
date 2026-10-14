# IRPT_ANLREQ release 28 -- ADDENDUM 1: the door steps D1 to D4 and C1 re-run as ONE synthetic Opal-internal viewer -- never-widen pair, COO half

**WRITTEN, NOT APPLIED. No order exists and none is cut on this file until the CTO half is signed on this file's blob.**
COO half: `2.0.0_SA_COO~Y2`, dell2, 2026-10-14. CTO half: owed, by `1.0.0_SA_CTO~DELL2`, bound to this file's blob (CTO msg 7505: "Write the addendum ... I sign the CTO side on receipt").
Addendum to the release-28 pair (`NEVER_WIDEN_PAIR_ANLREQ_RELEASE28_FWD1_CONSOLIDATED_FOUR_LEG.md`, COO blob `e9bb20d7fe2f6d610c88c4399e6a4387af5e7743`, CTO half @d3adae2fc8, all four legs closed). It changes nothing in section 3 or 4 of the pair; it adds ONE caller to section 8(d) for the door steps only.

Claim words: MEASURED = this seat read it in this session; RECORD = a committed record this seat opened (named); RELAYED = carried by another seat; INFERRED = said so.

## 1. Why

The sitting of `TO-EXERCISE-R28` (RECORD, `org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r28/SITTING_RESULT.txt`, AQ2 msg 7500) passed all eight ticket-service arms live (T4a 201, T4b 400, LIST-A, LIST-B, GET-B 403, PKG-1, PKG-2 409 already attached, PKG-3 409 `REPORT_REF_ALREADY_RECORDED_OTHER`) and FAILED D1 to D4: each post to the upload door as the 49financial client-human was refused `NOT_AUTHORIZED` before the file was read, because `reports/generate_installed.py :336` composes `ports["ordinary_authorizer"]` as None, so every non-Opal viewer is refused (pinned fail-closed by `reports/tests/test_generate_installed.py :201`; row `IRPT_ANLREQ-D2-S93`, BLOCKING; the CTO ruled the producer is built next round, msg 7502). C1 parsed three bodies, but they were refusal envelopes: it proved nothing about the door's answers. So the door's NEW answers (the reader r19.3 refusal, the price-date default, the re-open) are still unproven live. The partner-advisor run of the door stays owed until the ordinary authorizer lands (a new pair).

## 2. What moves

NOTHING is released. This addendum authorizes one more SITTING with one more identity, on the same terms as section 8(d): who may call is the only change.

## 3. The identity

ONE synthetic Opal-internal viewer: `irpt-r28-iv-<YYYYMMDD>@opal.invalid` (lowercase, the sitting's date), a users PROFILE row in `opal-users-v2` written with `attribute_not_exists(PK)`, `status` the exact string `active`, the user class the authorizer reads as an INTERNAL human (`verified_internal_subject`), `allowedFirmIds` `["49financial"]` and nothing else (the on-behalf door reads `allowedFirmIds` and refuses an absent, empty or `ALL` value: RECORD, `_scope/interactive_access.py :57-76`). ONE RS256 token for it, signed with the current slot, `exp` at most 20 minutes after `iat`, held in the lane's process only, never written, never logged. No partner row. No email is addressed to it (the door sends none; if the lane finds that it does, it STOPS).

## 4. The sitting (the applier lane `0.7.0_AE_CloudOps~AQ2`)

D1 to D4 and C1 of the release-28 pair, section 5, as the order `TO-EXERCISE-R28` states them (AMENDMENTS 1 and 2 apply), with the internal viewer as the caller and `selected_tenant=49financial`, three small SYNTHETIC CSV files constructed by the lane (round numbers, no client data, kept outside the repository): D1 a two-account file under `Accnt` answers NEEDS_CORRECTION `ACCOUNT_COLUMN_SEVERAL_VALUES`; D2 a one-account file under `Acct Market Value` answers NORMALIZED; D3 a Shares file with no price date answers NORMALIZED with the previous trading day's price date (printed beside `lib/trading_calendar.py prev_trading_day`); D4 re-open of D2's stored input is accepted. C1: the bodies of D1, D2, D3 in process through `parseIrEnvelope` from the portal at `origin/PROD`, and each must be an answer body (NEEDS_CORRECTION or NORMALIZED), NOT a refusal envelope; a refusal is a FAIL of the arm, not a pass of C1. Requests at least 15 s apart; only status, the finding code and the sha256 of the body are kept.

## 5. Blast radius

- **`opal-users-v2` PK `USER#irpt-r28-iv-<date>@opal.invalid` SK `PROFILE`:** created for the sitting, deleted after `exp` (`attribute_exists`), then ConsistentRead ABSENT and the email-index (GSI) ABSENT within a printed bounded 5-minute window. Rollback: the delete.
- **The intake store for firm 49financial (the door's writes):** D2 and D3 (NORMALIZED) each store one synthetic input; D1 is turned back and stores nothing (RECORD, release-21 pair: six of eleven cases stored nothing). **These stored inputs are NOT deleted by the lane** (an S3 delete needs Andrew's word) and are NAMED in the report with their input ids; they are synthetic, small, and visible only to an Opal viewer of 49financial's inputs until the partner page exists. Rollback: none by the lane; deletion is Andrew's word.
- **No Lambda, resident, Terraform, IAM, route or code change.** No YCharts call the lane causes beyond the door's own provider resolution (the hold of CTO msg 7438 is lifted; the 02:23Z probe read 200). No real client file, identity or figure.
- **Authorization changes: none.** An internal viewer already may upload on behalf of a firm named in its `allowedFirmIds`; this identity is created for the sitting and removed.

## 6. Both branches

- **A door arm answers differently from the expected (D1 to D4):** the lane records the answer and does NOT retry with a second token; the issuer reads it. A wrong answer in D1 (a two-account file accepted) is a BLOCKING finding about r19.3 live: the CTO decides whether L3 and L4 roll back (rollback order: L4, then L3, then L1; pair section 6).
- **The viewer is refused `NOT_AUTHORIZED`:** STOP; the row is removed; the report names the classifier code. It would mean the internal path does not admit a minted internal row (INFERRED against the code), and no further identity is tried without a new addendum.
- **The token is refused at the edge or a write fails:** remove what was written, record the status, no retry.

## 7. Limits named

- This addendum proves the door's ANSWERS under an internal caller. It does not prove that a partner-firm advisor can upload (`D2-S93`), nor the FWD-1 end-to-end journey.
- The synthetic stored inputs remain until Andrew's word deletes them.

## 8. Owed before the order is cut

1. The CTO half on this file's blob.
2. An amendment to `TO-EXERCISE-R28` (or a new order to `~AQ2`) citing this addendum and naming the one identity; cut by this seat after (1).
