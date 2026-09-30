# AMGT_CORPUS round 14 -- CRPS-p-4: the six render-owned fences re-measured on the deployed function

Worker 0.9.0_WK_AMGT_CORPUS~4, read 2026-09-29 20:50-21:00Z. Machine file: `FWD_EVIDENCE_ROUND14_SERVED.json`.

## Step 1 -- the ww-1 entry and the deployed function

- Governing entry: `amgt-resapp-ww1-redeploy-research-dossier-restart-20260929` -- CLOSED, "nothing stranded", closed
  20260929T195655Z, 4 of 4 legs (B0, T1, A1, V1). No ww1 file under `.open_deploys/` in the main tree or at HEAD.
- Earlier entry `amgt-resapp-ww1-redeploy-research-dossier-20260929` (20260929T1438Z): ABANDONED NOT-STARTED after the crash.
- Deployed `opal-amgt-scoped-api`: CodeSha256 `lg6NJ2JLYbTc9ZtlDaA9nckuNSOaZZmsYKzDjRPbB3s=`, LastModified
  2026-09-29T19:18:58Z, Successful (before ww-1: `CtIvirvM...EAOM=`).
- Because the entry is CLOSED, all six fences were measured.

## Step 2 -- what was measured

/thesis for IMB_LN_Equity, AZN_LN_Equity, AMD_US_Equity and ADBE_US_Equity, then all 93 readable dossier partitions of 95
(2 slash-safe partitions unreadable, row AMGT_CORPUS-Z-W4-S5). Each /thesis body was searched for the dossier's own text.

| fence | dossier holds | /thesis serves | portal DEV `ac8265668d` renders | state | owner |
|---|---|---|---|---|---|
| FWD-10 pillars | 157 pillars, 45 of 93 names | 0 of 157 | no pillar consumer | unmet | AMGT_RESAPP |
| FWD-11 management passage | 46 of 93 | 0 of 46 | none | unmet | AMGT_RESAPP |
| FWD-12 model rows + cases | rows 93 of 93; cases 33 of 93 | rows 0 of 93; cases 33 of 33 | Base only (ModelTab.tsx:310) | unmet | AMGT_RESAPP |
| FWD-15 fund / last position | fund 39, position 46 of 93 | 0 of 46 | none | unmet | AMGT_RESAPP |
| FWD-16 PDF-only pack | 33 PDF names hold pillars; 12 docx control | 0 | none | unmet | AMGT_RESAPP |
| FWD-18 terms and filter | 157 of 157 pillars carry terms | 0 of 157 | none | unmet | AMGT_RESAPP |

## Reading

ww-1 moved the function onto the canonical `research_dossier/` prefix and it reads the dossier, but its only dossier read is
`model.team_cases` (`lib/research/api/scoped_amgt.py` ~3105-3132): the team's three cases are served and match the dossier exactly
(33 of 33 per case). Pillars, the management passage, fund of record, last stated position, model rows and terms are not on the
route, and the portal has no consumer for them. The corpus half of each fence is unchanged and holds; the unmet part is the
served plane and the render. Every exercising act is an AMGT_RESAPP cell that adds a dossier passthrough to /thesis and renders
it; `python .scratch/p4/sweep.py` re-measures on demand.
