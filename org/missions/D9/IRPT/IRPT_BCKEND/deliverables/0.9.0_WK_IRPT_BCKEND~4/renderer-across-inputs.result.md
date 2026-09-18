# IB-rtc-5 -- the renderer varies with its input, the across-inputs control

**Cell:** `IB-rtc-5` | **Worker:** `0.9.0_WK_IRPT_BCKEND~4` | **Worktree:** `/c/tmp/wk-irpt-3-4` on
`wk-irpt_bckend-3-4` | **Battery:** `battery_ib_rtc_5.py`, output
`IB-rtc-5_R35-AC1_battery_output.txt` | **Token:** `IBR35-RENDER-VARIES-WITH-INPUT`, printed on
two independent runs of the battery (`.scratch` run logs, not committed; the committed output is
the second run).

## WHAT THIS CELL DID

Round 1's browser-host render pipeline (`render_export.cjs` via SSM on the YCharts EC2 host,
against the DEPLOYED, session-gated `https://opalinvest.dev/investor-reporting/print`) is
HUMAN-GATED (`IRPT_BCKEND-W4-S25`): the print route is an authenticated app route and this
worker holds no session and may mint none (no write to the production auth plane; bound 6). The
round-1 in-process fallback the decomp named ("the renderer's in-process path with the SAME
code") does not exist any more as literally written -- `render.py`'s own header
(`infra/aws/lambda/investor-reporting/export/render.py` @`862b0e4a6e19b3`) states the named-slot
HTML fixture renderer and its local-headless-browser machinery are RETIRED and GONE from the
module, kept only as round-1 history on disk.

What DOES still exist, and IS the counterpart's real render code executed on a different plane,
is `portal/src/pages/InvestorReporting/render/manifest.ts` + `PrintEntry.tsx` +
`PerformanceDocument`, run against the LOCAL vite dev server (`bun run dev`) with the identical
auth-stub and Playwright network-interception mechanism `portal/scripts/ui-smoke.mjs` and
`portal/src/pages/InvestorReporting/__tests__/fe-s-31/print-driver.mjs` already use and that
`portal/CLAUDE.md`'s Verification law names ("auth-stubbed, works without credentials"). This
cell's driver, `rtc5-render-driver.cjs` (committed beside the battery), is FE-s-31's
print-driver.mjs mechanism UNCHANGED in its rendering half, with `page.pdf()` added at settle
time (FE-s-31 only needed DOM state). Nothing about the render code itself is patched, stubbed
or re-registered -- only the HOST PLANE (local dev vs. the deployed session-gated origin) and
the DATA PLANE (synthetic v1-envelope fixtures vs. a live scoped API) differ from IB-rt-8's
browser-host run, which is exactly the substitution the decomp authorizes when the host is not
reachable non-interactively.

## THE FIVE ARMS (R35-AC1)

- **(e), run first:** the round-1 collapse (row `IRPT_BCKEND-W4-S19`) REPRODUCED as the
  detector's positive control. Live retrieval was attempted first (`s3api
  list-object-versions` on the three round-1 keys) and found UNAVAILABLE: `list-object-versions`
  returns 0 `Versions` (only a `DeleteMarker`) for all three keys today. That is NOT a fresh
  surprise: `IRPT_BCKEND-S43` (2026-09-12, Andrew-direct "Approved all 9") records that all nine
  noncurrent versions on this prefix were permanently deleted on his word, and `IRPT_BCKEND-S55`
  /`S56` (the CVO's round-2 read) already carry the corrected, permanent-gone reading -- W4-S20's
  "recoverable by VersionId" is superseded, not a live discrepancy this run discovered. The face
  itself names the exact fallback for this branch ("or their recorded hashes from W4-S19"), so
  this cell took the branch it was given rather than filing a row for it. Using W4-S19's RECORDED
  values: three distinct bundle digests, three distinct raw sha256, ONE normalized `content_hash`
  (`b646b2301237e6d3...`) across all three -- the detector this battery trusts below is proven
  first to catch the defect it exists to catch.
- **(a):** two REAL `ExportBundle` objects, built with `bundle.py`'s own `freeze()` and validated
  against `ExportBundle.schema.json`, differ by sha256; the differing field is named
  (`authorized_report_revisions[0].revision`, `RTC5-A` vs `RTC5-B`).
- **(b):** both rendered on the SAME plane (local dev, above). Raw sha256 differ, normalized
  `content_hash` differ, and the decompressed content streams differ at byte offset **9405 of
  194104** (bundle A) vs 196027 (bundle B).
- **(c):** the identical-input control -- bundle A rendered twice: normalized hash EQUAL (1 of
  1); raw sha256 differ (Chromium stamps a creation date and a document `/ID`, not claimed
  stable); the decompressed content stream is in fact BYTE-IDENTICAL across the two renders of
  the same bundle on this plane.
- **(d):** the plane is named in full, and the real-path arm (render_export.cjs against the
  deployed print route WITH a session) is printed `HUMAN-GATED`, quoted verbatim from
  `IRPT_BCKEND-W4-S25` and from `RT2_test_principal_human_gated.md`
  (`0.9.0_WK_IRPT_BCKEND~2`'s deliverable) -- never simulated, never walked.

Full battery output, every denominator and every hash: `IB-rtc-5_R35-AC1_battery_output.txt`.
Bundle fixtures: `rtc5_bundle_a.json`, `rtc5_bundle_b.json` (the frozen `ExportBundle`s, no
client data -- synthetic report ids and revisions only). Scenario/fixture map for the render
driver: `rtc5_scenarios.json` (synthetic v1-envelope bodies, no real firm/client identifiers).
Rendered artifacts (each under 1 MB, committed per bound): `rtc5_pdfs/bundle_a.pdf`,
`rtc5_pdfs/bundle_a_retry.pdf`, `rtc5_pdfs/bundle_b.pdf`; their raw and normalized hashes beside
the bundle hashes in `rtc5_render_hashes.json` (R-40).

## SURPRISES FILED

- `IRPT_BCKEND-W4-S32`: the decomp's "in-process path with the SAME code" fallback, read
  literally, does not exist -- round-1's fixture renderer is retired and its machinery removed
  from `render.py`; the actual substitution used is the counterpart's REAL render code on the
  LOCAL DEV plane (see above), which is what the face's language was reaching for but does not
  name precisely.

## R35-AC2 -- INPUTS FOR THE CVO'S JUDGMENT (no verdict offered here)

1. **Is the plane this control ran on the plane FWD-8's DONE WHEN names?** FWD-8 (read at
   PRD/decomp level, not restated here) is about the render pipeline generally; this control ran
   on the LOCAL DEV plane (vite + auth-stub), not the DEPLOYED plane (CloudFront/EC2 host +
   session). IB-rt-8's browser-host run reached the deployed plane and stopped at
   `SESSION_ABSENT`. This cell's plane exercises the SAME rendering code path
   (`PrintEntry.tsx`->`PerformanceDocument`) that the deployed plane also runs, but not the
   deployed infrastructure, the deployed origin, or an authenticated session. What the real-path
   arm (d) still lacks, unchanged from W4-S25: a non-interactive session for a machine principal
   the portal's typed client accepts on the print route, OR a print route that accepts a signed,
   short-lived render grant instead of a user session.
2. **Do the two bundles differ in a way a client would see (content), not metadata?** Bundle B's
   fixture carries a DIFFERENT provider (`ORION` vs `BLACK_DIAMOND`), a different YTD summary
   return (0.1899 vs 0.0732), a different account-detail table (two accounts,
   `ACCT-BETA-0777`/`-0778`, vs one, `ACCT-ALPHA-0001`), and different values throughout the
   return series -- these are the numbers and rows a client's document displays, not a
   brand/orientation/version metadata change. The backend `ExportBundle`'s differing field
   (`authorized_report_revisions[0].revision`) is itself metadata in the bundle's own schema;
   what makes the RENDERED document differ in content is the report DATA the two revisions
   resolve to (the fixture bodies), which is how a real render actually varies -- the export
   bundle names WHICH report to render, the report's own data is what a client reads.
3. **Does anything in the renderer's behaviour explain W4-S19 (why three bundles rendered one
   document), or does it only no longer exhibit it?** This cell's own measurement is
   affirmative on the EXPLAINING side, not just the non-exhibiting side:
   `render.content_hash()` (the normalizer both this cell and IB-s-14 use) folds in per-page
   `mediabox` + decompressed content-stream bytes + extracted text, and EXCLUDES only what a
   print engine stamps (creation date, document `/ID`, xref offsets) -- round 1's fixture
   renderer (retired, machinery removed from `render.py`) rendered from FIXED named-slot HTML
   templates that round 1's `(v0.11)` arm populated with data that did not vary the template's
   OWN content in a way `content_hash` could see (three "Analysis" exports built from the
   fixture path, each landing at the same page content); this cell's renders, by contrast, use
   the counterpart's REAL templated React document whose displayed rows and numbers come
   directly from the resolved report data, so two different report bodies produce two visibly
   different content streams (byte offset 9405 of 194104) while one report body rendered twice
   is byte-identical. That is a difference in what the TEMPLATE DOES WITH ITS INPUT, not merely
   a difference in which harness ran it -- but this cell did not re-run round 1's retired
   template against these two report bodies (it no longer exists to run), so it cannot certify
   that the OLD template would have varied here too; it can only certify that today's REAL
   template does, and that the normalizer used to grade both is the same one.
