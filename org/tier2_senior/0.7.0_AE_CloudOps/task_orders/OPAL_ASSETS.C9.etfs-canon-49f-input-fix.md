# OPAL_ASSETS.C9 — Fix the 49F ETFS_CANON input (frozen 2026-06-24): GROUND THE MECHANISM FIRST

<issued_to>0.7.0_AE_CloudOps</issued_to>
<issued_by>2.0.0_SA_COO (coordination lane, Andrew-direct ~01:07Z) — authored from PRD v1.3.1 §4 row C9 + master plan §1 row 8; architecture owner remains 1.0.0_SA_CTO</issued_by>
<date>2026-07-14</date>
<status>phase-a-DELIVERED--phase-b-rec-at-CTO-gate</status>
<phase_a_delivery date="2026-07-14 ~05:00Z" msg="20260714T050046Z">
GROUNDED, source-confirmed: THE INPUT NEVER DIED. Producer bd-49f-etf-ownership-daily is a DESIGNED
manual-monthly-batch Lambda (its own source :22-29: "Trigger: none scheduled (monthly batch). Invoke
per-batch"); NO resource policy exists (nothing CAN invoke it but a hand); last hand-run batch 06-25.
The fan-in is healthy + honest (re-upserts the latest slice with true vintage labeled). No INF resource
in the path -- advancing the input cannot advance the held chain. Staleness calendar-resolved: input 13
trading days behind, its RPS source 6. Row 8's "its input died" = a designed cadence mistaken for an
outage (the TO's named trap, second form). PHASE-B REC at CTO's gate: (a) GO-narrow -- per-date manual
invokes as designed (13 -> 6 today; moves served internal numbers, hence gated); (b) producer cadence ->
OPAL_RUNNERS scoping (the monthly-batch premise dissolves under the both-masters daily REST schedules).
</phase_a_delivery>
<sovereign_lift date="2026-07-14 ~03:3xZ" channel="Andrew -> COO, interactive" recorded_by="2.0.0_SA_COO">
ANDREW, VERBATIM: "Oh that is retarded, 49 is back on the menu now, take the sovereign block off
completely, that is no excuse to not verify the work."
EFFECT ON THIS TO: the HELD-SOVEREIGN status below is LIFTED. The 2026-07-09 prohibition (49F / Schwab /
RPS / data/black_diamond/ / opal-data-bd / bd custody) is OFF COMPLETELY — verification work in those
domains is not merely permitted, it is DEMANDED. Phase A's grounding now COMPLETES properly: read the bd
producer's source, resolve the input staleness on real artifacts (trading-calendar first, NEVER#1),
ground the stop mechanism per Rule 22. Phase B (the fix) is then scoped on that real grounding through
CTO's Rule-22 gate AS NORMAL WORK — the domain block is gone; the engineering rules are not.
STILL STANDING, DO NOT OVER-READ THE LIFT: the INF chain hold (Door 5, the frozen 3, mdpf freeze, Door 6,
the time-lock stamp order) is a SEPARATE hold with its own mechanism and is UNCHANGED. The 0824/0833
never-summed ruling stands (data-grain, "summing is a presentation question"). Bronze never rewritten in
place stands (17a). No ad-hoc gold runs to validate stands (NEVER-rule). Vendor egress rules unchanged.
The Phase-A stop below remains a correct record of the world as it was when taken.
</sovereign_lift>
<phase_a_outcome date="2026-07-14 ~03:19Z" by="0.7.0_AE_CloudOps" closed_by="2.0.0_SA_COO">
**THE STOP CONDITION FIRED ON THE FIRST GROUNDING PASS — this TO's predicted outcome, delivered.**
The 49F input's mechanism traces into THREE sovereign-prohibited domains at once: its producer is
`bd-49f-etf-ownership-daily-canonical` (bd-custody), the fan-in's 49F path reads
`avgcap_bd_rps_recon.py` (bd + RPS), and the subject is the 49F leg (49F). Grounded from filename
listings and one in-bounds etfs-side file — ZERO bd source reads, ZERO bd bucket access, staleness
deliberately NOT resolved to the trading day (an accurate count would itself be a bd verify; the DOMAIN
was the question and it is answered). The functional test lands the same place: reviving the input
re-derives served 49F figures — "no served re-derive," ruled out of scope three times.
**FINDING: the master plan's "FIX THE 49F INPUT" remedy is a HYPOTHESIS that turns out to be somebody's
HOLD wearing a defect's clothes. The input is frozen because its producer sits in a domain no agent is
authorized to run — that is the hold WORKING, not a defect. A frozen-known input in a held domain is
strictly safer than a producer nobody is cleared to touch (the LD-0292 class).**
**PHASE B IS HELD-SOVEREIGN — NOT parked, NOT pending-CTO, NOT resumable on any GO below Andrew.**
The fix is not in OPAL_ASSETS scope (a TO's filing does not relocate the estate it touches); reviving the
49F ETF-ownership leg needs ANDREW'S EXPLICIT ASK with its own scope ruling on the "No 49 Yet" line.
CTO may validate the grounding; he cannot GO the fix. Routed to Andrew's board 2026-07-14 ~03:2xZ.
</phase_a_outcome>
<project>OPAL_ASSETS — Grand Consolidation P2</project>
<prd>docs/architecture/OPAL_ASSETS_CONSOLIDATION_PRD.md §4 row C9 — authored against v1.3.8 @ a0ed08933; evidence base: master plan §1 matrix row 8 (9ce5b6841, measured live 2026-07-13)</prd>
<sequence>THIRD in your lane (C1 → C2 plans → this). Phase A below is READ-ONLY and may interleave with C1/C2 waiting-on-gates time. Phase B is SEPARATELY GATED — see below. P2: "as gates clear," per CTO's GO order.</sequence>

## What is known (measured, master plan §1 row 8 — and nothing more)

```
ETFS_CANON fan-in   per-partner ETF ownership (DERIVED — gold rows, not bronze)
  produces          etf_*__held_{partner} × 3 partners, + FLOAT residual
  the fan-in        RUNS — cron(45 15)Z, healthy
  its 49F INPUT     FROZEN since 2026-06-24 (~12 trading days at measurement, 07-13)
  remedy (plan)     "FIX THE 49F INPUT (the fan-in runs; its input died)"
```

**That is the SYMPTOM, whole and entire. The MECHANISM — what the 49F input actually is, who produces
it, and why it stopped on 06-24 — is NOT ESTABLISHED anywhere in the record.** This TO is structured
around that gap, deliberately.

## Phase A — GROUND THE MECHANISM (read-only; no fix, no writes, no deploys)

Rule 22 verbatim: **a causal claim is a HYPOTHESIS until source/graph-confirmed, and a hypothesis CANNOT
authorize a fix.** Live/served state grounds *what* (the input froze 06-24); only SOURCE + the dependency
graph grounds *why*. Deliver, with citations (`file:line @ <commit-ish>` or comp-tool + output, vintage
stated, denominators printed for every scan you reason from):

1. **What the 49F input IS:** the exact artifact/key/table the fan-in reads for the 49F leg — from the
   fan-in's SOURCE, not from its name or from memory.
2. **Who WROTE it last** and through what path (producer, schedule/trigger, role) — and what that
   producer's state was on 2026-06-24 vs now.
3. **Why it stopped:** source-confirmed. "proof / root cause / definitively" are RESERVED WORDS — legal
   only on a SOURCE-CONFIRMED claim. If you cannot confirm, say `INFERRED` and say what would confirm it.
4. **The blast map of the candidate fix:** `comp-blast` on the fan-in + the input's producer; who else
   reads that input; what the fan-in has been DOING for 12+ trading days without it (erroring? serving a
   stale leg? substituting?) — that behavior is load-bearing for whether a revived input changes served
   numbers.
5. **The trading calendar resolved FIRST** (NEVER#1) on every staleness statement you make.

**⚠ THE PRIOR ON THIS ONE IS DANGEROUS, AND YOU SHOULD KNOW IT BEFORE YOU START:** 06-24 sits in the
49F/SmartX estate where several producers were deliberately stopped, held, or superseded — the frozen
mdpf, the disabled SmartX export trigger (deliberate retirement, §1 correction 2), the sovereign "No 49
Yet" hold, the laptop-era ETF gaps. **A frozen input in THIS neighborhood has a real chance of being
somebody's HOLD wearing a defect's clothes — and "the fan-in runs, its input died, FIX THE INPUT" is
exactly the diligent-agent shape that walks through a held door.** The master plan's remedy line is a
HYPOTHESIS from a status matrix, not a diagnosis. If the mechanism turns out to be a deliberate stop, a
held domain (mdpf / INF / `wsb_49f_*` / bd), or anything whose revival would ADVANCE the held INF chain
or re-derive 49F served figures — **Phase A's deliverable is that finding, routed, and this TO's "fix"
never happens in its planned form.** That outcome is a SUCCESS of this TO, not a failure.

## Phase B — THE FIX (separately gated; do not begin on your own judgment)

Phase B starts ONLY after: Phase A's grounded mechanism is delivered to COO → CTO **validates the
grounding and rules the fix in-scope** (Rule 22's gate: the dispatch owner withholds the GO until the
causal claim cites its grounding) → COO relays the Phase-B GO. Then:
- The fix is scoped to the INPUT (pull/land/bronze-class repair) per the master plan remedy — riding the
  OPAL_ASSETS lift ONLY.
- Every deploy: Terraform via `safe-apply`, CTO apply gate, layers, source map, sizing, tag.
- No new alarms/watchdogs (§0's constraint binds).

## Fences

- **49F-adjacent.** "No 49 Yet": no 49F gold-runner build, no served re-derive, no reconciliation of 49F
  figures against each other (ruled out of scope three times). ⛔ Never compute a combined 0824+0833
  total. `wsb_49f_smartx_model_aua.py` untouched.
- **The functional test on every action:** *"would doing this ADVANCE the INF chain?"* — not "does it
  say INF." mdpf stays frozen (frozen-known-wrong is STRICTLY SAFER than unheld — LD-0292). Door 6
  (`opal-data-inf/gold/meta/pipeline-complete.json`) is never written; its ETag baseline
  `fbcddcbf4d9370310e0e5dccbbaa3efd` is the tripwire.
- The frozen 3 untouched: `build_assets_dim.py` · `_orion_api_silver_lib.py` ·
  `convert_transactions_to_silver.py`. The freeze is TWO-AXIS: not only "does this touch them" but
  **"does this turn a RED guard GREEN?"**
- `opal-data-cot` — the ETFS_CANON fan-in is the one-way fan-in PRECEDENT: reads cot, never writes it.
  Whatever the fix is, that direction survives it.

## <compiler_tools_mandate>
Phase A: `comp-blast` on the fan-in function + the input's producer (function names, not script names);
`comp-kuzu` / `pipescript` for the lineage (read the provenance header; state the vintage); every raw
inspection carries its `# rail-checked:` marker or goes through comp-grep.
Phase B (if GO'd): `comp-pipescript deployed` before any run; `comp-iam service <lambda>` on any new
boto3 surface (necessary-not-sufficient; live simulate per 22a for any new resource); `commit-gate.sh`
automatic.
</compiler_tools_mandate>

## <cross_domain_coordination>
- The fan-in's other two partner legs + FLOAT residual are LIVE AND SERVING — a fix to the 49F leg must
  not perturb them (comp-blast evidence, and Phase A item 4 exists to establish this).
- mdpf / INF / `wsb_49f_*` / bd-custody — held domains; if the mechanism traces into any of them, STOP at
  the finding and route (Phase A note above).
- `opal-data-cot` — read-only relationship preserved.
</cross_domain_coordination>

## <acceptance_criteria>
Phase A (this TO's guaranteed deliverable):
1. The 49F input identified at source: artifact/key + reader `file:line @ commit` + producer + its
   schedule/trigger state, quoted live.
2. The stop mechanism: SOURCE-CONFIRMED cause, or an explicit `INFERRED` with the confirming test named.
   No reserved words on unconfirmed claims.
3. The 12-trading-day behavior of the fan-in without the input, measured on its artifacts (what did the
   3 partner legs + FLOAT actually serve?), calendar-resolved.
4. A written GO/NO-GO recommendation for Phase B with the blast map — routed to COO, unadjudicated.
Phase B (only if CTO GOs it):
5. The input flowing again: fresh partitions landed, head-object verified, denominators printed; the
   fan-in's next SCHEDULED run (never an ad-hoc trigger — NEVER-rule) consumes it and the 49F leg
   updates while the other legs are byte-stable vs their prior run.
6. Session log with Compiler Tools section. RAVC close to COO.
</acceptance_criteria>

## RAVC
ACK to COO. Phase A evidence to COO; I route the Phase-B gate to CTO. If at any point the mechanism
touches a held domain, the report comes to me THE SAME TURN — that is a finding, not a detour.
