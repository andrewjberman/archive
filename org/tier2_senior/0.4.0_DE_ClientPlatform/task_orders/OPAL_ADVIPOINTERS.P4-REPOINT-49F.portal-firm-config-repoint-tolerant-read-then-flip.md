# TO OPAL_ADVIPOINTERS.P4-REPOINT-49F — portal firm-config repoint per served key: tolerant read -> flip (push plan §3 row 4c, DE half)

<task_order id="OPAL_ADVIPOINTERS.P4-REPOINT-49F" project="OPAL_ADVIPOINTERS">
<issued_to>0.4.0_DE_ClientPlatform</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-18T16:05Z</issued>
<dated>2026-08-22 — after 4a (platinum twins exist) + 4b (per-key pin + cert). Sequenced at your seat: T-A (in flight now) -> T-C (08-20) -> this. Per-key: a key flips only when ITS pin + cert exist; keys flip independently.</dated>
<status>staged -- GO paired; tolerant-read implementation may start once twins exist (08-20); flips gated per key on CVO cert</status>
<priority>P1 — the flip is the cutover; everything before it is preparation</priority>
<authority>Push plan @a2f27c8d0a §3 row 4c + §2 DE row (T-A first act, then P4 repoint). Never-widen per key (CTO+COO determination; DELTA=0 keys need no hold). Andrew's 08-12 "proceed with the cutover" answers the 49F cutover.</authority>
</task_order>

## Objective
Repoint the portal's 49financial Advisor Intelligence reads per served key from the legacy serve to
`platinum/advi/49financial/` — tolerant read first (new-preferred, legacy fallback, loud on shape
mismatch), then the flip per key once CVO's pre-flip pin + cert for that key exist.

## Context
Grounded this session (COO): the ADVI serve is firm-parametric — CloudFront
`/api/scoped/advisor-intelligence/artifacts/*` -> S3 origin via FIRM_BUCKET_MAP + shared-advisor-router;
portal cache keys carry `firmOverride` (105/105 useQuery call sites captured, zero hardcoded
49financial keys). So the repoint surface is firm-config + the router's key resolution for the
49financial firm — enumerate the actual per-key read surface as your first act (comp-routes +
firm-config), do not assume it is one file.

## Compiler tools (three-phase)
Phase 1: `comp-routes behaviors` (the ADVI behaviors + router legs) + `comp-cache key advisor-intelligence`
— expect the 7 standing keys w/ firmOverride; `comp-transform schema-check` per component whose read
shape could move. Phase 2: `bun run build` zero TS errors + schema-check 0 MISSING. Phase 3:
`/frontend-dev` rendered read on DEV per flipped key's surface.

## Cross-domain coordination
- shared_resource: `platinum/advi/49financial/**` (read) — DS~B writes (P4-EMIT); CVO pins. Per-key
  flip order: MCP CVO at each key's flip (their cert is per key AT flip).
- shared_resource: portal firm-config + router — DT promotes your commits (P4-PROMOTE); enumerate the
  exact commit set for DT (the PROD payload is exactly your repoint commits — DT's baseline is 0
  PROD..DEV today).
- shared_resource: `pairedProvenanceRead.ts` — T-A (in flight) touches it; land T-A before this TO's
  flips so the two changes never interleave in one surface.

## Acceptance criteria
- P4R-1 READ-SURFACE ENUMERATION: the per-key read surface committed first (key -> config/router/
  component read path), denominator = the FROZEN KEY LIST (P4E-1); any key whose read the portal does
  not exercise is stated as such (a key nobody reads cannot be flipped — it is disposed in writing,
  not silently skipped).
- P4R-2 TOLERANT READ: per key, new-preferred/legacy-fallback read landed with a LOUD shape-mismatch
  path (the FE-2 mutant discipline: unknown shape degrades loud, never silently falls back); zero
  TypeScript errors; schema-check 0 MISSING.
- P4R-3 FLIP PER KEY: flip commit per key (or per stated key group) ONLY after CVO's pre-flip pin +
  cert for that key are cited in the commit message; rendered read on DEV per flipped surface
  (screenshot via /frontend-dev — silver-canvas law holds).
- P4R-4 NOTHING BLENDED: before/after deltas per key reported as NAMED deltas (content-refresh vs
  route-move), never blended (the BP-5 discipline from row 0).
- P4R-5 DT HANDOFF: the exact commit enumeration to DT + MSTR for the PROD promote, with the flip
  keys listed.
- P4R-6 proof instance VALID rc=0 positional: ids P4R-1,P4R-2,P4R-3,P4R-4,P4R-5,P4R-6.

<proof_of_spec>
  <expected_criteria>P4R-1,P4R-2,P4R-3,P4R-4,P4R-5,P4R-6</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DE_ClientPlatform/deliverables/OPAL_ADVIPOINTERS.P4-REPOINT-49F_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

## Do not
- Portal main tree stays on DEV (Rule 19). No PROD push from your seat (DT + MSTR lane).
- No flip of a key whose pin/cert is absent — DECLARED-HELD per key, in writing.
- Do not modify the Lambda@Edge router's deployed version yourself — router changes route through AE
  if any are needed (surface to COO first; the tolerant read should live portal-side).

## Reporting
COO (cc CTO, CVO, DT, MSTR) at read-surface committed, at tolerant-read landed, per key at flip.
Surprise channel: one banked line to COO. Session log with Compiler Tools section = deliverable.
