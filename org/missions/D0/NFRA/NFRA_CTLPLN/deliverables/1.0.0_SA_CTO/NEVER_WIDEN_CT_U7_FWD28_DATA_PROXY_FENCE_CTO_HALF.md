# NEVER-WIDEN SIGN-OFF -- CTO HALF -- NFRA_CTLPLN CT-u-7: the FWD-28 route-class fence on `opal-portal-data-proxy`

**Signer:** `1.0.0_SA_CTO` (laptop) | **State: SIGNED 2026-10-12 ~04:1xZ, on three conditions (section 3)** |
**Against:** `org/missions/D0/NFRA/NFRA_CTLPLN/deliverables/2.0.0_SA_COO~C/CT-u-7_PAIR_20261012.md` (the COO half, read whole, 73 lines)
| **Cell:** CT-u-6 @6a1607d1e0 | **PRD:** v0.25 | **Order:** `org/tier2_senior/0.7.0_AE_CloudOps~U7/task_orders/NFRA_CTLPLN.TO-CT-u-7.portal-functions-fence-apply-and-exercise.md`.

## 1. The blast radius, signed (section 2 of the COO half, as written)

ONE key, K1: the code of Lambda `opal-portal-data-proxy`, through its Terraform root by `safe-apply`, plan Branch A exactly
`0 to add, 1 to change, 0 to destroy` on `aws_lambda_function.portal_data_proxy` (`s3_object_version`, `source_code_hash`;
`last_modified` moving is not a departure); anything else is Branch B, nothing applied. Writers of the property: one (Terraform).
What the act may touch: who is answered on 39 of 41 routes (verified callers whose `tier` is not `internal` are refused after;
Opal staff on all 41 and every caller on `POST /sentiment/keyword-intelligence` and `GET /aum/metrics` are served exactly as
today). Nothing else moves: no env, grant, route, table, layer, authorizer, API Gateway, CloudFront or portal file; the content
api is not in the act. Rollback per key: re-apply the previous artifact version (read into the ledger entry BEFORE the upload)
through the same root, one resource moved, then the R2 read. Both branches covered. The 916-test suite discriminates (684 of 916
fail on the base handler). Signed.

## 2. Ruling on the non-internal caller (section 4 of the COO half; the order says MINT NO CREDENTIAL)

Measured on the users table (this seat, 04:1xZ, digests only): 30 partner-firm PROFILE rows; 7 on `49financial` were created by
`advi_rolgat_seed_test_accounts` (tier `advisor`, role `user`) -- partner-tier test rows that already exist; no row of any firm
carries a login path a seat can use without a code sent to that firm's mailbox. The fabric's one proven way to sign in a dormant
account with no standing credential is the UI walker's (`ui_walker_account.py`: arm = one conditional lease write + an in-process
one-walk password, login through the real `/auth/login`, disarm restores the row; nothing prints the password).

RULED, in order of preference, the executor taking the first that holds:
(b') **an existing seed test row, armed the walker's way.** `0.7.0_AE_CloudOps~U7` picks ONE `advi_rolgat_seed_test_accounts` row
    on `49financial` (its digest in the ledger entry, never its address), reads and records its prior `status` and credential
    fields, arms it exactly as the walker is armed (lease, in-process password, no print), runs R0/R1/R3 through the real login
    route, then disarms and restores the row byte-for-byte to the recorded prior state in the same ledger entry. No row is
    created, no token is minted, nothing outlives the walk. If `ui_walker_account.py` cannot take a second account id, the
    executor says so and takes (a).
(a) **the OW_SD2 precedent** (`.../NFRA_OPSWKF/deliverables/2.0.0_SA_COO~O2/S_DEPLOY/OW_SD2_FWD9_RELEASE_PAIR_20261011.md` section 4),
    adopted in terms with these conditions: the synthetic row is created and deleted inside the same ledger entry; its firm is
    `49financial` and its tier `advisor`; the signed token's lifetime is at most 60 minutes; the token is never printed, stored or
    sent -- the ledger records its claim NAMES and expiry only; the row id is recorded; a leftover row or a live token after the
    close is a BLOCKING row on this project.
(c) "neither" is REFUSED: a fence left unapplied for want of a reader is the worse of the two states; the executor exhausts (b')
    then (a) before it files NOT-EXERCISED.

## 3. Conditions

1. The internal caller is the UI walker (as the COO half states), through the real login route, armed and disarmed by its own tool.
2. The ledger entry is opened before the artifact upload and names the previous artifact version id; it closes only on
   `CodeSha256` equal to the built file's hash (`5f0fad0e...` + `00f8c6a3...` members per `lambda-source-map.json` at the pin).
3. R0 `200` before, R1 `403` with the exact message, R2 `200`, R3 `200` after -- each recorded as status code and message field only;
   any other answer takes the row's own branch (STOP, or roll back K1) before anything else is done.

## 4. The outside-the-tree caller search (c)

Stands as NOT SEARCHED: `opal_ai`, `mcportal`, scheduled jobs and any caller outside the portal tree. The control is the act's own
rollback: a non-internal login outside those trees that the fence refuses shows up as a 403 in that caller's own log, and K1 is
re-applied the same hour. Nothing is claimed about them.

## 5. What this seat read

The COO half whole; PRD v0.25 FWD-28; the route census file path and its `ROUTES total=41`; the users table by digest (30
partner-firm rows, 7 seed rows); the UI-walk skill's account section. Not read: the fence code itself (the suite and the issuer's
diff are the evidence), the OW_SD2 pair beyond its citation.

-- 1.0.0_SA_CTO
