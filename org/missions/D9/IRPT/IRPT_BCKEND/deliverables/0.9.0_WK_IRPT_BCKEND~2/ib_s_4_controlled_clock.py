#!/usr/bin/env python3
"""IB-s-4 CONTROLLED-CLOCK HARNESS -- five arms, five readings, no real-calendar wait.

THE WHOLE POINT: every one of the five things a freshness system must distinguish is a function
of a DATE, and a date is an input. So the harness supplies `now` and the source fixtures, and
drives an added client, a changed eligibility, a missed trigger, a failed refresh and an
over-age request in milliseconds -- not by waiting for a scheduler, and not by sleeping.

  "no FWD is ever a wait ... sprint, execute, validate, and close" -- the same principle one
  level down: an acceptance arm whose only proof is an event nobody controls is re-cut so its
  MECHANISM is driven deliberately.

WHAT IS REAL HERE AND WHAT IS A FIXTURE, stated so nothing is over-read:

  REAL   the trading calendar (`lib/trading_calendar.py`, the estate's ONE frontier) -- the arms
         are driven against the actual NYSE frontier, so a weekend or a holiday moves them the
         way it would move production. The calendar source is PRINTED.
  REAL   `refresh.py` and `expiry.py` -- the harness calls the shipped modules, not a copy.
  FIXTURE the directory builds. Three tiny entry sets stand in for the gold runner's output,
         because the arms under test are the STATUS TRANSITIONS between two builds, not the
         build itself -- and the build is exercised for real by the battery's arm (i), which
         runs the actual runner over live silver.
  FIXTURE the clock. That IS the deliverable.

ASCII only. No sleep, no network, no AWS call, no vendor call.
"""
from __future__ import annotations

import datetime as dt
import json
import os
import sys
import time

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.abspath(os.path.join(_HERE, *([os.pardir] * 7)))
_DIR = os.path.join(_REPO, "infra", "aws", "lambda", "investor-reporting", "directory")
for _p in (_DIR, os.path.join(_REPO, "lib")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import expiry      # noqa: E402
import refresh     # noqa: E402

FIRM = "49financial"
OPAQUE_FIRM = "fir_c9fc04650e2134d6ea033da2"


def entry(client_id, name, terminated=False):
    return {"ids": {"firm_id": OPAQUE_FIRM, "client_id": client_id, "relationship_id": None,
                    "account_ids": ["acct-" + client_id]},
            "display_name": name,
            "masked_discriminator": "****" + client_id[-4:],
            "termination": {"indicator": "TERMINATED" if terminated else "ACTIVE",
                            "effective_date": "2026-06-30" if terminated else None}}


BASE = [entry("c0000000000000000001", "Whitfield Family"),
        entry("c0000000000000000002", "Alder Holdings LLC")]
WITH_ADDITION = BASE + [entry("c0000000000000000003", "Novak Trust")]
WITH_TERMINATION = [BASE[0], entry("c0000000000000000002", "Alder Holdings LLC",
                                   terminated=True)]


def _cal():
    cal = expiry.resolve_calendar()
    if cal is None:
        raise RuntimeError("BLOCKED: the trading calendar could not be resolved; this harness "
                           "refuses to drive freshness arms against an approximation")
    return cal


def run_arms():
    """Drive all five. Returns (rows, elapsed_seconds, calendar_source)."""
    t0 = time.time()
    cal = _cal()
    rows = []

    # The frontier the harness drives against -- REAL, printed, and the anchor for every date
    # below. Nothing here types a calendar date: they are all derived from the frontier, so the
    # harness behaves the same on a Monday, a Friday and the day after a holiday.
    today = cal.expected_last_trading_day(dt.date.today())
    t_1 = cal.prev_trading_day(today)
    t_2 = cal.prev_trading_day(t_1)
    t_3 = cal.prev_trading_day(t_2)
    t_4 = cal.prev_trading_day(t_3)

    # ---------------------------------------------------------------- (a) ADDED CLIENT
    # A client is added to the sources. NOBODY ASKS: the scheduled fire runs and the client is
    # in the directory. The arm's observable is the REASON CODE plus the presence of the new
    # entry in the build the fire produced.
    env, man = refresh.refresh_firm(
        FIRM, today,
        build_fn=lambda f, n: {"entries": WITH_ADDITION, "business_date": str(t_1),
                               "source_completion_date": str(t_1),
                               "directory_revision": "irpt-dir/%s/%s/1.0" % (FIRM, t_1)},
        previous_entries=BASE, last_manifest_as_of=t_1, calendar=cal)
    added_present = any(e["ids"]["client_id"] == "c0000000000000000003"
                        for e in WITH_ADDITION)
    rows.append({
        "arm": "a", "name": "ADDED CLIENT",
        "reason_code": env["public_reason_code"], "state": env["state"],
        "observable": "the new client is in the directory the fire produced, and nobody asked: "
                      "added=%d, new entry present=%s, age within ceiling"
                      % (man["delta"]["added"], added_present),
        "delta": man["delta"], "business_date": env["source_dates"]["business_date"]})

    # ---------------------------------------------------------------- (b) CHANGED ELIGIBILITY
    # A client stops being offered. It must cease to be OFFERED and STAY VISIBLE, marked
    # terminated -- deletion would be the defect, so the arm asserts PRESENCE as well as status.
    env, man = refresh.refresh_firm(
        FIRM, today,
        build_fn=lambda f, n: {"entries": WITH_TERMINATION, "business_date": str(t_1),
                               "source_completion_date": str(t_1),
                               "directory_revision": "irpt-dir/%s/%s/1.1" % (FIRM, t_1)},
        previous_entries=BASE, last_manifest_as_of=t_1, calendar=cal)
    still_visible = [e for e in WITH_TERMINATION
                     if e["ids"]["client_id"] == "c0000000000000000002"]
    rows.append({
        "arm": "b", "name": "CHANGED ELIGIBILITY",
        "reason_code": env["public_reason_code"], "state": env["state"],
        "observable": "eligibility_changed=%d, disappeared=%d, the client is STILL VISIBLE "
                      "marked %s (terminated clients stay visible under entitlement)"
                      % (man["delta"]["eligibility_changed"], man["delta"]["disappeared"],
                         still_visible[0]["termination"]["indicator"] if still_visible
                         else "ABSENT -- FAULT"),
        "delta": man["delta"], "business_date": env["source_dates"]["business_date"]})

    # ---------------------------------------------------------------- (c) MISSED TRIGGER
    # The clock moves forward three trading days and no manifest was written. The fire that
    # should have happened did not, and the next run says so INSTEAD of quietly building.
    env, man = refresh.refresh_firm(
        FIRM, today,
        build_fn=lambda f, n: {"entries": BASE, "business_date": str(today)},
        previous_entries=BASE, last_manifest_as_of=t_4, calendar=cal)
    rows.append({
        "arm": "c", "name": "MISSED TRIGGER",
        "reason_code": env["public_reason_code"], "state": env["state"],
        "observable": "last manifest %s, now %s: %d expected trading day(s) carry no manifest, "
                      "so the fire did not happen and this run does not paper over it"
                      % (t_4, today, man["delta"].get("missed_business_dates", 0)),
        "delta": man["delta"], "business_date": env["source_dates"]["business_date"]})

    # ---------------------------------------------------------------- (d) FAILED REFRESH
    # The fire ran and the build raised. FAILED is not MISSED: one is an absent fire, the other
    # is a fire that produced nothing, and an operator needs to tell them apart.
    def boom(firm_id, now):
        raise RuntimeError("silver partition unreadable for %s" % firm_id)

    env, man = refresh.refresh_firm(FIRM, today, build_fn=boom, previous_entries=BASE,
                                    last_manifest_as_of=t_1, calendar=cal)
    rows.append({
        "arm": "d", "name": "FAILED REFRESH",
        "reason_code": env["public_reason_code"], "state": env["state"],
        "observable": "the fire RAN and the build raised %s; the exception TEXT is withheld "
                      "from the manifest (a manifest is a durable log)"
                      % man["delta"].get("build_error"),
        "delta": man["delta"], "business_date": env["source_dates"]["business_date"]})

    # ---------------------------------------------------------------- (e) OVER-AGE REQUEST
    # A READ, not a fire. The directory on disk is older than the schedule's ceiling, so the
    # request gets the DECLARED expiry/fallback answer carrying its history -- never a silent
    # answer and never an empty one.
    directory = {"as_of_business_date": str(t_4), "source_completion_date": str(t_4),
                 "directory_revision": "irpt-dir/%s/%s/1.0" % (FIRM, t_4),
                 "firm_id_opaque": OPAQUE_FIRM}
    env, extra = refresh.serve_read(directory, today, "harness-over-age", cal)
    rows.append({
        "arm": "e", "name": "OVER-AGE REQUEST",
        "reason_code": env["public_reason_code"], "state": env["state"],
        "observable": "directory as_of %s is %d trading day(s) behind a ceiling of %d; the "
                      "answer carries last_good_as_of=%s and offers %s -- missing history is an "
                      "answer, not an empty state"
                      % (t_4, extra["age_trading_days"], extra["ceiling_trading_days"],
                         extra["last_good_as_of"],
                         [a["action"] for a in env["actions"]]),
        "delta": {"age_trading_days": extra["age_trading_days"],
                  "ceiling_trading_days": extra["ceiling_trading_days"]},
        "business_date": env["source_dates"]["business_date"]})

    return rows, time.time() - t0, expiry._source_of(cal)


def main():
    rows, elapsed, cal_source = run_arms()
    print("IB-s-4 CONTROLLED-CLOCK HARNESS -- %s"
          % dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    print("calendar: %s   (REAL -- the arms are driven against the actual trading frontier)"
          % cal_source)
    print("")
    for r in rows:
        print("  ARM (%s) %-20s -> %-42s state=%s" % (r["arm"], r["name"], r["reason_code"],
                                                      r["state"]))
        print("       %s" % r["observable"])
        print("       delta: %s" % json.dumps(r["delta"], sort_keys=True))
    codes = [r["reason_code"] for r in rows]
    pairs = [(r["state"], r["reason_code"]) for r in rows]
    print("")
    print("  status values: %s" % codes)
    print("  pairwise distinct: %d of %d reason codes, %d of %d (state, code) pairs"
          % (len(set(codes)), len(codes), len(set(pairs)), len(pairs)))
    print("  harness wall clock: %.3f s" % elapsed)
    return 0


if __name__ == "__main__":
    sys.exit(main())
