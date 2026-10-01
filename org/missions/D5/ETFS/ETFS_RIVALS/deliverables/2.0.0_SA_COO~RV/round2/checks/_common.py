"""Shared helpers for the ETFS_RIVALS round-2 checks (issuer-written, 2.0.0_SA_COO~RV).

Every check runs from the root of the worktree it grades (the worker's), imports the package from THAT tree, and reads the
device-local Bloomberg census captures from the MAIN worktree's .runtime/ (gitignored). Each check prints exactly one verdict
line of its own: '<ID> RESULT: PASS 0 failures' or '<ID> RESULT: FAIL <n> failures'.

The round-1 helpers (Verdict, guarded, setup_path, local_path, address, read_parquets, tmpdir, main_root, archive_files,
archive_meta, land) are re-exported from ../../round1/checks/_common.py.
"""
from __future__ import annotations

import importlib.util
import json
import pathlib
import sys

_R1 = pathlib.Path(__file__).resolve().parents[2] / "round1" / "checks" / "_common.py"
_spec = importlib.util.spec_from_file_location("_rivals_r1_common", _R1)
_r1 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_r1)

Verdict, guarded, setup_path, local_path, address = _r1.Verdict, _r1.guarded, _r1.setup_path, _r1.local_path, _r1.address
read_parquets, tmpdir, main_root, archive_files, archive_meta, land = (
    _r1.read_parquets, _r1.tmpdir, _r1.main_root, _r1.archive_files, _r1.archive_meta, _r1.land)

IDVZ_CAPTURES_REL = ".runtime/etfs-rivals-idvz-20260930/daily"
PFOE_CAPTURES_REL = ".runtime/amgt-reconn-daily-census-20260929"
DIVIDENDS_REL = ".runtime/etfs-rivals-idvz-20260930/dividends.json"

IDVZ_GROUP = ["IDVZ", "TXUE", "BIDD", "CGIC", "INEQ", "SCHY"]
PFOE_GROUP = ["PFOE", "WCMG", "GQGU", "TSEL", "BASG", "ETFT", "PCLG"]


def idvz_captures(n: int) -> list[pathlib.Path]:
    """The LAST n IDVZ-group Excel BQL census captures (requested-date order): real Bloomberg responses."""
    d = main_root() / IDVZ_CAPTURES_REL
    files = sorted(d.glob("20*.json"))
    if not files:
        raise SystemExit(f"IDVZ captures empty or absent: {d}")
    return files[-n:]


def capture(p: pathlib.Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))


def capture_rows_by_fund(p: pathlib.Path) -> dict:
    """{fund ticker: row count} from a capture's rows (first row is the header; ORIG_IDS names the fund, e.g.
    'IDVZ US Equity'; SOURCE reads 'ETF' and is NOT the fund)."""
    d = capture(p)
    rows = d["rows"]
    hdr = rows[0]
    si = hdr.index("ORIG_IDS")
    out: dict = {}
    for r in rows[1:]:
        f = str(r[si]).split()[0] if r[si] is not None else None
        out[f] = out.get(f, 0) + 1
    return out


def dividends_path() -> pathlib.Path:
    p = main_root() / DIVIDENDS_REL
    if not p.is_file():
        raise SystemExit(f"dividends.json absent: {p}")
    return p


def import_bloomberg(sink_dir: str, files: list[pathlib.Path], batch_id: str = "chk-import") -> dict:
    """RIV-b-1's import mode over real captures into a local sink."""
    from rivalfunds import collector_bloomberg

    return collector_bloomberg.handler_entry({"mode": "import", "captures": [str(f) for f in files],
                                              "batch_id": batch_id, "sink": f"local:{sink_dir}",
                                              "date": capture(files[-1])["requested_date"]})


def replay(module: str, sink_dir: str, date: str, batch_id: str = "chk") -> dict:
    mod = __import__(f"rivalfunds.{module}", fromlist=["handler_entry"])
    return mod.handler_entry({"mode": "replay", "batch_id": batch_id, "sink": f"local:{sink_dir}", "date": date})


def gold_dir(sink_dir: str, table: str) -> pathlib.Path:
    return local_path(sink_dir, address("rivalfunds", "etfs", "gold", table, "date=")).parent


def verdict_line(cid: str, failures: int) -> None:
    print(f"{cid} RESULT: PASS 0 failures" if failures == 0 else f"{cid} RESULT: FAIL {failures} failures")
    sys.exit(0 if failures == 0 else 1)


def run_idvz_chain(sink_dir: str, files: list[pathlib.Path], through: str) -> dict:
    """Real IDVZ-group captures -> Bloomberg bronze (import) -> Bloomberg silver -> canonical_shape [-> coverage]
    [-> corporate_actions (import) -> trade_schedule], local sink only. `through` in {silver, canonical, coverage, trades}."""
    import_bloomberg(sink_dir, files)
    date = capture(files[-1])["requested_date"]
    res = {"silver": replay("silver_bloomberg", sink_dir, date)}
    if through == "silver":
        return res
    res["canonical"] = replay("gold_canonical_shape", sink_dir, date)
    if through == "canonical":
        return res
    if through == "coverage":
        res["coverage"] = replay("gold_holdings_coverage", sink_dir, date)
        return res
    from rivalfunds import enrichment_bloomberg

    res["corporate_actions"] = enrichment_bloomberg.handler_entry(
        {"mode": "import", "dividends_json": str(dividends_path()), "batch_id": "chk-e1", "sink": f"local:{sink_dir}",
         "date": date})
    res["trades"] = replay("gold_trade_schedule", sink_dir, date)
    return res
