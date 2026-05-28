# RV0017-F003 — `max_concurrent` formula sister-amendment

**Parent:** RV-0017 P1 per `docs/briefs/rv-0017-p0-p1-p2-action-dispatch.md` §3.
**Owner:** `1.0.0_SA_CTO`
**Scope class:** PRD-light (proposal authoring; ratification gates on Andrew)

---

## §1 — Status

**PROPOSAL AUTHORED + READY FOR ANDREW RATIFICATION.**

Three artifacts shipped this commit (CTO-author-line scope):
1. **Proposal brief:** `docs/briefs/rv0017-f003-max-concurrent-formula-proposal.md` — full rationale + empirical anchor + amendment text + ratification ask
2. **Tool:** `.tools/check-concurrency.sh` — empirical hook-latency measurement + structural ceiling computation
3. **TO:** this file

**Andrew-gated artifacts (not authored this commit):**
- `org/tier0/STAKES_MATRIX.md` v1.6 entry — Andrew sovereign owned-paths-locked file; MSTR scribes on Andrew ratify per HARD-BLOCK #1 transcription discipline
- `CLAUDE.md` Rule 20 — bindable on ratify-or-acknowledge

## §2 — Acceptance

Per brief §3 "Acceptance: Formula documented in Constitution sister-amendment + checked into MEMORY.md / CLAUDE.md operating discipline section."

This commit closes the **proposal + tool** legs. The **ratification + binding** legs gate on Andrew sovereign verdict. Specifically:
- Proposal documented at `docs/briefs/rv0017-f003-max-concurrent-formula-proposal.md` ✓
- Tool ships `.tools/check-concurrency.sh` ✓
- STAKES_MATRIX.md v1.6 amend authored as text-block within the proposal brief (ready for MSTR transcription on Andrew ratify) ✓
- CLAUDE.md Rule 20 text authored within the proposal brief (ready for CTO transcription on Andrew ratify) ✓

If Andrew RATIFY arrives, CTO will:
- Ship CLAUDE.md Rule 20 in a follow-up commit (autonomous, transcription-from-ratified-proposal scope)
- MCP MSTR with the STAKES_MATRIX v1.6 amend text for MSTR transcription

## §3 — Tool verification

```bash
$ .tools/check-concurrency.sh --hook 1.5
check-concurrency (RV-0017 F-003)
  Formula:               max_concurrent = floor(target_cycle_s / hook_latency_s)
  Target cycle (s):      300
  Hook latency (s):      1.5  (3-trial empirical median on empty stage)
  Structural ceiling:    200
  STAKES_MATRIX cap:     20  (v1.5 per LD-0115)
  Verdict:               WITHIN-FORMULA
$ echo $?
0
```

Current state passes structurally: 20 cap is 10x headroom below the 200-worker structural ceiling.

## §4 — Risks accepted

- **Andrew silent ≥1 cycle** triggers LD-0090 ALWAYS-PROCEED defaults-bind. Operational-parameter-class amend doesn't have a "default" forward path beyond binding-on-ratify; if Andrew is silent, the proposal sits in inbox + CLAUDE.md Rule 20 doesn't bind. F-003 is observation-class (the formula is verifiable via the tool), so a silent week doesn't break anything — it just delays formal codification.
- **Hook latency measurement noisy under storm contention.** The auto-measure path can hang on a busy host; `--hook` override is the production-recommended path. Tuning the measurement window if false-positive rates surface.

## §5 — Out of scope

- F-005 orphan-detector + process-count observability — separate P1 (this session, sibling commit)
- F-006 commit-serialization research — separate P2 (this session, sibling commit)
- Per-fabric independent caps — preserved unified per LD-0028 + LD-0049
- `target_cycle_seconds` per-loop overrides (e.g., /work 20m vs /ws-charter 30m vs /drive 20m) — current formula uses the 300s common floor; if individual loops adopt longer/shorter cycles a refinement may be warranted

— `1.0.0_SA_CTO` 2026-05-28T~00:10Z
