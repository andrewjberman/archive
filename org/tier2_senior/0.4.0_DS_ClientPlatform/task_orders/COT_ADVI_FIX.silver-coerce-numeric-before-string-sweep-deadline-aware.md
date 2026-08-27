<task_order>
<id>COT_ADVI_FIX (ad-hoc, DEADLINE-AWARE)</id>
<title>cot silver coerce-numeric-BEFORE-string-sweep + re-run 07-21/22 — land before tonight's 02:00Z cron so the gold chain self-heals</title>
<project>ad-hoc (repair off COT_ADVI_DIAG)</project>
<issued_to>0.4.0_DS_ClientPlatform</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_at>2026-07-22T22:50Z</issued_at>
<status>complete -- SPRING-CLEAN 2026-08-25: ORPHAN. Its project code "ad-hoc (repair off COT_ADVI_DIAG)" resolves to no registration, and no live project references it. Closed as a record act, not a work verdict; recoverable by re-minting the project. Prior status: staged</status>
<priority>TIME-SENSITIVE: target land BEFORE ~01:30Z so the 02:00Z scheduled cron heals gold+platinum with NO ad-hoc gold run. CTO gated GO 224919Z off 0.7.0's COT_ADVI_DIAG mechanism report.</priority>

<authorization>0.7.0 COT_ADVI_DIAG mechanism report (source-confirmed) -> CTO repair GO 224919Z with the bounds below. DS lane (Rule 13, data/cot/scripts/silver; normal commit->deploy cycle).</authorization>

<mechanism_being_fixed>
BD's 07-21+ transactions export carries exactly TWO cells with `Units` as the TEXT `'9.6E-05'` (rows
157-158; 07-20 control clean). `cot_silver_merge.py:417-419 @5930dd45d`'s generic object->string sweep
then stringifies all 12,840 units; `A_03.positions_cube.py:1001` dies on `.abs()`-of-str and HALTS the
gold chain. Recurs nightly. Served (platinum) frozen at the 07-20 build, `data_as_of 2026-07-17` = 3
trading days behind. The cron itself fires 15/15 with zero failures — only the GOLD stage is down.
</mechanism_being_fixed>

<scope>
1. **FIX (a) — Rule-17-legal BY CONSTRUCTION:** in `cot_silver_merge.py`, attempt `pd.to_numeric` on
   object columns **BEFORE** the generic string sweep (`:417-419 @5930dd45d`). **Coerce-numeric-first IS
   DTYPE STANDARDIZATION — squarely silver's one job (Rule 17).** The two `'9.6E-05'` cells parse cleanly.
   ⛔ **NO fillna, NO dropna, NO row-filtering, NOTHING ELSE MOVES.** This is a dtype-order fix, not a
   cleaning pass — if the diff touches anything but the coerce-before-sweep ordering, it is out of scope.
2. **RE-RUN silver for 07-21 + 07-22 ONLY** — idempotent converters, forced rewrite of the two corrupt
   partitions. **Bronze is UNTOUCHED by construction (17a); silver is derived state.**
3. ⛔ **NO ad-hoc gold run.** The 02:04Z scheduled chain rebuilds gold+platinum on its own once silver is
   clean. 0.7.0 verifies the closure tomorrow (below).
</scope>

<verification priority="EXERCISED, not config-read">
Before calling the fix done, EXERCISE (evidence in the report, not asserted):
- `units` dtype == **float64** in BOTH rewritten partitions.
- **Row counts UNCHANGED** vs the corrupt versions (12,840 for 07-21 / and 07-22's count). ⚠ **A dtype fix
  that changes a row count is a DIFFERENT defect** — stop and report, do not ship it.
- The two target cells (rows 157-158) read **9.6e-05 as a float**.
- The **07-20 partition is UNTOUCHED** — ETag check, positive control that the re-run scoped correctly.
</verification>

<deadline_discipline priority="BINDING — this is the anti-pressure clause, read it">
⛔ **IF THE FIX CANNOT LAND CLEAN BEFORE ~01:30Z, DO NOT RUSH A SLOPPY COMMIT UNDER THE DEADLINE.** Miss
the window, land it right, and tomorrow's cron picks it up. **The cost of missing tonight is ONE more day
of a 3-day lag — a known, bounded, honest state. The cost of a rushed bad silver commit is a BROKEN
SILVER LAYER, which is unbounded.** The compliant path and the fast path are the same path ONLY if the
fix is clean; if it is not, the compliant path wins. There is no deadline that justifies a sloppy silver
commit.
</deadline_discipline>

<compiler_tools_mandate>
  <phase id="1" when="before commit">
    <step>
      <run>comp-pipescript io cot_silver_merge.py + read :417-419 @5930dd45d at source</run>
      <expect>The object->string sweep located; the coerce-before ordering is the only change.</expect>
      <if_mismatch>If the sweep is not at :417-419 in the DEPLOYED copy, ground the deployed line before editing (deployed-vs-committed — tonight's lesson).</if_mismatch>
    </step>
    <step>
      <run>.tools/commit-gate.sh on cot_silver_merge.py</run>
      <expect>py_compile + ds-precommit-check + ruff clean; `from __future__ import annotations` present.</expect>
      <if_mismatch>STOP. Do not commit.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after re-run">
    <step>
      <run>The four verification checks above (dtype, row-count-unchanged, cell-values, 07-20-ETag-untouched)</run>
      <expect>All four green, evidence captured.</expect>
      <if_mismatch>Any failure = stop and report; a row-count change or a touched 07-20 partition is a new defect, not a pass.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<data_reprocess_scope>
  <reprocess_required>07-21 + 07-22 silver ONLY, forced rewrite via the idempotent converter. Bronze
  untouched. Verify post-rewrite dtype + unchanged row counts + 07-20 ETag-untouched. The gold+platinum
  rebuild is NOT ours to run — the 02:04Z scheduled chain does it; 0.7.0 verifies the closure.</reprocess_required>
</data_reprocess_scope>

<cross_domain_coordination>
  <resource path="cot silver 07-21/22 -> gold chain -> platinum" shared_with="0.7.0_AE_CloudOps">
    0.7.0 owns the closure verification tomorrow: chain COMPLETE exit 0 + `platinum/firm/*` advancing +
    header `data_as_of` moving to 07-21/22. That closure IS the deliverable's last leg. MCP him when
    silver is clean so he knows the 02:04Z chain should heal.
  </resource>
</cross_domain_coordination>

<acceptance_criteria>
1. `cot_silver_merge.py` coerce-numeric-BEFORE-string-sweep fix, Rule-17-legal (dtype only, nothing else
   moves), committed + deployed via the normal cycle.
2. Silver 07-21 + 07-22 rewritten; all four verification checks green with evidence.
3. NO ad-hoc gold run performed. The scheduled 02:04Z chain is the rebuild path.
4. 0.7.0's closure verification tomorrow confirms gold chain COMPLETE + platinum advancing + `data_as_of`
   at 07-21/22.
5. If the deadline could not be met cleanly: an explicit "missed window, landing clean for tomorrow's
   cron" report — NOT a rushed commit.
6. Session log Compiler Tools section reproduces every `<run>` with observed output and pass/fail.
</acceptance_criteria>

<deferred_not_tonight>
- **(c) the A_03-side guard** is a DESIGN question, not tonight's patch: a silent coerce at GOLD could MASK
  vendor drift — the fail-LOUD halt is arguably CORRECT behavior; what is wrong is that the loudness has
  no consumer. Author later as a designed TO (coerce-with-counted-loud-note vs halt-with-visible-signal).
- A `comp-freshness` cadence entry for the cot ADVI platinum surface (INSTRUMENT, not alarm — same ruling
  as tonight's six MDPF legs; config lane).
</deferred_not_tonight>

<escalation>
Report to 2.0.0_SA_COO; CTO gated the repair. Escalate immediately if the coerce cannot be made
Rule-17-legal without a fillna/filter (that would be a design question, not a patch), or if a rewritten
partition's row count changes (a different defect).
</escalation>
</task_order>
