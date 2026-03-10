"""
Yang Pipeline - Capture Output Versions Lambda

After successful pipeline execution, captures S3 version IDs of all JSON outputs.
This enables true rollback by restoring exact previous versions.

Author: AWS Engineer
Date: 2026-02-02
"""

import json
import boto3
import logging
from datetime import datetime, timezone, timedelta

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3_client = boto3.client('s3', region_name='us-east-1')

BUCKET = 'opal-data-portal-v2'
JSON_PREFIX = 'json/'


def lambda_handler(event, context):
    """
    Capture S3 version IDs of all JSON outputs.

    Input:
        {
            "pipeline_execution_id": "exec-abc123",
            "pipeline_started_at": "2026-01-31T23:05:33Z",
            "manifest": {...},
            "data_as_of_date": "2026-01-30"
        }

    Output:
        {
            "outputCount": 18,
            "archiveKey": "data-refresh/archive/exec-abc123/outputs-manifest.json"
        }
    """
    logger.info(f"Event: {json.dumps(event)}")

    execution_id = event.get('pipeline_execution_id')
    started_at = event.get('pipeline_started_at')
    data_as_of = event.get('data_as_of_date')
    manifest = event.get('manifest', {})

    if not execution_id:
        raise ValueError("pipeline_execution_id is required")

    # Find all JSON files modified recently (within last 10 minutes)
    # This captures everything the pipeline just generated
    cutoff_time = datetime.now(timezone.utc) - timedelta(minutes=10)
    outputs = {}

    logger.info(f"Scanning {JSON_PREFIX} for files modified after {cutoff_time.isoformat()}")

    # Paginate through all JSON files
    paginator = s3_client.get_paginator('list_objects_v2')
    page_iterator = paginator.paginate(Bucket=BUCKET, Prefix=JSON_PREFIX)

    total_scanned = 0
    total_captured = 0

    for page in page_iterator:
        for obj in page.get('Contents', []):
            key = obj['Key']
            total_scanned += 1

            # Only process actual JSON files (not folders)
            if not key.endswith('.json'):
                continue

            # Get version info via HEAD request
            try:
                head_response = s3_client.head_object(Bucket=BUCKET, Key=key)

                last_modified = head_response['LastModified']

                # Check if modified recently (updated during this pipeline execution)
                if last_modified >= cutoff_time:
                    outputs[key] = {
                        'versionId': head_response.get('VersionId'),
                        'size': head_response['ContentLength'],
                        'etag': head_response['ETag'].strip('"'),
                        'lastModified': last_modified.isoformat()
                    }
                    total_captured += 1
                    logger.info(f"  ✓ Captured: {key} (version: {head_response.get('VersionId')})")

            except Exception as e:
                logger.warning(f"  ⚠ Error checking {key}: {e}")
                continue

    # Build outputs manifest
    outputs_manifest = {
        'schema_version': '1.0',
        'executionId': execution_id,
        'capturedAt': datetime.now(timezone.utc).isoformat(),
        'pipelineStartedAt': started_at,
        'dataAsOfDate': data_as_of,
        'inputFiles': manifest.get('files', {}),
        'outputCount': len(outputs),
        'outputs': outputs,
        'stats': {
            'totalScanned': total_scanned,
            'totalCaptured': total_captured,
            'cutoffTime': cutoff_time.isoformat()
        }
    }

    # Save to archive
    archive_key = f'data-refresh/archive/{execution_id}/outputs-manifest.json'

    s3_client.put_object(
        Bucket=BUCKET,
        Key=archive_key,
        Body=json.dumps(outputs_manifest, indent=2, default=str),
        ContentType='application/json'
    )

    logger.info(f"✓ Captured {len(outputs)} output versions for {execution_id}")
    logger.info(f"✓ Saved to s3://{BUCKET}/{archive_key}")

    return {
        'outputCount': len(outputs),
        'archiveKey': archive_key,
        'executionId': execution_id
    }
