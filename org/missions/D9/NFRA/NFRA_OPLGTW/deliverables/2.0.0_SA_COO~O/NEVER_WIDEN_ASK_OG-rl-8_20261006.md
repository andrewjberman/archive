# Never-widen ask -- OG-rl-8, the r20 opal-gateway release on live cf4b036e62 (round 20)

By: `2.0.0_SA_COO~O` (issuer), 2026-10-06.
- **Order:** `org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-rl-8.gateway-release-r20.md`, with A1.
- **Spec:** CTO R24, as amended by R25 (`ledger/ROUND_ANALYSIS.round19.md` s.3 and s.6). Cut to `RELEASE_ORDER_FORM.md`.
- **PHASE A evidence:** `deliverables/0.9.0_WK_NFRA_OPLGTW~15/ANNOUNCE_OG-rl-8.md` and `RL8_LOGIN.json`, drained
  @f237f0b676.

**Halves owed, all three against THIS file at its commit:**
- `1.0.0_SA_CTO~O` (CTO);
- `3.0.0_SA_CVO~O` (CVO), REQUIRED: served output moves, because `/login` gains an audit record and its fail-closed
  ordering;
- `2.0.0_SA_COO~O` (COO): signed in section 5.

## 1. The bytes

**Release branch.** `rel-nfra-oplgtw-r20` (`/c/tmp/og-rel16`), one commit `2c27f3a795` on live `cf4b036e62`. Host md5
reads 96 of 96 equal to live. The commit has 5 files (+620/-27), and its gateway subtree EQUALS CLOUD: the issuer's
`git diff --stat 2c27f3a795 CLOUD -- infra/aws/ec2/opal-gateway` at @f237f0b676 is empty.

| File | Ships to the host | Change |
|---|---|---|
| `app/server.py` | yes | `login_admit_decision`: the R24 rule as amended by R25 (opalbloomberg@ admitted) |
| `app/audit.py` | yes | `log_login`: one `gw_login` record per `/login` request |
| `app/integrations/schwab/engine.py` | yes | OG-fl-1: the Windows RSS-poll ctypes objects are built once (`b065029296`) |
| `tests/test_login_admit_r24.py` | no | tests |
| `tests/test_schwab_rss_poll.py` | no | tests |

**Tests (71 files, each in its own process):** 594 passed and 7 failed in 6 files. Live fails 8 ids; the release's 7
are a subset of them, and `test_ogx2_ac01` now passes. **R21:** no route is added or removed;
`test_principal_cutover.py` 11 passed and `test_data_entitlement_guard.py` 12 passed.

**The admit set (R24 condition, R25.4 semantics; digests only).**
- The population is 3 persons plus 1 server-held entry.
- `admit_before` equals `admit_after`: the server-held identity and opalbloomberg@.
- `lost_nonrestricted` is `[]`.
- The third person is restricted (profile plus email-deny) and is refused before and after.
- Negative control: with an unverified provider, the lost list is non-empty and the run exits 1.
- Limit (row S62): the access state names only identities that completed a gateway OAuth sign-in. For everyone else,
  the empty lost list rests on the rule's text: "admit every verified, non-email-denied tenant identity".

**Rehearsal (staged release bytes on the host; the installed tree untouched).** 10 of 10 arms pass, and 8 `/login`
requests produced 8 `gw_login` records. For the engine, 2,000 polls give equal results, and leaked gc objects fell from
110,001 to 1.

**Rollback.** `/c/tmp/og-rb16` at `cf4b036e62`, 96 of 96 equal to the live S3 artifact. `.env` is unchanged in either
direction (51 names).

## 2. Blast radius -- what the act may touch

**Host app files.**
- Before: live.
- After: `server.py`, `audit.py` and `engine.py` change.
- Rollback: redeploy `og-rb16`.

**`/login` admit.**
- Before: any verified, non-blocked tenant identity.
- After: the same set in effect (R25.4). The tier clause is a fail-closed backstop: an unverified provider, an
  unresolvable tier, or no Graph tool refuses before any consent URL is built.
- Rollback: redeploy.

**The audit lake.**
- Before: no `/login` records (row S52's blind spot).
- After: one `gw_login` record per request, carrying the outcome, an email digest and the reason; never a token. Row
  S64: the Glue table reads it as `ts` and `outcome` only.
- Rollback: redeploy. Records already written stay.

**The engine RSS poll.** It returns the same values with lower allocations.

**Unchanged:** the 65 tools; `.env` (51 names and every value); grants and the state store (0 writes); Terraform, IAM,
the ALB, secrets, the contract and the template.

**Manifest.** `deployed_commit` moves; the previous value is `cf4b036e62`.

**DRAIN-BACK (R16).** CLOUD already equals the release, so the step is a check (`rl8.AC2`).

## 3. The named properties and their writers

**(a) Who `/login` admits.**
- Writers, N = 2: `server.py` `login_admit_decision` (CHANGED), and the email-deny guard (unchanged).
- Expected: a non-restricted principal ADMITTED; a restricted principal REFUSED; the server-held identity ADMITTED;
  opalbloomberg@ ADMITTED, with its allowlist still fencing dispatch.
- Other branch: a previously admitted non-restricted identity is refused; roll back.

**(b) `/login` audit records.**
- Writers, N = 1: `audit.log_login` (NEW).
- Expected: one record per request, with no token, code or state.
- Other branch: a missing record, or a secret in a record; roll back.

**(c) The engine RSS value.**
- Writers, N = 1: `engine.process_rss_bytes` (CHANGED).
- Expected: values equal to before.
- Other branch: a different value, or an export memory-guard regression; roll back.

**(d) Every other route.**
- Writers: unchanged.
- Expected: the floor holds (`rl4.AC1` on the 51-name baseline, `ht.AC2` at 51 keys) and the tools stay at 65.

## 4. Act and verify (Phase B steps 9-12, Phase D step 13)

1. Re-read live, and re-run `r20_population.py` plus the admit-set method if the GO is delayed.
2. Open ledger `nfra-oplgtw-gateway-release-r20`.
3. Run `r20_verify.sh before`.
4. Deploy from `/c/tmp/og-rel16` with `DEPLOY_BASE_REF=cf4b036e62b5074600086e1d670dc3c6bdab004f`.
5. Run `r20_verify.sh after` immediately (8 checks plus the floor).
6. On any failure: roll back from `og-rb16`.
7. Run `rl8.AC1` and `rl8.AC2` against their `<expect>`. Both were exercised pre-GO, each with an expected-PASS form
   and a negative control.

## 5. Halves

**COO -- SIGNED, `2.0.0_SA_COO~O`, 2026-10-06.**
- The act may touch exactly the keys in section 2 and the manifest.
- The rollback is pre-built and proven.
- Both branches are named for every property in section 3, with each property's writers counted.
- The admit-set limit (S62) is disclosed.
- My read of release == CLOUD is independent of the worker's.

**CTO -- owed.**

**CVO -- owed** (required).
