#!/usr/bin/env python3
"""IB-pr-584 (TO IRPT_BCKEND.TO-IB-pr-584) -- the refusal anatomy of 49 Financial after the absent_at_source exemption.

READ-ONLY, in one process, over the live pinned inputs and the served publication, through the repository's own readers.
The S3 client is wrapped: only get_object, head_object and list_objects_v2 pass; any other call raises and is counted as
refused. Nothing is landed, published, written, signed or invoked; no refusal record is written.

The candidate is built ONCE (build_snapshot over VersionedInputs). The WITHOUT arm gates a deep copy with no evidence
provider; the WITH arm gates a second deep copy with the provider run_firm builds (hs._absent_provider). Each lost account
(the served account ids the candidate does not carry, computed as evaluate_publish_gate computes them) is classified into
exactly one class, first match in order: exempted_absent_at_source, closed_by_directory, in_source_with_positions,
evidence_incomplete, other. classified_security_lost is recomputed as the gate does: now_unclassified & (placed - unplaced).
Prints counts only, and writes the record JSON named by argv[2].

    python IB220-1_49f_refusal_anatomy_harness.py <repo_root> <record_out.json>
"""
import copy
import datetime as dt
import io
import json
import subprocess
import sys
from collections import Counter
from numbers import Integral
from pathlib import Path

READ_OPS = ("get_object", "head_object", "list_objects_v2")
CLASSES = ("exempted_absent_at_source", "closed_by_directory", "in_source_with_positions", "evidence_incomplete", "other")
SERVED_BATCH = 4096


class ReadOnlyS3:
    """Wraps the boto3 S3 client: a read operation passes and is counted; any other attribute raises (a write is refused)."""

    def __init__(self, client):
        self._client = client
        self.calls = Counter()
        self.refused = Counter()

    def __getattr__(self, name):
        if name.startswith("_"):
            raise AttributeError(name)
        if name == "get_paginator":
            def paginator(operation_name, *args, **kwargs):
                if operation_name not in READ_OPS:
                    self.refused["get_paginator:" + str(operation_name)] += 1
                    raise RuntimeError("READ-ONLY guard: refused paginator %s" % operation_name)
                self.calls["get_paginator:" + operation_name] += 1
                return self._client.get_paginator(operation_name, *args, **kwargs)
            return paginator
        if name not in READ_OPS:
            self.refused[name] += 1
            raise RuntimeError("READ-ONLY guard: refused S3 call %s" % name)
        fn = getattr(self._client, name)

        def call(*args, **kwargs):
            self.calls[name] += 1
            return fn(*args, **kwargs)
        return call


def evidence_complete(ev, hs) -> bool:
    """Mirror of the completeness rule absent_at_source_exempt applies (a day present, each partition's count an integer,
    the prior non-empty, the candidate at least the floor percent of the prior). True only when every rule holds."""
    if not isinstance(ev, dict) or not ev.get("candidate_day") or not ev.get("prior_day"):
        return False
    for table in hs.ABSENT_AT_SOURCE_TABLES:
        days = ev.get(table)
        if not isinstance(days, dict):
            return False
        cand, prior = days.get("candidate"), days.get("prior")
        if not isinstance(cand, dict) or not isinstance(prior, dict):
            return False
        n_cand, n_prior = cand.get("account_count"), prior.get("account_count")
        if not all(isinstance(n, Integral) and not isinstance(n, bool) and n >= 0 for n in (n_cand, n_prior)):
            return False
        if n_prior <= 0 or n_cand * 100 < n_prior * hs.ABSENT_AT_SOURCE_FLOOR_PERCENT:
            return False
    return True


def served_class_census(hs, publisher, expected, keys, pub, pq):
    """Distinct served SECURITY keys in `keys`, counted by the asset_class the served snapshot placed them in. Read from the
    served Gold parquet exactly as served_publication reads it; only class values are counted, no key is returned."""
    doc = expected["document"]
    date = doc["latest_date"]
    row = doc["dates"][date]
    revision, partition = row["revision"], "date=" + date
    manifest = json.loads(publisher.read_exact(row["manifest"], expected_location=publisher.location(
        "platinum", partition, revision + ".manifest.json"), max_bytes=pub.MAX_JSON_BYTES))
    data = publisher.read_exact(manifest["gold"], expected_location=publisher.location(
        "gold", partition, revision + ".parquet"), max_bytes=pub.MAX_GOLD_BYTES)
    parquet = pq.ParquetFile(io.BytesIO(data))
    del data
    seen = {}
    for batch in parquet.iter_batches(batch_size=SERVED_BATCH, columns=["node_json"]):
        for s in batch.column(0).to_pylist():
            node = json.loads(s)
            if node.get("node_kind") != "SECURITY":
                continue
            key = hs._gate_security_key(node)
            if key in keys and key not in seen:
                seen[key] = str(node.get("asset_class"))
    return Counter(seen.values())


def main():
    repo = Path(sys.argv[1]).resolve()
    out = Path(sys.argv[2]).resolve()
    sys.path.insert(0, str(repo / "data" / "assets" / "scripts" / "gold" / "investor_reporting"))
    import boto3
    import pyarrow.parquet as pq
    import holdings_snapshot as hs
    import holdings_49f
    import publication as pub

    base = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=str(repo)).decode("ascii").strip()
    read_date = dt.datetime.now(dt.timezone.utc).date().isoformat()
    s3 = ReadOnlyS3(boto3.client("s3", region_name="us-east-1"))
    today_business = hs.select_business_date()
    firm_ids = [k for k, b in hs.BUILDERS.items() if b is holdings_49f.build_49f_meshed]
    if len(firm_ids) != 1:
        print("ERROR: the 49financial builder does not resolve to exactly one firm key (%d)" % len(firm_ids))
        sys.exit(2)
    firm_id = firm_ids[0]
    bucket = hs.firm_bucket_map().get(firm_id, "")
    print("OK: business date selected %s; firm scope resolved by builder identity" % today_business)

    # Mirror run_firm up to the gate, WITHOUT writing: one build, the served publication, the directory marks.
    publisher = hs.HoldingsPublication(s3, firm_id, qa=False)
    expected = publisher.begin()
    inputs = hs.VersionedInputs(s3)
    snapshot = hs.build_snapshot(firm_id, inputs, today_business)
    served = hs.served_publication(publisher, expected)
    candidate_day = (snapshot.get("clocks") or {}).get("business_date")
    served_day = served.get("business_date") if served else None
    closed_set = hs.closed_account_ids(s3, bucket, firm_id)
    marks = hs.directory_marks_no_closures(s3, bucket, firm_id)
    print("OK: candidate_day=%s served_day=%s served_present=%s closed_directory_count=%d marks_no_closures=%s"
          % (candidate_day, served_day, served is not None, len(closed_set), marks))

    def closed():
        return closed_set

    def marks_fn():
        return marks

    # ARM WITHOUT: no evidence provider (plain deep copy of the one candidate).
    cand_wo = copy.deepcopy(snapshot)
    gate_wo = hs.evaluate_publish_gate(cand_wo, served, closed, marks_fn)
    cond_wo = [c["condition"] for c in gate_wo["conditions"]]
    print("OK: WITHOUT outcome=%s conditions=%s" % (gate_wo["outcome"], cond_wo))

    # ARM WITH: deep copy with the provider run_firm builds; the provider's evidence is captured for the classes.
    cand_with = copy.deepcopy(snapshot)
    captured = []
    provider = hs._absent_provider(captured, firm_id, inputs, cand_with, served)
    gate_with = hs.evaluate_publish_gate(cand_with, served, closed, marks_fn, absent_at_source_evidence=provider)
    cond_with = [c["condition"] for c in gate_with["conditions"]]
    gate_exempt = set(((gate_with.get("listed") or {}).get("account_lost_absent_at_source") or {}).get("dates") or {})
    print("OK: WITH outcome=%s conditions=%s gate_exempted=%d provider_called=%s"
          % (gate_with["outcome"], cond_with, len(gate_exempt), bool(captured)))
    evidence = next((e for e in reversed(captured) if e), None)

    # THE LOST ACCOUNTS, exactly as evaluate_publish_gate computes them.
    have = set((snapshot.get("scope") or {}).get("account_ids") or []) | hs._gate_account_ids(snapshot.get("nodes") or [])
    lost = set(served["account_ids"]) - have
    closed_gone = closed_set & lost
    lost_gate = lost - closed_gone
    exempt_ids = set()
    if evidence is not None and lost_gate:
        exempt_ids, _details = hs.absent_at_source_exempt(lost_gate, evidence)
    exempt_agrees = exempt_ids == gate_exempt
    present = set()
    if evidence is not None:
        for table in hs.ABSENT_AT_SOURCE_TABLES:
            for label in ("candidate", "prior"):
                part = (evidence.get(table) or {}).get(label) or {}
                present |= {str(i) for i in (part.get("accounts_with_positions") or ())}
    complete = evidence_complete(evidence, hs)
    classes = Counter()
    for acct in lost:
        if acct in exempt_ids:
            cls = CLASSES[0]
        elif acct in closed_gone:
            cls = CLASSES[1]
        elif acct in present:
            cls = CLASSES[2]
        elif not complete:
            cls = CLASSES[3]
        else:
            cls = CLASSES[4]
        classes[cls] += 1
    classes_full = {k: classes.get(k, 0) for k in CLASSES}
    total, exempted = len(lost), len(exempt_ids)
    print("OK: lost_accounts total=%d exempted=%d remaining=%d classes=%s exempt_agrees_with_gate=%s evidence_complete=%s"
          % (total, exempted, total - exempted, classes_full, exempt_agrees, complete))
    if sum(classes_full.values()) != total:
        print("ERROR: class sum %d does not equal lost total %d" % (sum(classes_full.values()), total))
        sys.exit(3)

    # CLASSIFIED_SECURITY_LOST, exactly as the gate computes it.
    secs = [n for n in (snapshot.get("nodes") or []) if n.get("node_kind") == "SECURITY"]
    now_unclassified = {hs._gate_security_key(n) for n in secs if n.get("asset_class") == "unclassified"} - {None}
    placed, unplaced = hs._gate_served_keys(served)
    lost_class = now_unclassified & (placed - unplaced)
    census = served_class_census(hs, publisher, expected, lost_class, pub, pq)
    print("OK: classified_security_lost total=%d served_placed_total=%d candidate_unclassified_total=%d served_unplaced_total=%d"
          % (len(lost_class), len(placed), len(now_unclassified), len(unplaced)))
    print("OK: served asset_class of the classified_security_lost securities (distinct, counts): %s" % dict(census))

    # CONDITIONS REMAINING and their agreement with the counts.
    remaining_accounts = lost_gate - exempt_ids
    expect_account_lost = bool(remaining_accounts) and not marks
    agree = ("account_lost" in cond_with) == expect_account_lost and ("classified_security_lost" in cond_with) == bool(lost_class)
    print("OK: conditions_remaining=%s agree_with_counts=%s" % (cond_with, agree))

    reading = ("The lost securities were placed by the served snapshot in the asset classes named in the census: %s. The candidate "
               "build classifies each security from the canonical ETF classification table first and the declared bd-securities "
               "fallback second, and leaves it unclassified when neither answers. The candidate carries %d unclassified securities "
               "against %d unclassified in the served publication; the count of the previous candidate is not read here."
               % (", ".join("%s=%d" % (k, v) for k, v in sorted(census.items())) or "none",
                  len(now_unclassified), len(unplaced)))
    method = ("READ-ONLY, in one process, of the HEAD code at the base commit over the live pinned inputs: the box default S3 client "
              "wrapped so only get_object, head_object and list_objects_v2 pass; select_business_date; HoldingsPublication.begin and "
              "VersionedInputs; build_snapshot once for the 49financial firm; served_publication; then the WITHOUT arm runs "
              "evaluate_publish_gate with no evidence provider on a deep copy and the WITH arm runs evaluate_publish_gate with the "
              "provider run_firm builds on a second deep copy; lost is the served account ids minus the candidate scope and "
              "account-node ids; each lost account is classed once in order; classified_security_lost is now_unclassified & "
              "(placed - unplaced). Nothing is landed, written, published, signed or invoked.")
    notes = [
        "Each count rests on one build of the candidate and one read of the served index and Gold parquet, through the repository's own readers.",
        "The WITH arm's evidence is the provider's own return; exempted counts come from absent_at_source_exempt and equal the gate's listing: %s." % exempt_agrees,
        "Not read: the refusal record, any landed object, any Lambda function, the previous candidate; no security identifier or account identifier is recorded.",
        "Served asset classes of the classified_security_lost securities (distinct keys, counted only): %s." % (dict(census) or "none"),
        "Read calls through the wrapper: %s. Refused write-capable calls: %s." % (dict(s3.calls), dict(s3.refused) or "none"),
        "Sparse directories added locally (never committed): investor-reporting gold and silver scripts, the investor-reporting Lambda, the mdpf gold and silver scripts, the v2_portal shared package, the investor-reporting contracts, lib.",
    ]
    record = {
        "firm_scope": "49financial",
        "candidate_day": candidate_day,
        "served_day": served_day,
        "lost_accounts": {"total": total, "exempted": exempted, "remaining": total - exempted, "classes": classes_full},
        "classified_security_lost": {"total": len(lost_class), "served_placed_total": len(placed),
                                     "candidate_unclassified_total": len(now_unclassified), "reading": reading},
        "conditions_remaining": cond_with,
        "base_commit": base, "read_date": read_date, "method": method, "claim": "measured", "notes": notes,
        "functions_invoked": 0, "sign_ins_made": 0, "aws_writes_made": 0,
        "rows_written": 0, "figures_written": 0, "vendor_requests_sent": 0,
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(record, indent=1, sort_keys=True) + "\n", encoding="ascii")
    print("OK: wrote record to %s" % out.name)


if __name__ == "__main__":
    main()
