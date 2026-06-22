<to_id>ADVI_NNAATTR.TO-1</to_id>
<project>ADVI_NNAATTR</project>
<title>DS battery — unify per-advisor NNA attribution to ONE all-roles canonical source, REMOVE D_00c over-resolving inference, KEEP 49F House + Unassigned as canonical buckets (F-0/F-1a/F-2/F-4/F-5)</title>
<assigned_to>0.4.0_DS_ClientPlatform</assigned_to>
<issued_by>2.0.0_SA_COO (CVO NNA audit 9543c4392, Andrew-approved + all 4 decisions settled in-session 2026-06-17)</issued_by>
<issued_date>2026-06-17</issued_date>
<status>complete</status>
<!-- 2026-06-22 re-verify (DS): all 5 ACs PASS on SERVED 06-22 artifacts. AC1 cross-route identity Travis QTD/YTD/MAX nna IDENTICAL to the cent (advisor_nna_canonical.json D_00f == leaderboard.json D_00c: $8,900,055.22 / $21,233,843.54 / $214,876,465.97); $4.14M-vs-$6.95M divergence GONE. AC2 49F House+Unassigned is_bucket rows preserved, D_00c reads architect_no_infer (Layer-3 removed not bypassed), C_07 emits it. AC3 all-roles + firm account-once (geo delta 0.0; per-advisor non-additive by design F-1a/invariant-4). AC4 MAX=2021-Q1; nna==inflows-outflows <=$0.01; reconciliation all_pass=true. AC5 D_02 F-5 fallback logging present. RAVC2 -> CVO 134444Z (CC COO/CTO) for #9 fast re-cert -> NNAATTR close. -->

<priority>HIGH — the unblocked critical path. F-0/F-1a are ungated (Andrew decided); they fix a SILENT financial-display defect (same advisor reads $4.14M vs $6.95M by route). Validate on the SERVED artifact, never self-report (Rule: verify against served, not rc=0).</priority>

<context>
SILENT route-dependent per-advisor NNA divergence (CVO audit, /seams-confirmed): D_00f (Distribution, via C_01 acct_dim SCD) parks 34.5%/$35.3M QTD in Unassigned + 49F-House placeholders; D_00c (profile card, via C_07 account_team Layer-3) RESOLVES those placeholders by inferring an architect -> OVER-credits individuals with the house book + transient arrivals. Same advisor, two numbers, no alarm. CTO NON-NEGOTIABLE: unify to ONE canonical per-advisor path so D_00f and D_00c read the SAME individual number.

ANDREW DECISIONS (all 4 baked — no fork remains):
- F-0: per-advisor NNA = ALL ROLES, ONE attribution source + ONE tenure rule, with 49F House + Unassigned KEPT AS THEIR OWN CANONICAL BUCKETS (NOT resolved into individuals). The fix = REMOVE D_00c's C_07 Layer-3 inference (it over-resolves placeholders into individuals). Align D_00c to the canonical's bucket-preservation. Individuals' per-advisor NNA EXCLUDES the house/unassigned buckets. NET: individual numbers come DOWN toward the canonical side; 49F House + Unassigned appear as their own rows. (CVO research: Unassigned = TRANSIENT, purely 2026 arrivals, self-clearing ~1-2 quarters; 49F House = the code-confirmed CANONICAL house book $357.6M continuous -> keep as "49F House", never attribute to individuals.)
</context>

<deliverable>
F-0 + F-1a (CORE, ungated — do FIRST):
- Unify per-advisor attribution onto ONE canonical all-roles source + ONE tenure rule. REMOVE D_00c's C_07 account_team Layer-3 placeholder-resolution inference; align D_00c to the canonical bucket-preservation (the same source/rule D_00f's canonical uses). Decide the ONE tenure rule (per-day vs snapshot) ONCE + apply identically both routes.
- Emit all-roles per-advisor in advisor_nna_canonical with 49F House + Unassigned as their OWN bucket rows (not folded into individuals); keep the FIRM total additive (account-once).
F-2 (decision-independent): MAX = 2021-Q1 everywhere (D_00f _build_windows + D_00c).
F-4 (decided): headline firm NNA = the canonical ADDITIVE account-once number (MAX=2021-Q1). Retire D_00's cum-diff computation + the dashboard.json zeroing fallback; add NNA to dashboard.json as additive-account-once.
F-5 (decision-independent): D_02 fallback logging (make the fallback path observable, not silent).
</deliverable>

<acceptance_criteria>
AC1 (CROSS-ROUTE IDENTITY — the core fix): D_00f and D_00c read the SAME per-advisor INDIVIDUAL number for the same advisor (the Travis $4.14M-vs-$6.95M silent divergence GONE). Prove on >=2 advisors incl. Travis, on the SERVED artifact post-nightly.
AC2 (BUCKETS PRESERVED): 49F House + Unassigned appear as their OWN canonical bucket rows in advisor_nna_canonical; individuals' per-advisor numbers EXCLUDE them (no individual carries the $357.6M house book or the transient Unassigned). D_00c no longer runs the Layer-3 placeholder-resolution inference (grep-confirm the inference path is removed, not bypassed).
AC3 (ALL-ROLES + ADDITIVE FIRM): per-advisor = all roles; firm total = additive account-once (sum of individuals + buckets = firm, no double-count). 
AC4 (WINDOWS + HEADLINE): MAX=2021-Q1 everywhere; headline firm NNA = additive-account-once (cum-diff + dashboard.json zeroing retired); within-surface nna==inflows-outflows holds.
AC5 (D_02 logging): the D_02 fallback path logs when it fires (observable).
VERIFY on the SERVED advisor_nna_canonical artifact post the scheduled nightly (NEVER an ad-hoc gold run — validate on the nightly's artifacts per the compute-discipline rule). CVO post-fix re-verification (cross-route identity + attribution-completeness w/ buckets-as-canonical + headline reconciliation) is the close-gate.
</acceptance_criteria>

<sequencing>
F-0/F-1a FIRST (the core, ungated). F-2/F-4/F-5 fold in (decision-independent / decided). The DE/RD leg (TO-2: F-1b/F-1c repoint Distribution/Continuous/profile to the all-roles number + drop the ADVI_INFMVP.F5 architect-only override; F-3 Inflection fee-split) is GATED on F-1a landing (the all-roles number must exist first) — I author + GO TO-2 when F-1a lands. Gate-of-record = the NFRA_GCONTR NNA value-limb (CVO updating it to: 49F House recognized-canonical, Unassigned bounded-transient) — your emit must satisfy it (advisory v1 today, it FLAGS the current divergence by design).
</sequencing>

<deploy_discipline>
DS owns the full commit->QA-deploy cycle for the gold scripts (CLAUDE.md Rule 13); ds-commit-gate per .py; from __future__ import annotations (Rule 15); silver untouched (Rule 17 — this is gold-tier attribution logic). comp-pipescript io [script] before editing (column gaps + portal consumers); comp-validate on the served artifact. RAVC2 to COO (CC CTO + CVO) with the served-artifact cross-route-identity proof + the bucket rows + the AC table.
</deploy_discipline>
