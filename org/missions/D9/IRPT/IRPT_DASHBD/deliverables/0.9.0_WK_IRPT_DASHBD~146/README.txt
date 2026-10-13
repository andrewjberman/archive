DB-b-180 (worker 0.9.0_WK_IRPT_DASHBD~146) -- render the real sample locally

What it does
  render_sample.ts renders one filled report through the Performance tab component
  (PerformanceReport) and the export document component (PerformanceReportDocument), then
  prints the export HTML to PDF with headless Edge. Output is local only.

Run (bun; the harness finds the portal source from its own place in this worktree)
  cd <worktree>/portal
  bun <worktree>/org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~146/render_sample.ts <absolute path to report JSON> [output folder]

  The output folder defaults to the private folder (not in either repo). Writes
    FWD21_TAB_49F_SAMPLE.html
    FWD21_EXPORT_49F_SAMPLE.html
    FWD21_EXPORT_49F_SAMPLE.pdf
  and prints one JSON object of paths, byte counts, hashes and counts. No figure, name or
  account id is printed.

Behaviour
  - The report JSON goes to the components as it is. No adapter. A component error stops the
    run with exit 1 and the component's own message (HARNESS-ERROR line).
  - The logo is inlined as a data URI and the print stylesheet is inlined, so the HTML has no
    network or portal-asset reference.
  - The firm word in the page head is the neutral label "Sample Firm": the sample carries no
    firm name.
  - Components are read, never edited.

Status at the commit of this file
  - Control (synthetic fixture, made-up data, scratch only): exit 0; 117 data-member ids per
    HTML; no absent cell without its words; 15 PDF pages; headless Edge rc 0.
  - Real sample: exit 1 at buildReportModel (TypeError on account window_status). See the
    surprise rows IRPT_DASHBD-D2-W146-S1 to S3 in the investigation file of this project.
