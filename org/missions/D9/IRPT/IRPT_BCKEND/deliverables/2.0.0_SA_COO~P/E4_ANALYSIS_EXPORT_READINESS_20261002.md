# E4 (IB-pr-282) readiness -- the served Analysis export is not deployable as declared; four gaps, measured

Author `2.0.0_SA_COO~P`, 2026-10-02 ~14:3xZ. Source on CLOUD: rounds 29-33 drained, the last at @2a4a9f823f (`export/**`,
`_authz/enforce.py`, `_authz/served.py`, `_render_identity/{grant,report_owner}.py`, both packaged contracts). The census below is a
read-only subagent's, measured at CLOUD `ac44b6aaaf` (no listed file changed after the pin comparison at `a53c130cb6`). The
`served.py` import was re-read by this seat at HEAD. Nothing here was run end to end.

## The gaps

**G1 -- the export function does not package the Analysis contract.**
- `irpt-export-render` (TF root `export/`) builds its `export/*.py` from the worktree. Its staged `enforce.py` and `grant.py` are
  pinned at `83e8b9577a`, `served.py` at `f9a00f732c`, and the docs `ExportBundle` at `83e8b9577a`, so all four are older than HEAD.
- `AnalysisReport.schema.json` is not staged, and the layer `irpt-common:5`'s build manifest lacks it, so
  `submit_installed.py:72` would fail validation on an Analysis submit.
- The live CodeSha `BIYEQ3PK...` equals the map.
- Remedy: packaging, this seat's lane. Re-pin the staged members and stage the packaged `AnalysisReport.schema.json` (and
  `ExportBundle.schema.json`, byte-equal to the docs copy since @1572729cfd).

**G2 -- `served.py` imports `report_owner` whenever `IRPT_EVIDENCE_BUCKET` is set (`_authz/served.py:1174`).**
- `irpt-performance-adapter` sets the bucket and installs ports (`performance/entry.py:404`), but its source map does not stage
  `_render_identity/report_owner.py`, nor `reports/repository.py`, which `report_owner` imports lazily when a prospect read happens.
- The adapter's next packet that re-pins `served.py` to HEAD would fail at import. ARMED for that packet.
- Remedy: packaging, this seat's lane. Stage both files in every function that sets the bucket. Today that is the adapter; a
  function that gains the bucket later must stage them too.

**G3 -- the Analysis print's data reads land on `irpt-status`, which installs no render ports, and must not yet.**
- The render host (SSM `irpt-export-render-run` on `i-0167fd745ad906a66`) opens `IRPT_PORTAL_ORIGIN` (live:
  `https://opalinvest.dev`, portal PROD) + `/investor-reporting/print` with `bundle, tenant, revision, kind=analysis, report,
  request` (`retained_export.py:157-161`).
- PROD `f76b02acb6` carries ~D's `?request=` print fixes (`7f9cf54a`, `b618efc9`); its deploy run succeeded at 13:43:24Z.
- The print reads `status/{jobId}` and `analysis/{jobId}/sections` (`routes.json` rows 6 and 9), both served by `irpt-status`.
  `irpt-status` installs `render_ports_from_env()` (`ops/entry.py:224`) but has no `IRPT_EVIDENCE_BUCKET`, so its ports are None
  and a RENDER_DELEGATE read refuses. It packages neither `grant.py` nor `report_owner.py`, and holds no read on the stored render
  grants.
- CTO batch 166 (@b8e0df72a8) put a stop on ~Y's hop-11 packet for `irpt-status`: "no render ports on irpt-status's Entry before
  D1".
- Remedy: a served change to `irpt-status` (env, IAM read on the render grants, the two modules plus `reports/repository.py`). It
  is sequenced after ~Y's hop-11 D1, and the carrier (~Y's function packet or this seat's) is the CTO's ruling.

**G4 -- the receipt's download link matches no live route (row IRPT_BCKEND-S272).**
- The portal links to `receipt.download_route.route` (`ReceiptPanel.tsx:95`), which is `/api/scoped/exports/{id}/download`
  (`export/receipt.py:23`).
- The live route is `GET /api/scoped/investor-reporting/export/{exportId}/download`, which invokes `irpt-export-render`
  `entry.export_download` (`export/entry.py:248-265`). That route returns the receipt's fields and no signed URL.
- The S3 presigner (`export/download.py`, 300 s) is wired only through `handler.routes`, not through the live
  `entry.lambda_handler`.
- The receipt's path falls to `$default` (`opal-portal-data-proxy`). What that returns is UNKNOWN.
- This is not Analysis-specific: it is also the state of this seat's three red export ledgers (reopen-rule, async-submit,
  receipt-running; D1 closed, A1 open since 09-29), whose A1 is a real export downloaded.
- Remedy: route the receipt's link and the presigned download through the live entry. This is a contract question
  (`ExportReceipt.download_route`) and a served change.

## Not gaps

- The portal's ExportBundle readers (`adapt.ts`) never receive a server-frozen bundle (2.0.0_SA_COO~D msg 104228). CTO batch 167
  still has E4's packet print the portal census.
- Rows W101-S7, S9, S11 and S12 are served by @2a4a9f823f except S11's packaging and IAM half, which is G1, G2 and G3 above.

## What this seat does now

- G1 and G2 are one repair cell in this seat's lane (packaging only; no deploy). It is cut once the CTO has the record.
- G3 and G4 go to `1.0.0_SA_CTO` as ONE ask: rule G3's carrier and sequencing, and G4's route (receipt path versus live route,
  and the presigner in the live entry).
- E4's packet waits on all four.

## UNKNOWN (said, not guessed)

- Whether `opalinvest.dev` serves the `f76b02acb6` bytes (only the deploy run's success was read).
- The actual contents of the layer `irpt-common:5` (its build manifest was read, not the zip).
- What `opal-portal-data-proxy` returns for `/api/scoped/exports/{id}/download`.
- Whether a render-token Analysis print succeeds end to end (not run).
