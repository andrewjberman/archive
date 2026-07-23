# NFRA_TOOLBHVR.ROUTE — Phase 1: the derived gap, and the question-class routing design

**Author:** 0.8.0_AE_CloudComp~B · **Date:** 2026-07-23 · **Gates:** 1.0.0_SA_CTO~Z · **Verifies:** 3.0.0_SA_CVO~Z
**Status:** Phase-1 COMPLETE (AC-1). Routing change HELD pending (a) ~Z's AC-2 ruling, (b) ~D's per-class
certification table. Nothing shipped to the rail yet — deliberately.

## AC-1 — the gap, derived with a denominator

Source: `org/mcp/comp-which-rail.log`, **18,014 events**.

| event | count |
|---|---|
| ROUTE-POSTERIOR (routed) | 12,147 |
| RUN-GREP / RUN-GLOB (on-rails primitives) | 2,321 / 708 |
| ROUTE | 1,487 |
| DENY (gate blocked) | 601 |
| RUN-OVERRIDE | 188 |
| `rail-checked` overrides | 67 |

Gate classes: `infra_grep` 320 · `aws_freshness` 268 · `aws_iam_inspect` 114 · `comp_which` 40 ·
`aws_deploy_verify` 24 · `aws_route` 17 · `aws_dynamodb` 6.

### THE GAP (named): the rail classifies by COMMAND SHAPE, never by QUESTION TYPE

The HUD's full class taxonomy is `aws_deploy_verify, aws_dynamodb, aws_freshness, aws_iam_inspect,
aws_route, comp_which, iam_role, infra_grep, lambda, object_heat, portal, react_query, s, script_id`.
**None of them is a path / lineage / serving class.** There is no way for the rail to express
"this agent is asking what serves this key."

Consequence, mechanically (`comp-tool-hud.sh:113` then `:131`): a served-key path question whose key
carries a `json/` prefix escapes the generic-listing exit at `:113` (because it HAS a matching prefix),
then FIRST-MATCH-WINS into `class=aws_freshness` at `:131` → nudged to `comp-freshness`
(EXISTS/FRESH/SCALED/NOT-FROZEN). **That answers a different question.** The rail fires, the answer
does not fit the intent, and the agent proceeds to hand-grep anyway.

So this class did not slip because it was *uncaught*. It slipped because the intent was **MIS-TYPED** —
and a wrong-tool nudge is worse than silence: it spends the rail's credibility and trains bypass (BL-1).

**Measured population:** 268 `aws_freshness` calls, **18** path/serve/resolve-shaped. The 67
`rail-checked` overrides are the measured "the nudge did not fit, going anyway" set. The logged queries
are literally the incident shape with an override attached:
`aws s3 ls s3://opal-data-portal-v2/json/mdpf/cottonwood/ # rail-checked: same content-enum`.

## The finding that inverts the TO's premise (~D, positive-control-proven)

`comp-routes trace <url>` falls through to the catch-all CloudFront behavior `/*` and returns
`Origin: S3-opalinvest-portal` for **any** path. ~D's positive control: a path WITH a known rewrite
rule returns **byte-identical** output to the mdpf path. It is **undiscriminating** for this class.

With `pipescript` on a 38-day snapshot (LOUD-VINTAGE banner @dcf153915 — mitigated, not cured) and
`comp-kuzu` canonical holding **no node for the live mdpf key** (post-build @2026-07-23T14:52:37Z):

> **There is currently NO tool that resolves a concrete URL to its S3 key for the static-rewrite class.**

My TO's scope-A instructs routing this class to "the definitive tool." For the trigger incident's own
question class that tool does not exist. Routing it anyway would replace a hand-grep that KNEW it was
uncertain with a tool answer that READS AUTHORITATIVE and cannot discriminate — strictly worse than the
grep, and the same silent-wrong class as the stale key with better manners. **Surfaced to ~Z for an
AC-2 ruling rather than reinterpreted here.**

**Cheap fix exists (~D's, routed to ~Z, not mine to build):** `comp-routes rewrites` ALREADY lists the
correct table including `/api/general/json/ -> json/` (exactly the MDPF hop); `trace` simply never
consults it. Wiring trace to the table it already has is a small fix, not a capability build. This
design flips the class from no-coverage to routable the moment that lands.

## AC-3 — the design: certify by QUESTION CLASS, not by tool

Adopted from ~D verbatim, because it is the load-bearing correction: **the same tool is current for one
question and stale for another** (pipescript is reasonable for thread topology and WRONG for served
keys). A tool-level allowlist routes agents into the stale HALF of a "trustworthy" tool.

So the routing table is `(question-class → tool)`, certified per class:

| question class | route to | certification (source: ~D 211545Z) |
|---|---|---|
| SOURCE structure (call / import / dataflow) | `comp-trace` `comp-build` `comp-xref` `comp-blast` | TRUSTWORTHY — source-scanned, HEAD-pinned, rebuilds on source-SHA drift |
| CF/edge CONFIG listing (behaviors, origins, rewrites, api-routes) | `comp-routes behaviors|origins|rewrites|api-routes` | TRUSTWORTHY — config-derived |
| RESOURCE / estate topology | `comp-kuzu` canonical | TRUSTWORTHY **as of build ts**; post-build changes UNCOVERED — read the provenance header |
| FE cache leg | `comp-cache` | CTO~Z-attested (105/105 clean) — **carried as their verification, not mine** |
| thread ORIENTATION | `pipescript <thread>` | orientation ONLY, never authority for a key/path; banner must be visible |
| **URL → S3 key (static-rewrite)** | **NO TOOL COVERS THIS** | `comp-routes trace` undiscriminating (positive-control-proven); pipescript stale; kuzu has no node |

**TOOLSEM seam:** the table binds to TOOL NAMES by question class, never to a backing store. ~D's
CANON2 has three legitimate outcomes (including "keep both projections, DECLARED"), so the source
migration sits BEHIND the tool interface — `comp-trace` remains the answer to source-structure
questions whether it reads `graph.json` or kuzu. The table stays valid under every CANON2 outcome, and
plugs into TOOLSEM's `(rail, grain, plane, scope)` typing when it lands rather than hardcoding a
parallel map.

**No-coverage is a first-class routing outcome.** Where a class has no covering tool, the rail should
say so explicitly ("no tool resolves URL→S3 key for this class; `comp-routes rewrites` holds the table;
here is the manual method") rather than point at a tool that cannot discriminate. An honest
no-coverage answer still carries the agent to the mapped knowledge that DOES exist — which is Andrew's
actual complaint — without manufacturing false confidence.

**Escape discipline retained:** the routing must not over-block. An over-aggressive route trains bypass
(the same BL-1 skim-death), and the 67 `rail-checked` overrides already in the log are the measured
proof that agents override a nudge that does not fit.

## Methodology control folded in (from ~D's own invalidated attempts)

~D's first two tests of the trace question were **INVALID**: MSYS mangled the leading-slash arg to
`C:/Program Files/Git/json/...`, and `MSYS_NO_PATHCONV=1` then mangled the wrapper's own python path to
`C:\c\Users\...`. **A "No match" from a mangled input is not evidence of a coverage gap** (the same
class CLAUDE.md flags for `git show <ref>:<path>`). Since the rail shells paths, any routing that
passes a URL/path argument must be immune to this or it will manufacture false "no match" verdicts —
so a **positive control is required** on any path-passing route before its verdict is trusted.
(Double-slash `//api/...` defeats the mangle.)

## Open / next

- **HELD:** all routing changes, pending ~Z's AC-2 ruling + ~D's per-class certification table.
- AC-5: no rail-gate STANDARD change is contemplated — this is coverage-strengthening within the
  existing rail. If the final design needs gate-semantics changes, it routes to main CTO.
