<to_id>NFRA_COMPRAIL.TO-6</to_id>
<project>NFRA_COMPRAIL</project>
<title>LD-0207 comp-rail hardening batch (Andrew-approved) -- 3 gates: broad-grep DENY + native-Grep/Glob GATE-on-estate-paths + Rule21<->22 mandatory comp-cite; announce-then-enforce per gate</title>
<assigned_to>1.0.0_SA_CTO (gate mechanism + announce-then-enforce) + 3.0.0_SA_CVO (Gate-3 grounding-field + TO-5 telemetry)</assigned_to>
<issued_by>2.0.0_SA_COO (decompose per MSTR GO 203955Z; LD-0207 Andrew-approved; CTO batch docs/architecture/NFRA_COMPRAIL_HARDENING_BATCH.md)</issued_by>
<issued_date>2026-06-22</issued_date>
<status>complete -- SPRING-CLEAN 2026-08-25: project NFRA_COMPRAIL is complete; this TO was last touched 2026-06-25, predating the project close 2026-07-01. Closed as a record act, not a work verdict. Prior status: active</status>
<!-- GO'd: Andrew approved the batch AS-PROPOSED (MSTR 203955Z). NON-URGENT (a hardening; announce-then-enforce, TO-3/TO-4 precedent). New leg under NFRA_COMPRAIL, not a new project. Different lane from the COT launch (CTO/CVO) -> no contention. -->

<context>
LD-0207 (Andrew-direct, b612199dd): a comp-rail SKIP IS a Rule 22 grounding SLIP (comp-transform/comp-blast ARE the mechanism-grounding tools; Rule 21=lookup, Rule 22=reasoning, one thesis). Anchor incident: CVO raw-Grep'd DistributionTab -> a render over-claim DE caught (the COT geo-display, same-day). Gaps the batch closes: native Grep/Glob nudge-too-soft, broad-repo-grep STAGED-not-denying, Rule21<->22 linkage unenforced.
</context>

<the_3_gates>
1. GATE-1 (CTO -- comp-tool-hud.sh PreToolUse hook): Bash broad repo grep/find/rg STAGED -> DENY. The `# rail-checked: <why>` inline escape STAYS (audited to comp-which-rail.log). (pipe-greps `cmd|grep`, operational, stay free.)
2. GATE-2 (CTO -- same hook): native Grep/Glob tools nudge -> GATE, but ONLY on estate-coupled paths (classify_path) -- generic/non-estate search stays free (don't over-gate). 
3. GATE-3 (CVO -- grounding emission-format; CTO ratifies): comp-transform/comp-blast citation MANDATORY in CVO's grounding: field for COMPONENT/FUNCTION mechanism claims (the DistributionTab-class -- a render/function "X because Y" claim must cite comp-transform/comp-blast, not raw-grep/Read). Extends the existing grounding: fold (e71e9d13e).
</the_3_gates>

<legs>
- LEG-0 (CTO -- PREREQUISITE GATE, LD-0208 fefcae83a): **COMPLETE 2026-06-25 (05235149c + 28e0e9e55).** FIXED comp-which routing: (A) use_cases->entries key, (B) backstop consulted before the grep fallback, (C) curated rules for freshness/validate/pii + comp-platinum/comp-xref + dropped bare "scoped", (D) committed regression guard .tools/comp-which-routing-test.py. Router now reaches ALL 28 routable tools (was ~8); guard PASSES 28/28 end-to-end self-routing + 3/3 audit reproduction. comp-to documented in manifest excluded_not_graph_use_cases (the only untracked tool; manifest-check/surface-check already excluded as enforce-gates). MSTR coverage-probe-corroborated; handed to MSTR for governance verify-and-close. **Gate-1/2 ENFORCE is now UNBLOCKED** (no longer funnels agents toward a router that dead-ends ~28 tools). TO-5 RUN-GREP-vs-ROUTE rate measures the before/after.
- LEG-A (CTO): implement Gate-1 + Gate-2 in comp-tool-hud.sh (the PreToolUse hook); classify_path-scoped for Gate-2; #rail-checked escape preserved for Gate-1. ENFORCE only after LEG-0 (comp-which routes well).
  - **GATE-2 RECONCILED 2026-06-25 (CTO, ground-truth read of comp-tool-hud.sh): SUPERSEDED as a DENY.** The hook records Andrew-direct 2026-06-22 "native Grep/Glob NEVER deny" (the 'native escape is fine' principle, comp-tool-hud.sh:152). Native Grep/Glob already get the advisory class-match nudge (fires for tool=Grep|Glob). So Gate-2's intent (nudge-on-estate-paths) is ALREADY LIVE as advisory; the DENY escalation is PROHIBITED by the later Andrew directive. Gate-2 needs NO further build -- advisory-live + deny-off. Net: LEG-A = **Gate-1 ONLY**.
  - **GATE-1 SCOPE (CTO 2026-06-25):** broad Bash repo-grep (grep/rg/find family) DENY, ESTATE/graph-scoped only (data/*/scripts/{gold,silver,bronze}, portal/src, infra/aws, *.tf, lambda src) per the governing principle "DENY fires IFF a graph backs it" -- a NO-GRAPH search (new project / non-estate / local lib / generic) stays advisory, NEVER denied (AC#5 over-gate guard). Built behind a DEFAULT-OFF marker (org/mcp/comprail-gate1.enforce): absent=advisory (current behavior, zero change); present=enforce. The flip is the announce-then-enforce step (LEG-C, COO-relayed). #rail-checked + /freeform escapes preserved. FP-test = .tools/comprail-gate1-fptest.sh (AC#5).
  - **GATE-1 EMPIRICAL GROUNDING + SCOPE-GOVERNANCE FINDING (CTO 2026-06-25, probed comp-tool-hud.sh classification of representative commands):** the deny surface of a comp_which-scoped Gate-1 is NARROW -- most estate greps already classify into SPECIFIC advisory classes (s3_artifact via /gold|silver/, portal via portal/src/, infra_grep which ALREADY denies), so only the bare `grep -r X data/<firm>/scripts/` greps (no /gold|silver/, no script-id) land in the comp_which catch-all Gate-1 targets. Must stay FREE (verified): pipe-greps (cmd|grep -> ADVISE today, NEVER deny), no-graph paths (newproject/ -> ADVISE), the deck_generation carve-out (-> SILENT). **OPEN SCOPE DECISION for the announce (COO/CVO, NOT a unilateral hook edit -- it materially changes fabric friction):** (a) deny ONLY the narrow comp_which-estate bucket [conservative, minimal new friction], vs (b) ALSO escalate the specific estate classes (s3_artifact/portal data-script greps) to deny [broader, the PRD-S6 "broad repo-grep" intent but more friction]. Default build = (a) conservative behind the flag; the (a)-vs-(b) call goes to COO/CVO at announce-design. NEXT: build (a) + the FP-test decision-table [marker-off=all advisory/silent unchanged; marker-on: data-scripts-comp_which=DENY, pipe-grep/no-graph/deck/single-file/override=FREE], prove green, bring mechanism + the (a)/(b) scope question to COO for the standalone announce.
- LEG-B (CVO): Gate-3 grounding-field extension (mandatory comp-transform/comp-blast cite for component/function mechanism claims) into molecule/seams/verify-channel; CTO ratifies (cross-tool, commits-through-owner per the grounding-doctrine precedent).
- LEG-C (CTO+COO): announce-then-enforce per gate (TO-3/TO-4 precedent -- announce -> grace -> enforce; COO relays the fabric announce).
- LEG-D (CVO TO-5 extension): override-rate telemetry post-enforce for the new gates (repeat override for one intent = a coverage gap -> build the tool). org/mcp/comp-which-rail.log.
</legs>

<acceptance_criteria>
1. Gate-1 (broad-grep DENY) + Gate-2 (native-Grep/Glob GATE-on-classify_path) live in comp-tool-hud.sh; #rail-checked escape + generic-search-free both verified (no over-gating regression).
2. Gate-3 mandatory comp-cite in CVO grounding: for component/function mechanism claims (CTO-ratified).
3. Announce-then-enforce sequenced per gate (announce + grace before enforce); COO relays the announce.
4. TO-5 override-rate telemetry extended to the new gates.
5. No false-deny regression on legitimate operational/pipe-grep/generic-search (the over-gate risk).
RAVC2 to COO + the LD-0207 ledger trail; CVO certifies the rail behaves (no over-gate) post-enforce.
</acceptance_criteria>
