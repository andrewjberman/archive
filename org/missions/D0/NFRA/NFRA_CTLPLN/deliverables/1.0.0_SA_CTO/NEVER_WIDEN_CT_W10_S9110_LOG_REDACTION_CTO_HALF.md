# NEVER-WIDEN SIGN-OFF -- CTO HALF -- NFRA_CTLPLN CT-w-10: the data proxy stops writing callers' bearer tokens into its log group (S9110; THIRD pair)

**Signer:** `1.0.0_SA_CTO` (laptop) | **State: SIGNED 2026-10-12 ~11:3xZ, on the conditions in section 3** |
**Against:** `org/missions/D0/NFRA/NFRA_CTLPLN/deliverables/2.0.0_SA_COO~C/CT-w-10_PAIR_20261012.md` @f716ffd301 (53 lines, read whole)
| **Cells:** CT-w-9 @bc07b57d76, CT-w-8 @2a978fab00 | **Ruling it serves:** `CTO_RULING_NFRA_CTLPLN_S9110_DATA_PROXY_LOGS_BEARER_TOKENS_20261012.md`
@05d359964b | **Live code:** the second pair's pin 50c8feb76b (members hashed in the COO half, line 19).

## 1. The blast radius, signed (section 2 of the COO half, as written)

ONE key, K1: the code of Lambda `opal-portal-data-proxy` through its Terraform root by `safe-apply`; `lambda_handler` no longer
prints `json.dumps(event)` and prints one line `Request: method=<M>, path=<P>, request_id=<id or ->`; nothing else in the handler
changes. Branch A exactly `0 to add, 1 to change, 0 to destroy` on `aws_lambda_function.portal_data_proxy`; Branch B = anything
else, OR a zip whose member list is not exactly the three files, OR a pre-apply measure that finds a long-lived credential --
nothing applied. What the act may touch: the function's log lines from the apply on (no header, cookie, query or body
reaches the log). Lines already written stay until the 14-day retention expires; the 15-minute access tokens in them are
dead. Served behaviour on every route is unchanged. Rollback per key: the previous artifact version (the second pair's package,
recorded in the ledger entry before the upload) through the same root, one resource moved, then R1. Both branches covered.
Signed.

## 2. Rulings asked of this half

- **(b) The callers:** as the second pair's CTO half -- the walker account armed the walker's way (internal); ONE existing seed
  test row on a partner firm, armed the same way and restored byte-for-byte in the same ledger entry (partner); (a) the OW_SD2
  precedent in terms only if the walker tool cannot take a second account; "neither" refused. Nothing minted, nothing printed.
- **(c) The `firm_page_access.py` mark-only difference RIDES this apply.** Condition: the executor proves it is header-only --
  `diff` of the deployed member against the built member with the single `GENERATED ... registry@<hash>` line excluded is EMPTY,
  the count of differing lines printed (expected 1). A non-empty diff is Branch B. Holding the module back would ship a package
  whose generated header lies about its registry hash, which is the worse state.

## 3. Conditions

1. PRE, before the build: the counts over the 14-day group (JWT-shaped lines; lines with `Cookie`/`cookie`/`refresh`; lines with
   `Set-Cookie`), key NAMES only, never a value. A long-lived credential found = STOP, no build, and ONE line to Andrew asking for
   a purge of the group's events (a delete, his class); with none found, no purge, retention stays 14 days.
2. P0: the deployed package's three members hash to the second pair's pin before the build (any other = STOP).
3. The ledger entry (opened before the upload) records the previous artifact version id and the three member hashes; it
   closes only on `CodeSha256` equal to the built file's; R1 (one request, then the log line read back: method, path,
   request id and NO Authorization/Cookie/JWT bytes) recorded as counts and hashes only.

## 4. Noted, outside this pair

The portal carrier is committed as 53506d49 on the portal repo (firmAccess.ts only) with `0.0.0_AB_MSTR` asked to push DEV
under the push law; the gitlink moves after the push lands, in the issuer's lane; the 10 workspace tests that read the checkout's
`firmAccess.ts` pass on the landed file and are not a Branch-B signal for this pair.

-- 1.0.0_SA_CTO
