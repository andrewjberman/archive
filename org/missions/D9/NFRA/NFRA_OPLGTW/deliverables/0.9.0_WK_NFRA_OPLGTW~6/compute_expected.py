"""NFRA_OPLGTW OG-v-3 -- independent instrument that computes each real-data RQ's expected
answer (WALKTHROUGH_PROTOCOL.md section 4), seals it as a salted hash, and writes the
plaintext answer OUTSIDE the repository.

INSTRUMENT: pyarrow.parquet (columnar Parquet reader, used only to decode the on-disk
Parquet byte format -- it performs no query, filter, group-by or aggregate operation) +
Python's stdlib decimal.Decimal for every summation and Python set()/Counter grouping.
No pandas float aggregation. No DuckDB. No import of, or dependency on, anything under
infra/aws/ec2/opal-gateway/app/integrations/schwab/ (the Gateway's own query engine lives
there -- C4: "Use PyArrow for Parquet projection and a local DuckDB engine for validated,
parameterized relational operations"; this script uses PyArrow for decode only and never
DuckDB, so it does not reproduce the engine's query path). TO-OG-v-3 BOUNDS: "Independence.
You never read or import app/integrations/schwab/."

SCOPE, BY THE ORDER'S OWN WORDS (TO-OG-v-3 WORKER FACE): "compute the expected answer from
the qualified silver objects OG-c-2 produced" and "The qualified object keys and VersionIds
are in OG-c-2's result file". The three VersionIds below are copied verbatim from
org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~4/producer-deploy-replay.result.md
section 1 and cross-checked against that same worker's replay/silver_versions_after.json
(both cite the identical VersionIds). This script does not query AWS for whatever the
catalog's current "latest qualified date" may be as of the day it runs -- see the result
file and surprise row NFRA_OPLGTW-W6-S5 for why a newer qualified closure (date=2026-09-16)
now exists in AWS and is deliberately NOT used here.

This script carries NO customer data. It GETs the three qualified silver Parquet objects
below by VersionId (read-only), computes the six walkthrough real-data questions
(RQ1..RQ6), and writes:
  * the actual answers, in plain text, to <SEALED_DIR>/expected/RQ<n>.txt (outside the repo);
  * a random salt to <SEALED_DIR>/expected/SALT.txt (outside the repo);
  * SEALED_EXPECTED.json beside this script (inside the repo) -- ids, kinds, masters,
    datasets, business dates, the qualified VersionIds used, the instrument name, and ONLY
    the salted sha256 hash of each answer's canonical text. No raw answer value is written
    to any file inside the repository, and none is printed to stdout by this script.

Retention: the outside-repository sealed directory (C:/tmp/nfra-oplgtw-sealed/) is kept
until OG-v-4 has graded the controlled walkthrough (A7), then removed by the COO at that
drain (stated on this cell's result file, sealed-real-expectations.result.md).
"""
from __future__ import annotations

import hashlib
import json
import os
import secrets
import subprocess
from decimal import Decimal

import pyarrow.parquet as pq

CELL_DIR = os.path.dirname(os.path.abspath(__file__))
SEALED_DIR = "C:/tmp/nfra-oplgtw-sealed"
WORK_DIR = SEALED_DIR + "/work"
EXPECTED_DIR = SEALED_DIR + "/expected"
SEALED_EXPECTED_PATH = os.path.join(CELL_DIR, "SEALED_EXPECTED.json")

REPO_ROOT = os.path.abspath(os.path.join(CELL_DIR, "..", "..", "..", "..", "..", "..", ".."))
AWS_SHIM = os.path.join(REPO_ROOT, ".tools", "aws.cmd")

INSTRUMENT = (
    "pyarrow.parquet Table read (columnar Parquet decode only, no query/filter/group-by/"
    "aggregate performed by pyarrow) + Python stdlib decimal.Decimal exact summation and "
    "Python set()/Counter-based (cusip, l_s) / (account_id, cusip, l_s) grouping; no pandas "
    "float aggregation, no DuckDB, no import from "
    "infra/aws/ec2/opal-gateway/app/integrations/schwab/."
)

MASTERS = {"08242234": "SmartX", "08335338": "BlackDiamond"}

# Verbatim from OG-c-2's result file section 1 (deliverables/0.9.0_WK_NFRA_OPLGTW~4/
# producer-deploy-replay.result.md) and its replay/silver_versions_after.json, both citing
# the same three VersionIds for the objects this cell's six questions need. D_r = 2026-09-15
# for both masters (OG-c-2's replayed business date; also each master's only qualified
# closure -- see PREVIOUS_QUALIFIED_DATE below and the result file for the AWS reads proving
# it).
QUALIFIED_OBJECTS = [
    {
        "master": "08242234",
        "table": "dim_balance",
        "date": "2026-09-15",
        "key": "schwab/08242234/silver/dim_balance/date=2026-09-15/data.parquet",
        "version_id": "rHBXO7hLBmHrcJuR3k29.7Us3gimdsE7",
    },
    {
        "master": "08335338",
        "table": "dim_balance",
        "date": "2026-09-15",
        "key": "schwab/08335338/silver/dim_balance/date=2026-09-15/data.parquet",
        "version_id": "zlXrNXfAJT96.QDWw67SNt0lyvhwdXYx",
    },
    {
        "master": "08335338",
        "table": "dim_position",
        "date": "2026-09-15",
        "key": "schwab/08335338/silver/dim_position/date=2026-09-15/data.parquet",
        "version_id": "M23kUZBy08KoL4UNiL7RE5tgoKfiGJv3",
    },
]

# PRD C3 (@f0aa50dbc0, line 159): "Legacy markers are nonqualifying until a controlled
# producer replay or metadata backfill reconciles against original inputs and exact current
# output versions." OG-c-2 is the only producer replay recorded for either master, and it
# replayed only 2026-09-15. This cell's own AWS reads (result file section "previous
# qualified date") confirm schwab/<master>/meta/complete/date=2026-09-14.json and
# date=2026-09-11.json for both masters still carry the pre-OG-c-1 legacy
# "opal.silver.complete/v1" schema (no "closure"/"status" key) -- nonqualifying. So as of
# what OG-c-2 produced, no previous qualified date exists for either master.
PREVIOUS_QUALIFIED_DATE = {"08242234": None, "08335338": None}


def _ensure_local(key: str, version_id: str, local_name: str) -> str:
    """GetObject by VersionId (read-only) into the outside-repo work cache, idempotent."""
    os.makedirs(WORK_DIR, exist_ok=True)
    local_path = os.path.join(WORK_DIR, local_name)
    cmd = [
        AWS_SHIM, "s3api", "get-object",
        "--bucket", "opal-data-assets",
        "--key", key,
        "--version-id", version_id,
        local_path,
    ]
    out = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if out.returncode != 0:
        raise RuntimeError(f"GetObject failed rc={out.returncode} key={key}: {out.stderr}")
    meta = json.loads(out.stdout)
    if meta.get("VersionId") != version_id:
        raise RuntimeError(f"VersionId mismatch on {key}: asked {version_id}, got {meta.get('VersionId')}")
    return local_path


def _load(qv_entry: dict) -> "pq.Table":
    local_name = f"{qv_entry['master']}_{qv_entry['table']}_{qv_entry['date']}.parquet"
    path = _ensure_local(qv_entry["key"], qv_entry["version_id"], local_name)
    return pq.read_table(path)


def _dec_sum(table, col: str) -> Decimal:
    total = Decimal(0)
    for v in table.column(col).to_pylist():
        if v is not None:
            total += v if isinstance(v, Decimal) else Decimal(str(v))
    return total


def _dec_str(d: Decimal) -> str:
    return format(d, "f")


def main() -> None:
    by_key = {(e["master"], e["table"]): e for e in QUALIFIED_OBJECTS}

    bal_sx = _load(by_key[("08242234", "dim_balance")])
    bal_bd = _load(by_key[("08335338", "dim_balance")])
    pos_bd = _load(by_key[("08335338", "dim_position")])

    answers: dict[str, dict] = {}

    # RQ1 -- SmartX (08242234) dim_balance, latest date: sum(net_mv_positions) across all
    # approved accounts, and count of accounts with non-null bank_cash. The proposed initial
    # profile (contract proposed_initial_profile) carries all_accounts_proposed=true and
    # approved_account_ids=[], so "approved accounts" is the full account population of the
    # snapshot.
    sx_net_mv = _dec_sum(bal_sx, "net_mv_positions")
    sx_bank_cash_nonnull = sum(1 for v in bal_sx.column("bank_cash").to_pylist() if v is not None)
    answers["RQ1"] = {
        "master": "08242234",
        "business_date": "2026-09-15",
        "sum_net_mv_positions": _dec_str(sx_net_mv),
        "accounts_total": bal_sx.num_rows,
        "accounts_with_non_null_bank_cash": sx_bank_cash_nonnull,
    }

    # RQ2 -- BlackDiamond (08335338) dim_position, latest date: count of distinct (cusip,
    # l_s) groups, and sum(market_value_settled_unsettled) over the whole snapshot (a single
    # additive field per contract additive_fields.dim_position, summed once -- not the
    # "never add different balance fields" case, which concerns adding TWO DIFFERENT
    # dim_balance fields together, C3 line 161).
    cusip_col = pos_bd.column("cusip").to_pylist()
    ls_col = pos_bd.column("l_s").to_pylist()
    groups = set(zip(cusip_col, ls_col))
    bd_mv_sum = _dec_sum(pos_bd, "market_value_settled_unsettled")
    # Row-grain check (informational only, not part of the question): (account_id, cusip,
    # l_s) is the contract's declared quantity_sum_required_groups grain at row level; this
    # real snapshot has a nonzero number of colliding (account_id, cusip, l_s) keys (the
    # exact counts are data-derived and are written only to the note text of the sealed,
    # outside-repository answer -- never hardcoded here, so this comment carries no real-data
    # count). See surprise row NFRA_OPLGTW-W6-S5-adjacent grounding in the result file. The
    # (cusip, l_s) GROUP BY the question asks for is unaffected by this row-grain collision.
    account_col = pos_bd.column("account_id").to_pylist()
    from collections import Counter
    triple_counts = Counter(zip(account_col, cusip_col, ls_col))
    colliding = {k: v for k, v in triple_counts.items() if v > 1}
    extra_rows = sum(v - 1 for v in colliding.values())
    answers["RQ2"] = {
        "master": "08335338",
        "business_date": "2026-09-15",
        "distinct_cusip_ls_groups": len(groups),
        "sum_market_value_settled_unsettled": _dec_str(bd_mv_sum),
        "note": (
            f"row-level (account_id, cusip, l_s) is NOT a unique grain in this real "
            f"snapshot ({len(colliding)} keys collide, {sum(colliding.values())} rows "
            f"across those keys, {extra_rows} rows beyond each key's first occurrence -- "
            f"see surprise row); the (cusip, l_s) GROUP BY here is the aggregate key the "
            f"question asks for, not a row-identity claim, and is unaffected by that "
            f"collision."
        ),
    }

    # RQ3 -- BlackDiamond dim_balance, latest date: three sums, reported separately, never
    # added (C3 line 161: "never construct a cash/AUA total by adding different balance
    # fields").
    bd_net_mv = _dec_sum(bal_bd, "net_mv_positions")
    bd_cash = _dec_sum(bal_bd, "cash_balance_settled_only")
    bd_net_mv_plus_cash = _dec_sum(bal_bd, "net_mv_plus_cash")
    answers["RQ3"] = {
        "master": "08335338",
        "business_date": "2026-09-15",
        "sum_net_mv_positions": _dec_str(bd_net_mv),
        "sum_cash_balance_settled_only": _dec_str(bd_cash),
        "sum_net_mv_plus_cash": _dec_str(bd_net_mv_plus_cash),
    }

    # RQ4 -- between masters: cash_balance_settled_only sum for SmartX and, separately, for
    # BlackDiamond -- two snapshot answers, never combined into one total.
    sx_cash = _dec_sum(bal_sx, "cash_balance_settled_only")
    answers["RQ4"] = {
        "smartx_08242234": {"business_date": "2026-09-15", "sum_cash_balance_settled_only": _dec_str(sx_cash)},
        "blackdiamond_08335338": {"business_date": "2026-09-15", "sum_cash_balance_settled_only": _dec_str(bd_cash)},
        "combined_total": "NEVER COMPUTED -- the two masters' snapshots are never added (PRD C3).",
    }

    # RQ5 -- SmartX between dates: sum(net_mv_plus_cash) on latest and previous qualified
    # date, and the exact difference. See PREVIOUS_QUALIFIED_DATE above: no previous
    # qualified date exists for 08242234 as of what OG-c-2 produced. The correct expected
    # answer states this; a fabricated two-date delta would be wrong.
    sx_net_mv_plus_cash = _dec_sum(bal_sx, "net_mv_plus_cash")
    answers["RQ5"] = {
        "master": "08242234",
        "latest_business_date": "2026-09-15",
        "sum_net_mv_plus_cash_latest": _dec_str(sx_net_mv_plus_cash),
        "previous_qualified_business_date": PREVIOUS_QUALIFIED_DATE["08242234"],
        "previous_qualified_business_date_status": "NONE_QUALIFIED",
        "delta": (
            "NOT COMPUTABLE -- no previous qualified date exists for 08242234 in what "
            "OG-c-2 produced (PRD C3: legacy markers are nonqualifying until a controlled "
            "producer replay or metadata backfill reconciles them; none has happened for "
            "any date before 2026-09-15). A correct answer states this; a fabricated "
            "two-date delta is wrong."
        ),
    }

    # RQ6 -- BlackDiamond between dates: position row count on each of the two dates. Same
    # measured fact as RQ5: no previous qualified date exists for 08335338 either.
    answers["RQ6"] = {
        "master": "08335338",
        "latest_business_date": "2026-09-15",
        "position_rows_latest": pos_bd.num_rows,
        "previous_qualified_business_date": PREVIOUS_QUALIFIED_DATE["08335338"],
        "previous_qualified_business_date_status": "NONE_QUALIFIED",
        "note": "NOT COMPUTABLE for a second date -- no previous qualified date exists for 08335338 in what OG-c-2 produced (same PRD C3 rule as RQ5).",
    }

    os.makedirs(EXPECTED_DIR, exist_ok=True)
    salt_path = EXPECTED_DIR + "/SALT.txt"
    salt = secrets.token_hex(32)
    with open(salt_path, "w", encoding="ascii") as fh:
        fh.write(salt)

    sealed_questions = []
    for rq_id, ans in sorted(answers.items()):
        canonical = json.dumps(ans, sort_keys=True, separators=(",", ":"))
        answer_path = EXPECTED_DIR + f"/{rq_id}.txt"
        with open(answer_path, "w", encoding="ascii") as fh:
            fh.write(canonical)
        digest = hashlib.sha256((salt + canonical).encode("ascii")).hexdigest()
        sealed_questions.append({
            "id": rq_id,
            "expected_answer_hash": f"sha256:{digest}",
            "expected_answer_file": answer_path + " (outside the repository)",
        })

    sealed = {
        "schema_version": "1.0",
        "cell": "OG-v-3",
        "instrument": INSTRUMENT,
        "hash_algorithm": "sha256(salt || canonical_json(answer)); salt at " + salt_path + " (outside the repository)",
        "qualified_objects_used": QUALIFIED_OBJECTS,
        "previous_qualified_business_date": PREVIOUS_QUALIFIED_DATE,
        "questions": sealed_questions,
    }
    with open(SEALED_EXPECTED_PATH, "w", encoding="ascii") as fh:
        json.dump(sealed, fh, indent=2, sort_keys=True)
        fh.write("\n")

    print("OK: sealed", len(sealed_questions), "of 6 questions; wrote", SEALED_EXPECTED_PATH)


if __name__ == "__main__":
    main()
