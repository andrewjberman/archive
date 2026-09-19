# IB-rtf-10 result (second pass): the re-cut packet and the re-taken plans -- STOP at the halves, as the face expects; K-CODE blocked on row S96

**Order:** `org/missions/D9/IRPT/IRPT_BCKEND/task-orders/IRPT_BCKEND.TO-IB-rtf-10.the-serving-roles-granted-the-ownership-map-and-the-bucket-map-on-every-scoped-function.md`.
- Status line: the second-pass re-hand @2b67d4ff7a, then the addendum @77bd04ca41.
- Rulings carried: the CTO's @606e7d14ce, plus the issuer's on S93, S94 and S95 (msg 98244) and the K-CODE addendum (msg 98246).

**Seat and worktree:** `0.7.0_AE_CloudOps~V`, worktree `/c/tmp/wk-irpt-6-ae1`, branch `wk-irpt_bckend-6-ae1`. CLOUD was merged in twice this pass: ff to ec57b58eb2, then @bbfe5aeac3, which carries rtf-11 @52ffa27636.

**The re-cut packet:** `NEVER_WIDEN_SIGNOFF_PACKET_IB-rtf-10.md`, **blob `609fbba9de2a50a06e9668107297f90b25f04155`**, committed @80d2383a3c. It supersedes blob `4e7ba624fa592ea74b2649d194303ca4fc6a3b43`; a re-cut packet is a re-signature.

**NOTHING APPLIED.**

## What the second pass did, in order

1. **The S95 build-store restore (issuer ruling: this order deploys no code).** For each of irpt-status, irpt-narrative, irpt-export-render and irpt-performance-adapter:
   - the LIVE zip was downloaded, and its sha256(b64) verified equal to the live `CodeSha256`;
   - it was uploaded to its manifest artifact key with `content-sha256` equal to the live hash;
   - it was read back and matched, and the function's `CodeSha256` was re-read unchanged.

   Result: **RESTORED 4 of 4**, run 12:08:42Z as `user/Andrew_Berman`. Ledger `irpt-bckend-ib-rtf-10-build-store-restore`: sentinel @407458fbb7, CLOSED 4 of 4 @cc154f5c7c. The displaced 07:29-07:31Z versions stay in the versioned bucket by VersionId. Script and output: `restore_build_store_ib_rtf_10.py` and `IB-rtf-10_build_store_restore_output.txt` @cc154f5c7c.
2. **K-DIR (issuer ruling on S93).** One new `aws_iam_role_policy` per role, for 4 roles, in `narrative/iam.tf`, `export/iam.tf`, `performance/iam.tf` and `ycharts/generate.tf` @80d2383a3c. Each is:
   - `Sid ReadFirmDirectoryPrefixOnly`, `s3:GetObject`;
   - on `local.irpt_directory_object_arns`, the registry-derived `<bucket>/investor-reporting/directory/*` per client-firm bucket, which is the same prefix `directory/iam.tf:36-38 @4ceb7f8361` derives for the directory role;
   - named by `lib/opal_naming.py name()`.

   The naming gate passed **4 of 4 CONFORMANT as IAM_POLICY**.
3. **K-CODE (the addendum): REFUSED by the builder, row S96.**
   - The prior live `CodeSha256 aQxATFkcdtEBvs+v/zztQBOPcbR9XH9Lzjm9kUOmhmU=` was read first, held at build-store version `l4JK6aUnUgtrg.TFrxiKU8.XBM_6APl4`, and re-downloaded equal. That is the rollback source.
   - Ledger `irpt-bckend-ib-rtf-10-k-code-build` was opened @e4ce69b77f.
   - `build-and-upload.sh investor-reporting irpt-directory-search` ran from HEAD bbfe5aeac3 and exited rc=1: `File not found: .../directory/data/custodian_key_seam.json`. The entry's `files[]` declares that member; its `staged_from` does not; 6 of 6 sibling functions stage it.
   - Nothing was written, re-read after the refusal. The ledger CLOSED @a91e5bc190 with the leg recorded as REFUSED-BEFORE-UPLOAD.
   - **The live zip carries the member as a CRLF hand copy** (197344 bytes, 6224 CR), not the committed blob (191120 bytes, sha256 `87f2f92f...`).
4. **The packet was re-cut:**
   - the CTO's four conditions mapped to their sections;
   - the registry vintage (`data/firm_registry.json` blob `99b8eeb54f...`, commit 39cbad4214) and the ARN lists;
   - the census, now with the directory line;
   - four key kinds: K-OM 6, K-DIR 4 and K-ENV 6, plus K-CODE 1, declared and not signable (S96);
   - the S95 restore table and the writers `W` per property;
   - the re-taken plans with their canonical digests;
   - both branches and the rollback per key;
   - the S94 carve-out and the identity line per arm;
   - what the packet does not cover, and the two ways forward on K-CODE.

## R67-AC1: FAIL, by output (a STOP at (d), the face's expected second-pass outcome, plus (c-code))

The battery ran at worktree HEAD 285e9cf46c with the criterion's exact invocation (`timeout 1800 py -3.12 .../battery_ib_rtf_10.py`), 12:46:51-12:48:22Z, rc 1.

The first run, @80d2383a3c under `timeout 3000`, was re-done because the proof checker grades the recorded invocation against the criterion's, and a record naming an invocation that was not run would be false. The two outputs differ in 8 lines only: the HEAD line and the 7 raw planfile sha256s, which change on every take. Every count, verdict and canonical digest is identical.

The deciding lines, verbatim from `IB-rtf-10_R67-AC1_battery_output.txt`:

- **(a)**
  - `ownership map readable: 0 of 21; directory readable: 9 of 21; bucket map present: 1 of 7; client firms 3 (registry)`.
  - Controls: `positive (user Andrew_Berman) allowed; negative (opalinvest-auth-lambda-role) implicitDeny`.
  - The three packet census lines read `EQUAL`.
- **(b)**
  - `blob at HEAD 609fbba9de2a50a06e9668107297f90b25f04155, worktree 609fbba9de2a50a06e9668107297f90b25f04155 -> COMMITTED, UNCHANGED`.
  - `REGISTRY-VINTAGE: packet 99b8eeb5..., HEAD data/firm_registry.json blob 99b8eeb5... -> EQUAL`.
  - `K-OM-ARNS: packet 3 ARN(s), derived from the registry 3 -> EQUAL`.
  - `K-DIR-ARNS: packet 3 ARN(s), derived from the registry 3 -> EQUAL`.
  - `W` per role: 2/2/2/4/5/3/3.
- **(c)**
  - `roots planned without destroy: 7 of 7; total destroy 0; total changes 17; lambda updates carrying a CODE change 0 (row S95: 0 required)`.
  - `canonical digests equal to the packet's: 7 of 7`.
  - The `PLAN-ROOTS` and `PLAN-CODE-CHANGES` lines read `EQUAL`.
  - The noise line names 6 lambda updates whose object version moves with `source_code_hash` unchanged. Its label says "object-version-only", but the per-address lines show 4 of those 6 also carry the env change (status, narrative, export-render, performance-adapter). ycharts is env only, with the object version the same.
- **(c-code)** `build store latest version l4JK6aUnUgtrg.TFrxiKU8.XBM_6APl4 content-sha256 aQxATFkc... -> the prior live bytes: NOT BUILT (row IRPT_BCKEND-S96 ...)`.
- **(d)** `COO half ... ABSENT`, `CTO half ... ABSENT`, `halves: 0 of 2`, so `STOP at (d)`.
- `RESULT: R67-AC1 FAIL -- 3 of 7 arms hold`.

**Identity.** Every arm printed `ran as arn:aws:iam::313476888478:user/Andrew_Berman -- a configuration/document claim, NOT a served behaviour`. None of (a)-(d) certifies a served path, and the CTO's identity bar binds (f).

**Determinism.** The canonical digests equal those of the 12:1xZ script take, 7 of 7. The raw planfile sha256 differs each take, as the packet states.

## R67-AC2: JUDGMENT, recorded for 3.0.0_SA_CVO and not self-graded

**1. The object-scoped read, or the map published to a directory-readable prefix?**

- **The CTO ruled @606e7d14ce:**
  - (a) ADOPTED: the object-scoped read.
  - (b) BARRED as a duplicate output path.
  - Moving the map was refused as a canon departure.
- **The packet now meets the four conditions:**
  - the vintage and ARN list are printed (section 1, and the ARN lines in section 3);
  - the ban comment was amended in the same commit as the statement (@9f21dedfd8, carried);
  - 0 to destroy, additive only (section 6);
  - the bucket map is the one registry-derived value (section 3).
- **Where the packet goes beyond the ruling, so the CVO can see it:**
  - **K-DIR** extends an EXISTING prefix to 4 more roles (the issuer's S93 amendment). It is not the ownership-map read the ruling addressed.
  - **K-CODE** is the issuer's addendum. It deploys code, where S95's ruling said this order deploys none, and is qualified to one function built from this project's own drained cell.
- **The design's precondition is unchanged:** S94. inflection's map is absent, and without ListBucket that reads AccessDenied (`_authz/loaders.py:106-114 @4ceb7f8361`). It is pitched to the CTO and carved out of the token.

**2. Why every earlier live proof passed, and what the acceptance instrument must do.**

- **Unchanged from the first pass.** rtf-2 and rtf-8 arm (e) ran the real code IN-PROCESS, under operator credentials and the harness's environment: the right code with the wrong identity and the wrong configuration.
- **The CTO's ruling makes the rule binding here:** an arm that claims a served behaviour names its principal, and that principal is the function's own execution role.
- **How this pass meets it:**
  - the packet states the principal per arm (section 9);
  - the battery prints its identity per arm and labels (a)-(d) configuration claims;
  - (f) on the third pass goes through the real route with the bounded principal.

**3. S91, and the same class one layer down.**

- `_authz/served.py:628, 649, 662 @4ceb7f8361` record internal errors to a `None` sink, so the outage was invisible in logs.
- **Row S96 is the same class at the BUILD layer:** the served `irpt-directory-search` zip carries a member the manifest cannot reproduce, a hand-placed CRLF copy.
  - Nothing reports it. The served bytes run, the plan reads at rest, and the manifest looks complete (10 `files[]`).
  - Only a rebuild from HEAD surfaces it, and that rebuild fails closed, which is correct.
  - The prior build therefore cannot be reproduced from the committed tree, and S89's "the manifest is not a rollback source" holds here for a second reason.

## Rows filed this pass

- `IRPT_BCKEND-S96`: BLOCKING, ARMED, `2.0.0_SA_COO~B`. The builder refuses `irpt-directory-search` from HEAD, because the seam member is declared but not staged, and the live zip carries a CRLF hand copy.
- `IRPT_BCKEND-S93`, `S94` and `S95`, from the first pass, are RULED by the issuer. S93 and S95 are executed here; S94 is pitched to the CTO.

## What the third pass needs

1. **The K-CODE decision** (packet section 11). This seat recommends (i):
   - the one `staged_from` object is added to `irpt-directory-search` (outside this order's grant);
   - this seat rebuilds under a new ledger, prints the built sha256, and re-plans the directory root;
   - the packet is re-cut ONCE with K-CODE complete, and the halves sign that blob only.

   Under (ii), the halves sign blob `609fbba9de` now for K-OM/K-DIR/K-ENV, and K-CODE follows in its own packet.
2. **Both halves at HEAD naming the blob chosen.**
3. **Then:**
   - (e): the apply under a ledger, with the canonical digests re-compared, `simulate-principal-policy` n of N plus the negative controls, the bucket map m of m, and `CodeSha256` re-read;
   - (f): the bounded principal (rtf-9 packet blob `a1f36b95b2`, a new epoch, the IB-rtf-3 lifecycle) through the real routes. Search runs WITH a query and resolve WITH a selection, and S92 is recorded as FIXED or not by output.
