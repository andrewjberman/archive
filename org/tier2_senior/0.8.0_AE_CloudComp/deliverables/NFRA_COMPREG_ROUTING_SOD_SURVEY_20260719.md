# Comp-tool registration flow -- ROUTING/SoD axis survey (consult-input to ~D's build)

**Author:** 0.8.0_AE_CloudComp~Z | **Date:** 2026-07-19 | **For:** 0.8.0_AE_CloudComp~D (owns the full registration-flow build, MSTR ruling) | **COO:** 2.0.0_SA_COO (sequenced this as read-only consult-input) | **archetype:** EXPLORE

**Grounded, not recalled** -- every count/claim is from live state at HEAD (comp-manifest-check, graph-call-manifest.yaml, comp-coverage-map.yaml, comp-which source, comp-tool-hud.sh, the recent registration commits). READ-ONLY survey; no build. Mirror of ~D's mechanics-axis grounding, on the ROUTING axis: *how a new/revised comp-tool becomes REACHABLE, who commits what, and where the ad-hoc path DRIFTS on routing.*

## 1. The routing surfaces a tool must register on (the "reachable" checklist)

| Surface | File | Live count (HEAD) | What it governs on the routing axis |
|---|---|---|---|
| Manifest entries | `org/modules/graph/graph-call-manifest.yaml` `entries[]` | **98 entries / 66 distinct tools** (all carry `use_case`) | The tool's natural-language `use_case` text -> the posterior/fuzzy backstop scores against it. Multiple entries per tool = multiple intents. |
| Routable catalog | same file `tools_index{}` | **61 tools** | THE routable set -- comp-which only routes TO a tool in `tools_index`. Not here = not a routing target (unreachable by the router). |
| Curated RULES | `.tools/comp-which` `RULES=[]` | **73 rules** | The curated fast-path (precision layer) -- a strong curated match wins rank-1 over the posterior. A tool with NO rule relies entirely on the posterior. |
| Coverage-map homes | `org/modules/graph/comp-coverage-map.yaml` | `tools[]` **35** (data/query tools, homed by presence -- no `routable` flag) + `meta_tools[]` **47 (30 routable=true)** | ONE-home invariant. META tools carry an explicit `routable` flag -- a meta tool is a routing target ONLY if `routable: true` (default false). Regular `tools[]` routability = `tools_index` membership. |
| Registration invariant | `comp-manifest-check` (fail-closed gate) | **79 executables all accounted** (tools_index 61 + excluded 15 + entries-tools 66; coverage-map 82) | DISK-IMPLIES-REGISTERED: every `.tools/comp-*` on disk must be registered-or-excluded, else the commit BLOCKS. This is the "one denominator" reconciler.

## 2. The routing pipeline a tool plugs into (comp-which, the reachability chain)

`comp-which "<question>"` routes through, in order:
1. **Curated RULES** (`.tools/comp-which` `_score_rule` over `RULES`, n=73) -- a strong curated match (score >= vetted band 1.0) wins.
2. **COMPROUTE posterior** (the default router, `comp_route.py`): `score = w_q*query_match + w_s*surface_prior + w_h*history_affinity`, margin-disambiguation gate, `relevance_floor = 0.25` (TO-2-set from the distribution).
3. **NO-FIT / abstain**: below `relevance_floor` -> `kind=="fallback"` -> RUNS comp-grep/comp-glob (never a dead-end); candidates above floor but below vetted band -> weak menu + warning + PRINT the fallback + `rc=1`. (WS-7 grounded + CVO-verified.)
4. **Top-3 output** (Andrew-direct, never argmax-to-1).

A tool is REACHABLE iff it is in `tools_index` AND either (a) has a curated RULE (deterministic rank-1 on its vocabulary) or (b) the posterior scores its `use_case` above the floor for the query. **(a) is a safety net; (b) alone is the weak-match risk (see Drift #2).**

## 3. The SoD -- grantee-cannot-self-register (the atomic exec/AE split)

Worked example: comp-similar (`e58a1bcd6` + `2956c2751`), comp-describe (`e3f6faa00`), comp-kuzu (`7288d1267`), comp-genesis (`59b37efea`).

- **AE/DS BUILDS** the engine (`org/modules/graph/*`) + the `.tools/comp-*` wrapper + authors its `comp-tools.yaml` entry + `coverage-map` home.
- **exec/COO LANDS the routing registration** -- the `graph-call-manifest` `tools_index` + `entries` + the `comp-which` curated RULE -- because **the grantee cannot self-register** (SoD). CTO arch-gates.
- **ATOMICITY is forced by the invariant:** `comp-manifest-check` requires the registered tool be git-tracked, so the routing row + the wrapper **cannot land alone** (a `.py`-only or row-only commit BLOCKS). The exec land is atomic (row + wrapper `git add -f` together); the AE commits `comp-tools.yaml` + `coverage-map` in a coordinated sibling commit. **This is the #1 mechanical friction ~D's flow must sequence** (comp-similar hit it: "neither can land alone").

## 4. WHERE THE AD-HOC PATH DRIFTS ON ROUTING (the high-value part -- what the flow must ENFORCE)

Each is grounded in a real incident this estate has already paid for:

1. **Registered-but-not-routable (silent).** A tool on disk lands `excluded` (15 are) or is homed in `coverage-map` without `routable: true` (meta default is false). The invariant passes (it IS accounted), but the tool is unreachable. **comp-describe + comp-kuzu both shipped needing an explicit `routable false->true` flip** (`e3f6faa00`, `7288d1267`) -- the flow must make the routable flip a REQUIRED step, not a remembered one.
2. **In tools_index but NO curated RULE -> posterior-only weak match.** Measured at HEAD (TO-1 harness cohort-C): **12 of ~66 tools' `use_case` text scores ZERO against the curated RULES** (comp-aws x5 sub-uses, comp-coverage, comp-gitdrill, comp-honesty, comp-shell, comp-tool-health, comp-xref, comp-which). Only **2/87 fail to route live** (the posterior saves the other 10) -- but they carry NO safety net. Comp-which source is littered with "comp-X had NO curated rule at all -> invisible" retrofits (comp-trace `:172`, comp-kuzu/comp-surface-check `:418`, comp-depth `:553`). **The flow must assert every new tools_index tool has >=1 curated RULE (or consciously accept posterior-only).**
3. **RANK-1 THEFT (the automated gate's HOLE).** A new tool's curated rule/vocab silently STEALS an existing tool's rank-1. **Exemplar (CTO-routed 2026-07-18, on COMPROUTE's blocking field): comp-genesis's first-draft vocab stole comp-system's "current compiled system state" rank-1 -- caught only by a HAND spot-check while `comp-which-routing-test.py` PASSED.** The routing-test asserts self-route *regression* (does each tool still route to itself?) but NOT cross-tool theft (did a NEW tool flip an EXISTING tool's rank-1?). **This is the single most important assertion ~D's flow should add: any tool add/vocab-edit must prove no existing tool's rank-1 flips to the new tool** (comp-similar's registration did verify this by hand: "comp-describe/comp-dups KEEP rank-1, no theft" -- but by hand, not by gate).
4. **write_path mis-tag -> wrong DR1 routing exclusion.** comp-kuzu-full/inc were corrected `write_path true->false` (`7288d1267`): DR1 excludes `write_path:true` tools from the "my graph is behind, refresh then query" READ intent. A mis-tagged producer-vs-reader flips whether the tool is routable for read intents.
5. **Divergent `use_case` per tool -> self-retrieval failure.** comp-aws carries 5 entries; several score 0 against their own catalog (cohort-C). Multiple divergent intents per tool dilute the posterior signal. The flow should sanity-check a new tool's `use_case`(s) retrieve the tool itself (cohort-C self-consistency, currently 13.8% fail).

## 5. Handoff note to ~D

This is the ROUTING-axis map + the 6 drift modes; it pairs with your MECHANICS-axis grounding. The **two flow-gates I'd most want the standardized registration flow to add** (both currently done by-hand or not-at-all):
- **A no-rank-1-theft assertion** (Drift #3) -- extend `comp-which-routing-test.py` so any tool add/vocab-edit asserts no EXISTING tool's rank-1 flips. This closes a live gate hole (comp-genesis proved it).
- **A required routable-flip + curated-rule step** (Drift #1 + #2) -- so a tool can't land registered-but-unreachable, and every routable tool has a curated safety net (or a conscious posterior-only waiver).

All source-cited above; happy to go deeper on any drift mode or pair on the routing-test extension when you hit that axis.
