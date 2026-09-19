# NEVER-WIDEN SIGN-OFF PACKET -- IB-rtf-10: the serving roles granted the ownership map, and the bucket map on every scoped function

**For:** the two halves required before IB-rtf-10 applies anything (CLAUDE.md never-widen: CTO + COO): `1.0.0_SA_CTO` and `2.0.0_SA_COO~B`. **The CTO half is also the ruling on the design question** the issuer pitched: an object-scoped read from the serving roles, versus the map published to a directory-readable prefix by its producer.
**Prepared by:** `0.7.0_AE_CloudOps~V` (`IRPT_BCKEND.TO-IB-rtf-10` @4ceb7f8361).
**Row it answers:** `IRPT_BCKEND-S90` (BLOCKING): 12 of 12 authenticated FIRM_ADVISOR requests refused UNEXPECTED before the scope resolved, measured @e7da534cc6.

**NOTHING IS APPLIED BY THIS PACKET.** The Terraform edits are committed on the branch and planned per root; no apply happens before both halves are at HEAD naming this packet's blob. Every line citation is at `@4ceb7f8361`.

A half signs the **blast radius** of the act: what each key may touch, and the rollback for each key. It does not sign an intention.

---

## 1. The census (arm (a)): 7 serving functions, measured, not recalled

The population is the 7 functions that stage `_authz/enforce.py` (the source map's `staged_from` entries).

| function | role | runtime loader (the line) | ownership map read (3 client firms) | directory read (3 firms) | `IRPT_DIRECTORY_BUCKET_MAP` |
|---|---|---|---|---|---|
| `irpt-directory-search` | `irpt-directory-role` | shared `_loaders.deps` (`directory/entry.py:155`) | **0 of 3** | 3 of 3 | present |
| `irpt-status` | `irpt-status-role` | shared (`ops/entry.py:97-98`) | **0 of 3** | 3 of 3 | **absent** |
| `irpt-holdings` | `irpt-holdings-role` | holdings' own triple with `_no_grant` (`holdings/entry.py:92-106`) | 0 of 3 (**not needed**, by design) | 3 of 3 | **absent** |
| `irpt-narrative` | `irpt-narrative-role` | shared (`narrative/entry.py:124-125`) | **0 of 3** | **0 of 3** | **absent** |
| `irpt-export-render` | `irpt-export-render-role` | shared (`export/entry.py:195-196`) | **0 of 3** | **0 of 3** | **absent** |
| `irpt-performance-adapter` | `irpt-performance-adapter-role` | shared (`performance/entry.py:110-111`) | **0 of 3** | **0 of 3** | **absent** |
| `irpt-ycharts-generate` | `irpt-ycharts-generate-role` | shared (`ycharts/generate/entry.py:181-182`) | **0 of 3** | **0 of 3** | **absent** |

- **Method.** `simulate-principal-policy` for `s3:GetObject`, one resource per call. The positive control (user `Andrew_Berman`) is allowed; the negative control (`opalinvest-auth-lambda-role`, which has no S3 grant) is denied. The environment is read with `get-function-configuration`.
- **Ownership map read:** 0 of 21 function-by-firm pairs.
- **Bucket map present:** 1 of 7 functions.
- **Holdings needs no ownership map.** Its entry composes `_no_grant` deliberately, so every FIRM_ADVISOR resolves to an empty permitted set (`holdings/entry.py:17-25 @4ceb7f8361`, IB-rt-7's design). After the fix, a holdings request reads a POLICY refusal (`EMPTY_GRANT`, with a `firm_id`), never a served snapshot. That is named here, not changed.
- **The ownership maps as objects:**
  - 49financial: `opal-data-bd/platinum/49financial/ownership_map.json`, AES256, VersionId `nR.FkCE1frsI9R5zRp2wJWB7vyMZ04NK`.
  - cottonwood: `opal-data-cot/platinum/cottonwood/ownership_map.json`, AES256, 107 bytes.
  - **inflection: ABSENT (404)**, which is row S94 below.

CENSUS-OWNERSHIP-GRANTED: 0 of 21
CENSUS-BUCKET-MAP-PRESENT: 1 of 7

---

## 2. The keys (arm (b)): exactly two kinds, and nothing else

### K-OM: one inline policy per affected role, one statement, object-scoped (6 roles)

`sid OwnershipMapReadOnly`, `Effect Allow`, `Action s3:GetObject`, and **Resource = exactly `arn:aws:s3:::<bucket>/platinum/<firm_id>/ownership_map.json` per client firm**.

- **Derivation.** The resources come from `data/firm_registry.json`, where `kind == "client" && enabled`, the same way `directory/iam.tf:19-41 @4ceb7f8361` derives `directory_object_arns`. Today that is 3 objects: 49financial in `opal-data-bd`, inflection in `opal-data-inf`, cottonwood in `opal-data-cot`.
- **Never** an enumerated list, a `platinum/*` prefix, or ListBucket.
- **Each is its own `aws_iam_role_policy` resource**, so the rollback is one resource.

| role | Terraform address (new) | policy name |
|---|---|---|
| `irpt-directory-role` | `aws_iam_role_policy.irpt_directory_ownership_map` (directory root) | `irpt-directory-ownership-map-read-policy` |
| `irpt-status-role` | `aws_iam_role_policy.irpt_status_ownership_map` (ops root) | `irpt-status-ownership-map-read-policy` |
| `irpt-narrative-role` | `aws_iam_role_policy.narrative_ownership_map` (narrative root) | `irpt-narrative-ownership-map-read-policy` |
| `irpt-export-render-role` | `aws_iam_role_policy.export_render_ownership_map` (export root) | `irpt-export-render-ownership-map-read-policy` |
| `irpt-performance-adapter-role` | `aws_iam_role_policy.performance_adapter_ownership_map` (performance root) | `irpt-performance-adapter-ownership-map-read-policy` |
| `irpt-ycharts-generate-role` | `aws_iam_role_policy.generate_ownership_map` (ycharts root) | `irpt-ycharts-generate-ownership-map-read-policy` |

`irpt-holdings-role` gets **no** K-OM: it does not read the map (section 1).

**The policy names are the naming builder's output, never typed.** Each is `lib/opal_naming.py name("irpt", None, <function>, "policy", "ownership-map-read")`, graded CONFORMANT as IAM_POLICY by `grade()`. The commit-time naming gate (LGIC_ENFORCE DEC-6, ENFORCE) refused the first spelling, which lacked the `policy` kind (Rule 30).

### K-ENV: one environment entry per function lacking the bucket map (6 functions)

`IRPT_DIRECTORY_BUCKET_MAP = jsonencode(<firm_id -> bucket for client firms>)`, derived from the same registry expression. Its planned value on every function is exactly `{"49financial":"opal-data-bd","cottonwood":"opal-data-cot","inflection":"opal-data-inf"}`, the value `irpt-directory-search` already carries. The functions: `irpt-status`, `irpt-holdings`, `irpt-narrative`, `irpt-export-render`, `irpt-performance-adapter`, `irpt-ycharts-generate`.

PACKET-KEYS: K-OM 6; K-ENV 6

**The comment amended at the ban:** `directory/iam.tf:3-6 @4ceb7f8361` (now lines 3-14 on this branch) names the ONE `platinum/` object it admits and why. A comment that says one thing while the policy says another is S91's shape in a different file.

---

## 3. Writers of each named property (the declared plane), `W` printed

These count the Terraform resources that write each role's policy set, including the new one.

| property | W | writers (declared) |
|---|---|---|
| `irpt-directory-role` policies | 2 | `irpt_directory`, `irpt_directory_ownership_map` |
| `irpt-status-role` | 2 | `irpt_status`, `irpt_status_ownership_map` |
| `irpt-holdings-role` | 2 | `holdings_logs`, `holdings_firm_read` (unchanged) |
| `irpt-narrative-role` | 3 | `narrative_logs`, `narrative_news_read`, `narrative_ownership_map` |
| `irpt-export-render-role` | 4 | `export_render_logs`, `export_render_evidence`, `export_render_dispatch`, `export_render_ownership_map` |
| `irpt-performance-adapter-role` | 2 | `performance_adapter_logs`, `performance_adapter_ownership_map` |
| `irpt-ycharts-generate-role` | 2 | `generate`, `generate_ownership_map` |
| each function's environment | 1 | its one `yang-lambda` module declaration |

**The qualifier the count cannot remove** (the CTO's rtf-8 half, carried): a console or CLI write to a role policy or a function configuration is physically possible and cannot be enumerated. It is banned by NEVER-9, and a ban is not a census. `W` counts the declared plane; the rollback's own re-read covers the rest.

---

## 4. The blast radius, both branches

**BRANCH -- GRANTED (K-OM + K-ENV applied):**

- **Which functions start resolving scope.** Every FIRM_ADVISOR request on `irpt-directory-search` and `irpt-status` now resolves its scope. It is SERVED by policy (the projected partial with `unprojected_grant` disclosed, the rtf-2 halves' signed behaviour) or REFUSED by policy (an empty set gets `EMPTY_GRANT` with a `firm_id`), never UNEXPECTED.
- **Holdings** resolves to its designed `EMPTY_GRANT`.
- **The cross-firm bound holds** on every key:
  - each K-OM statement names one object per firm, in that firm's own bucket, under a key that carries the firm id;
  - on the shared bucket (`opal-data-bd`, 49financial with the `mockadv` alias) the key IS the fence;
  - a firm-scoped request reaches exactly its firm's map, because the loader keys the map by the VERIFIED tenant (`loaders.py:104-105`), never by the request.
- **Nothing new is readable.** The rest of each firm's `platinum/` tier stays unreadable, and no bucket, prefix, table or route changes.
- **What each role gains.** A role that already reads a firm's directory gains one more object per firm. The four roles in S93 gain the map but still cannot read the directory, so their functions still refuse UNEXPECTED (see "does NOT cover").

**BRANCH -- NOT GRANTED (a STOP or the rollback):**

- The path stays as S90 measured it: an outage for every advisor of every firm, not a refusal. **Nothing a caller can reach widens on this branch either.**

**ROLLBACK:**

- Remove each K-OM resource and each K-ENV line (revert the commit) and re-apply per root through `.tools/safe-apply.sh`.
- Verify by re-reading:
  - `simulate-principal-policy` reads implicitDeny again on every role and firm map;
  - `get-function-configuration` reads each environment without the map;
  - one authenticated request reads UNEXPECTED again.

---

## 5. The plan per root (arm (c)): re-taken with the vendored binary at 11:4xZ, after the policy rename, APPLIED TO NOTHING

| root | Plan | addresses (actions) | canonical digest (sha256 of the resource changes) |
|---|---|---|---|
| directory | 1 add, 1 change, **0 destroy** | `aws_iam_role_policy.irpt_directory_ownership_map` (create); `module.irpt_directory_refresh.aws_lambda_function.this` (update: **s3_object_version only**, S95) | `3bc2229a2ff321832f3c204e49abafe001ac93f0c771412ed5a5c92db46938aa` |
| ops | 1 add, 1 change, **0 destroy** | `aws_iam_role_policy.irpt_status_ownership_map` (create); `module.irpt_status.aws_lambda_function.this` (update: env + **CODE**, S95) | `be832de35d1ae4cde35a7d742032a62ce84d3d1f7907a9a6664f1c6ba2b4f2bb` |
| holdings | 0 add, 1 change, **0 destroy** | `module.irpt_holdings.aws_lambda_function.this` (update: env + s3_object_version, hash unchanged) | `450a1ab86a6981a5d1269d65dfb32dbcc3442d8801a0973ab6ff96a5f12c1654` |
| narrative | 1 add, 1 change, **0 destroy** | `aws_iam_role_policy.narrative_ownership_map` (create); `module.irpt_narrative.aws_lambda_function.this` (update: env + **CODE**, S95) | `2c1a4f69fd13a929e4923f1daf0a4ecbb7b8e29976777f76af00d44aa139c1f7` |
| export | 1 add, 1 change, **0 destroy** | `aws_iam_role_policy.export_render_ownership_map` (create); `module.irpt_export_render.aws_lambda_function.this` (update: env + **CODE**, S95) | `6e6e5bb7d413e823082534af4789a27f891fbb30b73b2c963789012be6236cf7` |
| performance | 1 add, 1 change, **0 destroy** | `aws_iam_role_policy.performance_adapter_ownership_map` (create); `module.irpt_performance_adapter.aws_lambda_function.this` (update: env + **CODE**, S95) | `85e3cb8828e58a58d1c130554d97b0822e41e5da93d86ad5d5c91b7b1fcb2bdc` |
| ycharts | 1 add, 1 change, **0 destroy** | `aws_iam_role_policy.generate_ownership_map` (create); `module.irpt_ycharts_generate.aws_lambda_function.this` (update: **env ONLY**) | `8277b36e4795a3d8f463a90f4e4cc74f56283871b83894bfbbcd3e5c1df43e86` |

PLAN-ROOTS: 7 of 7 planned; destroy 0 of 7; changes 13

- **Why a canonical digest rather than the file hash.** A raw plan file carries timestamps, so a re-take never re-hashes equal. The comparable identity at the apply is the canonical digest: the sha256 of the sorted resource changes (address, actions, before, after). The battery re-derives both each run, and a different digest at the apply is a STOP.
- **S95 is the one thing the halves must decide.** Four of the seven plans also deploy CODE: artifacts uploaded at 07:29-07:31Z whose `source_code_hash` differs from the live `CodeSha256`. The face bars any code rebuild in this order. The halves either **sequence** (those artifacts' owner deploys first, then this plan is re-taken as env + grant only) or **sign the combined apply naming the four code changes**. This packet recommends sequencing.

---

## 6. What this packet does NOT cover -- named so nothing is read into the silence

1. **S93 (BLOCKING):** 4 roles (`irpt-narrative-role`, `irpt-export-render-role`, `irpt-performance-adapter-role`, `irpt-ycharts-generate-role`) cannot read ANY firm's directory objects. With K-OM + K-ENV, their functions still fail at `load_directory` (`loaders.py:71-80`). A directory-prefix read for them is a second key the face does not grant; the issuer amends the face (a K-DIR key signed here) or cuts it separately.
2. **S94 (BLOCKING, inferred):** inflection's ownership map is ABSENT. Under an object-scoped GetObject without ListBucket, a missing key reads AccessDenied, not NoSuchKey. The loader re-raises it (`loaders.py:106-114`), so inflection advisors stay UNEXPECTED. The remedy is the producer's (publish an empty map) or needs the CTO's word on a key-scoped ListBucket.
3. **S95 (BLOCKING):** the roots are not at rest (section 5).
4. **S92 (latent):** search and resolve read `q`/`selection` from the top level of a payload-2.0 event. That is IB-rtf-11's, recorded and not fixed here.
5. **Holdings serves nothing to an advisor, by design** (`_no_grant`). That is IB-rt-7's decision, not changed here.
6. The two LGIC firm buckets (fenced, rtf-5), any bucket policy, any code rebuild, any change to `_authz/` or a Lambda source.
7. **FWD-11**, which needs the roster plus an Opal login.

---

## 7. What the halves sign against

This file's blob. Each half names that blob, as `NEVER_WIDEN_SIGNOFF_COO_HALF_IRPT_BCKEND_IB-rtf-10_*.md` (`org/tier1_exec/2.0.0_SA_COO~B/deliverables/`) and `NEVER_WIDEN_SIGNOFF_CTO_HALF_IRPT_BCKEND_IB-rtf-10_*.md` (`org/tier1_exec/1.0.0_SA_CTO/deliverables/`).

If either half is ABSENT, arm (d) STOPS and the order stays open. That is the expected first-pass outcome.
