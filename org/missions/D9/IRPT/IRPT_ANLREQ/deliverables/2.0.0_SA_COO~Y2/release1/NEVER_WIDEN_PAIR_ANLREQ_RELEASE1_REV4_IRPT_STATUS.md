# IRPT_ANLREQ release 1 REVISION 4 -- irpt-status registers the research revision -- never-widen pair DRAFT

**Deployer:** `2.0.0_SA_COO~Y2`. **Applier:** `0.7.0_AE_CloudOps~DELL2`. Its own pair, per the CTO ruling
`org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_RULING_IRPT_YCDGEN_FWD1_RETENTION_REF_SKEW_20261009.md` AMENDMENTS 2-3 (msgs 3514/3548).

**Why:** live rev 3 (`t6OJTCcm`) still refuses the Opal 49financial report `REQ-5e4149d2...` with `RetentionRefused 'invalid retention reference'`
(status-job and analysis-report).
- All 13 stored refs fit (laptop walk, msgs 3484/3502).
- The cause is the READER's composition: `reports/status_installed.py:114` built the repositories without `additional_policy_revisions`, so
  `YCHARTS_OPAL_REPORT` was never registered under its research revision.

DRAFT: no half signed.

## 1. Pin and artifact

- **Pin:** box/dell2 `287b105600` (AR-y-21 AMENDMENTS 6-7 drained). It must be on origin before the apply.
- **Built** (BUILD_ONLY at the pin, this seat): `VC/r14kaXm6FqaZOOFm3fT+8qngsyGI5Yr7U+DgYx64=`. Import-closure OK, 38 files.
- **Live now / ROLLBACK:** `t6OJTCcmOnWGVl8iglcvfGoYb3PbPJqJYqsSgJBpGdI=` (rev 3).

## 2. Gates at the pin

| gate | reading |
|---|---|
| census against LIVE | `changed_members=1`: `status_installed.py` (live `59853db310e6` -> built `326fed4f54b4`). `resident_installed.py` stays at `80a79a7462` (NOT re-pinned, CTO ruling AMENDMENT 3) |
| symbol closure on the BUILT zip | `modules=37 pairs=115 missing=0` |
| `_authz` unguarded-route census | 9 passed, 22 of 22 |
| `reports/tests/test_status_installed_revisions.py` | 6 passed: set equality with the writer's `OPAL_RESEARCH_REVISION`; the family maps to it; a negative arm without it; zero-match and two-match arms FAIL CLOSED (no extra revision plus one `ERROR:` line) |
| `reports/tests/test_status_installed.py` | 4 passed |

## 3. What moves

- **One composition argument:** the research revision, derived from the PACKAGED registry (the policy whose families hold `YCHARTS_OPAL_REPORT`). It is
  never typed, and fails closed on zero or several matches.
- **Plans:** `investor-reporting/ops -target=module.irpt_status`, the code only. No API change; `/original` stays exactly one route.
- **Widens:** irpt-status may READ artifacts of the family the writer already retains under that revision. **Does not move:** any route, IAM, any other
  family's binding, `resident_installed.py`.

## 4. After-reads

- R0: live at start == `t6OJTCcm`. Per-member diff of the uploaded zip against live: EXACTLY `status_installed.py`, otherwise STOP.
- R1: symbol closure on the uploaded zip, `missing=0`.
- R2: live == `VC/r14ka`, re-plan 0, `_authz` census 22 of 22.
- R3: `REQ-5e4149d2`'s OWNER read through irpt-status (status-job and analysis-report) answers. This is `2.0.0_SA_COO~G2`'s sr1 read window under its own
  half; the CTO ruled that ~G2 re-runs the owner read after rev 4 lands.
- R4: a cottonwood request's read is unchanged.
- **Branch B:** re-promote rev 3's S3 version.

## 5. Owed before signing

- The CTO half.
- Pin `287b105600` on origin.
