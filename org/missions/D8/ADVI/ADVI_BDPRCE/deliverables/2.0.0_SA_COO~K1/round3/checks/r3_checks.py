"""ADVI_BDPRCE round 3: record-shape graders, issuer 2.0.0_SA_COO~K1.

  ruleprobe2 --file <RULE_PROBE2.json>   BP-c-1: R1 Amendment 1 run over real partitions
  replay2    --file <REPLAY2.json>       BP-c-2: the replay re-run on the amended rule
  packet2    --file <PACKET2.json>       BP-c-3: the FWD-7 packet on the amended list
  cap        --file <CAP.json>           BP-c-4: is 500,000 an export cap
  lotproof2  --file <LOT_PROOF2.json>    BP-c-5: the lot-key fixture proof, relationship id in the key
  sentinel   --file <SENTINEL.json>      BP-c-6: the sentinel line and the Monday/Tuesday export
  offcanon   --file <OFFCANON.json>      BP-c-7: the source of the lots priced off no canonical row
  ruleprobe3 / replay3 / packet3         Amendment 3 (R1.3): the same three records, plus the served-unit map and unit_changed 0

Each prints one last line `<NAME> record ok ...` or `<NAME> record FAIL <why>`; exit 0 on ok. The graders prove shape,
read-only discipline and arithmetic; they do not prove a measurement is right (the issuer re-reads cited objects).
ASCII only. Never edit this file.
"""
import argparse
import contextlib
import io
import json
import re
import sys

WRITE_VERBS = re.compile(
    r"\b(put-object|delete-object|delete-objects|copy-object|put-bucket|update-function|invoke|put-rule|put-targets|"
    r"start-execution|s3 cp [^ ]+ s3://|s3 rm|s3 sync [^ ]+ s3://|terraform apply|start-task|run-task)\b")
CLAIMS = {"measured", "inferred", "held", "absent"}
REPLAY_CLASSES = ["UNCHANGED", "CHANGED", "NOW_CARRY_FORWARD", "NOT_RECOMPUTABLE"]
OFFCANON_CLASSES = ["EQUALS_OLDER_CANONICAL_VERSION", "EQUALS_DAILY_FILE_ROW", "EQUALS_NAMED_OTHER_SOURCE", "UNEXPLAINED"]
CAP_VERDICTS = ["CAP", "NOT_A_CAP", "NOT_DETERMINED"]
SENTINEL_CAUSES = ["EXPORT_WINDOW_RULE", "VENDOR_EMPTY", "RUNNER_DEFECT", "NOT_DETERMINED"]


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


def head(rec, name):
    why = read_only(rec) or need(rec, ["claim"])
    if why:
        return why
    if rec["claim"] not in CLAIMS:
        return "claim not in the closed set"
    return None


def ruleprobe2(rec, amend="R1.2", label="RULEPROBE2"):
    why = head(rec, label) or need(rec, ["amendment", "deterministic", "assets", "reinvestment_in", "transfer_in_out",
                                              "par_quoted", "types_seen"])
    if why:
        return fail(label, why)
    if rec["amendment"] != amend or rec["deterministic"] is not True:
        return fail(label, "amendment must be %s" % amend + " and the probe deterministic")
    if rec["reinvestment_in"] is not True or rec["transfer_in_out"] is not True:
        return fail(label, "reinvestment buys must be in and Transfer In out")
    pq = rec["par_quoted"]
    for k in ("class_field", "assets_scaled", "withheld_disagreement", "unit_scale_rows_unchanged", "per_unit_left",
              "withheld_ratios"):
        if not isinstance(pq, dict) or k not in pq:
            return fail(label, "par_quoted lacks %s" % k)
    if not isinstance(rec["assets"], list) or not rec["assets"]:
        return fail(label, "assets empty")
    for a in rec["assets"]:
        for k in ("asset_name", "date", "price", "kind", "distinct_trade_ids"):
            if k not in a:
                return fail(label, "asset row lacks %s" % k)
    print(label + " record ok amendment=%s assets=%d par_scaled=%d withheld=%d"
          % (amend, len(rec["assets"]), int(pq["assets_scaled"]), int(pq["withheld_disagreement"])))
    return 0


def replay2(rec, amend="R1.2", label="REPLAY2"):
    why = head(rec, label) or need(rec, ["amendment", "window", "served_rows", "classes", "served_write", "deterministic",
                                           "list_file", "par_quoted_rows", "par_rows_unchanged", "transfer_in_carry_forwards",
                                           "carry_forwards_with_date", "interpolated", "lookback_keying", "list_sha256"])
    if why:
        return fail(label, why)
    if rec["amendment"] != amend or rec["served_write"] is not False or rec["deterministic"] is not True:
        return fail(label, "amendment must be %s" % amend + ", served_write false and the replay deterministic")
    why = partition(rec, "classes", REPLAY_CLASSES, "served_rows")
    if why:
        return fail(label, why)
    if rec["par_rows_unchanged"] != rec["par_quoted_rows"]:
        return fail(label, "par-quoted rows are not all UNCHANGED (%s of %s)" % (rec["par_rows_unchanged"], rec["par_quoted_rows"]))
    ncf = rec["classes"]["NOW_CARRY_FORWARD"]
    if rec["carry_forwards_with_date"] != ncf:
        return fail(label, "carry-forwards with an observation date %s != NOW_CARRY_FORWARD %s" % (rec["carry_forwards_with_date"], ncf))
    it = rec["interpolated"]
    for k in ("rows", "with_trade_price", "with_last_traded_date", "unresolved"):
        if not isinstance(it, dict) or k not in it:
            return fail(label, "interpolated lacks %s" % k)
    if int(it["with_trade_price"]) + int(it["with_last_traded_date"]) + int(it["unresolved"]) != int(it["rows"]):
        return fail(label, "interpolated fates do not sum to rows")
    lk = rec["lookback_keying"]
    if not isinstance(lk, dict) or lk.get("mode") not in ("trade_date_all_partitions", "limited") or not lk.get("statement"):
        return fail(label, "lookback_keying needs a mode in {trade_date_all_partitions, limited} and a statement")
    if not re.fullmatch(r"[0-9a-f]{64}", str(rec["list_sha256"])):
        return fail(label, "list_sha256 is not a sha256")
    c = rec["classes"]
    print(label + " record ok served=%d moved=%d unchanged=%d par_unchanged=%d deterministic=true"
          % (rec["served_rows"], c["CHANGED"] + c["NOW_CARRY_FORWARD"], c["UNCHANGED"], rec["par_rows_unchanged"]))
    return 0


def packet2(rec, amend="R1.2", label="PACKET2"):
    why = head(rec, label) or need(rec, ["amendment", "snapshot_date", "price_changes", "assets_changed", "lots_touched",
                                           "dollar_effect_latest_snapshot", "readers", "movers_file", "before_after_file",
                                           "served_write", "interpolated_fate", "par_rows_in_movers", "plain_page"])
    if why:
        return fail(label, why)
    if rec["amendment"] != amend or rec["served_write"] is not False:
        return fail(label, "amendment must be %s" % amend + " and served_write false")
    if rec["par_rows_in_movers"] != 0:
        return fail(label, "the par-quoted rows must not appear as movers")
    f = rec["interpolated_fate"]
    for k in ("rows", "trade_price", "last_traded_date", "unresolved"):
        if not isinstance(f, dict) or k not in f:
            return fail(label, "interpolated_fate lacks %s" % k)
    if int(f["trade_price"]) + int(f["last_traded_date"]) + int(f["unresolved"]) != int(f["rows"]):
        return fail(label, "interpolated fates do not sum to rows")
    rd = rec["readers"]
    if not isinstance(rd, list) or len(rd) < 4:
        return fail(label, "fewer than four downstream readers named")
    for r in rd:
        if "reader" not in r or r.get("class") not in ("client-facing", "internal", "unknown"):
            return fail(label, "a reader lacks its name or a class in {client-facing, internal, unknown}")
    print(label + " record ok changed=%d assets=%d readers=%d interpolated=%d served_write=false"
          % (rec["price_changes"], rec["assets_changed"], len(rd), int(f["rows"])))
    return 0


def cap(rec):
    why = head(rec, "CAP") or need(rec, ["days_checked", "rows_per_day", "days_at_500000", "paging_config", "verdict", "evidence",
                                       "second_window"])
    if why:
        return fail("CAP", why)
    rpd = rec["rows_per_day"]
    if not isinstance(rpd, dict) or len(rpd) != rec["days_checked"] or rec["days_checked"] < 10:
        return fail("CAP", "rows_per_day must hold one entry per day checked, at least 10")
    n500 = sum(1 for v in rpd.values() if int(v) == 500000)
    if n500 != rec["days_at_500000"]:
        return fail("CAP", "days_at_500000 %s != the count in rows_per_day %d" % (rec["days_at_500000"], n500))
    if rec["verdict"] not in CAP_VERDICTS:
        return fail("CAP", "verdict not in the closed set")
    if not rec["evidence"] or not rec["paging_config"]:
        return fail("CAP", "evidence and paging_config are required")
    sw = rec["second_window"]
    if not isinstance(sw, dict) or "dates" not in sw or "rows" not in sw:
        return fail("CAP", "second_window needs dates and rows")
    print("CAP record ok days=%d at_500000=%d verdict=%s" % (rec["days_checked"], n500, rec["verdict"]))
    return 0


def lotproof2(rec):
    why = need(rec, ["claim", "legacy_bytes_equal", "lot_rows", "rows_folded", "colliding_groups_differing", "keyed_on_lot",
                     "lot_key", "address", "address_from_builder", "new_columns_in_legacy", "key_basis"])
    if why:
        return fail("LOTPROOF2", why)
    if rec["claim"] not in CLAIMS:
        return fail("LOTPROOF2", "claim not in the closed set")
    if rec["legacy_bytes_equal"] is not True:
        return fail("LOTPROOF2", "the legacy output is not byte-unchanged")
    if rec["rows_folded"] != 0 or rec["colliding_groups_differing"] != 0:
        return fail("LOTPROOF2", "rows folded %s and differing colliding groups %s must both be zero"
                    % (rec["rows_folded"], rec["colliding_groups_differing"]))
    if rec["key_basis"] not in ("relationship_id", "export_lot_id"):
        return fail("LOTPROOF2", "key_basis must be relationship_id or export_lot_id")
    if rec["key_basis"] == "relationship_id" and "relationship_id" not in rec["lot_key"]:
        return fail("LOTPROOF2", "the lot key lacks relationship_id")
    if rec["keyed_on_lot"] is not True or rec["address_from_builder"] is not True or not str(rec["address"]).startswith("s3://"):
        return fail("LOTPROOF2", "keyed_on_lot and builder address are required")
    if rec["new_columns_in_legacy"]:
        return fail("LOTPROOF2", "Units or Cost Basis leaked into the legacy table")
    if not isinstance(rec["lot_rows"], int) or rec["lot_rows"] < 1:
        return fail("LOTPROOF2", "no lot rows")
    print("LOTPROOF2 record ok legacy_equal=true lots=%d folded=0 differing=0 key=%s" % (rec["lot_rows"], rec["key_basis"]))
    return 0


def sentinel(rec):
    why = head(rec, "SENTINEL") or need(rec, ["rerun", "deployed_fix", "runs_checked", "honest_lines", "dishonest_lines",
                                            "monday_tuesday", "window_rule", "cause"])
    if why:
        return fail("SENTINEL", why)
    if rec["rerun"] is not False:
        return fail("SENTINEL", "rerun must be false")
    df = rec["deployed_fix"]
    for k in ("deployed", "evidence"):
        if not isinstance(df, dict) or k not in df:
            return fail("SENTINEL", "deployed_fix lacks %s" % k)
    if not isinstance(rec["runs_checked"], int) or rec["runs_checked"] < 14:
        return fail("SENTINEL", "runs_checked must be at least 14")
    if int(rec["honest_lines"]) + int(rec["dishonest_lines"]) > rec["runs_checked"] * 3:
        return fail("SENTINEL", "line counts exceed any plausible total for the runs checked")
    mt = rec["monday_tuesday"]
    if not isinstance(mt, list) or not mt:
        return fail("SENTINEL", "monday_tuesday rows missing")
    for d in mt:
        for k in ("date", "weekday", "first_export_bytes", "sentinel_exists", "evidence"):
            if k not in d:
                return fail("SENTINEL", "a monday_tuesday row lacks %s" % k)
    if rec["cause"] not in SENTINEL_CAUSES:
        return fail("SENTINEL", "cause not in the closed set")
    if not rec["window_rule"]:
        return fail("SENTINEL", "window_rule (the export's date window, with file and line) is required")
    print("SENTINEL record ok runs=%d honest=%d dishonest=%d cause=%s deployed=%s"
          % (rec["runs_checked"], int(rec["honest_lines"]), int(rec["dishonest_lines"]), rec["cause"],
             str(df["deployed"]).lower()))
    return 0


def offcanon(rec):
    why = head(rec, "OFFCANON") or need(rec, ["lots_total", "classes", "exemplars", "extract_sha256", "named_sources"])
    if why:
        return fail("OFFCANON", why)
    why = partition(rec, "classes", OFFCANON_CLASSES, "lots_total")
    if why:
        return fail("OFFCANON", why)
    if not re.fullmatch(r"[0-9a-f]{64}", str(rec["extract_sha256"])):
        return fail("OFFCANON", "extract_sha256 is not a sha256")
    ex = rec["exemplars"]
    if not isinstance(ex, dict):
        return fail("OFFCANON", "exemplars must be an object keyed by class")
    for k, n in rec["classes"].items():
        if int(n) > 0 and k not in ex:
            return fail("OFFCANON", "class %s has rows but no exemplar" % k)
    if rec["classes"]["EQUALS_NAMED_OTHER_SOURCE"] and not rec["named_sources"]:
        return fail("OFFCANON", "EQUALS_NAMED_OTHER_SOURCE > 0 but named_sources empty")
    c = rec["classes"]
    print("OFFCANON record ok lots=%d older_canonical=%d daily=%d other=%d unexplained=%d"
          % (rec["lots_total"], c["EQUALS_OLDER_CANONICAL_VERSION"], c["EQUALS_DAILY_FILE_ROW"],
             c["EQUALS_NAMED_OTHER_SOURCE"], c["UNEXPLAINED"]))
    return 0



def _quiet(fn, *a, **k):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = fn(*a, **k)
    return rc, buf.getvalue().strip()


def _units(rec, label):
    su = rec.get("served_units")
    keys = ("assets", "per100", "per_unit", "unreadable")
    if not isinstance(su, dict) or any(k not in su for k in keys):
        return "served_units needs assets, per100, per_unit, unreadable"
    if int(su["per100"]) + int(su["per_unit"]) + int(su["unreadable"]) != int(su["assets"]) or int(su["assets"]) <= 0:
        return "served_units classes do not sum to assets"
    return None


def ruleprobe3(rec):
    rc, out = _quiet(ruleprobe2, rec, "R1.3", "RULEPROBE3")
    if rc:
        print(out)
        return rc
    why = _units(rec, "RULEPROBE3")
    if why:
        return fail("RULEPROBE3", why)
    if rec.get("unit_changed_assets") != 0:
        return fail("RULEPROBE3", "unit_changed_assets must be 0 (R1 changes values, never units)")
    su = rec["served_units"]
    print("RULEPROBE3 record ok amendment=R1.3 assets=%d per100=%d per_unit=%d unreadable=%d unit_changed=0"
          % (len(rec["assets"]), int(su["per100"]), int(su["per_unit"]), int(su["unreadable"])))
    return 0


def replay3(rec):
    rc, out = _quiet(replay2, rec, "R1.3", "REPLAY3")
    if rc:
        print(out)
        return rc
    why = _units(rec, "REPLAY3")
    if why:
        return fail("REPLAY3", why)
    if rec.get("unit_changed_rows") != 0:
        return fail("REPLAY3", "unit_changed_rows must be 0: no served row may change its unit")
    for k in ("unit_map_file", "unit_withheld_rows"):
        if k not in rec:
            return fail("REPLAY3", "lacks %s" % k)
    c = rec["classes"]
    print("REPLAY3 record ok served=%d moved=%d unchanged=%d unit_changed=0 unit_withheld=%d deterministic=true"
          % (rec["served_rows"], c["CHANGED"] + c["NOW_CARRY_FORWARD"], c["UNCHANGED"], int(rec["unit_withheld_rows"])))
    return 0


def packet3(rec):
    rc, out = _quiet(packet2, rec, "R1.3", "PACKET3")
    if rc:
        print(out)
        return rc
    if rec.get("held_unit_rows") != 0:
        return fail("PACKET3", "held_unit_rows must be 0: the unit is ruled, nothing is held out")
    print(out.replace("PACKET3 record ok", "PACKET3 record ok", 1))
    return 0


CMDS = {"ruleprobe2": ruleprobe2, "replay2": replay2, "packet2": packet2, "ruleprobe3": ruleprobe3,
        "replay3": replay3, "packet3": packet3, "cap": cap, "lotproof2": lotproof2,
        "sentinel": sentinel, "offcanon": offcanon}


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
