<task_order>
<to_id>ADHOC.tocheck-issuedto-keying</to_id>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_to>0.7.0_AE_CloudOps~B</issued_to>
<date>2026-08-04</date>
<status>complete</status>
<!-- COMPLETE 2026-08-04T0028Z, CTO no-redline on COO acceptance flex (002748Z flag, 002826Z
     accept). PREMISE FALSIFIED HONESTLY: to-check.py was ALREADY issued_to-keyed (:211/:136/
     :419-422) -- ~B's discriminating pair proved CORRECTNESS (lane query surfaces the
     lane-issued base-foldered CI-R7R8, excludes five same-folder siblings issued elsewhere).
     AC-2 UNSATISFIABLE BY CONSTRUCTION, and the WHY is the record (CTO requirement): the
     premise was false, the instrument was already correct, there was no pre-fix state to fail
     -- this is NOT a shortfall in ~B's delivery; THE UNEXERCISED PREMISE WAS THE EXECS' (CTO
     wrote the folder-vs-issued_to framing, COO staged it, neither exercised to-check first).
     AC-1 satisfied (census 293/294 in scope, 21 matches/11 files) + AC-3 satisfied
     (server.py:809-812 measured+flagged only). REAL DEFECTS FOUND INSTEAD, both ruled: the
     default view's PRD-age gate (startup --all line RULED IN, CTO lands the law text); the
     server.py folder-keyed surface (~B owns, sequenced behind the exposure scan + bd review,
     discriminating pair both directions required). -->
<priority>P2 (CTO BUILD ruling 000023Z rider 1: "it is HOW this sat 10 days... cheap and load-bearing." ACTIVATES when the CI-R7R8 fork resolves; you found the class, you fix it.)</priority>

<title>Key TO discovery on `issued_to`, never folder location -- the fix for "a lane reads its own folder, reports IDLE, and carries a live P0"</title>

<context>
Your own near-miss (235659Z): CI-R7R8 is issued_to your lane but lives in the BASE folder, so
your lane-folder read said "queue empty" while you carried an Andrew-direct P0 -- and the
fabric's status instruments showed a clear board for TEN DAYS. CTO (000023Z): "THAT IS THE
MECHANISM OF THIS ENTIRE INCIDENT... Keying to-check/startup tooling on issued_to rather than
folder location converts 'discovered by luck on a reboot' into 'visible every startup' --
THE THIRD TIME TODAY the fix has been to make an existing truth VISIBLE rather than to build
new machinery."

SURFACES TO FIX (enumerate at Phase 1; known members): .tools/to-check.py (the /to-check
engine -- its per-agent rollup must attribute by issued_to across ALL task_orders folders,
base + lane); the startup guidance's "read your folder" framing (org/XXX.md Step 1's TO
discovery -- a DOC edit routes to CTO if the fix needs law text, your report flags it);
list_task_orders / get_agent_status server-side reads if they folder-scope (org/mcp/server.py
-- measure, do not assume). NO alarms/monitors (moratorium) -- this is instrument correctness,
not notification.
</context>

<scope>
1. Census the discovery surfaces: every instrument/read-path that answers "what TOs does agent
   X hold" -- classify each as issued_to-keyed or folder-keyed (file:line @ commit). Denominator
   printed.
2. Fix the folder-keyed ones to attribute by the issued_to field scanned across all
   task_orders/ dirs (base + lane, both tilde families per the XXX.md two-families table).
3. EXERCISE with the real incident as the fixture: CI-R7R8's actual placement (lane-issued,
   base-foldered) must surface under your lane's query post-fix -- and a control TO placed
   normally must not duplicate.
4. Anything law-text (XXX.md wording) is a FLAG to CTO in your report, not an edit.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="census">
    <step>
      <run>comp-grep task_orders across .tools/ + org/mcp/server.py + skills; classify each read path</run>
      <expect>Denominator printed; every discovery surface classified with cites.</expect>
      <if_mismatch>An unclassifiable read path is UNKNOWN-loud, not skipped.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="fix + exercise">
    <step>
      <run>the CI-R7R8 fixture test (lane-issued base-foldered surfaces under lane query) + normal-placement no-duplicate control</run>
      <expect>Both legs pass post-fix; the fixture leg FAILS on pre-fix code (the discriminating pair).</expect>
      <if_mismatch>A pair passing on unfixed code is not discriminating -- redesign.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after">
    <step>
      <run>report to COO + CTO: surfaces census + fix commits + both exercise captures + any law-text flags</run>
      <expect>Every startup henceforth sees lane TOs wherever they live.</expect>
      <if_mismatch>REWORK on missing captures.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
.tools/to-check.py is shared instrument surface -- comp-blast before editing; the 0.8.0~B
universe-audit TO (staged, unspawned seat) is adjacent instrument work but independent -- no
gate between them. server.py changes, if any, are fabric-comms surface: STOP and route to CTO
before editing the broker (measure-only under this TO).
</cross_domain_coordination>

<acceptance_criteria>
1. Discovery-surface census with denominator + cites; folder-keyed paths fixed to issued_to.
2. The CI-R7R8 fixture exercise passes post-fix AND fails pre-fix (discriminating pair captured).
3. server.py/broker: measured + flagged only, never edited under this TO.
Plus: session log Compiler Tools section reproduces every <run> with observed output and
explicit pass/fail vs <expect>. Missing rows = REWORK.
</acceptance_criteria>

<references>
  <ref type="ruling">CTO 20260804T000023Z rider 1 (BUILD)</ref>
  <ref type="incident">Your 235659Z near-miss (the mechanism, verbatim)</ref>
</references>

<dependencies>
  <dependency agent="1.0.0_SA_CTO" task="CI-R7R8 gate verdict (the fork)" status="pending (this TO activates on its resolution)"/>
</dependencies>
</task_order>
