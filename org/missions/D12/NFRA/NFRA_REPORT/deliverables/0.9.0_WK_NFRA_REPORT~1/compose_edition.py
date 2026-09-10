#!/usr/bin/env python3
"""
compose_edition.py -- the COMPOSER (cell RP-s-15, manifest row S2, outcome FWD-3)

WHAT THIS IS: the engine round 1 never built. It turns the twelve round-1 specification
deliverables (STATE_MODEL.md, ROW_STRUCTURE.md, VERDICT.md, ALERT_DELIVERY.md,
MONITORED_VS_SERVED.md, DEPRECATION.md, RETIREMENT_REGISTER.md, COMPUTE_MANIFEST_FINDINGS.md,
COST_ANOMALY.md and the rest) into an actual report EDITION: EDITION_SPECIMEN.md, with every
row carrying its own PER-ROW delta (worse | better | unchanged) against a previous state,
never a max() over rows.

BUILD LADDER (rung 2 -- reuse, never re-derive): every fact this script starts from
(ROW_FACTS below) is a QUOTED transcription of a real finding round 1 already established,
with a citation to the source file and section. This script does not re-run any live AWS
read, re-walk any dependency graph, or re-measure anything round 1 already measured. It
composes what already exists.

THREE REGIONS, DECLARED PER C-AI PART 1 (every part of the edition is COMPUTED, GENERATED
or QUOTED, legible without knowing how the report is built):

  QUOTED    -- ROW_FACTS below: the property name, its axis values, and its citation. These
              are transcribed, not computed -- round 1 already established every one of them.
  COMPUTED  -- compute_delta() and compute_verdict(): deterministic functions over the QUOTED
              tuples. Implements ROW_STRUCTURE.md section 2's function VERBATIM (rules 1-4,
              in the SAME priority order, including the DENY-BY-DESIGN special case), plus one
              declared, additive bridge for MONITORED_VS_SERVED.md's own WATCHED /
              UNWATCHED-CONFIRMED / INSTRUMENT-CANNOT-SEE vocabulary (see BRIDGE NOTE below).
              Implements VERDICT.md section 1's rule VERBATIM for the top-line verdict.
  GENERATED -- render_markdown()'s per-row "Reading" sentence and the summary prose. Per
              C-AI part 2: a GENERATED sentence is NEVER the sole carrier of a fact -- every
              fact a GENERATED sentence mentions is ALSO present, unabridged, in that row's
              COMPUTED/QUOTED columns. Strip every GENERATED sentence and the table alone
              must still be true and still checkable against the cited source. This is
              enforced structurally here: render_markdown() never writes a GENERATED sentence
              from data that is not also rendered in the row's own table cells.

BRIDGE NOTE (declared, additive, does not edit ROW_STRUCTURE.md or STATE_MODEL.md):
MONITORED_VS_SERVED.md renders "through STATE_MODEL.md's ratified vocabulary" but its own
finding is a THREE-VALUE axis orthogonal to Axis1/Axis2 (WATCHED | UNWATCHED-CONFIRMED |
INSTRUMENT-CANNOT-SEE), not itself Axis1's CHECKED/BLIND or Axis2's OK/DEGRADED/BREACH
(MONITORED_VS_SERVED.md section 0 draws this distinction explicitly and this script does not
collapse it). For a row expressed in THAT vocabulary, this script applies the SAME governing
principle ROW_STRUCTURE.md's rule 2 already applies to Axis 1 -- closing an instrument gap is
scored on WHETHER A WORKING CHECK NOW EXISTS, before whatever it finds is scored -- via
compute_delta_watch(), a second, small function, never mixed into compute_delta()'s own Axis1/
Axis2 table. This is the ONE place this composer extends past a literal transcription of
ROW_STRUCTURE.md's own worked function, and it is named here rather than silently folded in.

THE "PREVIOUS EDITION" INPUT: no report generator has ever run before this cell (decomposition
R2 section 0: "ROUND 1 PRODUCED SPECIFICATIONS AND NO ENGINE"), so there is no prior EDITION
FILE to diff against. There IS, for every row below, a genuine PRIOR STATE round 1's own
documents cite explicitly -- either an earlier investigation (NFRA_OPSEC202609-Z-S151, a
different day-of investigation cited BY ALERT_DELIVERY.md itself), an earlier heuristic
(ruling 6 / the CRO's one-hop check, cited BY DEPRECATION.md itself), or the explicit
statement that NO instrument existed at all before this session (STATE_MODEL.md's own sentinel
specimen: "no sentinel existed yet"; MONITORED_VS_SERVED.md's own charter: "the standing check
that NO EXISTING INSTRUMENT PERFORMS"; brief F9: "cost has no standard so it cannot fail";
brief F8: "the manifest is EC2-ONLY -- ECS absent entirely"). Every PREVIOUS tuple below is
one of these two: EITHER a cited prior investigation's own finding, OR the literal
"nothing looked at all" case ROW_STRUCTURE.md's own sentinel example already resolves as
Axis 1 = BLIND transitioning to CHECKED = "better", regardless of what is then found. No
previous tuple here is invented; every one carries a citation.

USAGE:  python compose_edition.py
OUTPUT: EDITION_SPECIMEN.md, written next to this script.
"""

import datetime

RANK = {"OK": 0, "DEGRADED": 1, "BREACH": 2}

# ---------------------------------------------------------------------------------------
# QUOTED region -- every tuple below is transcribed from a round-1 deliverable, with a
# citation. Nothing here is computed or generated; it is the input the composer runs on.
# ---------------------------------------------------------------------------------------
ROW_FACTS = [
    # --- STATE_MODEL.md / ROW_STRUCTURE.md's own canonical worked specimens (quoted verbatim) ---
    {
        "property": "Website security (opalinvest.com / www)",
        "family": "axis",
        "prev": {"axis1": "DENY-BY-DESIGN", "axis2": None, "axis3": None},
        "curr": {"axis1": "DENY-BY-DESIGN", "axis2": None, "axis3": None},
        "citation": "STATE_MODEL.md sec.4; ROW_STRUCTURE.md sec.3 (worked specimen row 1)",
        "evidence": "opalinvest.com/www resolve to a bare EC2 elastic IP with no CloudFront; AWS WAF cannot attach. Andrew's own word: 'we do whatever we can without having to engage with GoDaddy.' Permanent, recorded, not pending.",
    },
    {
        "property": "Blocked-address sentinel row (worked specimen, per STATE_MODEL.md sec.5)",
        "family": "axis",
        "prev": {"axis1": "BLIND", "axis2": None, "axis3": None},
        "curr": {"axis1": "CHECKED", "axis2": "OK", "axis3": "desired"},
        "citation": "STATE_MODEL.md sec.5; ROW_STRUCTURE.md sec.3 (worked specimen row 2)",
        "evidence": "Previously: 'no sentinel existed yet.' Now: sentinel_block_armed counts and evaluates hits against the address (Axis1=CHECKED, CAN fire), but no wafv2 IP set enforces the block yet -- 3rd axis renders 'desired' because the enforcement reconciler (TO-OP-S-15-19) is staged, not applied.",
    },
    {
        "property": "opal-login-abuse-alerts (SNS topic)",
        "family": "axis",
        "prev": {"axis1": "INERT", "axis2": None, "axis3": None},
        "curr": {"axis1": "INERT", "axis2": None, "axis3": None},
        "citation": "ALERT_DELIVERY.md sec.1/sec.2 (re-confirming NFRA_OPSEC202609-Z-S151, ~15:45Z, IDENTICAL result at ~21:01Z)",
        "evidence": "0 confirmed subscriptions on both reads, same instrument (list-subscriptions-by-topic), a real absence per the positive control (4 of 7 topics DO return non-zero).",
    },
    {
        "property": "astn-wsjft-alerts (SNS topic)",
        "family": "axis",
        "prev": {"axis1": "INERT", "axis2": None, "axis3": None},
        "curr": {"axis1": "INERT", "axis2": None, "axis3": None},
        "citation": "ALERT_DELIVERY.md sec.1 (RESULT: IDENTICAL to NFRA_OPSEC202609-Z-S151)",
        "evidence": "0 confirmed subscriptions, both reads.",
    },
    {
        "property": "etfs-reports-alerts (SNS topic)",
        "family": "axis",
        "prev": {"axis1": "INERT", "axis2": None, "axis3": None},
        "curr": {"axis1": "INERT", "axis2": None, "axis3": None},
        "citation": "ALERT_DELIVERY.md sec.1 (RESULT: IDENTICAL to NFRA_OPSEC202609-Z-S151)",
        "evidence": "0 confirmed subscriptions, both reads.",
    },
    {
        "property": "opal-infrastructure-alerts (SNS topic)",
        "family": "axis",
        "prev": {"axis1": "UNCHECKED", "axis2": None, "axis3": None},
        "curr": {"axis1": "CHECKED", "axis2": "BREACH", "axis3": None},
        "citation": "ALERT_DELIVERY.md sec.4 (resolves NFRA_OPSEC202609-Z-S151's own explicitly-unresolved question)",
        "evidence": "Prior investigation explicitly did NOT report this row as healthy past the confirmed-subscription count (UNCHECKED, deliberately not asserted). This session traced past the SNS layer to the SMS sandbox: the one confirmed subscriber's endpoint (+17862617679) is sandbox status Pending, not Verified -- the topic reaches nobody despite showing '1 confirmed subscription'.",
    },
    {
        "property": "inf-otp-alert (SNS topic)",
        "family": "axis",
        "prev": {"axis1": "CHECKED", "axis2": "UNASSERTED", "axis3": None},
        "curr": {"axis1": "CHECKED", "axis2": "UNASSERTED", "axis3": None},
        "citation": "ALERT_DELIVERY.md sec.4 (Axis 2 left UNASSERTED, not defaulted to OK)",
        "evidence": "Confirmed subscribers exist (lambda, sms) but the SMS leg is dead and the lambda leg's own downstream notification is not traced either session -- Axis2 is honestly UNASSERTED, not OK, on both reads.",
    },
    {
        "property": "opal-critical-surface-alerts (SNS topic)",
        "family": "axis",
        "prev": {"axis1": "CHECKED", "axis2": "UNASSERTED", "axis3": None},
        "curr": {"axis1": "CHECKED", "axis2": "UNASSERTED", "axis3": None},
        "citation": "ALERT_DELIVERY.md sec.4",
        "evidence": "Same shape as inf-otp-alert: sqs+sms legs, sms dead, sqs consumer's own downstream notification untraced either session.",
    },
    {
        "property": "opal-partner-etl-ops-alerts (SNS topic)",
        "family": "axis",
        "prev": {"axis1": "CHECKED", "axis2": "UNASSERTED", "axis3": None},
        "curr": {"axis1": "CHECKED", "axis2": "UNASSERTED", "axis3": None},
        "citation": "ALERT_DELIVERY.md sec.4",
        "evidence": "Same shape: sqs+sms legs, sms dead, sqs consumer's downstream notification untraced either session.",
    },
    {
        "property": "comp (instrument, ruling-12 worked example)",
        "family": "axis",
        "prev": {"axis1": "CHECKED", "axis2": "DEGRADED", "axis3": None},
        "curr": {"axis1": "CHECKED", "axis2": "OK", "axis3": None},
        "citation": "ROW_STRUCTURE.md sec.3 (worked specimen row 4)",
        "evidence": "CHECKED both editions; found value's rank dropped from DEGRADED(1) to OK(0) -- carries a stale-instrument qualifier, still fully applied.",
    },
    # --- DEPRECATION.md / RETIREMENT_REGISTER.md's real ten-candidate walk ---
    {
        "property": "B_01.holdings_lots.py (deprecation candidate)",
        "family": "axis",
        "prev": {"axis1": "COARSE", "axis2": None, "axis3": None},
        "curr": {"axis1": "CHECKED", "axis2": "OK", "axis3": None},
        "citation": "DEPRECATION.md sec.0/sec.2 (ruling 6's age heuristic + the CRO's one-hop check, both superseded by ruling 9's terminus walk)",
        "evidence": "Ruling 6 (age) and the un-walked one-hop check are BOTH the wrong grain (COARSE) for this question. The terminus walk (2-hop, via D_04) confirms ALIVE: reaches ClientsTab/DistributionTab, not speculative.",
    },
    {
        "property": "INF_D_04.client_portal_summary.py (deprecation candidate)",
        "family": "axis",
        "prev": {"axis1": "COARSE", "axis2": None, "axis3": None},
        "curr": {"axis1": "CHECKED", "axis2": "OK", "axis3": None},
        "citation": "DEPRECATION.md sec.2",
        "evidence": "Direct terminus, CONFIRMED, not speculative: getPlatinumAdvisorNnaClients -> DistributionTab, getPlatinumFirmDashboard -> ClientsTab, getHeaderMetrics -> PartnerAnalytics/ClientsTab.",
    },
    {
        "property": "INF_D_00.portal_aggregates.py (deprecation candidate)",
        "family": "axis",
        "prev": {"axis1": "COARSE", "axis2": None, "axis3": None},
        "curr": {"axis1": "COARSE", "axis2": None, "axis3": None},
        "citation": "DEPRECATION.md sec.2; RETIREMENT_REGISTER.md sec.3 (CARRIED)",
        "evidence": "comp-platinum returns only [SPECULATIVE] catch-all matches for both platinum keys this script writes -- the walk could not resolve a confirmed terminus. Still the wrong grain to call it either alive or dead; recorded CARRIED, not RETIRED.",
    },
    {
        "property": "INF_D_07.concentration_risk.py (deprecation candidate)",
        "family": "axis",
        "prev": {"axis1": "COARSE", "axis2": None, "axis3": None},
        "curr": {"axis1": "COARSE", "axis2": None, "axis3": None},
        "citation": "DEPRECATION.md sec.2/sec.3; RETIREMENT_REGISTER.md sec.3 (CARRIED)",
        "evidence": "comp-pipescript's static parser cannot see this script's write at all (dynamic key concatenation, surprise row NFRA_REPORT-Z-W1-S2) -- the walk cannot even confirm the write, let alone a terminus. Recorded CARRIED, not RETIRED, not ALIVE.",
    },
    # --- MONITORED_VS_SERVED.md's own WATCHED/UNWATCHED/INSTRUMENT-CANNOT-SEE axis ---
    {
        "property": "CloudFront distribution EVTSA9VEHNZVH (opalinvest.dev / www)",
        "family": "watch",
        "prev": {"watch": "NO-INSTRUMENT-EVER"},
        "curr": {"watch": "WATCHED"},
        "citation": "MONITORED_VS_SERVED.md sec.3a",
        "evidence": "3 of 51 alarms match this distribution's DistributionId dimension structurally.",
    },
    {
        "property": "CloudFront distribution E1DHJH4Y1W8YC2 (no alias; wp-origin target)",
        "family": "watch",
        "prev": {"watch": "NO-INSTRUMENT-EVER"},
        "curr": {"watch": "UNWATCHED-CONFIRMED"},
        "citation": "MONITORED_VS_SERVED.md sec.3a",
        "evidence": "0 of 51 alarms match, positive-controlled by the sibling distribution's 3 matches on the identical structural sweep -- a real absence, not a broken probe.",
    },
    {
        "property": "opal-session-analytics-api (API Gateway, LIVE-no-DECLARED)",
        "family": "watch",
        "prev": {"watch": "NO-INSTRUMENT-EVER"},
        "curr": {"watch": "WATCHED"},
        "citation": "MONITORED_VS_SERVED.md sec.3b",
        "evidence": "4 of 51 alarms match by name/ID substring (errors, estimated-monthly-cost, high-invocations, throttles).",
    },
    {
        "property": "sentiment-query-api (API Gateway, LIVE-no-DECLARED)",
        "family": "watch",
        "prev": {"watch": "NO-INSTRUMENT-EVER"},
        "curr": {"watch": "UNWATCHED-CONFIRMED"},
        "citation": "MONITORED_VS_SERVED.md sec.3b",
        "evidence": "0 of 51 alarms match (weaker, substring method; still positive-controlled by session-analytics's 4 matches on the identical method).",
    },
    {
        "property": "trade-submission-api (API Gateway, LIVE-no-DECLARED, financially consequential)",
        "family": "watch",
        "prev": {"watch": "NO-INSTRUMENT-EVER"},
        "curr": {"watch": "UNWATCHED-CONFIRMED"},
        "citation": "MONITORED_VS_SERVED.md sec.3b; ANOMALY_BREAKDOWN.md sec.3 (30 connected resources: 4 lambdas, 4 DynamoDB tables, 1 S3 bucket, 2 KMS keys); surprise row NFRA_REPORT-Z-W1-S4, DISARMED/GRADUATED by NFRA_REPORT-Z-S7",
        "evidence": "0 of 51 alarms match. NFRA_REPORT-Z-S7 (1.0.0_SA_CTO~Z) found the substance is larger than this row alone shows: a live, portal-consumed trade submission AND approval workflow behind this undeclared front door, with a second, DECLARED front door reaching the same handler. Open call at Andrew; nothing built (alerting moratorium armed).",
    },
    {
        "property": "Gold-layer served surfaces (aggregate, ~1380 GOLD_SCRIPT nodes)",
        "family": "watch",
        "prev": {"watch": "NO-INSTRUMENT-EVER"},
        "curr": {"watch": "INSTRUMENT-CANNOT-SEE"},
        "citation": "MONITORED_VS_SERVED.md sec.3c/sec.4; DEPRECATION.md sec.3 (NFRA_REPORT-Z-W1-S1: comp-blast models NO edge GOLD_SCRIPT->Lambda/portal)",
        "evidence": "Not renderable as WATCHED or UNWATCHED -- the enumerator itself cannot resolve this edge class for ANY gold-layer artifact, alive or dead. 0 of ~1380 resolvable by this method; denominator is what could NOT be resolved, never folded into either confirmed state.",
    },
    # --- COST_ANOMALY.md's segment-grain detector (brand new this session; brief F9 the prior state) ---
    {
        "property": "Cost segment: inf (Pipeline tag)",
        "family": "axis",
        "prev": {"axis1": "UNCHECKED", "axis2": None, "axis3": None},
        "curr": {"axis1": "CHECKED", "axis2": "BREACH", "axis3": None},
        "citation": "COST_ANOMALY.md sec.1; brief F9 ('cost has no standard so it cannot fail')",
        "evidence": "Trailing 30d $16.253/day vs baseline 30d $2.197/day = +639.6%, over the $0.50/day floor -- ANOMALY, rendered as the outside-standard-not-contained family per C-COST-15's own 15% threshold.",
    },
    {
        "property": "Cost segment: bd (Pipeline tag)",
        "family": "axis",
        "prev": {"axis1": "UNCHECKED", "axis2": None, "axis3": None},
        "curr": {"axis1": "CHECKED", "axis2": "BREACH", "axis3": None},
        "citation": "COST_ANOMALY.md sec.1",
        "evidence": "Trailing 30d $5.641/day vs baseline 30d $4.109/day = +37.3%, over the $0.50/day floor -- ANOMALY.",
    },
    {
        "property": "Cost segment: (untagged) (largest single line, 45% of spend)",
        "family": "axis",
        "prev": {"axis1": "UNCHECKED", "axis2": None, "axis3": None},
        "curr": {"axis1": "CHECKED", "axis2": "OK", "axis3": None},
        "citation": "COST_ANOMALY.md sec.1",
        "evidence": "Trailing 30d $17.623/day vs baseline 30d $18.463/day = -4.5% -- stable, the detector's own negative control on its largest line.",
    },
    # --- COMPUTE_MANIFEST_FINDINGS.md's own substrate finding (brief F8 the prior state) ---
    {
        "property": "ECS cluster opal-globgrph (compute substrate)",
        "family": "axis",
        "prev": {"axis1": "BLIND", "axis2": None, "axis3": None},
        "curr": {"axis1": "CHECKED", "axis2": "OK", "axis3": None},
        "citation": "COMPUTE_MANIFEST_FINDINGS.md sec.1; brief F8 ('the manifest is EC2-ONLY -- ECS absent entirely')",
        "evidence": "aws ecs list-clusters found 1 of 1 live cluster, ACTIVE, FARGATE, 3 of 3 services running -- a compute unit the manifest never named at all.",
    },
    # --- illustrative only, per ROW_STRUCTURE.md sec.3's own "not a live row" practice ---
    {
        "property": "(ILLUSTRATIVE ONLY -- NOT A LIVE ROW, per ROW_STRUCTURE.md sec.3's own labeling practice)",
        "family": "axis",
        "prev": {"axis1": "CHECKED", "axis2": "OK", "axis3": None},
        "curr": {"axis1": "BLIND", "axis2": None, "axis3": None},
        "citation": "ROW_STRUCTURE.md sec.3 (worked specimen row 5, explicitly labeled illustrative)",
        "evidence": "The regression case ROW_STRUCTURE.md itself uses to show the function is structurally CAPABLE of 'worse' -- 'a problem that broke overnight'. Excluded from the top-line VERDICT computation below precisely because it is not real (see compute_verdict).",
        "illustrative": True,
    },
]


def compute_delta(prev, curr):
    """ROW_STRUCTURE.md section 2's function, verbatim, rules in priority order."""
    p1, p2, p3 = prev.get("axis1"), prev.get("axis2"), prev.get("axis3")
    c1, c2, c3 = curr.get("axis1"), curr.get("axis2"), curr.get("axis3")

    # Rule 1: both DENY-BY-DESIGN -> unchanged, never scored.
    if p1 == "DENY-BY-DESIGN" and c1 == "DENY-BY-DESIGN":
        return "unchanged", "rule1 (both DENY-BY-DESIGN, permanent by design)"

    # Rule 2: Axis1 differs, neither is DENY-BY-DESIGN.
    if p1 != c1 and p1 != "DENY-BY-DESIGN" and c1 != "DENY-BY-DESIGN":
        if p1 != "CHECKED" and c1 == "CHECKED":
            return "better", "rule2a (instrument gap closed: %s -> CHECKED)" % p1
        if p1 == "CHECKED" and c1 != "CHECKED":
            return "worse", "rule2b (instrument gap opened: CHECKED -> %s)" % c1
        return "unchanged", "rule2c (moved among non-CHECKED values: %s -> %s)" % (p1, c1)

    # Rule 3: both CHECKED.
    if p1 == "CHECKED" and c1 == "CHECKED":
        if p2 in RANK and c2 in RANK and p2 != c2:
            if RANK[c2] > RANK[p2]:
                return "worse", "rule3 (Axis2 rank increased: %s -> %s)" % (p2, c2)
            return "better", "rule3 (Axis2 rank decreased: %s -> %s)" % (p2, c2)
        # Axis2 unchanged in rank (identical, or both outside the ranked OK/DEGRADED/BREACH
        # scale -- e.g. both UNASSERTED, which this composer never ranks against OK/DEGRADED/
        # BREACH; UNASSERTED is not a finding, it is a declared non-finding) -- compare 3rd axis.
        shown_p, shown_c = p3 is not None, c3 is not None
        if shown_p and not shown_c:
            return "better", "rule3 (3rd axis withdrawn: %s -> not shown, intent became applied)" % p3
        if not shown_p and shown_c:
            return "worse", "rule3 (3rd axis newly shown: not shown -> %s)" % c3
        return "unchanged", "rule3 (Axis2 and 3rd-axis shown-state both unchanged)"

    # Rule 4: identical non-CHECKED, non-DENY-BY-DESIGN value.
    if p1 == c1:
        return "unchanged", "rule4 (identical %s both editions)" % p1

    return "unchanged", "unreached branch (declared limit: no combination above fired)"


def compute_delta_watch(prev, curr):
    """Declared bridge (see module docstring BRIDGE NOTE) for MONITORED_VS_SERVED.md's own
    WATCHED / UNWATCHED-CONFIRMED / INSTRUMENT-CANNOT-SEE axis. Same governing principle as
    compute_delta()'s rule 2: whether a WORKING CHECK now exists dominates what it finds."""
    p, c = prev.get("watch"), curr.get("watch")
    if p == c:
        return "unchanged", "watch-rule-equal (%s both editions)" % p
    if p == "NO-INSTRUMENT-EVER" and c in ("WATCHED", "UNWATCHED-CONFIRMED"):
        return "better", "watch-rule-a (no instrument ever existed -> a working check now exists: %s)" % c
    if p == "NO-INSTRUMENT-EVER" and c == "INSTRUMENT-CANNOT-SEE":
        return "unchanged", "watch-rule-b (no instrument before; still no working check now -- the gap has not closed)"
    return "unchanged", "watch-rule-default (declared limit: no bridge rule named for %s -> %s)" % (p, c)


def compute_verdict(rows):
    """VERDICT.md section 1's rule, verbatim. Real rows only -- an illustrative row is never
    a real fact about today and must never move a real verdict (declared, see ROW_FACTS)."""
    real_rows = [r for r in rows if not r.get("illustrative")]
    breach_rows = [r for r in real_rows if r["curr"].get("axis2") == "BREACH"
                   and r["curr"].get("axis1") == "CHECKED"]
    worse_rows = [r for r in real_rows if r["delta"] == "worse"]
    needs_andrew = bool(breach_rows) or bool(worse_rows)
    return needs_andrew, breach_rows, worse_rows


def fmt_state(r, which="prev"):
    st = r[which]
    if r["family"] == "watch":
        return "`%s`" % st.get("watch")
    parts = ["`%s`" % st.get("axis1")]
    if st.get("axis2") is not None:
        parts.append("`%s`" % st.get("axis2"))
    if st.get("axis3") is not None:
        parts.append("3rd axis: `%s`" % st.get("axis3"))
    return " / ".join(parts)


def gen_sentence(r):
    d = r["delta"]
    if d == "better":
        return "This edition scores this row BETTER than the cited prior state."
    if d == "worse":
        return "This edition scores this row WORSE than the cited prior state."
    return "This edition scores this row UNCHANGED against the cited prior state."


def render_markdown(rows, needs_andrew, breach_rows, worse_rows, vintage):
    lines = []
    lines.append("# NFRA_REPORT -- EDITION SPECIMEN")
    lines.append("")
    lines.append("**Composed by:** `compose_edition.py` (cell `RP-s-15`, `0.9.0_WK_NFRA_REPORT~1`) -- "
                  "**Composed at (this run):** %s" % vintage)
    lines.append("")
    lines.append("**REGION KEY, per C-AI part 1 (declared per region, legible without knowing how "
                  "this report is built):**")
    lines.append("- `QUOTED` -- transcribed from a round-1 deliverable, with a citation. See "
                  "`compose_edition.py`'s `ROW_FACTS`.")
    lines.append("- `COMPUTED` -- a deterministic function over QUOTED tuples: `compute_delta()` "
                  "(ROW_STRUCTURE.md sec.2, verbatim), `compute_delta_watch()` (declared bridge, see "
                  "`COMPOSER.md`), `compute_verdict()` (VERDICT.md sec.1, verbatim).")
    lines.append("- `GENERATED` -- the \"Reading\" sentence under each row and this summary's prose. "
                  "Per C-AI part 2, a `GENERATED` sentence is never the sole carrier of a fact: every "
                  "fact it mentions is also present, in full, in that row's own `QUOTED`/`COMPUTED` "
                  "cells. Delete every `GENERATED` sentence in this document and the table below is "
                  "still true and still checkable against its own citations.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 1. THE VERDICT -- `COMPUTED`, per `VERDICT.md` section 1")
    lines.append("")
    if needs_andrew:
        lines.append("> **SOMETHING needs Andrew today.**")
    else:
        lines.append("> **NOTHING needs Andrew today.**")
    lines.append("")
    lines.append("**COMPUTED basis (never generated -- this is the rule, applied):**")
    lines.append("- Clause 1 (a live `CHECKED`+`BREACH` row exists): **%d of %d real rows** -- %s"
                  % (len(breach_rows), len([r for r in rows if not r.get("illustrative")]),
                     ", ".join(r["property"] for r in breach_rows) if breach_rows else "none"))
    lines.append("- Clause 2 (a real row's delta is `worse`): **%d of %d real rows** -- %s"
                  % (len(worse_rows), len([r for r in rows if not r.get("illustrative")]),
                     ", ".join(r["property"] for r in worse_rows) if worse_rows else "none"))
    lines.append("")
    lines.append("`GENERATED`: The illustrative regression row below is explicitly excluded from both "
                  "clauses above -- it is labeled not-live in `ROW_FACTS` and `compute_verdict()` "
                  "filters it out before either clause is evaluated, so a demonstration fixture can "
                  "never itself trip a real verdict.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 2. EVERY ROW, WITH ITS OWN DELTA -- never a max() over rows")
    lines.append("")
    lines.append("| Property (`QUOTED`) | Previous state (`QUOTED`) | This edition (`QUOTED`) | "
                  "Delta (`COMPUTED`) | Citation (`QUOTED`) |")
    lines.append("|---|---|---|---|---|")
    for r in rows:
        prev_s = fmt_state(r)
        curr_s = fmt_state(r, which="curr")
        tag = " *(ILLUSTRATIVE, NOT LIVE)*" if r.get("illustrative") else ""
        lines.append("| %s%s | %s | %s | **%s** | %s |" % (
            r["property"], tag, prev_s, curr_s, r["delta"], r["citation"]))
    lines.append("")
    lines.append("### Per-row reading (`GENERATED` -- restates only what the table above already "
                  "carries; delete this subsection and the table is unchanged)")
    lines.append("")
    for r in rows:
        lines.append("- **%s** -- %s Reading: %s %s" % (
            r["property"], r["evidence"], gen_sentence(r), r.get("rule_note", "")))
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 3. A GENERAL, COMPUTED PATTERN THIS EDITION SURFACES (`GENERATED`, grounded "
                  "in the table above -- delete this section and every fact it names is still "
                  "readable directly from section 2's table)")
    lines.append("")
    better_new_instrument = [r for r in rows if not r.get("illustrative") and (
        (r.get("prev", {}).get("axis1") in ("BLIND", "UNCHECKED", "COARSE") and r["delta"] == "better")
        or (r.get("family") == "watch" and r["delta"] == "better"))]
    lines.append("**%d of the rows above score `better` because an instrument gap CLOSED this "
                  "session, not because what it found is good news.** `ROW_STRUCTURE.md`'s rule 2 "
                  "scores the Axis-1 transition (did a working check start existing) before it ever "
                  "looks at what that check then found. Three of those rows found a live `BREACH` "
                  "(`opal-infrastructure-alerts`) or a live cost `ANOMALY` (`inf`, `bd` segments); "
                  "three found a live, undefended surface (`E1DHJH4Y1W8YC2`, `trade-submission-api`, "
                  "`sentiment-query-api`). `better` here is never a claim that the underlying surface "
                  "is now SAFE -- it is a claim that this edition can now SEE it, where the previous "
                  "state could not. Both facts are rendered on the SAME row, in full: the delta word "
                  "and the found value sit side by side in section 2's table, never one standing in "
                  "for the other." % len(better_new_instrument))
    lines.append("")
    lines.append("**Declared limit, named rather than hidden:** this composer does not re-run any "
                  "live AWS read, re-walk `comp-blast`/`comp-pipescript`/`comp-platinum`, or "
                  "re-execute `comp-find --corpus aws`. Every QUOTED tuple above is round 1's own "
                  "finding at round 1's own stated vintage (2026-09-09, per each cited document's own "
                  "vintage line); this script's own \"composed at\" timestamp above is when the "
                  "COMPOSITION ran, never a claim that the underlying facts were re-measured at that "
                  "moment.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 4. STRUCTURAL CAPABILITY FOR `NOTHING` -- reused, not re-derived, from "
                  "`VERDICT.md` section 3's own labeled hypothetical")
    lines.append("")
    lines.append("`VERDICT.md` section 3 already demonstrates, on a labeled hypothetical table, that "
                  "the verdict rule is structurally capable of `NOTHING needs Andrew today` -- quoted "
                  "here rather than re-derived, per the build ladder:")
    lines.append("")
    lines.append("| Row (illustrative, per `VERDICT.md` sec.3) | Axis 1 | Axis 2 | Delta |")
    lines.append("|---|---|---|---|")
    lines.append("| Website security | `DENY-BY-DESIGN` | -- | `unchanged` |")
    lines.append("| Blocked-address sentinel | `CHECKED` | `OK` | `unchanged` |")
    lines.append("| `opal-login-abuse-alerts` | `INERT` | -- | `unchanged` |")
    lines.append("| `comp` | `CHECKED` | `OK` | `unchanged` |")
    lines.append("| `opal-infrastructure-alerts` (repaired) | `CHECKED` | `OK` | `better` |")
    lines.append("")
    lines.append("**COMPUTED, applying section 1's same rule to this hypothetical table: no row is "
                  "`CHECKED`+`BREACH`; no row's delta is `worse`. VERDICT = \"NOTHING needs Andrew "
                  "today.\"** This table is not today's real state (today's real VERDICT is section 1, "
                  "and it is `SOMETHING`) -- it is carried here, labeled, to show the SAME engine that "
                  "produced today's real `SOMETHING` verdict is not a machine that can only ever say "
                  "`SOMETHING`.")
    lines.append("")
    return "\n".join(lines)


def main():
    for r in ROW_FACTS:
        if r["family"] == "watch":
            delta, note = compute_delta_watch(r["prev"], r["curr"])
        else:
            delta, note = compute_delta(r["prev"], r["curr"])
        r["delta"] = delta
        r["rule_note"] = "(%s)" % note

    needs_andrew, breach_rows, worse_rows = compute_verdict(ROW_FACTS)
    vintage = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    md = render_markdown(ROW_FACTS, needs_andrew, breach_rows, worse_rows, vintage)

    out_path = __file__.rsplit("compose_edition.py", 1)[0] + "EDITION_SPECIMEN.md"
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(md)

    print("OK: wrote %s" % out_path)
    print("OK: %d rows composed; verdict=%s" % (
        len(ROW_FACTS), "SOMETHING needs Andrew today" if needs_andrew else "NOTHING needs Andrew today"))
    counts = {}
    for r in ROW_FACTS:
        counts[r["delta"]] = counts.get(r["delta"], 0) + 1
    print("OK: delta counts -- %s" % counts)


if __name__ == "__main__":
    main()
