# Bundle item 7 design — comp-constants POLYGLOT + `--complete-over` (NFRA_PSTMRT)

**Authority:** Andrew-direct handover @7cc6376e5 · ~Z Phase-1 interfaces (223500Z, validated-closed
224107Z) · CTO heads-up 224631Z (scope filter is load-bearing — he false-FAILed live on
portal-only mockadv). Design pinned before build; sequencing mine.

## The two bounded changes (postmortem #2, verbatim scope — nothing else)

### A. POLYGLOT: parse .mjs/.ts constant sites

- **Why:** the multifirm lane's sites are `.mjs`/`.ts` — `ast.parse()` structurally cannot read
  the ONE lane that covers firm enumeration (postmortem blindness #2; the 05-08 finding sat in a
  `notes:` string because the extractor could not see the site).
- **How (bounded, not a JS compiler):** `extract_ts_source.strip_comments` (@b6e4a784c — the
  item-2 stripper is the shared comment model) → structured regex extraction of TOP-LEVEL
  `const NAME = {...}` / `export const NAME = {...}` object literals → member KEY set (string keys
  + identifier keys). The unit of comparison is the KEY SET, exactly what firm-map completeness
  needs. Nested-object depth-1 only; a site needing deeper parsing gets an honest
  `UNPARSEABLE-SITE` verdict (never a silent 0 — comp-grep's clean-0 lesson).
- **Acceptance targets (~Z-set):** `infra/aws/lambda-edge/_shared/firm-config.mjs`
  (FIRM_CONFIG / FIRM_BUCKET_MAP) + `firmAccess.ts`. Test = the real files at vintage.

### B. `--complete-over`: the completeness AXIS (drift ≠ completeness)

- **Why:** every firm map agreed perfectly and was uniformly missing Cottonwood — zero drift,
  correctly reported, wrong axis. A completeness signal whose denominator is its own
  configuration is the whole postmortem.
- **Semantics (~Z PRD §2, adopted verbatim, all five):**
  1. Matching tokens = `firm_id` + `tree_token` + `aliases[]` from `data/firm_registry.json` —
     never a per-tool token list.
  2. **COMPLETE-OVER A DECLARED SCOPE** — config marks a constant
     `firm_keyed: {complete_over: portal|mdpf|pipeline}`; expected set = registry firms with
     `scopes[<scope>] == true` and `enabled == true`. NEVER the full registry (mockadv
     false-fire = the BL-1 death; CTO reproduced it live 224631Z — bake the filter in from the
     start, it is load-bearing for ANY assertion against this registry).
  3. Uniformly-incomplete set = **FAIL**. Unregistered token (a member NOT resolvable to any
     registry firm) = **FAIL equally loud** (the inverse defect: a phantom firm).
  4. **Denominator printed every run**: `checked K firm-keyed structures against N expected
     firms (scope=S, registry vintage=<mtime/sha>)`.
  5. Exemptions carry `{firm, by, date, why, expires}` — expiry past due = the exemption FAILS.
- **Verdict vocabulary** (the census lesson — FAIL must not mean five things): `COMPLETE` /
  `INCOMPLETE (missing: [...])` / `PHANTOM (unregistered: [...])` / `UNPARSEABLE-SITE` /
  `EXEMPT (expires ...)`, distinct exit codes, registry vintage on every line.

## Config schema (additive to comp-constants seed yamls)

```yaml
constants:
  FIRM_CONFIG:
    file: infra/aws/lambda-edge/_shared/firm-config.mjs   # .mjs now legal
    firm_keyed:
      complete_over: portal
    exemptions:
      - {firm: mockadv, by: <serial>, date: 2026-07-22, why: "demo tenant, portal-only", expires: 2026-10-01}
```

## Controls the build must ship with (discipline as on all bundle items)

- Positive control: registry temporarily extended with a synthetic firm in-test → every declared
  structure reads INCOMPLETE naming it (the gate CAN fire; run in isolation).
- Negative control: unregistered token injected in a fixture site → PHANTOM fires.
- Mutant: delete the scope filter → the mockadv false-fire test must go red (locks CTO's lesson).
- The 05-08 exhibit as regression: the multifirm seed's three `notes:` findings become the
  worked example — the gate must FAIL on the pre-Cottonwood shape of firm-config.mjs (fixture)
  and PASS on today's.
- Registry read is fail-closed: absent/unparseable registry = REFUSE (exit 3), never
  "no registry, no findings" (an ungated pass).

## Not in scope (said, not silent)

Postmortem #3 (`notes:` → assertions across all tools) is the generalization — SEPARATE, after
the bundle. Item 7 does it for comp-constants' firm axis only. The `.ts` half parses the SAME
const-object shape; anything TS-specific beyond that (types, enums) is out of the bounded scope
and lands UNPARSEABLE-SITE-honest until a real site needs it.
