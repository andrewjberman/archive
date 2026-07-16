"""WP5 TRUE-VINTAGE PARTIAL BACKFILL -- derive 07-14 + 07-15 feeder partitions
from LANDED monolith bronze (CTO ruling 051145Z option (b); riders honored).

DERIVATION, NOT FABRICATION: the C5 pulls landed the SAME API responses this
feeder consumes (enterprises/allocations per model -> model_allocations/
allocations.json; reportedmodels/{rmid}/holdings -> holdings/holdings.json)
as monolith bronze at GENUINE vintages 20260714 + 20260715. This script
replays the feeder's EXACT transform (wsb_49f_smartx_model_aua.py logic,
lifted verbatim where possible) over those landed bytes. ZERO VENDOR CALLS.

RIDERS (CTO 051145Z):
  R1 every input cited by bucket/key/ETag in the derivation manifest;
  R2 manifest names the derivation (derived-from-landed-bronze, zero vendor
     calls) + the transform's reviewed commit;
  R3 drift tie-check derived-07-15 vs fresh-07-16 (per-model sums, tolerance
     2%) runs BEFORE any partition publishes -- a miss aborts the publish;
  R4 (process) CTO diff review before this runs.

Also emits the HOLE MANIFEST for 07-09/10/13 (ruling: documented holes --
vendor-unrecoverable at feeder grain; the API is snapshot-only and C5 bronze
begins 20260714).

rmid pairing: read from LANDED fact_model_allocation_roster (date=2026-07-15)
-- landed data, not a live resolve (the feeder's live models/{id} fallback is
exactly the vendor call this derivation must not make).

Usage: python wp5_true_vintage_transform.py            # tie-check + publish
       python wp5_true_vintage_transform.py --dry-run  # everything except publish
"""
from __future__ import annotations

import argparse
import datetime as dt
import io
import json
import sys

import boto3
import pandas as pd

MONO = "opal-data-assets"
FEEDER_BUCKET = "opal-data-mdpf"
FEEDER_PREFIX = "mdpf/feeds"
REGISTRY_PATH = "data/mdpf/scripts/gold/mdpf_model_registry.json"
ROSTER_KEY = "smartx/platform/silver/fact_model_allocation_roster/date=2026-07-15/data.parquet"

# constants lifted from wsb_49f_smartx_model_aua.py (the reviewed feeder)
PARTNER_FIRM_ID = "49financial"
PARTNER_NAME = "49 Financial"
SOURCE_PIPELINE = "smartx"
OPEN_STATUS = "open"
OPAL_ETF_TICKERS = {"DIVZ", "IDVZ", "PFDE", "PFOE"}
CASH_TICKER = "CUSTODIAL_CASH"
POSITIONS_COLUMNS = [
    "firm_id", "partner_name", "model_key", "model_key_unmapped", "cohort_class",
    "account_id", "household_id", "as_of_date", "model_value", "custodian",
    "source_pipeline", "_ingested_at",
]
COMPOSITION_COLUMNS = [
    "firm_id", "model_key", "as_of_date", "ticker", "security_name",
    "product_class", "target_weight", "actual_weight", "is_opal_etf",
    "source_pipeline", "_ingested_at",
]

DATES = [("2026-07-14", "20260714"), ("2026-07-15", "20260715")]
HOLES = ["2026-07-09", "2026-07-10", "2026-07-13"]
TIE_TOLERANCE = 0.02   # R3: derived-07-15 vs fresh-07-16 per-model, 2%

s3 = boto3.client("s3", region_name="us-east-1")


def log(msg: str) -> None:
    ts = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    print(f"[{ts}] {msg}", flush=True)


def get_cited(key: str, inputs: list) -> bytes:
    """GET a landed object AND record its citation (R1: bucket/key/ETag)."""
    o = s3.get_object(Bucket=MONO, Key=key)
    body = o["Body"].read()
    inputs.append({"bucket": MONO, "key": key,
                   "etag": o["ETag"].strip('"'), "bytes": len(body)})
    return body


def load_models() -> tuple[list[dict], list[dict]]:
    """Registry smartx models + rmid pairing from LANDED roster silver.

    R1 FIX (CTO 051908Z): the roster and registry are INPUTS too -- both are
    cited (roster by bucket/key/ETag via get_cited; registry by version + file
    sha256) and returned for the manifest's shared_inputs."""
    import hashlib
    shared: list[dict] = []
    reg_bytes = open(REGISTRY_PATH, "rb").read()
    reg = json.loads(reg_bytes.decode("utf-8"))
    shared.append({"kind": "registry", "path": REGISTRY_PATH,
                   "version": reg.get("_version"),
                   "sha256": hashlib.sha256(reg_bytes).hexdigest()})
    models = [m for m in reg["models"] if m.get("smartx_model_id")]
    roster_citations: list = []
    roster = pd.read_parquet(io.BytesIO(get_cited(ROSTER_KEY, roster_citations)))
    shared.append(dict(roster_citations[0], kind="roster"))
    pairing = (roster.groupby("model_id")["rmid"].first()).to_dict()
    for m in models:
        rmid = m.get("smartx_reported_model_id") or pairing.get(m["smartx_model_id"])
        if not rmid:
            raise RuntimeError(f"NO rmid for {m['model_key']} in registry OR "
                               "landed roster -- refusing (a live resolve would "
                               "be the vendor call this derivation must not make)")
        m["_rmid"] = rmid
    log(f"OK: registry v{reg.get('_version')} -- {len(models)} models; rmid "
        f"pairing from landed roster ({ROSTER_KEY.split('/date=')[1][:10]})")
    return models, shared


def transform_date(models: list[dict], as_of: str, d8: str,
                   inputs: list) -> tuple[pd.DataFrame, pd.DataFrame]:
    """The feeder's pull_model logic, replayed over landed bronze bytes."""
    ingested = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    all_pos, all_comp = [], []
    for m in models:
        model_key, rmid = m["model_key"], m["_rmid"]
        cohort_class = m.get("model_type")

        alloc = json.loads(get_cited(
            f"smartx/model/{rmid}/bronze/model_allocations/{d8}/allocations.json",
            inputs))
        rows = alloc.get("data", []) or []
        positions = []
        for r in rows:
            if r.get("status") != OPEN_STATUS:
                continue
            value = r.get("value")
            if not isinstance(value, (int, float)):
                continue
            positions.append({
                "firm_id": PARTNER_FIRM_ID, "partner_name": PARTNER_NAME,
                "model_key": model_key, "model_key_unmapped": None,
                "cohort_class": cohort_class,
                "account_id": r.get("allocationId"), "household_id": None,
                "as_of_date": as_of, "model_value": float(value),
                "custodian": None,
                "source_pipeline": SOURCE_PIPELINE, "_ingested_at": ingested,
            })
        log(f"  [{as_of}] {model_key}: {len(positions)} open allocations, "
            f"sum {sum(p['model_value'] for p in positions):,.2f}")
        all_pos.extend(positions)

        holdings = json.loads(get_cited(
            f"smartx/model/{rmid}/bronze/holdings/{d8}/holdings.json", inputs))
        hrows = holdings.get("data", []) or []
        weight_sum = 0.0
        for h in hrows:
            sym = h.get("symbol", {}) or {}
            ticker = sym.get("ticker")
            weight = h.get("percentOfPortfolio")
            weight = float(weight) if isinstance(weight, (int, float)) else 0.0
            weight_sum += weight
            all_comp.append({
                "firm_id": PARTNER_FIRM_ID, "model_key": model_key,
                "as_of_date": as_of, "ticker": ticker,
                "security_name": sym.get("companyName"),
                "product_class": sym.get("assetType"), "target_weight": weight,
                "actual_weight": None,
                "is_opal_etf": ticker in OPAL_ETF_TICKERS,
                "source_pipeline": SOURCE_PIPELINE, "_ingested_at": ingested,
            })
        residual = round(1.0 - weight_sum, 8)
        if residual < -1e-6:
            # CTO 051908Z edge note: the feeder also skips silently here, so
            # parity holds -- but an over-1.0 vendor weight sum deserves a voice.
            log(f"  WARN: [{as_of}] {model_key} weight_sum {weight_sum:.6f} > 1.0 "
                "-- no residual emitted (mirrors the feeder; vendor state)")
        if residual > 1e-6:
            all_comp.append({
                "firm_id": PARTNER_FIRM_ID, "model_key": model_key,
                "as_of_date": as_of, "ticker": CASH_TICKER,
                "security_name": "Custodial cash residual",
                "product_class": "cash", "target_weight": residual,
                "actual_weight": None, "is_opal_etf": False,
                "source_pipeline": SOURCE_PIPELINE, "_ingested_at": ingested,
            })
    return (pd.DataFrame(all_pos, columns=POSITIONS_COLUMNS),
            pd.DataFrame(all_comp, columns=COMPOSITION_COLUMNS))


def tie_check(derived_15: pd.DataFrame) -> dict:
    """R3: derived 07-15 vs the fresh 07-16 partition, per-model, 2%."""
    fresh = pd.read_parquet(io.BytesIO(s3.get_object(
        Bucket=FEEDER_BUCKET,
        Key=f"{FEEDER_PREFIX}/model_aua_positions/{PARTNER_FIRM_ID}/2026-07-16.parquet"
    )["Body"].read()))
    d = derived_15.groupby("model_key")["model_value"].sum()
    f = fresh.groupby("model_key")["model_value"].sum()
    report, worst = {}, 0.0
    for k in sorted(set(d.index) | set(f.index)):
        dv, fv = float(d.get(k, 0)), float(f.get(k, 0))
        drift = abs(dv - fv) / fv if fv else 1.0
        worst = max(worst, drift)
        report[k] = {"derived_0715": round(dv, 2), "fresh_0716": round(fv, 2),
                     "drift": round(drift, 6)}
        log(f"  TIE {k}: derived-0715 {dv:,.2f} vs fresh-0716 {fv:,.2f} "
            f"(drift {drift:.4%})")
    if worst > TIE_TOLERANCE:
        raise RuntimeError(f"R3 TIE-CHECK MISS: worst drift {worst:.4%} > "
                           f"{TIE_TOLERANCE:.0%} -- PUBLISH ABORTED")
    log(f"OK: R3 tie-check PASS (worst drift {worst:.4%} <= {TIE_TOLERANCE:.0%})")
    return report


def publish(df: pd.DataFrame, artifact: str, date: str) -> str:
    buf = io.BytesIO()
    df.to_parquet(buf, index=False)
    key = f"{FEEDER_PREFIX}/{artifact}/{PARTNER_FIRM_ID}/{date}.parquet"
    s3.put_object(Bucket=FEEDER_BUCKET, Key=key, Body=buf.getvalue())
    listed = s3.list_objects_v2(Bucket=FEEDER_BUCKET, Prefix=key)
    if not any(o["Key"] == key and o["Size"] > 0
               for o in listed.get("Contents", [])):
        raise RuntimeError(f"publish landing MISSING: {key}")
    log(f"OK: published s3://{FEEDER_BUCKET}/{key} ({len(df)} rows, "
        "listing-verified)")
    return key


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--transform-commit", default="UNREVIEWED",
                    help="the reviewed commit sha of THIS script (R2/R4)")
    args = ap.parse_args()

    models, shared_inputs = load_models()
    frames, inputs_by_date = {}, {}
    for as_of, d8 in DATES:
        inputs: list = []
        pos, comp = transform_date(models, as_of, d8, inputs)
        frames[as_of] = (pos, comp)
        inputs_by_date[as_of] = inputs
        for cls, label in (("model", "1a"), ("sma", "1c")):
            sub = pos[pos["cohort_class"] == cls]
            log(f"  [{as_of}] Cohort {label}: {sub['model_value'].sum():,.2f} "
                f"({len(sub)} accounts)")

    report = tie_check(frames["2026-07-15"][0])   # R3 gates everything below

    if args.dry_run:
        log("OK: dry-run -- nothing published")
        return 0

    manifest_common = {
        "derivation": "derived-from-landed-bronze",
        "zero_vendor_calls": True,
        "ruling": "CTO 20260716T051145Z option (b); riders R1-R4",
        "transform": "org/tier2_senior/0.5.0_AE_OpalETL/deliverables/wp5_true_vintage_transform.py",
        "transform_commit": args.transform_commit,
        "rmid_pairing_source": f"s3://{MONO}/{ROSTER_KEY}",
        "shared_inputs": shared_inputs,   # R1 fix: roster ETag + registry sha
        "tie_check_derived0715_vs_fresh0716": report,
    }
    for as_of, _ in DATES:
        pos, comp = frames[as_of]
        publish(pos, "model_aua_positions", as_of)
        publish(comp, "model_composition", as_of)
        manifest = dict(manifest_common,
                        as_of_date=as_of,
                        generated_at=dt.datetime.now(dt.timezone.utc).isoformat(),
                        inputs=inputs_by_date[as_of])
        mkey = (f"{FEEDER_PREFIX}/derivation_manifests/{PARTNER_FIRM_ID}/"
                f"{as_of}.json")
        s3.put_object(Bucket=FEEDER_BUCKET, Key=mkey,
                      Body=json.dumps(manifest, indent=2).encode(),
                      ContentType="application/json")
        log(f"OK: derivation manifest s3://{FEEDER_BUCKET}/{mkey} "
            f"({len(inputs_by_date[as_of])} cited inputs)")

    holes = {
        "holes": HOLES,
        "reason": ("vendor-unrecoverable at feeder grain: the SmartX pull is "
                   "snapshot-only (no historical query) and C5 landed bronze "
                   "begins 20260714. Documented per the ruling-16 "
                   "honest-holes precedent; CTO ruling 20260716T051145Z."),
        "grain_note": ("model-grain daily closingEquity for these dates EXISTS "
                       "in landed smartx/model/*/bronze/model_aum series -- "
                       "approved P2 evidence doc, not a feeder partition."),
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
    }
    hkey = (f"{FEEDER_PREFIX}/derivation_manifests/{PARTNER_FIRM_ID}/"
            "HOLES_2026-07-09_to_2026-07-13.json")
    s3.put_object(Bucket=FEEDER_BUCKET, Key=hkey,
                  Body=json.dumps(holes, indent=2).encode(),
                  ContentType="application/json")
    log(f"OK: hole manifest s3://{FEEDER_BUCKET}/{hkey}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
