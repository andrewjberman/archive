"""portal_index -- the portal's purpose-built read tools (NFRA_MCPINDEX MX-t-8, round 2, decomp R2.1).

Ten read-only tools, each answering from ONE whole precomputed object the portal itself serves out of
`opal-data-portal-v2`, so a tool's figure and the page's figure are the same bytes (FWD-2 parity).
The tool set and the read fence come from the round-1 portal analysis
(org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/0.9.0_WK_NFRA_MCPINDEX~3/analysis-portal.result.md, AC7 + AC8).

THE FENCE (the one control, `read_object`): every tool owns an exact property prefix and an exact set of
whole-object keys under it. A key outside the tool's own prefix (a sibling property), under an excluded
sub-prefix (`archive/`, `_manifests/`) or not one of its exact keys is REFUSED before any S3 call. Keys are
built from the tool's arguments and then passed THROUGH the fence, so an argument can never steer a read
elsewhere. Reads are by key, never by bucket listing. The advisor tools read ONLY
`platinum/advi/49financial/`; the Inflection/Cottonwood firm buckets are outside this integration.

THE ANSWER: every answer names the bucket, the key and the object's OWN as-of date (the field the object
carries, never the call time). An absent or empty object, or an object whose as-of is not the date asked
for, answers "no data for that date" and carries no figure at all -- never a 0.

DORMANT (integrations standard s.6): nothing here runs unless `portal_index` is in ENABLED_INTEGRATIONS;
the S3 client is built on the first call, never at import.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Callable, Optional

from ..base import (
    AuthKind,
    Integration,
    IntegrationError,
    IntegrationSpec,
    run_integration_tool,
)
from ...destructive_ops import OpClass

BUCKET = "opal-data-portal-v2"
S3_HOST = "opal-data-portal-v2.s3.amazonaws.com"
NO_DATA = "no data for that date"

MDPF_SCOPES = ("49financial", "cottonwood", "global", "inflection")
ADVI_SCOPES = ("49financial",)
ETF_FUNDS = ("DIVZ", "IDVZ", "PFDE", "PFOE")
ADVI_PERIODS = {"annual": "partner_analytics_annual.json", "quarterly": "partner_analytics_quarterly.json"}
ADVI_CHARTS = {"cumulative": "cumulative_chart.json", "timeseries": "timeseries_chart.json",
               "overview": "timeseries_overview.json"}

MDPF_PREFIX = "platinum/mdpf/"
ETFS_KEY = "platinum/etfs/positioning_data.json"
ADVI_PREFIX = "platinum/advi/49financial/"

# The analysis's AC8 exclusions inside the fenced prefixes: historical snapshots and pipeline bookkeeping.
EXCLUDED_PREFIXES = (
    "platinum/mdpf/archive/",
    "platinum/mdpf/_manifests/",
    "platinum/etfs/_manifests/",
    "platinum/advi/49financial/_manifests/",
)

_DATE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")

# destructive_ops SAFE tag (the shape destructive_ops.classify returns for a read).
_SAFE_TAG = {"class": OpClass.SAFE, "reversible": True, "irreversible": False,
             "native_undo": None, "blast_dimensions": []}


@dataclass(frozen=True)
class ToolFence:
    prefix: str            # the property prefix this tool may read under
    keys: frozenset        # the exact whole-object keys it may read
    as_of_field: str       # dotted path to the object's own as-of date ("{fund}" is the fund argument)
    catalog_ref: str       # DATA_CATALOG.yaml entity id (workflows/atom_decomposition/catalog_entries/<id>.yaml)


def _mdpf(table: str, as_of_field: str, ref: str, scopes=MDPF_SCOPES) -> ToolFence:
    return ToolFence(MDPF_PREFIX, frozenset("%s%s/%s" % (MDPF_PREFIX, s, table) for s in scopes),
                     as_of_field, ref)


def _advi(tables, ref: str) -> ToolFence:
    return ToolFence(ADVI_PREFIX, frozenset("platinum/advi/%s/%s" % (s, t) for s in ADVI_SCOPES for t in tables),
                     "data_as_of", ref)


FENCES = {
    "mdpf_get_aum_metrics": _mdpf("aum-metrics.json", "period", "portal_mdpf_aum_metrics"),
    "mdpf_get_account_distribution": _mdpf("account-distribution.json", "period",
                                           "portal_mdpf_account_distribution"),
    "mdpf_get_aggregate_aua": _mdpf("aggregate-aua-timeseries.json", "as_of_last", "portal_mdpf_aggregate_aua"),
    "mdpf_get_category_views": _mdpf("category-views.json", "as_of", "portal_mdpf_category_views"),
    "mdpf_get_non_model_assets": _mdpf("non-model-assets.json", "latest.date", "portal_mdpf_non_model_assets",
                                       scopes=("global",)),
    "etfs_get_positioning": ToolFence("platinum/etfs/", frozenset({ETFS_KEY}), "portfolios.{fund}.data_as_of",
                                      "portal_etfs_positioning"),
    "advi_get_leaderboard": _advi(("leaderboard.json",), "portal_advi_leaderboard"),
    "advi_get_mix_summary": _advi(("mix_summary.json",), "portal_advi_mix_summary"),
    "advi_get_partner_analytics": _advi(tuple(ADVI_PERIODS.values()), "portal_advi_partner_analytics"),
    "advi_get_growth_chart": _advi(tuple(ADVI_CHARTS.values()), "portal_advi_growth_chart"),
}
TOOLS = tuple(FENCES)

# Key builders: arguments -> the ONE key the tool asks for. The result is never trusted; read_object fences it.
KEY_BUILDERS: dict = {
    "mdpf_get_aum_metrics": lambda scope: "%s%s/aum-metrics.json" % (MDPF_PREFIX, scope),
    "mdpf_get_account_distribution": lambda scope: "%s%s/account-distribution.json" % (MDPF_PREFIX, scope),
    "mdpf_get_aggregate_aua": lambda scope: "%s%s/aggregate-aua-timeseries.json" % (MDPF_PREFIX, scope),
    "mdpf_get_category_views": lambda scope: "%s%s/category-views.json" % (MDPF_PREFIX, scope),
    "mdpf_get_non_model_assets": lambda: "%sglobal/non-model-assets.json" % MDPF_PREFIX,
    "etfs_get_positioning": lambda fund: ETFS_KEY,
    "advi_get_leaderboard": lambda scope: "platinum/advi/%s/leaderboard.json" % scope,
    "advi_get_mix_summary": lambda scope: "platinum/advi/%s/mix_summary.json" % scope,
    "advi_get_partner_analytics": lambda scope, period: "platinum/advi/%s/%s" % (
        scope, ADVI_PERIODS.get(period, "partner_analytics_%s.json" % period)),
    "advi_get_growth_chart": lambda scope, chart: "platinum/advi/%s/%s" % (
        scope, ADVI_CHARTS.get(chart, "%s.json" % chart)),
}

SPEC = IntegrationSpec(
    id="portal_index",
    display_name="Portal precomputed objects (mdpf / etfs / advi)",
    description="Read-only purpose-built tools over the portal's own precomputed objects in "
                "opal-data-portal-v2: each tool reads ONE whole object by its exact key, fenced to its own "
                "property prefix, and answers with the object's own as-of date.",
    auth_kind=AuthKind.NONE,          # the gateway instance role (opal-gateway-role) reads the bucket
    # One field, three C3 system prefixes: the tool names follow {system}_{function} over systems.json keys.
    tool_prefix="mdpf_|etfs_|advi_",
    read_only=True,
    min_tier="read_only",
    hosts=(S3_HOST,),
    tools=TOOLS,
    tool_classifications={t: dict(_SAFE_TAG) for t in TOOLS},   # every tool is one S3 GetObject
    tool_catalog_refs={t: f.catalog_ref for t, f in FENCES.items()},
)


class PrefixRefused(IntegrationError):
    """A read aimed outside the tool's own exact prefix/keys. Raised before any S3 call."""


def read_object(tool: str, key: str, getter: Callable[[str, str], Optional[bytes]]) -> Optional[bytes]:
    """THE FENCE: return the bytes of `key` (None when absent) only if `key` is one of `tool`'s own exact keys."""
    fence = FENCES.get(tool)
    if fence is None:
        raise PrefixRefused("unknown portal_index tool '%s'" % tool)
    if not isinstance(key, str) or not key.startswith(fence.prefix):
        raise PrefixRefused("refused: %s reads only under %s; '%s' is a sibling property's key"
                            % (tool, fence.prefix, key))
    for excluded in EXCLUDED_PREFIXES:
        if key.startswith(excluded):
            raise PrefixRefused("refused: '%s' is under the excluded prefix %s" % (key, excluded))
    if key not in fence.keys:
        raise PrefixRefused("refused: '%s' is not one of %s's exact keys" % (key, tool))
    return getter(BUCKET, key)


def _dig(obj, path: str):
    cur = obj
    for part in path.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur


def _is_empty(value) -> bool:
    return value is None or (isinstance(value, (dict, list, str)) and len(value) == 0)


def _no_data(tool: str, key: str, requested: str, object_as_of=None, reason: str = "") -> dict:
    out = {"status": "no_data", "message": NO_DATA, "tool": tool, "bucket": BUCKET, "key": key,
           "requested_as_of": requested or None, "object_as_of": object_as_of,
           "mismatch": bool(requested and object_as_of and requested != object_as_of)}
    if reason:
        out["reason"] = reason
    return out


def answer(tool: str, getter: Callable[[str, str], Optional[bytes]], as_of: str = "", **args) -> dict:
    """One tool's answer: fence the key, read the whole object, return it with the object's own as-of date."""
    if as_of and not _DATE.match(as_of):
        raise IntegrationError("as_of must be YYYY-MM-DD or empty; got %r" % as_of)
    key = KEY_BUILDERS[tool](**args)
    raw = read_object(tool, key, getter)
    if raw is None or not raw.strip():
        return _no_data(tool, key, as_of, reason="the object is absent or empty")
    try:
        obj = json.loads(raw.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        raise IntegrationError("%s is not a JSON object" % key)
    if _is_empty(obj):
        return _no_data(tool, key, as_of, reason="the object is empty")
    fence = FENCES[tool]
    fund = args.get("fund")
    if tool == "etfs_get_positioning":
        data = _dig(obj, "portfolios.%s" % fund) if isinstance(fund, str) and "." not in fund else None
        if _is_empty(data):
            return _no_data(tool, key, as_of, reason="the object carries no fund %r" % fund)
    else:
        data = obj
    as_of_field = fence.as_of_field.replace("{fund}", fund or "")
    object_as_of = _dig(obj, as_of_field)
    if not isinstance(object_as_of, str) or not object_as_of:
        raise IntegrationError("%s carries no as-of date at %s" % (key, as_of_field))
    if as_of and object_as_of[:10] != as_of:
        return _no_data(tool, key, as_of, object_as_of=object_as_of[:10],
                        reason="the served object is as of %s" % object_as_of[:10])
    return {"status": "ok", "tool": tool, "bucket": BUCKET, "key": key, "as_of": object_as_of,
            "as_of_field": as_of_field, "data": data}


def s3_getter() -> Callable[[str, str], Optional[bytes]]:
    """The live reader: one GetObject per call on the gateway instance role; absent -> None."""
    state: dict = {}

    def get(bucket: str, key: str) -> Optional[bytes]:
        if "client" not in state:
            import boto3   # local import: module import stays side-effect-free
            state["client"] = boto3.client("s3")
        try:
            return state["client"].get_object(Bucket=bucket, Key=key)["Body"].read()
        except Exception as exc:  # noqa: BLE001 -- mapped to a named outcome, never a boto trace
            code = getattr(exc, "response", {}).get("Error", {}).get("Code", "")
            if code in ("NoSuchKey", "404"):
                return None
            raise IntegrationError("read of %s failed: %s %s" % (key, type(exc).__name__, code))
    return get


def _no_credential() -> None:
    return None


class PortalIndexIntegration(Integration):
    """The ten portal tools. `getter` is injectable for tests; the default reads S3 on the first call."""

    def __init__(self, getter: Optional[Callable[[str, str], Optional[bytes]]] = None) -> None:
        self.spec = SPEC
        self._getter = getter

    def _get(self) -> Callable[[str, str], Optional[bytes]]:
        if self._getter is None:
            self._getter = s3_getter()
        return self._getter

    def _run(self, tool: str, args: dict) -> dict:
        return run_integration_tool(self.spec, tool, args,
                                    lambda _credential: answer(tool, self._get(), **args),
                                    credential_provider=_no_credential)

    def register(self, mcp) -> list[str]:
        run = self._run

        @mcp.tool()
        def mdpf_get_aum_metrics(scope: str, as_of: str = "") -> dict:
            """Model AUM (total, model, non-model, per model, quarter-end snapshots) for one scope
            (49financial, cottonwood, inflection or global), from platinum/mdpf/{scope}/aum-metrics.json.
            Answers with the object's own `period`. Optional as_of (YYYY-MM-DD) must match it."""
            return run("mdpf_get_aum_metrics", {"scope": scope, "as_of": as_of})

        @mcp.tool()
        def mdpf_get_account_distribution(scope: str, as_of: str = "") -> dict:
            """Account-size distribution for one scope, from platinum/mdpf/{scope}/account-distribution.json."""
            return run("mdpf_get_account_distribution", {"scope": scope, "as_of": as_of})

        @mcp.tool()
        def mdpf_get_aggregate_aua(scope: str, as_of: str = "") -> dict:
            """Daily AUA spine for one scope, from platinum/mdpf/{scope}/aggregate-aua-timeseries.json
            (as-of = `as_of_last`)."""
            return run("mdpf_get_aggregate_aua", {"scope": scope, "as_of": as_of})

        @mcp.tool()
        def mdpf_get_category_views(scope: str, as_of: str = "") -> dict:
            """Category tree for one scope, from platinum/mdpf/{scope}/category-views.json."""
            return run("mdpf_get_category_views", {"scope": scope, "as_of": as_of})

        @mcp.tool()
        def mdpf_get_non_model_assets(as_of: str = "") -> dict:
            """Enterprise non-model assets, from platinum/mdpf/global/non-model-assets.json (as-of = latest.date)."""
            return run("mdpf_get_non_model_assets", {"as_of": as_of})

        @mcp.tool()
        def etfs_get_positioning(fund: str, as_of: str = "") -> dict:
            """One Opal ETF's positioning (DIVZ, IDVZ, PFDE or PFOE) from platinum/etfs/positioning_data.json;
            answers with that fund's own data_as_of. Never sum two funds."""
            return run("etfs_get_positioning", {"fund": fund, "as_of": as_of})

        @mcp.tool()
        def advi_get_leaderboard(scope: str, as_of: str = "") -> dict:
            """Advisor leaderboard for 49financial, from platinum/advi/49financial/leaderboard.json."""
            return run("advi_get_leaderboard", {"scope": scope, "as_of": as_of})

        @mcp.tool()
        def advi_get_mix_summary(scope: str, as_of: str = "") -> dict:
            """Book mix summary for 49financial, from platinum/advi/49financial/mix_summary.json."""
            return run("advi_get_mix_summary", {"scope": scope, "as_of": as_of})

        @mcp.tool()
        def advi_get_partner_analytics(scope: str, period: str, as_of: str = "") -> dict:
            """Partner analytics for 49financial; period is annual or quarterly."""
            return run("advi_get_partner_analytics", {"scope": scope, "period": period, "as_of": as_of})

        @mcp.tool()
        def advi_get_growth_chart(scope: str, chart: str, as_of: str = "") -> dict:
            """Growth chart for 49financial; chart is cumulative, timeseries or overview."""
            return run("advi_get_growth_chart", {"scope": scope, "chart": chart, "as_of": as_of})

        return list(TOOLS)
