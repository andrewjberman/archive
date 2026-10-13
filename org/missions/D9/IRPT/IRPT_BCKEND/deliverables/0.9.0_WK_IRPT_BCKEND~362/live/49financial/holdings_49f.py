#!/usr/bin/env python3
"""49 Financial Holdings: Schwab custody meshed with SmartX model membership.

Andrew-direct 2026-09-23 ~22:4xZ at the 2.0.0_SA_COO~M terminal: Holdings end to end for every
49 Financial client, meshed across the client's Schwab custody and SmartX model accounts, with a
SNAPSHOT model overlay -- which clients own which models and what assets are in those models.
No model time series.

THE MESH, MEASURED BEFORE IT WAS DESIGNED (2026-09-23, business date 2026-09-22):
- Schwab reporting master 0008335338 dim_balance carries 7,522 accounts with net_mv_plus_cash on
  every row; dim_position ties to net_mv_positions to the cent on 6,299 of the 6,325 accounts that
  carry positions; 1,197 accounts carry no position row (cash-only or empty).
- SmartX fact_allocation_account_map names 5,912 of those custody accounts (1,610 carry no SmartX
  allocation); 1,298 accounts hold more than one OPEN model allocation.
- SmartX allocation valuations NEVER tie to Schwab custody to the cent (0 of 5,912): SmartX values
  an allocation intraday on the overlay date while Schwab reports the prior close. So custody
  DOLLARS come from Schwab and model MEMBERSHIP comes from SmartX, and the two clocks are carried
  distinct on every node.

THE TREE (one basis per pie, every pie balanced to its parent, S12-AC1):
  ACCOUNT (OBSERVED, Schwab net_mv_plus_cash, custody clock)
    SLEEVE (OBSERVED, whole account) -- exactly one of
        Models          the account holds >= 1 open SmartX model allocation
        SMA > ALT Strategies > Tax   the account is a Traded=Yes row of the canonical Tax SMA workbook
        Client          neither (custody present, membership unattributed -- the plug)
      Models sleeve  -> MODEL_LEAF per open allocation (ASSIGNED).  One model: the whole sleeve,
                        claim=measured.  Several models: apportioned by SmartX's own open allocation
                        values, claim=inferred, and the apportionment is stated on the node.
                        MODEL_LEAF -> SECURITY / CASH (TARGET, USD at the SmartX overlay clock):
                        the assets SmartX holds in that model for this client. TARGET is outside
                        the custody reconciliation by contract, which is exactly right for a
                        different clock.
      Tax / Client   -> SECURITY (OBSERVED, Schwab dim_position rows) + CASH (OBSERVED,
                        net_mv_plus_cash - net_mv_positions). Where the position rows do not tie to
                        net_mv_positions within 0.01 USD the account is carried at its balance value
                        and the drill is WITHHELD with the difference stated -- never patched.

CURRENCY. Neither Schwab master nor SmartX carries a currency column (4.0.0_SA_CRO 10f3cf6f9f).
The firm report currency binds only through the shared attestation binder; without an
ANDREW_ATTESTATION record for 49financial this builder produces a CANDIDATE whose manifest says
currency_status=UNATTESTED and run_firm REFUSES to publish it. Node units say USD because the
contract's enum offers no other spelling; the manifest is the truth about that label.

NO LIVE VENDOR CALL: every read is a landed silver object; the Tax membership is a retained
projected snapshot of the canonical workbook (MDPF_TAXSMA_DATA_CONTRACT v0.5.0 projection), never
a SharePoint read from here.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import math
import re
from pathlib import Path

import pandas as pd

SOURCE_BUCKET = "opal-data-assets"
SCHWAB_PREFIX = "schwab/08335338/silver/"  # reporting master 0008335338
SMARTX_PREFIX = "smartx/platform/silver/"
PRODUCER = "holdings_snapshot.build_schwab_smartx_meshed"


def models_path() -> list:
    """The Models L0 node, from the shared taxonomy registry (CTO TAXONOMY-PATH-01)."""
    return _hs().taxonomy_path("Models")


def tax_path() -> list:
    """SMA > ALT Strategies > <the registry's Tax-Managed SMA display name>, from the registry;
    Andrew's word (d70decd6b2) placed 49F Tax under SMAs > ALT > Tax, the spelling is the registry's."""
    return _hs().taxonomy_path("SMA > ALT Strategies", "tax")
POSITION_KEY = ("cusip", "l_s", "accounting_rule_code", "tax_code")


def _firm_id() -> str:
    """The canonical long firm id, read through the registry lookup (LGIC naming gate), lazily
    so this module imports before holdings_snapshot has put lib/ on sys.path."""
    from opal_naming import lookup
    return lookup("49financial")["long"]


class FortyNineRefused(ValueError):
    pass


def _hs():
    import holdings_snapshot as hs  # late import: holdings_snapshot registers this builder
    return hs


def _sac():
    import schwab_account_codes as sac  # late import, same directory (IB-mr-213 / UIC-16 at 49F)
    return sac


def _num(value):
    if value is None or isinstance(value, bool):
        raise FortyNineRefused("REFUSED: 49F unknown numeric value is not zero")
    try:
        result = float(value)
    except (TypeError, ValueError):
        raise FortyNineRefused("REFUSED: 49F unknown numeric value is not zero") from None
    if not math.isfinite(result):
        raise FortyNineRefused("REFUSED: 49F unknown numeric value is not zero")
    return result


def _text(value):
    if value is None:
        return ""
    if isinstance(value, float) and math.isnan(value):
        return ""
    return str(value).strip()


def normalize_tax_account(value) -> "str | None":
    """MDPF_TAXSMA_DATA_CONTRACT v0.5.0 identity.normalization, nothing wider."""
    raw = _text(value).replace("-", "", 1) if _text(value).count("-") == 1 else _text(value)
    if re.fullmatch(r"[0-9]{8}", raw):
        return "00" + raw
    if re.fullmatch(r"00[0-9]{8}", raw):
        return raw
    return None


def tax_membership_from_snapshot(path) -> dict:
    """Traded=Yes account numbers from a retained projected workbook snapshot.

    Returns the normalized account set plus the snapshot's own provenance so the manifest can
    pin what it consumed. Rows that fail the contract's identity forms are counted, not fixed.
    """
    doc = json.loads(Path(path).read_text(encoding="utf-8"))
    rows = doc.get("rows") or []
    traded, rejected = set(), 0
    for row in rows:
        if row.get("row_kind") != "ACCOUNT_SLOT":
            continue
        if _text(row.get("Traded")).casefold() != "yes":
            continue
        account = normalize_tax_account(row.get("Account Number"))
        if account is None:
            rejected += 1
            continue
        traded.add(account)
    digest = hashlib.sha256(json.dumps(doc, sort_keys=True).encode("utf-8")).hexdigest()
    source = doc.get("source") if isinstance(doc.get("source"), dict) else {}
    return {"accounts": traded, "traded_row_count": len(traded) + rejected,
            "rejected_identity_rows": rejected,
            "provenance": {"contract": doc.get("contract"), "observed_at_utc": doc.get("observed_at_utc"),
                           "workbook_etag": source.get("etag_after"),
                           "workbook_last_modified": source.get("lastModifiedDateTime"),
                           "snapshot_sha256": digest}}


def _position_id(sleeve_id, row, ordinal):
    key = [sleeve_id] + [_text(row.get(c)) for c in POSITION_KEY] + [int(ordinal)]
    return sleeve_id + ":position:" + hashlib.sha256(
        json.dumps(key, separators=(",", ":")).encode("utf-8")).hexdigest()


def _security_identifier(row):
    for column, namespace in (("cusip", "CUSIP"), ("ticker_symbol", "TICKER"), ("isin", "ISIN")):
        supplied = _text(row.get(column))
        if supplied:
            return {"namespace": namespace, "value": supplied}
    return {"namespace": "UNKNOWN", "value": "schwab:" + (_text(row.get("accounting_rule_code")) or "row")}


def security_names(asset) -> dict:
    """CUSIP -> the Schwab security master's own name for it (dim_asset security_description_line_1 and _2,
    whitespace collapsed). It is read only for custody rows that carry no ticker_symbol (CTO R5 decision 4,
    RULINGS_IRPT_20260925.md @75156f2b18). The master carries no ticker for those rows, so only the name is
    filled. A CUSIP whose master rows disagree on the name is left out, never guessed. No master -> {}."""
    if asset is None or asset.empty or "cusip" not in asset.columns:
        return {}
    seen = {}
    for row in asset.to_dict("records"):
        cusip = _text(row.get("cusip"))
        name = " ".join(" ".join(_text(row.get(c)) for c in (
            "security_description_line_1", "security_description_line_2")).split())
        if cusip and name:
            seen.setdefault(cusip, set()).add(name)
    return {cusip: names.pop() for cusip, names in seen.items() if len(names) == 1}


def cusips_by_ticker(asset) -> dict:
    """ticker -> the sorted distinct CUSIPs the Schwab security master (dim_asset ticker_symbol, cusip) holds for it.
    SmartX carries no CUSIP; this join is the only source of one on a SmartX node. No master -> {}."""
    if asset is None or asset.empty or "cusip" not in asset.columns or "ticker_symbol" not in asset.columns:
        return {}
    seen = {}
    for row in asset.to_dict("records"):
        ticker, cusip = _text(row.get("ticker_symbol")), _text(row.get("cusip"))
        if ticker and cusip:
            seen.setdefault(ticker, set()).add(cusip)
    return {t: sorted(c) for t, c in seen.items()}


def _try_currency_authority():
    from currency_authority import CurrencyAuthorityRefused, bind_report_currency
    try:
        return bind_report_currency(_firm_id())["currency_authority"], None
    except CurrencyAuthorityRefused as exc:
        return None, str(exc)


def load_49f_sources(s3, as_of: str) -> dict:
    hs = _hs()
    custody_date = hs._latest_date_partition(s3, SOURCE_BUCKET, SCHWAB_PREFIX + "dim_balance/", as_of=as_of)
    overlay_date = hs._latest_date_partition(s3, SOURCE_BUCKET, SMARTX_PREFIX + "fact_allocation_account_map/", as_of=as_of)
    if custody_date is None or overlay_date is None:
        raise FortyNineRefused("REFUSED: 49F custody or overlay partition unavailable at cutoff")
    read = lambda key: hs._read_parquet(s3, SOURCE_BUCKET, key)  # noqa: E731
    frames = {
        "balance": read(SCHWAB_PREFIX + "dim_balance/date=%s/data.parquet" % custody_date),
        "positions": read(SCHWAB_PREFIX + "dim_position/date=%s/data.parquet" % custody_date),
        "map": read(SMARTX_PREFIX + "fact_allocation_account_map/date=%s/data.parquet" % overlay_date),
        "roster": read(SMARTX_PREFIX + "fact_model_allocation_roster/date=%s/data.parquet" % overlay_date),
        "valuation": read(SMARTX_PREFIX + "fact_allocation_valuation/date=%s/data.parquet" % overlay_date),
        "model_positions": read(SMARTX_PREFIX + "fact_allocation_positions/date=%s/data.parquet" % overlay_date),
    }
    for name in ("balance", "map", "roster", "valuation"):
        if frames[name].empty:
            raise FortyNineRefused("REFUSED: 49F %s frame empty at its partition" % name)
    # The security master names the custody rows that carry no ticker. It is display enrichment, so an absent
    # object reads empty and never refuses the build.
    frames["asset"] = read(SCHWAB_PREFIX + "dim_asset/date=%s/data.parquet" % custody_date)
    frames["custody_date"], frames["overlay_date"] = custody_date, overlay_date
    frames["positions_key"] = SCHWAB_PREFIX + "dim_position/date=%s/data.parquet" % custody_date
    return frames


def _custody_units(hs, prow, sleeve_id, custody_date, units_rev):
    """CUSTODY_UNITS from the Schwab dim_position row's own quantity_settled_unsettled (the quantity
    beside the market_value_settled_unsettled this node's amount reads), stated on the account's opaque
    id at the custody partition date, with the dim_position object's receipted sha256 as the revision
    (IRPT-HOLDINGS-VALUATION-FACTS-20260924; price is never computed). None -> no fact."""
    if not units_rev:
        return None
    fact = hs._custody_units_fact({"Units": prow.get("quantity_settled_unsettled"), "_source_as_of": custody_date},
                                  sleeve_id.split(":")[0], units_rev)
    return [fact] if fact else None


def _smartx_overlay(frames) -> "tuple[dict, dict, set]":
    """account_id10 -> list of open allocation dicts; SmartX accounts absent from custody."""
    hs = _hs()
    m = frames["map"].copy()
    if m["allocation_id"].duplicated().any():
        raise FortyNineRefused("REFUSED: 49F SmartX allocation repeated in the account map")
    m["account_id10"] = m["account_number"].map(hs._pad10)
    roster = frames["roster"].drop_duplicates("allocation_id").set_index("allocation_id")
    valuation = frames["valuation"].drop_duplicates("owner_id").set_index("owner_id")
    model_positions = frames["model_positions"]
    by_alloc = ({k: g for k, g in model_positions.groupby("owner_id")}
                if len(model_positions) and "owner_id" in model_positions.columns else {})
    overlay, closed = {}, {}
    for row in m.to_dict("records"):
        alloc = _text(row.get("allocation_id"))
        account = row["account_id10"]
        r = roster.loc[alloc] if alloc in roster.index else None
        v = valuation.loc[alloc] if alloc in valuation.index else None
        if r is None or v is None:
            raise FortyNineRefused("REFUSED: 49F SmartX allocation lacks roster or valuation row")
        status = _text(r.get("status"))
        if status != "open":
            closed.setdefault(account, []).append(alloc)
            continue
        for column in ("long_equity", "short_equity", "cash"):
            if pd.isna(v.get(column)):
                raise FortyNineRefused("REFUSED: 49F SmartX valuation incomplete; unknown is not zero")
        value = _num(v["long_equity"]) - _num(v["short_equity"]) + _num(v["cash"])
        model_id = _text(row.get("model_id"))
        if not model_id:
            raise FortyNineRefused("REFUSED: 49F open SmartX allocation without a model id")
        positions = by_alloc.get(alloc)
        overlay.setdefault(account, []).append({
            "allocation_id": alloc, "model_id": model_id, "model_name": _text(r.get("model_name")),
            "value": value, "cash": _num(v["cash"]),
            "positions": positions if positions is not None else pd.DataFrame()})
    return overlay, closed, set(m["account_id10"])


def build_49f_actual(s3, as_of: str, *, tax_membership_path=None) -> "tuple[list, dict]":
    hs = _hs()
    firm_id = _firm_id()
    frames = load_49f_sources(s3, as_of)
    custody_date, overlay_date = frames["custody_date"], frames["overlay_date"]
    balance, positions = frames["balance"], frames["positions"]
    if balance["account_id"].duplicated().any():
        raise FortyNineRefused("REFUSED: 49F duplicate custody account in dim_balance")
    balance = balance.set_index(balance["account_id"].map(_text))
    # CTO 101302: each ACCOUNT node's own mask, from the custody row that mints it. UIC-16
    # (IB-mr-213), amendment 1 (CTO refusal @05b9abe572): the label is the REGISTRATION type
    # (dim_balance acct_regis) through registration_name -- NEVER acct_type (the product code:
    # `IRA` spans six registrations, `S1` spans five) -- turned into its full name from the
    # committed table before it reaches account_mask; a code the acct_regis section lacks --
    # including blank -- prints "unrecognised (<code>)", never the bare code alone.
    sac = _sac()
    account_masks = hs.own_account_masks(firm_id, (
        (raw, raw, sac.registration_name(_text(t))) for raw, t in zip(balance.index,
                                             balance["acct_regis"] if "acct_regis" in balance.columns else [""] * len(balance))))
    positions = positions.copy()
    positions["account_id"] = positions["account_id"].map(_text)
    # A null market value refuses that account's drill below, never the whole build.
    positions["_mv"] = pd.to_numeric(positions["market_value_settled_unsettled"].astype(object).map(
        lambda v: None if v is None or (isinstance(v, float) and math.isnan(v)) else float(v)), errors="coerce")
    positions_by_account = {k: g for k, g in positions.groupby("account_id")}
    master_names = security_names(frames.get("asset"))
    master_cusips = cusips_by_ticker(frames.get("asset"))
    # the dim_position object's receipted sha256, ONLY when the published contract admits CUSTODY_UNITS
    units_rev = hs._receipt_sha(s3, SOURCE_BUCKET, frames["positions_key"]) if hs.custody_units_admitted() else None

    overlay, closed, smartx_accounts = _smartx_overlay(frames)
    tax = tax_membership_from_snapshot(tax_membership_path) if tax_membership_path else None
    tax_accounts = tax["accounts"] if tax else set()
    currency_authority, currency_refusal = _try_currency_authority()
    dir_ids = hs._directory_account_ids(s3, hs.firm_bucket_map().get(firm_id, ""), firm_id)
    client_path, MODELS_PATH, TAX_PATH = hs._client_hierarchy_path(), models_path(), tax_path()  # noqa: N806

    nodes, refused, withheld = [], [], []
    custody_ids, assigned_ids, value_by_account = set(), set(), {}
    census = {"models": 0, "sma_tax": 0, "client": 0, "client_closed_smartx_only": 0, "client_membership_conflict": 0,
              "model_leaves": 0, "model_leaves_inferred": 0, "model_assets": 0,
              "smartx_cusip_via_ticker": 0, "smartx_cusip_listed_ambiguous": 0, "smartx_cusip_listed_absent": 0,
              "schwab_positions": 0, "schwab_positions_named_from_master": 0, "drill_withheld": 0}
    dir_matched = 0
    total_before = 0.0
    for raw_account in sorted(balance.index):
        brow = balance.loc[raw_account]
        try:
            account_value = _num(brow["net_mv_plus_cash"])
            net_positions = _num(brow["net_mv_positions"])
        except FortyNineRefused as exc:
            refused.append({"account": raw_account, "reason": str(exc)})
            continue
        account_id = hs.opaque_id("account", firm_id, raw_account)
        custody_ids.add(account_id)
        value_by_account[account_id] = account_value
        total_before += account_value
        if dir_ids is not None and account_id in dir_ids:
            dir_matched += 1
        common = (PRODUCER, "schwab dim_balance net_mv_plus_cash (custody) x smartx account map (membership)",
                  1, 1, "measured")
        nodes.append(hs._node(account_id, None, 0, "ACCOUNT", "OBSERVED", account_value, "USD",
                              "UNIQUE_CUSTODY_TOTAL", account_value, None, None, *common,
                              drill_refs=[{"ref_kind": "ACCOUNT", "ref_id": account_id}],
                              classification=hs._unknown_classification(
                                  ["49F custody: Schwab master 0008335338 business_date=%s" % custody_date])))
        allocations = overlay.get(raw_account, [])
        in_tax = raw_account in tax_accounts
        if allocations and in_tax:
            # A per-account conflict between the two membership sources is carried in Client with the
            # conflict stated and counted, never a refusal of the whole build (CTO 49F-TAX-CONFLICT-01).
            refused.append({"account": account_id, "reason": "membership conflict: SmartX-modeled and Tax SMA Traded=Yes; "
                                                                "carried in Client, membership unattributed"})
            allocations, in_tax = [], False
            conflict = True
        else:
            conflict = False
        if allocations:
            sleeve_id, path, label = account_id + ":models", MODELS_PATH, "models"
            facts = ["SmartX is the model authority: %d open allocation(s)" % len(allocations)]
        elif in_tax:
            sleeve_id, path, label = account_id + ":sma:tax", TAX_PATH, "sma_tax"
            facts = ["Traded=Yes row of the canonical Tax SMA workbook (Andrew d70decd6b2); "
                     "value is Schwab net_mv_plus_cash, never workbook AUM",
                     # This sleeve's overlay clock is the workbook observation, not SmartX's partition (CTO INF-CLOCK-01).
                     "overlay clock for this sleeve: workbook observed_at %s, workbook last modified %s"
                     % ((tax or {}).get("provenance", {}).get("observed_at_utc"),
                        (tax or {}).get("provenance", {}).get("workbook_last_modified"))]
        else:
            sleeve_id, path, label = account_id + ":client", client_path, "client"
            facts = ["Known custody in Client; no open SmartX allocation and no Tax SMA membership"]
            if conflict:
                facts = ["MEMBERSHIP CONFLICT: this account is both SmartX-modeled and a Tax SMA Traded=Yes row; "
                         "carried in Client at full custody value, membership unattributed until the sources agree"]
                census["client_membership_conflict"] += 1
            if raw_account in closed:
                facts.append("SmartX allocation(s) present but not open: %d" % len(closed[raw_account]))
                census["client_closed_smartx_only"] += 1
        census[label] += 1
        if allocations or in_tax:
            assigned_ids.add(account_id)
        # L0 CATEGORY (CTO ruling msg 102475, cell IB-mr-202): exactly one category per account here
        # already (Models / SMAs (Tax) / Client), so this is a node_kind rename, not a shape change.
        nodes.append(hs._node(sleeve_id, account_id, 1, "CATEGORY", "OBSERVED", account_value, "USD",
                              "PARENT_NODE", account_value, None, None, *common,
                              classification=hs._unknown_classification(facts, hierarchy_path=path)))
        if allocations:
            smartx_total = sum(a["value"] for a in allocations)
            single = len(allocations) == 1
            leaf_values = []
            for a in allocations:
                if single:
                    leaf_value = account_value
                elif smartx_total > 0:
                    leaf_value = account_value * (a["value"] / smartx_total)
                else:
                    leaf_value = account_value / len(allocations)
                leaf_values.append(leaf_value)
            # The last leaf absorbs float residue so the ASSIGNED pie balances to the cent.
            if not single:
                leaf_values[-1] = account_value - sum(leaf_values[:-1])
            for a, leaf_value in zip(allocations, leaf_values):
                leaf_id = account_id + ":model:" + a["allocation_id"]
                claim = "measured" if single else "inferred"
                leaf_facts = ["model_name=%s" % a["model_name"],
                              "smartx_allocation_value=%.2f at overlay clock %s" % (a["value"], overlay_date)]
                if not single:
                    leaf_facts.append("INFERRED: custody dollars apportioned across %d open models by "
                                      "SmartX allocation values; the split is SmartX's, the total is Schwab's"
                                      % len(allocations))
                    census["model_leaves_inferred"] += 1
                census["model_leaves"] += 1
                nodes.append(hs._node(leaf_id, sleeve_id, 2, "MODEL_LEAF", "ASSIGNED", leaf_value, "USD",
                                      "PARENT_NODE", account_value, None, None, PRODUCER,
                                      "fact_allocation_account_map allocation -> model_id; roster status=open",
                                      1, 1, claim,
                                      model_id={"namespace": "SMARTX_MODEL", "value": a["model_id"]},
                                      drill_refs=[{"ref_kind": "MODEL", "ref_id": a["model_id"]}],
                                      classification=hs._unknown_classification(leaf_facts, hierarchy_path=MODELS_PATH)))
                # Assets in the model, at SmartX's own clock: a TARGET pie, outside custody reconciliation.
                model_positions = a["positions"]
                for ordinal, prow in enumerate(model_positions.sort_values("symbol_id").to_dict("records")
                                               if len(model_positions) else []):
                    mv = _num(prow.get("market_value"))
                    ticker = _text(prow.get("ticker"))
                    ident = ({"namespace": "TICKER", "value": ticker} if ticker
                             else {"namespace": "VENDOR", "value": _text(prow.get("symbol_id"))})
                    # SmartX holds no CUSIP: one is carried only when 49F's own Schwab master maps this ticker to exactly
                    # one, and it says so (cusip_basis). Zero or several -> the source id stays and the node is listed.
                    cusip_facts, matches = [], master_cusips.get(ticker, []) if ticker else []
                    if len(matches) == 1:
                        ident = {"namespace": "CUSIP", "value": matches[0]}
                        cusip_facts.append("cusip_basis: joined_via_ticker(dim_asset@%s)" % custody_date)
                        census["smartx_cusip_via_ticker"] += 1
                    elif matches:
                        cusip_facts.append("no unique CUSIP for ticker")
                        census["smartx_cusip_listed_ambiguous"] += 1
                    else:
                        cusip_facts.append("no CUSIP in source")
                        census["smartx_cusip_listed_absent"] += 1
                    weight = (mv / a["value"]) if a["value"] else None
                    nodes.append(hs._node(
                        leaf_id + ":asset:" + hashlib.sha256((_text(prow.get("symbol_id")) + "|" + str(ordinal)).encode()).hexdigest()[:24],
                        leaf_id, 3, "SECURITY", "TARGET", mv, "USD", "PARENT_NODE", a["value"], None, None,
                        PRODUCER, "fact_allocation_positions for the open allocation (SmartX overlay clock)",
                        1, 1, "measured", security_id=ident,
                        classification=hs._unknown_classification(
                            ["asset in the model at SmartX overlay clock %s; smartx_weight=%s"
                             % (overlay_date, "%.6f" % weight if weight is not None else "n/a"),
                             "company=%s" % _text(prow.get("company"))]
                            # The ticker travels as a fact whatever the security_id namespace: display (and so the class
                            # lookup) reads the symbol from `ticker=`, and a CUSIP id above would otherwise lose it.
                            + (["ticker=" + ticker] if ticker else []) + cusip_facts, hierarchy_path=MODELS_PATH)))
                    census["model_assets"] += 1
                nodes.append(hs._node(leaf_id + ":cash", leaf_id, 3, "CASH", "TARGET", a["cash"], "USD",
                                      "PARENT_NODE", a["value"], None, None, PRODUCER,
                                      "fact_allocation_valuation.cash (SmartX overlay clock)", 1, 1, "measured",
                                      security_id={"namespace": "CASH", "value": "SMARTX_CASH"},
                                      classification=hs._unknown_classification(
                                          ["cash held in the model at SmartX overlay clock %s" % overlay_date],
                                          hierarchy_path=MODELS_PATH)))
            continue
        # Tax and Client sleeves: the OBSERVED Schwab drill, or an explicit withholding.
        prows = positions_by_account.get(raw_account)
        null_rows = int(prows["_mv"].isna().sum()) if prows is not None else 0
        position_sum = float(prows["_mv"].sum()) if prows is not None else 0.0
        if null_rows or abs(position_sum - net_positions) > hs.RECON_TOLERANCE_USD:
            withheld.append({"account_id": account_id, "position_rows": int(len(prows)) if prows is not None else 0,
                             "null_market_value_rows": null_rows,
                             "position_sum": round(position_sum, 2), "net_mv_positions": round(net_positions, 2),
                             "difference": round(position_sum - net_positions, 2)})
            census["drill_withheld"] += 1
            nodes[-1]["classification"]["capability_facts"].append(
                "DRILL WITHHELD: dim_position rows sum to %.2f against net_mv_positions %.2f (%d null-value row(s)); "
                "the account is carried at its balance value and no security row is shown"
                % (position_sum, net_positions, null_rows))
            continue
        if prows is not None:
            for ordinal, prow in enumerate(prows.to_dict("records")):
                master_name = "" if _text(prow.get("ticker_symbol")) else master_names.get(_text(prow.get("cusip")), "")
                census["schwab_positions_named_from_master"] += 1 if master_name else 0
                nodes.append(hs._node(_position_id(sleeve_id, prow, ordinal), sleeve_id, 2, "SECURITY", "OBSERVED",
                                      prow["_mv"], "USD", "PARENT_NODE", account_value, None, None, PRODUCER,
                                      "schwab dim_position row (signed market_value_settled_unsettled)", 1, 1, "measured",
                                      security_id=_security_identifier(prow),
                                      classification=hs._unknown_classification(
                                          ["l_s=%s accounting_rule_code=%s" % (_text(prow.get("l_s")), _text(prow.get("accounting_rule_code")))]
                                          # the custody row's own ticker_symbol, stated as a fact so the display fill
                                          # (holdings_snapshot.fill_display_from_facts) can label the row without a guess
                                          + (["ticker=" + _text(prow.get("ticker_symbol"))] if _text(prow.get("ticker_symbol")) else [])
                                          # a row with no ticker: the Schwab security master's name for its CUSIP
                                          + (["company=" + master_name] if master_name else []),
                                          hierarchy_path=path),
                                      valuation_facts=_custody_units(hs, prow, sleeve_id, custody_date, units_rev)))
                census["schwab_positions"] += 1
        cash = account_value - net_positions
        nodes.append(hs._node(sleeve_id + ":cash", sleeve_id, 2, "CASH", "OBSERVED", cash, "USD", "PARENT_NODE",
                              account_value, None, None, PRODUCER,
                              "schwab dim_balance net_mv_plus_cash - net_mv_positions (signed)", 1, 1, "measured",
                              security_id={"namespace": "CASH", "value": "SCHWAB_CASH"},
                              classification=hs._unknown_classification(["custody cash remainder"], hierarchy_path=path)))

    holdouts = hs.holdout_block(custody_ids, assigned_ids, value_by_account, observable="MEASURED",
                                source="schwab/08335338/silver/dim_balance date=%s minus (smartx open allocations "
                                       "date=%s union Tax SMA workbook Traded=Yes)" % (custody_date, overlay_date))
    smartx_not_in_custody = sorted(a for a in smartx_accounts if a not in set(balance.index))
    tax_not_in_custody = sorted(a for a in tax_accounts if a not in set(balance.index))
    coverage = {"nodes_resolved": census["models"] + census["sma_tax"], "nodes_attempted": len(custody_ids),
                "remainder": {"amount": round(holdouts["value"]["value"], 2), "units": "USD",
                              "reason": "%d of %d custody account(s) carried in Client with membership unattributed"
                                        % (holdouts["account_count"], len(custody_ids))}}
    manifest = {"firm_id": firm_id, "source": "schwab/08335338/silver + smartx/platform/silver",
                "custody_date": custody_date, "overlay_date": overlay_date, "date": custody_date,
                "join_matched": census["models"], "join_attempted": len(custody_ids),
                "total_market_value": round(total_before, 2),
                "census": census, "refused_accounts": refused, "drill_withheld": withheld,
                "smartx_accounts_not_in_custody": len(smartx_not_in_custody),
                "tax_traded_not_in_custody": len(tax_not_in_custody),
                "tax_membership": ({k: v for k, v in tax.items() if k != "accounts"} if tax else None),
                "currency_status": "ATTESTED" if currency_authority else "UNATTESTED",
                "currency_authority": currency_authority,
                "currency_refusal": currency_refusal,
                "directory_cross_check": {"matched": dir_matched, "attempted": len(custody_ids),
                                          "note": "INFORMATIONAL ONLY, not a join gate"}}
    if currency_authority is None:
        manifest["publication_refused"] = ("REFUSED: 49F report currency unattested (%s); candidate only"
                                           % currency_refusal)
    hs.recompute_weights(nodes)
    stamped = hs.stamp_clocks(nodes, custody_date, overlay_date)
    return nodes, {"coverage": coverage, "manifest": manifest, "source_completion_date": custody_date,
                   "custody_as_of": custody_date, "overlay_as_of": overlay_date, "holdouts": holdouts,
                   "account_masks": account_masks,
                   "assigned_without_custody": {
                       "account_count": len(smartx_not_in_custody) + len(tax_not_in_custody),
                       "denominator": "%d SmartX-mapped and %d Tax-traded account(s) absent from custody"
                                      % (len(smartx_not_in_custody), len(tax_not_in_custody)),
                       "source": "smartx account map date=%s and Tax workbook minus dim_balance date=%s"
                                 % (overlay_date, custody_date)},
                   "nodes_stamped": stamped}


def model_snapshot(nodes: "list[dict]", firm_id: "str | None" = None) -> dict:
    """The snapshot model overlay Andrew asked for: which clients own which models, what is in them.

    A pure projection over accepted nodes, firm-agnostic. Per model: the accounts that hold it
    (with the ASSIGNED custody dollars) and the assets under each MODEL_LEAF aggregated across
    those accounts -- SmartX's TARGET pie at the overlay clock for 49F, the OBSERVED Orion
    positions for INF -- with the asset basis stated. No time series; one clock pair, stated once.
    """
    by_id = {n["node_id"]: n for n in nodes}
    models: "dict[str, dict]" = {}
    for leaf in (n for n in nodes if n["node_kind"] == "MODEL_LEAF"):
        model_id = leaf["model_id"]["value"]
        facts = leaf.get("classification", {}).get("capability_facts", [])
        name = next((f.split("=", 1)[1] for f in facts if f.startswith("model_name=")), "")
        entry = models.setdefault(model_id, {"model_id": model_id, "model_namespace": leaf["model_id"]["namespace"],
                                             "model_name": name, "accounts": [], "assigned_value": 0.0, "assets": {},
                                             "asset_basis": set()})
        sleeve = by_id[leaf["parent_node_id"]]
        entry["accounts"].append({"account_id": sleeve["parent_node_id"], "assigned_value": leaf["amount"]["value"],
                                  "claim": leaf["provenance"]["claim"]})
        entry["assigned_value"] += leaf["amount"]["value"]
    for asset in (n for n in nodes if n["node_kind"] in ("SECURITY", "CASH") and n.get("parent_node_id") in by_id):
        leaf = by_id[asset["parent_node_id"]]
        if leaf["node_kind"] != "MODEL_LEAF":
            continue
        entry = models[leaf["model_id"]["value"]]
        entry["asset_basis"].add(asset["basis"])
        key = asset["security_id"]["namespace"] + ":" + asset["security_id"]["value"]
        facts = asset.get("classification", {}).get("capability_facts", [])
        label = next((f.split("=", 1)[1] for f in facts if f.startswith("ticker=") and f != "ticker="),
                     asset["security_id"]["value"])
        slot = entry["assets"].setdefault(key, {"security_id": asset["security_id"], "label": label,
                                                "kind": asset["node_kind"], "value": 0.0, "accounts": 0})
        slot["value"] += asset["amount"]["value"]
        slot["accounts"] += 1
    clocks = next((n.get("clocks") for n in nodes if n.get("clocks")), None)
    out = []
    for entry in sorted(models.values(), key=lambda e: -e["assigned_value"]):
        assets = sorted(entry["assets"].values(), key=lambda a: -a["value"])
        out.append({**entry, "assigned_value": round(entry["assigned_value"], 2), "account_count": len(entry["accounts"]),
                    "asset_basis": sorted(entry["asset_basis"]),
                    "assets": [{**a, "value": round(a["value"], 2)} for a in assets]})
    return {"schema_version": "irpt-holdings-model-snapshot-v1", "firm_id": firm_id or _firm_id(), "clocks": clocks,
            "model_count": len(out), "models": out}


def build_49f_meshed(s3, as_of: str) -> "tuple[list, dict]":
    """The BUILDERS entry: the Tax membership snapshot path comes from the environment, so the
    runner's command line is unchanged. An ABSENT path REFUSES the build (Andrew-direct 2026-09-24 ~12:5xZ,
    card 6: the retained tax-managed membership snapshot is a required input of this build until it is a
    receipted source object under the holdings migration). Measured 2026-09-24 06:2xZ: with the variable
    unset this builder silently produced a candidate whose tax-managed sleeves were gone, and it validated,
    reconciled and passed every gate -- a silent regression, which a refusal is not."""
    if dt.date.fromisoformat(as_of).isoformat() != as_of:
        raise FortyNineRefused("REFUSED: ISO as_of required")
    path, vintage = _hs().retained_capture(
        s3, "IRPT_49F_TAX_MEMBERSHIP_SNAPSHOT", "gateway", _firm_id(), "taxsma_workbook_projection",
        "taxsma_workbook_projected_snapshot.json", as_of)
    if path is None:
        raise FortyNineRefused("REFUSED: 49F tax-managed membership snapshot not supplied "
                               "(IRPT_49F_TAX_MEMBERSHIP_SNAPSHOT unset and no landed capture at or before %s) -- a "
                               "retained input this build requires (Andrew-direct 2026-09-24 card 6)" % as_of)
    nodes, out = build_49f_actual(s3, as_of, tax_membership_path=path)
    out["manifest"]["tax_membership_vintage"] = vintage
    return nodes, out
