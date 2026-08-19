# TO D6_ANALYST.TO-CDBFG-SITEZ — Opal Analyst v0 bindings + GraphQL access layer (SITEZ; multi-workstream)

<task_order id="D6_ANALYST.TO-CDBFG-SITEZ" project="D6_OPAL_ANALYST">
<issued_to>site Z, seats assigned by 0.0.0_AB_MSTR~Z (multi-workstream -- see the per-row table)</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-19T20:05Z</issued>
<dated>HELD for pacing -- ferries on MSTR's signal that a seat is free, AFTER D9</dated>
<status>pending -- ferried + seats assigned 2026-08-19T20:06Z by 0.0.0_AB_MSTR~Z per the TO's per-row authority: build/author rows (TO-B/C/E/F/G-scaffold + TO-D build) -> 0.5.0_AE_OpalETL~Z (existing session, NO spawn -- the staged-note's 7-vs-6 census is superseded: D2 came off site Z and D6 rides existing seats, census 6/6); TO-D duty + runtime-exerciser -> 0.0.3_BG_BBGTerminal (G1 fence respected by construction). TO-A stays laptop per CTO ruling.</status>
<priority>P1-program</priority>
<authority>D6_OPAL_ANALYST_GRAPHQL_PRD.md §6 + the 2026-08-19 ~18:57Z ADDENDUM, at dispatch vintage @030b55b295 (CVO verdict @7ea13aa4ed absorbed). Placement: SITEZ, Andrew-RATIFIED ~19:3xZ, CTO FINAL 193804Z.</authority>
</task_order>

## KICKOFF TRIPLE (explicit, never implicit)
- **prd:** `docs/architecture/D6_OPAL_ANALYST_GRAPHQL_PRD.md` (body v1.0 + the ~18:57Z addendum)
- **workstream:** TO-B, TO-C, TO-D, TO-E(author-half), TO-F, TO-G — **NOT TO-A** (see the placement note)
- **head_version:** `@030b55b295`

## ROW TABLE — placement, gate, and what each row is
| Row | What | Gate | Placement note |
|---|---|---|---|
| TO-B | W5 index build (per R8 preconditions) | the certification state it keys off, **per-unit, not all-16** | sitez |
| TO-C | SharePoint binding (§4.3) | TO-B (the index is where the registry mounts) | sitez — the W7 registry exists; the binding is absent |
| TO-D | BBG standing read (§4.4) off the W8 map | TO-B | **SITEZ-ONLY** — blpapi is box-resident and the quota protocol lives with the box |
| TO-E | GraphQL plumbing (§4.5) | TO-B | **AUTHOR at sitez; the EC2/TF APPLY legs route through a laptop lane** as mechanical applies of sitez-authored config (CTO's envelope law, set for D8 and applied here) |
| TO-F | W6 guardrails review | TO-C/D/E landed — **LAST** | sitez authors; CTO certifies |
| TO-G | entity-resolution service | **D3's TO-D3.1 residual ENUM** | sitez; see the gate note below |

## ⛔ ONE ROW I DID NOT MOVE, AND WHY — TO-A STAYS LAPTOP (flagged to CTO, not held)
TO-A (certifications residual: W4b close + W4c-1..4) has its **authors/certifier seats and an
ESTABLISHED SoD CHAIN on the laptop fabric.** Whole-item sitez placement would relocate a
separation-of-duties chain mid-flight, and an SoD chain that silently changes hands is the kind of
thing that reads fine and is broken. **I have left TO-A at laptop and flagged the single row to CTO
rather than either moving it silently or holding the other six rows on the question.** If CTO rules
it moves, it moves — nothing here is blocked on that.

## TO-G's GATE IS THE LOAD-BEARING ONE
**TO-G gates on D3's TO-D3.1 residual ENUM specifically — not on all of D3 — and TO-G's
disambiguation classes are DRAWN FROM that enum.** One residual vocabulary for one identity plane.
CTO's ruled reason: a resolver built before the enum lands assigns confidence over a universe whose
residual is unclassified, **making "unresolvable" and "resolvable-but-in-the-residual"
indistinguishable.** D3's TO-D3.1 is cut, UNGATED, and startable now on the laptop fabric — so this
is a genuine cross-fabric sequencing edge. **Do not start TO-G's confidence model before the enum
lands; the service scaffold is fine.**

## THE RESOLVER FLOOR — A RULED EXCLUSION TO-B AND TO-F BOTH CARRY
**The W5 index / GraphQL resolver catalog does NOT include the ticket/DDB surface** unless and until
the ticket-API authorization design (D7 §7.3, standing at Andrew since 08-12) lands. This is a CTO
ruling on a CVO cross-package find, and its purpose is structural: it makes **D7's internal-only
deferral premise DURABLE BY CONSTRUCTION rather than incidental.** The partner-facing query layer
cannot become a path to a surface that stamps caller identity without checking it — and **a single
correct resolver check is never the only thing you want above an unchecked surface.**
**TO-B and TO-F each carry this as an ASSERTION in their acceptance.**

## v0 PHASING — ANDREW-QUALIFIED, AND IT BOUNDS TO-E
v0 = the GraphQL **TOOLING/YAML layer over the JSON/operational surfaces** the BBG agent already
plugs into (the W5-index binding). **The PARQUET-RESOLVER PLANE IS A DISTANT SECOND**: gated on the
client parquet structuring completing (POST the full ADVI refactor), and **INTERNAL-FIRST BY LAW** —
built and tested for our own fabric before any BG-agent exposure. **TO-E's v0 resolvers bind
operational surfaces ONLY; no parquet resolver ships in v0.**

Agent surface: the Analyst consumes a constrained **BUSINESS-TOOL surface** (the brief's five tools)
that compiles to GraphQL internally — **not raw GraphQL** ("reducing hallucinated fields").

Guardrails bind **as spec, not advice**: server-side tenant authz on EVERY resolver ("never rely on
the model to scope access correctly"), depth/complexity/row/time/scan limits, audit logging,
read-only default.

## Acceptance criteria (per row, plus the package-level ones)
- **D6-1 EACH ROW'S OWN PRD ACCEPTANCE MET** and reported per row, not as a package aggregate.
- **D6-2 THE RESOLVER-FLOOR EXCLUSION ASSERTED** in TO-B and TO-F deliverables.
- **D6-3 TO-E SHIPS NO PARQUET RESOLVER** in v0 — assert the boundary, do not merely observe it.
- **D6-4 TO-G's CONFIDENCE MODEL CITES THE D3.1 ENUM** it was drawn from, by path + vintage.
- **D6-5 ANY EC2/TF APPLY IS A LAPTOP-LANE MECHANICAL APPLY** of sitez-authored config; sitez does
  not apply.
- **D6-6 proof instances VALID rc=0 positional per row.** MEASURED/RULED-class run rows only;
  INFERRED-class expected values are mechanically ineligible.

<proof_of_spec>
  <expected_criteria>D6-1,D6-2,D6-3,D6-4,D6-5,D6-6</expected_criteria>
  <instance_path>(sitez trunk) deliverables/D6_ANALYST.TO-CDBFG-SITEZ_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

## Do not
- No alert/monitor/notification machinery (standing moratorium).
- Do not widen an identity allowlist or add a resolver over the ticket surface (see the floor).
- §7-Q2 (whether schema-live belongs inside v0) is a pure SCOPE CHOICE at Andrew now that U1 is
  discharged — it does not gate these rows.

## Reporting
COO via the MSTR ferry, per row. Surprise channel: one banked line. Session log per seat with a
Compiler Tools section.

---
## ⚖ v0 SCOPE RULED — 2026-08-19 ~20:12Z (Andrew; @1e0ec3b079 + @3c8c3f1035)
**v0 STAYS PLUMBING-ONLY. THE LIVE GraphQL SCHEMA IS v1.1.** §7-Q2 is CLOSED.
This is now backed by a fresh sovereign word, not only the earlier phasing note — so **TO-E's
"no parquet resolver in v0" boundary (acceptance D6-3) is ruled, not merely proposed.** The v0 DONE
bar does not re-time.
