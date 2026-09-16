# F1 -- the placeholder gaps re-run at HEAD, new count printed BESIDE 49 (round 5)

**Cell:** LGIC_NAMING `LN-f-1`, round 5 (decomposition v7.1 s.0f), task order
`LGIC_NAMING.TO-LN-f-1-r5`, written by `0.9.0_WK_LGIC_NAMING~3` on branch `wk-lgic-naming-5-3`, cut from
CLOUD @`119a08a196`. **outcome_ref** FWD-5.

## What moved, and why this cell exists

Round 4's headline (row `LGIC_NAMING-W4-S3`, adjudicated `LGIC_NAMING-C-S25`, GRADUATED) was **49**: of round
4's 69-name firm-attributed population, all 69 graded without a single `grade()` exception, and every one of
the 49 whose canonical form still carried a `{system}` placeholder was listed under that round's `raise` array
with a step and a `missing_row` -- at that round's convention, "raise" meant "carries an unfilled `{system}`
placeholder," not a Python exception, because in round 4's narrower population `grade()` itself never raised.
That count was measured at base `5e908a4929`, where `infra/logic/registry/resources.json` **does not exist**
(confirmed below, MEASURED). `infra/logic/registry/resources.json` now exists at HEAD -- minted by
`LGIC_ENFORCE` `EN-r-4`, commit `b15ed01ee6`, 30 rows -- so the world round 4 measured against moved under a
correctly-measured number (C-S25's own finding, adopted here rather than re-litigated).

**MEASURED (this tree):**
```
$ git cat-file -e 5e908a4929:infra/logic/registry/resources.json
fatal: path 'infra/logic/registry/resources.json' exists on disk, but not in '5e908a4929'
$ git ls-tree HEAD infra/logic/registry/
... resources.json  (blob ad38adcba51aa8598996138422f5063708f9f466, PRESENT)
```

## This round's population is WIDER than round 4's, by the order's own instruction

This order directs grading against `LIVE_NAMES.json`'s full `by_type.IAM_ROLE` list -- **240** names -- not
round 4's 69-name firm-attributed subset (`bd`/`49f`/`inf`/`inflection`/`cot`/`cottonwood`/`demo` alias
tokens only). Every name is graded with `lib/opal_naming.py`'s `grade(name, "IAM_ROLE")` called directly at
this tree, never hand-graded.

**Result over the 240:** 172 clean (no placeholder, no raise), 54 still carry `{system}` in their canonical
form (a placeholder, round 4's "raise" sense), and 14 now raise `RaiseDefect` outright -- a class that never
appeared in round 4's narrower 69-name population, where "0 names where `grade()` itself RAISEs" is the
measured fact recorded in that round's own deliverable (`firm-patterns.r4.result.md`).

## Item 3: 49 beside the new count -- and whether they are comparable

**They are NOT directly comparable, because they enumerate different populations (69 vs 240), and this
record does not subtract one from the other.** Two numbers, printed side by side, each with its own stated
population:

| | population | placeholder ("raise") count | base |
|---|---|---|---|
| round 4 headline | 69 (firm-attributed subset) | **49** | `5e908a4929` (resources.json ABSENT) |
| this round | 240 (full `by_type.IAM_ROLE`) | **54** | HEAD (resources.json PRESENT, 30 rows) |

54 is not "49 minus something" and not "49 plus something": it is a different count over a population 3.5x
larger, and the fact that it is numerically close to 49 is a coincidence of scale, not evidence either way
about the registry's effect.

**The one comparison that IS apples-to-apples: round 4's own 69 names, re-graded at THIS tree.** Re-running
`grade()` over exactly the 69 names round 4's `n4-firm-patterns.md` attributed, at HEAD:

| | placeholder count | clean | raised |
|---|---|---|---|
| round 4 (`5e908a4929`) | 49 | 20 | 0 |
| this tree (HEAD), SAME 69 names | **19** | 50 | 0 |

The drop is exactly **30** -- equal to `registry_rows` (30), the count of rows `EN-r-4` minted in
`resources.json`. That is not approximate: every one of the 30 rows resolves a name that was among round 4's
49 placeholders, and none of the 69 raises outright at either vintage. **This is the honest "new count beside
49": 19, on the same population 49 was measured against.** The 54 figure this record's JSON reports (required
by the order and by `F1R5-AC1`) is a different, wider measurement and is never substituted for the 19.

## Item 4/5: every remaining gap names a REAL `missing_row`, and the negative control

**68 gaps total** (54 placeholder + 14 raise, over the full 240-name population) are listed in the `raises`
array below, each with a `missing_row` pointing at a specific, checked absence in
`infra/logic/registry/`, never guessed:

- **The 54 PLACEHOLDER entries** (step `R1.d`, round 4's convention): each name's `missing_row` states that
  `infra/logic/registry/resources.json` carries no `resources[]` row for `(name, "IAM_ROLE")`, checked
  against all 30 rows present (none match) -- the same mechanism that, when a row IS present, resolves the
  placeholder (as it did for 30 of round 4's 49, above).
- **The 14 RAISE entries** (Python `RaiseDefect`, steps `R1.c`/`R1.d`/`R1.f`/`R2`) split into two REAL,
  checked classes:
  - **4 tokens already in `systems.json`'s `unresolved` array** (`astn`, `trade`, `news`, `find` -- 11 of the
    14 names): the `missing_row` names the specific `unresolved[]` entry and its stated `why`, and states
    that no row has been promoted to `systems.systems[]` to give the token a class/long/owner_directive.
  - **4 tokens with NO row anywhere** (`portal`, `security`, `sentiment`, `vpc` -- 4 names): the `missing_row`
    states, checked, that the token is absent from `systems.systems[]`, `systems.unresolved[]`, and every
    `refused_keys.*` list.

  No system is guessed for any of the 68 (CLAUDE.md Rule 30); every `missing_row` is a citation into a file
  this record's builder script (run at this tree) actually read, not typed from memory.

**Negative control (both readings recorded):** a planted name carrying no registry row anywhere,
`zzznonexistent-fabricated-lambda-role`, graded against `lib/opal_naming.py` at this tree:

```
PLANTED RAISED: RaiseDefect R1.f: 'zzznonexistent' is in no vocabulary; no registry row resolves it
REAL    RAISED: RaiseDefect R1.f: 'portal' is in no vocabulary; no registry row resolves it
```

Both raise the same step (`R1.f`), on the same "no row anywhere" class -- the mechanism that raises on a real
gap raises identically on a name deliberately given no row, so the raise path is exercised and not silently
bypassed.

## The record (ONE json fence, per the order)

```json
{
 "population": 240,
 "placeholder_count": 54,
 "raised_count": 14,
 "clean_count": 172,
 "r4_headline": 49,
 "r4_base": "5e908a4929",
 "registry_rows": 30,
 "same_population_comparison": {
  "round4_population": 69,
  "round4_placeholder_count_at_r4_base": 49,
  "round4_placeholder_count_at_HEAD": 19,
  "delta": -30,
  "note": "Round 4's own 69-name firm-attributed population, re-graded at THIS tree (HEAD): placeholder count drops from 49 to 19, a decrease of exactly 30 -- equal to registry_rows, the count of infra/logic/registry/resources.json rows LGIC_ENFORCE EN-r-4 minted. This is the one apples-to-apples comparison in this record; the 49-vs-54 comparison below is NOT apples-to-apples (different populations, 69 vs 240)."
 },
 "negative_control": {
  "planted_name": "zzznonexistent-fabricated-lambda-role",
  "planted_reading": "RaiseDefect R1.f: 'zzznonexistent' is in no vocabulary; no registry row resolves it",
  "real_reading_name": "portal-auth-lambda-role",
  "real_reading": "RaiseDefect R1.f: 'portal' is in no vocabulary; no registry row resolves it",
  "note": "The planted name carries no registry row anywhere (not systems[], not unresolved[], not refused_keys.*) and grade() still RAISEs on it, the same class of raise (R1.f) as a genuine gap (portal-auth-lambda-role). Both readings recorded above."
 },
 "raises": [
  {
   "name": "bd-allocation-checker-lambda-role",
   "missing_row": "infra/logic/registry/resources.json: no resources[] row for name='bd-allocation-checker-lambda-role' type='IAM_ROLE' (checked against all 30 rows present)",
   "step": "R1.d",
   "class": "PLACEHOLDER",
   "canonical": "{system}-49f-allocation-checker-lambda-role"
  },
  {
   "name": "bd-allocation-processor-role",
   "missing_row": "infra/logic/registry/resources.json: no resources[] row for name='bd-allocation-processor-role' type='IAM_ROLE' (checked against all 30 rows present)",
   "step": "R1.d",
   "class": "PLACEHOLDER",
   "canonical": "{system}-49f-allocation-processor-role"
  },
  {
   "name": "bd-daily-trigger-lambda-role",
   "missing_row": "infra/logic/registry/resources.json: no resources[] row for name='bd-daily-trigger-lambda-role' type='IAM_ROLE' (checked against all 30 rows present)",
   "step": "R1.d",
   "class": "PLACEHOLDER",
   "canonical": "{system}-49f-daily-trigger-lambda-role"
  },
  {
   "name": "bd-exporter-ec2-role",
   "missing_row": "infra/logic/registry/resources.json: no resources[] row for name='bd-exporter-ec2-role' type='IAM_ROLE' (checked against all 30 rows present)",
   "step": "R1.d",
   "class": "PLACEHOLDER",
   "canonical": "{system}-49f-exporter-ec2-role"
  },
  {
   "name": "bd-gold-detail-generator-role",
   "missing_row": "infra/logic/registry/resources.json: no resources[] row for name='bd-gold-detail-generator-role' type='IAM_ROLE' (checked against all 30 rows present)",
   "step": "R1.d",
   "class": "PLACEHOLDER",
   "canonical": "{system}-49f-gold-detail-generator-role"
  },
  {
   "name": "bd-gold-eventbridge-step-functions-role",
   "missing_row": "infra/logic/registry/resources.json: no resources[] row for name='bd-gold-eventbridge-step-functions-role' type='IAM_ROLE' (checked against all 30 rows present)",
   "step": "R1.d",
   "class": "PLACEHOLDER",
   "canonical": "{system}-49f-gold-eventbridge-step-functions-role"
  },
  {
   "name": "bd-gold-layer-lambda-role",
   "missing_row": "infra/logic/registry/resources.json: no resources[] row for name='bd-gold-layer-lambda-role' type='IAM_ROLE' (checked against all 30 rows present)",
   "step": "R1.d",
   "class": "PLACEHOLDER",
   "canonical": "{system}-49f-gold-layer-lambda-role"
  },
  {
   "name": "bd-gold-step-functions-role",
   "missing_row": "infra/logic/registry/resources.json: no resources[] row for name='bd-gold-step-functions-role' type='IAM_ROLE' (checked against all 30 rows present)",
   "step": "R1.d",
   "class": "PLACEHOLDER",
   "canonical": "{system}-49f-gold-step-functions-role"
  },
  {
   "name": "bd-merge-daily-lambda-role",
   "missing_row": "infra/logic/registry/resources.json: no resources[] row for name='bd-merge-daily-lambda-role' type='IAM_ROLE' (checked against all 30 rows present)",
   "step": "R1.d",
   "class": "PLACEHOLDER",
   "canonical": "{system}-49f-merge-daily-lambda-role"
  },
  {
   "name": "bd-pipeline-task-role",
   "missing_row": "infra/logic/registry/resources.json: no resources[] row for name='bd-pipeline-task-role' type='IAM_ROLE' (checked against all 30 rows present)",
   "step": "R1.d",
   "class": "PLACEHOLDER",
   "canonical": "{system}-49f-pipeline-task-role"
  },
  {
   "name": "bd-processor-lambda-role",
   "missing_row": "infra/logic/registry/resources.json: no resources[] row for name='bd-processor-lambda-role' type='IAM_ROLE' (checked against all 30 rows present)",
   "step": "R1.d",
   "class": "PLACEHOLDER",
   "canonical": "{system}-49f-processor-lambda-role"
  },
  {
   "name": "codebuild-semantic-clustering-role",
   "missing_row": "infra/logic/registry/resources.json: no resources[] row for name='codebuild-semantic-clustering-role' type='IAM_ROLE' (checked against all 30 rows present)",
   "step": "R1.d",
   "class": "PLACEHOLDER",
   "canonical": "{system}-codebuild-semantic-clustering-role"
  },
  {
   "name": "consolidation-gold-runner-automation-start-role",
   "missing_row": "infra/logic/registry/resources.json: no resources[] row for name='consolidation-gold-runner-automation-start-role' type='IAM_ROLE' (checked against all 30 rows present)",
   "step": "R1.d",
   "class": "PLACEHOLDER",
   "canonical": "{system}-consolidation-gold-runner-automation-start-role"
  },
  {
   "name": "consolidation-gold-runner-events-invoke-ssm-role",
   "missing_row": "infra/logic/registry/resources.json: no resources[] row for name='consolidation-gold-runner-events-invoke-ssm-role' type='IAM_ROLE' (checked against all 30 rows present)",
   "step": "R1.d",
   "class": "PLACEHOLDER",
   "canonical": "{system}-consolidation-gold-runner-events-invoke-ssm-role"
  },
  {
   "name": "consolidation-gold-runner-role",
   "missing_row": "infra/logic/registry/resources.json: no resources[] row for name='consolidation-gold-runner-role' type='IAM_ROLE' (checked against all 30 rows present)",
   "step": "R1.d",
   "class": "PLACEHOLDER",
   "canonical": "{system}-consolidation-gold-runner-role"
  },
  {
   "name": "cot-session-scheduler-role",
   "missing_row": "infra/logic/registry/resources.json: no resources[] row for name='cot-session-scheduler-role' type='IAM_ROLE' (checked against all 30 rows present)",
   "step": "R1.d",
   "class": "PLACEHOLDER",
   "canonical": "{system}-cot-session-scheduler-role"
  },
  {
   "name": "daily-sprint-generator-role",
   "missing_row": "infra/logic/registry/resources.json: no resources[] row for name='daily-sprint-generator-role' type='IAM_ROLE' (checked against all 30 rows present)",
   "step": "R1.d",
   "class": "PLACEHOLDER",
   "canonical": "{system}-daily-sprint-generator-role"
  },
  {
   "name": "deck-generation-lambda-role",
   "missing_row": "infra/logic/registry/resources.json: no resources[] row for name='deck-generation-lambda-role' type='IAM_ROLE' (checked against all 30 rows present)",
   "step": "R1.d",
   "class": "PLACEHOLDER",
   "canonical": "{system}-deck-generation-lambda-role"
  },
  {
   "name": "ec2-auto-shutdown-enforcer-role",
   "missing_row": "infra/logic/registry/resources.json: no resources[] row for name='ec2-auto-shutdown-enforcer-role' type='IAM_ROLE' (checked against all 30 rows present)",
   "step": "R1.d",
   "class": "PLACEHOLDER",
   "canonical": "{system}-ec2-auto-shutdown-enforcer-role"
  },
  {
   "name": "ec2-ssm-role",
   "missing_row": "infra/logic/registry/resources.json: no resources[] row for name='ec2-ssm-role' type='IAM_ROLE' (checked against all 30 rows present)",
   "step": "R1.d",
   "class": "PLACEHOLDER",
   "canonical": "{system}-ec2-ssm-role"
  },
  {
   "name": "ecsTaskExecutionRole",
   "missing_row": "infra/logic/registry/resources.json: no resources[] row for name='ecsTaskExecutionRole' type='IAM_ROLE' (checked against all 30 rows present)",
   "step": "R1.d",
   "class": "PLACEHOLDER",
   "canonical": "{system}-ecs-task-execution-role"
  },
  {
   "name": "etf-ownership-dashboard-role",
   "missing_row": "infra/logic/registry/resources.json: no resources[] row for name='etf-ownership-dashboard-role' type='IAM_ROLE' (checked against all 30 rows present)",
   "step": "R1.d",
   "class": "PLACEHOLDER",
   "canonical": "{system}-etf-ownership-dashboard-role"
  },
  {
   "name": "etf-positioning-producer-role",
   "missing_row": "infra/logic/registry/resources.json: no resources[] row for name='etf-positioning-producer-role' type='IAM_ROLE' (checked against all 30 rows present)",
   "step": "R1.d",
   "class": "PLACEHOLDER",
   "canonical": "{system}-etf-positioning-producer-role"
  },
  {
   "name": "exec-summary-generator-role",
   "missing_row": "infra/logic/registry/resources.json: no resources[] row for name='exec-summary-generator-role' type='IAM_ROLE' (checked against all 30 rows present)",
   "step": "R1.d",
   "class": "PLACEHOLDER",
   "canonical": "{system}-exec-summary-generator-role"
  },
  {
   "name": "finbert-ec2-backfill-role",
   "missing_row": "infra/logic/registry/resources.json: no resources[] row for name='finbert-ec2-backfill-role' type='IAM_ROLE' (checked against all 30 rows present)",
   "step": "R1.d",
   "class": "PLACEHOLDER",
   "canonical": "{system}-finbert-ec2-backfill-role"
  },
  {
   "name": "github-actions-opal-deploy",
   "missing_row": "infra/logic/registry/resources.json: no resources[] row for name='github-actions-opal-deploy' type='IAM_ROLE' (checked against all 30 rows present)",
   "step": "R1.d",
   "class": "PLACEHOLDER",
   "canonical": "{system}-github-actions-opal-deploy-role"
  },
  {
   "name": "gldinc-ss4c-canary-role",
   "missing_row": "infra/logic/registry/resources.json: no resources[] row for name='gldinc-ss4c-canary-role' type='IAM_ROLE' (checked against all 30 rows present)",
   "step": "R1.d",
   "class": "PLACEHOLDER",
   "canonical": "{system}-gldinc-ss4c-canary-role"
  },
  {
   "name": "historical-prices-lambda-role",
   "missing_row": "infra/logic/registry/resources.json: no resources[] row for name='historical-prices-lambda-role' type='IAM_ROLE' (checked against all 30 rows present)",
   "step": "R1.d",
   "class": "PLACEHOLDER",
   "canonical": "{system}-historical-prices-lambda-role"
  },
  {
   "name": "inf-assets-trigger-lambda-role",
   "missing_row": "infra/logic/registry/resources.json: no resources[] row for name='inf-assets-trigger-lambda-role' type='IAM_ROLE' (checked against all 30 rows present)",
   "step": "R1.d",
   "class": "PLACEHOLDER",
   "canonical": "{system}-inf-assets-trigger-lambda-role"
  },
  {
   "name": "inf-bronze-complete-emitter-role",
   "missing_row": "infra/logic/registry/resources.json: no resources[] row for name='inf-bronze-complete-emitter-role' type='IAM_ROLE' (checked against all 30 rows present)",
   "step": "R1.d",
   "class": "PLACEHOLDER",
   "canonical": "{system}-inf-bronze-complete-emitter-role"
  },
  {
   "name": "inf-exporter-ec2-role",
   "missing_row": "infra/logic/registry/resources.json: no resources[] row for name='inf-exporter-ec2-role' type='IAM_ROLE' (checked against all 30 rows present)",
   "step": "R1.d",
   "class": "PLACEHOLDER",
   "canonical": "{system}-inf-exporter-ec2-role"
  },
  {
   "name": "inf-gold-layer-ec2-role",
   "missing_row": "infra/logic/registry/resources.json: no resources[] row for name='inf-gold-layer-ec2-role' type='IAM_ROLE' (checked against all 30 rows present)",
   "step": "R1.d",
   "class": "PLACEHOLDER",
   "canonical": "{system}-inf-gold-layer-ec2-role"
  },
  {
   "name": "inf-gold-layer-lambda-role",
   "missing_row": "infra/logic/registry/resources.json: no resources[] row for name='inf-gold-layer-lambda-role' type='IAM_ROLE' (checked against all 30 rows present)",
   "step": "R1.d",
   "class": "PLACEHOLDER",
   "canonical": "{system}-inf-gold-layer-lambda-role"
  },
  {
   "name": "inf-gold-trigger-lambda-role",
   "missing_row": "infra/logic/registry/resources.json: no resources[] row for name='inf-gold-trigger-lambda-role' type='IAM_ROLE' (checked against all 30 rows present)",
   "step": "R1.d",
   "class": "PLACEHOLDER",
   "canonical": "{system}-inf-gold-trigger-lambda-role"
  },
  {
   "name": "infrastructure-ops-lambda-role",
   "missing_row": "infra/logic/registry/resources.json: no resources[] row for name='infrastructure-ops-lambda-role' type='IAM_ROLE' (checked against all 30 rows present)",
   "step": "R1.d",
   "class": "PLACEHOLDER",
   "canonical": "{system}-infrastructure-ops-lambda-role"
  },
  {
   "name": "infrastructure-snapshot-role",
   "missing_row": "infra/logic/registry/resources.json: no resources[] row for name='infrastructure-snapshot-role' type='IAM_ROLE' (checked against all 30 rows present)",
   "step": "R1.d",
   "class": "PLACEHOLDER",
   "canonical": "{system}-infrastructure-snapshot-role"
  },
  {
   "name": "lambda-access-anomaly-scanner-role",
   "missing_row": "infra/logic/registry/resources.json: no resources[] row for name='lambda-access-anomaly-scanner-role' type='IAM_ROLE' (checked against all 30 rows present)",
   "step": "R1.d",
   "class": "PLACEHOLDER",
   "canonical": "{system}-lambda-access-anomaly-scanner-role"
  },
  {
   "name": "lambda-cost-anomaly-scanner-role",
   "missing_row": "infra/logic/registry/resources.json: no resources[] row for name='lambda-cost-anomaly-scanner-role' type='IAM_ROLE' (checked against all 30 rows present)",
   "step": "R1.d",
   "class": "PLACEHOLDER",
   "canonical": "{system}-lambda-cost-anomaly-scanner-role"
  },
  {
   "name": "lambda-ec2-runtime-monitor-role",
   "missing_row": "infra/logic/registry/resources.json: no resources[] row for name='lambda-ec2-runtime-monitor-role' type='IAM_ROLE' (checked against all 30 rows present)",
   "step": "R1.d",
   "class": "PLACEHOLDER",
   "canonical": "{system}-lambda-ec2-runtime-monitor-role"
  },
  {
   "name": "lambda-edge-execution-role",
   "missing_row": "infra/logic/registry/resources.json: no resources[] row for name='lambda-edge-execution-role' type='IAM_ROLE' (checked against all 30 rows present)",
   "step": "R1.d",
   "class": "PLACEHOLDER",
   "canonical": "{system}-lambda-edge-execution-role"
  },
  {
   "name": "lambda-execution-role",
   "missing_row": "infra/logic/registry/resources.json: no resources[] row for name='lambda-execution-role' type='IAM_ROLE' (checked against all 30 rows present)",
   "step": "R1.d",
   "class": "PLACEHOLDER",
   "canonical": "{system}-lambda-execution-role"
  },
  {
   "name": "lambda-test-role",
   "missing_row": "infra/logic/registry/resources.json: no resources[] row for name='lambda-test-role' type='IAM_ROLE' (checked against all 30 rows present)",
   "step": "R1.d",
   "class": "PLACEHOLDER",
   "canonical": "{system}-lambda-test-role"
  },
  {
   "name": "market-data-generator-lambda-role",
   "missing_row": "infra/logic/registry/resources.json: no resources[] row for name='market-data-generator-lambda-role' type='IAM_ROLE' (checked against all 30 rows present)",
   "step": "R1.d",
   "class": "PLACEHOLDER",
   "canonical": "{system}-market-data-generator-lambda-role"
  },
  {
   "name": "market-update-lambda-role",
   "missing_row": "infra/logic/registry/resources.json: no resources[] row for name='market-update-lambda-role' type='IAM_ROLE' (checked against all 30 rows present)",
   "step": "R1.d",
   "class": "PLACEHOLDER",
   "canonical": "{system}-market-update-lambda-role"
  },
  {
   "name": "opalinvest-auth-lambda-role",
   "missing_row": "infra/logic/registry/resources.json: no resources[] row for name='opalinvest-auth-lambda-role' type='IAM_ROLE' (checked against all 30 rows present)",
   "step": "R1.d",
   "class": "PLACEHOLDER",
   "canonical": "{system}-opalinvest-auth-lambda-role"
  },
  {
   "name": "outset-drift-publisher-laptop",
   "missing_row": "infra/logic/registry/resources.json: no resources[] row for name='outset-drift-publisher-laptop' type='IAM_ROLE' (checked against all 30 rows present)",
   "step": "R1.d",
   "class": "PLACEHOLDER",
   "canonical": "{system}-outset-drift-publisher-laptop-role"
  },
  {
   "name": "partner-etl-ops-sqs-consumer-role",
   "missing_row": "infra/logic/registry/resources.json: no resources[] row for name='partner-etl-ops-sqs-consumer-role' type='IAM_ROLE' (checked against all 30 rows present)",
   "step": "R1.d",
   "class": "PLACEHOLDER",
   "canonical": "{system}-partner-etl-ops-sqs-consumer-role"
  },
  {
   "name": "partners-lambda-role",
   "missing_row": "infra/logic/registry/resources.json: no resources[] row for name='partners-lambda-role' type='IAM_ROLE' (checked against all 30 rows present)",
   "step": "R1.d",
   "class": "PLACEHOLDER",
   "canonical": "{system}-partners-lambda-role"
  },
  {
   "name": "portfolio-export-lambda-role",
   "missing_row": "infra/logic/registry/resources.json: no resources[] row for name='portfolio-export-lambda-role' type='IAM_ROLE' (checked against all 30 rows present)",
   "step": "R1.d",
   "class": "PLACEHOLDER",
   "canonical": "{system}-portfolio-export-lambda-role"
  },
  {
   "name": "portfolio-management-lambda-role",
   "missing_row": "infra/logic/registry/resources.json: no resources[] row for name='portfolio-management-lambda-role' type='IAM_ROLE' (checked against all 30 rows present)",
   "step": "R1.d",
   "class": "PLACEHOLDER",
   "canonical": "{system}-portfolio-management-lambda-role"
  },
  {
   "name": "quartz-si2-spike-role",
   "missing_row": "infra/logic/registry/resources.json: no resources[] row for name='quartz-si2-spike-role' type='IAM_ROLE' (checked against all 30 rows present)",
   "step": "R1.d",
   "class": "PLACEHOLDER",
   "canonical": "{system}-quartz-si2-spike-role"
  },
  {
   "name": "rds-monitoring-role",
   "missing_row": "infra/logic/registry/resources.json: no resources[] row for name='rds-monitoring-role' type='IAM_ROLE' (checked against all 30 rows present)",
   "step": "R1.d",
   "class": "PLACEHOLDER",
   "canonical": "{system}-rds-monitoring-role"
  },
  {
   "name": "workspace-sync-lambda-role",
   "missing_row": "infra/logic/registry/resources.json: no resources[] row for name='workspace-sync-lambda-role' type='IAM_ROLE' (checked against all 30 rows present)",
   "step": "R1.d",
   "class": "PLACEHOLDER",
   "canonical": "{system}-workspace-sync-lambda-role"
  },
  {
   "name": "wp5-49f-feeder-scheduler-role",
   "missing_row": "infra/logic/registry/resources.json: no resources[] row for name='wp5-49f-feeder-scheduler-role' type='IAM_ROLE' (checked against all 30 rows present)",
   "step": "R1.d",
   "class": "PLACEHOLDER",
   "canonical": "{system}-49f-wp5-feeder-scheduler-role"
  },
  {
   "name": "astn-wsjft-orchestrator-role",
   "missing_row": "infra/logic/registry/systems.json: token 'astn' is listed only under systems.unresolved (why: GRADING_RULE.md V1 lists it as a PRODUCT, but no DIRECTIVES.yaml line and no mission-tree project names its owner, so owner_directive cannot be written (row LGIC_ENFORCE-W1-S6)); no promoted row exists under systems.systems[] to give it a class/long/owner_directive",
   "step": "R1.c",
   "class": "RAISE",
   "detail": "R1.c: 'astn' is an unresolved token (V2)"
  },
  {
   "name": "astn-wsjft-scheduler-role",
   "missing_row": "infra/logic/registry/systems.json: token 'astn' is listed only under systems.unresolved (why: GRADING_RULE.md V1 lists it as a PRODUCT, but no DIRECTIVES.yaml line and no mission-tree project names its owner, so owner_directive cannot be written (row LGIC_ENFORCE-W1-S6)); no promoted row exists under systems.systems[] to give it a class/long/owner_directive",
   "step": "R1.c",
   "class": "RAISE",
   "detail": "R1.c: 'astn' is an unresolved token (V2)"
  },
  {
   "name": "astn-wsjft-scraper-role",
   "missing_row": "infra/logic/registry/systems.json: token 'astn' is listed only under systems.unresolved (why: GRADING_RULE.md V1 lists it as a PRODUCT, but no DIRECTIVES.yaml line and no mission-tree project names its owner, so owner_directive cannot be written (row LGIC_ENFORCE-W1-S6)); no promoted row exists under systems.systems[] to give it a class/long/owner_directive",
   "step": "R1.c",
   "class": "RAISE",
   "detail": "R1.c: 'astn' is an unresolved token (V2)"
  },
  {
   "name": "find-insure-lambda-role",
   "missing_row": "infra/logic/registry/systems.json: token 'find' is listed only under systems.unresolved (why: infra/logic/05_IDENTITY_SPINE.md s.3 marks harvest/find UNRESOLVED (tick-list row 18)); no promoted row exists under systems.systems[] to give it a class/long/owner_directive",
   "step": "R1.c",
   "class": "RAISE",
   "detail": "R1.c: 'find' is an unresolved token (V2)"
  },
  {
   "name": "news-dashboard-processor-role",
   "missing_row": "infra/logic/registry/systems.json: token 'news' is listed only under systems.unresolved (why: GRADING_RULE.md V1 lists it as a PRODUCT, but no DIRECTIVES.yaml line and no mission-tree project names its owner, so owner_directive cannot be written (row LGIC_ENFORCE-W1-S6)); no promoted row exists under systems.systems[] to give it a class/long/owner_directive",
   "step": "R1.c",
   "class": "RAISE",
   "detail": "R1.c: 'news' is an unresolved token (V2)"
  },
  {
   "name": "news-ingestion-lambda-role",
   "missing_row": "infra/logic/registry/systems.json: token 'news' is listed only under systems.unresolved (why: GRADING_RULE.md V1 lists it as a PRODUCT, but no DIRECTIVES.yaml line and no mission-tree project names its owner, so owner_directive cannot be written (row LGIC_ENFORCE-W1-S6)); no promoted row exists under systems.systems[] to give it a class/long/owner_directive",
   "step": "R1.c",
   "class": "RAISE",
   "detail": "R1.c: 'news' is an unresolved token (V2)"
  },
  {
   "name": "news-sentiment-lambda-role",
   "missing_row": "infra/logic/registry/systems.json: token 'news' is listed only under systems.unresolved (why: GRADING_RULE.md V1 lists it as a PRODUCT, but no DIRECTIVES.yaml line and no mission-tree project names its owner, so owner_directive cannot be written (row LGIC_ENFORCE-W1-S6)); no promoted row exists under systems.systems[] to give it a class/long/owner_directive",
   "step": "R1.c",
   "class": "RAISE",
   "detail": "R1.c: 'news' is an unresolved token (V2)"
  },
  {
   "name": "opal-news-lambda-role",
   "missing_row": "infra/logic/registry/systems.json: token 'news' is listed only under systems.unresolved (why: GRADING_RULE.md V1 lists it as a PRODUCT, but no DIRECTIVES.yaml line and no mission-tree project names its owner, so owner_directive cannot be written (row LGIC_ENFORCE-W1-S6)); no promoted row exists under systems.systems[] to give it a class/long/owner_directive",
   "step": "R2",
   "class": "RAISE",
   "detail": "R2: 'news' after opal is an unresolved token (V2)"
  },
  {
   "name": "portal-auth-lambda-role",
   "missing_row": "infra/logic/registry/systems.json: no row anywhere for token 'portal' -- absent from systems[], unresolved[], and refused_keys.{workstream_code,generic_noun,purpose_word}",
   "step": "R1.f",
   "class": "RAISE",
   "detail": "R1.f: 'portal' is in no vocabulary; no registry row resolves it"
  },
  {
   "name": "security-sweep-dedicated-role",
   "missing_row": "infra/logic/registry/systems.json: no row anywhere for token 'security' -- absent from systems[], unresolved[], and refused_keys.{workstream_code,generic_noun,purpose_word}",
   "step": "R1.f",
   "class": "RAISE",
   "detail": "R1.f: 'security' is in no vocabulary; no registry row resolves it"
  },
  {
   "name": "semantic-news-lambda-role",
   "missing_row": "infra/logic/registry/systems.json: token 'news' is listed only under systems.unresolved (why: GRADING_RULE.md V1 lists it as a PRODUCT, but no DIRECTIVES.yaml line and no mission-tree project names its owner, so owner_directive cannot be written (row LGIC_ENFORCE-W1-S6)); no promoted row exists under systems.systems[] to give it a class/long/owner_directive",
   "step": "R1.d",
   "class": "RAISE",
   "detail": "R1.d: the unresolved token 'news' (V2) comes before any system (V1)"
  },
  {
   "name": "sentiment_query_api-role",
   "missing_row": "infra/logic/registry/systems.json: no row anywhere for token 'sentiment' -- absent from systems[], unresolved[], and refused_keys.{workstream_code,generic_noun,purpose_word}",
   "step": "R1.f",
   "class": "RAISE",
   "detail": "R1.f: 'sentiment' is in no vocabulary; no registry row resolves it"
  },
  {
   "name": "trade-submission-lambda-role",
   "missing_row": "infra/logic/registry/systems.json: token 'trade' is listed only under systems.unresolved (why: GRADING_RULE.md V1 lists it as a PRODUCT, but no DIRECTIVES.yaml line and no mission-tree project names its owner, so owner_directive cannot be written (row LGIC_ENFORCE-W1-S6)); no promoted row exists under systems.systems[] to give it a class/long/owner_directive",
   "step": "R1.c",
   "class": "RAISE",
   "detail": "R1.c: 'trade' is an unresolved token (V2)"
  },
  {
   "name": "vpc-flow-logs-role",
   "missing_row": "infra/logic/registry/systems.json: no row anywhere for token 'vpc' -- absent from systems[], unresolved[], and refused_keys.{workstream_code,generic_noun,purpose_word}",
   "step": "R1.f",
   "class": "RAISE",
   "detail": "R1.f: 'vpc' is in no vocabulary; no registry row resolves it"
  }
 ]
}
```

## Not done, by the order's bounds

No live pull; no edit to `GRADING_RULE.md`, `NAMING_SCHEMA.json`, or any `infra/logic/registry/*.json` file
(BOUNDS: "the registry is NOT yours"); no system guessed for any `{system}` gap or unresolved token
(CLAUDE.md Rule 30); the negative-control name is a planted string used only in-memory against `grade()`,
never written into any live or tree artifact.
