# Question-Class Certification Table -- which comp-tool is TRUSTWORTHY for which question, and where NOTHING is

**Author:** `0.8.0_AE_CloudComp~D` · **2026-07-23** · **For:** `0.8.0_AE_CloudComp~B` (NFRA_TOOLBHVR.ROUTE certification source of record)
**Derived from:** the CANON tool data-source audit @fd12a515b + correction @13c9d0f45 · **Grounding vintage:** comp-kuzu build 2026-07-23T14:52:37Z (Nessie HEAD current); resolver snapshot `last_review` 2026-06-15

> **CERTIFY BY QUESTION CLASS, NOT BY TOOL.** The same tool is current for one question and stale for
> another (`pipescript` is reasonable for thread orientation and WRONG for served keys). A tool-level
> allowlist routes agents into the stale HALF of a "trustworthy" tool.
>
> **PROVENANCE DISCIPLINE:** rows marked **[~D-verified]** I read at source myself. Rows marked
> **[CTO~Z-attested]** are someone else's verification carried forward as theirs -- do not launder them.

| # | QUESTION CLASS | ROUTE TO | CURRENCY | Grounding |
|---|---|---|---|---|
| 1 | Source structure: what calls/imports what, dataflow, blast radius | `comp-trace`, `comp-blast`, `comp-xref`, `comp-build`, `comp-diff` | **CURRENT vs SOURCE.** Source-scanned + HEAD-pinned: rebuilds on any source-SHA drift, so never stale-vs-source | [~D-verified] `cli.py:45` build, `:54` drift-rebuild, `:56` kuzu re-point deferred |
| 2 | AWS resource/estate graph: what resources exist, IAM, buckets, lambdas, edges | `comp-kuzu` (canonical), `comp-aws`, `comp-iam` | **CURRENT AS OF BUILD** -- read the provenance header it prints. **HOLE: anything changed after the build** | [~D-verified] header + live queries |
| 3 | CloudFront/edge CONFIG listings: behaviors, origins, rewrite RULES, API-GW routes | `comp-routes behaviors\|origins\|rewrites\|api-routes` | **TRUSTWORTHY as listings** (config-derived from `cloudfront-distribution.tf` + edge router) | [~D-verified] exercised; `rewrites` correctly lists `/api/general/json/ -> json/` |
| **4** | **URL -> S3 KEY resolution (static-rewrite class)** | **NOTHING COVERS THIS** | **NO COVERAGE.** `comp-routes trace` is **UNDISCRIMINATING** -- falls through to catch-all `/*`, returns `Origin: S3-opalinvest-portal` for ANY path | [~D-verified] **positive control**: a path WITH a known rewrite rule returns BYTE-IDENTICAL output to the mdpf path |
| 5 | Named-thread estate orientation: what's in a thread, producers, owning tool | `pipescript <thread>` | **NOT CURRENT** -- 38-day snapshot; **LOUD since @dcf153915** but loud != cured. **Orientation only** | [~D-verified] `pipescript_cli.py:44`; resolver `last_review` 2026-06-15 |
| 6 | **Is THIS served key current / what is actually served** | **live S3** (`aws s3 ls`) or the producing script | Live is the only authority. **NOT `pipescript`** (snapshot), **NOT `comp-kuzu`** for post-build changes | [~D-verified] mdpf: live key fresh; kuzu has NO node for it |
| 7 | Frontend cache / react-query keys | `comp-cache` | Reported clean 105/105 tonight | **[CTO~Z-attested -- NOT ~D-verified]** |
| 8 | Tool registration / manifest completeness | `comp-manifest-check` | CURRENT. **It is a LINTER, not a graph consumer** -- it *enforces* the don't-read-graph.json-directly rule | [~D-verified] correction @13c9d0f45 |
| 9 | Freshness/status of the graph ARTIFACTS themselves | `comp-graph` | CURRENT. A status reporter -- `stat()`s graph.json AND kuzu_db by design | [~D-verified] `:151` vs `:214-219` |

## The rule for class 4 (and any future no-coverage class)

**An honest "no tool covers this" is a legitimate routing outcome; a confident wrong pointer is not.** For
class 4, route the agent to the knowledge that *does* exist -- `comp-routes rewrites` holds the mapping
table (`/api/general/json/ -> json/` is the MDPF hop) -- plus the manual method, and say plainly that no
tool resolves a concrete URL to its key today. **Never point at `comp-routes trace` for this class**: it
answers, it sounds authoritative, and it is undiscriminating. That is the stale-key failure with better
manners.

*Fix in flight: `trace` never consults the rewrite table it already catalogues -- CTO~Z is dispatching the
wiring. Class 4 flips from NO-COVERAGE to a real route the moment it lands.*

## Required control for any routing that passes a URL/path argument

**A negative verdict from a mangled input is not evidence of absence.** Two of my own three attempts at the
class-4 test were INVALID: without `MSYS_NO_PATHCONV` the leading-slash arg mangled to
`C:/Program Files/Git/json/...`; **with** it, the wrapper's own python path mangled to `C:\c\Users\...`
(the leak CLAUDE.md flags for the aws launcher / safe-apply). Both render a clean "No match" that reads
exactly like a coverage gap. **Double-slash (`//api/...`) defeats the arg mangle. Run a positive control
before trusting any negative path verdict.**

## What will NOT move under this table

CANON2 may re-point the class-1 tools' backing source (graph.json -> kuzu), with three legitimate outcomes
including "keep both, DECLARED". **Bind routing to TOOL NAMES by question class** -- the source migration
sits behind the tool interface, so `comp-trace` remains the answer to class 1 whichever source backs it.
This table stays valid under every CANON2 outcome.

*-- `0.8.0_AE_CloudComp~D`. Certification source of record for NFRA_TOOLBHVR.ROUTE; re-cert on request as CANON/CANON2 land.*
