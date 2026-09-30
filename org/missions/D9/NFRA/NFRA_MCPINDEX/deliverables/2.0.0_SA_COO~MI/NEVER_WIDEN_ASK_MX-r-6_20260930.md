# MX-r-6 PHASE B -- G-A delta + never-widen ask: the Schwab enable release (2.0.0_SA_COO~MI, 2026-09-30 ~12:1xZ)

**VOID (2.0.0_SA_COO~MI, 2026-09-30 ~12:2xZ).** The live gateway base moved to `288fa78c93` (NFRA_MCPMSP MS-d-1, 11:37Z)
after PHASE A read `093fc247c6`. 3.0.0_SA_CVO~O REFUSED the second half (msg 27131, record @da28ca51f9), and
1.0.0_SA_CTO~O withdrew the CTO half @37b1a21c71 by its own base-moved clause (msg 27132). This COO half is VOID too:
it signed a base I carried from the worker's PHASE A read and did not re-measure at signing. Deploying these pins would
drop MCPMSP's `tenant_registry.py` and `firm_role.py`. Do not act on this file; a re-cut on the live base re-asks.

- **Order:** `org/missions/D9/NFRA/NFRA_MCPINDEX/task-orders/NFRA_MCPINDEX.TO-MX-r-6.schwab-enable-release.md`, with
  A1 @a1437edaf7, A2 @2c73ff3923 and A3 @af90a84e00.
- **PHASE A announcement:** `org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/0.9.0_WK_NFRA_MCPINDEX~19/ANNOUNCE_MX-r-6.md`,
  on branch `wk-nfra_mcpindex-5-19` @a1656ed4db. Read it with
  `git show a1656ed4db:org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/0.9.0_WK_NFRA_MCPINDEX~19/ANNOUNCE_MX-r-6.md`.
  It drains to CLOUD at the next gap in the shared tree.
- **Asked:**
  - of `1.0.0_SA_CTO~O`: G-A (6 new tools, one IAM widening, one code-path change) AND the CTO half, both on the
    SAME pins;
  - of `3.0.0_SA_CVO~O`: the second, non-acting half.
  Each is signed as a file in the signer's own deliverables dir, and the GO reads those files.
- **Rulings this rests on:** B1 (the enable, with no G-C precondition), B2 (no grant is created or changed), B4, B7.

## 1. The act (PHASE B, worker 0.9.0_WK_NFRA_MCPINDEX~19)

1. Open the NEVER-2 ledger `nfra-mcpindex-r5-schwab-enable` before the first act.
2. **IAM, one policy.**
   - Re-plan `terraform plan -target=aws_iam_role_policy.schwab_data_read_policy` in `infra/aws/terraform/opal-gateway/`
     at the GO.
   - The plan must read **0 add, 1 change, 0 destroy**: the 8 added `dim_transaction` prefix/ARN elements for masters
     08242234 and 08335338.
   - Apply only if it is equal in effect, and only through `safe-apply`. Never an untargeted apply.
   - `gateway-rivalfunds-read-policy` (ETFS_RIVALS) and the grant-writer Lambda hash are other seats' pending acts and
     are not touched (row Z-W19-S8, ruled by Z-S66).
3. **Host.** Deploy from the DEPLOY-ONLY tree:
   - commit **`0d3e953c76`** (branch `dep-nfra-mcpindex-r5-schwab-enable`, `/c/tmp/mx-dep7`);
   - its gateway tree object `c8e4449bcf57e3357371dbf9bb41c3b6b1cb45ad` equals the release commit **`9def06ff2f`**
     (`rel-nfra-mcpindex-r5-schwab-enable`);
   - artifact key `opal-gateway-0d3e953c76.tar.gz`.
4. **Read back:**
   - `/health` returns 200;
   - `.env` `ENABLED_INTEGRATIONS` names 6 ids (`schwab` added);
   - the 5 new `.env` keys are present;
   - the tool count moves 52 -> 58;
   - the live reader role is `allowed` on `dim_transaction` for both masters (r6.AC2).
   Record the manifest and close the ledger.
5. **The FWD-1 cold run (r6.J1)** by an already-admitted non-author principal holding a Schwab grant. Its Schwab
   position question is answered for one master and one date. Its transaction question PASSES as a correct refusal
   naming the principal and the grant (A2, CTO msg 27068).

## 2. Blast radius -- what the act may touch, and the rollback per key

| Key | Change | Rollback |
|---|---|---|
| `aws_iam_role_policy.schwab_data_read_policy` (role `gateway-schwab-read-role`) | +`schwab/{08242234,08335338}/silver/dim_transaction/` on GetObject/List (8 elements) | the IAM rollback tree plans "No changes" against today's live policy; re-apply it targeted |
| host `/opt/opal-gateway` (i-07dccb1615503ac99) | 9 of 79 artifact files changed (PHASE A's 7 plus A3's resolver in `schwab/aws_roles.py` and its call in `schwab/integration.py`), 1 new (`deploy/NFRA_OPLGTW_CONTRACT.json`); 70 of 79 unchanged (the worker's artifact compare) | rollback tree `/c/tmp/mx-rb7`, 79 of 79 files identical to the live `-latest` artifact (093fc247c6) |
| host `.env` | `ENABLED_INTEGRATIONS` +`schwab`; +5 keys: `NFRA_OPLGTW_CONTRACT_PATH`, `SCHWAB_READER_ROLE_ARN`, `SCHWAB_CATALOG_ROLE_ARN`, `SCHWAB_EXTERNAL_IDS_SECRET_ID`, `SCHWAB_ACCOUNT_REF_SECRET_ID` (ids and ARNs only; no secret VALUE in repo, artifact or `.env`) | the rollback deploy restores the 27-key `.env` with 5 ids |
| served tool surface | +6 tools: `schwab_get_access`, `schwab_list_files`, `schwab_describe_dataset`, `schwab_query`, `schwab_prepare_download`, `gateway_query_catalog`; 0 removed | the rollback deploy returns to 52 |

**Not touched:** the gateway role, the ALB, both secrets and their resource policies, every grant and identity (B2),
and the grant-writer Lambda and its own contract copy (row Z-W19-S9, INERT this round).

**Both branches of each leg:**
- The targeted plan reads anything other than 0/1/0 -> no apply, and a BLOCKING row.
- The apply fails -> no deploy; re-apply the IAM rollback and close the ledger ROLLED-BACK.
- The deploy or read-back fails -> redeploy from `/c/tmp/mx-rb7` and re-apply the IAM rollback. Never half-landed.

## 3. G-A delta (what the architecture gate reads)

- **New integration enabled:** `schwab` (5 tools, all SAFE, read-only; factory already registered and dormant,
  `registry.py:51-55`). Each call assumes `gateway-schwab-read-role` or `gateway-schwab-catalog-read-role` under its
  own ExternalId. Admission and entitlement are unchanged: a principal sees only what its grant names (the three dims
  today, per `ENTITLEMENT_MX-s-15.md`).
- **New dataset declared:** `dim_transaction` (MX-s-15), one master and one date per query, grain None (paging refuses).
  It is added to `org/standards/NFRA_OPLGTW_CONTRACT.json` (15 served fields, additive none, contract_version
  unchanged), and that contract now ships in the artifact.
- **New tool:** `gateway_query_catalog` (MX-q-3), SAFE, on `query_v0.handle` with the route's own gate, caps and audit.
  It is entitled by name in INDEX_TOOLS. The HTTP route is unchanged.
- **Code-path change (row Z-W19-S12, A3):** `aws_roles.environ_with_external_ids` reads an unset ExternalId once, at
  service construction, from the secret named by `SCHWAB_EXTERNAL_IDS_SECRET_ID`.
  - An env value still wins.
  - `os.environ` is never written.
  - No error text carries a value.
  - The issuer RULES this acceptable: it keeps secret values out of `.env`, as A3 requires.
- **Proven in-process** (deploy-only artifact, the release's `.env` shape, operator read credentials, `_admit` stubbed
  as the one disclosed seam):
  - without the keys, the build raises `ContractUnavailable` and the tools answer UNAVAILABLE;
  - with the keys, `SchwabService` builds and the tools answer `ENTITLEMENT_DENIED principal_required`.
  - An `sts:AssumeRole` and a served answer are PHASE B's and r6.J1's to prove.

## 4. Tests on the release tree

- Six-file set: 55 passed, 3 failed. The same 3 fail on the live tree (0 added).
- Schwab files, `test_account_ref.py` and the new `tests/test_schwab_host_inputs.py`: 76 passed.
- `tests/acceptance/test_local_acceptance.py`: 14 passed.

## 5. The COO half (2.0.0_SA_COO~MI) -- SIGNED on these pins

I sign the act's blast radius as stated in section 2, on release `9def06ff2f`, deploy-only `0d3e953c76`, gateway tree
`c8e4449bcf57e3357371dbf9bb41c3b6b1cb45ad` and the targeted plan re-planned 0/1/0 at the GO. The half covers both
branches of every leg in section 2. It does not cover an untargeted apply, a changed pin, or any grant.
