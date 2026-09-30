# AMGT_CORPUS round 20 -- CRPS-v-2: six render-owned outcomes, SERVED census and PAGE walk

Worker 0.9.0_WK_AMGT_CORPUS~2, served census 2026-09-30T03:20Z, walk stamp `20260930T032251Z`. Machine file:
`FWD_EVIDENCE_ROUND20.json`. The walk's screenshots are local (`tmp/ui-walk/` in the main tree, gitignored) and are quoted here in words only.

## Instruments

- Deployed `opal-amgt-scoped-api`, CodeSha256 `pVa+sgzj8XNZ9uvJqCOwRNCJn0IZhUklnWZh6JbO7B0=` (round 14 read `lg6NJ2JLYbTc9ZtlDaA9nckuNSOaZZmsYKzDjRPbB3s=`,
  so the function was redeployed since; that is why the served counts below are no longer 0).
- Population: the 96 `security_key`s of `MODEL_BLOCK_CENSUS_ROUND17.json`. 96 of 96 /thesis calls returned 200 (including the two slash keys
  `BP/_LN_Equity` and `NG/_LN_Equity`); none was refused. Read-only `lambda:Invoke` via `capture_lib._invoke`.
- Fields read: `dossier_fields.thesis_pillars` (+ `.terms`, `.citation`), `dossier_fields.management`, `dossier_fields.fund_of_record`,
  `dossier_fields.last_stated_position`, `model.team_cases`, `posture.marked`. A "carrying" name has the element SERVED with a citation
  (report_key, locator, passage).
- Portal: working copy of `portal/` branch DEV at `29c8226a6b0aca46204aea3637d1df92ba940684`, walked on `http://localhost:5174` (200 at the start).
- Signed-out control: `--no-login --route /security-analysis` exited 3, `WALK VOID: step /security-analysis-load landed on the sign-in page`.
- Signed-in walk: IMB LN, AMD US, AZN LN, ADBE US; 127 screenshots, 0 guard aborts. Disarm read `HTTP 401 ... -> REFUSED`; the account status after the
  walk is `status=disabled ... armed=no; SSM ABSENT`.

## The six rows

| outcome | SERVED (n of 96) | PAGE (security, tab) | page state | owner |
|---|---|---|---|---|
| FWD-10 pillars | 46 carry cited pillars | IMB LN Thesis | unmet | DSGN_AMGTV1 |
| FWD-11 management | 47 carry a cited passage | IMB LN Exec Management | unmet | DSGN_AMGTV1 |
| FWD-12 team cases | 34 all-three SERVED and cited | AZN LN Model | unmet | DSGN_AMGTV1 |
| FWD-15 fund + position | 40 carry both, cited (fund 40, position 47) | IMB LN Posture and header line | unmet | DSGN_AMGTV1 |
| FWD-16 PDF-only names | 25 of 25 carry pillars, management and cases | ADBE US Thesis, Exec Management, Model | unmet | DSGN_AMGTV1 |
| FWD-18 terms | 46 carry terms on every pillar | IMB LN Thesis and header feed | unmet | DSGN_AMGTV1 |

Every served half reads met: the served counts are non-zero, and every non-carrying name reads ABSENT with a reason, except 6501_JP_Equity (one name with no
dossier at all; row `AMGT_CORPUS-Z-W2-S15`). FWD-12 census: 34 names all three cases SERVED, 62 all three ABSENT with a reason, 0 mixed.

## What the page shows (words)

- FWD-10, IMB LN Thesis: the THESIS panel body is one line, "No drafted prose for this name yet." No pillars, bold leads, open-to-report control or
  team marking. AMD US reads the same line (the ABSENT arm shows no reason).
- FWD-11, IMB LN Exec Management: "No officer list is in this name's pack yet: the company's 10-K had no officer section ...". The team's
  management passage does not appear, so nothing sits beside the roster.
- FWD-12, AZN LN Model: the team's Base case renders in a box titled "THE RESEARCH TEAM'S BASE CASE" with EPS, Multiple, Price and Return for 2026E-2030E
  and a source line naming the AstraZeneca pack. Upside and Downside read "not in the pack yet -- the method is to be agreed" though the served payload
  carries both as SERVED and cited for AZN. IMB LN (ABSENT arm) reads "The research team's Base case is not in this pack. The research team fills it in."
- FWD-15, IMB LN: the header posture line and the Posture tab show only the machine "NO CALL". Fund IDVZ and "Potential ADD in IDVZ (currently ~2.5%)" appear
  nowhere. The byte-unchanged-verdict clause is not exercised (no team posture renders to compare).
- FWD-16, ADBE US: Thesis "No drafted prose", Exec Management "No officer list is in this name's pack yet", Model shows only the team Base case (cited to the
  ADBE pack). The docx control IMB LN renders no pillars or management either.
- FWD-18, IMB LN: no pillars, so no terms; the header feed reads "no committed chatter ranking for today" and "No publisher item in the pool"; no filter control.

## Cause read

The portal working copy has no consumer of `dossier_fields`: `git grep -E 'dossier_fields|thesis_pillars|fund_of_record|last_stated_position' -- src` returns
0 files (positive control: `team_cases` hits ThesisCards.tsx, ModelTab.tsx, types.ts). The Model tab renders `team_cases.base` only.

## Limits stated

- FWD-16 "PDF-only" is a proxy (every report_key in the served citations ends `.pdf`): the payload carries no pack-shape field, so a PDF pack that failed to
  extract cannot be selected. 25 of 25 is therefore a floor on the shape. Control: 47 names carry a `.docx` key, 24 carry no citation.
- FWD-12 rows-from-typecast-and-template is read on the page only.
- The walk is a page read, not acceptance evidence by itself; the CTO grades the page half from it.
