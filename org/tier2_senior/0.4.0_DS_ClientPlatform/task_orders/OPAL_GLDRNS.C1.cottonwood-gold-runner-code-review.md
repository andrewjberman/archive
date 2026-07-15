<task_order>
<to_id>OPAL_GLDRNS.C1</to_id>
<title>Cottonwood gold runner: /gold-runner-code-review end-to-end — efficacy + pattern</title>
<issued_by>1.0.0_SA_CTO</issued_by>
<issued_to>0.4.0_DS_ClientPlatform~C</issued_to>
<status>staged</status>
<project>OPAL_GLDRNS (feeds the OPAL_RUNNERS casebook — cot ships on the group contracts per PRD §5)</project>
<provenance>Andrew-direct directive 4, VERBATIM: "In the case of DS~C they need to essentially
/code-review their way through the Cottonwood gold runner and identify efficacy and pattern."
Lane Andrew-spawned.</provenance>

<scope>READ-ONLY review. The cot gold runner estate (data/cot/scripts/gold/ — A/B/C groups + the 7
D publishers) via the /gold-runner-code-review framework (the repeatable per-script fan-out built
from the INF ADHC_GLDINC pass): per script — type issues / incremental-vs-forced-full-recompute /
unguarded reads / merge-dtype mismatches / silent served-number corruption — PLUS the two
directive-named lenses: EFFICACY (does the script's computation actually produce a correct,
consumed, decision-useful output — consumer-anchored per surface, unconsumed = retirement
candidate) and PATTERN (which group-contract patterns cot already matches vs deviates from; the
deviation list = the casebook's cot variance section; the known open variance = model-marking, per
PRD §5, carried explicitly). cot is a COMPLETELY SEPARATE firm pipeline from bd (Rule 13/IAM law):
this review READS cot only — never mirror/sync anything bd<->cot; pattern comparisons cite, never
copy. Known standing item to fold: the cot leaderboard 1Y 363-day window (SERVED; Andrew-parked)
gets a named finding entry, not a fix — a cot gold push AUTO-DEPLOYS, so NO code lands from this
TO at all: findings route to CTO; fixes are a SEPARATE gated wave.</scope>
<deliverable>Per-script review reports (the framework's colocated-folder form) + the rollup:
efficacy verdicts w/ consumer anchors, the pattern/variance matrix vs the group contracts, a
ranked fix backlog (severity + effort) for CTO gating, and the casebook cot-variance entry draft.</deliverable>
<compiler_tools_mandate>comp-pipescript io per script reviewed; comp-blast before proposing any
shared-surface fix; the framework's own verification steps. NO commits into data/cot/scripts/
(auto-deploy trap) — deliverables + logs only.</compiler_tools_mandate>
<cross_domain_coordination>~A (pattern matrix cross-reads the 49F casebook); CTO (all fix gating);
COO (registry). NONE with bd surfaces.</cross_domain_coordination>
<acceptance_criteria>100% of cot gold scripts reviewed (denominator printed); every script carries
an efficacy verdict + pattern classification; zero code commits into the cot tree; the ranked
backlog exists with severity/effort per item; the 363-day-window item carried as a named finding.</acceptance_criteria>
<session_log>Required, Compiler Tools section mandatory.</session_log>
</task_order>
