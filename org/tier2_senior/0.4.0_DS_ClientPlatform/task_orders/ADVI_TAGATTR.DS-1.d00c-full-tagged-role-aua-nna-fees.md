<to_id>ADVI_TAGATTR.DS-1</to_id>
<project>ADVI_TAGATTR</project>
<title>DS-1 -- D_00c: advisor role_breakdown = FULL TAGGED (drop split_pct/fee weighting) for AUA + NNA + fees; per-role uses aua_tagged_total. Firm = 49F (BD).</title>
<assigned_to>0.4.0_DS_ClientPlatform</assigned_to>
<issued_by>0.4.0_DE_ClientPlatform (Andrew-direct ruling 2026-07-01, relayed with source grounding)</issued_by>
<consult>0.4.0_DE_ClientPlatform (FE consumer + verification); 2.0.0_SA_COO (blast-radius coordination); 3.0.0_SA_CVO (served-verify)</consult>
<issued_date>2026-07-01</issued_date>
<status>pending</status>
<priority>HIGH -- Andrew-direct; live advisor-facing AUA inconsistency on the 49F AdvisorIntelligence page.</priority>

<andrew_ruling verbatim="near">
"They should not be split weighted. If he's working with a client and tagged to that client, the full amount should be tagged to him. We DO want to split roles in the sense that if Travis is an architect on a $200M account, he should have $200M included in his architect-role AUA. If an implementor is also tagged to the same account, the implementor should also have $200M tagged in his implementor balance. Doesn't matter what fee split they have or anything like that. If they are tagged to it, that full amount is included in their AUA, and tagged in 'Role Decomposition' to the advisorRole (architect, implementor, consultant, etc)."
Scope confirmed by Andrew: full-tagging applies to AUA + NNA + fees (ALL advisor-level + role-level metrics), NOT AUA-display-only.
</andrew_ruling>

<grounding>
DE ground-truthed the LIVE served artifact + producer source before issuing:
- Served s3://opal-data-bd/platinum/firm/leaderboard.json (firm_id=49financial, generated 2026-07-01T05:10Z), advisor travis_penfield, window YTD/MAX:
    total_aua (tagged, dedup)                = 439,968,591.28   <- CORRECT per Andrew (full tagged)
    sum(role_breakdown[*].aua) (split-wtd)   = 358,338,361.06   <- WRONG (split_pct/fee-weighted); gap 81,630,230.22
    role_breakdown: architect 327,494,415.05 / implementor 28,321,282.93 / consultant 1,576,794.00 / additional_advisor 945,869.08
- Producer data/black_diamond/scripts/gold/D_00c.portal_leaderboard.py:
    * total_aua = un-weighted dedup account sum: melted_dedup_acct.groupby('advisor')['total_aua'].sum()  (line ~865; tagged_aua_counts line ~590). CORRECT, keep.
    * role_breakdown[role].aua = split_pct "three-case" weighted (lines ~876-931): weight = split_pct[role] / sum(split_pct[all advisor roles on acct]); Case 3 zeroes non-fee-paying roles; house/zero-split accts excluded (lines ~925-926). THIS is the wrong logic per Andrew.
    * CRITICAL: the canonical role_aua source ALREADY carries `aua_tagged_total` per (date, advisor, role) -- documented at D_00c line ~164 -- but _load_canonical_role_aua_latest() reads ONLY ['date','advisor','role','aua'] (line ~188), dropping aua_tagged_total. The full-tagged per-role number DE wants likely already exists upstream; the fix is to READ + EMIT it.
</grounding>

<scope>
Change D_00c so advisor role-level attribution is FULL TAGGED, not split-weighted, for AUA + NNA + inflows/outflows + fees:

1. role_breakdown[role].aua := FULL account AUA summed over every account where (advisor, role) is tagged, with NO split_pct weighting, NO intra-advisor role normalization, NO fee-paying zeroing. An account where the advisor holds N roles contributes its FULL AUA to EACH of those N role buckets (buckets intentionally do NOT sum to the advisor's dedup total_aua). Prefer the canonical `aua_tagged_total` column (line 164) over recomputation.
2. Same full-tagged treatment for role-level NNA, inflows, outflows.
3. Fees: fee_breakdown / role fee sub-buckets (fee_paying / no_fee) -- full-tag by role too ("doesn't matter what fee split they have"). Reconcile with the C_08/fee-scorecard path; flag to DS+COO if the "three-case" fee rule is consumed elsewhere that must stay split (E_23.diagnose_fee_splits, C_08.advisor_fee_efficiency).
4. Advisor total_aua (dedup, full) is ALREADY correct -- DO NOT change it. Leaderboard + hero already render it.
5. Preserve a per-advisor DEDUP total (total_aua) distinct from the per-role tagged sum -- FE needs both (donut center = dedup total; slices = per-role full-tagged).

DO NOT touch inflection (INF_D_00c is a separate producer; inflection advisors are largely single-role) or cottonwood (no advisors) unless the shared canonical role_aua path forces a firm-separated change -- keep firm separation (NEVER#1).
</scope>

<blast_radius>
comp-blast D_00c + comp-pipescript io/consumers before changing. Known/suspected consumers to check: D_01.partner_analytics (firm-level -- should stay dedup), D_02.advisor_client_detail (book.json -- drilldown overlay), C_08.advisor_fee_efficiency + E_23/E_24 fee scorecard (fee semantics), portal AdvisorsTab (leaderboard partial-role path) + AdvisorPublicProfile Role Composition (DE-owned FE). Non-additivity is EXPECTED + accepted by Andrew (sum of advisor AUAs > firm AUA).
</blast_radius>

<arch_gates issued_by="1.0.0_SA_CTO 2026-07-01" status="REQUIRED before DS lands">
CTO GO'd the direction (full-tag, Andrew-set) but gated the SEMANTICS. Both are BINDING:
1. NON-ADDITIVE LABELING INVARIANT (schema/labeling, enforce not just accept). Full-tagged role_aua is NON-ADDITIVE to firm total. (a) The DS emit MUST label the per-role tagged field DISTINCTLY as advisor-TAGGED / non-additive, NOT firm-AUA (ties to the AUA/NNA-terminology non-negotiable). (b) NO consumer may SUM role_breakdown (or sum advisor total_aua across advisors) and present it as a firm total. DE FE-side verification (DONE, see note): the firm total renders from the CLIENT-level firm artifact (PartnerAnalytics views.aua.current.donut.total / gold_aua), NOT from advisor sums; the lone cross-advisor sum (AdvisorsTab summary.total_aua, line 537) is COMPUTED-BUT-UNRENDERED (latent risk -- DE to remove/guard in the FE follow-on); all other total_aua renders are per-advisor (entry.total_aua). SEV1-adjacent: a non-additive value presented as additive = wrong-number incident.
2. FEE-TAGGING BLAST-GATE (COO lane, CTO-required). comp-blast the FEE surface (role-fee field in D_00c + every fee-scorecard consumer C_08/E_23) BEFORE landing the fee change; enumerate ALL role-fee consumers; confirm each intends the full-tagged fee-BASIS or is excluded/coordinated. Full-fee-per-advisor RE-BASES the fee basis vs the "three-case" split rule -> must not silently change a fee scorecard (C_08 silent-rebasing precedent). Breaking consumer -> STOP + CTO arch-adjudicates. COO is driving this blast; DS executes it before the fee leg lands.
</arch_gates>

<compiler_tools_mandate>
  <phase id="1" when="before write"><step><run>comp-pipescript io D_00c.portal_leaderboard</run><expect>COLUMN GAPS + downstream portal consumers of role_breakdown.aua/nna + fee buckets.</expect></step><step><run>comp-blast D_00c</run><expect>every consumer of the emitted leaderboard.json fields.</expect></step></phase>
  <phase id="2" when="before commit"><step><run>.tools/ds-commit-gate.sh</run><expect>py_compile + ruff clean.</expect></step></phase>
  <phase id="3" when="after commit / on the SCHEDULED nightly artifact"><step><run>comp-validate D_00c.portal_leaderboard --artifact &lt;served leaderboard.json&gt;</run><expect>PASS/WAIVED; role_breakdown[role].aua now == canonical aua_tagged_total per role; travis_penfield architect bucket reflects FULL tagged (no ~$358M split sum).</expect><if_mismatch>STOP, do not signal DE/CVO safe.</if_mismatch></step></phase>
</compiler_tools_mandate>

<cross_domain_coordination>D_00c is the SOLE writer of s3://opal-data-bd/platinum/firm/leaderboard.json. Fee-bucket change may cross C_08/E_23 -- coordinate with whoever owns the fee scorecard before altering shared fee semantics. FE (AdvisorsTab role-filter path + AdvisorPublicProfile Role Composition donut) is DE-owned and will be adjusted AFTER this lands (donut center -> dedup total_aua; slices -> per-role full-tagged; remove the false "roles reconcile to Total AUM" helpText).</cross_domain_coordination>

<acceptance_criteria>
1. On the served leaderboard.json (scheduled nightly, NOT an ad-hoc gold run), travis_penfield: role_breakdown[architect].aua reflects the FULL tagged AUA of his architect-tagged accounts (per-role aua_tagged_total), and the same for every role; the per-role numbers are un-weighted (no split_pct / no fee zeroing).
2. total_aua unchanged at the dedup tagged value (~439.97M) -- FE hero/leaderboard still correct.
3. NNA + inflows/outflows + fee sub-buckets at the role level are full-tagged consistently.
4. A short note back to DE stating whether aua_tagged_total was available in the canonical role_aua source (preferred) or had to be recomputed, and the blast-radius result for the fee path.
5. Session log Compiler Tools section reproduces the mandate. RAVC2 to DE (CC COO + CVO).
6. ARCH-GATE 1 (labeling): the emitted per-role tagged field is named/labeled as advisor-TAGGED (non-additive), distinct from firm-AUA; no field invites cross-advisor summation as a firm total. (DE verifies the FE side; DS ensures the schema/label side.)
7. ARCH-GATE 2 (fee blast): comp-blast of the fee surface (D_00c role-fee + C_08/E_23) run BEFORE the fee leg lands, with every role-fee consumer enumerated + confirmed intending the full-tagged basis (or excluded/coordinated). Breaking consumer -> STOP + escalate to CTO. RAVC the fee-blast result to COO+DE before landing fees.
</acceptance_criteria>

<nightly_validation_runbook note="COO-requested fresh-DS handoff -- run if the base session is not live at the bd nightly ~04:00Z. leg-1 code = 0ab172d3f (D_00c) + fc8c18361 (D_04), deployed+MATCH; leg-2 = 3ba105354 (~A, fee labeling+assert).">
After the bd nightly regenerates s3://opal-data-bd/platinum/firm/leaderboard.json (data_as_of advances):
1. comp-validate D_00c.portal_leaderboard --artifact &lt;served leaderboard.json&gt; -> expect PASS/WAIVED.
2. Pull served leaderboard.json; travis_penfield (any window): role_breakdown[architect].aua = FULL tagged AUA of his architect accounts (NOT ~358,338,361 the old split-weighted role-sum); role buckets NON-ADDITIVE (sum role.aua > total_aua is EXPECTED); each role rd has aua_basis="tagged_full_nonadditive"; top-level role_breakdown_semantics="advisor_tagged_full_nonadditive".
3. total_aua UNCHANGED ~439,968,591 (dedup, from D_02 book.json via D_04).
4. PASS -> RAVC2 0.4.0_DE_ClientPlatform (CC 2.0.0_SA_COO + 3.0.0_SA_CVO); DE render-verifies + CVO served-verifies. MISMATCH -> STOP, do NOT signal safe, flag COO.
</nightly_validation_runbook>
<references><ref type="source">data/black_diamond/scripts/gold/D_00c.portal_leaderboard.py (lines 161-190 canonical loader; 442-518 role_detail; 865/590 tagged; 876-931 split_pct three-case)</ref><ref type="fe">portal/src/pages/AdvisorIntelligence/_shared/AdvisorPublicProfile.tsx (Role Composition ~790-847); _shared/tabs/AdvisorsTab.tsx (getDisplayMetrics ~330-439)</ref></references>
<lane_note>DS owns the D_00c gold-script change (rule 13). DE owns the FE follow-on + verification. GATE: land on the scheduled nightly artifact, never an ad-hoc gold run (NEVER rule).</lane_note>
