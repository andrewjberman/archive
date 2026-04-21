<task_order>
  <metadata>
    <id>2.1.0_SC_CompLearns-2026-04-21-comp-learns-029-scorer-stability-baseline-report</id>
    <issued_by>1.1.0_SA_CTO</issued_by>
    <issued_to>2.1.0_SC_CompLearns</issued_to>
    <date>2026-04-21</date>
    <status>complete</status>
    <project_code>COMP_LEARNS</project_code>
    <priority>P0 — first act of the SC role; the canonical baseline future runtime changes diff against</priority>
  </metadata>

  <references>
    <ref type="doctrine">docs/architecture/COMP_LEARNS_PROGRAM_PURPOSE.md — the measurement-substrate framing</ref>
    <ref type="prd">docs/architecture/COMP_LEARNS_RUNTIME_V1.md — what the Phase 3 close committed to</ref>
    <ref type="prompt">org/tier2_senior/2.1.0_SC_CompLearns/prompt.md — the 12-point checklist + Minimal Exit Bar</ref>
    <ref type="artifacts">comp/targets/httpx/ — champion.json, experiment_log.jsonl, scorecards/*.json, PROVING_SEQUENCE_R1_R5.md</ref>
  </references>

  <objective>
    Produce the canonical scorer-stability baseline report against the post-.027b httpx runtime. This report is the reference artifact every future runtime or scoring change will diff against. It is the SC role's first formal deliverable and its operating baseline.

    The report runs the full 12-point checklist (prompt.md §4), certifies against the Minimal Exit Bar (§5), and emits one of three recommendations: GREEN (scorer stable, phase exit permitted), YELLOW (scorer stable with named caveats, phase exit permitted with caveat documented in PRD), RED (gate failure, phase exit blocked, specific items listed with evidence).

    This is certification work, not implementation work. You read artifacts, commits, and code; you do not modify `comp/`.
  </objective>

  <scope>
    <files>
      <file action="create">org/tier2_senior/2.1.0_SC_CompLearns/deliverables/scorer_stability_baseline.md</file>
      <file action="create">org/tier2_senior/2.1.0_SC_CompLearns/deliverables/phase_3_certification.md</file>
      <file action="create">org/tier2_senior/2.1.0_SC_CompLearns/logs/2026-04-{DD}/session_01_baseline_report.md</file>
    </files>
  </scope>

  <wire_contract>
    **scorer_stability_baseline.md structure:**

    1. Front matter: date, target (httpx), target_version, champion compiler_sha, judge regime (real / mock), runtime commit hash (current HEAD), RUNTIME_V1.md reference commit.
    2. §1 Truth Surface — evidence + verdict.
    3. §2 Score Identity — evidence + verdict.
    4. §3 Deterministic Core — evidence + verdict.
    5. §4 Model-Mediated Scoring — evidence + verdict.
    6. §5 Selector Integrity — evidence + verdict.
    7. §6 Formula Simplicity — evidence + verdict.
    8. §7 Champion / Compare Semantics — evidence + verdict. Note: the mock-vs-real champion-mode divergence caught in .027 → .027b is a known issue here; document whether the Option A+ reset fully resolves it or whether `champion.judge_mode` is still a v1.1 parking-lot item.
    9. §8 Artifact Authority — evidence + verdict. Note: .028 Phase 2 legacy decommission touches this section; reference the inventory report.
    10. §9 Schema Discipline — evidence + verdict.
    11. §10 Reproducibility Proof — cite the 5 Option A+ proving runs + the 4 original .027 runs; verdict on each of the 5 required demonstrations.
    12. §11 Benchmark Honesty Flag — evidence + verdict.
    13. §12 Undocumented Load-Bearing Surfaces — explicit pass, named findings. The content-addressed AB cache identity discovered in .027 Run-5 Q3 is a known item — elevate it here. Look for others.
    14. §13 Minimal Exit Bar — seven-line checklist with pass/fail per line.
    15. §14 Recommendation — GREEN / YELLOW / RED + one-sentence justification.
    16. §15 Re-open triggers currently armed — which of the six trigger conditions (cache identity / compare semantics / judge backend / selector semantics / champion-state / target-version-schema) are at risk of firing in the near term, and what would trip them.

    **phase_3_certification.md structure** (shorter; separate file; cites the baseline):
    1. Phase boundary: Phase 3 close (post-.027b).
    2. What the phase committed to (RUNTIME_V1.md §14 success bar).
    3. What actually shipped (cite commits + tags).
    4. 12-point checklist signoff (by reference to scorer_stability_baseline.md).
    5. Minimal Exit Bar check.
    6. Caveats (KEEP/TIED verdicts proven under real judge in Option A+ extension; champion.judge_mode parking-lot item; anything else caught in the baseline pass).
    7. Signoff statement: "Scorer stable for regime X. Minimal Exit Bar satisfied. Baseline report at {path} @ {commit}." OR gate-failure block.

    **Evidence pointers to read:**
    - `comp/targets/httpx/champion.json` (current: sha=3fb8b69, pm=0.0664 real-judge)
    - `comp/targets/httpx/experiment_log.jsonl` (last ~15 entries span the Option A+ proving + v0 + .027)
    - `comp/targets/httpx/scorecards/` (all 4 real-judge scorecards + the Option A+ additions)
    - `comp/targets/httpx/PROVING_SEQUENCE_R1_R5.md` + Option A+ append
    - `comp/bench/scorecard.py` — score identity fields
    - `comp/bench/ab.py` — cache keying
    - `comp/bench/cache.py` — cache instrumentation (.025)
    - `comp/loop/ratchet.py` — compare_key_for + champion update logic
    - `comp/loop/experiment_log.py` — schema_version handling (.024)
    - `comp/loop/runner.py` — runner terminal conditions (.023)
    - `comp/loop/render.py` — tie reporting (.026)
    - Git tags: `comp-learns-v1-proving-start`, `comp-learns-v1-proving-reset`, `comp-learns-v1-proving-complete`, `comp-learns-v0-final`
    - Commits: `41225ed9` (.023), `506a9466 + bcf47646` (.024), `e7a12a12 + 53386ec7` (.025 + .026), `af89f12e + 1e5d67b2` (.027 + .027b), `5622dad4 + 09f7e798` (.028 Phase 1-2)
  </wire_contract>

  <acceptance_criteria>
    1. `scorer_stability_baseline.md` written in full — all 12 checklist sections + Minimal Exit Bar + recommendation + re-open triggers. No section left as "TODO" or "see later."
    2. Every verdict in sections §1-§12 cites at least one specific artifact (commit, file path, log line, test file) as evidence. No ungrounded claims.
    3. §10 (Reproducibility Proof) explicitly maps the 5 required demonstrations to the actual Option A+ runs — e.g. "Demonstration 1 (same compiler same regime identical score) ← sha=d87377a run #1 + run #2 both pm=0.0664 cache_misses=0 on run #2".
    4. §12 (Undocumented Load-Bearing Surfaces) names at least the content-addressed AB cache finding from .027 Q3. If you find others, name them.
    5. §14 recommendation is one of GREEN / YELLOW / RED with explicit justification.
    6. `phase_3_certification.md` cites the baseline report + emits the signoff statement or gate-failure block per `prompt.md §5`.
    7. Session log at `org/tier2_senior/2.1.0_SC_CompLearns/logs/2026-04-{DD}/session_01_baseline_report.md` documents the work: what you read, what you found, any escalations.
    8. Both deliverables committed under `--author="2.1.0_SC_CompLearns <2.1.0_SC_CompLearns@opal.agent>"`.
    9. On completion, MCP COMPLETE to 1.1.0_SA_CTO + 2.1.0_SA_COO with commit sha + recommendation (GREEN/YELLOW/RED) + link to baseline file.
    10. If recommendation is RED, do NOT flip this TO status to `complete`. Hand back to CTO via MCP as a gate failure.
  </acceptance_criteria>

  <dependencies>
    - None downstream — you are the first SC TO.
    - Upstream reads only — no new commits to `comp/` required from any DS agent to produce this report.
  </dependencies>

  <operational_notes>
    - This TO is scoped to a single sitting (~2-4 hours of read + synthesis). If you find the scope expanding, stop and MCP CTO for scope clarification rather than extending.
    - The content-addressed AB cache finding in §12 is the most interesting surface on the current runtime — spend disproportionate attention there. Confirm or contradict the operator's Run-5 Q3 claim by reading `comp/bench/cache.py` + `comp/bench/ab.py` directly.
    - Note for future SC work: re-open triggers §15 is the surface that most commonly gets ignored; agents will tell you "just a small change to X" and you need to know whether X is one of the six triggered conditions. Be disciplined.
    - Rule 7 pre-flag contract applies: mechanical pre-flags OK, verdict-interpretation holds = hard stop for explicit CTO ACK.
  </operational_notes>

  <closeout>
    - commit under `2.1.0_SC_CompLearns` author
    - MCP COMPLETE to 1.1.0_SA_CTO + 2.1.0_SA_COO (commit sha + GREEN/YELLOW/RED + baseline path)
    - flip TO status to `complete` with commit ref (only if recommendation ∈ {GREEN, YELLOW})
    - escalate to CTO via MCP as gate failure if recommendation is RED — do NOT flip status
  </closeout>
</task_order>
