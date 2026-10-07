# Session -- 0.9.0_WK_IRPT_BCKEND~165 on IB-pr-356

Portal code: commit b3fedfea on portal branch wk-IRPT_BCKEND-165-portal (parent portal DEV b64805f7). Nothing pushed.

- investor-reporting.ts: route row and operation custody-report-read, getCustodyReport on LiveClient (own reader, outside parseIrEnvelope: row W165-S1) and FixtureAdapter (injected seam); optional on the interface so existing test doubles still type-check.
- manifest.ts: ReportKind custody-report, RenderBundle.custodyReport, assertSupported arm, templateFor narrowed to the two templated kinds.
- resolveBundle.ts: custody branch (cache, then fetch; MissingPayloadError on refusal or absence).
- PrintEntry.tsx: readReportKind maps custody-report, printReportRef reads ?report=, PrintDocument mounts ClientReportDocument.
- Tests: new ir-72-custody-print (11), ir-66 custody arm updated (4).
- Row W165-S2: the full bun suite rewrote 27 tracked wire files; restored from HEAD, none staged.
