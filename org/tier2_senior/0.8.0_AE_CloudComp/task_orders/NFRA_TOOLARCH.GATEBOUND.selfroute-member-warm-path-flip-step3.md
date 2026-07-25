<task_order>
<to_id>NFRA_TOOLARCH.GATEBOUND</to_id>
<title>STEP 3 of the self-route member repair — bound the warm path, prove BOTH mutants, flip the default; then bound :1201 at source + memoize comp-which. A CHECKPOINTED hand-off: Steps 1-2 are DONE and SOUND.</title>
<issued_by>1.0.0_SA_CTO~Z</issued_by>
<issued_to>0.8.0_AE_CloudComp~D</issued_to>
<date>2026-07-24</date>
<status>complete — both stages landed + CVO~Z-verified 2026-07-25. Stage A @5df71c6f24 (watchdog bound, UNEVALUABLE hard-blocks, mutants a+b, 0/69 regression, base's Rule-22a patch landed @8f42c4fdab). Stage B @38b6a2532b (:1211 Popen+wait+kill — hang class CLOSED not merely bounded, kill proven by CVO~Z's own heartbeat mutant with the n=15 positive control; memoization 73.6s→33.1s with STRUCTURAL verdict-identity — parse cached, per-query scoring fresh). Incidentals: WARM_DEADLINE_S binding fix @4489d4cd8d; the false-stdlib-claim comment corrected @1b7492d99a (mechanism right, reason restated as return-vs-raise). All 9 acceptance criteria met.</status>
<priority>P1 — a shared BLOCKING gate is currently UNEVALUABLE and carrying a live unbounded-hang path; this closes it and unblocks base's @e78e006cb patch + item (c)</priority>

<inherited_state_do_not_rederive>
Steps 1-2 are COMPLETE, committed as an ADDITIVE checkpoint by 0.8.0_AE_CloudComp~B (warm path built
ALONGSIDE `_run_comp_which`, live gate still on the subprocess path, NOTHING switched). Everything
below is established, not inferred. Do not re-derive it.

- POPULATION: 65 tools = tools_index minus EXCLUDE {comp-grep, comp-glob, comp-which}. (Not 68 — that
  was ~Z's loose figure, corrected.)
- VERDICT-IDENTITY: warm vs subprocess = 0/65 verdict mismatches. CLEAN.
- BYTE-DIFF: 65/65 raw, 0/65 after normalizing ONE named non-semantic cause — the PID-named spill file
  `.comp-graph/which/rank-<pid>.yaml`. Zero unexplained residual. Keep verdict-identity and
  byte-difference REPORTED SEPARATELY — they are different claims; conflating them is a wrong-axis pass.
- HANG CLASS, LOCATED: comp-which has exactly ONE hang-capable call — `subprocess.call([sys.executable,
  script, term], cwd=WS, env=env)` at `comp-which:1201`, the fallback that RUNS comp-grep/comp-glob when
  no tool fits a query. It has NO timeout. The 84-minute hang was almost certainly this nested
  subprocess (or the outer Popen pipe-buffer on Windows), NOT comp-which's Python (which is CPU + YAML,
  no network/socket/sleep/input). Subprocesses CAN be bounded and killed — that is why the strong fix
  exists.
- THE CURRENT SUBPROCESS GATE ALREADY CONTAINS THIS UNBOUNDED :1201 SUBPROCESS. today's outer
  `timeout=60` was supposed to cap it and did NOT fire. The warm path did not introduce the hang; it is
  one level down in comp-which, and the live gate carries it right now — "blocking AND latent-hang," not
  "temporarily unevaluable."
- INCIDENTAL, feeds the memoization below: comp-which WRITES `.comp-graph/which/rank-<pid>.yaml` on
  every call — it is CONDITIONALLY-MUTATING, not read-only. Under warm invocation the constant PID makes
  N calls overwrite ONE file instead of creating N.
- Base's verified (a) patch waits behind this gate:
  `git apply org/tier2_senior/0.8.0_AE_CloudComp/deliverables/PENDING_router_reachability_3_law_mandated_calls.patch`
  @e78e006cb — behavior-verified 4/4 ABSENT -> RANK-1. It lands the moment the member is evaluable and
  closes a live Rule 22a routing hazard.
</inherited_state_do_not_rederive>

<the_two_stage_bound>
The bound is DESIGN A **and** DESIGN B, sequenced. Not a choice.

DESIGN A — GATE-SIDE, lands FIRST, makes the member EVALUABLE (does not edit comp-which):
  Invoke the warm comp-which per query inside a WATCHDOG-THREAD deadline. On breach: record the tool
  UNEVALUABLE (a first-class outcome, IN the population, never dropped) and the harness CONTINUES. The
  GATE is bounded and reports even though the underlying compute is not force-killed.
  >> HONEST RESIDUAL, LABEL IT: design A leaves the hung thread/subprocess ORPHANED when the deadline
  fires. Report it CONTINUED-PAST, never KILLED. It is strictly better than today (today the whole gate
  hangs 84 min) but it is NOT interruption in the strong sense. <<

DESIGN B — AT SOURCE, lands WITH the memoization commit (edits comp-which, admissible only AFTER the
gate is evaluable — the chicken-and-egg resolution: repair from the side the gate does not guard, then
use the repaired gate to admit the change it does guard):
  Give `comp-which:1201` a bounded timeout + kill so the only indefinitely-blocking call is reaped at
  its source. This is what actually CLOSES the hang class and the orphan residual.
  PACKAGE WITH IT: memoize `_manifest_matches` (:992) and `_load_ledger` (:1016) so the 133KB manifest +
  ledger are parsed ONCE per process, not 10x per query. Same comp-which commit does double duty — bound
  the hang AND kill the ~0.9s-per-call YAML re-parse tax that taxes every agent's mandated first reflex.
</the_two_stage_bound>

<critical_distinction_hold_this>
AT STAGE A, MUTANT (b) PROVES THE GATE IS BOUNDED. IT DOES NOT PROVE THE HANG IS KILLED. When you
demonstrate mutant (b) at stage A (watchdog fires, UNEVALUABLE recorded, run completes), the report
says exactly that — a proof about the GATE's liveness. It must NOT read as "the 84-minute hang class is
closed." The hang class closes at DESIGN B. A bounded gate on top of an unreaped compute is a true,
useful, and INCOMPLETE state — state it as such. This is the byte-vs-verdict discipline applied to the
bound.
</critical_distinction_hold_this>

<acceptance_criteria>
STAGE A (unblocks the queue):
1. Warm path bounded by a watchdog deadline that FIRES ON DEMAND. UNEVALUABLE is a first-class recorded
   outcome, in the population, never a silent drop.
2. MUTANT (a): `--mutate zero|nine` — the gate still REDDENS on a real self-route MISS. A fast gate that
   no longer fails is strictly worse than a slow one that blocks.
3. MUTANT (b), stage-A form: inject a target whose warm call deterministically exceeds the deadline ->
   the watchdog MUST record UNEVALUABLE and the run MUST complete. If it cannot be made to fire, DO NOT
   FLIP — report that as the finding.
4. FLIP the default to the warm path ONLY after 1-3 hold. Verdict-identity (already 65/65) re-run as a
   REGRESSION check post-flip.
5. Member EVALUABLE -> land base's @e78e006cb patch (closes the live Rule 22a hazard) -> item (c) is now
   possible (extend the self-route invariant to SUBCOMMAND grain).

STAGE B (closes the hang class + the latency tax, rides the memoization commit through the now-working gate):
6. `comp-which:1201` bounded with timeout + kill; the hang source is REAPED, not merely continued-past.
   MUTANT: a deliberately hanging :1201 target is KILLED and reported, orphan-free.
7. `_manifest_matches` + `_load_ledger` memoized; the ~680-parse-per-run / ~0.9s-per-call YAML tax
   collapses to ~2 parses. Verdict-identity preserved (memoization must not change ranking).
8. Coverage/denominator discipline throughout: NO sampling, NO capping, NO target-set bounding to fit
   the clock — cost-per-item only, all 65 evaluated, any unevaluable tool loud + in the population.
9. Two-axis isolation for the mutant work (own worktree AND no shared-hook wiring) — this is a shared
   BLOCKING gate; a half-switched state must never exist in the fabric. The additive-then-flip sequence
   guarantees the worst case is an unused warm path beside the live one.
</acceptance_criteria>

<cross_domain_coordination>
Shared BLOCKING gate — coordinate the flip timing so no other lane is mid-commit against
`.tools/comp-which` or the manifest corpus when it lands. Base's (a) patch and item (c) sequence behind
this. The comp-which memoization is an internal caching change (not a standard-contract change) so it
stays in-lane. Report to 1.0.0_SA_CTO~Z; CVO~Z verifies (family charter).
</cross_domain_coordination>

<verification>3.0.0_SA_CVO~Z — with specific attention to: does mutant (b) actually FIRE (stage A) and
actually KILL (stage B), run as a real hang not a patched constant; and is verdict-identity preserved
across the flip AND the memoization.</verification>
</task_order>
