# NFRA_OPLGTW.TO-OG-r-2 -- on-host capacity and existing-workflow regression on the candidate -- RESULT

**Assignee:** 0.9.0_WK_NFRA_OPLGTW~2 | **Worktree:** C:/tmp/wk-oplgtw-2r2 (branch wk-oplgtw-2-r2) | **PRD:**
org/missions/D9/NFRA/NFRA_OPLGTW/prd/NFRA_OPLGTW_PRD.md v0.2 @f0aa50dbc0 | **Decomp:**
org/missions/D9/NFRA/NFRA_OPLGTW/decompositions/NFRA_OPLGTW_DECOMP.md v1 @8768f46770, cell OG-r-2.

## Pickup

A previous instance of this slot was killed at ~18:55Z mid-order, leaving `onhost_bench.py` (written) and
local dry-run scratch (`CAPACITY.quick2.json`/`CAPACITY.full2.json`, never cited as acceptance evidence) but
no on-host run. Before anything else this pass: checked via SSM for a leftover bench scratch directory on
the host (`ssm:ab6a8e71-352a-46d1-b748-83faf6b82b51`: `ls -1d /tmp/ogr2-bench-*` -> `NONE_FOUND`) -- none
existed, nothing to remove. `probes/og_r2.py` did not exist and was written this pass.

## What was done

1. Fixed a path-depth bug in `onhost_bench.py`: `_HERE.parents[2]` raised `IndexError` when the file was
   copied directly to `/tmp/onhost_bench.py` on the host (too shallow); relocated to `/tmp/ogr2bench/onhost_bench.py`
   on the host side (no code change needed -- the bug was in HOW the file was placed, not the file itself).
2. Uploaded the harness to S3 (`s3://opal-313476888478-lambda-artifacts/ec2/opal-gateway/bench/onhost_bench-ogr2.py`)
   and pulled it onto `i-07dccb1615503ac99` via SSM (`aws s3 cp`) -- never SSH/SCP, matching the project's
   S3->SSM code-delivery discipline; confirmed the host venv (`/opt/opal-gateway/.venv`, python3.11.15,
   pyarrow 18.1.0, duckdb 1.2.2) imports `app.integrations.schwab.engine` cleanly as `ec2-user` before running
   anything at scale.
3. Ran `--scale quick` on the host first (smoke: RC=0, 4999-byte CAPACITY.quick.json) with the live service
   confirmed `active` and memory available (1415 MB) both before and after, then ran `--scale full` (the
   graded run): RC=0, 17.5s wall, `/tmp/CAPACITY.full.json` (6292 bytes), service still `active`, memory
   stable (1388 MB available after). Fetched the full JSON verbatim via a second SSM command
   (`ssm:e04355a6-d612-4b6e-a8b7-52a0daf90404`).
4. Read the ALB `idle_timeout.timeout_seconds` (60) and its ARN directly via `.tools/aws elbv2
   describe-load-balancer-attributes`, immediately before assembling the record.
5. Measured the existing-workflow before/after: re-ran OG-p-1's own `OGP1-AC11` instrument
   (`cloudwatch get-metric-statistics AWS/ApplicationELB TargetResponseTime`, `SampleCount`+`p95`) over the
   identical 14-day before-window (`2026-09-02T19:15:00Z..2026-09-16T19:15:00Z`) to confirm it still reads
   the recorded `sample_count=43745.0 p95=0.5535024102704742s`, then over a 14-day trailing after-window
   ending now (`sample_count=38903.0 p95=0.5516718987799433s` -- a slight improvement, well inside the 20%
   cap) and a narrow post-resize-only window (since OG-i-4's relaunch at `2026-09-18T14:53:48Z`:
   `sample_count=119.0 p95=0.4687358309578063s`). Also measured `HTTPCode_Target_5XX_Count` over all three
   windows (19 / 18 / 2 respectively) -- see the surprise row below.
6. Assembled `CAPACITY.json` (host run + AWS reads, every source command cited in its own
   `assembled_from` block), wrote `probes/og_r2.py`, ran every criterion's exact invocation, ran three
   mutant controls and a determinism control against the probe, then wrote this proof.

## Criteria

| id | verdict | denominator |
|---|---|---|
| OGR2-AC1 | PASS | 1 on-host run, 5 checks (ran_against_host_install/platform/bearer_token_minted/schwab_tool_enabled/app_server_imported) |
| OGR2-AC2 | PASS | 3 of 3 jobs cap-respected (1 maximal + 2 concurrent) |
| OGR2-AC3 | PASS | 3 of 3 jobs deadline-respected |
| OGR2-AC4 | **FAIL** | 1 export job at contract scale (250,000 rows/50 MiB) -- LIMIT_EXCEEDED, peak_child_rss_bytes=270581760 vs cap 268435456; temp cleanup itself worked (no leaks) |
| OGR2-AC5 | PASS | 1 peak-RSS read + 1 admission-reserve computation, recorded |
| OGR2-AC6 | **FAIL** | p95 regression PASSES its cap (fraction=-0.0033, an improvement); "zero failures" FAILS literally (18/38903 and 2/119 non-zero HTTPCode_Target_5XX_Count in both after-windows; the before-window already carried 19) |
| OGR2-AC7 | PASS | 1 ALB attribute read: idle_timeout=60s > 30s prep deadline |
| OGR2-AC8 | PASS | 1 capacity verdict recorded: INSUFFICIENT, with `for_prd_revision_if_insufficient` measurements |
| OGR2-J1 | RECORDED (judgment, no verdict) | benchmark workload representativeness -- for CVO at L9 |

**2 of 8 mechanical criteria FAIL, both real, measured, and disclosed** (not probe defects):

- **OGR2-AC4** fails on the same underlying fact `OGR2-AC8` records as the project's designed
  measured-evidence-for-a-PRD-revision outcome: the t4g.small host's export child process exceeds the
  256 MiB job-memory cap before it can render a 250,000-row/50 MiB CSV (it hits LIMIT_EXCEEDED at ~1.4s,
  peak RSS 270,581,760 bytes). The largest export this host completed cleanly at contract-realistic field
  widths was 62,500 rows / 9.47 MB at 214,065,152 bytes peak -- recorded for the PRD revision AC8 already
  calls for.
- **OGR2-AC6** fails on its literal "zero failures" clause only: the p95-regression half is comfortably
  met (an improvement, not a regression), but every window this cell can construct on the live ALB target
  group carries a non-zero `HTTPCode_Target_5XX_Count` -- including the BEFORE window itself (19 over the
  same 14 days, predating every change this project has made). Filed as surprise row `NFRA_OPLGTW-W2-S10`
  rather than silently substituting a regression-only reading for the written bar; graded FAIL on the text
  as written.

Per this order's bound ("Flip `complete` only when every MECHANICAL criterion PASSES by output"), `<status>`
is **not** flipped to `complete` -- two mechanical criteria genuinely FAIL.

## Controls

- **Mutant:** three mutants against the real `CAPACITY.json` (read via a test-only `OGR2_CAPACITY_PATH`
  env override the graded invocation never sets): (A) AC4's export forced to succeed -> FAIL became PASS;
  (B) AC6's after-window 5xx counts forced to 0 -> FAIL became PASS; (C) AC7's `idle_timeout_seconds`
  forced below the 30s deadline on an otherwise-PASSING criterion -> PASS became FAIL. All three fired
  exactly as expected; the unmutated baseline re-run alongside them still read FAIL/FAIL/PASS.
- **Determinism:** two consecutive full runs of `og_r2.py AC1..AC8` diffed byte-identical.

## Surprise rows filed this order

- **`NFRA_OPLGTW-W2-S10`**: OGR2-AC6's literal "zero failures" bar is measured unsatisfiable in every
  window this cell can construct (14-day trailing after: 18/38903; narrow post-resize-only: 2/119), because
  the BEFORE window (OG-p-1's own OGP1-AC11 window, predating this project entirely) already carries 19 --
  an ambient background rate this cell did not cause and cannot make literally zero. ARMED for the issuing
  COO/CVO: disarm either by ruling AC6's clause means "no failure-rate increase vs. the declared before"
  (which the printed evidence would then satisfy) or by accepting the FAIL as the correct, honest reading.

## Validation

`py -3.12 .tools/proof-of-spec-check.py
org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~2/NFRA_OPLGTW.TO-OG-r-2.onhost-capacity.proof_of_spec.json
OGR2-AC1,OGR2-AC2,OGR2-AC3,OGR2-AC4,OGR2-AC5,OGR2-AC6,OGR2-AC7,OGR2-AC8,OGR2-J1` -> `VALID (rc=0)`. A valid
instance with 2 disclosed mechanical FAILs is not a met order; `<status>` stays as issued.
