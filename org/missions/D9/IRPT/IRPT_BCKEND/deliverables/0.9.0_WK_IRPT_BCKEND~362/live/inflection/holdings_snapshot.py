#!/usr/bin/env python3
"""IRPT B12 / cell IB-s-12 -- the HOLDINGS SNAPSHOT runner.

Builds a per-firm `HoldingsSnapshot` from each partner's own custody/model data
(SmartX for 49F, Eclipse for INF, BD Rebalancer for COT) and lands it in the FIRM'S
OWN BUCKET -- the same destination discipline `directory_runner.py` (IB-s-1) already
established, reused here rather than re-derived (row IRPT_BCKEND-S1).

DESTINATION. The canonical opal_naming address builder resolves each private firm's
Gold Parquet history, bounded Platinum JSON, and version/hash-pinned manifest under
irpt/<firm>/<tier>/holdings/date=<date>/<content revision>.<extension>.
The --qa namespace uses holdings_qa. The destination is the canonical primary firm
home; legacy routed bucket aliases remain input reads only. One Platinum index records accepted
revisions; no legacy mutable snapshot/latest fallback is read or written.
Only this project's scoped handler serves an accepted snapshot after authorization.

NO LIVE VENDOR CALL. Every fact this module reads is an already-landed SILVER/GOLD
Parquet object in an Opal S3 bucket (SmartX/Eclipse/Rebalancer silver, already converted
by their own pipelines) -- no SmartX, Eclipse, Black Diamond or Orion CLIENT is imported
or reachable from here, and no HTTP call to a vendor endpoint is made.

THE JOIN IDENTITY (REWRITTEN BY IB-rt-3, CTO ruling 4). This runner MINTS NOTHING: every
opaque id comes from `_ids/ids.py`, the ONE normalizer, imported here and by the directory
runner and packaged into the `irpt-common` layer for the handlers. Round 1 said this module
"reuses directory_runner.opaque_id()'s EXACT formula" and that was TRUE and NOT ENOUGH: the
two copies agreed on the formula and read DIFFERENT RAW KEYS, so INF resolved 0 of 790 and
COT 0 of 946 against the directory (row W1-S7), and the `<firm>:acct:` prefix this module
minted made even 49F read 0 until a consumer stripped it (row W2-S11). Both are closed here:
the raw key per firm is DECLARED in `_ids/raw_keys.json` and read by BOTH producers, and the
node id is the bare opaque id -- the firm is `scope.firm_id`, a separate typed field the
contract already requires. No raw custodian account number crosses either module.

THE RECURSIVE EXPANSION MECHANISM IS THIS MODULE'S OWN, NOT `build_dim_model_portfolio.
decompose()` -- read, and DELIBERATELY not inherited (PRD v0.4 B12 row: "the old helper's
empty-list cycle handling is invalid"). `decompose()` returns `[]` on a cycle hit, which
SILENTLY DROPS the cyclic branch's weight; `expand_model()` below retains that weight as
UNRESOLVED MASS instead, does the same for a missing child, applies every edge weight
EXACTLY ONCE (multiplied down the recursion, never reapplied), and never renormalizes a
surviving sibling to compensate for a lost one -- a lost 30% branch leaves the other 70%
at its ORIGINAL fraction, not rescaled to 100%. Opal attribution is carried PER LEAF from
that leaf's OWN roster flag, independent of its wrapper's flag in either direction (an
Opal wrapper over a non-Opal leaf keeps the leaf non-Opal; an Opal leaf under a non-Opal
wrapper stays Opal) -- both directions are adversarial-fixture tested.

BASES NEVER SPLICED. Every node carries exactly one `basis` (OBSERVED / ASSIGNED /
TARGET): a custody-observed position, an account-to-model ASSIGNMENT weight, or a
recursively-expanded model TARGET weight are three different numbers and this module
never sums across them into one pie (`assert_bases_not_spliced` is the mechanical check;
S12-AC1 arm (c) exercises it directly).

BOUNDS observed structurally: no model's global AUM (Eclipse `model_composition.model_aum`,
a firm-wide cached figure) is ever read as an account's or client's holding -- this module
never opens that column; parallel position/asset tables are never unioned (COT holdings
duplicates are deduplicated only under an equal-value-or-null policy, with units and dates
checked, and an unequal duplicate pair is an explicit exception, never a silent keep-first
-- the same DC1 shape `build_dim_model_portfolio.collapse_relationship_grain` uses, applied
here rather than imported, because this module's grain and columns differ from BD's);
`vendor_account_supervised` (COT `fact_holdings["Account Supervised"]`) is carried in its
OWN field and is NEVER read as Opal `fee_taking_status`.

Usage:
  python holdings_snapshot.py --qa --firms all --dry-run
  python holdings_snapshot.py --qa --firms all --upload
  python holdings_snapshot.py --firms cottonwood --as-of 2026-09-09 --upload
"""
from __future__ import annotations

import argparse
import copy
import datetime as dt
import hashlib
import io
import json
import math
import os
import re
import sys
from decimal import Context, Decimal, InvalidOperation
from numbers import Integral
from pathlib import Path

import pandas as pd

_HERE = Path(__file__).resolve().parent
_REPO = _HERE.parents[4]

if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
if str(_REPO / "lib") not in sys.path:
    sys.path.insert(0, str(_REPO / "lib"))
import trading_calendar as tcal  # noqa: E402
from opal_naming import lookup  # noqa: E402

# THE ONE OPAQUE-ID NORMALIZER (IB-rt-3). Same file the directory runner imports and the
# same file the `irpt-common` layer packages for the Lambdas -- one definition, three readers.
_IDS_DIR = _REPO / "infra" / "aws" / "lambda" / "investor-reporting" / "_ids"
if str(_IDS_DIR) not in sys.path:
    sys.path.insert(0, str(_IDS_DIR))
import ids as _ids  # noqa: E402
_HOLDINGS_DIR = _REPO / "infra" / "aws" / "lambda" / "investor-reporting" / "holdings"
if str(_HOLDINGS_DIR) not in sys.path:
    sys.path.insert(0, str(_HOLDINGS_DIR))
from publication import HoldingsPublication  # noqa: E402
from source_inputs import VersionedInputs  # noqa: E402
from inf_positions import validate_inf_actual_positions  # noqa: E402
_REPORTS_DIR = _REPO / "infra" / "aws" / "lambda" / "investor-reporting" / "reports"
if str(_REPORTS_DIR) not in sys.path:
    sys.path.insert(0, str(_REPORTS_DIR))
from currency_authority import bind_report_currency  # noqa: E402
import holdings_49f  # noqa: E402  (49F custody x SmartX membership; registered in BUILDERS below)
import holdings_inf  # noqa: E402  (INF Orion custody x Eclipse membership; registered in BUILDERS below)
import holdings_membership  # noqa: E402  (COT Rebalancer membership at the account grain, used by build_cot)

SCHEMA_VERSION = "1.0"
HOLDINGS_REVISION_PREFIX = "irpt-hld"
ID_NAMESPACE = os.environ.get("IRPT_DIRECTORY_ID_NAMESPACE", "IRPT_DIRECTORY_ID_NS_V1")
# THE PUBLISHED CONTRACT IS THE ONE THIS RUNNER VALIDATES AGAINST (CTO ruling 1, one carrier).
# Until IB-rt-7 this read `infra/aws/lambda/investor-reporting/_contracts/`, a SECOND copy of a
# contract that is published under `docs/contracts/investor-reporting/v1/` -- and the two had
# already diverged (the published copy carries `contract_version` and `x-contract-version`; the
# lambda-tree copy does not). A producer validating against the unpublished copy can satisfy it
# and still answer something the published contract forbids, which is the whole failure mode
# "one carrier" exists to remove. The lambda-tree copy stays where it is: it is read by the
# DEPLOYED functions through `/opt/python/irpt_contracts` (performance/normalize.py's own
# resolution order) and is not this runner's to move.
CONTRACT_PATH = (_REPO / "docs" / "contracts" / "investor-reporting" / "v1"
                 / "HoldingsSnapshot.schema.json")
FIRM_REGISTRY_PATH = _REPO / "data" / "firm_registry.json"
FIRM_CONFIG_PATH = (_REPO / "infra" / "aws" / "lambda-edge" / "_shared" / "firm-config.mjs")

PROD_PREFIX = "investor-reporting/holdings"
QA_PREFIX = "investor-reporting/qa/holdings"
RECON_TOLERANCE_USD = 0.01  # to the cent, matching the acceptance clause's own phrase

# 9 Opal model IDs in Eclipse (ADVI_ECLDAT.002 confirmed list; cited, not re-derived --
# data/inf/scripts/gold/INF_E_00.eclipse_model_portfolios.py OPAL_ECLIPSE_MODEL_IDS).
OPAL_ECLIPSE_MODEL_IDS = frozenset([3, 5, 6, 7, 8, 9, 10, 28, 29])

# The 5-enum canonical asset-category vocabulary (data/mdpf/scripts/gold/
# mdpf_category_registry.py ASSET_CATEGORIES). READ, NEVER MINTED: this module tags a
# node's classification.hierarchy_path with one of these five strings and never a sixth.
ASSET_CATEGORIES = ("models", "strategy", "alternative", "insurance", "client")

# THE L0 CATEGORY GROUPING (CTO ruling msg 102475, cell IB-mr-202): the portal's Holdings card
# drills L-1 ACCOUNT -> L0 CATEGORY (Models / SMAs / Client, one per category present, each
# carrying the sum of its own children) -> L1 contents -- the PRODUCER serves every total, the
# page never sums. A shape change only: which node a leaf attaches under, never its amount, its
# classification or its membership rule.
CATEGORY_LABELS = {"models": "Models", "smas": "SMAs", "client": "Client"}


def category_key_for_path(hierarchy_path) -> str:
    """Which L0 CATEGORY a leaf's hierarchy_path first segment maps to: Models > ... -> models;
    SMA -> smas; anything else (including the Client residual) -> client (CTO ruling IB-mr-202)."""
    first = (hierarchy_path or [None])[0]
    if first == "Models":
        return "models"
    if first == "SMA":
        return "smas"
    return "client"

FORBIDDEN_VENDOR_MODULE_TOKENS = (
    "ycharts", "yc_client", "blackdiamond_client", "black_diamond_client", "bd_api", "bdapi",
    "orion_client", "smartx_client", "eclipse_client", "pershing", "schwab_api",
    "kimi", "vendor_client", "requests", "urllib.request", "httpx",
)


# --------------------------------------------------------------------------- identity
# "IDENTICAL to directory_runner.opaque_id" was a CLAIM about two copies, and round 1 is what
# happens when a claim like that is all there is: the two copies agreed on the formula and
# disagreed on the RAW KEY, so INF and COT resolved 0 of 790 and 0 of 946 (row W1-S7). There
# is now ONE definition, in `_ids/ids.py`, and this module IMPORTS it (IB-rt-3). The name
# `opaque_id` is kept because every call site below already uses it; it is a BINDING, not an
# implementation, and no `sha256(...)[:24]` remains in this file.
opaque_id = _ids.opaque


# GENERATED by lib/opal_naming.py from infra/logic/registry@f1800b494773650a over scopes.json [firm_bucket_map] -- do not edit by hand; regenerate with: python lib/opal_naming.py generate --out <dir> --target data/assets/scripts/gold/investor_reporting/holdings_snapshot.py
def firm_bucket_map() -> "dict[str, str]":
    """Every tenant's bucket, generated from the identity registry (LGIC_ENFORCE DEC-5)."""
    return {
        "49financial": "opal-data-bd",
        "inflection": "opal-data-inf",
        "cottonwood": "opal-data-cot",
        "mockadv": "opal-data-bd",
        "demo": "opal-data-demo",
    }
# END GENERATED [firm_bucket_map]


def client_firms(registry_path: "Path | None" = None) -> "list[dict]":
    reg = json.loads((registry_path or FIRM_REGISTRY_PATH).read_text(encoding="utf-8"))
    return [f for f in reg["firms"] if f.get("enabled") is True and f.get("kind") == "client"]


# THE SOURCE VENDOR KEYS (UIC-14, CTO ruling msg 102443, cell IB-mr-203): the portal turns keys into
# words, so this producer must write its own source vendor keys into its output rather than the
# portal hand-typing a firm/function-name map (refused by the LGIC naming gate, CLAUDE.md rule 30).
# Registry file: infra/logic/registry/systems.json -- every VENDOR-class row's `key` there is a token
# this module never types itself; it is matched, word-bounded and case-insensitive, against each
# builder's OWN pre-existing free-text `manifest["source"]` description (already written by
# build_49f/build_inf/build_cot for a different reason -- never a new per-firm constant). A source
# naming no registry vendor at all is REFUSED, never silently labelled.
SYSTEMS_REGISTRY_PATH = _REPO / "infra" / "logic" / "registry" / "systems.json"


def registry_vendor_keys(registry_path: "Path | None" = None) -> "list[str]":
    """Every VENDOR-class key in the identity registry's systems.json, read fresh (never cached as a
    per-firm constant)."""
    reg = json.loads((registry_path or SYSTEMS_REGISTRY_PATH).read_text(encoding="utf-8"))
    return sorted({s["key"] for s in reg["systems"] if s.get("class") == "VENDOR"})


def source_vendor_keys(source_text: "str | None", registry_path: "Path | None" = None) -> "list[str]":
    """Which registry VENDOR keys a builder's own `manifest["source"]` text names -- word-bounded,
    case-insensitive, sorted. REFUSED (raises ValueError) when the text names none: an unrecognized
    source is refused, never labelled with a guess."""
    text = source_text or ""
    found = sorted(v for v in registry_vendor_keys(registry_path)
                   if re.search(r"(?<![a-z0-9])%s(?![a-z0-9])" % re.escape(v), text, re.IGNORECASE))
    if not found:
        raise ValueError("REFUSED: source %r names no infra/logic/registry/systems.json VENDOR key" % text)
    return found


def _pad10(s) -> str:
    """The eight-to-ten-digit zero-pad grammar (b04_account_model_membership._pad),
    applied here rather than imported (different module, same rule)."""
    return str(s).strip().zfill(10)


# --------------------------------------------------------------------------- recursive expansion
class ExpansionResult:
    __slots__ = ("leaves", "unresolved_mass", "events")

    def __init__(self, leaves, unresolved_mass, events):
        self.leaves = leaves            # list[(leaf_model_id, weight, is_opal)]
        self.unresolved_mass = unresolved_mass  # float, 0..1 share of the CALLER's weight
        self.events = events            # list[str] -- cycle/missing narration


def expand_model(model_id, blend_children, roster_is_opal, *, weight: float = 1.0,
                 seen: "frozenset" = frozenset()) -> ExpansionResult:
    """Resolve `model_id` to its leaves at the given inbound `weight`, applying every
    edge weight EXACTLY ONCE (multiplied down the recursion, never reapplied at any other
    point). A leaf (no declared children) resolves to itself. A CYCLE (model_id already
    on the current path) or a MISSING NODE (not present in `roster_is_opal`) RETAINS its
    weight as unresolved mass -- it is never dropped to an empty list and never silently
    folded into a sibling. Surviving siblings keep their ORIGINAL weight fraction: this
    function never renormalizes remaining children to compensate for a lost one.
    """
    if model_id in seen:
        return ExpansionResult([], weight, [
            "CYCLE at %r (already on path %r) -- %.6f of inbound weight retained as "
            "unresolved mass, NOT dropped" % (model_id, tuple(seen), weight)])
    if model_id not in roster_is_opal:
        return ExpansionResult([], weight, [
            "MISSING NODE %r -- absent from the roster/blend universe -- %.6f of inbound "
            "weight retained as unresolved mass" % (model_id, weight)])
    children = blend_children.get(model_id)
    if not children:
        return ExpansionResult([(model_id, weight, bool(roster_is_opal[model_id]))], 0.0, [])
    nxt = seen | {model_id}
    leaves = []
    unresolved = 0.0
    events = []
    for child_id, child_w in children:
        sub = expand_model(child_id, blend_children, roster_is_opal, weight=weight * child_w, seen=nxt)
        leaves.extend(sub.leaves)
        unresolved += sub.unresolved_mass
        events.extend(sub.events)
    return ExpansionResult(leaves, unresolved, events)


def assert_bases_not_spliced(nodes: "list[dict]") -> None:
    """S12-AC1 arm (c), the mechanical check: every node carries EXACTLY one basis, and the bases are
    never added into one number.

    A PIE is the children of one parent IN ONE BASIS. A parent normally carries one pie. It may carry
    an OBSERVED pie and an ASSIGNED pie ONLY as two complete views of the same money: each must
    balance to the parent's own amount ON ITS OWN, to the cent (CTO rulings batch 96 item 3(b): an
    Inflection split account lists its custody positions beside Eclipse's managed and excluded parts).
    A mix that balances only when the bases are added together is the splice this refuses; TARGET
    never shares a parent with another basis; the roots carry one basis."""
    sums: "dict[object, dict]" = {}
    amounts = {}
    for n in nodes:
        b = n.get("basis")
        if b not in ("OBSERVED", "ASSIGNED", "TARGET"):
            raise ValueError("node %r carries basis %r, not exactly one of OBSERVED/ASSIGNED/TARGET"
                             % (n.get("node_id"), b))
        amounts[n.get("node_id")] = (n.get("amount") or {}).get("value")
        group = sums.setdefault(n.get("parent_node_id"), {})
        group[b] = group.get(b, 0.0) + float((n.get("amount") or {}).get("value") or 0.0)

    def two_views(parent, groups):
        own = amounts.get(parent)
        return (parent is not None and "TARGET" not in groups and isinstance(own, (int, float))
                and all(abs(total - own) <= RECON_TOLERANCE_USD for total in groups.values()))

    spliced = {p: set(groups) for p, groups in sums.items() if len(groups) > 1 and not two_views(p, groups)}
    if spliced:
        raise ValueError("REFUSED: a pie mixes bases under parent(s) %r -- %r" % (list(spliced), spliced))


# --------------------------------------------------------------------------- COT duplicate policy
def dedupe_cot_holdings(df: pd.DataFrame, key_cols, value_col, date_col=None, units_col=None):
    """The DECLARED equal-value/null duplicate policy (PRD v0.4 B12: 'COT duplicates
    deduplicated only under a declared equal-value/null policy with units and dates
    checked, incompatible duplicates are explicit exceptions'). Same DC1 shape as
    `build_dim_model_portfolio.collapse_relationship_grain` (dedupe on a key, ASSERT
    equal value among duplicates, never silent keep-first) -- applied here rather than
    imported, because the columns and firm differ.

    Returns (deduped_df, exceptions: list[dict]) -- exceptions are NEVER silently
    dropped or averaged; each is a row describing the incompatible duplicate.
    """
    dup_mask = df.duplicated(subset=list(key_cols), keep=False)
    if not dup_mask.any():
        return df.copy(), []
    exceptions = []
    keep_idx = []
    grouped = df[dup_mask].groupby(list(key_cols), dropna=False)
    for key, grp in grouped:
        vals = pd.to_numeric(grp[value_col], errors="coerce").round(2)
        distinct_vals = set(vals.fillna("NULL_SENTINEL").tolist())
        dates_ok = True
        if date_col and date_col in grp.columns:
            dates_ok = grp[date_col].astype(str).nunique() <= 1
        units_ok = True
        if units_col and units_col in grp.columns:
            units_ok = grp[units_col].astype(str).nunique() <= 1
        if len(distinct_vals) <= 1 and dates_ok and units_ok:
            keep_idx.append(grp.index[0])
        else:
            exceptions.append({
                "key": dict(zip(key_cols, key if isinstance(key, tuple) else (key,))),
                "reason": "incompatible duplicate: %s distinct value(s), dates_equal=%s, units_equal=%s"
                         % (len(distinct_vals), dates_ok, units_ok),
                "row_count": int(len(grp)),
            })
            keep_idx.append(grp.index[0])  # carried, not dropped -- flagged as an exception instead
    out = pd.concat([df[~dup_mask], df.loc[keep_idx]], axis=0).sort_index()
    return out, exceptions


def validate_cot_actual_positions(holdings: pd.DataFrame, account_totals: pd.DataFrame,
                                  *, custody_as_of: str, valuation_as_of: str,
                                  expected_account_ids=None, holdings_row_origins=None,
                                  total_row_origins=None, currency_authority=None):
    """Pure, bounded COT source checks, BEFORE model joins or security consolidation.

    Returns (unique relationship-collapsed positions, internal evidence). This is
    not current-owner authorization, snapshot acceptance, or a published S2 schema.
    Currency is explicit in BOTH inputs or established by the exact shared COT
    attestation. Authority is retained separately; raw fields are never invented.
    B03's 1bp flag/VARIANCE-EXPLAINED is never an admission substitute.
    Optional row origins are (private source-object reference, zero-based physical
    row ordinal) pairs. Without them row_index is only the input-frame ordinal,
    NOT proof of a physical object location. An explicit expected_account_ids set
    checks an independently supplied RAW account census; current authorization
    and canonical-to-source binding stay P-owned. Omitting it never implies the
    two frames jointly establish selected-account completeness.

    Internal evidence uses RAW account/asset IDs, not authorized canonical IDs or
    public receipt references. It must NOT be passed directly to a Y factory or
    exposed through a public response. Exact decimal text preserves source numeric
    precision, not an original CSV spelling unavailable in a typed Parquet column.
    P must bind each source-object reference to exact retained receipt bytes before
    admission; this pure helper cannot prove a caller's receipt or census authority.
    Missing currency/units means refusal,
    not a synthetic zero or a claim that all live sources have these columns.
    """
    for date in (custody_as_of, valuation_as_of):
        try:
            valid = isinstance(date, str) and dt.date.fromisoformat(date).isoformat() == date
        except ValueError:
            valid = False
        if not valid:
            raise ValueError("REFUSED: COT missing or invalid actual source date")
    if custody_as_of != valuation_as_of:
        raise ValueError("REFUSED: COT custody/independent total vintage mismatch")
    if currency_authority is not None:
        from opal_naming import lookup
        if currency_authority != bind_report_currency(lookup("cottonwood")["long"])["currency_authority"]:
            raise ValueError("REFUSED: COT currency authority mismatch")
    attested = currency_authority is not None

    def valid_currency(value):
        if isinstance(value, str) and value == "USD":
            return True
        return attested and (value is None or (not isinstance(value, (list, dict)) and pd.isna(value)))

    numeric = ("Market Value", "Unaccrued Market Value", "Accrual", "Units")
    currency_columns = set() if attested else {"Currency"}
    required = {"AccountID", "AssetID", "Relationship ID", *numeric} | currency_columns
    for frame, columns, label in (
        (holdings, required, "custody"),
        (account_totals, {"AccountID", "Account Market Value"} | currency_columns, "independent totals"),
    ):
        if not frame.columns.is_unique or not columns.issubset(frame.columns) or frame.empty:
            raise ValueError("REFUSED: COT %s missing required actual fields/rows (including explicit currency)"
                             % label)

    def identity(value):
        if isinstance(value, Integral) and not isinstance(value, bool):
            return str(value)
        if isinstance(value, str) and value.strip() == value and value:
            return value
        raise ValueError("REFUSED: COT missing/ambiguous source identity")

    def number(value):
        if isinstance(value, (bool, type(None))) or type(value).__name__ == "bool_":
            raise ValueError("REFUSED: COT unknown is not zero")
        try:
            result = Decimal(str(value))
        except (InvalidOperation, ValueError):
            raise ValueError("REFUSED: COT unknown is not zero") from None
        if (not result.is_finite() or not math.isfinite(float(result))
                or len(result.as_tuple().digits) > 1000 or abs(result.as_tuple().exponent) > 1000):
            raise ValueError("REFUSED: COT unknown is not zero")
        return result

    def optional(value):
        # Null-vs-value is distinct. Non-scalar cells are not a valid source field.
        if value is None or (pd.api.types.is_scalar(value) and pd.isna(value)):
            return None
        if not pd.api.types.is_scalar(value):
            raise ValueError("REFUSED: COT nonscalar consumed field")
        return (type(value).__name__, str(value))

    def origins(items, size):
        if items is None:
            return None
        if not isinstance(items, (list, tuple)) or len(items) != size:
            raise ValueError("REFUSED: COT source origin census mismatch")
        result = []
        for item in items:
            if (not isinstance(item, (list, tuple)) or len(item) != 2
                    or not isinstance(item[0], str) or not item[0].strip()
                    or type(item[1]) is not int or item[1] < 0):
                raise ValueError("REFUSED: COT invalid per-object source row origin")
            result.append(tuple(item))
        if len(set(result)) != len(result):
            raise ValueError("REFUSED: COT repeated physical source row origin")
        return result

    h_origins = origins(holdings_row_origins, len(holdings))
    t_origins = origins(total_row_origins, len(account_totals))

    tolerance = Decimal(str(RECON_TOLERANCE_USD))
    # Do not inherit a caller's decimal context (e.g. prec=6 would erase cents
    # on million-dollar accounts). Bounded inputs above fit this exact context.
    economics = Context(prec=4096)
    # Limit is binding even if a future caller accidentally loosens the constant.
    if not Decimal("0") <= tolerance <= Decimal("0.01"):
        raise ValueError("REFUSED: COT reconciliation tolerance exceeds 0.01 USD")
    h = holdings.copy(deep=True).reset_index(drop=True)
    for column in ("AccountID", "AssetID", "Relationship ID"):
        h[column] = h[column].map(identity)
    # A source row with absent currency cannot be laundered by an equal-MV twin.
    if any(not valid_currency(c) for c in h.get("Currency", [None] * len(h))):
        raise ValueError("REFUSED: COT unresolved/unsupported source currency")
    values = [{column: number(row[column]) for column in numeric}
              for row in h.to_dict("records")]
    for row in values:
        if economics.subtract(economics.subtract(row["Market Value"], row["Unaccrued Market Value"]),
                              row["Accrual"]).copy_abs() > tolerance:
            raise ValueError("REFUSED: COT native accrual decomposition differs by more than 0.01 USD")
    compared = [c for c in ("Currency", "CUSIP", "Ticker", "Symbol", "Asset Name",
                            "Cash Equivalent", "Account Number", "Account Supervised",
                            "_source_as_of") if c in h.columns]
    positions, keep, account_values = [], [], {}
    unsupported_rows = [i for i, row in enumerate(values) if row["Market Value"] <= 0]
    for (account, asset), group in h.groupby(["AccountID", "AssetID"], sort=True):
        ordinals = group.index.tolist()
        first = ordinals[0]
        # Not rounded: cent tolerance is for reconciliation, not duplicate equality.
        if any(values[i] != values[first] for i in ordinals):
            raise ValueError("REFUSED: COT incompatible duplicate economic fields")
        if any(len({optional(v) for v in group[c]}) != 1 for c in compared):
            raise ValueError("REFUSED: COT incompatible duplicate security/currency/provenance fields")
        relationships = group["Relationship ID"].tolist()
        if len(set(relationships)) != len(relationships):
            raise ValueError("REFUSED: COT repeated row within relationship grain")
        keep.append(first)
        account_values[account] = economics.add(account_values.get(account, Decimal("0")),
                                                values[first]["Market Value"])
        positions.append({"account_id": account, "asset_id": asset,
                          "market_value": str(values[first]["Market Value"]),
                          "quantity": str(values[first]["Units"]),
                          "source_row_ordinals": ordinals, "relationship_ids": relationships})
    totals, total_rows = {}, {}
    for ordinal, row in enumerate(account_totals.to_dict("records")):
        account = identity(row["AccountID"])
        if not valid_currency(row.get("Currency")):
            raise ValueError("REFUSED: COT unresolved/unsupported independent-total currency")
        value = number(row["Account Market Value"])
        if account in totals and totals[account] != value:
            raise ValueError("REFUSED: COT conflicting independent account totals")
        totals[account] = value
        total_rows.setdefault(account, []).append(ordinal)
    if set(account_values) != set(totals):
        raise ValueError("REFUSED: COT account census differs from independent totals; missing is not empty")
    if expected_account_ids is not None:
        if (not isinstance(expected_account_ids, (set, frozenset)) or not expected_account_ids
                or {identity(a) for a in expected_account_ids} != set(account_values)):
            raise ValueError("REFUSED: COT requested account census mismatch (including omissions from both inputs)")
    reconciliation = []
    for account in sorted(account_values):
        value, total = account_values[account], totals[account]
        difference = economics.subtract(value, total)
        if not math.isfinite(float(value)) or difference.copy_abs() > tolerance:
            raise ValueError("REFUSED: COT per-account independent tie exceeds 0.01 USD")
        reconciliation.append({"account_id": account, "position_value": str(value),
                               "independent_value": str(total), "difference": str(difference),
                               "independent_source_row_ordinals": total_rows[account],
                               "independent_source_origins": ([t_origins[i] for i in total_rows[account]]
                                                               if t_origins is not None else None)})
    # Use the validated economic values downstream; original signed and zero rows
    # remain in the source receipt and this ordinal census before any collapse.
    for column in numeric:
        h[column] = [row[column] for row in values]
    evidence = {"custody_as_of": custody_as_of, "valuation_as_of": valuation_as_of,
                "raw_row_count": len(h), "unique_position_count": len(keep),
                "relationship_rows_collapsed": len(h) - len(keep),
                "account_count": len(totals), "positions": positions,
                "accounts": [{"account_id": account,
                              "raw_row_count": int((h["AccountID"] == account).sum()),
                              "unique_position_count": sum(p["account_id"] == account for p in positions),
                              "duplicate_relationship_row_count": int((h["AccountID"] == account).sum())
                                  - sum(p["account_id"] == account for p in positions),
                              "conflict_original_row_count": 0,  # conflicts raise; no partial success
                              "unsupported_original_row_count": sum(h.at[i, "AccountID"] == account
                                                                    for i in unsupported_rows)}
                             for account in sorted(totals)],
                "nonpositive_original_row_ordinals": unsupported_rows,
                "negative_quantity_original_row_ordinals": [i for i, row in enumerate(values)
                                                             if row["Units"] < 0],
                "requested_census_checked": expected_account_ids is not None,
                "source_origins_supplied": h_origins is not None and t_origins is not None,
                "original_rows": [{"row_index": i, "account_id": h.at[i, "AccountID"],
                                   "asset_id": h.at[i, "AssetID"],
                                   "relationship_id": h.at[i, "Relationship ID"],
                                   "source_origin": h_origins[i] if h_origins is not None else None,
                                   "market_value": str(row["Market Value"]),
                                   "quantity": str(row["Units"])}
                                  for i, row in enumerate(values)],
                "reconciliation": reconciliation, "tolerance_usd": float(tolerance),
                "status": "LOCAL_SOURCE_CONTROLS_ONLY_NOT_CUSTODY_ACCEPTANCE"}
    if attested:
        evidence["currency_authority"] = dict(currency_authority)
        evidence["vendor_currency_field_present"] = {
            "holdings": "Currency" in holdings, "independent_totals": "Currency" in account_totals}
    return h.loc[keep].reset_index(drop=True), evidence


# --------------------------------------------------------------------------- provenance / nodes
def _node(node_id, parent_node_id, level, node_kind, basis, amount_value, amount_units,
         denom_kind, denom_value, of_parent, of_total, producer, join_method,
         join_matched, join_attempted, claim, model_id=None, security_id=None,
         drill_refs=None, classification=None, display=None, valuation_facts=None) -> dict:
    n = {
        "node_id": node_id,
        "parent_node_id": parent_node_id,
        "level": level,
        "node_kind": node_kind,
        "basis": basis,
        "amount": {"value": round(float(amount_value), 6), "units": amount_units,
                  "denominator": {"kind": denom_kind, "value": round(float(denom_value), 6)}},
        "percentages": {"of_parent": of_parent, "of_total": of_total},
        "provenance": {"producer": producer, "join_method": join_method,
                      "join_matched": int(join_matched), "join_attempted": int(join_attempted),
                      "claim": claim},
    }
    if model_id is not None:
        n["model_id"] = model_id
    if security_id is not None:
        n["security_id"] = security_id
    if drill_refs is not None:
        n["drill_refs"] = drill_refs
    if classification is not None:
        n["classification"] = classification
    if display is not None:
        n["display"] = display
    if valuation_facts:
        n["valuation_facts"] = list(valuation_facts)
    return n


# --------------------------------------------------------------- custody units (CTO 100208 item 4)
# Ruling IRPT-HOLDINGS-VALUATION-FACTS-20260924: quantity rides the node's `valuation_facts` as an
# ADDITIVE fact_kind CUSTODY_UNITS with units "UNITS" (P extends the enum and the units rule in both
# schema copies, portal-first), source_as_of = fact_holdings._source_as_of, source_revision = the
# receipted custody object's sha256, source_scope = the account's opaque id; on every OBSERVED
# custody SECURITY and as a fact on a definition-component row the account actually holds. PRICE is
# REFUSED: the feed states none and Market Value / Units would be a computation. Gated exactly as
# `display` is: emitted only when the contract this runner validates against admits the kind.
CUSTODY_UNITS_KIND = "CUSTODY_UNITS"
CUSTODY_UNITS_UNITS = "UNITS"


def custody_units_admitted() -> bool:
    """True when the published contract's valuation_facts admits CUSTODY_UNITS with units UNITS."""
    try:
        props = load_contract()["properties"]["nodes"]["items"]["properties"]["valuation_facts"]["items"]["properties"]
    except Exception:  # noqa: BLE001 -- no such member: nothing admitted
        return False
    kinds = (props.get("fact_kind") or {}).get("enum") or []
    units = props.get("units") or {}
    unit_ok = units.get("const") == CUSTODY_UNITS_UNITS or CUSTODY_UNITS_UNITS in (units.get("enum") or [])
    return CUSTODY_UNITS_KIND in kinds and unit_ok


def _receipt_sha(s3, bucket, key) -> "str | None":
    """The receipted sha256 of ONE source object this build read, from the versioned-input wrapper's
    own receipts; None on a plain client or when the object was not receipted (then no fact is
    emitted: a required field is never guessed)."""
    receipts = getattr(s3, "receipts", None)
    if not callable(receipts):
        return None
    try:
        for r in receipts() or []:
            if r.get("bucket") == bucket and r.get("key") == key and isinstance(r.get("sha256"), str):
                return r["sha256"]
    except Exception:  # noqa: BLE001
        return None
    return None


def _custody_units_fact(row, account_id, source_revision) -> "dict | None":
    """One CUSTODY_UNITS fact from a custody row, or None when any required field is absent."""
    units = row.get("Units")
    try:
        units = float(units)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(units):
        return None
    as_of = _text_cell(row.get("_source_as_of"))
    if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", as_of or "") or not source_revision or not account_id:
        return None
    return {"fact_kind": CUSTODY_UNITS_KIND, "value": units, "units": CUSTODY_UNITS_UNITS,
            "source_as_of": as_of, "source_revision": source_revision, "source_scope": account_id}


def custody_units_census(nodes) -> dict:
    """Nodes carrying a CUSTODY_UNITS fact, of all SECURITY nodes."""
    secs = [n for n in nodes if n.get("node_kind") == "SECURITY"]
    with_fact = sum(1 for n in secs if any(f.get("fact_kind") == CUSTODY_UNITS_KIND for f in n.get("valuation_facts") or []))
    return {"with_custody_units": with_fact, "security_nodes": len(secs)}


# --------------------------------------------------------------- display names (CTO 100157)
# Andrew-direct ~04:0xZ 2026-09-24 (via 1.0.0_SA_CTO, ruling IRPT-HOLDINGS-DISPLAY-NAMES-20260924):
# "a lot of very random strings ... dont really understand why we still dont have holdings and model
# names pinned down". The v1 node contract carried no human-readable member, so every row rendered
# an id. The ruled remedy is an ADDITIVE, OPTIONAL `display` object on a node -- {label (required),
# symbol?, description?} -- owned by 2.0.0_SA_COO~P on the contract and the portal (PORTAL FIRST: a
# closed-key validator that meets an unknown member refuses the whole response), filled here.
# THE GATE IS THE PUBLISHED CONTRACT ITSELF: `display` is emitted only when the contract this runner
# validates against admits it, so a build can never carry a member the served validator refuses,
# and the fill lands the moment P's schema edit does. The manifest census states which happened.
def display_admitted() -> bool:
    """True when the published HoldingsSnapshot contract admits a node `display` member."""
    try:
        node = load_contract()["properties"]["nodes"]["items"]
    except Exception:  # noqa: BLE001 -- an unreadable contract admits nothing
        return False
    return isinstance(node, dict) and "display" in (node.get("properties") or {})


def _display(label, symbol=None, description=None):
    """The ruled shape: label required; symbol / description only when present."""
    label = _text_cell(label)
    if not label:
        return None
    out = {"label": label}
    if _text_cell(symbol):
        out["symbol"] = _text_cell(symbol)
    if _text_cell(description):
        out["description"] = _text_cell(description)
    return out


def _security_display(symbol, description):
    """SECURITY: label = "<symbol> -- <description>", or whichever half exists."""
    symbol, description = _text_cell(symbol), _text_cell(description)
    label = (symbol + " -- " + description) if symbol and description else (symbol or description)
    return _display(label, symbol or None, description or None)


def _custody_display(row) -> "dict | None":
    """A COT custody row's own name: the custody Symbol (Ticker as the fallback) and the custody
    security description (Asset Display Name, Asset Name as the fallback) -- both already in
    fact_holdings (CTO 100157 item 1)."""
    symbol = _text_cell(row.get("Symbol")) or _text_cell(row.get("Ticker"))
    description = _text_cell(row.get("Asset Display Name")) or _text_cell(row.get("Asset Name"))
    return _security_display(symbol, description)


_MASK_NON_DIGIT = re.compile(r"[^0-9]")


def account_mask(account_number, account_type="") -> str:
    """`****1234 / IRA` for ONE account: its own masked tail and type (CTO 101302, ruling on S146). The same
    rule as directory_runner.masked_discriminator (pinned by test_account_mask_equals_the_directory_rule),
    kept here because the Holdings package does not ship the directory runner. Never a name, never a full
    number."""
    digits = _MASK_NON_DIGIT.sub("", str(account_number or ""))
    tail = digits[-4:] if len(digits) >= 4 else digits
    masked = ("*" * 4 + tail) if tail else "****"
    # The type in the source's own words and case, whole (UIC-16, CTO 102111): no uppercasing, no 24-character cut,
    # so INF's "Individual Retirement Account" reads in full. A code-only source (49F's Schwab codes) shows its code.
    token = " ".join(re.sub(r"[^A-Za-z0-9 ]", "", str(account_type or "")).split())
    return masked + (" / " + token if token else "")


def own_account_masks(firm_id, rows) -> dict:
    """opaque account id -> account_mask, from (raw_key, account_number, account_type) triples the builder already
    holds. A raw key minted twice keeps its first mask; a row with no number still masks its type."""
    out = {}
    for raw_key, number, acct_type in rows:
        if raw_key in (None, "") or str(raw_key) in ("nan", "None"):
            continue
        out.setdefault(opaque_id("account", firm_id, str(raw_key)), account_mask(number, acct_type))
    return out


def _directory_account_labels(s3, bucket, firm_id) -> dict:
    """opaque account id -> the landed DirectoryEntry's own account label ("****9237 / BROKERAGE"),
    the directory's own account label (CTO 100157 item 1; AD-10, CTO 102702). An entry carrying
    `account_masks` gives each account ITS OWN mask, by account_id; an entry without `account_masks`
    (older builds, or additive-field absence) falls back to the entry's one `masked_discriminator`
    for every account under it, stated, not hidden. {} when no directory landed."""
    labels = {}
    for prefix in (PROD_PREFIX.replace("holdings", "directory"),
                  QA_PREFIX.replace("holdings", "directory")):
        try:
            ptr = s3.get_object(Bucket=bucket, Key=prefix + "/latest.json")
            pointer = json.loads(ptr["Body"].read())
            body = s3.get_object(Bucket=bucket, Key=pointer["key"])
        except Exception:  # noqa: BLE001 -- absent directory: no labels, never a guess
            continue
        doc = json.loads(body["Body"].read())
        for e in doc.get("entries", []):
            entry_label = _text_cell(e.get("masked_discriminator"))
            own_masks = {}
            for m in e.get("account_masks", []) or []:
                aid = m.get("account_id")
                mask = _text_cell(m.get("masked_discriminator"))
                if aid and mask:
                    own_masks[aid] = mask
            for aid in (e.get("ids", {}) or {}).get("account_ids", []) or []:
                label = own_masks.get(aid) or entry_label
                if not label:
                    continue
                labels.setdefault(aid, label)
        return labels
    return labels


_FACT_PREFIXES = ("model_name=", "strategy_name=", "ticker=", "company=")


def fill_display_from_facts(nodes, account_labels=None) -> int:
    """For the builders that already carry a name INSIDE capability_facts (49F: model_name= on a
    leaf, ticker= / company= on a model asset and ticker= on a custody row; INF: model_name=, ticker=)
    or a taxonomy path on a sleeve: derive `display` for nodes that carry none. ACCOUNT nodes read
    the landed directory's own masked discriminator (account_labels, opaque id -> label; CTO 100157
    item 1, the same source build_cot uses); CASH nodes read the contract's own kind word with the
    producer's fact as the description. Returns the count filled. Never invents: a node with no name
    fact, no path and no directory entry stays without `display` and is counted by display_census."""
    filled = 0
    account_labels = account_labels or {}
    for n in nodes:
        if n.get("display"):
            continue
        cls = n.get("classification") or {}
        facts = cls.get("capability_facts") or []
        def fact(prefix):
            return next((f[len(prefix):].strip() for f in facts if f.startswith(prefix) and len(f) > len(prefix)), "")
        kind = n.get("node_kind")
        display = None
        if kind == "ACCOUNT":
            display = _display(account_labels.get(n.get("node_id")))
        elif kind == "CASH":
            display = _display("Cash", None, facts[0] if facts else None)
        elif kind == "MODEL_WRAPPER":
            name = fact("strategy_name=") or fact("model_name=")
            display = _display("Rebalancer strategy: " + name) if name else None
        elif kind == "MODEL_LEAF":
            display = _display(fact("model_name="))
        elif kind == "CATEGORY":
            path = cls.get("hierarchy_path") or []
            display = _display(CATEGORY_LABELS.get(category_key_for_path(path))) if path else None
        elif kind == "SLEEVE":
            path = cls.get("hierarchy_path") or []
            display = _display(" > ".join(path)) if path else None
        elif kind == "SECURITY":
            sid = n.get("security_id") or {}
            symbol = fact("ticker=") or (sid.get("value") if sid.get("namespace") == "TICKER" else "")
            display = _security_display(symbol, fact("company="))
        if display:
            n["display"] = display
            filled += 1
    return filled


def display_census(nodes) -> dict:
    """The producer's own count: nodes carrying a display label, of all nodes, by kind."""
    by_kind = {}
    for n in nodes:
        k = n.get("node_kind")
        tot, lab = by_kind.get(k, (0, 0))
        by_kind[k] = (tot + 1, lab + (1 if n.get("display", {}).get("label") else 0))
    return {"labelled": sum(v[1] for v in by_kind.values()), "denominator": len(nodes),
            "by_kind": {k: {"labelled": v[1], "of": v[0]} for k, v in sorted(by_kind.items())}}


# --------------------------------------------- asset class + model code (CTO 100905, DSGN_IRPTV1 v0.6)
# Spec: org/tier1_exec/2.0.0_SA_COO/deliverables/IRPT_HOLDINGS_CLASSIFICATION_MEMBERS_SPEC_20260924.md
# (@025cc1b799, amended @a8a287b992). The same gate as `display`: emitted only when the published
# contract admits the members. The class is the CANONICAL classifier's answer and never a guess of
# this producer's; the layer that answered travels beside it, so an inferred class stays visible.
# `other` = personal and held-away assets (Andrew-direct 2026-09-25 ~14:4xZ, @705be61575; v1 contract @3d5a590ad0).
# `structured` and `commodities`: the ETF Classifier's own tags (Andrew-direct 2026-09-26 ~21:2xZ; CTO 101511 ruled (a),
# ETF-tag half SIGNED CTO @c516dab84b + CRO @07525238da, Part B step B1). Admitted here before any value is written.
#
# NARROWED RELEASE (IB-mr-291, CTO RULING 103169; Andrew ~05:0xZ "PHYS is Commodities / Metals but it
# continues displaying in Alternatives"): the canonical cross-firm `etf-classifications` table (SC-t-1)
# answers FIRST for a ticker it holds -- served EXACTLY as the row holds it, no hedge fold, no guess;
# `data/assets/scripts/gold/investor_reporting/bd_securities_fallback.py` (the DECLARED FWD-6 exception,
# see its own header) answers everything else, UNCHANGED from the pre-SC-t-1 BD library. The full
# canonical migration (IB-mr-251..272) stays HELD -- cutting over fully today would unclassify hundreds
# of securities the canonical table does not yet cover. `asset_class_basis` keeps the PUBLISHED
# contract's existing enum (docs/contracts/investor-reporting/v1/HoldingsSnapshot.schema.json,
# additionalProperties:false, outside this cell's write grant): a canonical-table hit is served as
# "TABLE" (a direct ticker-table lookup is exactly what that basis has always meant), the SAME value a
# fallback ticker-table hit already used -- no new enum member, no new node field. Which table actually
# answered (`etf-classifications` vs `bd-securities-fallback`) is tracked ONLY in this runner's own
# census (`annotate_classification`'s `by_class_source`, never served on a node) -- see surprise row
# IRPT_BCKEND-W93-S1 for why the CTO's literal "asset_class_basis CANONICAL" / "class source" node
# fields are not on the wire.
ASSET_CLASS_VALUES = ("equity", "fixed_income", "alternatives", "cash", "other", "structured", "commodities",
                      "multi_asset", "unclassified")  # multi_asset: CTO batch 164 (readers first)
ASSET_CLASS_BASES = ("TABLE", "NAME_ALIAS", "NAME_PATTERN", "TICKER_SHAPE", "NONE")
CLASSIFICATION_MEMBERS = ("asset_class", "sub_asset_class", "asset_class_basis", "model_code")
CANONICAL_CLASS_SOURCE = "etf-classifications"
FALLBACK_CLASS_SOURCE = "%s-securities-fallback" % next(   # the served label, spelled through the registry (LGIC context rule)
    a["spelling"] for a in lookup("49financial")["aliases"] if "serving-route" in a.get("planes", []))


def classification_admitted() -> bool:
    """True when the published HoldingsSnapshot contract admits all four members on a node."""
    try:
        props = load_contract()["properties"]["nodes"]["items"]["properties"]
    except Exception:  # noqa: BLE001 -- an unreadable contract admits nothing
        return False
    return all(k in props for k in CLASSIFICATION_MEMBERS)


class _NarrowedClassifier:
    """CTO RULING 103169: the canonical `etf-classifications` table FIRST, the declared
    `bd_securities_fallback` module behind it for a ticker the table does not yet hold. Never the
    reverse; never blended for one ticker. Exposes the fallback's own `_ticker_map`/`_name_map`
    (proxied) so `_classifier_basis` keeps mirroring the fallback's four layers unchanged."""

    def __init__(self, canonical, fallback):
        self._canonical = canonical
        self._fallback = fallback

    @property
    def _ticker_map(self):
        return self._fallback._ticker_map

    @property
    def _name_map(self):
        return self._fallback._name_map

    def canonical_lookup(self, ticker) -> "dict | None":
        """The canonical table's row for this ticker, VERBATIM, or None (not held / no ticker)."""
        t = str(ticker or "").strip().upper()
        if not t or t in ("NONE", "NAN"):
            return None
        return self._canonical.get_classification(t)

    def classify(self, ticker, name):
        """The FALLBACK's own answer only -- the caller has already tried the canonical table."""
        return self._fallback.classify(ticker, name)

    def get_sub_asset_class(self, ticker, name=None):
        return self._fallback.get_sub_asset_class(ticker, name)

    @staticmethod
    def normalize_name(s):
        import bd_securities_fallback as bdf
        return bdf.ETFClassifier.normalize_name(s)


def canonical_classifier():
    """Loads TWO things, replacing the single BD-library import this used to be:
    (1) the ONE canonical `etf-classifications` client, loaded from its ONE home
        (infra/aws/lambda/v2_portal/_shared/etf_classifications_dynamodb.py) -- never copied;
    (2) the DECLARED bd-securities FALLBACK (bd_securities_fallback.py, FWD-6 exception, see its
        header), whose scan SWALLOWS a failure into empty maps; an empty map would label every
        uncovered security unclassified, so it is refused here instead.
    Returns (fallback_module, wrapper) so every existing (ec, clf) caller keeps its shape."""
    import bd_securities_fallback as bdf
    fallback = bdf.ETFClassifier.instance()
    if not fallback._ticker_map:
        raise ValueError("REFUSED: the fallback classifier loaded no rows (bd-securities scan failed)")
    shared_dir = str(_REPO / "infra" / "aws" / "lambda" / "v2_portal" / "_shared")
    if shared_dir not in sys.path:
        sys.path.insert(0, shared_dir)
    import etf_classifications_dynamodb as canonical_mod
    canonical = canonical_mod.ETFClassifier()
    return bdf, _NarrowedClassifier(canonical, fallback)


def _classifier_basis(ec, clf, ticker, name) -> str:
    """Which FALLBACK layer answers (bd_securities_fallback.py, same four layers, unchanged order).
    Only reached once the canonical table has already been tried and missed (classify_security)."""
    t = str(ticker or "").strip().upper()
    if t == "CASH_USD" or (t and t not in ("NONE", "NAN") and t in clf._ticker_map):
        return "TABLE"
    if name and clf._name_map.get(clf.normalize_name(str(name))) in clf._ticker_map:
        return "NAME_ALIAS"
    upper = str(name or "").upper()
    if ec._RE_ALT.search(upper) or ec._RE_CASH.search(upper) or ec._RE_FI.search(upper):
        return "NAME_PATTERN"
    if t and ec.re.fullmatch(r"[A-Z]{1,5}(\.[A-Z])?", t):
        return "TICKER_SHAPE"
    return "NONE"


def classify_security(ec, clf, ticker, name, description=None) -> dict:
    """{asset_class, sub_asset_class, asset_class_basis, class_source} for ONE security.
    CANONICAL FIRST (CTO RULING 103169): a ticker `etf-classifications` holds is served exactly as
    the row holds it -- no hedge fold, no guess -- with `class_source` CANONICAL_CLASS_SOURCE.
    Every other ticker falls to the declared bd-securities FALLBACK, exactly as before this cell
    (same four layers, same mirror-disagreement refusal, same cash rule), with `class_source`
    FALLBACK_CLASS_SOURCE. `class_source` is an internal-only key: `annotate_classification` pops
    it into the census and never merges it onto a node (the published contract's node schema is
    additionalProperties:false and outside this cell's write grant -- see surprise
    IRPT_BCKEND-W93-S1)."""
    if (str(ticker or "").strip().upper() == "CASH" and " ".join(str(description or "").split()).upper() == "CASH"):
        # Black Diamond's own cash line, never the ticker CASH (Pathward Financial in bd-securities; CTO 101547). Keyed
        # on the row's own asset name (display.description), NEVER the label: a 49F Pathward node's label is its symbol.
        # The cash rule is unchanged by the narrowed release -- checked before either classifier layer.
        return {"asset_class": "cash", "sub_asset_class": None, "asset_class_basis": "NAME_PATTERN",
                "class_source": FALLBACK_CLASS_SOURCE}
    canonical_row = clf.canonical_lookup(ticker)
    if canonical_row is not None:
        asset_class = canonical_row.get("asset_class") or "unclassified"
        if asset_class not in ASSET_CLASS_VALUES:
            raise ValueError("REFUSED: the canonical table returned %r, outside the admitted "
                             "asset_class enum" % asset_class)
        sub = canonical_row.get("sub_asset_class") or None
        return {"asset_class": asset_class, "sub_asset_class": sub, "asset_class_basis": "TABLE",
                "class_source": CANONICAL_CLASS_SOURCE}
    answer = clf.classify(ticker, name) or ""
    basis = _classifier_basis(ec, clf, ticker, name)
    if (basis == "NONE") != (answer == ""):
        raise ValueError("REFUSED: classifier layer mirror (%s) disagrees with classify() (%r)" % (basis, answer))
    asset_class = answer or "unclassified"
    if asset_class not in ASSET_CLASS_VALUES:
        raise ValueError("REFUSED: classifier returned %r, outside the admitted asset_class enum" % asset_class)
    sub = clf.get_sub_asset_class(ticker, name) or None
    return {"asset_class": asset_class, "sub_asset_class": sub, "asset_class_basis": basis,
            "class_source": FALLBACK_CLASS_SOURCE}


def model_code_for(node) -> "str | None":
    """The canonical model code of ONE MODEL_LEAF: the MDPF crosswalk's model_key by the vendor id the
    node already carries (SmartX model id, Eclipse model id), or the registry rule the COT build
    already applies (cot_constituent_taxonomy). Never read from the display label; unknown -> None."""
    registry_dir = str(_REPO / "data" / "mdpf" / "scripts" / "gold")
    if registry_dir not in sys.path:
        sys.path.insert(0, registry_dir)
    import mdpf_revamp_model_crosswalk as xw
    ref = node.get("model_id") or {}
    namespace, value = ref.get("namespace"), ref.get("value")
    try:
        if namespace == "SMARTX_MODEL":
            return xw.resolve_model_id(str(value)).model_key
        if namespace == "ECLIPSE_MODEL_ID":
            return xw.resolve_eclipse_id(int(value)).model_key
    except (xw.UnknownModelError, ValueError, TypeError):
        return None
    if namespace == "COT_REBALANCER_MODEL":
        facts = (node.get("classification") or {}).get("capability_facts") or []
        name = next((f.split("=", 1)[1] for f in facts if isinstance(f, str) and f.startswith("model_name=")), None)
        return cot_constituent_taxonomy(name).get("registry_key") if name else None
    return None


def annotate_classification(nodes, classifier=None) -> dict:
    """Adds the four CONTRACT members in place and returns the producer's own census of them.
    `class_source` (etf-classifications / bd-securities-fallback, IB-mr-291) is popped from
    `classify_security`'s answer before the node update -- it is a census-only key, never served
    on a node (the published node schema is additionalProperties:false)."""
    ec, clf = classifier or canonical_classifier()
    by_basis, by_class, by_source, leaves, coded = {}, {}, {}, 0, 0
    for n in nodes:
        kind = n.get("node_kind")
        if kind == "SECURITY":
            disp = n.get("display") or {}
            found = classify_security(ec, clf, disp.get("symbol"), disp.get("description") or disp.get("label"),
                                      description=disp.get("description"))
            source = found.pop("class_source", FALLBACK_CLASS_SOURCE)
            n.update(found)
            by_basis[found["asset_class_basis"]] = by_basis.get(found["asset_class_basis"], 0) + 1
            by_class[found["asset_class"]] = by_class.get(found["asset_class"], 0) + 1
            by_source[source] = by_source.get(source, 0) + 1
        elif kind == "MODEL_LEAF":
            n["model_code"] = model_code_for(n)
            leaves += 1
            coded += 1 if n["model_code"] else 0
    return {"security_nodes": sum(by_class.values()), "by_asset_class_basis": by_basis,
            "by_asset_class": by_class, "by_class_source": by_source,
            "model_leaf_nodes": leaves, "model_leaf_nodes_with_code": coded,
            "classifier_rows": len(clf._ticker_map)}


# --------------------------------------------------------------- the two clocks (IB-rt-7)
def recompute_weights(nodes):
    """Derive weights after all unique roots exist; never use a running denominator."""
    by_id = {n["node_id"]: n for n in nodes}
    if len(by_id) != len(nodes):
        raise ValueError("duplicate holdings node identity")
    total = sum(n["amount"]["value"] for n in nodes if n["node_kind"] == "ACCOUNT")
    for node in nodes:
        parent = by_id.get(node.get("parent_node_id"))
        denominator = parent["amount"]["value"] if parent else total
        value = node["amount"]["value"]
        node["amount"]["denominator"]["value"] = round(denominator, 6)
        node["percentages"] = {
            "of_parent": value / denominator if denominator > 0 else None,
            "of_total": value / total if total > 0 else None,
        }


class ClocksCollapsed(ValueError):
    """A snapshot or a node carries one clock where the contract needs two."""


def stamp_clocks(nodes, custody_as_of, overlay_as_of):
    """Put BOTH source clocks on EVERY node the caller just produced, and return the count.

    STAMPED OVER THE PRODUCED LIST, NEVER AT THE CALL SITES. There are eleven `_node(...)` call
    sites in this module and a twelfth is one edit away; an enumeration of them is a forward
    list that loses a member silently, while iterating the list a builder actually returned
    cannot. `assert_clocks_carried` then reads `N of N` off the same list.
    """
    if not custody_as_of or not overlay_as_of:
        raise ClocksCollapsed(
            "BLOCKED: both clocks are required -- custody_as_of=%r overlay_as_of=%r. A node "
            "dated by one clock cannot tell a reader whether its ASSIGNED attribution is older "
            "than the OBSERVED holdings beside it." % (custody_as_of, overlay_as_of))
    for n in nodes:
        n["clocks"] = {"custody_as_of": str(custody_as_of),
                       "overlay_as_of": str(overlay_as_of)}
    return len(nodes)


def assert_clocks_carried(snapshot) -> dict:
    """REFUSE a snapshot that collapses the two clocks -- the arm (c) difference control.

    Three ways to collapse, all refused: the snapshot header carrying neither; a node carrying
    neither; and a node whose pair is not the header's pair (a node silently re-dated). The
    census is `N of N` over the real node list.
    """
    clocks = snapshot.get("clocks") or {}
    custody, overlay = clocks.get("custody_as_of"), clocks.get("overlay_as_of")
    if not custody or not overlay:
        raise ClocksCollapsed(
            "BLOCKED: the snapshot header carries custody_as_of=%r overlay_as_of=%r -- a "
            "snapshot that collapses its two source clocks into one is refused"
            % (custody, overlay))
    nodes = snapshot.get("nodes") or []
    carried = 0
    for n in nodes:
        c = n.get("clocks") or {}
        if c.get("custody_as_of") == custody and c.get("overlay_as_of") == overlay:
            carried += 1
    if carried != len(nodes):
        raise ClocksCollapsed(
            "BLOCKED: %d of %d node(s) carry the snapshot's two clocks; the rest carry one, "
            "none, or a different pair" % (carried, len(nodes)))
    return {"denominator": "%d of %d" % (carried, len(nodes)),
            "custody_as_of": custody, "overlay_as_of": overlay,
            "clocks_differ": custody != overlay,
            "note": ("DISTINCT means two FIELDS, not two values: a firm whose custody and "
                     "overlay feeds land on the same date is correctly reported as equal. What "
                     "is refused is a snapshot that cannot say which is which.")}


# ------------------------------------------------- the attribution holdouts (IB-rt-7, C-S75)
def holdout_block(custody, assigned, value_by_account, *, observable, source, currency="USD"):
    """The `attribution_holdouts.unassigned` block, from two REAL populations.

    `custody` and `assigned` are sets of ISSUED opaque account ids. An account in custody with
    no overlay assignment keeps its FULL custody value here and is emitted as its own ACCOUNT
    node by the builder -- it is never folded into a sleeve that does have a model, which is
    the redistribution this block exists to make impossible to do quietly. A firm whose custody
    population is only reachable THROUGH the assignment table reports NOT-OBSERVABLE rather
    than a zero that reads like a clean measurement (bound 12: a 0 of 0 is VACUOUS, never a
    pass).
    """
    unassigned = sorted(custody - assigned)
    value = round(sum(float(value_by_account.get(a, 0.0)) for a in unassigned), 2)
    return {
        "account_count": len(unassigned),
        "account_ids": unassigned,
        "value": {"value": value, "currency": currency},
        "basis": "OBSERVED",
        "observable": observable,
        "denominator": ("%d of %d custody account(s) have no overlay assignment"
                        % (len(unassigned), len(custody))),
        "source": source,
    }


def redistribute_holdouts(snapshot) -> dict:
    """THE DIFFERENCE CONTROL. Returns a snapshot that spreads the unassigned accounts' value
    across the assigned sleeves pro rata and DROPS their nodes -- the economically wrong build
    that still reconciles to the cent, because the money is all still there.

    This is the negative arm arm (b) needs: without it, "the total reconciles" is a claim no
    observation could contradict. `holdouts_held()` below must PASS the honest snapshot and
    FAIL this one.

    MEMORY (TO-IB-m19-2 amendment 3, row IRPT_BCKEND-W42-S2's OOM-SINGLE ruling): every reader
    of the returned object -- this function, `holdouts_held()`, and `run_firm()`'s
    `difference_control` block -- touches only ACCOUNT-kind nodes plus the small
    `attribution_holdouts`/`custody_totals` blocks; none reads a SLEEVE/MODEL_LEAF/SECURITY/CASH
    node back. The prior `json.loads(json.dumps(snapshot))` deep-copied the WHOLE node tree to
    get an isolated ACCOUNT-kind subset -- measured at +567 MB RSS for 49F's 152,280-node build
    (`R19_49F_MEMORY_PROFILE_20260928.json`). This copies only what is read: identical
    `_redistributed`, `holdouts_held()` and reconciliation outcomes, proven by
    `test_holdouts.py` unchanged.
    """
    out = {"nodes": [{"node_id": n["node_id"], "node_kind": n["node_kind"],
                      "amount": dict(n["amount"])}
                     for n in snapshot["nodes"] if n["node_kind"] == "ACCOUNT"],
           "attribution_holdouts": copy.deepcopy(snapshot.get("attribution_holdouts") or {}),
           # read-only downstream (holdouts_held's informational census field); never mutated here.
           "custody_totals": snapshot.get("custody_totals") or {}}
    held = set((out.get("attribution_holdouts") or {}).get("unassigned", {}).get(
        "account_ids") or [])
    if not held:
        out["_redistributed"] = {"accounts": 0, "value": 0.0,
                                 "note": "nothing to redistribute for this firm"}
        return out
    moved = 0.0
    keep = []
    for n in out["nodes"]:
        if n["node_id"] in held and n["node_kind"] == "ACCOUNT":
            moved += float(n["amount"]["value"])
            continue                      # DROPPED -- the holdout disappears
        keep.append(n)
    out["nodes"] = keep
    sleeves = [n for n in keep if n["node_kind"] == "ACCOUNT"]
    base = sum(float(n["amount"]["value"]) for n in sleeves)
    for n in sleeves:                     # ... and its money reappears inside the sleeves
        share = (float(n["amount"]["value"]) / base) if base else 0.0
        n["amount"]["value"] = round(float(n["amount"]["value"]) + moved * share, 6)
    out["attribution_holdouts"]["unassigned"]["account_count"] = 0
    out["attribution_holdouts"]["unassigned"]["account_ids"] = []
    out["attribution_holdouts"]["unassigned"]["value"] = {"value": 0.0, "currency": "USD"}
    out["_redistributed"] = {"accounts": len(held), "value": round(moved, 2),
                             "note": "the unassigned accounts were dropped and their value "
                                     "spread pro rata across the accounts that DO carry a "
                                     "model -- the total is unchanged and the attribution is "
                                     "wrong"}
    return out


def holdouts_held(snapshot, expected_ids) -> "tuple[bool, dict]":
    """Did the holdouts survive? `expected_ids` is the population MEASURED from the sources.

    PASS needs all three: every expected id present as an ACCOUNT node, the block's own count
    equal to the expectation, and the custody total unchanged. The redistributing build fails
    the first two while passing the third -- which is exactly why the third alone is not a
    control.
    """
    expected = set(expected_ids or [])
    account_ids = {n["node_id"] for n in snapshot.get("nodes", [])
                   if n["node_kind"] == "ACCOUNT"}
    present = expected & account_ids
    block = (snapshot.get("attribution_holdouts") or {}).get("unassigned") or {}
    counted = int(block.get("account_count", -1))
    census = {
        "expected_unassigned": len(expected),
        "present_as_account_nodes": "%d of %d" % (len(present), len(expected)),
        "block_count": counted,
        "block_matches_expectation": counted == len(expected),
        "custody_total": snapshot.get("custody_totals", {}).get(
            "total_market_value", {}).get("value"),
    }
    ok = (len(present) == len(expected)) and counted == len(expected)
    return ok, census


def _unknown_classification(facts=None, hierarchy_path=None) -> dict:
    return {"fee_taking_status": "UNKNOWN", "advisory_status": "UNKNOWN",
           "vendor_account_supervised": "UNKNOWN", "hierarchy_path": hierarchy_path or [],
           "authoritative": False, "capability_facts": facts or []}


# --------------------------------------------------------------------------- S3 plumbing
def _read_parquet(s3, bucket, key) -> pd.DataFrame:
    try:
        obj = s3.get_object(Bucket=bucket, Key=key)
    except s3.exceptions.NoSuchKey:
        return pd.DataFrame()
    except Exception as exc:  # noqa: BLE001
        code = getattr(getattr(exc, "response", None), "get", lambda *_: None)("Error") or {}
        if isinstance(code, dict) and code.get("Code") in ("NoSuchKey", "404", "NotFound"):
            return pd.DataFrame()
        raise
    return pd.read_parquet(io.BytesIO(obj["Body"].read()))


def _latest_date_partition(s3, bucket, prefix, date_prefix="date=", *, as_of=None) -> "str | None":
    paginator = s3.get_paginator("list_objects_v2")
    dates = []
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix, Delimiter="/"):
        for cp in page.get("CommonPrefixes", []):
            tail = cp["Prefix"].rstrip("/").split("/")[-1]
            if tail.startswith(date_prefix):
                candidate = tail[len(date_prefix):]
                try:
                    valid = dt.date.fromisoformat(candidate).isoformat() == candidate
                except ValueError:
                    valid = False
                if valid and (as_of is None or candidate <= as_of):
                    dates.append(candidate)
    return sorted(dates)[-1] if dates else None


def retained_capture(s3, env_var, source, scope, table, obj, as_of):
    """A retained input a builder requires, as (local path, vintage), or (None, None) when there is none.

    An operator's environment variable wins, so local runs are unchanged. Otherwise the input is the latest capture at
    or before `as_of` under its lib/opal_naming address (CTO R4 ruling, msg 100965: "the build reads latest-at-or-before
    D and states its vintage"). The object is read through the build's own `s3`, so VersionedInputs receipts it, and
    written to a temporary file for the builder's path-based reader. No capture at or before `as_of` -> (None, None),
    and the caller refuses."""
    path = os.environ.get(env_var) or None
    if path:
        return path, {"env": env_var, "path": path}
    from urllib.parse import urlparse
    from opal_naming import address
    probe = urlparse(address(source, scope, "bronze", table, "date=%s" % as_of))
    date = _latest_date_partition(s3, probe.netloc, probe.path.lstrip("/").rsplit("/", 1)[0] + "/", as_of=as_of)
    if date is None:
        return None, None
    uri = address(source, scope, "bronze", table, "date=%s" % date, obj)
    found = urlparse(uri)
    got = s3.get_object(Bucket=found.netloc, Key=found.path.lstrip("/"))
    body = got["Body"].read()
    import tempfile
    handle, local = tempfile.mkstemp(suffix="-" + obj)
    with os.fdopen(handle, "wb") as out:
        out.write(body)
    return local, {"s3": uri, "capture_date": date, "version_id": got.get("VersionId"),
                   "sha256": hashlib.sha256(body).hexdigest()}


def _directory_account_ids(s3, bucket, firm_id) -> "set[str] | None":
    """The already-landed DirectoryEntry population for this firm (IB-s-1), read so the
    holdings population can be intersected against the directory's authorized accounts.
    Returns None (not an empty set) when no directory has landed yet -- an ABSENT
    population is a different state than an EMPTY one and must not be conflated."""
    for prefix in (PROD_PREFIX.replace("holdings", "directory"),
                  QA_PREFIX.replace("holdings", "directory")):
        try:
            ptr = s3.get_object(Bucket=bucket, Key=prefix + "/latest.json")
        except Exception:  # noqa: BLE001
            continue
        pointer = json.loads(ptr["Body"].read())
        try:
            body = s3.get_object(Bucket=bucket, Key=pointer["key"])
        except Exception:  # noqa: BLE001
            continue
        doc = json.loads(body["Body"].read())
        ids = set()
        for e in doc.get("entries", []):
            ids.update(e.get("ids", {}).get("account_ids", []))
        return ids
    return None


# --------------------------------------------------------------------------- 49F (SmartX)
def build_49f(s3, as_of: str) -> "tuple[list, dict]":
    firm_id = "49financial"
    bucket = "opal-data-assets"
    date = _latest_date_partition(s3, bucket, "smartx/platform/silver/fact_allocation_account_map/", as_of=as_of) or as_of
    m = _read_parquet(s3, bucket, "smartx/platform/silver/fact_allocation_account_map/date=%s/data.parquet" % date)
    roster = _read_parquet(s3, bucket, "smartx/platform/silver/fact_model_allocation_roster/date=%s/data.parquet" % date)
    pos = _read_parquet(s3, bucket, "smartx/platform/silver/fact_allocation_positions/date=%s/data.parquet" % date)
    val = _read_parquet(s3, bucket, "smartx/platform/silver/fact_allocation_valuation/date=%s/data.parquet" % date)

    dir_ids = _directory_account_ids(s3, firm_bucket_map().get(firm_id, ""), firm_id)

    nodes = []
    join_attempted = int(len(m))
    join_matched = 0
    exceptions = []
    total_before = 0.0
    dir_cross_check_matched = [0]

    if join_attempted:
        m = m.copy()
        # One allocation is one economic observation, even if the map repeats it.
        if m.duplicated("allocation_id").any():
            for _, group in m.groupby("allocation_id", dropna=False):
                if len(group.drop_duplicates()) > 1:
                    raise ValueError("conflicting SmartX allocation-account rows")
            m = m.drop_duplicates("allocation_id")
        m["account_number_10"] = m["account_number"].map(_pad10)
        m["opaque_account_id"] = m["account_number_10"].map(lambda a: opaque_id("account", firm_id, a))
        val_by_alloc = val.set_index("owner_id") if len(val) else pd.DataFrame()
        roster_by_alloc = roster.set_index("allocation_id") if len(roster) else pd.DataFrame()

        for _, row in m.iterrows():
            acc_opaque = row["opaque_account_id"]
            if dir_ids is not None and acc_opaque in dir_ids:
                dir_cross_check_matched[0] += 1
            alloc_id = row["allocation_id"]
            v = val_by_alloc.loc[alloc_id] if alloc_id in getattr(val_by_alloc, "index", []) else None
            r = roster_by_alloc.loc[alloc_id] if alloc_id in getattr(roster_by_alloc, "index", []) else None
            if v is None or pd.isna(v.get("equity")) or pd.isna(v.get("cash")):
                raise ValueError("SmartX allocation valuation incomplete; unknown is not zero")
            account_value = float(v["equity"]) + float(v["cash"])
            join_matched += 1
            total_before += account_value

            # NO NAMESPACE PREFIX IN AN ID (IB-rt-3, row W2-S11). Round 1 minted
            # "49f:acct:<opaque>" here; the prefix made this snapshot's account ids
            # unequal to the directory's for ALL THREE firms until a consumer
            # stripped it, and nothing declared that a strip was needed. The FIRM is
            # already a separate typed field -- scope.firm_id, required by
            # HoldingsSnapshot.schema.json -- so the prefix carried no information
            # the snapshot did not already carry once, correctly, at its own scope.
            account_node_id = acc_opaque
            existing_account = next((n for n in nodes if n["node_id"] == account_node_id), None)
            if existing_account is not None:
                existing_account["amount"]["value"] += account_value
                existing_account["amount"]["denominator"]["value"] += account_value
            else:
                nodes.append(_node(
                account_node_id, None, 0, "ACCOUNT", "OBSERVED", account_value, "USD",
                "UNIQUE_CUSTODY_TOTAL", account_value, None, None,
                "holdings_snapshot.build_49f", "fact_allocation_account_map+valuation zfill(10) join",
                join_matched, join_attempted, "measured",
                drill_refs=[{"ref_kind": "ACCOUNT", "ref_id": acc_opaque}],
                classification=_unknown_classification(
                    ["49F cohort not resolved by this cell -- see DirectoryEntry.cohort"]),
            ))
            model_id = row.get("model_id")
            status = str(r.get("status")) if r is not None and "status" in getattr(r, "index", []) else None
            has_model = pd.notna(model_id) and bool(str(model_id).strip())
            model_node_id = "%s:allocation:%s" % (acc_opaque, alloc_id)
            nodes.append(_node(
                model_node_id, account_node_id, 1, "MODEL_LEAF" if has_model else "UNRESOLVED",
                "ASSIGNED", account_value, "USD",
                "PARENT_NODE", account_value, 1.0 if account_value else None, None,
                "holdings_snapshot.build_49f", "fact_allocation_account_map (allocation->model)",
                join_matched, join_attempted, "measured",
                model_id={"namespace": "SMARTX_MODEL", "value": str(model_id)} if has_model else None,
                drill_refs=[{"ref_kind": "MODEL", "ref_id": str(model_id)}] if has_model else [],
                classification=_unknown_classification(
                    ["allocation_status=%s" % status] if has_model else
                    ["UNRESOLVED: allocation has no model membership"]),
            ))
            # position-grain nodes -- SmartX roster/valuation/position are DIFFERENT
            # grains (PRD v0.4 B12): positions are NEVER summed into the valuation total
            # above, and a position absent from `pos` for this allocation is NOT reported
            # as a zero -- it is simply not enumerated (missing != zero).
            if len(pos):
                prows = pos[pos["owner_id"] == alloc_id]
                for i, prow in enumerate(prows.itertuples(index=False)):
                    mv = float(getattr(prow, "market_value", 0.0) or 0.0)
                    nodes.append(_node(
                        "%s:pos:%d" % (model_node_id, i), model_node_id, 2, "SECURITY", "OBSERVED",
                        mv, "USD", "PARENT_NODE", account_value if account_value else mv,
                        (mv / account_value) if account_value else None, None,
                        "holdings_snapshot.build_49f", "fact_allocation_positions (position grain, not summed into valuation)",
                        join_matched, join_attempted, "measured",
                        security_id={"namespace": "TICKER" if getattr(prow, "ticker", None) else "UNKNOWN",
                                    "value": str(getattr(prow, "ticker", "") or getattr(prow, "symbol_id", ""))},
                    ))

    # ---- THE HOLDOUTS (IB-rt-7, C-S75) ---------------------------------------------------
    # 49F's custody and overlay arrive in ONE table: fact_allocation_account_map carries the
    # account, its allocation and the model that allocation follows. So "in custody with no
    # assignment" is observable here ONLY as an account whose every row names no model -- and
    # that is a REAL measurement over a REAL denominator, not a vacuous zero. What is NOT
    # observable from this source set is an account the custodian holds that never reached the
    # allocation map at all; that is stated rather than counted as zero.
    custody_ids, assigned_ids, value_by_account = set(), set(), {}
    if join_attempted:
        for _, row in m.iterrows():
            aid = row["opaque_account_id"]
            custody_ids.add(aid)
            if pd.notna(row.get("model_id")) and str(row.get("model_id")).strip():
                assigned_ids.add(aid)
            aum = row.get("aum_value")
            value_by_account[aid] = value_by_account.get(aid, 0.0) + (
                float(aum) if pd.notna(aum) else 0.0)
    holdouts = holdout_block(
        custody_ids, assigned_ids, value_by_account,
        observable="MEASURED",
        source="smartx/platform/silver/fact_allocation_account_map (account_number -> model_id; "
               "aum_value is the custody figure), date=%s" % date)
    for aid in holdouts["account_ids"]:
        if any(n["node_id"] == aid for n in nodes):
            continue  # Already emitted once, with an unresolved allocation child.
        # VISIBLE, WITH ITS FULL CUSTODY VALUE, AND NEVER REDISTRIBUTED: an ACCOUNT node with
        # no model child, so nothing downstream can attribute it to a sleeve it does not have.
        v = round(float(value_by_account.get(aid, 0.0)), 6)
        total_before += v
        nodes.append(_node(
            aid, None, 0, "ACCOUNT", "OBSERVED", v, "USD", "UNIQUE_CUSTODY_TOTAL", v, None, None,
            "holdings_snapshot.build_49f", "fact_allocation_account_map rows with no model_id "
            "(custody present, overlay absent)", join_matched, join_attempted, "measured",
            drill_refs=[{"ref_kind": "ACCOUNT", "ref_id": aid}],
            classification=_unknown_classification(
                ["UNASSIGNED: in custody with no model assignment; carried at full custody "
                 "value and NOT redistributed"]),
        ))

    unmatched = join_attempted - join_matched
    coverage = {"nodes_resolved": join_matched, "nodes_attempted": join_attempted,
               "remainder": {"amount": 0.0, "units": "USD",
                             "reason": ("%d of %d allocation-account row(s) excluded: not present in the "
                                       "landed DirectoryEntry account population (cross-check, not a data "
                                       "defect)" % (unmatched, join_attempted)) if join_attempted else
                                       "no fact_allocation_account_map rows at date=%s" % date}}
    manifest = {"firm_id": firm_id, "source": "smartx/platform/silver", "date": date,
               "join_matched": join_matched, "join_attempted": join_attempted,
               "total_market_value": round(total_before, 2), "exceptions": exceptions,
               "directory_cross_check": {
                   "matched": dir_cross_check_matched[0], "attempted": join_matched,
                   "note": ("INFORMATIONAL ONLY, not a join gate (row IRPT_BCKEND-W1-S7): "
                            "opaque_id(account, firm, raw) matches the landed DirectoryEntry "
                            "population when both sides derive the opaque id from the SAME "
                            "raw key. Verified 5 of 5 for 49F's fact_acc account numbers "
                            "before this module was written.")}}
    manifest["total_market_value"] = round(total_before, 2)
    # ONE date partition feeds both halves for 49F, so the two clocks are EQUAL here -- and
    # they are still carried as two FIELDS, because "equal today" is a measurement and
    # "collapsed" is a design that can never report the day they differ.
    recompute_weights(nodes)
    stamped = stamp_clocks(nodes, date, date)
    return nodes, {"coverage": coverage, "manifest": manifest, "source_completion_date": date,
                  "custody_as_of": date, "overlay_as_of": date, "holdouts": holdouts,
                  "assigned_without_custody": {
                      "account_count": len(assigned_ids - custody_ids),
                      "denominator": "%d of %d overlay account(s) absent from custody"
                                     % (len(assigned_ids - custody_ids), len(assigned_ids)),
                      "source": "the same map -- 49F's overlay cannot name an account its "
                                "custody half does not, so this is 0 by construction and is "
                                "reported rather than omitted"},
                  "nodes_stamped": stamped}


# --------------------------------------------------------------------------- INF (Eclipse)

def taxonomy_path(view_path: str, member_id: "str | None" = None) -> list:
    """A hierarchy_path read from the shared MDPF taxonomy registry, never a copied enum
    (CTO TAXONOMY-PATH-01): `view_path` must be a declared VIEW_TREE node ("Models",
    "SMA > ALT Strategies", "Client"); an optional registry member (e.g. "tax") appends that
    member's registered display name as the leaf, and must sit under that node."""
    registry_dir = str(_REPO / "data" / "mdpf" / "scripts" / "gold")
    if registry_dir not in sys.path:
        sys.path.insert(0, registry_dir)
    import mdpf_category_registry as registry
    if view_path not in registry.VIEW_TREE:
        raise ValueError("REFUSED: %r is not a declared taxonomy view node" % view_path)
    path = view_path.split(" > ")
    if member_id is not None:
        member = registry.resolve(member_id)
        if member.view_path != view_path:
            raise ValueError("REFUSED: registry member %r sits under %r, not %r" % (member_id, member.view_path, view_path))
        path = path + [member.display_name]
    return path


def _client_hierarchy_path():
    """Resolve the display category from the shared MDPF taxonomy."""
    return taxonomy_path("Client")


def build_inf_actual_nodes(positions, account_totals, *, expected_account_ids,
                           custody_as_of, valuation_as_of, overlay_as_of):
    """Construct custody/security drill at the exact caller's independent census.

    Source-backed currency is required; the live landed inputs currently lack it.
    This is the actual-position adapter, not a currency default or a publication.
    Account/portfolio model assignments cannot invent security membership: actual
    positions without that proof belong in the canonical Client display category.
    """
    validated, controls = validate_inf_actual_positions(
        positions, account_totals, expected_account_ids=expected_account_ids,
        custody_as_of=custody_as_of, valuation_as_of=valuation_as_of)
    client_path = _client_hierarchy_path()
    from opal_naming import lookup
    firm_id = lookup("inflection")["long"]
    nodes = []
    for account in controls["reconciliation"]:
        raw_account = account["account_id"]
        account_id = opaque_id("account", firm_id, raw_account)
        value = float(account["independent_value"])
        rows = validated.loc[validated.account_id == raw_account]
        common = (__name__ + "." + build_inf_actual_nodes.__name__,
                  "native Orion positions reconciled with independent custody total",
                  len(rows), len(rows), "measured")
        nodes.append(_node(account_id, None, 0, "ACCOUNT", "OBSERVED", value, "USD",
                           "UNIQUE_CUSTODY_TOTAL", value, None, None, *common,
                           drill_refs=[{"ref_kind": "ACCOUNT", "ref_id": account_id}],
                           classification=_unknown_classification()))
        client_id = account_id + ":client"
        category = _unknown_classification(
            ["Known custody; security-to-Opal-model/SMA membership not established"],
            hierarchy_path=client_path)
        nodes.append(_node(client_id, account_id, 1, "SLEEVE", "OBSERVED", value, "USD",
                           "PARENT_NODE", value, None, None, *common, classification=category))
        for row in rows.sort_values("id").to_dict("records"):
            position_id = hashlib.sha256((account_id + "|" + row["id"]).encode()).hexdigest()
            nodes.append(_node(position_id, client_id, 2, "SECURITY", "OBSERVED",
                               float(row["current_value"]), "USD", "PARENT_NODE", value,
                               None, None, *common,
                               security_id={"namespace": "VENDOR", "value": row["product_id"]},
                               classification=_unknown_classification(
                                   ["Native Orion product identity; no ticker merge or inferred price"],
                                   hierarchy_path=client_path)))
    recompute_weights(nodes)
    stamp_clocks(nodes, custody_as_of, overlay_as_of)
    return nodes, controls


# ONE declaration of the INF input bucket this runner has always read (legacy firm bucket, ACTIVE
# input home until the D14 rename). holdings_inf.py reads this name rather than re-typing it; the
# two silver prefixes are resolved through the producers' own key builders, never re-typed.
INF_SOURCE_BUCKET = "opal-data-inf"


def build_inf(s3, as_of: str) -> "tuple[list, dict]":
    firm_id = "inflection"
    bucket = INF_SOURCE_BUCKET
    date = _latest_complete_eclipse_date(s3, bucket, as_of) or as_of
    simple = _read_parquet(s3, bucket, "silver/eclipse/%s/portfolios_simple.parquet" % date)
    full = _read_parquet(s3, bucket, "silver/eclipse/%s/portfolios_full.parquet" % date)
    acc_date = _latest_date_partition(s3, bucket, "silver/api_dims/accounts_v2/", date_prefix="snapshot_date=", as_of=as_of) or as_of
    accounts = _read_parquet(s3, bucket, "silver/api_dims/accounts_v2/snapshot_date=%s/data.parquet" % acc_date)

    dir_ids = _directory_account_ids(s3, firm_bucket_map().get(firm_id, ""), firm_id)

    nodes = []
    join_attempted = int(len(simple))
    join_matched = 0
    total_before = 0.0
    multi_account_full_portfolios = 0
    dir_cross_check_matched = [0]

    if join_attempted and len(full):
        full_by_id = full.set_index("id") if "id" in full.columns else pd.DataFrame()
        acc_by_id = accounts.set_index("account_id") if "account_id" in accounts.columns else pd.DataFrame()
        # 13 MULTI-ACCOUNT FULL PORTFOLIOS NEVER REPEATED PER ACCOUNT (PRD v0.4 B12): a
        # full portfolio's managed_value is EMITTED ONCE at the portfolio grain, and each
        # member account gets an ACCOUNT node that DRILLS INTO it rather than repeating
        # the portfolio's value once per member.
        counts_per_portfolio = simple.groupby("id")["account_id"].nunique() if "id" in simple.columns else pd.Series(dtype=int)
        emitted_portfolios = set()
        emitted_accounts = set()
        portfolios_per_account = simple.groupby("account_id")["id"].nunique()
        for _, row in simple.iterrows():
            acc_id = row.get("account_id")
            if pd.isna(acc_id) or (acc_by_id is not None and len(acc_by_id) and acc_id not in getattr(acc_by_id, "index", [])):
                continue
            opaque_acc = opaque_id("account", firm_id, str(acc_id))
            if opaque_acc in emitted_accounts:
                continue
            emitted_accounts.add(opaque_acc)
            if dir_ids is not None and opaque_acc in dir_ids:
                dir_cross_check_matched[0] += 1
            join_matched += 1
            portfolio_id = row.get("id")
            model_id_raw = row.get("model_id")
            try:
                model_id_int = int(model_id_raw)
            except (TypeError, ValueError):
                model_id_int = None
            is_opal_model = model_id_int in OPAL_ECLIPSE_MODEL_IDS if model_id_int is not None else False

            fp = full_by_id.loc[portfolio_id] if portfolio_id in getattr(full_by_id, "index", []) else None
            managed_value = float(fp["managed_value"]) if fp is not None and pd.notna(fp.get("managed_value")) else 0.0
            excluded_value = float(fp["excluded_value"]) if fp is not None and pd.notna(fp.get("excluded_value")) else 0.0
            # managed/excluded meaning PRESERVED (PRD v0.4 B12) -- never summed into one
            # figure without saying so; the account node's amount is the MANAGED value,
            # and excluded is carried as a sibling node under the same account.
            n_members = int(counts_per_portfolio.get(portfolio_id, 1)) if len(counts_per_portfolio) else 1
            # The flattened simple export may expose only ONE of a portfolio's
            # associated accounts. Its row count alone is not a membership census.
            # Full's explicit count must agree before allocating portfolio value.
            declared_members = fp.get("num_of_associated_accounts") if fp is not None else None
            valid_member_count = (
                isinstance(declared_members, (Integral, float))
                and not isinstance(declared_members, bool)
                and math.isfinite(float(declared_members))
                and declared_members >= 1 and int(declared_members) == declared_members)
            membership_complete = valid_member_count and int(declared_members) == n_members
            if (n_members > 1 or (valid_member_count and declared_members > 1)) \
                    and portfolio_id not in emitted_portfolios:
                multi_account_full_portfolios += 1
                emitted_portfolios.add(portfolio_id)
            account_row = acc_by_id.loc[acc_id]
            if isinstance(account_row, pd.DataFrame) or pd.isna(account_row.get("current_value")):
                raise ValueError("Eclipse custody account value ambiguous or unavailable")
            account_value = float(account_row["current_value"])
            total_before += account_value

            # NO NAMESPACE PREFIX IN AN ID (IB-rt-3, row W2-S11). Round 1 minted
            # "inf:acct:<opaque>" here; the prefix made this snapshot's account ids
            # unequal to the directory's for ALL THREE firms until a consumer
            # stripped it, and nothing declared that a strip was needed. The FIRM is
            # already a separate typed field -- scope.firm_id, required by
            # HoldingsSnapshot.schema.json -- so the prefix carried no information
            # the snapshot did not already carry once, correctly, at its own scope.
            account_node_id = opaque_acc
            nodes.append(_node(
                account_node_id, None, 0, "ACCOUNT", "OBSERVED", account_value, "USD",
                "UNIQUE_CUSTODY_TOTAL", account_value, None, None,
                "holdings_snapshot.build_inf", "portfolios_simple+portfolios_full (accountId join)",
                join_matched, join_attempted, "measured",
                drill_refs=[{"ref_kind": "ACCOUNT", "ref_id": opaque_acc},
                           {"ref_kind": "SOURCE_ROW", "ref_id": str(portfolio_id)}],
                classification=_unknown_classification(
                    ["shared portfolio, %d members; account value comes only from custody" % n_members]
                    if n_members > 1 else []),
            ))
            if (not membership_complete or n_members > 1
                    or portfolios_per_account.get(acc_id, 0) != 1 or fp is None
                    or abs(managed_value + excluded_value - account_value) > RECON_TOLERANCE_USD
                    or model_id_int is None):
                # Portfolio-level values cannot be allocated to accounts by inference.
                # Preserve the independently observed account value as unresolved.
                nodes.append(_node(
                    account_node_id + ":unresolved", account_node_id, 1, "UNRESOLVED", "OBSERVED",
                    account_value, "USD", "PARENT_NODE", account_value, None, None,
                    "holdings_snapshot.build_inf", "accounts_v2.current_value; portfolio attribution unavailable",
                    join_matched, join_attempted, "measured",
                    classification=_unknown_classification([
                        "shared/missing/incompatible portfolio membership; no pro-rata allocation inferred"])))
                continue
            # BASES NEVER SPLICED: the account's OBSERVED total is broken into an
            # OBSERVED "managed" sub-node and an OBSERVED "excluded" sub-node (both
            # observed-basis siblings, one pie); the ASSIGNED model view is then a child
            # of "managed" ONLY, in its OWN pie -- never a sibling of an OBSERVED node.
            managed_node_id = "%s:managed" % account_node_id
            nodes.append(_node(
                managed_node_id, account_node_id, 1, "SLEEVE", "OBSERVED", managed_value, "USD",
                "PARENT_NODE", managed_value + excluded_value, None, None,
                "holdings_snapshot.build_inf", "portfolios_full.managed_value",
                join_matched, join_attempted, "measured",
                drill_refs=[{"ref_kind": "SOURCE_ROW", "ref_id": str(portfolio_id)}],
            ))
            if excluded_value:
                nodes.append(_node(
                    "%s:excluded" % account_node_id, account_node_id, 1, "UNRESOLVED", "OBSERVED",
                    excluded_value, "USD", "PARENT_NODE", managed_value + excluded_value,
                    None, None, "holdings_snapshot.build_inf", "portfolios_full.excluded_value",
                    join_matched, join_attempted, "measured",
                    drill_refs=[{"ref_kind": "SOURCE_ROW", "ref_id": str(portfolio_id)}],
                ))
            model_node_id = "%s:model:%s" % (managed_node_id, model_id_raw)
            nodes.append(_node(
                model_node_id, managed_node_id, 2, "MODEL_LEAF", "ASSIGNED", managed_value, "USD",
                "PARENT_NODE", managed_value, 1.0 if managed_value else None, None,
                "holdings_snapshot.build_inf", "portfolios_simple.model_id -> Eclipse OPAL_ECLIPSE_MODEL_IDS",
                join_matched, join_attempted, "measured",
                model_id={"namespace": "ECLIPSE_MODEL_ID", "value": str(model_id_raw)},
                drill_refs=[{"ref_kind": "MODEL", "ref_id": str(model_id_raw)}],
                classification=_unknown_classification(
                    ["is_opal=%s (canonical Eclipse id list)" % is_opal_model]),
            ))

    # ---- THE HOLDOUTS (IB-rt-7, C-S75) ---------------------------------------------------
    # INF's two halves are genuinely two tables: `accounts_v2` is the CUSTODY dimension (it
    # carries current_value) and Eclipse `portfolios_simple` is the OVERLAY. An account in
    # accounts_v2 with no Eclipse portfolio is in custody with no assignment, and it keeps its
    # full current_value here rather than vanishing from a snapshot built by walking the
    # overlay -- which is exactly what this runner did before this cell.
    custody_ids, value_by_account = set(), {}
    if len(accounts) and "account_id" in accounts.columns:
        for _, arow in accounts.iterrows():
            raw = arow.get("account_id")
            if pd.isna(raw):
                continue
            aid = opaque_id("account", firm_id, str(raw))
            custody_ids.add(aid)
            cv = arow.get("current_value")
            if pd.isna(cv) or isinstance(cv, bool) or not math.isfinite(float(cv)):
                raise ValueError("Eclipse custody account value unavailable; unknown is not zero")
            if aid in value_by_account:
                raise ValueError("Eclipse custody account identity ambiguous")
            value_by_account[aid] = float(cv)
    assigned_ids = set()
    if join_attempted and "account_id" in simple.columns:
        for raw in simple["account_id"].dropna():
            assigned_ids.add(opaque_id("account", firm_id, str(raw)))
    holdouts = holdout_block(
        custody_ids, assigned_ids, value_by_account,
        observable="MEASURED",
        source="silver/api_dims/accounts_v2 (custody dimension, current_value) "
               "snapshot_date=%s vs silver/eclipse/%s/portfolios_simple (overlay)"
               % (acc_date, date))
    represented_ids = {n["node_id"] for n in nodes if n["node_kind"] == "ACCOUNT"}
    for aid in sorted(custody_ids - represented_ids):
        v = round(float(value_by_account.get(aid, 0.0)), 6)
        total_before += v
        nodes.append(_node(
            aid, None, 0, "ACCOUNT", "OBSERVED", v, "USD", "UNIQUE_CUSTODY_TOTAL", v, None, None,
            "holdings_snapshot.build_inf",
            "accounts_v2 minus portfolios_simple (custody present, overlay absent)",
            join_matched, join_attempted, "measured",
            drill_refs=[{"ref_kind": "ACCOUNT", "ref_id": aid}],
            classification=_unknown_classification(
                ["UNASSIGNED: in the accounts_v2 custody dimension with no Eclipse portfolio; "
                 "carried at full current_value and NOT redistributed"]),
        ))

    unmatched = join_attempted - join_matched
    coverage = {"nodes_resolved": join_matched, "nodes_attempted": join_attempted,
               "remainder": {"amount": 0.0, "units": "USD",
                             "reason": ("%d of %d portfolio-simple row(s) excluded: no accounts_v2 match or "
                                       "not present in the landed DirectoryEntry population" % (unmatched, join_attempted))
                                       if join_attempted else "no eclipse portfolios_simple rows at date=%s" % date}}
    manifest = {"firm_id": firm_id, "source": "eclipse silver", "date": date,
               "join_matched": join_matched, "join_attempted": join_attempted,
               "multi_account_full_portfolios": multi_account_full_portfolios,
               "total_market_value": round(total_before, 2),
               "directory_cross_check": {
                   "matched": dir_cross_check_matched[0], "attempted": join_matched,
                   "note": ("INFORMATIONAL ONLY, not a join gate (row IRPT_BCKEND-W1-S7): 0 of "
                            "%d matched for INF -- the directory's opaque account id for this firm "
                            "derives from a raw key this cell did not verify aligns with "
                            "accounts_v2.account_id; the join used here is the firm's own "
                            "eclipse/accounts_v2 population, matching the PRD's own historical "
                            "figures elsewhere is the discriminator, not this cross-check."
                            % join_matched)}}
    manifest["total_market_value"] = round(total_before, 2)
    # TWO FEEDS, TWO CLOCKS: the accounts_v2 snapshot_date is the CUSTODY clock and the Eclipse
    # partition is the OVERLAY clock. They are read separately above and are carried separately
    # here, whether or not they happen to agree on a given day.
    recompute_weights(nodes)
    stamped = stamp_clocks(nodes, acc_date, date)
    return nodes, {"coverage": coverage, "manifest": manifest, "source_completion_date": date,
                  "custody_as_of": acc_date, "overlay_as_of": date, "holdouts": holdouts,
                  "assigned_without_custody": {
                      "account_count": len(assigned_ids - custody_ids),
                      "denominator": "%d of %d overlay account(s) absent from custody"
                                     % (len(assigned_ids - custody_ids), len(assigned_ids)),
                      "source": "silver/eclipse/%s/portfolios_simple minus accounts_v2" % date},
                  "nodes_stamped": stamped, "_accounts_frame": accounts}



def inf_producer_dir() -> Path:
    """ONE declaration of where the INF silver producers live; holdings_inf.py reads their pure
    locator helpers from here (never a writer, never a re-typed prefix)."""
    return _REPO / "data" / "inf" / "scripts" / "silver"


def _inf_positions_source_key(s3, as_of: str) -> "tuple[str, str]":
    """Reuse the actual Orion writer's locator without using its S3 client.

    The complete producer module must accompany this runner in its repository
    layout. Only its pure key helper is called; reads remain on VersionedInputs.
    """
    silver_dir = inf_producer_dir()
    if str(silver_dir) not in sys.path:
        sys.path.insert(0, str(silver_dir))
    from _orion_api_silver_lib import silver_api_dim_s3_key

    cutoff = dt.date.fromisoformat(as_of)
    produced_key = silver_api_dim_s3_key("positions_mv", cutoff)
    prefix, partition, filename = produced_key.rsplit("/", 2)
    if partition != "snapshot_date=" + cutoff.isoformat() or filename != "data.parquet":
        raise ValueError("INF producer partition/file shape changed")
    source_date = _latest_date_partition(
        s3, "opal-data-inf", prefix + "/", date_prefix="snapshot_date=", as_of=as_of)
    if source_date is None:
        raise ValueError("INF actual positions unavailable at requested cutoff")
    selected_key = silver_api_dim_s3_key("positions_mv", dt.date.fromisoformat(source_date))
    selected_prefix, selected_partition, selected_filename = selected_key.rsplit("/", 2)
    if (selected_prefix != prefix or selected_partition != "snapshot_date=" + source_date
            or selected_filename != filename):
        raise ValueError("INF producer selected key shape changed")
    return source_date, selected_key


def build_inf_actual(s3, as_of: str) -> "tuple[list, dict]":
    """Production INF construction requires actual positions before publication.

    The old account/portfolio projection is retained privately as attribution
    evidence. It cannot replace actual security rows or certify a USD default.
    Currency absent from the current landed frames refuses until the bounded
    source-authority adapter is supplied; a successful overlay is not acceptance.
    """
    overlay_nodes, extra = build_inf(s3, as_of)
    custody_date = extra["custody_as_of"]
    positions_date, positions_key = _inf_positions_source_key(s3, as_of)
    positions = _read_parquet(s3, "opal-data-inf", positions_key)
    accounts = extra.pop("_accounts_frame")
    if "account_id" not in accounts or accounts.empty:
        raise ValueError("INF independent custody census unavailable")
    expected = set(accounts.account_id)
    nodes, controls = build_inf_actual_nodes(
        positions, accounts, expected_account_ids=expected,
        custody_as_of=positions_date, valuation_as_of=custody_date,
        overlay_as_of=extra["overlay_as_of"])
    extra["manifest"]["portfolio_attribution_nodes"] = overlay_nodes
    extra["manifest"]["actual_position_controls"] = controls
    extra["manifest"]["source"] = "Orion positions_mv + accounts_v2; Eclipse attribution retained separately"
    extra["coverage"] = {
        "nodes_resolved": 0, "nodes_attempted": controls["selected_position_count"],
        "remainder": {"amount": extra["manifest"]["total_market_value"], "units": "USD",
                      "reason": "Known actual custody in Client; position model/SMA membership not established"}}
    extra["nodes_stamped"] = len(nodes)
    return nodes, extra


def _latest_complete_eclipse_date(s3, bucket, as_of=None) -> "str | None":
    paginator = s3.get_paginator("list_objects_v2")
    dates = []
    for page in paginator.paginate(Bucket=bucket, Prefix="silver/eclipse/", Delimiter="/"):
        for cp in page.get("CommonPrefixes", []):
            tail = cp["Prefix"].rstrip("/").split("/")[-1]
            if re.match(r"^\d{4}-\d{2}-\d{2}$", tail) and (as_of is None or tail <= as_of):
                dates.append(tail)
    for d in sorted(dates, reverse=True):
        if s3.list_objects_v2(Bucket=bucket, Prefix="silver/eclipse/%s/_meta/silver_complete.json" % d).get("KeyCount", 0) > 0:
            return d
    return None


# --------------------------------------------------------------------------- COT (BD Rebalancer)
def _cot_taxonomy_rules():
    """The MDPF registry's own Primary / Custom / SMA rules and the strict Opal-name test, imported
    from their one home (CTO ruling IRPT-COT-HOLDINGS-TREE-20260924 item 1) -- never re-typed here."""
    for rel in ((), ("data", "assets", "scripts", "gold"), ("data", "assets", "scripts", "silver")):
        p = str(_REPO.joinpath(*rel))   # the repo root first: the slice module imports lib.opal_naming
        if p not in sys.path:
            sys.path.insert(0, p)
    if "lib.opal_naming" not in sys.modules:
        # Another `lib` package can already sit in sys.modules (a lambda tree's own lib/ during a full
        # test run), which shadows the repo's; bind the repo's opal_naming by file so the slice module's
        # `from lib.opal_naming import ...` resolves to the one LGIC builder either way.
        import importlib.util
        spec = importlib.util.spec_from_file_location("lib.opal_naming", str(_REPO / "lib" / "opal_naming.py"))
        module = importlib.util.module_from_spec(spec)
        sys.modules["lib.opal_naming"] = module
        spec.loader.exec_module(module)
    import build_cottonwood_mdpf_slice as slice_mod
    import build_cottonwood_mdpf_pair as pair_mod
    import rebalancer_schemas as rs
    return slice_mod, pair_mod, rs


def cot_constituent_taxonomy(model_name) -> dict:
    """Where ONE blend child (a Rebalancer 'Model') sits in the Opal taxonomy, by the registry rule:
    the five PRIMARY names (build_cottonwood_mdpf_slice.CANONICAL_KEY) -> Models > Primary; an SMA
    leaf (build_cottonwood_mdpf_pair.OPAL_SMA_LEAF_KEYS) -> SMA; any other Opal-named model
    (is_auto_custom) -> Models > Custom; a non-Opal model -> the Client residual (Andrew-direct
    2026-09-23 ~19:4xZ answer 2: third-party models go to Client). is_opal is the NAME test
    (rebalancer_schemas.is_opal_name), never the roster default."""
    slice_mod, pair_mod, rs = _cot_taxonomy_rules()
    name = "" if model_name is None else str(model_name)
    norm = slice_mod._norm(name)
    is_opal = bool(rs.is_opal_name(name))
    if norm in slice_mod._CANONICAL_BY_NORM:
        return {"qualifier": "primary", "hierarchy_path": taxonomy_path("Models > Primary"), "is_opal": is_opal,
                "leaf": True, "registry_key": slice_mod._CANONICAL_BY_NORM[norm]}
    if norm in {slice_mod._norm(k) for k in pair_mod.OPAL_SMA_LEAF_KEYS}:
        return {"qualifier": "sma", "hierarchy_path": taxonomy_path("SMA"), "is_opal": is_opal, "leaf": True,
                "registry_key": pair_mod.OPAL_SMA_LEAF_KEYS.get(name.strip())}
    if slice_mod.is_auto_custom(name):
        return {"qualifier": "custom", "hierarchy_path": taxonomy_path("Models > Custom"), "is_opal": is_opal,
                "leaf": True, "registry_key": None}
    return {"qualifier": "client", "hierarchy_path": _client_hierarchy_path(), "is_opal": is_opal,
            "leaf": False, "registry_key": None}


def _text_cell(value) -> str:
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except (TypeError, ValueError):
        pass
    return str(value).strip()


def _weight_cell(row, *columns):
    for c in columns:
        w = row.get(c)
        if w is None:
            continue
        try:
            if pd.isna(w):
                continue
        except (TypeError, ValueError):
            pass
        return float(w)
    return None


def cot_constituents(blend: pd.DataFrame, definition: pd.DataFrame) -> dict:
    """strategy model_id -> its constituent index, from the two silver tables the ruling names.

    `children`: one entry per fact_model_blend edge (child id, name, absolute weight, taxonomy);
    `components`: sleeve_name -> the fact_model_definition rows (symbol, asset_id, absolute weight)
    at sleeve_depth 1; `root_components`: the strategy's own depth-0 rows (a client-held security
    such as PHYS or GLD). Weights are the tables' absolute allocations; nothing is renormalised.
    """
    out: "dict[str, dict]" = {}
    if len(blend) and {"model_id", "child_model_id"}.issubset(blend.columns):
        for row in blend.to_dict("records"):
            sid = _text_cell(row.get("model_id"))
            cid = _text_cell(row.get("child_model_id"))
            if not sid or not cid:
                continue
            w = _weight_cell(row, "absolute_allocation", "relative_allocation")
            if w is None:
                continue
            name = _text_cell(row.get("child_model_name")) or cid
            entry = out.setdefault(sid, {"children": [], "components": {}, "root_components": []})
            entry["children"].append({"model_id": cid, "model_name": name, "weight": w,
                                      "taxonomy": cot_constituent_taxonomy(name)})
    if len(definition) and {"model_id", "sleeve_name", "sleeve_depth"}.issubset(definition.columns):
        for row in definition.to_dict("records"):
            sid = _text_cell(row.get("model_id"))
            if not sid:
                continue
            w = _weight_cell(row, "absolute_allocation", "relative_allocation")
            comp = {"symbol": _text_cell(row.get("symbol")), "asset_id": _text_cell(row.get("asset_id")),
                    "component_name": _text_cell(row.get("component_name")), "weight": w}
            entry = out.setdefault(sid, {"children": [], "components": {}, "root_components": []})
            depth = row.get("sleeve_depth")
            try:
                depth = int(depth)
            except (TypeError, ValueError):
                depth = None
            if depth == 0:
                entry["root_components"].append(comp)
            else:
                entry["components"].setdefault(_text_cell(row.get("sleeve_name")), []).append(comp)
    return out


def _cot_security_identifier(comp: dict) -> dict:
    if comp.get("symbol"):
        return {"namespace": "TICKER", "value": comp["symbol"]}
    return {"namespace": "VENDOR", "value": comp.get("asset_id") or "unknown"}


def _cot_position_id(account_id: str, parent_id: str, asset_key: str) -> str:
    return account_id + ":position:" + hashlib.sha256(json.dumps(
        [account_id, parent_id, asset_key], separators=(",", ":")).encode("utf-8")).hexdigest()


def cot_actual_security_tree(account_nodes, validated_holdings, membership=None, constituents=None, labels=None):
    """Project already validated custody rows; membership only where a dated adapter supplies it.

    Rebalancer targets are not an economic partition of these positions. With no `membership`
    every account's observed value sits under the canonical Client category (the accepted
    93f930c265 shape). With `membership` (opaque account id -> the assigned Rebalancer STRATEGY,
    whole-account grain, from holdings_membership.rebalancer_membership) and `constituents`
    (strategy id -> its blend children and definition components, from cot_constituents) an
    assigned account carries the RULED tree (CTO ruling IRPT-COT-HOLDINGS-TREE-20260924, on
    Andrew-direct ~03:1xZ 2026-09-24 "the Models are constituents at a drilldown level beneath
    the Strategy"), REGROUPED under L0 CATEGORY nodes (CTO ruling msg 102475, cell IB-mr-202: NO
    MODEL_WRAPPER node -- the strategy identity is a fact, never a node):

      L1 CATEGORY       one per category actually present (Models / SMAs / Client), ASSIGNED,
                        each the sum of its own children -- never the whole account value;
      L2 MODEL_LEAF     one per Opal-named or SMA blend child, ASSIGNED = account value x the
                        child's absolute blend weight, hierarchy_path by the MDPF registry rule
                        (Models > Primary / Models > Custom / SMA), is_opal by NAME; attaches
                        under its category by that hierarchy_path's first segment;
      L2 SLEEVE Client  THE PLUG (Andrew-direct 2026-09-23 ~19:4xZ: "Client is the plug figure so
                        no need for unresolved") = account value minus the assigned leaves; the
                        non-Opal children's weight lands here by construction (answer 2: third-
                        party models go to Client); attaches under the Client category;
      L3 SECURITY       under a leaf: that constituent's definition components at account value x
                        component weight (ASSIGNED; the observed custody position for the same
                        asset is a FACT on the row, never the amount); under Client: the strategy's
                        own root components and the non-Opal children's components, the same way;
                        an UNRESOLVED node carries any remainder the definition's weights leave.

    MODEL DOLLARS ARE ASSIGNED, NEVER POSITION-MATCHED: no observed position is split between
    constituents and none is re-attributed by identity. The observed positions the strategy's
    definition does not cover are counted and named as facts on the Client sleeve and censused by
    the caller; they are not nodes, because the plug is a residual dollar figure and a pie must sum
    to its parent (reconcile_before_after). Every pie carries ONE basis (assert_bases_not_spliced):
    the wrapper's children are all ASSIGNED, which is why the plug is ASSIGNED too. Custody totals
    are unchanged. The caller must first run validate_cot_actual_positions; no null/default or
    duplicate policy is implemented a second time here.
    """
    nodes = []
    client_path = _client_hierarchy_path()
    models_path = taxonomy_path("Models")
    smas_path = taxonomy_path("SMA")
    membership = membership or {}
    constituents = constituents or {}
    labels = labels or {}
    admit = bool(labels.get("admit"))             # display_admitted() at the caller; never assumed here
    account_labels = labels.get("accounts") or {}
    units_cfg = labels.get("custody_units") or {}
    units_rev = units_cfg.get("source_revision") if units_cfg.get("admit") else None
    groups = {opaque_id("account", "cottonwood", str(raw)): group
              for raw, group in validated_holdings.groupby("AccountID", sort=True)}
    roots = {node["node_id"]: node for node in account_nodes}
    if len(roots) != len(account_nodes) or set(roots) != set(groups):
        raise ValueError("REFUSED: COT actual tree differs from validated custody census")
    for account_id, root in sorted(roots.items()):
        if admit and account_labels.get(account_id) and not root.get("display"):
            root["display"] = _display(account_labels[account_id])
        value = root["amount"]["value"]
        model = membership.get(account_id)
        if model is not None:
            # AMENDMENT 1 R1 (row IRPT_BCKEND-W44-S1): the assigned Rebalancer strategy is carried as a
            # FIELD on the ACCOUNT node, never a node -- this is the only place it lived before IB-mr-202
            # removed the MODEL_WRAPPER node (which carried model_id/model_name) along with the shape it
            # existed only to hold.
            root["assigned_strategy"] = {
                "model_id": {"namespace": "COT_REBALANCER_MODEL", "value": _text_cell(model.get("model_id"))},
                "name": _text_cell(model.get("model_name"))}
        nodes.append(root)
        if model is not None:
            _cot_strategy_subtree(nodes, account_id, value, model, constituents.get(str(model["model_id"])),
                                  groups[account_id], models_path, smas_path, client_path,
                                  root["provenance"]["producer"], admit, units_rev)   # the account's own producer name, never a new literal
            continue
        else:
            parent = account_id + ":client"
            path = client_path
            nodes.append(_node(
                parent, account_id, 1, "CATEGORY", "OBSERVED", value, "USD",
                "PARENT_NODE", value, None, None, "holdings_snapshot.build_cot",
                "actual custody; Rebalancer assignment/target does not establish position membership",
                0, len(groups[account_id]), "measured",
                classification=_unknown_classification([
                    "Known custody in Client; position model/SMA membership not established",
                    "Model targets are separate and are not actual position amounts"],
                    hierarchy_path=client_path),
                display=_display("Client") if admit else None))
        for row in groups[account_id].sort_values("AssetID").to_dict("records"):
            # AssetID, not ticker, defines a position within a custody account.
            # A digest avoids raw account/asset identity in the public node key.
            position_id = hashlib.sha256(json.dumps(
                [account_id, str(row["AssetID"])], separators=(",", ":")
            ).encode("utf-8")).hexdigest()
            identifier = {"namespace": "VENDOR", "value": str(row["AssetID"])}
            for column, namespace in (("CUSIP", "CUSIP"), ("Ticker", "TICKER")):
                supplied = row.get(column)
                if isinstance(supplied, str) and supplied.strip():
                    identifier = {"namespace": namespace, "value": supplied.strip()}
                    break
            nodes.append(_node(
                account_id + ":position:" + position_id, parent, 3 if model is not None else 2, "SECURITY",
                "OBSERVED", row["Market Value"], "USD", "PARENT_NODE", value,
                None, None, "holdings_snapshot.build_cot",
                "validated AccountID/AssetID custody position; equal relationship duplicates collapsed",
                1, 1, "measured", security_id=identifier,
                classification=_unknown_classification([
                    "Security identifier is custody-sourced; membership is the account's, never inferred per position"],
                    hierarchy_path=path),
                display=_custody_display(row) if admit else None,
                valuation_facts=[f for f in [_custody_units_fact(row, account_id, units_rev)] if f] if units_rev else None))
    recompute_weights(nodes)
    return nodes


def _cot_strategy_subtree(nodes, account_id, value, model, index, positions, models_path, smas_path, client_path, producer,
                          admit=False, units_rev=None):
    """Append the ruled subtree for ONE assigned account (see cot_actual_security_tree).

    L0 CATEGORY GROUPING (CTO ruling msg 102475, cell IB-mr-202): NO MODEL_WRAPPER node -- the
    strategy identity is a fact, never a node. One CATEGORY node per category actually present
    (Models / SMAs / Client), parented directly on the ACCOUNT, each carrying the sum of its own
    children; the assigned blend-child MODEL_LEAF rows attach under their category by
    hierarchy_path first segment, and the Client plug SLEEVE attaches under the Client category.
    Amounts, classification and the membership rule are all unchanged -- only which node a leaf
    attaches under moved."""
    index = index or {"children": [], "components": {}, "root_components": []}
    strategy_name = _text_cell(model.get("model_name"))
    observed_by_asset = {}
    observed_rows = {}
    for row in positions.to_dict("records"):
        observed_by_asset[str(row["AssetID"])] = observed_by_asset.get(str(row["AssetID"]), 0.0) + float(row["Market Value"])
        observed_rows.setdefault(str(row["AssetID"]), row)
    assigned_total = 0.0
    folded = []          # non-Opal children -> Client by rule
    covered_assets = set()
    by_category: "dict[str, list]" = {"models": [], "smas": []}
    for child in index["children"]:
        tax = child["taxonomy"]
        comps = index["components"].get(child["model_name"], [])
        for c in comps:
            if c.get("asset_id"):
                covered_assets.add(c["asset_id"])
        if not tax["leaf"]:
            folded.append(child)
            continue
        leaf_value = round(value * child["weight"], 6)
        assigned_total += leaf_value
        leaf = account_id + ":model:" + child["model_id"]
        key = category_key_for_path(tax["hierarchy_path"])
        by_category.setdefault(key, []).append((child, leaf, leaf_value, comps, tax))

    for key in ("models", "smas"):
        entries = by_category.get(key) or []
        if not entries:
            continue
        cat_total = round(sum(e[2] for e in entries), 6)
        cat_id = account_id + ":category:" + key
        cat_path = models_path if key == "models" else smas_path
        nodes.append(_node(
            cat_id, account_id, 1, "CATEGORY", "ASSIGNED", cat_total, "USD", "PARENT_NODE", value, None, None,
            producer, "sum of the assigned Rebalancer strategy's blend-child model leaves in this category",
            1, 1, "measured",
            classification=_unknown_classification(
                ["category=%s" % CATEGORY_LABELS[key], "strategy_name=%s" % strategy_name,
                 "rebalance_model_type=%s" % _text_cell(model.get("rebalance_model_type")),
                 "provider=%s" % _text_cell(model.get("provider")), "is_opal=%s" % bool(model.get("is_opal")),
                 "Rebalancer strategy %s (fact_model_assignment); dollars are ASSIGNED = account value x blend "
                 "weight, never position-matched" % strategy_name],
                hierarchy_path=cat_path),
            display=_display(CATEGORY_LABELS[key]) if admit else None))
        for child, leaf, leaf_value, comps, tax in entries:
            nodes.append(_node(
                leaf, cat_id, 2, "MODEL_LEAF", "ASSIGNED", leaf_value, "USD", "PARENT_NODE", value, None, None,
                producer, "fact_model_blend child of the assigned strategy; account value x absolute_allocation",
                1, 1, "measured",
                model_id={"namespace": "COT_REBALANCER_MODEL", "value": child["model_id"]},
                drill_refs=[{"ref_kind": "MODEL", "ref_id": child["model_id"]}],
                classification=_unknown_classification(
                    ["model_name=%s" % child["model_name"], "rebalance_model_type=Model", "is_opal=%s" % tax["is_opal"],
                     "qualifier=%s" % tax["qualifier"], "blend_weight=%s" % child["weight"]],
                    hierarchy_path=tax["hierarchy_path"]),
                display=_display(child["model_name"]) if admit else None))
            _cot_component_rows(nodes, account_id, leaf, value, comps, observed_by_asset, tax["hierarchy_path"],
                                "component of %s (fact_model_definition); account value x component weight" % child["model_name"], producer,
                                admit, observed_rows, units_rev)

    plug = round(value - assigned_total, 6)
    uncovered = [(a, v) for a, v in observed_by_asset.items() if a not in covered_assets
                 and a not in {c.get("asset_id") for c in index["root_components"]}
                 and not any(a == c.get("asset_id") for f in folded for c in index["components"].get(f["model_name"], []))]
    uncovered_value = round(sum(v for _, v in uncovered), 2)
    facts = ["residual of the strategy assignment: account custody value minus the assigned constituent leaves "
             "(Client is the plug; not an observed position set; no Unresolved bucket)",
             "observed positions outside the strategy definition: %d row(s), %.2f USD -- counted, not attributed"
             % (len(uncovered), uncovered_value)]
    for f in folded:
        facts.append("non-Opal constituent %s (blend weight %s) lands in Client: third-party models go to Client"
                     % (f["model_name"], f["weight"]))
    root_and_folded = list(index["root_components"])
    for f in folded:
        root_and_folded.extend(index["components"].get(f["model_name"], []))
    if abs(plug) > 0.005 or root_and_folded:
        client_cat = account_id + ":category:client"
        client = account_id + ":client"
        nodes.append(_node(
            client_cat, account_id, 1, "CATEGORY", "ASSIGNED", plug, "USD", "PARENT_NODE", value, None, None,
            producer, "sum of the Client sleeve under the assigned Rebalancer strategy (the plug)",
            1, 1, "measured",
            classification=_unknown_classification(
                ["category=Client", "strategy_name=%s" % strategy_name], hierarchy_path=client_path),
            display=_display("Client") if admit else None))
        nodes.append(_node(
            client, client_cat, 2, "SLEEVE", "ASSIGNED", plug, "USD", "PARENT_NODE", value, None, None,
            producer, "account value minus assigned constituent leaves (the plug)",
            1, 1, "measured", classification=_unknown_classification(facts, hierarchy_path=client_path),
            display=_display("Client (residual, not in a model)") if admit else None))
        placed = _cot_component_rows(nodes, account_id, client, value, root_and_folded, observed_by_asset, client_path,
                                     "strategy-root or non-Opal-constituent component (fact_model_definition); account value x component weight", producer,
                                     admit, observed_rows, units_rev)
        remainder = round(plug - placed, 6)
        if abs(remainder) > 0.005:
            nodes.append(_node(
                client + ":unallocated", client, 3, "UNRESOLVED", "ASSIGNED", remainder, "USD", "PARENT_NODE", plug,
                None, None, producer,
                "plug minus the definition's root/folded components: weight the tables do not allocate",
                1, 1, "inferred",
                classification=_unknown_classification(
                    ["remainder of the Client plug the strategy definition's weights do not allocate; carried, never redistributed"],
                    hierarchy_path=client_path),
                display=_display("Unallocated remainder of the strategy assignment") if admit else None))


def _cot_component_rows(nodes, account_id, parent, value, comps, observed_by_asset, path, join_method, producer,
                        admit=False, observed_rows=None, units_rev=None) -> float:
    """SECURITY rows for a constituent's (or the plug's) definition components, ASSIGNED; returns the placed sum."""
    placed = 0.0
    observed_rows = observed_rows or {}
    for comp in comps:
        if comp.get("weight") is None:
            continue
        amount = round(value * comp["weight"], 6)
        placed += amount
        asset_key = comp.get("asset_id") or comp.get("symbol") or comp.get("component_name") or "?"
        observed = observed_by_asset.get(comp.get("asset_id") or "")
        facts = ["component_weight=%s" % comp["weight"],
                 ("observed custody position for this asset: %.2f USD (a FACT, not this node's amount)" % observed)
                 if observed is not None else "no observed custody position for this asset in fact_holdings"]
        if comp.get("component_name"):
            facts.append("component_name=%s" % comp["component_name"])
        display = None
        held = observed_rows.get(comp.get("asset_id") or "")
        if admit:
            description = ((_text_cell(held.get("Asset Display Name")) or _text_cell(held.get("Asset Name"))) if held else "") \
                or comp.get("component_name") or ""
            display = _security_display(comp.get("symbol") or (_text_cell(held.get("Symbol")) if held else ""), description)
        units_fact = _custody_units_fact(held, account_id, units_rev) if (held and units_rev) else None
        nodes.append(_node(
            _cot_position_id(account_id, parent, asset_key), parent, 3, "SECURITY", "ASSIGNED", amount, "USD",
            "PARENT_NODE", value, None, None, producer, join_method, 1, 1, "measured",
            security_id=_cot_security_identifier(comp),
            classification=_unknown_classification(facts, hierarchy_path=path), display=display,
            valuation_facts=[units_fact] if units_fact else None))
    return round(placed, 6)


COT_NUMERIC_FACTS = ["Market Value", "Units", "Unaccrued Market Value", "Accrual"]


def cot_screen_accounts(holdings, independent_totals, firm_id, custody_as_of, valuation_as_of):
    """A full-firm COT build (what a scheduled run is): validate each source account ALONE, with the same no-position
    rule and validate_cot_actual_positions, and keep the accounts that pass. Every other account is carried with its
    refusal.

    This is the per-account census the served 841-account publication was accepted on
    (COT_EXPANDED_COVERAGE_CANDIDATE_20260923.json: 981 source, 841 supported, 140 refused). One account's source
    defect refuses that account, never the firm (IRPT_BCKEND-S134). The validator itself stays all-or-nothing over
    whatever it is given. Returns (supported canonical account ids, screen evidence)."""
    authority = bind_report_currency(firm_id)["currency_authority"]
    raw_ids = sorted(set(holdings.AccountID.dropna().astype(str)) | set(independent_totals.AccountID.dropna().astype(str)))
    supported, refused = set(), []
    for raw in raw_ids:
        h = holdings.loc[holdings.AccountID.astype(str) == raw]
        if set(COT_NUMERIC_FACTS) <= set(h):
            h = h.loc[~h[COT_NUMERIC_FACTS].isna().all(axis=1)]
        t = independent_totals.loc[independent_totals.AccountID.astype(str) == raw]
        try:
            validate_cot_actual_positions(h, t, custody_as_of=custody_as_of, valuation_as_of=valuation_as_of,
                                          expected_account_ids={raw}, currency_authority=authority)
            supported.add(opaque_id("account", firm_id, raw))
        except ValueError as exc:
            refused.append({"account": opaque_id("account", firm_id, raw), "reason": str(exc)})
    reasons = {}
    for r in refused:
        reasons[r["reason"]] = reasons.get(r["reason"], 0) + 1
    return supported, {"scope": "FULL_FIRM_SCREENED_PER_ACCOUNT", "source_accounts": len(raw_ids),
                       "supported_accounts": len(supported), "refused_accounts": len(refused),
                       "refusal_reasons": reasons, "refused": refused}


def build_cot(s3, as_of: str, *, account_ids=None) -> "tuple[list, dict]":
    from opal_naming import lookup
    firm_id = lookup("cottonwood")["long"]
    bucket = "opal-data-assets"
    # Existing monolith source plane, resolved with the registry's firm spelling.
    silver_prefix = "blackdiamond/%s/silver/" % firm_id
    assign_date = _latest_date_partition(s3, bucket, "blackdiamond/cottonwood/silver/fact_model_assignment/", as_of=as_of) or as_of
    blend_date = _latest_date_partition(s3, bucket, "blackdiamond/cottonwood/silver/fact_model_blend/", as_of=as_of) or as_of
    roster_date = _latest_date_partition(s3, bucket, "blackdiamond/cottonwood/silver/fact_model_roster/", as_of=as_of) or as_of
    definition_date = _latest_date_partition(s3, bucket, silver_prefix + "fact_model_definition/", as_of=as_of) or as_of
    value_date = _latest_date_partition(s3, bucket, silver_prefix + "fact_holdings/", as_of=as_of)
    total_date = _latest_date_partition(s3, bucket, silver_prefix + "fact_allocations/", as_of=as_of)
    if not value_date or not total_date:
        raise ValueError("REFUSED: COT actual custody/independent total partition absent")
    if value_date != total_date:
        raise ValueError("REFUSED: COT custody/independent total vintage mismatch")

    assign = _read_parquet(s3, bucket, "blackdiamond/cottonwood/silver/fact_model_assignment/date=%s/data.parquet" % assign_date)
    blend = _read_parquet(s3, bucket, "blackdiamond/cottonwood/silver/fact_model_blend/date=%s/data.parquet" % blend_date)
    roster = _read_parquet(s3, bucket, "blackdiamond/cottonwood/silver/fact_model_roster/date=%s/data.parquet" % roster_date)
    definition = _read_parquet(s3, bucket, silver_prefix + "fact_model_definition/date=%s/data.parquet" % definition_date)
    holdings_key = silver_prefix + "fact_holdings/date=%s/data.parquet" % value_date
    totals_key = silver_prefix + "fact_allocations/date=%s/data.parquet" % total_date
    holdings = _read_parquet(s3, bucket, holdings_key)
    independent_totals = _read_parquet(s3, bucket, totals_key)

    holdings_origins = [(f"s3://{bucket}/{holdings_key}", i) for i in range(len(holdings))]
    totals_origins = [(f"s3://{bucket}/{totals_key}", i) for i in range(len(independent_totals))]
    expected_raw = None
    selected_control = None
    screen = None
    if account_ids is None:
        account_ids, screen = cot_screen_accounts(holdings, independent_totals, firm_id, value_date, total_date)
        if not account_ids:
            raise ValueError("REFUSED: COT no source account passes the per-account source controls: %s"
                             % "; ".join(sorted(screen["refusal_reasons"])))
    if account_ids is not None:
        if (not isinstance(account_ids, (set, frozenset)) or not account_ids
                or any(not isinstance(a, str) or not a for a in account_ids)):
            raise ValueError("REFUSED: explicit nonempty canonical account census required")
        if "AccountID" not in holdings or "AccountID" not in independent_totals:
            raise ValueError("REFUSED: COT selected account source census absent")
        raw_ids = set(holdings.AccountID.dropna().astype(str)) | set(independent_totals.AccountID.dropna().astype(str))
        bound = {opaque_id("account", firm_id, raw): raw for raw in raw_ids}
        if not account_ids <= set(bound):
            raise ValueError("REFUSED: requested COT account absent from both source censuses")
        expected_raw = {bound[a] for a in account_ids}
        h_mask = holdings.AccountID.astype(str).isin(expected_raw)
        t_mask = independent_totals.AccountID.astype(str).isin(expected_raw)
        selected_control = {"scope": "REQUESTED_ACCOUNTS_ONLY", "requested_account_count": len(account_ids),
                            "source_custody_rows": len(holdings), "selected_custody_rows": int(h_mask.sum()),
                            "outside_requested_custody_rows": int((~h_mask).sum()),
                            "source_total_rows": len(independent_totals), "selected_total_rows": int(t_mask.sum())}
        holdings_origins = [origin for origin, keep in zip(holdings_origins, h_mask) if keep]
        totals_origins = [origin for origin, keep in zip(totals_origins, t_mask) if keep]
        holdings = holdings.loc[h_mask].copy()
        independent_totals = independent_totals.loc[t_mask].copy()
        if len(assign) and "external_id" in assign:
            assign = assign.loc[assign.external_id.astype(str).isin(expected_raw)].copy()

    # Canonical Assets_Dim/includeAll lists the account/asset dimension, including
    # pairs with no position at this end date. CTO5ee54ac0d4/CROf307d58415:
    # all FOUR facts absent means no-position, never a numeric zero. Do not apply
    # this rule to partial nulls or another source family. Preserve physical rows.
    numeric = ["Market Value", "Units", "Unaccrued Market Value", "Accrual"]
    if not set(numeric) <= set(holdings):
        raise ValueError("REFUSED: COT source lacks no-position discriminator")
    absent = holdings[numeric].isna().all(axis=1)
    absence_control = {
        "source_rule": "COT_ASSETS_DIM_INCLUDE_ALL_NO_POSITION_AT_AS_OF",
        "authority": "5ee54ac0d4",
        "source_evidence": "f307d5841512f8de005b2dd5272350029d1f1b11",
        "selected_dimension_row_count": len(holdings),
        "active_original_row_count": int((~absent).sum()),
        "excluded_no_position_count": int(absent.sum()),
        "excluded_source_origins": [origin for origin, exclude in zip(holdings_origins, absent) if exclude],
    }
    holdings_origins = [origin for origin, exclude in zip(holdings_origins, absent) if not exclude]
    holdings = holdings.loc[~absent].copy()
    holdings, actual_controls = validate_cot_actual_positions(
        holdings, independent_totals, custody_as_of=value_date, valuation_as_of=total_date,
        expected_account_ids=expected_raw,
        holdings_row_origins=holdings_origins, total_row_origins=totals_origins,
        currency_authority=bind_report_currency(firm_id)["currency_authority"])
    actual_controls["source_dimension_census"] = absence_control
    if selected_control is not None:
        actual_controls["selection"] = selected_control
    if screen is not None:
        actual_controls["selection"]["scope"] = screen["scope"]
        actual_controls["account_screen"] = screen
    control_values = {r["account_id"]: float(r["position_value"])
                      for r in actual_controls["reconciliation"]}
    # This result is INTERNAL evidence only; publishing extra actual_custody wire
    # fields needs P/Y agreement and P's paired schema/projection integration.
    if len(assign) and ("external_id" not in assign.columns
                        or assign["external_id"].isna().any()
                        or assign["external_id"].astype(str).duplicated().any()):
        raise ValueError("REFUSED: COT ambiguous model account assignment")
    if len(assign):
        assign = assign.copy()
        assign["external_id"] = assign["external_id"].astype(str)

    dir_ids = _directory_account_ids(s3, firm_bucket_map().get(firm_id, ""), firm_id)

    exceptions = []

    roster_is_opal = {}
    if len(roster):
        roster_is_opal = dict(zip(roster["model_id"], roster["is_opal"].astype(bool)))
    blend_children: "dict[str, list]" = {}
    if len(blend):
        for _, r in blend.iterrows():
            parent = r["model_id"]
            child = r["child_model_id"]
            w = r.get("relative_allocation")
            if pd.isna(w):
                w = r.get("absolute_allocation")
            if pd.isna(w) or w is None:
                continue
            blend_children.setdefault(parent, []).append((child, float(w)))
            roster_is_opal.setdefault(parent, bool(r.get("is_opal", False)))
            roster_is_opal.setdefault(child, False)  # a child absent from roster stays False, never guessed True

    nodes = []
    join_attempted = int(len(assign))
    join_matched = 0
    total_before = 0.0
    dir_cross_check_matched = [0]
    holdings_by_account = (holdings.groupby("AccountID") if len(holdings) and "AccountID" in holdings.columns
                           else None)
    unresolved_total = 0.0

    if join_attempted:
        for _, row in assign.iterrows():
            external_id = row.get("external_id")
            if external_id is None:
                continue
            opaque_acc = opaque_id("account", firm_id, str(external_id))
            if dir_ids is not None and opaque_acc in dir_ids:
                dir_cross_check_matched[0] += 1
            grp = None
            if holdings_by_account is not None:
                try:
                    grp = holdings_by_account.get_group(external_id)
                except KeyError:
                    grp = None
            if grp is None or not len(grp):
                continue
            join_matched += 1
            account_value = control_values[external_id]
            total_before += account_value
            vendor_supervised = "UNKNOWN"
            if "Account Supervised" in grp.columns and len(grp):
                v = grp["Account Supervised"].dropna()
                if len(v):
                    vendor_supervised = "YES" if bool(v.iloc[0]) else "NO"

            # NO NAMESPACE PREFIX IN AN ID (IB-rt-3, row W2-S11). Round 1 minted
            # "cot:acct:<opaque>" here; the prefix made this snapshot's account ids
            # unequal to the directory's for ALL THREE firms until a consumer
            # stripped it, and nothing declared that a strip was needed. The FIRM is
            # already a separate typed field -- scope.firm_id, required by
            # HoldingsSnapshot.schema.json -- so the prefix carried no information
            # the snapshot did not already carry once, correctly, at its own scope.
            account_node_id = opaque_acc
            nodes.append(_node(
                account_node_id, None, 0, "ACCOUNT", "OBSERVED", account_value, "USD",
                "UNIQUE_CUSTODY_TOTAL", account_value, None, None,
                "holdings_snapshot.build_cot", "fact_holdings (Market Value, deduped DC1)",
                join_matched, join_attempted, "measured",
                drill_refs=[{"ref_kind": "ACCOUNT", "ref_id": opaque_acc}],
                # "vendor AccountSupervised is NOT Opal fee-taking status" (PRD v0.4 B12):
                # carried in ITS OWN field, fee_taking_status stays UNKNOWN/not-authoritative
                # because no Opal supervision source was resolved for COT by this cell.
                classification={"fee_taking_status": "UNKNOWN", "advisory_status": "UNKNOWN",
                               "vendor_account_supervised": vendor_supervised,
                               "hierarchy_path": [], "authoritative": False, "capability_facts": []},
            ))

            model_id = row.get("strategy_name") or row.get("program_name")
            if model_id and model_id in roster_is_opal:
                # RECURSIVE EXPANSION -- this module's own mechanism (see module docstring),
                # applying every blend edge weight exactly once and retaining cycle/missing
                # mass rather than dropping or renormalizing it away.
                result = expand_model(model_id, blend_children, roster_is_opal)
                unresolved_total += result.unresolved_mass * account_value
                for i, (leaf_id, w, is_opal) in enumerate(result.leaves):
                    leaf_value = w * account_value
                    nodes.append(_node(
                        "%s:target:%d" % (account_node_id, i), account_node_id, 1,
                        "MODEL_LEAF" if not blend_children.get(leaf_id) else "MODEL_WRAPPER",
                        "TARGET", leaf_value, "USD", "PARENT_NODE", account_value,
                        w, (leaf_value / total_before) if total_before else None,
                        "holdings_snapshot.build_cot", "expand_model (Rebalancer blend, recursive, weights applied once)",
                        join_matched, join_attempted, "measured",
                        model_id={"namespace": "COT_REBALANCER_MODEL", "value": str(leaf_id)},
                        drill_refs=[{"ref_kind": "MODEL", "ref_id": str(leaf_id)}],
                        classification=_unknown_classification(["is_opal=%s" % is_opal]),
                    ))
                if result.unresolved_mass:
                    nodes.append(_node(
                        "%s:unresolved" % account_node_id, account_node_id, 1, "UNRESOLVED", "TARGET",
                        result.unresolved_mass * account_value, "USD", "PARENT_NODE", account_value,
                        result.unresolved_mass, None,
                        "holdings_snapshot.build_cot", "expand_model (cycle/missing-node retained mass)",
                        join_matched, join_attempted, "inferred",
                    ))

    # ---- THE HOLDOUTS (IB-rt-7, C-S75) ---------------------------------------------------
    # COT's custody half is `fact_holdings` (the Market Value this builder already sums) and
    # its overlay half is `fact_model_assignment`. The loop above walks the OVERLAY and keeps
    # only rows with a holdings match, so before this cell a custody account with no assignment
    # left no trace at all. Here it becomes its own ACCOUNT node at full custody value.
    custody_ids, value_by_account = set(), {}
    if holdings_by_account is not None:
        for raw, grp in holdings_by_account:
            aid = opaque_id("account", firm_id, str(raw))
            custody_ids.add(aid)
            value_by_account[aid] = control_values[raw]
    assigned_ids = set()
    if join_attempted and "external_id" in assign.columns:
        for raw in assign["external_id"].dropna():
            assigned_ids.add(opaque_id("account", firm_id, str(raw)))
    holdouts = holdout_block(
        custody_ids, assigned_ids, value_by_account,
        observable="MEASURED",
        source="blackdiamond/cottonwood/silver/fact_holdings date=%s (custody, deduped Market "
               "Value) vs fact_model_assignment date=%s (overlay)" % (value_date, assign_date))
    for aid in holdouts["account_ids"]:
        v = round(float(value_by_account.get(aid, 0.0)), 6)
        total_before += v
        nodes.append(_node(
            aid, None, 0, "ACCOUNT", "OBSERVED", v, "USD", "UNIQUE_CUSTODY_TOTAL", v, None, None,
            "holdings_snapshot.build_cot",
            "fact_holdings minus fact_model_assignment (custody present, overlay absent)",
            join_matched, join_attempted, "measured",
            drill_refs=[{"ref_kind": "ACCOUNT", "ref_id": aid}],
            classification={"fee_taking_status": "UNKNOWN", "advisory_status": "UNKNOWN",
                           "vendor_account_supervised": "UNKNOWN", "hierarchy_path": [],
                           "authoritative": False,
                           "capability_facts": [
                               "UNASSIGNED: held in fact_holdings with no fact_model_assignment "
                               "row; carried at full custody value and NOT redistributed"]},
        ))

    coverage_denom = join_attempted
    unmatched = coverage_denom - join_matched
    coverage = {"nodes_resolved": join_matched, "nodes_attempted": coverage_denom,
               "remainder": {"amount": round(unresolved_total, 2), "units": "USD",
                             "reason": ("%d of %d assignment row(s) excluded (no holdings match or outside the "
                                       "landed directory population); %.2f USD retained as recursive-expansion "
                                       "unresolved mass across matched accounts"
                                       % (unmatched, coverage_denom, unresolved_total)) if coverage_denom else
                                       "no fact_model_assignment rows at date=%s" % assign_date}}
    manifest = {"firm_id": firm_id, "source": "blackdiamond/cottonwood/silver",
               "assign_date": assign_date, "blend_date": blend_date, "roster_date": roster_date,
               "value_date": value_date, "join_matched": join_matched, "join_attempted": join_attempted,
               "total_market_value": round(total_before, 2), "duplicate_exceptions": exceptions,
               "actual_custody_controls": actual_controls,
               "directory_cross_check": {
                   "matched": dir_cross_check_matched[0], "attempted": join_matched,
                   "note": ("INFORMATIONAL ONLY, not a join gate (row IRPT_BCKEND-W1-S7): the "
                            "directory's opaque account id for COT derives from a raw key this "
                            "cell did not verify aligns with fact_model_assignment.external_id; "
                            "the external_id-to-AccountID join used here reproduces the PRD's own "
                            "946-of-950 figure directly.")}}
    manifest["total_market_value"] = round(total_before, 2)
    # Preserve the old target calculation privately for review, never use it as
    # the actual holdings tree. No target dollar is added to custody economics.
    target_nodes = [node for node in nodes if node["basis"] == "TARGET"]
    recompute_weights(nodes)
    manifest["model_target_nodes"] = target_nodes
    # MEMBERSHIP AT THE ACCOUNT GRAIN (CTO 3c8392cf2f): the dated Rebalancer assignment, joined to
    # the roster by exact unique name, puts an assigned account's custody under Models with one
    # measured MODEL_LEAF; custody totals and positions are unchanged, targets stay separate.
    membership = holdings_membership.rebalancer_membership(assign, roster)
    constituents = cot_constituents(blend, definition) if membership else {}
    admit_display = display_admitted()
    admit_units = custody_units_admitted()
    holdings_sha = _receipt_sha(s3, bucket, holdings_key) if admit_units else None
    own_masks = own_account_masks(firm_id, zip(
        independent_totals["AccountID"],
        independent_totals["Account Number"] if "Account Number" in independent_totals else [""] * len(independent_totals),
        independent_totals["Account Type"] if "Account Type" in independent_totals else [""] * len(independent_totals)))
    directory_labels = _directory_account_labels(s3, firm_bucket_map().get(firm_id, ""), firm_id) if admit_display else {}
    labels = {"admit": admit_display,
              "accounts": {**directory_labels, **own_masks} if admit_display else {},
              "custody_units": {"admit": admit_units and holdings_sha is not None, "source_revision": holdings_sha}}
    nodes = cot_actual_security_tree(
        [node for node in nodes if node["node_kind"] == "ACCOUNT"], holdings, membership=membership,
        constituents=constituents, labels=labels)
    manifest["display_labels"] = {"contract_admits_display": admit_display,
                                  "account_labels_from_directory": len(directory_labels),
                                  "account_labels_own_mask": len(own_masks) if admit_display else 0, **display_census(nodes)}
    manifest["custody_units"] = {"contract_admits_custody_units": admit_units, "custody_receipt_sha_present": holdings_sha is not None,
                                 **custody_units_census(nodes)}
    assigned_value = round(sum(n["amount"]["value"] for n in nodes
                               if n["node_kind"] == "ACCOUNT" and n["node_id"] in membership), 2)
    assigned_count = sum(1 for n in nodes if n["node_kind"] == "ACCOUNT" and n["node_id"] in membership)
    account_count = sum(1 for n in nodes if n["node_kind"] == "ACCOUNT")
    leaves = [n for n in nodes if n["node_kind"] == "MODEL_LEAF"]
    constituent_value = round(sum(n["amount"]["value"] for n in leaves), 2)
    # L0 CATEGORY (CTO ruling msg 102475, IB-mr-202): the assigned-strategy plug is the only
    # SLEEVE-kind ":client" node left -- the unassigned-account Client bucket is CATEGORY-kind now,
    # so this no longer needs the old ":strategy:" id-substring test to tell them apart.
    plug_value = round(sum(n["amount"]["value"] for n in nodes
                           if n["node_kind"] == "SLEEVE" and n["node_id"].endswith(":client")), 2)
    coverage = {"nodes_resolved": assigned_count, "nodes_attempted": account_count,
                "remainder": {"amount": round(total_before - constituent_value, 2), "units": "USD",
                              "reason": "%d of %d custody account(s) carry an assigned Rebalancer strategy; %.2f USD sits in "
                                        "constituent model leaves (ASSIGNED = account value x blend weight), the rest is "
                                        "Client (the plug, %.2f USD across assigned accounts) or unassigned custody"
                                        % (assigned_count, account_count, constituent_value, plug_value)}}
    by_qualifier = {}
    for n in leaves:
        q = next((f.split("=", 1)[1] for f in n["classification"]["capability_facts"] if f.startswith("qualifier=")), "?")
        by_qualifier[q] = by_qualifier.get(q, 0) + 1
    manifest["membership"] = {"assigned_accounts": assigned_count, "assigned_value": assigned_value,
                              "strategies": len({m["model_id"] for m in membership.values()}),
                              "constituent_models": len({n["model_id"]["value"] for n in leaves}),
                              "constituent_leaf_rows": len(leaves), "constituent_value": constituent_value,
                              "client_plug_value": plug_value, "leaf_rows_by_qualifier": by_qualifier,
                              "definition_date": definition_date, "definition_rows": int(len(definition)),
                              "join": "fact_model_assignment.strategy_name -> fact_model_roster.model_name, exact, unique; "
                                      "fact_model_blend children x fact_model_definition components (CTO ruling "
                                      "IRPT-COT-HOLDINGS-TREE-20260924)"}
    # TWO FEEDS, TWO CLOCKS, AND FOR COT THEY GENUINELY DIFFER: fact_holdings and
    # fact_model_assignment land on their own partitions. This is the firm whose snapshot can
    # actually show a model assignment dated after the holdings it attributes.
    recompute_weights(nodes)
    stamped = stamp_clocks(nodes, value_date, assign_date)
    return nodes, {"coverage": coverage, "manifest": manifest,
                  "source_completion_date": value_date,
                  "custody_as_of": value_date, "overlay_as_of": assign_date,
                  "holdouts": holdouts,
                  "assigned_without_custody": {
                      "account_count": len(assigned_ids - custody_ids),
                      "denominator": "%d of %d overlay account(s) absent from custody"
                                     % (len(assigned_ids - custody_ids), len(assigned_ids)),
                      "source": "fact_model_assignment date=%s minus fact_holdings date=%s"
                                % (assign_date, value_date)},
                  "nodes_stamped": stamped}


def eclipse_target_percent_node(model_id, target_percent: float, *, join_matched: int,
                                join_attempted: int, node_id="inf:target_pct",
                                parent_node_id=None) -> dict:
    """A NODE FOR ECLIPSE'S RAW `targetPercent` FIELD, IF ANY CALLER EVER SURFACES ONE.

    NOT called anywhere in `build_inf` today -- this cell does not read
    `model_composition`/`portfolios_full`'s target-percent columns at all, precisely
    because the PRD v0.4 B12 row says 'Eclipse numeric ids get a declared
    canonicalization and `targetPercent` units stay uncertified until certified'. This
    function exists so that claim has a MECHANICAL guard rather than a promise: any
    future caller that DOES surface a raw Eclipse target percentage must route it through
    here, and `provenance.claim` is HARDCODED to 'held' -- never 'measured' -- until a
    future cell certifies the unit convention and repoints this constant.
    """
    return _node(node_id, parent_node_id, 1, "MODEL_LEAF", "TARGET", float(target_percent),
                "WEIGHT_DECIMAL", "PARENT_NODE", 1.0, float(target_percent), None,
                "holdings_snapshot.eclipse_target_percent_node",
                "Eclipse targetPercent (raw, UNCERTIFIED unit convention)",
                join_matched, join_attempted, "held",
                model_id={"namespace": "ECLIPSE_MODEL_ID", "value": str(model_id)})


# 49F: `build_49f` (SmartX-only custody, retained above for review) is superseded by the meshed
# builder -- Schwab custody as the population and value, SmartX as the model authority
# (Andrew-direct 2026-09-23 ~22:4xZ at 2.0.0_SA_COO~M; holdings_49f.py carries the measurements).
# INF: `build_inf_actual` (Client-only tree, retained above) is superseded by the meshed builder that
# keeps the same validated Orion custody and adds Eclipse membership at its measured grain.
BUILDERS = {"49financial": holdings_49f.build_49f_meshed, "inflection": holdings_inf.build_inf_meshed,
            "cottonwood": build_cot}


# --------------------------------------------------------------------------- snapshot assembly
def build_snapshot(firm_id: str, s3, as_of: str, *, account_ids=None) -> dict:
    if account_ids is not None:
        if firm_id != "cottonwood":
            raise ValueError("explicit account construction is not yet supported for this firm")
        nodes, extra = build_cot(s3, as_of, account_ids=account_ids)
    else:
        nodes, extra = BUILDERS[firm_id](s3, as_of)
    assert_bases_not_spliced(nodes)
    # CTO 100157: the builders that carry a name only inside capability_facts (49F, INF) get their
    # `display` derived here, in one place, and ONLY when the published contract admits the member.
    own_masks = extra.pop("account_masks", None) or {}
    if display_admitted():
        # CTO 101302: an ACCOUNT node carries ITS OWN masked tail and type; the directory's relationship-level
        # discriminator is the fallback only for an account the builder could not mask.
        directory_labels = _directory_account_labels(s3, firm_bucket_map().get(firm_id, ""), firm_id) if s3 is not None else {}
        account_labels = {**directory_labels, **own_masks}
        filled = fill_display_from_facts(nodes, account_labels)
        census = extra["manifest"].get("display_labels") or {"contract_admits_display": True}
        census.update({"filled_from_facts": filled, "account_labels_from_directory": len(directory_labels),
                       "account_labels_own_mask": len(own_masks),
                       **display_census(nodes)})
        extra["manifest"]["display_labels"] = census
    else:
        extra["manifest"].setdefault("display_labels", {"contract_admits_display": False, **display_census(nodes)})
    # every firm states its CUSTODY_UNITS census (build_cot writes its own richer block first)
    extra["manifest"].setdefault("custody_units", {"contract_admits_custody_units": custody_units_admitted(),
                                                   **custody_units_census(nodes)})
    # CTO 100905: asset class on SECURITY nodes, model code on MODEL_LEAF nodes, ONLY once admitted.
    if classification_admitted():
        extra["manifest"]["classification_members"] = {"contract_admits": True,
                                                       **annotate_classification(nodes)}
    else:
        extra["manifest"].setdefault("classification_members", {"contract_admits": False})

    account_nodes = [n for n in nodes if n["node_kind"] == "ACCOUNT"]
    unique_account_ids = sorted({n["node_id"] for n in account_nodes})
    total_value = round(sum(n["amount"]["value"] for n in account_nodes), 2)
    fingerprint = hashlib.sha256("|".join(unique_account_ids).encode("utf-8")).hexdigest()

    scope = {"resolved_scope_fingerprint": fingerprint, "firm_id": firm_id,
            "account_ids": unique_account_ids}
    source_set_revision = [{"source": extra["manifest"].get("source", firm_id),
                            "revision": "%s@%s" % (firm_id, extra["source_completion_date"]),
                            "completion_date": extra["source_completion_date"]}]
    # THE TWO SOURCE CLOCKS ARE CARRIED DISTINCT (IB-rt-7, C-S75) -- as their own named fields
    # AND as two entries in `source_as_of`, so a consumer reading either shape sees both. A
    # snapshot that collapsed them would still validate and would still reconcile; the only
    # thing that catches it is a producer that refuses to build one, which is
    # `assert_clocks_carried` below.
    custody_as_of = extra["custody_as_of"]
    overlay_as_of = extra["overlay_as_of"]
    clocks = {"business_date": extra["source_completion_date"],
             "as_of_timestamp": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
             "custody_as_of": custody_as_of,
             "overlay_as_of": overlay_as_of,
             "source_as_of": [
                 {"source": "%s (custody)" % extra["manifest"].get("source", firm_id),
                  "as_of": custody_as_of},
                 {"source": "%s (overlay)" % extra["manifest"].get("source", firm_id),
                  "as_of": overlay_as_of}]}
    custody_totals = {"unique_account_count": len(unique_account_ids),
                      "unique_position_count": len([n for n in nodes if n["node_kind"] == "SECURITY"]),
                      "total_market_value": {"value": total_value, "currency": "USD"},
                      "deduplicated": True}
    before = round(float(extra["manifest"].get("total_market_value", 0.0)), 2)
    # UIC-14 (CTO ruling msg 102443, cell IB-mr-203): this snapshot's own source vendor keys,
    # derived from the registry by the sources this build actually opened (never a per-firm constant).
    source_vendor_keys_out = source_vendor_keys(extra["manifest"].get("source"))
    snapshot = {
        "scope": scope, "source_set_revision": source_set_revision, "clocks": clocks,
        "custody_totals": custody_totals, "nodes": nodes, "coverage": extra["coverage"],
        "source_vendor_keys": source_vendor_keys_out,
        "attribution_holdouts": {
            "unassigned": extra["holdouts"],
            "assigned_without_custody": extra["assigned_without_custody"],
            "reconcile": {
                "total_before": before,
                "total_after": total_value,
                "difference": round(before - total_value, 2),
                "tolerance": RECON_TOLERANCE_USD,
                "reconciled": abs(before - total_value) <= RECON_TOLERANCE_USD,
            },
        },
        "_manifest": extra["manifest"],
    }
    # REFUSED AT THE PRODUCER, not merely described in the contract: the two clocks are
    # OPTIONAL in v1 (the contract is immutable and an added field may not be made required),
    # so the schema cannot be the thing that catches a collapse. This can, and it runs on every
    # build including the QA ones.
    snapshot["_clock_census"] = assert_clocks_carried(snapshot)
    return snapshot


def reconcile_before_after(snapshot: dict) -> "tuple[bool, float, float]":
    """Unique custody total BEFORE the overlay (the manifest's raw sum) vs AFTER (the
    account nodes' sum) -- S12-AC1 arm (b). Equal to the cent, or the divergence is a
    real defect, never rounded away."""
    before = round(float(snapshot["_manifest"].get("total_market_value", 0.0)), 2)
    after = round(snapshot["custody_totals"]["total_market_value"]["value"], 2)
    nodes = snapshot.get("nodes") or []
    by_id = {n["node_id"]: n for n in nodes}
    if len(by_id) != len(nodes):
        return False, before, after
    partitions = {}
    for n in nodes:
        value = n.get("amount", {}).get("value")
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
            return False, before, after
        parent = n.get("parent_node_id")
        if parent is not None:
            if parent not in by_id:
                return False, before, after
            if n.get("basis") != "TARGET":
                key = (parent, n.get("basis"))
                partitions[key] = partitions.get(key, 0.0) + value
    balanced = all(abs(value - by_id[parent]["amount"]["value"]) <= RECON_TOLERANCE_USD
                   for (parent, _basis), value in partitions.items())
    return balanced and abs(before - after) <= RECON_TOLERANCE_USD, before, after


# --------------------------------------------------------------------------- validation / destination
def load_contract() -> dict:
    return json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))


def contract_validator_class():
    """The jsonschema validator class for the `_contracts/` schemas, TOLERANT OF THE INSTALLED
    VERSION (row IRPT_BCKEND-W2-S56). The contracts declare draft 2020-12, but the MDPF host runs
    jsonschema 3.2.0, which has no 2020-12 class (it arrived in 4.18.0). None of the eleven
    contracts uses a 2019-09/2020-12-only keyword, a `$ref` or an array-form `items`, so draft 7
    grades them identically: the 2020-12 class where the installed version has it, else draft 7.
    DUPLICATED VERBATIM in directory_runner.py and holdings_snapshot.py (a shared module would
    be a new bundle member)."""
    import jsonschema
    # vars(), not getattr(): jsonschema 4.x defines a module __getattr__ that raises NameError
    # (not AttributeError) for this name once it is absent, which getattr's default cannot catch.
    return vars(jsonschema).get("Draft202012Validator") or jsonschema.Draft7Validator


def error_path(err) -> str:
    """The failing location as a JSONPath string, built from `absolute_path` (present in
    jsonschema 3.2.0 and 4.x) -- the same text 4.x's `json_path` renders, e.g. `$.ids.firm_id`."""
    return "$" + "".join(f"[{p}]" if isinstance(p, int) else f".{p}" for p in err.absolute_path)


def validate_snapshot(snapshot: dict) -> "tuple[bool, list]":
    """jsonschema, LOCAL validation. This runner is a GOLD SCRIPT, never a Lambda -- it
    does not ship or need the `irpt-common` Lambda layer (IB-s-13, in flight) that would
    carry jsonschema into a Lambda runtime. Stated explicitly per the hand-off. Each error
    line names its failing path, as the directory runner's does."""
    schema = load_contract()
    body = {k: v for k, v in snapshot.items() if not k.startswith("_")}
    validator = contract_validator_class()(schema)
    errors = sorted(validator.iter_errors(body), key=lambda e: list(e.path))
    return (not errors), [f"{error_path(e)}: {e.message}" for e in errors[:10]]


def gold_parquet_bytes(nodes) -> bytes:
    """The Gold tier of one snapshot, from its nodes -- the ONE definition `land` and any republish share.
    Scalar economics remain queryable in Gold; canonical node JSON preserves every nested identity,
    classification, denominator and provenance field."""
    from publication import canonical_bytes
    rows = [{"node_id": n["node_id"], "parent_node_id": n.get("parent_node_id"),
             "node_kind": n["node_kind"], "basis": n["basis"],
             "amount_value": n["amount"]["value"],
             "node_json": canonical_bytes(n).decode("utf-8")}
            for n in nodes]
    output = io.BytesIO()
    pd.DataFrame(rows).to_parquet(output, index=False)
    return output.getvalue()


def land(bucket: str, prefix: str, as_of: str, payload: dict, upload: bool,
         local_out: "str | None", s3_client=None, expected=None) -> dict:
    """Emit immutable Gold/Platinum artifacts; advance only the verified index."""
    from publication import HoldingsPublication, canonical_bytes, digest
    firm = payload["scope"]["firm_id"]
    publisher = HoldingsPublication(s3_client, firm, qa=prefix == QA_PREFIX)
    if prefix not in (PROD_PREFIX, QA_PREFIX):
        raise RuntimeError("REFUSED: unknown publication namespace")
    body_payload = {k: v for k, v in payload.items() if not k.startswith("_")}
    body = canonical_bytes(body_payload)
    revision = digest(body)
    parquet = gold_parquet_bytes(payload["nodes"])
    partition = "date=" + as_of
    gold_location = publisher.location("gold", partition, revision + ".parquet")
    platinum_location = publisher.location("platinum", partition, revision + ".json")
    if gold_location[0] != bucket or platinum_location[0] != bucket:
        raise RuntimeError("REFUSED: canonical publication and verified firm home disagree")
    out = {"bucket": bucket, "revision": revision, "key": platinum_location[1],
           "gold_key": gold_location[1], "bytes": len(body), "uploaded": False,
           "sha256": digest(body), "gold_sha256": digest(parquet)}
    if local_out:
        for location, content in ((gold_location, parquet), (platinum_location, body)):
            target = Path(local_out) / location[0] / location[1]
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
        out["local_state"] = "UNPUBLISHED_NO_VERSIONED_ACCEPTANCE"
    if upload:
        if expected is None or s3_client is None:
            raise RuntimeError("REFUSED: publication must capture index before building")
        out["accepted"] = publisher.publish(body_payload, parquet, business_date=as_of,
            expected=expected, validate=lambda doc: validate_snapshot(payload)[0]
                and reconcile_before_after(payload)[0], source_objects=payload.get("_source_objects"))
        out["uploaded"] = True
    return out


# --------------------------------------------------------------------------- the publish gate (FWD-14)
# PRD IRPT_BCKEND v0.31 + v0.32 (Andrew-direct @f8e7d992dd): a firm's holdings publication never gets WORSE from one
# fire to the next. Before the firm's index moves, the candidate is compared with the publication the firm serves NOW.
# WORSE is any of SIX conditions; on WORSE the index does not move, the firm keeps its last good publication, and ONE
# refusal record per firm is written beside the manifest. A gate on the producer's own write -- never a monitor or alert.
PUBLISH_SIX_CLASSES = frozenset({"cash", "fixed_income", "equity", "structured", "alternatives", "commodities"})
PUBLISH_GATE_CONDITIONS = ("reconcile_difference", "multi_asset", "class_outside_six", "classified_security_lost",
                           "account_lost", "source_frontier_older")
PUBLISH_REFUSAL_OBJECT = "publish_refusal.json"   # the object beside current/manifest.json; its address is address() output
PUBLISH_REFUSAL_SCHEMA = "irpt-holdings-publish-refusal-v1"
PUBLISH_GATE_ID_CAP = 1000                        # ids named per condition; the count is always the true count


def _gate_security_key(node) -> "str | None":
    sid = node.get("security_id") or {}
    ns, value = sid.get("namespace"), sid.get("value")
    return "%s:%s" % (ns, value) if ns and value else None


def _gate_ids(ids) -> dict:
    ids = sorted({str(i) for i in ids})
    return {"count": len(ids), "ids": ids[:PUBLISH_GATE_ID_CAP], "ids_truncated": len(ids) > PUBLISH_GATE_ID_CAP}


def _gate_account_ids(nodes) -> "set[str]":
    return {n["node_id"] for n in nodes if n.get("node_kind") == "ACCOUNT" and n.get("parent_node_id") is None}


def served_publication(publisher, expected) -> "dict | None":
    """The publication the firm serves NOW, read by exact version from the index `begin()` captured -- or None when the
    firm has none. Read from the Gold parquet (bounded 64 MB) and the manifest, never through the 4 MB whole-document
    load, so a multi-part publication of a large firm is still comparable."""
    doc = (expected or {}).get("document")
    if doc is None:
        return None
    import publication as pub
    import pyarrow.parquet as pq
    date = doc["latest_date"]
    row = doc["dates"][date]
    revision, partition = row["revision"], "date=" + date
    manifest = json.loads(publisher.read_exact(row["manifest"], expected_location=publisher.location(
        "platinum", partition, revision + ".manifest.json"), max_bytes=pub.MAX_JSON_BYTES))
    data = publisher.read_exact(manifest["gold"], expected_location=publisher.location(
        "gold", partition, revision + ".parquet"), max_bytes=pub.MAX_GOLD_BYTES)
    nodes = [json.loads(s) for s in pq.read_table(io.BytesIO(data), columns=["node_json"]).column("node_json").to_pylist()]
    return {"business_date": (manifest.get("clocks") or {}).get("business_date") or date, "index_date": date,
            "revision": revision, "nodes": nodes, "account_ids": _gate_account_ids(nodes),
            "index_version": ((expected.get("reference") or {}).get("version_id"))}


def _directory_entries(s3, bucket) -> "list | None":
    """The landed DirectoryEntry list (prod prefix, then QA), or None when no directory is readable."""
    for prefix in (PROD_PREFIX.replace("holdings", "directory"), QA_PREFIX.replace("holdings", "directory")):
        try:
            ptr = json.loads(s3.get_object(Bucket=bucket, Key=prefix + "/latest.json")["Body"].read())
            doc = json.loads(s3.get_object(Bucket=bucket, Key=ptr["key"])["Body"].read())
        except Exception:  # noqa: BLE001 -- absent is a state, handled by the next prefix, then by "names none"
            continue
        return doc.get("entries", [])
    return None


def closed_account_ids(s3, bucket, firm_id) -> "set[str]":
    """Accounts the firm's SOURCE records as closed or terminated: the landed DirectoryEntry set (IB-s-1) carries the
    custodian's `termination.indicator` per entry (49F `dim_account.account_is_open`/`closed_date`; a relationship is
    TERMINATED only when every account in it is). An absent directory names none, so the exemption fails CLOSED: with
    nothing recorded a lost account is refused, never waved through."""
    ids = set()
    for e in _directory_entries(s3, bucket) or []:
        if (e.get("termination") or {}).get("indicator") == "TERMINATED":
            ids.update(e.get("ids", {}).get("account_ids", []))
    return ids


def directory_marks_no_closures(s3, bucket, firm_id) -> bool:
    """PRD v0.33: True only when a directory IS readable, has entries, and NO entry carries a termination marking other
    than UNKNOWN (cottonwood marks every entry UNKNOWN). An absent or empty directory is False: fails CLOSED."""
    entries = _directory_entries(s3, bucket)
    if not entries:
        return False
    return all(((e.get("termination") or {}).get("indicator") or "UNKNOWN") == "UNKNOWN" for e in entries)


def evaluate_publish_gate(candidate: dict, served: "dict | None", closed_accounts=lambda: set(),
                          marks_no_closures=lambda: False) -> dict:
    """Compare the candidate snapshot with the served publication. Returns
    {"outcome": "REFUSED"|"PUBLISHED", "conditions": [...WORSE...], "listed": {...never refused...}}.
    A first publication (served is None) is judged on the ABSOLUTE conditions only: reconcile, multi_asset, class
    outside the six. `closed_accounts` is called only if an account was lost. PRD v0.33: where `marks_no_closures()` is
    True (the firm's directory marks every entry UNKNOWN) a lost account is LISTED, never refused on its own."""
    nodes = candidate.get("nodes") or []
    secs = [n for n in nodes if n.get("node_kind") == "SECURITY"]
    conditions, listed = [], {}

    def add(name, ids, **detail):
        conditions.append({"condition": name, **_gate_ids(ids), **detail})

    recon_ok, before, after = reconcile_before_after(candidate)
    diff = round(before - after, 2)
    if not recon_ok or abs(diff) > RECON_TOLERANCE_USD:
        add("reconcile_difference", [], difference=diff, tolerance=RECON_TOLERANCE_USD,
            balanced=bool(recon_ok))
        conditions[-1]["count"] = 1
    multi = [_gate_security_key(n) or n["node_id"] for n in secs if n.get("asset_class") == "multi_asset"]
    if multi:
        add("multi_asset", multi)
    outside = {n.get("asset_class") for n in secs} - PUBLISH_SIX_CLASSES - {None, "unclassified"}
    if outside:
        add("class_outside_six", [_gate_security_key(n) or n["node_id"] for n in secs if n.get("asset_class") in outside],
            classes=sorted(str(c) for c in outside))
    now_unclassified = {_gate_security_key(n) for n in secs if n.get("asset_class") == "unclassified"} - {None}
    if served is not None:
        ps = [n for n in served["nodes"] if n.get("node_kind") == "SECURITY"]
        placed = {_gate_security_key(n) for n in ps if n.get("asset_class") not in (None, "unclassified")} - {None}
        unplaced = {_gate_security_key(n) for n in ps if n.get("asset_class") in (None, "unclassified")} - {None}
        lost_class = now_unclassified & (placed - unplaced)
        if lost_class:
            add("classified_security_lost", lost_class)
        listed["new_unclassified"] = _gate_ids(now_unclassified - placed - unplaced)
        have = set((candidate.get("scope") or {}).get("account_ids") or []) | _gate_account_ids(nodes)
        gone = served["account_ids"] - have
        if gone:
            closed = closed_accounts() & gone
            if closed:
                listed["closed_accounts_not_refused"] = _gate_ids(closed)
            if gone - closed:
                if marks_no_closures():
                    listed["account_lost_not_refused"] = _gate_ids(gone - closed)
                else:
                    add("account_lost", gone - closed)
        cand_date = (candidate.get("clocks") or {}).get("business_date")
        if not cand_date:
            add("source_frontier_older", [], reason="candidate carries no source business date", served_frontier=served["business_date"])
            conditions[-1]["count"] = 1
        else:
            behind = tcal.trading_days_behind(cand_date, served["business_date"])
            if behind > 0:
                add("source_frontier_older", [cand_date], candidate_frontier=cand_date,
                    served_frontier=served["business_date"], trading_days_behind=behind)
                conditions[-1]["count"] = behind
    else:
        listed["new_unclassified"] = _gate_ids(now_unclassified)
    return {"outcome": "REFUSED" if conditions else "PUBLISHED", "conditions": conditions, "listed": listed}


def write_refusal_record(publisher, s3, candidate: dict, served: "dict | None", gate: dict) -> dict:
    """ONE refusal record per firm, at address() output beside current/manifest.json, overwritten by each refused fire.
    It names the served index version it was refused against, so a reader can tell a record is stale once the index moves."""
    from publication import canonical_bytes, digest
    bucket, key = publisher.location("platinum", "current", PUBLISH_REFUSAL_OBJECT)
    body = {k: v for k, v in candidate.items() if not k.startswith("_")}
    record = {"schema_version": PUBLISH_REFUSAL_SCHEMA, "firm_id": publisher.firm, "outcome": "REFUSED",
              "refused_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
              "candidate": {"business_date": (candidate.get("clocks") or {}).get("business_date"),
                            "revision": digest(canonical_bytes(body)), "node_count": len(candidate.get("nodes") or []),
                            "account_count": len((candidate.get("scope") or {}).get("account_ids") or [])},
              "served": None if served is None else {k: served[k] for k in ("business_date", "revision", "index_version")},
              "conditions": gate["conditions"], "listed": gate["listed"]}
    out = s3.put_object(Bucket=bucket, Key=key, Body=canonical_bytes(record), ContentType="application/json")
    return {"bucket": bucket, "key": key, "version_id": out.get("VersionId")}


# --------------------------------------------------------------------------- orchestration
def select_business_date(now: "dt.date | None" = None) -> str:
    target = tcal.expected_last_trading_day(now if now is not None else dt.datetime.now(dt.timezone.utc))
    return target.isoformat()


# THE PUBLISH PRINCIPAL (R-44 split by bucket; CTO R4 row 4). The publication lands in the firm's OWN bucket, whose policy
# admits only a principal carrying the firm's scope. A scheduled dispatch names that principal here, per firm; the
# builders' source reads stay on the host session. Unset -> the caller's client, which is an operator run, unchanged.
PUBLISH_ROLE_ENV = "IRPT_HOLDINGS_PUBLISH_ROLE_ARN"
PUBLISH_SESSION_NAME = "irpt-holdings-publish"


def publish_client(default, sts=None):
    """The s3 client the publication writes with: an assumed session on the named publish principal, else `default`."""
    arn = (os.environ.get(PUBLISH_ROLE_ENV) or "").strip()
    if not arn:
        return default
    import boto3
    creds = (sts or boto3.client("sts", region_name="us-east-1")).assume_role(
        RoleArn=arn, RoleSessionName=PUBLISH_SESSION_NAME)["Credentials"]
    return boto3.client("s3", region_name="us-east-1", aws_access_key_id=creds["AccessKeyId"],
                        aws_secret_access_key=creds["SecretAccessKey"], aws_session_token=creds["SessionToken"])


def run_firm(firm_id: str, s3, *, qa: bool, upload: bool, local_out: "str | None",
            as_of: "str | None", now: "dt.date | None" = None, account_ids=None) -> dict:
    business_date = as_of or select_business_date(now)
    pub_s3 = publish_client(s3) if upload and s3 is not None else s3
    publisher = HoldingsPublication(pub_s3, firm_id, qa=qa)
    expected = publisher.begin() if upload and s3 is not None else None
    if account_ids is not None and expected is not None and expected.get("document") is not None:
        raise RuntimeError("REFUSED: bounded initial publication cannot replace an existing firm index")
    inputs = VersionedInputs(s3) if s3 is not None else s3
    snapshot = (build_snapshot(firm_id, inputs, business_date, account_ids=account_ids)
                if account_ids is not None else build_snapshot(firm_id, inputs, business_date))
    # A source-selection cutoff is not the source's economic business date. An invalid build
    # without clocks must reach the REFUSED path below, never a KeyError here.
    publication_date = (snapshot.get("clocks") or {}).get("business_date") or business_date
    if isinstance(inputs, VersionedInputs):
        from publication import canonical_bytes, digest
        receipts = inputs.receipts()
        if not receipts:
            raise RuntimeError("REFUSED: no versioned source receipts for publication")
        snapshot["_source_objects"] = receipts
        snapshot["source_set_revision"].append({
            "source": "irpt-source-objects", "revision": digest(canonical_bytes(receipts)),
            "completion_date": snapshot["clocks"]["business_date"]})
    recon_ok, before, after = reconcile_before_after(snapshot)
    valid, errors = validate_snapshot(snapshot)
    # The generated map includes legacy routed aliases for existing input reads.
    # New publication uses the canonical builder's primary private firm home.
    bucket = publisher.location("platinum", "current", "manifest.json")[0]
    prefix = QA_PREFIX if qa else PROD_PREFIX
    # THE DIFFERENCE CONTROL RUNS ON EVERY BUILD (IB-rt-7 arm (b)). The honest snapshot must
    # HOLD its holdouts and the redistributing build of the SAME snapshot must FAIL -- both
    # while reconciling to the cent, which is precisely why the reconcile alone is not a
    # control. Refusing here rather than only in a test means a build that starts
    # redistributing cannot land.
    holdouts = snapshot["attribution_holdouts"]["unassigned"]
    held_ok, held_census = holdouts_held(snapshot, holdouts["account_ids"])
    wrong = redistribute_holdouts(snapshot)
    wrong_ok, wrong_census = holdouts_held(wrong, holdouts["account_ids"])
    wrong_recon = abs(round(sum(n["amount"]["value"] for n in wrong["nodes"]
                                if n["node_kind"] == "ACCOUNT"), 2) - after)
    if not held_ok:
        raise RuntimeError("REFUSED: %s built a snapshot whose unassigned holdouts are not "
                           "visible as account nodes: %s" % (firm_id, held_census))
    if wrong_ok and holdouts["account_count"]:
        raise RuntimeError("REFUSED: the redistributing build PASSED the holdout check for %s "
                           "-- the check cannot discriminate and proves nothing" % firm_id)
    # THE PUBLISH GATE (FWD-14) runs on an upload that captured the firm's index; there a reconcile difference is one of
    # its six WORSE conditions (refused WITH a record), not a bare raise. Without a captured index the old raise stands.
    gated = bool(upload and expected is not None)
    if not valid or (not recon_ok and not gated):
        raise RuntimeError("REFUSED: holdings validation/reconciliation failed before publication: %s"
                           % errors)
    # A builder may hand back a CANDIDATE it refuses to publish (49F/INF without a firm report
    # currency attestation): local and dry runs proceed, an upload does not.
    if upload and snapshot["_manifest"].get("publication_refused"):
        raise RuntimeError(snapshot["_manifest"]["publication_refused"])
    recompute_weights(snapshot["nodes"])  # also rejects duplicate identity before any write
    gate = {"outcome": "NOT_EVALUATED", "reason": "no upload with a captured index: nothing is published"}
    if gated:
        served = served_publication(publisher, expected)
        gate = evaluate_publish_gate(snapshot, served, lambda: closed_account_ids(
            s3, firm_bucket_map().get(firm_id, ""), firm_id), lambda: directory_marks_no_closures(
            s3, firm_bucket_map().get(firm_id, ""), firm_id))
        gate["served"] = None if served is None else {k: served[k] for k in ("business_date", "revision", "index_version")}
        if gate["outcome"] == "REFUSED":
            try:
                gate["refusal_record"] = write_refusal_record(publisher, pub_s3, snapshot, served, gate)
            except Exception as exc:  # noqa: BLE001 -- the refusal stands; the index does not move either way
                gate["refusal_record"] = None
                gate["refusal_record_error"] = "%s: %s" % (type(exc).__name__, exc)
    landed = ({"bucket": bucket, "uploaded": False, "refused": True}
              if gate["outcome"] == "REFUSED" else
              land(bucket, prefix, publication_date, snapshot, upload, local_out,
                   s3_client=pub_s3, expected=expected))
    return {"firm_id": firm_id, "business_date": publication_date, "publish_gate": gate,
           "source_cutoff": business_date, "reconcile_ok": recon_ok,
           "reconcile_before": before, "reconcile_after": after, "schema_valid": valid,
           "schema_errors": errors, "landed": landed, "coverage": snapshot["coverage"],
           "manifest": snapshot["_manifest"], "node_count": len(snapshot["nodes"]),
           "unique_account_count": snapshot["custody_totals"]["unique_account_count"],
           "clocks": snapshot["_clock_census"],
           "holdouts": {k: v for k, v in holdouts.items() if k != "account_ids"},
           "holdouts_held": held_census,
           "difference_control": {
               "redistributing_build_holds_holdouts": wrong_ok,
               "redistributing_build_census": wrong_census,
               "redistributing_build_total_drift_usd": round(wrong_recon, 2),
               "reading": ("the wrong build moves %0.2f USD out of %d account(s) and still "
                           "reconciles to within %0.2f USD -- the total is not the control"
                           % (wrong.get("_redistributed", {}).get("value", 0.0),
                              wrong.get("_redistributed", {}).get("accounts", 0),
                              round(wrong_recon, 2)))}}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--firms", default="all")
    ap.add_argument("--as-of", default=None)
    ap.add_argument("--account-id", action="append", default=None,
                    help="Operator-bound COT initial publication census; refuses an existing index")
    ap.add_argument("--qa", action="store_true")
    ap.add_argument("--upload", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--local-out", default=None)
    args = ap.parse_args(argv)
    if args.upload and args.dry_run:
        ap.error("--upload and --dry-run are mutually exclusive")

    firms = list(BUILDERS) if args.firms == "all" else args.firms.split(",")
    if args.account_id is not None and firms != ["cottonwood"]:
        ap.error("--account-id requires exactly --firms cottonwood")
    import boto3
    s3 = boto3.client("s3", region_name="us-east-1")
    results = []
    for firm_id in firms:
        r = run_firm(firm_id, s3, qa=args.qa, upload=args.upload,
                    local_out=args.local_out, as_of=args.as_of,
                    account_ids=set(args.account_id) if args.account_id else None)
        results.append(r)
        if r["publish_gate"]["outcome"] == "REFUSED":
            print("REFUSED: %s keeps its last good publication; %s; record=%s"
                  % (firm_id, ", ".join("%s(%d)" % (c["condition"], c["count"]) for c in r["publish_gate"]["conditions"]),
                     r["publish_gate"].get("refusal_record")))
        else:
            print("OK: %s business_date=%s nodes=%d accounts=%d reconcile=%s(%0.2f/%0.2f) valid=%s"
                 % (firm_id, r["business_date"], r["node_count"], r["unique_account_count"],
                    r["reconcile_ok"], r["reconcile_before"], r["reconcile_after"], r["schema_valid"]))
    print(json.dumps({"results": results}, indent=1, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
