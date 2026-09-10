# MONITORED-vs-SERVED RECONCILER — what we publish that NOTHING is watching (cell RP-s-11, outcome FWD-11)

Authority: `NFRA_REPORT_PRD.md` manifest row S11 (`FWD-11`), the L1 brief's Part II Owns
(*"the standing check that NO EXISTING INSTRUMENT PERFORMS"*), and this cell's own bound. Renders
through `STATE_MODEL.md`'s ratified vocabulary; adds ONE new, explicitly-orthogonal qualifier this
document's own investigation showed to be necessary (§2), by the same discipline `RP-s-1` used for its
own third axis — reuse first, extend only where a real gap is demonstrated, never collapse two
questions onto one field.

## 0. FWD-11 is NOT FWD-10 — the distinction, stated so it cannot be collapsed

**`FWD-10`** (`RP-s-10`, `COVERAGE.md`) makes a STATED NUMBER honest about what it counted out of —
"3 of 7," never a bare "3." It presupposes something was counted at all.

**`FWD-11`** finds the surfaces that produce **NO NUMBER WHATSOEVER** — nothing counted them, so there
is no numerator to attach a denominator to and no row on any dashboard to be honest or dishonest about.
**A surface FWD-11 finds is invisible to FWD-10 by construction**, because FWD-10's discipline only
binds a count that exists; FWD-11's job starts one step earlier, asking whether a count exists at all
for a thing this estate serves to a human.

A third, adjacent-but-distinct category this document does NOT claim as its own, named so it is not
confused with either: `RP-s-6`'s alert-delivery read (`FWD-5`) is about an instrument that DOES exist
(an alarm) whose delivery LEG is broken (zero confirmed subscribers) — that is neither an honesty
problem about a stated number (`FWD-10`) nor an absence of any instrument at all (`FWD-11`); it is a
present-but-non-firing instrument, and this document does not re-collapse it into either.

## 1. THE ACT, MADE OPERATIONAL: three per-row states, not two

**"A part of the business with nothing watching it must look DIFFERENT from one that is watched and
healthy"** (cell text, verbatim) requires the reconciler to render, per served surface, one of:

- **WATCHED** — a real instrument (alarm, drift check, etc.) is confirmed attached to this surface.
- **UNWATCHED** — confirmed, positive-controlled absence: the SAME sweep that finds instruments on
  comparable surfaces returns zero for this one.
- **INSTRUMENT-CANNOT-SEE** (new, orthogonal qualifier — see §2) — the enumerator this reconciler is
  built on does not model the edge type needed to answer the question at all, for EITHER surfaces that
  are actually watched or ones that are not. This is never rendered as UNWATCHED.

**Collapsing the third state into the second is exactly the failure this cell exists to prevent, one
level up from the failure `FWD-10` prevents:** an "unwatched" verdict born of instrument blindness is a
false coverage claim wearing a coverage-honesty template.

## 2. THE ORTHOGONAL QUALIFIER IS NOT HYPOTHETICAL — this project's own RP-s-7 already needed it

The coordinator's steer named the concrete case directly: `RP-s-7`'s own row `NFRA_REPORT-Z-W1-S1`
established that `comp-blast`'s served graph models **NO edge at all** between `GOLD_SCRIPT` nodes and
Lambda/portal nodes — confirmed by a positive-control failure on a definitely-live lambda
(`inf-api-positions`) showing zero `gold:` ancestors upstream, despite that lambda demonstrably reading
gold-layer output at runtime.

**Applied here:** if this reconciler tried to answer "is the data `INF_D_04.client_portal_summary.py`
produces being watched by any freshness/error instrument at the point it reaches a client," it would
need to walk gold-script → serving-Lambda/route → instrument. The FIRST hop of that walk is exactly the
edge `comp-blast` cannot see. **A reconciler that ran this check and reported "UNWATCHED" for every
gold-layer artifact would be reporting its OWN blindness as a finding about the WORLD** — the precise
trap the coordinator named. This document does not run that check via `comp-blast` for that reason, and
any future extension of this reconciler that walks gold-layer artifacts MUST inherit this same
declared limit rather than re-discovering it.

**This is why the qualifier must be a THIRD, orthogonal field and not a value squeezed into the
WATCHED/UNWATCHED axis:** the two questions — *is this surface watched* and *can my own instrument even
tell* — are different grains (rule 24(ii)/(iii)), same shape as `RP-s-1`'s `desired|applied|exercised`
axis being kept separate from `CHECKED`/`OK`.

## 3. THE WALK, PERFORMED — live AWS-plane reads, positive-controlled, denominators carried (per `RP-s-10`)

Enumerator: `comp-find --corpus aws` (repaired, vintage-carrying — see §5). Bounded per node type, never
an unbounded sweep. Vintage of every read below: **2026-09-09 21:05:17 UTC**, manifest `09be45b5ff92`.

### 3a. CloudFront distributions vs. CloudWatch alarms (WATCHED / UNWATCHED, high confidence)

| Distribution | Declared? | Alarms matching (structural `DistributionId` dimension) | Verdict |
|---|---|---|---|
| `EVTSA9VEHNZVH` (aliases `opalinvest.dev`, `www.opalinvest.dev`) | yes | 3 of 51 (`cloudfront-high-error-rate`, `cloudfront-high-origin-latency`, `cloudfront-low-cache-hit-rate`) | **WATCHED** |
| `E1DHJH4Y1W8YC2` (aliases: none; target origin `wp-origin`) | yes | **0 of 51** | **UNWATCHED (confirmed)** |

**Positive control:** the same 51-alarm sweep, same method, returns 3 hits for the sibling — a broken
probe would return zero for both. It does not. `E1DHJH4Y1W8YC2` genuinely has no CloudWatch alarm of any
kind attached, by the exact structural field (`dimensions.DistributionId`) that finds its sibling three
times over. Declared, not overclaimed: whether public traffic currently flows through this distribution
at all is a separate question this reconciler does not resolve (it carries no alias, so the two named
properties' domains do not route through it) — the finding is that IF anything does, or ever does again,
nothing here would notice.

### 3b. API Gateways vs. CloudWatch alarms (WATCHED / UNWATCHED, weaker method, declared)

| API Gateway | Declared? | Alarms matching (name/ID substring) | Verdict |
|---|---|---|---|
| `opal-session-analytics-api` | no (`LIVE-no-DECLARED`) | 4 of 51 (`errors`, `estimated-monthly-cost`, `high-invocations`, `throttles`) | **WATCHED** |
| `sentiment-query-api` | no (`LIVE-no-DECLARED`) | **0 of 51** | **UNWATCHED (confirmed, weaker evidence — see below)** |
| `trade-submission-api` | no (`LIVE-no-DECLARED`) | **0 of 51** | **UNWATCHED (confirmed, weaker evidence — see below)** |

**Method is weaker than §3a, declared rather than hidden:** this match is a NAME/ID SUBSTRING search
over whatever `comp-find`'s AWS corpus indexes (alarm name, ARN, a truncated JSON excerpt), not a
structural dimension field like `DistributionId`. An alarm targeting the same underlying Lambda under
an unrelated name would be missed by this method and would read as a false `UNWATCHED`. **Still
positive-controlled** (the identical method finds `session-analytics`'s 4 alarms), so the zero is not a
dead probe — but it carries less certainty than §3a's structural match, and this document says so rather
than presenting both at the same confidence.

**`trade-submission-api` is named here deliberately.** A live, undeclared, apparently-unwatched API
surface named for a financially consequential function is precisely the class of finding `FWD-11`
exists to make findable rather than buried in an undifferentiated list — filed as surprise row
`NFRA_REPORT-Z-W1-S4` (`ARMED`) alongside `E1DHJH4Y1W8YC2` and `sentiment-query-api`, because a live
report row is not itself the escalation channel and the finding should not depend on a future reader
opening this specific deliverable.

### 3c. Gold-layer served data (INSTRUMENT-CANNOT-SEE — the third state, not collapsed)

Any question of the shape "is `INF_D_00c.portal_leaderboard.py`'s output watched once it reaches
`AdvisorsTab`/`ClientsTab`" is rendered **`INSTRUMENT-CANNOT-SEE`**, citing `NFRA_REPORT-Z-W1-S1`
directly, for every one of `DEPRECATION.md`'s ten walked candidates and by extension any gold-layer
artifact this reconciler has not individually re-verified. **Not rendered `UNWATCHED`.**

## 4. TALLY, DENOMINATED (per `RP-s-10`'s own discipline, practiced here rather than only stated)

- CloudFront distributions swept: **2 of 2**. WATCHED: 1. UNWATCHED (confirmed, structural): 1.
- API Gateways swept: **5 of 5** (2 declared, not individually re-checked here; 3 undeclared, all
  checked). WATCHED: 1 of 3 checked. UNWATCHED (confirmed, weaker method): 2 of 3 checked.
- Gold-layer serving edges: **0 of ~1380 `GOLD_SCRIPT` nodes** resolvable by this reconciler's
  enumerator for this specific question — rendered `INSTRUMENT-CANNOT-SEE`, denominator stated as the
  count this method could NOT resolve, not folded into either confirmed state.

**No row in this document is UNWATCHED without a positive control in the same sweep, and no row is
INSTRUMENT-CANNOT-SEE without a named, cited instrument limit.** Both are stronger claims than "an
absence," which is exactly what `RP-s-10`'s own doctrine (a value must carry its claim) asks of a
finding like this one.

## 5. Grounding note on the enumerator itself (battery finding, re-verified not assumed)

`PRD` section 7 still describes `comp-find --corpus aws`'s vintage as `UNREAD`; that text is stale and
its own author has said so. Re-verified fresh this session rather than taken on the battery's word
alone: `comp-find '.' --corpus aws IAM_ROLE --limit 5` (the literal AC1 invocation as written fails —
see surprise row `NFRA_REPORT-Z-W1-S3`; the corrected, shim-routed form is what was actually run) prints
`VINTAGE: Built from the estate as of 2026-09-09 21:05:17 UTC... manifest: 09be45b5ff92`, never the
literal string `VINTAGE: UNREAD`. The instrument is live and carries a real timestamp.

## 6. What this document does NOT do

- Does not re-grade `RP-s-6`'s alert-delivery findings, or fold a broken-delivery-leg instrument into
  either WATCHED or UNWATCHED — that is a different, already-served question (§0).
- Does not build, propose, or script a new alarm/monitor for any UNWATCHED surface found — the standing
  alerting/monitor moratorium binds this cell exactly as it bound `RP-s-6`; findings are filed, not
  fixed.
- Does not claim the API-gateway UNWATCHED verdicts (§3b) are as certain as the CloudFront one (§3a) —
  the method difference is stated, not smoothed over.
- Does not render a single gold-layer artifact `UNWATCHED` on `comp-blast`'s silence — every such case
  renders `INSTRUMENT-CANNOT-SEE`, per §2/§3c.
