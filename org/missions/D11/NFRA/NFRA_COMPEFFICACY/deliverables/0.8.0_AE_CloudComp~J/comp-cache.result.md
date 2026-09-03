# comp-cache — NFRA_COMPEFFICACY per-tool result (PRD s.4, T-23)

**Status:** implementation and file-grain validation are complete. A task-order `complete`
flip is blocked only on T23-AC3's portal-clean-state attestation; its carrier is
`NFRA_COMPEFFICACY-S24`.

```json
{
  "schema": "NFRA_COMPEFFICACY PRD v0.5 s.4 @5bbdab5ec7",
  "row": "T-23",
  "measured_by": "0.8.0_AE_CloudComp~J",
  "measured_at_utc": "2026-09-03T14:23:00Z..14:53:00Z",
  "read_vintage": "HEAD @273b4f9c20 before implementation; implementation @0084db376a",
  "identity": {
    "tool": "comp-cache",
    "shim_path": ".tools/comp-cache (8 lines)",
    "engine_path": "org/modules/graph/cache_cli.py (569 lines)",
    "engine_vintage": "0084db376a (predecessor 17cfd531b1)",
    "aliases": [],
    "purpose_1line": "React Query cache-key analysis across portal/src; not comp-platinum, which answers the separate portal-page-to-gold-script plane.",
    "self_identifies": "--help prints tool name and Rule T carrier; engine path is ABSENT from help."
  },
  "disclosure": {
    "subject": "portal/src React Query useQuery call-sites",
    "corpus_or_backend": "portal/src, read-only; portal HEAD 18c0c5cb",
    "vintage": "portal submodule HEAD 18c0c5cb; implementation 0084db376a",
    "denominator": "scanned 415 of 415 portal source file(s); skipped 0 file(s); captured 118 of 118 useQuery call-site(s); 0 unparseable",
    "resolved_unresolved": "118 entries -> 94 distinct keys across 44 files; 17 shared keys; 0 TYPE MISMATCH",
    "blind_spots": "useQueries / useInfiniteQuery / useAutoSaveQuery are not audited; generated/unreadable files and unparseable calls are listed and force PARTIAL_OR_BLIND",
    "pagination": "Rule T work pagination: deterministic source-file cursor and true source-file total on every sweep; result rows are not page-limited",
    "timeout": "default 90s; --budget > COMP_BUDGET_S > default; --budget 0 unbounded; forced 1e-12s run prints BUDGET REACHED plus --cursor START"
  },
  "answer_state": {
    "SUBJECT_ABSENT_FROM_CORPUS": "fixture map over missing portal/src -> ANSWER_STATE: SUBJECT_ABSENT_FROM_CORPUS; rc 0",
    "PRESENT_WITH_ZERO_RESULTS": "live key ZZZ_T23_ABSENT_KEY -> 0 hits; ANSWER_STATE: PRESENT_WITH_ZERO_RESULTS; rc 0",
    "PARTIAL_OR_BLIND": "fixture collisions with @generated TSX -> ANSWER_STATE: PARTIAL_OR_BLIND and COLLISION VERDICT: INCOMPLETE; rc 0",
    "NOT_APPLICABLE": "fixture collisions with no useQuery population -> ANSWER_STATE: NOT_APPLICABLE and COLLISION VERDICT: NOT EVALUATED; rc 0",
    "verdict": "PASS: four planted states have four distinct ratified-enum tokens. Each state arm has a source mutant that runs and makes the arm RED."
  },
  "bounds": {
    "subprocess_timeouts": "none",
    "ceiling_behaviour": "BUDGET REACHED: 1e-12 s (flag); scanned 0 of 415 file; results are a PREFIX, not the answer; resume: comp-cache map --cursor START; rc 0",
    "page_contract": "--cursor resumes after a deterministic source-file label; skipped-file denominator prints on every sweep",
    "size_invariance": "caller-provided work ceiling, default 90s; source-file units, not a corpus-size constant",
    "consumer_census": "execution-only: .tools/portal-hooks/VALGATE_D1.md says collisions is not hook-wired; no hook/gate consumes collisions as a verdict."
  },
  "passcraft": {
    "moves_1_to_8": "shim resolved to engine; read-only source plane; live and fixture evidence separated; every scan prints denominators; four state branches and mutants exercise answer shape; findings are routed rather than fixed; cache-key and comp-platinum planes are named apart.",
    "archetype": "read-only portal-source cache-key analyzer; body tokens, not rc, express partial state.",
    "findings": "17 shared live cache keys are portal-owner-class (DE) findings; 0 type mismatches; no portal edit in this cell."
  },
  "usage": {
    "runs_jsonl": "79 comp-cache-named rows in this device-local ledger at read time; not an estate-wide or time-filtered total",
    "rail_log": "617 comp-cache-named rail rows at read time; routing/search references are not necessarily executions",
    "hook_driven": "0 observed consumers; HUD is advisory and the portal hook document says collisions is not wired",
    "battery": "new .tools/tests/test_comp_cache_battery.py: 10/10 direct, 1 pytest pass; existing test_cache_cli.py: 22 passed; one red source mutant per state arm",
    "overlap": "not comp-platinum: comp-cache is portal-source cache keys; comp-platinum is portal-page to gold-script",
    "proposed": "implementation committed at 0084db376a; certification awaits AC3 clean-state disposition and push measurement"
  },
  "acceptance_status": {
    "T23-AC1": "READY",
    "T23-AC2": "READY",
    "T23-AC3": "BLOCKED — zero edits by this lane, but portal has 14 pre-existing untracked paths; NFRA_COMPEFFICACY-S24",
    "T23-AC4": "READY",
    "T23-AC5": "READY",
    "T23-AC6": "PENDING — proof validation and measured push state before complete flip"
  }
}
```

## Evidence excerpts

Default map: `scanned 415 of 415 portal source file(s); skipped 0 file(s); captured 118 of
118 useQuery call-site(s); 0 unparseable`, then `118 entries -> 94 distinct keys across 44
files`. The live collision scan found `17 shared key(s); 0 with a TYPE MISMATCH`.

Forced production budget run: `ANSWER_STATE: PARTIAL_OR_BLIND` and `BUDGET REACHED: 1e-12 s
(flag); scanned 0 of 415 file; results are a PREFIX, not the answer; resume: comp-cache map
--cursor START`.
