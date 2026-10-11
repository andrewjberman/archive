# NEVER-WIDEN -- COO half -- ADVI_COTBKF round 50, CB-ax-2: redeploy cot B_00, the writer and the files beside them

**Signer:** `2.0.0_SA_COO~C2` (dell2) | **State: GIVEN 2026-10-09 ~17:0xZ**

**Act:** `0.7.0_AE_CloudOps~CB2` writes the keys below in `s3://opal-data-cot/code/gold/`. The rulings behind it are CTO ADDENDA 18,
21, 22, 22.1 and 23 (rows D2-S71, D2-S72). The code is round 50's CB-ax-1, drained @b874540474 (gold suite 50 passed in the
issuer's run).

## 1. Write set -- the UNION of every tool's printed list (ADDENDUM 18), in write order

| # | key | prior | new bytes (repo blob) | new sha256 | how |
|---|---|---|---|---|---|
| 1 | `code/gold/ticker_overrides.py` | none: MINTS (404) | `data/cot/scripts/gold/lib/ticker_overrides.py` @ blob `bcb98391...` | `4d407c3acf2c3fd4106050af98010541646571b88148115549b0997ccc817015` | one put-object of the exact blob bytes |
| 2 | `code/gold/legacy_addresses.json` | none: MINTS (404) | `infra/logic/registry/legacy_addresses.json` @ blob `04b8e2ee...` | `34dfcb376088328686d1c9a3fabae279e1316373f8470a969b5d513d7eedfe17` | one put-object of the exact blob bytes |
| 3 | `code/gold/build_canonical_prices_v2.py` | VersionId `GAOI7tORcF7V7F0fW9NMH35bonjXEwzj` | repo HEAD @ blob `5abaded2...` | `8b733bb10eee6fb96396b73e61e09453b38d5ed087abdac425c074554520a76b` | `.tools/safe-deploy.sh` |
| 4 | `code/gold/B_00.canonical_holdings.py` | VersionId `hU7ZrZTD5NDlVvuSo9aBMUd1hKUg_lAe` | repo HEAD @ blob `189d37d5...` | `2b38b1425d31091e5625affcb4e0787e2f15afef5ac3624b3a2ab5edb78a36ec` | `.tools/safe-deploy.sh` |

- `code/gold/scopes.json` is **NOT written**. Its served sha256 (`13947f7f...`) equals the repo blob `261c0cf8...` read at ~17:0xZ.
- The prior VersionIds were re-read at ~17:0xZ, and the applier re-reads each key immediately before its write. A moved version, or
  a minted key that now exists, means STOP.
- **Diff census (issuer, served versus repo, ~17:0xZ):**
  - B_00: 26 changed lines, in two hunks only. The first adds the beside-module `scopes.json` own-firm reader at :96-116. The second
    replaces the `opal_naming` lookup inside `_ff_worker` at :1362-1365.
  - The writer: 182 changed lines (the round 46, 48 and 50 changes: input resolution, `source_firm` metadata, keys from the pinned
    registry, fail-closed overrides).
  - Any changed line outside the two scripts' named changes means STOP.

## 2. Rollback

- **Scripts (3, 4):** `copy-object` of the prior VersionIds above.
- **Minted files (1, 2):** they are NEVER deleted by the seat; deletes are Andrew's act. The scripts restored to their priors do not
  read them, because the prior writer imported `lib.ticker_overrides` and built keys through `opal_naming`.
- `scopes.json` is unchanged.

## 3. Writers and readers

- **Writers of `code/gold/`:** `safe-deploy.sh` and this act's two put-objects. There is no scheduled writer.
- **Readers:** the cot gold run's code sync (`gold_dispatch.sh`:497-498).
  - **The writer** runs only on a MANUAL silver-prep (scheduled writers: 0).
  - **B_00** runs in the gold run. Its changed lines are the own-firm reader and `_ff_worker`, which runs only when
    `schwab/silver/rps/` holds data. That prefix read 0 keys against a positive control (round 42). So **B_00's scheduled output is
    unchanged by this deploy**; the module-level reader runs, reads the deployed `scopes.json`, and returns.
  - **Both branches:** the own firm resolves (normal), or `scopes.json` is unreadable and the run STOPS before any write, by design.
    The deployed `scopes.json` is present (VersionId `7ChC4J0G...`), so the stop branch does not fire.

## 4. Proof on the SERVED files (CB-ax-2's order and its amendments)

- Fetch keys 1-4 and confirm each sha256.
- In a detached scratch worktree with NO `lib/opal_naming` on the path, run `data/cot/scripts/gold/tests/test_cot_gold_failclosed.py`
  against the fetched bytes:
  - a synthetic rps day with no ImportError;
  - the scopes-absent, overrides-absent and legacy-addresses-absent STOPs, each with 0 rows;
  - 757 overrides and 104 corrections loaded;
  - the written-key census equal to the pre-change writer's.
- The **import-closure read** (ADDENDUM 23):
  - B_00 imports `lib.config` (:56), `lib.s3_layout` (:57) and `lib.exclusions` (:1131), plus stdlib and installed packages. All
    three, with `lib/__init__.py`, are in the mirror's `code/gold/lib/` listing read by the issuer at ~17:2xZ (16 keys).
  - The writer imports only stdlib and installed packages (`boto3`, `numpy`, `pandas`, `pyarrow`). It loads `ticker_overrides.py`
    from beside itself through `importlib.util`, which is key 1.
  - `missing=0` is required, or STOP.
