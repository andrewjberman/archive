# IB-rt-5 -- THE GOLD FIRST-MINT: result

**TO:** `IRPT_BCKEND.TO-IB-rt-5` | **serial:** `0.4.0_DS_ClientPlatform~X` |
**branch:** `wk-irpt_bckend-2-ds` | **worktree:** `/c/tmp/wk-irpt-2-ds`
**Invocation:** `timeout 600 python org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.4.0_DS_ClientPlatform~X/battery_ib_rt_5.py`
**Result:** `rc=0`, **4 of 4 arms PASS**, final line `IBRT5-FIRST-MINT-SERVED`.

---

## What changed in the world

`s3://opal-data-mdpf/code/scripts/assets_gold/investor_reporting/investor-reporting.tar.gz`
now exists. That prefix held **0 objects** before the act and holds **1** after.
The two investor-reporting runners, committed in round 1 and served by nothing,
are inside it under their own sha stamps.

Two commits, in the order NEVER-2 requires:

| | commit | what |
|---|---|---|
| declare + OPEN sentinel | `36e4fbf826` | `CODE_TREES['mdpf']['bundles']` gains `investor_reporting`; ledger entry and its OPEN sentinel committed **before** the mint |
| mint + CLOSE | `e9a6ba27db` | all three legs proven, entry CLOSED, sentinel removed, **before** any grading read |

Both are LOCAL to `wk-irpt_bckend-2-ds` (push state: not pushed; the issuer merges
at the drain).

---

## The four arms

### (a) DECLARED
The guard's own line, not a resolver call:

```
ERROR: no bundle named 'nonexistent' declared (declared: ['accrual_bridge', 'investor_reporting'])
```

Denominator: 2 declared bundles. The pre-edit negative control on the same command
read `declared: ['accrual_bridge']` with rc=2 -- which is round 1's rows W1-S8 and
W2-S5 reproduced directly.

**The self-test is used as a CONTROL, because it was already red.** Measured on
this worktree BEFORE the edit:

| suite | baseline | after | |
|---|---|---|---|
| `.tools/test_code_trees_invariant.py` | FAIL 3/18 | FAIL 3/18 | output **byte-identical** |
| `.tools/test_safe_deploy.py` | FAIL 7/14 | FAIL 7/14 | differs only by a tempdir nonce inside a pre-existing failure line |
| `.tools/tests/*.py` (standalone) | 47 PASS / 8 FAIL of 55 | 47 PASS / 8 FAIL of 55 | same 8 files |

The three invariant failures are a frozen `PIPELINE_MAP` that predates the `advi`
tree (added 2026-08-18); the seven deploy failures are fixtures built outside the
workspace (`INDEX_MISSING`) and `Strings must be encoded before hashing`. None is
reachable from a bundle addition, and the byte-identical invariant output is the
discriminator that says so. Row `IRPT_BCKEND-S27`.

⚠ `pytest .tools/tests/` collects **ZERO** -- `test_fabric_check_classify.py`
raises `SystemExit` at import and takes the whole directory with it
(`INTERNALERROR ... no tests ran`). The counts above come from running each file
standalone, which is how these tests are written to run. The runner is committed
beside this file as `run_tools_tests.sh` so the count is reproducible rather than
asserted.

### (b) MINTED, verified on the served artifact
The mint ran through the guard's own explicit first-mint path
(`.tools/safe-deploy.sh --mint-bundle investor_reporting`, rc=0), never a bare
`aws s3 cp`. Verification re-derives everything with a **different instrument**
than the mint's internal check -- `aws s3api head-object` plus `sha256sum` of the
repo bytes:

```
ContentLength 26935   ETag cd188f6edb7270300a7409d66f9a3432 (== the mint's local md5)
VersionId BAv6hA9Iut0wlKFtuq5PsOKfl4hMEKy5   SSE AES256
directory-runner-sha256  = 431e89285a609fbf3cd695f4cc88722d2f912c37b5e3e88149a9fcd3dff2f491  MATCH
holdings-snapshot-sha256 = 18838c953c4b2c6fb24a83aa546ab7a69a4471dcad7909a4083846e2076b8dc3  MATCH
MEMBERS verified: 2 of 2   |   KEYS at the prefix: 1 of 1
```

**The denominator is 1 key, not 2, and that is not a shortfall.** The face grades
"each of the 2 keys". The guard's bundle mechanism mints exactly one object:
members are tar members inside one gzip payload and `mint_bundle` does a single
`s3 cp` to a single `b['s3_key']`. Minting two loose twins would satisfy the
literal words and is refused here -- the X-iii design freezes the loose leg for a
bundle member (CTO 2026-08-06, no S3 roster twin). Row `IRPT_BCKEND-S25`.

**The per-member sha keys are distinct, and that is load-bearing.** The L5 note
says `sha_metadata_key: script-sha256` for both members. `build_bundle_payload`
assigns `shas[spec["sha_metadata_key"]]` inside a loop over sorted members, so one
shared key collides: only `holdings_snapshot.py`'s sha would have reached S3,
under a stamp that reads as though it covered both files. `accrual_bridge` -- the
shape this order says to copy -- is per-member for exactly this reason. Row
`IRPT_BCKEND-S26`.

### (c) MEMBER now, with the input held fixed
Instead of editing a runner (BOUNDS 1 forbids it while `RT5-AC1(c)` asks for a
no-op commit -- row `IRPT_BCKEND-S29`), the gate's own `--commit-range` path was
run over the two **real commits that added the runners**: `3654197107` (IB-s-1)
and `2dbc92e956` (IB-s-12). That is byte-identical input to what produced round
1's SKIP-NOT-MEMBER finding, so the before/after varies only the declaration.

```
BUNDLE-ROUTED: .../directory_runner.py  -> bundle investor_reporting (loose leg frozen 2026-08-11, X-iii)
BUNDLE-ROUTED: .../holdings_snapshot.py -> bundle investor_reporting (loose leg frozen 2026-08-11, X-iii)
```

**In-run negative control.** The same runs, the same prefix, still print:

```
SKIP-NOT-MEMBER  [mdpf] .../tests/test_directory_runner.py
   probed s3://... -> 404; prefix .../tests/ carries 0 member(s) (single page).
```

2 of 2 runners MEMBER, 2 of 2 sibling tests still SKIP-NOT-MEMBER. So the MEMBER
verdict **discriminates** rather than blanket-passing, and "tests excluded from the
bundle" is measured, not assumed.

**Idempotence:** every mint this cell performed -- the explicit one and both gate
runs -- produced md5 `cd188f6edb7270300a7409d66f9a3432`. `build_bundle_payload`
zeroes mtime/uid/gid and gzips with `mtime=0`, so a re-mint is a byte-identical
overwrite and the ETag is a content address rather than a timestamp lottery.

### (d) LEDGER
Entry `org/critical_paths/change_management/20260911T1227Z_irpt-bckend-rt5-mint_deploy_completion.md`
reads CLOSED, all three legs carry proof, the OPEN sentinel is gone. Both hashes
are read from git history by the battery, not typed: OPEN `36e4fbf826`, removal
`e9a6ba27db`.

---

## Two environment traps the battery had to be repaired around

Recorded because they cost two runs and both fail in the *quiet* direction:

1. **Bare `bash` here is the WSL stub.** It answers `Windows Subsystem for Linux
   has no installed distributions` on stdout and exits, so a shelled gate run
   returns a clean-looking empty result rather than an error -- the battery read
   `declared bundles (denominator 0): []` and called arm (a) FAIL while the
   declaration was in fact live. Fixed by `.tools/git_bash_resolver.bash_argv`.
2. **`.tools/aws` is an extensionless bash wrapper**; `CreateProcess` raises
   `OSError WinError 193` on it from Windows Python. `safe_deploy_core.py` carries
   the same note about `comp-pipescript`. Fixed by using the `.cmd` twin and
   stripping CRLF.

---

## What this does NOT prove (for `3.0.0_SA_CVO` at L9)

**The bundle is not the whole runner.** Both members import `boto3`, `jsonschema`,
`pandas` and `trading_calendar`; the bundle carries **2 files and no dependency**.
`trading_calendar` is first-party (`lib/trading_calendar.py`) and both runners
reach it by `_REPO = Path(__file__).resolve().parents[4]` then
`sys.path.insert(0, _REPO / "lib")`. On a host where the tar is unpacked **flat**
into a scripts directory -- which is the `accrual_bridge` pattern (`tar -xzf` into
`/opt/mdpf/scripts/gold/`) -- `parents[4]` is not a repo root, `lib/` is not
beside it, and `import trading_calendar` raises at import time. **Nothing in this
cell exercised either runner on any host.**

**No consumer of this object exists yet.** A census of the tarball name returns 9
hits across 31,208 files: the declaration, this cell's own artifacts, and the
ledger entry. Nothing fetches it, nothing untars it, no schedule references it.
The mint makes the code *reachable*; IB-rt-6 is the cell that makes it *run*.

**The served artifact proves DEPLOYED, not EXERCISED.** It proves the declaration
resolves, the bytes landed, the stamps match the repo files, and a future member
commit routes to the bundle. It proves nothing about whether either runner
executes correctly, on which host, against which data, or on what schedule.

**Two round-1 batteries will now read a FALSE RED** -- `battery_ib_s_4.py` and
`battery_ib_s_12.py` both grade "served" as `head-object` on a **loose per-file
key**, and those keys are permanent 404s by design now. `battery_ib_s_12.py` also
probes `--mint-bundle holdings_snapshot`, a bundle name that does not exist (the
declared bundle is `investor_reporting`, of which that file is a *member*), so it
will still print `DEPLOY LEG: BLOCKED` after a successful first-mint. Row
`IRPT_BCKEND-S30`. The current instrument for this surface is this battery.

---

## Rows filed (6), none of which stopped the work

| id | one line |
|---|---|
| `IRPT_BCKEND-S25` | the mechanism mints 1 key, the face grades 2 |
| `IRPT_BCKEND-S26` | one shared `sha_metadata_key` collides and silently drops a member's sha |
| `IRPT_BCKEND-S27` | the guard's self-tests were already red pre-edit; the run is a control |
| `IRPT_BCKEND-S28` | the face's `IRPT_BCKEND-D-S<k>` id form is refused by the ratified schema |
| `IRPT_BCKEND-S29` | `RT5-AC1(c)` asks for a runner edit that BOUNDS 1 forbids |
| `IRPT_BCKEND-S30` | round-1 batteries read ABSENT after a correct first-mint |
