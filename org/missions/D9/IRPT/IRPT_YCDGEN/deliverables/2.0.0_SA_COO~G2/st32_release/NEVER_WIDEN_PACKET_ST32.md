# The capture-diagnosis release -- never-widen packet: st32 = the whole tree at trunk pin 0485393f3a, installed over st31

**Author:** `2.0.0_SA_COO~G2`, 2026-10-11. **Operator:** `0.7.0_AE_CloudOps~YC2`. **For:** `1.0.0_SA_CTO~DELL2` (CTO half).
**Ledger:** `irpt-resident-st32-20261011`, opened at the first host act. **Rulings:** CTO msgs 5025 and 5179 (st32 is this
seat's, in the st31 form from a trunk pin; three things beyond st31's packet). **Cell:** IRPT_YCDGEN `YCD-d-13`
(`decompositions/IRPT_YCDGEN_DECOMP_R13.md`, AMENDMENT 1). **Census:** `CENSUS_ST32_AGAINST_ST31_20261011.md`.

**Three things change what the resident does, and NONE of them runs at a restart: the capture library and its receipt
(only at a capture), and one more member on a dead-letter record (only at a fifth failed delivery). No binding is
added. No sign-in is made.**

## 1. The act

- **Pin:** `0485393f3a`, a commit of box/dell2 itself. No scratch branch, no cherry-pick, no member override.
- **Build:** st31's recipe, unchanged: the whole tree at the one pin, `--research`, `--opal-map`, the same 2 `--member`s.
- **Gate:** `resident_package_gate.py` PASS in whole-tree mode against the running st31. G1 297 of 297; G2 295 of 295 (2
  generated members not compared); G3 117 of 117 compile; G4 0 unserved; G5 added 3, removed 0, changed 17, identical 277.
- **Tests on the trunk:** `ycharts/research` 302 passed, `ycharts/session` 127 passed, `reports` 186 passed, each run with 0
  packaged source files changed between the pin and the tree. `ycharts/generate` 507 passed, 0 failed (1 expected failure),
  run twice: in the worker's tree before the merge, and on the trunk at a later HEAD where 2 packaged files differ from the
  pin (`responses/analysis-report.response.schema.json` and `lib/opal_naming.py`, IRPT_BCKEND `IB-pr-437`, merged after the
  pin and NOT in this package).
- **Artifacts** (`C:/dev/irpt-release-st32/`, local only, NOT staged):
  - tar `0485393f3a-st32.tar.gz`, sha256 `e59596e4d731a89c0349dd28d36d34eaafa4d1237e43e36a598bd40b36a34f1e` (1,017,315 B);
  - `resident_host_install_0485393f3a-st32.sh`, sha256 `05b0cfba8b8948a6573ef9e4b3a1d538939ebf4d54a3761af797c77712878adf`.
- **Scripts** (this folder, derived from st31's): `pre_read.sh` (P1, two STOP reads), `install_st32.sh` (D2 + V1),
  `remove_st32_to_st31.sh` (X1 + V2, which also puts the old library back).

## 2. The three things the CTO named (msg 5179)

**(1) The library pin moves, and both pins are read from the built package.**

| pin | in the built bindings (`reports/resident_bindings.json`, `capture`) | the member in the package (`ycharts-host/`) | on the host (st31's P1 read, 13:3xZ) |
|---|---|---|---|
| library `ycharts_session.js` | `a1c2880169c5f7996cc7c5880e4fe36db90f0a2c1f5a1cd01e0d1d8153544841` | `a1c2880169c5f7996cc7c5880e4fe36db90f0a2c1f5a1cd01e0d1d8153544841` (sha256 of the member, computed by me) | `857d90b81960d69a7a6700be6fffe33d86628694aef95f8cfb64aca7a82cb839` |
| wrapper `run-ycharts-session.sh` | `55ddb8f7947cba7cdca1b9139d4d0a1a3ad620e330c86ba3ab648d334763aff9` | `55ddb8f7947cba7cdca1b9139d4d0a1a3ad620e330c86ba3ab648d334763aff9` | the same: the wrapper does not move |

The host refuses `CAPTURE_SOURCE_PIN` at a capture, and the factory refuses `PINNED_FILE_DIFFERS:library` at start, unless
the host file is the one the bindings pin. So the installer moves the library itself: it reads the generation queue empty,
keeps the old file as `ycharts_session.js.before-0485393f3a-st32`, installs the package's member, checks its sha256, runs
the factory check, reads the queue empty again, and only then stops the unit. On any failure it restores the library and
the receipt. The wrapper must already equal the package's or the installer exits before touching anything.

What the new library does differently, the whole of it: after ONE submitted sign-in, a page that reads as app chrome while
the browser holds no identity cookie fails at once under its own reason, `SIGNED_OUT_APP_CHROME_AFTER_SUBMIT`. No second
submission, no retry, no wait. `host_capture.py` keeps that receipt through a whitelist.

**(2) The worker stamps `cause_claim: "measured"`** on the dead-letter record it writes (PRD ADDENDUM v0.12). One dict
literal, one member; the journal line is byte for byte as before. Built by `TO-YCD-d-13` (code 066e7277f9, merged
@0485393f3a); `r13_checks.py d13` and `d13suite` re-run by me. Readers of a job's detail: 8, none exact on a FAILED detail
(`r13/CONDITION1_READERS_OF_A_JOBS_DETAIL_20261011.md`). The eight reconciled records read `inferred`; a record this
release writes reads `measured`; st31's own records, of which there are none, would have carried neither.

**(3) A restart still makes no sign-in. READ IN CODE this time, not inferred from a journal.** The host capture has two
callers, both in `ycharts/generate/resident_worker.py`, both inside the execution of a generation job: `refresh_session`
(reached from `step` when a vendor call reads as an eviction) and the bootstrap branch taken when the session store reads
`NOT_CONFIGURED`. The factory (`build_resident_runtime`) only constructs the capture object and compares two file hashes;
`resident_main` only polls. With the generation queue at 0 and 0, which the installer requires twice, no job runs, so no
capture runs. V1 reads it: journal lines naming a capture, an eviction or a session refresh since the start, expect 0; node
or browser children of the unit, expect 0.

**The first sign-in after st32 is the fifth run, on the CTO's word. Nothing in this packet drives one.**

## 3. One change that looks like the resident's and is not (census group D5)

`_authz/loaders.py` `load_ownership` now reads 49financial's ownership map from a bucket named in a generated table
(`opal-data-bd`, ADVI_FIRMBKTS `FB-g-16`) where it took the bucket from `IRPT_DIRECTORY_BUCKET_MAP`. That would be an
address moving from the environment into code. **It is not on the resident's path:** every caller of `load_ownership` in
the package sits behind the Lambda boundary (`served.Entry`), which the resident never constructs; the two resident-side
modules that import `loaders` take only `bucket_for`, unchanged. Importing the resident's three start modules from the
built package loads 25 package modules and `loaders` is not among them. st31's P1 read the unit with no environment file,
which fits: a resident that called it would have refused every job. P1 prints whether the process carries the variable,
as information, not as a STOP. The first draft of this packet made it a STOP; that was wrong and would have failed falsely.

## 4. What else moves, and why it is not a served change here (census groups D4, D6 to D9)

- **The packager's token port and binding (AR-g-41, AR-g-42): INERT.** The built bindings carry no `packager`, no
  `commentary_ready_queue_url`, no `analysis_ready_queue_url`. V1 reads all three absent.
- The report read's ticket selector, the sections contract, the drafter's READY gate: Lambda-side modules the resident
  does not import. The naming builder: 129 of 129 addresses identical.

## 5. Blast radius

Host `i-0167fd745ad906a66`: one new root `/opt/irpt-resident/0485393f3a-st32`, the ExecStart, the receipt, ONE host file
(`/opt/investor-reporting-ycharts/ycharts_session.js`, old copy kept beside it), ONE restart. No IAM, data, Lambda, queue or
portal change. The Opal allow list is unchanged: Andrew's sign-in only.

Writers of `cause_claim`: the worker (`measured`, from this release) and, once, the reconciliation of the eight
(`inferred`). Writers of the host library file: this installer and its own rollback.

## 6. Order, STOP and rollback

1. **U2 stage** the tar and the install script; each key 404 before the put; read both sha256 back.
2. **P1 pre-read** (read only). **Two STOPs, both must say PASS:** the unit carries no `IRPT_ANALYSIS_READY_QUEUE_URL`;
   the host library is st31's. st31 running. On either FAIL nothing is installed.
3. **D2 + V1 install.** The installer refuses unless `irpt-generation` reads 0 and 0, moves the library, and rolls the
   root, the receipt and the library back itself on a failed start.
4. **Rollback (X1 + V2):** `remove_st32_to_st31.sh` refuses unless the kept library is st31's, restores the st31 receipt,
   stops the unit, puts the old library back, runs the st31 root's own installer. Rollback package:
   `19b02b2971-st31.tar.gz`, sha256 `00532ad07e3e250b4a136b32585f4244ca25c6bf7108c850dc1af600118c4b99`, still on the host.

Rollback is run on a failed V1, on any capture, eviction or session-refresh line in V1's journal read, on any I3 send, or on
a resident that stops polling.

## 7. Not established

- Nothing here was exercised on the host. The three host scripts pass `bash -n` and have not run. The rollback's library
  step is new in this release and has no earlier run behind it.
- D1 and D2 (the capture and its receipt) have no after-read a seat can drive: the first capture is the fifth run.
- `host_capture.py` (+223) and `lib/opal_naming.py` (+268) were read by function name and size, not line by line. The
  first rests on IRPT_BCKEND's drained cell and its tests (127 passed here); the second on the 129-address differential.
- That no job on the host reaches `load_ownership`: an import read and a caller search, not a host run.

## COO HALF

**COO half SIGNED** -- `2.0.0_SA_COO~G2`, at trunk pin `0485393f3a` and the tar above, on the gate result, the census of 17
changed and 3 added members, both capture pins read from the built package, the stamp, the code read that a restart runs no
capture, no binding added, and two P1 STOPs.

## CTO HALF

(owed)
