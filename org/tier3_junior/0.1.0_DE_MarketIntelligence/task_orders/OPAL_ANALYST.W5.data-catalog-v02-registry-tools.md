# OPAL_ANALYST.W5 — DATA_CATALOG v0.2: the registry rigged properly + tools with tags/fuzzy match

<task_order>
<id>OPAL_ANALYST.W5</id>
<issued_by>1.0.0_SA_CTO~Z</issued_by>
<issued_to>0.1.0_DE_MarketIntelligence~Z</issued_to>
<date>2026-08-19</date>
<status>superseded</status>
<superseded_by>D6_ANALYST.TO-CDBFG-SITEZ row TO-B — the D6 root-gate index build IS this artifact, executing at 0.5.0_AE_OpalETL~Z (the PRD wave-table's ORIGINAL W5 owner)</superseded_by>
<priority>P1</priority>
<!-- SUPERSEDED 2026-08-19 ~2015Z BY THE ISSUER (TO-status law: superseded = the need is met
     another way, named). Reconciliation: MSTR~Z 201242Z as D6 per-row seat holder, collision
     surfaced by 0.5.0_AE_OpalETL~Z at 201138Z PRE-BYTES (no index artifact existed). Grounds
     accepted: this TO's re-route was CAPACITY-grounded and the premise died — D7 TO-A closed
     1931Z; capacity adjudication is MSTR~Z's. No METHOD ground for DE~Z exists (the wave table's
     original owner WAS 0.5.0~Z; separation-of-duties sits at CVO~Z certification, not at the
     lift). Zero cost: no GO ever fired, no spawn ever happened, the seat stayed dark.
     BINDING NOTE FOR THE D6 TO-B EXECUTOR: the SPEC RIDES THE ARTIFACT, NOT THE TO SHELL.
     Every requirement and criterion below (the s10.1 preconditions a-d, the merged-definition
     ruling, F4 factor-tilts correction, the three approved widenings, the query-to-route battery
     with denominator, firm-as-first-class-key, the loud-refusal negative control) binds the v0.2
     index build wherever it executes — they are PRD s9.6/s10.1/s9.11 law, quoted here for
     convenience, not created here.
     ORIGINAL STAGING TERMS (for the record): spawn-on-GO to a dark DE~Z seat, GO gated on the
     08-20 07:00 WDAC acceptance + census sequencing; grounded on COO~Z census 193218Z + 193325Z. -->

<references>
  <ref type="prd">docs/architecture/OPAL_ANALYST_PRD.md — §9.6 (W5 spec) · §10.1 (Part-1 amendment: preconditions a–d) · §8.2 (EXTEND ruling — never a second registry) · §9.3 (semantics delegation to CVO~Z) · §10.8 + §10.8.1 (firm isolation, sovereign-backed; firm from PREFIX, never bucket name) · §9.11 (BG fold: F2 urgency, F4 named correction) · §9.8.1-A (consumable = `rectangle.final.certified.json`, only that name)</ref>
  <ref type="required-reading">Consolidated lift-constraints file @f28e15d4b5 (CVO~Z) — ten rulings the certifications produced. READ BEFORE WRITING; a constraint nobody knows about looks exactly like an absence of constraints. Plus M-15 (§9.6): verify endpoint-completeness per relation before consuming it — a relation can rest its conclusion on an entity it omits from `endpoints`.</ref>
  <ref type="context">FRESH-SPAWN CONTEXT (you will load with no session memory): you executed W4a + W4c-1 + W4c-3 under this program — your own runs are your prior art. Site-Z bounds: shared checkout, commit your OWN LANE, NEVER push (MSTR~Z integrates :55–:00); scratchpad is the only safe harbour for uncommitted work; cma env is WDAC law, pip-owned pins (census: MSTRZ_WDAC_OPTIONC_EXPOSURE_CENSUS_20260819.md); zero crons at launch; /watcher once at load.</ref>
</references>

<scope>
`refs/DATA_CATALOG.yaml` v0.1 → v0.2 — **EXTEND in place, never a second registry** (§8.2; a
parallel registry is the standing-comparator class). The catalog is the program's LANDING SURFACE:
every certified unit's atom_decomp output lifts into it, and the live concierge answers off it —
today off v0.1's 12 channels, which is the F2 urgency this TO discharges.

v0.2 grammar (per §8.2 + §9.6, unchanged): `tool:` per channel · `census_ref:` per path ·
`vintage_field:` at ARTIFACT grain (dotted path) · `vintage_grain:` (`date|month|year`) ·
`semantics:` per field-group (per §9.3) · tags + fuzzy match made explicit and testable ·
vintage field MULTI-VALUED as a property, never an enum of counted variants (§10.1 L-4) ·
**firm as a first-class key** (§10.8).
</scope>

<requirements>
  <requirement id="1">**PRECONDITION (a), §10.1 — per-key expansion pass FIRST.** Andrew's binding sequencing: locations *"covered and validated first and foremost"*, only then the index. Every family entity expands to its member keys (measured gap: `sscn.02` = 6 keys, `news.01` = 360 — an artifact-keyed catalog misses 366 of them), each member key validated reachable by an EXERCISED read, with the denominator printed (N keys of M families).</requirement>
  <requirement id="2">**PRECONDITION (b), §10.1 — fix ONE definition of "merged" BEFORE leaning on any semantics count** (100-in-rectangle vs 168-sidecar and 128 vs 144 are different instruments on adjacent axes — settle the definition WITH CVO~Z, then re-derive both counts under it). Then: the lift reads `rectangle.final.certified.json` ONLY and **REFUSES LOUDLY on a unit that has none**. 10 units carry unmerged `SEMANTICS_CVO_PLANE_BC*.json` sidecars — existence of certified.json is NOT evidence its semantics merged.</requirement>
  <requirement id="3">**PRECONDITION (c), §10.1 — every lift keys off `certification.json`'s VERDICT, never file presence.** `security-scanner/0158Z` is VOID with its rectangle still carrying the planted cell; `cma/1729Z` is superseded beside canonical `1801Z`. Marking the void/superseded runs is authorized as part of this TO rather than left to whoever globs first.</requirement>
  <requirement id="4">**PRECONDITION (d), §10.1 — the lift transliterates non-ASCII ON READ** (emoji → the estate's `WARN:`/`BLOCKED:`/`OK:` convention; em/en dashes → ASCII). The 156 certified cells are NOT edited — the prohibition applies where the bytes execute, not where they were authored.</requirement>
  <requirement id="5">**F4 NAMED CORRECTION (§9.11):** the catalog's `factor-tilts/{tier1|tier2}.json` is drift against the bucket's actual `tier1-snapshot.json` / `tier2-spreads.json` / `tier3-timeseries.json` (BG grounding: rc=1 on a COMPLETE 3-key walk, denominator 3/3). v0.2 carries the TRUE keys, each validated by read.</requirement>
  <requirement id="6">**The three approved-but-unlanded widenings ride v0.2** (Andrew: *"Yes approved rec"* @d2f2e01d9): `json/capital-markets/` into the `portal_lookup` channel map + `PORTAL_RETRIEVAL` + `BUCKET_ALLOWLIST`. No OTHER widening — catalog widening stays Andrew-only, version bumps carry his verbatim.</requirement>
  <requirement id="7">**Tags/fuzzy deliverable: a query→route test battery WITH ITS DENOMINATOR** — N asks in, N routes out, misroutes named, NEGATIVE cases included. A matcher with no negative cases has never been tested.</requirement>
  <requirement id="8">**Grain caveat (§9.6):** `/cma` + `/positioning` consumer counts were accepted at ACCESSOR grain; the true grain is per CALL SITE (K8). Re-derive per call site before any decommission is proposed from those counts — a count at the wrong grain proposing a decommission is the deletion-warrant class.</requirement>
  <requirement id="9">**Units without certification at lift time (W4b if still in flight): the catalog row REFUSES LOUDLY per requirement 2.** W4b lands late into the same grammar. Do NOT wait on it; do NOT hand-copy its uncertified content.</requirement>
</requirements>

<compiler_tools_mandate>
  <before_write>`comp-which` routing for every search; `comp-estate` for channel/serving topology — and per CLAUDE.md Rule 21's own caveat, treat its topology/served-name claims as a PRIOR UNDER TEST: ground every served key on the live primitive (an exercised read), which requirement 1 mandates anyway. Read @f28e15d4b5 BEFORE writing.</before_write>
  <before_commit>`.tools/commit-gate.sh` on any `.py`; a YAML parse check on `DATA_CATALOG.yaml` (python -c yaml.safe_load, rc captured as the next statement).</before_commit>
  <after_commit>python .tools/proof-of-spec-check.py &lt;instance&gt;.json C1,C2,C3,C4,C5,C6,C7,C8,C9   # POSITIONAL argv[2]; CHECK THE RC</after_commit>
</compiler_tools_mandate>

<cross_domain_coordination>
- **3.0.0_SA_CVO~Z** — semantics authority (§9.3) + certification; the "merged" definition (req 2) is agreed WITH CVO~Z before the lift consumes either count.
- **0.5.0_AE_OpalETL~Z** — W4b author; NO shared file edits; their semantics stage into v0.2 at their close via the same grammar.
- **1.0.0_SA_CTO~Z** — issuer, PRD owner, surprise channel (one line, no action, keep working).
- **2.0.0_SA_COO~Z** — fabric census + RAVC validation of the deliverable.
- Lane commits only; no push (MSTR~Z integrates).
</cross_domain_coordination>

<acceptance_criteria>
  <criterion id="C1">Per-key expansion pass complete: every family entity expanded, every member key exercised by read, denominator printed (N keys of M families; failures named, not dropped).</criterion>
  <criterion id="C2">"Merged" defined in ONE ruling co-signed by CVO~Z; both prior counts re-derived under it and recorded.</criterion>
  <criterion id="C3">Lift consumes `rectangle.final.certified.json` only, keyed on `certification.json` verdict; void/superseded runs marked; the loud-refusal exercised on at least one uncertified unit as a NEGATIVE CONTROL.</criterion>
  <criterion id="C4">`DATA_CATALOG.yaml` at `version: 0.2`, parses clean, EXTENDED in place — the diff shows no second registry file anywhere.</criterion>
  <criterion id="C5">F4 factor-tilts keys corrected + validated by read; the three approved widenings landed; zero other widenings.</criterion>
  <criterion id="C6">Query→route battery committed with denominator, negative cases included, misroutes named.</criterion>
  <criterion id="C7">Non-ASCII transliteration exercised on real cells (emoji + dash cases shown); certified rectangles diff-clean (untouched).</criterion>
  <criterion id="C8">Firm key present per row per §10.8; firm derived from prefix, never from bucket name (§10.8.1).</criterion>
  <criterion id="C9">Proof-of-spec instance validator-clean BEFORE any status flip; session log with Compiler Tools section.</criterion>
</acceptance_criteria>

<proof_of_spec>
  <expected_criteria>C1,C2,C3,C4,C5,C6,C7,C8,C9</expected_criteria>
  <instance_path>org/tier3_junior/0.1.0_DE_MarketIntelligence/deliverables/OPAL_ANALYST.W5_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

<deliverables>
  <deliverable type="commit">`refs/DATA_CATALOG.yaml` v0.2 (lane commit)</deliverable>
  <deliverable type="document">The "merged" definition ruling record (with CVO~Z co-sign)</deliverable>
  <deliverable type="document">Query→route battery + results with denominator</deliverable>
  <deliverable type="document">Proof-of-spec, validator-clean before any flip; session log</deliverable>
</deliverables>

<do_not>
  <rule>No second registry · no edits to certified rectangles · no allowlist widening on own authority · no monitors/alerts (moratorium) · no push · no waiting on W4b · never quote a family total as member coverage (the §10.1(a) denominator rule) · no decommission proposed from an accessor-grain count.</rule>
</do_not>
</task_order>
