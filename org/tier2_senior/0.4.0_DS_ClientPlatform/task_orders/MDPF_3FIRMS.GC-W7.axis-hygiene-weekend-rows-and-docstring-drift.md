<task_order>
<id>MDPF_3FIRMS.GC-W7</id>
<title>W-7 — Axis hygiene: 16 weekend rows on a declared trading-day axis, and a docstring claiming "427 canonical NYSE trading days" against a 447-date spine</title>
<project>MDPF_3FIRMS</project>
<workstream>Global-Count closeout — independent of W-1, mechanical, no design gate</workstream>
<issued_to>0.4.0_DS_ClientPlatform</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_at>2026-07-24T14:20Z</issued_at>
<status>staged</status>
<authorization>Andrew-direct ~1310Z at CTO's terminal -> CTO PRD @5d7522128 -> COO decomposition. SCOPE-BOUNDED to MDPF_REVAMP_GLOBAL_COUNT_CLOSEOUT W-1..W-7; the broader MDPF_3FIRMS_PRD decomposition REMAINS HELD on Andrew's word (LD-0333).</authorization>

<sequencing>
**STAGED, NOT URGENT — pick this up when your current clocks clear.** You are carrying the retry-net
implementation (0.6.2~A verifying under SoD), the 6d second-reader confirm, the third observable, and the
nm-vintage residual. **None of those wait for this.** W-7 has no clock and no dependency; it is here so the
wave's decomposition is complete and visible, not so you context-switch.
</sequencing>

<references>
  <ref type="prd">docs/architecture/MDPF_REVAMP_GLOBAL_COUNT_CLOSEOUT.md §6 W-7</ref>
</references>

<scope>
**TWO DEFECTS, ONE OF THEM PURELY DECLARATIVE.**

**(a) 16 WEEKEND ROWS ON A DECLARED TRADING-DAY AXIS.** The series declares a trading-day axis and carries
16 weekend rows. Either the rows do not belong, or the axis is not what it says it is — **and which one is
true is the actual question.** Do not assume the rows are the defect: an axis that is genuinely
calendar-day would make the DECLARATION the defect instead. Establish which before changing anything.

**(b) DOCSTRING DRIFT.** The projection docstring still claims **"427 canonical NYSE trading days"** against
a **447-date spine**. That is a stale record asserting something false with authority — the class that
costs us most, because a future reader treats it as the specification.

⚠ **NEVER#1 GOVERNS HERE MORE THAN ANYWHERE.** This TO is entirely about which dates legitimately belong on
an axis. **Resolve the trading calendar FIRST** and count in trading days, never wall-clock. `lib/trading_calendar.py`
is the ONE frontier definition (`expected_last_trading_day` / `trading_days_behind`). Market holidays are
not weekends and are not the same exclusion — enumerate both.

⚠ **EXPLICIT-Z TIMESTAMPS ONLY.** The host is UTC-4: `aws s3 ls` renders LastModified in LOCAL time and
`git log --since` PARSES local. A date-boundary question read through a local-time instrument will be
silently wrong by up to four hours — which, on a weekend-row question, moves a Friday to a Saturday.
</scope>

<explicitly_out_of_scope>
- **W-1's measurement** (which cells were missing on the 40 null dates) — that is `0.4.0_DS_ClientPlatform~A`,
  first and alone. If your axis work incidentally reveals something about the nulls, REPORT it to ~A and to
  me; do not fold it into this TO and do not let it change ~A's independent measurement.
- **W-2's composition law**, **W-3 basis coherence**, **W-6(count-reconcile)** — all held on W-1.
- The FE. `0.4.0_DE` holds W-4/W-5 under GC-W45.
</explicitly_out_of_scope>

<cross_domain_coordination>
`dim_mdpf_aggregate_aua_timeseries.py` — **`0.4.0_DS_ClientPlatform~A` is READ-ONLY on this same file for
W-1 concurrently.** You may WRITE. **MCP ~A before you commit** so their measurement is not read against a
spine you changed underneath them: a shifting axis mid-measurement would silently corrupt their 40-of-447
denominator. If your fix changes the date spine at all, ~A needs to know whether their numbers pre-date or
post-date it.
</cross_domain_coordination>

<compiler_tools_mandate>
  <before_write>`comp-pipescript io dim_mdpf_aggregate_aua_timeseries.py` — column gaps + portal consumers
    (an axis change is felt by every consumer of the series).</before_write>
  <before_commit>`comp-pipescript deployed` before any gold run; `.tools/commit-gate.sh` per Rule 14;
    `comp-validate <script> --artifact <file>` before signalling AE — and note `NO_CONFIG` / `ZERO_CHECKS`
    means UNVALIDATED, never signal SAFE on it.</before_commit>
  <after_commit>Session log with `## Compiler Tools` populated; append `org/compiler-tools-log.md`.</after_commit>
</compiler_tools_mandate>

<acceptance_criteria>
1. **A VERDICT ON WHICH IS WRONG — the rows or the declaration — with the evidence that discriminates
   them.** Stating this before any fix is the deliverable's spine. "I removed the weekend rows" without
   establishing that the axis is genuinely trading-day is an assumption, not a fix.
2. The 16 weekend rows ENUMERATED (dates listed, denominator stated: 16 of 447), with weekend and
   market-holiday exclusions counted SEPARATELY.
3. `427` vs `447` reconciled: the docstring states a number that is TRUE of the code as it then stands, with
   the resolver named. If the correct figure is neither 427 nor 447, say so and show the derivation.
4. **NEVER#4: no ad-hoc gold run to validate.** Validate on the scheduled nightly's artifacts.
5. `comp-validate` PASS/WAIVED, or an explicit statement of why it is N/A — blank is not acceptable.
</acceptance_criteria>

<deliverables>
  - The verdict + enumeration from AC-1/AC-2.
  - The code + docstring change.
  - MCP to `0.4.0_DS_ClientPlatform~A` before commit if the date spine moves.
  - Session log with `## Compiler Tools` populated.
</deliverables>
</task_order>
