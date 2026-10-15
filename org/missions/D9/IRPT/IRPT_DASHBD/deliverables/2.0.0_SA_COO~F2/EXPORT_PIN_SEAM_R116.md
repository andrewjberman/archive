# The filled-report export pin: the browser cannot supply what the freeze requires (2026-10-15 ~05:4xZ)

Issuer `2.0.0_SA_COO~F2`. Facts read from the merged tree at `HEAD` (the files and functions named, read at that commit), not from a status line.

## What the signed pair says and what the build requires

- The signed packet (`org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~395/SERVE_PATH_PAIR_PACKET_V1.md`, hop 4): the filled object "is frozen with its VersionId and
  sha256, as PATH B freezes the platinum series". PATH B: the page sends `performance_source` `{path, account_id, start, end}` and NEVER a VersionId, sha256 or as_of; the server pins them
  at submit (`portal .../export/submit.ts`, `PerformanceSource`).
- The merged hop-4 build (IB-pr-555, `6ae988c274`): `infra/aws/lambda/investor-reporting/export/retained_export.py` `parse_filled_report_source` refuses a request body whose
  `filled_report_source` lacks `client_id`, `version_id`, `sha256` or `size` ("a pin without its VersionId is refused, never defaulted"); `freeze_filled_report` then reads the object at that
  VersionId and checks the bytes against the pin. `bundle.py` `validate_filled_report_pin` requires `source_kind`, `client_id`, `key`, `version_id`, `sha256`, `size` on a revision's
  `filled_report_source`. So the CLIENT must supply the pin.
- The route's design (IB-pr-554, hop 3): "reads the one filled-report object at the hop-2 address and returns its bytes unchanged". Nothing in the packet, the design record or the order says
  the route returns the object's VersionId, sha256 or size, and the page's reader (`dashboard/report/reportRead.ts`) reads the body only.

## The gap

The page has no way to learn the VersionId of the report it shows, so it cannot build the pin the freeze demands. The two documents disagree: the packet says PATH B's server-side pin, the build
demands a client-supplied pin. The portal's proposed source (`export/filledReportSource.ts`: `performance_source: {path: 'FILLED_REPORT', client_id}`) matches the packet; it does not match the
build in two ways: the field is `filled_report_source` on a revision item (the new ExportBundle contract branch, IB-pr-557), and it carries the pin.

Not yet wired: at `HEAD` the only callers of `freeze_filled_report` are its own tests (`export/tests/test_filled_report_source.py`, which feed it a body holding a full pin); no submit handler
calls it. So the request shape is still the owners' to choose, and the decision costs them nothing yet.

## Options for the owners (hop 3 and hop 4: `2.0.0_SA_COO~P2`; the signature: the CTO)

- (a) **Server pins at submit, as PATH B and the packet say.** `freeze_filled_report` accepts `{client_id}` (the page names only the client) and reads the CURRENT object's VersionId, sha256 and size
  itself. The portal sends the client only. No route change. The page exports the object as it is at submit, the way a dashboard export takes the series as it is at submit.
- (b) **The browser pins what it displayed.** The route returns the object's VersionId (a response header) and the page computes the sha256 and byte count of the exact bytes it read and sends the
  full pin. The export then renders exactly what the advisor saw. More portal code (raw bytes, a digest) and a route change.

## Issuer's recommendation

(a): it is what the signed packet says, it keeps the portal's source one field (the page never holds a hash it could get wrong), and it needs no route change. The build (IB-pr-555) is the part that
departs from the packet, so it is the part to change. After the ruling the portal follows by an issuer amendment to `export/filledReportSource.ts` and `submit.ts` (the wire location and names); no new round.

-- 2.0.0_SA_COO~F2
