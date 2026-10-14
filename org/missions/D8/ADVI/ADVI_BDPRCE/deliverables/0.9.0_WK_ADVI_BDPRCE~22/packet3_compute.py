"""BP-c-3 (0.9.0_WK_ADVI_BDPRCE~22): the FWD-7 packet numbers on the R1.3 list. READ-ONLY.

Reads: the R1.3 list (BEFORE_AFTER3.csv, ESTIMATED_ROWS3.csv, REPLAY3.json, UNIT_MAP.csv) from the merged
deliverables of 0.9.0_WK_ADVI_BDPRCE~21, and the lot extract by its absolute path (sha256 checked).
Writes: PACKET3.json, MOVERS3.csv, and prints every figure the page quotes with its denominator.
No S3 call, no served write, no producer run. Outputs ASCII only (non-ASCII names are escaped).

Run at its own path:  python org/.../0.9.0_WK_ADVI_BDPRCE~22/packet3_compute.py
"""
import collections
import csv
import datetime
import hashlib
import json
import os
import sys
from decimal import Decimal as D, getcontext

getcontext().prec = 80

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, *([os.pardir] * 7)))
R21 = os.path.join(ROOT, "org/missions/D8/ADVI/ADVI_BDPRCE/deliverables/0.9.0_WK_ADVI_BDPRCE~21")
EXTRACT = "C:/dev/wk-bdprce-r2-7-data/lot_extract.csv"
EXTRACT_SHA = "e7e618d76516c8b7977179aefb3f77ce4fc13c17fbcf1dbeb92001a6e0a2b50b"
BA_SHA = "0dfcd23dd606db5fd6283d6564b09cf8e81e81fdb2138e7e5d60e7ea12bd937a"
EST_SHA = "8c07ccc1167c816e74b25349bb2532742fa71199cbde372170b01535527c94dc"
UNIT_SHA = "c47ce738cd1ca34b132d785704a210f5528accacf3dbe4d02c9309c50428435e"
MOVERS_N = 25


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        h.update(fh.read())
    return h.hexdigest()


def cents(d):
    """Presentation only: the CSV shows each mover's effect to the cent; totals stay exact."""
    return str(D(d).quantize(D("0.01")))


def ascii_out(s):
    """Escape any non-ASCII character so the committed text stays ASCII."""
    return "".join(ch if ord(ch) < 128 else "\\u%04x" % ord(ch) for ch in str(s))


def main():
    # ---- inputs and their hashes -------------------------------------------------------------
    ext_sha = sha256(EXTRACT)
    if ext_sha != EXTRACT_SHA:
        print("BLOCKED: extract sha256 %s != %s" % (ext_sha, EXTRACT_SHA))
        return 2
    ba_path = os.path.join(R21, "BEFORE_AFTER3.csv")
    est_path = os.path.join(R21, "ESTIMATED_ROWS3.csv")
    unit_path = os.path.join(R21, "UNIT_MAP.csv")
    for p, want in ((ba_path, BA_SHA), (est_path, EST_SHA), (unit_path, UNIT_SHA)):
        got = sha256(p)
        print("input %s sha256 %s match=%s" % (os.path.basename(p), got, got == want))
        if got != want:
            print("BLOCKED: input hash mismatch")
            return 2
    print("extract %s sha256 %s match=True" % (EXTRACT, ext_sha))
    with open(EXTRACT, "r", encoding="utf-8", newline="") as fh:
        lots = list(csv.DictReader(fh))
    with open(ba_path, "r", encoding="utf-8", newline="") as fh:
        ba = list(csv.DictReader(fh))
    with open(est_path, "r", encoding="utf-8", newline="") as fh:
        est = list(csv.DictReader(fh))
    replay = json.load(open(os.path.join(R21, "REPLAY3.json"), encoding="utf-8"))

    # ---- 1. the latest snapshot ----------------------------------------------------------------
    total_lots = len(lots)
    dates = collections.Counter(r["data_as_of"] for r in lots)
    snap, n_snap = dates.most_common(1)[0]
    assert n_snap * 2 > total_lots, "no majority snapshot"
    snap_lots = [r for r in lots if r["data_as_of"] == snap]
    share = n_snap / total_lots
    print("SNAPSHOT date=%s lots=%d of %d share=%.6f (%d/%d) outside=%d"
          % (snap, n_snap, total_lots, share, n_snap, total_lots, total_lots - n_snap))
    by_name = collections.defaultdict(list)
    for r in snap_lots:
        by_name[r["asset_name"]].append(r)
    # 34 lots of the extract carry the text nan for current_price and market_value (the census excluded
    # the same 34 from its identity check: 198,295 - 34 = 198,261). None sits in a touched asset.
    nan_lots = [r for r in snap_lots if not D(r["current_price"]).is_finite()]
    priced_snap = [r for r in snap_lots if D(r["current_price"]).is_finite()]
    print("UNPRICED snapshot lots (current_price nan)=%d" % len(nan_lots))
    snap_value = sum(D(r["quantity"]) * D(r["current_price"]) for r in priced_snap)

    # ---- 2. the dollar effect on the BEFORE_AFTER3 rows of the snapshot date -------------------
    touched = [r for r in ba if r["date"] == snap and r["class"] in ("CHANGED", "NOW_CARRY_FORWARD")]
    rows = []
    mv_off_all = 0
    for r in touched:
        name = r["asset_name"]
        old = D(r["old_price"])
        new = D(r["new_price"])
        lots_r = by_name.get(name, [])
        eff_q = D(0)
        eff_lot = D(0)
        eff_mv = D(0)
        eff_mv_lot = D(0)
        value = D(0)
        for lot in lots_r:
            q = D(lot["quantity"])
            cp = D(lot["current_price"])
            mv = D(lot["market_value"])
            eff_q += (new - old) * q
            eff_lot += (new - cp) * q
            eff_mv += mv * (new / old - 1)
            if cp != 0:
                eff_mv_lot += mv * (new / cp - 1)
            value += q * cp
        rows.append({
            "r": r, "name": name, "old": old, "new": new, "lots": lots_r,
            "moved": new != old, "eff_q": eff_q, "eff_lot": eff_lot, "eff_mv": eff_mv,
            "eff_mv_lot": eff_mv_lot, "value": value,
        })
    print("UNPRICED snapshot lots in touched assets=%d" % sum(1 for r in nan_lots if r["asset_name"] in set(x["name"] for x in rows)))
    moved_rows = [x for x in rows if x["moved"]]
    not_moved_rows = [x for x in rows if not x["moved"]]
    lots_touched = sum(len(x["lots"]) for x in rows)
    lots_moved_rows = sum(len(x["lots"]) for x in moved_rows)
    names_moved = sorted(set(x["name"] for x in moved_rows))
    names_touched = sorted(set(x["name"] for x in rows))
    with_lots_moved = [x for x in moved_rows if x["lots"]]
    total_eff_q = sum((x["eff_q"] for x in rows), D(0))
    total_eff_lot = sum((x["eff_lot"] for x in rows), D(0))
    total_eff_mv = sum((x["eff_mv"] for x in rows), D(0))
    total_eff_mv_lot = sum((x["eff_mv_lot"] for x in rows), D(0))
    touched_value = sum((x["value"] for x in rows), D(0))
    print("TOUCHED rows(snapshot, CHANGED|NOW_CARRY_FORWARD)=%d (CHANGED=%d NOW_CARRY_FORWARD=%d)"
          % (len(rows), sum(1 for x in rows if x["r"]["class"] == "CHANGED"),
             sum(1 for x in rows if x["r"]["class"] == "NOW_CARRY_FORWARD")))
    print("MOVED rows (new != served old)=%d  TOUCHED-NOT-MOVED rows (new == old)=%d"
          % (len(moved_rows), len(not_moved_rows)))
    print("  moved rows with >=1 snapshot lot=%d ; moved rows with no snapshot lot=%d (names: %s)"
          % (len(with_lots_moved), len(moved_rows) - len(with_lots_moved),
             "; ".join(ascii_out(x["name"]) for x in moved_rows if not x["lots"])))
    print("  touched-not-moved rows: %s" % ("; ".join("%s (%s, lots=%d)" % (ascii_out(x["name"]), x["r"]["class"], len(x["lots"])) for x in not_moved_rows) or "none"))
    print("  distinct assets moved=%d touched=%d ; lots in touched assets=%d (of which in moved rows=%d)"
          % (len(names_moved), len(names_touched), lots_touched, lots_moved_rows))
    print("EFFECT qty*price basis (order formula, old=served old_price) total=%s" % total_eff_q)
    print("EFFECT lot-basis (new - lot current_price) total=%s" % total_eff_lot)
    print("EFFECT served-market_value basis (mv*(new/old-1)) total=%s" % total_eff_mv)
    print("EFFECT lot market_value basis (mv*(new/lot_price-1)) total=%s" % total_eff_mv_lot)
    print("VALUE of priced snapshot lots qty*current_price=%s over %d priced lots; touched-asset lots value=%s share=%s"
          % (snap_value, len(priced_snap), touched_value, (touched_value / snap_value)))

    # ---- lot price vs served price (the basis question) ----------------------------------------
    lot_eq_old = 0
    lot_ne_old = 0
    for x in rows:
        for lot in x["lots"]:
            if D(lot["current_price"]) == x["old"]:
                lot_eq_old += 1
            else:
                lot_ne_old += 1
    print("LOT PRICE BASIS: touched-asset snapshot lots whose current_price == served old_price=%d ; != =%d (of %d)"
          % (lot_eq_old, lot_ne_old, lot_eq_old + lot_ne_old))

    # ---- market_value identity over all snapshot lots (census tolerance) -------------------------
    off = []
    for lot in priced_snap:
        q = D(lot["quantity"])
        cp = D(lot["current_price"])
        mv = D(lot["market_value"])
        tol = max(D("0.01"), D("0.000001") * abs(mv))
        if abs(mv - q * cp) > tol:
            off.append(lot)
    mv_off_all = len(off)
    off_touched = [lot for lot in off if lot["asset_name"] in by_name and any(x["name"] == lot["asset_name"] for x in rows)]
    eff_off_q = D(0)
    eff_off_mv = D(0)
    for x in rows:
        offs = set(id(lt) for lt in off)
        for lot in x["lots"]:
            if id(lot) in offs:
                q = D(lot["quantity"])
                eff_off_q += (x["new"] - x["old"]) * q
                eff_off_mv += D(lot["market_value"]) * (x["new"] / x["old"] - 1)
    print("MV IDENTITY snapshot lots with market_value != quantity*current_price: %d of %d checkable (%d unpriced excluded)"
          % (mv_off_all, len(priced_snap), len(nan_lots)))
    print("  of which in touched assets: %d ; effect on those lots, qty basis=%s ; served mv basis=%s"
          % (len(off_touched), eff_off_q, eff_off_mv))

    # ---- movers ---------------------------------------------------------------------------------
    ranked = sorted(rows, key=lambda x: (-abs(x["eff_q"]), x["name"]))
    movers = ranked[:MOVERS_N]
    par_flag_rows = [x for x in rows if "scale_100x" in x["r"]["flags"]]
    par_in_movers = sum(1 for x in movers if "scale_100x" in x["r"]["flags"])
    movers_value = sum((x["value"] for x in movers), D(0))
    movers_eff = sum((x["eff_q"] for x in movers), D(0))
    print("MOVERS top %d by |effect qty basis|: effect sum=%s ; value of their lots=%s share of snapshot value=%s"
          % (MOVERS_N, movers_eff, movers_value, movers_value / snap_value))
    print("  par-quoted (scale_100x) rows on the snapshot date=%d ; in movers=%d" % (len(par_flag_rows), par_in_movers))

    # ---- BEFORE_AFTER3 classes, withheld rows ------------------------------------------------------
    nr_all = collections.Counter(r["reason"] for r in ba if r["class"] == "NOT_RECOMPUTABLE")
    nr_snap = collections.Counter(r["reason"] for r in ba if r["class"] == "NOT_RECOMPUTABLE" and r["date"] == snap)
    snap_all_rows = [r for r in ba if r["date"] == snap]
    print("NOT_RECOMPUTABLE window (%d): %s" % (sum(nr_all.values()), dict(nr_all)))
    print("NOT_RECOMPUTABLE snapshot (%d of %d snapshot-date rows): %s"
          % (sum(nr_snap.values()), len(snap_all_rows), dict(nr_snap)))
    print("BA classes window: %s" % dict(collections.Counter(r["class"] for r in ba)))
    print("BA classes snapshot: %s" % dict(collections.Counter(r["class"] for r in snap_all_rows)))
    print("withheld FI trade rows=%s assets=%s (REPLAY3.json)" % (replay["withheld_fi_trade_rows"], replay["withheld_assets_count"]))

    # ---- snapshot-date interpolated rows (disclosed, outside the order formula) -----------------
    est_snap = [e for e in est if e["date"] == snap]
    est_snap_fate = collections.Counter(e["fate"] for e in est_snap)
    est_snap_held = [e for e in est_snap if e["fate"] == "last_traded_date" and D(e["r1_price"]) != D(e["canonical_price"])]
    print("INTERPOLATED on snapshot date rows=%d fates=%s ; last_traded rows whose R1 price differs from canonical=%d"
          % (len(est_snap), dict(est_snap_fate), len(est_snap_held)))
    est_snap_eff = D(0)
    est_snap_lots = 0
    for e in est_snap_held:
        for lot in by_name.get(e["asset_name"], []):
            est_snap_eff += (D(e["r1_price"]) - D(e["canonical_price"])) * D(lot["quantity"])
            est_snap_lots += 1
    print("  supplementary (NOT in the order formula): effect on snapshot lots of those assets=%s over %d lots"
          % (est_snap_eff, est_snap_lots))

    # ---- interpolated fates over the window ----------------------------------------------------------
    fates = collections.Counter(e["fate"] for e in est)
    f_rows = len(est)
    print("INTERPOLATED window rows=%d fates=%s (trade_price=%d last_traded_date=%d unresolved=%d)"
          % (f_rows, dict(fates), fates.get("trade_price", 0), fates.get("last_traded_date", 0), fates.get("unresolved", 0)))

    # ---- write PACKET3.json and MOVERS3.csv --------------------------------------------------------
    mv_path = os.path.join(HERE, "MOVERS3.csv")
    with open(mv_path, "w", encoding="ascii", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["rank", "asset_name", "date", "class", "served_old_price", "new_price", "distinct_trades",
                    "snapshot_lots", "quantity", "effect_qty_basis", "effect_lot_basis", "effect_served_mv_basis",
                    "observation_date", "reason"])
        for i, x in enumerate(movers, 1):
            r = x["r"]
            qty = sum((D(lt["quantity"]) for lt in x["lots"]), D(0))
            w.writerow([i, ascii_out(x["name"]), r["date"], r["class"], r["old_price"], r["new_price"],
                        r["distinct_trades"], len(x["lots"]), "%s" % qty, cents(x["eff_q"]), cents(x["eff_lot"]),
                        cents(x["eff_mv"]), r["observation_date"], r["reason"]])
    print("WROTE %s rows=%d" % (mv_path, len(movers)))

    # Named readers are written by hand into PACKET3.json (readers.json) by the caller, see below.
    readers_path = os.path.join(HERE, "readers3.json")
    readers = json.load(open(readers_path, encoding="utf-8")) if os.path.exists(readers_path) else []

    rec = {
        "order": "BP-c-3",
        "read_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "claim": "measured",
        "calls": [
            "read %s sha256 %s (equal to extract_sha256 in CENSUS.json)" % (EXTRACT, ext_sha),
            "read %s sha256 %s (equal to REPLAY3.json list_sha256)" % ("BEFORE_AFTER3.csv", BA_SHA),
            "read %s sha256 %s" % ("ESTIMATED_ROWS3.csv", EST_SHA),
            "read %s sha256 %s" % ("UNIT_MAP.csv", UNIT_SHA),
            "read REPLAY3.json, REPLAY3.md (0.9.0_WK_ADVI_BDPRCE~21)",
            "python packet3_compute.py (local arithmetic only; no S3 call; no served write)",
            "read ADVI_BDPRCE_PRD.md (CONTRACTS, Not in scope, DEC-6, DEC-7); MDPF_SECCLASS_PRD.md:744; IRPT_DASHBD_PRD.md:1",
            "grep (native, worktree-pathed) of portal/src/pages/InvestorReporting, infra/aws/lambda/exec-summary-generator, data/inf/scripts/gold, data/black_diamond/scripts/gold/B_03.account_gains.py",
        ],
        "amendment": "R1.3",
        "snapshot_date": snap,
        "snapshot_share": share,
        "lots_outside_snapshot": total_lots - n_snap,
        "snapshot_lots": n_snap,
        "snapshot_lots_priced": len(priced_snap),
        "total_lots": total_lots,
        "price_changes": len(moved_rows),
        "assets_changed": len(names_moved),
        "touched_rows": len(rows),
        "touched_not_moved": len(not_moved_rows),
        "lots_touched": lots_touched,
        "dollar_effect_latest_snapshot": float(total_eff_q),
        "dollar_effect_basis": "sum over snapshot lots of (new_price - served old_price) * quantity",
        "dollar_effect_lot_basis": float(total_eff_lot),
        "dollar_effect_served_mv_basis": float(total_eff_mv),
        "snapshot_value_qty_price": float(snap_value),
        "touched_value_qty_price": float(touched_value),
        "movers_value_share": float(movers_value / snap_value),
        "market_value_identity": {
            "lots_off": mv_off_all,
            "lots_checked": len(priced_snap),
            "lots_unpriced_nan": len(nan_lots),
            "lots_off_in_touched_assets": len(off_touched),
            "effect_on_quantity_basis": float(eff_off_q),
            "effect_on_served_market_value_basis": float(eff_off_mv),
            "tolerance": "max(0.01, 1e-6*abs(market_value)) (census tolerance)",
        },
        "movers_file": "MOVERS3.csv",
        "before_after_file": "BEFORE_AFTER3.csv",
        "par_rows_in_movers": par_in_movers,
        "interpolated_fate": {
            "rows": f_rows,
            "trade_price": fates.get("trade_price", 0),
            "last_traded_date": fates.get("last_traded_date", 0),
            "unresolved": fates.get("unresolved", 0),
        },
        "readers": readers,
        "plain_page": "PACKET3.md",
        "served_write": False,
        "held_unit_rows": 0,
        "unit_changed_rows": replay.get("unit_changed_rows", None),
        "unit_withheld_rows_window": replay.get("unit_withheld_rows"),
    }
    with open(os.path.join(HERE, "PACKET3.json"), "w", encoding="ascii", newline="\n") as fh:
        json.dump(rec, fh, indent=1, ensure_ascii=True)
        fh.write("\n")
    print("WROTE PACKET3.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
