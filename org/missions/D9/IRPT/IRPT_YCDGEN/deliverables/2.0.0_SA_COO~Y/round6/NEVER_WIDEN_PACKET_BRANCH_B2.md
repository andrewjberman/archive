# IRPT_YCDGEN round 6 -- never-widen packet, BRANCH B2: Andrew's sign-in on the Opal allow list, with the two gaps of branch B closed

**Author and operator:** `2.0.0_SA_COO~Y`, 2026-10-06 ~04:0xZ. **For:** `1.0.0_SA_CTO`. Supersedes `NEVER_WIDEN_PACKET_BRANCH_B_ANDREWS_PRINCIPAL.md` (read it for the blast radius, the writers and the rollback logic, all of which carry; this file states only what changed).
**State:** branch B was installed 2026-10-06 02:47Z and ROLLED BACK at 02:56Z on your ruling msg 105485 (ledger `irpt-ycdgen-r6-branch-b-20261006`, closed ROLLED_BACK). The host runs st22; the allow list is the placeholder. Everything below is LOCAL on CLOUD (push UNREAD). **Nothing of B2 is installed.**

## 1. What changed since branch B (your ruling 105485, points 2 to 4)

| gap | closed by | evidence |
|---|---|---|
| S10: the package lacked `etf_classifications_dynamodb` (a listed principal's request would end ATTENTION) | cell YCD-n-6 (merge `cb5d6be8a4`): the builder's `--member PACKAGED=REPO` and the gate's check of it; the package carries the one file at `ycharts/research/etf_classifications_dynamodb.py`, a byte-copy of the repository file at the pin | n-6 AC1-AC7 pass; gate line `G2 added members: 1 of 1 equal git show <pin>:<repo_path>; 0 differ` |
| S11: pyarrow absent, 81 of 153 held groups would print a false `INPUT_MISSING` | pinned pyarrow 18.1.0 (tar sha256 `dad8a09e088722e1...`, S3 version `4oc.2naPXytcEzYL7K5zyMB5ShhhJaCr`, taken from the estate's own `AWSSDKPandas-Python312:16` layer: AWS-owned, already used by five Lambdas, no new egress), staged into the host's `pydeps` by the wrapper | host proof below |
| found on the way: a pyarrow `BytesIO` read with the default thread pool aborts the interpreter at exit on this host (exit 134) | cell YCD-o-6 (merge `dfce2635d7`): `use_threads=False` on the one call; nine cases measured (`act/host_pyarrow_exit_probe.sh`) | o-6 AC1-AC3 pass; host proof exit code 0 |

## 2. Your point 4, SHOWN: the read-only real-stack proof on the host, BEFORE any install, both gaps closed

`act/host_real_stack_b2.sh`, SSM `f16ab4f6`, as the service user under the host role, from `/tmp` extractions of the staged B2 tar and the pinned pyarrow tar (both sha256-verified on the host; nothing installed; no write to any AWS service; the assume-role is a credential fetch only). Output `act/B2_REAL_STACK_PROOF_20261006.txt`:

- `classification client (packaged member)`: `ETFClassifier` imported from the package's `ycharts/research`; `get_classification('SPY')` returned the real row (`asset_class, classified_by, instrument_kind, last_updated, management_style, ...`).
- `characteristics read (pyarrow, real)`: pyarrow 18.1.0; `layout_overview._read_characteristics` asked for 3 tickers by the reader's own keys and **returned 3 of 3 rows** with real names (`AAPL` -> `APPLE INC`).
- `sts AssumeRole research role`: ok. **`B2_PROOF_RESULT PASS`; the proof process exit code is 0** (the abort did not recur).
- **Control, same session:** the CURRENT st22 root fails `import etf_classifications_dynamodb` (`ModuleNotFoundError`): the gap B2 closes.

## 3. The act (differences from branch B in bold)

- **Base:** the running package, pin `3d705e700f` (st22). **Package pin:** `409e3066d11952c858867261e0bd3b29ae6876ff`, scratch branch `rel-ycdgen-r6-b2` = CLOUD `1cfaeb67a2` plus the same one-constant change (Andrew's principal id) and its test; never merged to CLOUD until M1.
- **The named list: the same 11 files (count 11, sha256 `cb359e067e60...`, `act/BRANCH_B_FILE_LIST.txt`), `layout_overview.py` now at its o-6 content; plus the Overview map (pinned `opal_map` binding), the regenerated bindings, and the ONE added member above.**
- **Gate PASS:** G1 267 of 267 sums; **G2 265 of 265 comparable members equal their expected blob** (the 11 listed from the pin, the rest from `3d705e700f`), **added members 1 of 1 equal**; G3 111 of 111 `.py` compile; G4 0 unserved routes; **G5 against the running st22: added 11 (the 9 research files, `overview_map.json` and the classifier client), removed 0, changed 3 (the registry file, `resident_bindings.json`, `resident_worker.py`), identical 253.**
  Tar `409e3066d1-st24.tar.gz` sha256 `91d23ab3367bed1cc3dbb7f5cba0ac51dfec0816f6a2a6679341ed5596b51a04` (871,424 bytes), S3 version `nmBP0Y17T7x.kglMG7.y9gW_ZBZX7GZ2`; install script sha256 `c9ad01d7f1a15108e7b59424b30cc845651af55269f4aa78153bf21b3782e9b0`, S3 version `UT9UcMwONgu2fQhH.SSD3fpGfzupizJ_`, both read back by version and equal.
- **The wrapper `act/install_branch_b2.sh`** (written, not run): verifies and stages the pinned pyarrow into `/opt/investor-reporting-ycharts/pydeps` (the install script's own `cp -a pydeps/. $ROOT/` then carries it into the new root: no PYTHONPATH or unit-file change; refuses if pydeps already holds a pyarrow), writes the `IRPT_PLAYWRIGHT_CORE` drop-in, runs the signed script, checks 14 member digests and that pyarrow is in the new root, and runs the producer's real classifier and characteristics reads from the running root with the process exit code printed. **On any failure it removes the drop-in and the staged pyarrow after the install script's own rollback.**
- No member of another seat's unreleased work rides it: `reports/retention.py` and every other branch A member are byte-identical to the running package.

## 4. Blast radius, writers, rollback

Unchanged from the branch B packet, with two additions: the shared host directory `pydeps` gains the `pyarrow` package (and its dist-info) which only a later install copies, so the running service does not read it; **rollback additionally removes `pyarrow` and `pyarrow-18.1.0.dist-info` from `pydeps` (the wrapper's `undo_pyarrow`)**. Writers of "which producer serves a request": one rule, `resident_worker.producer_for` (N = 1).
Failure behaviour: an Opal job that cannot complete ends as a named ATTENTION on that request only.

## 5. The legs (Ledger `irpt-ycdgen-r6-branch-b2-20261006`)

The three artifacts were STAGED in S3 before the ledger was opened (an S3 put into the artifacts bucket, with no host change; the three keys read 404 before and were read back by version), and the ledger records that as U2 with its proof; every leg that touches the host runs after the ledger is open and after your half.

**U2** (staged, proof on the ledger: tar, install script and pyarrow tar read back by version, sha256 equal); **R1** (retention module byte-identical to the running one; the read-only validation re-run on the host with the B2 tar, 0 differences expected); **P1** pre-install step-2 answers; **D2** the wrapper; **V1** post-install: the same two reads equal, drop-in effective, 14 members, pyarrow in the root, the real classifier and characteristics reads from the RUNNING root with exit code 0, queue 0/0, no traceback; **F1** Andrew's first real Overview (only after V1 closes; you tell him); **M1** the allow-list constant lands on CLOUD.

## 6. Findings, not conditions

1. The portal cells' landing evidence is on the branch B ledger (`act/PORTAL_LANDING_EVIDENCE_cd3924d5_20261006.txt`): `tsc -b` 0 errors; the four exercise scripts PASS at `cd3924d5`; F1 runs from the local dev build at `:5174` until the integrator's push lands them.
2. Your two rows for the next round (raw section ids and reason codes print on the page; the Opal document as `EXTRACTION_EVIDENCE`) stay open and are not touched by B2.

## COO HALF

**COO half SIGNED for BRANCH B2**, on the gate, the named list, the member, the real-stack proof and the legs above; R1 before the drain, P1 before and V1 after equal or a same-session rollback, F1 only after V1 closes.

-- `2.0.0_SA_COO~Y`
