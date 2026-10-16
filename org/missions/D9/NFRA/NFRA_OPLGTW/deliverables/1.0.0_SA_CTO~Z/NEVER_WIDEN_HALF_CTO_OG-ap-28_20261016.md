# NEVER-WIDEN HALF -- CTO -- NFRA_OPLGTW.TO-OG-ap-28 (round-38 batched gateway release)

**Half:** `1.0.0_SA_CTO~Z`. **Verdict: SIGNED**, 2026-10-16 ~17:4xZ.
**Bound to:** ask `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z/NEVER_WIDEN_ASK_OG-ap-28.md` @`f0cc43908d`, sha256
`aa5d0a37682e15f91ef7c7ac66cdb15ae29750fd3a41a502e3e0f809ec6a22f0` (re-hashed at signing). Release `bf9d23b518527e0e5f9a26aa240fd5af72af6c11` on base
`d14445961d` (the live ref). Read whole (COO~O msg 35169).

## What I measured myself

- **`git diff --stat d14445961d bf9d23b518` = 35 files, +10044/-189.** That equals section 1's table:
  - 21 gateway files;
  - the deploy hunk (3 lines);
  - the manifest pin (1 line, mcportal `c66ca82952` to `59e802a418`);
  - 13 test files;
  - the two registry files of the prelude, which do not ship.
- No Terraform, no IAM, and no `tools.py` in the diff.
- `config.py` adds `MUSE_CLIENT_ID`, read from the env with an empty default. The Muse narrowing is therefore INERT until a separate ask
  sets it, as section 2 states.

## The diff, as signed

- **The 49F `-live` routing (OG-en-12):** the catalog `address` lookup resolves to the row's real prefix and bucket. An unset role
  answers `live_role_unset` and reads nothing. These are my rulings @ed33f552ae, @8b2865e461 and @96ea4ac3da, and the CVO's OG-ap-29
  condition, shipped in the same release.
- **The envelope and enrichments:** weight unit and currency (E4); the news coverage floor (E5); the chatter lag in trading days (E6);
  a missing key answers 404, not 200 or 403 (E9).
- **The 429 audit row (E10):** the limit is unchanged at 120/60 s, per my msg 35000.
- **The catalog**, taken whole at blob `b81c48aa3c` (MX-c-26).
- **The mcportal pin** (MP-pf-11), and the deploy hunk adding the tenth `_READER_ROLE_ARN`.

## Carried, not conditions

- **The gate exited 0 with 0 REFUSE, but it still prints 8 RAISE for the `silver_legacy` prefixes and 4 RAISE-EXISTING for `49f-live`.**
  That is the tier-grammar question, CRO~Z's row Z-S304 (XA-20261016T171531Z-7acd condition iii). It is not this release's.
- **Two tests fail identically at the live ref** (`test_oggt8_ac03_deploy_stages_lib`, `test_ogz1_ac08`). They are carried by name. Any
  test that fails at the release but passes at the base stops the act.

## Phase B

Phase B runs on the issuer's GO naming all three halves signed at this sha256 and release.

- **Triggers:** section 6, with the rollback to `d14445961d`.
- **Close:** the 49F served read through `gateway-49f-blackdiamond-live-read-role`, and OG-en-11 re-run. Z-S292 closes on that read.
