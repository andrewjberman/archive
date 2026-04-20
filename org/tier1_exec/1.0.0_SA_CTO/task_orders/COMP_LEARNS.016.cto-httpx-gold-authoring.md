<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-04-16-comp-learns-016-httpx-gold-authoring</id>
    <issued_by>2.0.0_SA_COO~B</issued_by>
    <issued_to>1.0.0_SA_CTO</issued_to>
    <date>2026-04-16</date>
    <status>staged</status>
    <project_code>COMP_LEARNS</project_code>
    <priority>P1 — gates .013 precision/recall + .015 A/B + .017 ratchet</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/COMP_LEARNS_ARCHITECTURE.md @ 8df31d86 (v3 — peer review invariant-breakage fixes)</ref>
    <ref type="prd_section">§6.1 ratchet-critical vs exploratory split, §6.3 required benchmark components (gold + ab_questions + ab_answer_key), §6.4 A/B LLM protocol + judge-split (ratchet pool: enumerable/set_membership/numeric only; open-ended → exploratory), §6.4.1 cached-answer regime (target_version bump orphans cache), §4.5 dimensional ontology (gold records carry attribute tags), §8 inaugural subtype rationale, §11.1 R1 (gold-before-code) + R14 (judge drift), §16 item 3 (hard cap 2-3 manual gold targets)</ref>
    <ref type="predecessor_prd">docs/architecture/COMP_LEARNS_HTTPX_TARGET.md (PRD #2 — Phase 0 shipped at fd2d0515; Steps 2-7 absorbed into this TO)</ref>
  </references>

  <objective>
    Author `httpx` gold artifacts per §6.3, with **dimensional-attribute tagging per §4.5 AND v3 ratchet/exploratory question-pool split per §6.1/§6.4.** CTO-owned (2-hour burn per §11.2).

    Deliver:
    1. `comp/targets/httpx/gold/imports_gold.jsonl` — hand-enumerated import edges for every `httpx/*.py` module. **Each gold record carries the same dimensional attributes `{resolution, guard, binding}` as .013's SubtypeRecords.** Attribute values derived by the human reader from source reading, NOT from running a compiler.
    2. `comp/targets/httpx/gold/ab_questions.yaml` — 15-30 A/B questions per §6.3, **split into two pools:**
       - **`ratchet_critical` pool:** every question answerable deterministically — `enumerable` / `set_membership` / `numeric` only. Feeds `primary_metric` via §6.4.1 cached-answer regime.
       - **`exploratory` pool:** open-ended / free-text questions. Feeds `scorecard.exploratory.open_ended_judge` only; NEVER contributes to champion selection.
    3. `comp/targets/httpx/gold/ab_answer_key.yaml` — human-verified correct answers, each entry typed per §6.4 judge split: `{answer_type: enumerable, values: [...]}` OR `{answer_type: set_membership, values: [...]}` OR `{answer_type: numeric, value: N, tolerance: T}` OR `{answer_type: open_ended, rubric: "..."}`. Ratchet-pool entries MUST be one of the first three types; `.015`'s `ab_answer_key_validator.py` rejects open-ended in the ratchet pool at load time.
    4. `comp/targets/httpx/gold/target_version.txt` — **SHA-256 of the concatenation of `imports_gold.jsonl` + `ab_questions.yaml` + `ab_answer_key.yaml` + the frozen `httpx/` source tree.** Committed with the gold. Per §6.4.1, any edit to these files bumps `target_version` and orphans all prior cache entries — this is the only sanctioned way for gold changes to invalidate champion selection.
    5. `comp/targets/httpx/gold/GOLD_SURVEY.md` — written record of gold authoring process (modules read in order, what counted as a static import, time spent, ambiguities resolved, gold-before-code attestation).

    **Gold-before-code invariant (§11.1 R1):** gold MUST be authored without running any COMP_LEARNS `imports` subtype extractor. Reading .013's synthetic fixtures for calibration is allowed; running .013 against httpx and cross-checking answers is NOT. If a gold edge count matches the compiler's count exactly by construction, the bench is broken.

    **Ratchet-pool discipline (§6.4 v3 — non-negotiable):** every ratchet-pool question has a mechanically-checkable answer. If a question can't be answered via set equality, enumeration match, or numeric tolerance, it goes in the exploratory pool — not the ratchet pool. Ratchet-pool questions are what the primary_metric is built on; fuzziness here = R14 judge drift.

    Explicitly out of scope: multiple targets (httpx only — per §16 item 3, beyond 2-3 targets we pivot to mutation-based validation). Multi-subtype gold (imports only for this TO).
  </objective>

  <scope>
    <files>
      <file action="create">comp/targets/httpx/gold/imports_gold.jsonl</file>
      <file action="create">comp/targets/httpx/gold/ab_questions.yaml</file>
      <file action="create">comp/targets/httpx/gold/ab_answer_key.yaml</file>
      <file action="create">comp/targets/httpx/gold/target_version.txt</file>
      <file action="create">comp/targets/httpx/gold/GOLD_SURVEY.md</file>
    </files>
  </scope>

  <wire_contract>
    **imports_gold.jsonl format — one record per edge:**
    ```json
    {"source": "module:httpx._client", "predicate": "imports", "target": "module:httpx._transports", "attributes": {"resolution": "static", "guard": "unconditional", "binding": "resolved"}, "confidence": "certain", "gold_authored_at": "2026-04-16T14:00:00Z"}
    ```

    **Required attribute coverage in gold:** at least 2 records per dimension value must exist somewhere in the gold set. Specifically:
    - ≥2 records with `resolution=static`, ≥2 records with `resolution=dynamic` (httpx has `importlib` usage in `_transports`).
    - ≥2 records with `guard=unconditional`, ≥2 records with `guard=conditional` (httpx has `TYPE_CHECKING` guards).
    - ≥2 records with `binding=resolved`, ≥2 records with `binding=unresolved` (httpx has star imports or relative imports that need resolution context).

    If httpx does not naturally contain enough instances of a dimension value, CTO flags it to COO~B — we either pick a different inaugural target or add a synthetic extension to httpx for test coverage.

    **ab_questions.yaml format (v3):** each question has `id`, `question`, `pool` (`ratchet_critical` | `exploratory`), `adversarial` (bool).

    ```yaml
    - id: q01
      pool: ratchet_critical
      adversarial: false
      question: "Which modules does httpx._client import from within httpx?"
    - id: q15
      pool: ratchet_critical
      adversarial: true
      question: "How many modules import httpx._transports.default?"
    - id: q22
      pool: exploratory
      adversarial: false
      question: "Describe httpx's transport layer architecture in 2-3 sentences."
    ```

    **Target question breakdown (15-30 total, v3 split):**
    - **Ratchet-critical pool (minimum 12, maximum 22):** deterministic grading via `enumerable` / `set_membership` / `numeric`. Includes 3-5 adversarial questions (conditional imports, dynamic resolution, star imports). This pool is what primary_metric is computed against.
    - **Exploratory pool (minimum 3, maximum 8):** open-ended / qualitative questions graded via rubric or LLM-majority-of-three (post-v0). Reported but never ratchets champion selection.

    **ab_answer_key.yaml format (v3) — typed per §6.4 judge split:**
    ```yaml
    q01:
      pool: ratchet_critical
      answer_type: set_membership
      values: ["httpx._transports.default", "httpx._config", "httpx._exceptions"]
    q15:
      pool: ratchet_critical
      answer_type: numeric
      value: 4
      tolerance: 0
    q22:
      pool: exploratory
      answer_type: open_ended
      rubric: "Answer should cover: (1) AsyncBaseTransport / BaseTransport hierarchy, (2) default HTTP/1.1 + HTTP/2 split, (3) MockTransport test use."
    ```

    **Validator enforcement (§6.4 + .015 `ab_answer_key_validator.py`):** at load time, every `pool: ratchet_critical` entry MUST have `answer_type` ∈ `{enumerable, set_membership, numeric}`. `open_ended` in the ratchet pool raises `RatchetPoolOpenEndedRejected` citing the offending `id`. Do NOT try to work around this — if a question can't be answered deterministically, flip its pool to `exploratory`.

    **target_version.txt format:**
    ```
    sha256=<64-hex-chars>
    computed_at=<iso8601>
    inputs=imports_gold.jsonl+ab_questions.yaml+ab_answer_key.yaml+httpx_source_tree
    ```
    Generated via `python -c "from comp.bench.cache import compute_target_version; print(compute_target_version('comp/targets/httpx/'))"` (helper ships with .015). Committed alongside the gold. Any edit to gold inputs bumps this hash; prior cache entries are orphaned per §6.4.1.
  </wire_contract>

  <acceptance_criteria>
    1. `imports_gold.jsonl` loads cleanly via `bench.structural.load_gold()` (function shipped by .015).
    2. Record count matches hand-counted tally in GOLD_SURVEY.md.
    3. **Attribute coverage:** `jq -r '.attributes.resolution' imports_gold.jsonl | sort -u` returns `dynamic\nstatic`; `jq -r '.attributes.guard' imports_gold.jsonl | sort -u` returns `conditional\nunconditional`; `jq -r '.attributes.binding' imports_gold.jsonl | sort -u` returns `resolved\nunresolved` (**all six dimension values present in gold**).
    4. If any dimension value is absent, CTO surfaces to COO~Z before commit — decision: pick a different inaugural target OR synthetic-extend httpx. Do NOT ship gold with missing dimension values — it defeats the §4.5 invariant test.
    5. `ab_questions.yaml` contains 15-30 questions; ratchet_critical pool has 12-22 entries (incl. 3-5 adversarial); exploratory pool has 3-8 entries. **Every question has a `pool` field.**
    6. `ab_answer_key.yaml` has an entry for every question ID; every entry has `answer_type`. **Ratchet-pool entries have `answer_type` ∈ `{enumerable, set_membership, numeric}` only.**
    7. **Ratchet-pool validator PASSES (NEW v3):** `python -c "from comp.bench.ab_answer_key_validator import validate; validate('comp/targets/httpx/gold/ab_answer_key.yaml')"` exits 0 with no `RatchetPoolOpenEndedRejected` raise. This is the §6.4 judge-split enforcement — if any ratchet entry is `open_ended`, the validator raises and commit halts.
    8. **target_version.txt committed alongside gold.** File contains a 64-char SHA-256 hex line. `python -c "from comp.bench.cache import compute_target_version; import sys; actual = compute_target_version('comp/targets/httpx/'); stored = open('comp/targets/httpx/gold/target_version.txt').read().split('=')[1].split()[0]; sys.exit(0 if actual == stored else 1)"` exits 0 (stored hash matches recomputed hash).
    9. `GOLD_SURVEY.md` documents authoring process: modules read, time spent, ambiguities resolved, deliberate choices made (e.g., how `TYPE_CHECKING` guards were counted), ratchet-vs-exploratory classification rationale for borderline questions.
    10. **Gold-before-code attestation (in GOLD_SURVEY.md):** explicit sentence — "Gold was authored without running comp/compiler_subtypes/imports.py against httpx. Calibration on .013 synthetic fixtures allowed; cross-checking against .013 output not allowed."
    11. Session log `## Compiler Tools` reproduces every `<run>` below with observed output + pass/fail vs. `<expect>`. Missing rows = REWORK.
    12. MCP COMPLETE to 2.0.0_SA_COO~Z with commit hash + gold record count + attribute coverage table + ab_question pool breakdown (ratchet_critical count / exploratory count / adversarial count) + target_version hash.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>ls comp/targets/httpx/httpx/</run>
        <expect>Source tree exists — confirms PRD #2 Phase 0 shipped.</expect>
        <if_mismatch>STOP. httpx source tree missing; `fd2d0515` delivery state issue. Escalate to Andrew.</if_mismatch>
      </step>
      <step>
        <run>find comp/targets/httpx/httpx -name "*.py" | wc -l</run>
        <expect>Non-zero .py file count (typically ~30 modules — GOLD_SURVEY.md documents the exact number).</expect>
        <if_mismatch>Sparse or empty tree — re-fetch httpx target.</if_mismatch>
      </step>
      <step>
        <run>grep -rn "TYPE_CHECKING\|importlib" comp/targets/httpx/httpx/ | head -20</run>
        <expect>Non-zero matches — confirms the target contains conditional + dynamic imports so the gold can exercise all six dimension values.</expect>
        <if_mismatch>If zero matches, flag to COO~B — pivot target choice OR synthetic-extend httpx before gold authoring.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>jq -r '.attributes | keys[]' comp/targets/httpx/gold/imports_gold.jsonl | sort -u</run>
        <expect>Output is exactly three lines: `binding`, `guard`, `resolution`. Every gold record has all three dimensions populated.</expect>
        <if_mismatch>Fix gold — every record must have all three dimensions.</if_mismatch>
      </step>
      <step>
        <run>for d in resolution guard binding; do echo "=== $d"; jq -r ".attributes.$d" comp/targets/httpx/gold/imports_gold.jsonl | sort -u; done</run>
        <expect>resolution shows both `dynamic` and `static`; guard shows both `conditional` and `unconditional`; binding shows both `resolved` and `unresolved`. **All six dimension values present.**</expect>
        <if_mismatch>STOP. Flag to COO~Z — either pivot target or synthetic-extend httpx. Do NOT ship gold that defeats the §4.5 invariant test.</if_mismatch>
      </step>
      <step>
        <run>python -c "import yaml; q = yaml.safe_load(open('comp/targets/httpx/gold/ab_questions.yaml')); a = yaml.safe_load(open('comp/targets/httpx/gold/ab_answer_key.yaml')); rc_q = sum(1 for x in q if x['pool']=='ratchet_critical'); ex_q = sum(1 for x in q if x['pool']=='exploratory'); print(f'Q_total:{len(q)} ratchet:{rc_q} exploratory:{ex_q} A:{len(a)} match:{set(x[\"id\"] for x in q)==set(a.keys())}')"</run>
        <expect>Q_total between 15 and 30; ratchet between 12 and 22; exploratory between 3 and 8; ratchet + exploratory == Q_total; A count equals Q count; ID sets match.</expect>
        <if_mismatch>Fix mismatch — ensure every question has a `pool` field and pool populations fall in the specified ranges.</if_mismatch>
      </step>
      <step>
        <run>python -c "from comp.bench.ab_answer_key_validator import validate; validate('comp/targets/httpx/gold/ab_answer_key.yaml'); print('VALIDATOR_PASS')"</run>
        <expect>Prints `VALIDATOR_PASS`. No `RatchetPoolOpenEndedRejected` raise. §6.4 judge-split satisfied: every ratchet-pool entry has `answer_type` ∈ `{enumerable, set_membership, numeric}`.</expect>
        <if_mismatch>STOP. A ratchet-pool entry is open-ended — either make its answer deterministic (enumerable/set_membership/numeric) or flip its pool to `exploratory`. Do NOT bypass the validator; R14 defense depends on it.</if_mismatch>
      </step>
      <step>
        <run>python -c "from comp.bench.cache import compute_target_version; print(compute_target_version('comp/targets/httpx/'))" > /tmp/target_version_actual.txt && diff <(grep -oE 'sha256=[a-f0-9]{64}' comp/targets/httpx/gold/target_version.txt | head -1 | cut -d= -f2) <(cat /tmp/target_version_actual.txt | tr -d '[:space:]') &amp;&amp; echo "TARGET_VERSION_MATCH"</run>
        <expect>Prints `TARGET_VERSION_MATCH`. Stored target_version hash matches recomputed hash — gold is frozen.</expect>
        <if_mismatch>Regenerate target_version.txt from the current gold state and re-commit. Cache-invalidation correctness depends on this.</if_mismatch>
      </step>
      <step>
        <run>grep -l "Gold was authored without running" comp/targets/httpx/gold/GOLD_SURVEY.md</run>
        <expect>Matches. Gold-before-code attestation is present.</expect>
        <if_mismatch>Add the attestation sentence. This is the R1 mitigation paper trail.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>python -c "from comp.bench.structural import load_gold; g = load_gold('comp/targets/httpx/gold/imports_gold.jsonl'); print(f'records={len(g)}')"</run>
        <expect>Prints non-zero record count. Gold loads through bench loader cleanly.</expect>
        <if_mismatch>If .015 bench.structural.load_gold has not shipped, skip this step and note in session log.</if_mismatch>
      </step>
      <step>
        <run>python -c "from comp.bench.ab_answer_key_validator import validate; from comp.bench import load_ab_questions; validate('comp/targets/httpx/gold/ab_answer_key.yaml'); q = load_ab_questions('comp/targets/httpx/gold/ab_questions.yaml'); rc_ids = {x['id'] for x in q if x['pool']=='ratchet_critical'}; print(f'ratchet_pool_question_ids={sorted(rc_ids)}')"</run>
        <expect>Prints ratchet-pool ID list. No validator raise. Confirms the .015 validator accepts this gold end-to-end as the authoritative ratchet pool for primary_metric.</expect>
        <if_mismatch>If .015's `ab_answer_key_validator` / `load_ab_questions` has not shipped yet, skip this step and note in session log — the phase-2 inline validator call already proves correctness.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <risks>
    <risk id="R1">**Benchmark dishonesty — gold authored to match compiler output. (Medium/Critical)** Mitigation: **Gold-before-code invariant enforced by attestation in GOLD_SURVEY.md. .013 extractor is NOT consulted during gold authoring. Mutation engine (.021) is the second line of defense against biased gold.**</risk>
    <risk id="R3">Subtype explosion. (High/High) Mitigation: **Gold records use dimensional attributes per §4.5. Gold never emits flat-string subtype names.**</risk>
    <risk id="R4">Scope creep. (High/High) Mitigation: **httpx only. imports only. No multi-target gold, no multi-subtype gold.**</risk>
    <risk id="R7">Legacy churn. (Low/Medium) Mitigation: gold lands in `comp/targets/httpx/gold/` — new directory. Does not touch framework or legacy extractors.</risk>
    <risk id="R14">**Judge drift — ratchet questions with fuzzy answers will drift across LLM re-runs feeding primary_metric. (Medium/Critical)** Mitigation: ratchet pool is typed (`enumerable` / `set_membership` / `numeric` only); `.015`'s `ab_answer_key_validator.py` raises `RatchetPoolOpenEndedRejected` on any open-ended ratchet entry at load time; CTO MUST classify every question rigorously — if it can't be mechanically graded, it belongs in the exploratory pool. `target_version.txt` freezes the gold; editing any gold input bumps the hash and orphans the cache (§6.4.1). Without this discipline, primary_metric drifts and R14 is back.</risk>
  </risks>

  <dependencies>
    <dependency to="COMP_LEARNS.011" status="preferred">Scorecard + pool-typed answer key schema lands here. Gold can be authored in parallel; validator integration gates Phase 3.</dependency>
    <dependency to="COMP_LEARNS.015" status="preferred-parallel">`ab_answer_key_validator.py` + `compute_target_version()` ship here; Phase 2 validator step is gated on .015 landing (fallback: CTO ships inline validator stub in this TO if .015 slips past gold authoring).</dependency>
  </dependencies>

  <cross_domain_coordination>
    **v3 sweep marker (2026-04-20 COO~Z):** swept from v2→v3 per CTO checklist 2026-04-16 13:59Z (preserved in ~B handoff log). Deltas applied: ratchet/exploratory question-pool split (§6.1, §6.4), typed ab_answer_key with validator enforcement of deterministic answer types in ratchet pool (§6.4), `target_version.txt` frozen gold hash (§6.4.1 cache-invalidation discipline), R14 risk added, pool breakdown enforcement in Phase 2 + validator Phase 3.

    **Validator dependency:** Phase 2 + Phase 3 validator steps assume `.015` has shipped `ab_answer_key_validator.py` + `compute_target_version()`. If .015 has not landed when CTO reaches Phase 2, CTO ships an inline validator stub in this commit (temporary; .015 swap-in on its commit). Flag to COO~Z for coordination.
  </cross_domain_coordination>

  <next>On commit + MCP COMPLETE to 2.0.0_SA_COO~Z: .013 precision/recall gate clears; .015 A/B + `ab_answer_key_validator` have real ratchet-pool to validate against; .017 ratchet's KEEP cycle has honest scoring under §6.4.1 cached-answer regime.</next>
</task_order>
