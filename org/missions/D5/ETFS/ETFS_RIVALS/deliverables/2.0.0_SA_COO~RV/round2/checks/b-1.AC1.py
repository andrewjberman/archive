"""RIV-b-1 AC1 -- two real IDVZ-group Excel BQL captures import into Bloomberg bronze in a local sink: one raw object
(<batch>-<requested_date>-<ts>-<sha12>.json) + its <stem>.sidecar.json per capture at the builder address, the key carrying the requested date, the sidecar's per-fund row counts equal
to the capture's, provenance capture_origin census:*, the fetch-bloomberg marker written; a rerun lands nothing new. The
issuer collector's key carries the requested date too (row W1-S2)."""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402


def run(v):
    c.setup_path()
    files = c.idvz_captures(2)
    sink = c.tmpdir("rv_b1a_")
    r1 = c.import_bloomberg(sink, files)
    print("r1:", str(r1)[:300])
    v.check(r1.get("status") == "OK", f"import status {r1.get('status')}")
    bronze = c.local_path(sink, c.address("bloomberg", "etfs", "bronze", "holdings", "date=")).parent
    raws = sorted(p for p in bronze.rglob("*") if p.is_file() and not p.name.endswith(".sidecar.json"))
    sides = sorted(p for p in bronze.rglob("*") if p.is_file() and p.name.endswith(".sidecar.json"))
    v.check(len(raws) == 2 and len(sides) == 2, f"2 raw + 2 sidecars under {bronze} (got {len(raws)} + {len(sides)})")
    for f in files:
        req = c.capture(f)["requested_date"]
        hit = [p for p in raws if req in p.name]
        v.check(len(hit) == 1, f"one raw key carries requested date {req} ({[p.name for p in hit]})")
        sc = [p for p in sides if req in p.name]
        if not sc:
            continue
        s = json.loads(sc[0].read_text(encoding="utf-8"))
        v.check(s.get("row_count") == c.capture_rows_by_fund(f), f"{req} sidecar row_count per fund == capture's")
        v.check(str(s.get("capture_origin", "")).startswith("census:"), f"{req} capture_origin {s.get('capture_origin')}")
        v.check(s.get("requested_date") == req and s.get("sha256"), f"{req} sidecar carries requested_date and sha256")
    from rivalfunds import markers
    v.check(markers.has_marker("fetch-bloomberg", c.capture(files[-1])["requested_date"], f"local:{sink}"),
            "fetch-bloomberg marker written")
    c.import_bloomberg(sink, files, batch_id="chk-import-rerun")
    raws2 = [p for p in bronze.rglob("*") if p.is_file() and not p.name.endswith(".sidecar.json")]
    v.check(len(raws2) == len(raws), f"rerun lands nothing new ({len(raws)} -> {len(raws2)})")

    isink = c.tmpdir("rv_b1i_")
    out = c.land(isink, c.archive_files(1))
    req = c.archive_meta(c.archive_files(1)[0])["requested_date"]
    v.check(req in out[0].get("bronze_uri", ""), f"issuer bronze key carries requested date {req}: {out[0].get('bronze_uri')}")


failures = c.guarded("AC1", run)
if failures == 0:
    print("AC1 RESULT: PASS 0 failures")
else:
    print(f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
