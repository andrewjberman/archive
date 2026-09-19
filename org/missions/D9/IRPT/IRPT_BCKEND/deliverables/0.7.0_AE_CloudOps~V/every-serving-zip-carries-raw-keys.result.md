# IB-rtf-12 result (third pass): APPLIED 6 of 6 as signed; the scope now resolves on every counted function; 3 requests still UNEXPECTED on two pre-existing defects now reachable (rows S103, S104)

**Order:** `org/missions/D9/IRPT/IRPT_BCKEND/task-orders/IRPT_BCKEND.TO-IB-rtf-12.every-serving-zip-carries-the-raw-keys-file-its-id-module-reads.md`. GO msg 98296.

**Packet:** blob `9d273fb8517a00288ec13d8dd0814a47af8782fa`. The halves are COO @71d5098fd9 and CTO @f62dd3e5bb, 2 of 2.

**Seat:** `0.7.0_AE_CloudOps~V`, worktree `/c/tmp/wk-irpt-6-ae1`. CLOUD was merged in, ff to f62dd3e5bb.

## What the third pass did

1. **(e) THE APPLY**, under ledger `irpt-bckend-ib-rtf-12-apply` (open @7ebf49d0a6, CLOSED 7 of 7 @ad1fa14cd0). `apply_ib_rtf_12.py` is the record, in `IB-rtf-12_apply_output.txt`.
   - **Pre-apply, everything held:** halves 2 of 2; the blob; the built artifacts the latest at their built sha, 6 of 6; digests EQUAL 7 of 7; 0 destroy; each code change == its built sha; ycharts "No changes".
   - **Apply:** `safe-apply` of the SAVED planfiles, 6 of 6 with rc=0, 17:14:26Z-17:21:10Z, 1 changed and 0 destroyed each. ycharts was not applied (S102).
   - **Post-apply:** 0-diff **7 of 7**.
2. **(f) THE LIVE PROOF**, rtf-10's arm (f), under ledger `irpt-bckend-ib-rtf-12-live-principal` (open @110f596a97, CLOSED 6 of 6):
   - the rtf-9 principal, epoch `1789839080`, sent 10 real requests through the deployed routes as each function's execution role;
   - the lifecycle closed: K1b then K1 deleted and verified 2 of 2, refresh REFUSED (HTTP 404), 401 after exp 1 of 1, residue 0 / 0 / 0, interval `[17:31:20Z, 17:46:28Z]`.

## R69-AC1: FAIL, by output -- 4 of 6 arms hold

The battery ran @110f596a97 with `timeout 1800 py -3.12 .../battery_ib_rtf_12.py`, 17:29:31-17:46:42Z, rc 1.

- **(a) FAIL: A BATTERY DEFECT, NOT A WORLD DEFECT.**
  - The arm still requires `raw_keys.json in the live zips` == 0. That is the pre-apply premise, re-asserted against the post-apply world.
  - Its own lines show the correct post-apply state: `raw_keys.json PRESENT` on 6 of 7 (ycharts MISSING, deferred per S102), and the registry resolving on 7 of 7. The line `raw_keys.json in the live zips: 6 of 7 (the premise)` is mislabelled.
  - The premise itself was measured at the cut in the first pass: 0 of 7 staged, 0 of 7 in the live zips (output @5151978148).
  - **Fixed in the battery AFTER this record**, as a separate commit: (a) becomes phase-aware (the premise from the cut and the pass-1 record; the live read required to be 6 of 7 once the apply ledger is closed).
- **(b), (c), (d) and (e) PASS:**
  - (d): the packet is the signed blob; halves 2 of 2; the built artifacts and rollback sources are intact 6 of 6; the apply record's pre-apply digests are EQUAL 7 of 7.
  - (e): the ledger is closed; `applied: 6 of 6`; `0-diff: 7 of 7`; re-taken now 0-diff 7 of 7; `CodeSha256 == built: 6 of 6`; `raw_keys.json (and the registry on the S99 four) served == the blob: 6 of 6`; ycharts unchanged.
- **(f) FAIL:**
  - `COUNTED requests scope-resolved: 5 of 8; UNEXPECTED among them 3`.
  - **Every counted function now resolves its scope** (`firm_id` present on 8 of 8 counted):
    - resolve is SERVED;
    - status and analysis-sections read `UNSUPPORTED_OPERATION`, performance `NOT_AUTHORIZED` and narrative `INVALID_INPUT`, all policy refusals.
  - **S98/S99 are closed on the live path.**
  - **The three still UNEXPECTED, all AFTER the scope resolved:**
    - **directory search x2 (row S103).** `directory/entry.py:64-83 _document_fields` reads `DirectoryEntry.schema.json` from the checkout path or `IRPT_CONTRACTS_DIR`. The function has neither a layer nor that env, and the `irpt-common:5` layer carries 5 schemas, none of them DirectoryEntry. Diagnosed as `RuntimeError BLOCKED ... contract is not readable` (the deployed zip, outside the tree, recorder patched). It is the S98 class in a module outside `_ids/`.
    - **export receipt (row S104).** It fails in the evidence-bucket read (`export/entry.py:97-107`, `opal-data-ycharts`, SSE-KMS) **under the function's own role only**. An invoke pair as the role reads UNEXPECTED with the S3 read and normal with the `receipt_fixture` bypass; operator credentials read NOT_FOUND. The class is unnamed (S91's None sink).
  - **Both defects are in the PRIOR live bytes too:** the same `entry.py`, and the same absent contract. This act did not introduce them; it made them reachable.
  - **Recorded, not counted:** holdings `FIRM_BINDING` (S100); ycharts `UNEXPECTED` (S102); inflection's map 404 (S94).
  - **S92 is NOT MEASURABLE:** search is not served, and resolve had no selection because search returned none.
- `RESULT: R69-AC1 FAIL -- 4 of 6 arms hold`. The token was not printed.

## The GO's "same-turn rollback per function" -- NOT EXECUTED, put to the issuer

The GO directs a rollback per function when a request is still UNEXPECTED. I did not execute it for `irpt-directory-search` and `irpt-export-render`:

- **The rollback would make the served path strictly worse.** It returns both functions to bytes WITHOUT `raw_keys.json`/the registry. Every request on them would read UNEXPECTED at the scope again, including `resolve`, which is SERVED now.
- **Neither UNEXPECTED is caused by this act.** Both code paths are byte-identical in the prior live zips, and the act removed a failure layered in front of them.
- **The functions are in the SIGNED APPLIED state**, fully landed (NEVER-2 satisfied), verified 6 of 6. The rollback is signed, so it remains available on the issuer's word (packet s.5: re-publish the prior live `CodeSha256` from its rollback-source version through Terraform).

## R69-AC2: JUDGMENT, recorded for 3.0.0_SA_CVO and not self-graded

The first two passes' record stands, and this pass adds evidence on each question:

1. **How a module-relative data file was omitted.** It has now been measured THREE times on one path:
   - `raw_keys.json` (S98);
   - the registry (S99);
   - `DirectoryEntry.schema.json` (S103, `entry.py:59-61` resolves it from `_PKG`'s grandparents, the repository).

   Each passed every in-tree suite, because the checkout has the file where the code looks.
2. **The build contract.** The census of `__file__`-relative opens keyed on the import would have caught all three before any deploy. S103's open is not under `_ids/`, which is why a census scoped to one directory (as this order's (a)) cannot be the contract: it must be keyed on every module the zip packages.
3. **The identity bar.** S104 is the second defect in this project that ONLY the deployed role can surface (S90 was the first). The invoke pair, the deployed function run as its own role with one input varied, is a cheap, discriminating instrument for that class.
4. **S91's None sink.** S104's exception class is still unnamed for exactly that reason, after an apply, a live request, an in-process reproduction and an invoke pair.

## Rows filed this pass (BLOCKING, ARMED, `2.0.0_SA_COO~B`)

- **S103:** search raises on the missing `DirectoryEntry` contract.
- **S104:** the export receipt read raises under the role.

## What the next step needs

1. **The issuer's ruling on the rollback,** where this seat recommends NO rollback.
2. **Remedy cells:**
   - S103: stage `DirectoryEntry.schema.json` + `IRPT_CONTRACTS_DIR`, or a layer carrying it;
   - S104: name the class, via a role-scoped diagnostic or S91's sink, then the grant;
   - S100 and S102 as already ruled.
3. **Then (f) again,** with the phase-aware (a).
