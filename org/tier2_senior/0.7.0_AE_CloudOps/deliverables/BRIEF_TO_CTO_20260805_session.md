# BRIEF TO CTO (base) — 0.7.0_AE_CloudOps session 2026-08-05 (1410–1840Z)

**From:** `0.7.0_AE_CloudOps` · **To:** `1.0.0_SA_CTO` (base) · **Issued:** 2026-08-05T18:4xZ
**Requested by:** Andrew, direct at the AE terminal.

Ordered by what needs YOUR decision, not by what happened. Everything is grounded; where it is not,
it says so.

---

## 1. TWO TOOL DEFECTS IN `deploy_ledger.py` — YOURS AS TOOL OWNER. THIS IS THE HEADLINE.

`.tools/deploy_ledger.py` has two independent defects. Both are live now.

### 1a. `close` CRASHES — four ledgers are PERMANENTLY UNCLOSABLE, and the gate RED-alerts them forever

```
python .tools/deploy_ledger.py close --slug cot-pair-tolerance-recal
  -> Traceback ... KeyError: 'log'   at cmd_close:318   state["log"].append(...)
```

**The two code paths disagree on the schema.** `_read_sentinel` validates only
`slug/opened_at/legs/entry_path/window_hours` — `log` is **not** required — so `cmd_check` **accepts**
these sentinels, reports `OPEN [PAST-WINDOW]`, and fires RED. `cmd_close` then **refuses** to process
the very same file.

> **A gate that can see an entry, alert on it indefinitely, and structurally cannot close it.**

Affected: `cot-pair-tolerance-recal`, `emitter-wo4a-totals-refusal`, `mdpf-trigger-d2-event-log`,
`wo2-publisher-repoint-schedule` (all missing `log`; `emitter-wo4c` also missing it).
**Not hand-patched** — hand-editing a sentinel is what created this state. No mutation occurred: the
crash precedes `_write_entry`/`_save`/`unlink`, so all four files are byte-unchanged.

### 1b. The PRESCRIBED REMEDY IS DESTRUCTIVE

The drift message says *"Fix: deploy_ledger.py close (never hand-edit the entry)."* But `_write_entry`
(`:177-179`) is `Path(entry_path).write_text(_render_entry(state))` — a **full overwrite** of the
hand-authored markdown with a generated stub.

Running the sanctioned fix on `cot-pair` would have erased: upload ETag `e0ef77832f`, identity-(i)
delta `0.0100` logged PASS, commit `16ed33b6c6`, run id `mdpf_daily_20260728_225137`,
cycle-complete first emit `22:55:12Z`, and the carried residual that accrual has no runner-side home.
**None of it reconstructible from the sentinel's leg fields.**

**Interim handling already executed** (MSTR ruling LD-0090, you cc'd with countermand room): all five
hand-authored markdowns archived byte-exact to `<slug>.hand-authored-20260805.md`, md5 src==dst
verified, committed FIRST @`1f17b81e3`. MSTR then VOIDED the close half once 1a surfaced.
**MSTR ranks 1a above 1b as the primary fix. Countermand is yours if you differ.**

### 1c. Coverage observation (banked, nothing built)

`last_red_at` on all four was **None** until my 155910Z run — despite 185h past window, they had
**never alerted anyone**. I also invoked `check --red` expecting a report; `--red` *delivers*. It put
3 alerts in COO's inbox. Disclosed and owned; plain `check` from here.

---

## 2. INF GOLD CHAIN — NOT COMPLETED SINCE 2026-07-31. TWO BLOCKERS, AND THE SECOND IS HIDDEN.

Found by a retraction, not by an instrument (§5). Diagnosed read-only under COO GO. **The framing
matters: the pipeline is not broken — a guard is doing its job.**

### Blocker #1 — `INF_C_01`, a CORRECT guard refusing a real data loss (needs a DECISION, not a fix)

```
CHAIN chain:full FAILED at INF_C_01 (exit=1)   2026-08-05T14:50:56Z
nna_coverage_guard.NNACoverageRegression
  raised  nna_coverage_guard.py:320  (assert_partition_coverage_continuity)
  called  INF_C_01.canonical_nna.py:918 <- main() :956
evidence  s3://opal-data-inf/gold/logs/chain_full_20260805_134750.log
          4,305,235 B / 36,127 lines; exactly 1 ERROR + 1 Traceback (denominator printed)
```

**5 accounts carrying $514,487.47 of SERVED NNA** would be dropped from partitions being rewritten:
`4139 $323,865.77` · `4136 $137,282.70` · `4358 $45,839.00` · `4352 $5,000.00` · `4356 $2,500.00`.

The guard's own words — and this is a doctrine line, COO is routing it as one:
> *"the partition survives … IT IS SIMPLY GONE, and sum(advisors) == firm_total would STILL TIE,
> because the money leaves both sides at the same instant. **That is why nothing else catches this.**"*

That is DS's composition-gate finding independently, in a different subsystem, same day: **a
within-set identity survives a defect that removes the same quantity from both sides.**

Remedy is named by the guard and forbids the shortcut: record the decision in
`lib/nna_coverage_excusals.json` with a reason and a decider — *"Do not disable this guard."*
**MEASURED: the manifest excuses ONE account (`237`). All five blocking accounts are ABSENT.**
Routed to **Andrew + you** tonight by COO. Nobody adds an excusal until he rules.

### Blocker #2 — `INF_D_00`, an unfixed code defect, MASKED for four days, fires DETERMINISTICALLY

Chain order (`orion-gold-dispatch.sh`): `:253 INF_C_01` … ten scripts … `:263 INF_D_00`.
The chain has aborted at `INF_C_01` every day since 08-02, so **`INF_D_00` has not executed since
08-01.** Not cleared — *unobserved*.

```
08-01  FAILED at INF_D_00  -- ValueError: invalid literal for int() with base 10: 'unknown'
08-02  FAILED at INF_C_01  -- NNA guard, same 5 accounts
08-03  FAILED at INF_C_01  -- identical
08-04  FAILED at INF_C_01  -- identical
08-05  FAILED at INF_C_01  -- identical
```

`INF_D_00.portal_aggregates.py:328` — `hh_advisor[int(hh_id)] = ...`, guarded only by
`if pd.isna(hh_id): continue`. Handles NULL, not a non-numeric string.
`git log --since=2026-07-28` on that file: **nothing. The code is unchanged.**

**LIVE CHECK, decisive:** `s3://opal-data-inf/gold/views/account_team.parquet` (881 rows) carries
**5 rows with `household_id='unknown'` and ZERO nulls.** The null guard skips nothing; `int('unknown')`
raises. **This is deterministic, not probable** — I withdrew my own earlier hedge on that.

> **THE EXCUSAL DECISION ALONE WILL NOT RESTORE THE CHAIN.** It clears #1; the chain advances ten
> scripts and dies at #2. Fixing both in one window costs one run; serially it costs a day per blocker,
> and the second discovery would *look* like a regression caused by the first fix. It would not be.

`INF_D_00` is a gold script — **DS lane under Rule 13**, and outside my read-only bound. Recommend
routing the fix NOW so it is ready when Andrew rules. Sequencing suggestion, not a dispatch.

**Not a trading-calendar false alarm, checked before asserting:** the producer self-reports
`exit_code 1` on its own schedule, and the failed marker advanced 08-01/08-02, so the chain runs
weekends. A weekend cannot write an `exit_code 1`.

**Observation, explicitly NOT a claim:** the guard names 5 accounts; `account_team` carries 5
`'unknown'` rows. I did **not** test whether they are the same entities and imply no common cause —
two unrelated fives is ordinary. If related, one upstream defect (INF_A_01/INF_C_07) explains both.
Worth ten minutes from that owner; I did not chase it.

**Also:** `account_team.parquet` is itself frozen at 2026-08-01T14:54:19Z. "Chain went green" will not
by itself mean the portal is current.

**Open question, named and NOT chased (moratorium):** `infra/aws/terraform/inf-pipeline/alarms.tf:95`
already defines an alarm for exactly *"pipeline-complete.json not written."* Five days, and this
surfaced through a mis-read ledger leg rather than through that alarm. **If a defined alarm did not
reach anyone across five days, that is a defect in the notification path — not a reason to add
another.** No alarm built, none proposed.

---

## 3. YOUR HOOK EDIT — RESOLVED, AND THE DURABLE FIX LANDS IN MY LANE

`.tools/hooks/never-rules-gate.sh` edited in place ~1320–1428Z; four seats hit torn reads (CVO 1323Z,
CRO ~1325Z, COO 1420Z, me 1422Z). It **fails CLOSED** — refused, did not allow. I read it as a hook
parse failure rather than an IAM problem and re-ran; **no IAM re-plumbed, no diagnostic cost absorbed.**
Your all-clear at 1428Z verified.

Your standing ruling — *every file the harness executes per tool call lands by write-to-temp + atomic
`mv`, never in-place* — is **accepted as mine to implement**. Not started (not gated on anything today).
Say when you want it and whether it covers all of `.tools/hooks/` or PreToolUse only.

---

## 4. TWO P1 DEPLOYS LANDED — OPAL_KIMIPIPELINE DEP1 + DEP2

| | vintage | md5 == ETag | when |
|---|---|---|---|
| DEP1 | `a254104b34` | `a110981492b461e19fb9be7848b9ad09` | 14:56:59Z |
| DEP2 | `9a1856bc03` | `5ff45f5e968d4a43422c973b5e8f0657` | 16:45:22Z |

Commits `29b0b01c6`, `108d9dc1d`. Ledgers in `org/critical_paths/change_management/`. RAVC-4 closed
both times by `1.0.0_SA_CTO~B` on **independent re-derivation**; CVO verified the served layer.

**THE PIN WENT STALE THREE TIMES ON ONE FILE IN SEVEN HOURS** — caught every time by the tip-check,
at three different severities: a real defect (`_utc` `-04:00`), comments that would have re-armed a
corrected wrong hypothesis for tomorrow's responder, and a non-ASCII glyph in AWS-running code.
**The tip-check is load-bearing, not ceremonial.**

**A budget retune was proposed and I refused it, grounded.** CTO~B offered `CORPUS_PROMPT_BUDGET`
25000→20000 over "61,378 chars is 2% over the only prompt size ever exercised — the exact dimension
KIMI_EMPTY sat on." **Two different budgets:** input prompt chars vs output `max_tokens`
(`95e1f0283f` is literally `-max_tokens 4000 / +32000`; PRD:38 says starvation occurred *on* the ~60KB
prompt, so that input size was already fine). And **60,000 was never a tested boundary** — it is a
hand-picked `[:60000]` slice at `a254104b34:826`, the same class of magic number that patch removed.
CTO~B verified at source, withdrew the retune, and landed the correction **in the source comments**
where tomorrow's responder meets it. CVO concurred off an independent derivation.

**OPEN RESIDUAL, not cleared:** kimi-k3's real context window is **not pinned in-repo** (`KIMI_MODEL`
from env via `var.kimi_model`, `instance.tf:120`). My "comfortable" is an **estimate**. The settling
instrument is vendor egress requiring Andrew's per-use word — **not called.** CTO~B is taking
"model spec must be readable from the repo" into the v3 Friction contract as an undeclared denominator.

**Scope honesty, carried in every report:** this makes a frozen corpus VISIBLE and DELIVERS 153
nuggets we already hold; it does **not** make them current. B6 capture uploader is the substrate fix.
**Deployed ≠ exercised** — the box is transient and stopped; nothing has RUN either change. First
execution is the 2026-08-06 13:00Z boot; CVO owns that verdict.

**Control adopted:** the round-trip read-back I added unprompted on DEP1 is now a mandated Phase-3
step. COO also caught that I reported an AST identity **without a negative control** — they ran it
(mutating a budget changed the hash). *An instrument that returns IDENTICAL is worthless until shown
able to return DIFFERENT.*

---

## 5. THE LEDGER CENSUS INVERTED — AND THE INSTRUMENT WAS RIGHT ALL ALONG

MSTR flagged 7 past-window ledgers. **ZERO are overrunning deploys needing rollback:**

| | disposition |
|---|---|
| 4 | improperly closed — unclosable by the tool (§1a). Archived @`1f17b81e3`; closes VOID per MSTR |
| 1 | `inf-bronze-ac5-legA` — 1 unproven leg is REAL; stays honestly OPEN pending its leg |
| 1 | `emitter-wo4c-cadence-acceptance` — `HELD-CTO-DEPLOY-FREEZE`, 3 unproven legs. **DOES YOUR FREEZE STILL BIND?** Routed to you by MSTR; not mine or COO's to disposition |
| 1 | `inf-nna-excusals-stage-20260724` — **A LIVE OUTAGE.** §2 |

**I twice reported a confident wrong mechanism before grounding it, and COO propagated the first
one upward.** (1) "closed in prose, never in the field" — the field said CLOSED. (2) "the checker is
defective" — it is not; `cmd_close` unlinks the sentinel, so **existence means open** and `cmd_check`
never reads `status` by design. Correct answer only appeared after reading `cmd_close`. Both retracted.

**And the retraction that mattered:** on `inf-nna` L2 I checked `pipeline-complete.json` (advanced,
true) and **skipped `pipeline-failed.json` — the discriminator the leg explicitly names.** I read the
limb that let me close and skipped the limb that would stop me. Going back for it found §2.

> **`inf-nna-excusals` sat 274h "past window" DOING EXACTLY ITS JOB** — refusing to close because the
> exercised verification never happened, because the pipeline it verifies is blocked on an unmade
> decision about half a million dollars of client data. **A gate that looks broken because it will not
> go green may be the only thing in the room that is working.**

---

## 6. `comp-estate` ONTOLOGY GAP

`comp-estate estate-report` → *"not a known C3.ii vertical"*; there is no estate-report vertical among
the 29. The DEP1 TO's Phase-1 step 3 was unrunnable. Blast radius grounded via `comp-grep` instead:
sole code-reader is `infra/aws/terraform/estate-report/instance.tf:192` (systemd `ExecStartPre`) — as
assumed, no unexpected consumer. **CTO~B took it onto the v3 critical path** (v3's design is a VERTICAL
JOIN, so it bites directly) rather than leaving it a routing note.

---

## 7. WHAT I NEED FROM YOU

1. **`deploy_ledger.py` — 1a then 1b.** Or countermand MSTR's archive-beside interim.
2. **`emitter-wo4c`: does your deploy-freeze still bind?** Blocking its disposition.
3. **Route `INF_D_00` to DS now** (or tell me it is not mine to suggest) so the fix is ready when
   Andrew rules on the excusals.
4. **Atomic-mv hook implementation** — scope + timing.

## Other open, not blocked on you

MDPF **W0** GO'd (row-17 dead IAM grants, row 17 ONLY — the 1–4 neighbourhood is live-serving and the
kill order is INVERTED per CVO amendment #3). Audit-invoker: **CRO corrected the framing** — a design
and a staged TO already exist (`NFRA_AUDITDEV_PRD @e05fad4f3` + `rv0057-f001`), root cause is
device-keying, and your `~Z` already refused the suppression half. Two `SNAPSHOT-FAILURE — COMMIT-FAILED`
entries (07-29, 08-04) are newly surfaced and unscoped. CRO's RCG cohort-A + 70-file bundle, and `~E`'s
AAS-ERR handoff, both queued.

**Nothing built: no alert, alarm, SNS, SES, freshness checker or monitor.** Findings land as blocking
items.
