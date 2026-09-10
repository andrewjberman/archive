# IB-s-11 RESULT -- the performance adapters, the normalizer, and the re-grounding of a stopped instance

TO: `IRPT_BCKEND.TO-IB-s-11` (`org/missions/D9/IRPT/IRPT_BCKEND/task-orders/IRPT_BCKEND.TO-IB-s-11.performance-adapters-black-diamond-orion-normalizer.md`)
Worker: `0.9.0_WK_IRPT_BCKEND~4` | Branch: `wk-irpt_bckend-1-4` | Worktree: `/c/tmp/wk-irpt-1-4`
Cell: `IB-s-11` (PRD row B11, FWD-3 contrib) | Fabric: laptop | Date: 2026-09-10

## 0. THIS INSTANCE IS A RESPAWN, AND WHICH COMMITS PREDATE IT

A previous instance of slot ~4 ran this order under a mis-configured worker definition and was
STOPPED by the issuer after it had committed twice on this branch. Those two commits are
WORLD-DONE and are read, never re-executed (NEVER-2):

- `de87f0976d` -- the adapter package, the Terraform root, the fixtures, the tests, the
  source-map entry and the ledger sentinel. **PREDATES THIS INSTANCE.**
- `b146774670` -- the `irpt-bckend-s11` deploy ledger closed, four legs proven, the sentinel
  removed by the close. **PREDATES THIS INSTANCE.**

What the stop left UNCOMMITTED in the worktree: the `PATH_MANIFEST.json` registration of this
cell (29 entries), four surprise rows `IRPT_BCKEND-W4-S1..S4`, and `battery_ib_s_11.py`. There was
no `.result.md`, no proof-of-spec instance and no `complete` flip. **This instance re-grounded
every committed claim by output before adding anything, then finished the order.**

### What the re-grounding measured, and with which instrument

| claim the stopped instance made | instrument this instance ran | result |
|---|---|---|
| the battery passes | `timeout 600 python .../battery_ib_s_11.py` | rc=0, `7 of 7 mechanical arms passed`, token `IBS11-PERFORMANCE-NORMALIZED` |
| 28 offline unit tests pass | `python -m pytest infra/aws/lambda/investor-reporting/performance/tests -q` | `28 passed in 0.41s` |
| the Lambda serves the built bytes | `aws lambda get-function-configuration --function-name irpt-performance-adapter` run DIRECTLY, not through the battery | `CodeSha256 = Tl+NwcWAWl46YWeCrHShPpjoX5RgGUWm2UVQPLRJdFM=`, `State=Active`, `Runtime=python3.12`, `Handler=handler.lambda_handler`, `LastModified 2026-09-10T23:10:33.497+0000` -- equal to the built zip sha256 the ledger records |
| the root is converged | `timeout 120 .tools/terraform.exe -chdir=... plan -no-color -input=false -lock=false` | rc=0, `No changes. Your infrastructure matches the configuration.` |
| the ledger is closed and the sentinel gone | read `org/critical_paths/change_management/20260910T2304Z_irpt-bckend-s11_deploy_completion.md`; `ls org/critical_paths/.open_deploys/` | `Status: CLOSED -- nothing stranded -- closed 20260910T231202Z`; all four legs `CLOSED`; `irpt-bckend-s11.json` absent from 6 open sentinels; `git log --full-history` on the sentinel shows it added at `de87f0976d` and removed at `b146774670` |
| the manifest covers the cell | parsed `PATH_MANIFEST.json` for `registered_by` starting `IB-s-11` | 29 entries of 103 total; the 17 repo paths match `git ls-files` under the two new directories EXACTLY, 17 of 17 |

**One defect was found and fixed by this instance:** `battery_ib_s_11.py` did not pass
`.tools/commit-gate.sh` -- ruff `F401 'math' imported but unused`, `BLOCKED: ruff check failed`.
The unused import was removed, the gate re-run clean (`OK: pre-commit gate clean for 1 of 1
file(s)`), and the battery re-run byte-identical to its pre-fix output. Had the stopped instance
committed the battery, the commit would have been refused.

## 1. WHAT IS BUILT

`infra/aws/lambda/investor-reporting/performance/` -- `units.py` (Quantity = value + unit +
source path; the only path that changes a unit RECORDS the conversion, and `unit_blind_link()`
exists so the difference control can fail), `tenants.py` (three firms, three routes),
`transport.py` (`RecordedTransport` over the scrubbed capture; `LiveTransport` refuses to
construct without the per-use word in TWO independent halves and imports `requests` only inside
the call), `bd_adapter.py`, `orion_adapter.py`, `normalize.py` (the four named refusals, the
identity triple, absence-with-reason, the `PerformanceReport` assembly and contract validation),
`handler.py`, `fixtures/` (5 scrubbed bodies + `FIXTURE_MANIFEST.json`), `tests/` (28 offline
tests). `infra/aws/terraform/investor-reporting/performance/` -- `main.tf`, `iam.tf`, `lambda.tf`,
applied, 4 added / 0 changed / 0 destroyed.

## 2. ACCEPTANCE

### S11-AC1 -- PASS by output (7 of 7 arms)

`timeout 600 python org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~4/battery_ib_s_11.py`
-> rc=0, final line `IBS11-PERFORMANCE-NORMALIZED`. Full transcript committed as
`IB-s-11_S11-AC1_battery_output.txt`. Deciding numbers, each beside its denominator:

- **(a)** 3 of 3 firm pairs separated. F-49F and F-COT share `bd3.bdreporting.com` and are still
  DIFFERENT routes: different session secret (`blackdiamond/49f/session` vs
  `blackdiamond/cot/session`) and different data plane (`opal-data-assets/blackdiamond/49f/` vs
  `opal-data-cot/forwardfill_v2/`). F-INF -> `api.cloud.orionadvisor.com`. An unknown firm is
  refused, never defaulted.
- **(b)** 9 of 9 receipts accounted; 3 of 3 reports validate against the contract; the two 401s
  produce ABSENT-with-reason (`vendor returned HTTP 401 with a 0-byte body`) and no value.
- **(c)** max `|daily percent/100 - (factor-1)| = 0.0` across 92 points x 3 groups; linked
  factors minus vendor summary = `1.2085818457130415e-13` / `1.064634491676486e-13` /
  `3.236334811251851e-13`; the UNIT-BLIND control link reads `-0.999998816706432` against the
  true `0.018564905412121`, i.e. the 100x failure the arm requires.
- **(d)** vendor household calculation `0.018564905412` is carried; SUM of the 2 account returns
  is `0.037130402931` and the MEAN is `0.018565201466` -- wrong by `+2.961e-07`, close enough to
  survive review, which is why it is REFUSED rather than tolerated.
- **(e)** hierarchy `levels` chosen, `combinedLevels` recorded present-and-not-summed; 11 Segment
  TWRs sum to `0.148930573` against an account TWR of `0.016410648` (9.1x); id `Period` collides
  6 ways and the group-path + `$type` + id triple separates 6 of 6; `startValue + valueChange`
  refused -- 6 of 9 cells match, 3 do not, max `$210.68`.
- **(f)** 7 absence rows across 2 providers, 5 of 5 required Orion facts carried as absences,
  UNSUPPORTED 6 / PARTIAL 1; `fee_basis=UNKNOWN accrual_basis=UNKNOWN annualization=UNKNOWN`.
- **(g)** 0 of 0 vendor connections during arms (a)-(f) (denominator: `bd3.bdreporting.com`,
  `api.cloud.orionadvisor.com`); the POSITIVE CONTROL moved the counter 0 -> 1, so the zero is
  MEASURED and not a dead guard; `CodeSha256` equals the built zip; the ledger reads CLOSED.

### S11-AC2 -- PASS by output

`timeout 120 .tools/terraform.exe -chdir=infra/aws/terraform/investor-reporting/performance plan -no-color -input=false -lock=false`
-> rc=0, `No changes. Your infrastructure matches the configuration.` Run AFTER the apply and
AFTER the ledger closed. Transcript committed as `IB-s-11_S11-AC2_plan_output.txt`.

### S11-AC3 -- JUDGMENT, RECORDED, NOT SELF-GRADED

Output at `S11-AC3_judgment.md`, carried in the instance under `UNVERIFIABLE-BY-INSTRUMENT` with
`status_reason` naming `3.0.0_SA_CVO` at L9. It dispositions 9 of 9 entries of the evidence file
own `unverified` array -- the denominator is READ, not recalled -- states the UNSUPPORTED-vs-
PARTIAL rule it applied and the single PARTIAL that survives it, and names six reads the first
live call must produce before the report is advertised for a tenant.

## 3. CONTROLS

**Mutant.** Four difference controls run INSIDE the battery and each is required to fail:
(1) the unit-blind link, which produces `-0.999998816706432` where the truth is `0.018564905412121`
-- a 100x-class error; (2) the summing build, `BLOCKED: REFUSE_SUMMED_AGGREGATE`; (3) the
`startValue + valueChange` shortcut, which agrees 6 of 9 times and disagrees by up to `$210.68`;
(4) the socket positive control, which moves the vendor-connection counter 0 -> 1 and so proves
the zero in arm (g) is a live measurement. All four fired as expected.

**Determinism.** The battery was run three times. Runs 1 and 2 (pre-fix) diff to 0 lines; run 3
(post-`math`-import removal) is byte-identical to run 1. STABLE.

## 4. SURPRISE ROWS FILED UNDER THIS CELL

`IRPT_BCKEND-W4-S1` OBSERVATION / INERT -- the named `probe_performance.py` invocation cannot
produce the named result: the evidence JSON carries no response bodies and the probe reads three
HAR files that are not in the repository. The bodies were recovered from the probe own output
tree and tied by digest, 8 of 8 equal to `http_receipts[].response_sha256`, then scrubbed and
committed as fixtures -- so the arm is proven from the same bytes the evidence attests.

`IRPT_BCKEND-W4-S2` OBSERVATION / **ARMED**, disarm owner `2.0.0_SA_COO~B` -- `safe-apply` halt
gate resolves identity ONLY from `org/mcp/sessions/${CLAUDE_CODE_SESSION_ID}.serial` and consults
no environment variable, so `OPAL_AGENT_SERIAL` alone blocks the first apply of every
deploy-carrying cell in this round.

`IRPT_BCKEND-W4-S3` OBSERVATION / **ARMED**, disarm owner `2.0.0_SA_COO~B` -- the deployed zip
cannot carry `jsonschema` (no layer declares it) nor the bounded BD helpers (they live in another
Lambda source tree); both remedies are outside this order `<paths>`. Both gaps are VISIBLE in the
function own output rather than silent.

`IRPT_BCKEND-W4-S4` OBSERVATION / INERT -- what "scrubbed" was read to mean for the committed
fixtures: identifiers replaced (242 across five files, verified by a leak check that fails the
generator), every economic number preserved exactly because the numbers ARE the evidence.

## 5. BOUNDS HELD

No live Black Diamond or Orion call (measured: 0 vendor connections, positive control live). No
monitor, alarm, SNS topic or SES send; no schedule and no event source -- the function is
invoke-only and its default transport is `recorded`. No credential in any artifact, fixture or
commit. No served output touched: the apply was 4 added, 0 changed, 0 destroyed. Deploy via
`.tools/safe-apply.sh` with `.tools/terraform.exe` by path; ledger opened before the act, closed
after, sentinel committed then removed by the close. Scratch confined to `/c/tmp/wk-irpt-1-4/.scratch/`.
