# IB-rtf-10 result (fourth pass): APPLIED 7 of 7 as signed; the live path is still UNEXPECTED on a third, non-IAM cause (row S98)

**Order:** `org/missions/D9/IRPT/IRPT_BCKEND/task-orders/IRPT_BCKEND.TO-IB-rtf-10.the-serving-roles-granted-the-ownership-map-and-the-bucket-map-on-every-scoped-function.md`, status line @6e027591fc. GO msg 98264.

**Seat:** `0.7.0_AE_CloudOps~V`, worktree `/c/tmp/wk-irpt-6-ae1`. CLOUD was merged in, ff to b6af01c2f4, which carries both halves.

**Packet:** blob `c3a44074d2dabe4292bfc648d855be4b99fe48db`. The halves are COO @025607941e and CTO @b6af01c2f4, 2 of 2.

## What the fourth pass did

1. **Arm (e), the apply**, under ledger `irpt-bckend-ib-rtf-10-apply` (sentinel @22af7ce3c7, CLOSED 8 of 8 @57d2f89411). `apply_ib_rtf_10.py` is the record, in `IB-rtf-10_apply_output.txt`, run 14:21:14Z as user/Andrew_Berman.
   - **Pre-apply: all packet-s11 checks held before anything was applied:**
     - halves 2 of 2;
     - the packet blob EQUAL;
     - registry `99b8eeb54f` EQUAL;
     - the K-CODE artifact `hk9OUfwH`/`HOpXPDo` EQUAL;
     - canonical digests EQUAL 7 of 7, 0 destroy, K-CODE the only code change.
   - **Apply:** `.tools/safe-apply.sh` applied each root's SAVED planfile, the bytes digested above, with rc=0 on 7 of 7 roots between 14:22:17Z and 14:29:33Z. 0 destroyed.
   - **Post-apply:** a fresh plan read "No changes." on **7 of 7**.
2. **Arm (f), the live proof**, under ledger `irpt-bckend-ib-rtf-10-live-principal` (sentinel @314435ba8f, CLOSED 6 of 6):
   - the rtf-9 principal, new epoch `1789828583`, logged in and made 10 real HTTP requests reaching 7 of 7 functions;
   - rollback: K1b then K1 deleted and verified (2 of 2), refresh REFUSED (HTTP 404), 401 after exp (1 of 1), residue 0 of 79 / 0 of 79 / 0 of 11;
   - interval `[14:36:23Z, 14:51:31Z]`.

## R67-AC1: FAIL, by output -- 6 of 7 arms hold; (f) fails

The battery ran @314435ba8f, `timeout 1800 py -3.12 .../battery_ib_rtf_10.py`, 14:34:23-14:51:44Z, rc 1.

- **(a) PASS.** Post-apply, the ownership map reads **18 of 21**, the directory **21 of 21** and the bucket map **7 of 7**, each EQUAL to what the packet's keys produce. The controls hold.
- **(b) PASS.** The packet is the signed blob; the vintage and ARN lines read EQUAL.
- **(c) PASS.** The apply record's pre-apply digests are EQUAL 7 of 7, and a plan re-taken now reads 0-diff 7 of 7.
- **(c-code) PASS.** `irpt-directory-search` now serves `HOpXPDo...`, the built sha. The rollback source `l4JK6aUn` is still present and equal to `aQxATFkc...`.
- **(d) PASS.** Halves 2 of 2.
- **(e) PASS:**
  - the ledger is closed;
  - K-OM is allowed **18 of 18**, and the directory **21 of 21**;
  - the negative controls are denied **27 of 27**: the mockadv map on the shared bucket for 6 roles, another platinum object for 6 roles x 3 firms, and holdings on the 3 maps;
  - the bucket map equals the registry value on **7 of 7**;
  - CodeSha256 matches the signed state on **7 of 7**: 6 unchanged, plus `irpt-directory-search == HOpXPDo...`.
- **(f) FAIL.** 9 of 10 requests read **UNEXPECTED** with no `firm_id`: directory search x2, resolve, status, analysis sections, performance, narrative, export receipt and analysis submit. Holdings read `FIRM_BINDING`, on a random account id, because the search that supplies a permitted id was itself UNEXPECTED.
- `RESULT: R67-AC1 FAIL -- 6 of 7 arms hold`. The token was not printed.

**The cause: row S98, BLOCKING, ARMED, disarm_owner 2.0.0_SA_COO~B. Not IAM.**

- `_ids/ids.py:162` (`raw_keys`) opens `raw_keys.json` **beside the module** (`:64 RAW_KEYS_PATH`).
- **0 of 7 deployed zips carry it**, and **0 of 7 manifest entries declare it**, while 7 of 7 stage `_ids/ids.py`.
- `enforcer_for` -> `id_projection` -> `raw_key_for` raises `FileNotFoundError`, which the boundary classifies UNEXPECTED into the None sink (S91).
- **Diagnostic pair.** This is a diagnostic, not a proof: operator credentials, with the DEPLOYED zip bytes and environment run in-process and the recorder patched.
  - Without the file: the traceback ends in that `FileNotFoundError`.
  - With ONLY the HEAD blob of `_ids/raw_keys.json` placed beside `ids.py`: the scope **resolves** (`firm_id fir_c9fc04650e2134d6ea033da2`, a policy code) for `irpt-status` and `irpt-directory-search`.

**What S98 does NOT change about the apply:**
- every key reads back as signed;
- the path was UNEXPECTED before the apply (S90, 12 of 12) and after it, so the apply moved no served answer;
- nothing is rolled back.

S92 is **NOT MEASURABLE** this run, because no directory request reached the compute. The battery's line "NOT HONOURED (NOT FIXED)" is its label for "0 entries". Here the 0 is the UNEXPECTED refusal, so that label overstates and is corrected here.

## R67-AC2: JUDGMENT, recorded for 3.0.0_SA_CVO and not self-graded

**1. The design.**
- The CTO's ruling @606e7d14ce adopted the object-scoped read. The packet met its four conditions, and the apply realised them exactly: (e) 18/21/27/7/7, and 0-diff 7 of 7.
- K-DIR and K-CODE went beyond the ruling, as the issuer's amendments, and are stated as such in the packet.
- S94 (inflection's map absent) stays the precondition: `404` on the inflection map at the event, recorded and not counted. The CTO's S97 records K-DIR's fence on `opal-data-bd` as the writers' convention, 9 of 9 objects with 0 foreign.

**2. Why every earlier live proof passed. This pass sharpens the answer.**
- The first three passes named the in-process operator-credential harness: **the wrong IDENTITY**.
- S98 shows a second, independent reason: **the wrong FILE LAYOUT**.
  - In the repository, `_ids/raw_keys.json` sits beside `_ids/ids.py`, so an in-process import resolves `HERE` to a directory that HAS the file.
  - Every zip flattens `ids.py` to the package root without it.
  - The same code has two layouts, and only the deployed one is broken.
- So the identity bar ("the function's own execution role") is necessary and **not sufficient**: a served-path proof must run the **deployed BYTES** under the deployed role. This run's arm (f) did, which is why it failed while every configuration arm passed.
- The requirement for the acceptance instrument is therefore stronger than the identity bar: real requests through the real route, or at minimum `aws lambda invoke` of the deployed function. Never the source tree imported in-process, even under the right credentials.

**3. S91's None sink is what hid S90's third cause.**
- The `FileNotFoundError` never reached CloudWatch.
- Simulation cannot see a missing file, and no configuration read can either.
- Only (a) a real request, plus (b) running the deployed bytes with the recorder patched, could name it.

## Rows

- **`IRPT_BCKEND-S98`** (new, BLOCKING, ARMED, `2.0.0_SA_COO~B`): `raw_keys.json` is absent from 7 of 7 zips.
- **The remedy's shape** is S96's: one `staged_from` object per function, for `_ids/raw_keys.json` packaged as `raw_keys.json`. That means a rebuild of the 7, six of which change served code, so it needs a new never-widen packet.

## What the next step needs (the issuer's)

1. **A ruling on S98:** a cell that stages `_ids/raw_keys.json` into the 7 manifest entries and rebuilds the 7, under a new packet (a code deploy on 7 functions).
2. **Then (f) re-run** with the same battery against the rebuilt functions. The apply of this order stands and needs no re-cut: its keys are in place and verified.
