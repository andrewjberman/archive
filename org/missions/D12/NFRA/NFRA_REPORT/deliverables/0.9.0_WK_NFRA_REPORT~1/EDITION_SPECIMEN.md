# NFRA_REPORT -- EDITION SPECIMEN

**Composed by:** `compose_edition.py` (cell `RP-s-15`, `0.9.0_WK_NFRA_REPORT~1`) -- **Composed at (this run):** 2026-09-10T03:25:45Z

**REGION KEY, per C-AI part 1 (declared per region, legible without knowing how this report is built):**
- `QUOTED` -- transcribed from a round-1 deliverable, with a citation. See `compose_edition.py`'s `ROW_FACTS`.
- `COMPUTED` -- a deterministic function over QUOTED tuples: `compute_delta()` (ROW_STRUCTURE.md sec.2, verbatim), `compute_delta_watch()` (declared bridge, see `COMPOSER.md`), `compute_verdict()` (VERDICT.md sec.1, verbatim).
- `GENERATED` -- the "Reading" sentence under each row and this summary's prose. Per C-AI part 2, a `GENERATED` sentence is never the sole carrier of a fact: every fact it mentions is also present, in full, in that row's own `QUOTED`/`COMPUTED` cells. Delete every `GENERATED` sentence in this document and the table below is still true and still checkable against its own citations.

---

## 1. THE VERDICT -- `COMPUTED`, per `VERDICT.md` section 1

> **SOMETHING needs Andrew today.**

**COMPUTED basis (never generated -- this is the rule, applied):**
- Clause 1 (a live `CHECKED`+`BREACH` row exists): **3 of 24 real rows** -- opal-infrastructure-alerts (SNS topic), Cost segment: inf (Pipeline tag), Cost segment: bd (Pipeline tag)
- Clause 2 (a real row's delta is `worse`): **0 of 24 real rows** -- none

`GENERATED`: The illustrative regression row below is explicitly excluded from both clauses above -- it is labeled not-live in `ROW_FACTS` and `compute_verdict()` filters it out before either clause is evaluated, so a demonstration fixture can never itself trip a real verdict.

---

## 2. EVERY ROW, WITH ITS OWN DELTA -- never a max() over rows

| Property (`QUOTED`) | Previous state (`QUOTED`) | This edition (`QUOTED`) | Delta (`COMPUTED`) | Citation (`QUOTED`) |
|---|---|---|---|---|
| Website security (opalinvest.com / www) | `DENY-BY-DESIGN` | `DENY-BY-DESIGN` | **unchanged** | STATE_MODEL.md sec.4; ROW_STRUCTURE.md sec.3 (worked specimen row 1) |
| Blocked-address sentinel row (worked specimen, per STATE_MODEL.md sec.5) | `BLIND` | `CHECKED` / `OK` / 3rd axis: `desired` | **better** | STATE_MODEL.md sec.5; ROW_STRUCTURE.md sec.3 (worked specimen row 2) |
| opal-login-abuse-alerts (SNS topic) | `INERT` | `INERT` | **unchanged** | ALERT_DELIVERY.md sec.1/sec.2 (re-confirming NFRA_OPSEC202609-Z-S151, ~15:45Z, IDENTICAL result at ~21:01Z) |
| astn-wsjft-alerts (SNS topic) | `INERT` | `INERT` | **unchanged** | ALERT_DELIVERY.md sec.1 (RESULT: IDENTICAL to NFRA_OPSEC202609-Z-S151) |
| etfs-reports-alerts (SNS topic) | `INERT` | `INERT` | **unchanged** | ALERT_DELIVERY.md sec.1 (RESULT: IDENTICAL to NFRA_OPSEC202609-Z-S151) |
| opal-infrastructure-alerts (SNS topic) | `UNCHECKED` | `CHECKED` / `BREACH` | **better** | ALERT_DELIVERY.md sec.4 (resolves NFRA_OPSEC202609-Z-S151's own explicitly-unresolved question) |
| inf-otp-alert (SNS topic) | `CHECKED` / `UNASSERTED` | `CHECKED` / `UNASSERTED` | **unchanged** | ALERT_DELIVERY.md sec.4 (Axis 2 left UNASSERTED, not defaulted to OK) |
| opal-critical-surface-alerts (SNS topic) | `CHECKED` / `UNASSERTED` | `CHECKED` / `UNASSERTED` | **unchanged** | ALERT_DELIVERY.md sec.4 |
| opal-partner-etl-ops-alerts (SNS topic) | `CHECKED` / `UNASSERTED` | `CHECKED` / `UNASSERTED` | **unchanged** | ALERT_DELIVERY.md sec.4 |
| comp (instrument, ruling-12 worked example) | `CHECKED` / `DEGRADED` | `CHECKED` / `OK` | **better** | ROW_STRUCTURE.md sec.3 (worked specimen row 4) |
| B_01.holdings_lots.py (deprecation candidate) | `COARSE` | `CHECKED` / `OK` | **better** | DEPRECATION.md sec.0/sec.2 (ruling 6's age heuristic + the CRO's one-hop check, both superseded by ruling 9's terminus walk) |
| INF_D_04.client_portal_summary.py (deprecation candidate) | `COARSE` | `CHECKED` / `OK` | **better** | DEPRECATION.md sec.2 |
| INF_D_00.portal_aggregates.py (deprecation candidate) | `COARSE` | `COARSE` | **unchanged** | RETIREMENT_ROUNDTRIP.md sec.2 (Edition B); RETIREMENT_REGISTER.md sec.3 row 1 (CARRIED, owner 0.9.0_WK_NFRA_REPORT~1, 2026-09-09) -- cited via the register's current-state view, not re-walked this edition |
| INF_D_07.concentration_risk.py (deprecation candidate) | `COARSE` | `COARSE` | **unchanged** | RETIREMENT_ROUNDTRIP.md sec.2 (Edition B); RETIREMENT_REGISTER.md sec.3 row 4 (CARRIED, owner 0.9.0_WK_NFRA_REPORT~1, 2026-09-09) -- cited via the register's current-state view, not re-walked this edition |
| CloudFront distribution EVTSA9VEHNZVH (opalinvest.dev / www) | `NO-INSTRUMENT-EVER` | `WATCHED` | **better** | MONITORED_VS_SERVED.md sec.3a |
| CloudFront distribution E1DHJH4Y1W8YC2 (no alias; wp-origin target) | `NO-INSTRUMENT-EVER` | `UNWATCHED-CONFIRMED` | **better** | MONITORED_VS_SERVED.md sec.3a |
| opal-session-analytics-api (API Gateway, LIVE-no-DECLARED) | `NO-INSTRUMENT-EVER` | `WATCHED` | **better** | MONITORED_VS_SERVED.md sec.3b |
| sentiment-query-api (API Gateway, LIVE-no-DECLARED) | `NO-INSTRUMENT-EVER` | `UNWATCHED-CONFIRMED` | **better** | MONITORED_VS_SERVED.md sec.3b |
| trade-submission-api (API Gateway, LIVE-no-DECLARED, financially consequential) | `NO-INSTRUMENT-EVER` | `UNWATCHED-CONFIRMED` | **better** | MONITORED_VS_SERVED.md sec.3b; ANOMALY_BREAKDOWN.md sec.3 (30 connected resources: 4 lambdas, 4 DynamoDB tables, 1 S3 bucket, 2 KMS keys); surprise row NFRA_REPORT-Z-W1-S4, DISARMED/GRADUATED by NFRA_REPORT-Z-S7 |
| Gold-layer served surfaces (aggregate, ~1380 GOLD_SCRIPT nodes) | `NO-INSTRUMENT-EVER` | `INSTRUMENT-CANNOT-SEE` | **unchanged** | MONITORED_VS_SERVED.md sec.3c/sec.4; DEPRECATION.md sec.3 (NFRA_REPORT-Z-W1-S1: comp-blast models NO edge GOLD_SCRIPT->Lambda/portal) |
| Cost segment: inf (Pipeline tag) | `UNCHECKED` | `CHECKED` / `BREACH` | **better** | COST_ANOMALY.md sec.1; brief F9 ('cost has no standard so it cannot fail') |
| Cost segment: bd (Pipeline tag) | `UNCHECKED` | `CHECKED` / `BREACH` | **better** | COST_ANOMALY.md sec.1 |
| Cost segment: (untagged) (largest single line, 45% of spend) | `UNCHECKED` | `CHECKED` / `OK` | **better** | COST_ANOMALY.md sec.1 |
| ECS cluster opal-globgrph (compute substrate) | `BLIND` | `CHECKED` / `OK` | **better** | COMPUTE_MANIFEST_FINDINGS.md sec.1; brief F8 ('the manifest is EC2-ONLY -- ECS absent entirely') |
| (ILLUSTRATIVE ONLY -- NOT A LIVE ROW, per ROW_STRUCTURE.md sec.3's own labeling practice) *(ILLUSTRATIVE, NOT LIVE)* | `CHECKED` / `OK` | `BLIND` | **worse** | ROW_STRUCTURE.md sec.3 (worked specimen row 5, explicitly labeled illustrative) |

### Per-row reading (`GENERATED` -- restates only what the table above already carries; delete this subsection and the table is unchanged)

- **Website security (opalinvest.com / www)** -- opalinvest.com/www resolve to a bare EC2 elastic IP with no CloudFront; AWS WAF cannot attach. Andrew's own word: 'we do whatever we can without having to engage with GoDaddy.' Permanent, recorded, not pending. Reading: This edition scores this row UNCHANGED against the cited prior state. (rule1 (both DENY-BY-DESIGN, permanent by design))
- **Blocked-address sentinel row (worked specimen, per STATE_MODEL.md sec.5)** -- Previously: 'no sentinel existed yet.' Now: sentinel_block_armed counts and evaluates hits against the address (Axis1=CHECKED, CAN fire), but no wafv2 IP set enforces the block yet -- 3rd axis renders 'desired' because the enforcement reconciler (TO-OP-S-15-19) is staged, not applied. Reading: This edition scores this row BETTER than the cited prior state. (rule2a (instrument gap closed: BLIND -> CHECKED))
- **opal-login-abuse-alerts (SNS topic)** -- 0 confirmed subscriptions on both reads, same instrument (list-subscriptions-by-topic), a real absence per the positive control (4 of 7 topics DO return non-zero). Reading: This edition scores this row UNCHANGED against the cited prior state. (rule4 (identical INERT both editions))
- **astn-wsjft-alerts (SNS topic)** -- 0 confirmed subscriptions, both reads. Reading: This edition scores this row UNCHANGED against the cited prior state. (rule4 (identical INERT both editions))
- **etfs-reports-alerts (SNS topic)** -- 0 confirmed subscriptions, both reads. Reading: This edition scores this row UNCHANGED against the cited prior state. (rule4 (identical INERT both editions))
- **opal-infrastructure-alerts (SNS topic)** -- Prior investigation explicitly did NOT report this row as healthy past the confirmed-subscription count (UNCHECKED, deliberately not asserted). This session traced past the SNS layer to the SMS sandbox: the one confirmed subscriber's endpoint (+17862617679) is sandbox status Pending, not Verified -- the topic reaches nobody despite showing '1 confirmed subscription'. Reading: This edition scores this row BETTER than the cited prior state. (rule2a (instrument gap closed: UNCHECKED -> CHECKED))
- **inf-otp-alert (SNS topic)** -- Confirmed subscribers exist (lambda, sms) but the SMS leg is dead and the lambda leg's own downstream notification is not traced either session -- Axis2 is honestly UNASSERTED, not OK, on both reads. Reading: This edition scores this row UNCHANGED against the cited prior state. (rule3 (Axis2 and 3rd-axis shown-state both unchanged))
- **opal-critical-surface-alerts (SNS topic)** -- Same shape as inf-otp-alert: sqs+sms legs, sms dead, sqs consumer's own downstream notification untraced either session. Reading: This edition scores this row UNCHANGED against the cited prior state. (rule3 (Axis2 and 3rd-axis shown-state both unchanged))
- **opal-partner-etl-ops-alerts (SNS topic)** -- Same shape: sqs+sms legs, sms dead, sqs consumer's downstream notification untraced either session. Reading: This edition scores this row UNCHANGED against the cited prior state. (rule3 (Axis2 and 3rd-axis shown-state both unchanged))
- **comp (instrument, ruling-12 worked example)** -- CHECKED both editions; found value's rank dropped from DEGRADED(1) to OK(0) -- carries a stale-instrument qualifier, still fully applied. Reading: This edition scores this row BETTER than the cited prior state. (rule3 (Axis2 rank decreased: DEGRADED -> OK))
- **B_01.holdings_lots.py (deprecation candidate)** -- Ruling 6 (age) and the un-walked one-hop check are BOTH the wrong grain (COARSE) for this question. The terminus walk (2-hop, via D_04) confirms ALIVE: reaches ClientsTab/DistributionTab, not speculative. Reading: This edition scores this row BETTER than the cited prior state. (rule2a (instrument gap closed: COARSE -> CHECKED))
- **INF_D_04.client_portal_summary.py (deprecation candidate)** -- Direct terminus, CONFIRMED, not speculative: getPlatinumAdvisorNnaClients -> DistributionTab, getPlatinumFirmDashboard -> ClientsTab, getHeaderMetrics -> PartnerAnalytics/ClientsTab. Reading: This edition scores this row BETTER than the cited prior state. (rule2a (instrument gap closed: COARSE -> CHECKED))
- **INF_D_00.portal_aggregates.py (deprecation candidate)** -- Edition A (EDITION_SPECIMEN.md@5e2131d851) quoted the comp-platinum walk directly (both platinum keys return only [SPECULATIVE] catch-all matches, no confirmed terminus). Edition B does not re-run that walk: it cites RETIREMENT_REGISTER.md's own CARRIED row -- owner, reason and date already recorded there -- and stops there. Still COARSE, still not RETIRED: no resolution is claimed, only that re-derivation is suppressed. Reading: This edition scores this row UNCHANGED against the cited prior state. (rule4 (identical COARSE both editions))
- **INF_D_07.concentration_risk.py (deprecation candidate)** -- Edition A (EDITION_SPECIMEN.md@5e2131d851) quoted the comp-pipescript walk directly (static parser cannot see this script's dynamic-key write at all, surprise row NFRA_REPORT-Z-W1-S2). Edition B does not re-run that walk: it cites RETIREMENT_REGISTER.md's own CARRIED row -- owner, reason and date already recorded there -- and stops there. Still COARSE, still not RETIRED: no resolution is claimed, only that re-derivation is suppressed. Reading: This edition scores this row UNCHANGED against the cited prior state. (rule4 (identical COARSE both editions))
- **CloudFront distribution EVTSA9VEHNZVH (opalinvest.dev / www)** -- 3 of 51 alarms match this distribution's DistributionId dimension structurally. Reading: This edition scores this row BETTER than the cited prior state. (watch-rule-a (no instrument ever existed -> a working check now exists: WATCHED))
- **CloudFront distribution E1DHJH4Y1W8YC2 (no alias; wp-origin target)** -- 0 of 51 alarms match, positive-controlled by the sibling distribution's 3 matches on the identical structural sweep -- a real absence, not a broken probe. Reading: This edition scores this row BETTER than the cited prior state. (watch-rule-a (no instrument ever existed -> a working check now exists: UNWATCHED-CONFIRMED))
- **opal-session-analytics-api (API Gateway, LIVE-no-DECLARED)** -- 4 of 51 alarms match by name/ID substring (errors, estimated-monthly-cost, high-invocations, throttles). Reading: This edition scores this row BETTER than the cited prior state. (watch-rule-a (no instrument ever existed -> a working check now exists: WATCHED))
- **sentiment-query-api (API Gateway, LIVE-no-DECLARED)** -- 0 of 51 alarms match (weaker, substring method; still positive-controlled by session-analytics's 4 matches on the identical method). Reading: This edition scores this row BETTER than the cited prior state. (watch-rule-a (no instrument ever existed -> a working check now exists: UNWATCHED-CONFIRMED))
- **trade-submission-api (API Gateway, LIVE-no-DECLARED, financially consequential)** -- 0 of 51 alarms match. NFRA_REPORT-Z-S7 (1.0.0_SA_CTO~Z) found the substance is larger than this row alone shows: a live, portal-consumed trade submission AND approval workflow behind this undeclared front door, with a second, DECLARED front door reaching the same handler. Open call at Andrew; nothing built (alerting moratorium armed). Reading: This edition scores this row BETTER than the cited prior state. (watch-rule-a (no instrument ever existed -> a working check now exists: UNWATCHED-CONFIRMED))
- **Gold-layer served surfaces (aggregate, ~1380 GOLD_SCRIPT nodes)** -- Not renderable as WATCHED or UNWATCHED -- the enumerator itself cannot resolve this edge class for ANY gold-layer artifact, alive or dead. 0 of ~1380 resolvable by this method; denominator is what could NOT be resolved, never folded into either confirmed state. Reading: This edition scores this row UNCHANGED against the cited prior state. (watch-rule-b (no instrument before; still no working check now -- the gap has not closed))
- **Cost segment: inf (Pipeline tag)** -- Trailing 30d $16.253/day vs baseline 30d $2.197/day = +639.6%, over the $0.50/day floor -- ANOMALY, rendered as the outside-standard-not-contained family per C-COST-15's own 15% threshold. Reading: This edition scores this row BETTER than the cited prior state. (rule2a (instrument gap closed: UNCHECKED -> CHECKED))
- **Cost segment: bd (Pipeline tag)** -- Trailing 30d $5.641/day vs baseline 30d $4.109/day = +37.3%, over the $0.50/day floor -- ANOMALY. Reading: This edition scores this row BETTER than the cited prior state. (rule2a (instrument gap closed: UNCHECKED -> CHECKED))
- **Cost segment: (untagged) (largest single line, 45% of spend)** -- Trailing 30d $17.623/day vs baseline 30d $18.463/day = -4.5% -- stable, the detector's own negative control on its largest line. Reading: This edition scores this row BETTER than the cited prior state. (rule2a (instrument gap closed: UNCHECKED -> CHECKED))
- **ECS cluster opal-globgrph (compute substrate)** -- aws ecs list-clusters found 1 of 1 live cluster, ACTIVE, FARGATE, 3 of 3 services running -- a compute unit the manifest never named at all. Reading: This edition scores this row BETTER than the cited prior state. (rule2a (instrument gap closed: BLIND -> CHECKED))
- **(ILLUSTRATIVE ONLY -- NOT A LIVE ROW, per ROW_STRUCTURE.md sec.3's own labeling practice)** -- The regression case ROW_STRUCTURE.md itself uses to show the function is structurally CAPABLE of 'worse' -- 'a problem that broke overnight'. Excluded from the top-line VERDICT computation below precisely because it is not real (see compute_verdict). Reading: This edition scores this row WORSE than the cited prior state. (rule2b (instrument gap opened: CHECKED -> BLIND))

---

## 3. A GENERAL, COMPUTED PATTERN THIS EDITION SURFACES (`GENERATED`, grounded in the table above -- delete this section and every fact it names is still readable directly from section 2's table)

**13 of the rows above score `better` because an instrument gap CLOSED this session, not because what it found is good news.** `ROW_STRUCTURE.md`'s rule 2 scores the Axis-1 transition (did a working check start existing) before it ever looks at what that check then found. Three of those rows found a live `BREACH` (`opal-infrastructure-alerts`) or a live cost `ANOMALY` (`inf`, `bd` segments); three found a live, undefended surface (`E1DHJH4Y1W8YC2`, `trade-submission-api`, `sentiment-query-api`). `better` here is never a claim that the underlying surface is now SAFE -- it is a claim that this edition can now SEE it, where the previous state could not. Both facts are rendered on the SAME row, in full: the delta word and the found value sit side by side in section 2's table, never one standing in for the other.

**Declared limit, named rather than hidden:** this composer does not re-run any live AWS read, re-walk `comp-blast`/`comp-pipescript`/`comp-platinum`, or re-execute `comp-find --corpus aws`. Every QUOTED tuple above is round 1's own finding at round 1's own stated vintage (2026-09-09, per each cited document's own vintage line); this script's own "composed at" timestamp above is when the COMPOSITION ran, never a claim that the underlying facts were re-measured at that moment.

---

## 4. STRUCTURAL CAPABILITY FOR `NOTHING` -- reused, not re-derived, from `VERDICT.md` section 3's own labeled hypothetical

`VERDICT.md` section 3 already demonstrates, on a labeled hypothetical table, that the verdict rule is structurally capable of `NOTHING needs Andrew today` -- quoted here rather than re-derived, per the build ladder:

| Row (illustrative, per `VERDICT.md` sec.3) | Axis 1 | Axis 2 | Delta |
|---|---|---|---|
| Website security | `DENY-BY-DESIGN` | -- | `unchanged` |
| Blocked-address sentinel | `CHECKED` | `OK` | `unchanged` |
| `opal-login-abuse-alerts` | `INERT` | -- | `unchanged` |
| `comp` | `CHECKED` | `OK` | `unchanged` |
| `opal-infrastructure-alerts` (repaired) | `CHECKED` | `OK` | `better` |

**COMPUTED, applying section 1's same rule to this hypothetical table: no row is `CHECKED`+`BREACH`; no row's delta is `worse`. VERDICT = "NOTHING needs Andrew today."** This table is not today's real state (today's real VERDICT is section 1, and it is `SOMETHING`) -- it is carried here, labeled, to show the SAME engine that produced today's real `SOMETHING` verdict is not a machine that can only ever say `SOMETHING`.
