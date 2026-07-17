# V2-5 -- 01_raw bronze closeout certificate (EMITTED)

**Filed by:** 0.5.0_AE_OpalETL, 2026-07-17 ~16:2xZ. **Status: EMITTED at the CTO gate,
2026-07-17 16:34:47Z** (CTO acceptance message 20260717T163447Z; his independent count-tie:
01_raw 7,222 objects / 195,214,439,280 bytes, monolith 0824 bronze 13,233 -- both tie this
cert's denominators exactly). Consequences per the acceptance: D4 zero-reader window OPENS;
ruling-pending prefixes stay a separate CTO cell (do NOT ride this cert); D6 delete word
remains Andrew's after D4/D5.
Per the D3 plan (@ 09920d35b / fa05ca53a): the post-copy census and this certificate are the same
evidence worn two ways -- one run emitted both. Composes WP8-DECOM D3 (complete) into the V2-5 cell.

## 1. D3 COMPLETION (run 2, 2026-07-17 ~15:35-16:11Z)

- Restore-state census BEFORE re-run (per the 3b standing action): **6,328/6,328 RESTORED**
  (0 IN-FLIGHT / 0 failed) -- the 07-16 BULK/Days=21 leg delivered whole. New fact caught by the
  run-time census: GLACIER class had grown 6,328 -> **6,339** (11 objects, all `CRS20260416.*`,
  lifecycle-transitioned AFTER run 1); all 11 were already landed monolith-side, so the executor
  never needed them readable.
- Executor re-run (idempotent, never-overwrite): run-time denominators source 7,222 / target
  tree 7,122. PLAN: COPY 6,111 / SKIP-TIED 751 / SKIP-SHAPE-CLASS 360 (sum 7,222).
  **COPIED 6,111/6,111, FAILURES 0**, wall 2,147s. Converged: run 1 (854) + run 2 (6,111) +
  pre-existing ties account for every source object.

## 2. THE 13c VERIFY (five tiers, run 2026-07-17 16:1xZ, instrument + result JSON in session record)

Run-time denominators: 01_raw 7,222 / monolith 0824 bronze 13,233 / rps-mirror 338.

| tier | check | result |
|---|---|---|
| 1 KEYS | fresh ListObjectsV2 both sides; only-legacy | **0 missing** (PASS) |
| 2 SIZE | size-tie on all 7,222 | **0 mismatches** (PASS) |
| 3 CONTENT | ETag-exact 3,543; shape-class 3,679 via sampled true-MD5 (seeded sample n=10, denominator printed) | **10/10 MATCH** (PASS) |
| 4 LOGICAL | (type,date) superset: src 7,222 pairs vs monolith 7,256 | **GAP 0** (PASS) -- the 988-pair band 2024-01-12..2024-07-05 reads 0 |
| 5 RPS-MIRROR | each of 338 bronze/ objects a member of the 01_raw content set | **338/338 ETag-member, 0 no-tie** (PASS) -- derivative status proven; the S1 disposition (verify-membership, no separate copy) closes |

**Positive control (SEPARATE invocation, before targets):** known-tied pair
`CRS20230117.RLD` src_md5 == dst_md5 (adea4fe9...); **mutant leg fired**: a different object's
md5 does NOT tie (5313878e... != adea4fe9...) -- the instrument can fail, and didn't.

**13c VERDICT: PASS.** `wp8_d3_verify_13c_result.json` carries the machine-readable form.

## 3. WHAT THIS CERTIFIES (and what it does not)

- CERTIFIES: the complete 01_raw pre-SI2 delivery history (7,222 objects / 195.21 GB) exists
  byte-verified in `opal-data-assets/schwab/08242234/bronze/{type}/{date}/` under monolith
  grammar; monolith logical coverage is a strict SUPERSET of 01_raw; the bronze/ rps mirror is
  a pure derivative (no unique content). **01_raw and bronze/ carry NOTHING the monolith lacks.**
- NOT CERTIFIED / NOT IN SCOPE: the ruling-pending prefixes (02_anonymized / 03_mappings
  [P2-sensitive] / 03_silver / _archive / backfill / 01_raw_quartz_validation) -- dispositions
  remain at CTO. D4 zero-reader window, D5 read-only+IAM, D6 Andrew's final delete word: all
  still ahead. Restore expiry (temp copies) is restore-side only; the landed monolith copies
  are permanent STANDARD objects.

## 4. Provenance

Executor: `wp8_d3_copy_executor.py` (predecessor-authored, recovered intact from its session
scratchpad, output path repointed -- logic untouched). Census + verify instruments authored this
session; all three print run-time denominators. Copy = server-side CopyObject, additive-only,
zero egress; no policy/notification/TF/scheduler touched anywhere in D3.
