"""IRPT_DASHBD round 126, cell DB-i-13 (TO IRPT_DASHBD.TO-DB-i-13, worker 0.9.0_WK_IRPT_DASHBD~313).

The series-ended cause read. Each Orion Scope Account series in the two saved round-122 response bodies has a last end
date. An account whose last end date is strictly before the window end (2026-10-13) is early-ending. For each one, the
partitions of Opal's own fact_positions silver strictly after that last end date and not after the window end are read
through the GET-only reader, and the account is classified:
  STALE_AT_SOURCE        Opal still holds the account on the newest partition after the series ended
  CLOSED_OR_TRANSFERRED  the account is not held on the newest partition after the series ended
  NOT_DETERMINED         no partition after the series ended
No vendor call, no write, no secret read. The saved bodies and the extract are private; the repo record carries counts,
verdict words and digests only.

Usage: python -I <this file>            reads the silver partitions, writes the private extract and the repo record
       python -I <this file> --plan     parses the saved bodies only (no S3 call) and prints counts
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import sys
from pathlib import Path

PRIV_IN = Path("C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~309")
PRIV_OUT = Path("C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~313")
BODY_FILES = ("hist_A.json", "hist_B.json")
EXTRACT_NAME = "positions_extract.json"
END = "2026-10-13"
READ_CAP = 200
SELF_REL = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~313/series_ended_cause.py"
REC_REL = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~313/SERIES_ENDED_CAUSE_R126.json"
VERDICTS = ("STALE_AT_SOURCE", "CLOSED_OR_TRANSFERRED", "NOT_DETERMINED")


def _find_root() -> Path:
    here = Path(__file__).resolve()
    for anc in here.parents:
        if (anc / "lib" / "trading_calendar.py").is_file() and (anc / "data").is_dir():
            return anc
    raise SystemExit("repo root not found above this file")


ROOT = _find_root()
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "data" / "assets" / "scripts" / "gold" / "irpt_reporting" / "adapters"))
import inflection_account_dim as iad  # noqa: E402
import inflection_account_return_daily as iar  # noqa: E402


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha_str(s) -> str:
    return sha(str(s).encode("utf-8"))


def walk(node):
    if isinstance(node, dict):
        yield node
        for v in node.values():
            yield from walk(v)
    elif isinstance(node, list):
        for v in node:
            yield from walk(v)


def day_of(s) -> dt.date:
    s = str(s)
    if "/" in s:
        return dt.datetime.strptime(s[:10], "%m/%d/%Y").date()
    return dt.date.fromisoformat(s[:10])


def key_of(raw):
    """An account key as the dimension carries it: a string, no '.0'."""
    try:
        return str(int(float(raw)))
    except (TypeError, ValueError):
        return None


def last_ends(body) -> dict:
    """{account key: last end date} for the Account groups of one body that carry a series."""
    out = {}
    for g in walk(body):
        if g.get("$type") != "calculated-group" or g.get("grouping") != "Account":
            continue
        ends = [n.get("endDate") for n in walk(g) if n is not g and n.get("factor") is not None and n.get("endDate")]
        if ends:
            out[key_of(g.get("groupEntityId"))] = max(day_of(e) for e in ends)
    return out


def verdict_of(n_after: int, held_on_newest: bool) -> str:
    if n_after == 0:
        return "NOT_DETERMINED"
    return "STALE_AT_SOURCE" if held_on_newest else "CLOSED_OR_TRANSFERRED"


def measure(last_end: dt.date, extract_values: dict, partitions: list):
    """(partitions after, held days, held on newest) of one account: partitions strictly after its last series day and
    not after the window end; held means a positive total value."""
    end = dt.date.fromisoformat(END)
    after = sorted(p for p in partitions if last_end < dt.date.fromisoformat(p[len("date="):]) <= end)
    vals = [extract_values.get(p) for p in after]
    held = [isinstance(v, (int, float)) and v > 0 for v in vals]
    return len(after), sum(held), bool(held and held[-1])


def build_accounts(ends: dict, values: dict, partitions: list):
    end = dt.date.fromisoformat(END)
    rows = []
    for key, last in ends.items():
        if last >= end:
            continue
        n_after, held_days, on_newest = measure(last, values.get(key, {}), partitions)
        rows.append({"account_sha256": sha_str(key), "series_ended_days_before_window_end": (end - last).days,
                     "partitions_after": n_after, "held_days_after": held_days, "held_on_newest": on_newest,
                     "verdict": verdict_of(n_after, on_newest)})
    rows.sort(key=lambda a: a["account_sha256"])
    return rows


def basis_words(n_series: int, rows: list, n_parts_read: int) -> str:
    counts = {v: sum(1 for a in rows if a["verdict"] == v) for v in VERDICTS}
    lines = [
        "Round 126 DB-i-13 series-ended cause read. Saved round-122 Orion bodies (two) carry %d Account series in total; "
        "%d of them are early-ending, their last series end date strictly before the window end. Opal positions silver was read "
        "through the GET-only reader over %d daily partitions (the ones after the earliest early-ending series end, up to the "
        "window end); no vendor call and no write was made." % (n_series, len(rows), n_parts_read),
    ]
    for i, a in enumerate(rows, 1):
        lines.append("Early-ending account %d: last series end %d days before the window end; %d partitions after it, %d of them "
                     "hold a positive total, the newest %s; verdict %s." % (
                         i, a["series_ended_days_before_window_end"], a["partitions_after"], a["held_days_after"],
                         "holds" if a["held_on_newest"] else "does not hold", a["verdict"]))
    lines.append("Verdict counts: STALE_AT_SOURCE %d, CLOSED_OR_TRANSFERRED %d, NOT_DETERMINED %d." % (
        counts["STALE_AT_SOURCE"], counts["CLOSED_OR_TRANSFERRED"], counts["NOT_DETERMINED"]))
    lines.append("For the feed: a STALE_AT_SOURCE account means the feed's SERIES_ENDED_AT_SOURCE rows hide an account Opal still "
                 "holds after Orion's series ended, so the feed would serve a hole for a live account. A CLOSED_OR_TRANSFERRED "
                 "account is not held on the newest partition, so the series end is consistent with a close or transfer. "
                 "NOT_DETERMINED means no partition exists after the series end to test.")
    lines.append("What this does not establish: a held position after a series end is not proof of a vendor fault, and an "
                 "absent position is not proof that the account closed.")
    return " ".join(lines)


def plan(ends: dict) -> int:
    end = dt.date.fromisoformat(END)
    early = {k: v for k, v in ends.items() if v < end}
    print("PLAN series_total=%d early_end_count=%d" % (len(ends), len(early)))
    print("PLAN no S3 call made")
    return 0


def main(argv) -> int:
    bodies_raw = [(PRIV_IN / name).read_bytes() for name in BODY_FILES]
    body_shas = [sha(b) for b in bodies_raw]
    ends = {}
    for raw in bodies_raw:
        ends.update(last_ends(json.loads(raw.decode("utf-8"))))
    if "--plan" in argv:
        return plan(ends)

    end = dt.date.fromisoformat(END)
    early = {k: v for k, v in ends.items() if v < end}
    earliest = min(early.values())
    reader = iad.InflectionSilverReader()
    table = iar.ORION_SILVER + "fact_positions"
    all_parts = reader.list_partitions(table)
    to_read = [p for p in all_parts if earliest < dt.date.fromisoformat(p[len("date="):]) <= end]
    if reader.reads + len(to_read) > READ_CAP:
        print("STOP read cap: %d reads so far + %d GETs would exceed %d; nothing read further" % (
            reader.reads, len(to_read), READ_CAP))
        return 3
    values = {k: {} for k in early}
    accounts_set = set(early)
    for p in to_read:
        frame = reader.read_parquet(table.rstrip("/") + "/" + p + "/data.parquet")
        tot = iar.account_values(frame, accounts_set)
        for k in early:
            values[k][p] = tot.get(k)
        del frame

    PRIV_OUT.mkdir(parents=True, exist_ok=True)
    ext_path = PRIV_OUT / EXTRACT_NAME
    ext_bytes = (json.dumps({"partitions": to_read, "values": values}, sort_keys=True) + "\n").encode("ascii")
    ext_path.write_bytes(ext_bytes)

    rows = build_accounts(ends, values, to_read)
    counts = {v: sum(1 for a in rows if a["verdict"] == v) for v in VERDICTS}
    rec = {
        "script": {"file": SELF_REL, "sha256": sha(Path(__file__).read_bytes())},
        "bodies_sha256": body_shas,
        "extract": {"path": ext_path.as_posix(), "sha256": sha(ext_bytes)},
        "series_total": len(ends),
        "early_end_count": len(rows),
        "accounts": rows,
        "verdict_counts": counts,
        "basis_words": basis_words(len(ends), rows, len(to_read)),
        "reads": {"s3_reads": reader.reads, "s3_writes": 0, "dynamodb_writes": 0, "vendor_calls": 0, "secret_reads": 0},
        "files_in_repo_private": False,
        "served_values_changed": False,
        "pushed": False,
        "deployed": False,
    }
    rec_path = ROOT / REC_REL
    rec_path.write_bytes((json.dumps(rec, indent=2, sort_keys=True) + "\n").encode("ascii"))
    print("OK series_total=%d early_end_count=%d partitions_read=%d s3_reads=%d" % (
        len(ends), len(rows), len(to_read), reader.reads))
    print("OK verdict_counts STALE_AT_SOURCE=%d CLOSED_OR_TRANSFERRED=%d NOT_DETERMINED=%d" % (
        counts["STALE_AT_SOURCE"], counts["CLOSED_OR_TRANSFERRED"], counts["NOT_DETERMINED"]))
    for i, a in enumerate(rows, 1):
        print("OK account %d days_before=%d partitions_after=%d held_days_after=%d verdict=%s" % (
            i, a["series_ended_days_before_window_end"], a["partitions_after"], a["held_days_after"], a["verdict"]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
