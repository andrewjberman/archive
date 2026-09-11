# IB-s-13 RESULT -- the narrative packet, and the shared layer that closed row W4-S3 in the world

TO: `IRPT_BCKEND.TO-IB-s-13`
(`org/missions/D9/IRPT/IRPT_BCKEND/task-orders/IRPT_BCKEND.TO-IB-s-13.narrative-events-dated-evidence-contemporaneity.md`)
Worker: `0.9.0_WK_IRPT_BCKEND~4` | Branch: `wk-irpt_bckend-1-4` | Worktree: `/c/tmp/wk-irpt-1-4`
Cell: `IB-s-13` (PRD row B13, FWD-8 contrib) | Fabric: laptop | Date: 2026-09-10/11

## 1. WHAT IS BUILT

**`infra/aws/lambda/investor-reporting/narrative/`** -- `events.py` (event detection on the
verified daily cumulative TWR, three refusals), `evidence.py` (dated topic evidence,
READ-ONLY, future excluded by date, syndication deduped, missing history distinguished from
an empty list, timezone verified from the producer's own bytes), `prose.py` (a deterministic
template and the validator that decides whether it ships), `handler.py`, `event_policy.json`
(the declared, versioned materiality policy), `fixtures/` (four files), `tests/` (37 offline
tests). **`infra/aws/terraform/investor-reporting/narrative/`** -- `main.tf` completed,
`iam.tf` (one role, READ-ONLY on the news plane with a named NOT-GRANTED list), `lambda.tf`.
**`infra/aws/lambda/layers/irpt-common/`** -- the shared layer and its reproducible build.
**`infra/aws/terraform/investor-reporting/performance/layers.tf`** -- the layer version,
declared in the root that owns its first consumer.

## 2. ACCEPTANCE

### S13-AC1 -- PASS by output (8 of 8 arms)

`timeout 600 python org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~4/battery_ib_s_13.py`
-> rc=0, final line `IBS13-NARRATIVE-DETERMINISTIC`. Transcript committed as
`IB-s-13_S13-AC1_battery_output.txt`. Deciding numbers, each beside its denominator:

- **(a) DETERMINISTIC.** 92 points in against a declared daily denominator of 92; 9 events;
  run-to-run event diff **0 entries** and the whole packet byte-identical under
  `json.dumps(sort_keys=True)`. 5 drawdown episodes found, 2 material; 35 raw movement
  windows merged to 4, so the merge **collapsed 31** -- exercised on real data rather than
  asserted. CONTROL: the same detector handed the 14-point 7th-of-the-points curve returns
  `REFUSE_DOWNSAMPLED`.
- **(b) THE FUTURE IS EXCLUDED -- the difference control.** The future-dated item is
  `EXCLUDED_FUTURE` with its published instant printed beside the cutoff, and **0 of 1**
  future ids reach the prose. Moving the cutoff to 2026-12-31 makes the SAME code admit the
  SAME article (1 -> 0 excluded), so the exclusion is a decision and not an accident of the
  fixture. 1 undated item is `EXCLUDED_UNDATED`, never assumed contemporaneous.
- **(c) MISSING HISTORY IS AN ANSWER.** Against a store whose bounds are
  `['2026-10-01', '2026-10-07']`: **9 of 9 windows uncovered**, `missing_history =
  MISSING_HISTORY`, the reason names both the window and the bounds, and the prose carries
  the words MISSING HISTORY. The covered store renders `NONE` at 9 of 9 -- the contrast is
  printed, so the arm is not satisfied by a constant.
- **(d) THE TIMEZONE IS VERIFIED FROM THE PRODUCER.** 6 of 6 timezone facts cited to
  `file:line` and printed with their source lines: the table's `date` partition is a UTC
  calendar date (`news_layer3_curation:2256`), `created_at` is an explicit UTC instant
  (`:1908`), the S3 archive PATH date is the writer's **naive local clock**
  (`news_trending_analysis:1366`), the only timezone-bearing stamp inside the archive is UTC
  (`:1167`), a naive article stamp is assumed UTC by the producer itself (`:334`), and **ET
  is established nowhere**, so the packet says UTC. Per-item basis over the window:
  47 `EXPLICIT_OFFSET`, 1 `UNDATED`. LIVE READS: DynamoDB **5,156 items over 289 distinct
  dates, 599 in the last 30 days**; S3 **696 objects** (695 dated + `latest.json`).
- **(e) SECONDARY SIGNALS GATED; SYNDICATION DEDUPED.** **1 of 4** signals admitted; the
  three refusals each name what they lack (a `CURRENT` value state, a missing `observed_at`,
  a missing `universe`). **72 syndicated copies** collapsed across the 9 event windows, and
  evidence ids are **48 of 48 unique** in the window.
- **(f) CONTEMPORANEITY, NEVER CAUSE.** 1 of 1 contemporaneous sentence ACCEPTED; **3 of 3**
  causal phrasings REJECTED with the pattern named (`because`, `drove / driven by`,
  `in response to`). The shipped prose: VALIDATED, contemporaneity true, causation false,
  citations **45 of 45** resolved, 0 unknown, every cited id inside the admitted set.
- **(g) SCHEMA-VALID, READ-ONLY, LEDGER CLOSED.** The packet validates in the worktree AND
  on the deployed function. **0 of 10** probed write/secret/model actions appear in
  `iam.tf` (comment lines excluded, so the NOT-GRANTED list cannot be miscounted as a
  grant); the store seam refuses a write; `irpt-narrative` CodeSha256
  `nuMb7eMlN8ou41LSSUOsUDR8T5U5uilo7N1XUcwU1IQ=` equals the built zip; ledger CLOSED.
- **(h) THE SHARED LAYER (issuer amendment, row W4-S3).** 6 of 6 requested helpers emitted
  from pin `3788926beb`, plus 3 constants and 1 import; `_request`, the session chain, the
  S3 writer and the import-time boto3 clients NOT carried. **2 of 2** functions carry
  `irpt-common:2`. **2 of 2** deployed invokes -- one per provider -- return
  `contract_validated=true` with **0 helper-degraded cells** (IB-s-11 shipped 1).

### S13-AC2 -- PASS by output
`timeout 120 .tools/terraform.exe -chdir=infra/aws/terraform/investor-reporting/narrative plan -no-color -input=false -lock=false`
-> rc=0, `No changes. Your infrastructure matches the configuration.` Run after the apply
(5 added, 0 changed, 0 destroyed) and after the ledger closed.

### S13-AC4 -- PASS by output
`timeout 120 .tools/terraform.exe -chdir=infra/aws/terraform/investor-reporting/performance plan -no-color -input=false -lock=false`
-> rc=0, `No changes. Your infrastructure matches the configuration.` Run after the layer
apply and after the layer ledger closed.

### S13-AC3 -- JUDGMENT, RECORDED, NOT SELF-GRADED
Output at `S13-AC3_judgment.md`. Headline findings: usable history is **2025-11-21 ..
2026-09-10, 289 of 294 calendar days, 5 absent in 3 named runs** -- 9.7 months against the
brief's "almost a full year", short at the OLD end, and the table reaches 10 days further
back than the S3 archive. The prefilter archive is **NOT** the final Topic Cloud, and the
final Topic Cloud **has no dated history at all** (722 keys under `json/sentiment/`, exactly
2 top-level files, one overwritten-in-place Topic Cloud object). Four places a reader still
reads causation are named, none of which the sentence-level validator can reach.

## 3. CONTROLS

**Mutant.** Five difference controls, each required to fail: the downsampled curve
(`REFUSE_DOWNSAMPLED`); the moved cutoff, which makes the same code admit the same future
article; a store whose bounds postdate every window (MISSING_HISTORY at 9 of 9 against NONE
at 9 of 9); three causal paragraphs (all REJECTED, each with its pattern named); and the
socket positive control, which moved the vendor counter 0 -> 1 so the zeros are measured.
All five fired.

**Determinism.** The battery was run twice end to end and the transcripts diff to **0
lines** -- including the live DynamoDB, S3 and Lambda reads. The layer build was run twice
and the zips compare byte-identical (`cmp` clean), which is what makes its digest
re-derivable from BUILD_MANIFEST rather than only recorded by it.

## 4. THREE DEFECTS THIS CELL FOUND IN ITS OWN WORK, AND HOW EACH WAS CAUGHT

1. **An evidence-id collision.** `evidence_id` keyed on the TOPIC headline, so two different
   articles under one topic row were minted the same id while the dedupe (keyed on the
   ARTICLE headline) correctly kept both. 48 candidates, 46 ids. Caught by a test asserting
   ids are unique across candidates. The key is now the article headline, url and source.
2. **A layer build that was not reproducible.** Three builds, three digests. The mover was
   pip's Windows console-script launcher and the dist-info RECORD line that hashes it --
   both excluded, both recorded in `excluded_members`.
3. **An assembled module that parsed and could not import.** The AST closure carried
   functions and constants but not module-level IMPORTS, so `bd_helpers` raised
   `NameError: name 'os' is not defined` at `/opt/python/bd_helpers.py:21` on the runtime.
   `compile()` passed it. Caught only by invoking the DEPLOYED function -- and only on the
   Black Diamond path, because the Orion path never loads those helpers: **one provider read
   green on a layer that was broken for the other.** The fix is the closure AND the
   falsifier: the build now execs what it generated in a clean namespace, so a missed member
   fails the build instead of the deployment. Filed as `IRPT_BCKEND-W4-S7`.

## 5. SURPRISE ROWS FILED UNDER THIS CELL

`IRPT_BCKEND-W4-S5` OBSERVATION / INERT -- arm (h)'s clean-Python import of `jsonschema`
cannot succeed on a Windows build host, and that is BECAUSE the layer is correct: its one
native member is `rpds.cpython-312-x86_64-linux-gnu.so`. The runtime import is proved by the
two deployed invokes instead; both readings are printed.

`IRPT_BCKEND-W4-S6` OBSERVATION / INERT -- the amendment names two missing dependencies;
there is a third (the contract SCHEMA FILE), and `jsonschema` alone would not have moved the
arm. The layer carries the contracts and `normalize.py` resolves env -> layer -> repo by
presence of the file, repo last and unchanged.

`IRPT_BCKEND-W4-S7` OBSERVATION / INERT -- the NameError above, the single-provider green,
and the non-reproducible build, with the build-time falsifier that now catches the class.

`IRPT_BCKEND-W4-S8` OBSERVATION / INERT -- `.tools/aws` cannot be spawned from a Windows
Python (`WinError 193`); `.tools/aws.cmd` via `cmd /c` is the usable face of the same shim.

## 6. BOUNDS HELD

No live Black Diamond, Orion or YCharts call (0 vendor connections, positive control live).
**No external model API call** -- the prose step is a deterministic template and the packet
says so in `versions.model_version`; 0 model-host connections, and the role carries no
`bedrock:` action. No monitor, alarm, SNS topic or SES send. No schedule and no event source
on either function. The news producers were READ and are unchanged; the role carries no
mutating action on either table or the archive bucket. No credential in any artifact or
fixture; the committed topic fixtures are public news headlines, sources and URLs with no
client identifier, account number, position or firm name. No served output touched: the
narrative apply was 5 added / 0 changed / 0 destroyed, and the only destroy in the whole
cell was `irpt-common:1`, created minutes earlier by this same cell. Deploys via
`.tools/safe-apply.sh` with `.tools/terraform.exe` by path, under two ledger entries opened
before the acts and closed after, with both sentinels committed and then removed by the
closes. Scratch confined to `/c/tmp/wk-irpt-1-4/.scratch/`.
