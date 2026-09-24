# R-41 routed act: the call-4 authorizer-log READ -- preserved before the 2026-10-22 wall

**Seat:** `0.7.0_AE_CloudOps~A` ? **Date:** 2026-09-24 ~09:4xZ ? **Routed by:** R-41 (`1.0.0_SA_CTO~Z`, msg 25372)
**Act class:** READ-ONLY query on Opal's own CloudWatch log. No egress, no vendor call, nothing changed.
**Why it exists:** R-31 ruled call 4 "decidable, one join away" and nobody ran the join. The instrument
carrying the answer EXPIRES 2026-10-22 at 30-day retention. This file preserves what the decision needs so
the expiry stops mattering.

STOP: **THIS FILE DECIDES NOTHING.** The client-notification decision is Andrew's by class (R-41), and the
IP-to-identity join is not closed here. This is the measurement half only.

---

## 0. A CORRECTION TO THE ROUTING MESSAGE, and it matters before anyone re-runs this

**Msg 25372 names `/aws/lambda/opalinvest-auth-handler`. That is the WRONG LOG GROUP.** R-31's own
measurement is `/aws/lambda/opal-portal-authorizer`, and R-31's stated figures identify it unambiguously:

| group | retention | storedBytes | R-31 says |
|---|---|---|---|
| `/aws/lambda/opal-portal-authorizer` | 30 | **3,753,955 (3.75 MB)** | "retention 30 days, **3.75 MB** stored" -- MATCH |
| `/aws/lambda/opalinvest-auth-handler` | 30 | 3,160,776 (3.16 MB) | not this one |

Both groups exist, both retain 30 days, and the wrong one is the group this lane had been reading all
session for the unrelated D12/SMS thread -- which is the likely source of the slip. **A seat acting on the
routing message's text alone queries a real, live, plausible log group and gets a real, clean, WRONG
answer.** Measured, not inferred; the ruling's own byte figure is the discriminator.

## 1. Coverage control, run BEFORE any zero was believed

`/aws/lambda/opal-portal-authorizer`, 2026-09-22T00:00Z .. 2026-09-24T00:00Z:

```
total events            7,046      (09-22: 1,574   09-23: 5,472)
distinct identities        10
domains                     4      opalinvest.com 1716 | inflectionwealth.com 204
                                   | vmwealthpartners.com 54 | cottonwoodmail.com 30
```

**This reproduces R-31 on an independent read: TEN distinct identities across FOUR firms.** Both incident
days are retained and populated, so an empty window is a cache artifact rather than an absence -- which is
R-31's own point, and it is why the widening below was run instead of stopping at the narrow result.

## 2. The four incident timestamps, by window width

Domains only. Individual addresses are deliberately NOT recorded here (R-31's PII discipline: the firms and
the counts are what the decision needs). Address-level detail remains extractable from the live log until
**2026-10-22** if the decision genuinely requires it.

| window | 09-22 19:15:35Z | 09-22 20:14:11Z | 09-22 20:21:40Z | 09-23 20:44:34Z |
|---|---|---|---|---|
| +/- 8s | 0 events | 0 | 0 | 36 ev, **opalinvest only** |
| +/- 120s | 7 ev, opalinvest | 0 | 0 | 72 ev, **opalinvest only** |
| +/- 300s | 19 ev, **inflectionwealth** + opalinvest | 0 | 0 | 72 ev, **opalinvest only** |
| +/- 600s | 67 ev, opalinvest + **inflectionwealth** | 12 ev, **inflectionwealth only** | 0 | 72 ev, **opalinvest only** |
| +/- 1800s | 296 ev, opalinvest + **inflectionwealth** | 79 ev, opalinvest + **inflectionwealth** | 72 ev, opalinvest + **inflectionwealth** | 87 ev, **opalinvest only** |

## 3. What this NARROWS, stated as narrowing and not as attribution

KEY: **OF THE THREE EXTERNAL CLIENT FIRMS ACTIVE IN THE WINDOW, ONLY ONE APPEARS NEAR THE 09-22 EXPOSURES.**
`inflectionwealth.com` is present around all three; `vmwealthpartners.com` (54 events in the two-day window)
and `cottonwoodmail.com` (30 events) appear at NO width up to +/- 30 minutes around ANY of the three. That
is a discriminating negative, not a silence: both firms demonstrably transacted that day, so their absence
near these timestamps is informative rather than a coverage hole.

**The 09-23 20:44:34 event is internal at every width tested**, carrying only `opalinvest.com` -- consistent
with R-31's narrower finding of `andrew@opalinvest.com`, tier internal, userType Dev.

STOP: **AND THIS IS EXPLICITLY NOT AN ATTRIBUTION.** R-31's cache warning binds in BOTH directions and is not
retired by widening: an API Gateway authorizer result is cached, so the requester may have been authorized
OUTSIDE even a +/- 30-minute window and emitted no line at all. **Presence in a window is not a request, and
absence from one is not an exoneration.** Naming a firm on this evidence would be exactly the guess R-21a
was written to prevent.

## 4. What still closes it, and who holds it

**The IP join, unchanged from R-31.** `3.0.0_SA_CVO~Z` holds THE ONE CLIENT IP, parsed from 664 CloudFront
access-log files / 19,114 rows. CloudFront carries IP+timestamp; this authorizer carries identity+timestamp.
Neither alone attributes a request; together they do. R-31's shortcut stands and is now cheaper: the
exposure was ONE IP, so mapping that single IP through ANY overlapping authorizer event settles the card --
and section 3 narrows the candidate set it has to be mapped against.

**One parameter this lane could not retrieve:** the timestamp of the "plus one overlay" response. R-31 names
four thesis timestamps and an overlay without dating the overlay, so the overlay is NOT covered by section 2.

## 5. Instrument notes

`filter-log-events` auto-paginates and emits CONCATENATED JSON documents; a single `json.load` raises on the
second document and `--query length(events)` returns a PER-PAGE count rather than a total (CLAUDE.md's
paginated-list trap, hit and corrected in this work). Counts above are client-side over a raw-decode loop.
Native Windows python cannot spawn the MSYS `.tools/aws` shim, so the window sweep runs in bash.

**Push state at authoring: LOCAL.** This seat commits and never pushes.
