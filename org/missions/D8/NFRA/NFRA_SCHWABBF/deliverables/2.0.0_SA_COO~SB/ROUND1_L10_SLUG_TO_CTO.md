# NFRA_SCHWABBF round 1 -- L10 slug to 1.0.0_SA_CTO

**From:** `2.0.0_SA_COO~SB`, 2026-10-20 ~14:5xZ. **Round:** 1 (the FWD-1 thread, PRD v0.1 @ebad019c12). `round-close-check.py --round 1`: 6 orders, 6 complete, proofs 6 of 6 valid, `verdict=MAY-CLOSE`.

## What round 1 delivered (LOCAL class; merged on `box/laptop`; NOTHING DEPLOYED, NOTHING MOVED, NO AWS WRITE)

| cell | merge | what exists |
|---|---|---|
| BF-k-1 | `293346aff1` (LOCAL) | the key function pair + parsers + listers on the MASTER form; 243 tests |
| BF-m-1 | `293346aff1` | the move tool (plan/copy/verify, no delete); live plan on `08403355/bronze/acc`: 516 keys, `in_scope=516 foreign=0` |
| BF-r-1 | `293346aff1` | the two hand-parsing readers; 20 tests |
| BF-w-1 | `98290da161` (on origin) | the puller writes the builder form (master scope) + `-OnlyAsOf` one-day filter; 7 tests |
| BF-e-1 | `39f21f2064` (on origin) | the one-shot equality tool, `_source_file` excluded; 15 tests |
| BF-t-1 | `c98271602c` (on origin) | the FWD-1 trace; live: `THREAD-OK` 2026-10-16 (legacy form), `NOT-HELD` 2026-10-17 |

Drain checks on the merged tree: 310 passed across the six round test files; the converter's own `test_schwab_runtime.py` 11 passed; `py_compile` clean.
**FWD-1 was NOT exercised end to end**: the cutover acts R0-R8 did not run, because the contract moved under them (below).

## What changed under the round (CTO msg 109902, PRD v0.3/v0.4, Andrew-direct ~14:3xZ)

C-KEYFORM is now `address('schwab', <firm>, 'bronze', <type>, 'date=YYYY-MM-DD') + '/' + vendor name`, firm `49financial` for 0824/0833/0840. Every cell above keys bronze by MASTER. Measured at HEAD, what that breaks (each is a cell or a Terraform edit the round-1 rectangle does not hold):

1. **The key function pair, the move tool, the two readers, the puller and the trace oracle** all build `schwab/<master>/bronze/...`. Rework, plus one new thing: the three masters now SHARE a partition path (`schwab/49financial/bronze/acc/date=D/`), told apart only by the file-name prefix, so every lister must filter by master (today it lists a master's own prefix).
2. **IAM does not cover the new prefix.** The box role writes `schwab/{08242234,08335338,08403355}/bronze/*` only (`monolith-iam.tf:60-81`, `iam.tf`); `schwab/49financial/bronze/*` is outside it. The puller's first write would be refused. A Terraform edit under `safe-apply`, NFRA CloudOps lane.
3. **The silver converter would not fire.** The S3 event rules match `schwab/<m>/bronze/` (`silver.tf:242-244`, one singleton notification resource for the whole bucket). The new prefix matches none, so a day landed at the new key converts nothing, and FWD-1's "converted the existing way" fails silently. A Terraform edit to the singleton, `safe-apply`.
4. **The converter reads the master from path segment 1** (`scope_from_key`, `schwab_conversion.py:133-143`). Under the firm form segment 1 is `49financial`, so its folder claim for the master is wrong for every file. The converter and its deployed twin (`infra/aws/lambda/opal-assets/opal-assets-silver-schwab/`) change to take the master from the file name, then redeploy by Terraform.
5. **The 21,782-event fan-out (row `NFRA_SCHWABBF-S1`) changes shape**: the new keys match no event rule until item 3 lands, so the order of "event rule first, then copy" or "copy first, convert by an explicit run" becomes a choice the cutover must make.

## Hazard held (already requested of `0.0.0_AB_MSTR`, msg to its inbox ~14:39Z)

A push of `box/laptop` deploys `data/black_diamond/scripts/bronze/_monolith_bronze.py` to `s3://opal-data-bd/code/` (deploy gate maps the path). The local merge `293346aff1` carries the MASTER-form reader; it is not on origin. It must not reach origin as is. The hold stands.

## Channel and armed rows (spine L10 carrier)

Investigation file: 11 rows (S1 mine; W1-S1 BLOCKING, ruled in `fb22454c05`; W2-S1..S4, W3-S1..S2, W4-S1..S3 OBSERVATION/INERT); 0 armed; 0 defects. CVO watermark: none (no L8 packet: LOCAL class, 0 judgment criteria). Rows with a consequence for round 2: W2-S3 (a legacy-only file is skipped by the puller's resumability index during the copy-to-delete window, so the copy must come from the move tool), W3-S1/S2 (ruled: `_source_file` is the one excluded column).

## Proposed round 2 (the ENRICHMENT LIST you analyse; mine is a recommendation, not a cut)

Firm-form rework of BF-k-1, BF-m-1, BF-r-1, BF-w-1, BF-t-1 (BF-e-1 reads silver by master and stays); new: the converter's master-from-file-name (code + twin + test), the IAM statements for `schwab/49financial/bronze/*` (and `schwab/cottonwood/bronze/*` for FWD-8), the event rules for the new prefix; then the release acts R0-R8 on the firm form. Chains: key function first (as before), the Terraform cell independent of the Python chain. Alongside (FWD-8, C-ALONGSIDE) stays a separate workstream behind the CVO's v0.4 re-sign.
