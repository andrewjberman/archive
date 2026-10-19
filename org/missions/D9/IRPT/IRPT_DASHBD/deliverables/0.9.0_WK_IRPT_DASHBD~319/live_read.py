"""IRPT_DASHBD round 132, workstream B-IN (issuer 2.0.0_SA_COO~I2), cell DB-i-19 -- the LIVE read of the Scope feed's first silver.

Runs the round-129 run script's run_real() on the landed silver into a PRIVATE directory (the real run through the round-127
wrapper), then reads each landed day's bronze envelope through the GET-only reader and keeps counts only: the universe rows,
the failed-household count, the per-call row counts and the households-without-id count. Silver rows per day are the lengths of
the silver frames. Writes the private extract and the repo record. Read-only against AWS: LIST and GET only.

Usage: python -I <this file> --private <private dir, exists and empty> --record <record file to write>
The wrapper output goes to <private dir>/wrapper_out, which must not exist yet.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import importlib.util
import json
import sys
from pathlib import Path


def _find_root() -> Path:
    here = Path(__file__).resolve()
    for anc in here.parents:
        if (anc / "lib" / "trading_calendar.py").is_file() and (anc / "data").is_dir():
            return anc
    raise SystemExit("repo root not found above this file")


ROOT = _find_root()
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "data" / "assets" / "scripts" / "gold" / "irpt_reporting" / "adapters"))
from lib import trading_calendar as tc  # noqa: E402
import inflection_account_dim as iad  # noqa: E402
import inflection_account_return_daily as iar  # noqa: E402

RUN_SCRIPT = ROOT / "org" / "missions" / "D9" / "IRPT" / "IRPT_DASHBD" / "deliverables" / "0.9.0_WK_IRPT_DASHBD~316" / "run_scope_feed_real.py"
FEED_SCRIPT = ROOT / "data" / "inf" / "manual_api" / "pull_inflection_scope_account_returns.py"
PART = "date="
STATIC_LIMIT = ("This establishes only that the wrapper output on the landed silver days matches the feed's own manifest counts and "
                "the calendar arithmetic. It does not establish any return value against Orion, the coverage of days not yet landed, "
                "or the correctness of the boundary measure beyond the counts shown.")


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def trading_days_iso(first: str, last: str) -> list:
    return [d.isoformat() for d in tc.trading_days_between(first, last)]


def agrees(e: dict) -> bool:
    return e["silver_rows"] == sum(e["call_row_counts"]) and e["households_failed"] == 0 and e["universe_rows"] >= e["silver_rows"]


def basis_words(days: dict, run: dict, parts: list, bronze_parts: list) -> str:
    names = sorted(days)
    agree = sum(1 for d in names if agrees(days[d]))
    gap_days = [abs(days[d]["silver_rows"] - sum(days[d]["call_row_counts"])) for d in names]
    gap_days = [g for g in gap_days if g]
    failed_days = sum(1 for d in names if days[d]["households_failed"] > 0)
    short_universe = sum(1 for d in names if days[d]["universe_rows"] < days[d]["silver_rows"])
    absent = json.dumps(run["absent_by_reason"], sort_keys=True)
    b = run["boundary"]
    c = run["chain"]
    return ("Landed silver day partitions listed: %d; bronze manifest partitions listed: %d; days read: %d. "
            "Silver row count agrees with the bronze manifest on %d day(s) and disagrees on %d day(s): %d with a row gap "
            "(gap sizes in rows, day order: %s), %d with failed households, %d with universe rows below the silver count. "
            "Rows present %d, rows absent %d; ABSENT rows by reason class: %s. "
            "Boundary measure: %s pairs, %s equal within 0.005, maximum relative difference %s basis points. "
            "Chain check status %s over %s accounts checked, %s matching. %s"
            % (len(parts), len(bronze_parts), len(names), agree, len(names) - agree, len(gap_days),
               ", ".join(str(g) for g in gap_days) or "none", failed_days, short_universe,
               run["rows_present"], run["rows_absent"], absent,
               b["pairs"], b["pairs_equal"], b["max_rel_diff_bp"],
               c["status"], c["accounts_checked"], c["accounts_matching"], STATIC_LIMIT))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Live read of the Scope feed's first silver through the wrapper, against the manifest.")
    ap.add_argument("--private", required=True, help="a private directory that exists and is empty")
    ap.add_argument("--record", required=True, help="the record file to write (ASCII JSON)")
    args = ap.parse_args(argv)
    priv = Path(args.private)
    if not priv.is_dir() or any(priv.iterdir()):
        raise SystemExit("the private directory must exist and be empty")
    out_dir = priv / "wrapper_out"
    if out_dir.exists():
        raise SystemExit("the wrapper output directory must not exist yet")

    run_mod = _load("run_scope_feed_real_r132", RUN_SCRIPT)
    pull = _load("pull_scope_feed_r132", FEED_SCRIPT)
    reader = iad.InflectionSilverReader()
    _n, holdings = reader.latest_partition(iar.ORION_SILVER + "fact_positions")
    _n, roster = reader.latest_partition(iar.ORION_SILVER + "fact_assets")
    dim_ids = iad.build_account_dim(holdings, roster).column("account_id").to_pylist()
    run = run_mod.run_real(reader, str(out_dir), dim_ids, trading_days_iso, iad.FIRM, 0)
    print("status: %s" % run["status"])
    if run["status"] != "RAN":
        rec = {"run": run, "verdict": "NOT_RUN"}
        Path(args.record).write_bytes((json.dumps(rec, indent=2, sort_keys=True) + "\n").encode("ascii"))
        return 1

    parts = reader.list_partitions(run_mod.TABLE_URI)
    bronze_prefix = pull.feed_addresses(parts[0][len(PART):])[0].split("/" + PART)[0]
    bronze_parts = reader.list_partitions(bronze_prefix)
    direct_gets = 0
    days = {}
    for name in parts:
        day = name[len(PART):]
        frame = reader.read_parquet(run_mod.TABLE_URI + "/" + name + "/data.parquet")
        bucket, key = reader._split(pull.feed_addresses(day)[0])
        body = reader._api().get_object(Bucket=bucket, Key=key)["Body"].read()
        direct_gets += 1
        env = json.loads(gzip.decompress(body).decode("utf-8"))
        del body
        wo = env["households_without_id"]
        days[day] = {
            "silver_rows": int(len(frame)),
            "universe_rows": int(env["universe_rows"]),
            "households_failed": len(env["households_failed"]),
            "call_row_counts": [int(c["row_count"]) for c in env["calls"]],
            "households_without_id": int(wo) if isinstance(wo, int) else len(wo),
        }
        del env

    ex_path = priv / "live_extract.json"
    ex_bytes = json.dumps({"days": days}, sort_keys=True).encode("ascii")
    ex_path.write_bytes(ex_bytes)

    names = sorted(days)
    agree = sum(1 for d in names if agrees(days[d]))
    disagree = len(names) - agree
    failed_days = sum(1 for d in names if days[d]["households_failed"] > 0)
    tdays = trading_days_iso(names[0], names[-1])
    rec = {
        "script": {"file": Path(__file__).resolve().relative_to(ROOT).as_posix(),
                   "sha256": sha(Path(__file__).resolve().read_bytes())},
        "extract": {"path": ex_path.resolve().as_posix(), "sha256": sha(ex_bytes)},
        "run": run,
        "days_total": len(names),
        "days_manifest_agree": agree,
        "days_manifest_disagree": disagree,
        "days_with_failed_households": failed_days,
        "trading_days_in_window": len(tdays),
        "expected_rows": run["accounts_in_feed"] * len(tdays),
        "rows_accounted": run["rows_present"] + run["rows_absent"],
        "verdict": "MANIFEST_AGREES" if disagree == 0 else "MANIFEST_DISAGREES",
        "reads": {"s3_reads": reader.reads + direct_gets, "s3_writes": 0, "dynamodb_writes": 0, "vendor_calls": 0,
                  "secret_reads": 0},
        "files_in_repo_private": False,
        "served_values_changed": False,
        "pushed": False,
        "deployed": False,
        "basis_words": basis_words(days, run, parts, bronze_parts),
    }
    Path(args.record).write_bytes((json.dumps(rec, indent=2, sort_keys=True) + "\n").encode("ascii"))
    print("days: %d agree: %d disagree: %d verdict: %s" % (len(names), agree, disagree, rec["verdict"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
