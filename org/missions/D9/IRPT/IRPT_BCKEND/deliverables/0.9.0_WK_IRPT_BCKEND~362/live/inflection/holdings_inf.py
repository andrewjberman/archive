#!/usr/bin/env python3
"""Inflection Holdings: Orion custody meshed with Eclipse model membership.

Andrew-direct 2026-09-23 ~22:4xZ at the 2.0.0_SA_COO~M terminal: Holdings end to end for every
Inflection client, meshed across the client's Eclipse and Orion accounts, with a SNAPSHOT model
overlay -- which clients own which models and what assets are in those models. No time series.

THE MESH, MEASURED BEFORE IT WAS DESIGNED (2026-09-23):
- Orion silver/api_dims/accounts_v2 carries 876 accounts with current_value; positions_mv carries
  36,044 native positions over 958 accounts and ties to current_value to the cent on 876 of 876
  (4.0.0_SA_CRO 10f3cf6f9f established that a daily key holds the prior close; the two feeds are
  read at the same snapshot date and that date is the custody clock).
- Eclipse portfolios_simple maps 786 accounts to exactly one portfolio each (0 multi-portfolio
  accounts, 0 portfolios exposing more than one account); 663 of those portfolios carry a model
  id, 181 do not. portfolios_full carries managed_value and excluded_value; 132 portfolios hold a
  nonzero excluded part. Every Orion position row says is_managed=True, so a position cannot be
  attributed to the managed or the excluded part of an account from these sources.
- Eclipse models.parquet names 18 models; model_composition.parquet describes the 9 Opal models
  as Security Sets without security-level rows. So the assets in an Inflection model, for this
  snapshot, are the member accounts' actual Orion positions (OBSERVED), never an inferred target.

THE TREE (one basis per pie, every pie balanced to its parent):
  ACCOUNT (OBSERVED, accounts_v2.current_value, custody clock)
    whole-account model (portfolio has a model, membership complete, excluded ~ 0, managed ties):
      SLEEVE Models (OBSERVED, whole account) -> MODEL_LEAF (ASSIGNED, whole account, claim=measured,
        ECLIPSE_MODEL_ID) -> SECURITY (OBSERVED, the validated Orion positions)
    split account (portfolio has a model, membership complete, excluded > 0, managed + excluded = total):
      TWO VIEWS OF THE SAME MONEY UNDER THE ACCOUNT, one basis each, never summed together
      (CTO rulings batch 96, INFLECTION-HOLDINGS-SPLIT-ACCOUNTS-20261001):
      the ASSIGNED view -- CATEGORY Models (ASSIGNED, managed_value) -> MODEL_LEAF (ASSIGNED,
        managed_value, measured), and CATEGORY Client (ASSIGNED, excluded_value): Eclipse's split;
      the OBSERVED view -- SECURITY (OBSERVED, the validated Orion positions) directly under the
        ACCOUNT, attributed to NEITHER part, because Orion does not say which position sits in
        which part. What the account holds is measured; only the part is not.
    everything else (no portfolio, no model, incomplete membership, or values that do not tie):
      SLEEVE Client (OBSERVED, whole account, the plug) -> SECURITY (OBSERVED, Orion positions)

CURRENCY. Orion carries no currency column; the firm report currency binds only through the
shared attestation binder. Without an ANDREW_ATTESTATION record for inflection this builder
produces a CANDIDATE (validator in candidate_unattested mode) whose manifest says
currency_status=UNATTESTED and run_firm REFUSES to publish it.

NO LIVE VENDOR CALL: every read is a landed silver object.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import math
from pathlib import Path

import pandas as pd

PRODUCER = "holdings_snapshot.build_orion_eclipse_meshed"


class InflectionRefused(ValueError):
    pass


def _hs():
    import holdings_snapshot as hs
    return hs


def _firm_id() -> str:
    from opal_naming import lookup
    return lookup("inflection")["long"]


def _num(value):
    if value is None or isinstance(value, bool):
        return None
    try:
        result = float(value)
    except (TypeError, ValueError):
        return None
    return result if math.isfinite(result) else None


def _text(value):
    """Identity text for a nullable-integer or string cell: '' for absent, '44' for 44 or 44.0.

    A pandas Int64 column with nulls maps its values through float, so a naive str() renders
    '44.0' and no longer matches the '44' the other frame produced (measured 2026-09-23: every
    Eclipse-mapped account read as unmapped because of it).
    """
    if value is None or isinstance(value, bool):
        return ""
    try:
        if pd.isna(value):
            return ""
    except (TypeError, ValueError):
        pass
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value).strip()


def _try_currency_authority():
    from currency_authority import CurrencyAuthorityRefused, bind_report_currency
    try:
        return bind_report_currency(_firm_id())["currency_authority"], None
    except CurrencyAuthorityRefused as exc:
        return None, str(exc)


def _producer_path():
    """The INF silver producers' directory on sys.path, the same way the runner reaches the
    positions key builder; only pure locator helpers are read from it, never a writer."""
    import sys
    silver_dir = _hs().inf_producer_dir()
    if str(silver_dir) not in sys.path:
        sys.path.insert(0, str(silver_dir))


def _orion_dim_prefix(dim: str) -> str:
    """The Orion silver dim prefix, from the producer's own key builder (never re-typed here),
    exactly as holdings_snapshot._inf_positions_source_key resolves the positions key."""
    _producer_path()
    from _orion_api_silver_lib import silver_api_dim_s3_key
    key = silver_api_dim_s3_key(dim, dt.date(2000, 1, 1))
    prefix, partition, filename = key.rsplit("/", 2)
    if partition != "snapshot_date=2000-01-01" or filename != "data.parquet":
        raise InflectionRefused("REFUSED: INF producer partition/file shape changed")
    return prefix + "/"


def _eclipse_prefix() -> str:
    """The Eclipse silver prefix, from the Eclipse converter's own declaration (its SILVER_PREFIX),
    never re-typed here."""
    _producer_path()
    from convert_eclipse_portfolios_to_silver import SILVER_PREFIX
    if not isinstance(SILVER_PREFIX, str) or not SILVER_PREFIX:
        raise InflectionRefused("REFUSED: INF Eclipse producer prefix unavailable")
    return SILVER_PREFIX.rstrip("/") + "/"


def load_inf_sources(s3, as_of: str) -> dict:
    hs = _hs()
    bucket, eclipse, accounts_prefix = hs.INF_SOURCE_BUCKET, _eclipse_prefix(), _orion_dim_prefix("accounts_v2")
    overlay_date = hs._latest_complete_eclipse_date(s3, bucket, as_of)
    accounts_date = hs._latest_date_partition(s3, bucket, accounts_prefix, date_prefix="snapshot_date=", as_of=as_of)
    if overlay_date is None or accounts_date is None:
        raise InflectionRefused("REFUSED: INF custody or overlay partition unavailable at cutoff")
    positions_date, positions_key = hs._inf_positions_source_key(s3, as_of)
    if positions_date != accounts_date:
        raise InflectionRefused("REFUSED: INF positions and accounts snapshots are not the same custody date")
    read = lambda key: hs._read_parquet(s3, bucket, key)  # noqa: E731
    frames = {
        "accounts": read(accounts_prefix + "snapshot_date=%s/data.parquet" % accounts_date),
        "positions": read(positions_key),
        "positions_key": positions_key,
        "simple": read(eclipse + "%s/portfolios_simple.parquet" % overlay_date),
        "full": read(eclipse + "%s/portfolios_full.parquet" % overlay_date),
        "models": read(eclipse + "%s/models.parquet" % overlay_date),
        # The Opal models (3, 5, 6, ...) are named only in model_composition; the firm's own
        # models (IWM ...) only in models. Both feed the name census; neither is a membership source.
        "model_composition": read(eclipse + "%s/model_composition.parquet" % overlay_date),
    }
    # Custody is required; an empty Eclipse overlay is a MEASURED absence at that partition (every
    # account then lands in Client with its reason), never a refusal of the custody build.
    for name in ("accounts", "positions"):
        if frames[name].empty:
            raise InflectionRefused("REFUSED: INF %s frame empty at its partition" % name)
    frames["overlay_rows"] = {name: int(len(frames[name])) for name in ("simple", "full", "models", "model_composition")}
    frames["custody_date"], frames["overlay_date"] = accounts_date, overlay_date
    return frames


def eclipse_membership_capture(path) -> dict:
    """The retained point-in-time Eclipse membership capture (4.0.0_SA_CRO 138fad2935: nine read-only
    accounts/simple/list calls over every portfolio, under a grant to the CRO only), as raw account
    id -> record, with the file's own provenance. It is consumed ONLY for accounts the silver export
    does not expose (the sleeve accounts of multi-account portfolios); it is not a pipeline."""
    raw = Path(path).read_bytes()
    doc = json.loads(raw)
    rows = doc if isinstance(doc, list) else (doc.get("rows") or doc.get("memberships") or [])
    by_account = {}
    for row in rows:
        account = _text(row.get("accountId"))
        if not account or row.get("isDeleted") not in (0, False, None):
            continue
        if account in by_account:
            raise InflectionRefused("REFUSED: INF membership capture names an account twice")
        by_account[account] = {"portfolio_id": _text(row.get("portfolioId")), "model_id": _text(row.get("modelId")),
                               "model_name": _text(row.get("model")), "is_sleeve": bool(row.get("isSleeve")),
                               "sleeve_type": _text(row.get("sleeveType")), "status": _text(row.get("status"))}
    return {"accounts": by_account, "provenance": {"path": str(path), "sha256": hashlib.sha256(raw).hexdigest(),
                                                  "byte_length": len(raw), "rows": len(rows),
                                                  "record": "4.0.0_SA_CRO IRPT_INF_ECLIPSE_MEMBERSHIP_CAPTURE_20260923 @138fad2935"}}


def _eclipse_overlay(frames, capture=None) -> "tuple[dict, dict]":
    """raw account_id -> one portfolio membership record, plus model id -> name.

    `capture` (eclipse_membership_capture) supplies membership for accounts ABSENT from the silver
    export only; an account the export names keeps the export's record, so the capture never
    overrides the pipeline's own source."""
    simple, full, models = frames["simple"], frames["full"], frames["models"]
    overlay, names = {}, {}
    if capture:
        for account, rec in capture["accounts"].items():
            overlay.setdefault(account, []).append({
                "portfolio_id": rec["portfolio_id"], "model_id": rec["model_id"], "model_name": rec["model_name"],
                "managed_value": None, "excluded_value": 0.0, "full_row": True, "portfolios_for_account": 1,
                "declared_members": 1.0, "exposed_members": 1, "membership_complete": True,
                "source": "capture", "sleeve_type": rec["sleeve_type"], "is_sleeve": rec["is_sleeve"]})
            if rec["model_id"] and rec["model_name"]:
                names.setdefault(rec["model_id"], rec["model_name"])
    if simple.empty or "account_id" not in simple.columns or "id" not in simple.columns:
        return overlay, names
    if "id" not in full.columns:
        raise InflectionRefused("REFUSED: INF portfolios_full lacks portfolio id")
    full_by_id = full.drop_duplicates("id").set_index("id")
    for table in (models, frames.get("model_composition", pd.DataFrame())):
        if len(table) and {"id", "name"}.issubset(table.columns):
            for row in table.to_dict("records"):
                if _text(row["id"]):
                    names.setdefault(_text(row["id"]), _text(row.get("name")))
    # Key both censuses by the TEXT identity the rest of the builder uses: accounts_v2 and
    # portfolios_simple carry integer account ids, and an int-keyed Series read with a str
    # returns the default silently (measured 2026-09-23: 786 of 786 mapped accounts fell to Client).
    keyed = simple.assign(_account=simple["account_id"].map(_text))
    per_account = keyed.groupby("_account")["id"].nunique()
    per_portfolio = keyed.groupby("id")["_account"].nunique()
    for row in simple.to_dict("records"):
        account = _text(row.get("account_id"))
        if not account:
            continue
        if account in overlay and overlay[account][0].get("source") == "capture":
            overlay[account] = []  # the export names this account: its record wins over the capture's
        portfolio = row.get("id")
        f = full_by_id.loc[portfolio] if portfolio in full_by_id.index else None
        model_id = row.get("model_id")
        try:
            model_id = str(int(model_id)) if model_id is not None and not pd.isna(model_id) else ""
        except (TypeError, ValueError):
            model_id = ""
        declared = _num(f.get("num_of_associated_accounts")) if f is not None else None
        exposed = int(per_portfolio.get(portfolio, 0))
        record = {
            "portfolio_id": _text(portfolio), "model_id": model_id, "model_name": names.get(model_id, ""),
            "managed_value": _num(f.get("managed_value")) if f is not None else None,
            "excluded_value": _num(f.get("excluded_value")) if f is not None else None,
            "full_row": f is not None, "portfolios_for_account": int(per_account.get(account, 0)),
            "declared_members": declared, "exposed_members": exposed,
            "membership_complete": (f is not None and declared is not None and declared == exposed == 1
                                    and int(per_account.get(account, 0)) == 1),
        }
        overlay.setdefault(account, []).append(record)
    return overlay, names


def build_inf_meshed(s3, as_of: str) -> "tuple[list, dict]":
    if dt.date.fromisoformat(as_of).isoformat() != as_of:
        raise InflectionRefused("REFUSED: ISO as_of required")
    hs = _hs()
    from inf_positions import validate_inf_actual_positions
    firm_id = _firm_id()
    frames = load_inf_sources(s3, as_of)
    custody_date, overlay_date = frames["custody_date"], frames["overlay_date"]
    # THE ORION DAILY KEY HOLDS THE PRIOR CLOSE (4.0.0_SA_CRO 10f3cf6f9f, measured 3 of 3; CTO
    # INF-CLOCK-01): the snapshot key is the REQUEST date, the valuation date is the prior trading
    # day. The validator still binds rows to the key they were written under; the clocks the
    # reader shows carry the valuation date, with the key recorded beside it. Values unchanged.
    valuation_date = hs.tcal.prev_trading_day(dt.date.fromisoformat(custody_date)).isoformat()
    accounts, positions = frames["accounts"], frames["positions"]
    if "account_id" not in accounts.columns or accounts["account_id"].duplicated().any():
        raise InflectionRefused("REFUSED: INF custody census ambiguous")
    currency_authority, currency_refusal = _try_currency_authority()
    expected = {str(a) for a in accounts["account_id"] if not pd.isna(a)}
    # CTO 101302: each ACCOUNT node's own mask -- accounts_v2.account_number and account_type, the columns the
    # directory masks from, keyed by account_id, the raw key this builder mints from.
    account_masks = hs.own_account_masks(firm_id, zip(
        accounts["account_id"],
        accounts["account_number"] if "account_number" in accounts.columns else [""] * len(accounts),
        accounts["account_type"] if "account_type" in accounts.columns else [""] * len(accounts)))
    source_currency = "currency" in positions.columns and "currency" in accounts.columns
    validated, controls = validate_inf_actual_positions(
        positions, accounts, expected_account_ids=expected, custody_as_of=custody_date, valuation_as_of=custody_date,
        currency_authority=currency_authority,
        candidate_unattested=currency_authority is None and not source_currency)
    currency_status = controls["currency_status"]
    capture_path, capture_vintage = hs.retained_capture(
        s3, "IRPT_INF_ECLIPSE_MEMBERSHIP_SNAPSHOT", "eclipse", firm_id, "eclipse_membership_map",
        "membership_map.json", as_of)
    # An ABSENT capture REFUSES the build (Andrew-direct 2026-09-24 ~12:5xZ, card 6): the retained Eclipse
    # membership map is a required input until it is a receipted source object under the holdings migration.
    # Measured 2026-09-24 06:2xZ: with the variable unset this builder silently produced a candidate with
    # models_whole_from_capture 35 -> 0 that validated, reconciled and passed every gate.
    if capture_path is None:
        raise InflectionRefused("REFUSED: INF Eclipse membership capture not supplied "
                                "(IRPT_INF_ECLIPSE_MEMBERSHIP_SNAPSHOT unset and no landed capture at or before %s) -- a "
                                "retained input this build requires (Andrew-direct 2026-09-24 card 6)" % as_of)
    capture = eclipse_membership_capture(capture_path)
    overlay, model_names = _eclipse_overlay(frames, capture)
    dir_ids = hs._directory_account_ids(s3, hs.firm_bucket_map().get(firm_id, ""), firm_id)
    client_path, MODELS_PATH = hs._client_hierarchy_path(), hs.taxonomy_path("Models")  # noqa: N806  (registry, CTO TAXONOMY-PATH-01)
    tolerance = hs.RECON_TOLERANCE_USD

    nodes, withheld, split_unattributed = [], [], []
    custody_ids, assigned_ids, value_by_account = set(), set(), {}
    census = {"models_whole": 0, "models_whole_from_capture": 0, "models_split": 0, "client": 0, "client_no_portfolio": 0, "client_no_model": 0,
              "client_incomplete_membership": 0, "client_values_do_not_tie": 0, "model_leaves": 0,
              "positions_shown": 0, "drill_withheld": 0, "split_positions_unattributed": 0}
    dir_matched, total_before = 0, 0.0
    positions_by_account = {k: g for k, g in validated.groupby("account_id")}
    common = (PRODUCER, "accounts_v2.current_value (custody) x eclipse portfolios_simple (membership)", 1, 1, "measured")
    # the positions_mv object's receipted sha256, ONLY when the published contract admits CUSTODY_UNITS
    units_rev = (hs._receipt_sha(s3, hs.INF_SOURCE_BUCKET, frames.get("positions_key"))
                 if hs.custody_units_admitted() and frames.get("positions_key") else None)

    def custody_units(row, parent_id):
        """CUSTODY_UNITS from the Orion positions_mv row's own current_shares (beside the current_value this
        node's amount reads), on the account's opaque id at the node's custody clock (valuation_date: the prior trading
        day the snapshot key holds -- the row's as_of_date is the snapshot key, not the close it states), with the
        positions_mv object's receipted sha256 as the revision. None -> no fact."""
        if not units_rev:
            return None
        fact = hs._custody_units_fact({"Units": row.get("current_shares"), "_source_as_of": valuation_date},
                                      parent_id.split(":")[0], units_rev)
        return [fact] if fact else None

    def emit_positions(parent_id, raw_account, parent_value, path, extra_facts=()):
        rows = positions_by_account.get(raw_account)
        shown = 0
        for row in (rows.sort_values("id").to_dict("records") if rows is not None else []):
            position_id = hashlib.sha256((parent_id + "|" + str(row["id"])).encode("utf-8")).hexdigest()
            nodes.append(hs._node(parent_id + ":position:" + position_id[:32], parent_id, len(parent_id.split(":")) , "SECURITY",
                                  "OBSERVED", float(row["current_value"]), "USD", "PARENT_NODE", parent_value, None, None,
                                  PRODUCER, "native Orion positions_mv row reconciled to accounts_v2 total", 1, 1, "measured",
                                  security_id={"namespace": "VENDOR", "value": str(row["product_id"])},
                                  classification=hs._unknown_classification(
                                      ["ticker=%s" % _text(row.get("ticker")), "Native Orion product identity; no inferred price"]
                                      # the row's own Orion name: the ticker is often a masked CUSIP (06xxxx4Y5), so this
                                      # is what names the row on screen and what the classifier reads as the name
                                      + (["company=%s" % " ".join(_text(row.get("name")).split())] if _text(row.get("name")) else [])
                                      + list(extra_facts),
                                      hierarchy_path=path),
                                  valuation_facts=custody_units(row, parent_id)))
            shown += 1
        return shown

    for control in controls["reconciliation"]:
        raw_account = control["account_id"]
        account_value = float(control["independent_value"])
        account_id = hs.opaque_id("account", firm_id, raw_account)
        custody_ids.add(account_id)
        value_by_account[account_id] = account_value
        total_before += account_value
        if dir_ids is not None and account_id in dir_ids:
            dir_matched += 1
        nodes.append(hs._node(account_id, None, 0, "ACCOUNT", "OBSERVED", account_value, "USD", "UNIQUE_CUSTODY_TOTAL",
                              account_value, None, None, *common,
                              drill_refs=[{"ref_kind": "ACCOUNT", "ref_id": account_id}],
                              classification=hs._unknown_classification(
                                  ["INF custody: Orion accounts_v2 snapshot_date=%s holds the prior close; valuation date %s"
                                   % (custody_date, valuation_date)])))
        records = overlay.get(raw_account, [])
        rec = records[0] if len(records) == 1 else None
        managed = rec["managed_value"] if rec else None
        excluded = rec["excluded_value"] if rec else None
        nothing_excluded = rec is not None and excluded is not None and abs(excluded) <= tolerance
        ties = (rec is not None and managed is not None and excluded is not None
                and abs(managed + excluded - account_value) <= tolerance)
        reason = None
        if not records:
            reason = "client_no_portfolio"
        elif rec is None or not rec["membership_complete"]:
            reason = "client_incomplete_membership"
        elif not rec["model_id"]:
            reason = "client_no_model"
        elif not nothing_excluded and not ties:
            # An excluded part exists but Eclipse's parts do not sum to Orion's custody total, so
            # the managed share cannot be stated; the model membership is recorded in the facts.
            reason = "client_values_do_not_tie"
        if reason is None and nothing_excluded:
            # Whole-account model membership, measured: Eclipse excludes nothing from the model, so
            # the whole custody value is modeled whatever the two valuation clocks say. The
            # managed-vs-custody difference is stated, never used.
            sleeve_id, leaf_id = account_id + ":models", account_id + ":model:" + rec["model_id"]
            if rec.get("source") == "capture":
                facts = ["Eclipse portfolio %s -> model %s (%s) via the retained accounts/simple/list capture "
                         "(4.0.0_SA_CRO 138fad2935): this account is a %s sleeve of a multi-account portfolio; the "
                         "portfolio-level managed/excluded split is not stated at sleeve grain, the whole sleeve "
                         "account is modeled" % (rec["portfolio_id"], rec["model_id"], rec["model_name"], rec["sleeve_type"] or "Normal")]
                census["models_whole_from_capture"] += 1
            else:
                facts = ["Eclipse portfolio %s -> model %s (%s); excluded_value 0; managed_value %.2f vs custody %.2f at "
                         "two clocks" % (rec["portfolio_id"], rec["model_id"], rec["model_name"], managed or 0.0, account_value)]
            nodes.append(hs._node(sleeve_id, account_id, 1, "CATEGORY", "OBSERVED", account_value, "USD", "PARENT_NODE",
                                  account_value, None, None, *common, classification=hs._unknown_classification(facts, hierarchy_path=MODELS_PATH)))
            nodes.append(hs._node(leaf_id, sleeve_id, 2, "MODEL_LEAF", "ASSIGNED", account_value, "USD", "PARENT_NODE", account_value,
                                  None, None, PRODUCER, "portfolios_simple.model_id (Eclipse); whole account", 1, 1, "measured",
                                  model_id={"namespace": "ECLIPSE_MODEL_ID", "value": rec["model_id"]},
                                  drill_refs=[{"ref_kind": "MODEL", "ref_id": rec["model_id"]}],
                                  classification=hs._unknown_classification(
                                      ["model_name=%s" % rec["model_name"],
                                       "is_opal=%s" % (int(rec["model_id"]) in hs.OPAL_ECLIPSE_MODEL_IDS)], hierarchy_path=MODELS_PATH)))
            census["positions_shown"] += emit_positions(leaf_id, raw_account, account_value, MODELS_PATH)
            census["models_whole"] += 1
            census["model_leaves"] += 1
            assigned_ids.add(account_id)
            continue
        if reason is None:
            # Split account (CTO rulings batch 96 items 2-3): Eclipse states a managed part and an excluded part
            # that tie to custody; Orion does not say which part a position sits in. The account's positions are a
            # measured fact of custody, so they are listed -- directly under the ACCOUNT, attributed to neither
            # part -- and the two parts are the ASSIGNED view beside them. The tree's sum rule is per
            # (parent, basis): the ASSIGNED children (managed + excluded) and the OBSERVED children (the
            # positions) each sum to the account, and the two are never added together.
            sleeve_id, leaf_id = account_id + ":models", account_id + ":model:" + rec["model_id"]
            note = ("PART NOT STATED BY THE FEED: Orion marks every position is_managed and does not say which sit in "
                    "the excluded part (managed %.2f, excluded %.2f); the positions are listed under the account, "
                    "attributed to neither part" % (managed, excluded))
            nodes.append(hs._node(sleeve_id, account_id, 1, "CATEGORY", "ASSIGNED", managed, "USD", "PARENT_NODE", account_value,
                                  None, None, *common, classification=hs._unknown_classification(
                                      ["Eclipse portfolio %s managed part" % rec["portfolio_id"], note], hierarchy_path=MODELS_PATH)))
            nodes.append(hs._node(leaf_id, sleeve_id, 2, "MODEL_LEAF", "ASSIGNED", managed, "USD", "PARENT_NODE", managed, None, None,
                                  PRODUCER, "portfolios_simple.model_id (Eclipse); managed part only", 1, 1, "measured",
                                  model_id={"namespace": "ECLIPSE_MODEL_ID", "value": rec["model_id"]},
                                  drill_refs=[{"ref_kind": "MODEL", "ref_id": rec["model_id"]}],
                                  classification=hs._unknown_classification(
                                      ["model_name=%s" % rec["model_name"],
                                       "is_opal=%s" % (int(rec["model_id"]) in hs.OPAL_ECLIPSE_MODEL_IDS)], hierarchy_path=MODELS_PATH)))
            nodes.append(hs._node(account_id + ":client", account_id, 1, "CATEGORY", "ASSIGNED", excluded, "USD", "PARENT_NODE",
                                  account_value, None, None, *common, classification=hs._unknown_classification(
                                      ["Eclipse portfolio %s excluded part in Client" % rec["portfolio_id"], note], hierarchy_path=client_path)))
            census["positions_shown"] += emit_positions(
                account_id, raw_account, account_value, None,
                extra_facts=["part=NOT_STATED: the custody feed does not state whether this position sits in the "
                             "managed or the excluded part of the account"])
            split_unattributed.append({"account_id": account_id, "managed_value": managed, "excluded_value": excluded})
            census["models_split"] += 1
            census["model_leaves"] += 1
            census["split_positions_unattributed"] += 1
            assigned_ids.add(account_id)
            continue
        sleeve_id = account_id + ":client"
        facts = {"client_no_portfolio": "Known custody in Client; no Eclipse portfolio for this account",
                 "client_incomplete_membership": "Known custody in Client; Eclipse portfolio membership incomplete or shared, no pro-rata inferred",
                 "client_no_model": "Known custody in Client; Eclipse portfolio carries no model",
                 "client_values_do_not_tie": "Known custody in Client; Eclipse portfolio %s names model %s (%s) with an excluded part, "
                                             "and managed + excluded does not tie to custody, so the modeled share is not stated"
                                             % (rec["portfolio_id"], rec["model_id"], rec["model_name"]) if rec else ""}[reason]
        nodes.append(hs._node(sleeve_id, account_id, 1, "CATEGORY", "OBSERVED", account_value, "USD", "PARENT_NODE", account_value,
                              None, None, *common, classification=hs._unknown_classification([facts], hierarchy_path=client_path)))
        census["positions_shown"] += emit_positions(sleeve_id, raw_account, account_value, client_path)
        census["client"] += 1
        census[reason] += 1

    holdouts = hs.holdout_block(custody_ids, assigned_ids, value_by_account, observable="MEASURED",
                                source="accounts_v2 snapshot_date=%s minus eclipse %s portfolios with a model and complete membership"
                                       % (custody_date, overlay_date))
    overlay_not_in_custody = sorted(a for a in overlay if hs.opaque_id("account", firm_id, a) not in custody_ids)
    coverage = {"nodes_resolved": census["models_whole"] + census["models_split"], "nodes_attempted": len(custody_ids),
                "remainder": {"amount": round(holdouts["value"]["value"], 2), "units": "USD",
                              "reason": "%d of %d custody account(s) carried in Client with membership unattributed"
                                        % (holdouts["account_count"], len(custody_ids))}}
    manifest = {"firm_id": firm_id, "source": "Orion accounts_v2 + positions_mv (custody) x Eclipse portfolios (membership)",
                "custody_snapshot_key": custody_date, "custody_valuation_date": valuation_date,
                "custody_date": valuation_date, "overlay_date": overlay_date, "date": valuation_date,
                "join_matched": coverage["nodes_resolved"], "join_attempted": len(custody_ids),
                "total_market_value": round(total_before, 2), "census": census, "drill_withheld": withheld,
                "split_positions_unattributed": split_unattributed,
                "overlay_accounts_not_in_custody": len(overlay_not_in_custody),
                "positions_outside_custody_census": {"accounts": controls["outside_requested_account_count"],
                                                     "positions": controls["outside_requested_position_count"]},
                "actual_position_controls": {k: v for k, v in controls.items() if k != "reconciliation"},
                "eclipse_models_named": len(model_names), "overlay_rows": frames["overlay_rows"],
                "eclipse_membership_capture": (capture["provenance"] if capture else None),
                "eclipse_membership_vintage": capture_vintage,
                "currency_status": currency_status,
                "currency_authority": currency_authority, "currency_refusal": currency_refusal,
                "directory_cross_check": {"matched": dir_matched, "attempted": len(custody_ids), "note": "INFORMATIONAL ONLY, not a join gate"}}
    if currency_status == "UNATTESTED":
        manifest["publication_refused"] = ("REFUSED: INF report currency unattested (%s); candidate only" % currency_refusal)
    hs.recompute_weights(nodes)
    stamped = hs.stamp_clocks(nodes, valuation_date, overlay_date)
    return nodes, {"coverage": coverage, "manifest": manifest, "source_completion_date": valuation_date,
                   "custody_as_of": valuation_date, "overlay_as_of": overlay_date, "holdouts": holdouts,
                   "account_masks": account_masks,
                   "assigned_without_custody": {
                       "account_count": len(overlay_not_in_custody),
                       "denominator": "%d Eclipse-mapped account(s) absent from accounts_v2" % len(overlay_not_in_custody),
                       "source": "eclipse %s portfolios_simple minus accounts_v2 %s" % (overlay_date, custody_date)},
                   "nodes_stamped": stamped}
