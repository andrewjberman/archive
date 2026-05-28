# ADVI_INFMVP.F2 — Remove Trade Submission / Tools from Inflection sidebar (RD)

**Project:** [ADVI_INFMVP](../../../projects/ADVI_INFMVP.json)
**PRD:** `docs/architecture/ADVI_INFMVP.md` v0.1 §3 F2 (commit 5f6018778)
**Pod:** 0.4.2_RD_AdvisorIntelligence
**Lane:** RD_AdvisorIntelligence (portal FE)
**Issued to:** 0.4.2_RD_AdvisorIntelligence
**Author:** 2.0.0_SA_COO 2026-05-28T~19:46Z (/drive — CTO NOVEL_PRD_READY handoff 19:45Z)
**Sizing:** ~15-25min wall (one-line allowlist edit + Peter/49F sidebar verify)
**Authority anchor:** CTO PRD v0.1 5f6018778 + Andrew direct 2026-05-28 ("Inflection users should have no Tools pages at this time")

<status>complete</status>

## Objective

Inflection users must see **no Tools section** in the sidebar (Trade Submission is the only Tools item currently in their allowlist). The sidebar already auto-hides any nav section with zero visible items (`portal/src/App.tsx:288-309`, filtered by `isPathAllowedForFirm`), and `isPathAllowedForFirm` also gates the route. So removing `/trade-submission` from the `inflection` allowlist both drops the sidebar item AND redirects the route.

## The change (verified)

`portal/src/lib/firmAccess.ts:39` — remove the `'/trade-submission'` entry from the `'inflection'` Set. The inflection set does NOT contain `/security-scanner` or `/portfolio-management`, so after this removal the Tools section has zero visible items and disappears entirely. **No nav-config change. No deletion of the Trade Submission feature** — it remains for `49financial` / `cottonwood` / `demo` / internal firms whose allowlists are untouched.

## Acceptance criteria

- **AC2a.** Logged in as `peter@inflectionwealth.com`: no "Tools" section header, no Trade Submission link in sidebar.
- **AC2b.** Direct-navigating to `/trade-submission` as an Inflection user redirects to `/market`.
- **AC2c.** `49financial` sidebar UNCHANGED — still shows Trade Submission (regression check; verify the other firms' allowlists were not touched).
- **AC2d.** Portal runs on DEV (Rule 19: main tree stays on DEV); `bun run dev` predev check clean. No PROD promotion in this TO.

## Dependencies

- None. Independent + can land immediately (PRD §4: "F2 is independent, small, FE-only — can land immediately").

## Sequencing

1. ~3min: confirm `firmAccess.ts:31-40` inflection set + read `App.tsx:288-309` auto-hide filter
2. ~3min: remove the `/trade-submission` line
3. ~10min: `bun run dev --port 5175`, log in as Peter (verify no Tools), check 49F unchanged, direct-nav `/trade-submission` redirect
4. ~5min: commit (portal DEV) + RAVC2-Request

## RAVC2 deliverable

`[RAVC2-Request] ADVI_INFMVP.F2 — Inflection sidebar Tools strip` to ws COO. CC ws CTO. Body: commit hash + the one-line diff + AC2a-c verification evidence (Peter sidebar screenshot/observation + 49F-unchanged confirmation + redirect confirmation).

## Cross-domain coordination

`<minimal/>` — portal FE-only, single firm-allowlist line. **MDPF_SCOPED overlap note:** Andrew is authoring a sibling whole-Portal scoping PRD (MDPF_SCOPED) that may also touch firm allowlists; this F2 change is Inflection-only and narrow — flag ws COO if MDPF_SCOPED lands mid-flight so we de-conflict the allowlist surface.

## Notes

- Per Rule 19: portal main worktree stays on DEV; if you find it on PROD, `cd portal && git checkout DEV` first.
- This is the cleanest immediate win in the INFMVP set — land it first.

— ws COO /drive 2026-05-28T~19:46Z
