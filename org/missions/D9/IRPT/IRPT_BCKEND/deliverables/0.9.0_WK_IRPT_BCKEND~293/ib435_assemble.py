#!/usr/bin/env python3
"""IB-pr-435 phase C: assemble IB133-1_outside_anchor_coverage.json and IB133-1_OUTSIDE_ANCHOR_COVERAGE_READ.md from phase A (ib435_measure.py) and phase B
(ib435_stores.py).  Read only; counts and security identifiers only -- no account key, no balance, no single account's holding reaches the output.

    python -I ib435_assemble.py <phaseA.pkl> <phaseB.pkl> <out_dir> [<local_security_day_price.parquet>]
"""
from __future__ import annotations

import collections
import json
import pickle
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[7]
sys.path[:0] = [str(ROOT), str(ROOT / "lib"), str(ROOT / "data/assets/scripts/analysis"), str(ROOT / "data/assets/scripts/silver")]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import commonwealth_price_census as cpc  # noqa: E402
import ib435_stores as sto  # noqa: E402

ORDER = {"market_close": 0, "custodian_mark": 1}


def own(s):
    """The run-time own-firm key never reaches the output: store ids are written own-firm-<tail>."""
    return s.replace(cpc.OWN_FIRM, "own-firm") if isinstance(s, str) else s


def ascii_(s):
    return re.sub(r"[^\x20-\x7e]", "?", str(s or ""))


def pct(a, b):
    return round(100.0 * a / b, 2) if b else None


def cover_n(counts, share):
    total, run = sum(counts), 0
    for i, c in enumerate(counts, 1):
        run += c
        if run >= share * total:
            return i


def main():
    pa = pickle.load(open(sys.argv[1], "rb"))
    pb = pickle.load(open(sys.argv[2], "rb"))
    out_dir = Path(sys.argv[3])
    local_parquet = sys.argv[4] if len(sys.argv) > 4 else None
    stores = pb["stores"]
    opened = [s for s in stores if s.get("opened")]
    # needed dates per security, on the pre-cash-rule basis and for the three securities the cash rule adds
    need_pre = {c: set(pa["needed_dates"][c]) for c in pa["securities"]}
    need_add = {c: set(pa["needed_dates_added"][c]) for c in pa["securities_added"]}
    need_all = dict(need_pre)
    need_all.update(need_add)
    info = dict(pa["securities"])
    info.update(pa["securities_added"])

    # per store: found security-days restricted to the needed set
    found = {}
    for s in opened:
        found[s["id"]] = {c: set(s["found"].get(c, [])) & need_all[c] for c in need_all}
    kind_of = {s["id"]: s["price_kind"] for s in opened}

    def union(c, kinds):
        u = set()
        for sid, f in found.items():
            if kind_of[sid] in kinds:
                u |= f[c]
        return u

    def cls(n_found, n_need):
        return "every_needed_day" if n_found == n_need else "some_needed_days" if n_found else "no_needed_day"

    rows = []
    for c in sorted(need_pre, key=lambda c: (-info[c]["account_days"], c)):
        n = len(need_pre[c])
        per = {sid: len(f[c]) for sid, f in found.items()}
        allu, mkt = union(c, ("market_close", "custodian_mark")), union(c, ("market_close",))
        best = None
        if allu:
            best = sorted(per, key=lambda sid: (-per[sid], ORDER[kind_of[sid]], [s["id"] for s in stores].index(sid)))[0]
        rows.append({"security": c, "ticker": (info[c]["tickers"] or [None])[0], "tickers": info[c]["tickers"], "asset_name": ascii_(info[c]["name"]),
                     "account_days_carried": info[c]["account_days"], "coverage": cls(len(allu), n), "best_store": own(best) if best else None,
                     "best_store_price_kind": kind_of[best] if best else None, "needed_days": n, "found_days": len(allu), "share_found_percent": pct(len(allu), n),
                     "coverage_market_close_stores_only": cls(len(mkt), n), "found_days_market_close_stores_only": len(mkt)})
    counts = [r["account_days_carried"] for r in rows]
    total = sum(counts)
    assert total == pa["security_account_days_total"] and len(rows) == len(pa["securities"])
    cov_by = collections.Counter(r["coverage"] for r in rows)
    coverage_by_security = {k: cov_by[k] for k in ("every_needed_day", "some_needed_days", "no_needed_day")}

    # upper bounds: account-days that stop holding an OUTSIDE_ANCHOR row if every security whose close is in hand on EVERY needed day were gradeable
    def bound(struct, kinds, need_of):
        ok = {c for c in need_of if len(union(c, kinds)) == len(need_of[c])}
        stop = sum(n for (cs, other), n in struct.items() if cs <= ok)
        clean = sum(n for (cs, other), n in struct.items() if cs <= ok and not other)
        return {"account_days_no_longer_outside_anchor": stop, "of_which_holding_no_other_ungradeable_kind": clean, "securities_treated_as_gradeable": len(ok),
                "of_account_days_holding_an_outside_anchor_row": sum(struct.values())}
    pre_struct, cash_struct = pa["ad_structure_pre"], pa["ad_structure_cash"]
    mk, al = ("market_close",), ("market_close", "custodian_mark")
    ub_m, ub_a = bound(pre_struct, mk, need_pre), bound(pre_struct, al, need_pre)
    ub_m2, ub_a2 = bound(cash_struct, mk, need_all), bound(cash_struct, al, need_all)

    # stores
    st_out = []
    for s in stores:
        e = {"id": own(s["id"]), "legacy_key": own(s["legacy_key"]), "bucket_class": s["bucket_class"], "price_kind": s["price_kind"], "opened": bool(s.get("opened"))}
        if not s.get("opened"):
            e["not_opened_reason"] = s["not_opened_reason"]
            st_out.append(e)
            continue
        f = found[s["id"]]
        need_days = sum(len(need_pre[c]) for c in need_pre)
        got = sum(len(f[c]) for c in need_pre)
        e.update({"first_date": s["first_date"], "last_date": s["last_date"], "first_date_any": s["first_date_any"], "last_date_any": s["last_date_any"],
                  "window": ["2026-06-09", "2026-10-09"], "security_days_needed": need_days, "security_days_found": got,
                  "share_found_percent": pct(got, need_days), "securities_matched": {k: v for k, v in s["match_kind"].items()},
                  "securities_with_every_needed_day": sum(1 for c in need_pre if len(f[c]) == len(need_pre[c])),
                  "securities_with_some_needed_days": sum(1 for c in need_pre if 0 < len(f[c]) < len(need_pre[c])),
                  "rows_raw": s["rows_raw"], "rows_kept_for_the_wanted_keys": s["rows_kept"], "objects_read": s["objects_read"], "sources": s["sources"],
                  "key_columns": s["key_cols"], "format": s["fmt"]})
        st_out.append(e)
    notes = {
        "silver-canonical-prices": "ticker key only; price_kind custodian_mark as grouped by 2.0.0_SA_COO~C2 (msg 5084), though the store's own source column mixes yahoo_finance, linear_interpolation and transaction_observed; it ends 2026-06-09, so it holds the prior-day close of the first graded day and nothing after, and no security can have every needed day from it.",
        "gold-canonical-holdings": "the custodian's own mark on the held position (source bd_snapshot), the same value the source partition carries; NOT an independent close.",
        "rivalfunds-etfs-gold-security-market": "a market store; one CUSIP of the ranking has a close here, on one date.",
        "etfs-bbg-testpull-ticker-history": "Bloomberg-stored closes by ticker; ends 2026-08-24; a few tickers only.",
        "etfs-bbg-fund-daily": "36 daily CSVs of four ETFs (security column first token); none of the ranked tickers (the key declaration reaches it as declared; the first-token form was also checked: 0 overlap).",
        "portal-canon-return-daily-values": "87 index and currency series keyed by bbg_ticker (e.g. an index name); none of the ranked tickers (exact and first-token overlap both 0).",
    }
    for e in st_out:
        for t, n in notes.items():
            if e["id"].endswith(t):
                e["note"] = n

    # the LOCAL seventh store
    local = []
    if local_parquet and Path(local_parquet).is_file():
        import pyarrow.parquet as pq
        t = pq.read_table(local_parquet, columns=["cusip", "date", "price", "store"]).to_pandas()
        t["cusip"] = t["cusip"].astype(str).str.strip().str.upper()
        t = t[t["price"].notna() & (t["price"] > 0)]
        want = {cpc.norm_key(c): c for c in need_all}
        t = t[t["cusip"].isin(want)]
        t["day"] = t["date"].astype(str)
        by_c = {c: set(g["day"]) for c, g in t.groupby("cusip")}
        got_pre = sum(len(by_c.get(cpc.norm_key(c), set()) & need_pre[c]) for c in need_pre)
        n_pre = sum(len(v) for v in need_pre.values())
        in_win = t[(t["day"] >= "2026-06-09") & (t["day"] <= "2026-10-09")]
        orig = collections.Counter()
        for c in need_pre:
            sub = t[(t["cusip"] == cpc.norm_key(c)) & t["day"].isin(need_pre[c])]
            for sname in sub["store"]:
                orig[own(str(sname))] += 1
        every = sum(1 for c in need_pre if len(by_c.get(cpc.norm_key(c), set()) & need_pre[c]) == len(need_pre[c]))
        local.append({"id": "LOCAL-advi-cotbkf-after-security_day_price", "local_only": True, "served": False, "opened": True, "path": local_parquet.replace("\\", "/"),
                      "note": "ADVI_COTBKF's derived table (cusip, date, price, store), read-only, another worker's scratch; a DERIVED table whose rows are copies of closes from the "
                              "stores it names in its own `store` column, so it is not a seventh independent source; not served; not built here.",
                      "first_date": str(in_win["day"].min()) if len(in_win) else None, "last_date": str(in_win["day"].max()) if len(in_win) else None,
                      "price_kind": "derived_from_stores", "security_days_needed": n_pre, "security_days_found": got_pre, "share_found_percent": pct(got_pre, n_pre),
                      "securities_with_every_needed_day": every, "origin_store_of_the_found_security_days": dict(orig)})
    else:
        local.append({"id": "LOCAL-advi-cotbkf-after-security_day_price", "opened": False, "not_opened_reason": "no readable copy found on this box"})

    ranking = {
        "basis": "BEFORE the cash rule's additions: a priced, non-cash row the anchor carries on neither day (row type outside_anchor), as the re-count typed it.",
        "securities": rows, "securities_count": len(rows), "security_account_days_total": total,
        "securities_covering_half": cover_n(counts, 0.5), "securities_covering_ninety_percent": cover_n(counts, 0.9),
        "account_days_holding_an_outside_anchor_row": pa["account_days_holding_an_outside_anchor_row"],
        "added_by_the_cash_rule": pa["added_by_the_cash_rule"]["security_account_days"],
        "added_by_the_cash_rule_detail": dict(pa["added_by_the_cash_rule"], securities=[
            {"security": c, "ticker": (v["tickers"] or [None])[0], "asset_name": ascii_(v["name"]), "account_days": v["account_days"],
             "needed_days": len(need_add[c]), "found_days": len(union(c, al)), "coverage": cls(len(union(c, al)), len(need_add[c]))}
            for c, v in sorted(pa["securities_added"].items(), key=lambda kv: -kv[1]["account_days"])]),
    }
    cr = pa["cash_outcome_account_days"]
    cl, cl_old, cl_nc = pa["claims_cash_rule"], pa["claims_pre"], pa["claims_cash_rule_not_comparable_stays_cash"]
    sv, sv_old, sv_nc = pa["serving_cash_rule"], pa["serving_pre"], pa["serving_cash_rule_not_comparable_stays_cash"]

    def srv(x):
        return {"eligible": x["eligible"], "served": x["served"], "blank": x["blank"], "blank_share_percent": x["blank_share_percent"],
                "accounts_never_served": x["accounts_never_served"], "accounts_always_served": x["accounts_always_served"],
                "accounts_with_eligible_days": x["accounts_with_eligible_days"], "blank_by_reason": x["blank_by_reason"]}
    ctl_cash, ctl_store = pa["control_cash"], sto.control_run()
    doc = {
        "same_account_days_read": pa["same_account_days_read"],
        "same_account_days_read_basis": "this run's v0.35 totals %s equal the re-count's file %s" % (pa["v035_totals"], pa["expected_v035_totals"]),
        "days": {"graded": len(pa["graded_days"]), "first": pa["graded_days"][0], "last": pa["graded_days"][-1], "prior_partition_of_the_first_day": "2026-06-09 (read, not graded)"},
        "ranking": ranking,
        "cash_rule": {
            "rule": "a cash-flagged priced row outside the anchor is cash only where its price (Market Value / Units) is equal, within 1e-4 relative, in the day's partition and in the "
                    "prior trading day's partition for the same account and CUSIP; otherwise it is OUTSIDE_ANCHOR",
            "account_days_examined": pa["cash_account_days_examined"], "price_equal_both_days_stays_cash": cr["price_equal_both_days_stays_cash"],
            "price_differs_becomes_OUTSIDE_ANCHOR": cr["price_differs_becomes_OUTSIDE_ANCHOR"], "not_comparable": cr["not_comparable"],
            "not_comparable_treated_as": "OUTSIDE_ANCHOR (not cash): the ruling's word is 'only where measured' and a row absent from the prior trading day's partition is unmeasured. "
                                         "The other treatment (not comparable stays cash) is counted beside, under `if_not_comparable_stayed_cash`.",
            "account_days_cash_flagged_priced_outside_anchor_all": pa["cash_account_days_all"],
            "outcome_of_those_all": pa["cash_outcome_account_days_all_31k"], "rows_by_outcome": pa["cash_rows_by_outcome"],
            "outcome_rule_for_an_account_day": "any row whose price differs -> differs; else any row not comparable -> not_comparable; else equal",
            "if_not_comparable_stayed_cash": {"claims": {k: cl_nc[k] for k in ("present", "UNGRADEABLE", "ACCT_PRIOR_DATE", "ACCT_OWN_DATE", "NOTHING_TO_GRADE")},
                                              "serving": srv(sv_nc)}},
        "account_days_under_the_cash_rule": {k: cl[k] for k in ("present", "UNGRADEABLE", "ACCT_PRIOR_DATE", "ACCT_OWN_DATE", "NOTHING_TO_GRADE")},
        "account_days_recount_v035": {k: cl_old[k] for k in ("present", "UNGRADEABLE", "ACCT_PRIOR_DATE", "ACCT_OWN_DATE", "NOTHING_TO_GRADE")},
        "serving_rule_under_the_cash_rule": srv(sv),
        "serving_rule_recount_v035": srv(sv_old),
        "sixth_reason": dict(pa["sixth_reason"], treatment="a non-cash row with Units zero and Market Value positive stays a refusal of the stamp; counted as the re-count counted it, nothing changed for it"),
        "stores": st_out,
        "local_stores": local,
        "coverage_by_security": coverage_by_security,
        "coverage_basis": "a security's needed days are the day and the prior trading day of every account-day it is carried on (distinct dates); its coverage is the union over all "
                          "six opened stores; the module's match (CUSIP first, ticker second, a reused ticker not credited) decides whether a store answers for it",
        "needed_security_days_total": sum(len(v) for v in need_pre.values()),
        "upper_bound_if_market_close_stores_used": ub_m["account_days_no_longer_outside_anchor"],
        "upper_bound_if_market_close_stores_used_detail": dict(ub_m, kind="UPPER BOUND: a found close does not say the holding sits at it; securities with every needed day in the union of the market_close stores; no claim re-graded"),
        "upper_bound_if_custodian_mark_stores_also_used": ub_a["account_days_no_longer_outside_anchor"],
        "upper_bound_if_custodian_mark_stores_also_used_detail": dict(ub_a, kind="UPPER BOUND, custodian_mark stores admitted beside the market_close stores: a custodian mark is the same custodian's value of the same holding, not an independent close"),
        "upper_bounds_after_the_cash_rule": {"market_close": ub_m2, "market_close_and_custodian_mark": ub_a2,
                                             "basis": "the ranking with the cash rule's three added securities (not-comparable rows typed OUTSIDE_ANCHOR)"},
        "control": {
            "planted": {"store_reader": ctl_store and sto.PLANTED, "cash_rule": ctl_cash["planted"]},
            "read": {"store_reader": ctl_store, "cash_rule": ctl_cash["read"]},
            "fixture": "(1) a 4-row fixture parquet read by the census module's own read_store through an in-memory client: FIXA priced on day X (found), FIXB priced only on the next day "
                       "(not found on X), FIXC priced 0 on X (not a close), and a key nobody asked for (dropped); (2) the cash rule on 3 days, 4 accounts: equal, differs, absent-prior "
                       "and inside-tolerance cases with the claim of each known by construction.",
        },
    }
    doc["control"]["planted"]["store_reader"] = sto.PLANTED
    assert doc["control"]["planted"] == doc["control"]["read"], "control mismatch"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "IB133-1_outside_anchor_coverage.json").write_text(json.dumps(doc, indent=1), encoding="utf-8")

    # ------------------------------------------------------------------ the one-page read
    top = rows[:20]
    L = []
    L.append("# IB-pr-435 -- the securities the anchor does not carry, the cash rule counted, and the price stores the estate already holds (counts only)")
    L.append("")
    L.append("Read only. Same source, anchor, price rule, tolerance and trading-day axis as the re-count of IB-pr-429 AMENDMENT 2. 85 graded days, %s to %s. The same account-days were read: %s. "
             "No account id, balance or single account's holding is written." % (pa["graded_days"][0], pa["graded_days"][-1], "yes, this run's v0.35 totals equal the re-count file exactly (UNGRADEABLE 42,967; ACCT_OWN_DATE 20,138; NOTHING_TO_GRADE 13,636; ACCT_PRIOR_DATE 55; present 76,796)" if doc["same_account_days_read"] else "NO"))
    L.append("")
    L.append("**Ranking (counted BEFORE the cash rule's additions; list, total and both cover counts are on that one basis).** %d securities sit behind an OUTSIDE_ANCHOR row, carrying %s security-account-days over %s distinct account-days (the re-count read 34,437). %d securities cover half of the carried security-account-days; %d cover ninety percent." % (
        len(rows), format(total, ","), format(ranking["account_days_holding_an_outside_anchor_row"], ","), ranking["securities_covering_half"], ranking["securities_covering_ninety_percent"]))
    L.append("")
    L.append("| # | CUSIP | ticker | name | account-days | coverage (found of needed days) | best store |")
    L.append("|---|---|---|---|---|---|---|")
    for i, r in enumerate(top, 1):
        L.append("| %d | %s | %s | %s | %s | %s (%d of %d) | %s |" % (i, r["security"], r["ticker"] or "-", r["asset_name"][:40], format(r["account_days_carried"], ","), r["coverage"], r["found_days"], r["needed_days"], r["best_store"] or "-"))
    L.append("")
    L.append("**The cash rule, as ruled.** Of the 19,809 account-days the re-count named (31,307 hold a cash-flagged priced row outside the anchor): %s keep every such row as cash (price equal in the day's partition and the prior trading day's); %s have a row whose price differs and become OUTSIDE_ANCHOR; %s cannot be compared because the row is absent from the prior trading day's partition. A not-comparable row is not cash (\"only where measured\"), so those %s turn UNGRADEABLE in the primary counts (and the other treatment is counted beside). Across all 31,307 account-days: %s equal, %s differs, %s not comparable; by row: %s equal, %s differs, %s not comparable." % (
        format(cr["price_equal_both_days_stays_cash"], ","), format(cr["price_differs_becomes_OUTSIDE_ANCHOR"], ","), format(cr["not_comparable"], ","), format(cr["not_comparable"], ","),
        pa["cash_outcome_account_days_all_31k"].get("equal"), pa["cash_outcome_account_days_all_31k"].get("differs", 0), pa["cash_outcome_account_days_all_31k"].get("not_comparable"),
        pa["cash_rows_by_outcome"].get("equal"), pa["cash_rows_by_outcome"].get("differs", 0), pa["cash_rows_by_outcome"].get("not_comparable")))
    L.append("")
    L.append("Four claims under the rule, 76,796 account-days: UNGRADEABLE %s (re-count 42,967); ACCT_OWN_DATE %s (20,138); NOTHING_TO_GRADE %s (13,636); ACCT_PRIOR_DATE %s (55). Serving: eligible %s, served %s, blank %s = **%.3f percent** beside the re-count's 57.332 percent; accounts never served %d of %d (re-count 382 of 999). If the not-comparable rows stayed cash the counts equal the re-count's exactly. The securities the rule adds to OUTSIDE_ANCHOR: %d, adding %d security-account-days (%d of them by a differing price) and taking the account-days holding an outside-anchor row from 34,437 to %s; they are not in the ranking above." % (
        format(cl["UNGRADEABLE"], ","), format(cl["ACCT_OWN_DATE"], ","), format(cl["NOTHING_TO_GRADE"], ","), cl["ACCT_PRIOR_DATE"], format(sv["eligible"], ","), format(sv["served"], ","), format(sv["blank"], ","), sv["blank_share_percent"],
        sv["accounts_never_served"], sv["accounts_with_eligible_days"], len(pa["securities_added"]), ranking["added_by_the_cash_rule"], pa["added_by_the_cash_rule"]["of_which_price_differs"], format(pa["added_by_the_cash_rule"]["account_days_holding_an_outside_anchor_row_after"], ",")))
    L.append("")
    L.append("**Sixth reason.** %d row (Units zero, Market Value above zero, not cash-flagged), %d account-day, which reads UNGRADEABLE by its other rows. A refusal of the stamp, unchanged." % (pa["sixth_reason"]["rows"], pa["sixth_reason"]["account_days"]))
    L.append("")
    L.append("**The six stores** (found of needed security-days; needed = the day and the prior trading day of every account-day a ranked security is carried on, %s in all; read through the census module's own readers; no other firm's store opened, barred calls %d):" % (format(doc["needed_security_days_total"], ","), pb["barred_read"]))
    L.append("")
    for e in st_out:
        if e["opened"]:
            win = ("%s to %s in the window (store range %s to %s)" % (e["first_date"], e["last_date"], e["first_date_any"], e["last_date_any"])) if e["first_date"] else "no row for a ranked key in the window"
            L.append("- %s: opened, %s, %s; %s of %s found (%s percent); %d of %d securities with every needed day. %s" % (
                e["id"], win, e["price_kind"], format(e["security_days_found"], ","), format(e["security_days_needed"], ","), e["share_found_percent"],
                e["securities_with_every_needed_day"], len(rows), e.get("note", "")))
        else:
            L.append("- %s: NOT opened -- %s" % (e["id"], e["not_opened_reason"]))
    for e in local:
        if e["opened"]:
            L.append("- LOCAL, not in the six: %s, %s of %s found (%s percent), %d securities with every needed day. %s" % (e["path"], format(e["security_days_found"], ","), format(e["security_days_needed"], ","), e["share_found_percent"], e["securities_with_every_needed_day"], e["note"]))
        else:
            L.append("- LOCAL, not in the six: not found (%s); not built." % e["not_opened_reason"])
    L.append("")
    L.append("**Coverage by security** (union of the six stores): every needed day %d; some needed days %d; no needed day %d, of %d. **Upper bounds** (a found close does not say the holding sits at it; no claim re-graded): if every security with a close on every needed day from a market_close store were gradeable, %s of the 34,437 account-days would stop being OUTSIDE_ANCHOR (%s of them holding no other ungradeable kind, so ungradeable no longer); with custodian_mark stores admitted as well, %s (%s). The custodian mark is the same custodian's value of the same holding, not an independent close." % (
        coverage_by_security["every_needed_day"], coverage_by_security["some_needed_days"], coverage_by_security["no_needed_day"], len(rows),
        format(ub_m["account_days_no_longer_outside_anchor"], ","), format(ub_m["of_which_holding_no_other_ungradeable_kind"], ","),
        format(ub_a["account_days_no_longer_outside_anchor"], ","), format(ub_a["of_which_holding_no_other_ungradeable_kind"], ",")))
    L.append("")
    L.append("**Control.** (1) The census module's own read_store read a 4-row fixture store: the planted present security-day read found, the planted absent one not found, a zero price not a close, an unasked key dropped; read equal to planted. (2) The cash rule on a 3-day, 4-account fixture with the equal, differs, absent-prior and inside-tolerance cases, claims known by construction; read equal to planted. (3) The inherited v0.35 claims control also reads equal.")
    L.append("")
    L.append("**Not measured.** Whether any found close is the right price for the holding or sits where the account holds it; the value or balance weight of any blank; any claim re-graded with a store's price; any gold producer or anchor widening; days after 2026-10-09; the stores' content outside the ranked securities and the window; per-row claims (only per account-day).")
    (out_dir / "IB133-1_OUTSIDE_ANCHOR_COVERAGE_READ.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("OK ranking", len(rows), total, ranking["securities_covering_half"], ranking["securities_covering_ninety_percent"], coverage_by_security, ub_m["account_days_no_longer_outside_anchor"], ub_a["account_days_no_longer_outside_anchor"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
