# IB-rtf-12 result (second pass): 6 built and verified at rest, the packet committed -- STOP at the halves, as the face expects

**Order:** `org/missions/D9/IRPT/IRPT_BCKEND/task-orders/IRPT_BCKEND.TO-IB-rtf-12.every-serving-zip-carries-the-raw-keys-file-its-id-module-reads.md`, status line @9fc936185d. GO msg 98279 carries the rulings:
- S101: the seam CRLF->LF is ACCEPTED as part of the act.
- S102: ycharts is DEFERRED, so K-CODE covers 6 functions.
- S100: holdings is recorded-not-counted.

**Seat:** `0.7.0_AE_CloudOps~V`, worktree `/c/tmp/wk-irpt-6-ae1`. CLOUD was merged in, ff to 9fc936185d.

**The packet:** `NEVER_WIDEN_SIGNOFF_PACKET_IB-rtf-12.md`, **blob `9d273fb8517a00288ec13d8dd0814a47af8782fa`**, committed @8562971010.

**NOTHING APPLIED. No function was touched.** Every `CodeSha256` was re-read unchanged.

## What this pass did

1. **The build, under ledger `irpt-bckend-ib-rtf-12-build`** (sentinel @0414444120, CLOSED 6 of 6 @1c71ed7c12).
   - Before the build: each function's prior live `CodeSha256` was read, and its build-store latest version (content-sha256 == live) was kept as the ROLLBACK SOURCE.
   - The build: `build-and-upload.sh investor-reporting <fn>` for the 6, from HEAD 0414444120, with rc=0 and the upload write-verified on 6 of 6.
   - The builder's `artifact_sha256` rewrite (6 lines) was reverted to the committed bytes (S89).
2. **Verified at rest, 6 of 6** (`verify_build_ib_rtf_12.py` and `IB-rtf-12_build_verify_output.txt` @1c71ed7c12):
   - each new version is the latest, with metadata == bytes == built;
   - the members equal `files[]`, and each equals its source;
   - **the delta vs live is exactly the added member(s)**: `raw_keys.json` on 6, `firm_registry.json` on the S99 four;
   - **plus the seam line endings** on status, narrative, export-render and performance-adapter (197,344 CRLF -> 191,120 LF, the same JSON once normalised);
   - every other member is byte-identical, and **the own CRLF members are byte-identical to live, 14 of 14** (holdings 3, narrative 5, performance-adapter 6);
   - each rollback source equals the prior live hash, and every function is unchanged.
3. **Plans re-taken.** 7 roots, **0 destroy**, **6 changes**. Each change is one serving function's code update, with its after-hash == its built sha and its env unchanged. ycharts reads "No changes", and the digests are printed.
4. **The packet:**
   - K-CODE x 6: the prior live hash and rollback version, and the built sha and version, per function;
   - the per-function delta, and the two added members described;
   - writers `W`, the plans with their digests, and both branches;
   - the rollback per function via Terraform;
   - the S100/S102 carve-outs and the identity line per arm.

## R69-AC1: FAIL, by output (3 of 6 arms; STOP at (d) on the halves -- the expected second-pass outcome)

`timeout 1800 py -3.12 .../battery_ib_rtf_12.py` @8562971010, rc 1.

- **(a), (b) and (c) PASS**, as in the first pass: the premise at the cut 0 of 7 / 0 of 7; both files described; the manifest 11 objects with a clean parse-diff.
- **(d):**
  - `packet ... blob at HEAD 9d273fb8517a00288ec13d8dd0814a47af8782fa, worktree 9d273fb8517a00288ec13d8dd0814a47af8782fa -> COMMITTED, UNCHANGED`;
  - `built and verified at rest: 6 of 6; own CRLF members byte-identical to live: 14 of 14`;
  - `plans: roots 7; destroy 0; changes 6; code changes == built 6 of 6; digests EQUAL to the packet 7 of 7`;
  - `COO half ... ABSENT`, `CTO half ... ABSENT`, `halves: 0 of 2`.
- `RESULT: R69-AC1 FAIL -- 3 of 6 arms hold`. The token was not printed.

## R69-AC2: JUDGMENT, recorded for 3.0.0_SA_CVO and not self-graded

The first pass's record stands, with one addition from this pass. The four questions:

1. **How a module-relative data file was omitted.** `ids.py:64` and `:113-138 @9fc936185d` resolve `raw_keys.json` and the registry relative to the module. The repository has both there, and the zip does not. The seat's own S98 diagnostic ran inside the repository and inherited the registry through the walk-up (S99).
2. **What the build contract must carry.** A build-time census of `__file__`-relative opens keyed on the import (the binding-check class @3580608505), and builds reproducible from the committed tree.
   - **This pass adds a measured instance of the reproducibility half.** 14 own members of these 6 functions ship CRLF because this checkout is `core.autocrlf=true`, and the live zips carry exactly those CRLF bytes because their builders' checkouts did too.
   - The build is byte-identical to live ONLY on a checkout with the same EOL setting. An LF checkout ships 14 different members for the same commit. Carried to the CTO (S101).
3. **The identity bar's "deployed BYTES" clause.** The evidence supports stating as law: a served-path proof runs the deployed bytes, as the deployed role, outside the source tree. The CTO's call.
4. **S91's None sink.** It is why S98 took three passes. Only the recorder-patched diagnostic named the swallowed `FileNotFoundError` and `KeyComponentRefused`.

## Rows

- **None new this pass.** S99-S102 are ruled, and executed as ruled: S99 included; S101 accepted and named per function in the packet; S102 deferred; S100 recorded-not-counted.

## What the third pass needs

1. **Both halves at HEAD naming blob `9d273fb8517a00288ec13d8dd0814a47af8782fa`.**
2. **(e), the apply under a ledger.** First, the pre-apply re-verification: halves 2 of 2, the blob, digests EQUAL, every built artifact the latest at its sha. Then safe-apply of the SAVED planfiles, 0-diff after. Then `CodeSha256 == built` 6 of 6, and one `raw_keys.json` member downloaded and hashed in each served zip.
3. **(f), rtf-10's arm (f), unchanged.** The bounded principal, real HTTP requests as each function's role, scope-resolved m of m with 0 UNEXPECTED:
   - over the rebuilt functions minus holdings, on the existing-map firms;
   - holdings and ycharts recorded and not counted (S100, S102);
   - S92 now measurable.
