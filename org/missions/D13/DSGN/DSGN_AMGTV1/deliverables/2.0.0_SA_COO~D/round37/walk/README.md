# round37/walk -- reads37.mjs (DSGN_AMGTV1 round 37 issuer walk, issuer 2.0.0_SA_COO~D)

The reads of FWD-5, FWD-11 and FWD-19 that rounds 34-36 never reached (`../../round36/COMPLETION_GRADES.round36.json`,
all three NOT_EVALUATED). The script copies `../../round35/walk/closewalk35.mjs`; it does not import it. It keeps that
script's walker lease (arm HOLDER, secret by name, holder-only disarm in `finally`, and the login-REFUSED line after disarm,
now parsed and printed as `LEASE: login after disarm REFUSED|NOT REFUSED|UNREAD`). It also keeps the login, the request
guard (GET/HEAD/OPTIONS and login/refresh/logout only; telemetry answered locally; refusals are now also listed), the
output folder (`read-<UTC stamp>/` beside the script), the per-read record/ERROR discipline and the 50-minute lease
budget. The script has NOT been run against the live site. Arming the walker lease is the issuer's act.

## Run (repo root, against a local build of portal DEV on the live API)

    cd <tree>/portal && bun run dev:live --port 5174          # in its own shell
    node org/missions/D13/DSGN/DSGN_AMGTV1/deliverables/2.0.0_SA_COO~D/round37/walk/reads37.mjs --names "BA US,AMD US" --base http://localhost:5174

`--names` defaults to `BA US,AMD US` and `--base` defaults to `http://localhost:5174`. The script prints one line per read,
`PASS|FAIL|ERROR <read> :: <evidence path> :: <detail>`, then `READS: n (...)` and `OUT <folder>`. It exits 0 only when no
read is ERROR, whatever the grades say.

## Reads

| read | outcome | what it records |
|---|---|---|
| `fwd5-markers-<name>` | FWD-5 v0.9 | Presses one coverage-event marker and one earnings marker if any is drawn (`g[data-timeline-marker][data-marker-day]`). Checks that the shared HeroDialog (Close button, "Opal Capital / News timeline" eyebrow) opens on THAT day (`[data-timeline-selected-day]`). Each article row (`li[data-timeline-article]`) must show headline, publisher (`span[data-publisher]`) and time at rest, with the mention/flags/tier detail (`[data-article-detail]`) closed. "More" opens that detail on demand, and Escape closes the dialog. Every request between the press and the close is logged; a non-GET (other than the background `/auth/refresh`) or a guard refusal is a FAIL with its URL. PNGs: the open dialog, the page, and "More" open. |
| `fwd5-own-first-<name>` | FWD-5 ACCEPT | Opens the served day with the most distinct publishers, using its bar (`rect[data-day-bar]`). Records the served `/timeline/day` row order against the shown order, every served row field, any field that could name an origin, and the publisher codes. As context it also records the recent-news card's served feed against its shown `[data-feed-item]` order. `own_first_basis` is `ORIGIN_FIELD`, `UNKNOWN_PUBLISHER` (FAIL) or `SINGLE_SOURCE_VACUOUS`. |
| `fwd11-side-by-side` | FWD-11 | Captures `/security-analysis/<first name>`, `/market`, `/positioning` and `/philosophy`: a full-page PNG at 1440 of each, plus a JSON of the compared computed styles: Panel chrome, PanelHeader title type, PanelFooter "time \| source", other bordered cards, chart library and the hovered tooltip (DataTooltip or not), designed vs look-alike empty states, type size/weight, ink and the root tokens. A `differs` list names the facts that vary. CAPTURE ONLY: PASS means captured, and the person's side-by-side read grades FWD-11. |
| `fwd19-panels-<name>` | FWD-19 | Covers the three panels round 32 named: the timeline, the identity header and What changed (Model tab). Each panel is captured in its loading and error state ON THE LIVE ROUTE, a fresh load per capture, with ONE `page.route` on that panel's GET (`/timeline`, `/overlay`, `/compare`). For loading, the request is held until the PNG is taken and then continued. For error, the route answers `route.fulfill` status 500. Each capture is graded DESIGNED (the `src/ui/components/states` component), LOOKALIKE (`data-panel-state` without the states Frame classes), NONE, or NOT_EXERCISED (the GET never fired, so the read is an ERROR). PNGs: the panel and the page. |
| `fwd19-no-permission` | FWD-19 | Captures PanelNoPermission on the real route `/security-analysis/<first name>`, runs LAST, and is graded on `[data-slot="route-no-permission"] [data-panel-state="no-permission"]`. See below. |

## What the sources at portal origin/DEV 56b71adb say (read with `git show origin/DEV:<path>`)

- **A marker press is GET-only.** The marker's onClick is `onSelectDay`, which is `setSelectedDay` (`TimelinePanel.tsx:314-325, 524`). That opens the HeroDialog (`:666-679`), and `DayDissection` reads `useTimelineDay`, which calls `apiRequest(path)` with no options (`:175-183, 450-451`). `api-client.ts:141-166` passes no method, so the request is a GET.
- **"Own harvested publications first"** comes from brief O5: "Opal Data Harvest publications lead and the News Scanner supplements" (`docs/briefs/dsgn-amgtv1-security-analysis-frontend-brief-20260928.md:86-87`). The served day row carries no origin field (`lib/research/harvest/timeline_api.py:125-128`), and its order is the server's (tier, mentions, time; `:133-140`). The day route serves Harvest rows only, so unless the live payload carries a field the code does not know, this read will report `SINGLE_SOURCE_VACUOUS`: no News Scanner row exists in the dialog to order.
- **FWD-19 on DEV, as coded:**
  - The timeline (`TimelinePanel.tsx:535-563`) and the identity header (`SecurityOverlay.tsx:321-351`) render the real PanelLoading/PanelError.
  - What changed renders a hand-rolled `div[data-panel-state="loading"]` and a bare `<p>` error (`WhatChangedPanel.tsx:398-408, 473-483`). The Model tab's own states are local look-alikes too (`ModelTab.tsx:103-124`).
  - If the live build matches the code, expect `fwd19-panels-*` to FAIL on What changed (LOOKALIKE loading, NONE error).
- **PanelNoPermission IS wired to a real route.** `ProtectedRoute.tsx:115-122, 128-136` renders `RouteNoPermission`, a `PanelNoPermission` inside `[data-slot="route-no-permission"]`, for a signed-in viewer who fails requireAdmin, requireInternal or requireDev. `/security-analysis` is requireDev + requireAdmin (`App.tsx:470-471`). The comment at `PanelStates.tsx:41-45` ("no live consumer") is stale.
  - The walker row is admin / opal-capital / Dev (`ui_walker_account.py:14, 113-114`), so the walker clears every gate and never sees the state itself.
  - The read therefore SIMULATES a non-Dev viewer. It sets `userType` to null in the walker's OWN `/auth/refresh` and `/auth/me` responses, in this browser only, with no server write; claims come from those responses (`AuthContext.tsx:170-201, 109-140`).
  - The JSON records each rewrite. If no auth response carried a user object, the read is an ERROR.

## Not settled without a live run

- Whether the live day payload carries any field beyond `timeline_api.py`'s nine. The read lists `fields_beyond_timeline_api`.
- Whether BA US and AMD US draw an earnings marker. Round 36 saw only the designed empty state.
- Whether a marker's center is hit-testable. If another element sits on top, the click falls back to `force` and the record says so.
- Whether each name serves at least 2 model versions. What changed mounts only then. With fewer, the `/compare` intercept never fires and that limb is NOT_EXERCISED (ERROR, with the versions count).
- How long the planted 500 takes to reach the error state: the overlay and compare hooks retry twice (about 3 s), and the timeline retries 0 times. The read waits up to 45 s.
- Whether the rewritten `/auth/refresh` keeps the session usable. It runs last, so nothing after it depends on it.
