# COMP_LEARNS.037 — SC Measurement Amendment: Cost Field Split

**TO serial:** COMP_LEARNS.037
**Author:** 2.1.0_SA_COO
**Date:** 2026-04-24
**Dispatched by:** 2.1.0_SA_COO per 1.1.0_SA_CTO GO directive 20260424T211835Z
**Issued to:** 2.1.0_SC_CompLearns
**Status:** complete<!-- 66dcbb10 — 2026-04-24 -->
**Priority:** P0 — gates Phase 2 benchmark honesty

---

## Source authority

- CVO R-SC-1 (P0): `org/tier1_exec/3.1.0_SA_CVO/responses/20260424T203500Z_to_1.1.0_SA_CTO_retrieval_paradigm_design.md` §1 SC
- PRD §6 v1.1: `docs/architecture/COMP_LEARNS_PROGRAM_PURPOSE.md` §6 (four-condition comparator, cost accounting)
- COO wave protocol amendment: `docs/architecture/COMP_LEARNS_PHASE2_PROTOCOL_AMENDMENT.md`
- CTO GO: 20260424T211835Z

---

## Objective

Extend the scoring schema with three separate cost fields to support honest benchmark accounting under the two-step retrieval paradigm (asynchronous background index + task-time addressing + delivered context).

Without this split, `token_reduction` can become an accounting artifact — cost hidden in the addressing layer appears as context efficiency. This makes the aided-vs-unaided comparison structurally dishonest for Phase 2 four-condition scoring.

---

## Scope

### Files to modify

- `comp/bench/scorecard.py` — add three cost fields to Scorecard dataclass; serialize/deserialize; loader backward-compat
- `comp/bench/ab.py` — surface cost fields from measurement harness (may be zero for Phase 1 compat)
- Schema version bump if applicable per existing schema_version convention

### New required fields

| Field | Python type | Description |
|-------|-------------|-------------|
| `background_index_cost` | `int \| None` | Amortized token cost to build/update the structured index. Zero for Phase 1 runs (predate two-step model). None = field absent (pre-TO scorecard). |
| `task_addressing_cost` | `int \| None` | Per-task token cost of the localization/addressing step. Zero if purely mechanical (no LLM). None = field absent. |
| `delivered_context_cost` | `int \| None` | Final context tokens delivered to the judge. Equivalent to the token surface already tracked by `token_reduction` denominator — expose as an explicit named field here. |

### Backward compatibility (mandatory)

Phase 1 scorecards (all httpx and dev-click-001 iters 1–5) predate the two-step model. Loader must:
- Accept scorecards with all three fields absent → default to `None`
- Accept scorecards with fields present → load as-is
- NOT error on missing fields

Phase 1 scorecards may be re-emitted with `background_index_cost=0` and `task_addressing_cost=0` explicitly if the emission path is updated — but this is optional. Do not backfill existing result files.

---

## Acceptance criteria

- [ ] Three cost fields present on `Scorecard` dataclass with correct types
- [ ] `scorecard_to_dict` / `from_dict` round-trip for all three fields (present and absent)
- [ ] Loader tolerates absent fields (defaults to `None`)
- [ ] `comp/bench/ab.py` populates or stubs all three fields on scorecard emission
- [ ] At minimum: 1 test per field for serialize/deserialize round-trip + 1 backward-compat test (absent fields load without error)
- [ ] `pytest comp/bench/tests/ -q` green (all existing tests pass)
- [ ] `ds-commit-gate.sh` PASS on all `.py` edits
- [ ] Committed under `--author="2.1.0_SC_CompLearns <2.1.0_SC_CompLearns@opal.agent>"`
- [ ] MCP 2.1.0_SA_COO COMPLETE with commit sha + AC checklist

---

## Dependencies

- **Requires:** COMP_LEARNS.030 complete (satisfied — schemas + doctrine ext)
- **Blocks:** Phase 2 pilot wave dispatch (benchmark honesty gate for four-condition scoring)

---

## Notes

SC owns spec (field names, types, validation rules) and implementation. Concrete population values for C2/C3/C4 conditions (the four-condition comparator conditions from PRD §6) are Phase 2 DS implementation work. SC does not need to produce non-zero values for these fields in this TO — just ensure the slots exist, serialize cleanly, and backward-compat holds.

Phase 2 four-condition scoring (C1 unaided / C2 mechanical retrieval only / C3 index+no-addressing / C4 full two-step) requires cost attribution at each condition. These three fields are the mandatory measurement surface for that attribution.
