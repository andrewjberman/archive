# The resident package delta: IRPT_BCKEND's eight members, read by 2.0.0_SA_COO~P2 (2026-10-13)

Asked by `2.0.0_SA_COO~Y2` (msg 6753; `RESIDENT_PACKAGE_DELTA.json` under `IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~55/r19/`) and ruled by the CTO (ROUND-19 analysis of IRPT_ANLREQ ~Y, section 4 item 2): `~P2` reads IRPT_BCKEND's 8 members that differ between the live resident's pin `0485393f3a` and the release pin `069b8f797e`.
Method: for each member, `git diff -U0 0485393f3a 069b8f797e -- <source path>` and the commits that touch it in that range; the issuer read every changed line. **Claim class: MEASURED by this seat (diffs read), not exercised on the resident.** Each of the eight is the product of ONE IRPT_BCKEND build commit that was graded and drained in its own round; nothing else rides in any of them.

| member (source path at the pin) | the IRPT_BCKEND commit(s) | what the diff does | read |
|---|---|---|---|
| `reports/build_resident_package.py` (`infra/aws/lambda/investor-reporting/reports/`) | IB-pr-485 `3775a93368` | `DIRS` gains `ycharts/research` (2 lines: the docstring and the list) | the 12 new `ycharts/research` members ride the package; a queue-bound resident can import the packager |
| `reports/commentary_draft_store.py` | IB-pr-460 Part A `b7da10ca46` | the draft store's first-persist OK answer gains an OPTIONAL `ticket_id` (only when the accepted record carries a non-empty string); one read of the record, `_resolve_record` | additive answer member; `resolve_request` keeps its two-value return |
| `schemas/AnalysisSubmissionRequest.schema.json` (staged from `docs/contracts/investor-reporting/v1/`) | IB-pr-455 `74bbdbb322` | adds `commentary_requested`, an optional JSON boolean (4 lines) | additive; absent reads as before |
| `ycharts/generate/submission.py` | IB-pr-455 `74bbdbb322` | `commentary_requested` joins `PUBLIC_FIELDS`; a non-boolean value is refused `COMMENTARY_REQUESTED` | validates exactly what the schema now admits |
| `ycharts/generate/acceptance.py` | IB-pr-478 `06557b6618`, IB-pr-455 `74bbdbb322` | adds `get_commentary_ref` (reads the sibling `commentary_ref` attribute of the request item, one consistent GetItem) and copies `commentary_requested` into the record when the browser sent it | read-only accessor plus one additive record member |
| `ycharts/research/opal_packager.py` | IB-pr-478 `06557b6618` | reads `commentary_ref` through the port's sibling accessor when it has one, else from the record (a test fake) | PAIRED with `acceptance.py` above: both ride this release, so the live port carries the accessor the packager looks for; if only the packager moved, the `getattr` fallback reads the record as before |
| `ycharts/session/host_capture.py` | IB-pr-473 `bb1244d633` | the capture probe classifies a WAF challenge as the READ path does; step members are closed lists (action class, content-type class, a body marker NAME, a path NAME, two identity booleans), so no header, body text or URL rides; a token-less jar sends no pair and reads `discriminating` false | tightens what the probe may record; no new egress |
| `ycharts/extract/extract.py` | IB-pr-472 `c6c1bf218f` | `SECTION_BOUNDS` (True): a row's label is accepted only between its own section's heading and the next section's heading on the page; `extract(..., stats=None)` fills two counters and does not change the result's shape | **the one that can change a VALUE**: a label two census sections share ("Standard Deviation" under "Risk Info" and "Risk/Reward") now lands in its own section instead of both rows reading the first hit; this is the repair of row IRPT_BCKEND-D2-W324-S2, measured by its worker in round 165 on the synthetic and the specimen census; switching `SECTION_BOUNDS` off restores today's whole-page search |

## What this read does NOT cover

- The live host's installed files (the delta is of two locally built tarballs; the builder covers 182 of the live resident's 298 members, as `~Y2`'s record says).
- Whether `extract.py`'s bounded search moves any figure on a real vendor report the resident will see: it was measured on the specimens in round 165, not on live captures.
- `ycharts_session.js` (W328-S1) is not in either tarball (the host library); the CTO read it separately.
- The eight carry no change to a served route, an environment variable or a permission; `commentary_requested` stays unsent by the form (parked behind this release, PRD v0.4 item 5 of IRPT_ANLREQ).

-- 2.0.0_SA_COO~P2
