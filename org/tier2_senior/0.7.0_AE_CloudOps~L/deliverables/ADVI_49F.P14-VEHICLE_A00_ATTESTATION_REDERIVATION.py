"""INDEPENDENT re-derivation of the a00 attestation split for ADVI_49F.P14-VEHICLE.

METHOD INDEPENDENCE, stated because it is the whole point (CLAUDE.md Rule 22: a second seat's
confirmation via the FIRST seat's method is REPETITION, not corroboration):
  - I did NOT run 0.4.0_DS_ClientPlatform~U's committed enumeration script.
  - The predicate below is transcribed by ME from a00_runner.py:83-100 at source, not from ~U's
    description of it.
  - Counting, pagination and denominators are my own.
The SUBSTRATE is necessarily the same S3 (it is the very thing a00 reads at run time); independence
here is of METHOD, and I state that limit rather than claiming more.

a00 has TWO refusal gates and they are different questions -- main() checks partition existence
FIRST (:114-116), then attestation (:118). Both are enumerated separately below.

STRUCTURE (2026-08-27, 0.7.0_AE_CloudOps~L): the report moved under `main()` behind a
`__main__` guard and the measurement moved into `derive()`. REASON: the campaign driver must
decide the --declared-historical flag from THIS predicate and no other -- a second transcription
of a00's gate is how two artifacts drift apart while both look right. The driver loads this file
by path (the filename carries `.` and `-`, so it is not importable by name) and calls `derive()`.
Without the guard that load would execute the whole report. Printed output is unchanged.
"""
from __future__ import annotations

import json
from io import BytesIO

import boto3
import pandas as pd

SILVER_BUCKET = "opal-data-assets"
GOLD_BUCKET = "opal-data-49financial"
SCOPE = "schwab/08335338"
ACC_PREFIX = f"{SCOPE}/silver/fact_acc/"
CONV_PREFIX = f"{SCOPE}/meta/conversions/"
CAL_PREFIX = "gold/advi/dimensions/dim_calendar/"

# E-1 (C02-g-9): the DOMAIN is the trading calendar INTERSECT input presence. It is NEVER an
# output table. The old line here read gold/advi/canonical/flow_ledger/ -- an OUTPUT of the very
# chain whose missing dates this vehicle exists to find, so a date absent from the output was
# absent from its own work list. That is how 2026-08-11..08-17 stayed invisible.
#
# PRESENCE = the inputs the chain HALTS without, derived AT SOURCE, not from coextension with the
# store. rc.read_partition raises FileNotFoundError on absence (runner_common.py:81); only two
# callers catch it and both are GOLD dependencies (b01:123 dim_boundary, b04:328 dim_relationship),
# so every silver read at the chain date halts. Sites:
HALTING_INPUTS = {
    "fact_acc":        "a01:228, a02:166, a06:180",
    "fact_sec":        "a03:100, b02:104",
    "fact_trn":        "a05:111, c00:520",
    "dim_balance":     "b00:97, b02:107",
    "dim_position":    "b01:108, b02:105",
    "fact_upn":        "b02:108",
    "dim_transaction": "c01:232",   # inline f-string, invisible to a prefix-constant census
}
# ANNOTATIONS -- carried beside each date, NEVER membership tests. A membership test is a claim
# that the chain cannot produce the date without the input; these are inputs the chain proceeds
# past. fact_fam is read at a RESOLVED latest (a01:206/:227) with a WARN and fam_declared_stale,
# so it cannot raise on the chain date. fact_rps and fact_slm are read by NO chain stage at all --
# fact_rps's exact coextension with the store was upstream schedule coincidence, not dependency.
ANNOTATION_INPUTS = ("fact_fam",)
NOT_READ_BY_CHAIN = ("fact_rps", "fact_slm")

s3 = boto3.client("s3")


def list_partition_dates(bucket, prefix):
    """date= partition dirs under a prefix. Paginated (never --no-paginate / page-1 reasoning)."""
    dates = set()
    pag = s3.get_paginator("list_objects_v2")
    for page in pag.paginate(Bucket=bucket, Prefix=prefix, Delimiter="/"):
        for cp in page.get("CommonPrefixes", []):
            part = cp["Prefix"].rstrip("/").rsplit("/", 1)[-1]
            if part.startswith("date="):
                dates.add(part[5:])
    return dates


def trading_days():
    """dim_calendar's trading_day column, read from its NEWEST partition. The calendar is the
    domain's authority (CLAUDE.md: one frontier, lib/trading_calendar.py's convention)."""
    dates = list_partition_dates(GOLD_BUCKET, CAL_PREFIX)
    if not dates:
        raise FileNotFoundError("no dim_calendar partition -- the domain has no authority; REFUSE")
    newest = sorted(dates)[-1]
    key = f"{CAL_PREFIX}date={newest}/data.parquet"
    body = s3.get_object(Bucket=GOLD_BUCKET, Key=key)["Body"].read()
    frame = pd.read_parquet(BytesIO(body))
    return newest, {str(x) for x in frame["trading_day"]}


def compute_domain(trading_days_set, per_input):
    """PURE. The domain from a calendar set and per-input presence -- no I/O.

    The seam exists so an arm can drive it with SYNTHETIC sets, including a date deliberately
    masked from the output table. A domain function that can only be exercised against live S3
    cannot be shown to ignore the output, because live S3 currently agrees with it.
    """
    presence = None
    for d in per_input.values():
        presence = d if presence is None else (presence & d)
    presence = presence or set()
    return (trading_days_set & presence), presence


def input_presence():
    """Per-input partition dates for the HALTING set, plus the annotation inputs.

    Returns (per_input, presence, annotations). `presence` is the AND over the halting set --
    a date the chain could actually be run for. Annotations are measured and reported, never
    intersected: doing so would refuse dates the chain demonstrably produced.
    """
    per = {t: list_partition_dates(SILVER_BUCKET, f"{SCOPE}/silver/{t}/") for t in HALTING_INPUTS}
    presence = None
    for d in per.values():
        presence = d if presence is None else (presence & d)
    ann = {t: list_partition_dates(SILVER_BUCKET, f"{SCOPE}/silver/{t}/") for t in ANNOTATION_INPUTS}
    return per, (presence or set()), ann


def attested_dates():
    """a00_runner.py:83-100 predicate, transcribed from source by this seat:
       some conversion record with per_type.fact_acc.action == 'converted'
       AND the date present in that record's 'partitions' list."""
    pag = s3.get_paginator("list_objects_v2")
    keys = [o["Key"] for page in pag.paginate(Bucket=SILVER_BUCKET, Prefix=CONV_PREFIX)
            for o in page.get("Contents", [])]
    attested = {}
    malformed = 0
    for k in keys:
        try:
            rec = json.loads(s3.get_object(Bucket=SILVER_BUCKET, Key=k)["Body"].read())
        except Exception:
            malformed += 1
            continue
        per = (rec.get("per_type") or {}).get("fact_acc")
        if not per or per.get("action") != "converted":
            continue
        for d in rec.get("partitions", []) or []:
            attested.setdefault(d, set()).add(int(per["t1_expected"]))
    return keys, attested, malformed


def derive():
    """The measurement, with no printing. Returns every figure the report quotes.

    PERISHABLE BY CONSTRUCTION -- the epoch and the attested set advance with every converter
    run, so this is called at execution time and its result is never carried across a session.
    """
    keys, attested, malformed = attested_dates()
    acc = list_partition_dates(SILVER_BUCKET, ACC_PREFIX)
    cal_asof, tdays = trading_days()
    per_input, _presence, annotations = input_presence()
    flow, presence = compute_domain(tdays, per_input)   # THE DOMAIN: calendar AND presence
    att = set(attested)
    epoch = min(att) if att else None

    proceed = flow & att
    refuse_attest = flow - att
    lt = {d for d in flow if epoch and d < epoch}
    ge = {d for d in flow if epoch and d >= epoch}
    gap = sorted(ge - att)

    # Controls travel WITH the numbers -- a split quoted without them is not evidence.
    pos = ["2026-08-24", "2026-08-25", "2026-08-26"]
    neg = ["2026-03-24", "2026-01-15", "2025-06-10"]
    pos_ok = all(d in att for d in pos)
    neg_ok = all(d not in att for d in neg)

    return {
        "conversion_keys": keys,
        "attested_map": attested,
        "malformed": malformed,
        "fact_acc_dates": acc,
        "domain": flow,
        "calendar_asof": cal_asof,
        "trading_days": tdays,
        "per_input": per_input,
        "presence": presence,
        "annotations": annotations,
        "attested": att,
        "epoch": epoch,
        "proceed": proceed,
        "refuse_attest": refuse_attest,
        "pre_epoch": lt,
        "at_or_after_epoch": ge,
        "residual_hole": gap,
        "pos_control": (pos, pos_ok),
        "neg_control": (neg, neg_ok),
        "controls_ok": pos_ok and neg_ok,
    }


def main():
    print("=" * 78)
    print("INDEPENDENT RE-DERIVATION -- a00 attestation vs the backfill set")
    print("=" * 78)

    r = derive()
    keys, attested, malformed = r["conversion_keys"], r["attested_map"], r["malformed"]
    print(f"conversion records SCANNED : {len(keys)}   (malformed/unreadable: {malformed})")
    print(f"fact_acc-ATTESTED dates    : {len(attested)}")
    if attested:
        ad = sorted(attested)
        print(f"  attested range           : {ad[0]} .. {ad[-1]}")

    conflicting = {d: v for d, v in attested.items() if len(v) > 1}
    print(f"  of those, CONFLICTING     : {len(conflicting)}  "
          f"(a00 REFUSES these too, :98 -- a second refusal mode)")

    acc, flow = r["fact_acc_dates"], r["domain"]
    tdays, presence = r["trading_days"], r["presence"]
    per_input, annotations = r["per_input"], r["annotations"]
    print()
    print("=" * 78)
    print("THE DOMAIN -- trading calendar AND input presence, never an output table")
    print("=" * 78)
    print(f"  dim_calendar read at date={r['calendar_asof']}")
    print(f"  DENOMINATOR 1  calendar trading days in span      : {len(tdays)}")
    print("  DENOMINATOR 2  per-input partition presence (the HALTING set, source-derived):")
    for t, sites in HALTING_INPUTS.items():
        d = per_input[t]
        print(f"      {t:<16} {len(d):>5}   halts at {sites}")
    print(f"  DENOMINATOR 3  presence = AND over the halting set : {len(presence)}")
    print(f"  DENOMINATOR 4  DOMAIN = calendar AND presence      : {len(flow)}")
    print("  ANNOTATIONS -- measured and carried, never intersected:")
    for t, d in annotations.items():
        short = sorted(tdays - d)
        print(f"      {t:<16} {len(d):>5}   short {len(short)} vs the calendar"
              f"{' -- frontier ' + max(d) if d else ''}")
        if short:
            print("          those dates ARE emitted; the chain proceeds and declares staleness")
    for t in NOT_READ_BY_CHAIN:
        print(f"      {t:<16}     -   NOT READ by any chain stage -- excluded from the predicate")
    excluded = sorted(tdays - presence)
    print(f"  DENOMINATOR 5  calendar days EXCLUDED for absent input : {len(excluded)}")
    for d in excluded:
        missing = [t for t in HALTING_INPUTS if d not in per_input[t]]
        print(f"      {d}  UNBACKFILLABLE-INPUTS-ABSENT: {missing}")
    if not excluded:
        print("      (none -- every calendar trading day has all seven halting inputs)")

    att = r["attested"]
    proceed, refuse_attest = r["proceed"], r["refuse_attest"]
    print()
    print("=" * 78)
    print("THE SPLIT, denominator beside every number")
    print("=" * 78)
    D = len(flow)
    print(f"  DOMAIN (denominator)                             : {D}")
    print(f"  a00 PROCEEDS (attested)                          : {len(proceed)}  "
          f"({100.0*len(proceed)/D:.2f}% of {D})")
    print(f"  a00 REFUSES  (not attested)                      : {len(refuse_attest)}  "
          f"({100.0*len(refuse_attest)/D:.2f}% of {D})")
    print(f"  cross-check proceeds+refuses == denominator      : "
          f"{len(proceed)+len(refuse_attest)} == {D} -> "
          f"{'OK' if len(proceed)+len(refuse_attest)==D else 'MISMATCH'}")
    print()
    print(f"  ALSO gate 1 (fact_acc partition missing entirely): "
          f"{len(flow - acc)} of {D} domain dates have NO fact_acc partition")
    print(f"  attested dates NOT in the domain                  : {len(att - flow)} of {len(att)}")

    print()
    print("=" * 78)
    print("CONTROLS -- both arms, on my own enumeration")
    print("=" * 78)
    POS, pos_ok = r["pos_control"]
    NEG, neg_ok = r["neg_control"]
    print("  POSITIVE (dates the chain demonstrably ran on -- must be ATTESTED):")
    for d in POS:
        print(f"    {d}  attested={d in att}   in_domain={d in flow}")
    print("  NEGATIVE (the exercised abort + two others -- must be NOT attested):")
    for d in NEG:
        print(f"    {d}  attested={d in att}   in_domain={d in flow}")

    print()
    print(f"  positive control: {'FIRED (all attested)' if pos_ok else '*** FAILED ***'}")
    print(f"  negative control: {'FIRED (none attested)' if neg_ok else '*** FAILED ***'}")
    if not (pos_ok and neg_ok):
        print("  -> a control failed; the split above is NOT trustworthy. Do not quote it.")

    # -----------------------------------------------------------------------
    # COVERAGE CHECK vs CTO 76379's ruled two-mode design.
    # The mode REFUSES any date >= the attestation epoch, so any in-set date that is
    # at-or-after the epoch AND unattested would refuse under BOTH the guard and the
    # mode -- un-runnable either way. That set must be empty for the ruling to cover
    # the backfill set. Measured, not assumed.
    # -----------------------------------------------------------------------
    epoch = r["epoch"]
    lt, ge, gap = r["pre_epoch"], r["at_or_after_epoch"], r["residual_hole"]
    print()
    print("=" * 78)
    print("COVERAGE vs the ruled two-mode design (CTO 76379)")
    print("=" * 78)
    print(f"  epoch, MEASURED from the converter record set (never typed): {epoch}")
    print(f"  in-set dates <  epoch -> declared-historical : {len(lt)}")
    print(f"  in-set dates >= epoch -> guard must bind     : {len(ge)}")
    print(f"  cross-check {len(lt)} + {len(ge)} == {len(flow)} -> {len(lt)+len(ge)==len(flow)}")
    print(f"  >= epoch AND NOT attested (the residual hole): {len(gap)} of {len(ge)}")
    if gap:
        print(f"    dates: {gap[:15]}{' ...' if len(gap)>15 else ''}")
        print("    -> RESIDUAL HOLE EXISTS: these refuse in BOTH modes. Surface before building.")
    else:
        print(f"    -> NO RESIDUAL HOLE. Coverage {len(lt)} declared + {len(ge & att)} attested "
              f"= {len(lt)+len(ge & att)} of {len(flow)}.")
    print()
    print("PERISHABLE: the epoch and the attested set ADVANCE with every converter run.")
    print("These figures measure the instant they were taken. V14-4 re-derives at execution time.")


if __name__ == "__main__":
    main()
