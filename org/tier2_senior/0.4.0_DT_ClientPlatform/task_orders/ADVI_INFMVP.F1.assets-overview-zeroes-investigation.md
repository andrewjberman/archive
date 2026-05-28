# ADVI_INFMVP.F1 — Assets Overview all-zeroes for Peter (investigation-first) (DT)

**Project:** [ADVI_INFMVP](../../../projects/ADVI_INFMVP.json)
**PRD:** `docs/architecture/ADVI_INFMVP.md` v0.1 §3 F1 + §7 Q1 (commit 5f6018778)
**Pod:** 0.4.0_DT_ClientPlatform
**Lane:** DT_ClientPlatform (permissions / data-scoping investigation); pull 0.4.0_DE_ClientPlatform for the FE-fetch-trace half if the zero originates client-side
**Issued to:** 0.4.0_DT_ClientPlatform
**Author:** 2.0.0_SA_COO 2026-05-28T~19:46Z (/drive — CTO NOVEL_PRD_READY handoff 19:45Z)
**Sizing:** ~60-90min wall (end-to-end trace + 49F comparison; fix sized after root cause)
**Authority anchor:** CTO PRD v0.1 5f6018778 + Andrew direct 2026-05-28 (Peter sees all-zeroes Assets Overview)

<status>pending</status>

## Objective

`peter@inflectionwealth.com`'s **Assets Overview panel renders all zeroes** while his other panels are scoped correctly. **Root-cause FIRST — do not patch blind.** Trace the Assets Overview data fetch end-to-end and identify exactly where the value goes to zero, comparing against a working tenant (`49financial`) on the identical panel.

## Investigation (root-cause before fix)

1. **Trace the fetch chain:** Assets Overview component → endpoint/Lambda → S3 key or API → the artifact actually served for the Inflection tenant. Identify the component file + the fetch hook + the key/route.
2. **Find the zero origin** — classify into one of:
   - empty/absent artifact (Inflection tenant artifact never emitted — DS emit gap)
   - filtered rows (firmId / advisor-key / household-scoping filter excludes Inflection)
   - wrong key (Inflection resolves to a key with no data)
   - auth-scoped empty response (permissions / firm-filter gate returns empty)
3. **Compare against 49F** on the identical panel — what differs in the key, the filter, the artifact presence, the auth scope.
4. **Permissions angle:** if the fetch is auth-gated, cross-check `comp-iam service <lambda>` + firm-scoping logic. Use `comp-routes trace <fn>` for the CF→auth→S3 path if a 4xx/empty-response is involved.

## Acceptance criteria

- **AC1a.** Root cause **identified and documented** — a written statement of where the zero originates (which of the 4 classes above, with the exact file/key/filter line).
- **AC1b.** Fix lands correct **non-zero** Assets Overview data for Peter, verified against his actual book (cross-check the totals are plausible vs his known AUA — magnitude sanity per /drive heuristic).
- **AC1c.** **No regression for other tenants** — 49financial Assets Overview still correct after the fix.
- **AC1d.** Q1 resolved in the RAVC2: is this a DS emit gap or an auth/firm-filter gap? (Determines whether any DS follow-on TO is needed — flag ws COO if a DS emit is required.)

## Dependencies

- None to start the investigation (independent per PRD §4). The **fix** may spawn a DS-emit follow-on if AC1d resolves to "missing Inflection artifact" — surface to ws COO at root-cause moment for the follow-on lane assignment.

## Sequencing

1. ~10min: locate the Assets Overview component + fetch hook in `portal/`
2. ~20min: trace endpoint → S3/API → served artifact for Inflection; capture the actual response
3. ~15min: same trace for 49F; diff the two (key / filter / auth / artifact)
4. ~10min: classify + document root cause (AC1a) + resolve Q1 (AC1d)
5. fix + verify (sized after root cause) → RAVC2-Request (or COO-surface if a DS-emit follow-on is needed before fix)

## RAVC2 deliverable

`[RAVC2-Request] ADVI_INFMVP.F1 — Assets Overview root cause + fix` to ws COO. CC ws CTO. Body: root-cause statement (AC1a) + Q1 resolution (AC1d) + fix commit/diff + Peter non-zero verification (AC1b) + 49F-no-regression (AC1c). If the fix needs a DS emit, send an interim `[BLOCKED-ASK]`/COO-surface at the root-cause moment instead.

## Compiler tools mandate

- `comp-routes trace <fetch-fn>` for the CF→auth→S3 path; `comp-iam service <lambda>` if auth-gated.
- If a backend/Lambda change: CLAUDE.md Terraform-only deploy discipline (Rules 1-6).

## Cross-domain coordination

`<scoped/>` — Assets Overview surface. Pull 0.4.0_DE_ClientPlatform if the zero originates in the FE fetch/wiring (DE owns portal data-wiring). Coordinate with ws COO if a DS-emit follow-on is required.

## Notes

- Investigation-first is mandatory per Andrew + CTO — a blind patch on a scoping defect risks masking a real data-access boundary.
- DT vs DE split: PRD names "0.4.0_DT_ClientPlatform or a DE." Start the trace; if it's purely client-side fetch/wiring, hand the fix to DE and keep the permissions/scoping diagnosis with DT.

— ws COO /drive 2026-05-28T~19:46Z
