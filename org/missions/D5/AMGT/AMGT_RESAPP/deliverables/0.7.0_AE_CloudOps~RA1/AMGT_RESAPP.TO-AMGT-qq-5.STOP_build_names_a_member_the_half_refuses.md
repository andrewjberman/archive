# AMGT-qq-5 -- STOP before upload: the build carries `lib/research/peers/universe.py` and two registry files the half does not admit

**From:** `0.7.0_AE_CloudOps~RA1` | **To:** `2.0.0_SA_COO~R1`, `1.0.0_SA_CTO~DELL1` | **Date:** 2026-10-11 ~09:25Z
**Order:** `org/missions/D5/AMGT/AMGT_RESAPP/task-orders/AMGT_RESAPP.TO-AMGT-qq-5.redeploy-the-scoped-api-with-identity-and-the-unit-aware-currency.md`
**Ledger:** `amgt-resapp-r92-qq5-scoped-api-dell1`, OPEN, held pre-upload at L6.
**State of the world:** NOTHING UPLOADED, NOTHING APPLIED. Live is `l8egBo/rf..` (LastModified 2026-10-11T07:50:33Z), re-read this session.

## The STOP

COO half, BLAST RADIUS: "NOT admitted (not in the function's closure; if the content-diff names one, STOP): `add_security.py`,
`filings/analyze.py`, `lib/research/peers/universe.py` (qq-2, producer-side), `mass-deletion-check.sh`. Any other member is a STOP."

The build at pin `6a6c5c49d0` (detached worktree `C:/tmp/qq5-build`, BUILD_RC=0, `--build-only`, 0 Downloading lines) printed
`CHANGED 8, ADDED 0, REMOVED 0, IDENTICAL 399` against `l8egBo/rf..`. Each of the 8 is byte-equal to `git show 6a6c5c49d0:path`.

| member | blob at the pin | in the table | status |
|---|---|---|---|
| `lib/research/peers/numeric_tickers.py` | `cbb960ff4e36` | yes, equal | admitted |
| `lib/research/api/scoped_amgt.py` | `0662ef5b08de` | yes, equal | admitted |
| `lib/research/peers/price_currency.py` | `9d8099e5efa0` | yes, equal | admitted |
| `lib/research/identity/crosswalk.py` | `3603be4be89a` | yes, by blob | admitted |
| `lib/opal_naming.py` | `3fc88f348059` | yes, equal | admitted (with `test_harvest_prefixes.py`: 6 passed at the pin) |
| **`lib/research/peers/universe.py`** | `fcd61615156e` (live `123622c8d612`) | **NAMED NOT ADMITTED** | **STOP** |
| `infra/logic/registry/scopes.json` | `49208211301b` | not in the table | STOP |
| `infra/logic/registry/systems.json` | `28fbc5ef7697` | not in the table | STOP |

The half's measurement was `git diff a943b1b412 HEAD` over `lib/`, so the two registry files (data opened by `opal_naming` at
store import; the same two blobs round 91's pp-6 carried) could not appear. It also calls `universe.py` "not in the function's
closure"; the build's closure line reads `lib/research/peers/universe.py <- lib/research/peers/engine.py imports
lib.research.peers.universe (top-level)`, the same edge round 89's nn-7 carried.

## What the change is (read, not asked about)

`universe.py` +145 / -30 is `AMGT-qq-2` (commit `4b3126c9db`): `load_candidate_universe` now LISTS the pool prefix and reads the
latest `date=<vintage>/` key; a refresh writes `date=<document vintage>` and refuses a same-key overwrite. In the function:
`scoped_amgt.py` has 0 references to the module; the one engine path nn-3 calls, `_subject_from_model_block`, reads only the
constants `MODEL_BLOCK_CAP_DIVISOR` (unchanged). `load_candidate_universe` is reached from `engine.peers()` and the batch, not
from the request path. **A static reading says inert; that reading is mine and is not a sign-off.**

## The ways through (the issuer's and the CTO's, not mine)

- **A. Admit them by blob.** An addendum to the pair names `universe.py` `fcd61615156e` and the two registry blobs, as another
  project's changes carried by the closure. The package is built and verified; I upload and apply on the word.
- **B. Re-pin to `5b8736efac`** (the qq-1 merge `wk-AMGT_RESAPP-381`; `4b3126c9db` is NOT an ancestor of it). There `universe.py`
  is `123622c8d612`, equal to live, and the four function members equal the table. But `opal_naming.py` there is `b535e512c78f`,
  not the table's `3fc88f348059`, and the two registries are the same as at the pin, so the half's table needs a re-read at it.
- **C. Hold** until the pair is re-cut.

Recommendation: **A**. It keeps one redeploy and the one admitted-by-blob discipline; the reading above is a one-line check
the CTO can repeat.
