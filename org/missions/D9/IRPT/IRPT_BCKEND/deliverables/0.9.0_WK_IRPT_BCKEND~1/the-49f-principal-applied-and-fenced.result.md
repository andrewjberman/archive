# IB-rtc-7 -- THE 49 FINANCIAL PRINCIPAL APPLIED UNDER SIGN-OFF, PROVEN FENCED, AND THE THIRD DIRECTORY BUILT: result

**TO:** `IRPT_BCKEND.TO-IB-rtc-7` | **serial:** `0.9.0_WK_IRPT_BCKEND~1` |
**branch:** `wk-irpt_bckend-3-1b` | **worktree:** `/c/tmp/wk-irpt-3-1b` | **base:** `34029b1ba3`
**Invocation:** `timeout 1800 py -3.12 org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~1/battery_ib_rtc_7.py`
**Result:** `rc=0`, **5 of 5 graded arms PASS**, `IBR37-PRINCIPAL-FENCED-AND-THREE-OF-THREE-DIRECTORIES`.
**R37-AC1 = PASS-by-output.** R37-AC2 recorded below for `3.0.0_SA_CVO`.

---

## The short version

Both never-widen halves (`437789944a` COO, `3a976e1e1d` CTO) were re-read at HEAD and re-hashed
against the packet blob `bb92a81c697c6d3fb8b01cb65fedfb9cb0563e38` -- match. The directory root's
Lambda artifact was rebuilt (K5's `refresh.py` hand-off edit, already at HEAD, plus IB-rtc-3's
dispatch-date fix, already at HEAD) via `rt6_package.py`'s `SHARED_ROOTS` resolution (the same
mechanism IB-rtc-3 used, since `build-and-upload.sh`'s generic packer cannot resolve
`trading_calendar.py` from `lib/` and `errors.py` from `_authz/`), uploaded, verified by
`head-object` size+`content-sha256`, and registered in `lambda-source-map.json`. The directory
root applied `2 to add, 1 to change, 0 to destroy` -- exactly K1 (role), K2 (inline policy) and K4
+artifact (Lambda env + rebuilt code) -- and re-plans 0-diff. The `mdpf-pipeline` root applied
TARGETED, `-target=aws_iam_role_policy.mdpf_runner`, `0 to add, 1 to change, 0 to destroy` -- K3
only, exactly the CTO half's mechanical condition (1). `mdpf-runner-scoped` moved 32 -> 33
statements.

The negative control (SSM, host by host, read-only, assumed role) ran twice manually and once more
inside the battery: three probes on **another firm's prefix and the 49 Financial destination** all
`AccessDenied` (Inflection's `silver/api_dims/representatives/`, Cottonwood's
`blackdiamond/cottonwood/silver/fact_allocations/` in the shared `opal-data-assets` bucket, and a
write to `opal-data-bd/investor-reporting/directory/...`), and the positive control (a read of
`opal-data-49financial/gold/advi/dimensions/dim_relationship/`) `READ-OK`. The assumed role's ARN
matches `0 of 4` of the four old Deny-prefix patterns.

The deployed dispatch was fired for real with the schedule's own payload (read live from
`schedule.tf`, no `business_date` override) and reconciled: **for the first time in this
project's history, all three firms landed a `directory.json` in the SAME fire** --
`49financial` **4562 entries**, `cottonwood` **259 entries**, `inflection` **291 entries** --
each at revision `.../1.0` (a first mint). 49 Financial's build read its five dimension tables
through the assumed source principal (`session irpt-directory-source-read`) and the BD cross-
reference on the host session, exactly as K5 describes.

The writer census of the 49 Financial directory prefix, re-run with IB-rtc-6's own instrument
(`writer_census_ib_rtc_6.py`), reads **12 writers, same membership**, against a denominator of
**263** (262 + the new role itself, which the census confirms is not a writer -- `implicitDeny`).
Neither of the CTO half's mechanical stop conditions fired.

---

## The five arms

### (a) HALVES -- PASS
Packet blob hash re-derived by `git hash-object`: `bb92a81c697c6d3fb8b01cb65fedfb9cb0563e38`,
equal to both halves' cited hash. Each half names all five keys (K1-K5). 2 of 2 halves present.

### (b) APPLIED -- PASS
Fresh `terraform plan` on both roots, immediately re-run by the battery (not the apply-time plan):
directory root `(0, 0, 0)`, mdpf-pipeline targeted `(0, 0, 0)` -- both 0-diff, proving the live
state is exactly what was signed. `get-role`/`get-role-policy` read fresh via boto3: K1 role
`arn:aws:iam::313476888478:role/irpt-49f-directory-read-role`, trust document sha256
`7ce5283bfd18ee5770df3de4d8fd4639ae611abf9b775abb21c86eb35b0b23c3`; K2 inline policy sha256
`ab11263f5730a1a4b8b0b12c9cff209adbfeb290e501a853c71fe12648287c29`, 2 statements. `mdpf-runner-
scoped` (K3's target): 33 statements (was 32), sha256
`aa94eeb6d0f89977958f66d14c6541fd32be91393e5183ec1aaee9cf45181f4a`, and the new
`IrptDirectory49fAssumeSourcePrincipal` statement is present, resourced to K1's ARN.

### (c) NEG-CONTROL -- PASS
A fresh SSM command each run (final graded run: `8df73c4a-15a5-4953-a414-09e52fba4b02`,
`i-02448edb624a7a7cf`, `Status=Success`). N1 (Inflection), N2 (Cottonwood, shared
`opal-data-assets` bucket) and N3 (49 Financial destination write) all `AccessDenied`, `3 of 3`.
P1 (the five 49 Financial dimension prefixes) `READ-OK`, `1 of 1`. Name-check: the assumed ARN
matches `0 of 4` of `role/cot-*`, `role/inf-*`, `role/mdpf-*`, `role/opal-assets-mdpf-*`.

### (d) THIRD-DIR -- PASS
The schedule's own payload is read LIVE from `schedule.tf`'s `irpt_directory_refresh` resource
block (bounded so it cannot pick up the sibling `irpt_holdings_snapshot` schedule's payload --
an early version of this battery had exactly that bug, caught before it was committed: see
Rows filed). Bundle in use: current `VersionId` `0XLkiPt4wljdniLnF2fkPKN4qAIkjUbc`, matching
IB-rtc-9's mint. The Lambda was invoked; all three firms returned `state=READY` on the FIRST
invoke this run (the business dates -- 2026-09-16 for 49f/cot, 2026-09-17 for inf -- were already
the reconciled frontier from the manual pre-battery fire; the dispatcher's own `same_frontier`
path made the second invoke a no-op, which is the READY state itself, not a re-dispatch). Each
firm's landed `directory.json` was re-fetched fresh (never read from an earlier run's cache) and
hashed:

| firm | bucket | key | ETag | sha256 | size |
|---|---|---|---|---|---|
| 49financial | opal-data-bd | investor-reporting/directory/2026-09-16/directory.json | `fcdf90de75f24a591c1073489ad1b21f` | `fd0beeca5fb4f785e2db9afeab0bc41e99e1d696368bec5bb8eb9f66e986c6f2` | 6445354 |
| cottonwood | opal-data-cot | investor-reporting/directory/2026-09-16/directory.json | `264e0fbedc24c09bd066ee9eb278ea5f` | `af0b61da8ddc43a5eb89f0d58b67e9c7fb2488f018fccb6aed2b55a8882b658e` | 416638 |
| inflection | opal-data-inf | investor-reporting/directory/2026-09-17/directory.json | `782324f961078b228a32af9316af9836` | `09e349d2886bdc5bfeb79069cf747e616c6bfbf9fe7bb03506b83b4aae9e57c7` | 447976 |

`3 of 3` directories present. 49 Financial `state=READY`, `1 of 1` landed.

**The first real fire (manual, pre-battery, 2026-09-18T09:01:14Z, dispatch SSM ids
`6a856ec7-c0a1-4d1a-b49d-b87bda4ac9d4` (49financial), `c25a3bdb-7d18-41f0-b521-cf9d513ea6a2`
(cottonwood), `e0f6a54c-d43c-4276-a3e4-41923573d79d` (inflection)):** all three `rc=0`. 49
Financial's stdout: `OK: firm=49financial bucket=opal-data-bd entries=4562 valid=4562 of 4562
as_of=2026-09-16 ... key=s3://opal-data-bd/investor-reporting/directory/2026-09-16/directory.json
uploaded=True`, with the note `dimension reads through the assumed source principal (session
irpt-directory-source-read); the xref on the host session` -- K1-K5 working end to end, for the
first time. The reconciliation fire (2026-09-18T09:06:14Z) read all three back to
`REFRESH_COMPLETED_WITH_ADDITIONS` / `state=READY` / `action=NONE`, revision `pending -> .../1.0`.

### (e) CENSUS -- PASS
`writer_census_ib_rtc_6.py`'s own `census()` re-run live: `verdict=EVALUATED`, **12 writers of
263 principals** (262 + the new role, confirmed `implicitDeny` and not counted), membership
identical to IB-rtc-6's baseline (`bd-allocation-processor-role`, `bd-daily-trigger-lambda-role`,
`bd-exporter-ec2-role`, `bd-gold-detail-generator-role`, `bd-gold-layer-lambda-role`,
`bd-merge-daily-lambda-role`, `bd-pipeline-task-role`, `bd-processor-lambda-role`,
`mdpf-daily-runner-ec2-role`, `Andrew_Berman`, `Andrew_Berman_Console`, `Opal_Terminal`). Neither
CTO mechanical stop condition (13 writers, or 12 with different membership) fired.

---

## Ledger

`irpt-bckend-rtc7-49f-principal` -- OPENED `d8720e83df` with 4 legs (L1 directory-root
role/policy, L2 mdpf-pipeline targeted, the Lambda leg, L3 verify), CLOSED `1bd528592b` with all
4 legs proven. Every commit and the sentinel removal happened before the grading reads.

## What this cell did NOT do, and why

- **Did not touch `directory_runner.py` or `holdings_snapshot.py`.** Both fixes (the business-date
  walk, the jsonschema tolerance) and the bundle mint were already merged at HEAD by IB-rtc-3
  (amendment 2) and IB-rtc-9; this cell's job was the sign-off-gated apply and the fence proof.
- **Did not apply the `mdpf-pipeline` root untargeted.** `aws_s3_object.mdpf_route_bindings` (row
  `IRPT_BCKEND-S68`) remains someone else's unapplied, CRLF-divergent change, exactly as the CTO
  half accepted and left owned at `1.0.0_SA_CTO`.
- **Did not move the 49 Financial destination out of legacy `opal-data-bd`.** That is D14's, and
  R36-AC2/R37-AC2 record the facts for `3.0.0_SA_CVO`, not a decision this cell makes.
- **Did not re-mint the `investor_reporting` bundle.** That was IB-rtc-8/IB-rtc-9's act; this cell
  only confirmed (arm d) that the bundle the host actually ran was still that exact mint.

## Rows filed

**None.** Every premise the face names held: both halves present with matching keys and hash, both
plans matched the packet exactly, the negative control fenced as designed, the third directory
landed, and the writer census stayed unchanged. (A bug in this cell's OWN first battery draft --
reading the wrong Terraform `target` block for the schedule payload -- was caught and fixed before
any commit, by this battery's own second run disagreeing with its first; it never reached a
committed artifact or a wrong ACT, so it is not a task-order premise failure and is not filed as a
surprise row. It is recorded here, in this result, as the discipline that caught it.)

---

## R37-AC2 -- the facts, for `3.0.0_SA_CVO` (no verdict)

1. **Is the fence proven in (c) the fence R-44 asked for?** The negative control denies a read of
   ANOTHER FIRM's prefix specifically (Inflection's own silver prefix in `opal-data-inf`;
   Cottonwood's own silver prefix inside the SHARED `opal-data-assets` bucket, at Cottonwood's own
   `blackdiamond/cottonwood/` path) -- not merely an unrelated bucket. It also denies a write to
   the 49 Financial DESTINATION itself (`opal-data-bd/investor-reporting/directory/...`), which the
   role was never granted (K2 is read-only). The positive control on the role's own five granted
   prefixes succeeds. The assumed role's ARN carries none of the four historical Deny-prefix
   patterns. This is the shape R-44 names: a firm-scoped read grant that cannot reach another
   firm's data and cannot write anywhere.
2. **Are the three directories comparable artifacts?** All three are produced by the SAME
   `directory_runner.py` code path (`DirectoryEntry` schema, `Draft7Validator` fallback per
   IB-rtc-9), so SAME SCHEMA. They are NOT the same business date: 49financial and cottonwood
   landed at `2026-09-16`, inflection at `2026-09-17` -- each is that firm's own newest
   COMPLETE source date (the trading-day walk IB-rtc-3 amendment 2 built), which is by design,
   not a defect; the three firms' upstream source completion cadences differ. All three are at
   revision `1.0` (a first mint for each, in the SAME shape `irpt-dir/<firm>/<date>/1.0`) -- SAME
   REVISION SHAPE.
3. **What FWD-1/FWD-7 still lack after this:** (a) the SCHEDULED fire on a real business day --
   this cell fired the dispatch manually with the schedule's exact payload; the standing
   `cron(0 9 ? * MON-FRI *)` schedule is unchanged and ENABLED, and its next organic fire (today
   13:00Z, since this cell ran before it) will exercise the same code path, but that is a WAIT
   this cell does not observe as an ACT; (b) D14's destination move -- 49 Financial's directory
   still lands in the LEGACY `opal-data-bd` bucket (K2/K5 deliberately did not touch this), and
   whether FWD-7's DONE WHEN requires the firm's own bucket is a decision this packet places and
   does not make (packet section "What this packet does not decide").
