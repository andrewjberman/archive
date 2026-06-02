# VERIFY-CHANNEL ADDENDUM — ADVI_INFPRM W4b/W4c P2 resolutions (both CLOSED)

- **Verifier:** 3.0.0_SA_CVO — independent re-confirm of RD~C's fixes to my two P2 findings
- **Timestamp:** 2026-06-02T20:20Z
- **Parents:** verify_channel_2009Z (W4b, P2-a) + verify_channel_2014Z (W4c, P2-b)
- **Method:** read the artifact (git diff + consumer code), not the tsc-green self-report.

## P2-a (W4b distribution single-layer guard) — RESOLVED, independently verified
RD~C `328a8459` added `&& isFirmAdmin` to the inflection **distribution** (`index.tsx:225`) and **advisors** branches, mirroring the books guard (`:254`). Confirmed against the diff:
- `{activeTab === 'distribution' && (` → `{activeTab === 'distribution' && isFirmAdmin && (`
- `{activeTab === 'advisors' && (` → `{activeTab === 'advisors' && isFirmAdmin && (`

**Strictly additive (no behavior change today):** non-admins were already unreachable (`tabs=[profile]`); admins have `isFirmAdmin=true` so the guard is transparent on the admin path (admin defaultTab=distribution still renders). All three admin-content branches (distribution / advisors / books) + profile (`!isFirmAdmin`) are now explicitly role-gated → the defense-in-depth asymmetry is closed; a future URL-restore/deep-link in `useTabNavigation` can no longer re-open the BI-leak. PASS.

## P2-b (W4c external 49F/demo graceful-empty) — RESOLVED, independently confirmed (no code change)
`DistributionTab.tsx:1977` `relationshipStackedPeriods = stackedPeriodsQuery.data?.book?.relationship_stacked_periods ?? null`. Every consumer guards on `&& length > 0`: `:2041`, `:2064`, `:2110` (`if (!… || length === 0) return null`), and the render `:2452` (`… && length > 0 ? <stacked> : <placeholder>`). So a Lambda book lacking the field → `null` → placeholder; a Lambda error (retry:false) → undefined → `null` → placeholder. **Never an error.** PASS.

**RD~C refinement (correct, narrows the surface):** 49F non-admins have NO Distribution tab (`tabs=[advisors, profile]`), so only 49F/demo **external admins** could newly fire the query — they degrade to the same placeholder, or render correctly if the Lambda carries `relationship_stacked_periods` (edge-gated, no leak). The changed-but-untested surface is therefore narrower (and safer) than my original P2-b framing.

## Net state
INFPRM access-model: W4a (edge) + W4b (+P2-a) + W4c (+P2-b) all PASS; both P2s CLOSED. The only remaining gate is the rendered-pixel **joint Andrew smoke** on a fresh Peter login (my honest-limit, not a code gate). **Recommend** folding a 49F/demo-external-admin Segment-drill spot into that smoke to empirically confirm the Lambda-has/lacks-field branch (no code risk — the guard is in place). CTO is convening the smoke.
