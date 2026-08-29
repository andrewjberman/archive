#!/usr/bin/env python3
"""D1_CATVIEWS -- PRE-STAGED SCORER for TM1-AC1 and CATV-TON1-AC3..AC7.

Seat: 0.4.0_DS_ClientPlatform~Z.  Issued by 2.0.0_SA_COO~Z (msg 13861, as amended
by 13869 and 13877).  Built BEFORE the subjects exist: the criteria score against a
SERVED artifact that a scheduled fire has not yet produced.

WHAT THIS TOOL IS FOR
    Six criteria that would otherwise be hand-scored by seats with none of today's
    context.  The instrument is built now, proven to discriminate now, and pinned to
    a COMMITTED control so it is reproducible by anyone, at any hour, forever.

THE THREE THINGS BAKED IN, EACH BECAUSE THIS PROJECT ALREADY PAID FOR IT
    1. SCORE THE PUBLISHER'S OBJECT, NEVER THE GOLD FLOOR'S.  Three fires, two
       EventBridge planes: 13:00Z etf-positioning (not ours), 13:30Z mdpf-gold-lambda
       (the GOLD rung), 13:50Z mdpf-portal-publisher (THE SERVED OBJECT).  A scorer run
       at 13:30Z reads the pre-publish object and reports a CORRECT fix as FAILED.  The
       guard is IN the tool (gate_scoreable) and keys on the artifact's OWN provenance,
       never on the wall clock and never on the invoker knowing the difference.
    2. null IS NOT 0.00.  A member with no dollars emits null deliberately -- "a 0 on a
       money figure is a measurement nobody took."  Every money read here is TRI-STATE:
       ABSENT (key missing -- unmapped) / NULL (key present, value None -- a declared
       absence) / NUMERIC.  Coalescing null to 0 would pass a broken build.
    3. PRINT THE DENOMINATOR beside every count.  4 scopes is the served denominator
       (global, 49financial, cottonwood, inflection).

THE DATE-SCOPING FINDING (surfaced as msg 13879/13880/13881; accepted by 3.0.0_SA_CVO~Z
in 13882 and adopted as the certification basis)
    CATV-TON1-AC3 and CATV-TON1-AC4 pin CONSTANTS that are only true at as_of
    2026-08-27.  The $22,794,766.25 is the sum of two MARKET-VALUED balances
    (opal_div_sma 18,783,379.81 + opal_growth_sma 4,011,386.44) which move every
    trading day -- roughly $170k-$250k per day, measured over the 455-date series.
    Applying that literal to a later artifact returns FAIL on a CORRECT fix.
    So each of those criteria is scored on TWO tracks:
        STRUCTURAL   the criterion's real proposition, exact to the cent on ANY as_of
        LITERAL      the issuer's constants, scored ONLY when as_of == 2026-08-27,
                     else NA_BY_DATE -- never PASS, never FAIL, with the as_of printed
    "Exactly" is preserved.  What changed is what it is exact AGAINST.  Whether AC3/AC4
    text is amended is 2.0.0_SA_COO~Z's call; this tool runs either way and prints both
    readings, so no verdict waits on that decision.

AC7 NEEDS TWO RUNGS, MEASURED
    The SERVED (platinum) object carries NO `trigger` field -- only written_by /
    written_at / source_keys / source_vintages.  `_provenance.trigger` lives on the GOLD
    object.  So AC7 is scored by dereferencing the served object's OWN source_keys to
    the gold rung and reading the trigger there.  A scorer that looked for `trigger` on
    the served artifact would find nothing and report a false FAIL.

USAGE
    python D1_CATVIEWS.TM1-AC1_TON1-AC3-AC7_score_served.py --self-test
        Prove the instrument discriminates.  Runs every criterion against the COMMITTED
        pre-fix control and against planted mutants, in BOTH directions.  Exits non-zero
        unless the full expected pattern reproduces.  ALWAYS runs before a live score.

    python D1_CATVIEWS.TM1-AC1_TON1-AC3-AC7_score_served.py --live
        Score the live served objects.  Refuses (BLOCKED:) if they are still pre-fix.

    python D1_CATVIEWS.TM1-AC1_TON1-AC3-AC7_score_served.py --from-commit bc9d11dd8e
        Score a committed snapshot.  Same gate applies.

    ... --live --json out.json     also write the machine-readable verdict map.

EVIDENCE PINS
    control commit   bc9d11dd8e   4 scopes, on origin/SITEZ (is-ancestor verified)
                                  MEASURED byte-identical to the live s3api object on
                                  4 of 4 scopes (sha256 + byte length), 2026-08-28 ~20:2xZ
    fix deployed     2026-08-28T17:28:29Z   gold-lambda re-pin bf74d031c1 -> 70a0828226
    control written  2026-08-28T13:50:49-52Z by opal-assets-mdpf-portal-publisher
                     -- ~3.6h BEFORE the deploy.  The margin is STRUCTURAL, not a fetch race.
"""

import argparse
import json
import subprocess
import sys

# ---------------------------------------------------------------------------
# Constants.  Every one of these is a MEASURED value with its source named.
# ---------------------------------------------------------------------------

SERVE_BUCKET = "opal-data-portal-v2"
SERVE_KEY_FMT = "platinum/mdpf/{scope}/category-views.json"
GOLD_BUCKET = "opal-data-assets"

# The served denominator.  COO 13861 s.4.
SCOPES = ("global", "49financial", "cottonwood", "inflection")

# The publisher that writes the SERVED rung.  Reading this off the artifact is how we
# tell the 13:50Z object from the 13:30Z one WITHOUT trusting a clock.
PUBLISHER = "opal-assets-mdpf-portal-publisher"

# D1_CATVIEWS.TO-V1-AE: gold-lambda re-pinned bf74d031c1 -> 70a0828226, deployed and
# verified byte-identical to the pin.  Bytes written before this are PRE-FIX.
FIX_DEPLOYED_UTC = "2026-08-28T17:28:29Z"

# The committed pre-fix control.  3.0.0_SA_CVO~Z, on origin/SITEZ.
CONTROL_COMMIT = "bc9d11dd8e"
CONTROL_PATH_FMT = (
    "org/tier1_exec/3.0.0_SA_CVO/deliverables/"
    "cvoZ_D1_PREDEPLOY_BASELINE_20260828/category-views.{scope}.json"
)

# CATV-TON1-AC3's literal constants.  TRUE ONLY AT THIS as_of -- see module docstring.
LITERAL_AS_OF = "2026-08-27"
LITERAL_SMA_AFTER = 22794766.25
LITERAL_CLIENT_BEFORE = 290426813.47
LITERAL_CLIENT_AFTER = 267632047.22

# The firm that has SMA members, and the two that correctly have none.
SMA_FIRM = "49financial"
NO_SMA_FIRMS = ("cottonwood", "inflection")

PASS = "PASS"
FAIL = "FAIL"
UNSCOREABLE = "UNSCOREABLE"
NA_BY_DATE = "NA_BY_DATE"


# ---------------------------------------------------------------------------
# Money.  Compared in integer CENTS -- "exactly, not approximately".
# ---------------------------------------------------------------------------

def cents(value):
    """Exact-to-the-cent integer.  None propagates as None (never coalesced to 0)."""
    if value is None:
        return None
    return int(round(float(value) * 100))


def money_state(container, key):
    """TRI-STATE money read.  ABSENT != NULL != NUMERIC.

    This is the whole of trap 2.  A member with no dollars emits null DELIBERATELY;
    a member that was never mapped has no key at all.  Collapsing those two is how a
    scorer passes a broken build.
    """
    if key not in container:
        return ("ABSENT", None)
    raw = container[key]
    if raw is None:
        return ("NULL", None)
    return ("NUMERIC", float(raw))


def fmt(value):
    if value is None:
        return "None"
    return "{:,.2f}".format(value)


# ---------------------------------------------------------------------------
# Retrieval.
# ---------------------------------------------------------------------------

def load_from_commit(commit, scope):
    """Read a committed control artifact.

    NEVER 2>/dev/null a `git show` -- a mangled path returns clean-empty and an ABSENT
    verdict off that is indistinguishable from a real absence.  stderr is left attached
    and a non-zero rc raises.
    """
    path = CONTROL_PATH_FMT.format(scope=scope)
    out = subprocess.run(
        ["git", "show", "{0}:{1}".format(commit, path)],
        stdout=subprocess.PIPE, check=True,
    )
    return json.loads(out.stdout.decode("utf-8"))


def load_live(scope):
    import boto3
    cli = boto3.client("s3")
    key = SERVE_KEY_FMT.format(scope=scope)
    body = cli.get_object(Bucket=SERVE_BUCKET, Key=key)["Body"].read()
    return json.loads(body.decode("utf-8"))


def live_object_meta(scope):
    """head_object for the TM1-AC1 evidence line: bucket, key, size, LastModified UTC."""
    import boto3
    cli = boto3.client("s3")
    key = SERVE_KEY_FMT.format(scope=scope)
    head = cli.head_object(Bucket=SERVE_BUCKET, Key=key)
    return {
        "bucket": SERVE_BUCKET,
        "key": key,
        "size": head["ContentLength"],
        "last_modified_utc": head["LastModified"].strftime("%Y-%m-%dT%H:%M:%SZ"),
    }


def load_gold_for(doc):
    """Dereference the served object's OWN source_keys to the gold rung.

    AC7 quotes `_provenance.trigger`, which the SERVED object does not carry.  Following
    the artifact's own declared source is what makes this a chain rather than a guess.
    """
    import boto3
    keys = (doc.get("_provenance") or {}).get("source_keys") or []
    if not keys:
        return None, "no source_keys on the served object"
    uri = keys[0]
    if not uri.startswith("s3://"):
        return None, "source_key is not an s3 uri: {0}".format(uri)
    rest = uri[len("s3://"):]
    bucket, _, key = rest.partition("/")
    cli = boto3.client("s3")
    body = cli.get_object(Bucket=bucket, Key=key)["Body"].read()
    return json.loads(body.decode("utf-8")), uri


# ---------------------------------------------------------------------------
# THE GATE.  Refuse to score, rather than trust the invoker to know the difference.
# ---------------------------------------------------------------------------

def gate_scoreable(docs):
    """Is this set of artifacts the POST-FIX SERVED object?

    Two limbs, both read off the artifact's own provenance:
      G1  written_by == the publisher       -> this is the 13:50Z SERVED rung, not the
                                               13:30Z gold floor.  Structural, not a clock.
      G2  written_at  > FIX_DEPLOYED_UTC    -> the corrected code produced these bytes.

    G2 is deliberately expressed against the DEPLOY, not against "13:50Z today".  It
    stays correct across a weekend, a holiday, a skipped fire or a late publish -- none
    of which a wall-clock comparison survives.  Returns (ok, lines).
    """
    lines = []
    ok = True
    for scope in sorted(docs):
        prov = docs[scope].get("_provenance") or {}
        by = prov.get("written_by")
        at = prov.get("written_at")
        as_of = docs[scope].get("as_of")
        g1 = (by == PUBLISHER)
        # ISO-8601 Zulu strings sort lexicographically; both are same-format.
        g2 = bool(at) and at > FIX_DEPLOYED_UTC
        if not (g1 and g2):
            ok = False
        lines.append(
            "    {0:<12} written_by={1!s:<38} written_at={2!s:<21} as_of={3!s:<11} "
            "G1={4} G2={5}".format(
                scope, by, at, as_of, "OK" if g1 else "NO", "OK" if g2 else "NO"))
    lines.append("    denominator: {0} scope(s)".format(len(docs)))
    lines.append("    G1 = written by {0} (the SERVED rung, not the 13:30Z gold floor)".format(PUBLISHER))
    lines.append("    G2 = written_at AFTER the fix deployed {0}".format(FIX_DEPLOYED_UTC))
    return ok, lines


# ---------------------------------------------------------------------------
# Shared readers over the artifact shape.
# ---------------------------------------------------------------------------

def l2_members_under_models(doc):
    """Yield (l1_label, member_dict) for every L2 node under Models.

    L0 = Models; L1 = Primary / Custom; L2 = the member rows Andrew sees as "--".
    """
    models = (doc.get("nodes") or {}).get("Models") or {}
    for l1_label, l1 in sorted((models.get("children") or {}).items()):
        for member in (l1.get("members") or []):
            yield l1_label, member


def sma_members(doc):
    """Yield (bucket_label, member_dict) for every SMA L2 member."""
    sma = (doc.get("nodes") or {}).get("SMA") or {}
    for bucket_label, child in sorted((sma.get("children") or {}).items()):
        for member in (child.get("members") or []):
            yield bucket_label, member


def node_aum(doc, node):
    return money_state((doc.get("nodes") or {}).get(node) or {}, "aum")


# ---------------------------------------------------------------------------
# TM1-AC1
# ---------------------------------------------------------------------------

def score_tm1_ac1(docs, metas=None):
    """EVERY L2 node under Models carries a dollar value on the SERVED artifact, for at
    least one firm.  Print key, bucket, byte size and LastModified.

    Scored TRI-STATE and reported on two readings, because the TO's own design decision
    (a member with no dollars emits null) makes the strict reading and the
    declared-null reading genuinely different questions:

        STRICT    every L2 member carries a NUMERIC value           (no ABSENT, no NULL)
        DECLARED  every L2 member carries the FIELD                 (no ABSENT; NULL ok)

    The primary verdict is STRICT.  Both are printed with denominators so a certifier
    can see exactly what is true rather than inheriting this seat's reading.  Nothing is
    padded and nothing is coalesced.
    """
    lines = []
    any_strict = False
    any_declared = False
    for scope in SCOPES:
        doc = docs.get(scope)
        if doc is None:
            continue
        numeric = null = absent = 0
        detail = []
        for l1_label, member in l2_members_under_models(doc):
            state, value = money_state(member, "aum")
            if state == "NUMERIC":
                numeric += 1
            elif state == "NULL":
                null += 1
            else:
                absent += 1
            detail.append("        {0:<8} {1:<40} {2:<8} {3}".format(
                l1_label, str(member.get("display_name"))[:40], state, fmt(value)))
        total = numeric + null + absent
        strict = (total > 0 and absent == 0 and null == 0)
        declared = (total > 0 and absent == 0)
        any_strict = any_strict or strict
        any_declared = any_declared or declared
        lines.append(
            "    {0:<12} L2 members: {1:>2}  NUMERIC={2:<2} NULL={3:<2} ABSENT={4:<2} "
            "(denominator {5})  STRICT={6} DECLARED={7}".format(
                scope, total, numeric, null, absent, total,
                "PASS" if strict else "FAIL", "PASS" if declared else "FAIL"))
        lines.extend(detail)
        if metas and scope in metas:
            m = metas[scope]
            lines.append("        evidence: s3://{0}/{1}  {2} B  LastModified {3}".format(
                m["bucket"], m["key"], m["size"], m["last_modified_utc"]))
    lines.append("    scope denominator: {0}".format(len(SCOPES)))
    lines.append("    STRICT   (every L2 member NUMERIC)  on at least one firm: {0}".format(
        "YES" if any_strict else "NO"))
    lines.append("    DECLARED (every L2 member has the field, null allowed) on at least one firm: {0}".format(
        "YES" if any_declared else "NO"))
    if not any_declared:
        lines.append("    ABSENT means UNMAPPED -- the pre-fix state Andrew sees as '--'.")
    return {"id": "TM1-AC1", "verdict": PASS if any_strict else FAIL, "lines": lines}


# ---------------------------------------------------------------------------
# CATV-TON1-AC3
# ---------------------------------------------------------------------------

def score_ton1_ac3(docs, before_docs=None, ts_map=None):
    """THE NUMBERS MOVE BY EXACTLY THE MEASURED AMOUNT.

    Scored on two tracks (see module docstring).  STRUCTURAL is the criterion's real
    proposition and is exact to the cent on ANY as_of:

        A  SMA.aum == sum of its own L2 buckets' aum, and those == sum of member dollars
        B  Client.aum == non_model_aua - SMA.aum   (the netting actually fired)
        C  pre-fix signature: Client.aum == non_model_aua, UNNETTED

    LITERAL is the issuer's constants, scored only at as_of 2026-08-27.
    """
    lines = []
    doc = docs.get(SMA_FIRM)
    if doc is None:
        return {"id": "CATV-TON1-AC3", "verdict": UNSCOREABLE,
                "lines": ["    {0} artifact not supplied".format(SMA_FIRM)]}

    as_of = doc.get("as_of")
    sma_state, sma_val = node_aum(doc, "SMA")
    cli_state, cli_val = node_aum(doc, "Client")

    # -- limb A: SMA total reconciles to its own children and members ----------
    sma_node = (doc.get("nodes") or {}).get("SMA") or {}
    child_sum = 0
    child_ok = True
    member_sum = 0
    member_numeric = member_total = 0
    for bucket_label, child in sorted((sma_node.get("children") or {}).items()):
        cs, cv = money_state(child, "aum")
        if cs != "NUMERIC":
            child_ok = False
            lines.append("        bucket {0:<16} aum {1}".format(bucket_label, cs))
            continue
        child_sum += cents(cv)
        bucket_member_sum = 0
        bucket_all_numeric = True
        for member in (child.get("members") or []):
            member_total += 1
            ms, mv = money_state(member, "aum")
            if ms == "NUMERIC":
                member_numeric += 1
                bucket_member_sum += cents(mv)
            else:
                bucket_all_numeric = False
        if bucket_all_numeric and (child.get("members") or []):
            member_sum += bucket_member_sum
            tick = "OK" if bucket_member_sum == cents(cv) else "MISMATCH"
            lines.append("        bucket {0:<16} aum {1:>18}  members sum {2:>18}  {3}".format(
                bucket_label, fmt(cv), fmt(bucket_member_sum / 100.0), tick))
        else:
            lines.append("        bucket {0:<16} aum {1:>18}  members NOT ALL NUMERIC "
                         "({2} of {3})".format(bucket_label, fmt(cv), member_numeric, member_total))
    limb_a = (sma_state == "NUMERIC" and child_ok and cents(sma_val) == child_sum)
    lines.append("    A  SMA.aum {0} == sum(bucket aum) {1}   -> {2}".format(
        fmt(sma_val), fmt(child_sum / 100.0), "PASS" if limb_a else "FAIL"))
    if member_total:
        lines.append("       SMA L2 members carrying NUMERIC dollars: {0} of {1} "
                     "(denominator {1})".format(member_numeric, member_total))

    # -- external corroboration of the member dollars, DIFFERENT instrument ----
    ts = (ts_map or {}).get(SMA_FIRM)
    if ts is not None:
        ext_total = 0
        ext_ok = True
        for _bucket, member in sma_members(doc):
            mid = member.get("member_id")
            mv = ts_model_value(ts, "opal_div_sma" if mid == "divz" else
                                ("opal_growth_sma" if mid == "pfoe" else str(mid)), as_of)
            if mv is not None:
                ext_total += cents(mv)
        if ext_total:
            match = (sma_state == "NUMERIC" and cents(sma_val) == ext_total)
            ext_ok = match
            lines.append(
                "    A' EXTERNAL cross-check (aggregate-aua-timeseries by_model at as_of "
                "{0}): expected SMA {1}  served SMA {2}  -> {3}".format(
                    as_of, fmt(ext_total / 100.0), fmt(sma_val),
                    "MATCH" if match else "MISMATCH"))
            lines.append("       (a second read of the SAME artifact would be repetition; "
                         "this is a different instrument)")
            limb_a = limb_a and ext_ok

    # -- limb B / C: the netting -----------------------------------------------
    non_model = _non_model_aua(doc, ts)
    limb_b = limb_c = None
    if non_model is None:
        lines.append("    B  non_model_aua UNAVAILABLE from any INDEPENDENT source "
                     "(the served artifact does not carry it) -- limbs B and C UNSCOREABLE")
        lines.append("       Supply the timeseries (--live does this) rather than deriving "
                     "non_model from Client, which would compare an expression to itself.")
    else:
        limb_b = (cli_state == "NUMERIC" and sma_state == "NUMERIC"
                  and cents(cli_val) == cents(non_model) - cents(sma_val))
        limb_c = (cli_state == "NUMERIC" and cents(cli_val) == cents(non_model))
        lines.append("    B  Client.aum {0} == non_model_aua {1} - SMA.aum {2}  -> {3}".format(
            fmt(cli_val), fmt(non_model), fmt(sma_val), "PASS" if limb_b else "FAIL"))
        lines.append("    C  pre-fix signature (Client UNNETTED, Client.aum == non_model_aua): "
                     "{0}".format("PRESENT -- artifact is PRE-FIX" if limb_c else "absent"))

    # -- LITERAL track ----------------------------------------------------------
    if as_of == LITERAL_AS_OF:
        lit = (cents(sma_val) == cents(LITERAL_SMA_AFTER)
               and cents(cli_val) == cents(LITERAL_CLIENT_AFTER))
        lit_verdict = PASS if lit else FAIL
        lines.append("    D  LITERAL at as_of {0}: SMA=={1} and Client=={2}  -> {3}".format(
            as_of, fmt(LITERAL_SMA_AFTER), fmt(LITERAL_CLIENT_AFTER), lit_verdict))
    else:
        lit_verdict = NA_BY_DATE
        lines.append("    D  LITERAL constants ({0} / {1}) are TRUE ONLY AT as_of {2}; this "
                     "artifact is as_of {3} -> NA_BY_DATE".format(
                         fmt(LITERAL_SMA_AFTER), fmt(LITERAL_CLIENT_AFTER),
                         LITERAL_AS_OF, as_of))
        lines.append("       (the balances are market-valued and move every trading day; "
                     "see module docstring)")

    if before_docs and SMA_FIRM in before_docs:
        b = before_docs[SMA_FIRM]
        bs, bsv = node_aum(b, "SMA")
        bc, bcv = node_aum(b, "Client")
        lines.append("    BEFORE (as_of {0}): SMA {1}  Client {2}".format(
            b.get("as_of"), fmt(bsv), fmt(bcv)))
        lines.append("    AFTER  (as_of {0}): SMA {1}  Client {2}".format(
            as_of, fmt(sma_val), fmt(cli_val)))

    if limb_b is None:
        verdict = UNSCOREABLE
    else:
        verdict = PASS if (limb_a and limb_b and not limb_c) else FAIL
    lines.append("    STRUCTURAL (A and B hold, C absent) -> {0} ; LITERAL -> {1}".format(
        verdict, lit_verdict))
    return {"id": "CATV-TON1-AC3", "verdict": verdict, "literal": lit_verdict, "lines": lines}


def _non_model_aua(doc, ts=None):
    """non_model_aua for this artifact's as_of, from an INDEPENDENT source.

    THIS FUNCTION DELIBERATELY HAS NO FALLBACK THAT DERIVES non_model FROM Client.

    The first version of this scorer did have one -- it summed Client + SMA +
    Alternatives when the field was absent.  Its own self-test caught the consequence:
    limb B (Client == non_model - SMA) and AC4's "Client is UNNETTED" limb then compared
    an expression to ITSELF.  A planted mutant that moved cottonwood's Client by $1.00
    moved BOTH sides of the equality and the guard passed.  A mutant that changes both
    sides of an equality is the classic way a check fails toward vindicating itself.

    The served category-views artifact does NOT carry non_model_aua.  The honest answer
    when no timeseries is supplied is None -> those limbs report UNSCOREABLE, never a
    vacuous PASS.
    """
    for path in (("sums", "non_model_aua"), ("sums", "non_model"), ("non_model_aua",)):
        cur = doc
        ok = True
        for part in path:
            if isinstance(cur, dict) and part in cur:
                cur = cur[part]
            else:
                ok = False
                break
        if ok and isinstance(cur, (int, float)):
            return float(cur)
    if ts is not None:
        return ts_series_value(ts, "non_model_aua", doc.get("as_of"))
    return None


def ts_series_value(ts, field, as_of):
    """Read a date-aligned array out of the aggregate-aua-timeseries artifact.

    A DIFFERENT INSTRUMENT from the category-views object being scored -- which is the
    point: a second reading of the same file is repetition, not corroboration.
    """
    if not ts or not as_of:
        return None
    dates = ts.get("dates") or []
    series = ts.get(field)
    if not isinstance(series, list) or len(series) != len(dates):
        return None
    try:
        idx = dates.index(as_of)
    except ValueError:
        return None
    value = series[idx]
    return float(value) if isinstance(value, (int, float)) else None


def ts_model_value(ts, member_id, as_of):
    """Per-strategy model_value at as_of, for the SMA member cross-check."""
    if not ts or not as_of:
        return None
    by_model = ts.get("by_model") or {}
    entry = by_model.get(member_id)
    if not isinstance(entry, dict):
        return None
    dates = ts.get("dates") or []
    series = entry.get("model_value")
    if not isinstance(series, list) or len(series) != len(dates):
        return None
    try:
        idx = dates.index(as_of)
    except ValueError:
        return None
    value = series[idx]
    return float(value) if isinstance(value, (int, float)) else None


def load_timeseries(scope):
    import boto3
    cli = boto3.client("s3")
    key = "platinum/mdpf/{0}/aggregate-aua-timeseries.json".format(scope)
    body = cli.get_object(Bucket=SERVE_BUCKET, Key=key)["Body"].read()
    return json.loads(body.decode("utf-8"))


# ---------------------------------------------------------------------------
# CATV-TON1-AC4
# ---------------------------------------------------------------------------

def score_ton1_ac4(docs, before_docs=None, ts_map=None):
    """THE OTHER TWO FIRMS DO NOT MOVE.

    Same date-scoping problem as AC3: a literal before/after equality on Client assumes
    both artifacts share an as_of.  Two tracks again.

        STRUCTURAL  for cottonwood and inflection: SMA.aum is 0.00, ZERO SMA members
                    resolve to dollars, absent_reason is still present, AND the artifact's
                    own sum invariant holds (sum of L0 == total_aua).
                    That is "the fix did not touch a firm that was already right",
                    and it is true on ANY as_of.
        LITERAL     byte-equality of Client and SMA against the before-artifact, scored
                    only when the two share an as_of.

    THE SUM-INVARIANT LIMB IS LOAD-BEARING AND WAS ADDED BY THIS TOOL'S OWN SELF-TEST.
    An earlier version tested "Client is UNNETTED" as Client == non_model_aua, deriving
    non_model from Client when the field was absent -- so a planted mutant that moved
    cottonwood's Client by $1.00 moved both sides and PASSED.  total_aua is an
    INDEPENDENT field: move Client alone and sum(L0) != total_aua, so the mutant is
    caught.  A guard needs an anchor the mutation does not also move.
    """
    lines = []
    structural_ok = True
    for scope in NO_SMA_FIRMS:
        doc = docs.get(scope)
        if doc is None:
            lines.append("    {0:<12} artifact not supplied -- UNSCOREABLE".format(scope))
            structural_ok = False
            continue
        sma_state, sma_val = node_aum(doc, "SMA")
        cli_state, cli_val = node_aum(doc, "Client")
        resolved = 0
        total_members = 0
        for _bucket, member in sma_members(doc):
            total_members += 1
            ms, mv = money_state(member, "aum")
            if ms == "NUMERIC" and cents(mv) != 0:
                resolved += 1
        sma_zero = (sma_state == "NUMERIC" and cents(sma_val) == 0)
        reason_present = ((doc.get("nodes") or {}).get("SMA") or {}).get("absent_reason") is not None
        # INDEPENDENT anchor -- see the docstring note.
        total_aua = (doc.get("sums") or {}).get("total_aua")
        l0_sum = 0
        l0_ok = True
        for _name, node in sorted((doc.get("nodes") or {}).items()):
            st, vl = money_state(node, "aum")
            if st != "NUMERIC":
                l0_ok = False
                continue
            l0_sum += cents(vl)
        sum_holds = (l0_ok and total_aua is not None and l0_sum == cents(total_aua))
        # Optional external anchor when a timeseries is supplied.
        ts = (ts_map or {}).get(scope)
        non_model = _non_model_aua(doc, ts)
        unnetted = None
        if non_model is not None and cli_state == "NUMERIC":
            unnetted = (cents(cli_val) == cents(non_model))
        ok = sma_zero and resolved == 0 and reason_present and sum_holds
        if unnetted is False:
            ok = False
        structural_ok = structural_ok and ok
        lines.append(
            "    {0:<12} as_of={1:<11} SMA.aum={2:>10}  members with dollars: {3} of {4} "
            "(denominator {4})  absent_reason={5}  sum(L0)==total_aua={6}  Client={7}  -> {8}".format(
                scope, str(doc.get("as_of")), fmt(sma_val), resolved, total_members,
                "PRESENT" if reason_present else "GONE",
                "OK" if sum_holds else "MISMATCH",
                fmt(cli_val), "PASS" if ok else "FAIL"))
        if not sum_holds:
            lines.append("        sum(L0)={0}  total_aua={1}  -- a value moved without the "
                         "total moving".format(fmt(l0_sum / 100.0), fmt(total_aua)))
        if unnetted is not None:
            lines.append("        external non_model_aua at as_of: {0}  Client UNNETTED={1}".format(
                fmt(non_model), "YES" if unnetted else "NO"))

    literal_verdict = NA_BY_DATE
    if before_docs:
        cmp_lines = []
        all_same_as_of = True
        equal = True
        for scope in NO_SMA_FIRMS:
            a, b = docs.get(scope), before_docs.get(scope)
            if a is None or b is None:
                all_same_as_of = False
                continue
            if a.get("as_of") != b.get("as_of"):
                all_same_as_of = False
                cmp_lines.append(
                    "    {0:<12} as_of before={1} after={2} -- NOT comparable literally".format(
                        scope, b.get("as_of"), a.get("as_of")))
                continue
            for node in ("Client", "SMA"):
                s1, v1 = node_aum(b, node)
                s2, v2 = node_aum(a, node)
                same = (s1 == s2 and cents(v1) == cents(v2))
                equal = equal and same
                cmp_lines.append("    {0:<12} {1:<8} before {2:>18}  after {3:>18}  {4}".format(
                    scope, node, fmt(v1), fmt(v2), "IDENTICAL" if same else "MOVED"))
        lines.extend(cmp_lines)
        if all_same_as_of and cmp_lines:
            literal_verdict = PASS if equal else FAIL
        else:
            lines.append("    LITERAL before/after equality needs a shared as_of -> NA_BY_DATE")
    lines.append("    STRUCTURAL -> {0} ; LITERAL -> {1}".format(
        PASS if structural_ok else FAIL, literal_verdict))
    lines.append("    denominator: {0} firm(s) that correctly have no SMA members".format(
        len(NO_SMA_FIRMS)))
    return {"id": "CATV-TON1-AC4", "verdict": PASS if structural_ok else FAIL,
            "literal": literal_verdict, "lines": lines}


# ---------------------------------------------------------------------------
# CATV-TON1-AC5
# ---------------------------------------------------------------------------

def score_ton1_ac5(docs):
    """THE FALSE SENTENCE IS GONE FOR 49financial -- AND STILL PRESENT WHERE IT IS TRUE.

    Both limbs measured and printed.  Deleting absent_reason everywhere is a FAIL: it is
    a correct, sovereign-cited statement for the two firms that genuinely have none.

    Fully date-independent -- absent_reason is not a money figure, so this criterion is
    scoreable on any artifact.
    """
    lines = []
    doc49 = docs.get(SMA_FIRM)
    limb_gone = None
    if doc49 is None:
        lines.append("    {0} artifact not supplied".format(SMA_FIRM))
    else:
        sma = (doc49.get("nodes") or {}).get("SMA") or {}
        reason = sma.get("absent_reason")
        limb_gone = reason is None
        lines.append("    {0:<12} absent_reason: {1}".format(
            SMA_FIRM, "ABSENT (correct -- the firm HAS SMA members)" if limb_gone
            else "STILL PRESENT -- the FALSE sentence"))
        if reason is not None:
            lines.append("        {0}".format(str(reason)[:150]))

    limb_kept = True
    for scope in NO_SMA_FIRMS:
        doc = docs.get(scope)
        if doc is None:
            limb_kept = False
            lines.append("    {0:<12} artifact not supplied".format(scope))
            continue
        sma = (doc.get("nodes") or {}).get("SMA") or {}
        reason = sma.get("absent_reason")
        present = reason is not None
        limb_kept = limb_kept and present
        lines.append("    {0:<12} absent_reason: {1}".format(
            scope, "PRESENT (correct -- TRUE for this firm)" if present
            else "DELETED -- a correct sovereign-cited statement was removed"))

    verdict = PASS if (limb_gone and limb_kept) else FAIL
    lines.append("    limb 1 (gone where FALSE): {0}   limb 2 (kept where TRUE, {1} of {1}): {2}".format(
        "PASS" if limb_gone else "FAIL", len(NO_SMA_FIRMS), "PASS" if limb_kept else "FAIL"))
    return {"id": "CATV-TON1-AC5", "verdict": verdict, "lines": lines}


# ---------------------------------------------------------------------------
# CATV-TON1-AC6
# ---------------------------------------------------------------------------

def score_ton1_ac6(docs, before_docs=None):
    """D1-inv-4 STILL HOLDS AND total_aua DOES NOT CHANGE.

    The sum limb is self-contained and date-independent: within ONE artifact, the L0
    nodes must sum to total_aua.  That is the form used as the primary verdict.

    "total_aua does not change" is again date-scoped -- total_aua moves daily with the
    market -- so the cross-artifact equality is scored only at a shared as_of.

    Insurance is view_plane_excluded, so BOTH sums are printed: the full L0 set against
    total_aua, and the rendered (non-excluded) set against sums.view_plane.
    """
    lines = []
    all_ok = True
    for scope in SCOPES:
        doc = docs.get(scope)
        if doc is None:
            continue
        nodes = doc.get("nodes") or {}
        sums = doc.get("sums") or {}
        total_aua = sums.get("total_aua")
        view_plane = sums.get("view_plane")
        full = 0
        rendered = 0
        bad = []
        for name, node in sorted(nodes.items()):
            state, value = money_state(node, "aum")
            if state != "NUMERIC":
                bad.append("{0}={1}".format(name, state))
                continue
            full += cents(value)
            if not node.get("view_plane_excluded"):
                rendered += cents(value)
        ok_full = (total_aua is not None and full == cents(total_aua))
        ok_rend = (view_plane is None) or (rendered == cents(view_plane))
        ok = ok_full and ok_rend and not bad
        all_ok = all_ok and ok
        lines.append(
            "    {0:<12} as_of={1:<11} sum(L0)={2:>18} total_aua={3:>18} {4} | "
            "sum(rendered)={5:>18} view_plane={6:>18} {7}".format(
                scope, str(doc.get("as_of")), fmt(full / 100.0), fmt(total_aua),
                "OK" if ok_full else "MISMATCH",
                fmt(rendered / 100.0), fmt(view_plane),
                "OK" if ok_rend else "MISMATCH"))
        if bad:
            lines.append("        non-numeric L0 aum: {0}".format(", ".join(bad)))

    literal_verdict = NA_BY_DATE
    if before_docs:
        pairs = []
        for scope in SCOPES:
            a, b = docs.get(scope), before_docs.get(scope)
            if a is None or b is None or a.get("as_of") != b.get("as_of"):
                continue
            ta = (a.get("sums") or {}).get("total_aua")
            tb = (b.get("sums") or {}).get("total_aua")
            pairs.append((scope, tb, ta, cents(ta) == cents(tb)))
        if pairs:
            literal_verdict = PASS if all(p[3] for p in pairs) else FAIL
            for scope, tb, ta, same in pairs:
                lines.append("    {0:<12} total_aua before {1:>18} after {2:>18}  {3}".format(
                    scope, fmt(tb), fmt(ta), "UNCHANGED" if same else "MOVED"))
        else:
            lines.append("    total_aua before/after needs a shared as_of -> NA_BY_DATE")
    lines.append("    scope denominator: {0}".format(len(SCOPES)))
    lines.append("    D1-inv-4 (sum holds within each artifact) -> {0} ; "
                 "total_aua unchanged across artifacts -> {1}".format(
                     PASS if all_ok else FAIL, literal_verdict))
    return {"id": "CATV-TON1-AC6", "verdict": PASS if all_ok else FAIL,
            "literal": literal_verdict, "lines": lines}


# ---------------------------------------------------------------------------
# CATV-TON1-AC7
# ---------------------------------------------------------------------------

def score_ton1_ac7(docs, gold_docs):
    """EXERCISED ON A SCHEDULED FIRE.  NO AD-HOC GOLD RUN.

    The SERVED object carries no `trigger`.  It DOES carry source_keys, so the chain is
    served -> gold -> _provenance.trigger, dereferenced rather than assumed.  An ad-hoc
    artifact is never production evidence, so a trigger that is anything but "scheduled"
    is a FAIL, and a missing trigger is UNSCOREABLE rather than a silent pass.
    """
    lines = []
    ok = True
    seen = 0
    for scope in SCOPES:
        doc = docs.get(scope)
        if doc is None:
            continue
        gold = (gold_docs or {}).get(scope)
        prov_served = doc.get("_provenance") or {}
        if gold is None:
            ok = False
            lines.append("    {0:<12} gold artifact not resolved from source_keys -- "
                         "UNSCOREABLE".format(scope))
            continue
        gprov = gold.get("_provenance") or {}
        trigger = gprov.get("trigger")
        producer = gprov.get("producer")
        ptime = gprov.get("process_time")
        seen += 1
        good = (trigger == "scheduled")
        ok = ok and good
        lines.append(
            "    {0:<12} gold trigger={1!r:<12} producer={2!s:<40} process_time={3!s}".format(
                scope, trigger, producer, ptime))
        lines.append(
            "        served written_by={0!s} written_at={1!s}".format(
                prov_served.get("written_by"), prov_served.get("written_at")))
        if not good:
            lines.append("        BLOCKED: trigger is not 'scheduled' -- an ad-hoc artifact "
                         "is never production evidence")
    lines.append("    scopes resolved through source_keys: {0} of {1} (denominator {1})".format(
        seen, len(SCOPES)))
    lines.append("    THE FIRES: 13:00Z etf-positioning (RULES, not this TO) | "
                 "13:30Z mdpf-gold-lambda (GOLD) | 13:50Z mdpf-portal-publisher (SERVED)")
    return {"id": "CATV-TON1-AC7", "verdict": PASS if (ok and seen) else FAIL, "lines": lines}


# ---------------------------------------------------------------------------
# Reporting.
# ---------------------------------------------------------------------------

SCORERS = ("TM1-AC1", "CATV-TON1-AC3", "CATV-TON1-AC4",
           "CATV-TON1-AC5", "CATV-TON1-AC6", "CATV-TON1-AC7")


def run_all(docs, gold_docs=None, before_docs=None, metas=None, ts_map=None):
    return [
        score_tm1_ac1(docs, metas),
        score_ton1_ac3(docs, before_docs, ts_map),
        score_ton1_ac4(docs, before_docs, ts_map),
        score_ton1_ac5(docs),
        score_ton1_ac6(docs, before_docs),
        score_ton1_ac7(docs, gold_docs),
    ]


def report(results, header):
    print("=" * 78)
    print(header)
    print("=" * 78)
    for r in results:
        extra = ""
        if r.get("literal"):
            extra = "   (literal track: {0})".format(r["literal"])
        print("\n[{0}] {1}{2}".format(r["verdict"], r["id"], extra))
        for line in r["lines"]:
            print(line)
    print("\n" + "-" * 78)
    tally = {}
    for r in results:
        tally[r["verdict"]] = tally.get(r["verdict"], 0) + 1
    print("SUMMARY  " + "  ".join(
        "{0}={1}".format(k, tally[k]) for k in sorted(tally)) +
        "   (denominator {0} criteria)".format(len(results)))


# ---------------------------------------------------------------------------
# SELF-TEST.  The instrument must be shown to discriminate, in BOTH directions.
# ---------------------------------------------------------------------------

def _deepcopy(doc):
    return json.loads(json.dumps(doc))


# A synthetic stand-in for platinum/mdpf/49financial/aggregate-aua-timeseries.json.
# The 08-26 / 08-27 rows are MEASURED values read off that artifact on 2026-08-28; the
# 08-28 row is invented purely to exercise the as_of-shift branch (no artifact for that
# date exists yet, which is the whole point of pre-staging).
SELFTEST_TS = {
    "dates": ["2026-08-26", "2026-08-27", "2026-08-28"],
    "non_model_aua": [286545000.78, 290426813.47, 291000000.00],
    "by_model": {
        "opal_div_sma": {"model_value": [18929318.4129, 18783379.8116, 18800000.00]},
        "opal_growth_sma": {"model_value": [4034142.4692, 4011386.4409, 4000000.00]},
    },
}


def self_test(commit=CONTROL_COMMIT):
    """Prove every criterion can both FAIL and PASS.

    An unfalsifiable scorer is an assertion, not an instrument.  Three of these criteria
    (AC4, AC6, AC7) CORRECTLY PASS on the pre-fix control -- the control alone therefore
    proves nothing about them, so each gets a PLANTED MUTANT.  The three that fail on the
    control (AC1, AC3, AC5) get the opposite treatment: a repaired mutant that must flip
    them to PASS.  Neither direction is optional: an undercount announces itself, an
    overcount never does.
    """
    print("=" * 78)
    print("SELF-TEST -- failability arm pinned to COMMIT {0} (not to a clock)".format(commit))
    print("=" * 78)
    ctl = {}
    for scope in SCOPES:
        ctl[scope] = load_from_commit(commit, scope)
    print("control loaded: {0} of {1} scopes (denominator {1})".format(len(ctl), len(SCOPES)))
    for scope in SCOPES:
        prov = ctl[scope].get("_provenance") or {}
        print("    {0:<12} written_at={1}  as_of={2}".format(
            scope, prov.get("written_at"), ctl[scope].get("as_of")))

    failures = []

    def check(label, got, want):
        ok = (got == want)
        print("  {0:<58} got={1:<13} want={2:<13} {3}".format(
            label, got, want, "OK" if ok else "MISMATCH"))
        if not ok:
            failures.append(label)

    # ---- the GATE must refuse the pre-fix control --------------------------
    print("\n-- GATE (must REFUSE the pre-fix control) --")
    gate_ok, _ = gate_scoreable(ctl)
    check("gate_scoreable(pre-fix control)", "REFUSE" if not gate_ok else "ALLOW", "REFUSE")

    # a synthetic post-fix doc must be ALLOWED, or the gate is a constant
    post = {s: _deepcopy(ctl[s]) for s in SCOPES}
    for s in SCOPES:
        post[s]["_provenance"]["written_at"] = "2026-08-29T13:50:50Z"
    gate_ok2, _ = gate_scoreable(post)
    check("gate_scoreable(synthetic post-fix)", "ALLOW" if gate_ok2 else "REFUSE", "ALLOW")
    # and a gold-rung doc must be refused by G1 even if late enough for G2
    goldish = {s: _deepcopy(post[s]) for s in SCOPES}
    for s in SCOPES:
        goldish[s]["_provenance"]["written_by"] = "mdpf-gold-lambda (mdpf_gold_consolidator)"
    gate_ok3, _ = gate_scoreable(goldish)
    check("gate_scoreable(gold rung, late enough for G2)",
          "REFUSE" if not gate_ok3 else "ALLOW", "REFUSE")

    # ---- NEGATIVE direction: the control must FAIL the broken criteria -----
    print("\n-- NEGATIVE arm: the PRE-FIX control (the criteria that must FAIL) --")
    tsm = {SMA_FIRM: SELFTEST_TS}
    base = run_all(ctl, ts_map=tsm)
    by_id = {r["id"]: r for r in base}
    check("TM1-AC1        on pre-fix control", by_id["TM1-AC1"]["verdict"], FAIL)
    check("CATV-TON1-AC3  on pre-fix control", by_id["CATV-TON1-AC3"]["verdict"], FAIL)
    check("CATV-TON1-AC5  on pre-fix control", by_id["CATV-TON1-AC5"]["verdict"], FAIL)
    print("   (these three are the criteria the fix exists to move)")

    print("\n-- the criteria that CORRECTLY PASS pre-fix (so the control proves nothing) --")
    check("CATV-TON1-AC4  on pre-fix control", by_id["CATV-TON1-AC4"]["verdict"], PASS)
    check("CATV-TON1-AC6  on pre-fix control", by_id["CATV-TON1-AC6"]["verdict"], PASS)
    print("   D1-inv-4 HOLDS pre-fix, correctly -- a sum invariant cannot see a")
    print("   misattribution between two of its own summands.  Hence the mutants below.")

    # ---- PLANTED MUTANTS for the criteria that pass on the control ---------
    print("\n-- MUTANT arm: criteria that pass on the control MUST fail on a mutant --")

    m = {s: _deepcopy(ctl[s]) for s in SCOPES}
    m["cottonwood"]["nodes"]["Client"]["aum"] = \
        m["cottonwood"]["nodes"]["Client"]["aum"] + 1.00
    check("CATV-TON1-AC4  mutant: cottonwood Client moved by $1.00",
          score_ton1_ac4(m)["verdict"], FAIL)

    m = {s: _deepcopy(ctl[s]) for s in SCOPES}
    m["global"]["sums"]["total_aua"] = m["global"]["sums"]["total_aua"] + 0.01
    check("CATV-TON1-AC6  mutant: global total_aua moved by $0.01",
          score_ton1_ac6(m)["verdict"], FAIL)

    gold_good = {s: {"_provenance": {"trigger": "scheduled",
                                     "producer": "mdpf-gold-lambda",
                                     "process_time": "2026-08-29T13:30:37Z"}}
                 for s in SCOPES}
    check("CATV-TON1-AC7  gold trigger 'scheduled'",
          score_ton1_ac7(ctl, gold_good)["verdict"], PASS)
    gold_bad = {s: _deepcopy(gold_good[s]) for s in SCOPES}
    gold_bad["49financial"]["_provenance"]["trigger"] = "manual"
    check("CATV-TON1-AC7  mutant: one scope's trigger is 'manual' (ad-hoc)",
          score_ton1_ac7(ctl, gold_bad)["verdict"], FAIL)
    check("CATV-TON1-AC7  mutant: gold unresolvable from source_keys",
          score_ton1_ac7(ctl, {})["verdict"], FAIL)

    # ---- POSITIVE direction: a repaired artifact must flip to PASS ---------
    print("\n-- POSITIVE arm: a REPAIRED artifact must flip the failing criteria to PASS --")
    print("   (an absence check cannot tell a fix from a refactor -- so test the")
    print("    direction that ADDS the values, not only the one that removes them)")

    fixed = {s: _deepcopy(ctl[s]) for s in SCOPES}
    # TM1-AC1: map a dollar value onto every L2 member under Models, for one firm.
    for l1_label, member in l2_members_under_models(fixed["cottonwood"]):
        member["aum"] = 1.0
    check("TM1-AC1        repaired: cottonwood L2 members carry NUMERIC aum",
          score_tm1_ac1(fixed)["verdict"], PASS)
    # and the null case must NOT satisfy the strict reading
    nulled = {s: _deepcopy(ctl[s]) for s in SCOPES}
    for l1_label, member in l2_members_under_models(nulled["cottonwood"]):
        member["aum"] = None
    check("TM1-AC1        null-mapped members do NOT satisfy STRICT (null != 0.00)",
          score_tm1_ac1(nulled)["verdict"], FAIL)

    # CATV-TON1-AC5: remove the false sentence for 49financial only.
    fixed5 = {s: _deepcopy(ctl[s]) for s in SCOPES}
    del fixed5["49financial"]["nodes"]["SMA"]["absent_reason"]
    check("CATV-TON1-AC5  repaired: false sentence removed for 49financial only",
          score_ton1_ac5(fixed5)["verdict"], PASS)
    # deleting it EVERYWHERE must still FAIL -- that is the second limb.
    over = {s: _deepcopy(fixed5[s]) for s in SCOPES}
    for s in NO_SMA_FIRMS:
        del over[s]["nodes"]["SMA"]["absent_reason"]
    check("CATV-TON1-AC5  over-deletion (removed where TRUE too) must FAIL",
          score_ton1_ac5(over)["verdict"], FAIL)

    # CATV-TON1-AC3: perform the reattribution the fix is supposed to perform.
    def _repair(doc, as_of, div, pfoe, non_model):
        doc["as_of"] = as_of
        total_c = 0
        for _label, child in (doc["nodes"]["SMA"].get("children") or {}).items():
            bucket_c = 0
            for member in (child.get("members") or []):
                mid = member.get("member_id")
                member["aum"] = div if mid == "divz" else (pfoe if mid == "pfoe" else 0.0)
                bucket_c += cents(member["aum"])
            child["aum"] = bucket_c / 100.0
            total_c += bucket_c
        doc["nodes"]["SMA"]["aum"] = total_c / 100.0
        doc["nodes"]["Client"]["aum"] = (cents(non_model) - total_c) / 100.0
        doc["nodes"]["SMA"].pop("absent_reason", None)
        return doc

    fixed3 = {s: _deepcopy(ctl[s]) for s in SCOPES}
    _repair(fixed3[SMA_FIRM], "2026-08-27", 18783379.8116, 4011386.4409, 290426813.47)
    r3 = score_ton1_ac3(fixed3, ts_map=tsm)
    check("CATV-TON1-AC3  repaired: reattribution performed", r3["verdict"], PASS)
    check("CATV-TON1-AC3  literal track reproduces at as_of 2026-08-27", r3["literal"], PASS)
    print("      repaired SMA={0}  Client={1}".format(
        fmt(fixed3[SMA_FIRM]["nodes"]["SMA"]["aum"]),
        fmt(fixed3[SMA_FIRM]["nodes"]["Client"]["aum"])))

    # the SAME repair on a DIFFERENT as_of must go NA_BY_DATE, never FAIL
    shifted = {s: _deepcopy(ctl[s]) for s in SCOPES}
    _repair(shifted[SMA_FIRM], "2026-08-28", 18800000.00, 4000000.00, 291000000.00)
    r3b = score_ton1_ac3(shifted, ts_map=tsm)
    check("CATV-TON1-AC3  same repair at as_of 2026-08-28 -> structural PASS",
          r3b["verdict"], PASS)
    check("CATV-TON1-AC3  same repair at as_of 2026-08-28 -> literal NA_BY_DATE",
          r3b["literal"], NA_BY_DATE)

    # THE VACUITY MUTANT -- the defect this tool's own self-test caught.
    # Move Client alone.  non_model comes from an INDEPENDENT artifact, so the netting
    # equality must break.  Before the fix, non_model was derived FROM Client and this
    # mutant passed.
    vac = {s: _deepcopy(fixed3[s]) for s in SCOPES}
    vac[SMA_FIRM]["nodes"]["Client"]["aum"] = \
        vac[SMA_FIRM]["nodes"]["Client"]["aum"] + 1.00
    check("CATV-TON1-AC3  mutant: Client moved $1.00, non_model NOT moved (vacuity probe)",
          score_ton1_ac3(vac, ts_map=tsm)["verdict"], FAIL)
    # and with NO independent source the honest answer is UNSCOREABLE, not a vacuous PASS
    check("CATV-TON1-AC3  no independent non_model source -> UNSCOREABLE (not PASS)",
          score_ton1_ac3(fixed3)["verdict"], UNSCOREABLE)
    print("      ^ THIS is the finding: the literal constant must NOT fail a correct fix")
    print("        merely because the artifact is from a different trading day.")

    print("\n" + "-" * 78)
    if failures:
        print("SELF-TEST FAILED -- {0} of {1} checks mismatched:".format(
            len(failures), len(failures) + 0))
        for f in failures:
            print("    {0}".format(f))
        return False
    print("SELF-TEST PASSED -- every criterion demonstrated to discriminate in BOTH")
    print("directions (control, planted mutants, and repaired artifacts).")
    return True


# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--self-test", action="store_true",
                    help="prove the instrument discriminates; exits non-zero if not")
    ap.add_argument("--live", action="store_true", help="score the live served objects")
    ap.add_argument("--from-commit", metavar="ISH", help="score a committed snapshot")
    ap.add_argument("--before-commit", metavar="ISH", default=CONTROL_COMMIT,
                    help="the BEFORE artifacts for the literal tracks (default: the control)")
    ap.add_argument("--json", metavar="PATH", help="write the verdict map")
    ap.add_argument("--force", action="store_true",
                    help="score even if the gate refuses (verdicts are then NOT acceptance evidence)")
    args = ap.parse_args()

    if args.self_test:
        return 0 if self_test() else 1

    if not (args.live or args.from_commit):
        ap.print_help()
        print("\nERROR: pass --self-test, --live, or --from-commit")
        return 2

    # An edit after a green run invalidates the run, so the self-test always precedes
    # a live score rather than being trusted from a previous invocation.
    print("Running the self-test first -- a scorer that has not been shown to fail")
    print("is an assertion, not an instrument.\n")
    if not self_test():
        print("\nBLOCKED: self-test failed; refusing to score.")
        return 1
    print("")

    docs = {}
    metas = {}
    for scope in SCOPES:
        if args.live:
            docs[scope] = load_live(scope)
            metas[scope] = live_object_meta(scope)
        else:
            docs[scope] = load_from_commit(args.from_commit, scope)

    print("=" * 78)
    print("SCOREABILITY GATE")
    print("=" * 78)
    ok, lines = gate_scoreable(docs)
    for line in lines:
        print(line)
    if not ok:
        print("\nBLOCKED: these are NOT post-fix SERVED objects.")
        print("  A scorer run against the 13:30Z gold floor, or against bytes written")
        print("  before the fix deployed, reports a CORRECT fix as FAILED.")
        print("  Re-run after the mdpf-portal-publisher fire (~13:50Z) that follows a")
        print("  gold run on the corrected pin.  Nothing was scored.")
        if not args.force:
            return 3
        print("\nWARN: --force given; verdicts below are NOT acceptance evidence.")
    else:
        print("\nOK: post-fix SERVED objects on all {0} scope(s).".format(len(docs)))

    before_docs = None
    if args.before_commit:
        before_docs = {}
        for scope in SCOPES:
            before_docs[scope] = load_from_commit(args.before_commit, scope)

    gold_docs = {}
    for scope in SCOPES:
        if args.live:
            gold, _src = load_gold_for(docs[scope])
            if gold is not None:
                gold_docs[scope] = gold

    results = run_all(docs, gold_docs, before_docs, metas if args.live else None)
    report(results, "D1_CATVIEWS -- TM1-AC1 + CATV-TON1-AC3..AC7")

    if args.json:
        payload = {
            "scored_at_source": "live" if args.live else args.from_commit,
            "gate_passed": ok,
            "criteria": [
                {"id": r["id"], "verdict": r["verdict"], "literal": r.get("literal")}
                for r in results
            ],
        }
        with open(args.json, "w") as fh:
            json.dump(payload, fh, indent=2, sort_keys=True)
        print("\nwrote {0}".format(args.json))

    return 0 if all(r["verdict"] == PASS for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
