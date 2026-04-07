"""
Corpus query engine — two-tier data access.

Tier 1 (JSON):  S3 GET on pre-computed per-entity JSON. ~100ms.
                Use for any question about a specific contractor by UEI.
                Path: s3://{bucket}/json/contractor/{UEI}/{file}.json

Tier 2 (Parquet): DuckDB column-specific SELECT on S3 parquet via httpfs.
                  0.3-2s. Use for search, aggregation, ranking, comparison.

All queries run server-side. The client never sees the bucket, the schema,
or the query logic.
"""

import os
import json as _json
import logging
import duckdb

log = logging.getLogger(__name__)

# S3 bucket
PARQUET_BUCKET = os.environ.get("PARQUET_BUCKET", "corporeal-agg")
S3_REGION = os.environ.get("AWS_REGION", "us-east-1")

# ── Tier 1: JSON entity lookups ──────────────────────────────────

_s3_client = None


def _get_s3():
    global _s3_client
    if _s3_client is None:
        import boto3
        _s3_client = boto3.client("s3", region_name=S3_REGION)
    return _s3_client


def json_fetch(uei: str, file_key: str) -> dict:
    """Fetch pre-computed JSON for a contractor from S3.

    Args:
        uei: Contractor UEI (e.g., 'DUBENSKH21G8')
        file_key: File name without extension (e.g., 'identity', 'network', 'peers')

    Returns:
        Parsed dict, or None if not found.
    """
    s3_key = f"json/contractor/{uei}/{file_key}.json"
    try:
        resp = _get_s3().get_object(Bucket=PARQUET_BUCKET, Key=s3_key)
        return _json.loads(resp["Body"].read().decode("utf-8"))
    except _get_s3().exceptions.NoSuchKey:
        log.warning("JSON not found: s3://%s/%s", PARQUET_BUCKET, s3_key)
        return None
    except Exception as e:
        log.warning("JSON fetch failed for %s/%s: %s", uei, file_key, e)
        return None


# ── In-memory search index ────────────────────────────────────────

_search_index = None  # list of dicts, loaded once

_INDEX_CACHE_PATH = os.path.join(os.path.dirname(__file__), ".search_index_cache.json")


def _get_search_index() -> list:
    """Load the 354K-entry search index into memory.

    Priority: local disk cache → S3 download → empty list.
    Local cache avoids the 28s S3 download on every restart.
    """
    global _search_index
    if _search_index is not None:
        return _search_index

    # Try local disk cache first
    if os.path.exists(_INDEX_CACHE_PATH):
        try:
            with open(_INDEX_CACHE_PATH, "r") as f:
                _search_index = _json.load(f)
            log.info("Search index loaded from disk cache: %d entries", len(_search_index))
            return _search_index
        except Exception as e:
            log.warning("Disk cache read failed: %s", e)

    # Fall back to S3
    s3_key = "json/index/search_index.json"
    try:
        log.info("Downloading search index from S3 (%s)...", s3_key)
        resp = _get_s3().get_object(Bucket=PARQUET_BUCKET, Key=s3_key)
        raw = resp["Body"].read().decode("utf-8")
        _search_index = _json.loads(raw)
        log.info("Search index loaded from S3: %d entries", len(_search_index))
        # Cache to disk for next restart
        try:
            with open(_INDEX_CACHE_PATH, "w") as f:
                f.write(raw)
            log.info("Search index cached to disk: %s", _INDEX_CACHE_PATH)
        except Exception as e:
            log.warning("Disk cache write failed: %s", e)
    except Exception as e:
        log.error("Failed to load search index: %s", e)
        _search_index = []

    return _search_index


def preload_search_index():
    """Call at startup to load the index before any requests arrive."""
    _get_search_index()


def search_index_by_name(pattern: str, limit: int = 50) -> list[dict]:
    """Search contractors by name using in-memory index. Instant."""
    idx = _get_search_index()
    pattern_lower = pattern.lower()
    results = [e for e in idx if pattern_lower in e["n"].lower()]
    results.sort(key=lambda e: e["r"], reverse=True)
    return results[:limit]


def search_index_by_naics(code: str, limit: int = 50) -> list[dict]:
    """Search contractors by NAICS code using in-memory index."""
    idx = _get_search_index()
    results = [e for e in idx if e.get("c") == code]
    results.sort(key=lambda e: e["r"], reverse=True)
    return results[:limit]


def search_index_by_state(state: str, limit: int = 50) -> list[dict]:
    """Search contractors by state using in-memory index."""
    idx = _get_search_index()
    state_upper = state.upper()
    results = [e for e in idx if e.get("s") == state_upper]
    results.sort(key=lambda e: e["r"], reverse=True)
    return results[:limit]


def search_index_by_sector(sector: str, limit: int = 50) -> list[dict]:
    """Search contractors by 2-digit NAICS sector using in-memory index."""
    idx = _get_search_index()
    results = [e for e in idx if e.get("k") == sector]
    results.sort(key=lambda e: e["r"], reverse=True)
    return results[:limit]


def _format_search_result(entry: dict) -> dict:
    """Expand short keys to full names for API response."""
    return {
        "contractorUei": entry["u"],
        "contractorName": entry["n"],
        "primaryNaicsCode": entry.get("c"),
        "contractorState": entry.get("s"),
        "contractorCity": entry.get("y"),
        "revenueTtmMillions": entry.get("r", 0),
        "defenseLifetimePercent": entry.get("d", 0),
        "isPerforming": entry.get("p", False),
        "sectorCode": entry.get("k"),
    }


# ── Tier 2: Parquet search/aggregation ───────────────────────────

# Parquet file paths in S3
_TABLES = {
    "identity": f"s3://{PARQUET_BUCKET}/parquet/identity.parquet",
    "discovery": f"s3://{PARQUET_BUCKET}/parquet/discovery.parquet",
    "peers": f"s3://{PARQUET_BUCKET}/parquet/peers.parquet",
    "peer_group_lookup": f"s3://{PARQUET_BUCKET}/parquet/peer_group_lookup.parquet",
    "network": f"s3://{PARQUET_BUCKET}/parquet/network.parquet",
    "monthly": f"s3://{PARQUET_BUCKET}/parquet/monthly/*.parquet",
    "activity": f"s3://{PARQUET_BUCKET}/parquet/activity/*.parquet",
    "peer_percentiles": f"s3://{PARQUET_BUCKET}/parquet/peer_percentiles.parquet",
}

# Singleton connection
_db: duckdb.DuckDBPyConnection = None


def _snake_to_camel(name: str) -> str:
    """Convert UPPER_SNAKE_CASE to camelCase. E.g. CONTRACTOR_NAME -> contractorName."""
    parts = name.lower().split("_")
    return parts[0] + "".join(p.capitalize() for p in parts[1:])


def _get_db() -> duckdb.DuckDBPyConnection:
    """Get or create the DuckDB connection with S3 access."""
    global _db
    if _db is None:
        _db = duckdb.connect()
        _db.execute("INSTALL httpfs; LOAD httpfs;")
        _db.execute(f"SET s3_region='{S3_REGION}';")
        _db.execute("SET s3_use_ssl=true;")
        # Load AWS credentials from boto3 session for local dev.
        # On Lambda, IAM role provides credentials automatically.
        try:
            import boto3
            session = boto3.Session()
            creds = session.get_credentials()
            if creds:
                resolved = creds.get_frozen_credentials()
                _db.execute(f"SET s3_access_key_id='{resolved.access_key}';")
                _db.execute(f"SET s3_secret_access_key='{resolved.secret_key}';")
                if resolved.token:
                    _db.execute(f"SET s3_session_token='{resolved.token}';")
                log.info("DuckDB S3 credentials loaded from boto3 session")
        except Exception as e:
            log.warning("Could not load boto3 credentials for DuckDB: %s", e)
        # Create views with camelCase column aliases.
        # Parquet files use UPPER_SNAKE_CASE; all SQL and frontend expect camelCase.
        # The view layer is the adapter between the two conventions.
        for name, path in _TABLES.items():
            _db.execute(f"CREATE OR REPLACE VIEW _raw_{name} AS SELECT * FROM '{path}'")
            cols = [r[0] for r in _db.execute(
                f"SELECT column_name FROM information_schema.columns WHERE table_name = '_raw_{name}'"
            ).fetchall()]
            aliases = ", ".join(
                f'"{c}" AS {_snake_to_camel(c)}' for c in cols
            )
            _db.execute(f"CREATE OR REPLACE VIEW {name} AS SELECT {aliases} FROM _raw_{name}")
        log.info("DuckDB initialized with %d views (camelCase aliased)", len(_TABLES))
    return _db


def query(sql: str, params: list = None) -> list[dict]:
    """Execute a SQL query and return results as list of dicts.

    This is the only function the tools call. All SQL is constructed
    server-side — never from client input.
    """
    db = _get_db()
    try:
        if params:
            result = db.execute(sql, params)
        else:
            result = db.execute(sql)
        columns = [desc[0] for desc in result.description]
        rows = result.fetchall()
        return [dict(zip(columns, row)) for row in rows]
    except Exception as e:
        log.error("Query failed: %s\nSQL: %s", e, sql[:200])
        raise


def query_df(sql: str, params: list = None):
    """Execute a SQL query and return a pandas DataFrame."""
    db = _get_db()
    if params:
        return db.execute(sql, params).fetchdf()
    return db.execute(sql).fetchdf()


# ── Pre-built query functions (the tools call these) ─────────────────

def search_by_naics(naics_code: str, limit: int = 500) -> list[dict]:
    """All contractors in a 6-digit NAICS code."""
    return query("""
        SELECT contractorUei, contractorName, primaryNaicsCode,
               contractorCity, contractorState, revenueTtmMillions,
               pipelineActiveMillions, obligationsTtmMillions,
               entityClassificationLifetime, smallBusinessIndicator,
               defenseLifetimePercent, isPerforming
        FROM identity
        WHERE primaryNaicsCode = ?
        ORDER BY revenueTtmMillions DESC
        LIMIT ?
    """, [naics_code, limit])


def search_by_naics_sector(sector: str, limit: int = 500) -> list[dict]:
    """All contractors in a 2-digit NAICS sector."""
    return query(f"""
        SELECT contractorUei, contractorName, primaryNaicsCode,
               contractorCity, contractorState, revenueTtmMillions,
               pipelineActiveMillions, entityClassificationLifetime,
               defenseLifetimePercent, isPerforming
        FROM identity
        WHERE sectorCode = ?
        ORDER BY revenueTtmMillions DESC
        LIMIT ?
    """, [sector, limit])


def search_by_state(state: str, limit: int = 500) -> list[dict]:
    """All contractors in a state."""
    return query("""
        SELECT contractorUei, contractorName, primaryNaicsCode,
               contractorCity, contractorState, revenueTtmMillions,
               pipelineActiveMillions, entityClassificationLifetime,
               defenseLifetimePercent, isPerforming
        FROM identity
        WHERE contractorState = ?
        ORDER BY revenueTtmMillions DESC
        LIMIT ?
    """, [state.upper(), limit])


def search_by_name(name_pattern: str, limit: int = 50) -> list[dict]:
    """Search contractors by name (case-insensitive contains)."""
    return query("""
        SELECT contractorUei, contractorName, primaryNaicsCode,
               contractorCity, contractorState, revenueTtmMillions,
               pipelineActiveMillions, entityClassificationLifetime
        FROM identity
        WHERE LOWER(contractorName) LIKE LOWER(?)
        ORDER BY revenueTtmMillions DESC
        LIMIT ?
    """, [f"%{name_pattern}%", limit])


_IDENTITY_COLS = """
    contractorUei, contractorName, contractorCity, contractorState,
    contractorStateName, contractorCountry,
    entityClassificationLifetime, entityClassificationActive,
    primaryNaicsCode, primaryNaicsDescription,
    revenueTtmMillions, revenueGrowthYoyPercent,
    pipelineActiveMillions, obligationsActiveMillions,
    obligationsTtmMillions, obligationsActiveCount,
    awardsActiveCount, awardsActiveMillions,
    awardsLifetimeCount, awardsLifetimeMillions,
    defenseLifetimePercent, defenseActivePercent,
    primeObligationsLifetimePercent, primeObligationsActivePercent,
    primeObligationsActiveMillions, subObligationsActiveMillions,
    topAgencyName, totalAgencyObligationsMillions,
    compositeScore, performanceTier,
    cloudId, cloudStatus, cloudSimilarityEstimate,
    isPerforming, smallBusinessIndicator
""".strip()


def get_identity(uei: str) -> dict:
    """Key identity fields for a contractor (~30 fields, sub-second over S3).

    Avoids SELECT * on the 134-column identity parquet which forces DuckDB to
    read all column chunks (~1.5GB). Selecting specific columns uses predicate
    pushdown + column pruning for fast remote queries.
    """
    rows = query(f"SELECT {_IDENTITY_COLS} FROM identity WHERE contractorUei = ?", [uei])
    return rows[0] if rows else {}


def get_peers(uei: str) -> dict:
    """Peer group positioning for a contractor."""
    rows = query("SELECT * FROM peers WHERE contractorUei = ?", [uei])
    return rows[0] if rows else {}


def get_peer_group(uei: str) -> list[dict]:
    """All contractors in the same peer vector group."""
    # First get the peer group hash
    peer = get_peers(uei)
    if not peer or not peer.get("peerGroupHash"):
        return []
    group_hash = peer["peerGroupHash"]
    return query("""
        SELECT p.contractorUei, p.contractorName, p.cloudCompositeScore,
               p.cloudPerformanceTier, p.cloudCompositeRank, p.cloudGroupSize,
               p.cloudRevenueTtmScore, p.cloudPipelineActiveScore,
               p.cloudRevenueGrowthBlendedScore,
               i.revenueTtmMillions, i.pipelineActiveMillions,
               i.revenueGrowthYoyPercent, i.contractorCity, i.contractorState
        FROM peers p
        JOIN identity i ON p.contractorUei = i.contractorUei
        WHERE p.peerGroupHash = ?
        ORDER BY p.cloudCompositeScore DESC
    """, [group_hash])


def get_network(uei: str) -> list[dict]:
    """Supply chain relationships for a contractor."""
    return query("""
        SELECT * FROM network
        WHERE subjectContractorUei = ?
        ORDER BY activeObligationsValue DESC
    """, [uei])


def get_monthly(uei: str, months: int = 36) -> list[dict]:
    """Monthly time-series for a contractor."""
    return query("""
        SELECT * FROM monthly
        WHERE contractorUei = ?
        ORDER BY snapshotMonth DESC
        LIMIT ?
    """, [uei, months])


def get_activity(uei: str, limit: int = 200) -> list[dict]:
    """Activity events for a contractor."""
    return query("""
        SELECT * FROM activity
        WHERE contractorUei = ?
        ORDER BY flowDate DESC
        LIMIT ?
    """, [uei, limit])


def get_peer_percentiles(uei: str, months: int = 24) -> list[dict]:
    """Peer percentile time-series."""
    return query("""
        SELECT * FROM peer_percentiles
        WHERE contractorUei = ?
        ORDER BY snapshotMonth DESC
        LIMIT ?
    """, [uei, months])


## ── Dashboard rankings (in-memory from discovery JSONs) ───────────

_dashboard_index = None  # list[dict] or None

_DASHBOARD_CACHE_PATH = os.path.join(os.path.dirname(__file__), ".dashboard_index_cache.json")

# Sort key mapping: (entity_class, metric, timeframe) → short key in dashboard index
# Index keys: o=obligations, g=originations; po/so=prime/sub obligations; pg/sg=prime/sub originations
# Timeframe suffixes: 90=90d, 1y, 2y, 3y, 5y, 10=10y
_SORT_KEY_MAP = {}
for _tf_label, _tf_key in [("90d", "90"), ("1y", "1y"), ("2y", "2y"), ("3y", "3y"), ("5y", "5y"), ("10y", "10")]:
    _SORT_KEY_MAP[("combined", "obligations", _tf_label)] = f"o{_tf_key}"
    _SORT_KEY_MAP[("combined", "originations", _tf_label)] = f"g{_tf_key}"
    _SORT_KEY_MAP[("prime", "obligations", _tf_label)] = f"po{_tf_key}"
    _SORT_KEY_MAP[("prime", "originations", _tf_label)] = f"pg{_tf_key}"
    _SORT_KEY_MAP[("sub", "obligations", _tf_label)] = f"so{_tf_key}"
    _SORT_KEY_MAP[("sub", "originations", _tf_label)] = f"sg{_tf_key}"


def _get_dashboard_index() -> list[dict]:
    """Load the dashboard index (from discovery JSONs) into memory.

    Source: s3://corporeal-agg/json/index/dashboard_index.json
    Built from 22,750 pre-computed discovery JSONs (DISCOVERY_PAGE_METRICS).
    Priority: local disk cache → S3 download → empty list.
    """
    global _dashboard_index
    if _dashboard_index is not None:
        return _dashboard_index

    # Try local disk cache first
    if os.path.exists(_DASHBOARD_CACHE_PATH):
        try:
            with open(_DASHBOARD_CACHE_PATH, "r") as f:
                data = _json.load(f)
            _dashboard_index = data.get("entries", data) if isinstance(data, dict) else data
            log.info("Dashboard index loaded from disk cache: %d entries", len(_dashboard_index))
            return _dashboard_index
        except Exception as e:
            log.warning("Dashboard disk cache read failed: %s", e)

    # Fall back to S3
    s3_key = "json/index/dashboard_index.json"
    try:
        log.info("Downloading dashboard index from S3 (%s)...", s3_key)
        resp = _get_s3().get_object(Bucket=PARQUET_BUCKET, Key=s3_key)
        raw = resp["Body"].read().decode("utf-8")
        data = _json.loads(raw)
        _dashboard_index = data.get("entries", data) if isinstance(data, dict) else data
        log.info("Dashboard index loaded from S3: %d entries", len(_dashboard_index))
        # Cache to disk for next restart
        try:
            with open(_DASHBOARD_CACHE_PATH, "w") as f:
                f.write(raw)
            log.info("Dashboard index cached to disk: %s", _DASHBOARD_CACHE_PATH)
        except Exception as e:
            log.warning("Dashboard disk cache write failed: %s", e)
    except Exception as e:
        log.error("Failed to load dashboard index: %s", e)
        _dashboard_index = []

    return _dashboard_index


def preload_dashboard_index():
    """Call at startup to load the dashboard index before any requests arrive."""
    _get_dashboard_index()


def get_discovery_schema() -> list[str]:
    """Return the short keys used in the dashboard index (for debugging)."""
    idx = _get_dashboard_index()
    return list(idx[0].keys()) if idx else []


def dashboard_rankings(
    timeframe: str = "1y",
    metric: str = "obligations",
    entity_class: str = "combined",
    sector: str = None,
    limit: int = 100,
) -> dict:
    """Top N contractors from in-memory discovery index. Instant.

    Data source: 22,750 pre-computed discovery JSONs from DISCOVERY_PAGE_METRICS.
    """
    idx = _get_dashboard_index()

    # Resolve the sort key
    sort_key = _SORT_KEY_MAP.get((entity_class, metric, timeframe))
    if not sort_key:
        sort_key = "ot"
        log.warning("No sort key for %s/%s/%s — falling back to oblTtm", metric, timeframe, entity_class)

    # Human-readable sort column label
    prefix_label = {"prime": "Prime ", "sub": "Sub ", "combined": ""}
    sort_column = f"{prefix_label.get(entity_class, '')}{metric.capitalize()} {timeframe}"

    # Filter by sector (2-digit NAICS prefix)
    entries = idx
    if sector and sector != "all":
        entries = [e for e in entries if (e.get("nc") or "")[:2] == sector]

    # Sort descending by metric
    entries = sorted(entries, key=lambda e: e.get(sort_key) or 0, reverse=True)
    entries = entries[:limit]

    # Map to the response shape the frontend expects
    contractors = []
    for i, e in enumerate(entries):
        contractors.append({
            "rank": i + 1,
            "contractorUei": e["u"],
            "contractorName": e["n"],
            "primaryNaicsCode": e.get("nc", ""),
            "sectorCode": (e.get("nc") or "")[:2],
            "contractorCity": e.get("ci", ""),
            "contractorState": e.get("st", ""),
            "entityClassificationLifetime": e.get("ec", ""),
            "revenueTtmMillions": e.get("rt", 0) or 0,
            "revenueGrowthYoyPercent": e.get("gy"),
            "pipelineActiveMillions": e.get("pm", 0) or 0,
            "obligationsTtmMillions": e.get("ot", 0) or 0,
            "defenseLifetimePercent": 100.0 if e.get("di") else 0.0,
            "isPerforming": bool(e.get("rt", 0)),
            "metricValue": e.get(sort_key, 0) or 0,
        })

    return {"sort_column": sort_column, "contractors": contractors}


def compare_contractors(ueis: list[str]) -> list[dict]:
    """Pull identity + peer data for multiple contractors."""
    placeholders = ",".join(["?" for _ in ueis])
    return query(f"""
        SELECT i.*, p.cloudCompositeScore, p.cloudPerformanceTier,
               p.cloudCompositeRank, p.cloudGroupSize,
               p.cloudRevenueTtmScore, p.cloudPipelineActiveScore,
               p.cloudRevenueGrowthBlendedScore, p.peerGroupHash
        FROM identity i
        LEFT JOIN peers p ON i.contractorUei = p.contractorUei
        WHERE i.contractorUei IN ({placeholders})
    """, ueis)


def sector_summary() -> list[dict]:
    """Summary stats per NAICS sector."""
    return query("""
        SELECT sectorCode, sectorDescription,
               COUNT(*) as contractorCount,
               ROUND(SUM(revenueTtmMillions), 1) as totalRevenueTtm,
               ROUND(AVG(revenueTtmMillions), 1) as avgRevenueTtm,
               ROUND(MIN(revenueTtmMillions), 1) as minRevenueTtm,
               ROUND(MAX(revenueTtmMillions), 1) as maxRevenueTtm
        FROM identity
        GROUP BY sectorCode, sectorDescription
        ORDER BY contractorCount DESC
    """)


def naics_summary() -> list[dict]:
    """Summary stats per 6-digit NAICS code."""
    return query("""
        SELECT primaryNaicsCode, primaryNaicsDescription,
               COUNT(*) as contractorCount,
               ROUND(SUM(revenueTtmMillions), 1) as totalRevenueTtm,
               ROUND(AVG(revenueTtmMillions), 1) as avgRevenueTtm
        FROM identity
        GROUP BY primaryNaicsCode, primaryNaicsDescription
        ORDER BY contractorCount DESC
        LIMIT 300
    """)


def top_contractors(
    naics: str = None,
    state: str = None,
    defense_only: bool = False,
    min_revenue: float = 0,
    limit: int = 20,
) -> list[dict]:
    """Flexible top-N query with filters."""
    conditions = []
    params = []

    if naics:
        if len(naics) == 2:
            conditions.append("sectorCode = ?")
        else:
            conditions.append("primaryNaicsCode = ?")
        params.append(naics)

    if state:
        conditions.append("contractorState = ?")
        params.append(state.upper())

    if defense_only:
        conditions.append("defenseLifetimePercent > 50")

    if min_revenue > 0:
        conditions.append("revenueTtmMillions >= ?")
        params.append(min_revenue)

    where = "WHERE " + " AND ".join(conditions) if conditions else ""
    params.append(limit)

    return query(f"""
        SELECT contractorUei, contractorName, primaryNaicsCode,
               primaryNaicsDescription, contractorCity, contractorState,
               revenueTtmMillions, pipelineActiveMillions,
               revenueGrowthYoyPercent, revenueGrowthBlendedPercent,
               entityClassificationLifetime, defenseLifetimePercent,
               isPerforming, topClientName
        FROM identity
        {where}
        ORDER BY revenueTtmMillions DESC
        LIMIT ?
    """, params)


def concentration_risk(uei: str) -> dict:
    """Analyze supply chain concentration risk for a contractor."""
    network = get_network(uei)
    identity = get_identity(uei)

    if not network or not identity:
        return {"error": "Contractor not found"}

    # Aggregate by entity name
    inflows = {}
    total_obligations = 0
    for r in network:
        if r.get("flowDirection") == "INFLOW":
            name = r.get("relationshipEntityName", "UNKNOWN")
            val = r.get("activeObligationsValue", 0) or 0
            inflows[name] = inflows.get(name, 0) + val
            total_obligations += val

    # Compute concentration
    sorted_inflows = sorted(inflows.items(), key=lambda x: x[1], reverse=True)
    top_customer_pct = (sorted_inflows[0][1] / total_obligations * 100) if total_obligations > 0 and sorted_inflows else 0

    return {
        "contractor": identity.get("contractorName"),
        "uei": uei,
        "totalActiveObligations": total_obligations,
        "customerCount": len(inflows),
        "topCustomer": sorted_inflows[0][0] if sorted_inflows else None,
        "topCustomerObligations": sorted_inflows[0][1] if sorted_inflows else 0,
        "topCustomerPercent": round(top_customer_pct, 1),
        "concentrationRisk": "EXTREME" if top_customer_pct > 80 else "HIGH" if top_customer_pct > 60 else "MODERATE" if top_customer_pct > 40 else "LOW",
        "allCustomers": [{"name": n, "obligations": v, "percent": round(v/total_obligations*100, 1) if total_obligations > 0 else 0} for n, v in sorted_inflows],
    }
