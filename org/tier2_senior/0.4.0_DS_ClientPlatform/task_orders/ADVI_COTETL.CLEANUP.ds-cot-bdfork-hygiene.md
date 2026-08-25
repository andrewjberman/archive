<to_id>ADVI_COTETL.CLEANUP</to_id>
<project>ADVI_COTETL</project>
<title>cot bd-fork hygiene cleanup (post-$24M-close): retire the dead account_gains/C_00/C_02 lots-path + per-class cot-gold ruff cleanup</title>
<assigned_to>0.4.0_DS_ClientPlatform</assigned_to>
<issued_by>2.0.0_SA_COO (COTETL closeout; CTO-flagged 171350Z + 140130Z)</issued_by>
<issued_date>2026-06-22</issued_date>
<status>complete -- SPRING-CLEAN 2026-08-25: closed WITH its project ADVI_COTETL, which was closed the same day for having no directive attachment. Closed as a record act, not a work verdict; the work is recoverable by re-minting the project. Prior status: active</status>
<!-- GO 2026-06-22 1723Z: DS signaled bandwidth (P0 closed, idle-available). NON-URGENT/DS-paced. Sequence (DS-proposed): Leg-1a comp-blast re-confirm 0 live cot consumers -> CTO rules retire-vs-snapshot-wire -> Leg-1c execute; Leg-2 ruff cleanup in parallel (no CTO-gate). Both NON-CORRECTNESS, cot-scoped, firm-separated. -->
<!-- RECONCILE 2026-07-14 (DS, comp-state candidate routed by CTO 073443Z): the C2 cot-map re-scope
     (59249227c, applied+verified 07:2xZ) changes what the MONOLITH mirrors FROM opal-data-cot
     (bronze/ markers -> forwardfill_v2/; opal-data-cot itself untouched per new-territory). This TO's
     items live in the cot GOLD tree + SSM chain (C_00/C_02 retire, D_00* fallback branches, C_01 ruff)
     -- none read the mirror's source mapping, so the re-scope changes NOTHING here. Status stays
     `active`: DS half staged-not-committed by design, awaiting the COO-scheduled coordinated
     AE-dechain-FIRST landing window. NOT stale, correctly parked. -->


<objective>
Two same-class bd-fork hygiene items surfaced by the COTETL $24M served-AUA fix (5c80bf6ca, CVO-certified). Both are NON-CORRECTNESS, cot-path-scoped, DS-lane (gold-script Rule-13). The served firm-AUA is CORRECT + certified ($395.30M/06-18); this is debt-cleanup so the dead-fork remnants don't mislead a future toucher.
</objective>

<the_fix>
1. RETIRE the dead lots-FIFO path for cot -- CTO-RULED = RETIRE (not snapshot-wire); pre-gated CLEAN (0-live-consumers, firm-separated, portal refs are comments-not-reads). **DESTRUCTIVE MULTI-LANE -- COORDINATED LANDING, COO-SCHEDULED, HARD SEQUENCE (delete-before-dechain = a gold-chain FAIL):**
   - **DS stages NOW (authored, NOT committed):** comp-blast re-confirm 0 live cot consumers + author the diff = remove the C_00/C_02 fallback branches from D_00/D_00b/D_00c + delete C_00.py/C_02.py (cot-scoped). DO NOT LAND SOLO.
   - **AE lane (goes FIRST or atomic):** drop C_00/C_02 from the cot SSM gold chain (ssm.tf:234) -- the de-chain MUST precede the script-delete.
   - **COO schedules the coordinated DS+AE landing** (AE-dechain-FIRST -> DS-delete-AFTER) on a NON-P0-adjacent clean window, under a deploy-completion ledger (multi-lane destructive). Post-verify: served $395.30M + all 7 @06-18 UNCHANGED on that one nightly. NON-URGENT (0 consumers, zero rush).
2. cot-gold per-class RUFF cleanup: C_01 carries 8 pre-existing bd-fork ruff violations (all OUTSIDE the C00SNAPSHOT change; RULE15 gate-note-bypass documented in 5c80bf6ca). Clean them per-class MANUALLY (py_compile + AST + ruff --select FA must stay green), NOT a `ruff --fix` bundle on the live script (banked: bd-fork ruff debt on a live cot gold script). Sweep the broader C_01/C_03 bd-fork debt in the same pass if cheap.
</the_fix>

<compiler_tools_mandate>
  <step><run>comp-blast account_gains + comp-pipescript io C_00/C_02 (cot)</run><expect>0 LIVE cot consumers of the dead path (re-confirm the cert finding) before retiring</expect></step>
  <step><run>ds-commit-gate (py_compile + ds-precommit-check + ruff FA) per touched script</run><expect>PASS; the per-class ruff cleanup makes C_01 ruff-clean WITHOUT a --fix bundle</expect></step>
  <step><run>safe-commit (cot-tree only) + comp-pipescript deployed (firm-sep)</run><expect>49F/bd ZERO-touch (firm-separated, like the C00SNAPSHOT fix)</expect></step>
</compiler_tools_mandate>

<acceptance_criteria>
1. Dead account_gains/C_00/C_02 cot path retired-or-snapshot-wired per CTO's (a)/(b) confirm; comp-blast re-confirms no live cot consumer left dangling.
2. C_01 (+ C_03 if swept) ruff-clean WITHOUT a --fix bundle (per-class manual); ds-commit-gate PASS.
3. Firm-separated (cot-tree only; 49F/bd untouched, comp-pipescript deployed MATCH).
4. Served firm-AUA UNCHANGED at $395.30M/06-18 post-cleanup (this is hygiene, must not move the certified number) -- verify on the next nightly's served artifact, no ad-hoc gold run.
5. Session-log reproduces the comp-runs; RAVC2 COO + CTO.
</acceptance_criteria>
