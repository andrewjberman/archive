# SPEC SECTION -- The Mention Timeline, for HVST-h-8 (THE TIMELINE DESIGN SPEC)

Author: `0.9.0_WK_AMGT_HARVST~8` (AMGT_HARVST, cell HVST-h-8). Serves FWD-5 and FWD-6.
**This section describes the DATA SHAPE, the interaction and the API shape; it prescribes no
`.tsx` and no API implementation (`C-HV-DESIGN-SPEC-FIRST`). The build is a later cell, cut on
this spec's approval.**

Follows `AMGT_RESAPP`'s own precedent for form (`0.9.0_WK_AMGT_RESAPP~1`'s `DESIGN_SPEC.md` and
its per-surface `SPEC_SECTION_*.md` files, and `1.0.0_SA_CTO~Z`'s frontend framework/synthesis):
canvas law and per-figure vintage bind unchanged; every honest-state rule below follows the
same discipline S4/S7/S10 already established -- say the state, never hide it; mark, never
degrade.

## 1. Placement

`AMGT_HARVST`'s `C-HV-BOUNDARY` gives this project the timeline view; the rest of the security
page belongs to `AMGT_RESAPP`. The page shell (`AMGT_RESAPP_FRONTEND_FRAMEWORK_20260911.md`
section 1, and the synthesis's amended shell) is: a persistent top panel, then three tabs
(Thesis, Peers, Coverage), with Print/Drafting as an upper-right action.

**The timeline mounts in the PAGE HEADER, directly above the company feed's article list.**
*(AMENDED 2026-09-28 per `ledger/CTO_RULING_TIMELINE_PLACEMENT_20260928.md` @`277b0795ac`. The
SUPERSEDED text read: "The timeline lives at the top of the Coverage tab, above the existing article
list (S4, the Coverage Reader)." **`AMGT_RESAPP` RETIRED the Coverage tab into the header feed and
deleted it** -- the built page carries five tabs and no `CoverageTab.tsx` -- and that feed is the surface
that now holds Coverage's content (`AMGT_RESAPP_PRD.md:843`, on Andrew's header word at `:1891`). So the
timeline follows the content it was placed beside. Row `AMGT_HARVST-Z-S33`.)*
This is a placement, not a new tab: dissecting a day or an event on the
timeline drives the SAME article list S4 already renders below it -- a click sets a filter on
that list rather than opening a second list elsewhere on the page. This mirrors the framework's
own instruction that a surface without an explicit home is placed by the design-spec worker
without inventing a new top-level region (framework section 5's OPEN PLACEMENTS note, applied
here to a genuinely new surface rather than an unplaced FWD).

**Not the persistent top panel's Security-mode overlay.** That overlay (per the synthesis's Lead
Panel) plots this security's chatter AXIS against its peers and against price, at the universe's
relative/ranked scale (Trending/Breakout, computed server-side by the chatter projection, H7).
This timeline is a different view of the same underlying `chatter_daily` rows: this security's
OWN absolute day-by-day mention line, with day- and event-level dissection down to individual
articles. The two views may end up sharing a charting component in the `.tsx` build; this spec
does not decide that (section 7).

## 2. The line

**One chart, one security, dense from the floor.** The x-axis is UTC day, dense from
`2026-01-01` (`C-HV-DAILY-DENSE`'s floor) through the latest day `chatter_daily` carries for this
security -- never a gap, because a day with no coverage is a real zero row, not an absent one.

**Default measure: `mention_score`** (the tier-weighted sum `C-HV-MENTION-GRADE` computes,
carried on `chatter_daily` as stored). This is the "how much it was written about" line Andrew
asked for -- strength-weighted, not a raw count.

**Toggles**, each swapping the plotted series without changing the x-axis or the day-click
behavior:
- `articles_total` -- the raw count, for a reader who wants volume rather than strength.
- **Tier stack** -- the same `mention_score` height, decomposed into a stacked bar by
  `tier_a`/`tier_b`/`tier_c`/`tier_d` counts, so a reader can see whether a spike is real
  (tier A/B) or a wave of passing mentions (tier D). This is the chart-level answer to Andrew's
  "how much is it mentioned, is it mentioned in the headline" question, at the DAY grain; the
  ARTICLE grain answer is section 3.

**Time range:** the full dense range renders by default (pannable/zoomable, `.tsx` decision);
the exact initial zoom window is an open call (section 7). `trailing_7d_sum` and
`trailing_30d_sum` are available for an on-hover secondary reading of a single day without
changing the plotted series.

**`data_status` -- PARTIAL and DENIED never read as a quiet day.** Every day's bar/point carries
`data_status` (`COMPLETE | PARTIAL | DENIED`) from `chatter_daily`. Rendering, following the
check-face precedent (S10) so the three states never look alike at a glance:
- `COMPLETE` -- rendered plainly, full weight, the state most days carry.
- `PARTIAL` -- rendered at its stored height (whatever coverage WAS captured) but with a visible
  marker distinct from a normal bar (for example a hatched fill) -- never a plain bar that reads
  as "this is the whole story for that day." Hovering names the reason if `chatter_daily` carries
  one.
- `DENIED` -- rendered with its own distinct marker (never the same hatch as PARTIAL, never a
  blank gap in the dense series) regardless of its stored height, because a DENIED day's height
  cannot be trusted as the count of what happened -- it is the count of what retrieval was
  DENIED for. The literal state name renders on hover, following S10's `[REFUSED: reason]`
  discipline rather than a silently smaller bar.

A quiet day (a real `COMPLETE` day with `mention_score` at or near zero) and a `PARTIAL`/`DENIED`
day must never share a visual encoding -- that is the one rule this section exists to state, and
the whole reason `data_status` is a stored, per-day field rather than inferred from height.

## 3. Dissecting a day

**The click:** selecting a day on the line opens that day's article list (rendered in the
Coverage tab's existing list area, per section 1's placement, or an expandable panel directly
beneath the timeline -- `.tsx` decision, either satisfies this spec).

**Order: strongest first**, sorted by:
1. `signal_tier` (A, then B, then C, then D) -- `article_security_mention`'s tier for THIS
   security, not a page-wide tier;
2. within a tier, `mention_count` descending;
3. within a tie, `published_utc` -- earliest first, so the article that likely triggered the
   day's coverage leads its tier band (the eventual `.tsx` may reverse this to latest-first if
   Andrew prefers a "what's new" reading; this spec does not fix the direction as a constant,
   only the two-clause tie-break existing above it).

**Each row shows:**
- the headline (`article_security_mention`'s parent article record, or the bronze/silver
  article's own headline field -- the exact join is a build-cell detail, not fixed here);
- the publisher (the `{source}` this article came from);
- the tier (`signal_tier`, A-D, rendered with the same visual language as the timeline's tier
  stack toggle so a reader can connect a row back to the chart);
- **"in headline" and "in lead" marks** -- two small, always-present marks reading
  `mention_in_title` and `mention_in_lead` directly (both booleans on `article_security_mention`
  in the header field list) -- present-but-unmarked when false, never omitted, so a reader can
  scan a day's list for the in-headline articles without opening each one;
- the time (`published_utc`, rendered with its UTC offset/precision per `published_precision`
  where the silver row carries one -- an article whose precision is coarser than a timestamp
  states so rather than showing a false-precise clock reading).

**A day with zero articles is reachable and honest.** A `COMPLETE` day with `articles_total = 0`
opens to an explicit "no articles this day" state, not a blank list a reader cannot distinguish
from a loading failure. A `PARTIAL`/`DENIED` day's dissection additionally carries the same
marker named in section 2, restated at the top of the opened list (never only on the chart,
where the state can be scrolled past).

## 4. Event spans

**Drawn over the line**, not as a separate list: a `chatter_event` row spans from `first_day` to
`last_day` (a single-day event has `days_span = 1` and renders as a marked point rather than a
band). The span sits as a shaded band along the day axis, layered above or behind the plotted
bars (`.tsx` decision) so the underlying day values stay readable.

**Every span carries its `lead_headline`** as a visible label on or immediately beside the band
-- never a span with no headline, per FWD-6's own bar ("marked events with a headline, not just
spikes in a count"). Where two events' bands would visually collide (adjacent or overlapping
runs), the label placement is a build-cell `.tsx` detail; this spec's rule is only that every
rendered span keeps its own headline legible, never truncated to nothing.

**Opening an event** (clicking its band or label) lists its articles -- `chatter_event`'s
`article_keys`, resolved to the same row shape and the same strongest-first order as section 3's
day dissection (tier, then `mention_count`, then `published_utc`). This reuses the day-dissection
list component; an event's opened list is not a visually distinct component from a day's.

**No event on a security with no qualifying run.** `chatter_event` rows exist only where the
working rule (`C-HV-EVENT-SPINE`: tier A+B articles >= 2, from >= 2 publishers, merged across
gaps <= 1 day) is met -- a security with real coverage that never clears that bar shows a line
with no spans, which is the correct, honest state, not a gap to fill with an invented event.

## 5. The API shape

Following the security page's existing per-security route shape (`GET .../security/{security_key}/<surface>`,
query parameters for range/window rather than new path segments) -- the route itself is named and
built by the cell this spec unblocks; no implementation file is named here.

**`GET .../security/{security_key}/timeline?from=<date>&to=<date>`** -- the line plus its events,
in one call (both are read from the same day range and are shown together, so one round trip
serves the chart):
- `security_key`, and the resolved `floor_date` (`2026-01-01`, or the security's own dense start
  if that ever differs from the project floor).
- `series`: one entry per UTC day in range, each carrying, READ STRAIGHT FROM `chatter_daily`:
  `date`, `mention_score`, `articles_total`, `tier_a`, `tier_b`, `tier_c`, `tier_d`,
  `mention_count_total`, `publishers_distinct`, `trailing_7d_sum`, `trailing_30d_sum`,
  `cumulative_ytd`, `data_status`. Plus, COMPUTED AT SERVE TIME (never stored,
  `C-HV-ABSOLUTE-ONLY`): a `breakout_ratio` (the day's activity against its `baseline_30d_sum` /
  `baseline_30d_days`) and a `z_score` against the same trailing baseline -- both exposed for a
  future chart mode; neither is required for the section-2 default view, which plots stored
  absolute fields only.
- `events`: one entry per `chatter_event` row whose `first_day`/`last_day` intersects the
  requested range, READ STRAIGHT FROM `chatter_event`: `first_day`, `last_day`, `days_span`,
  `articles_total`, `tier_a`, `tier_b`, `publishers_distinct`, `lead_article_key`,
  `lead_headline`. No relative figure is computed on this arm.

**`GET .../security/{security_key}/timeline/day/{date}`** -- one day's dissection: `security_key`,
`date`, `data_status` (restated here per section 3's rule), and `articles`: the strongest-first
list, each entry carrying, READ STRAIGHT FROM `article_security_mention` (joined to its article's
own headline/publisher fields): `article_key`, headline, publisher, `signal_tier`,
`mention_count`, `mention_in_title`, `mention_in_lead`, `published_utc`, `published_precision`.
No relative figure appears on this arm; strength is expressed by the stored tier and count, not
a computed score.

**`GET .../security/{security_key}/timeline/event/{first_day}`** -- one event's dissection, same
`articles` shape as the day route, resolved from that event's `article_keys`. Keyed by
`first_day` because `C-HV-EVENT-SPINE` does not name a stored `event_id`; whether the build cell
mints a stable synthetic id instead is an open call (section 7).

**The error envelope.** Any of the three routes above, on failure (a non-200 status, a timeout, or
an exception in the route), returns ONE shape rather than a partial or malformed version of its
normal body: `{"error": true, "error_code": <string>, "message": <string>}` -- `error_code` a
stable machine token (for example `TIMELINE_FETCH_FAILED`, `TIMELINE_TIMEOUT`,
`TIMELINE_DAY_NOT_FOUND`), `message` a short human-readable reason. A response carrying
`error: true` is NEVER rendered as data: it is never merged into `series`, `events` or `articles`
as if it were a data row, and never rendered as a zero-length or otherwise empty version of those
arrays -- an empty
`series`/`events`/`articles` array means "the call succeeded and there is nothing in range," which
is a different, honest state (section 6) from a call that did not succeed at all. The client's only
correct action on `error: true` is the section-6 failed-call state; no fallback quiet or zero
render.

## 6. States

- **Loading** -- the line and its events render a skeleton/placeholder while the range call is
  in flight; the day/event dissection panel shows its own loading state independently (opening a
  day should not force the whole line to re-render).
- **No articles for the security** -- a security WITH `chatter_daily` rows (it is in the covered
  set) but every day `COMPLETE` at `articles_total = 0` for the requested range: the line still
  renders (a real, flat, honest zero line), with a stated note that no coverage has been found in
  this range yet -- distinct from the next state below.
- **The floor date** -- a request (or a pan/zoom) reaching before `2026-01-01` clamps to the
  floor and states it plainly ("history starts 2026-01-01," per `C-HV-DAILY-DENSE`/FWD-9's
  backfill floor) rather than showing broken or absent pre-floor days.
- **PARTIAL and DENIED days** -- per section 2's marking rule, restated: never rendered
  identically to a quiet `COMPLETE` day, on the line or in its dissection.
- **A security that was never collected** -- no `chatter_daily` rows exist for this
  `security_key` at all (it is outside the project's covered set, not merely quiet): the timeline
  area shows a page-level "publication history not collected for this security" state instead of
  an empty chart -- the same discipline S1 uses for a security AMGT-s-1 has not yet pulled.
- **The timeline request itself failed** -- any of section 5's routes returns a non-200 status,
  times out, or comes back with a malformed or unparseable body; the client has NO trustworthy
  response, which is decided by the transport/envelope outcome, never by any row `chatter_daily`
  or `chatter_event` holds. Never a blank chart, an empty series, or a zero-height line is drawn for
  this state -- each of those reads as "we hold nothing for this range," the same encoding a
  quiet security or a PARTIAL/DENIED day already claims, and this state means something different:
  "we do not know what we hold." It renders its own distinct, page-level error state (for example a
  banner in the timeline's area, visually apart from the chart canvas and from any bar/marker
  language used above) stating plainly that the timeline could not be loaded, never that coverage
  is quiet or the security is uncollected, and offers a retry action. If the day/event dissection
  call fails while the line itself loaded, only the dissection panel shows this state
  independently -- it does not force the whole line into it. This state and the error envelope in
  section 5 exist so a build against this spec cannot omit the call-failure case the way the page's
  other panels once did (section 7).

## 7. What this spec does not decide

- The tier weights and the 0.3 share threshold (`C-HV-MENTION-GRADE`) and the event rule's
  exact thresholds (`C-HV-EVENT-SPINE`) are working defaults Andrew resets without a contract
  change -- this spec renders whatever they currently produce and invents no different value.
- The initial zoom/window shown when the timeline first opens (the full dense range vs. a
  recent slice, e.g. the last 90 or 180 days) is not fixed here.
- The exact tie-break direction (earliest-first vs. latest-first) within a tied tier/count band
  in the strongest-first order (section 3) is left to the build cell / Andrew's preference.
- Whether the build cell mints a stable synthetic `event_id` in place of keying the event
  dissection route by `first_day` (section 5).
- The precise visual encoding (color, hatch pattern, icon) for `PARTIAL` vs `DENIED` days and
  for an event span vs. a single-day event marker -- this spec fixes only that the three states
  (quiet-COMPLETE, PARTIAL, DENIED) must never look alike, and that a span always carries its
  headline; the exact pixels are a `.tsx` decision.
- Whether `is_roundup` articles are visually de-emphasized within a day's dissected list (they
  still count toward the day's `mention_score` per the stored tier rule; whether the list marks
  them separately is not decided here).
- Where the shared charting component (if any) between this timeline and the top panel's
  Security-mode chatter overlay lives -- section 1 notes they read the same table but does not
  require or forbid a shared component.
- The failed-call state (section 6) and error envelope (section 5) were added because the same
  omission -- no state for the call itself failing -- was a real, graduated defect on this page's
  other panels (`Z-S227`/`C-S400`); this section does not restate that history further.

## 8. Acceptance

On the validation security, Lenovo (`992_HK_Equity`), once `HVST-h-5`/`HVST-h-6`/`HVST-h-10`
have run and this spec is approved and built:

**FWD-5:** an analyst opens Lenovo's security page, sees in the PAGE HEADER above the company feed
*(AMENDED 2026-09-28, same ruling @`277b0795ac`; SUPERSEDED: "reaches the Coverage tab". FWD-5's own
ENDPOINT text is NOT amended and never named a tab -- only this spec's walk changes.)* the day-by-day
line dense from 2026-01-01 with `mention_score` plotted by default, picks a day that carries
`articles_total > 0`, and the day opens to its article list ordered strongest first (tier A
before B before C before D, `mention_count` descending within a tier) -- each row showing
headline, publisher, tier, in-headline/in-lead marks and time, per section 3.

**FWD-6:** the same timeline shows at least the event runs `chatter_event` holds for Lenovo (per
the working rule in `C-HV-EVENT-SPINE`, evaluated on Lenovo's landed gold), each drawn as a
marked span carrying its `lead_headline`; opening one lists its articles in the same
strongest-first shape as a day's dissection, per section 4.

A build that cannot show both of the above on Lenovo's own landed data has not met this spec,
regardless of how the chart looks on synthetic or placeholder data.
