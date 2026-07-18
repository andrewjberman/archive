# NFRA_COMPREG Deliverable 5 -- ANY_EXEC_OR_AE ownpath grant PROPOSAL (for CTO arch-gate)

**Author:** 0.8.0_AE_CloudComp~B (PROPOSES). **Lands:** CTO arch-gates + MSTR/CTO commits the
`.owned-paths.yaml` edit at canonization (SoD -- grantee never commits its own grant; every precedent in
this file is grantor-landed). **Mandate:** Andrew-direct @04bee845a ("...ownpath alongside CTO/CVO for
committing tools according to that process... probably ANY_EXEC_OR_AE for ease of ops"). **Grounded on:**
`.owned-paths.yaml` @ current CLOUD, path-rules block lines 1006-1112 + the DECOMTOOL bridge-grant note
line 1056.

## Finding: the grant is ONE additive path rule (the registration surface is already 95% AE-permitted)

CTO gate point 1 was: *"Show me the grant's scope is the registration files ... and NOT the locked do-er
surfaces."* Grounded against the live `.owned-paths.yaml`, almost the entire registration surface is
**already** on `ANY_EXEC_OR_AE` (or `ANY`). Exactly one file that the atomic bundle must touch is not:

| Registration-surface path (what an atomic bundle commits) | Current lane | AE-permitted today? |
|---|---|---|
| `org/modules/graph/comp-tools.yaml` | ANY_EXEC_OR_AE (1058) | YES |
| `org/modules/graph/comp-coverage-map.yaml` | ANY_EXEC_OR_AE (1062) | YES |
| `org/modules/graph/comp_*.py` (engines, incl. `comp_capability_provider.py`) | ANY_EXEC_OR_AE (1006) | YES |
| `org/modules/graph/*_cli.py` (CLI entrypoints) | ANY_EXEC_OR_AE (1010) | YES |
| `.tools/comp-which`, `.tools/comp-*` (router + wrappers) | ANY (1465) | YES (any agent) |
| **`org/modules/graph/graph-call-manifest.yaml`** (tools_index + entries + excluded_not_graph_use_cases) | **none -> falls to `org/modules/**` = ANY_EXEC (1112)** | **NO -- the gap** |

`graph-call-manifest.yaml` is the sole registration file with no specific rule, so it falls to the
`org/modules/**` catch-all (`ANY_EXEC`, which excludes AE). It holds the three keys member 5 checks
(`tools_index`, `entries:`, `excluded_not_graph_use_cases`), so an AE currently cannot self-commit a tool's
registration -- which is exactly why comp-iam-usage was landed by CTO under single-editor SoD. The DECOMTOOL
bridge-grant note (line 1056) predicted this general grant and named the locks to preserve.

## The exact delta (ADDITIVE-ONLY -- one rule inserted, nothing changed or removed)

Insert BEFORE the `org/modules/**` catch-all (longest-match-wins), mirroring the adjacent
`comp-tools.yaml` / `comp-coverage-map.yaml` / `drift-topology.yaml` grants verbatim in shape:

```yaml
  "org/modules/graph/graph-call-manifest.yaml":
    lane: ANY_EXEC_OR_AE
    note: "The comp-tool CATALOG + registration surface (tools_index, entries:, excluded_not_graph_use_cases)
      -- the keys comp-manifest-check's registration invariant (members 4/5) reads. AE registers a tool here
      as part of the atomic bundle (executable + registration, one commit) per the canonical comp-tool flow
      (org/modules/graph/COMPTOOL_REGISTRATION_FLOW.md). Registration DATA, not gate LOGIC: the completeness
      gate (manifest_check_cli.py, COMPILER_MANIFEST_CHECK lane) still enforces on every commit regardless of
      author lane, so this cannot weaken any gate. Mirrors the comp-tools.yaml / comp-coverage-map.yaml
      ANY_EXEC_OR_AE grants (longest-match over org/modules/** ANY_EXEC). Supersedes the per-tool bridge
      globs' manifest half. NFRA_COMPREG (Andrew-direct @04bee845a); CTO arch-gate; grantor-landed (SoD)."
```

**That is the entire delta.** Members `0.8.0_AE_CloudComp` (base) + `~B` are already in the
`ANY_EXEC_OR_AE` lane (lines 562/564), so no lane-membership edit is needed -- only the path rule.

## Preserved exec-locks (explicitly NOT touched -- CTO gate point 1)

| Exec-lock surface | Rule / lane | Status under this proposal |
|---|---|---|
| debtscan do-er-gate (suppressions, scan config, non-.md) | `org/modules/graph/debtscan/**` exec-locked (962) | UNTOUCHED |
| comp-manifest-check gate family (the enforcement logic) | `org/modules/graph/manifest_check_*` -> COMPILER_MANIFEST_CHECK (1034) | UNTOUCHED |
| pipescript CLI | `org/modules/graph/pipescript_cli.py` -> NFRA_PIPESCRIPT_TOOL (1038) | UNTOUCHED |
| comp-system / NFRA_SYSTEM do-er | `comp_system.py` already ANY_EXEC_OR_AE via `comp_*.py`; `infra/system/**` docs (1360) | UNTOUCHED |
| everything else under org/modules/ | `org/modules/**` = ANY_EXEC (1112) | UNCHANGED (still exec-only) |

The proposal adds exactly one longest-match rule and changes/removes nothing, so every existing lock holds
by construction. **Why granting the manifest is safe:** `graph-call-manifest.yaml` is registration DATA; the
gate that polices it (`manifest_check_cli.py`) is separate and runs on every commit no matter who authors --
an AE editing the manifest to REGISTER a tool is the intended action, and it cannot bypass the completeness
family (the family fail-closes on a malformed or incomplete registration regardless of author).

## Companion flow guidance (keeps future grants at zero)

To avoid a new per-tool glob every time (the recurring pattern this file is full of), the canonical flow
recommends: **name a tool's engine `comp_<name>.py` or `<name>_cli.py`** (both already ANY_EXEC_OR_AE) and
**put the launcher under `.tools/`** (ANY). With the manifest rule above, an AE can then land a complete
atomic bundle -- engine + wrapper + tools_index + entries + excluded + coverage-map home + comp-which route
-- with no further owned-paths change. Oddly-named engine modules (e.g. `debris_*.py` adapters) still need a
per-tool glob; that is a naming choice, not a gap in this grant.

## Deliverable 4 companion (prompt.md reference -- MSTR lands at canonization)

Proposed reference line for `org/tier2_senior/0.8.0_AE_CloudComp/prompt.md` (MSTR lands it with the
canonized doc, per MSTR 041434Z):

> **Committing a comp-tool:** follow the canonical flow at `org/modules/graph/COMPTOOL_REGISTRATION_FLOW.md`
> -- decide the disposition (routable / entries-only / excluded), land the ATOMIC BUNDLE (executable +
> registration in ONE commit), validate with `comp-manifest-check completeness` + `comp-which "<question>"`.
> You hold `ANY_EXEC_OR_AE` ownpath on the registration surface alongside CTO/CVO.
