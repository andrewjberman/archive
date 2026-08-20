#!/usr/bin/env python3
"""COT_SUPERVISED G1 -- the ONE account-attributes DataMining pull (design leg a).

Andrew-sanctioned (CTO design 63310, TO COT_SUPERVISED.G1-G7): pull the current
account-attribute mapping {AccountID, Account Supervised, Account Billable,
Position Only, Portfolio Group} at Account grain from Cottonwood Black Diamond
DataMining and land it BRONZE-RAW (Rule 17a, byte-faithful) at the seam agreed
with 0.2.0_DS (their 63328 / my ACK 173411Z):

    s3://opal-data-cot/forwardfill_v2/account_attributes/ACCOUNT_ATTRIBUTES_DAILY_{asof}.xlsx

One-shot by design: the retroactive filter (DS G3) is a dimension join of this
mapping onto existing history; the FORWARD belt is G4 (holdings template). This
is not a production pipeline and arms no schedule.

Egress basis: standing cot-BD lift (Cottonwood Black Diamond ONLY).

Mechanism reuse (build ladder rung 2): the proven DataMining flow is imported
from data/cot/scripts/bronze/cot_bronze_ingest.py (DS-owned, Rule 13 -- imported,
never edited here). The template body is derived in-memory from the committed
captured qt4 (unrealized) body, which embeds the full level catalogs:
  Portfolio Group level 33: "Portfolio Group" (id 1140)
  Account level 36: "AccountID" (id 198), "Account Supervised" (id 33),
                    "Account Billable" (id 34), "Position Only" (id 5144)
Only those five are selected; every captured dim/measure selection is cleared.
If BD refuses a zero-measure run, ONE minimal measure (Market Value id 17) is
selected on retry and the extra column is disclosed loudly (bronze carries
whatever BD delivers either way).

Usage:
  python fetch_account_attributes_oneshot.py --dry-run          # build + print template, no egress
  python fetch_account_attributes_oneshot.py --asof 2026-08-19  # the real pull
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import date, timedelta
from io import BytesIO
from pathlib import Path

WS_ROOT = Path(__file__).resolve().parents[5]  # device-agnostic: derived, never baked
BRONZE_DIR = WS_ROOT / "data" / "cot" / "scripts" / "bronze"
sys.path.insert(0, str(BRONZE_DIR))

import cot_bronze_ingest as cbi  # noqa: E402  (the proven flow; DS-owned, imported not edited)

TABLE = "account_attributes"
TARGET_DIMS = {
    33: ["Portfolio Group"],
    36: ["AccountID", "Account Supervised", "Account Billable", "Position Only"],
}
FALLBACK_MEASURE = "Market Value"  # id 17 -- selected only if the zero-measure run fails
TEMPLATE_EVIDENCE = Path(__file__).with_name("account_attributes_template_asrun.json")


def build_template(asof: str, with_measure: bool) -> dict:
    src = json.loads((BRONZE_DIR / "templates" / "unrealized.json").read_text())
    tpl = json.loads(json.dumps(src))  # deep copy; qt4 snapshot family
    tpl["templateId"] = False  # create-then-run (one-shot); id recorded from the response
    tpl["name"] = "opal_cot_account_attributes_oneshot"
    tpl["comment"] = ("COT_SUPERVISED G1 one-shot: account-attribute mapping at Account "
                      "grain. Derived from the captured qt4 body; 0.6.2_AE_PartnerETL.")
    found: list[str] = []
    for lvl in tpl["levels"]:
        want = TARGET_DIMS.get(lvl["queryLevelId"], [])
        for dm in lvl["dimensions"]:
            dm["isSelected"] = dm["name"] in want
            if dm["isSelected"]:
                found.append(dm["name"])
    for fact in tpl["facts"]:
        for m in fact.get("measures", []):
            m["isSelected"] = bool(with_measure) and m["name"] == FALLBACK_MEASURE
    expect = [n for names in TARGET_DIMS.values() for n in names]
    missing = sorted(set(expect) - set(found))
    if missing:
        raise SystemExit("ABORT: target dims not found in the captured catalog: %s" % missing)
    start = (date.fromisoformat(asof) - timedelta(days=14)).isoformat()
    tpl["dateRangeType"] = "Custom"
    tpl["startDate"] = cbi._mmddyyyy(start)
    tpl["endDate"] = cbi._mmddyyyy(asof)
    return tpl


def pull(asof: str) -> bytes:
    cookie = cbi.load_bd_session()
    token = cbi.get_datamining_token(cookie)
    print("auth OK (firm=%s, bucket=%s)" % (cbi.BD_FIRM_ID, cbi.BD_S3_BUCKET), flush=True)
    for with_measure in (False, True):
        tpl = build_template(asof, with_measure)
        TEMPLATE_EVIDENCE.write_text(json.dumps(tpl, indent=1))
        mode = "zero-measure" if not with_measure else "FALLBACK +%s (extra column, disclosed)" % FALLBACK_MEASURE
        print("attempt: %s" % mode, flush=True)
        try:
            run_id, guid = cbi.run_query(token, tpl)
            print("  run=%s guid=%s templateId recorded in %s -- polling"
                  % (run_id, guid, TEMPLATE_EVIDENCE.name), flush=True)
            cbi.poll_status(token, run_id)
            xlsx = cbi.download_export(cookie, guid)
        except (RuntimeError, TimeoutError) as exc:
            print("  %s attempt failed: %s" % (mode, exc), flush=True)
            if with_measure:
                raise
            continue
        has_data = cbi._export_has_data_rows(xlsx)
        if has_data == 0:
            raise SystemExit("ABORT: export is header-only (%d bytes) -- attribute snapshot "
                             "absent for as-of %s; NOT landing a stub." % (len(xlsx), asof))
        return xlsx
    raise SystemExit("ABORT: both attempts failed")


def land_and_verify(asof: str, xlsx: bytes) -> None:
    path = cbi.land_to_s3(TABLE, xlsx, asof)
    print("OK: landed %s (%d bytes)" % (path, len(xlsx)), flush=True)
    cbi._write_completeness_sidecar(TABLE, asof, cbi._export_has_data_rows(xlsx), len(xlsx))

    # Verify + measure on the SERVED bytes (never the in-memory buffer).
    key = cbi._bronze_object_key(TABLE, asof)
    served = cbi.s3.get_object(Bucket=cbi.BD_S3_BUCKET, Key=key)["Body"].read()
    print("served sha256=%s bytes=%d (buffer match: %s)"
          % (hashlib.sha256(served).hexdigest(), len(served), served == xlsx), flush=True)

    import openpyxl
    wb = openpyxl.load_workbook(BytesIO(served), read_only=True, data_only=True)
    ws = wb.active
    rows = list(ws.iter_rows(values_only=True))
    wb.close()
    header = [str(c) if c is not None else "" for c in rows[0]]
    data = rows[1:]
    print("HEADER ROW (exact, for DS): %s" % json.dumps(header), flush=True)
    print("data rows: %d" % len(data), flush=True)
    ai = header.index("AccountID") if "AccountID" in header else None
    if ai is None:
        print("WARN: no AccountID column in header -- uniqueness not measurable", flush=True)
        return
    ids = [r[ai] for r in data if ai < len(r)]
    print("AccountID: %d values, %d distinct, duplicates: %d"
          % (len(ids), len(set(ids)), len(ids) - len(set(ids))), flush=True)
    for col in ("Account Supervised", "Account Billable", "Position Only", "Portfolio Group"):
        if col in header:
            ci = header.index(col)
            counts: dict = {}
            for r in data:
                v = r[ci] if ci < len(r) else None
                counts[str(v)] = counts.get(str(v), 0) + 1
            top = sorted(counts.items(), key=lambda kv: -kv[1])[:8]
            print("%s value counts (top): %s" % (col, top), flush=True)
        else:
            print("WARN: expected column ABSENT from export: %s" % col, flush=True)


def main() -> int:
    ap = argparse.ArgumentParser(description="COT_SUPERVISED G1 one-shot account-attributes pull")
    ap.add_argument("--asof", default="2026-08-19",
                    help="as-of date (YYYY-MM-DD); default 2026-08-19 = the HAR oracle date")
    ap.add_argument("--dry-run", action="store_true", help="build + print the template; no egress")
    args = ap.parse_args()
    if args.dry_run:
        tpl = build_template(args.asof, with_measure=False)
        sel = [(lv["queryLevelId"], d["name"]) for lv in tpl["levels"]
               for d in lv["dimensions"] if d["isSelected"]]
        meas = [m["name"] for f in tpl["facts"] for m in f.get("measures", []) if m.get("isSelected")]
        print("DRY-RUN template: qt=%s window=%s..%s" % (tpl["queryTypeId"], tpl["startDate"], tpl["endDate"]))
        print("selected dims: %s" % sel)
        print("selected measures: %s" % (meas or "NONE (zero-measure attempt)"))
        return 0
    xlsx = pull(args.asof)
    land_and_verify(args.asof, xlsx)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
