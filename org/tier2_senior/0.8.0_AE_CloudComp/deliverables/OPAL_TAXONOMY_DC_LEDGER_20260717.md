# OPAL_TAXONOMY — DEVIATION-CLASS (DC) LEDGER v0.1

**Author:** `0.8.0_AE_CloudComp~B` — OPAL_TAXONOMY DRIVER (Andrew-spawned 2026-07-17 ~18:5xZ; CTO founding brief).
**Project:** `org/projects/OPAL_TAXONOMY.json` (@567b4c374). **Owner (ruler):** `1.0.0_SA_CTO`.
**Routed to CTO for:** the ruling-20 per-DC disposition (migrate-now / migrate-at-next-touch / recorded-carve-out) + the standard-clause decisions flagged CLASS-X. **CTO rules; ~B builds the lints on the rulings.**

## Basis (what this ledger is built on)
- **Census:** `OPAL_CONSOLIDATION_TAXONOMY_CENSUS_20260717.md` **v0.1.2 @7d076fcfa** (`0.8.0_AE_CloudComp~C` — the FINAL measurement basis; DC-7 + DC-15 folded as scored rows, 16 classes), measured vs the standard. Both Phase-2 controls PASS (instrument discriminates). *(This ledger was first staged @6020a79c7 on v0.1.1 @7df414694; ~C's independent DC-7/DC-15 findings MATCH mine — corroboration, no rework. Rebased to v0.1.2.)*
- **Standard (authoritative HEAD):** `docs/architecture/OPAL_CONSOLIDATION_TAXONOMY_STANDARD.md` **@59805972b** — carries the SS-C **region co-location** clause (lines 61-65) landed AFTER the census basis. **The single gap between census-basis and standard-HEAD is DC-15**, added below.
- **Repo HEAD at authoring:** `d8eaf705e`. **READ-ONLY: zero remediation performed on any resource.** Two census residuals ground-truthed live this session (DC-5 tracking status, DC-7 sha-tie) — evidence inline, flagged for fold-back into census v0.1.2.
- **Handoff (proposed to ~C, 192426Z):** ~C = MEASUREMENT AUTHORITY (owns census + re-census verification); ~B = FORWARD DRIVE (this ledger + lints + sequencing + STNDRD fold). Neither both-runs-census nor both-builds-lints.

---

## CTO RULING-20 DISPOSITIONS (LANDED 2026-07-17 ~20:07Z) + W1 BUILD STATUS

CTO ruled the ledger (msg 200722Z). Live disposition + build state (this section is the living record; the per-DC analysis below is the original proposal):

| DC | CTO disposition | Build status |
|---|---|---|
| DC-1 `code/`/`_probe/` | **reserved-prefix BLESS** (`code/`,`_probe/`,`_ops/`,`meta/` = reserved system prefixes → CONFORM-BY-AMENDMENT; CTO amending SS-A) | ~C folds census; no lint |
| DC-2 `_ops` | **reserved-prefix BLESS** (as DC-1) | ~C folds census |
| DC-3 eclipse omits `{type}` | real DEVIATE → next-touch (producer) | W3 producer-code gate |
| DC-4 inline `_meta` | next-touch (producer) | W3 producer-code gate |
| DC-5 `org/mcp` spill | **HOOK-FIX** (telemetry hook absolute-path) + clear the 7-stray sweep; NOT the blind commit-lint | **CLOSED @b9c5f5243 (CTO lane).** Root cause: post-tool-telemetry.sh wrote repo-relative paths from the agent's cwd. Fix = ${ROOT} anchor. Positive-control PASSED (data/assets cwd → telemetry at repo root, zero spill); 7 strays swept (0 tracked touched). CTO committed canonical + reconciled the stale installed copy (bonus: closed the installed-vs-canonical jq-ladder sync gap). |
| DC-6 dual schwab home | next-touch, schwab-window-gated post-D4 | W4 |
| DC-7 landing_guard | canonical `data/assets/scripts/lib/landing_guard.py` + build-manifest sha-tie gate | W3 |
| DC-8..11 scheduler grammar | grammar-reconcile **APPROVED**; refined 3-check definition **BLESSED**; `fees-*-daily` DC-11 → `-weekdays` next-touch (DISABLED); enforce-flip design blessed | **BUILT + ENFORCE.** Reconcile @1ed893633 (153/154→11, 9 controls PASS); `--enforce-grammar` @e9b271291 (grandfather-pin 11, consolidation-scoped exit-2, estate-wide WARN, 9 enforce-scope controls PASS). WARN-FIRST — CI doesn't pass the flag yet (CTO's announce→enforce flip pending). |
| DC-12 absence twins | **DEFER** (Andrew alert-suspension); requirement stands, twin-BUILD held; emitter = CTO's candidate-exception surfaced to Andrew | HELD |
| DC-12b 3 mechanisms | ruled **YES** (bless all 3); gate enforcement defers with the suspension | HELD |
| DC-13 AL2023 + DC-15 region | **GO build-now**, WARN-first, + live AMI→OS resolver (APPLIED) | **BUILT @4ee2888e3** — controls PASS. `--enforce` already opt-in (WARN-first; AL2023 = fleet-wide SS-E, not consolidation-scoped, per CTO). CI flip pending. canonical-schwab rebuild post-D4. |
| DC-14 role infix | next-touch, schwab-window-gated post-D4 | W4 |

**A-axis (DC-1..4) = CLASS-D confirmed** (producer-code/CI, NOT runtime deny — 17a reasoning accepted). **ALERT-SUSPENSION (Andrew-direct 2026-07-17):** new twin/alarm creation paused for the consolidation → DC-12 build held (SS-D absence-twin enforcement footnoted paused @f9fdde92a).

**Sequencing now:** W1 remaining = the two enforce-flips (CTO word) + the 2 DC-8..11 decisions. W2 = reserved-prefix + DC-12b census folds (~C). W3 = DC-3/4/6/7 producer-code + at-touch. W4 = schwab-window-gated (post-D4 2026-07-24).

---

## FRAMING (read before the table — this is the driver's analytic layer over the census)

### Framing 1 — every DC is TWO decisions, ruled independently
For each deviation class:
1. **EXISTING instances** → migrate-now / migrate-at-next-touch / recorded-carve-out.
2. **The GATE** that prevents NEW instances → build-now or migrate-first-then-gate.

These are independent. A gate can be **build-now** even when existing instances are **carve-out** (the gate stops the estate from getting worse while the existing drift rides its natural touch). This is the "gate-what-you-measured, renames ride natural touches, never big-bang" mechanic made concrete.

### Framing 2 — enforcement-surface taxonomy (WHICH gates are safe to build-now)
The census's gate candidates are not uniform. They fall into four classes with **opposite** safety profiles — this is the single most important input to sequencing:

| Class | Where the gate lives | Safe to build-now? | DCs |
|---|---|---|---|
| **CLASS-D** — definition/provision path | commit-gate / TF-plan / build-manifest / trigger-map CI gate. Evaluates only NEW or CHANGED resource *definitions*. | **YES** — never touches a live resource; existing instances ride their next touch. | DC-6, 7, 8, 9, 10, 11, 13, 14, 15 |
| **CLASS-R** — runtime write path | S3 bucket-policy PutObject **deny**. Evaluates LIVE writes. | **NO** — a deny built before its producer is migrated **breaks the live producer** (the 17a-gate incident class). Migrate producer FIRST, then gate — OR re-express as a CLASS-D check on the producer *code*. | DC-1, 2, 3, 4 |
| **CLASS-X** — standard/structural question | no lint; a CTO ruling / SS-* amendment. | n/a | DC-12b, DC-12(silver-sweeps), DC-1(`_probe/`) |
| **CLASS-F** — filesystem hygiene, **gate-blind** | the deviation is UNTRACKED; a commit-gate never sees it. | census gate-candidate is **mis-targeted** — real fix = root-cause + a sweep. | DC-5 |

**Headline recommendation:** enforce **A-axis grammar (DC-1/2/3/4) at the producer-code / CI layer (CLASS-D), NOT a runtime bucket-policy deny (CLASS-R).** A runtime deny on `opal-data-assets` PutObject would reject the live writes of the very producers that currently write those keys (bd49f `_ops/`, eclipse bronze, the gold-runner `code/` deploy) — a self-inflicted outage. The producer-code check catches the same drift at the point it is introduced, without a live-write failure mode.

---

## THE LEDGER (DC-1 .. DC-15 + DC-12b)

Legend — **Disp** = proposed EXISTING-instance disposition · **Gate** = proposed enforcement + its surface-class + hook · all dispositions are **PROPOSED (CTO rules)**.

### Axis A — Bucket / prefix grammar (SS-A)

**DC-1 — Non-grammar / non-`{source}` root in the monolith**
- **Instances:** `s3://opal-data-assets/code/consolidation-gold/*` (3 keys: `run-gold.sh`, `setup-instance.sh`, `watchdog-shutdown.sh`); `s3://opal-data-assets/_probe/*` (22 keys, `_probe/{source}/{scope}/{layer}/{type}/{date}/grammar.probe`).
- **Disp (`code/`):** **migrate-at-next-touch** → move runner shell scripts to the dedicated `opal-runner-shared` bucket when the gold-runner deploy path is next revised (owner: CloudOps / runner lane). NOT now: the runner pulls these live; move + pull-path update must be lock-step.
- **Disp (`_probe/`):** **CLASS-X CTO ruling** → bless as a reserved test-scaffolding root (add an SS-A `_probe/` clause) **or** migrate-now-delete if debris. (22 keys of grammar-probe scaffolding; likely intentional but unstandardized — CTO decides bless-vs-delete.)
- **Gate:** prefix-lint "root ∈ enumerated `{source}` ∪ `{meta}`". **CLASS-R if runtime deny → build migrate-first, or re-express CLASS-D** as a deploy-path check (deny an `aws s3 cp` to a non-grammar root). build-now-safe **only** in CLASS-D form.

**DC-2 — Non-canonical `{layer}` token (`_ops`)**
- **Instances:** `s3://opal-data-assets/blackdiamond/49f/_ops/*` (5 keys: `probe/*.json`, `pull_state.json`).
- **Disp:** **migrate-at-next-touch** → bd49f pull code writes `blackdiamond/49f/meta/` on next revision. NOT now: `pull_state.json` is an **active** state file the pull reads/writes each cycle; an in-flight move risks the pull losing state.
- **Gate:** layer-token lint `{layer} ∈ {bronze,silver,gold,meta}`. **CLASS-R (runtime deny UNSAFE — the pull writes `_ops/` today).** Migrate-first-then-gate, or CLASS-D producer-code check.

**DC-3 — Per-feed grammar drift: `{type|feed}` segment omitted (eclipse)**
- **Instances:** eclipse feed `eclipse/inflection/bronze/{date}/model_composition_NN.json` (type encoded in filename, not a path segment). 1 feed.
- **Disp:** NEW writes → **migrate-at-next-touch** (eclipse producer writes `bronze/{type}/{date}/`). HISTORICAL eclipse bronze → **recorded-carve-out** (do NOT re-partition historical bronze — 17a bronze-immutability + re-partitioning is the big-bang we avoid).
- **Gate:** bronze key-depth==5 check. **CLASS-D producer-code check on go-forward writes** (build-now-safe). A runtime deny would reject historical-shaped keys too → unsafe.

**DC-4 — Pull-provenance written inline (`{date}/_meta/`) not `meta/pulls/{YYYYMMDD}/`**
- **Instances:** eclipse + blackdiamond write `{date}/_meta/pull_complete.json`. 2 feeds. (Cross-listed with A.2 inline-`_meta` + SS-D pull-provenance row.)
- **Disp:** **migrate-at-next-touch** (producer writes `meta/pulls/`). Historical → carve-out.
- **Gate:** provenance-path lint. **CLASS-D producer-code check** (build-now-safe).

### Axis B — Local repo `data/` tree (SS-B)

**DC-5 — Non-data subtree in the data tree (`data/assets/**/org/mcp/`)** — **CLOSED @b9c5f5243** (verified 2026-07-17 ~2205Z by 0.8.0_AE_CloudComp~B: canonical commit is an ancestor of origin/CLOUD AND on local HEAD, local<->origin in sync `0 0`; ROOT anchor present at line 41 `ROOT="${CLAUDE_PROJECT_DIR:-$(cd "${SCRIPT_DIR}/../.." ...)}"` + `.` fallback line 42; positive-control PASS; 7 strays swept, 0 tracked touched; CTO folded the stale installed `.tools/hooks` copy into the same commit, closing the pre-existing installed-vs-canonical jq-ladder sync gap). *Detail below is the pre-ruling grounding.*
- **Instances:** 7 files `data/assets/**/org/mcp/agent_telemetry/*.jsonl` (telemetry for `0.4.0_DS`, `0.6.2_AE`, `1.0.0_SA_CTO`, `0.4.0_DS~A`). **`git ls-files` → NONE TRACKED** — untracked filesystem spill only.
- **Root cause (grounded):** the agent_telemetry PostToolUse hook writes to a **relative** `org/mcp/agent_telemetry/` path; from a cwd inside `data/assets/scripts/...` it lands there instead of repo-root. Same class as the CLAUDE.md "lingering portal/ cwd is a defect" hazard.
- **Disp:** **migrate-now** — remove the stray `org/mcp` subtrees under `data/assets/` (untracked telemetry debris, zero data value). *(Removal of untracked files, not recursive-delete of a real resource — CTO clears the cleanup.)*
- **Gate:** **CLASS-F — the census's proposed commit-gate "no `org/` under `data/*/`" is STRUCTURALLY BLIND here** (untracked files never stage → the gate never fires). Real fixes: **(1)** telemetry hook writes an ABSOLUTE repo-root path (owner: hook owner); **(2)** a filesystem-hygiene sweep (rides `/kill storage` class or a periodic scan). **Census gate-candidate correction — surfaced, per driver duty to pressure-test a gate before building it.**

**DC-6 — Dual code home (`data/canonical/schwab/` + `data/schwab/`)**
- **Instances:** schwab converter code under two parallel homes.
- **Disp:** **migrate-at-next-touch** → consolidate to ONE canonical home when schwab converters next touched (owner: DS + 49-schwab-conv skill owner AE). **Proposed canonical = `data/canonical/schwab/`** (the "canonical" name), `data/schwab/` deprecated — **CTO/DS confirm which is canonical.** Repo refactor touches no schwab live data, so likely D4-window-safe (confirm w/ 0.5.0).
- **Gate:** deny NEW schwab `.py` under `data/schwab/` once canonical designated. **CLASS-D** (build-now-safe after designation).

**DC-7 — Vendored canonical copy without verified sha-tie (`landing_guard.py`)** — GROUNDED THIS SESSION
- **Instances:** `infra/aws/lambda/smartx_assets_pull/landing_guard.py` + `infra/aws/lambda/etfs-pipeline/etfs-netassets-daily/landing_guard.py`. **BOTH byte-identical this session — sha256 `a715b04be3145ca3186cf7e10320d2b91d87492cd63c03031df1390b13f9d2ef`.** No separate canonical file exists (only these 2 + a smartx `test_landing_guard.py`).
- **Status:** **CONFORM-BY-LUCK** — copies match today, but there is **NO drift-prevention mechanism** (edit one, the other drifts silently). This is precisely the bd49f BUILD_MANIFEST lesson SS-B cites.
- **Disp:** **migrate-at-next-touch** → designate a canonical home (**proposed `data/assets/scripts/lib/landing_guard.py`** per SS-B "shared libs in a named `lib/`", OR bless the smartx copy as the SS-C C5 reference — **CTO chooses**) + wire the build-manifest sha-tie when either Lambda is next built.
- **Gate:** build-manifest sha-tie assertion. **CLASS-D (build-time)** — build-now-safe. **The gate converts today's luck into a guarantee.**

### Axis D — Implementation patterns / scheduler grammar (SS-D)

**DC-8 — Scheduler-name cadence-stutter (`daily...daily`)**
- **Instances:** `opal-assets-bd49f-daily-pull-pull-daily`, `opal-assets-daily-emitter-daily`, `smartx-assets-daily-pull-daily` (3).
- **Disp:** **migrate-at-next-touch** (rename = delete+recreate the EventBridge/scheduler rule, risks a dropped fire → ride a maintenance touch; owner = resource lane: opal-assets → CloudOps/monolith, smartx → 0.5.0).
- **Gate:** name-lint (`{cadence}` token once, suffix only). **CLASS-D on the trigger-map CI gate** (CTO's stated hook). build-now-safe. **CTO's recommended start.**

**DC-9 — Scheduler-name missing / non-cadence suffix (`-scheduled-start`, `-schedule`, `-sched`)**
- **Instances:** `consolidation-gold-runner-scheduled-start`, `canonical-schwab-si2-download-schedule`, `bd-49f-freshness-sched`, `bd-49f-keepalive-sched` (+ schwab si2, DC-11 overlap). 5.
- **Disp:** **migrate-at-next-touch.** **Gate:** name-lint suffix ∈ `{daily,hourly,weekdays,15min,...}`. **CLASS-D** trigger-map gate. build-now-safe.

**DC-10 — Scheduler-name cadence embedded in function (`daily-pull*`)**
- **Instances:** `opal-assets-bd49f-daily-pull-*` family (4; overlaps DC-8/9).
- **Disp:** **migrate-at-next-touch.** **Gate:** same name-lint family — **DC-8/9/10 are ONE lint.** CLASS-D trigger-map gate. build-now-safe.

**DC-11 — Misleading cadence: function says `daily`, cron fires twice-daily (schwab si2)**
- **Instances:** `canonical-schwab-si2-08242234-daily-pull` (cron `15 10,22`), `canonical-schwab-si2-08335338-daily-pull` (cron `45 9,21`). 2.
- **Disp:** **migrate-at-next-touch** → rename to reflect twice-daily (e.g. `-2xdaily`). **schwab-lane — coordinate 0.5.0 D4 zero-reader window (through 2026-07-24T17:21Z);** a scheduler rename is a TF change not a schwab live-data call, likely window-safe — **flag for CTO/0.5.0.**
- **Gate:** name-vs-cron cross-check lint (the only one that must PARSE the cron; higher-effort than pure name-lint). **CLASS-D** trigger-map gate. build-now-safe.

**DC-12 — Scheduled producer WITHOUT an absence twin** — **HIGHEST CONSEQUENCE IN THE LEDGER**
- **Instances:** `smartx-assets-daily-pull` (no twin); **`opal-assets-daily-emitter` — the Door-6 completion-signal producer** (`cron(15 17)` → `gold/meta/pipeline-complete.json` → `mdpf-daily-trigger`; **if it silently stops, mdpf never fires and NOTHING pages**); + 5 `opal-assets-silver-{firm}-sweep` (DEVIATE-BY-LETTER / CONFORM-BY-DESIGN).
- **Disp (emitter):** **migrate-now** — the one migrate-now in this ledger. Rationale: standing law *"A KNOWN-WRONG FROZEN NUMBER IS STRICTLY SAFER THAN AN UNHELD PIPELINE"* — an untwinned Door-6 completion producer is an unheld-pipeline blind spot. Add a **pure-ADD** absence twin (an `absence-config.json` unit + `opal-assets-absence-check` schedule, or a CloudWatch invocations-lo alarm). **Pure-add → NEW-TERRITORY-compatible → routes through CTO plan-gate + safe-apply.** *(Twin DETECTS absence; it does not write the Door-6 key — never hand-write `pipeline-complete.json`.)*
- **Disp (smartx):** **migrate-now-or-next-touch** (smartx lane 0.5.0; lower consequence than emitter, still a real gap).
- **Disp (5 silver sweeps):** **CLASS-X CTO ruling** → I recommend **CONFORM-BY-DESIGN recorded-carve-out**: they are S3-event-primary (fire on bronze landing), so silver-absence follows bronze-absence which IS twinned upstream (bd49f-pull, mirror-cot, mirror-inf); converter failures route to `opal-assets-silver-dlq` — the DLQ is the event-primary producer's twin-equivalent.
- **Gate:** provisioning gate — every `aws_scheduler_schedule`/`aws_cloudwatch_event_rule` with a cron pairs with an absence alarm/twin **OR** declares `upstream-covered`. **CLASS-D** (TF-plan, trigger-map gate). build-now-safe. **Highest-value gate in the ledger — it prevents the next Door-6-class blind spot.**

**DC-12b — Absence detection implemented TWO ways**
- **Instance:** mechanism split — scheduler+checker-lambda (`absence-config.json`, 4 opal-assets units) vs CloudWatch freshness alarm (schwab sentinel/si2, etfs, bd-49f freshness-probe). Registry lists 7 units, 4 scheduler-twinned.
- **Disp:** **CLASS-X standard question** → I recommend **bless BOTH** (SS-D clause naming both as canonical twin implementations): an S3-event-primary producer is well-served by a freshness alarm, a scheduler-primary producer by a scheduler-twin — forcing one mechanism would be worse. No resource migration; **route to CTO as an SS-D amendment.**

**DC-3/4 note:** the SS-D "Pull provenance" row is the same fact as Axis-A DC-4 (cross-listed, one migration).

### Axis E — Device OS + IAM (SS-E) + region (SS-C)

**DC-13 — New consolidation runner not on AL2023** — **CTO's stated highest-signal start**
- **Instances:** `consolidation-gold-runner` (`ami-0c7217cdde317cfec`, ubuntu-jammy-22.04); `canonical-schwab-runner` (same AMI). 2.
- **Disp:** **migrate-at-REBUILD** (SS-E's own rule: existing boxes migrate at rebuild, not in place; in-place OS swap on a live runner is high-risk). **PAIR canonical-schwab-runner with DC-15** — one rebuild fixes OS + region. schwab rebuild **BLOCKED by D4 window till 2026-07-24.**
- **Gate:** provisioning lint — new `aws_instance` AMI is an AL2023 owner-alias. **CLASS-D**, rides the **EC2 manifest-lint** (safe-ec2-deploy, CTO's stated hook). build-now-safe. **Build design note:** AMI is a TF `aws_instance` attribute; reconcile at build whether the lint reads TF `aws_instance.ami` or an OS field in `EC2_MANIFEST.json`.

**DC-14 — IAM role naming infix (`schwab-anonymizer-lambda-role`)**
- **Instance:** only role with a `-lambda-` infix; should be `{resource}-role`.
- **Disp:** **migrate-at-next-touch** (when the anonymizer's IAM is next rebuilt) **— or recorded-carve-out** if CTO deems the rename not worth it (IAM role rename = every trust/attachment/ARN-ref updates; high friction, low value). schwab-lane (D4 window). **CTO chooses next-touch vs carve-out.**
- **Gate:** name-lint on NEW roles (`{resource}-role` + blessed helper suffixes). **CLASS-D** (TF/commit). build-now-safe; existing role rides its next touch.

**DC-15 — Region co-location: `canonical-schwab-runner` (us-east-1) ↔ `opal-data-schwab` (us-east-2)** — **NEWLY SCORED (SS-C region clause @59805972b)**
- **Instance:** cross-region runner→bucket hop. (`consolidation-gold-runner` us-east-1 ↔ `opal-data-assets` us-east-1 = CONFORM; dedicated telemetry buckets = named exception.)
- **Disp:** **migrate-at-REBUILD** (region change = rebuild). **PAIR WITH DC-13** — one canonical-schwab-runner rebuild does AL2023 + us-east-2. **BLOCKED by D4 window till 2026-07-24.**
- **Gate:** region-co-location lint — new `aws_instance` region == its primary data bucket region. **CLASS-D** (TF-plan). build-now-safe. **Build design note:** "primary data bucket" needs a declared runner→bucket mapping (propose reading `EC2_MANIFEST.json`).

---

## PROPOSED SEQUENCING (P1 CLOUD FIRST — the driver's recommendation)

| Wave | Content | Why first / gating |
|---|---|---|
| **W1 — build-now CLASS-D gates** | DC-8/9/10/11 name-lint (ONE lint, trigger-map CI gate); DC-13 + DC-15 provisioning lint (EC2 manifest-lint / TF-plan). | Pure prevent-new, **zero live-resource risk**; CTO's stated starting set. Stops the estate getting worse immediately. |
| **W1 — the one migrate-now** | DC-12 **emitter absence twin** (pure-add TF → CTO plan-gate + safe-apply). | The only ACTIVE operational blind spot (Door-6 unheld-pipeline risk). |
| **W2 — standard decisions (no code)** | DC-12b (bless both mechanisms), DC-12 silver-sweep ruling, DC-1 `_probe/` bless-or-delete. | CTO rulings + SS-* amendments; unblock the W3 gates that depend on them. |
| **W3 — CLASS-D producer gates + at-touch migrations** | DC-3/4 (eclipse/bd producer key templates), DC-7 (landing_guard canonical + sha-tie), DC-6 (schwab code home), DC-2 (`_ops`→`meta`), DC-1 (`code/`→`opal-runner-shared`). | Producer migrations ride natural touches; A-axis enforced at CI/producer-code layer (NOT runtime deny). |
| **W4 — CLASS-F + schwab-window-gated** | ~~DC-5 (telemetry-hook fix + filesystem sweep)~~ **CLOSED @b9c5f5243**; DC-11 / DC-14 / DC-6 / DC-13+DC-15 schwab-runner rebuild — **after D4 window closes 2026-07-24.** | Untracked-spill root-cause fix DONE; schwab-lane items respect the zero-reader window. |

---

## OPEN CTO DECISIONS (the ruling asks)

1. **DC-1 `_probe/`:** bless as a reserved test-scaffolding root (SS-A clause) or migrate-now-delete?
2. **DC-12 silver-sweeps:** does event-primary + `opal-assets-silver-dlq` + upstream-twin coverage satisfy the twin duty? *(I recommend CONFORM-BY-DESIGN carve-out.)*
3. **DC-12b:** bless BOTH absence mechanisms (SS-D amend) or unify? *(I recommend bless both.)*
4. **DC-14:** migrate-at-next-touch the role rename, or recorded-carve-out (rename friction > value)?
5. **A-axis enforcement surface (DC-1/2/3/4):** confirm **CLASS-D producer-code/CI checks over CLASS-R runtime bucket-policy denies** — the latter break live producers.
6. **DC-7 canonical home:** `data/assets/scripts/lib/landing_guard.py`, or bless the smartx C5 copy as the reference?
7. **DC-5:** ~~approve the telemetry-hook-fix + filesystem-sweep approach (the census's commit-gate lint is gate-blind), and clear the 7-file untracked cleanup?~~ **RULED (RULING-20): GO — hook-fix + sweep, positive-control-first. CLOSED @b9c5f5243.**
8. **DC-13 + DC-15 pairing:** confirm one `canonical-schwab-runner` rebuild does AL2023 + us-east-2 together, post-D4-window. And confirm DC-15 folds into census v0.1.2 (coordinating with ~C).

---

## RIDE-SURFACE RECONNAISSANCE (W1 build-readiness — added ~19:5xZ, before CTO rules)

I read the existing hooks the W1 lints must ride BEFORE promising they ride them. Three findings materially inform the ruling — **the instruments exist, but two of them measure the WRONG breadth and must be reconciled by a CTO ruling before their enforcement mode is sound.**

**RS-1 (DC-8..11) — the grammar instrument flags 153/154; the enforcement lint CANNOT ride the raw `conforms` field.**
`infra/aws/lambda/ci/trigger-census.py` ALREADY computes grammar conformance (`GRAMMAR_RE = ^{unit}-{function}-{cadence}$`, function ∈ {run,reattempt,absence-check}, cadence ∈ {daily,weekly,monthly,hourly}) and writes a `conforms` bool + `grammar-debt` flag per trigger — **the parser exists; DC-8..11 is an ENFORCEMENT-mode add, not a new parser** (and it already has a `--warn-only` announce-then-enforce ramp). BUT `trigger-map.json` (built 2026-07-15) shows **153 of 154 triggers `conforms:false`** — because the regex REQUIRES a literal `-{run|reattempt|absence-check}-` token that ~99% of reasonable names omit (`inf-api-assets-v2-daily`, `news-api-100am`, `bd-49f-runner-daily`, `opal-assets-silver-*-sweep-daily` all fail). **The census scored only ~14 as DEVIATE by applying JUDGMENT the raw field lacks.** An enforcement lint on the raw `conforms` field would block essentially every new trigger — a false-positive flood.
- **PREREQUISITE CTO RULING (before the lint):** reconcile the grammar with intent — **(a)** `function` OPTIONAL (default `run`, so `{unit}-{cadence}` conforms); **(b)** extend the cadence vocabulary from `{daily,weekly,monthly,hourly}` to the real estate set (`15min,5min,6h,72h,weekdays,twicedaily,6hourly,...` — enumerated live from the registry). Then re-measure; the true DC-8..11 residue = the ~14 genuinely-malformed (stutter / missing-cadence-suffix / embedded-cadence / misleading-cadence).
- **Proposed reconciled grammar:** `^{unit}(-{function})?-{cadence}$` + a **name-vs-cron consistency check** (parse `ScheduleExpression`, compare to the cadence token) for DC-11. The census carries `expression` per trigger, so the data is present.

**RS-2 (DC-12) — the twin instrument sees 1 of 3 mechanisms; DC-12b is a PREREQUISITE to a sound DC-12 gate.**
`trigger-census.py`'s `absence_twin` field only links a NAMED `-absence-check` rule — it is **blind** to the other two twin mechanisms (`absence-config.json` + shared checker-lambda; CloudWatch freshness alarm). So it UNDER-COUNTS: the registry shows `absence_twin:null` on ~every run trigger, including the 8 the census confirmed PAIRED. A DC-12 provisioning gate built on this field would false-flag every genuinely-twinned producer. **The gate needs a THREE-mechanism resolver (named-twin OR `absence-config.json` unit OR CloudWatch freshness alarm) — which requires DC-12b (bless-both) ruled FIRST.** Confirmed against all three mechanisms: `opal-assets-daily-emitter` is genuinely untwinned (migrate-now stands).

**RS-3 (DC-13) — ride-surface confirmed present + a clean fit; shovel-ready on a new-row assertion.**
`infra/aws/ec2/manifest-lint.py` (OPAL_STNDRD ph5, WARN-first + `--enforce` flip, invoked by `safe-ec2-deploy.sh`) lints EC2_MANIFEST rows for `{telemetry,duty_cycle,autoshutdown,sizing_review}` with a **GRANDFATHER set** (26 rows @ratification, INCLUDING both DC-13 boxes) that "fill on natural touches." **`EC2_MANIFEST.json` carries an `ami` field per row.** So DC-13's AL2023 check is a clean extension: add an AL2023 assertion (propose a self-declared `os_baseline` field on NEW rows — simplest, rides the WARN-first pattern; OR an AMI→OS resolver via `describe-images` for APPLIED truth). **The existing GRANDFATHER set already implements "the 2 existing Ubuntu boxes migrate at rebuild"** — DC-13 needs only the new-row assertion. *Sub-finding: manifest `ami` (DESIRED) may differ from the census's live `describe-instances` AMI (APPLIED) — a DESIRED-vs-APPLIED reconciliation the lint should surface.*

**NET:** the W1 CLASS-D gates ride EXISTING instruments (`trigger-census.py`, `manifest-lint.py`) — **no new hook to build**, exactly the consolidation win. But **DC-8..11 and DC-12 each need a CTO grammar/mechanism ruling before their enforcement mode is sound** (RS-1, RS-2); **DC-13 is shovel-ready** on a new-row assertion (RS-3). This is the "measure the ride-surface before promising the lint rides it" pass — an instrument that measures the wrong breadth is a gate that either floods or lies.

---

## RESIDUALS still UNVERIFIED (honest, not laundered to CONFORM — carried forward from census + this ledger)
- **SS-E scope-exactness** (per-role `simulate-principal-policy` with isolated positive controls, Rule 22a) — a distinct deep pass, not in this structural ledger.
- **Per-lambda source patterns** (chunking on large workloads / Retry session / telemetry-at-provision) — the D.3 scoped-out "next census slice."
- **DC-1 `_probe/` activity** (22 keys) — bless-vs-delete pends CTO; last-modified not deep-dived (proportionate).
