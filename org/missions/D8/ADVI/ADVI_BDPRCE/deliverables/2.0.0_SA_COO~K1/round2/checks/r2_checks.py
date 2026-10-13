"""ADVI_BDPRCE round 2: record-shape graders, issuer 2.0.0_SA_COO~K1.

  ruleprobe --file <RULE_PROBE.json>      BP-b-1: THE rule run over a real partition
  replay    --file <REPLAY.json>          BP-b-2: R1 replayed over the served rows
  census    --file <CENSUS.json>          BP-b-3: the lot census over every client object
  trace2    --file <TRACE2_PROBE.json>    BP-b-4: the trace follows the served row
  cause     --file <CAUSE.json>           BP-b-5: the cause of missing daily files / lagging objects
  lotproof  --file <LOT_PROOF.json>       BP-b-6: the legacy output byte-unchanged, the lot table keyed on the lot
  packet    --file <PACKET.json>          BP-b-7: the FWD-7 before/after packet
  thread2   --file <THREAD2.json>         BP-b-8: the thread on a truly unlisted holding

Each prints one last line `<NAME> record ok ...` or `<NAME> record FAIL <why>`; exit 0 on ok. The graders prove shape,
read-only discipline and arithmetic; they do not prove a measurement is right (the issuer re-reads cited objects).
ASCII only. Never edit this file.
"""
import argparse
import json
import re
import sys

WRITE_VERBS = re.compile(
    r"\b(put-object|delete-object|delete-objects|copy-object|put-bucket|update-function|invoke|put-rule|put-targets|"
    r"start-execution|s3 cp [^ ]+ s3://|s3 rm|s3 sync [^ ]+ s3://|terraform apply|start-task|run-task)\b")
CLAIMS = {"measured", "inferred", "held", "absent"}
REPLAY_CLASSES = ["UNCHANGED", "CHANGED", "NOW_CARRY_FORWARD", "NOT_RECOMPUTABLE"]
CENSUS_CLASSES = ["PRICED_FROM_CANONICAL", "PRICED_OFF_NO_CANONICAL", "NOT_UNTICKERED"]
CAUSE_CLASSES = ["NO_RUN", "RUN_FAILED", "RUN_SKIPPED_BY_SCHEDULE", "WROTE_ELSEWHERE", "NOT_DETERMINED"]


def fail(name, why):
    print("%s record FAIL %s" % (name, why))
    return 1


def read_only(rec):
    calls = rec.get("calls")
    if not isinstance(calls, list) or not calls:
        return "calls missing or empty"
    for c in calls:
        if WRITE_VERBS.search(str(c)):
            return "write verb in calls: %s" % str(c)[:80]
    return None


def need(rec, keys):
    for k in keys:
        if k not in rec:
            return "lacks %s" % k
    return None


def partition(rec, key, classes, total_key):
    cls = rec.get(key)
    total = rec.get(total_key)
    if not isinstance(cls, dict) or not isinstance(total, int) or total <= 0:
        return "%s or %s (the denominator) missing" % (key, total_key)
    if sorted(cls) != sorted(classes):
        return "%s keys are not the closed set" % key
    s = sum(int(v) for v in cls.values())
    if s != total:
        return "%s sum %d != %s %d" % (key, s, total_key, total)
    return None


def ruleprobe(rec):
    why = read_only(rec) or need(rec, ["claim", "assets", "excluded_by_type", "deterministic", "variants"])
    if why:
        return fail("RULEPROBE", why)
    if rec["claim"] not in CLAIMS:
        return fail("RULEPROBE", "claim not in the closed set")
    if rec["deterministic"] is not True:
        return fail("RULEPROBE", "two runs were not byte-equal")
    if not isinstance(rec["assets"], list) or not rec["assets"]:
        return fail("RULEPROBE", "assets empty")
    for a in rec["assets"]:
        for k in ("asset_name", "date", "price", "distinct_trade_ids"):
            if k not in a:
                return fail("RULEPROBE", "asset row lacks %s" % k)
        if not isinstance(a["distinct_trade_ids"], list):
            return fail("RULEPROBE", "distinct_trade_ids must be a list")
    if not isinstance(rec["excluded_by_type"], dict) or not rec["excluded_by_type"]:
        return fail("RULEPROBE", "excluded_by_type empty")
    if sorted(rec["variants"]) != ["A_trades_only", "B_plus_reinvestment"]:
        return fail("RULEPROBE", "variants must be exactly A_trades_only and B_plus_reinvestment")
    print("RULEPROBE record ok assets=%d deterministic=true excluded_types=%d"
          % (len(rec["assets"]), len(rec["excluded_by_type"])))
    return 0


def replay(rec):
    why = read_only(rec) or need(rec, ["claim", "window", "classes", "served_rows", "served_write", "deterministic",
                                       "list_file", "variants", "no_trade_policy"])
    if why:
        return fail("REPLAY", why)
    if rec["claim"] not in CLAIMS:
        return fail("REPLAY", "claim not in the closed set")
    if rec["served_write"] is not False:
        return fail("REPLAY", "served_write must be false")
    if rec["deterministic"] is not True:
        return fail("REPLAY", "two runs were not byte-equal")
    why = partition(rec, "classes", REPLAY_CLASSES, "served_rows")
    if why:
        return fail("REPLAY", why)
    for v in ("A_trades_only", "B_plus_reinvestment"):
        if v not in rec["variants"]:
            return fail("REPLAY", "variant %s missing" % v)
    c = rec["classes"]
    print("REPLAY record ok served=%d changed=%d unchanged=%d deterministic=true"
          % (rec["served_rows"], c["CHANGED"] + c["NOW_CARRY_FORWARD"], c["UNCHANGED"]))
    return 0


def census(rec):
    why = read_only(rec) or need(rec, ["claim", "objects_total", "objects_read", "lots_total", "classes", "listed_untickered",
                                       "extract_file", "extract_sha256", "by_entity_class"])
    if why:
        return fail("CENSUS", why)
    if rec["claim"] not in CLAIMS:
        return fail("CENSUS", "claim not in the closed set")
    if not isinstance(rec["objects_total"], int) or rec["objects_read"] > rec["objects_total"] or rec["objects_read"] <= 0:
        return fail("CENSUS", "objects_read must be positive and not exceed objects_total")
    why = partition(rec, "classes", CENSUS_CLASSES, "lots_total")
    if why:
        return fail("CENSUS", why)
    lu = rec["listed_untickered"]
    if not isinstance(lu, dict) or "count" not in lu or "assets" not in lu:
        return fail("CENSUS", "listed_untickered needs count and assets")
    if not re.fullmatch(r"[0-9a-f]{64}", str(rec["extract_sha256"])):
        return fail("CENSUS", "extract_sha256 is not a sha256")
    print("CENSUS record ok objects=%d lots=%d off_canonical=%d listed_untickered=%d"
          % (rec["objects_read"], rec["lots_total"], rec["classes"]["PRICED_OFF_NO_CANONICAL"], lu["count"]))
    return 0


def trace2(rec):
    why = need(rec, ["asset_name", "date", "served_price", "followed_source", "followed_price", "follows_served",
                     "trade_ids", "match", "daily_row", "canonical_row"])
    if why:
        return fail("TRACE2", why)
    if rec["followed_source"] not in ("canonical", "daily"):
        return fail("TRACE2", "followed_source must be canonical or daily")
    if rec["follows_served"] is not True:
        return fail("TRACE2", "the trace does not follow the served value")
    if not isinstance(rec["match"], bool) or not isinstance(rec["trade_ids"], list):
        return fail("TRACE2", "match must be boolean and trade_ids a list")
    print("TRACE2 record ok followed=%s trades=%d match=%s follows_served=true"
          % (rec["followed_source"], len(rec["trade_ids"]), str(rec["match"]).lower()))
    return 0


def cause(rec):
    why = read_only(rec) or need(rec, ["claim", "dates", "rerun", "behind_objects"])
    if why:
        return fail("CAUSE", why)
    if rec["claim"] not in CLAIMS:
        return fail("CAUSE", "claim not in the closed set")
    if rec["rerun"] is not False:
        return fail("CAUSE", "rerun must be false")
    ds = rec["dates"]
    if not isinstance(ds, list) or not ds:
        return fail("CAUSE", "dates empty")
    undet = 0
    for d in ds:
        if "date" not in d or d.get("class") not in CAUSE_CLASSES or not d.get("evidence"):
            return fail("CAUSE", "a date row lacks date, a closed-set class or evidence")
        if d["class"] == "NOT_DETERMINED":
            undet += 1
    b = rec["behind_objects"]
    if not isinstance(b, dict) or not b.get("producer") or not b.get("derivation"):
        return fail("CAUSE", "behind_objects needs producer and derivation")
    print("CAUSE record ok dates=%d determined=%d undetermined=%d producer=%s"
          % (len(ds), len(ds) - undet, undet, re.sub(r"\s+", "_", str(b["producer"]))[:40]))
    return 0


def lotproof(rec):
    why = need(rec, ["claim", "legacy_bytes_equal", "lot_rows", "keyed_on_lot", "lot_key", "address", "address_from_builder",
                     "new_columns_in_legacy"])
    if why:
        return fail("LOTPROOF", why)
    if rec["claim"] not in CLAIMS:
        return fail("LOTPROOF", "claim not in the closed set")
    if rec["legacy_bytes_equal"] is not True:
        return fail("LOTPROOF", "the legacy output is not byte-unchanged")
    if not isinstance(rec["lot_rows"], int) or rec["lot_rows"] < 1:
        return fail("LOTPROOF", "no lot rows")
    if rec["keyed_on_lot"] is not True or sorted(rec["lot_key"]) != sorted(["account_id", "asset_id", "open_date", "unit_cost"]):
        return fail("LOTPROOF", "the lot key is not (account_id, asset_id, open_date, unit_cost)")
    if rec["address_from_builder"] is not True or not str(rec["address"]).startswith("s3://"):
        return fail("LOTPROOF", "the address is not builder output")
    if rec["new_columns_in_legacy"]:
        return fail("LOTPROOF", "Units or Cost Basis leaked into the legacy table")
    print("LOTPROOF record ok legacy_equal=true lots=%d keyed_on_lot=true" % rec["lot_rows"])
    return 0


def packet(rec):
    why = need(rec, ["claim", "price_changes", "assets_changed", "dollar_effect_latest_snapshot", "snapshot_date", "readers",
                     "before_after_file", "served_write"])
    if why:
        return fail("PACKET", why)
    if rec["claim"] not in CLAIMS:
        return fail("PACKET", "claim not in the closed set")
    if rec["served_write"] is not False:
        return fail("PACKET", "served_write must be false")
    if not isinstance(rec["readers"], list) or len(rec["readers"]) < 4:
        return fail("PACKET", "fewer than four downstream readers named")
    for r in rec["readers"]:
        if "reader" not in r or r.get("class") not in ("client-facing", "internal", "unknown"):
            return fail("PACKET", "a reader lacks its name or a class in {client-facing, internal, unknown}")
    print("PACKET record ok changed=%d assets=%d readers=%d served_write=false"
          % (rec["price_changes"], rec["assets_changed"], len(rec["readers"])))
    return 0


def thread2(rec):
    if "account_id" in rec or "advisor_name" in rec or "client_name" in rec:
        return fail("THREAD2", "a raw account id or a name is present")
    why = need(rec, ["claim", "served_object_key", "as_of_date", "account_ref", "asset_name", "ticker", "served_price",
                     "rule_id", "trade_ids", "distinct_trade_ids", "recomputed_price", "recompute_equals_served",
                     "unlisted_sources_checked", "tie_order_applied", "client_entity_class", "one_served_price"])
    if why:
        return fail("THREAD2", why)
    if rec["claim"] not in CLAIMS:
        return fail("THREAD2", "claim not in the closed set")
    if rec["ticker"] not in (None, "", "UNKNOWN"):
        return fail("THREAD2", "the holding carries a served ticker")
    if rec["rule_id"] != "R1":
        return fail("THREAD2", "rule_id must be R1")
    ids = rec["trade_ids"]
    if not isinstance(ids, list) or not ids or rec["distinct_trade_ids"] != len(set(ids)):
        return fail("THREAD2", "trade_ids empty or distinct_trade_ids disagrees")
    if not isinstance(rec["unlisted_sources_checked"], list) or len(rec["unlisted_sources_checked"]) < 3:
        return fail("THREAD2", "fewer than three ticker sources checked")
    if rec["client_entity_class"] != "normal" or rec["one_served_price"] is not True:
        return fail("THREAD2", "client_entity_class must be normal and one_served_price true")
    if not re.fullmatch(r"[0-9a-f]{12}", str(rec["account_ref"])):
        return fail("THREAD2", "account_ref is not a 12-hex digest")
    print("THREAD2 record ok rule=R1 distinct_trades=%d sources_checked=%d equal=%s"
          % (rec["distinct_trade_ids"], len(rec["unlisted_sources_checked"]),
             str(rec["recompute_equals_served"]).lower()))
    return 0


CMDS = {"ruleprobe": ruleprobe, "replay": replay, "census": census, "trace2": trace2, "cause": cause,
        "lotproof": lotproof, "packet": packet, "thread2": thread2}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=sorted(CMDS))
    ap.add_argument("--file", required=True)
    a = ap.parse_args()
    try:
        with open(a.file, "r", encoding="utf-8") as fh:
            rec = json.load(fh)
    except Exception as e:  # noqa: BLE001 -- the grader reports, never raises
        return fail(a.cmd.upper(), "unreadable record: %s" % type(e).__name__)
    return CMDS[a.cmd](rec)


if __name__ == "__main__":
    sys.exit(main())
