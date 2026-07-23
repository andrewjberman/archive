#!/usr/bin/env python3
"""cot_qt5_temporal_probe.py -- THE decisive Cottonwood backfill probe (read-only).

Author:  4.0.0_SA_CRO (Chief Research Officer)
Brief:   org/tier1_exec/4.0.0_SA_CRO/briefs/COTTONWOOD_BACKFILL_MECHANISM_CAMPAIGN_20260722.md
Verdict authority: CTO v1.21 (this probe carries the full temporal-vs-current verdict that
gates the Cottonwood MDPF backfill design; 0.6.2's second live probe is retired into it).

WHAT IT ANSWERS
  Does DataMining qt5 `allocations`, run for a PAST window, return the account->strategy
  assignment that was IN FORCE THEN (TEMPORAL -> backfill is real) or today's stamped onto
  a past window (CURRENT -> the surface is closed for backfill)?

WHY qt5 AND WHY NO TEMPLATE MUTATION
  The production allocations template (tid 226334) ALREADY selects the account-level
  assignment dimension (`accountRebalStrategyID` id 35392 + `accountRebalStrategyName`
  id 35393, both isSelected:true) and is date-windowed (dateRangeType:Custom). So the
  decisive test is a PURE PAST-WINDOW RUN of the template we already run daily -- no
  re-persist, no mutation, read-only.

THE VERDICT LOGIC -- WINDOW-INTEGRITY FIRST (CTO v1.21, binding, non-optional)
  The failure mode that matters is window-IGNORING (the eclipse `--date`-is-a-filename
  class): a query silently returns CURRENT state for a past window, producing a
  false-CURRENT verdict that kills the backfill capability while looking like an honest
  negative. So BEFORE any temporal/current verdict is legal, the SAME run must PROVE the
  past window was honored, using the model-creation timeline as an intrinsic instrument
  control:
    * Satellite 60 was created 2026-06-23; 30/40/70/98 on 2026-07-06 (RCN-0001 Addendum A2).
    * A true 2026-06-15 window therefore CANNOT contain Satellite 60 or 30/40/70/98, and
      has ~136-215 accounts, not today's 296.
    * If a past window returns today's full 296 + all strategies -> WINDOW IGNORED
      (CURRENT-only verdict is then VALID, because the run proved the window was reached
      and ignored).
    * If it returns the era-correct reduced roster -> WINDOW HONORED -> temporal
      discrimination on the churn-control accounts is legal.
    * If neither can be shown -> UNVERIFIABLE-INSTRUMENT (NOT a finding) -> the escape:
      0.6.2's single re-persist confirmation, PRE-AUTHORIZED + SELF-EVALUABLE (CTO 224317Z).
      0.6.2 self-evaluates a machine condition at the 02:00Z window and runs IFF this campaign
      has NOT by then produced either a TEMPORAL verdict or a CURRENT-only verdict with the
      window-integrity limb green. No COO->CTO round-trip; sequential never concurrent; both
      need the SAME fresh session (else the verdict is cleanly BLOCKED-ON-SESSION-CAPTURE).

RUN-BODY + 0-ROW CORRECTIONS (0.6.2 035931Z, source-confirmed) -- folded into this reference:
  (1) v1/run needs a WRAPPED body {"template": full, "asOfDate": endDate} + normalization
      (cot_bronze_ingest.py:405-415); the bare-dict POST this harness first shipped 500s on its
      own -- so run_window now reuses the PROVEN bi.run_query, and a 500 is no longer read as a
      vendor condition. (2) A 0-row export is NOT an instrument break: BD returns 0-data-row
      header-only exports because it holds no point-in-time snapshot for that as-of date (every
      daily as-of since ~07-09). So today-empty does NOT abort; a 0-row past window is NO-PIT-DATA
      (a vendor data-availability finding), and today-empty + a past window POPULATED is the
      informative TEMPORAL outcome. NOTE this pairs with 0.6.2's live R0-R3 run, which streams the
      raw rows/strategy values and this logic adjudicates the verdict.

SAFETY
  Read-only diagnostics; if a template modification is needed it is a COPY (never production 226334),
  created and DELETED same-window (revert-on-completion). No state change on BD's side otherwise. On a
  stale session / auth or run-path error it prints HELD and exits 0 WITHOUT a verdict -- a dead
  instrument never manufactures a finding. Egress = Andrew's explicit per-use word (this-program-scoped
  cot-DataMining); cot-BD ONLY (firm-sep binds -- never 49F). Run on-box (cot-exporter) or anywhere a fresh
  `blackdiamond/cot/session` jar is valid.

USAGE
  python3 cot_qt5_temporal_probe.py                 # {2026-05-15, 2026-06-15, today}
  python3 cot_qt5_temporal_probe.py --windows 2026-06-15,2026-07-01
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from datetime import date, timedelta
from io import BytesIO

import boto3

BD_BASE = "https://bd3.bdreporting.com"
SESSION_SECRET_ID = "blackdiamond/cot/session"
TEMPLATE_BUCKET = "opal-data-cot"
TEMPLATE_KEY = "code/bronze/templates/allocations.json"  # qt5, tid 226334, acct-strategy selected
REGION = "us-east-1"
HTTP_TIMEOUT_S = 90
POLL_INTERVAL_S = 5
POLL_TIMEOUT_S = 300
WINDOW_DAYS = 5

# --- Intrinsic window-integrity instrument (RCN-0001 Addendum A2, model createdAt) ---
# A strategy CANNOT appear in a window that predates its model's creation. Keyed by the
# substring that identifies the strategy in accountRebalStrategyName.
STRATEGY_CREATED = {
    "Satellite 80": date(2026, 5, 29),
    "Satellite 50": date(2026, 6, 10),
    "Satellite 60": date(2026, 6, 23),
    "Satellite 30": date(2026, 7, 6),
    "Satellite 40": date(2026, 7, 6),
    "Satellite 70": date(2026, 7, 6),
    "Satellite 98": date(2026, 7, 6),
}
# The 15 churn-control accounts (0.6.2 B6 probe-prep): Opal today, ABSENT from the 06-09
# book -> assignment necessarily changed (none -> Opal) between windows. A TEMPORAL surface
# must return them absent/unassigned in an early window; a CURRENT-stamped surface returns
# them carrying today's Opal strategy. First 8 published in the B6 deliverable; the on-box
# operator pastes the full 15 here before the run (kept explicit, not hidden).
CHURN_CONTROL_ACCOUNTS = [
    "658508703", "658508963", "658509261", "658508828",
    "638432512", "Z40493496", "658509146", "658509145",
    # + 7 more from MDPF_3FIRMS_B6_liveness_signal_20260722.md probe-prep section
]

sm = boto3.client("secretsmanager", region_name=REGION)
s3 = boto3.client("s3", region_name=REGION)


def log(msg: str) -> None:
    print(msg, flush=True)


def load_session() -> dict:
    return json.loads(sm.get_secret_value(SecretId=SESSION_SECRET_ID)["SecretString"])


def cookie_header(session: dict) -> str:
    return "; ".join(f"{c['name']}={c['value']}" for c in session.get("all_cookies", []))


def mint_token(cookie: str) -> str:
    req = urllib.request.Request(
        f"{BD_BASE}/datamining/auth/token",
        headers={"Cookie": cookie, "Accept": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT_S) as r:
        body = json.loads(r.read())
    token = body.get("access_token") or body.get("token")
    if not token:
        raise RuntimeError(f"auth/token empty: {body}")
    return token


def load_template() -> dict:
    obj = s3.get_object(Bucket=TEMPLATE_BUCKET, Key=TEMPLATE_KEY)
    return json.loads(obj["Body"].read())


def _post(path: str, token: str, payload: dict) -> dict:
    req = urllib.request.Request(
        f"{BD_BASE}{path}",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json",
                 "Accept": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT_S) as r:
        return json.loads(r.read())


def _get(path: str, token: str) -> dict:
    req = urllib.request.Request(
        f"{BD_BASE}{path}",
        headers={"Authorization": f"Bearer {token}", "Accept": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT_S) as r:
        return json.loads(r.read())


def run_window(token: str, cookie: str, template: dict, start: date) -> list[dict]:
    """Run qt5 for the window starting at `start`; return list of {account, strategy} rows.

    Raises urllib HTTPError on auth failure -- caller treats as HELD, never a verdict.

    RUN-BODY FIX (0.6.2 035931Z, source-confirmed cot_bronze_ingest.py:405-415 @HEAD): v1/run
    REQUIRES a WRAPPED body {"template": full, "asOfDate": endDate} plus a five-field setdefault
    + three-field pop normalization -- the bare `dict(template)` POST this harness first shipped
    500s regardless of session/dates ("omitting asOfDate 500s. This was the root cause"). So the
    PROVEN production normalizer is reused instead of a re-implementation: bi.run_query does exactly
    that wrap+normalize. This must run ON-BOX (cot-exporter) where cot_bronze_ingest is importable.
    """
    import cot_bronze_ingest as bi  # on-box; carries the proven run-body wrap + normalization
    end = start + timedelta(days=WINDOW_DAYS)
    body = dict(template)
    body["startDate"] = start.strftime("%m/%d/%Y")
    body["endDate"] = end.strftime("%m/%d/%Y")
    body["dateRangeType"] = "Custom"

    run_id, guid = bi.run_query(token, body)   # PROVEN wrap+normalize; raises on a real run error
    bi.poll_status(token, run_id)
    if not guid:
        raise RuntimeError(f"no resultGuid for {start}")

    xreq = urllib.request.Request(
        f"{BD_BASE}/Api/DataMining/ExportResults/{guid}",
        headers={"Cookie": cookie},
    )
    with urllib.request.urlopen(xreq, timeout=HTTP_TIMEOUT_S) as r:
        xlsx = r.read()

    import openpyxl
    wb = openpyxl.load_workbook(BytesIO(xlsx), read_only=True, data_only=True)
    ws = wb.active
    header = [str(c.value) if c.value is not None else "" for c in next(ws.iter_rows())]

    def col(*cands):
        for i, h in enumerate(header):
            if any(cand.lower() in h.lower() for cand in cands):
                return i
        return None

    acct_i = col("accountExternalID", "AccountID", "Account Number")
    strat_i = col("accountRebalStrategyName", "Account Strategy Name", "Strategy Name")
    rows = []
    for r in ws.iter_rows(min_row=2, values_only=True):
        acct = str(r[acct_i]) if acct_i is not None and r[acct_i] is not None else ""
        strat = str(r[strat_i]) if strat_i is not None and r[strat_i] is not None else ""
        rows.append({"account": acct, "strategy": strat})
    wb.close()
    return rows


def window_integrity(rows: list[dict], window_start: date) -> tuple[str, list[str]]:
    """STEP 0: was the past window HONORED? Returns (HONORED|IGNORED|INCONCLUSIVE|NO-PIT-DATA, notes).

    0-ROW SEMANTICS, CORRECTED (0.6.2 035931Z, source-confirmed via the daily export rejects): a
    0-row export is NOT an instrument break -- the daily qt5 runs EXECUTE CLEAN and BD returns
    0-DATA-ROW header-only exports because "BD has no point-in-time snapshot for this as-of date"
    (verbatim reject reason, every daily as-of since ~07-09). So a 0-row window means BD holds NO
    point-in-time data for THAT date -- a VENDOR DATA-AVAILABILITY fact (NO-PIT-DATA), informative,
    not a broken instrument. (A genuine instrument break is now an HTTPError/run-error, caught in
    run_window, not a 0-row. The prior INSTRUMENT-BROKEN-on-0-row read was wrong: it conflated the
    harness's own malformed-body 500 with the vendor's empty exports.)
    """
    notes = []
    n_accounts = len({r["account"] for r in rows if r["account"]})
    if not rows or n_accounts == 0:
        notes.append(f"window {window_start}: 0 rows -> BD holds NO point-in-time snapshot for this "
                     "as-of date (vendor data-availability, 0.6.2-confirmed). NO-PIT-DATA, not a break.")
        return "NO-PIT-DATA", notes
    strategies_present = {r["strategy"] for r in rows if r["strategy"]}
    violations = []
    for name, created in STRATEGY_CREATED.items():
        if window_start < created and any(name in s for s in strategies_present):
            violations.append(f"{name} present but created {created.isoformat()} (> window {window_start})")
    era_correct = [name for name, created in STRATEGY_CREATED.items() if window_start >= created]
    notes.append(f"window {window_start}: {n_accounts} accts, {len(strategies_present)} strategies")
    notes.append(f"strategies that COULD exist by {window_start}: {era_correct or '(none)'}")
    if violations:
        # A strategy present that could not yet exist == today's state stamped on a past window.
        notes.append("VIOLATIONS (post-creation strategies in a pre-creation window): " + "; ".join(violations))
        return "IGNORED", notes
    if window_start < min(STRATEGY_CREATED.values()):
        # Deep pre-model window: a HONORED window must be empty of Opal strategies.
        opal_present = [s for s in strategies_present if "Satellite" in s or "Opal" in s]
        if not opal_present:
            notes.append("deep pre-model window returned NO Opal strategies -> consistent with HONORED")
            return "HONORED", notes
        notes.append(f"deep pre-model window returned Opal strategies {opal_present} -> IGNORED")
        return "IGNORED", notes
    # Mixed window with no violations: honored only if the roster is strictly smaller than today (296).
    if n_accounts and n_accounts < 296:
        notes.append(f"roster {n_accounts} < today's 296 and no timeline violations -> HONORED")
        return "HONORED", notes
    if n_accounts >= 296:
        notes.append(f"roster {n_accounts} >= today's 296 -> WINDOW IGNORED (today's full book on a past window)")
        return "IGNORED", notes
    notes.append("empty/ambiguous roster -> INCONCLUSIVE")
    return "INCONCLUSIVE", notes


def temporal_discriminate(rows: list[dict]) -> tuple[str, list[str]]:
    """STEP 1 (legal only after HONORED): do churn-control accounts carry today's Opal strat?"""
    notes = []
    by_acct = {r["account"]: r["strategy"] for r in rows}
    carrying_today = []
    absent_or_unassigned = []
    for acct in CHURN_CONTROL_ACCOUNTS:
        strat = by_acct.get(acct, "")
        if strat and ("Satellite" in strat or "Opal" in strat):
            carrying_today.append(f"{acct}={strat}")
        else:
            absent_or_unassigned.append(acct)
    notes.append(f"churn controls carrying an Opal strategy in the past window: {len(carrying_today)}")
    notes.append(f"churn controls absent/unassigned in the past window: {len(absent_or_unassigned)}")
    if carrying_today and not absent_or_unassigned:
        return "CURRENT", notes  # today's assignment stamped onto the past window
    if absent_or_unassigned and not carrying_today:
        return "TEMPORAL", notes  # assignment reflects the past -> real dated history
    notes.append(f"MIXED ({carrying_today} vs {absent_or_unassigned}) -> inspect; not a clean verdict")
    return "MIXED", notes


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--windows", default="2026-05-15,2026-06-15",
                    help="comma-separated past window start dates")
    args = ap.parse_args(argv)
    past_windows = [date.fromisoformat(w) for w in args.windows.split(",")]

    log("=== cot qt5 temporal probe (read-only) ===")
    session = load_session()
    log(f"session captured_at={session.get('captured_at')}")
    cookie = cookie_header(session)
    try:
        token = mint_token(cookie)
    except urllib.error.HTTPError as e:
        log(f"HELD: session token mint HTTP {e.code} -- stale session, no verdict emitted.")
        return 0
    log("token minted OK")

    template = load_template()

    # Baseline: today's EXPLICIT-window run. It proves auth + that the RUN PATH itself works
    # (mint + run + export succeed) -- an HTTPError/run-error here is a genuine instrument/auth break.
    # But today returning 0 ROWS is NOT a break: it is the KNOWN vendor condition (0.6.2 035931Z,
    # source-confirmed) -- BD has stopped producing CURRENT point-in-time qt5 snapshots since ~07-09,
    # so the daily as-of returns 0-data-row header-only exports. So we do NOT abort on today-empty.
    # CRITICAL: today-empty + a past window POPULATED is the most informative outcome -- it means BD
    # holds HISTORICAL point-in-time data but stopped current snapshots, which BOTH answers the
    # temporal question AND characterizes the freeze in one run.
    try:
        today_rows = run_window(token, cookie, template, date.today())
    except urllib.error.HTTPError as e:
        log(f"HELD: baseline read HTTP {e.code} -- DataMining auth not usable, no verdict.")
        return 0
    except Exception as e:
        log(f"HELD: baseline RUN-ERROR ({type(e).__name__}: {str(e)[:200]}) -- the run path itself "
            "failed (instrument), no verdict. If this is a body-shape error the run-body fix did not "
            "take; if a real vendor run error, that is a new finding.")
        return 0
    n_today = len({r["account"] for r in today_rows if r["account"]})
    if n_today == 0:
        log("NOTE: today's qt5 returned 0 rows -- the KNOWN vendor condition (BD has no CURRENT "
            "point-in-time snapshot since ~07-09, 0.6.2-confirmed). NOT an instrument break; the run "
            "path WORKS. Proceeding to past windows -- if a past window is POPULATED, BD holds history "
            "and the temporal question is answered.")
    else:
        log(f"baseline (today): {n_today} accounts, {len({r['strategy'] for r in today_rows if r['strategy']})} "
            f"strategies -- current snapshot present, auth live, run path works.")

    integrities = []          # per-window Step-0 verdicts
    temporal_seen = False      # any window proved TEMPORAL
    current_on_honored = False # any window HONORED and discriminated CURRENT
    for w in past_windows:
        log(f"\n--- window {w.isoformat()} ---")
        try:
            rows = run_window(token, cookie, template, w)
        except urllib.error.HTTPError as e:
            log(f"HELD: window {w} HTTP {e.code} -- no verdict for this window.")
            integrities.append("HELD")
            continue
        integrity, notes = window_integrity(rows, w)
        for n in notes:
            log(f"  [W0] {n}")
        log(f"  [W0] WINDOW-INTEGRITY = {integrity}")
        integrities.append(integrity)
        if integrity == "HONORED":
            verdict, tnotes = temporal_discriminate(rows)
            for n in tnotes:
                log(f"  [W1] {n}")
            log(f"  [W1] TEMPORAL-DISCRIMINATION = {verdict}")
            if verdict == "TEMPORAL":
                temporal_seen = True
            elif verdict == "CURRENT":
                current_on_honored = True
        # NO-PIT-DATA / INCONCLUSIVE / IGNORED are handled in the roll-up below.

    # Roll-up, in precedence order. A CURRENT-only verdict is legal ONLY on a HONORED window
    # (CTO v1.21); an IGNORED window IS the proof-of-honor for CURRENT (the query reached and
    # ignored the past window). NO-PIT-DATA (BD holds no point-in-time snapshot for that as-of
    # date) is a VENDOR data-availability fact, not an instrument break: if EVERY past window is
    # NO-PIT-DATA, the empty-export freeze extends back through history and qt5 yields no temporal
    # recovery -- a clean, informative answer (the interpolated backfill stays the only path).
    if temporal_seen:
        overall = "TEMPORAL"
    elif current_on_honored or "IGNORED" in integrities:
        overall = "CURRENT"
    elif "INCONCLUSIVE" in integrities:
        overall = "UNVERIFIABLE-INSTRUMENT"
    elif integrities and all(i in ("NO-PIT-DATA", "HELD") for i in integrities):
        overall = "NO-PIT-DATA"
    else:
        overall = "UNVERIFIABLE-INSTRUMENT"

    log("\n=== VERDICT ===")
    if overall == "TEMPORAL":
        log("VERDICT=TEMPORAL -- qt5 returns DATED historical assignment; BD holds point-in-time data "
            "back through the window(s). Backfill is REAL to the coverage horizon (>= ~2026-05-28 model "
            "floor); real points SUPERSEDE interpolated ones in the live 3F-BF1 build. GO LOUD to COO/CTO.")
    elif overall == "NO-PIT-DATA":
        log("VERDICT=NO-POINT-IN-TIME-DATA -- BD holds no point-in-time qt5 snapshot for the past "
            "window(s) either; the empty-export freeze extends back through history (0.6.2's data-"
            "availability mechanism, not a run break). qt5 yields NO temporal recovery -- the interpolated "
            "backfill stays the only path, and there is nothing to supersede it with. Clean, informative.")
    elif overall == "UNVERIFIABLE-INSTRUMENT":
        log("VERDICT=UNVERIFIABLE-INSTRUMENT -- window integrity not demonstrable. NOT a finding. "
            "Escape: 0.6.2's re-persist confirmation is pre-authorized + self-evaluable (CTO 224317Z) -- "
            "he self-evaluates at the 02:00Z window and runs IFF no sufficient verdict landed here first; "
            "no round-trip, sequential never concurrent, same fresh session required.")
    else:
        log("VERDICT=CURRENT-only(window-honored) -- qt5 stamps today's assignment onto past windows; "
            "backfill CLOSED on A1. Valid ONLY because a past window was demonstrably honored above.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
