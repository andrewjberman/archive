# NEVER-WIDEN SIGN-OFF PACKET -- IB-rtf-10 (RE-CUT, second pass): the serving roles granted the ownership map and the directory, and the bucket map on every scoped function

**For:** the two halves required before IB-rtf-10 applies anything (CLAUDE.md never-widen: CTO + COO): `1.0.0_SA_CTO` and `2.0.0_SA_COO~B`.
**Prepared by:** `0.7.0_AE_CloudOps~V` (`IRPT_BCKEND.TO-IB-rtf-10`, re-handed @2b67d4ff7a).
**Supersedes:** the first-pass packet at blob `4e7ba624fa592ea74b2649d194303ca4fc6a3b43`. A re-cut packet is a re-signature, so no half signed against that blob covers this one.
**Executes:** the CTO's ruling @606e7d14ce (`org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_RULING_IRPT_BCKEND_S90_OWNERSHIP_MAP_GRANT_20260919.md`), which ADOPTED (a) the object-scoped read and BARRED (b) the publisher copy as a duplicate output path. It also executes the issuer's rulings on rows S93, S94 and S95 (msg 98244), and the addendum (msg 98246, face status line @77bd04ca41) that adds K-CODE.

**K-CODE IS DECLARED BUT CANNOT BE SIGNED IN THIS BLOB (row S96, BLOCKING).** The builder refuses `irpt-directory-search` from HEAD, so there is no built artifact whose hash a half could sign. K-OM, K-DIR, K-ENV and the S95 restore are complete here. See section 11 for the two ways forward.

**NOTHING IS APPLIED BY THIS PACKET.** The Terraform is committed on the branch and planned per root. Line citations are at `@4ceb7f8361` unless another vintage is given.

A half signs the **blast radius** of the act: what each key may touch, and the rollback for each key. It does not sign an intention.

---

## 0. The CTO's four conditions, and where each is met

| condition | where |
|---|---|
| (1) the registry vintage the grant derives from, plus the resulting ARN list, so a new firm is a visible plan diff | section 1 (vintage) and the ARN lines in section 3 |
| (2) the `platinum/` ban comment amended in the SAME commit as the statement | `directory/iam.tf:3-14`, committed @9f21dedfd8 together with `aws_iam_role_policy.irpt_directory_ownership_map`, and carried unchanged here |
| (3) `0 to destroy`, additive only, nothing outside the seven serving roles | section 6: 7 of 7 roots `0 to destroy`; every key is a NEW resource; no existing statement is edited |
| (4) the bucket map is configuration, not a second source of truth | K-ENV is the ONE value the directory root already sets, from the same registry expression (section 3) |

---

## 1. The registry vintage (condition 1)

The grant is derived from `data/firm_registry.json`, **blob `99b8eeb54fb08a7ea6e4b89b64f300ee6cab3200`**, last touched by commit `39cbad4214` (2026-09-16). The filter is `kind == "client" && enabled`.

That yields **3 client firms**: 49financial (`opal-data-bd`), inflection (`opal-data-inf`) and cottonwood (`opal-data-cot`). `mockadv` (kind `test`) and `demo` (kind `demo`) are excluded **by kind**.

REGISTRY-VINTAGE: blob 99b8eeb54fb08a7ea6e4b89b64f300ee6cab3200

**If the registry blob at apply time differs from this, the ARN list differs.** The re-taken plan then shows it as a diff, and the canonical digest will not match section 6's. That is a STOP.

---

## 2. The census (arm (a)): the 7 serving functions, measured

| function | role | runtime loader | ownership map (3 firms) | directory (3 firms) | bucket map |
|---|---|---|---|---|---|
| `irpt-directory-search` | `irpt-directory-role` | shared `_loaders.deps` (`directory/entry.py:155`) | 0 of 3 | 3 of 3 | present |
| `irpt-status` | `irpt-status-role` | shared (`ops/entry.py:97-98`) | 0 of 3 | 3 of 3 | ABSENT |
| `irpt-holdings` | `irpt-holdings-role` | own triple with `_no_grant` (`holdings/entry.py:92-106`) | not needed, by design | 3 of 3 | ABSENT |
| `irpt-narrative` | `irpt-narrative-role` | shared (`narrative/entry.py:124-125`) | 0 of 3 | **0 of 3** | ABSENT |
| `irpt-export-render` | `irpt-export-render-role` | shared (`export/entry.py:195-196`) | 0 of 3 | **0 of 3** | ABSENT |
| `irpt-performance-adapter` | `irpt-performance-adapter-role` | shared (`performance/entry.py:110-111`) | 0 of 3 | **0 of 3** | ABSENT |
| `irpt-ycharts-generate` | `irpt-ycharts-generate-role` | shared (`ycharts/generate/entry.py:181-182`) | 0 of 3 | **0 of 3** | ABSENT |

CENSUS-OWNERSHIP-GRANTED: 0 of 21
CENSUS-DIRECTORY-READ: 9 of 21
CENSUS-BUCKET-MAP-PRESENT: 1 of 7

**Method.** `simulate-principal-policy` for `s3:GetObject`, one resource per call, with a positive control (user `Andrew_Berman`, allowed) and a negative control (`opalinvest-auth-lambda-role`, denied). The environment is read with `get-function-configuration`.

**The maps:**
- 49financial: present, AES256, VersionId `nR.FkCE1frsI9R5zRp2wJWB7vyMZ04NK`.
- cottonwood: present, AES256.
- **inflection: ABSENT** (row S94, section 8).

---

## 3. The keys: three kinds, each its own resource, each named by the builder

Every policy name below is `lib/opal_naming.py name("irpt", None, <function>, "policy", <qualifier>)`, graded CONFORMANT as `IAM_POLICY` by `grade()`. The commit-time naming gate (LGIC_ENFORCE DEC-6, ENFORCE) passed on them.

### K-OM: the ownership-map read (6 roles)

`Sid OwnershipMapReadOnly`, `s3:GetObject`, on exactly these resources, derived from the section-1 vintage:

K-OM-ARNS: arn:aws:s3:::opal-data-bd/platinum/49financial/ownership_map.json | arn:aws:s3:::opal-data-inf/platinum/inflection/ownership_map.json | arn:aws:s3:::opal-data-cot/platinum/cottonwood/ownership_map.json

| role | new resource | name |
|---|---|---|
| `irpt-directory-role` | `aws_iam_role_policy.irpt_directory_ownership_map` (directory) | `irpt-directory-ownership-map-read-policy` |
| `irpt-status-role` | `aws_iam_role_policy.irpt_status_ownership_map` (ops) | `irpt-status-ownership-map-read-policy` |
| `irpt-narrative-role` | `aws_iam_role_policy.narrative_ownership_map` (narrative) | `irpt-narrative-ownership-map-read-policy` |
| `irpt-export-render-role` | `aws_iam_role_policy.export_render_ownership_map` (export) | `irpt-export-render-ownership-map-read-policy` |
| `irpt-performance-adapter-role` | `aws_iam_role_policy.performance_adapter_ownership_map` (performance) | `irpt-performance-adapter-ownership-map-read-policy` |
| `irpt-ycharts-generate-role` | `aws_iam_role_policy.generate_ownership_map` (ycharts) | `irpt-ycharts-generate-ownership-map-read-policy` |

### K-DIR: the directory read (4 roles; GRANTED by the issuer on row S93)

`Sid ReadFirmDirectoryPrefixOnly`, `s3:GetObject`. It is the SAME prefix-scoped read `directory/iam.tf:36-38 @4ceb7f8361` already derives for the directory role, extended to the four roles that bind the shared loader, whose `load_directory` runs BEFORE the ownership read (`_authz/loaders.py:71-80`). Never ListBucket, and nothing beyond that prefix.

K-DIR-ARNS: arn:aws:s3:::opal-data-bd/investor-reporting/directory/* | arn:aws:s3:::opal-data-inf/investor-reporting/directory/* | arn:aws:s3:::opal-data-cot/investor-reporting/directory/*

| role | new resource | name |
|---|---|---|
| `irpt-narrative-role` | `aws_iam_role_policy.narrative_directory_read` | `irpt-narrative-directory-read-policy` |
| `irpt-export-render-role` | `aws_iam_role_policy.export_render_directory_read` | `irpt-export-render-directory-read-policy` |
| `irpt-performance-adapter-role` | `aws_iam_role_policy.performance_adapter_directory_read` | `irpt-performance-adapter-directory-read-policy` |
| `irpt-ycharts-generate-role` | `aws_iam_role_policy.generate_directory_read` | `irpt-ycharts-generate-directory-read-policy` |

### K-ENV: the bucket map (6 functions)

`IRPT_DIRECTORY_BUCKET_MAP = {"49financial":"opal-data-bd","cottonwood":"opal-data-cot","inflection":"opal-data-inf"}`. It is the ONE value `irpt-directory-search` already carries, from the same registry expression (condition 4). The functions: `irpt-status`, `irpt-holdings`, `irpt-narrative`, `irpt-export-render`, `irpt-performance-adapter`, `irpt-ycharts-generate`.

### K-CODE: `irpt-directory-search` rebuilt from HEAD (1 function; the addendum, msg 98246) -- BLOCKED, row S96

- **What it is.** `irpt-directory-search` rebuilt by `infra/aws/lambda/ci/build-and-upload.sh investor-reporting irpt-directory-search` from a HEAD at or after `52ffa27636`. That commit is the IB-rtf-11 fix: `directory/entry.py` reads `q`/`limit`/`selection` from the payload-2.0 shape. At the apply, the served `CodeSha256` must equal the built sha256 by content.
- **The prior LIVE state, read before the build (the rollback source):**
  - `CodeSha256 aQxATFkcdtEBvs+v/zztQBOPcbR9XH9Lzjm9kUOmhmU=`, 122693 bytes.
  - It is held in the build store at version `l4JK6aUnUgtrg.TFrxiKU8.XBM_6APl4` (05:22:21Z). Those bytes were re-downloaded and hash equal to the live `CodeSha256`.
- **The build, run 2026-09-19 ~12:28Z from worktree HEAD `bbfe5aeac3`** (contains `52ffa27636`; `infra/aws/lambda/` clean), under ledger `irpt-bckend-ib-rtf-10-k-code-build` (@e4ce69b77f, closed @a91e5bc190): **REFUSED before upload, rc=1.**
  - `ERROR: File not found: infra/aws/lambda/investor-reporting/directory/data/custodian_key_seam.json`.
  - The manifest's `files[]` for this function declares that member, but its `staged_from` does not (0 of 1). 6 of 6 sibling functions stage it from `_ids/data/custodian_key_seam.json` (pin `c28c728a30`).
  - Nothing was written: the build-store latest and the function `CodeSha256` were re-read unchanged.
  - The live zip does carry the member, but as a **CRLF hand copy** (197344 bytes), not the committed blob (191120 bytes, sha256 `87f2f92f...`).
- **The remedy** is one `staged_from` object on `irpt-directory-search`, identical to the siblings'. It is outside this order's grant; the issuer routes it (row S96).
- **Once the remedy lands:**
  - the rebuild ships the committed LF blob, so the served seam member moves CRLF -> LF (the same JSON parse);
  - the built sha256 is printed and the directory root re-planned, and that plan carries ONE code change (`module.irpt_directory_search`), with a new canonical digest.
- **Name:** no new IAM name.

PACKET-KEYS: K-OM 6; K-DIR 4; K-ENV 6; K-CODE 1 (BLOCKED, row S96 -- not signable in this blob)

---

## 4. The S95 build-store restore: RUN IN THIS PASS, so the plans in section 6 are the plans the halves sign

This follows the issuer's ruling (msg 98244): **this order deploys NO code.** Each function whose first-pass plan carried a code change had its LIVE zip downloaded (`get-function` `Code.Location`). The bytes were verified `sha256(b64) == live CodeSha256`, then uploaded to its manifest artifact key with `content-sha256` metadata equal to the live hash.

- **When and as whom:** run at 2026-09-19T12:08:42Z as `arn:aws:iam::313476888478:user/Andrew_Berman`, under ledger `irpt-bckend-ib-rtf-10-build-store-restore` (sentinel @407458fbb7, CLOSED with 4 of 4 legs @cc154f5c7c).
- **Script and output:** `restore_build_store_ib_rtf_10.py` and `IB-rtf-10_build_store_restore_output.txt`.

| function | live `CodeSha256` (= the uploaded bytes) | new artifact version (latest) | displaced (kept in the versioned bucket) |
|---|---|---|---|
| `irpt-status` | `LHprxKSP1lM3VhoP2ijEcUVCtI+yeZt8tPRkZwpRBdY=` | `QNerDSUu9GMYB0bZrjon6n_6VG9q3aR6` | `Fp_QWlcKDid_IrVgxtdbSHZoTcu5iHLx` (07:31:20Z build) |
| `irpt-narrative` | `sgolF/uXedgXpePoBoi5y1dIgOybQkgcokihEJFM+0I=` | `Pu2QRmDx58Qo3hHwVM8L_gyotsmQ8h_6` | `xJmLYKYZ6Ad5W6NMIusKtOh3QbY_IIvM` (07:29:54Z) |
| `irpt-export-render` | `4Dp6e0Vy+SfziPY+9wUSWSBS4JzS9diUtduOTxIqclQ=` | `5tV41pNz.TpJ8O1f6zZCAJ9M6BRqoYlI` | `4SHjHG9.poTQt9USOtnNtLqg393Ww1b_` (07:30:50Z) |
| `irpt-performance-adapter` | `/Cn8XUZoSn1EGBax3+/UaVjJSAQiybZQ84vRVwiRcWs=` | `KI0U8m08xPkCgvem5bLmcU2fuWwOCLzs` | `b_FS5lpcphi04WwjjlTTXT_NxIkCFomi` (07:29:41Z) |

Each read back identical, and the functions' `CodeSha256` was unchanged after the upload (4 of 4). The build store only was touched; no function was.

---

## 5. Writers of each named property (the declared plane), `W` printed

| property | W | declared writers |
|---|---|---|
| `irpt-directory-role` policies | 2 | `irpt_directory`, `irpt_directory_ownership_map` |
| `irpt-status-role` | 2 | `irpt_status`, `irpt_status_ownership_map` |
| `irpt-holdings-role` | 2 | `holdings_logs`, `holdings_firm_read` (unchanged) |
| `irpt-narrative-role` | 4 | `narrative_logs`, `narrative_news_read`, `narrative_ownership_map`, `narrative_directory_read` |
| `irpt-export-render-role` | 5 | `export_render_logs`, `export_render_evidence`, `export_render_dispatch`, `export_render_ownership_map`, `export_render_directory_read` |
| `irpt-performance-adapter-role` | 3 | `performance_adapter_logs`, `performance_adapter_ownership_map`, `performance_adapter_directory_read` |
| `irpt-ycharts-generate-role` | 3 | `generate`, `generate_ownership_map`, `generate_directory_read` |
| each function's environment | 1 | its one `yang-lambda` module |
| each function's artifact key (the build store) | 2 | `infra/aws/lambda/ci/build-and-upload.sh`, and this order's restore (section 4, once, under its ledger) |
| `irpt-directory-search` code (K-CODE) | 1 | `module.irpt_directory_search` (the directory root); its artifact key has 1 declared writer, `build-and-upload.sh`, whose input is the manifest entry row S96 names |

**The qualifier the count cannot remove** (the CTO's rtf-8 half, carried): a console or CLI write to a role policy, a function configuration or the build store is physically possible and cannot be enumerated. It is banned by NEVER-9, and a ban is not a census. `W` counts the declared plane; the rollback's own re-read covers the rest.

---

## 6. The plan per root: re-taken after the restore and K-DIR, APPLIED TO NOTHING

| root | Plan | addresses (actions) | canonical digest |
|---|---|---|---|
| directory | 1 add, 1 change, **0 destroy** | `aws_iam_role_policy.irpt_directory_ownership_map` (create); `module.irpt_directory_refresh.aws_lambda_function.this` (update: object version only, hash unchanged) | `3bc2229a2ff321832f3c204e49abafe001ac93f0c771412ed5a5c92db46938aa` |
| ops | 1 add, 1 change, **0 destroy** | `aws_iam_role_policy.irpt_status_ownership_map` (create); `module.irpt_status.aws_lambda_function.this` (update: env + object version, hash unchanged) | `a9197cc1b8bb4f796fbcff7522be08bdfab3b813814bf7b5a3a8458af8ee0e19` |
| holdings | 0 add, 1 change, **0 destroy** | `module.irpt_holdings.aws_lambda_function.this` (update: env + object version, hash unchanged) | `450a1ab86a6981a5d1269d65dfb32dbcc3442d8801a0973ab6ff96a5f12c1654` |
| narrative | 2 add, 1 change, **0 destroy** | `aws_iam_role_policy.narrative_directory_read` (create); `aws_iam_role_policy.narrative_ownership_map` (create); `module.irpt_narrative.aws_lambda_function.this` (update: env + object version, hash unchanged) | `5e0e1ed7317bdacdfd8b744e52f34331b7361cedd2c8bcb13ca914e4ea96973c` |
| export | 2 add, 1 change, **0 destroy** | `aws_iam_role_policy.export_render_directory_read`; `aws_iam_role_policy.export_render_ownership_map` (create); `module.irpt_export_render.aws_lambda_function.this` (update: env + object version, hash unchanged) | `527c2a500d1d1e32324ee6f3cc0e8d2f60b4e7357b3ae2672ae87df2f6caf80c` |
| performance | 2 add, 1 change, **0 destroy** | `aws_iam_role_policy.performance_adapter_directory_read`; `aws_iam_role_policy.performance_adapter_ownership_map` (create); `module.irpt_performance_adapter.aws_lambda_function.this` (update: env + object version, hash unchanged) | `5059fda3e68f5f5f2cd729f1d7845aaea3ee4044b5ee95cd53371d1c3ce60d37` |
| ycharts | 2 add, 1 change, **0 destroy** | `aws_iam_role_policy.generate_directory_read`; `aws_iam_role_policy.generate_ownership_map` (create); `module.irpt_ycharts_generate.aws_lambda_function.this` (update: env ONLY) | `063b9919d876ea86f8f4d3831d30ff8aa853070438b107e67721cfe12c212aeb` |

PLAN-ROOTS: 7 of 7 planned; destroy 0 of 7; changes 17
PLAN-CODE-CHANGES: 0 of 7

**K-CODE is not in these plans.** The build was refused (row S96), so `module.irpt_directory_search` plans no change: its artifact at rest equals the live `CodeSha256`. When K-CODE builds, the directory root is re-planned and its digest changes. Every other root's digest stays as printed.

- **The accepted plan noise, named.** Six object-version-only bumps with an unchanged `source_code_hash`: directory-refresh and holdings (as the issuer ruled), plus the four restored functions, whose latest version is now the restore's upload of the served bytes. **An apply re-points each function at an object whose bytes equal what it already runs, so `CodeSha256` is unchanged by construction.** Arm (e) re-reads it after the apply, 7 of 7.
- **The canonical digest** is the sha256 of the sorted resource changes (address, actions, before, after). It is the comparable identity at the apply, because a raw planfile hash differs every take. A different digest at the apply is a STOP.

---

## 7. The blast radius, both branches

**BRANCH -- GRANTED (K-OM + K-DIR + K-ENV applied):**

- **Which functions resolve scope.** `irpt-directory-search`, `irpt-status`, `irpt-narrative`, `irpt-export-render`, `irpt-performance-adapter` and `irpt-ycharts-generate` can each read the firm's directory, its ownership map and its bucket from the VERIFIED tenant. A FIRM_ADVISOR request resolves its scope and is SERVED by policy (the projected partial with `unprojected_grant` disclosed) or REFUSED by policy (`EMPTY_GRANT` or another policy code, with a `firm_id`), never UNEXPECTED.
- **Holdings** resolves to its designed `EMPTY_GRANT`.
- **The exception is S94:** inflection's absent map still reads AccessDenied (section 8).
- **The cross-firm bound holds for every key:**
  - each resource names one object or one prefix in that firm's own bucket;
  - on the shared `opal-data-bd`, 49financial's key (`platinum/49financial/...`) is the fence against `mockadv`, exactly as the CTO requires;
  - the loaders key everything by the VERIFIED tenant (`loaders.py:76, 104-105`), never by the request.
- **Nothing new is readable** beyond each firm's directory prefix and its one map object. No bucket, table, route or code changes (section 4, section 6).

**BRANCH -- NOT GRANTED (a STOP or the rollback):**

- The path stays as S90 measured it: 12 of 12 UNEXPECTED, an outage and not a refusal.
- The restored build store is harmless on this branch, because it equals what AWS already serves.

**ROLLBACK, per key:**

- **K-OM / K-DIR:** remove the resource (revert the commit), then re-apply the root through `.tools/safe-apply.sh`. Verify `simulate-principal-policy` reads implicitDeny again, per role per firm.
- **K-ENV:** revert the line and re-apply. Verify `get-function-configuration` reads no map.
- **The served behaviour:** one authenticated request reads UNEXPECTED again.
- **The build-store restore:** the displaced 07:29-07:31Z versions are kept by VersionId (section 4). Their owner re-points by re-uploading or re-building; nothing was deleted.

**K-CODE, both branches (once it is signable):**

- **Built and applied.** On the deployed route, search honours `q`/`limit` and resolve honours `selection`. Today search ignores its query and resolve answers "nothing" (row S92). The served `CodeSha256` equals the built sha256 by content. The only served-byte change besides `entry.py` is the seam member's line endings, CRLF -> LF (row S96).
- **Not built, or rolled back.** S92 stands: search ignores `q` and resolve answers "nothing". That is a wrong answer, not an outage, and not a cross-firm exposure.
- **Rollback.** Re-publish the prior live `CodeSha256 aQxATFkcdtEBvs+v/zztQBOPcbR9XH9Lzjm9kUOmhmU=` through Terraform:
  - the bytes are at build-store version `l4JK6aUnUgtrg.TFrxiKU8.XBM_6APl4`; re-upload them as the latest, with `content-sha256` equal to that hash, then run `.tools/safe-apply.sh` on the directory root;
  - never `update-function-code`, and never the manifest as the source (row S89);
  - verify with `get-function-configuration` `CodeSha256 == aQxATFkc...`.

---

## 8. The S94 carve-out (issuer ruling, msg 98244)

- inflection's ownership map is ABSENT, so under the object-scoped grant without ListBucket an inflection advisor's request reads AccessDenied, which the loader re-raises (`loaders.py:106-114`).
- **It is NOT this order's.** The recommendation that the producer publish an empty map for every enabled client firm is pitched to `1.0.0_SA_CTO`.
- **Arm (f) records inflection as UNEXPECTED-BY-ABSENCE with S94 cited, and does NOT count it against the token.** The token's `0 UNEXPECTED` reads over the firms whose map EXISTS, `n of N` printed. Today that is 2 of 3: 49financial and cottonwood.

---

## 9. The identity line, per arm (the CTO's standing bar)

| arm | claims a SERVED behaviour? | runs as |
|---|---|---|
| (a) census, (b) packet, (c) plan, (d) halves | **No.** A configuration census, a document check and a plan are claims about configuration, not about a served path. | the operator identity the seat holds (`arn:aws:iam::313476888478:user/Andrew_Berman`, printed by the battery) |
| (e) apply + post-apply reads | **No.** It is a claim about what is DEPLOYED (policies, environment, `CodeSha256`). | the operator identity; `safe-apply`'s runtime identity is printed at the apply |
| (f) the live proof | **YES.** | **each route's own function EXECUTION ROLE.** The bounded principal's real HTTP request goes through `https://opalinvest.dev/api/scoped/investor-reporting/<route>`, and the served compute runs as the function's role (`irpt-directory-role` for search/resolve, `irpt-status-role` for status, and so on). The arm prints the route and the function and role it reached. |

**No arm certifies a served path in-process.**

---

## 10. What this packet does NOT cover

1. **S94's remedy** (the producer's map, pitched to the CTO).
2. **S92** (search and resolve read `q`/`selection` from the top level of the payload-2.0 event). The code fix is IB-rtf-11's (drained @52ffa27636). This packet deploys it only through K-CODE, once row S96 clears. Until then, (f) records S92 on the directory route by output and does not count it as UNEXPECTED.
2a. **The manifest remedy for S96** (one `staged_from` object in `infra/aws/lambda/ci/lambda-source-map.json`). It is not this order's write.
3. **Holdings serves nothing to an advisor by design** (`_no_grant`, IB-rt-7). The CTO owns that decision (ruling @606e7d14ce).
4. The two LGIC firm buckets, any bucket policy, any code rebuild, any `_authz/` or Lambda source change, and **FWD-11**.
5. The pre-existing `terraform fmt` deltas in the edited files (the new lines are fmt-clean).

---

## 11. What the halves sign against

This file's blob. Each half names that blob, as `NEVER_WIDEN_SIGNOFF_COO_HALF_IRPT_BCKEND_IB-rtf-10_*.md` (`org/tier1_exec/2.0.0_SA_COO~B/deliverables/`) and `NEVER_WIDEN_SIGNOFF_CTO_HALF_IRPT_BCKEND_IB-rtf-10_*.md` (`org/tier1_exec/1.0.0_SA_CTO/deliverables/`).

If either half is ABSENT, arm (d) STOPS; that is the expected second-pass outcome. The third pass runs (e) and (f).

**Two ways forward on K-CODE. The issuer chooses; this seat recommends (i).**

- **(i) Remedy S96 first (recommended).** The one `staged_from` object is added, then this seat rebuilds `irpt-directory-search` under a new ledger, prints the built sha256, and re-plans the directory root. The packet is re-cut ONCE with K-CODE complete, and the halves sign that blob only, so no half is spent on this one.
- **(ii) Sign this blob now for K-OM, K-DIR and K-ENV.** K-CODE then goes in its own packet and its own apply after S96. That means two signatures and two applies on the directory root.
