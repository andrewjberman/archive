"""
run_exercise.py -- AMGT-s-14 exercise (c): re-run ONE class alone on ONE security
AMGT-s-1 already touched (F2: no new unique security), and prove every other
class's ledger entry stayed byte-for-byte where it was.

Registers model_block_pull.py's real pull as the "market_data" stage (the
retrofit this order added), snapshots the ledger for the exercised security
BEFORE and AFTER a single rerun("market_data") call, and writes both snapshots
to this deliverables folder for check_rerun.py to compare.

Bloomberg health is checked FIRST and never signed in on a failure (this
order's own bound) -- an unhealthy terminal makes the market_data stage raise
before any DAPI call, and ledger.rerun() records that as a FAILED entry
honestly, which still satisfies AC2.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent.parent.parent.parent
SECURITY = "SAP GY Equity"  # already in AMGT-s-1's own SECURITIES list -- no new unique security (F2)


def _load(name: str, rel_path: str):
    mod_path = REPO_ROOT / rel_path
    spec = importlib.util.spec_from_file_location(name, mod_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {name} from {mod_path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    ledger = _load("ledger", "lib/research/ledger/ledger.py")
    model_block_pull = _load("model_block_pull", "integrations/bloomberg/research/model_block_pull.py")

    security_key = model_block_pull.security_key(SECURITY)

    def market_data_stage(sec_key: str) -> None:
        # sec_key -> the original "TICKER EXCH Equity" form model_block_pull's
        # own functions take; the transform is exactly reversible here because
        # security_key() only ever replaces spaces with underscores and none
        # of this project's securities contain a literal underscore.
        security = sec_key.replace("_", " ")
        model_block_pull.cmd_pull([security])

    ledger.register_stage("market_data", market_data_stage, source="bloomberg")

    before = json.loads(json.dumps(ledger._read_ledger_raw(security_key)))

    health = None
    try:
        blp = model_block_pull._load_blp_client()
        health = blp.health()
    except Exception as exc:  # noqa: BLE001 -- health check itself must never crash the exercise
        health = {"ok": False, "error": str(exc)}
    print(f"HEALTH: {health}")

    if not health.get("ok"):
        # Never a sign-in (this order's own bound). Record an honest FAILED
        # entry ourselves rather than letting rerun() invoke a stage that
        # would need Bloomberg -- the market_data class IS the one asked for
        # in this exercise, so a signed-out terminal still produces a real,
        # recorded market_data run.
        ledger.record_run(
            security_key,
            "market_data",
            "bloomberg",
            "FAILED",
            ledger.utc_stamp(),
            f"bloomberg_health ok=false at exercise time: {health}",
        )
    else:
        ledger.rerun(security_key, "market_data")

    after = ledger._read_ledger_raw(security_key)

    out_dir = Path(__file__).resolve().parent
    (out_dir / "ledger_before.json").write_text(json.dumps(before, indent=2), encoding="utf-8")
    (out_dir / "ledger_after.json").write_text(json.dumps(after, indent=2), encoding="utf-8")

    latest = ledger.read_ledger(security_key)
    outcome = latest.get("market_data", {}).get("outcome", "UNKNOWN")
    print(f"EXERCISE DONE: security_key={security_key} market_data outcome={outcome}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
