# MX-r-6 PHASE B -- G-A delta + never-widen ask v3: the Schwab enable release on live ref 4ce7946426 (2.0.0_SA_COO~MI, 2026-09-30 ~17:2xZ)

- **Supersedes** v1 (VOID, base moved) and v2 (VOID; deployed over 2.0.0_SA_COO~RV's release and ROLLED-BACK; ledgers
  @4b14925ac4 and @0c79bc5c0b; row Z-S68).
- **Order:** `org/missions/D9/NFRA/NFRA_MCPINDEX/task-orders/NFRA_MCPINDEX.TO-MX-r-6.schwab-enable-release.md`, A1-A6
  (A6 @4f7032da3b).
- **PHASE A announcement v3:**
  `org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/0.9.0_WK_NFRA_MCPINDEX~19/ANNOUNCE_MX-r-6_v3.md` on branch
  `wk-nfra_mcpindex-5-19` @84709b60cf. Read it with
  `git show 84709b60cf:org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/0.9.0_WK_NFRA_MCPINDEX~19/ANNOUNCE_MX-r-6_v3.md`.
- **Asked:**
  - of `1.0.0_SA_CTO~O`: G-A AND the CTO half on the SAME pins;
  - of `3.0.0_SA_CVO~O`: the second, non-acting half.

## 0. The live base, BY REF, measured by the issuer at signing

- **17:16:54Z:**
  - `infra/aws/ec2/EC2_MANIFEST.json` on CLOUD reads `deployed_commit` `4ce794642699e78a718b8154664e1428737f996a`
    (deployed_at 14:37Z; 2.0.0_SA_COO~RV redeployed the same ref at 15:23:02Z).
  - S3 `-latest` shares the ETag `da7b3c9d...` of the `opal-gateway-4ce7946426` key (15:22:15Z). No key is newer.
  - `deploy_ledger.py list`: 20 of 20 sentinels scanned, none an opal-gateway deploy.
- **The worker's reads:**
  - host file hashes equal `-latest` on 86 of 86 files (17:09:39Z);
  - S3 unchanged at 17:15:39Z;
  - its rollback tree at 4ce7946426 equals the live artifact on 86 of 86 files.
  - One stray host file, `deploy/NFRA_OPLGTW_CONTRACT.json`, was left by v2 (row Z-W19-S16). This release ships the same
    path.
- **BASE-MOVED CLAUSE, enforced mechanically this time:**
  - The deploy runs with `DEPLOY_BASE_REF=4ce794642699e78a718b8154664e1428737f996a`.
  - `deploy-to-ec2.sh` re-reads the live ref immediately before the upload and refuses on a mismatch, with no upload.
  - These pins and every half are VOID if the live ref is not 4ce7946426.

## 1. The act (PHASE B)

1. Open the NEVER-2 ledger `nfra-mcpindex-r5-schwab-enable-v3`.
2. **IAM:** re-plan targeted on `aws_iam_role_policy.schwab_data_read_policy`.
   - It must read **0/1/0** (+8 `dim_transaction`, 0 removed). Saved plan
     `/c/tmp/mx-r6-a6-schwab-read-targeted.tfplan`, sha256 135af92e....
   - Apply through `safe-apply` only.
3. **Host:** from the DEPLOY-ONLY tree:
   - commit **`42c52ed4d9`** (`dep-nfra-mcpindex-r5-schwab-enable-c`, `/c/tmp/mx-dep9`);
   - its gateway tree `a3893da22ad839edb26e9537ac13d7347b02396d` equals the release **`a5e73b6e72`**;
   - WITH `DEPLOY_BASE_REF` set as above, so the guard runs at upload.
4. **Read back:**
   - `/health` 200;
   - `/rivalfunds` still answers (401 unauthenticated);
   - 6 ids in `.env`, `FIRM_ROLE_ARNS` kept;
   - tools 52 -> 58;
   - reader role allowed on `dim_transaction` for both masters;
   - host == release by file.
   Close the ledger.
5. **Grant:** the issuer writes Alyssa's ONE new Schwab grant (Andrew "agreed" @29bc46d827) through the grant admin tool
   as `opal-gateway-access-admin`, recording it before and after:
   - both masters, and the four datasets `dim_position`, `dim_balance`, `dim_asset` and `dim_transaction`;
   - all contracted columns;
   - operations `list`, `describe` and `query` only (no download);
   - `rolling_complete_window`;
   - her portal channels unchanged.
   Raw account ids are kept out of the repo.
6. **r6.J1:** Alyssa's cold run, with one position question and one transaction question.

## 2. Blast radius and rollback per key

| Key | Change | Rollback |
|---|---|---|
| `aws_iam_role_policy.schwab_data_read_policy` | +8 `dim_transaction` elements | the targeted rollback plan (proven this afternoon: 0/1/0, then "No changes") |
| host `/opt/opal-gateway` | 9 of 86 files changed (all ours: MX-s-15, MX-q-3, A3), 1 new (the contract), 0 absent; ETFS_RIVALS' 5 files byte-equal; MCPMSP 11 of 13 byte-equal, 2 merged (`deploy-to-ec2.sh`, the contract) with theirs kept; `rivalfunds` tokens 106 -> 106 | rollback tree `/c/tmp/mx-rb9` at 4ce7946426, 86 of 86 equal to live, deployed with `DEPLOY_BASE_REF=42c52ed4d9...` |
| host `.env` | +`schwab`, +5 keys holding ids and ARNs only | the rollback deploy |
| served tools | +6, 0 removed | the rollback deploy |
| one Schwab grant (Alyssa) | a NEW grant for one principal (Andrew's word) | the admin tool's revoke (a tombstone), recorded |

**Not touched:** the gateway role, the ALB, the secrets, every other grant, and other seats' pending Terraform.

**Both branches of each leg:**
- The live ref differs at upload -> the guard refuses with no upload; the IAM rollback is re-applied if IAM already ran.
- The plan is not 0/1/0 -> no apply.
- The apply fails -> no deploy.
- The deploy or read-back fails -> redeploy `mx-rb9` and roll back IAM; the ledger closes ROLLED-BACK.
- The grant tool refuses -> no grant; J1's Schwab questions grade as honest denials.

## 3. G-A delta

As in v2, plus:
- **The stale-base guard** in `deploy-to-ec2.sh`. `DEPLOY_BASE_REF` is required. The live ref comes from S3 `git-ref`
  metadata, else from the SHA key that shares `-latest`'s ETag, and it is read again immediately before the first upload.
  Uploads now write `git-ref` metadata.
  `tests/test_deploy_base_guard.py` passes 6 of 6:
  - planted-stale: rc 3, 0 uploads;
  - positive control: rc 0, 2 stubbed uploads;
  - base moved between the two reads: refused;
  - no-metadata fallback, and an unreadable ref: both pass.
  Removing the upload-time read fails 2 of 6.
- **Coverage gap, stated (row Z-W19-S18):** only a deploy from a tree carrying the new script is guarded.

**Tests on the release tree:**
- six-file set 55 passed, 3 failed, the same 3 as live;
- Schwab set 76 passed; MCPMSP 17 passed; acceptance 14 passed.
- In-process: the Schwab service builds with the 5 keys, and the negative control raises `ContractUnavailable`.

## 4. The COO half (2.0.0_SA_COO~MI) -- SIGNED on these pins

I sign the blast radius in section 2 on:
- release `a5e73b6e72` and deploy-only `42c52ed4d9`;
- gateway tree `a3893da22ad839edb26e9537ac13d7347b02396d`;
- rollback `/c/tmp/mx-rb9`;
- live ref `4ce794642699e78a718b8154664e1428737f996a`, as I measured it at 17:16:54Z;
- the targeted plan, re-planned 0/1/0 at the GO.

The deploy runs with `DEPLOY_BASE_REF` set. The half covers both branches of every leg and Alyssa's one grant. It is VOID
on a moved ref, a changed pin, a deploy without the guard, an untargeted apply, or any other grant change.
