"""
FRED Credit Spread Cache Refresh Lambda

Scheduled to run weekly (Sundays 6 AM UTC) to keep credit spread data current.
Downloads ICE BofA credit spread indices from FRED and caches in S3.

Data Series:
- BAMLC0A0CM: ICE BofA US Corporate Master OAS (Investment Grade)
- BAMLH0A0HYM2: ICE BofA US High Yield Master II OAS (High Yield)

Cache Location:
- s3://opal-data-portal-v2/cache/fred/BAMLC0A0CM.csv
- s3://opal-data-portal-v2/cache/fred/BAMLH0A0HYM2.csv

Used by: yang-generate-risk-premium Lambda
"""

import json
import boto3
import logging
from datetime import datetime
from urllib.request import urlopen
from urllib.error import URLError, HTTPError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3_client = boto3.client('s3', region_name='us-east-1')

BUCKET = 'opal-data-portal-v2'
FRED_BASE_URL = 'https://fred.stlouisfed.org/graph/fredgraph.csv'

# FRED series to download
FRED_SERIES = {
    'BAMLC0A0CM': {
        'description': 'ICE BofA US Corporate Master OAS (Investment Grade)',
        's3_key': 'cache/fred/BAMLC0A0CM.csv',
    },
    'BAMLH0A0HYM2': {
        'description': 'ICE BofA US High Yield Master II OAS (High Yield)',
        's3_key': 'cache/fred/BAMLH0A0HYM2.csv',
    },
}


def lambda_handler(event, context):
    """
    Download FRED credit spread data and cache in S3.

    Triggered by: CloudWatch Events schedule (weekly)
    """
    logger.info(f"FRED Cache Refresh started at {datetime.utcnow().isoformat()}")
    logger.info(f"Event: {json.dumps(event)}")

    results = {}
    errors = []

    for series_id, config in FRED_SERIES.items():
        try:
            logger.info(f"Downloading {series_id}: {config['description']}")

            # Download from FRED
            url = f"{FRED_BASE_URL}?id={series_id}"
            csv_data = download_fred_data(url)

            if not csv_data:
                raise ValueError(f"Empty response from FRED for {series_id}")

            # Count data points (subtract 1 for header)
            line_count = csv_data.count('\n')
            data_points = line_count - 1 if line_count > 0 else 0

            logger.info(f"Downloaded {data_points} data points for {series_id}")

            # Upload to S3
            s3_key = config['s3_key']
            upload_to_s3(BUCKET, s3_key, csv_data)

            logger.info(f"Uploaded to s3://{BUCKET}/{s3_key}")

            results[series_id] = {
                'status': 'SUCCESS',
                'data_points': data_points,
                's3_key': s3_key,
            }

        except Exception as e:
            logger.error(f"Failed to process {series_id}: {str(e)}")
            errors.append(series_id)
            results[series_id] = {
                'status': 'FAILED',
                'error': str(e),
            }

    # Summary
    success_count = sum(1 for r in results.values() if r['status'] == 'SUCCESS')
    total_count = len(FRED_SERIES)

    summary = {
        'completed_at': datetime.utcnow().isoformat() + 'Z',
        'success': success_count,
        'failed': len(errors),
        'total': total_count,
        'results': results,
    }

    logger.info(f"FRED Cache Refresh complete: {success_count}/{total_count} successful")

    if errors:
        logger.warning(f"Failed series: {errors}")

    return summary


def download_fred_data(url: str) -> str:
    """Download CSV data from FRED."""
    try:
        logger.info(f"Fetching: {url}")

        with urlopen(url, timeout=30) as response:
            data = response.read().decode('utf-8')
            return data

    except HTTPError as e:
        logger.error(f"HTTP Error {e.code}: {e.reason}")
        raise
    except URLError as e:
        logger.error(f"URL Error: {e.reason}")
        raise
    except Exception as e:
        logger.error(f"Download failed: {str(e)}")
        raise


def upload_to_s3(bucket: str, key: str, data: str) -> None:
    """Upload CSV data to S3."""
    s3_client.put_object(
        Bucket=bucket,
        Key=key,
        Body=data.encode('utf-8'),
        ContentType='text/csv',
        Metadata={
            'refreshed_at': datetime.utcnow().isoformat(),
            'source': 'FRED',
        }
    )
