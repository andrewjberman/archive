# IB-rtf-12 result (first pass): the premise measured, the manifest staged (11 objects), the build WITHHELD -- STOP at (d)

**Order:** `org/missions/D9/IRPT/IRPT_BCKEND/task-orders/IRPT_BCKEND.TO-IB-rtf-12.every-serving-zip-carries-the-raw-keys-file-its-id-module-reads.md` @083cc54350. GO msg 98272.

**Seat:** `0.7.0_AE_CloudOps~V`, worktree `/c/tmp/wk-irpt-6-ae1`. CLOUD was merged in, ff to 083cc54350.

**Nothing was built and nothing was deployed. The build store and the functions are unchanged.**

## What this pass did

1. **(a) The premise, re-measured.**
   - `_ids/raw_keys.json` was staged in **0 of 7** at the cut, and a `raw_keys.json` member was in **0 of 7** live zips (each downloaded zip's sha256 == its live `CodeSha256`).
   - `ids.py:64` and `:162 @HEAD` are printed by the battery.
   - **The `_ids/` census: 5 path constructions serving 3 of 3 families:**
     - `raw_keys.json`;
     - the firm registry (`:113-138`: env, then a `data/` walk-up, then beside);
     - `data/<seam>.json`, staged in 7 of 7.
   - **The registry resolves nowhere on the deployed layout for 4 of 7 functions:** directory-search, status, narrative and performance-adapter. That makes it a **second missing member, row S99, INCLUDED** as the face directs.
   - **S99 also CORRECTS S98's diagnostic.** S98's "with ONLY `raw_keys.json` the scope resolves" ran inside the repository, whose walk-up found the repo's `data/firm_registry.json`.
     - Re-run outside the repository, with the deployed layer mapped (`diag_ib_rtf_12.py`, 21 runs), directory-search and status FIRST fail on `keys.KeyComponentRefused REGISTRY_UNREADABLE`.
     - With both members, the scope resolves on 6 of 7.
2. **(b) The files, described for the halves:**
   - `_ids/raw_keys.json`: blob `eed32b39ad`, 6,492 bytes, the headers `_artifact/_purpose/_written_by/_grammar/_claim`, and `firms` with **k=3**. Each firm has account/relationship/client rows naming the UPSTREAM FIELD a firm's id is minted from, with citations. It holds no client identifiers and no credential-named keys, and has W=1 writer (`0.9.0_WK_IRPT_BCKEND~1`, 2 commits).
   - `data/firm_registry.json`: blob `99b8eeb54f`, 5,326 bytes, a generated view with **k=5** firms. `tree_token` is a folder token, not a secret. It has W=5 writers across 8 commits.
   - The id module keys by the VERIFIED tenant: `ids.py:408 raw_key_for(firm_id, ...)`, reached from `served.py:582` with `tenant`.
3. **(c) The manifest, @dbf7667178.** 11 `staged_from` objects were added, each immediately after and in the same shape as the `_ids/ids.py` object:
   - `raw_keys.json` in 7 of 7;
   - `firm_registry.json` in the 4 of S99;
   - `files[]` +11, `artifact_sha256` untouched 7 of 7, and a parse-diff equal to exactly these additions.
4. **(d) The build: WITHHELD.** A read-only prediction compared each live zip with what `build-and-upload.sh` would package: own members from DISK, staged members from their pins.
   - **Every `.py` member is byte-identical on 7 of 7.**
   - **The seam member `data/custodian_key_seam.json` MOVES on 5 of 7:** status, narrative, export-render, performance-adapter and ycharts-generate. It would go from the live CRLF hand copy (197,344 bytes) to the committed LF blob (191,120 bytes). That is the face's STOP, row **S101**.
   - **`irpt-ycharts-generate` has 2 members with no source:** `firm_registry.json` (row W4-S34) and `settings.json`, which was never tracked. So `build-and-upload.sh` refuses it, row **S102**.
   - Built 0 of 7. There is no packet, and the halves are 0 of 2.
   - **The DISK-vs-blob half of S101:** 29 of the 66 own members sit CRLF on disk in this checkout (`core.autocrlf=true`), and are identical to live today. A builder on an LF checkout would move all 29.

## R69-AC1: FAIL, by output (3 of 6 arms; STOP at (d))

`timeout 1800 py -3.12 .../battery_ib_rtf_12.py` @e7797ca699, rc 1.

- **(a) PASS:** `_ids/raw_keys.json staged: at the cut 0 of 7 (the premise); at HEAD 7 of 7 (after (c))`; `raw_keys.json in the live zips: 0 of 7 (the premise)`; the families 3 of 3, with a per-function class printed.
- **(b) PASS:** both files described; credential-named keys 0 and 0.
- **(c) PASS:** `staged_from objects added: raw_keys.json 7 of 7, firm_registry.json 4 ... files[] +11; parse-diff == exactly these additions: True`.
- **(d) FAIL:**
  - the seam member MOVES on 5 functions, and ycharts has 2 unresolvable members;
  - `built and verified at rest: 0 of 7`;
  - the packet ABSENT;
  - `halves: 0 of 2`.
- `RESULT: R69-AC1 FAIL -- 3 of 6 arms hold`. The token was not printed.
- One battery line reads `functions whose rebuild moves a member beyond the added ones: see above of 7`. The count is **5 of 7**, from the per-function lines above it.

## R69-AC2: JUDGMENT, recorded for 3.0.0_SA_CVO and not self-graded

**1. How a module-relative data file was omitted from every zip while every suite passed.**
- `ids.py:64 @HEAD` resolves `raw_keys.json` beside itself, and `:113-138` walks up for `data/firm_registry.json`.
- In the repository both exist at those relative places, so every test, battery and in-process harness that imports `_ids/ids.py` from the tree finds them.
- The manifest names only the modules. The zip flattens `ids.py` to `/var/task`, so both reads fail there.
- **The same class caught the seat's OWN diagnostic.** S98's "with ONLY `raw_keys.json` the scope resolves" ran inside the repository and inherited `data/firm_registry.json` through the walk-up (S99). Running the deployed bytes is not enough: the run must also sit OUTSIDE any directory that holds the source tree.

**2. What the build contract must carry.**
- A **build-time census of `__file__`-relative opens**, keyed on the IMPORT: every module the zip packages is parsed for `os.path.join(HERE/__file__, ...)` / `open(...)` targets, and each target must be a packaged member or an env-resolved path whose target is itself packaged or layered.
- This belongs to the binding-check class the CTO adopted @3580608505, never a filename list.
- **And the build must be reproducible from the committed tree** (S101, S102):
  - an `eol` attribute on the Lambda source trees, or the index-sourced member gate widened from `declared_blobs` to every data member;
  - otherwise two builders on two checkouts ship different bytes for the same commit.

**3. The identity bar's "deployed BYTES" clause.**
- Two independent layout defects (S98, S99) passed every check that ran the source tree under ANY identity.
- The bar @606e7d14ce ("the function's own execution role") was satisfied by rtf-10's arm (f), and that arm is what found them.
- The evidence supports stating the clause as law: **a served-path proof runs the deployed bytes, as the deployed role, outside the source tree.** Whether it is law is the CTO's.

**4. S91's None sink is why S98 took three passes to surface.**
- The `FileNotFoundError` and the `KeyComponentRefused` never reached CloudWatch.
- Only the recorder-patched diagnostic named them, and the None sink would have hidden S99 behind S98 had the diagnostic not been re-run outside the tree.

## Rows filed this pass (all BLOCKING, ARMED, disarm_owner `2.0.0_SA_COO~B`)

- **S99:** the registry is a second missing member, INCLUDED @dbf7667178. It corrects S98's with-the-file half.
- **S100:** holdings reads the directory POINTER as the artifact. Its EMPTY_GRANT is unreachable, and staging does not change that (source or env; not this order's).
- **S101:** a HEAD rebuild also moves the seam member CRLF->LF on 5 functions, so the build is withheld. Builds are not reproducible across checkout EOL settings.
- **S102:** `irpt-ycharts-generate` is unbuildable from HEAD, because 2 members have no source.

## What the re-hand needs (the issuer's rulings)

1. **S101:** accept the seam member's CRLF->LF on the 5 as part of the act (the S96 precedent). This seat recommends it; the packet then names it per function.
2. **S102:** K-CODE on 6 functions with ycharts deferred to a sourcing cell, or a sourcing cell first.
3. **S100:** holdings in (f) as recorded-not-counted, or a holdings cell first.
4. **Then:** the build under one ledger, the packet, the STOP at the halves, and (e)/(f) on the re-hand.
