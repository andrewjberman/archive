# IB-rtf-10 result (third pass): K-CODE built, the packet re-cut once with all four keys signable, the STOP at the halves the face expects

**Order:** `org/missions/D9/IRPT/IRPT_BCKEND/task-orders/IRPT_BCKEND.TO-IB-rtf-10.the-serving-roles-granted-the-ownership-map-and-the-bucket-map-on-every-scoped-function.md`, status line and `<paths>` @6e027591fc. That is the S96 ruling (i), msg 98251, on top of the re-hand @2b67d4ff7a and the addendum @77bd04ca41.

**Seat:** `0.7.0_AE_CloudOps~V`, worktree `/c/tmp/wk-irpt-6-ae1`, branch `wk-irpt_bckend-6-ae1`. CLOUD was merged in at the start of the pass, ff to 6e027591fc; the second pass had been drained @7906c853b8.

**The packet:** `NEVER_WIDEN_SIGNOFF_PACKET_IB-rtf-10.md`, **blob `c3a44074d2dabe4292bfc648d855be4b99fe48db`**, committed @94bbf091ee.
- It supersedes `609fbba9de` (second pass) and `4e7ba624fa` (first pass). No half was signed against either.
- The halves sign THIS blob.

**NOTHING APPLIED. No function was touched.**

## What the third pass did, in order

1. **The S96 remedy (ruling (i)), @2b1c672e1f.** `irpt-directory-search`'s `staged_from` in `infra/aws/lambda/ci/lambda-source-map.json` gained the seam object its six siblings carry, copied byte-for-byte from `irpt-status`:
   - `_ids/data/custodian_key_seam.json` at pin `c28c728a30`, packaged as `data/custodian_key_seam.json`, sha256 `87f2f92f...`;
   - a parse-diff asserts exactly one appended object, 6 lines added;
   - `artifact_sha256` is untouched (S89).
2. **The K-CODE build**, under ledger `irpt-bckend-ib-rtf-10-k-code-build-2` (sentinel @46a106b4d1, CLOSED @b1032a0ee1):
   - Before the build, the prior live `CodeSha256` was re-read as `aQxATFkc...`, held at build-store version `l4JK6aUn...`.
   - `build-and-upload.sh investor-reporting irpt-directory-search` ran from HEAD 46a106b4d1 and exited rc=0.
   - Built: **sha256 `HOpXPDoHhrVK/ayqsx1uKgzt9mWOjDlK+Ix2CPbCamI=`**, version **`hk9OUfwHZxlcwZDqN7cEknbJOXtvB3jd`**, 123282 bytes.
   - The builder also rewrote `artifact_sha256` in the manifest. That write was reverted to the committed bytes, because the grant is one object.
3. **Verified at rest, 7 of 7 checks** (`verify_k_code_build_ib_rtf_10.py` and its output, @b1032a0ee1):
   - the new version is the latest, and its metadata equals the re-downloaded bytes, which equal the built sha;
   - the zip members are **10 of 10 == `files[]`, each equal to its committed blob**; the seam member is the LF blob, 191120 bytes with 0 CR;
   - the rollback source is kept and equals the prior live hash;
   - the function's `CodeSha256` is **unchanged**.
   - **The served delta against the prior live zip is exactly `entry.py`** (the rtf-11 fix, 9123 -> 11539 bytes) **plus the seam member's line endings.** The other 8 members are byte-identical.
4. **The re-plan:**
   - 7 of 7 roots, 0 destroy, **18 changes**;
   - **ONE code change, K-CODE's own:** `module.irpt_directory_search`, `source_code_hash aQxATFkc... -> HOpXPDo...` plus the object version, with the environment and role unchanged;
   - 6 of 7 canonical digests are EQUAL to the second-pass packet. The directory root's moves `3bc2229a -> 0f66bef1` by exactly that one address.
5. **The packet re-cut ONCE:**
   - K-CODE is complete: the built sha and version, the member-level served delta, both branches, and the rollback to `aQxATFkc...` at `l4JK6aUn...` through Terraform (never `update-function-code`, never the manifest);
   - the writers table now counts the manifest's `artifact_sha256` at 2 writers: the builder, and `record-terraform-deploy.sh:748-768 @6e027591fc` post-apply;
   - section 11 lists the pre-apply re-verifications, where any difference is a STOP.

## R67-AC1: FAIL, by output (the STOP at (d) the face expects; every arm before it holds)

The battery ran @94bbf091ee with the criterion's exact invocation (`timeout 1800 py -3.12 .../battery_ib_rtf_10.py`), 13:16:17-13:17:39Z, rc 1. The deciding lines, verbatim from `IB-rtf-10_R67-AC1_battery_output.txt`:

- **(a)** `ownership map readable: 0 of 21; directory readable: 9 of 21; bucket map present: 1 of 7; client firms 3 (registry)`. The controls read positive allowed and negative implicitDeny, and the three packet census lines read `EQUAL`.
- **(b)**
  - `blob at HEAD c3a44074d2dabe4292bfc648d855be4b99fe48db, worktree c3a44074d2dabe4292bfc648d855be4b99fe48db -> COMMITTED, UNCHANGED`.
  - `packet keys line: K-OM 6; K-DIR 4; K-ENV 6; K-CODE 1`.
  - `REGISTRY-VINTAGE ... -> EQUAL`.
  - Both ARN lines read `EQUAL`.
- **(c)**
  - `roots planned without destroy: 7 of 7; total destroy 0; total changes 18; lambda updates carrying a CODE change 1 (K-CODE's own, after-hash == built: 1; any other: 0 -- 0 allowed)`.
  - `canonical digests equal to the packet's: 7 of 7`.
  - The `PLAN-ROOTS`, `PLAN-CODE-CHANGES` and `PLAN-CODE-CHANGE-ADDRESS` lines read `EQUAL`.
- **(c-code)** `K-CODE at rest: 5 of 5 checks hold`.
- **(d)** `halves: 0 of 2`, so `STOP at (d)`.
- `RESULT: R67-AC1 FAIL -- 4 of 7 arms hold`.

**Identity.** Every arm printed that it ran as `user/Andrew_Berman`, a configuration or document claim, NOT a served behaviour. The CTO's identity bar binds (f).

**Determinism.** The battery's plan equals the 13:0xZ script's plan, 7 of 7 digests. The raw planfile sha256 differs each take, as the packet states.

## R67-AC2: JUDGMENT, recorded for 3.0.0_SA_CVO and not self-graded

**1. The object-scoped read, or the map published to a directory-readable prefix?**

- **The CTO ruled @606e7d14ce:**
  - (a) ADOPTED: the object-scoped read.
  - (b) BARRED as a duplicate output path.
  - Moving the map was refused.
- **The packet meets the four conditions:**
  - the vintage and ARN list are printed;
  - the ban comment was amended in the same commit as the statement (@9f21dedfd8);
  - the plans are 0 to destroy, and every IAM key is additive;
  - the bucket map is the one registry-derived value.
- **Where the packet goes beyond the ruling, stated so the CVO can see it:**
  - **K-DIR:** an EXISTING prefix extended to 4 roles (the issuer's S93 amendment).
  - **K-CODE:** a code deploy the S95 ruling had excluded, qualified by the issuer to one function built from this project's own drained cell. Its served delta is exactly `entry.py` plus the seam member's line endings; `_authz/`, `_scope/`, `_keys/`, `_ids/` and `handler.py` are byte-identical.
- **The precondition is unchanged:** S94. inflection's map is absent, and without ListBucket that reads AccessDenied (`_authz/loaders.py:106-114 @4ceb7f8361`). It is pitched to the CTO and carved out of the token.

**2. Why every earlier live proof passed, and what the acceptance instrument must do.**

- rtf-2 and rtf-8 arm (e) ran the real code IN-PROCESS, under operator credentials and the harness's environment: the right code with the wrong identity and the wrong configuration.
- The CTO's identity bar binds this order: an arm that claims a served behaviour names its principal, and that principal is the function's own execution role.
- Packet section 9 states the principal per arm. The battery prints its identity per arm and labels (a)-(d) and (c-code) configuration claims. (f) goes through the real route with the bounded principal.

**3. S91, and S96 as the same class one layer down.**

- `_authz/served.py:628, 649, 662 @4ceb7f8361` record internal errors to a `None` sink.
- **S96 is the same class at the build layer:** the served directory-search zip carried a hand-placed CRLF member that no committed tree state reproduces.
  - The plan read "at rest", the manifest looked complete, and the function ran. Only a rebuild from HEAD could see it, and that rebuild failed closed, which is correct.
  - The remedy (one declared `staged_from` object) makes the served bytes reproducible from the tree: 10 of 10 members equal to committed blobs.
- **The discriminator:** the same builder on the same function REFUSED @bbfe5aeac3, without the object, and BUILT @46a106b4d1, with it.

## Rows

- `IRPT_BCKEND-S96` is **RULED (i) and EXECUTED** this pass: the manifest line @2b1c672e1f, and the build verified @b1032a0ee1. It was filed BLOCKING/ARMED with disarm_owner `2.0.0_SA_COO~B`; its disposition is the issuer's.
- S93, S94 and S95 are ruled as before.
- **No new row this pass.**

## What the next pass needs

1. **Both halves at HEAD naming blob `c3a44074d2dabe4292bfc648d855be4b99fe48db`.**
2. **(e), the apply under a ledger.** Before any `safe-apply`, re-verify:
   - the per-root canonical digests EQUAL to packet section 6;
   - the registry blob EQUAL to `99b8eeb54f`;
   - the latest `irpt-directory-search.zip` is `hk9OUfwH...` with content-sha256 `HOpXPDo...`.

   Then, after the apply:
   - `simulate-principal-policy` n of N, plus the negative controls;
   - the bucket map m of m;
   - `CodeSha256` unchanged on 6 of 7 serving functions, and `irpt-directory-search == HOpXPDo...`.
3. **(f), the bounded principal through the real routes** (rtf-9 packet blob `a1f36b95b2`, a new epoch, the IB-rtf-3 lifecycle):
   - search WITH a query and resolve WITH a selection;
   - S92 recorded FIXED or not, by output;
   - inflection recorded as UNEXPECTED-BY-ABSENCE (S94).
