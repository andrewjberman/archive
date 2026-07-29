# TAXONOMY 11 — `org/compiler-tools-log.md` (THE MONOLITH)

    size:      4,388,163 B / 27,993 lines
    span:      2026-04-09 .. 2026-07-29 (81 distinct days)
    role:      the estate's only QUANTITATIVE record of its own verification activity.
               One row per comp-tool invocation, auto-appended via .comp-graph/.agent_context
    method:    parsed programmatically (4.4MB cannot be read); aggregates below are reproducible

> **This file is not an incident corpus. It is BEHAVIOUR.** Files 01–10 record what agents *wrote
> down about being wrong*. This records what agents *actually ran*. Where the two disagree, this one
> is the less flattering and the more trustworthy — nobody curates a row they did not know was being
> written.

    PARSE: 26,235 rows | 1,055 malformed | 703 non-row lines
    Malformed rate 3.9% -- the log has its own data-quality defect. All figures below are over the
    26,235 parseable rows and are therefore a FLOOR (AXES.md scope note).

---

## 1. FINDING ZERO — THE RESULT COLUMN IS UNDEFINED, AND EVERY NUMBER BELOW INHERITS IT

Before any statistic: **`FAIL` in this log conflates at least three unrelated events.** Sampled
directly:

```
| 2026-06-26 | 3.0.0_SA_CVO   | comp-transform | comp-transform __bogus_zzz_target__      | FAIL |   <- DELIBERATE negative control
| 2026-07-10 | 3.0.0_SA_CVO~B | comp-trace     | comp-trace zzz_nonexistent_node_xyz      | FAIL |   <- DELIBERATE negative control
| 2026-07-17 | 0.8.0_AE~D     | comp-describe  | comp-describe                            | FAIL |   <- usage error, no args
| 2026-04-17 | 0.4.0_DS~B     | comp-pipescript| comp-pipescript io B_01.holdings_lots    | FAIL |   <- plausibly a REAL FINDING
```

> ## **THE ESTATE'S ONLY QUANTITATIVE RECORD OF ITS VERIFICATION ACTIVITY CANNOT DISTINGUISH**
> ## **"I PROBED WITH A BOGUS INPUT ON PURPOSE" FROM "THE TOOL BROKE" FROM "THE TOOL FOUND A DEFECT."**

This is **M5 (scalar collapse)** and the Guards law *"A NULL THAT MEANS TWO THINGS IS A LIE ABOUT ONE
OF THEM"* — committed by the log that records the estate's use of the tools that enforce those laws.
A well-run positive control and a broken tool produce the **same character string**.

**Consequence, stated plainly: no FAIL-rate figure in this file can be read as an estate-health
signal.** They are reported below because their *structure* is still informative — but any narrative
of the form "failures are falling, we are improving" is unsupported by this instrument, in either
direction.

---

## 2. BASE DISTRIBUTIONS

**Result column (n = 26,235)**

| result | n | % |
|---|---|---|
| PASS | 22,911 | **87.33%** |
| FAIL | 2,006 | **7.65%** |
| VERDICT | 499 | 1.90% |
| UNKNOWN | 75 | 0.29% |
| N/A | 44 | 0.17% |
| MIXED / REFUSE / PARTIAL / SKIPPED | 39 | 0.15% |
| (14 further one-off strings) | ~660 | 2.5% |

**Volume by month** — Apr 1,821 · May 1,397 · Jun 6,019 · **Jul 16,997**. A **9.3× rise** from April
to July.

**Agents:** 104 distinct serials. Top: `0.7.0_AE_CloudOps` 2,365 (9.0%) · `2.0.0_SA_COO` 2,230 ·
`0.4.0_DS_ClientPlatform` 2,174 · `3.0.0_SA_CVO` 1,857 · `1.0.0_SA_CTO` 1,808 · `0.0.0_AB_MSTR` 1,753.

---

## 3. THE TOOL SURFACE IS FOUR TOOLS AND A TAIL

| tool | n | % of ALL invocations |
|---|---|---|
| `comp-surface-check` | 10,224 | **38.97%** |
| `comp-pulse` | 3,383 | 12.89% |
| `comp-pipescript` | 2,792 | 10.64% |
| `comp-kuzu` | 2,592 | 9.88% |
| **TOP 4 COMBINED** | **18,991** | **72.4%** |
| `comp-iam` | 743 | 2.83% |
| `comp-blast` | 680 | 2.59% |
| `comp-system` | 628 | 2.39% |

**The long tail, measured against 551 distinct tool-name strings:**

| names used ≤ N times | count of names | % of all names | % of all volume |
|---|---|---|---|
| ≤ 1 | **437** | **79.5%** | **1.67%** |
| ≤ 5 | 482 | 87.6% | 2.15% |
| ≤ 50 | 526 | 95.6% | 5.46% |

> **79.5% of distinct tool-name strings appear exactly ONCE, and together account for 1.67% of all
> activity.** (Some are certainly parse artifacts and subcommand variants — this is a floor on
> concentration, not a precise tool census.) **The estate reasons about itself as a ~60–93-tool
> platform. Behaviourally it is four tools carrying three quarters of all use.**

**Attribution:** **61.47%** of rows carry no task-order (`(no-TO)`). Most tool use is not attributable
to any commissioned work. **`--help` invocations: 2.32%** — exploration is a rounding error; agents
run tools they already know.

---

## 4. THE FRICTION RANKING (FAIL rate by tool, n ≥ 100)

| tool | n | FAIL | rate |
|---|---|---|---|
| `comp-drift` | 111 | 45 | **40.54%** |
| `comp-validate` | 254 | 83 | **32.68%** |
| `comp-xref` | 106 | 27 | 25.47% |
| `comp-transform` | 394 | 91 | 23.10% |
| `comp-lambdamap` | 145 | 30 | 20.69% |
| `comp-pipescript` | 2,792 | 567 | 20.31% |
| `comp-blast` | 680 | 116 | 17.06% |
| `comp-aws` | 241 | 41 | 17.01% |
| `comp-pulse` | 3,383 | 358 | 10.58% |
| `comp-kuzu` | 2,592 | 240 | 9.26% |
| `comp-iam` | 743 | 32 | 4.31% |
| `comp-routes` | 414 | 6 | 1.45% |
| **`comp-surface-check`** | **10,224** | **15** | **0.15%** |

---

## 5. ★ THE DECLINE IS A COMPOSITION ARTIFACT — CAUGHT BY THE DOCTRINE'S OWN RULE

**The encouraging headline:**

| month | n | FAIL | rate |
|---|---|---|---|
| 2026-04 | 1,821 | 221 | 12.14% |
| 2026-05 | 1,397 | 178 | 12.74% |
| 2026-06 | 6,019 | 563 | 9.35% |
| 2026-07 | 16,997 | 1,044 | **6.14%** |

Weekly it looks even better: 11.73% (Apr 13) → 4.46% (Jul 20) → 0.51% (Jul 27, partial).

**`CONTROLS_OVER_CARE.md` §III-b corollary forbids grading an aggregate on its total: *"diff every
parallel series an aggregate publishes … require each to move on its own. Offsetting moves are the
target, not the noise."* Applying its own rule to the estate's own telemetry:**

**MIX SHIFT — share of monthly volume**

| tool | Apr | May | Jun | Jul |
|---|---|---|---|---|
| `comp-surface-check` (0.15% FAIL) | 0.0% | 0.0% | **49.9%** | **42.5%** |
| `comp-pulse` (10.58% FAIL) | 0.0% | 0.0% | 0.0% | 19.9% |
| `comp-pipescript` (20.31% FAIL) | **51.2%** | 36.1% | 13.9% | **3.0%** |

**SAME-TOOL FAIL RATE — holds the mix constant**

| tool | Apr | May | Jun | Jul |
|---|---|---|---|---|
| `comp-pipescript` | 13.83% | 24.55% | 28.91% | 13.93% |
| `comp-blast` | 0.99% | 0.00% | 15.38% | **37.88%** |
| `comp-iam` | 0.00% | 0.00% | 6.60% | 5.43% |
| `comp-kuzu` | — | — | 12.75% | 7.97% |
| `comp-surface-check` | — | — | 0.33% | 0.07% |

> ## **THE AGGREGATE IMPROVED WHILE SEVERAL CONSTITUENT SERIES GOT WORSE.**
> `comp-blast` went **0.99% → 37.88%**. `comp-iam` went **0.00% → 5.43%**. `comp-pipescript` is
> **no better than April**. The headline fell because a near-always-PASS tool
> (`comp-surface-check`, 0.15%) went from **0% to ~43–50% of all volume**.
>
> **This is exactly the defect §III-b was written to name — a clean headline over offsetting moves —
> and it is sitting in the estate's own behavioural record, unexamined, for three months.**

---

## 6. ★ THE MOST-RUN TOOL IN THE ESTATE FAILS 0.15% OF THE TIME

`comp-surface-check`: **10,224 invocations (39.0% of ALL comp-tool activity), 71 distinct agents,
15 FAILs.**

**All 15 FAILs, in full:**

```
2026-06-12  comp-surface-check selfcheck                          <- self-test
2026-06-12  comp-surface-check check --file portal/.../aum.ts
2026-06-12  comp-surface-check check --file .../BenchmarkHeatmap.tsx
2026-06-12  comp-surface-check --list-watched-files               <- usage
2026-06-16  comp-surface-check check --file .../aum.ts --mode blocking   (x2)
2026-06-17  comp-surface-check                                    <- bare, usage error
2026-06-17  comp-surface-check                                    <- bare, usage error
2026-06-22  comp-surface-check                                    <- bare, usage error
2026-06-26  comp-surface-check __bogus_subcmd_zzz__               <- DELIBERATE probe
2026-07-01  comp-surface-check   (x2)                             <- bare
2026-07-07  comp-surface-check   (x3)                             <- bare
```

**At most 3 of 15 are substantive.** The rest are bare invocations, `--help`-class usage, a
self-test, and one deliberate bogus-subcommand probe.

**Two readings, and I cannot discriminate them from this log alone:**
1. the estate's critical surfaces are genuinely clean, and 10,224 clean runs are 10,224 true negatives; or
2. the check is near-vacuous on the workspace side, where **CLAUDE.md states it is ADVISORY and cannot block**.

**What the log CAN establish:** the estate spends **39% of all measured verification effort** on a
tool whose result column has moved off PASS **15 times in four months**, and whose workspace-side
verdict cannot stop a commit. **`CONTROLS_OVER_CARE.md` §I opens with *"A CONTROL THAT CANNOT FAIL IS
NOT A CONTROL. Before recording a PASS, ask: could this have failed?"* That question has never been
asked of the estate's most-run tool.**

*(Fair statement of the other side: the portal-side invocation IS blocking — `rc=2 BLOCKED`, hook
refuses — per CLAUDE.md's 2026-07-24 correction. This log cannot separate portal-side from
workspace-side calls, so the 0.15% is over both.)*

---

## 7. PER-AGENT VARIATION (n ≥ 400)

| agent | n | FAIL |
|---|---|---|
| `0.4.0_DS_ClientPlatform` | 2,174 | **14.26%** |
| `0.0.0_AB_MSTR` | 1,753 | 11.75% |
| `0.8.0_AE_CloudComp~B` | 714 | 9.94% |
| `3.0.0_SA_CVO` | 1,857 | 7.92% |
| `0.7.0_AE_CloudOps` | 2,365 | 7.86% |
| `1.0.0_SA_CTO` | 1,808 | 6.86% |
| `3.0.0_SA_CVO~Z` | 552 | 3.62% |
| `2.0.0_SA_COO` | 2,230 | **2.96%** |
| `0.8.0_AE_CloudComp~C` | 679 | 2.21% |

**A 6.5× spread.** **DO NOT read this as an agent-quality ranking** — it is confounded by tool mix
exactly as §5 is. An agent who runs mostly `comp-surface-check` (0.15%) will outperform one who runs
mostly `comp-pipescript` (20.31%) with no difference in competence. **The same composition trap,
one axis over.** Reported here so that nobody later computes it and reads it as performance.

---

## 8. WHAT THIS FILE PROVES THAT THE DOCTRINE CANNOT

| finding | why only this file can show it |
|---|---|
| **Verification effort is concentrated 4:551** | no narrative records what agents *didn't* reach for |
| **The improvement narrative is a mix artifact** | requires 26k rows and a per-series decomposition |
| **39% of effort goes to a near-always-PASS advisory check** | no incident write-up would ever record a tool that keeps passing |
| **61% of tool use has no task-order** | invisible from any curated record |
| **The result column is semantically undefined** | only visible by sampling raw rows across tools |

> **The doctrine corpus is a museum of the times agents were wrong. This log is the record of what
> they habitually DO — and its two loudest signals (concentration, and a headline improving while its
> parts worsen) are both invisible from the doctrine tier.**

---

## 9. PRUNE VERDICT

**This is NOT a prune candidate in the doctrine sense — it is an append-only telemetry stream.** But
Andrew's underlying question ("is this monolith worth its weight?") has a measured answer:

| move | rationale |
|---|---|
| **KEEP the stream; it is the only behavioural record the estate has** | §8 |
| **FIX THE RESULT COLUMN — the highest-value single change in this analysis** | split `FAIL` into `TOOL-ERROR` / `NEGATIVE-CONTROL` / `FINDING`. Without it every number here is uninterpretable, and the estate cannot answer "are we getting better?" at all |
| **FIX the 3.9% malformed rate** | 1,055 rows are unparseable; a telemetry stream that cannot be parsed is a diary |
| **ROTATE by month** | 4.4MB single file; it blocked an Andrew-ordered `git pull` today because two auto-appended rows collided |
| **DO NOT delete history** | the composition finding in §5 required all four months |
| **STOP hand-committing rows** | Andrew banned this churn 2026-07-29; the appends are hook-generated and should ride a peer commit, never their own |

**AND ONE OPEN ITEM FOR THE OWNER (not actioned here):** ask of `comp-surface-check` the question
§I of the doctrine demands — *could it have failed?* If a mutant surface violation does not turn it
red on the workspace side, then 39% of the estate's measured verification effort is a control that
cannot fail, and the doctrine's own first law applies to it.
