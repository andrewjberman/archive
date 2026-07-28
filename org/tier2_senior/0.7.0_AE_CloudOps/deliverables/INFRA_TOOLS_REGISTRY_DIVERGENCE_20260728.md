# One Declaration, Three Registries, Three Different Answers -- the mdpf deploy surface

**Author:** `0.7.0_AE_CloudOps~C` | **Date:** 2026-07-28 | **Mission:** `INFRA.TOOLS`
**Dispatch:** `1.0.0_SA_CTO` 20260728T201342Z item (1) -- land the findings before touching IAM.
**Status:** FINDINGS ONLY. **Nothing patched.** No registry edited, no tool edited, no apply.

---

## Why this document exists

Andrew's ask was *"make sure MDPF is added to the pipeline map."* Two AE sessions have now
independently concluded that executing that sentence literally would make it **true on paper and
false in the estate**. This is the grounded reason why, plus three further divergences found while
establishing it.

**The unifying defect, stated once:** the mdpf code-deploy surface is described by **three separate
machine-readable authorities**, each of which **restates the layout at its own call site** instead of
deriving it from one declaration. All three are currently wrong, in three *different* ways. That is
the same root as the row-13 per-source grammar ruling (154511Z) and the roster-derived freshness
ruling (171123Z) -- **derive from one declared authority, never restate at a call site** -- and this
is its third live instance.

---

## The live ground truth (measured 2026-07-28 ~1840-1850Z)

```
s3://opal-data-mdpf/code/          PRE backfill/  PRE diag/  PRE scripts/
                                   mdpf-daily-dispatch.sh   32077 B   2026-07-23 06:55
s3://opal-data-mdpf/code/scripts/  assets_gold/ backfill/ bronze/ feeders/ gold/ silver/   <- SIX
repo data/mdpf/scripts/            backfill/ bronze/ feeders/ gold/ probes/                <- FIVE
```
Deployed dispatch `:125`: `s3 sync "s3://${MDPF_BUCKET}/${CODE_PREFIX}/scripts/" "$SCRIPTS_DIR/" --delete`

**Per-layer `.py` census under `code/scripts/`. DENOMINATOR = 28.**

| layer | `.py` | seen by `comp-pipescript deployed`? |
|---|---:|---|
| gold | 14 | yes |
| backfill | 6 | yes |
| feeders | 3 | yes |
| bronze | 1 | yes |
| **assets_gold** | **3** | **NO** |
| **silver** | **1** | **NO** |

---

## F-1. `mdpf`'s absence from `PIPELINE_MAP` is a DOCUMENTED DECISION, not an oversight

`.tools/safe_deploy_core.py:22-26` carries exactly three entries -- `black_diamond`, `inf`, `cot`.
`file_to_s3_target` (`:91-118`) emits `code/<layer>/` with **no `scripts/` segment**; `VALID_LAYERS`
(`:29`) is `{gold, silver, bronze}`.

The exclusion is deliberate and the reason is recorded. `org/modules/graph/pipeline_cli.py:54-60`,
verbatim:

> *"mdpf is appended as a CHECK-ONLY tree: it is **deliberately NOT** in the deploy-gate PIPELINE_MAP
> (Rule 13 = bd/inf/cot; mdpf deploys via its own mechanism and uses a non-standard,
> internally-INCONSISTENT S3 layout -- **both `code/<layer>/` and `code/scripts/<layer>/` exist on
> opal-data-mdpf, so it cannot live in `file_to_s3_target`'s single-layout derivation**).
> comp-pipescript STILL checks its deployed status because MDPF_COUNTS (2026-06-05) proved an mdpf
> script can strand stale on S3 -- the exact blind spot this TO closes."*

**Two sessions re-derived that reason from scratch today because the comment lives in the tool that
worked around it, not in the map that excluded it.** The record was correct and unfindable.

**What actually follows -- and it is worse than an omission:** the comment names a *constraint*
(`file_to_s3_target` is single-layout) and **nobody ever removed the constraint.** The tree was
excused from the gate instead. **`mdpf` has a checker and no deploy path.** `comp-pipescript deployed`
can tell you an mdpf script is STALE and there is no sanctioned mechanism to deploy it.

> **CTO ruling 201342Z, accepted:** this moves the item from *"add mdpf to PIPELINE_MAP"* (closes the
> instance, leaves the class open) to ***"the single-layout constraint in `file_to_s3_target` is the
> actual blocker."*** That is the Rule-12 class. Do not paper it.

**Why a naive registration is affirmatively harmful, not merely useless:** `data/mdpf/scripts/gold/x.py`
would resolve to `code/gold/x.py` while the runner reads `code/scripts/gold/x.py`. It would *resolve*,
*satisfy the gate*, and *point at a key that does not exist* -- and a `safe-deploy` upload would land
artifacts at a prefix the runner never reads. **A deploy that reports success and changes nothing:
the TRUE-BUT-NOT-LIVE class, re-created inside the tool built to detect it.**

---

## F-2. `comp-pipescript`'s mdpf override hardcodes FOUR layers against SIX live

The workaround at `pipeline_cli.py:1814-1820` is the **right shape** -- a per-tree override declaring
mdpf's own bucket and layer vocabulary. It is the in-house precedent for the schema change. **But its
layer list is hand-maintained and has drifted.** `pipeline_cli.py:1915`:

```
"DEPLOYED STATUS [mdpf]: local repo vs s3://opal-data-mdpf/code/scripts/{gold,backfill,feeders,bronze}/"
```

Corroborated by the path regexes at `:297` and `:345`, both `(?:gold|silver|bronze|backfill|feeders)`
-- **no `assets_gold`** -- and by the sweep's own output, which emitted `[mdpf:gold]`,
`[mdpf:backfill]`, `[mdpf:feeders]`, `[mdpf:bronze]` and nothing else.

**4 of 28 `.py` files are structurally invisible. Named:**

```
code/scripts/assets_gold/build_dim_model_portfolio.py     18963 B   <- STAGE 6. Fails rc=1 daily.
code/scripts/assets_gold/build_cottonwood_mdpf_pair.py    23543 B   <- cottonwood
code/scripts/assets_gold/build_cottonwood_mdpf_slice.py   19203 B   <- cottonwood
code/scripts/silver/rebalancer_schemas.py                 12553 B
```

>> **The tool built specifically to catch a stranded mdpf deploy -- commissioned after MDPF_COUNTS
> proved that exact failure -- cannot see the Stage-6 script or either cottonwood script.** Its
> four-layer list was correct when four was the answer; `assets_gold/` arrived later and the
> hand-maintained enumeration did not follow. <<

**This is another cottonwood omission, and its lineage matters more than its ordinal.** Prior
mechanisms on the same victim: the legacy 2-partner producer cannot emit it; `fact_holdings` stalled
07-24; the OAC allowlist omits its two served keys; no freshness cohort (and then no freshness Lambda
at all); and AE-base's `|| return 1` short-circuit at `:523`, which meant the two cottonwood emitters
never ran. **This one is distinct from all of those in a way worth stating: it is in the
DETECTOR.** *(Ordinal collision with AE-base's find is acknowledged and deliberately not
reconciled -- CTO 201342Z. The count was never the finding.)*

**Not patched, on purpose.** Adding a fifth string to that list rebuilds the defect with one more
member and guarantees the seventh layer repeats it -- CTO's own 171123Z ruling on the freshness
cohort table, applied to its sibling.

---

## F-2b. The SAME script reads MATCH or invisible depending on how you spell its name

`0.4.0_DS` logged this tool today as *"GAP -- mdpf tree UNCOVERED, reported as 0 MATCH/0 STALE/0
MISSING (clean-looking summary for a tree it cannot see)"* (`org/compiler-tools-log.md`, 2026-07-28).
**That contradicted my no-arg sweep, which covered mdpf.** Both reports are correct. Reconciled by a
discriminating pair, run minutes apart on the same script:

```
A  comp-pipescript deployed dim_mdpf_aggregate_aua_timeseries.py            <- bare filename (DS's form)
   DEPLOYED STATUS: local repo vs s3://opal-data-bd/code/{gold,silver,bronze}/     <- THE BD TREE
   Summary: 0 MATCH, 0 STALE, 0 MISSING_ON_S3, ... 0 UNCOVERED       rc=0
   "No scripts matched filter: 'dim_mdpf_aggregate_aua_timeseries.py'"

B  comp-pipescript deployed data/mdpf/scripts/gold/dim_mdpf_aggregate_aua_timeseries.py   <- path form
   DEPLOYED STATUS [mdpf]: local repo vs s3://opal-data-mdpf/code/scripts/{gold,backfill,feeders,bronze}/
   [mdpf:gold] dim_mdpf_aggregate_aua_timeseries.py    MATCH
   Summary: 1 MATCH, ... 0 UNCOVERED                                 rc=0
```

**MECHANISM, source-confirmed at `pipeline_cli.py:1773-1785`** (not inferred from the output): the
path auto-detect routes a filter only when it contains a **path** -- `f"data/{_dir}/scripts/" in _np`
or `_np.startswith(f"data/{_dir}/")`. A **bare filename matches no directory** and falls through to
`:1785` `pipeline = 'bd-gold'`. The comment at `:1777` acknowledges the fall-through as intentional
and backward-compatible for bare bd ids like `D_00`. **For a non-bd script the same fall-through
produces a confident answer about the wrong tree.**

**To be fair to the tool: it is not silent.** It prints `No scripts matched filter: '<name>'`. The
defect is that **three signals disagree and two of them say "fine"**: the header asserts it searched
`opal-data-bd`, the summary reads all-zeros **including `0 UNCOVERED`**, and `rc=0`. A reader
reasonably concludes *"this script is not deployed anywhere"* rather than *"you named a tree I did
not search."*

>> **The `uncovered` list at `:1929` is documented as the "TOOL-03 false-clean guard: tool-blindness,
> named -- NEVER silent." It reports `0` here.** The guard cannot fire, because the script was never
> admitted to any tree's population -- **it was excluded before the thing that counts exclusions ran.**
> A guard that sits downstream of the routing it is meant to protect against is not a guard. <<

**Consequence, and DS already named it:** this reads green while a deployed producer is stale. DS's
log says it *"would have read green for 7 days while the deployed producer was 4 days stale."*
**Two agents, two invocation forms, two opposite verdicts, same tool, same day, both rc=0.**

---

## F-3. `EC2_MANIFEST.code_prefix` is one segment too coarse to address the code tree

`infra/aws/ec2/EC2_MANIFEST.json`, `mdpf-daily-runner`:
```
"code_prefix": "s3://opal-data-mdpf/code/"
```
**Not false** -- `dispatch_script` genuinely lives at `code/mdpf-daily-dispatch.sh`. But
**non-discriminating**: `code/` holds a shell script at depth 1 and six layer directories at depth 2,
so no consumer can derive a *script* deploy target from it.

**`PIPELINE_MAP` drops the `scripts/` segment; `EC2_MANIFEST` stops short of it; `pipeline_cli` gets
it right and then under-enumerates the layers. Three authorities, three granularities, one tree.**

---

## F-4. The Rule-8 source of truth asserts a cron that DOES NOT EXIST

`EC2_MANIFEST.json` `mdpf-daily-runner.cron_schedule`, verbatim:
> *"The ONLY mdpf cron is mdpf-freshness-check-trigger (cron(45 16 * * ? *)) = the freshness ALARM,
> not the dispatch."*

**Applied plane, measured:**
```
aws events list-rules --name-prefix mdpf
  -> mdpf-daily-refresh-trigger | ScheduleExpression None | ENABLED     (that is ALL)
aws lambda list-functions | mdpf
  -> mdpf-daily-trigger, opal-assets-mdpf-portal-publisher
```
`mdpf-freshness-check-trigger` **does not exist.** Third independent confirmation that the freshness
instrument is a document -- CVO's morning measurement, AE-base's 17:23Z `ResourceNotFoundException`,
and now the EventBridge rule itself absent.

**The new part is WHERE the false claim lives:** not in a code comment but in the Rule-8 source of
truth, in the `cron_schedule` field, on the runner at the centre of today's P0. Under Andrew's ~1725Z
ruling (*canonical routes and schedules first*) this is route-and-schedule work, not monitoring: **the
record says this runner has a cron; it does not.**

**Not corrected, pending CTO.** Writing *"no cron"* today would be true and would still describe a
topology we intend to change. Flagged for a decision, not silently fixed.

---

## F-5. Rule-12 coverage floor -- the denominator AE-base declined to guess

PREDICATE: every entry under `services{}` in `EC2_MANIFEST.json`. **DENOMINATOR = 27.**

```
deploy_mechanism   22/27 present:  s3-pull-runtime 8 | pre-manifest-era-unknown 6 | s3-ssm 4
                                   s3-pull-launch 2 | windows-scheduled-tasks 1 | ssm-operator-scripts 1
                    5/27 ABSENT
code_prefix         4/27 present:  inf-bronze-runner, mdpf-daily-runner,
                                   canonical-schwab-runner, opal-website-wp
NEITHER field       5:  consolidation-gold-runner, orion-crawl-harness, astn-wsjft-scraper,
                        bd-49f-auto-login, m365-mcp-gateway
```

**23 of 27 carry no machine-readable S3 code prefix; 11 of 27 have a deploy mechanism absent or
recorded literally as `pre-manifest-era-unknown`.**

**This is a COVERAGE FLOOR WITH ITS PREDICATE STATED, not a defect rate.**
`pre-manifest-era-unknown` is an honest label rather than a finding, and some entries may be
legitimately code-free. **Do not extrapolate a rate from it** -- the sample was not drawn to support
one.

---

## A live parallel-channel instance (DEBT.BACKEND shape)

Two `backfill/` prefixes under one code root:
```
code/backfill/          1 file, build_mdpf_wsc_inflection_nonmodel_backfill.py, 2026-05-28
                        -> the dispatch's --delete sync covers code/scripts/ ONLY. Unreachable orphan.
code/scripts/backfill/  build_aggregate_aua_timeseries.py  32715 B  2026-07-02   <- the LIVE ROLLUP
```
**This pins the open handoff item:** the ROLLUP that "still logged 2 partner(s)" is
`code/scripts/backfill/`, deployed artifact dated **2026-07-02**. DS's fix went to
`code/scripts/gold/` -- a different directory. *The chain ran; the product is not fixed.*

---

## Recommendation (AE; the architecture call is CTO's)

**One declaration, three consumers.** `PIPELINE_MAP`'s `dir -> (bucket, label)` becomes at minimum
`dir -> (bucket, label, key_prefix, layers)`, so a tree declares its own prefix and its own layer
vocabulary; `EC2_MANIFEST.code_prefix` and `pipeline_cli`'s mdpf override both derive from it rather
than restating it.

**The mutant that must fail loudly is not hypothetical:** *a tree whose declared layer set is missing
a layer that exists live.* That is `assets_gold/` today. A schema change that would not have caught
F-2 has not fixed the class.

This touches a shared gate that bd/inf/cot all depend on, so it wants its own plan, its own tests, and
its own apply. **Nothing landed.**

---

## Compiler Tools

| Tool | Where | Result | Note |
|---|---|---|---|
| `comp-pipescript deployed` (no-arg sweep) | all trees | rc=0 -- 18 MATCH, 3 STALE, 7 MISSING_ON_S3, 0 UNCOVERED | **Ran >4 min emitting ZERO bytes before completing.** See O2 note below. Its mdpf coverage is real but 4-of-6 layers (F-2). |
| `comp-grep` | `.tools/`, `pipeline_cli.py` | 0 matches for `code/scripts` across 246 files | A true zero -- the tool states its own working set, which is why the zero was trustworthy enough to act on. It correctly reported `scanned 0 file(s)` for a path that does not exist, instead of a bare 0. |
| `comp-which` rail | raw `aws` inspections | 4 calls carried `# rail-checked:` markers | Each because the routed tool structurally could not answer: comp-pipescript **omits the two layers I was measuring**, and comp-aws/comp-iam model DESIRED, not the applied plane a suspected-stale-record question turns on. |
| `comp-iam` | NOT used | n/a | Models `(action)` never `(action, resource)` and fails GREEN. Nothing here was an IAM question. |

**INFRA.TOOLS.O2 datapoint (the mission's own subject).** `comp-pipescript deployed` emits nothing
until complete -- >4 minutes of silence, then a full report. **I read that silence as a possible hang
and said so to CTO before it finished; it was fine.** I reasoned from a partial retrieval inside a
report about the danger of partial retrievals. Corrected within the hour (msg `184924Z`). **The
instrument defect is real and narrower than I first said: not "it breaks", but "it has no progress
contract, so silence and failure are byte-identical to the caller."** That is exactly O2's frontier --
a per-tool output contract that says *"there is more"* rather than saying nothing.

## Method note

Every claim here is measured on the plane it is about: registry contents from source at HEAD with
line citations, S3 layout from live listings, the absent cron from `events list-rules` on the applied
plane. **F-1's "documented decision" reading is the one that changed the shape of the work**, and it
was only available by reading the tool that worked *around* the map rather than the map itself -- the
same deployed-vs-repo ordering error AE-base bound as a rule at 17:23Z, avoided here by reading first.

---
---

# PART II -- THE FIX, AND THE 22-OF-27 CENSUS

*Appended 2026-07-28 ~2115Z by `0.7.0_AE_CloudOps~C`. CTO rulings `203649Z` (one plan, all three, or
none) + `204943Z` (proceed; PROVE the invariant) + `204454Z` (the trigger-field ruling).*
*Landed `85a64cada` + `d11b98e2ae`. Tooling + tests only -- no deploy, no apply, no IAM.*

## F-6. NAMED FINDING, independent of any fix: ONE S3 CODE TREE IS FED BY TWO REPO TREES

Recorded on its own because the next person needs it whether or not they touch `CODE_TREES`.

```
s3://opal-data-mdpf/code/scripts/assets_gold/  <-  data/assets/scripts/gold     NOT data/mdpf/
s3://opal-data-mdpf/code/scripts/silver/       <-  data/assets/scripts/silver   NOT data/mdpf/
```

**Two consumers hardcoded the false assumption that a repo home is derivable from the tree name**
(`data/<tree>/scripts/<layer>/`): `safe_deploy_core.file_to_s3_target:97-118` and `pipeline_cli:1944`.
**A layer LIST cannot express this shape.**

>> **AND THIS IS WHY THE OBVIOUS FIX WAS THE MUTANT.** The literal reading of *"correct the layer
> count"* -- add `assets_gold` and `silver` to the `:1945` tuple -- globs a nonexistent
> `data/mdpf/scripts/<layer>/`, hits `:1947 if not _ldir.is_dir(): continue`, and **skips both
> silently.** Same clean summary, same `rc=0`, same `0 UNCOVERED`, now with a layer list that *looks*
> complete. **It converts a VISIBLE 4-vs-6 gap into an INVISIBLE one** -- the precise outcome the
> one-plan ruling was issued to prevent, reproduced by the fix for it. <<

## The fix: one declaration, three consumers derive

`safe_deploy_core.CODE_TREES` -- per-`(tree, layer)` to `(repo_home, s3_prefix)`, plus `deploy_gated`,
`shared_repo_homes`, and `artifacts`.

| registry | BEFORE | AFTER |
|---|---|---|
| `safe_deploy_core` | 3 trees x 3 layers = **9 cells**; mdpf **inexpressible (0)** | **4 trees** (3 gated + 1 check-only) = **15 cells**; mdpf = **6** |
| `pipeline_cli` mdpf sweep | **4 layers hardcoded / 6 live** -- 4 of 28 `.py` invisible | **6 derived / 6 live** -- **0 invisible** |
| `EC2_MANIFEST.code_prefix` | depth-1 `code/`, non-discriminating | `code/scripts/` + separate `dispatch_script_prefix`, **pointing at `CODE_TREES`** |

**The Rule-13 deploy gate is UNCHANGED, and that is test-proven rather than asserted** --
`PIPELINE_MAP` = `{black_diamond, cot, inf}`, `VALID_LAYERS` = `{bronze, gold, silver}`.

**`mdpf` is `deploy_gated: False`.** Registering it as gated would silently begin uploading on DS
pushes -- a live-behavior change nobody authorized, on the lane boundary Rule 13 polices. This is the
**declared-UNKNOWN sentinel applied to gate membership**: *"mdpf has no deploy path"* becomes an
auditable one-line fact instead of an absence nobody can query. **That decision is CTO's and remains
OPEN.**

**Fail-loudly, the load-bearing line:** a declared layer whose `repo_home` does not exist is a
**DECLARATION DEFECT** and surfaces as `UNCOVERED` -- never `continue`. The check sits **upstream of
the skip**, which is the only place it can fire. **This is the fix for F-2b's `:1929` defect** -- a
guard downstream of the routing it audits cannot see what the routing dropped.

**No fallback copy of `CODE_TREES` in `pipeline_cli`** -- a hand-maintained duplicate is exactly the
divergence this table ends. On import failure it reports `UNCOVERED` loudly rather than guessing.

## A false-positive class I INTRODUCED, and caught before shipping

`data/assets/scripts/{gold,silver}` serve multiple destinations: only **3 of 7** and **1 of 13** deploy
to mdpf's tree. Naively mapping the whole directory emitted **~16 false `MISSING_ON_S3` rows.**
**A sweep with more false positives than findings trains people to ignore it -- the same end state as
the blindness it replaced.** `shared_repo_homes` reclassifies "absent on S3" as `not-in-tree`
(informational); `STALE`/`MATCH` still bind and the `UNCOVERED` direction is untouched.

## Non-script artifacts (AE-base `210149Z`, measured)

The dispatch syncs `code/scripts/` **with `--delete`**; the tree holds 34 objects and
`partner_roster.json` is **ABSENT**. A cross-tree import RAISEs, a repo-relative read fail-closes, and
**`--delete` silently reverts a hand-placed copy.** A model knowing only `.py` excludes the class, and
the next person solves it with a one-off `aws s3 cp` the following sync undoes. `artifacts` now models
it; `s3_key: None` = **declared, target unresolved** -- the destination is a real decision and
inventing it here would be the call-site literal this table abolishes.

## Verification

**14 cases, `.tools/test_code_trees_invariant.py`.** Expected values are a **FROZEN LITERAL FIXTURE**
transcribed from `safe_deploy_core.py:22-29 @92e41ad1b3` -- *a fixture computed from the code under
test cannot detect that code changing.* Pre-existing `test_safe_deploy.py`: **14/14, no regression.**

**Mutants exercised against the SOURCE FILE, both directions reported:**

| mutant | result |
|---|---|
| **A** `cot` bucket to `opal-data-bd` (firm-separation breach) | **4 of 11 FAIL**, incl. byte-identity + bucket-collision |
| **B** `assets_gold` repo_home to `data/mdpf/scripts/assets_gold` (**exactly what the naive fix would have written**) | **1 of 11 FAIL**: "every declared repo_home exists on disk" |
| **C** rename the `artifacts` key | **1 of 12 FAIL**: "mdpf declares a non-script artifact class" |
| restore | byte-identical (`diff -q`), suite back to **14/14** |

## What the newly-visible layers found immediately

```
[mdpf:assets_gold] build_cottonwood_mdpf_pair.py    STALE
[mdpf:assets_gold] build_cottonwood_mdpf_slice.py   STALE
```
**Both cottonwood scripts are STALE on S3, and the tool could not see either until this commit.**
Reported, **not fixed** -- deploying them is a DS/CTO call, not a side effect of a tooling change.

## THE 22-OF-27 CENSUS (durable record, per CTO `204454Z`)

**PREDICATE:** any field whose NAME contains `cron`/`schedule`/`trigger`, OR whose VALUE contains a
`cron(`/`rate(` expression. **DENOMINATOR = 27 services**, verified against the **full 100-rule**
applied-plane EventBridge inventory -- *not* a name-prefix query, **which is how the phantom survived
a `--name-prefix mdpf` check for weeks.**

```
5 of 27 carry a schedule assertion:
  inf-bronze-runner        cron(30 13 * * ? *)            TRUE   opal-inf-bronze-runner-cron, ENABLED
  canonical-schwab-runner  canonical-schwab-xref-success  TRUE   present, ENABLED, no schedule
  cot-exporter             "cron(0 2) chain"              TRUE   cot-bd-session-daily
  mdpf-daily-runner        phantom                        FALSE  -> CORRECTED b17260251c
  bd-price-runner          sequence-position claim        NOT VERIFIABLE by list-rules -- left
                                                          UNVERIFIED, endorsed by CTO
```

>> **22 OF 27 SERVICES ASSERT NOTHING AT ALL ABOUT HOW THEY ARE TRIGGERED.** Not 22 defects -- some
> are ephemeral or manual by design, and **absence of a field is not absence of a schedule.** It is 22
> entries where the Rule-8 source of truth cannot answer *"what starts this, and on what cadence"*
> without a console trip. **An optional field cannot be audited for absence; only a required one
> can.** <<

**CTO RULING (`204454Z`), build routed separately -- NOT this session:** the trigger/schedule field
becomes **REQUIRED** in `EC2_MANIFEST.json`, **and** an explicit declared-unknown value is
**PERMITTED** (e.g. `{"mechanism": "UNVERIFIED", "measured_at": null}`). **Both halves, and the second
makes the first landable** -- requiring the field with no unknown-sentinel would break Rule-8 CI on 22
entries and force someone to guess 22 values under deadline, manufacturing exactly the false
assertions we just deleted one of. Precedent already ratified one tree over, in
`partner_roster.json`'s `gate_coverage`: *"A NOT_COVERED partner MUST be reported as UNMEASURED --
never omitted, and never counted as fresh. Not-knowing renders as an unknown, never as health."*

## My errors in Part II

1. **I shipped three tests that never ran.** The artifact tests were written and **not registered in
   `main_test()`**; the suite reported a clean `11/11` over a suite that never executed them. **I
   noticed only because I expected 14 and got 11.** A guard nothing invokes is not a guard --
   committed inside the change whose subject is guards that cannot fire, hours after writing up F-2b.
   **The COUNT caught it, not the result: a passing suite is silent about what it did not run.**
   Fixed, then exercised (Mutant C).
2. **My own earlier recommendation was wrong on the axis that mattered.** In `184924Z` I proposed
   `tree -> (bucket, label, key_prefix, layers)`. **A layer list cannot express two repo trees feeding
   one S3 tree** -- I would have shipped a schema that still could not describe the defect it was
   designed for. Corrected before writing code, not after.
