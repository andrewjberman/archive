"""ADVI_BDPARITY W2 -- the census pull orchestrator (performance-only, pass 1).

SEAT 0.4.0_DS_ClientPlatform~Y. Authorisation: Andrew-direct ~21:1xZ 2026-08-31 ("recs approved
1 and 2"), carried by 0.0.0_AB_MSTR msg 90006, dispatched by 2.0.0_SA_COO msg 90018, rulings in
90040. Record: org/tier0_exec/0.0.0_AB_MSTR/deliverables/
ANDREW_DIRECT_20260831_2110Z_OPEN_CALLS_SIX_RULINGS_GLOBALALARM_AND_THE_COMB.md

WHAT THIS DOES: invokes the ALREADY-DEPLOYED opal-assets-bd49f-reporting-pull once per chunk of
the 5,309-account pullable cohort, performance feed only. It deploys nothing and changes no code.

EVERY OPERAND IS PINNED, AND THAT IS THE POINT:
  q_start  2026-07-01  measured at the artifact (BP1-2 probe table :19 `ASOF, QSTART`)
  q_end    2026-08-28  RULED by 2.0.0_SA_COO 90040 (i). NEVER derived at fire time --
                       `expected_last_trading_day` returns 2026-08-31 today and 2026-09-01 after
                       midnight, and gold twr_daily's frontier IS date=2026-08-28, so a derived
                       q_end would ask BD for a window our gold does not cover at all.
  pull_date PINNED by the caller, identical on every invocation. RULED 90040 (ii). The puller
                       defaults it to utcnow() PER INVOCATION (:486), so a run straddling
                       midnight would split chunks across two partitions and break the resume
                       predicate and the landed-vs-requested denominator at the same time.
  feeds    ["performance"]  one vendor call per account instead of three.

THE RESUME PREDICATE, AND WHY IT IS WRITTEN THIS WAY:
`land_bronze()` :325 builds `reporting_{feed}/{pull_date}/reporting_{feed}_{acct}_{q_end}.json`
-- a BARE date segment. The handoff relayed to this seat said a successor "lists the `pull_date=`
prefix". That Hive form DOES NOT EXIST here: listing it returns 0 objects, which reads as
"nothing landed" and re-pulls the entire census. It fails toward DOUBLE SPEND and the zero is
indistinguishable from a true absence. Corrected at source before the first fire.

RESUME IS AT ACCOUNT GRAIN, NOT CHUNK GRAIN: `run()` calls land_bronze INSIDE the per-account
loop, so a Lambda timeout mid-chunk still persists every account already landed. Re-running this
script picks up exactly where it stopped.

A 401 MID-RUN ABORTS THE WHOLE RUN AND DOES NOT RETRY (2.0.0_SA_COO 90018): a 401 is not
transient, retrying proves nothing, and hammering a vendor auth endpoint is its own bad act.
"""
from __future__ import annotations

import argparse
import collections
import io
import json
import sys
import datetime as dt

import boto3
import pandas as pd

FUNCTION = "opal-assets-bd49f-reporting-pull"
GOLD_BUCKET = "opal-data-49financial"
SILVER_BUCKET = "opal-data-assets"
TWR_KEY = "gold/advi/canonical/twr_daily/date=%s/data.parquet"
XREF_PREFIX = "blackdiamond/49f/silver/dim_account_xref/"
BRONZE_FMT = "blackdiamond/49f/bronze/reporting_%s/%s/"

Q_START = "2026-07-01"
Q_END = "2026-08-28"
FEED = "performance"

# 148 was the relayed sizing for the 300 s timeout at 1.40 s/call (207 s, 31 pct margin). 120 is
# used instead because it tolerates 2.5 s/call.
#
# ⛔ CORRECTED by 2.0.0_SA_COO 90067 -- THIS COMMENT SAID "COSTS NOTHING" AND THAT CONTRADICTED THE
# ACCOUNTING IN THIS SAME FILE. run() mints a token PER INVOCATION, so the invocation count IS a
# vendor cost, and the chunk size is precisely what moves it:
#     chunk 148 -> ceil(5309/148) = 36 invocations -> 36 auth calls
#     chunk 120 -> ceil(5309/120) = 45 invocations -> 45 auth calls   (+9)
# The DATA leg is one call per account either way; only the AUTH leg moves. 120 is kept because 9
# calls against ~5,354 is noise and the timeout headroom is worth more -- but the cost is +9, NOT
# zero, and it must not be reported as zero. The seat that wrote "zero" is the same seat that had
# just discovered the auth leg one paragraph earlier.
CHUNK = 120

_s3 = boto3.client("s3")
_lam = boto3.client("lambda")


def _read_parquet(bucket: str, key: str) -> pd.DataFrame:
    return pd.read_parquet(io.BytesIO(_s3.get_object(Bucket=bucket, Key=key)["Body"].read()))


def latest_xref_key() -> str:
    """The xref MOVES (census plan section 9), so the cohort is re-derived at FIRE time and both
    figures are stated. Never reuse the plan's census-vintage number as if it were today's."""
    pag = _s3.get_paginator("list_objects_v2")
    keys = [o["Key"] for pg in pag.paginate(Bucket=SILVER_BUCKET, Prefix=XREF_PREFIX)
            for o in pg.get("Contents", []) if o["Key"].endswith("data.parquet")]
    if not keys:
        raise SystemExit("REFUSED: no dim_account_xref partition found under %s -- that is an "
                         "instrument failure, not an empty cohort." % XREF_PREFIX)
    return sorted(keys)[-1]


def derive_cohort() -> tuple:
    """PULLABLE = twr_daily accounts INTERSECT xref accounts carrying a bd_account_id.

    ids are `bd_account_id[3:]` -- the column is `z08` + the numeric BD id. The strip is applied
    only after a census confirms the prefix is uniform, because a mixed prefix would silently
    truncate a different id space."""
    twr = _read_parquet(GOLD_BUCKET, TWR_KEY % Q_END)
    xkey = latest_xref_key()
    xr = _read_parquet(SILVER_BUCKET, xkey)

    twr_acct = set(twr["account_id"].dropna().astype(str))
    # DROP nulls BEFORE astype(str): astype on a None yields the STRING "None", which enters the
    # set as a phantom key and inflates the residual by one. Measured at this seat 2026-08-31 --
    # it produced a false "67 vs the plan's 66" finding that was this instrument, not the data.
    xr2 = xr[xr["bd_account_id"].notna() & xr["schwab_account_id"].notna()].copy()
    xr2["sa"] = xr2["schwab_account_id"].astype(str)
    xr2["bd"] = xr2["bd_account_id"].astype(str)

    prefixes = collections.Counter(xr2["bd"].str[:3])
    if len(prefixes) != 1 or "z08" not in prefixes:
        raise SystemExit("REFUSED: bd_account_id prefix is NOT uniformly 'z08' (%r). The [3:] "
                         "strip would truncate a different id space." % dict(prefixes))
    xr2["derived"] = xr2["bd"].str[3:]

    pull = xr2[xr2["sa"].isin(twr_acct)]
    cohort = [{"bd_account_id": int(r.derived), "schwab_account": r.sa, "inception": None}
              for r in pull.itertuples()]
    cohort.sort(key=lambda a: a["bd_account_id"])
    resid = {"ours_not_pullable": len(twr_acct - set(xr2["sa"])),
             "bd_pullable_no_our_value": len(set(xr2["sa"]) - twr_acct),
             "twr_accounts": len(twr_acct), "xref_with_bd": len(xr2), "xref_key": xkey}
    return cohort, resid


def landed_accounts(pull_date: str) -> set:
    """List the REAL prefix (bare date segment), paginated. A page is not an answer."""
    prefix = BRONZE_FMT % (FEED, pull_date)
    pag = _s3.get_paginator("list_objects_v2")
    out = set()
    for pg in pag.paginate(Bucket=SILVER_BUCKET, Prefix=prefix):
        for o in pg.get("Contents", []):
            base = o["Key"].rsplit("/", 1)[-1]
            # reporting_performance_<acct>_<q_end>.json
            if base.startswith("reporting_%s_" % FEED) and base.endswith("_%s.json" % Q_END):
                mid = base[len("reporting_%s_" % FEED):-len("_%s.json" % Q_END)]
                if mid.isdigit():
                    out.add(int(mid))
    return out


def preflight() -> bool:
    """ONE vendor auth call, ZERO data calls, ZERO objects -- and it exercises THIS SCRIPT's own
    invoke/parse path, not just the CLI's.

    MECHANISM: `feeds: []`. In run() the auth chain is UNCONDITIONAL and PRECEDES the feed check:
        :406 _assert_firm_separation()
        :408 cookie = load_bd_session()
        :410 token  = get_clientview_token(cookie)   <- THE ONE VENDOR CALL
        :412 selected_feeds = resolve_feeds(feeds)   <- RAISES on the empty list
    So reaching a :412 ValueError is ONLY possible by passing :410. A dead cookie cannot surface
    as that error -- it fails at :410 with a different named error or a 401. The probe
    discriminates and it structurally cannot spend a data call.

    `accounts` carries one real id because `event.get("accounts") or discover_accounts()` treats
    an EMPTY list as falsy and would fall back to the tax-SMA roster. It is never reached.
    """
    payload = {"leg": "reporting", "q_start": Q_START, "q_end": Q_END,
               "accounts": [{"bd_account_id": 13477111, "schwab_account": "PREFLIGHT-NOT-USED",
                             "inception": None}],
               "feeds": []}
    r = _lam.invoke(FunctionName=FUNCTION, InvocationType="RequestResponse",
                    Payload=json.dumps(payload).encode())
    body = json.loads(r["Payload"].read() or b"{}")
    msg = str(body.get("errorMessage", ""))
    trace = " ".join(body.get("stackTrace", []) or [])
    ok = body.get("errorType") == "ValueError" and "EMPTY feed list" in msg and "resolve_feeds" in trace
    print("PRE-FLIGHT: errorType=%s" % body.get("errorType"))
    print("  message : %s" % msg[:120])
    if ok:
        print("  VERDICT : AUTH PASSED -- reached resolve_feeds, which is only reachable past the")
        print("            token mint. 1 vendor auth call, 0 data calls, 0 objects.")
    else:
        print("  VERDICT : AUTH DID NOT PASS (or the signature changed). Full body:")
        print("            %s" % json.dumps(body)[:500])
        print("  A 401 IS NOT TRANSIENT -- do NOT retry. Wait for a fresh mint.")
    return ok


def verify_untouched(before_path: str) -> bool:
    """Criterion 3: both prior snapshots UNTOUCHED. Compares the live object versions against the
    pinned before-image BY VersionId -- never by count, because a count is equal under a
    same-count overwrite."""
    before = json.load(open(before_path))
    pinned = {r["key"]: r["version_id"] for r in before["versions"] if r.get("is_latest")}
    pag = _s3.get_paginator("list_object_versions")
    live = {}
    for pg in pag.paginate(Bucket=before["bucket"], Prefix=before["prefix"]):
        for v in pg.get("Versions", []):
            if v["IsLatest"]:
                live[v["Key"]] = v["VersionId"]
    moved = [k for k, v in pinned.items() if live.get(k) != v]
    gone = [k for k in pinned if k not in live]
    print("CRITERION 3 -- prior snapshots untouched")
    print("  pinned baseline objects : %d" % len(pinned))
    print("  still at pinned VersionId: %d of %d" % (len(pinned) - len(moved), len(pinned)))
    print("  MOVED (version changed) : %d %s" % (len(moved), moved[:5]))
    print("  DISAPPEARED             : %d %s" % (len(gone), gone[:5]))
    print("  VERDICT: %s" % ("UNTOUCHED" if not moved and not gone else "*** TOUCHED -- INVESTIGATE ***"))
    return not moved and not gone


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pull-date", required=True,
                    help="PINNED ingestion asOf, identical on every invocation (YYYY-MM-DD)")
    ap.add_argument("--plan-only", action="store_true",
                    help="derive cohort + resume set and print the plan. ZERO vendor calls.")
    ap.add_argument("--preflight", action="store_true",
                    help="ONE auth call, zero data calls. Run this against a fresh mint first.")
    ap.add_argument("--verify-untouched", metavar="BEFORE_JSON", default="",
                    help="criterion-3 check against a pinned before-image. ZERO vendor calls.")
    ap.add_argument("--limit-chunks", type=int, default=0,
                    help="fire at most N chunks (0 = all). For a bounded first fire.")
    a = ap.parse_args()

    dt.date.fromisoformat(a.pull_date)  # fail closed on a malformed pin

    if a.verify_untouched:
        return 0 if verify_untouched(a.verify_untouched) else 1
    if a.preflight:
        return 0 if preflight() else 1

    cohort, resid = derive_cohort()
    done = landed_accounts(a.pull_date)
    todo = [c for c in cohort if c["bd_account_id"] not in done]
    chunks = [todo[i:i + CHUNK] for i in range(0, len(todo), CHUNK)]

    print("ADVI_BDPARITY W2 -- %s" % dt.datetime.now(dt.timezone.utc).isoformat())
    print("  q_start=%s  q_end=%s  pull_date=%s  feeds=[%r]" % (Q_START, Q_END, a.pull_date, FEED))
    print("  xref partition (fire-time)   : %s" % resid["xref_key"])
    print("  twr_daily accounts           : %d" % resid["twr_accounts"])
    print("  xref rows with BOTH ids      : %d" % resid["xref_with_bd"])
    print("  COHORT (pullable intersect)  : %d" % len(cohort))
    print("  ours NOT pullable            : %d" % resid["ours_not_pullable"])
    print("  BD-pullable, no our value    : %d" % resid["bd_pullable_no_our_value"])
    print("  already landed (resume)      : %d" % len(done))
    print("  REMAINING to pull            : %d  in %d chunk(s) of %d" % (len(todo), len(chunks), CHUNK))
    print("  projected vendor calls       : %d data + %d auth (one token mint per invocation) = %d"
          % (len(todo), len(chunks), len(todo) + len(chunks)))

    if a.plan_only:
        print("PLAN-ONLY: zero vendor calls made.")
        return 0
    if not todo:
        print("NOTHING TO DO: every cohort account already landed under this pull_date.")
        return 0

    if a.limit_chunks:
        chunks = chunks[:a.limit_chunks]
        print("  LIMITED to %d chunk(s) this fire." % len(chunks))

    data_calls = auth_calls = 0
    t0 = dt.datetime.now(dt.timezone.utc)
    for i, ch in enumerate(chunks, 1):
        if not ch:  # a payload with an empty accounts list falls back to discover_accounts()
            raise SystemExit("REFUSED: empty chunk -- `accounts or discover_accounts()` would "
                             "silently pull the tax-SMA roster instead of the census cohort.")
        payload = {"leg": "reporting", "q_start": Q_START, "q_end": Q_END,
                   "pull_date": a.pull_date, "feeds": [FEED], "accounts": ch}
        r = _lam.invoke(FunctionName=FUNCTION, InvocationType="RequestResponse",
                        Payload=json.dumps(payload).encode())
        auth_calls += 1
        body = json.loads(r["Payload"].read() or b"{}")
        if r.get("FunctionError"):
            msg = json.dumps(body)[:400]
            print("CHUNK %d/%d FAILED: %s" % (i, len(chunks), msg))
            if any(t in msg for t in ("401", "no access_token", "session stale", "Unauthorized")):
                print("ABORT: auth-class failure. A 401 is not transient -- NOT retrying. "
                      "Landed work is durable; re-run after a fresh mint to resume.")
                break
            print("ABORT: non-auth failure -- stopping rather than burning the budget blind.")
            break
        got = int(body.get("count", 0))
        data_calls += got
        el = (dt.datetime.now(dt.timezone.utc) - t0).total_seconds()
        print("  chunk %3d/%d  requested=%3d landed=%3d  cum_data_calls=%5d  elapsed=%.0fs"
              % (i, len(chunks), len(ch), got, data_calls, el))

    final = landed_accounts(a.pull_date)
    print()
    print("REQUESTED this run : %d" % sum(len(c) for c in chunks))
    print("VENDOR CALLS       : %d data + %d auth = %d" % (data_calls, auth_calls, data_calls + auth_calls))
    print("LANDED (S3 census) : %d of %d cohort" % (len(final), len(cohort)))
    print("STILL MISSING      : %d" % len([c for c in cohort if c["bd_account_id"] not in final]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
