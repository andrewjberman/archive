# CHARTER SITEZ_F001 -- The governance layer reads records that are device-local. Close the gap.

    from:      0.0.0_AB_MSTR~Z (Tier-0 charter)
    to:        1.0.0_SA_CTO~Z (Tier-1, site Z)
    authority: Andrew-direct ~1945Z 2026-07-29 -- "spawn a ~Z agent to work the F-001 audit gap"
    source:    org/tier0/reviews/RV-0057.md  F-001 + F-002 + Amendment 1b

**THIS IS A CHARTER, NOT A TASK ORDER, AND THE DISTINCTION IS THE GATE'S DOING.** I first wrote it
into `org/tier1_exec/1.0.0_SA_CTO/task_orders/` and the owned-paths gate refused: that path is lane
`ANY_EXEC` and `0.0.0_AB_MSTR~Z` is not a permitted agent. **The gate is right and I was wrong** --
Constitution Art. VI and the `/mstr-spawn` skill both say MSTR provisions and charters while the
substantive TO authoring stays at Tier 1. I walked past my own skill's discipline note.

**CTO~Z: decompose this into your own TO in your own folder, which you ARE permitted to write.**
Scope, criteria and anti-goals below are the charter; the TO shape is yours.

<issued_to>1.0.0_SA_CTO~Z</issued_to>
<issued_by>0.0.0_AB_MSTR~Z (Andrew-direct, ~1945Z 2026-07-29: "spawn a ~Z agent to work the F-001 audit gap")</issued_by>
<date>2026-07-29</date>
<status>pending</status>
<go>GO IS LIVE. This is your first item; begin on read. Andrew tasked it directly and it is SITE-Z SCOPED -- run it here, do NOT route any part of it into the laptop fabric (his standing rule ~1815Z: "you do not send work to the main fabric ... run these projects off your own ~Z spawns"). Coordination messages to base MSTR are fine; work dispatch is not.</go>
<project>NFRA (governance-records portability). Source finding: `org/tier0/reviews/RV-0057.md` F-001 + F-002.</project>

## THE FINDING, ALREADY MEASURED -- DO NOT RE-MEASURE IT

Re-deriving this is the circling Andrew named. It is measured, positive-controlled, and committed
at `00f876caa` / `8519ff817`. Take it as given and start from the fix.

**`.gitignore:68` is a blanket `*.log`.** Every audit log is therefore device-local and untracked,
while the governance processes that consume them are git-shared. Consequences, all measured on
site Z 2026-07-29:

| instrument | laptop | site Z |
|---|---|---|
| `org/git-author-override-audit.log` all-time | 17,174 lines (RV-0056, 07-28) | **73 lines** |
| same, in the RV-0057 window | 570 | **0** |
| serials present | fabric-wide | **`0.0.0_AB_MSTR~Z` + `1.0.0_SA_CTO~Z` only** |
| earliest line | -- | `2026-07-29T01:50:20Z`, ~11h AFTER the window opened |

**And it is not only logs. `memory/` has ZERO tracked files in ALL of git history**
(`git ls-files memory/` = 0; `git log --all --name-only | grep '^memory/'` = 0). Positive control:
the same `find` locates `CLAUDE.md`, so the method is sound. **CLAUDE.md cites `memory/` paths as
the durable record behind live NEVER-rules** -- `feedback_trading_calendar_before_staleness_tminus1_default.md`,
`feedback_silver_no_field_slimming.md`, `feedback_commit_only_flag.md` -- and **all three are absent
here.** From site Z the law points at evidence that never entered git.

## WHY IT MATTERS, AND IT IS NOT "WE LOSE SOME LOGS"

**Every one of these instruments fails toward the CLEAN answer.**

1. **`/mstr-review` cannot perform its Step-2 audit walk from site Z** -- and its Step-4
   `ACCEPTED-PROXY` gate is conditioned on *"no overrides."* From here that reads TRUE **always**,
   so a site-Z review would **always self-accept**. The gate that exists to force a window to
   Andrew/CVO is disarmed by the device it runs on.
2. **The Tier-1 liveness check is worse than blind -- it is actively harmful.** `liveness.json` is
   device-local too, so a naive pass finds 6/6 canonical Tier-1 serials absent, raises a
   fabric-wide `liveness_gap`, and reaches for its prescribed remediation: **`spawn-agent.ps1`**.
   **A false negative whose remediation WRITES.** It would spawn duplicate Tier-1 agents against
   serials already live on the laptop.
3. **`audit-archive-invoker` is already contaminating the shared record** (RV-0057 F-002). It
   diffs **git-tracked** baselines against **gitignored** logs, so off the minting device every
   covered log diverges at line 1 *by construction* and is classed `NON-APPEND-EDIT` -- the tamper
   class, action *"needs human authority ruling."* Two false batches are already committed to
   `org/audit/archive/FINDINGS.md` by `~Z` sessions: `426da9d8e`, `4982db745`. Clause 2 also
   freezes the baseline, so site Z re-emits them every startup, forever.

**A tamper detector that fires falsely on an entire device trains its readers to dismiss it.**

## THE ONE THING YOU MUST NOT DO

**Do not conclude that the whole class is a benign device artifact.** RV-0057 Amendment 1b exists
precisely to stop that: `1.0.0_SA_CTO~B` independently reported the same `NON-APPEND-EDIT` on
`git-author-override-audit.log` at **`1696149B -> 12917B`, diverging at byte one**, and filed it
**UNOWNED**. **`~B` is on the LAPTOP** -- proven: its 5 in-window commits land 17:02Z-17:41Z UTC and
are absent from site Z's override log, which covers 01:50Z-17:33Z UTC. So a ~1.7MB log collapsed to
~13KB **on the primary device**, which the device-portability mechanism does **not** explain.

**A tidy explanation is exactly what invites someone to skip the residue. A false all-clear on
audit integrity is worse than the false alarm, because nothing later re-raises it.** Treat that
laptop-side truncation as OPEN and unexplained. If you cannot determine it from site Z -- you
probably cannot -- say so and leave it open rather than absorbing it.

## SCOPE

**IN:**
1. Rule on what SHOULD be durable and shared vs legitimately device-local. Not everything belongs
   in git; a per-device operational log may be correctly local. **The defect is the MISMATCH** --
   a shared consumer reading a local producer -- not locality itself.
2. For records that must be shared: the mechanism. `.gitignore` carve-outs, a consolidation step,
   per-device namespacing (`<log>.<device>.log`), or something better. Prefer the option that makes
   the failure LOUD over one that makes it rare.
3. Fix the instruments that currently fail clean: `/mstr-review` Step 2 + Tier-1 liveness must
   report UNMEASURABLE rather than a zero when their inputs are not present. **That half is worth
   more than the consolidation** -- an instrument that knows what it cannot see is safe on any
   device; a consolidated log that silently regresses is not.
4. `audit-archive-invoker`: device-scope the INTEGRITY clause, and retract the two false batches.
5. The `memory/` dangling-citation problem: CLAUDE.md's cited evidence must resolve, or the
   citations must change. **Ruling only -- do not bulk-commit the laptop's `memory/` from here;**
   you cannot see it, and base MSTR holds those bytes.

**OUT:**
- **No alerts, alarms, SNS, SES, freshness checkers or monitors.** Standing moratorium
  (CLAUDE.md, Andrew-direct 2026-07-28). This is a records-plumbing and instrument-honesty item;
  if you find yourself designing a notifier you have left scope.
- No changes to laptop-side state. No dispatch into the main fabric.

## ACCEPTANCE CRITERIA (machine-checkable, not "code runs")

- [ ] `/mstr-review`'s audit walk, run on site Z, either **reads the fabric's real override
      history** OR **returns an explicit UNMEASURABLE/BLIND verdict**. A silent `0` is a FAIL.
- [ ] Same for the Tier-1 liveness check: it must be structurally unable to emit a
      `liveness_gap` it cannot substantiate, and must never reach `spawn-agent.ps1` off a
      device-local read.
- [ ] `audit-archive-invoker` on site Z emits **zero** `NON-APPEND-EDIT` findings attributable
      solely to device-locality, **exercised** (run it), not config-read.
- [ ] The two false FINDINGS.md batches are retracted in-record.
- [ ] Every `memory/` path cited in CLAUDE.md either resolves on this device or the citation is
      corrected. Enumerate them; print the denominator.
- [ ] The laptop-side `1696149B -> 12917B` truncation is either explained with evidence or
      explicitly recorded as OPEN and unexplained. **Absorbing it into the device story is a FAIL.**

<compiler_tools_mandate>
BEFORE WRITE: `comp-which` to route; `comp-grep` for the consumer census of any log or record you
propose to move -- **who reads this, and would they notice if it were empty?** That census is the
step that does the work (`/prune-quant` doctrine).
BEFORE COMMIT: `.tools/commit-gate.sh` on any `.py`; `comp-blast` before deleting or relocating any
record file.
AFTER COMMIT: re-run the instrument you fixed and paste its OUTPUT, not its rc. Rule 22a: a
config-read cannot support a behavioral claim.
</compiler_tools_mandate>

<cross_domain_coordination>
`audit-archive-invoker` is owned by `0.7.0_AE_CloudOps` and gated by base `1.0.0_SA_CTO` -- both on
the laptop and both OUT OF REACH under Andrew's standing rule. **Do not dispatch to them.** Design
and land the site-Z-side fix; where a change would bind laptop-side owners, produce the RULING and
route it to base MSTR as COORDINATION for custody. `.gitignore` is a shared file -- a change there
affects every agent on both devices, so it is the one edit that needs base MSTR's ack before
landing, not after.
</cross_domain_coordination>

<deliverables>
1. The fix, landed and exercised on site Z.
2. A ruling doc on durable-vs-device-local for governance records.
3. A session log with a populated `## Compiler Tools` section (blank/N-A not acceptable).
4. Report to `0.0.0_AB_MSTR~Z`; base MSTR holds record custody for anything crossing to the laptop.
</deliverables>
