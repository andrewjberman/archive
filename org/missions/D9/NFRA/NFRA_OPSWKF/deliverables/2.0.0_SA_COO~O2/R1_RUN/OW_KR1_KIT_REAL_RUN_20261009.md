# NFRA_OPSWKF OW-k-r-1 -- the starter kit's real run, 2026-10-09 ~07:0xZ (2.0.0_SA_COO~O2)

| Step | Act | Read |
|---|---|---|
| 1 | `git archive` of `HEAD:tools/ops_kit` -> `opal_ops_kit.zip`, unzipped into an EMPTY scratch folder (outside the repo) | 9 files, no `__pycache__` |
| 2 | One command: `python serve.py --selftest` | `PANEL trade_rec rows=12 source=fixture`, `PANEL billing rows=12 source=fixture` |
| 3 | One command: `python serve.py --port 8777`; page loaded in a headless browser | HTTP 200; `ops_kit_fixture_run.png`: Opal band, light canvas, two white hairline panels, `source: fixture` stamped on each |
| 4 | A FRESH Claude session, given only the unzipped folder and the request "put Billing above Trade reconciliation; add fees by status under the total" | It changed `static/index.html`, `app.js` and `theme.css` only. Selftest still printed both PANEL lines. Its verdict on the guide: "short, says which files to edit and which not to touch" |
| 5 | Re-loaded the page | `ops_kit_after_claude_edit.png`: Billing first; `PAID $15,406.25 / INVOICED $14,156.25 / DRAFT $12,375.00` sums to the $41,937.50 total |
| 6 | Opal's tree after the edit | `git status --short tools/ops_kit` = 0 lines; `diff -rq` against the shipped zip = the 3 `static/` files only |

**FWD-7 status:** the build is EXERCISED on fixtures. Two clauses remain open:
- "live data through its one adapter" waits on X2: NFRA_MCPINDEX readers, owner `2.0.0_SA_COO~MI`, target 2026-10-12.
- Delivery to his SharePoint is not done. The gateway's site upload takes text only and no folder is named; this is an ask of
  Andrew.
- The organic arm, the operations lead's own Claude changing his own copy, is recorded, never waited on.
