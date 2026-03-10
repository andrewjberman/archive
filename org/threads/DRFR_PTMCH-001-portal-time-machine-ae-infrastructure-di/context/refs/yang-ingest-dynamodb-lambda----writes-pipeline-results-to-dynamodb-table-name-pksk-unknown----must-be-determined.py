"""
Yang Pipeline - Ingest DynamoDB Lambda

Reads data PKL and ingests market data to DynamoDB incrementally.
Uses prior metadata to determine start date for incremental loading.

Creates two types of entries:
1. DAILY entries: data_key = 'DAILY#YYYY-MM-DD' (historical data)
2. LATEST entries: data_key = 'LATEST' (most recent per ticker, for quick lookups)

The portal's Market Overview page queries LATEST entries for fast loading.
"""

import json
import boto3
import pickle
import logging
import pandas as pd
from decimal import Decimal
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3_client = boto3.client('s3', region_name='us-east-1')
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

BUCKET = 'opal-data-portal-v2'
TABLE_NAME = 'opal-portal-market-data'

# Entity type mapping - COMPLETE mapping for all index_names in data PKL
# Updated 2026-01-19: Added all Bloomberg bonds, MSCIs, sectors, commodities
ENTITY_TYPES = {
    # === EQUITY INDICES ===
    'S&P 500': 'INDEX',
    'Dow Jones': 'INDEX',
    'Nasdaq': 'INDEX',
    'Russell 1000': 'INDEX',
    'Russell 1000 Growth': 'INDEX',
    'Russell 1000 Value': 'INDEX',
    'Russell 2000': 'INDEX',
    'Russell Mid Cap': 'INDEX',
    'Russell Mid Cap Growth': 'INDEX',
    'Russell Mid Cap Value': 'INDEX',

    # MSCI Global Indices
    'MSCI ACWI': 'INDEX',
    'MSCI ACWI ex US': 'INDEX',
    'MSCI EAFE': 'INDEX',
    'MSCI EAFE Growth': 'INDEX',
    'MSCI EAFE Value': 'INDEX',
    'MSCI Emerging Markets': 'INDEX',
    'MSCI USA': 'INDEX',
    'MSCI USA Growth': 'INDEX',
    'MSCI USA Value': 'INDEX',
    'MSCI USA Momentum': 'INDEX',
    'MSCI USA Quality': 'INDEX',
    'MSCI USA Size': 'INDEX',
    'MSCI USA Minimum Volatility': 'INDEX',

    # MSCI Country Indices
    'MSCI Australia': 'INDEX',
    'MSCI Brazil': 'INDEX',
    'MSCI China': 'INDEX',
    'MSCI France': 'INDEX',
    'MSCI Germany': 'INDEX',
    'MSCI India': 'INDEX',
    'MSCI Italy': 'INDEX',
    'MSCI Japan': 'INDEX',
    'MSCI Netherlands': 'INDEX',
    'MSCI Saudi Arabia': 'INDEX',
    'MSCI South Africa': 'INDEX',
    'MSCI South Korea': 'INDEX',
    'MSCI Spain': 'INDEX',
    'MSCI Sweden': 'INDEX',
    'MSCI Switzerland': 'INDEX',
    'MSCI Taiwan': 'INDEX',
    'MSCI United Kindom': 'INDEX',  # Note: typo in source data

    # S&P 500 Sectors
    'Communication Services': 'INDEX',
    'Consumer Discretionary': 'INDEX',
    'Consumer Staples': 'INDEX',
    'Energy': 'INDEX',
    'Financials': 'INDEX',
    'Health Care': 'INDEX',
    'Industrials': 'INDEX',
    'Information Technology': 'INDEX',
    'Materials': 'INDEX',
    'Real Estate': 'INDEX',
    'Utilities': 'INDEX',

    # Digital Assets (classified as INDEX for portal display)
    'Bitcoin': 'INDEX',
    'Ethereum': 'INDEX',

    # === BOND INDICES (Fixed Income) ===
    'Bloomberg Aggregate': 'BOND_INDEX',
    'Bloomberg US Corporate': 'BOND_INDEX',
    'Bloomberg High Yield': 'BOND_INDEX',
    'Bloomberg Municipal': 'BOND_INDEX',
    'Bloomberg TIPS': 'BOND_INDEX',
    'Bloomberg 0-1 Year Treasury': 'BOND_INDEX',
    'Bloomberg 0-5 Year High Yield': 'BOND_INDEX',
    'Bloomberg 0-5 Year TIPS': 'BOND_INDEX',
    'Bloomberg 1-3 Year Gov/Credit': 'BOND_INDEX',
    'Bloomberg 1-5 Year Gov/Credit': 'BOND_INDEX',
    'Bloomberg 20+ Year Treasury': 'BOND_INDEX',

    # === COMMODITIES ===
    'Gold': 'COMMODITY',
    'Silver': 'COMMODITY',
    'Copper': 'COMMODITY',
    'Crude Oil WTI': 'COMMODITY',
    'Crude Oil Brent': 'COMMODITY',
    'Natural Gas': 'COMMODITY',
    'S&P GSCI': 'COMMODITY',
}


def lambda_handler(event, context):
    """Ingest market data to DynamoDB."""
    logger.info(f"Event: {json.dumps(event)}")

    manifest = event.get('manifest', {})
    processed = event.get('processed', {})
    prior = event.get('prior', {})

    bucket = manifest.get('bucket', BUCKET)
    data_pkl_key = processed.get('data_pkl_key')
    data_version = manifest.get('version', 'unknown')

    if not data_pkl_key:
        raise ValueError("Missing data_pkl_key")

    # Determine start date for incremental loading
    start_date = prior.get('start_date')
    is_first_upload = prior.get('is_first_upload', False)

    if is_first_upload:
        logger.info("First upload - will do full load")
        start_date = None
    elif start_date:
        logger.info(f"Incremental load from {start_date}")
        start_date = pd.to_datetime(start_date)
    else:
        logger.info("No prior date - will do full load")

    # Load data PKL
    logger.info(f"Loading data PKL from s3://{bucket}/{data_pkl_key}")
    pkl_data = load_pkl(bucket, data_pkl_key)

    # Get return_daily DataFrame
    df = pkl_data.get('return_daily')
    if df is None:
        raise ValueError("return_daily not found in PKL")

    logger.info(f"Loaded {len(df)} rows")

    # Filter by start date if incremental
    if start_date is not None:
        original_count = len(df)
        df = df[df['date'] >= start_date]
        logger.info(f"Filtered to {len(df)} rows (from {original_count})")

    # Transform to DynamoDB format
    logger.info("Transforming to DynamoDB format...")
    items = transform_to_dynamodb(df, data_version)
    logger.info(f"Transformed {len(items)} items")

    # Upload DAILY entries to DynamoDB
    logger.info("Uploading DAILY entries to DynamoDB...")
    daily_uploaded, daily_failed = upload_to_dynamodb(items)

    # Update LATEST entries for each ticker (critical for portal performance)
    logger.info("Updating LATEST entries...")
    latest_uploaded, latest_failed = update_latest_entries(items)

    return {
        'daily_uploaded': daily_uploaded,
        'daily_failed': daily_failed,
        'latest_uploaded': latest_uploaded,
        'latest_failed': latest_failed,
        'data_version': data_version,
        'start_date': str(start_date) if start_date else 'full_load'
    }


def load_pkl(bucket: str, key: str) -> dict:
    """Load PKL from S3."""
    response = s3_client.get_object(Bucket=bucket, Key=key)
    return pickle.loads(response['Body'].read())


def transform_to_dynamodb(df: pd.DataFrame, data_version: str) -> list:
    """Transform DataFrame to DynamoDB items with DAILY data_key."""
    items = []

    for _, row in df.iterrows():
        index_name = row.get('index_name')
        date = row.get('date')
        price = row.get('price')
        ret = row.get('return')

        if pd.isna(index_name) or pd.isna(date) or pd.isna(price):
            continue

        # Skip model portfolios (they have their own data structures)
        if index_name in ['UST', 'ST', 'INT', 'LTC', 'LTA']:
            continue

        # Skip "Term" entries (used for benchmark calculations, not market data)
        if 'Term' in str(index_name):
            continue

        # Determine entity type
        entity_type = ENTITY_TYPES.get(index_name, 'INDEX')

        # Format date
        date_str = date.strftime('%Y-%m-%d') if hasattr(date, 'strftime') else str(date)

        item = {
            'ticker_id': f"{entity_type}#{index_name}",
            'data_key': f"DAILY#{date_str}",  # Key for daily entries
            'entity_type': entity_type,  # Store for filtering by asset class
            'ticker': index_name,  # Store ticker name for easy access
            'date': date_str,
            'price': Decimal(str(round(price, 2))),
            'data_version': data_version,
        }

        if not pd.isna(ret):
            item['daily_return'] = Decimal(str(round(ret, 6)))

        items.append(item)

    return items


def update_latest_entries(items: list) -> tuple:
    """
    Update LATEST entries for each ticker based on the most recent daily data.

    This is critical for the portal's Market Overview page which queries
    data_key='LATEST' for quick lookups.

    Args:
        items: List of DynamoDB items (already uploaded daily data)

    Returns:
        tuple: (uploaded_count, failed_count)
    """
    table = dynamodb.Table(TABLE_NAME)

    # Group by ticker_id and find latest date for each
    latest_by_ticker = {}
    for item in items:
        ticker_id = item['ticker_id']
        date = item['date']

        if ticker_id not in latest_by_ticker or date > latest_by_ticker[ticker_id]['date']:
            latest_by_ticker[ticker_id] = item.copy()

    logger.info(f"Found {len(latest_by_ticker)} unique tickers for LATEST update")

    # Create LATEST entries
    latest_items = []
    for ticker_id, item in latest_by_ticker.items():
        latest_item = item.copy()
        latest_item['data_key'] = 'LATEST'  # Override data_key to LATEST
        latest_items.append(latest_item)

    # Upload LATEST entries
    uploaded = 0
    failed = 0

    batch_size = 25
    for i in range(0, len(latest_items), batch_size):
        batch = latest_items[i:i + batch_size]

        try:
            with table.batch_writer() as writer:
                for item in batch:
                    writer.put_item(Item=item)
            uploaded += len(batch)
        except Exception as e:
            logger.error(f"LATEST batch write failed: {e}")
            failed += len(batch)

    logger.info(f"LATEST entries: {uploaded} uploaded, {failed} failed")
    return uploaded, failed


def upload_to_dynamodb(items: list) -> tuple:
    """Upload items to DynamoDB using batch write."""
    table = dynamodb.Table(TABLE_NAME)

    uploaded = 0
    failed = 0

    # Batch write (max 25 items per batch)
    batch_size = 25
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]

        try:
            with table.batch_writer() as writer:
                for item in batch:
                    writer.put_item(Item=item)
            uploaded += len(batch)
        except Exception as e:
            logger.error(f"Batch write failed: {e}")
            failed += len(batch)

        # Log progress every 1000 items
        if (i + batch_size) % 1000 == 0:
            logger.info(f"Progress: {i + batch_size}/{len(items)}")

    logger.info(f"Upload complete: {uploaded} uploaded, {failed} failed")
    return uploaded, failed
