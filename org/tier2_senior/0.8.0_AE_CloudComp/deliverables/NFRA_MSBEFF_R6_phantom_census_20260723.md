# NFRA_MSBEFF.R6 — phantom-name census (derived live) + the honest scope finding

**Author:** 0.8.0_AE_CloudComp~B · **Date:** 2026-07-23 · **Verifies:** 3.0.0_SA_CVO~Z · **Reports:** 1.0.0_SA_CTO~Z
**Method:** derive the LIVE known-name set from the registration universe, scan the reference surfaces,
diff, PRINT the denominator (TO: "the Phase-0 list is a STARTING POINT, not the census").

## Denominators (derived, not Phase-0)

- **KNOWN-LIVE comp-* names: 84** = tools_index 64 ∪ excluded 15 ∪ entries-tools 69 ∪ coverage-map 85 ∪
  on-disk-tracked comp-* 82 (union, dedup).
- **Reference surfaces scanned:** `docs/**` + `.tools/hooks/comp-tool-hud.sh` + `**/prompt.md` +
  `.claude/skills/**` + `org/compiler-tools-log.md`.
- Token = `comp-[a-z0-9]+(-[a-z0-9]+)*`, filtered by a **prefix-of-a-live-tool** rule (kills the
  English-hyphenation class: `comp-blast-confirmed` = "comp-blast confirmed"; `comp-iam-gaps` = the real
  `comp-iam gaps` subcommand) + date-fragment + concept-token exclusions.

## The split that matters (operational vs design)

| Surface class | distinct phantom tokens | total refs | disposition |
|---|---|---|---|
| **Operational routing** (HUD, prompts, skills, CLAUDE.md/XXX.md) | 9 | 62 | **ALL resolve to real things — ZERO dead-tool routing directives** |
| **Design docs** (`docs/architecture`, `docs/briefs`, `docs/references`) | 65 | 334 | never-built **PROPOSALS** + historical names — out of gate scope |

### Every "operational-surface phantom" grounded (none is a retired tool misrouting an agent)

| token | what it actually is |
|---|---|
| `comp-tools-directive` (34) | a real FILE: `org/ref/prompts/comp-tools-directive.md` |
| `comp-loop` (13) | a real **skill** (`.claude/skills/comp-loop/`), self-referenced in its own SKILL.md |
| `comp-tool-hud` (6) | a real FILE: `.tools/hooks/comp-tool-hud.sh` (the HUD itself) |
| `comp-answerable`, `comp-call` (5) | **concepts** in HUD prose ("comp-answerable searches", "the canonical comp-call") — not tools |
| `comp-rail` (1) | the COMPRAIL **concept** |
| `comp-tracker` (1) | the real underscore engine `comp_tracker.py` (the doc names the hyphen/underscore trap) |
| `comp-learns-backlog` (1) | a real FILE: `org/modules/graph/comp-learns-backlog.md` (drive reads it) |
| `comp-ferry` (1) | the ferry **mechanism** concept (LD-0119), in my own persona prompt |

**The HUD routes to NO dead tool.** Its `msg=` routing directives cite only live tools (comp-which, comp-iam, …).

### The design-doc mass is PROPOSALS, not retirements

Top design-doc "phantoms": `comp-learns-run`(35) `comp-learns`(30) `comp-debt`(27) `comp-lint`(20)
`comp-events`(17) `comp-dev-loop`(17) `comp-preflight`(13) `comp-ladder`(10) `comp-ms*`(family) `comp-aws-{ec2,s3,dynamodb,cloudfront,eventbridge}` … — tools **described in PRDs/briefs that were never built**
(the comp-learns orchestrator family shipped only as comp-learns-score/comp-learns-status; the comp-aws
sub-tools were a single comprehensive-cloud-compiler proposal). **A PRD naming a proposed tool is a design
record, not a misroute.** No clean `retired-tool → live-successor` pair exists in the estate.

## The finding (honest, negative-test-integrity)

The "~46 phantoms" (Phase-0, measured over the historical `compiler-tools-log`) are **historical-log names +
design-doc PROPOSALS + files/concepts/skills** — **NOT retired tools misrouting agents.** There is **no live
operational misroute-to-a-dead-tool problem** in the estate today.

Therefore AC-3 as literally written ("every hit repointed or deleted-with-citation") is **not the right
action**, for two doctrine reasons ~Z owns:
1. **TRIGGER_LAYER clause 2** — "the lint is on the STRUCTURED FIELD, never a text-match over prose
   (matchers that fire on mentions are the wrong mechanism)." A bulk prose-scrub of 334 design-doc refs is
   exactly that.
2. **TRIGGER_LAYER boundary** — "does not license bulk-converting historical notes… manufactures a hundred
   unowned items." Rewriting PRDs to delete proposed-tool names vandalizes legitimate design records.

## What R6 shipped instead (the durable value)

- **retired_aliases** — the 3rd coordinated name-authority section in `graph-call-manifest.yaml` (dead names,
  successor|null, why). SEED IS MINIMAL (2, defensible): `comp-learns-run`, `comp-coverage-view`.
- **retired-alias completeness invariant** (`_retired_alias_invariant`, wired into the family @23db0d32c):
  guardrail A (sections disjoint) + guardrail B (successors validate) + a **routing-surface check keyed on
  the CLOSED retired set** — a committed HUD/prompt/skill citing a *declared-retired* name BLOCKS. This is
  "the registration invariant pointed at the routing surface," structured (not a prose scan), so it **cannot
  storm** on the 334 proposals. A **forward guard**: when a real tool is retired, declare it here and no
  routing surface may cite it.
- Mutant-proven: guardrail-A (live tool declared retired → BLOCK), guardrail-B (dangling successor → BLOCK),
  routing-surface (declared-retired name in HUD → BLOCK; live name → PASS) — 6 unit paths + a real-CLI block
  (which fired the routing check against the **real** HUD, since comp-which is genuinely cited there).

**Recommendation to ~Z:** accept the structured forward-guard as the R6-D deliverable; do NOT bulk-edit
design docs; grow retired_aliases at touch-time as real retirements occur. Confirm or rule otherwise.
