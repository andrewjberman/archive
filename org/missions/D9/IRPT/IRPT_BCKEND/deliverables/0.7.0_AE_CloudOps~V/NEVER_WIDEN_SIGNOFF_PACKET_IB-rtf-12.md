# NEVER-WIDEN SIGN-OFF PACKET -- IB-rtf-12: every serving zip carries the raw-keys file its id module reads (K-CODE x 6)

**For:** the two halves required before IB-rtf-12 applies anything (CLAUDE.md never-widen: CTO + COO): `1.0.0_SA_CTO` and `2.0.0_SA_COO~B`.

**Prepared by:** `0.7.0_AE_CloudOps~V` (`IRPT_BCKEND.TO-IB-rtf-12`, second pass; face status line @9fc936185d; GO msg 98279).

**Executes:** the issuer's rulings (msg 98279):
- **S99:** the registry is INCLUDED as the second missing member.
- **S101:** the seam member's CRLF->LF is ACCEPTED as part of the act.
- **S102:** `irpt-ycharts-generate` is DEFERRED to a sourcing cell, so K-CODE covers 6 functions.
- **S100:** holdings is recorded-not-counted in (f).

**NOTHING IS APPLIED BY THIS PACKET.** The 6 builds are in the build store, and no function was touched: every `CodeSha256` was re-read unchanged. Line citations are `@9fc936185d` unless another vintage is given.

A half signs the **blast radius** of the act: what each key may touch, and the rollback for each key.

---

## 1. The keys: K-CODE x 6 (one per serving function; ycharts deferred)

Each function was rebuilt by `infra/aws/lambda/ci/build-and-upload.sh investor-reporting <fn>` from worktree HEAD `0414444120`. That HEAD contains the manifest commit @dbf7667178. The build ran under ledger `irpt-bckend-ib-rtf-12-build` (sentinel @0414444120, CLOSED 6 of 6 @1c71ed7c12).

| function | prior LIVE `CodeSha256` = ROLLBACK SOURCE (build-store version) | BUILT sha256 (new version) | served-byte delta vs the live zip |
|---|---|---|---|
| `irpt-directory-search` | `HOpXPDoHhrVK/ayqsx1uKgzt9mWOjDlK+Ix2CPbCamI=` (`hk9OUfwHZxlcwZDqN7cEknbJOXtvB3jd`) | `PUjH3OjDe8Yj3RwdIO0KT3GXsYGfvUCmzG/aHsi6e1c=` (`DOwCkAXXw1oLuzL_yzf2AqNJ0v.WnYDF`) | + `raw_keys.json`, + `firm_registry.json`; the other 10 members byte-identical |
| `irpt-status` | `LHprxKSP1lM3VhoP2ijEcUVCtI+yeZt8tPRkZwpRBdY=` (`QNerDSUu9GMYB0bZrjon6n_6VG9q3aR6`) | `O3TyGqfqjiwZP9OSXmryonnAst+SbYMLzyuSGphOyCE=` (`z8VnRXEPFTioTwjwWlR_TCCQYiqU6mmV`) | + `raw_keys.json`, + `firm_registry.json`; seam 197,344 CRLF -> 191,120 LF (S101); the other 12 byte-identical |
| `irpt-holdings` | `78XvypHOpeybejwKd5KLCwNcgat2jbQr6O3PhdwaFSU=` (`XGnVW2ED9FW0zOpRr0V5K12adFHrpeO7`) | `uS+WBeNxiCkYU2pdGalaONZ74SvoWEiYx669KWYKQDA=` (`U4sKRs.HJ0Jc4Ik323Y0b.qY7LsWU2Pg`) | + `raw_keys.json`; the other 14 byte-identical, including its 3 own CRLF members |
| `irpt-narrative` | `sgolF/uXedgXpePoBoi5y1dIgOybQkgcokihEJFM+0I=` (`Pu2QRmDx58Qo3hHwVM8L_gyotsmQ8h_6`) | `o4newc7E9m1pD61k+P/xGdlwHMO7cheYbDfR6Urzgh8=` (`jM9scOJ005ovgidfDS3DBRHRmjvLzUwn`) | + `raw_keys.json`, + `firm_registry.json`; seam CRLF -> LF (S101); the other 16 byte-identical, including 5 own CRLF |
| `irpt-export-render` | `4Dp6e0Vy+SfziPY+9wUSWSBS4JzS9diUtduOTxIqclQ=` (`5tV41pNz.TpJ8O1f6zZCAJ9M6BRqoYlI`) | `9IMayS94if11cyKq51TbcyBG8cUwbbUWlQMlT9XhiaQ=` (`dECFEZtZArSJYdPy4.ImeVHBv6Q.jxBH`) | + `raw_keys.json`; seam CRLF -> LF (S101); the other 17 byte-identical |
| `irpt-performance-adapter` | `/Cn8XUZoSn1EGBax3+/UaVjJSAQiybZQ84vRVwiRcWs=` (`KI0U8m08xPkCgvem5bLmcU2fuWwOCLzs`) | `IHosoGqGUxh2M/UjefNnmbLSXVgTxlNG76cGPjEd1tw=` (`38i7y_iXZqvWIzUNetKnBxXxs9dAuOGF`) | + `raw_keys.json`, + `firm_registry.json`; seam CRLF -> LF (S101); the other 20 byte-identical, including 6 own CRLF |

BUILT: irpt-directory-search PUjH3OjDe8Yj3RwdIO0KT3GXsYGfvUCmzG/aHsi6e1c= DOwCkAXXw1oLuzL_yzf2AqNJ0v.WnYDF
BUILT: irpt-status O3TyGqfqjiwZP9OSXmryonnAst+SbYMLzyuSGphOyCE= z8VnRXEPFTioTwjwWlR_TCCQYiqU6mmV
BUILT: irpt-holdings uS+WBeNxiCkYU2pdGalaONZ74SvoWEiYx669KWYKQDA= U4sKRs.HJ0Jc4Ik323Y0b.qY7LsWU2Pg
BUILT: irpt-narrative o4newc7E9m1pD61k+P/xGdlwHMO7cheYbDfR6Urzgh8= jM9scOJ005ovgidfDS3DBRHRmjvLzUwn
BUILT: irpt-export-render 9IMayS94if11cyKq51TbcyBG8cUwbbUWlQMlT9XhiaQ= dECFEZtZArSJYdPy4.ImeVHBv6Q.jxBH
BUILT: irpt-performance-adapter IHosoGqGUxh2M/UjefNnmbLSXVgTxlNG76cGPjEd1tw= 38i7y_iXZqvWIzUNetKnBxXxs9dAuOGF

PACKET-KEYS: K-CODE 6

**Verified at rest, 6 of 6** (`verify_build_ib_rtf_12.py` and `IB-rtf-12_build_verify_output.txt` @1c71ed7c12):
- each new version is the latest, and metadata == the re-downloaded bytes == the built sha;
- the members equal `files[]`, and each equals its source: staged members equal the blob at their pin and declared sha256; own members equal the disk bytes the builder read, and every own `.py` also equals its HEAD blob;
- the delta vs the live zip is **exactly** the added member(s), plus the seam line endings on 4 functions;
- every other member is byte-identical to live, and the own CRLF members are byte-identical to live **14 of 14**;
- each rollback source is still present and hashes to the prior live `CodeSha256`;
- every function's `CodeSha256` is unchanged.

---

## 2. The added members, described (arm (b))

| member | source | blob / size | what it is | credentials | writers |
|---|---|---|---|---|---|
| `raw_keys.json` | `infra/aws/lambda/investor-reporting/_ids/raw_keys.json` @47f21dab95 | `eed32b39ad`, 6,492 bytes, sha256 `f81db571...` | a dict: `_artifact/_purpose/_written_by/_grammar/_claim` + `firms` (**k=3**: 49financial, inflection, cottonwood). Each has account/relationship/client rows naming the UPSTREAM FIELD the firm's opaque id is minted from, with source citations. **Declarations, never client identifiers.** | 0 credential-named keys | W=1 (`0.9.0_WK_IRPT_BCKEND~1`, 2 commits) |
| `firm_registry.json` (4 functions) | `data/firm_registry.json` @39cbad4214 | `99b8eeb54f`, 5,326 bytes, sha256 `5a4c0c3d...` | the generated firm view: `firms` **k=5** (id, bucket, email domain, kind, enabled, scopes, `tree_token` = the firm's folder token) | 0 (`tree_token` is a folder token, not a secret) | W=5 (8 commits) |

**Why these 4 get the registry, and the other functions do not** (row S99; `diag_ib_rtf_12.py` @018c7c2408):
- `ids.py:113-138` and `keys.py` resolve the registry from the env, then a `data/` walk-up, then beside the module.
- On the deployed layout that resolves nowhere for directory-search, status, narrative and performance-adapter.
- holdings and export-render resolve it through `IRPT_FIRM_REGISTRY` to the `irpt-common:5` layer's copy; ycharts packages its own.
- With exactly the members the manifest declares, the deployed path's scope resolves on 6 of 7 (holdings: S100).

---

## 3. Writers of each named property (the declared plane), `W` printed

| property | W | declared writers |
|---|---|---|
| each function's served code | 1 | its one `yang-lambda` module (`module.irpt_<fn>`) in its root, which reads the build store's latest version and its `content-sha256` |
| each function's artifact key (the build store) | 2 | `build-and-upload.sh`; and this order's build (section 1, once, under its ledger) |
| `lambda-source-map.json` `staged_from`/`files[]` for the 6 | 1 | this order's manifest commit @dbf7667178 (the 11 objects) |
| `lambda-source-map.json` `artifact_sha256` | 2 | `build-and-upload.sh` (the builder's rewrite was REVERTED to the committed bytes, S89) and `record-terraform-deploy.sh:748-768` post-apply |

**The qualifier** (carried from the rtf-8 and rtf-10 halves): a console or CLI write to a function or the build store is physically possible and cannot be enumerated. It is banned by NEVER-9, and the rollback's own re-read covers it.

---

## 4. The plan per root: re-taken after the build, APPLIED TO NOTHING

| root | Plan | the one address and what moves | canonical digest |
|---|---|---|---|
| directory | 0 add, 1 change, **0 destroy** | `module.irpt_directory_search.aws_lambda_function.this`: `source_code_hash` -> `PUjH3OjD...` == built; object version; env and every other attribute unchanged | `d26db7c034ca5461325881af8a70c66790aab8b1f592112ed9f00170eed0cadc` |
| ops | 0 add, 1 change, **0 destroy** | `module.irpt_status...`: -> `O3TyGqfq...` == built | `82b6c8efa3ce899dbc6621d160b8e668beae5d7dbd687bf7b17bb7852fa30b75` |
| holdings | 0 add, 1 change, **0 destroy** | `module.irpt_holdings...`: -> `uS+WBeNx...` == built | `9635d3b90fdb76daf49f124bfe591b7a890a54e4cf928537ea79879ae47d331a` |
| narrative | 0 add, 1 change, **0 destroy** | `module.irpt_narrative...`: -> `o4newc7E...` == built | `a292e3786a24963e2e0426b0b4698311972c2b68ea0029b5af9f7ef093f1d9c9` |
| export | 0 add, 1 change, **0 destroy** | `module.irpt_export_render...`: -> `9IMayS94...` == built | `328dab19b150d19a9b8df1d54041901a1aeaeb8d0f98bb9cc48aec7997c12425` |
| performance | 0 add, 1 change, **0 destroy** | `module.irpt_performance_adapter...`: -> `IHosoGqG...` == built | `3ab3ce3d3b266411dbc00496e260fef59bb51a9a6cf810412df7261b5b736cff` |
| ycharts | **No changes** (deferred, S102; recorded) | none | `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945` |

PLAN-ROOTS: 7 of 7 planned; destroy 0 of 7; changes 6
PLAN-CODE-CHANGES: 6 of 7

- Every change is a code-carrying update on exactly one serving function, with its after-hash == its built sha (6 of 6). There is no environment change, no IAM change, no added or destroyed resource, and no other attribute moves.
- rtf-10's grants and bucket maps stand. They are re-read, never re-applied.
- **A different digest at the apply is a STOP.**

---

## 5. The blast radius, both branches

**BRANCH -- APPLIED (the 6 served zips carry the members):**
- `raw_key_for` (`ids.py:166-179`) and the registry resolution (`ids.py:113-138`, `keys.py`) find their files. `enforcer_for` (`_authz/served.py:569-592`) completes.
- Every FIRM_ADVISOR request on the 6 functions' routes resolves its scope. It is SERVED by policy (the disclosed partial) or REFUSED by policy with a `firm_id` -- **never UNEXPECTED for this cause** (diagnostic: 6 of 7 resolve, holdings excluded per S100).
- **Holdings** still reads FIRM_BINDING (S100: it reads the directory POINTER as the artifact). This act moves nothing on it except the added `raw_keys.json`.
- **Cross-firm bound:**
  - the added members are the SAME two blobs in every zip;
  - the id module keys by the VERIFIED tenant (`ids.py:408` `raw_key_for(firm_id, ...)` from `served.py:582` with `tenant`), and `raw_keys.json` holds declarations for 3 firms, not data;
  - no IAM, bucket, prefix or route changes;
  - **nothing new is reachable across firms.**
- The seam member's CRLF->LF on 4 functions parses to the identical JSON (S101, accepted).

**BRANCH -- NOT APPLIED / ROLLED BACK:** the path stays as rtf-10's (f) measured it: 9 of 10 UNEXPECTED, an outage and not a refusal.

**ROLLBACK, per function (never `update-function-code`, never the manifest):**
1. Re-publish the prior live `CodeSha256` through Terraform. Its bytes are at the rollback-source version in section 1, verified present and equal.
2. Re-upload those bytes as the latest with `content-sha256` equal to the prior hash, then `.tools/safe-apply.sh` the function's root.
3. Verify `get-function-configuration` `CodeSha256` == the prior hash.
4. The served behaviour reverts to UNEXPECTED on the routes.

---

## 6. Carve-outs (the issuer's rulings, msg 98279)

- **S102, `irpt-ycharts-generate` DEFERRED.** It is not rebuilt, and its root plans "No changes". In arm (f) its route is recorded **UNEXPECTED-BY-UNBUILDABLE** with S102 cited, and NOT counted.
- **S100, `irpt-holdings` recorded-not-counted.** Its route is recorded with S100 cited, and NOT counted. Its served behaviour is the CTO's (ruling @606e7d14ce s.4).
- **The token's `0 UNEXPECTED`** reads over the rebuilt functions minus holdings, on the firms whose ownership map EXISTS (`n of N` printed; inflection per S94).

---

## 7. The identity line, per arm

| arm | claims a SERVED behaviour? | runs as |
|---|---|---|
| (a)-(d) census, files, manifest, build at rest, plans, halves | **No:** configuration and artifact claims | the operator identity (`arn:aws:iam::313476888478:user/Andrew_Berman`, printed) |
| (e) apply + read-backs | **No:** what is DEPLOYED | the operator identity; `safe-apply`'s runtime identity printed |
| (f) the live proof (rtf-10's arm (f), unchanged) | **YES** | **each route's own function EXECUTION ROLE.** The bounded principal's real HTTP requests go through `https://opalinvest.dev/api/scoped/investor-reporting/<route>`, and the route, function and role are printed per request. The DEPLOYED BYTES run, outside any source tree. |

---

## 8. What this packet does NOT cover

1. `irpt-ycharts-generate` (S102) and the holdings pointer defect (S100).
2. Any `_authz/`, `_scope/` or `_ids/` SOURCE change, any IAM change, and any Terraform edit.
3. Cross-checkout build reproducibility (S101's second half, carried to the CTO).
4. The `irpt-common:5` layer's stale copies (`ids.py`, `keys.py`, `raw_keys.json` 5,990 bytes, `firm_registry.json` 5,094 bytes). They are shadowed at `/var/task` for `ids.py`, and read for the registry by holdings/export; recorded, not moved.

---

## 9. What the halves sign against

This file's blob, named in each half:
- `NEVER_WIDEN_SIGNOFF_COO_HALF_IRPT_BCKEND_IB-rtf-12_*.md` (`org/tier1_exec/2.0.0_SA_COO~B/deliverables/`);
- `NEVER_WIDEN_SIGNOFF_CTO_HALF_IRPT_BCKEND_IB-rtf-12_*.md` (`org/tier1_exec/1.0.0_SA_CTO/deliverables/`).

ABSENT is a STOP at (d), the expected second-pass outcome.

**At the apply, (e) re-verifies BEFORE any `safe-apply`:**
- halves 2 of 2;
- this blob;
- the digests EQUAL to section 4;
- every built artifact the latest at its built sha (section 1).

Any difference is a STOP. The apply then runs from the SAVED planfiles; the reads after are `CodeSha256 == built` 6 of 6, and one `raw_keys.json` member downloaded and hashed in each served zip.
