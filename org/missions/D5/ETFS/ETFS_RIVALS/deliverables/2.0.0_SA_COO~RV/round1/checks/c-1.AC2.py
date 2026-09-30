"""RIV-c-1 AC2 -- a file that is not the requested day, or carries no BASG rows, lands with a status and NO report date.

Fed with real archived issuer bytes through land_bronze (no network).
"""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402


def run(v):
    c.setup_path()
    from rivalfunds.collector_issuer import land_bronze

    f = c.archive_files(1)[0]
    meta = c.archive_meta(f)
    raw = f.read_bytes()
    sink = c.tmpdir("rv_c1b_")

    ok = land_bronze(raw=raw, requested_date=meta["requested_date"], source_url=meta["url"], sink=f"local:{sink}", captured_at=meta["at"])
    v.check(ok.get("status") == "OK" and ok.get("claimed_report_date") == meta["requested_date"],
            f"control arm: the real file for its own day -> OK, report date {meta['requested_date']} (got {ok.get('status')}, {ok.get('claimed_report_date')})")

    mism = land_bronze(raw=raw, requested_date="2099-01-02", source_url=meta["url"], sink=f"local:{sink}", captured_at=meta["at"])
    v.check(mism.get("status") == "DATE-MISMATCH", f"requested another day -> DATE-MISMATCH (got {mism.get('status')})")
    v.check(not mism.get("report_date"), "DATE-MISMATCH carries no report_date")

    lines = raw.decode("utf-8-sig").splitlines()
    i = lines[0].split("|").index("fund_ticker")
    no_basg = "\n".join([lines[0]] + [ln for ln in lines[1:] if ln.strip() and ln.split("|")[i].strip() != "BASG"]).encode()
    nf = land_bronze(raw=no_basg, requested_date=meta["requested_date"], source_url=meta["url"], sink=f"local:{sink}", captured_at=meta["at"])
    v.check(nf.get("status") == "NO-FUND-ROWS", f"no BASG rows -> NO-FUND-ROWS (got {nf.get('status')})")
    v.check(not nf.get("report_date"), "NO-FUND-ROWS carries no report_date")
    print(json.dumps({"ok": ok, "mismatch": mism, "no_fund": nf}, default=str)[:900])


failures = c.guarded("AC2", run)
if failures == 0:
    print("AC2 RESULT: PASS 0 failures")
else:
    print(f"AC2 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
