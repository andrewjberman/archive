# Schwab ingestion behavior map — the autoschwab box, the token lifecycle, the writer census

**Author:** `0.7.0_AE_CloudOps` · **Date:** 2026-07-30 · **Requested by:** Andrew (direct)
**Scope:** investigation + documentation ONLY. No builds, no alarms, no fixes. Nothing in this
document was changed by producing it.
**Feeds:** the `opal-data-schwab` decommission gate + OPAL_ASSETS consolidation + the cleanup sweep.

---

## ANDREW-DIRECT RULING — recorded verbatim (channel: this session, 2026-07-30 ~17:3xZ)

> **"49F Converter ops are all deprecated, that is a skill off main chain for schwab data now. We are
> doing this because a lot of these resources are surely deprecated and I want to clean it all up."**

**Scope, as stated and NOT adjudicated by me:** the `/49-schwab-conv` converter operation is
deprecated and off the main chain for Schwab data. The main chain for Schwab data is the monolith
path documented in §5 (box → `opal-data-assets/schwab/{master}/bronze` → `opal-assets-silver-schwab`).
The purpose of this map is therefore a **cleanup census**, not only a behavior map — see §7a.

**Broadcast obligation NOT yet discharged:** XXX.md requires MCP broadcast to COO + CTO + MSTR in the
same turn. I cannot send — the serial `0.7.0_AE_CloudOps` is held LIVE by a halted incumbent session
(PID 33636) and `send_message` refuses a `from_agent` that is not my registered serial. Forging past
the identity guard is not something I will do to satisfy a broadcast rule. **This block is the
durable record; the broadcast is owed the moment the serial conflict is resolved.**

⚠ **THE RULING HAS ONE LIVE CONSEQUENCE THAT MUST BE SETTLED BEFORE ANYTHING IS DELETED — see §7a
item A.** Deprecating the 49F converter ops strands a **live, daily-invoked MDPF feeder** that reads
their output.
**Grounding:** source citations are `file:line`; live-plane claims are marked LIVE and were read
from the applied plane (EC2/EventBridge/CloudWatch/S3S/SecretsManager) on 2026-07-30 ~15:4x–16:0xZ.

---

## 0. THE HEADLINE CORRECTION — two boxes, and the named one is not the Schwab ingester

The instruction names `canonical-schwab-runner` (`i-0ed92ce2e72f505dc`) as "the autoschwab EC2 box …
It has the Schwab SI2 desktop GUI logged in." **That is two different machines conflated under one
name.** LIVE (`ec2 describe-instances`, 2026-07-30):

| Instance | Name | OS / type | State | What it actually is |
|---|---|---|---|---|
| `i-0ed92ce2e72f505dc` | `canonical-schwab-runner` | **Linux/UNIX** r6i.xlarge | **stopped** ("User initiated") | The **canonical BUILD orchestrator** (CUTOVER-1 S4). Never held SI2; SI2 is a Windows desktop app. |
| `i-0f3d57a97f14727af` | `quartz-si2-spike` | **Windows** t3.large | **running** | **THE autoschwab box.** Holds the SI2 desktop GUI + the standing session, and runs the daily pull. |

This distinction is load-bearing for questions 3 and 4, because **every Schwab daily-pull rule targets
`i-0f3d…`, which is running — not the stopped box.** Sources: `runner.tf:20-45` (the Linux
orchestrator, `ami-0c7217cdde317cfec` Ubuntu 22.04, `filebase64(…/canonical-schwab-runner/user-data.sh)`)
vs `iam.tf:1-11` + `monolith-daily-schedule.tf:56` (`values = ["i-0f3d57a97f14727af"] # the SI2 box
(quartz-si2-spike) -- holds the SDD session + creds`).

---

## 1. What is the box actually FOR today?

### The stopped box (`canonical-schwab-runner`)
Not an ingester at all. It is a **start-stop ephemeral Linux build box**: an event starts it, systemd
runs `run-canonical.sh` (S8 raw-completeness gate → canonical build → log), then it self-stops via OS
`shutdown -h now` with `instance_initiated_shutdown_behavior = "stop"` so its role needs no `ec2:*`
(`runner.tf:3-5`, `:27`). **Stopped is its designed idle state.** See §4 for why it has never left it.

### The real autoschwab box (`quartz-si2-spike`) — hypothesis CORRECTED, and inverted

> **Working hypothesis:** "its only remaining job is minting session tokens for a Schwab REST API …
> and Lambdas now do the real ingestion into opal-data-assets/schwab/."
>
> **Verdict: INVERTED.** The box *is* the ingester and it *is* the REST client. The Lambdas do the
> **silver conversion**, not the ingestion. And the Secrets-Manager token-minting machinery you're
> thinking of exists but is **dormant, with zero consumers.**

The box's live job is to run `sdd-daily-pull.ps1`, which is itself a REST client against the SDD
backend and lands raw vendor bytes straight into the monolith:

- REST base URL `https://si2.schwabinstitutional.com/fileservices/SDDServices/` (`sdd-daily-pull.ps1:293`),
  TLS 1.2 pinned (`:294`), two endpoints: `FetchDetails/SpecificFileDetails.aspx` (enumerate, `:324`)
  and `Download/SpecificFile.aspx` (fetch, `:448`).
- It lands **direct to the monolith**: `$BUCKET='opal-data-assets'`,
  `$KEYROOT="schwab/$Master/bronze"` when `-Target monolith`, which is the **default** (`:44`, `:53-56`),
  and the S3 write is `:481`.
- The box needs SI2 only for the app's own .NET DLLs, which it loads out of the Administrator profile
  to serialize the SDD wire format (`:277-292` — `Schwab.SI.Framework.dll`,
  `Schwab.SI.SI2Desktop.Contract.Download.dll`, `XmlHelper.SerializeWithCompression`).

So the SI2 GUI is not a downloader any more — it is the **credential and DLL host** for a REST client
that runs on the same box. The GUI's own auto-download channel is dead and deliberately replaced
(`sdd-daily-pull.ps1:3-5`: it "exited rc=0 on ~22 consecutive cycles over 11 days while landing
NOTHING"; its EventBridge rule `canonical-schwab-si2-download-schedule` is **DISABLED** — LIVE).

**The half of the hypothesis that is right:** the *architecture you described was designed*, under
ADVI_SCHWABAUTO A-PRIME — a capturer minting `schwab/sdd/session` for a `schwab_sdd_ingest.py` that
would call SDD from Lambda. It got to Gate-2 and stopped. See §2.

---

## 2. Token lifecycle — there are TWO token systems and only one is live

### 2a. LIVE: the Windows Credential Manager refresh token (`SDDSecure`)

| Question | Answer | Evidence |
|---|---|---|
| Who logs in | **A human**, into the SI2 desktop GUI on the box, establishing a standing session | `sdd-daily-pull.ps1:246-251`, `schwab_sdd_session_capture.py:6-8` |
| Where the token lives | Windows Credential Manager, target `SDDSecure`, in **Administrator's** vault — **per-user** | `sdd-daily-pull.ps1:229` (`CredReadW('SDDSecure',1,0,…)`), `:249-251` |
| How it is used | Read at start, sent as HTTP header `x-refresh-token` on every SDD call | `:238`, `:301` |
| Refresh cadence | **None on a clock.** Re-read from the vault every 500 files mid-run (`:437`). The token itself has not died in ~10 months | `:437`; TTL note `schwab_sdd_session_capture.py:69-72` ("tokens have not died in ~10 months (Andrew 2026-07-10)") |
| Concurrency control | Box-wide lockfile `C:\schwab-sdd\.sdd-session.lock`; a second puller **refuses** (exit 7) rather than risk the shared session; stale-safe (dead pid or >2h) | `:144-191` |
| Consumer | `sdd-daily-pull.ps1` only, running **on the box** | as above |

**What breaks it — three distinct failure modes, all named at source:**

1. **Wrong execution identity.** SSM `AWS-RunPowerShellScript` runs as `nt authority\system`, whose
   vault is empty, so `CredRead` returns null **100% of the time regardless of session health**.
   A/B-measured on one box 9 minutes apart: `06:02:32Z` as SYSTEM → FATAL; `06:11:25Z` as
   Administrator → OK, token len=128, 5 files landed (`monolith-daily-schedule.tf:68-72`). The script
   discriminates the two causes explicitly and refuses to blame the session
   (`sdd-daily-pull.ps1:240-272`) — that guard exists because the conflated version once sent an
   operator hunting a session that was never dead (`:243-245`).
   **This is why the trigger is SSM→scheduled-task and not SSM→script** (see §3).
2. **Console session logged off.** The task runs `/RU Administrator /IT` (InteractiveToken), so it
   requires the Administrator console session to stay logged on. Named as a residual, not hidden
   (`monolith-daily-schedule.tf:90-92`), with a start-assertion that converts a silent no-run into a
   loud one (`:134-138`).
3. **Box stopped.** SSM cannot dispatch to a stopped instance; the script — and therefore its own SNS
   paging, which lives *inside* the script (`sdd-daily-pull.ps1:134-142`) — never executes. This is
   the real hazard shape, and it applies to `quartz-si2-spike`, **not** to the stopped box (§4).

### 2b. DORMANT: `schwab/sdd/session` — built, captured once, never consumed

- **Producer:** `schwab_sdd_session_capture.py` — reads the SI2 app's own WebView2/Chromium profile at
  rest (DPAPI master key → AES-256-GCM cookie decrypt), assembles the **full** Schwab cookie jar plus
  OAuth access/refresh JWTs, and writes them to Secrets Manager (`:14-22`, `:187-223`, `:226-263`,
  `:289-297`). Gated by design: `--fixture` / `--dry-run` / `--live`, no default (`:34-45`). Fires as
  a scheduled task under the Administrator SID, InteractiveToken, for the same DPAPI reason
  (`run-capture.ps1:1-6`, `:17-30`).
- **Intended consumer:** `schwab_sdd_ingest.py`, named in the capturer's own docstring (`:8`) — so that
  ingestion could "call the SDDServices REST backend directly, no re-login."
  **That file does not exist anywhere in the repo.** The only two files in the estate that mention it
  are the capturer's docstring and the design brief
  (`docs/briefs/schwab-sdd-rest-ingest-aprime-design-20260702.md`).
- **LIVE secret metadata** (`describe-secret`, metadata only — no value read):

  | Secret | Created | LastChanged | LastAccessed (day-grain) | KMS |
  |---|---|---|---|---|
  | `schwab/sdd/session` | 2026-07-09 | **2026-07-10, never since** | ~2026-07-09/10 | dedicated CMK `8863d4ac…` |
  | `schwab/sdd-credentials` | 2026-06-29 | 2026-06-29 | ~2026-06-28 | default |
  | `schwab/ec2-credentials` | 2026-06-29 | 2026-07-06 | ~2026-07-06 | default |
  | `schwab/anonymization-key` | 2025-12-23 | 2025-12-23 | ~2026-01-02 | default |

  `schwab/sdd/session` was written **once**, at the Gate-2 exercise on 2026-07-10, and has not been
  written or read since. There is no refresh cadence because there is no refresher and no consumer.

- **Grant shape worth flagging:** the box role holds `secretsmanager:GetSecretValue` **and
  `PutSecretValue`** on `secret:schwab/*` — a prefix wildcard that confers every future `schwab/*`
  secret (`iam.tf:72-79`; the hazard is self-flagged at `secrets.tf:11-13`).

**Net answer to "who consumes that secret": nobody.** Its consumer was never built. It is a
completed Gate-2 artifact sitting behind an unfinished gate — and it is the one piece of the estate
that matches the token-minter hypothesis, which is presumably why the hypothesis is attractive.

---

## 3. Writer census — `opal-data-assets/schwab/{08242234,08335338}/`

| # | Writer | Writes | Trigger | LIVE status |
|---|---|---|---|---|
| 1 | **The box** via `sdd-daily-pull.ps1` | `…/bronze/{type}/{YYYYMMDD}/{vendor}.zip`; `…/_ops/daily_pull/`; `…/meta/pulls/` | 2 EventBridge rules → SSM → **Windows scheduled task as Administrator** | **WORKING TODAY** |
| 2 | **`opal-assets-silver-schwab`** | `…/silver/fact_*`; `…/meta/conversions/`; `backfill-status.json` | **Two paths:** S3 notifications on `schwab/{m}/bronze/` suffix `.zip`, **plus** EventBridge sweep `cron(15 12)` `{"mode":"sweep"}` | **WORKING** (155 invocations/7d, **0 errors**) |
| 3 | `opal-assets-ingest-mirror` | **NOTHING under `schwab/`** | n/a | **NOT A SCHWAB WRITER** — see below |
| 4 | *(unattributed)* `08335338/gold/{_runlogs,canonical,dimensions}` | gold tier, 0833 only | not identified this pass | **OPEN ITEM** |

### 3a. The box path (writer 1) — and it is healthy right now

Rules (LIVE `describe-rule` + `list-targets-by-rule`), both **ENABLED**, both targeting
**`i-0f3d57a97f14727af` (running)**:

- `canonical-schwab-si2-08242234-daily-pull` — `cron(15 10,22 * * ? *)`
- `canonical-schwab-si2-08335338-daily-pull` — `cron(45 9,21 * * ? *)`

The target is *not* the puller. It is a shim that pulls `sdd-daily-pull.ps1` fresh from
`s3://opal-data-assets/code/canonical-schwab-si2/` (Rule 12), registers a scheduled task
`/RU Administrator /IT /RL HIGHEST`, runs it, **asserts it actually started**, waits, and propagates
`LastTaskResult` as the SSM exit code (`monolith-daily-schedule.tf:116-148`).

**Exercise evidence, not config evidence** — the puller's own run manifests, read from S3 today:

| Master | run_id | enumerated | downloaded | skipped | failed | landing guard |
|---|---|---|---|---|---|---|
| 08242234 | `20260730T101519Z` | 240 | 11 | 229 | 0 | `ok=true`, shortfall/surplus/collision all 0 |
| 08335338 | `20260730T094553Z` | 278 | 13 | 265 | 0 | `ok=true`, shortfall/surplus/collision all 0 |

Both carry `trading_frontier: 2026-07-29` (T-1, correctly resolved) over a 30-day window. Run ids
match the cron minutes exactly (10:15Z / 09:45Z). Corroborated by SSM history (two
`AWS-RunPowerShellScript` invocations, **Status: Success**, at ~09:45Z and ~10:15Z today) and by
CloudWatch `AWS/Events` Invocations = **33 per rule over 30 days**, which is exactly twice-daily since
the rules were created on 2026-07-14.

Both manifest homes are live: `_ops/daily_pull/` **and** the ruling-21 home `meta/pulls/` (listing
shows `20260729T101519Z.json`, `20260729T221519Z.json`, `20260730T101519Z.json`). Worth recording
because `sdd-daily-pull.ps1:557-561` still says the `MonolithSchwabMetaPullsWrite` grant is
"authored-not-applied until CTO's gate" — **it has applied; the comment is stale, the WARN path is not
firing.** *(S3 `ls` timestamps render LOCAL/UTC-4 on this host; `06:16:13` local = `10:16:13Z`, which
is why they agree with the run ids.)*

### 3b. `opal-assets-ingest-mirror` — the one you flagged: it is NOT a schwab writer

You asked me to look hardest here. **It never writes `schwab/`, by explicit ruling.** Its MAP has
exactly three rows and is forbidden to grow (`lambda_function.py:92-139`):

1. `orion/inflection` ← `opal-data-inf` (flat generation only)
2. `eclipse/inflection` ← `opal-data-inf/bronze/eclipse/`
3. `blackdiamond/cottonwood` ← `opal-data-cot/forwardfill_v2/`

plus one non-row provenance rider for cot BD query templates (`:151-159`). The file states the reason
directly at `:13-17`: *"THE MAP IS BORN WITH THREE ROWS AND NEVER GROWS … These three exist only
because their producers CANNOT be retargeted … Everything else lands NATIVE (schwab C3, ETF C4,
SmartX C5). A fourth row is an architecture fork for CTO, not a map edit."* The string `schwab`
appears **once** in the whole file — in that sentence. Its Terraform (`mirror.tf`) provisions only the
INF rule `cron(15 14)` and the cot ET Scheduler `cron(30 18) America/New_York`; no schwab schedule
exists. **Clean negative: drop it from the schwab writer set.**

### 3c. Which writers still function with the box stopped?

Reading the question as intended (the *SI2* box, `i-0f3d…`, since the stopped box writes nothing here):

- **Writer 1 stops entirely, and silently.** SSM cannot reach a stopped instance; the puller's SNS
  paging is *inside* the script, so nothing pages. The rule still reports fine in `describe-rule`.
  This is the genuine "silent no-run" hazard — it is simply not currently occurring.
- **Writer 2 keeps running and keeps reporting success.** The event path has no events; the 12:15Z
  sweep runs, finds no new bronze, and converts nothing. An absent day is honestly absent, but the
  sweep does not raise on "the source produced nothing today" — so **silver looks healthy while
  ingestion is dead.** The failure would surface only at the bronze frontier, which nothing currently
  watches (and per the standing moratorium, nothing should be built to watch it without your word).
- The stopped box's absence changes nothing in this tree.

---

## 4. Was the stop deliberate? Is the lifecycle coherent?

**The premise "SSM at a stopped box = silent no-run" does not apply here** — the daily-pull rules
target the *running* box (§3a). But following the thread produced a **different and larger finding**.

**Was the stop deliberate?** Effectively yes, and it is the designed state. `canonical-schwab-runner`
is start-stop ephemeral by construction: it self-stops via OS shutdown with
`instance_initiated_shutdown_behavior = "stop"` (`runner.tf:3-5`, `:27`), and its tags say so
(`AutoShutdown = "self-stop"`, `:36`). `StateTransitionReason` is `"User initiated"` — **note that a
self-stop and a human stop are not distinguishable from that string alone**, so I am not claiming
which one it was; it does not change the conclusion.

**Intended lifecycle: event-woken, not always-on.** `canonical-schwab-xref-success` matches
`{source: opal.canonical-xref, detail-type: XrefRefreshSuccess}` → SSM `AWS-StartEC2Instance`
(`runner-trigger.tf:19-36`). The design gates "build ONLY after a fresh+successful xref" by
construction, prevention over detection (`:6-9`).

**Are the crons coherent with it? Yes — and that is not the problem. THE PROBLEM IS THE BOX HAS NO
LIVE PATH TO EVER START.**

- `canonical-schwab-xref-success` is **ENABLED** (LIVE) and has **zero invocations in the last 30
  days** — CloudWatch `AWS/Events` Invocations returns an **empty datapoint set**, versus 33/33/17 for
  the three sibling rules measured in the same call (that contrast is the positive control: the metric
  and the query work; this rule simply never fired).
- **Nothing emits the event.** No `put_events` with `source=opal.canonical-xref` exists in the
  codebase — every hit is the rule itself, design docs, or census artifacts. The emitter was assigned
  as a follow-up on 2026-06-29 and never landed: *"[0.4.0_DS_ClientPlatform] Wire the S10
  xref-refresh-success put_events emit … Next-after"*
  (`0.6.0_AE_PartnerETL/logs/2026-06-29/session_cutover1_canonical_runner_standup.md:94-95`).
- The Terraform file **says it should not have been applied yet**: *">>> HELD: … Do NOT apply until the
  xref bug is fixed + the sentinel emit is wired (CTO 194437Z). <<<"* (`runner-trigger.tf:13-16`).
  **The rule is applied and live anyway.**

So the coherent statement is: **this is not an incoherent schedule, it is an unfinished cutover left
in a state that reads GREEN.** An ENABLED rule, a healthy-looking instance, and a box that has been
stopped since it launched on 2026-06-29 with no reachable start path. Every config-read instrument
reports this correctly and none of them reports it as a problem — `describe-rule` says ENABLED,
`describe-instances` says stopped-user-initiated (which is the *designed* idle state), and only the
invocation metric distinguishes "idle between events" from "never once woken."

*(One consequence worth stating for the gate: if the sentinel is ever wired, this box starts and runs
`run-canonical.sh` for the first time in a month against whatever state exists then. That is a
decision, not a formality — flagged, not adjudicated.)*

---

## 5. End-to-end mechanics — which paths are live, which legacy

### LIVE (the production path)
```
human → SI2 desktop login on quartz-si2-spike (standing session; SDDSecure in Administrator's vault)
          │
EventBridge cron(45 9,21) / cron(15 10,22)
          │  SSM RunPowerShellScript (as SYSTEM — trigger only)
          ▼
   Windows scheduled task /RU Administrator /IT  ──► sdd-daily-pull.ps1
          │   single WIDE 30d search (never chunked: the date-range search is boundary-lossy)
          │   partition date from API AsOfDATE, never the filename; master observed from vendor bytes
          ▼
   s3://opal-data-assets/schwab/{master}/bronze/{type}/{YYYYMMDD}/{vendor}.zip   ← artifact of record
          │                                    + _ops/daily_pull/ + meta/pulls/ manifests
          │  S3 notification (prefix schwab/{m}/bronze/, suffix .zip)   ── and ──  EventBridge cron(15 12) sweep
          ▼
   opal-assets-silver-schwab  ──►  …/silver/fact_*  + meta/conversions/ + backfill-status.json
```
Health: monolith `08242234/silver/fact_uln/` newest partition is `date=2026-07-29` — the T-1 frontier.

### LEGACY / DEAD
- **The OneDrive delivery flow (`/49-schwab-conv` Step 1) is INERT.** The local delivery folder stopped
  receiving after `CRS20260715`; `01_raw/` is frozen (newest object `01_raw/CRS20260715.UPT`, landed
  2026-07-16). All seven converters were re-pointed to **monolith bronze** on 2026-07-17, and running
  the full cycle *without* Step 1 on 2026-07-24 landed 42/42 partitions — proof of inertness by
  exercise, not by argument (`49-schwab-conv/SKILL.md:26-32`, `:51-61`).
- **`opal-data-schwab` is the staging escape hatch only**, exactly as the script source says
  (`sdd-daily-pull.ps1:38-43`) — reachable only by an explicit `-Target staging`, which no schedule
  passes. Its legacy trees are frozen: `silver/{ACC,ULN}` newest `date=20260508`, `silver/TRN` newest
  `date=20260420`, `03_silver/{TRN,TRN_NNA,account_xref}`, `bronze/rps/`, `01_raw` at 2026-07-15.
- The 49F silver chain now lands in a **third** location — `s3://opal-data-bd/schwab/silver/{acc,rps,
  trn,trn_nna,uln,ult,rld}/` — all seven tables at `date=20260723` (`SKILL.md:30-31`).
- **The box no longer holds write grants to `opal-data-schwab`** — WP8 CELL-4 removed
  SchwabRawList/Write + SchwabBronzeList/Write (`iam.tf:35-41`) and the 0833 backfill policy
  (`:123-126`). Only two narrow `GetObject` **code-read** grants remain, one per code home (`:49-52`
  legacy, `:63-66` monolith), with the legacy one explicitly slated for the D5 removal battery.

### The sharpest remaining item for the decommission gate

**`data/canonical/schwab/build_canonical_daily.py` still reads the dead bucket on a live call path.**

- `SRC_BUCKET = "opal-data-schwab"` (`:48`, whose own comment says *"LEGACY 01_raw tree -- DEAD, frozen
  at CRS20260715"*).
- `latest_rps_date()` paginates `Bucket=SRC_BUCKET, Prefix="01_raw/"` and returns the max `.RPS` date
  (`:141-146`).
- It **is called**: `t1 = _normalize_date(args.date) or latest_rps_date()` (`:228`) — i.e. it is the
  fallback whenever the script is invoked without `--date`.

Two failure shapes, and **both are silent**:

1. **Today, with the bucket present:** it returns **2026-07-15** as "latest" — the frozen value — while
   monolith bronze is current to 2026-07-29. An operator running the script without `--date` silently
   builds against a two-week-old frontier.
2. **After decommission:** the listing returns empty, `ds` is empty, the function returns `""`, and
   `t1` becomes `""` — which flows downstream rather than raising at the call site.

Neither shape is loud. This is the one dependency I would put in front of the gate first. *(Note: the
similarly-named `_latest_rps_date` in `data/mdpf/scripts/feeders/wsd_partner_held_etf.py:100` and its
deployed twin read `schwab/silver/rps/` on the **bd** bucket — a different function against a
different bucket. Do not conflate them; that one is not a `opal-data-schwab` dependency.)*

Other remaining dependents from the sweep card that this pass did **not** re-derive (carry forward,
unverified here): the bd-* gold fleet, ephemeral price-fetchers, and `quartz-si2-spike`'s own graph
READ edge. **`schwab-anonymizer` I did check: LIVE, `State: Active`, last modified 2025-12-23, and
`get-policy` returns `ResourceNotFoundException` — it has NO resource policy, therefore no S3 or
EventBridge invoker. It is directly-invocable only. Dormant, not wired.**

---

## 6. Corrections this pass makes to existing records

| Record | Said | Correction |
|---|---|---|
| `SCHWAB_PROCESS_SWEEP.md:42-47` FINDING 2 | "Two ENABLED twice-daily rules fire SSM at a STOPPED box … The SDD daily pull is silently not-running" | **FALSE.** Both rules target `i-0f3d57a97f14727af` (**running**), not the stopped `i-0ed92…`. The pull ran successfully today, both masters, guard OK. The card conflated the two boxes. |
| `SCHWAB_PROCESS_SWEEP.md:9` | `canonical-schwab-runner` = "THE 'autoschwab box'" | It is the **Linux canonical build orchestrator**. The autoschwab box is `quartz-si2-spike`. |
| `sdd-daily-pull.ps1:557-561` | `MonolithSchwabMetaPullsWrite` is "authored-not-applied until CTO's gate" | The grant **has applied**; `meta/pulls/` manifests are landing daily. Comment is stale. |
| `runner-trigger.tf:13-16` | "Do NOT apply until … the sentinel emit is wired" | The rule **is applied and ENABLED**; the emit was never wired; zero fires in 30d. |

**The genuine temporal-incoherence specimen survives — it just lives somewhere else than the card
placed it.** It is not a cron firing at a stopped box; it is an **ENABLED rule waiting on an event
that no code emits, gating a box that has therefore never started**, in a file that documents its own
hold and was applied anyway.

---

## 7a. CLEANUP CENSUS — deprecation candidates, by evidence class

Per the ruling above. **Nothing here has been deleted, disabled, or changed.** Confidence is stated so
the cheap-and-safe removals are separable from the ones that need a decision.

### A. ⚠ BLOCKER — settle this before the 49F converter ops are removed

**`wsd-49f-partner-held-etf-daily` reads the 49F converter chain's output and is invoked EVERY DAY.**

- Source: `RPS_SILVER_BUCKET = "opal-data-bd"` / `RPS_SILVER_PREFIX = "schwab/silver/rps"`
  (`wsd_partner_held_etf.py:72-73`), read at `:109` / `:140-142`.
- LIVE: Lambda `State: Active`; CloudWatch Invocations = **1/day, every day through 2026-07-30**.
  Note it has **no EventBridge rule targeting it** (`list-rule-names-by-target` → `[]`) — it is driven
  by the MDPF daily chain (SSM `"mdpf daily chain 2026-07-30"` ran today). So a config read alone
  would have called it unwired; the invocation metric is what proves it live.
- Its source frontier is already frozen: newest partition `s3://opal-data-bd/schwab/silver/rps/
  date=20260723/`, unchanged since the converter chain last ran on 2026-07-24.
- **The failure mode is silent, and it has already started.** `_latest_rps_date(s3, on_or_before)`
  returns the newest partition **≤** the requested date (`:100-118`). With the producer deprecated it
  will keep returning `20260723` **forever**, with no error, no empty result, and no log anomaly —
  MDPF partner-held-ETF quietly pinned to a stale holdings snapshot that ages one day per day.
- **Decision owed (yours or CTO's, not mine):** re-source this feeder onto the monolith
  (`opal-data-assets/schwab/08242234/silver/`), or retire the feeder, or keep the RPS leg of the
  converter chain alive as an exception. **Until one of those lands, the 49F converter chain is not
  safely deletable.**

> **This is the same defect shape as §5's `build_canonical_daily.py` finding, and that is the
> generalizable lesson for the whole cleanup: these consumers do not fail when their producer dies.
> They pin to the last partition and keep answering confidently.** A frozen frontier is the
> characteristic signature of a half-finished deprecation here — expect more of it, and check for it
> by comparing each consumer's newest source partition against the monolith frontier, not by looking
> for errors. There will not be any errors.

### B. HIGH confidence — dead, no live consumer found

| Resource | Evidence | Note |
|---|---|---|
| `canonical-schwab-si2-download-schedule` (rule) | **DISABLED** (LIVE); the GUI channel it drove is the one that landed nothing for 11 days (`sdd-daily-pull.ps1:3-5`) | Superseded by the two monolith daily-pull rules |
| `schwab-anonymizer` (Lambda) | `get-policy` → `ResourceNotFoundException` = **no invoker**; last modified 2025-12-23 | Also `schwab/anonymization-key`, last accessed ~2026-01-02 |
| `/49-schwab-conv` Step 1 (OneDrive→`01_raw` sync) | Proven inert **by exercise** — full cycle run without it landed 42/42 (`SKILL.md:51-61`); local folder dead after `CRS20260715` | Already documented as retired in the skill |
| `opal-data-schwab/01_raw/` | Frozen at `CRS20260715` (landed 2026-07-16) | **One live reader remains** — §5 `build_canonical_daily.py:141-146,228` |
| `opal-data-schwab` legacy silver trees (`silver/{ACC,TRN,ULN}`, `03_silver/*`) | Newest `date=20260508` / `20260420` | Superseded by the bd tree, itself now deprecated |
| Box grants `SchwabRawList/Write`, `SchwabBronzeList/Write`, backfill policy | **Already removed** (`iam.tf:35-41`, `:123-126`) | Cleanup already partly done |
| `SchwabOpsCodeRead` (legacy code home) | Superseded by `SchwabOpsCodeReadMonolith`; slated for the D5 removal battery by its own note (`iam.tf:49-52` vs `:63-66`) | "Never two homes forever" |

### C. DECISION-CLASS — built, unused, holding live material or live config

| Resource | State | The decision |
|---|---|---|
| `schwab/sdd/session` + `schwab_sdd_session_capture.py` + its CMK | Captured **once** 2026-07-10, never re-written, never read; consumer `schwab_sdd_ingest.py` **does not exist** | Resume A-PRIME, or retire. It currently holds a live Schwab auth jar with no purpose. |
| `canonical-schwab-xref-success` (rule) + `canonical-schwab-runner` (box) + its start-role/automation IAM | Rule ENABLED, **0 fires/30d**, no emitter; box stopped since launch 2026-06-29; TF carries its own HELD banner (`runner-trigger.tf:13-16`) | Wire the S10 emit, or retire rule + box + start-path IAM together. **Do not start the box casually** — it would run `run-canonical.sh` for the first time in a month. |
| `opal-data-bd/schwab/silver/*` (7 tables) | Output of the now-deprecated converter chain | Gated behind item A |
| `data/canonical/schwab/build_canonical_daily.py` | Live call path onto the dead bucket (`:48`, `:141-146`, `:228`) | Under the ruling this becomes a **delete-candidate rather than a repair-candidate** — but confirm no other caller first |
| `schwab/*` prefix-wildcard grant incl. `PutSecretValue` (`iam.tf:72-79`) | Live, self-flagged (`secrets.tf:11-13`) | Narrow to enumerated secrets once the dormant set is retired |

### D. KEEP — this is the main chain

`quartz-si2-spike` + its two daily-pull rules + `sdd-daily-pull.ps1` + `opal-assets-silver-schwab` +
its two S3 notifications + the 12:15Z sweep + `MonolithSchwabWrite`/`OpsWrite`/`MetaPullsWrite` +
`SchwabOpsCodeReadMonolith`. Verified working today (§3a).

### E. NOT RE-DERIVED THIS PASS — carry forward as unverified

bd-* gold fleet edges, ephemeral price-fetchers, `quartz-si2-spike`'s graph READ edge on
`opal-data-schwab`, `01_raw_quartz_validation/`, `02_anonymized/`, `03_mappings/`, `_archive/`,
`backfill/`, and the unattributed `08335338/gold/` writer. **Listing them as unverified is the point —
none of these should be counted as cleared.**

---

## 7. Open items (surfaced, not adjudicated — no fixes made)

1. **`build_canonical_daily.py:141-146,228`** — live call path onto the dead bucket; silently wrong
   both before and after decommission. **Decommission-gate blocker.**
2. **`canonical-schwab-xref-success`** — applied against its own HELD banner, zero fires, no emitter.
   Decide: wire the S10 emit, or retire rule + box.
3. **`08335338/gold/`** exists (`_runlogs/`, `canonical/`, `dimensions/`) and `08242234/` has **no gold
   tier**. Writer unattributed in this pass.
4. **Two stale source comments** (§6) — a class this estate treats as a defect, not a nit.
5. **`schwab/*` prefix-wildcard grant** with `PutSecretValue` on the box role (`iam.tf:72-79`) —
   self-flagged at `secrets.tf:11-13`, still open.
6. **`schwab/sdd/session` + its capturer** — a complete, CMK-encrypted, zero-consumer subsystem.
   Either the A-PRIME REST ingest resumes, or this is dead weight holding live session material.
7. ~~**The 49F bd-tree chain has no schedule**~~ — **SUPERSEDED by the Andrew-direct ruling above
   (2026-07-30 ~17:3xZ): the 49F converter ops are deprecated and off the main chain.** The absence of
   a schedule is therefore not a defect to fix; the chain is a removal candidate. What survives from
   this item is **§7a-A**: its output has a live daily consumer, so the removal is gated, not free.
   *(Recording the supersession rather than deleting the line — the original observation was correct
   on the evidence available, and the ruling is what changed, not the measurement.)*
