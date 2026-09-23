"""Read-only C02 census and I4 retained-data examples; no cloud writer exposed."""
from pathlib import Path
import collections
import datetime
import hashlib
import io
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[7]))
import boto3
from botocore.config import Config
from lib.research.corpus import library, backlog, typed, substrate
from lib.research.harvest import store

OUT = Path(__file__).resolve().parent / "evidence"


class ReadOnlyS3:
    def __init__(self):
        self.client = boto3.client("s3", region_name="us-east-1", config=Config(
            retries={"total_max_attempts": 1}, connect_timeout=10, read_timeout=30))
        self.cache = {}
        self.calls = collections.Counter()

    def get_object(self, Bucket, Key):
        identity = (Bucket, Key)
        if identity not in self.cache:
            self.calls["get_object"] += 1
            response = self.client.get_object(Bucket=Bucket, Key=Key)
            raw = response["Body"].read()
            self.cache[identity] = (response, raw)
        response, raw = self.cache[identity]
        return {**response, "Body": io.BytesIO(raw)}

    def head_object(self, Bucket, Key):
        self.calls["head_object"] += 1
        return self.client.head_object(Bucket=Bucket, Key=Key)

    def get_paginator(self, name):
        if name not in {"list_objects_v2", "list_object_versions"}:
            raise RuntimeError("unsupported read-only paginator " + name)
        self.calls[name] += 1
        return self.client.get_paginator(name)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def keys(client, prefix):
    return sorted(item["Key"] for page in client.get_paginator("list_objects_v2").paginate(
        Bucket=store.HARVEST_BUCKET, Prefix=prefix) for item in page.get("Contents", []))


def save(name, document):
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(json.dumps(document, indent=2, ensure_ascii=True, default=str) + "\n",
                            encoding="ascii")


def main():
    root = Path(library.library_root()).resolve()
    entries = library.census(str(root))
    document = backlog.build(str(root))
    assert document["resolved"] + document["unresolved"] + document["ambiguous"] == document["folders_read"]
    by_folder = {r["folder"]: r for r in document["records"]}
    client = ReadOnlyS3()
    latest = store.silver_latest(typed.SOURCE, typed.TABLE, typed.RECORD_KEY_FIELDS, client=client)
    rows = list(latest.values())
    if not rows:
        raise RuntimeError("empty admitted population cannot prove lineage")
    required = {"security_key", "report_id", "bronze_key", "extract_key", "source_relpath", "period"}
    if any(not required.issubset(row) for row in rows):
        raise RuntimeError("typed row schema mismatch")
    by_path = collections.defaultdict(list)
    for row in rows:
        by_path[row["source_relpath"]].append(row)
    measured = []
    for entry in entries:
        source = root / entry["path"]
        if root not in source.resolve().parents:
            raise RuntimeError("source path escaped library: " + entry["path"])
        local_hash = sha(source.read_bytes())
        record = by_folder.get(entry["folder"], {})
        admitted = []
        for row in by_path[entry["path"]]:
            bucket, key = substrate._split_uri(row["bronze_key"])
            bronze = client.get_object(Bucket=bucket, Key=key)["Body"].read()
            extract_bucket, extract_key = substrate._split_uri(row["extract_key"])
            extraction_bytes = client.get_object(Bucket=extract_bucket, Key=extract_key)["Body"].read()
            extraction = json.loads(extraction_bytes)
            admitted.append({"security_key": row["security_key"], "report_id": row["report_id"],
                "bronze_key": row["bronze_key"], "bronze_byte_sha256": sha(bronze),
                "local_bytes_match": local_hash == sha(bronze),
                "identity_matches_backlog": row["security_key"] == record.get("security_key"),
                "extract_key": row["extract_key"], "extract_byte_sha256": sha(extraction_bytes),
                "extract_bronze_key_matches": extraction.get("bronze_key") == row["bronze_key"],
                "extract_bronze_hash_matches": extraction.get("bronze_sha256") == sha(bronze),
                "extractable": extraction.get("extractable"),
                "extraction_reason": extraction.get("reason"),
                "period": row["period"], "period_source": row.get("period_source"),
                "period_evidence": row.get("period_evidence"),
                "period_absent_reason": row.get("period_absent_reason"),
                "report_class": row.get("report_class")})
        measured.append({**entry, "local_byte_sha256": local_hash,
                         "identity_state": record.get("state", "UNRESOLVED"),
                         "identity_reason": record.get("reason"), "admitted_rows": admitted})
    bronze_keys = keys(client, store.table_prefix(typed.SOURCE, "bronze", typed.BRONZE_REQUEST))
    extraction_keys = keys(client, store.table_prefix(typed.SOURCE, "bronze", typed.EXTRACT_REQUEST))
    referenced_bronze = {substrate._split_uri(row["bronze_key"])[1] for row in rows}
    referenced_extractions = {substrate._split_uri(row["extract_key"])[1] for row in rows}
    source_paths = {e["path"] for e in entries}
    period_order = {}
    for security_key in sorted({r["security_key"] for r in rows}):
        ordered, ties = typed.order_reports_with_evidence(
            [r for r in rows if r["security_key"] == security_key])
        period_order[security_key] = {
            "periods": [r["period"] for r in ordered],
            "independent_order_ok": typed.period_order_ok([r for r in ordered if r["period"]]),
            "renderer_tiebreaks": ties}
    if not all(item["independent_order_ok"] for item in period_order.values()):
        raise RuntimeError("independent period-order validation failed")
    admitted = [a for item in measured for a in item["admitted_rows"]]
    failures = [a for a in admitted if not all(a[k] for k in (
        "local_bytes_match", "identity_matches_backlog", "extract_bronze_key_matches", "extract_bronze_hash_matches"))]
    missing_admitted = [item["path"] for item in measured
                        if item["identity_state"] == "RESOLVED" and not item["admitted_rows"]]
    summary = {"folders": document["folders_read"], "files": len(entries),
        "bytes": sum(e["size"] for e in entries),
        "extensions": dict(collections.Counter(e["ext"] for e in entries)),
        "resolved_folders": document["resolved"], "unresolved_folders": document["unresolved"],
        "ambiguous_folders": document["ambiguous"], "admitted_rows": len(rows),
        "admitted_source_files": sum(bool(e["admitted_rows"]) for e in measured),
        "excluded_source_files": sum(not e["admitted_rows"] for e in measured),
        "unique_security_keys": len({r["security_key"] for r in rows}),
        "bronze_objects": len(bronze_keys), "extraction_objects": len(extraction_keys),
        "lineage_failures": len(failures), "missing_admitted_files": missing_admitted,
        "typed_paths_absent_from_library": sorted(set(by_path) - source_paths),
        "unreferenced_bronze_objects": sorted(set(bronze_keys) - referenced_bronze),
        "unreferenced_extractions": sorted(set(extraction_keys) - referenced_extractions),
        "period_present": sum(bool(row["period"]) for row in rows),
        "period_absent_with_reason": sum(not row["period"] and bool(row.get("period_absent_reason")) for row in rows)}
    save("C02_RECONCILIATION.json", {"evidence_level": "retained-data read",
        "measured_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "root_source": library.library_root_source(), "backlog": document,
        "typed_row_keys": sorted(rows[0]), "summary": summary, "files": measured,
        "period_order": period_order,
        "read_calls": dict(client.calls), "actual_s3_writes": 0})
    selected = substrate._pick_first_covered_security_key(client)
    if selected is None:
        raise RuntimeError("no representative continuation with covered fields")
    result = substrate.substrate(selected, client=client)
    derived = {}
    for member in substrate.DERIVED_MEMBERS:
        entry = result[member]
        if "absent" in entry:
            derived[member] = entry
            continue
        bucket, key = substrate._split_uri(entry["uri"])
        raw = client.get_object(Bucket=bucket, Key=key)["Body"].read()
        parsed = json.loads(raw)
        derived[member] = {"uri": entry["uri"], "retained_byte_sha256": sha(raw),
                           "artifact_content_sha256": parsed["content_sha256"], "document": parsed}
    save("I4_RETAINED_EXAMPLE.json", {"evidence_level": "retained-data read",
        "measured_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "substrate": result, "referenced_documents": derived, "read_calls": dict(client.calls),
        "actual_s3_writes": 0})
    print(json.dumps(summary, indent=2))
    print("I4 retained example: " + selected)
    return 1 if failures or missing_admitted or summary["typed_paths_absent_from_library"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
