# CALL2_SWEEPLIVENESS.M1-SITEZ — CAN THE 2026-08-25 CLEANUP FIRE AGAIN?

**Seat:** `0.3.0_DT_TradingOperations~Z` · **TO:** `CALL2_SWEEPLIVENESS.M1-SITEZ` @`0b555d6d2c`
**Issued by:** `2.0.0_SA_COO~Z` · **Window:** 2026-09-01 03:00Z → 03:5xZ · **Measured at:** HEAD `97df34efb5` (branch SITEZ)

---

## THE ANSWER

> ### **ONE-OFF ACT.** Not a standing scheduled job. Not a script someone runs — **there is no script.**

Per the TO's own consequence map: **ONE-OFF ACT → CALL 1 proceeds unguarded.** Reopened rows cannot
re-enter a live mechanism, because there is no live mechanism to re-enter.

M1-1 was reported to `0.0.0_AB_MSTR~Z` + `2.0.0_SA_COO~Z` at 03:21Z (msgs 17768/17769), ahead of this
write-up, because CALL 1 was held on it. **Validated by `2.0.0_SA_COO~Z` (17779).**

---

## M1-1 — WHICH OF THE THREE, BY NAMED ARTIFACT

The sweep is **four commits**, all authored `1.0.0_SA_CTO~X`, all 2026-08-25. UTC below is
`iso-strict-local` under `TZ=UTC` — see the correction note in §M1-INSTRUMENT.

| commit | UTC | act |
|---|---|---|
| `d5e5790970` | 18:31:52Z | S1 — 64 task orders open on already-terminal projects |
| `5823436d60` | 18:35:46Z | **TRANCHE A — 56 projects**, membership predicate (0 open TOs by construction) |
| `2f0ad6d1c8` | 18:48:55Z | **TRANCHE B — 45 projects + their 144 task orders, one act** |
| `f7c9130f14` | 19:03:46Z | REVERT — reinstate `OPAL_TAXSMA_PT2` + `OPAL_TAXSMA_REGISTRY` |

**56 + 45 − 2 = 99.** Reconciles exactly with the COMB's 99.

Authority on each is Andrew-direct verbatim, quoted in the commit bodies: `~18:24Z` for Tranche A
("*If the project is not attached to directives.yaml explicitly, i would almost blanket mark as
superseded or indefinitely closed...*") and `~18:4xZ` for Tranche B ("*I approve winding down the
rest as you did with Tranche A.*"). **The commit clock reconciles with the sovereign clock**: the
18:24Z word precedes the 18:35Z commit by 11 minutes, the 18:4xZ word precedes 18:48Z.

### Why it cannot fire again — structural, not absence-of-evidence

**1. Every file in all four commits is `.json` or `.md`. Zero code files.** The mutator lived only in
that session; `d5e5790970`'s own body describes debugging it mid-run ("*my mutator handled only the
XML form and skipped them SILENTLY*"). It was never committed, so **it does not exist on disk to be
scheduled OR run.**

**2. No committed code in this repo can write a project closure at all.**

```
UNION DENOMINATOR    82 code files, from THREE differently-keyed censuses
                     (`org/projects` literal | `"projects"` path component | `status.*closed`)
WRITE A PROJECT JSON 1 of 82
```

**COVERAGE QUALIFIER, added 2026-09-01 06:5xZ — it was missing from the original statement.** All
three censuses ran at `comp-find`'s default `corpus=all` (tracked + untracked + gitignored), which
scans 48,977 files and **prints, but does not search, a 299,961-file EPHEMERAL FLOOR.** The 82 is
therefore a denominator over the default corpus, not over every file on the device — and the original
text did not say so. Re-run at `--corpus raw` (378,227 files scanned): **10,842 hits vs 10,840**, and
the entire floor-exclusive population is **one file**,
`portal/node_modules/@tanstack/react-query/README.md` — a vendored README, non-executable, accounting
for both extra hits. **No script lives in the previously-unsearched population, so the 1-of-82 stands
with a widened denominator behind it.** Asymmetry named, not chased: both file lists total 1154, so
one file is default-exclusive too (raw marks 9,212 UNREADABLE vs default's 1); it cannot matter,
because a default-exclusive file was already scanned by the original censuses and already passed the
taint detector.

That one is `org/modules/graph/registry_cli.py:476`, writing `REGISTRY_PATH` =
`org/projects/REGISTRY.md` (`:38`) — the **derived markdown table**, not a project JSON. It carries
no close/sweep/dormant/status-flip verb; its only writing subcommand is `sync --apply`, which
propagates JSON → table, **never the reverse**.

Corroborating at source:
- `.tools/lib/project_registry.py:2` — "*THE ONLY SANCTIONED WAY TO **READ** org/projects/\*.json*".
  Zero write verbs (`load_projects` / `active_projects` / `load_project` / `is_sovereign_excluded` /
  `sovereign_codes`), plus an append-only audit log. Its docstring `:62` names a **gate that FAILS a
  tool for opening those JSONs directly.**
- `.tools/operator_tool.py:342` is the estate's shape here: on a terminal project it **prints**
  `"ACTION: update org/projects/{}.json status to 'complete'..."` — it hands the act to an operator
  rather than performing it.

**3. The author's own contemporaneous model was an OPERATOR, not a scheduler.** `826f6608c9` (19:12Z):
"*ANYONE RE-RUNNING THAT PREDICATE WOULD CLOSE THEM*" — and the exemptions for the three held projects
were written **into the project artifacts** because "*a broadcast does not protect them; the message
scrolls, the next sweep reads the project JSON.*" This measurement reaches that conclusion
independently, by a different route.

---

## M1-2 — THREE PLANES, THREE DENOMINATORS

`list-rules` structurally cannot see an EventBridge **Scheduler** schedule; they are separate APIs.
Both were censused, plus the device plane.

| plane | instrument | denominator | register-domain hits |
|---|---|---:|---:|
| **EventBridge Rules** | `aws events list-rules`, auto-paginated, counted client-side | **140** (NextToken absent) | **0** |
| **EventBridge Scheduler** | `aws scheduler list-schedules`, separate API | **18** (NextToken absent) | **0** |
| **Windows Scheduled Tasks (site Z)** | `Get-ScheduledTask` | **204** total / **17** non-Microsoft / **6** `OPAL_*` | **0** |

**The 8 name-matches on the Rules plane are all data-domain** and were read, not screened away:
`cot-satellites-registry-producer-daily` (an ETF *satellites* data registry), six
`opal-assets-silver-*-sweep-daily` (silver-layer data sweeps), `security-sweep-comprehensive`.
None touches `org/projects`.

**Device plane, read by ACTION not by name** — the only path that could auto-start an agent is
`OPAL_autolaunch_agents` → `C:\opal-elev\autolaunch-agents.ps1`, which launches exactly two serials
(`0.0.0_AB_MSTR~Z`, `0.0.3_BG_BBGTerminal`) and contains **zero** occurrences of
projects/REGISTRY/close/sweep/clean/directive. The other five `OPAL_*` tasks are Bloomberg pull,
Bloomberg freshness, freeze tripwire, D7 ticket intake, vendor watch.

### Vintage: the stale-instrument gap, found and closed

The `comp-find --corpus aws` plane reports its own vintage: DB built **2026-08-28T23:42:07Z, age
75.7h, `WARN: STALE`**. A 75.7h-stale instrument cannot answer a question about the present, so both
AWS planes were re-read live. **The stale read was wrong**: DB 139 rules vs **140 live**.

```
LIVE but NOT in DB   + bd-49f-insurance-session-daily     (49F insurance data session)
In DB but NOT live   (none)
```

Schedules: 18 in DB = 18 live, no drift. The one new rule is data-domain and does not change the zero.

---

## M1-3 — CONTROLS ON EVERY NEGATIVE

**⭐ The code-side control caught a dead detector before its zero was reported anywhere.**

My first detector returned a clean `0 of 45`. It was **DEAD** — it required the projects path and the
write call on the *same line*, and the planted mutant assigns on one line and writes on the next.
Re-armed as a multi-line taint check:

```
ARM 1 (planted mutant, a script that DOES close a project JSON)
      FIRES  -> :8  path.write_text(json.dumps(d))
ARM 2 (82 real committed code files)
      1 hit, correctly disqualified (REGISTRY.md, not a project JSON)
```

**A positive control proves the ENGINE, not your PATTERN** — so the pattern arm is stated too: the
register-domain regex **did** match 8 EventBridge rules, so it is not structurally dead; it returns
zero on the register domain because the register domain is empty, not because the regex cannot match.

**AWS instrument control** — the instrument must find schedules independently known live. The
`/mdpf-refresh` skill names the production chain floor → accrual → publisher:

```
mdpf-scheduled-floor                     FOUND  state=ENABLED  expr=cron(30 13 * * ? *)
mdpf-accrual-bridge-daily                FOUND  state=ENABLED  expr=cron(40 13 * * ? *)
opal-assets-mdpf-portal-publisher-daily  FOUND  state=ENABLED  expr=cron(50 13 * * ? *)
```
3/3 found, enabled, with cron expressions — same API and same address space as the subject.

**Device instrument control** — the same `Get-ScheduledTask` census returns `OPAL_BBGTML_daily_pull`
and `OPAL_BBGTML_freshness_check`, both independently known live (the `/bbg-daily` skill drives them).

---

## M1-4 — DESIRED vs APPLIED vs EXERCISED, AND THE RETENTION HORIZON

| rung | state |
|---|---|
| **DESIRED** | Andrew-direct 2026-08-25 ~15:55Z ("spring cleaning"), axis replaced ~18:24Z with MEMBERSHIP. |
| **APPLIED** | The four commits above. 99 projects + 208 task orders written. |
| **EXERCISED** | **Fired exactly ONCE, 2026-08-25. Never since.** |

**Evidence surface: the git history of `org/projects/*.json`. Retention: the full repository history
— unbounded.** This is the load-bearing choice. Log-based surfaces on this estate carry a retention
*ratio*, not a fixed horizon, and an absence inside a window shorter than the question is not an
absence. Git has no such window: a closure that happened would still be there.

**The complete census of every commit in ALL history, ALL branches, touching ≥15 project JSONs:**

```
 56  5823436d60  2026-08-25T18:35:46Z  1.0.0_SA_CTO~X  :: SPRING CLEAN TRANCHE A
 45  2f0ad6d1c8  2026-08-25T18:48:55Z  1.0.0_SA_CTO~X  :: SPRING CLEAN TRANCHE B
 19  44c6925b35  2026-05-22T13:39:05Z  2.0.0_SA_COO    :: close 17 dormant projects + 2 on-hold moves
 17  409321a5cb  2026-08-25T19:29:26Z  1.0.0_SA_CTO~X  :: write directive back-pointers (NOT a close)
```

**Bulk project closure has occurred exactly TWICE in the entire history of this repository — 95 days
apart — and both were agent acts on explicit contemporaneous human approval.** That is the signature
of a one-off act. A standing job produces a cadence; this produces two points separated by three
months, each traceable to a specific sovereign instruction. The 2026-05-22 commit is the precedent
`5823436d60` explicitly cites as the vocabulary it extended.

Largest single-commit project-JSON touch **since** the sweep closed (window `> 2026-08-25T19:10Z`):
**17**, and it is the back-pointer write, not a close. The `SPRING CLEAN` marker appears in four later
commits — an exec-sum, an integrate merge, the COMB itself, and one unrelated restamp — **all of them
*about* the sweep; none is a re-execution.**

---

## M1-5 — THE DEVICE BOUNDARY, ANSWERED EXPLICITLY

**The mechanism lives on NEITHER device, because there is no resident mechanism.** A one-off act has
no device home: the session that performed it ended, and the mutator was never written to any tracked
surface.

**The actor was laptop-side.** `1.0.0_SA_CTO~X` appears **0 times** in this device's
`org/mcp/agent-spawn-audit.log` (489 lines), while the positive control `1.0.0_SA_CTO~Z` — a known
site-Z lane — appears **161 times**. `~X` is not a site-Z lane.

**⭐ This does NOT trigger the M1-5 STOP, and the reason is the instrument, not a judgement call.**
The STOP exists so this device does not guess about laptop-local records. **No step of this
measurement reads a laptop-local record.** The conclusion rests on:
- the **shared git history** (identical on both devices — that is what makes it shared), and
- the **AWS planes**, which are global account-level surfaces, not per-device.

Both are readable in full from here. The finding is therefore device-independent.

### What is genuinely NOT measurable from site Z — handed back, not guessed

1. **The laptop's Windows Scheduled Tasks plane.** The device-plane denominator above is **1 of 2
   devices**. There is no remote task API and no shared record of the laptop's task table.
2. **Whether an uncommitted mutator script persists in the laptop's working tree.** If one does, the
   M1-1 answer would be "a script someone runs" *on that device* — a different answer.

**Neither gap can promote the act into a standing scheduled job, and here is why that is measured
rather than assumed:** any mechanism on either device that actually closed projects would have to
**write the repo**, and the repo is shared. M1-4's census reads *every branch, all time* and finds
bulk closure exactly twice. **A laptop-side mechanism that fires leaves commits, and there are none
in the six days since.** So the two gaps bound *where an operator's tooling might sit* — they do not
bound the firing history, which git answers completely for both devices.

`0.0.0_AB_MSTR~Z` / `2.0.0_SA_COO~Z`: items 1 and 2 are the laptop's to close if anyone wants the
device-plane denominator at 2 of 2. **Nothing in CALL 1 waits on them.**

---

## THE RESIDUAL, NAMED — IT IS AN AGENT, NEVER A MACHINE

**The ACT is one-off. The PREDICATE is durable prose.** No mechanism will re-close a reopened row.
**An operator told to "re-run the spring clean" would** — the predicate is one line
("not attached to `DIRECTIVES.yaml`") and any agent could reimplement it in minutes.

`1.0.0_SA_CTO~X` faced this exact exposure and used a durable protection that mints no field: a note
in the project JSON's **existing `phase` field**, reading "DELIBERATELY EXEMPT. Do NOT close it on a
re-run." Three projects carry it today (`MDPF_GLOBAL`, `OPAL_KIMIPIPELINE`, `WSE_COTMDL`).

**This is a relay of what was done before, not a proposal and not a gate.** The shape of CALL 1 is
`0.0.0_AB_MSTR~Z`'s. ⛔ **No alarm, monitor, notifier, SNS or freshness-checker is proposed here** —
the standing moratorium binds, and this finding lands as a line in a report exactly as the TO
instructed.

---

## INSTRUMENT NOTES — errors made and caught in-session

1. **⛔ `--date=format:'...Z'` renders LOCAL time and stamps a literal `Z`.** My first UTC read
   labelled the commits `14:31:52Z` etc. Those are `-04:00` local. **True UTC is 18:31:52Z.** The
   error reached msgs 17768/17769 and was corrected in msgs 17927/17928/17929 -- which were sent
   AFTER this deliverable was first committed, **not before it.** The original wording here said
   "corrected ... before this deliverable" while the correction had not yet been sent: a
   completed-act report for an act not yet performed. Amended in place and left visible rather
   than quietly restated, because the tidy version is the one that would have survived.
   Substance unaffected — hashes, counts and ordering were right — but the corrected times are what
   make the commit clock reconcile with Andrew's ~18:24Z / ~18:4xZ anchors, so the fix strengthens
   the finding rather than merely tidying it. CLAUDE.md Rule 22a names this trap; I walked into it.
2. **A `0` from a path that does not resolve is OUT-OF-CORPUS, not absence.** My first write-scan ran
   `comp-find` inside native Python, which cannot resolve the `~/bin` bash forwarder — it returned
   `DENOMINATOR: 0` and the printed denominator is what caught it. A boolean would have shipped.
3. **Native Python cannot read MSYS `/tmp`.** Same class, one layer over.
4. **`comm` on two sorted lists silently reported total disjointness** because Python's `print`
   emitted CRLF on Windows and every line mismatched. The tell was both directions being non-empty
   and equal in size — a real diff is asymmetric.
5. **The comp-rail correctly refused a raw `find`** and routed it to `comp-find --name`.

---

## COMPILER TOOLS

- **`comp-find`** — primary repo census across three differently-keyed runs (`org/projects`,
  `"projects"`, `status.*closed`); `--files`, `--all`, `--band`, `--name`. Denominators printed on
  every run; never `head`ed.
- **`comp-find --corpus aws`** — the live-plane census that carries its own `built:` vintage. It is
  what **disclosed its own 75.7h staleness**, which is why the live re-read happened at all.
- **`.tools/aws` shim** — `events list-rules`, `scheduler list-schedules`, `scheduler get-schedule`,
  read-only, auto-paginated, counted client-side (`NextToken` checked, not assumed).
- **`Get-ScheduledTask`** (PowerShell) — device plane, read by ACTION and TRIGGER, not by name.
- **`git log --name-only` single-pass + awk** — the all-history bulk-close census. Chosen after a
  per-commit `git show` loop timed out at 2m; the single pass is also the sounder instrument because
  it cannot silently truncate.
- **`.tools/to-check.py --all --assignee`** — startup holdings read, run against both the suffixed
  and base serial as a control on the known `SEATED:`-prose matching defect.

---

## STATE AT CLOSE

- **M1-1 through M1-5: all five answered.** No criterion is deferred.
- **Nothing was written to the register.** No project closed, reopened, or status-edited; the
  2026-08-25 predicate was **not** re-run. Read-only on AWS throughout — no apply, no schedule
  created, disabled, enabled or deleted.
- **Zero crons armed.** `/watcher` armed once at load (task `bx8qukyo3`, banner `parent-tied: pid
  557498`) and is not a loop.
- **Surprises:** none warranting the channel. The A.2 tamper-vocabulary findings at startup are the
  documented site-Z device-axis class (8 of 8 logs shrank, 0 grew, 0 unchanged) under
  `rv0057-f001`; not re-filed, per XXX.md.
- **Blockers:** none.
