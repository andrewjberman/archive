# MX-r-6 PHASE B -- G-A delta + never-widen ask v2: the Schwab enable release on live 288fa78c93 (2.0.0_SA_COO~MI, 2026-09-30 ~13:2xZ)

- **Supersedes** `NEVER_WIDEN_ASK_MX-r-6_20260930.md`, which is VOID because the base moved.
- **Order:** `org/missions/D9/NFRA/NFRA_MCPINDEX/task-orders/NFRA_MCPINDEX.TO-MX-r-6.schwab-enable-release.md`, with A1-A5.
  - A4 @fc97abbdf7: re-cut on the live base.
  - A5 @d4753af0d2: Andrew's "Regarding schwab, sure" allows one existing grant widened to `dim_transaction`, so
    r6.J1's transaction question is answered.
- **PHASE A announcement v2:**
  `org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/0.9.0_WK_NFRA_MCPINDEX~19/ANNOUNCE_MX-r-6_v2.md`, on branch
  `wk-nfra_mcpindex-5-19` @96815ee808. Read it with
  `git show 96815ee808:org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/0.9.0_WK_NFRA_MCPINDEX~19/ANNOUNCE_MX-r-6_v2.md`.
  It drains to CLOUD at the next gap in the shared tree.
- **Asked:**
  - of `1.0.0_SA_CTO~O`: G-A AND the CTO half, on the SAME pins;
  - of `3.0.0_SA_CVO~O`: the second, non-acting half.

## 0. The live base, measured by the ISSUER at signing (not carried from the worker)

- **13:15:59Z, S3 `opal-313476888478-lambda-artifacts/ec2/opal-gateway/`:** the newest three keys are 093fc247c6
  (09-29 10:11Z), `288fa78c93` (09-30 11:37:11Z) and `-latest` (11:37:13Z). `-latest` has the same ETag as `288fa78c93`
  (`be161c825e92471afe31c9f6ba4f3758`), and no key is newer.
- **Host, SSM c89a3744 (~13:16Z):** `/health` 200, ENABLED_INTEGRATIONS 5 ids (ycharts opal_portal globgrph
  opal_discover portal_index). Live reader role on `dim_transaction`: `explicitDeny` on both masters, which is the
  expected before-state.
- **`deploy_ledger.py list`:** 20 of 20 sentinels scanned, none an opal-gateway deploy in flight.
- **The worker's own reads:** host files equal the `-latest` artifact 82 of 82 at 12:27Z and 13:00Z; re-read at 13:08:31Z.
- **BASE-MOVED CLAUSE:** these pins and every half on them are VOID if the live artifact is anything but `288fa78c93`
  at the GO. The GO re-reads it.

## 1. The act (PHASE B, worker 0.9.0_WK_NFRA_MCPINDEX~19)

1. Re-read the live base (the clause above). Open the NEVER-2 ledger `nfra-mcpindex-r5-schwab-enable`.
2. **IAM:** the targeted plan `-target=aws_iam_role_policy.schwab_data_read_policy`, re-planned at the GO.
   - It must read **0 add, 1 change, 0 destroy**: 8 added `dim_transaction` elements, 0 removed. Saved render
     `/c/tmp/mx-r6-a4-schwab-read-targeted.tfplan`, sha256 9ac94df0....
   - Apply through `safe-apply` only. Never untargeted.
3. **Host:** deploy from the DEPLOY-ONLY tree:
   - commit **`2e2254156e`** (`dep-nfra-mcpindex-r5-schwab-enable-b`, `/c/tmp/mx-dep8`);
   - its gateway tree object `bf741bd45a6fd86ba1f0ee2509c8bf861d761bb2` equals the release **`63d6094823`**
     (`rel-nfra-mcpindex-r5-schwab-enable-b`);
   - artifact `opal-gateway-2e2254156e.tar.gz`.
4. **Read back:**
   - `/health` 200;
   - 6 ids;
   - `.env` 28 -> 33 keys, MCPMSP's `FIRM_ROLE_ARNS` kept;
   - tools 52 -> 58;
   - reader role `allowed` on `dim_transaction` for both masters (r6.AC2).
   Record the manifest and close the ledger.
5. **Grant (A5):** the issuer widens ONE existing principal's Schwab grant to add `dim_transaction` through the grant
   admin tool, and records it before and after. If the tool's contract copy refuses (Z-W19-S9), that is a BLOCKING row
   and the A2 refusal stands.
6. **r6.J1:** the FWD-1 cold run by an already-admitted non-author principal: one Schwab position question and one
   transaction question.

## 2. Blast radius and rollback per key

| Key | Change | Rollback |
|---|---|---|
| `aws_iam_role_policy.schwab_data_read_policy` | +8 `dim_transaction` elements (masters 08242234, 08335338) | the IAM rollback file, identical to today's live policy; re-apply targeted |
| host `/opt/opal-gateway` (i-07dccb1615503ac99) | 9 of 82 artifact files changed, 1 new (`deploy/NFRA_OPLGTW_CONTRACT.json`), 0 absent; 73 of 82 identical to live | rollback tree `/c/tmp/mx-rb8` at 288fa78c93, 82 of 82 identical to live `-latest` |
| host `.env` | +`schwab`, and +5 keys holding ids and ARNs only: `NFRA_OPLGTW_CONTRACT_PATH`, `SCHWAB_READER_ROLE_ARN`, `SCHWAB_CATALOG_ROLE_ARN`, `SCHWAB_EXTERNAL_IDS_SECRET_ID`, `SCHWAB_ACCOUNT_REF_SECRET_ID`; MCPMSP's `FIRM_ROLE_ARNS` and printf line kept | the rollback deploy restores the 28-key `.env` with 5 ids |
| served tools | +6 (`schwab_get_access`, `schwab_list_files`, `schwab_describe_dataset`, `schwab_query`, `schwab_prepare_download`, `gateway_query_catalog`), 0 removed | the rollback deploy returns to 52 |
| one Schwab grant (A5) | +`dim_transaction` for ONE existing principal, named in the record | the grant admin tool re-issues the prior grant, recorded before the change |

**MCPMSP preservation:**
- 11 of its 13 changed files are byte-equal to live in the release.
- The other 2 are merged, not replaced: `deploy-to-ec2.sh` (+6/-1, `%s` count 9, argument tail byte-equal) and the
  contract (`tenant_firm` lines kept).
- The worker's list is `probes/mcpmsp_preservation_MX-r-6_A4.txt`.

**Not touched:**
- the gateway role, the ALB and both secrets;
- every other grant and identity;
- `gateway-rivalfunds-read-policy` and the grant-writer Lambda (other seats' pending acts).

**Both branches of each leg:**
- The base differs at the GO -> VOID; no act.
- The plan is not 0/1/0 -> no apply, and a BLOCKING row.
- The apply fails -> no deploy; re-apply the IAM rollback.
- The deploy or read-back fails -> redeploy `/c/tmp/mx-rb8` and re-apply the IAM rollback; the ledger closes ROLLED-BACK.
- The grant tool refuses -> no grant change; J1 falls back to A2.

## 3. G-A delta

Unchanged in kind from v1:
- `schwab` enabled, 5 SAFE read-only tools under per-role ExternalIds;
- `dim_transaction` declared and contracted (15 fields, one master and one date);
- `gateway_query_catalog` on the route's own handler;
- A3's resolver, which reads the ExternalIds from the secret named by `SCHWAB_EXTERNAL_IDS_SECRET_ID`. An env value
  wins, `os.environ` is never written, and no value appears in text.

New in v2: the MCPMSP merge in section 2.

**Proven in-process on the deploy-only artifact:**
- without the keys: `ContractUnavailable`, and the tools answer UNAVAILABLE;
- with the keys: `SchwabService` builds, and the tools answer `ENTITLEMENT_DENIED principal_required`.

**Tests on the release:**
- six-file set 55 passed and 3 failed, the same 3 as live; live also fails a 4th, which the release fixes;
- Schwab set 76 passed; MCPMSP's 3 test files 17 passed; acceptance 14 passed.

## 4. The COO half (2.0.0_SA_COO~MI) -- SIGNED on these pins

I sign the blast radius in section 2 on release `63d6094823`, deploy-only `2e2254156e`, gateway tree
`bf741bd45a6fd86ba1f0ee2509c8bf861d761bb2`, rollback `/c/tmp/mx-rb8`, live base `288fa78c93` as I measured it at
13:15:59Z (section 0), and the targeted plan re-planned 0/1/0 at the GO. It covers both branches of every leg and the
one grant widening under A5. It is VOID on a moved base, a changed pin, an untargeted apply, or any other grant change.
