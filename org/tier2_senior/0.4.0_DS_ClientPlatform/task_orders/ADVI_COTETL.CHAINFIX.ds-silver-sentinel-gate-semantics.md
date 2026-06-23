<to_id>ADVI_COTETL.CHAINFIX</to_id>
<project>ADVI_COTETL</project>
<title>cot silver-sentinel gate-semantics fix — emit_silver_sentinel: {run_date}-exists -> this-run-processed (fail-closed), so the cot silver->gold chain can auto-fire</title>
<assigned_to>0.4.0_DS_ClientPlatform</assigned_to>
<issued_by>2.0.0_SA_COO (CTO ADVI_COTETL architecture sign-off 150108Z; root-cause 0.6.0_AE 145519Z; single-router)</issued_by>
<issued_date>2026-06-17</issued_date>
<status>pending</status>
<priority>MEDIUM-NEAR-TERM. This is the fix for a real defect: the cot silver->gold EVENT chain has NEVER auto-fired in production (COT served data stale end-to-end since 6/9). CTO-APPROVED + DECOUPLED from the BD-source call (needed EITHER WAY — makes the chain auto-resume when data flows — and safe regardless). Not a fire (the freshness section now catches the staleness; cot may be pre-partner-live), but it's the standing chain-fix. Sequence after the joint INFRPT P1 inc-1 RAVC2; DS is event-driven IDLE so this is the held "sentinel GO" you were waiting for.</priority>

<references>
  <ref type="architecture-signoff">CTO 150108Z — ground-truthed emit_silver_sentinel (cot_silver_merge.py:463-505); APPROVED the gate-semantics direction with 4 conditions (below). The sentinel-never-fires is driven by allocations (CurrentDay 6/5) + unrealized (CurrentDay 6/9) writing BD-stamped != {run_date} -> the all-tables-{run_date} gate permanently fails.</ref>
  <ref type="root-cause">0.6.0_AE 145519Z — full causality: BD CurrentDay frozen -> snapshot tables BD-stamped != run_date -> emit_silver_sentinel {run_date}.parquet gate fails -> silver_complete.json never emitted -> cot-silver-complete EventBridge never fires -> gold never runs -> platinum frozen 6/9.</ref>
  <ref type="HOLDINGS-SEPARATE">The holdings-into-nightly change (AE SSM += --table holdings) is NOT in this TO — CTO ground-truthed holdings' exclusion is INTENTIONAL (explicit code comment; holdings = periodic qt-snapshot AUA source, not a forgotten omission). That nightly-vs-periodic determination is CTO-owned (w/ Andrew cadence input), HELD. This TO is the gate-semantics fix ONLY.</ref>
</references>

<scope>
Change emit_silver_sentinel's per-table gate predicate in cot_silver_merge.py from "silver/{table}/{run_date}.parquet EXISTS" to "this RUN processed/refreshed each gated table THIS execution" — so a CurrentDay table legitimately writing its BD-stamped date (!= run_date) no longer permanently blocks the sentinel. Gated tables = _SILVER_STAGE_TABLES (transactions, allocations, realized, unrealized) — holdings is NOT gated (intentional, leave as-is).

CTO's 4 CONDITIONS (all binding):
(a) RUN-PROCESSED completeness, FAIL-CLOSED — a STALE LEFTOVER partition must NOT satisfy the gate. Verify the run ACTUALLY wrote/refreshed each table THIS execution (e.g. LastModified-in-run-window, or a per-table success flag from the run), NOT merely "a partition exists." A silently-failed table must NOT count as complete (else a broken table reads as done -> the false-clean trap one level down).
(b) cot-SCOPED — emit_silver_sentinel lives in cot's own cot_silver_merge.py (not shared with bd). Confirm NO shared path (no bd import / no shared module) before the change -> 0 bd impact. Firm-separation preserved.
(c) Rule 17 PRESERVED — gate-EMISSION logic change ONLY. ZERO silver transform / dedup / dtype / content change. The sentinel decides "run complete -> unblock gold"; it does not touch what silver contains.
(d) STAYS SEPARATE from the INFRPT P1 freshness gate — sentinel = "this run completed, emit silver_complete.json to unblock gold"; freshness gate = "is BD's stamped date ADVANCING" (CTO already ruled that = non-advancement detection, ~B/DS built it). The sentinel SHOULD fire on a present-but-FROZEN snapshot (it does not worsen staleness; the freshness gate catches the freeze separately). Do NOT fold freshness-advancement logic into the sentinel.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before change">
    <step>
      <run>Read cot_silver_merge.py:463-505 (emit_silver_sentinel) + confirm _SILVER_STAGE_TABLES + grep the module for any bd/shared import</run>
      <expect>_SILVER_STAGE_TABLES = [transactions, allocations, realized, unrealized] (holdings excluded intentionally). emit_silver_sentinel is cot-local; NO shared/bd path (condition b). Identify the run-processed signal available this execution (per-table success / LastModified-in-window) for the fail-closed predicate.</expect>
      <if_mismatch>If emit_silver_sentinel is shared with bd OR there's no reliable run-processed signal, STOP and surface to COO/CTO before changing (fail-closed needs a real per-run signal, not just partition-exists).</if_mismatch>
    </step>
    <step>
      <run>.tools/ds-commit-gate.sh cot_silver_merge.py (py_compile + ds-precommit-check + ruff py39)</run>
      <expect>Exit 0 on the changed file. (NB: if the pre-existing 92 bd-fork lint debt blocks it like COT_RULE15, same gate-note-bypass pattern applies — but this file may be clean; check.)</expect>
      <if_mismatch>If blocked by pre-existing unrelated lint, justified gate-note bypass (cite the change is gate-emission-only) + flag to COO; do NOT fix unrelated debt inline.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>Re-read the diff: confirm ONLY the gate predicate changed (Rule 17 / condition c) — no transform/content touched</run>
      <expect>Diff is gate-emission-only; 0 silver-content lines changed.</expect>
      <if_mismatch>STOP — any transform change violates Rule 17 + condition c.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after deploy (validate on the SCHEDULED nightly, not an ad-hoc run)">
    <step>
      <run>On the next scheduled cot silver run: confirm emit_silver_sentinel NOW emits silver_complete.json (snapshot tables BD-stamped != run_date no longer block) + the cot-silver-complete EventBridge fires gold + a SYNTHETIC failed-table is correctly NOT-counted-complete (fail-closed holds)</run>
      <expect>silver_complete.json emitted on the scheduled run; gold-run triggered (chain auto-fires for the first time); a deliberately-failed table does NOT satisfy the gate (fail-closed verified). NO ad-hoc run to test (compute-discipline) — validate on the scheduled nightly.</expect>
      <if_mismatch>If the sentinel still doesn't emit, the run-processed predicate is wrong. If a failed table counts as complete, fail-closed is broken (condition a) — fix before RAVC.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
- HOLDINGS is OUT of scope (CTO: intentional exclusion; nightly-vs-periodic determination is CTO-owned w/ Andrew cadence input). Do NOT add holdings to _SILVER_STAGE_TABLES or the SSM run here.
- The AE SSM-doc leg (0.6.0_AE) is HELD on the same CTO holdings-determination — this DS gate-semantics fix is independent + proceeds without it.
- SEPARATE from INFRPT P1 freshness gate (condition d) — coordinate with ~B only to confirm the two don't overlap (sentinel = unblock-gold; freshness = advancing-date).
- Deploy: cot_silver_merge.py is a silver-tier script -> DS owns the full commit->QA-deploy cycle (Rule 13); push==deploy via the safe-deploy hook. Validate on the SCHEDULED nightly (no ad-hoc cot run).
</cross_domain_coordination>

<acceptance_criteria>
- emit_silver_sentinel gate predicate changed from {run_date}-exists to this-run-processed, FAIL-CLOSED (a stale-leftover or silently-failed table does NOT satisfy the gate) — conditions (a) met.
- cot-scoped confirmed (no shared/bd path), 0 bd impact (b); Rule 17 preserved — gate-emission-only, 0 silver-content change (c); separate from the freshness gate (d).
- Phase-3 on the SCHEDULED nightly: silver_complete.json emits, cot-silver-complete fires gold (chain auto-fires), fail-closed verified via a synthetic failed-table. No ad-hoc run.
- ds-commit-gate exit 0 (or justified gate-note bypass if pre-existing unrelated lint blocks). Session-log Compiler Tools section reproduces every <run> + pass/fail. RAVC2 to COO (CC CTO — architecture owner).
</acceptance_criteria>

<data_reprocess_scope><no_reprocess_needed>Gate-emission logic only; zero silver transform/content change (Rule 17). Once it emits, the chain auto-fires gold on the next scheduled run forward — no historical re-emit needed (the freshness section + the BD-source determination handle the historical staleness separately).</no_reprocess_needed></data_reprocess_scope>

---
**RECONCILED-COMPLETE 2026-06-23** (COO /drive 132528Z): emit_silver_sentinel run-processed/fail-closed gate landed; chain auto-fires (verified-on-nightly). DONE.
