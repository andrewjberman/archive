# round34/walk -- gapread.mjs (DSGN_AMGTV1 round 34 gap read, issuer 2.0.0_SA_COO~D)

Built on `../../served-reread-20261002/servedread.mjs`: the same walker lease (arm HOLDER, secret, holder-only disarm in
`finally`), login, request guard (GET/HEAD/OPTIONS and login/refresh/logout only; telemetry answered locally) and output
folder (`read-<UTC stamp>/` beside the script). Not yet run against the live site.

## Run (repo root, against a local build of portal PROD dbd29c6320 on the live API)

    cd portal && bun run dev:live --port 5174      # in its own shell
    node org/missions/D13/DSGN/DSGN_AMGTV1/deliverables/2.0.0_SA_COO~D/round34/walk/gapread.mjs --no-officer "<TICKER>"
         [--base http://localhost:5174] [--names "BA US,VLO US,AMD US"] [--non-usd "ROG SW,1299 HK"]

`--no-officer` is required, and nothing is armed without it. `find_no_officer.py` (in this folder) lists the candidate names.

## Reads (one JSON each, plus PNGs; one `PASS|FAIL|ERROR <read> :: <evidence> :: <detail>` line each)

| read | outcomes | what it records |
|---|---|---|
| `fwd2-bubbles`, `fwd2-bars` | FWD-2 | servedread's identity hovers (3 bubbles at 30D, the 3 largest price moves) |
| `fwd21-labels-30D/90D/365D` | FWD-21 | every label ending in "..." hovered; its SVG `<title>` must hold the full served name |
| `fwd21-no-clear-tone` | FWD-21 | one drawn bubble with a null or absent served tone; the hover must say "no clear tone" |
| `fwd24-overlay-census <name>` | FWD-24 | "not served / not supplied / unavailable / not carried" strings in the header, each tied to an overlay field; 0 on carried fields; one lacking field shown as its designed empty state |
| `fwd24-control-any-name` | FWD-24 | at least one of the three names showed a positive control |
| `fwd5-timeline-hover` | FWD-5 | the 3 busiest days' bar tooltips on the first name with articles (hover only, never a click) |
| `tabs-dialog-closed <name>` | FWD-27 coverage | Escape until no `[role=dialog]` is visible, then each of the 5 tabs: full-page PNG and visible text |
| `nonusd-header` | FWD-4, FWD-13 | the first `--non-usd` name opening with non-USD key figures: tile label, value, as-of words, numerals |
| `no-officer-exec <ticker>` | FWD-7 | the Exec Management tab, its PNG and text, and the served management block |
| `fwd27-account-menu-escape` | FWD-27 | the account menu opens and Escape closes it (never "Log Out") |
| `display-names <name>` | FWD-27 | every visible string naming the security (Lead Panel at 30/90/365D, all price bars, every tab), grouped |

An ERROR line means the read could not run; its cause is the detail. Exit 0 only when no read is an ERROR, whatever the
grades say. The run stops after 50 minutes of the 60-minute lease, and the reads it did not reach are marked ERROR.
