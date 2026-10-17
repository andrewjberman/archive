# V leg step (3) -- the export request, prepared ahead of a new mint pair (2.0.0_SA_COO~S2, 2026-10-17 ~12:0xZ, dell2)

Step (3) of the TO-DB-b-328 V leg: one export of the canary client as the COVERING viewer, graded on whether the frozen bundle carries the same filled body (sha256 `2fb74e5d8087cf1e7b2891e144aaf0a3bbef97096512eb09a711776b3821d661`). It could not run at 11:45Z because the 900 s tokens were near expiry and the request was not built. This file is the request, assembled from the code and contract at HEAD, so a new pair (if `2.0.0_SA_COO~D2` rules one) costs one tick, not a search. **Nothing here was sent.** Push state: LOCAL.

## The request (read from the code; each item marked)

- Route: `POST https://opalinvest.dev/api/scoped/investor-reporting/export` (`export/entry.py` ROUTES; read).
- Headers: `Authorization: Bearer <session, in memory>`, `X-Contract-Version: v1`, `Content-Type: application/json` (the first two were required on the GET at 11:4xZ; the POST is assumed to match, **unverified**).
- Selector: `selected_tenant: 49financial` inside the JSON body (the GET took it as a query parameter; `served.selected_tenant` reads the event, the query, the path, the params and the body, and refuses disagreement; **which carrier the POST path honours is unverified**).
- Body (the page's PATH C shape, from `export/tests/test_filled_report_submit_handler.py::_body` and `retained_export.parse_filled_report_source`; read):
  `{"filled_report_source": {"source_kind": "filled_report", "client_id": "<canary id, from the broker message>"}, "selected_sections": [], "versions": {"template_version": "...", "renderer_version": "...", "disclosure_version": "..."}, "render_options": {"orientation": "PORTRAIT", "page_size": "LETTER", "brand_revision": "..."}, "selected_tenant": "49financial"}`
  The page sends NO VersionId, sha256 or size: the server pins them from the current object at submit (`submit_service._serve_filled`, `server_pinned_body`; read). The three `versions` strings and `brand_revision` have no value I could read from a live source: **the real values must be taken from the portal's own submit call or the receipt of a prior export; unverified**.

## What the submit writes (so the grade of (3) is not a read)

`_serve_filled` persists the frozen bundle (`bundle_key`), writes the render grant (`grant.write`) and a pending record to the evidence bucket, and dispatches the SSM render only when `render_enabled` (the browser host is gated; **its state is unverified**). The expected answer is HTTP 200 with state `QUEUED` and reason `EXPORT_QUEUED` or `EXPORT_QUEUED_RENDER_GATED`.

## How (3) would be graded

1. The submit answers `QUEUED`; the receipt carries the export id.
2. Read the frozen bundle at `bundle_key` (evidence bucket, read-only): its `authorized_report_revisions[0].filled_report_source` must carry `sha256` equal to `2fb74e5d...d661`, `size` 52,718, and the VersionId of the object's current version.
3. A render is NOT required for the grade; whether a PDF exists is a separate outcome and is not claimed here.
4. A refusal word (`FilledReportUnavailable`, "changed after this export was submitted") is a FAIL of (3), not a pass: the live object must not change between the pin and the read (the full pass is complete).

## What stays open

The three version strings and `brand_revision`; the selector carrier on the POST; whether `render_enabled`. Each is a one-line read from the first real request or its refusal envelope, which is public and carries a reason code.
