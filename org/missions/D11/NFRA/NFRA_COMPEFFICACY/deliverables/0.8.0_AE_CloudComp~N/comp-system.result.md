# comp-system - NFRA_COMPEFFICACY per-tool result (PRD s.4, T-21)

Status: COMPLETE lane evidence; FWD-9 remains an independent receiving-seat action.

```json
{
  "schema": "NFRA_COMPEFFICACY PRD v0.5 s.4 @5bbdab5ec7",
  "row": "T-21",
  "measured_by": "0.8.0_AE_CloudComp~N",
  "identity": {"tool":"comp-system","shim_path":".tools/comp-system (not changed)","engine_path":"org/modules/graph/comp_system.py","engine_vintage":"2e1102da897dfc61e2bc08bf632d2e3f5c7106dd; blob e048780c50c14b9dc774557c81be08a1abe94d43","aliases":[],"purpose_1line":"Comp-system compiles repository-local cross-surface evidence into served infra/system/06_current_state and reports current, stale, error, or not-decidable.","self_identifies":"--help names the compiler and its 0/2/1/3 check contract."},
  "disclosure":{"subject":"NFRA_SYSTEM current-state cross-surface compile","corpus_or_backend":"repository-local required sources and managed regions","vintage":"Served JSON: compile_complete=true; as_of_head=ee51681c45; emitted_at_utc=2026-09-03T16:31:12Z; required=7; unreadable=[].","denominator":"Complete record: 1 of 1 cross_surface_compile. Forced check: 0 of 1 check_verdict.","resolved_unresolved":"Complete record has no unreadable required source; forced check is PARTIAL_OR_BLIND/NOT-DECIDABLE.","blind_spots":"Unreadable or expired work is named and never represented as complete.","pagination":"Deferred work prints resume --cursor BEGIN.","timeout":"--budget > COMP_BUDGET_S > 90 s default; --budget 0 is unbounded."},
  "answer_state":{"SUBJECT_ABSENT_FROM_CORPUS":"Self-test planted scope-class fixture; no source carries this class.","PRESENT_WITH_ZERO_RESULTS":"Self-test planted real-present fixture; 0 rows across 1 present surface.","PARTIAL_OR_BLIND":"Moved-aside required source is named, NOT-DECIDABLE, compile_complete false, and no complete record.","NOT_APPLICABLE":"Self-test planted mode fixture; no population.","verdict":"All four exact ratified tokens appear in one self-test invocation; 45/45 passed."},
  "bounds":{"subprocess_timeouts":"Shared .tools/_compbudget.py carrier; no dependency added.","ceiling_behaviour":"--check --budget 0.001 printed BUDGET REACHED and returned rc 3.","page_contract":"Partial output is a prefix/not-decidable answer, never a complete 06 record.","size_invariance":"Caller-supplied wall-clock budget, not a corpus-size cutoff.","consumer_census":"--check preserves complete-run 0/2/1 and adds rc 3 only for expiry/unreadable source."},
  "passcraft":{"moves_1_to_8":"Reviewed and adopted COO-authorized dead-~P engine edit: answer states, budget carrier, unreadable-source guard, no complete write on partial, check rc 3. Retained passing lane battery test_comp_system_battery_ae_n.py; removed authorized foreign hung scratch battery.","archetype":"Repository-local served-record compiler and verdict-bearing staleness oracle.","findings":"NFRA_COMPEFFICACY-S30 records worktree provenance discrepancy; comp_blast_universe.py untouched."},
  "usage":{"runs_jsonl":"584 task-order read-vintage; not a live estate total.","rail_log":"ABSENT -- unnecessary for behavior proof.","hook_driven":"Task order names --check as auto-refresh verdict surface; no hook changed.","battery":"test_comp_system_battery_ae_n.py: 5/5 direct PASS in 356.322 s; pytest 5 passed in 358.46 s; engine self-test 45/45 PASS.","overlap":"Not comp-blast; T-6 owns comp_blast_universe.py.","proposed":"Engine commit 2e1102d is LOCAL ONLY; FWD-9 requested from another seat."},
  "acceptance_status":{"T21-AC1":"READY","T21-AC2":"READY","T21-AC3":"READY","T21-AC4":"READY","T21-AC5":"READY","T21-AC6":"READY"}
}
```

## Evidence excerpts

--help says: staleness probe (0=current 2=stale 1=error 3=NOT-DECIDABLE; never writes).
--check --budget 0.001 returned rc 3 and printed PARTIAL_OR_BLIND (NOT-DECIDABLE),
NO COMPLETE RECORD WAS WRITTEN, and BUDGET REACHED: 0.001 s (flag); scanned 0 of 1 check_verdict.

Post-commit self-test ended: self-test: 45/45 passed (grounded-or-UNKNOWN, no fabrication, shape-locked).

The required prior unit-1 regeneration is recorded at c08c1bbe99 for
infra/system/06_current_state.{md,json}. Its header carries as_of_head, source_fingerprint,
emitted_at_utc, source_health, and rule_t; this lane did not regenerate or widen that shared record.

## FWD-9 distinct-seat exercise

COO seat `2.0.0_SA_COO` ran the exact command `python org/modules/graph/comp_system.py --check`
from the workspace root at 2026-09-03T18:03:30Z on HEAD `1fb2f2a21e`; both evidence commit
`b6a2274c7d` and engine commit `2e1102da89` were ancestors. It returned rc 0 and printed
`SYSTEM CURRENT`, `WITHIN BUDGET: scanned 1 of 1 check_verdict; budget: 90 s (default), used
4.688 s`, and `DEFERRED: 0 of 1 check_verdict(s) did not return`. This is the required
independent verdict-bearing FWD-9 exercise.
