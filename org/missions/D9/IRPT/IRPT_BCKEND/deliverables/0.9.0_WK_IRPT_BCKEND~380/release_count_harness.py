#!/usr/bin/env python3
"""Release re-measure harness for the holdings producer (IRPT_BCKEND, IB-pr-533, round 192).

READ ONLY. The harness makes get and list calls with the caller's own boto3 identity and evaluates
the producer's own functions in memory. It holds no write, publish or invoke call: its text is
checked for them by IB192-1-AC1.

Usage:
  python release_count_harness.py <repo_root> --as-of <YYYY-MM-DD>[,<firm>=<YYYY-MM-DD>...]
      --firms <all|firm,...> --out <json path outside the repo>
      [--date-check <fire date>] [--seed-receipts <json>] [--receipts-out <json>]

Per firm, for the pinned source date as_of (never select_business_date):
  1. build_snapshot(firm, inputs, as_of) over one VersionedInputs, the code as it stands;
     then build_snapshot again over the SAME inputs with apply_cash_rule replaced by identity
     (a monkeypatch inside this process only).
  2. A mover is a SECURITY node whose asset_class differs between the two builds, matched by node_id.
     Its layer is the producer's classify_security class_source, re-run on its display symbol,
     description and security id (the node carries no per-node layer).
  3. The served publication is read the way the producer's orchestration reads it (begin and
     served_publication, read calls only), and evaluate_publish_gate runs on the with-rule candidate twice: BEFORE with the
     pre-repair marks rule (written here), AFTER with directory_marks_no_closures and
     closed_account_ids.
  4. Receipts are the objects the builds read (VersionedInputs.receipts()); the digest is the sha256
     of their canonical JSON (sort_keys, compact separators, ASCII).
--seed-receipts pins RUN B's reads to a RUN A receipts file (VersionedInputs._refs pre-seeded): every
object is then read at the version RUN A read, and a changed byte raises in the producer's own reader.
--date-check <fire date> also builds each firm once with as_of = select_business_date(fire date), no
replay, and records the newest candidate's clocks.business_date beside the calendar's previous trading day.
"""
import argparse
import datetime as dt
import hashlib
import json
import re
import sys
import time
from pathlib import Path

FIRMS = ["49financial", "cottonwood", "inflection"]
TICKER_SHAPE = re.compile(r"[A-Z]{2,5}")


class _Recorder:
    """The read client: logs each get_object (Bucket, Key); every other attribute is the client's own."""

    def __init__(self, client):
        self._client = client
        self.reads = []

    def get_object(self, **kwargs):
        self.reads.append((kwargs.get("Bucket"), kwargs.get("Key")))
        return self._client.get_object(**kwargs)

    def __getattr__(self, name):
        return getattr(self._client, name)


def canonical_digest(obj):
    text = json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(text.encode("ascii")).hexdigest()


def parse_as_of(text):
    default, per_firm = None, {}
    for part in [p.strip() for p in text.split(",") if p.strip()]:
        if "=" in part:
            firm, day = part.split("=", 1)
            per_firm[firm.strip()] = day.strip()
        else:
            default = part
    return default, per_firm


def as_of_for(firm, default, per_firm):
    day = per_firm.get(firm, default)
    if day is None:
        raise SystemExit("no --as-of for %s" % firm)
    dt.date.fromisoformat(day)  # validates the pin
    return day


def marks_before_rule(hs, client, bucket):
    """The pre-repair rule, written in this harness: every landed directory entry counts, a missing
    termination indicator counts UNKNOWN, all UNKNOWN and the directory non-empty. Carried-forward
    entries are not excluded (the base commit's rule)."""
    entries = hs._directory_entries(client, bucket) or []
    if not entries:
        return False
    return all(((e.get("termination") or {}).get("indicator") or "UNKNOWN") == "UNKNOWN" for e in entries)


def measure(hs, firm, as_of, client, seed):
    inputs = hs.VersionedInputs(client)
    seed_keys = set()
    for ref in seed:
        key = (ref["bucket"], ref["key"])
        inputs._refs[key] = dict(ref)
        seed_keys.add(key)
    start = len(client.reads)
    with_rule = hs.build_snapshot(firm, inputs, as_of)
    real_rule = hs.apply_cash_rule
    hs.apply_cash_rule = lambda result: result
    try:
        identity = hs.build_snapshot(firm, inputs, as_of)
    finally:
        hs.apply_cash_rule = real_rule
    build_keys = set(client.reads[start:])

    sec = [n for n in with_rule["nodes"] if n.get("node_kind") == "SECURITY"]
    by_id = {n["node_id"]: n for n in identity["nodes"] if n.get("node_kind") == "SECURITY"}
    unmatched = sum(1 for n in sec if n["node_id"] not in by_id)
    dupes = len(sec) - len({n["node_id"] for n in sec})
    movers = [n for n in sec if n["node_id"] in by_id
              and n.get("asset_class") != by_id[n["node_id"]].get("asset_class")]

    ec, clf = hs.canonical_classifier()
    layer_counts, rerun_mismatch, tickers = {}, 0, set()
    for n in movers:
        disp = n.get("display") or {}
        symbol = disp.get("symbol")
        found = hs.classify_security(ec, clf, symbol, disp.get("description") or disp.get("label"),
                                     description=disp.get("description"), security_id=n.get("security_id"))
        layer = found.get("class_source")
        layer_counts[layer] = layer_counts.get(layer, 0) + 1
        if found.get("asset_class") != n.get("asset_class"):
            rerun_mismatch += 1
        if layer == hs.CANONICAL_CLASS_SOURCE and isinstance(symbol, str) and TICKER_SHAPE.fullmatch(symbol):
            tickers.add(symbol)
    canon = layer_counts.get(hs.CANONICAL_CLASS_SOURCE, 0)
    fallb = layer_counts.get(hs.FALLBACK_CLASS_SOURCE, 0)

    hs.recompute_weights(with_rule["nodes"])  # the producer's orchestration does this before its gate
    bucket = hs.firm_bucket_map().get(firm, "")
    reader = hs.HoldingsPublication(client, firm, qa=False)
    expected = reader.begin()  # reads only
    served = hs.served_publication(reader, expected)
    closed = lambda: hs.closed_account_ids(client, bucket, firm)  # noqa: E731
    before = hs.evaluate_publish_gate(with_rule, served, closed, lambda: marks_before_rule(hs, client, bucket))
    after = hs.evaluate_publish_gate(with_rule, served, closed,
                                     lambda: hs.directory_marks_no_closures(client, bucket, firm))

    receipts = inputs.receipts()
    summary = {
        "pinned_as_of": as_of,
        "business_date_built": with_rule["clocks"]["business_date"],
        "security_nodes": len(sec),
        "movers_canonical": canon,
        "movers_fallback": fallb,
        "movers_other_layer": len(movers) - canon - fallb,
        "movers_total": len(movers),
        "canonical_tickers": sorted(tickers),
        "rerun_asset_class_mismatch": rerun_mismatch,
        "security_node_id_duplicates": dupes,
        "security_nodes_unmatched_in_identity_build": unmatched,
        "gate_before": before["outcome"],
        "gate_after": after["outcome"],
        "conditions_before": [c["condition"] for c in before["conditions"]],
        "conditions_after": [c["condition"] for c in after["conditions"]],
        "lost_accounts_listed_after": after["listed"].get("account_lost_not_refused", {}).get("count", 0),
        "closed_accounts_not_refused_after": after["listed"].get("closed_accounts_not_refused", {}).get("count", 0),
        "receipts_digest": canonical_digest(receipts),
        "receipts_count": len(receipts),
        "seeded_receipts": len(seed_keys),
        "distinct_objects_read_by_builds": len(build_keys),
        "build_reads_outside_seed": len(build_keys - seed_keys),
    }
    return summary, receipts


def date_check(hs, tcal, fire, firms, client):
    fire_day = dt.date.fromisoformat(fire)
    cutoff = hs.select_business_date(fire_day)
    dates = {}
    for firm in firms:
        try:
            snap = hs.build_snapshot(firm, hs.VersionedInputs(client), cutoff)
            dates[firm] = snap["clocks"]["business_date"]
        except Exception as exc:  # noqa: BLE001 -- recorded by type; the message may carry object names
            dates[firm] = "ERROR:" + type(exc).__name__
    t_minus_1 = tcal.prev_trading_day(fire_day).isoformat()
    return {"fire_date": fire, "cutoff_select_business_date": cutoff, "t_minus_1": t_minus_1,
            "newest_candidate_dates": dates,
            "all_equal_to_t_minus_1": all(v == t_minus_1 for v in dates.values())}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("repo_root")
    ap.add_argument("--as-of", required=True)
    ap.add_argument("--firms", default="all")
    ap.add_argument("--out", required=True)
    ap.add_argument("--date-check")
    ap.add_argument("--seed-receipts")
    ap.add_argument("--receipts-out")
    args = ap.parse_args(argv)

    repo = Path(args.repo_root).resolve()
    for target in [Path(args.out).resolve()] + ([Path(args.receipts_out).resolve()] if args.receipts_out else []):
        if target == repo or repo in target.parents:
            raise SystemExit("REFUSED: output paths must sit outside the repository")
    prod = repo / "data" / "assets" / "scripts" / "gold" / "investor_reporting"
    if not prod.is_dir():
        raise SystemExit("no producer directory under the repo root")
    sys.path.insert(0, str(prod))
    sys.path.insert(0, str(repo / "lib"))

    import boto3
    import holdings_snapshot as hs  # the producer, imported from this tree
    import source_inputs  # noqa: F401 -- VersionedInputs is the producer's own input reader
    import trading_calendar as tcal

    firms = FIRMS if args.firms == "all" else [f.strip() for f in args.firms.split(",") if f.strip()]
    if any(f not in FIRMS for f in firms):
        raise SystemExit("REFUSED: unknown firm in --firms")
    default, per_firm = parse_as_of(args.as_of)
    seed = json.loads(Path(args.seed_receipts).read_text(encoding="utf-8")) if args.seed_receipts else {}
    client = _Recorder(boto3.client("s3", region_name="us-east-1"))

    result = {"harness": "release_count_harness.py", "as_of_argument": args.as_of, "firms": {}}
    receipts_store = {}
    for firm in firms:
        as_of = as_of_for(firm, default, per_firm)
        began = time.time()
        summary, receipts = measure(hs, firm, as_of, client, seed.get(firm) or [])
        summary["build_and_gate_seconds"] = round(time.time() - began)
        result["firms"][firm] = summary
        receipts_store[firm] = receipts
        print("OK: %s as_of=%s canonical=%d fallback=%d gate_before=%s gate_after=%s digest=%s"
              % (firm, as_of, summary["movers_canonical"], summary["movers_fallback"],
                 summary["gate_before"], summary["gate_after"], summary["receipts_digest"][:12]))

    if args.date_check:
        fire = dt.date.fromisoformat(args.date_check).isoformat()
        result["first_fire_check"] = date_check(hs, tcal, fire, firms, client)
        print("OK: date-check fire=%s t_minus_1=%s" % (fire, result["first_fire_check"]["t_minus_1"]))

    Path(args.out).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.receipts_out:
        Path(args.receipts_out).write_text(json.dumps(receipts_store, sort_keys=True), encoding="utf-8")
    print("OK: wrote %s" % args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
