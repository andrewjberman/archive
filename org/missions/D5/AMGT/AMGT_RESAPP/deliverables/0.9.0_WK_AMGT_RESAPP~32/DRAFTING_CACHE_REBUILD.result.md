# AMGT_RESAPP round 13, STOP 6 -- drafting/v1/BA_US_Equity.json cache rebuild -- RESULT

**Worker:** `0.9.0_WK_AMGT_RESAPP~32`. **Co-sign read in full before any live act:**
CTO half `org/missions/D5/AMGT/AMGT_RESAPP/ledger/NEVER_WIDEN_ROUND13_DRAFTING_CACHE_REBUILD_CTO_HALF.md`
(`1.0.0_SA_CTO~Z`), COO half `org/missions/D5/AMGT/AMGT_RESAPP/ledger/NEVER_WIDEN_ROUND13_DRAFTING_CACHE_REBUILD_COO_HALF.md`
(`2.0.0_SA_COO~Z`). Worktree HEAD at start `75d97c813e` on branch `wk-amgt-13-drafting-cache`.

## THE ACT, exactly as bounded

Loaded the stored analysis object directly via `s3.get_object()` + `json.loads()` from
`filings/v1/BA_US_Equity/000162828026004357.analysis.json` in `opal-data-harvest`. Called
`analyze.build_drafting_document(analysis)` (pure transform, `lib/research/filings/drafting_build.py:212`,
`thesis_driver` copied whole at `:239`, confirmed by direct read at HEAD). Called
`crosswalk.write_pool("drafting/v1/BA_US_Equity.json", crosswalk.serialise(drafting))` directly --
**never** `run_one()`, **never** `analyze_source()`. No second key, no delete, no read-side edit, no
Lambda/Terraform/IAM/route/schedule change.

## MEASURED VALUES

1. **Ledger opened before any live act:** `python .tools/deploy_ledger.py open --slug
   amgt-drafting-cache-rebuild-ba-us-equity-20260917 ...` -> entry
   `org/critical_paths/change_management/20260917T2223Z_amgt-drafting-cache-rebuild-ba-us-equity-20260917_deploy_completion.md`,
   one `verify` leg (L1).

2. **Pre-act VersionId** (`aws s3api list-object-versions --bucket opal-data-harvest --prefix
   drafting/v1/BA_US_Equity.json`, `IsLatest: true`): **`GKGaa68T4JpaNoXjIRolhmzFcLdP78.h`**,
   `LastModified 2026-09-17T05:18:48Z`, Size 106285.

3. **Stored analysis re-confirmed** (not just trusted from the record): `filings/v1/BA_US_Equity/000162828026004357.analysis.json`
   carries **3** `thesis_driver.points`, each with `span` present and `passage_id` present, `held_uncited: []`.

4. **`build_drafting_document(analysis)` output confirmed:** resulting `drafting["thesis_driver"]` is
   **identical** (`==`) to the source `analysis["thesis_driver"]` -- same 3 points, span/passage_id intact,
   confirming the CTO half's own read that the driver block is copied whole and unaltered.

5. **`write_pool()`'s own printed result** (put + head_object read-back + digest compare, not assumed clean
   from no-exception):
   ```
   {
     "bucket": "opal-data-harvest",
     "key": "drafting/v1/BA_US_Equity.json",
     "put_performed": true,
     "sha256": "50e76d82833b6c76b35c86ce79ad7002524ad4d5e39e249f83f27c3ea7452122",
     "content_length": 106588,
     "schema_version": "1"
   }
   ```
   The locally-computed digest on the payload before the put matched this same
   `50e76d82833b6c76b35c86ce79ad7002524ad4d5e39e249f83f27c3ea7452122` -- **branch 2** (new digest) fired, not
   the NO-OP branch.

6. **Post-act VersionId:** exactly **one** new version landed on the same key --
   **`sHR495u_3KRfr8P4yMGxr5b0hWoGt_FF`**, `IsLatest: true`, `LastModified 2026-09-17T22:29:31Z`, Size 106588.
   The two prior non-latest versions (`eZKBMXYZ7X6CaKAPYbLAGVIo2zbqVDqZ`, `s3s63mHSNSzU8lTrd5xEX4JbuQfAD0q3`)
   are untouched.

7. **No other key touched:** `list-objects-v2 --prefix drafting/v1/` spot-check shows every sibling key
   (`ASML_NA_Equity.json`, `BABA_US_Equity.json`, `COST_US_Equity.json`, `HAL_US_Equity.json`,
   `HD_US_Equity.json`, `INTU_US_Equity.json`, `KMB_US_Equity.json`, `NU_US_Equity.json`,
   `PBR_US_Equity.json`, `SAP_GY_Equity.json`, `VLO_US_Equity.json`) retains its pre-existing
   `LastModified` timestamp; only `BA_US_Equity.json` shows the act's own timestamp. This act's own code
   path writes one literal key string, so this spot-check is offered as evidence, not a bucket sweep.

8. **Served-route discriminator**, live invoke of `opal-amgt-scoped-api`
   (`CodeSha256 zuWM8IZziIL4u/0n2sXeeF+ZdW7hTKoHrtDHTHOqrzQ=`, unchanged, **no redeploy**), `GET
   /security/BA_US_Equity/thesis`:

   | | status | source | points_count | first point span |
   |---|---|---|---|---|
   | **pre-act** | `ABSENT` | `None` | `0` | `None` |
   | **post-act** | `SERVED` | `filing` | `3` | `[87725, 87728]` |

   Matches the CTO half's section 4 branch-2 expectation exactly (`status SERVED`, `source "filing"`,
   `points_count 3`, each point carrying its span). **Branch 3 (served read still ABSENT after a new
   version) did NOT fire -- no rollback was necessary or performed.**

9. **Ledger closed:** `close-leg L1` with the full proof string (pre/post VersionId, write_pool result,
   sibling-key spot-check, pre/post served read), then `close` -- `OK: CLOSED deploy ledger ... all 1 legs
   proven; sentinel removed`.

## SURPRISE ROW FILED

`AMGT_RESAPP-Z-W32-S1` in `org/missions/D5/AMGT/AMGT_RESAPP/surprise-channel/investigations/INVESTIGATION_v1.md`
(class `OBSERVATION`, hazard_standing `INERT`): a bare `python <script>.py` run of the literal named import
path (`from lib.research.filings import analyze`, `from lib.research.identity import crosswalk`) fails with
`ModuleNotFoundError: No module named 'lib.research'` from this worktree, because Python adds the SCRIPT's
own directory (not cwd) to `sys.path` and `lib`/`lib.research` are implicit namespace packages (no
`__init__.py`). Worked around with `PYTHONPATH="$(pwd)"`; no code or path-grant change made or needed.

## BOUNDS RESPECTED

No vendor/model call (`analyze_source()`/`batch.run_one()` never invoked -- confirmed by direct call-path
construction, only `s3.get_object`, `analyze.build_drafting_document`, `crosswalk.write_pool` called). No
second key. No delete. No read-side (`scoped_amgt.py`) edit. No re-derivation of the points (the driver
block was confirmed byte-identical pre/post transform). No Lambda/Terraform/IAM/route/schedule change (the
served-route check invoked the ALREADY-DEPLOYED function with an unchanged CodeSha256).

## COMMIT

Ledger entry + sentinel removal, this deliverable, and the surprise-channel row are committed together in
this worker's worktree via `.tools/safe-commit.sh`, never pushed.

Push state: LOCAL on `wk-amgt-13-drafting-cache` (SITEZ fabric).

-- `0.9.0_WK_AMGT_RESAPP~32`
