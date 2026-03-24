"""
Lambda Function: opal-partners-data

Purpose: Serve Advisor Intelligence gold layer data for multi-tenant portal
Author: Dashboard Engineer
Version: 2.8 - Added firm+advisor composition S3-proxy routes, cors_response_nocache, serve_s3_json_nocache (ADVI_BKSCMP WS2)

API Endpoints (v2):
  GET /api/partners                                              - List partners user can access
  GET /api/shared/advisor-intelligence/timeseries/{dimension}    - Time series by dimension
  GET /api/shared/advisor-intelligence/snapshots/{dimension}     - Current AUA breakdown
  GET /api/shared/advisor-intelligence/filters                   - Available filter options
  GET /api/shared/advisor-intelligence/clients/growth            - Client growth time series
  GET /api/shared/advisor-intelligence/clients/tax-breakdown     - Tax basis pie charts
  GET /api/shared/advisor-intelligence/clients/tax-deferred      - Strategy candidates
  GET /api/shared/advisor-intelligence/summary                   - Header summary metrics
  GET /api/shared/advisor-intelligence/partner-analytics         - Partner analytics header (detailed)
  GET /api/health/advisor-intelligence                           - Health check endpoint

API Endpoints (v3 - Books Tab):
  GET /api/scoped/partners/books/relationship/{id}/timeseries                - Daily AUA/NNA for relationship
  GET /api/scoped/partners/books/account/{id}/timeseries                     - Daily AUA/NNA for account
  GET /api/scoped/partners/books/relationship/{id}/composition               - Mix + Concentration snapshot
  GET /api/scoped/partners/books/account/{id}/composition                    - Mix + Concentration snapshot
  GET /api/scoped/partners/books/relationship/{id}/mix-timeseries            - Historical mix pct timeseries
  GET /api/scoped/partners/books/relationship/{id}/concentration-timeseries  - Historical top-10 concentration
  GET /api/scoped/partners/books/firm/all/mix-views                          - Firm-level period mix views (quarterly/monthly/annually)
  GET /api/shared/advisor-intelligence/advisors/{id}/mix-views               - Per-advisor period mix views
  GET /api/scoped/partners/books/advisor/{id}/timeseries                     - Daily AUA/NNA for advisor book
  GET /api/scoped/partners/books/advisor/{id}/mix-timeseries                 - AUA-weighted mix pct timeseries for advisor book
  GET /api/scoped/partners/books/firm/all/composition?firmId=xxx             - Firm-level per-class composition + top holdings (no-store)
  GET /api/scoped/partners/books/advisor/{id}/composition?firmId=xxx         - Advisor-level per-class composition + top holdings (no-store)

Access Control:
  - firmId is passed as query parameter
  - Validates firmId against allowedFirmIds from authorizer context
  - Internal users (allowedFirmIds = "ALL") can access any partner

Gold Layer Structure:
  s3://{bucket}/gold/timeseries/nna_by_{dimension}.json
  s3://{bucket}/gold/snapshots/aua_by_{dimension}.json
  s3://{bucket}/gold/clients/*.json
  s3://{bucket}/gold/filters/dimensions.json

Changelog v2.3:
  - Added data validation (no 200 with empty data)
  - Added S3 timeouts (5s connect, 10s read)
  - Added retry hints in error responses
  - Return 503 (not 200) for empty/invalid data
  - Added health check endpoint
"""

import json
import io
import os
import boto3
from botocore.config import Config
from decimal import Decimal
from typing import Optional
from datetime import datetime, timedelta

import awswrangler as wr
from etf_classifier import ETFClassifier as _ETFClassifier
_clf = _ETFClassifier.instance()

# Initialize AWS clients
s3_client = boto3.client('s3', region_name='us-east-1')
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

# DynamoDB table for firm metadata
USERS_TABLE = os.environ.get('USERS_TABLE', 'opal-users-v2')
users_table = dynamodb.Table(USERS_TABLE)

# Valid dimensions for timeseries endpoints (11 total)
TIMESERIES_DIMENSIONS = [
    'total',           # nna_total.json (no dimension breakdown)
    'category',        # nna_by_category.json (NMNC/NMEC)
    'architect',       # nna_by_architect.json
    'region',          # nna_by_region.json
    'account_type',    # nna_by_account_type.json
    'tax_status',      # nna_by_tax_status.json
    'client_segment',  # nna_by_client_segment.json
    'state',           # nna_by_state.json
    'city',            # nna_by_city.json
    'relationship',    # nna_by_relationship.json
    'implementor'      # nna_by_implementor.json
]

# Valid dimensions for snapshot endpoints (7 total)
SNAPSHOT_DIMENSIONS = [
    'architect',       # aua_by_architect.json
    'region',          # aua_by_region.json
    'tax_status',      # aua_by_tax_status.json
    'account_type',    # aua_by_account_type.json
    'implementor',     # aua_by_implementor.json
    'state',           # aua_by_state.json
    'city'             # aua_by_city.json
]


class DecimalEncoder(json.JSONEncoder):
    """Convert Decimal to float for JSON serialization"""
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)


def cors_response(status_code: int, body: dict) -> dict:
    """Create HTTP response with CORS headers"""
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET,OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type,Authorization',
            'Cache-Control': 'max-age=300'  # 5-minute cache for gold layer
        },
        'body': json.dumps(body, cls=DecimalEncoder)
    }


def cors_response_nocache(status_code: int, body: dict) -> dict:
    """Create HTTP response with no-store Cache-Control for confidential composition data.

    Used by firm/advisor composition routes -- position-level AUM data must not
    be cached anywhere in the request path (CDN, browser, or intermediary proxies).
    """
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET,OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type,Authorization',
            'Cache-Control': 'no-store, no-cache, must-revalidate',
        },
        'body': json.dumps(body, cls=DecimalEncoder)
    }


def is_authorized(firm_id: str, allowed_firms: str) -> bool:
    """Check if user is authorized to access firm data.

    Args:
        firm_id: The firm ID being requested
        allowed_firms: Comma-separated firm IDs or "ALL"

    Returns:
        True if authorized, False otherwise
    """
    if not firm_id:
        return False
    if allowed_firms == 'ALL':
        return True
    return firm_id in allowed_firms.split(',')


def get_firm_bucket(firm_id: str) -> Optional[str]:
    """Look up S3 bucket for firm from DynamoDB.

    Args:
        firm_id: The firm ID to look up

    Returns:
        S3 bucket name or None if not found
    """
    try:
        response = users_table.get_item(
            Key={
                'PK': f'FIRM#{firm_id}',
                'SK': 'META'
            }
        )
        item = response.get('Item')
        if item:
            return item.get('s3Bucket')
    except Exception as e:
        print(f'Error looking up firm bucket for {firm_id}: {e}')
    return None


def get_firm_metadata(firm_id: str) -> Optional[dict]:
    """Get firm metadata from DynamoDB."""
    try:
        response = users_table.get_item(
            Key={'PK': f'FIRM#{firm_id}', 'SK': 'META'}
        )
        return response.get('Item')
    except Exception as e:
        print(f'Error getting firm metadata for {firm_id}: {e}')
        return None


def get_all_firms() -> list:
    """Get all firm metadata records from DynamoDB."""
    try:
        response = users_table.scan(
            FilterExpression='SK = :meta AND attribute_exists(s3Bucket)',
            ExpressionAttributeValues={':meta': 'META'},
            ProjectionExpression='firmId, #n, tier, s3Bucket, parentFirmId',
            ExpressionAttributeNames={'#n': 'name'}
        )
        return response.get('Items', [])
    except Exception as e:
        print(f'Error scanning firms: {e}')
        return []


def validate_data_content(data: any, key: str) -> tuple[bool, str]:
    """Validate that data payload is not empty.

    Args:
        data: The data payload to validate
        key: S3 key for error messaging

    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check for null/None
    if data is None:
        return False, f'Data is null: {key}'

    # Check for empty dict
    if isinstance(data, dict) and len(data) == 0:
        return False, f'Data is empty dict: {key}'

    # Check for empty list
    if isinstance(data, list) and len(data) == 0:
        return False, f'Data is empty list: {key}'

    # For dict responses, check if required fields have content
    if isinstance(data, dict):
        # Special validation for partner list
        if 'partners' in data and isinstance(data['partners'], list) and len(data['partners']) == 0:
            # Empty partner list is suspicious but might be valid (no partners assigned)
            # Log it but allow
            print(f'Warning: Empty partners list in {key}')

        # Check for common data fields that shouldn't be empty
        for field in ['timeseries', 'snapshots', 'metrics', 'data']:
            if field in data:
                if isinstance(data[field], (dict, list)) and len(data[field]) == 0:
                    return False, f'Data field "{field}" is empty: {key}'

    return True, ''


def serve_s3_json(bucket: str, key: str) -> dict:
    """Read JSON from S3 and return with CORS headers.

    CRITICAL: This function now validates data content and returns 503 (not 200)
    if data is empty/null/missing. This enables frontend retry logic.

    Args:
        bucket: S3 bucket name
        key: S3 object key

    Returns:
        HTTP response dict
    """
    try:
        # Add timeout to S3 request (10 seconds)
        config = boto3.session.Config(
            connect_timeout=5,
            read_timeout=10,
            retries={'max_attempts': 2}
        )
        s3_with_timeout = boto3.client('s3', region_name='us-east-1', config=config)

        # Fetch from S3
        response = s3_with_timeout.get_object(Bucket=bucket, Key=key)

        # Check if file is empty (0 bytes)
        content_length = response.get('ContentLength', 0)
        if content_length == 0:
            print(f'ERROR: S3 file is 0 bytes: {bucket}/{key}')
            return cors_response(503, {
                'error': 'Data unavailable',
                'message': 'Data file exists but is empty',
                'retry': True,
                'key': key
            })

        # Parse JSON
        body_content = response['Body'].read().decode('utf-8')
        if not body_content or body_content.strip() == '':
            print(f'ERROR: S3 file has no content: {bucket}/{key}')
            return cors_response(503, {
                'error': 'Data unavailable',
                'message': 'Data file is empty',
                'retry': True,
                'key': key
            })

        data = json.loads(body_content)

        # CRITICAL: Validate data content
        is_valid, error_msg = validate_data_content(data, key)
        if not is_valid:
            print(f'ERROR: Data validation failed: {error_msg}')
            return cors_response(503, {
                'error': 'Data unavailable',
                'message': 'Data exists but is empty or invalid',
                'retry': True,
                'key': key,
                'validation_error': error_msg
            })

        # Data is valid - return 200
        print(f'SUCCESS: Served {bucket}/{key} ({content_length} bytes)')
        return cors_response(200, data)

    except s3_client.exceptions.NoSuchKey:
        print(f'ERROR: S3 file not found: {bucket}/{key}')
        return cors_response(404, {
            'error': 'Data not found',
            'message': f'File does not exist: {key}',
            'retry': False
        })
    except json.JSONDecodeError as e:
        print(f'ERROR: Invalid JSON in {bucket}/{key}: {e}')
        return cors_response(503, {
            'error': 'Data unavailable',
            'message': 'Data file is corrupted (invalid JSON)',
            'retry': True,
            'key': key
        })
    except Exception as e:
        print(f'ERROR: Failed to read {bucket}/{key}: {type(e).__name__}: {e}')
        return cors_response(500, {
            'error': 'Internal server error',
            'message': str(e),
            'retry': True,
            'key': key
        })


def serve_s3_json_nocache(bucket: str, key: str) -> dict:
    """Read JSON from S3 and return with no-store Cache-Control headers.

    Structural copy of serve_s3_json -- only difference is all cors_response
    calls are replaced with cors_response_nocache. Used for firm/advisor
    composition routes where position-level data must not be cached.

    Args:
        bucket: S3 bucket name
        key: S3 object key

    Returns:
        HTTP response dict
    """
    try:
        config = boto3.session.Config(
            connect_timeout=5,
            read_timeout=10,
            retries={'max_attempts': 2}
        )
        s3_with_timeout = boto3.client('s3', region_name='us-east-1', config=config)

        response = s3_with_timeout.get_object(Bucket=bucket, Key=key)

        content_length = response.get('ContentLength', 0)
        if content_length == 0:
            print(f'ERROR: S3 file is 0 bytes: {bucket}/{key}')
            return cors_response_nocache(503, {
                'error': 'Data unavailable',
                'message': 'Data file exists but is empty',
                'retry': True,
                'key': key
            })

        body_content = response['Body'].read().decode('utf-8')
        if not body_content or body_content.strip() == '':
            print(f'ERROR: S3 file has no content: {bucket}/{key}')
            return cors_response_nocache(503, {
                'error': 'Data unavailable',
                'message': 'Data file is empty',
                'retry': True,
                'key': key
            })

        data = json.loads(body_content)

        is_valid, error_msg = validate_data_content(data, key)
        if not is_valid:
            print(f'ERROR: Data validation failed: {error_msg}')
            return cors_response_nocache(503, {
                'error': 'Data unavailable',
                'message': 'Data exists but is empty or invalid',
                'retry': True,
                'key': key,
                'validation_error': error_msg
            })

        print(f'SUCCESS: Served {bucket}/{key} ({content_length} bytes)')
        return cors_response_nocache(200, data)

    except s3_client.exceptions.NoSuchKey:
        print(f'ERROR: S3 file not found: {bucket}/{key}')
        return cors_response_nocache(404, {
            'error': 'Data not found',
            'message': f'File does not exist: {key}',
            'retry': False
        })
    except json.JSONDecodeError as e:
        print(f'ERROR: Invalid JSON in {bucket}/{key}: {e}')
        return cors_response_nocache(503, {
            'error': 'Data unavailable',
            'message': 'Data file is corrupted (invalid JSON)',
            'retry': True,
            'key': key
        })
    except Exception as e:
        print(f'ERROR: Failed to read {bucket}/{key}: {type(e).__name__}: {e}')
        return cors_response_nocache(500, {
            'error': 'Internal server error',
            'message': str(e),
            'retry': True,
            'key': key
        })


def extract_path_param(path: str, segment: str) -> str:
    """Extract parameter after a path segment.

    Args:
        path: Full request path
        segment: Segment to find (e.g., 'timeseries', 'snapshots')

    Returns:
        The parameter after the segment, or empty string
    """
    parts = path.rstrip('/').split('/')
    for i, part in enumerate(parts):
        if part == segment and i + 1 < len(parts):
            return parts[i + 1]
    return ''


# =============================================================================
# V1 Handlers (Backward Compatibility)
# =============================================================================

def handle_get_partners(allowed_firms: str) -> dict:
    """Return list of partners user can access.

    Response matches TypeScript Partner interface:
    {
        firmId: string
        firmName: string
        tier: 'advisor' | 'subadvisor' | 'branch'
        parentFirmId: string | null
    }
    """
    all_firms = get_all_firms()

    # Filter to non-internal firms (partner firms only)
    partner_firms = [f for f in all_firms if f.get('tier') != 'internal']

    # Format response to match TypeScript interface
    partners = []
    for firm in partner_firms:
        firm_id = firm.get('firmId', '')

        # Check authorization
        if allowed_firms != 'ALL' and firm_id not in allowed_firms.split(','):
            continue

        partners.append({
            'firmId': firm_id,
            'firmName': firm.get('name', firm_id),
            'tier': firm.get('tier', 'advisor'),
            'parentFirmId': firm.get('parentFirmId') or None
        })

    return cors_response(200, {'partners': partners})


# =============================================================================
# V2 Handlers (New Endpoints)
# =============================================================================

def handle_timeseries(bucket: str, dimension: str) -> dict:
    """Serve time series data for a dimension.

    Args:
        bucket: S3 bucket name
        dimension: One of TIMESERIES_DIMENSIONS

    Returns:
        Time series JSON from gold layer
    """
    if dimension not in TIMESERIES_DIMENSIONS:
        return cors_response(400, {
            'error': f'Invalid dimension: {dimension}',
            'valid_dimensions': TIMESERIES_DIMENSIONS
        })

    if dimension == 'total':
        key = 'gold/timeseries/nna_total.json'
    else:
        key = f'gold/timeseries/nna_by_{dimension}.json'

    return serve_s3_json(bucket, key)


def handle_snapshots(bucket: str, dimension: str) -> dict:
    """Serve AUA snapshot for a dimension.

    Args:
        bucket: S3 bucket name
        dimension: One of SNAPSHOT_DIMENSIONS

    Returns:
        Snapshot JSON from gold layer
    """
    if dimension not in SNAPSHOT_DIMENSIONS:
        return cors_response(400, {
            'error': f'Invalid dimension: {dimension}',
            'valid_dimensions': SNAPSHOT_DIMENSIONS
        })

    key = f'gold/snapshots/aua_by_{dimension}.json'
    return serve_s3_json(bucket, key)


def handle_filters(bucket: str) -> dict:
    """Serve available filter dimensions.

    Args:
        bucket: S3 bucket name

    Returns:
        Filter dimensions JSON from gold layer
    """
    return serve_s3_json(bucket, 'gold/filters/dimensions.json')


def handle_client_growth(bucket: str) -> dict:
    """Serve client growth time series.

    Args:
        bucket: S3 bucket name

    Returns:
        Client growth JSON from gold layer
    """
    return serve_s3_json(bucket, 'gold/clients/growth_timeseries.json')


def handle_tax_breakdown(bucket: str) -> dict:
    """Serve tax basis pie chart data.

    Args:
        bucket: S3 bucket name

    Returns:
        Tax breakdown JSON from gold layer
    """
    return serve_s3_json(bucket, 'gold/clients/tax_basis_breakdown.json')


def handle_tax_deferred(bucket: str) -> dict:
    """Serve tax-deferred strategy candidates.

    Args:
        bucket: S3 bucket name

    Returns:
        Tax-deferred candidates JSON from gold layer
    """
    return serve_s3_json(bucket, 'gold/clients/tax_deferred_candidates.json')


def handle_summary(bucket: str) -> dict:
    """Serve header summary metrics (Model Portfolios-style header).

    Args:
        bucket: S3 bucket name

    Returns:
        Header summary JSON from gold layer
    """
    return serve_s3_json(bucket, 'gold/summary/header_metrics.json')


def handle_partner_analytics(bucket: str) -> dict:
    """Serve partner analytics header metrics (detailed NNA/AUA breakdown).

    Args:
        bucket: S3 bucket name

    Returns:
        Partner analytics JSON from gold layer
    """
    return serve_s3_json(bucket, 'gold/partner_analytics/header_metrics.json')


def handle_advisor_book(bucket: str, advisor_id: str) -> dict:
    """Serve per-advisor book view data.

    Args:
        bucket: S3 bucket name (from firm lookup)
        advisor_id: Advisor identifier (e.g., 'travis_penfield', '49f_house')

    Returns:
        Advisor book JSON from gold layer
    """
    # Validate advisor_id (basic sanitization - alphanumeric + underscore only)
    if not advisor_id or not all(c.isalnum() or c == '_' for c in advisor_id):
        return cors_response(400, {'error': f'Invalid advisor_id: {advisor_id}'})

    key = f'gold/advisors/{advisor_id}/book.json'
    return serve_s3_json(bucket, key)


def handle_health_check() -> dict:
    """Health check endpoint for data availability.

    Tests connectivity to key data sources:
    - DynamoDB (firm metadata)
    - S3 (gold layer data for each firm)

    Returns:
        Health status with details for each data source
    """
    health_status = {
        'service': 'advisor-intelligence',
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'status': 'healthy',
        'checks': {}
    }

    # Check 1: DynamoDB connectivity
    try:
        all_firms = get_all_firms()
        health_status['checks']['dynamodb'] = {
            'status': 'ok',
            'firms_found': len(all_firms)
        }
    except Exception as e:
        health_status['status'] = 'degraded'
        health_status['checks']['dynamodb'] = {
            'status': 'error',
            'error': str(e)
        }

    # Check 2: S3 data availability for each firm
    s3_checks = {}
    try:
        firms = get_all_firms()
        for firm in firms:
            firm_id = firm.get('firmId', 'unknown')
            bucket = firm.get('s3Bucket')

            if not bucket:
                s3_checks[firm_id] = {'status': 'error', 'error': 'No bucket configured'}
                continue

            # Test if summary metrics file exists (critical file)
            try:
                s3_client.head_object(Bucket=bucket, Key='gold/summary/header_metrics.json')
                s3_checks[firm_id] = {'status': 'ok', 'bucket': bucket}
            except s3_client.exceptions.NoSuchKey:
                s3_checks[firm_id] = {'status': 'missing_data', 'bucket': bucket}
                health_status['status'] = 'degraded'
            except Exception as e:
                s3_checks[firm_id] = {'status': 'error', 'error': str(e), 'bucket': bucket}
                health_status['status'] = 'degraded'

        health_status['checks']['s3_data'] = s3_checks

    except Exception as e:
        health_status['status'] = 'unhealthy'
        health_status['checks']['s3_data'] = {
            'status': 'error',
            'error': str(e)
        }

    # Return appropriate status code
    status_code = 200 if health_status['status'] == 'healthy' else 503

    return cors_response(status_code, health_status)


# =============================================================================
# Books Tab Handlers (L3/L4 drill views)
# =============================================================================

# Canonical asset class hierarchy for Mix response
# Top-level: equity | fixed_income | alternatives | cash | hedge | other
# structured_notes sits under alternatives (Halo Shield products, buffer ETFs,
# indexed annuities — equity-linked with defined-outcome / protection structures)
_ASSET_CLASS_LABELS = {
    'equity':           'Equities',
    'fixed_income':     'Fixed Income',
    'structured_notes': 'Structured Notes',  # sub-class of alternatives
    'alternatives':     'Alternatives',
    'cash':             'Cash',
    'other':            'Other',
}


def _classify_holding(ticker, asset_name):
    """Classify a holding via ETFClassifier (bd-securities DynamoDB table).

    Returns: 'equity' | 'fixed_income' | 'alternatives' | 'other'
    'other' is the cash residual bucket in the portal mix view.

    Classification is delegated entirely to _clf (ETFClassifier), which:
    1. Looks up ticker in bd-securities DynamoDB table
    2. Resolves asset_name via name_aliases to a ticker, then looks up
    3. Applies name pattern matching (structured notes, cash, fixed income)
    4. Falls back to alpha-ticker heuristic (equity)
    5. Returns '' for unknowns -- mapped here to 'other' (cash residual)
    """
    # Coerce pd.NA / None / NaN to None for safe boolean checks
    try:
        if not ticker or ticker != ticker:
            ticker = None
    except (ValueError, TypeError):
        ticker = None
    try:
        if not asset_name or asset_name != asset_name:
            asset_name = None
    except (ValueError, TypeError):
        asset_name = None

    result = _clf.classify(ticker, asset_name)
    return result if result else 'other'



def _validate_entity_id(entity_id):
    """Validate relationship_id or account_id (alphanumeric + hyphen + underscore)."""
    if not entity_id:
        return False
    return all(c.isalnum() or c in ('_', '-', '.') for c in entity_id)


def _find_latest_holdings_lots(bucket):
    """Find the latest non-backfill holdings_lots snapshot key."""
    prefix = 'gold/holdings_lots/'
    try:
        resp = s3_client.list_objects_v2(Bucket=bucket, Prefix=prefix)
        keys = [
            obj['Key'] for obj in resp.get('Contents', [])
            if obj['Key'].endswith('.parquet')
            and 'backfill_' not in obj['Key'].rsplit('/', 1)[-1]
        ]
        return sorted(keys)[-1] if keys else None
    except Exception:
        return None


def _get_active_account_ids(bucket, as_of_date, max_age_days=45):
    """Return set of account_ids active in account_performance within max_age_days.

    account_performance is the authoritative activity ledger. holdings_lots.is_open
    can lag for departed accounts — this gate ensures composition only includes
    accounts confirmed live by the downstream canonical source.

    Args:
        bucket: S3 bucket
        as_of_date: YYYY-MM-DD string (holdings snapshot date)
        max_age_days: accounts last seen within this window are considered active

    Returns:
        set of active account_id strings, or None if AP is unavailable (degrade
        gracefully — caller skips the gate rather than failing the request).
    """
    import pandas as pd
    try:
        df = wr.s3.read_parquet(
            path=f's3://{bucket}/gold/account_performance.parquet',
            columns=['date', 'account_id'],
        )
        df['date'] = pd.to_datetime(df['date'])
        cutoff = pd.Timestamp(as_of_date) - pd.Timedelta(days=max_age_days)
        active_ids = set(df.loc[df['date'] >= cutoff, 'account_id'].unique())
        print(f'AP active gate: {len(active_ids):,} accounts active within {max_age_days}d of {as_of_date}')
        return active_ids
    except Exception as e:
        print(f'WARN: Could not load account_performance for active gate: {e} -- skipping gate')
        return None


def handle_books_timeseries(bucket, entity_type, entity_id):
    """Daily AUA/NNA timeseries for a single relationship or account.

    Args:
        bucket: S3 bucket
        entity_type: 'relationship' or 'account'
        entity_id: The entity identifier
    """
    if not _validate_entity_id(entity_id):
        return cors_response(400, {'error': f'Invalid {entity_type}_id: {entity_id}'})

    if entity_type == 'relationship':
        key = 'gold/client_performance.parquet'
        filter_col = 'relationship_id'
        columns = ['date', 'relationship_id', 'total_aua', 'aua_taxable',
                    'aua_tax_deferred', 'aua_tax_exempt', 'cum_inflows',
                    'cum_outflows', 'nna']
    else:
        key = 'gold/account_performance.parquet'
        filter_col = 'account_id'
        columns = ['date', 'account_id', 'total_aua', 'cum_inflows',
                    'cum_outflows', 'nna', 'num_positions', 'pct_priced']

    try:
        df = wr.s3.read_parquet(
            path=f's3://{bucket}/{key}',
            columns=columns,
        )
        df = df[df[filter_col] == entity_id]
    except Exception as e:
        print(f'ERROR: Failed to read {key}: {e}')
        return cors_response(500, {'error': f'Failed to read data: {type(e).__name__}'})

    if df.empty:
        return cors_response(404, {'error': f'No data for {entity_type}_id: {entity_id}'})

    df = df.sort_values('date')
    data_as_of = str(df['date'].max().date()) if hasattr(df['date'].iloc[0], 'date') else str(df['date'].max())

    records = []
    for _, row in df.iterrows():
        rec = {
            'date': str(row['date'].date()) if hasattr(row['date'], 'date') else str(row['date']),
            'total_aua': round(float(row['total_aua']), 2),
            'cum_inflows': round(float(row['cum_inflows']), 2),
            'cum_outflows': round(float(row['cum_outflows']), 2),
            'nna': round(float(row['nna']), 2),
        }
        # Include optional columns if present
        for opt_col in ['aua_taxable', 'aua_tax_deferred', 'aua_tax_exempt',
                        'num_positions', 'pct_priced']:
            if opt_col in df.columns:
                val = row[opt_col]
                rec[opt_col] = round(float(val), 2) if val == val else None  # NaN check
        records.append(rec)

    response_body = {
        'generated_at': datetime.utcnow().isoformat() + 'Z',
        'data_as_of': data_as_of,
        f'{entity_type}_id': entity_id,
        'data': records
    }
    print(f'SUCCESS: books/{entity_type}/{entity_id}/timeseries -> {len(records)} records')
    return cors_response(200, response_body)


def handle_books_composition(bucket, entity_type, entity_id):
    """Mix (asset class) + Concentration (security) for a single entity.

    Args:
        bucket: S3 bucket
        entity_type: 'relationship', 'account', or 'firm'
        entity_id: The entity identifier ('all' for firm scope)
    """
    # Firm scope uses entity_id='all' which is not a real ID -- skip validation
    if entity_type != 'firm' and not _validate_entity_id(entity_id):
        return cors_response(400, {'error': f'Invalid {entity_type}_id: {entity_id}'})

    # Find latest holdings_lots snapshot
    holdings_key = _find_latest_holdings_lots(bucket)
    if not holdings_key:
        return cors_response(404, {'error': 'No holdings_lots snapshots available'})

    read_cols = ['account_id', 'relationship_id', 'ticker', 'asset_name',
                 'market_value', 'is_open']

    try:
        df = wr.s3.read_parquet(
            path=f's3://{bucket}/{holdings_key}',
            columns=read_cols,
            dtype_backend='numpy',
        )
        if entity_type == 'firm':
            # Firm scope: aggregate ALL open holdings -- the bucket IS the firm
            df = df[df['is_open'].fillna(False) == True]
        else:
            filter_col = 'relationship_id' if entity_type == 'relationship' else 'account_id'
            df = df[(df[filter_col] == entity_id) & (df['is_open'].fillna(False) == True)]
    except Exception as e:
        print(f'ERROR: Failed to read {holdings_key}: {e}')
        return cors_response(500, {'error': f'Failed to read holdings: {type(e).__name__}'})

    if df.empty:
        return cors_response(404, {'error': f'No open holdings for {entity_type}: {entity_id}'})

    # Gate: filter to accounts confirmed active in account_performance.
    # holdings_lots.is_open can lag for departed accounts; AP is the authoritative
    # activity ledger and prevents stale positions from inflating composition totals.
    snapshot_date = holdings_key.rsplit('/', 1)[-1].replace('.parquet', '')
    active_ids = _get_active_account_ids(bucket, snapshot_date)
    if active_ids is not None:
        before = len(df)
        df = df[df['account_id'].isin(active_ids)]
        excluded = before - len(df)
        if excluded > 0:
            print(f'AP gate excluded {excluded:,} lots from {before:,} '
                  f'({excluded/before*100:.1f}% of entity holdings from inactive accounts)')

    if df.empty:
        return cors_response(404, {'error': f'No active holdings for {entity_type}_id: {entity_id}'})

    # Classify each holding
    df['asset_class'] = df.apply(
        lambda r: _classify_holding(r.get('ticker'), r.get('asset_name')), axis=1
    )

    total_mv = float(df['market_value'].sum())
    if total_mv == 0:
        return cors_response(200, {
            'generated_at': datetime.utcnow().isoformat() + 'Z',
            'data_as_of': holdings_key.rsplit('/', 1)[-1].replace('.parquet', ''),
            'scope': {f'{entity_type}_id': entity_id},
            'mix': [],
            'concentration': {'top_n': 10, 'items': [], 'other': {'market_value': 0, 'pct': 0}},
            'unclassified': {'count': 0, 'market_value': 0}
        })

    # --- Mix: group by asset_class ---
    mix_agg = df.groupby('asset_class')['market_value'].sum().sort_values(ascending=False)
    # pct is 0-1 (e.g., 0.625 = 62.5%). Consumers multiply by 100 to display.
    mix_items = []
    for ac, mv in mix_agg.items():
        mix_items.append({
            'asset_class': ac,
            'label': _ASSET_CLASS_LABELS.get(ac, ac.replace('_', ' ').title()),
            'market_value': round(float(mv), 2),
            'pct': round(float(mv) / total_mv, 6)
        })

    # --- Concentration: group by ticker (or asset_name fallback) ---
    def _conc_key(r):
        t = r.get('ticker')
        try:
            if t and t == t and str(t).strip() not in ('', 'nan', 'None'):
                return str(t).strip().upper()
        except (ValueError, TypeError):
            pass
        return str(r.get('asset_name', '')).strip()[:50]
    df['conc_key'] = df.apply(_conc_key, axis=1)
    conc_agg = df.groupby('conc_key').agg(
        market_value=('market_value', 'sum'),
        asset_class=('asset_class', 'first'),
        label=('conc_key', 'first')
    ).sort_values('market_value', ascending=False)

    top_n = 10
    top_items = []
    for key_val, row in conc_agg.head(top_n).iterrows():
        top_items.append({
            'key': key_val,
            'label': key_val,
            'asset_class': row['asset_class'],
            'market_value': round(float(row['market_value']), 2),
            'pct': round(float(row['market_value']) / total_mv, 6)
        })

    other_mv = float(conc_agg.iloc[top_n:]['market_value'].sum()) if len(conc_agg) > top_n else 0.0

    # Unclassified count
    unclassified_mask = df['asset_class'] == 'other'
    unclassified_count = int(unclassified_mask.sum())
    unclassified_mv = float(df.loc[unclassified_mask, 'market_value'].sum())

    snapshot_date = holdings_key.rsplit('/', 1)[-1].replace('.parquet', '')
    response_body = {
        'generated_at': datetime.utcnow().isoformat() + 'Z',
        'data_as_of': snapshot_date,
        'scope': {f'{entity_type}_id': entity_id},
        'mix': mix_items,
        'concentration': {
            'top_n': top_n,
            'items': top_items,
            'other': {
                'market_value': round(other_mv, 2),
                'pct': round(other_mv / total_mv, 6) if total_mv > 0 else 0
            }
        },
        'unclassified': {
            'count': unclassified_count,
            'market_value': round(unclassified_mv, 2)
        }
    }
    print(f'SUCCESS: books/{entity_type}/{entity_id}/composition -> '
          f'{len(mix_items)} classes, {len(top_items)} top holdings')
    return cors_response(200, response_body)


# =============================================================================
# Mix + Concentration Timeseries Handlers (pre-computed per-relationship JSON)
# Pattern: identical to handle_advisor_book -- serve_s3_json passthrough.
# Gold script 06b writes: gold/client_timeseries/{relationship_id}.json
# Both endpoints serve the same file; portal destructures what it needs.
# =============================================================================

def handle_mix_timeseries(bucket, relationship_id):
    """Serve pre-computed mix + concentration timeseries for a relationship."""
    if not _validate_entity_id(relationship_id):
        return cors_response(400, {'error': f'Invalid relationship_id: {relationship_id}'})
    return serve_s3_json(bucket, f'gold/client_timeseries/{relationship_id}.json')


def handle_concentration_timeseries(bucket, relationship_id):
    """Serve pre-computed mix + concentration timeseries for a relationship."""
    if not _validate_entity_id(relationship_id):
        return cors_response(400, {'error': f'Invalid relationship_id: {relationship_id}'})
    return serve_s3_json(bucket, f'gold/client_timeseries/{relationship_id}.json')


def _filter_window(data_list: list, window: str) -> list:
    """Filter a data list (items with 'date' keys) to trailing window from today.

    window values: '3M' (90d), '6M' (180d), '1Y' (365d), '2Y' (730d), '3Y' (1095d).
    Unrecognised window values return the full list unchanged.
    """
    window_days = {'3M': 90, '6M': 180, '1Y': 365, '2Y': 730, '3Y': 1095}
    days = window_days.get((window or '').upper())
    if not days:
        return data_list
    cutoff = (datetime.utcnow() - timedelta(days=days)).strftime('%Y-%m-%d')
    return [row for row in data_list if row.get('date', '') >= cutoff]


def handle_advisor_timeseries(bucket: str, advisor_id: str) -> dict:
    """Serve pre-computed AUA timeseries for one advisor book.

    Written by bd-portal-advisor-publisher at gold/advisors/{advisor_id}/timeseries.json.
    Shape: {advisor_id, advisor_name, data_as_of, data: [{date, total_aua,
            cum_inflows, cum_outflows, nna}]}
    """
    if not advisor_id or '/' in advisor_id or '..' in advisor_id:
        return cors_response(400, {'error': f'Invalid advisor_id: {advisor_id}'})
    key = f'gold/advisors/{advisor_id}/timeseries.json'
    return serve_s3_json(bucket, key)


def handle_advisor_mix_timeseries(bucket: str, advisor_id: str,
                                   window: str | None) -> dict:
    """Serve pre-computed AUA-weighted mix timeseries for one advisor book.

    Written by bd-portal-advisor-publisher at gold/advisors/{advisor_id}/mix_timeseries.json.
    Shape: {advisor_id, data_as_of, data: [{date, total_aua, equity, fixed_income,
            structured_notes, cash, other}]} -- pct fields are 0-1 convention.
    Optional ?window= query param filters data list to trailing window.
    """
    if not advisor_id or '/' in advisor_id or '..' in advisor_id:
        return cors_response(400, {'error': f'Invalid advisor_id: {advisor_id}'})
    key = f'gold/advisors/{advisor_id}/mix.json'
    response = serve_s3_json(bucket, key)
    if window and isinstance(response, dict) and response.get('statusCode', 200) == 200:
        body = response.get('body')
        if body:
            try:
                parsed = json.loads(body)
                if parsed.get('data'):
                    parsed['data'] = _filter_window(parsed['data'], window)
                response['body'] = json.dumps(parsed)
            except Exception:
                pass
    return response


def handle_firm_mix_views(bucket: str) -> dict:
    """Serve pre-computed firm-level period mix views (quarterly/monthly/annually).

    Written by 06b_build_client_mix_timeseries.py at gold/firm_mix_views.json.
    Shape: {generated_at, data_as_of, firm_id, views: {quarterly, monthly, annually}}
    Each period entry: {period, label, end_date, total_aua, equity: {value, pct}, ...}
    pct values are 0-1.
    """
    return serve_s3_json(bucket, 'gold/firm_mix_views.json')


def handle_advisor_mix_views(bucket: str, advisor_id: str) -> dict:
    """Serve pre-computed per-advisor period mix views (quarterly/monthly/annually).

    Written by 06b_build_client_mix_timeseries.py at gold/advisors/{id}/mix.json.
    Shape: {generated_at, data_as_of, advisor_id, advisor_name, views: {quarterly, monthly, annually}}
    """
    if not advisor_id or '/' in advisor_id or '..' in advisor_id:
        return cors_response(400, {'error': f'Invalid advisor_id: {advisor_id}'})
    return serve_s3_json(bucket, f'gold/advisors/{advisor_id}/mix.json')


def handle_firm_composition(bucket: str) -> dict:
    """Serve pre-computed firm-level per-class composition (asset mix + top holdings).

    Written by 12_build_composition_artifacts.py at gold/views/firm_composition.json.
    Shape: {data_as_of, scope, total_market_value, top_holdings, other, mix, unclassified}
    Each mix item includes top_holdings (top 9 per class, pct relative to class AUM).
    Cache-Control: no-store -- position-level firm AUM data must not be cached.
    """
    return serve_s3_json_nocache(bucket, 'gold/views/firm_composition.json')


def handle_advisor_composition(bucket: str, advisor_id: str) -> dict:
    """Serve pre-computed per-advisor per-class composition (asset mix + top holdings).

    Written by 12_build_composition_artifacts.py at gold/advisors/{id}/composition.json.
    Shape: same as firm_composition.json with scope = {advisor_id, firm_id}.
    advisor_id must match the sanitization used in script 12 and ClientsTab.tsx:383.
    Cache-Control: no-store -- position-level advisor AUM data must not be cached.
    """
    if not advisor_id or '/' in advisor_id or '..' in advisor_id:
        return cors_response_nocache(400, {'error': 'Invalid advisor_id'})
    return serve_s3_json_nocache(bucket, f'gold/advisors/{advisor_id}/composition.json')


# =============================================================================
# Main Handler
# =============================================================================

def lambda_handler(event, context):
    """Main Lambda handler - routes requests to appropriate function.

    Args:
        event: API Gateway event
        context: Lambda context

    Returns:
        HTTP response dict
    """
    print(f'Event: {json.dumps(event)}')

    # Handle OPTIONS request (CORS preflight)
    http_method = event.get('httpMethod', 'GET')
    if http_method == 'OPTIONS':
        return cors_response(200, {'message': 'OK'})

    # Extract path
    path = event.get('path', event.get('rawPath', ''))

    # Normalize path (remove stage prefix if present)
    for prefix in ['/prod', '/dev', '/api']:
        if path.startswith(prefix):
            path = path[len(prefix):]

    # ===================
    # Health Check (No Auth Required)
    # ===================
    if http_method == 'GET' and (path == '/health/advisor-intelligence' or path == '/health/advisor-intelligence/'):
        return handle_health_check()

    # Extract authorizer context (handles both REST API and HTTP API v2 formats)
    authorizer = event.get('requestContext', {}).get('authorizer', {})
    # HTTP API v2 nests context under 'lambda' key
    auth_context = authorizer.get('lambda', authorizer)
    allowed_firms = auth_context.get('allowedFirmIds', '')
    user_email = auth_context.get('email', 'unknown')
    user_tier = auth_context.get('tier', '')

    # For internal users, grant ALL access even if allowedFirmIds is missing
    # (backwards compatibility during authorizer migration)
    if not allowed_firms and user_tier == 'internal':
        print(f'Internal user {user_email} - granting ALL access (fallback)')
        allowed_firms = 'ALL'

    # Extract query parameters
    query_params = event.get('queryStringParameters') or {}

    print(f'Routing: method={http_method}, path={path}, user={user_email}, allowedFirms={allowed_firms}')

    # If no auth context, deny access (should have been blocked by authorizer)
    if not allowed_firms:
        print('No allowedFirmIds in authorizer context - denying access')
        return cors_response(403, {'error': 'Access denied - no authorization context'})

    # ===================
    # V1: GET /partners
    # ===================
    if http_method == 'GET' and (path == '/partners' or path == '/partners/'):
        return handle_get_partners(allowed_firms)

    # ===================
    # V2: Advisor Intelligence Endpoints
    # ===================
    # All v2 endpoints require firmId query parameter
    if '/shared/advisor-intelligence' in path:
        firm_id = query_params.get('firmId', '')

        if not firm_id:
            return cors_response(400, {'error': 'Missing required query parameter: firmId'})

        # Authorization check
        if not is_authorized(firm_id, allowed_firms):
            print(f'Access denied: user cannot access firm {firm_id}')
            return cors_response(403, {'error': 'Access denied to this firm'})

        # Get S3 bucket for this firm
        bucket = get_firm_bucket(firm_id)
        if not bucket:
            return cors_response(404, {'error': f'Unknown firm: {firm_id}'})

        # Route to v2 handlers
        if '/timeseries/' in path:
            dimension = extract_path_param(path, 'timeseries')
            return handle_timeseries(bucket, dimension)

        elif '/snapshots/' in path:
            dimension = extract_path_param(path, 'snapshots')
            return handle_snapshots(bucket, dimension)

        elif path.endswith('/filters'):
            return handle_filters(bucket)

        elif '/clients/growth' in path:
            return handle_client_growth(bucket)

        elif '/clients/tax-breakdown' in path:
            return handle_tax_breakdown(bucket)

        elif '/clients/tax-deferred' in path:
            return handle_tax_deferred(bucket)

        elif path.endswith('/summary'):
            return handle_summary(bucket)

        elif '/partner-analytics' in path or path.endswith('/partner-analytics'):
            return handle_partner_analytics(bucket)

        elif '/advisors/' in path and '/book' in path:
            # Extract advisor_id from path: /advisors/{advisor_id}/book
            advisor_id = extract_path_param(path, 'advisors')
            return handle_advisor_book(bucket, advisor_id)

        elif '/advisors/' in path and '/mix-views' in path:
            # Extract advisor_id from path: /advisors/{advisor_id}/mix-views
            advisor_id = extract_path_param(path, 'advisors')
            return handle_advisor_mix_views(bucket, advisor_id)

    # ===================
    # V3: Books Tab Endpoints (L3/L4 drill views)
    # ===================
    if '/scoped/partners/books/' in path:
        firm_id = query_params.get('firmId', '')

        if not firm_id:
            return cors_response(400, {'error': 'Missing required query parameter: firmId'})

        if not is_authorized(firm_id, allowed_firms):
            print(f'Access denied: user cannot access firm {firm_id}')
            return cors_response(403, {'error': 'Access denied to this firm'})

        bucket = get_firm_bucket(firm_id)
        if not bucket:
            return cors_response(404, {'error': f'Unknown firm: {firm_id}'})

        # Parse: /scoped/partners/books/{entity_type}/{entity_id}/{action}
        books_parts = path.split('/scoped/partners/books/')[-1].rstrip('/').split('/')
        if len(books_parts) >= 3:
            entity_type = books_parts[0]   # 'relationship', 'account', 'firm', or 'advisor'
            entity_id = books_parts[1]
            action = books_parts[2]        # 'timeseries', 'composition', 'mix-timeseries', etc.

            if entity_type not in ('relationship', 'account', 'firm', 'advisor'):
                return cors_response(400, {'error': f'Invalid entity type: {entity_type}'})

            if action == 'timeseries' and entity_type == 'advisor':
                return handle_advisor_timeseries(bucket, entity_id)
            elif action == 'mix-timeseries' and entity_type == 'advisor':
                window = query_params.get('window')
                return handle_advisor_mix_timeseries(bucket, entity_id, window)
            elif action == 'timeseries':
                return handle_books_timeseries(bucket, entity_type, entity_id)
            elif action == 'composition' and entity_type == 'firm':
                return handle_firm_composition(bucket)
            elif action == 'composition' and entity_type == 'advisor':
                return handle_advisor_composition(bucket, entity_id)
            elif action == 'composition':
                return handle_books_composition(bucket, entity_type, entity_id)
            elif action == 'mix-timeseries' and entity_type == 'relationship':
                return handle_mix_timeseries(bucket, entity_id)
            elif action == 'concentration-timeseries' and entity_type == 'relationship':
                return handle_concentration_timeseries(bucket, entity_id)
            elif action == 'mix-views' and entity_type == 'firm':
                return handle_firm_mix_views(bucket)

        return cors_response(400, {'error': 'Invalid books endpoint path'})

    # ===================
    # UNKNOWN ROUTE
    # ===================
    return cors_response(404, {
        'error': 'Route not found',
        'path': path,
        'method': http_method,
        'available_routes': [
            'GET /api/partners',
            'GET /api/shared/advisor-intelligence/timeseries/{dimension}?firmId=xxx',
            'GET /api/shared/advisor-intelligence/snapshots/{dimension}?firmId=xxx',
            'GET /api/shared/advisor-intelligence/filters?firmId=xxx',
            'GET /api/shared/advisor-intelligence/clients/growth?firmId=xxx',
            'GET /api/shared/advisor-intelligence/clients/tax-breakdown?firmId=xxx',
            'GET /api/shared/advisor-intelligence/clients/tax-deferred?firmId=xxx',
            'GET /api/shared/advisor-intelligence/summary?firmId=xxx',
            'GET /api/shared/advisor-intelligence/partner-analytics?firmId=xxx',
            'GET /api/shared/advisor-intelligence/advisors/{advisorId}/book?firmId=xxx',
            'GET /api/scoped/partners/books/relationship/{id}/timeseries?firmId=xxx',
            'GET /api/scoped/partners/books/relationship/{id}/composition?firmId=xxx',
            'GET /api/scoped/partners/books/account/{id}/timeseries?firmId=xxx',
            'GET /api/scoped/partners/books/account/{id}/composition?firmId=xxx',
            'GET /api/scoped/partners/books/relationship/{id}/mix-timeseries?firmId=xxx&window=1Y',
            'GET /api/scoped/partners/books/relationship/{id}/concentration-timeseries?firmId=xxx&window=1Y',
            'GET /api/scoped/partners/books/firm/all/mix-views?firmId=xxx',
            'GET /api/shared/advisor-intelligence/advisors/{advisorId}/mix-views?firmId=xxx',
            'GET /api/scoped/partners/books/advisor/{id}/timeseries?firmId=xxx',
            'GET /api/scoped/partners/books/advisor/{id}/mix-timeseries?firmId=xxx&window=1Y',
            'GET /api/scoped/partners/books/firm/all/composition?firmId=xxx',
            'GET /api/scoped/partners/books/advisor/{id}/composition?firmId=xxx'
        ]
    })
