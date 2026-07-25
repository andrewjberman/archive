# NFRA_TOOLARCH.CANON / CANON2 -- Status Audit (in response to the "widen from census" redirect)

**Author:** `0.8.0_AE_CloudComp~D` · **2026-07-25** · **Redirect:** `1.0.0_SA_CTO~Z`, 20260725T053319Z
**Verifies:** `3.0.0_SA_CVO~Z` · **Gate (design/next-step):** `1.0.0_SA_CTO~Z`

---

## Headline: neither TO is unstarted. Both `<status>pending</status>` fields are stale, not a reflection
of the work. CANON is ~90% landed; CANON2's Leg A is 100% landed. The redirect's premise ("never got
executed") does not hold once the deliverables folder and git log are read -- and reading them surfaced a
bigger finding than a fresh audit would have: **the exact re-point work CANON2 is asking for was already
built and deliberately deferred a month ago, under a different project name, for a reason CANON2's own
framework can now formally resolve.**

---

## 1 · CANON status (not re-derived -- read from disk + git, per the redirect's own instruction)

| Acceptance criterion | Status | Evidence |
|---|---|---|
| 1. Floating-json audit, denominator derived | **DONE** | `NFRA_TOOLARCH_CANON_TOOL_SOURCE_AUDIT.md` (`fd12a515b9`, corrected `13c9d0f454`): 10/84 tools, 3 families, ground-verified |
| 2. Reroute-or-justify per tool | **DONE as routed recommendations** | Family 1 (pipescript) -> interim fix + refresh; Family 2 (graph.json, 7 tools) -> spun off as CANON2; Family 3 (stitch) -> folded into the exhibit fix; `nerves-risk-edges.json` (6 tools) justified LOUD-VINTAGE, kept |
| 3. Exhibit fixed, before/after on record | **PARTIALLY DONE.** Interim loud-vintage disclosure **LANDED** (`dcf1539150`, CTO~Z ruling 204001Z, confirmed in log `eb76769acd`). **The underlying fix (canonical mdpf refresh) is STILL BLOCKED** -- and this session has fresh, first-hand evidence of that: REC-1's mutant exercise (this same session, ~0410Z) ran `derive_stitch.py` directly and got `GRAIN_SENTINEL_FAIL` (rc=2, `EXTERNAL_ENDPOINT` count 0 vs baseline 3), matching 166 lines / 83 commits in the local `stitch-refresh.log` going back to 07-08. **The canonical thread has not been successfully refreshed since before CANON's own audit was written.** This is the one genuinely open, active item from CANON. |
| 4. comp-routes CF gap named | **DONE** | Named + recommended as a separate TO in the audit's own §"Item D" |
| 5. Session log | **DONE** | `logs/2026-07-23/session_D_toolarch_canon_floating_json_audit.md` |

**Net: 4 of 5 acceptance criteria fully closed; the 5th (exhibit fix) has its interim half landed and its
root-cause half blocked on a dependency this lane does not own (base 0.8.0 / the stitch producer) -- and
that dependency is confirmed STILL blocked as of this session, not merely "as of 07-23."**

## 2 · CANON2 status

| Leg | Status | Evidence |
|---|---|---|
| Leg A (coverage-parity precheck, BLOCKING+DECIDING) | **100% COMPLETE -- all 7 tools dispositioned** | Pilot 1 `comp-surface-check` (`e8934f81b8`): parity FAILS on `source_sha`, outcome 2/3 boundary, guard-3 item filed. Pilot 2 `comp-gitdrill` (`29d4d7d4a6`): RE-POINT CANDIDATE, gated only on a small `path` extension. cli.py five (`2b620f361a`): `source_sha` scopes to ONE tool (`comp-surface-check`), NOT the family -- but two NEW costs found (freshness-currency regression + silent vocabulary-mismatch, both all-5) |
| Leg B (re-point, outcome-1/2 tools only) | **NOT STARTED at the code level.** The MANDATORY pre-req (type-adapter mutant suite) is **spec'd but not built**: `NFRA_TOOLARCH_CANON2_ADAPTER_MUTANT_SPEC.md` (`fa8a9533ec`) states "No cli.py re-point lands before this suite is green" -- confirmed via source read this session: `org/modules/graph/cli.py` and `platinum_cli.py` have **zero** references to the marker-head bridge (see §4). `comp-gitdrill` itself still reads `.comp-graph/graph.json` directly (confirmed via source read this session, `comp_gitdrill.py:57-67`) -- it has the 07-24 vintage-guard fix (routes through `cli._get_graph()`, SHA-drift-checked) but has NOT been re-pointed to kuzu. |
| Leg C (output-contract re-declare, base 0.8.0's) | **No landed commit found** (searched `git log --all --grep`) -- appears to not have started, consistent with Leg B not having started (nothing to re-declare a contract for yet) |
| Leg D (verify) | Not applicable yet -- nothing has re-pointed |

**Net: Leg A is genuinely, fully done -- no new audit work is needed there. Leg B/C/D are genuinely open.**

## 3 · Denominator overlap (the redirect's specific ask)

Cross-referenced CANON's 10-tool floating-json set against the NFRA_TOOLUNIFY P1 census's (`D.md`, this
lane, 2026-07-24 -- one day AFTER CANON) `reads[]` typing, programmatically:

- **CANON's 10 floating-json readers are a 100% subset of the census's `FROZEN-SNAPSHOT` column (12
  tools).** Full agreement where they overlap -- the census's independent, later, differently-methoded
  audit did not contradict CANON's finding anywhere.
- **The census's `FROZEN-SNAPSHOT` column has 2 tools CANON's audit never covered: `comp-depth` and
  `comp-platinum`.** Checked both at source this session (not asserted from the census label alone):
  - `comp-depth` -- backed by `comp_depth_cli.py`, reads via `comp_marker_read.py`'s marker-head handle
    (NOT `.comp-graph/graph.json` directly) -- **this is a DIFFERENT, newer read path than the one CANON
    audited**, not a CANON gap so much as a fourth family CANON's audit vintage predates.
  - `comp-platinum` -- **this is exactly one of the two historical re-point targets from NFRA_GRAPHUNI.P2/D2**
    (see §4) -- CANON's audit and CANON2's 7-tool family both missed it, likely because `platinum_cli.py`'s
    graph read doesn't share `cli.py`'s literal string pattern the original scans keyed on.

**So the honest overlap answer: ~100% of CANON's own audit target is corroborated by the census, and the
census surfaces exactly one small genuine gap (`comp-platinum`) worth folding into CANON2's family --
raising it from 7 to 8 tools if `comp-platinum`'s graph.json read is confirmed live (not yet
individually source-verified to CANON2's HIGH-confidence bar; flagging, not asserting).**

## 4 · The headline finding: the CANON2 re-point was already built, and already deferred, a month ago

While checking `comp-platinum`'s backing (§3), its sibling module `org/modules/graph/comp_marker_read.py`
surfaced a direct hit. Its own docstring (authored by this same lane, `0.8.0_AE_CloudComp~D`,
**2026-07-01**, under project `NFRA_GRAPHUNI.P2/D2`):

> "The single read path every structure-tool (comp-blast/trace/xref/platinum) calls, so no tool ever reads
> a private divergent-vintage local cache (.comp-graph/graph.json) again... Re-point targets:
> `org/modules/graph/cli.py::_get_graph` (blast/trace/xref), `platinum_cli.py`."

**This is CANON2's own mission statement, verbatim, dated three weeks before CANON2 was dispatched.**
Confirmed via source read (this session): `cli.py` and `platinum_cli.py` currently hold **zero** call sites
into `comp_marker_read.py` -- the module was built, but the re-point was never wired in. Why, grounded in
its own commit message (`42b7f3c48a`, 2026-07-01):

> "RE-POINT NO-REGRESSION DEFERRED (finding surfaced to COO~B/CVO~B/CTO): the marker-head compute slice is
> NOT coverage-equivalent to build_graph's pre-delta trace graph -- scoped projection 2040n/2353e vs
> pre-delta 2152n/2772e; blast reachability far lower (e.g. `gold:D_01.partner_analytics` script blast exp
> 216 vs got 13). ... NOT closeable at the read-handle (the edges aren't there to canonicalize) -- needs an
> architectural decision (re-populate at build_graph fidelity vs re-run build_graph pinned to the marker
> head vs re-baseline the fixture). The re-point (cli.py flag) stays UNwired pending that decision."

**No commit resolving that architectural decision was found in the month since** (`git log --all --grep`
across "marker_read"/"marker-head" turns up only the build + a GRAPHDEPTH follow-on that rides the SAME
handle for a narrower purpose, comp-depth -- never the cli.py/platinum re-point itself).

**What this means, precisely:**
- The infrastructure CANON2's adapter-mutant-spec calls "the highest-risk, not-yet-built component" is
  **already built, smoke-verified, and has a CVO-accepted no-regression fixture on disk**
  (`org/tier1_exec/3.0.0_SA_CVO/NFRA_GRAPHUNI_P0-CVO_fixture/`, dated 2026-06-30).
- The coverage-parity concern CANON2's Leg A independently re-derived a month later (comp-surface-check's
  `source_sha` gap, the cli.py-five's freshness/vocabulary costs) has a **more precise, already-measured
  sibling finding** from NFRA_GRAPHUNI: an exact node/edge/reachability shortfall, with a real script's
  blast radius named and numbered (216 expected vs 13 got).
- **CANON2's own three-outcome coverage-parity framework (re-point / extend-then-re-point / declare-both)
  is exactly the disposition mechanism the NFRA_GRAPHUNI finding has been waiting a month for** -- but
  CANON2's Leg A work did not cite or re-measure against it, so the two threads are currently running in
  parallel without having been connected.
- **I did not re-measure the marker-head bridge's current coverage.** The 2040n/2353e-vs-2152n/2772e
  numbers are a month old and the estate has moved since (comp-manifest-check/comp-graph were voided as
  CANON2 pilot false-positives in that same window, the census itself found LAMBDA drift, etc.) -- citing
  them as still-true today would be exactly the stale-record-with-authority class this whole program exists
  to catch. **Recommending a fresh, targeted re-measurement as the next concrete action, not asserting the
  old numbers still hold.**

## 5 · What this changes about "genuinely new work needed" (the redirect's framing)

The redirect asked me to report how much of CANON's audit ask is already answered by the census vs.
genuinely new. The honest answer turned out to be sharper than that framing: **almost none of CANON/CANON2
Leg A is unanswered -- both by the census (§3) and, it turns out, by an even earlier, more precise internal
thread (§4) neither TO's authors connected to it.** The genuinely new work is not audit work at all; it is:

1. **A fresh coverage-parity re-measurement** of `comp_marker_read.py`'s projection against today's
   `build_graph` output, superseding the month-old numbers -- this directly answers CANON2's Leg A
   coverage-parity question for the cli.py five and `comp-platinum` in one pass, using infrastructure that
   already exists, rather than building a new adapter from zero.
2. **Closing the deferred architectural decision** from `42b7f3c48a` (re-populate marker-head at
   build_graph fidelity / re-run build_graph pinned to the marker head / re-baseline the fixture) -- this
   was escalated to COO~B/CVO~B/CTO a month ago and, as far as this session's search found, was never
   closed. It should be re-surfaced now that CANON2 gives it a formal outcome-1/2/3 disposition path.
3. **The canonical mdpf refresh** (CANON's one open item, §1) -- confirmed still blocked this session, not
   this lane's to fix (base-owned per the original TO's coordination clause).
4. **`comp-platinum`'s addition to the CANON2 family**, pending individual source-verification to the same
   bar as the other 7 (flagged, not yet done).

**None of this is a re-audit. It is closing two already-open threads that turned out to be the same
thread.**

## 6 · What this lane did NOT do

Did not re-measure marker-head coverage (recommended as next step, not executed -- a real engineering
measurement belongs to a dispatched leg, not a status-audit report). Did not wire any re-point. Did not
resolve the deferred architectural decision (COO~B/CVO~B/CTO's call, now CTO~Z's to re-open or re-route).
Did not individually source-verify `comp-platinum`'s graph.json read to CANON2's HIGH-confidence bar (flagged
as a gap, not closed). Did not touch either TO's `<status>` field -- flagging the drift, not self-correcting
another agent's/my own prior TO's status without a ruling on whether "pending" should become
"blocked"/"partial"/something else.

## 7 · Recommendation on the TO status fields (a process finding, not just a data one)

Both `NFRA_TOOLARCH.CANON` and `NFRA_TOOLARCH.CANON2` TO files still read `<status>pending</status>` despite
the work in §1-2. **This is very likely why the redirect assumed they "never got executed"** -- the TO
status field is the fastest signal a dispatcher reads, and it was never updated across ~10 substantive
commits. Recommend: TOs with this much landed work get an intermediate status (`in-progress` /
`blocked-on-X`) rather than staying `pending` indefinitely, or a rule that a session log with a
`Current State` section pointing at a TO should trigger a status touch. Surfacing, not self-ruling on the
mechanism.
