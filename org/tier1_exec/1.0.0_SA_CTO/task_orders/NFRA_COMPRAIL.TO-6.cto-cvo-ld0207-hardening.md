<to_id>NFRA_COMPRAIL.TO-6</to_id>
<project>NFRA_COMPRAIL</project>
<title>LD-0207 comp-rail hardening batch (Andrew-approved) -- 3 gates: broad-grep DENY + native-Grep/Glob GATE-on-estate-paths + Rule21<->22 mandatory comp-cite; announce-then-enforce per gate</title>
<assigned_to>1.0.0_SA_CTO (gate mechanism + announce-then-enforce) + 3.0.0_SA_CVO (Gate-3 grounding-field + TO-5 telemetry)</assigned_to>
<issued_by>2.0.0_SA_COO (decompose per MSTR GO 203955Z; LD-0207 Andrew-approved; CTO batch docs/architecture/NFRA_COMPRAIL_HARDENING_BATCH.md)</issued_by>
<issued_date>2026-06-22</issued_date>
<status>active</status>
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
- LEG-A (CTO): implement Gate-1 + Gate-2 in comp-tool-hud.sh (the PreToolUse hook); classify_path-scoped for Gate-2; #rail-checked escape preserved for Gate-1.
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
