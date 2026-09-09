# EG-s-2 result -- bd-49f-etf-ownership-daily: the catch-up ported, the tail arm, deployed

**TO:** `ETFS_GUARDRAIL.TO-EG-s-2` | **Worker:** `0.9.0_WK_ETFS_GUARDRAIL~2` | **Premise:** EG-s-11's own
result (`which-49f-twin-writes-the-served-slices.result.md`) confirmed `WRITER=bd-49f-etf-ownership-daily
EVIDENCE=3` -- the `-canonical` twin is NOT LIVE. This order's premise holds; no BLOCKING row owed on that
account. Neither the `-canonical` twin nor the DS module `backfill_49f_daily_from_monolith_rps.py` is edited.

---

## 1. Acceptance criteria, verbatim with rc and denominator

### S2-AC1 -- the ten-arm battery is green (tail arm (i) + negative control (j) included)

**Invocation:** `python -m pytest infra/aws/lambda/bd-pipeline/bd-49f-etf-ownership-daily/test_catchup_window.py -q`

```
..........                                                              [100%]
10 passed in 1.76s
```
rc=0. Denominator: 10 of 10 arms passed (h, c, d, a, b, e, f, g, i, j). **PASS.**

Built as real `def test_*` functions from the start (per the issuer's amendment on row
`ETFS_GUARDRAIL-W2-S4` from EG-s-1) -- never the bare-script-with-`sys.exit()` shape.

### S2-AC2 -- four properties of the bytes

```
DAYCOUNT_WINDOW=False SHIPPED_SIGNAL=True PROBE=True EMPTY_SOURCE_GUARD=True
```
rc=0. Denominator: 4 of 4 matched. **PASS.**

### S2-AC3 -- NO fifth in-repo copy; the DS module untouched

```
COMMITTED_CAL_COPY=False DS_MODULE_UNTOUCHED=True
```
rc=0. Denominator: 1 of 1 absence check; 1 of 1 sha256 pair match. **PASS.**

**Attached layer ARNs (`get-function-configuration --query Layers[].Arn`, post-apply):**
```json
[
  "arn:aws:lambda:us-east-1:313476888478:layer:pandas-pyarrow-layer:1",
  "arn:aws:lambda:us-east-1:313476888478:layer:opal-trading-calendar-layer:1"
]
```
Both the pre-existing pandas layer and the newly-attached `opal-trading-calendar-layer:1` present.

### S2-AC4 -- the commit gate is clean

```
All checks passed!
OK: no unguarded strict-utf8 log reads.
OK: pre-commit gate clean for 2 of 2 file(s)
```
rc=0. **PASS.**

### S2-AC5 -- the plan changes this Lambda + the layer + the one Sid, nothing else

**Invocation:** `.tools/terraform.exe -chdir=infra/aws/terraform/bd-pipeline plan -no-color -input=false -lock=false`

**Summary line:** `Plan: 0 to add, 2 to change, 0 to destroy.`

**Every resource named (denominator: 2 of 2 changed, 0 of 0 added/destroyed):**
1. `aws_iam_role_policy.bd_49f_etf_ownership_daily_s3` -- adds `ReadShippedSignal`
   (`s3:GetObject` on `arn:aws:s3:::opal-data-etfs/platinum/reports/*/etf_ownership.pdf`).
2. `module.bd_49f_etf_ownership_daily.aws_lambda_function.this` -- `layers` gains
   `opal-trading-calendar-layer:1`; `s3_object_version`/`source_code_hash` change to the new upload
   (`5Q9X+m0VzbY2kab3NaOa26Ho5mjmS1DiRnBshz4xrUo=`).

`bd-pipeline` IS a wide directory (dozens of resources across many functions) -- the plan named
exactly these two addresses and no others; applied whole (no `-target` narrowing was needed).
**PASS -- no BLOCKING row owed.**

### S2-AC6 -- 0-diff after the apply

Applied via `HALT_ACK=1 .tools/safe-apply.sh -chdir=infra/aws/terraform/bd-pipeline apply -input=false -auto-approve`
-> `Apply complete! Resources: 0 added, 2 changed, 0 destroyed.`

```
...
No changes. Your infrastructure matches the configuration.
rc=0
```
No pre-existing foreign drift was found in the (wide) `bd-pipeline` directory either before or
after this order's changes -- the 0-diff replan covers the whole directory cleanly. **PASS.**

### S2-AC7 -- served CodeSha256 == built artifact_sha256

```
SERVED CodeSha256 (live get-function-configuration): 5Q9X+m0VzbY2kab3NaOa26Ho5mjmS1DiRnBshz4xrUo=
BUILT  artifact_sha256 (lambda-source-map.json, written by build-and-upload.sh): 5Q9X+m0VzbY2kab3NaOa26Ho5mjmS1DiRnBshz4xrUo=
VERDICT: MATCH
```
rc=0. **PASS.**

### S2-AC8 -- the deployed probe answers for 2026-08-04, writes nothing

**Invocation:** `.tools/aws lambda invoke --function-name bd-49f-etf-ownership-daily --payload "{\"date\":\"2026-08-04\",\"probe\":true}" .scratch/bd49f_probe_out.json`
(written to a real file directly, per the lesson already recorded in EG-s-1's result -- the literal
`/dev/stdout` target fails under the CLI v1 shim on this box with an MSYS pipe error unrelated to the
payload form.)

```
{"status": "probe", "date": "2026-08-04", "partition": true, "priced": 93398, "output_exists": true}
```
Denominator: `"partition": true` matched; `priced=93398`, `output_exists=true` recorded. **PASS.**
No write reachable (proven at the unit level by arm (g), which raises `AssertionError` if
`put_object` is ever called).

### S2-AC9 -- judgment, RECORD; NO VERDICT

Arm (i) proves a partition for day D (real-`today` minus 14 calendar days, walked to the nearest
trading day) is found and processed by the reporting-obligation window, exercising `_catchup_missing_dates`'s
own internal `datetime.now()` call (not a mocked clock). Arm (j) is the negative control: the SAME D,
tested against the OLD `CATCHUP_WINDOW_DAYS=10` semantics SIMULATED (not calling any production code,
since that constant no longer exists in the module by construction of arm (h)) -- D falls outside the
simulated 10-day window, proving the two designs are discriminable, not merely that the new one happens
to pass. No day count is re-proposed (arm (h) confirms `CATCHUP_WINDOW_DAYS` absent from the deployed
module). The DS module (`backfill_49f_daily_from_monolith_rps.py`) is byte-identical to its source
(S2-AC3). FWD-1's EXERCISED grade is explicitly NOT manufactured here -- the next scheduled fire
(`cron(45 10 * * ? *)`) is the evidence this order deploys the mechanism for.

---

## 2. THE DEPLOY -- sequence, hashes, ledger

| step | invocation | result |
|---|---|---|
| commit source | `safe-commit.sh` (lambda_function.py, test_catchup_window.py, .tf edit) | `71cb2e8579` |
| build+upload | `bash infra/aws/lambda/ci/build-and-upload.sh bd-pipeline bd-49f-etf-ownership-daily` | SHA256 `5Q9X+m0VzbY2kab3NaOa26Ho5mjmS1DiRnBshz4xrUo=`, uploaded, write VERIFIED |
| commit artifact | `safe-commit.sh` (lambda-source-map.json) | `f65d81a020` |
| ledger open | `deploy_ledger.py open --slug etfs-guardrail-eg-s-2-bd49f-catchup-port ... --lambda bd-49f-etf-ownership-daily` | 1 tf-lambda leg opened |
| commit ledger open | `safe-commit.sh` | `a1c372983f` |
| terraform init | `.tools/terraform.exe -chdir=infra/aws/terraform/bd-pipeline init -input=false` | initialized |
| plan | see S2-AC5 | 0 add / 2 change / 0 destroy |
| apply | `HALT_ACK=1 .tools/safe-apply.sh -chdir=infra/aws/terraform/bd-pipeline apply -input=false -auto-approve` | `Apply complete! Resources: 0 added, 2 changed, 0 destroyed.` |
| 0-diff | see S2-AC6 | `No changes.` |
| served vs built | see S2-AC7 | MATCH |
| probe | see S2-AC8 | `partition: true` |
| record deploy (PARTIAL -- see s.3) | `bash infra/aws/lambda/ci/record-terraform-deploy.sh bd-pipeline --function bd-49f-etf-ownership-daily --author "..."` | REFUSED by the owned-paths gate (CHANGELOG.json out of grant); recovered by committing the source-map half only |
| commit source-map record | `safe-commit.sh` (lambda-source-map.json + surprise row) | `cd56795673` |
| close-leg | `deploy_ledger.py close-leg --slug ... --leg-id bd-49f-etf-ownership-daily --proof "..."` | leg closed |
| close | `deploy_ledger.py close --slug etfs-guardrail-eg-s-2-bd49f-catchup-port` | `CLOSED ... all 1 legs proven` |
| commit ledger close | `safe-commit.sh` | `fcb3e42f31` |

**No leg left open; the change-management entry is CLOSED.**

---

## 3. Instrument note -- `record-terraform-deploy.sh` writes outside this TO's `<paths>` grant

`record-terraform-deploy.sh bd-pipeline --function bd-49f-etf-ownership-daily ...` is itself named on
the TO's `<paths>` grant, but running it also stages a write to
`infra/aws/terraform/bd-pipeline/CHANGELOG.json` -- a file the TO's `<paths>` block does NOT name
(only the two specific files `bd-49f-etf-ownership-daily.tf` and `.terraform.lock.hcl` are granted
under that directory; `bd-pipeline` is "a wide directory" per S2-AC5's own text, deliberately not
handed over wholesale). The script's internal `git commit` was REFUSED by the owned-paths lane gate:

```
ERROR: owned-paths lane violation(s) detected (block mode):
VIOLATION: infra/aws/terraform/bd-pipeline/CHANGELOG.json -- lane=CLOUD_OPS_OR_ETL ...
agent=0.9.0_WK_ETFS_GUARDRAIL~2 not in permitted_agents -- WORKER: no NON-TERMINAL task order
at HEAD issued_to this serial names this path in its <paths> block
ERROR: safe-commit did NOT commit (rc=1).
```

Per the TO's own BOUNDS ("A path you need that it does not name is a BLOCKING row, never an
override"), filed `ETFS_GUARDRAIL-W2-S5` rather than widening my own grant. Recovered by unstaging
the CHANGELOG.json half (`git reset`, non-destructive; left as an untouched unstaged worktree
difference) and committing ONLY `infra/aws/lambda/ci/lambda-source-map.json` (in-grant) with the
same `last_deployed_commit`/`last_deployed_at` values the script had computed. The deploy itself is
independently verified without this commit (S2-AC7 MATCH, S2-AC6 0-diff); the gap is purely the
CHANGELOG.json audit-trail entry, which this worker cannot write.

---

## 4. Bounds honored

- No served `daily/49financial/*.json` object deleted; no dated non-probe invoke run (would write a slice).
- NEVER#1/NEVER#2: no read added on `opal-data-bd`, `opal-data-cot`, `opal-data-inf`, or `blackdiamond/`;
  the existing `MonolithFactRpsRead`/`List` Sids stay scoped to `schwab/08242234/silver/fact_rps/*`
  exactly; the one new Sid reads only `opal-data-etfs/platinum/reports/*/etf_ownership.pdf`.
- `.tools/safe-apply.sh` only; `aws lambda update-function-code` never called; ledger opened before the
  apply, closed after; plan read before apply (S2-AC5); 0-diff after (S2-AC6); artifact upload preceded
  the plan.
- `.tools/terraform.exe` (v1.9.8, the estate's pinned binary, provisioned by the issuer into this
  worktree) used throughout; confirmed via `.tools/terraform.exe version` before any plan; the PATH
  `terraform` (v1.14.5) was never invoked.

## 5. Push state (measured)

See the WORKER REPORT for the value read at report time.
