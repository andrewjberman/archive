<to_id>ADVI_TAGATTR.DS-2</to_id>
<project>ADVI_TAGATTR</project>
<title>DS-2 -- served advisor AUA basis = a SHARED 2-way toggle (default no_infer), single-sourced across D_00c/D_00f/D_02/D_01 + stamped into the served artifact. D_02+D_01 stop crediting 49F House / impl-pairing-inferred accounts (served MOVE); D_00c/D_00f = no-op-at-default rewire. Keep Layer-2. Firm = 49F (BD).</title>
<assigned_to>0.4.0_DS_ClientPlatform</assigned_to>
<issued_by>Andrew-direct 2026-07-01 (accepted 0.4.0_DS recommendation; staged by 0.4.0_DS)</issued_by>
<consult>0.4.0_DE_ClientPlatform (FE consumer of served total_aua + PartnerAnalytics ADV); 1.0.0_SA_CTO (arch-gate -- served-number move); 2.0.0_SA_COO (blast-radius + sequencing); 3.0.0_SA_CVO (served-verify of the number movement)</consult>
<issued_date>2026-07-01</issued_date>
<status>complete -- SPRING-CLEAN 2026-08-25: closed WITH its project ADVI_TAGATTR, which was closed the same day for having no directive attachment. Closed as a record act, not a work verdict; the work is recoverable by re-minting the project. Prior status: deferred</status>
<deferred_note by="Andrew-direct 2026-07-01">SHELVED (not cancelled-wrong; deliberately deprioritized). Andrew: the affected surface (per-advisor served total_aua / advisor-detail views) is low-usage, and the current inferred-basis number is DEFENSIBLE/EXPLAINABLE if ever questioned (the served total_aua uses the C_07 Layer-3-inferred architect, which credits 49F House / orphan accounts to the modal/likely advisor -- a "coverage" attribution, not a bug). So the served-number MOVE (down ~$336.8M firm-wide de-attributed; top movers Kyle Sims -38%, Travis -19%, Greg Rosner -26% -- preliminary dry-run) is NOT worth the CTO-gate + never-widen + Andrew-magnitude-confirm ceremony for a low-traffic view. The finding is banked (memory/reference_bd_architect_inference_no_infer_split.md) as a documented, explainable known-gap. Re-open only if the surface's usage/importance changes or someone questions the numbers. No toggle built; no numbers moved; leg-1 (split-weighting fix) + leg-2 (fee labeling, ~A 3ba105354) stand.</deferred_note>
<priority>MEDIUM -- correctness/consistency, NOT a P0. The served numbers have carried the inferred rollup for a while; this is a grounded correctness fix Andrew flagged, sequenced AFTER TAGATTR.DS-1 leg-1 validates. Moves a live advisor-facing number (downward) -> gated on CTO arch + Andrew-confirm before serve.</priority>

<andrew_context>
Andrew-direct 2026-07-01 (while DS was in the TAGATTR attribution code): "make sure we're not doing any normalizing of assigning AUA to advisors who are not explicitly tagged to an account (unassigned or 49F House) ... e.g. rolling up ownership to relationship level for untagged accounts." DS grounded that we DO (report banked memory/reference_bd_architect_inference_no_infer_split.md), Andrew accepted the DS rec to fix it on the served advisor-AUA surfaces. This TO is that fix.
</andrew_context>

<grounding>
Source-grounded 2026-07-01 (DS, Rule 22):
- C_07.advisor_attribution.py emits TWO architect columns: `architect` (Layer-3 inferred: resolve_architect L232-262 -- T1 relationship modal-real applied incl. 49F House; T2 impl-pairing GUESS) and `architect_no_infer` (resolve_architect_no_infer L269-307 -- 49F House PRESERVED as its own bucket, blank->relationship modal REAL architect [Layer-2 only], residual Unassigned).
- Only 4 files read `architect_no_infer` today: D_00c (leaderboard role_breakdown), D_00f (canonical NNA), lib/advisor_nna_attribution.py, C_07. This is the ADVI_NNAATTR F-0 basis (Andrew 2026-06-17) -- Layer-3 turned OFF because it over-credited individuals with the $357.6M 49F House book. That ruling was scoped to leaderboard + canonical NNA; the ~14 other consumers were left on the inferred `architect` (incomplete migration, not a deliberate carve-out).
- The two consumers that attribute AUA on the inferred `architect`:
  * D_02.advisor_client_detail.py: overlays architect with the Layer-3 `resolved_architect` (_load_rel_lookup L354-359 -> apply L3155-3166) and sums book total_aua over any-role membership (L1235-1260). book.json summary.total_aua therefore INCLUDES Layer-3-inferred (incl. impl-paired House/blank) accounts. D_04 sources the SERVED platinum/firm/leaderboard.json total_aua from D_02 book.json (D_04 L2311-2313) -> the served advisor total_aua + AdvisorPublicProfile carry the rollup.
  * D_01.partner_analytics.py: PartnerAnalytics ADV view (AUA-by-architect donut) uses the inferred architect (rel_arch_lookup L355 = rel_lookup['architect']; account_team fallback L359-362), not architect_no_infer.
- FEASIBILITY confirmed: account_team (which carries architect_no_infer) is ALREADY loaded in both D_02 (_load_account_team L364/L463/L473) and D_01 (ACCOUNT_TEAM L359). So the migration is a source-repoint, not a new load.
- Post-TAGATTR.DS-1 the SAME served leaderboard entry mixes bases: role_breakdown[role].aua uses architect_no_infer (House excluded) while total_aua uses D_02's Layer-3-inferred architect (House rolled up). This TO removes that inconsistency.
</grounding>

<toggle_design andrew_direct="2026-07-01 -- keep it as a toggle, 2-way">
Implement the basis as a SINGLE SHARED, ARTIFACT-STAMPED, 2-way TOGGLE -- NOT a per-script hard-repoint (a per-script toggle would REINTRODUCE the exact drift this fixes: D_00c on no_infer while D_02 on inferred).
- ONE source of truth: a shared selector in lib (e.g. lib.advisor_nna_attribution ARCHITECT_BASIS, env-overridable ADVI_ARCHITECT_BASIS) = `no_infer` (DEFAULT) | `inferred`. NO third level (2-way per Andrew; explicit-tag-only would need a C_07 column -- OUT of scope).
- ALL FOUR advisor-AUA producers read that ONE selector so they always move together: D_02 + D_01 (the served MOVE; today inferred -> default no_infer) AND D_00c + D_00f (today hard-no_infer -> now READ the selector; NO-OP at the default -- their served numbers must stay BYTE-UNCHANGED at no_infer).
- STAMP the active basis into the served artifacts (`attribution_basis: "no_infer"` in book.json / leaderboard.json / partner_analytics ADV) so the served number self-documents which basis produced it (CVO/FE/audit assertable).
- FLIPPING the toggle is a DELIBERATE GATED DEPLOY (config-as-code, versioned), NOT a runtime env-flip on a live financial number -- a flip carries the same never-widen + CVO-verify + Andrew magnitude-confirm as any served move. Default no_infer is correct; `inferred` retained for revert/A-B.
- bd/cot-pipeline scope only: inf uses a separate orion per-advisor attribution (not C_07 no_infer) -- untouched.
</toggle_design>

<scope>
Ship the shared toggle (default no_infer). At the default, migrate the 49F (BD) SERVED advisor-AUA attribution from the Layer-3-inferred architect to architect_no_infer, on the TWO consumers that attribute AUA:
1. D_02.advisor_client_detail.py: replace the Layer-3 `resolved_architect` overlay (L3155-3166) source with account_team.architect_no_infer so book.json summary.total_aua (the SERVED advisor total via D_04) no longer credits 49F House / impl-pairing-inferred accounts to named individuals. (Other-role attribution -- implementor/consultant/etc -- is unchanged; only the architect-role inference source changes.)
2. D_01.partner_analytics.py: switch the ADV-view architect source (L355/L916-929) to architect_no_infer so the PartnerAnalytics architect AUA donut matches the same basis.

KEEP Layer-2 (blank-architect account inherits the relationship's modal REAL architect) -- architect_no_infer already includes Layer-2, so "use architect_no_infer" = "kill Layer-3 (House + impl-pairing guess), keep Layer-2 (real-sibling inheritance)" by construction. Do NOT turn off Layer-2 (that is a separate, more-aggressive call Andrew has NOT made -- it would shrink every book to literal tags + dump accounts to Unassigned).

DO NOT touch the other ~12 inferred-`architect` consumers (they use architect for labels, not AUA attribution) -- scoped to the two AUA surfaces only. DO NOT touch inf (INF_D_02 uses a separate orion-based per-advisor attribution, NOT the C_07 architect_no_infer mechanism) or cot (no segmentable advisor dimension). Firm separation held (bd tree only).
</scope>

<arch_gates issued_by="pending 1.0.0_SA_CTO" status="REQUIRED before serve">
1. SERVED-NUMBER MOVE (CTO arch-gate + Andrew-confirm). This LOWERS each 49F advisor's served total_aua by the House/impl-paired AUA they were over-credited (the firm's House/orphan AUA stops appearing under named individuals). That is the intended correctness effect, but it moves a live advisor-facing number DOWN -> CTO arch-gate on the change + Andrew-confirm the downward shift + magnitude BEFORE it serves. Quantify the per-advisor delta (and the firm-level total of what de-attributes) on a dry-run/pre-serve basis for the confirm.
2. FIRM-TOTAL INVARIANT. After migration, sum(advisor total_aua) will drop further below the firm total (more non-additive) -- confirm NO consumer sums advisor total_aua to a firm total (ties to TAGATTR.DS-1 ARCH-GATE 1; DE already verified the firm total renders from the client-level artifact, not advisor sums).
</arch_gates>

<compiler_tools_mandate>
  <phase id="1" when="before write"><step><run>comp-pipescript io D_02.advisor_client_detail + D_01.partner_analytics</run><expect>consumers of book.json total_aua + PA ADV; confirm D_04 total_aua source path.</expect></step><step><run>comp-blast D_02 + comp-blast D_01</run><expect>every consumer of the changed AUA fields; confirm the ~12 label-only consumers are NOT AUA-attributing.</expect></step></phase>
  <phase id="2" when="before commit"><step><run>.tools/ds-commit-gate.sh</run><expect>py_compile + AST + ruff clean; from __future__ import annotations.</expect></step></phase>
  <phase id="3" when="after commit / on the SCHEDULED nightly artifact"><step><run>comp-validate D_02/D_01 --artifact &lt;served book.json / leaderboard.json / partner_analytics ADV&gt;</run><expect>PASS; served advisor total_aua no longer includes 49F House / impl-paired accounts; role_breakdown + total_aua now share the no_infer basis; Layer-2 (real-sibling) attributions PRESERVED.</expect><if_mismatch>STOP; do not signal DE/CVO safe.</if_mismatch></step></phase>
</compiler_tools_mandate>

<cross_domain_coordination>D_02 -> D_04 (D_04 sources served leaderboard total_aua from D_02 book.json L2311-2313); D_01 -> PartnerAnalytics ADV. Sequence AFTER TAGATTR.DS-1 leg-1 validates on the nightly (clean baseline; both touch the same served advisor artifact -- do not confound). FE (AdvisorPublicProfile total_aua hero + PartnerAnalytics ADV) is DE-owned; the number moves but the shape does not (zero FE change expected -- DE confirms render + the moved number is expected).</cross_domain_coordination>

<acceptance_criteria>
1. A SINGLE shared basis selector exists (lib, env-overridable, `no_infer` default | `inferred`), and ALL FOUR advisor-AUA producers (D_00c, D_00f, D_02, D_01) read THAT ONE selector -- no per-script hard-code, no drift path. 2-way only (no explicit-tag-only / no C_07 column add).
2. The served artifacts stamp the active basis (`attribution_basis` in book.json / leaderboard.json / partner_analytics ADV).
3. Toggle REVERTS cleanly: setting the selector to `inferred` reproduces the pre-DS-2 (Layer-3) served numbers (dry-run-provable), confirming it is a true toggle, not a one-way migration.
4. At the DEFAULT (`no_infer`): on the served nightly artifacts (scheduled nightly, NOT ad-hoc), 49F advisor total_aua + ADV-donut AUA no longer credit 49F House / impl-pairing-inferred accounts to named individuals.
5. D_00c + D_00f served output BYTE-UNCHANGED at the default (they already produced no_infer; the rewire to read the selector is a no-op at default -- prove unchanged, must not move DS-1 leg-1's leaderboard numbers).
6. Layer-2 PRESERVED: a blank-architect account still credits the relationship's modal REAL architect (advisors do NOT lose real-sibling-inherited accounts; only House + impl-pairing-guesses removed).
7. role_breakdown[role].aua (DS-1) and total_aua (this TO) share the no_infer basis on the same served entry -- the mixed-basis inconsistency is gone.
8. The ~12 label-only inferred-architect consumers UNTOUCHED; inf + cot UNTOUCHED; firm separation held (bd tree only; comp-pipescript deployed MATCH, 49F-only).
9. Pre-serve delta quantified (D_02/D_01 downward shift) + CTO arch-gate + COO never-widen co-sign + Andrew magnitude-confirm obtained BEFORE it serves. Flipping the toggle later carries the SAME gate (it is not a casual env-flip).
10. Session-log Compiler Tools reproduces the mandate. RAVC2 to COO + CTO + DE (CC CVO); CVO served-verifies the number movement + confirms attribution_basis stamp.
</acceptance_criteria>

<references><ref type="source">data/black_diamond/scripts/gold/D_02.advisor_client_detail.py (L354-359 resolved_architect load; L3155-3166 overlay; L1235-1260 total_aua over role_mask); D_01.partner_analytics.py (L355 rel_arch_lookup; L916-929 ADV multi-role AUA); C_07.advisor_attribution.py (L232-262 resolve_architect Layer-3; L269-307 resolve_architect_no_infer)</ref><ref type="precedent">ADVI_NNAATTR F-0 (Andrew 2026-06-17) -- Layer-3-off basis for leaderboard + canonical NNA; this extends it to the served advisor total_aua + ADV.</ref><ref type="memory">memory/reference_bd_architect_inference_no_infer_split.md</ref></references>
<lane_note>DS owns the D_02/D_01 gold-script change (rule 13). DE owns the FE (number moves, shape unchanged). GATE: land on the scheduled nightly, never ad-hoc; sequenced after DS-1 leg-1 validates; CTO arch-gate + Andrew-confirm on the served-number move before serve.</lane_note>
