"""
Lambda Function: opal-data-refresh-api

Purpose: Handle Data Refresh Portal API endpoints for uploading optimizer outputs
         and monitoring the Yang Pipeline execution.

Author: AWS Engineer
Date: 2026-01-19

API Endpoints:
    POST /data-refresh/upload-urls    - Get presigned S3 URLs for browser uploads
    POST /data-refresh/trigger        - Move staged files to uploads/ to kick off Yang Pipeline
    GET  /data-refresh/status/{id}    - Poll Step Functions execution status
    GET  /data-refresh/history        - List past executions with metadata
    POST /data-refresh/rollback       - Re-run pipeline from archived files

SECURITY SCANNER ENDPOINTS:
    POST /security-scanner/upload-url                          - Presigned PUT URL for FactSet Excel upload
    GET  /security-scanner/factors                             - Factor metadata (S3: json/security_scanner/latest/factor_metadata.json)
    GET  /security-scanner/universe/{universeId}/data          - Universe security-level data
    GET  /security-scanner/universe/{universeId}/scanner       - Universe scanner percentile data

Security:
    - All endpoints require valid JWT with userType: 'Dev' claim
    - Files validated for type (only .pkl, .json, .xlsx, .csv allowed)
"""

import json
import boto3
import os
import uuid
import re
from datetime import datetime, timezone, timedelta
from decimal import Decimal
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

# Initialize AWS clients
s3_client = boto3.client('s3', region_name='us-east-1')
sfn_client = boto3.client('stepfunctions', region_name='us-east-1')
cloudfront_client = boto3.client('cloudfront', region_name='us-east-1')
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

# Configuration
BUCKET = os.environ.get('BUCKET', 'opal-data-portal-v2')
TABLE_NAME = os.environ.get('TABLE_NAME', 'opal-data-refresh-executions')
STATE_MACHINE_ARN = os.environ.get(
    'STATE_MACHINE_ARN',
    'arn:aws:states:us-east-1:313476888478:stateMachine:YangDataPipeline'
)
CLOUDFRONT_DIST_ID = os.environ.get('CLOUDFRONT_DIST_ID', 'EVTSA9VEHNZVH')
PRESIGN_EXPIRY = int(os.environ.get('PRESIGN_EXPIRY', 3600))  # 1 hour default
SSCN_PRESIGN_EXPIRY = 900  # 15 minutes for security scanner uploads
SSCN_VALID_UNIVERSES = {'sp500', 'r1000', 'r1000v', 'acwx', 'eafe', 'eafev'}
SSCN_S3_PREFIX = 'json/security_scanner/latest'
MAX_ROLLBACK_EXECUTIONS = int(os.environ.get('MAX_ROLLBACK_EXECUTIONS', 10))

# Initialize DynamoDB table
table = dynamodb.Table(TABLE_NAME)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'.pkl', '.json', '.xlsx', '.csv'}


class DecimalEncoder(json.JSONEncoder):
    """Convert Decimal to float for JSON serialization"""
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)


def cors_response(status_code, body):
    """Create HTTP response with CORS headers"""
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET,POST,OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type,Authorization,X-Api-Key'
        },
        'body': json.dumps(body, cls=DecimalEncoder)
    }


def validate_user_type(event):
    """
    Validate that the user has 'Dev' userType claim.
    Returns (is_valid, user_email) tuple.
    """
    try:
        # Method 1: Lambda authorizer with simple response format (EnableSimpleResponses=true)
        # Context is directly in requestContext.authorizer
        authorizer_context = event.get('requestContext', {}).get('authorizer', {})

        if 'email' in authorizer_context:
            # We have Lambda authorizer context (our opal-portal-authorizer)
            user_email = authorizer_context.get('email', 'unknown')
            user_type = authorizer_context.get('userType', 'null')

            # 'null' string means no userType set (from authorizer line 202)
            if user_type == 'null':
                user_type = ''

            print(f"Lambda authorizer context: email={user_email}, userType={user_type}, tier={authorizer_context.get('tier', 'null')}")

            # Allow Dev users or users without userType restriction
            if not user_type or user_type == 'Dev':
                return True, user_email
            else:
                print(f"User {user_email} has userType={user_type}, requires 'Dev'")
                return False, user_email

        # Method 2: Cognito JWT authorizer (claims in authorizer.claims)
        claims = authorizer_context.get('claims', {})
        if not claims:
            claims = authorizer_context.get('jwt', {}).get('claims', {})

        if claims:
            user_type = claims.get('custom:userType', claims.get('userType', ''))
            user_email = claims.get('email', 'unknown')
            print(f"JWT claims: email={user_email}, userType={user_type}")

            if user_type != 'Dev':
                print(f"User {user_email} has userType={user_type}, requires 'Dev'")
                return False, user_email

            return True, user_email

        # Method 3: No authorizer (development fallback)
        print("WARNING: No authorizer context found - using development fallback")
        print(f"Full requestContext.authorizer: {json.dumps(authorizer_context)}")
        return True, 'dev@test.com'

    except Exception as e:
        print(f"Error validating user: {e}")
        import traceback
        traceback.print_exc()
        return False, 'unknown'


def validate_file_extension(filename):
    """Check if file has allowed extension"""
    ext = os.path.splitext(filename.lower())[1]
    return ext in ALLOWED_EXTENSIONS


def generate_manifest_from_files(file_names):
    """
    Auto-generate manifest.json from uploaded file names.

    File type detection:
        - data*.pkl, data_*.pkl, data *.pkl → data_pkl
        - model*.pkl, model_*.pkl, model *.pkl → model_pkl
        - *cma*.xlsx → cma_excel
        - *peer*.xlsx → peer_excel
        - *attribution*.xlsx → attribution_excel

    Date extraction from filenames:
        - YYYYMMDD pattern (e.g., data_20260117_v1.pkl → 2026-01-17)
        - MMDDYYYY pattern (e.g., data 01172026 v1.pkl → 2026-01-17)

    Returns:
        (manifest_dict, data_as_of_date)
    """
    files = {}
    extracted_date = None

    for filename in file_names:
        filename_lower = filename.lower()

        # Skip manifest.json if already present
        if filename_lower == 'manifest.json':
            continue

        # Detect file type
        file_type = None

        if filename_lower.endswith('.pkl'):
            if filename_lower.startswith('data') or '_data' in filename_lower:
                file_type = 'data_pkl'
            elif filename_lower.startswith('model') or '_model' in filename_lower:
                file_type = 'model_pkl'
        elif filename_lower.endswith('.xlsx'):
            if 'screening' in filename_lower:
                file_type = 'screening_excel'
            elif 'cma' in filename_lower:
                file_type = 'cma_excel'
            elif 'peer' in filename_lower:
                file_type = 'peer_excel'
            elif 'attribution' in filename_lower:
                file_type = 'attribution_excel'
            elif 'saa' in filename_lower:
                file_type = 'saa_excel'
        if file_type:
            files[file_type] = filename
            print(f"Detected {file_type}: {filename}")

            # Try to extract date from filename
            if not extracted_date:
                extracted_date = extract_date_from_filename(filename)

    # Build manifest
    manifest = {
        'version': datetime.now(timezone.utc).strftime('%Y%m%d_v1'),
        'date': extracted_date or datetime.now(timezone.utc).strftime('%Y-%m-%d'),
        'files': files,
        'auto_generated': True,
        'generated_at': datetime.now(timezone.utc).isoformat()
    }

    return manifest, extracted_date


def extract_date_from_filename(filename):
    """
    Extract date from filename patterns.

    Supported patterns:
        - YYYYMMDD (e.g., 20260117)
        - MMDDYYYY (e.g., 01172026)
        - YYYY-MM-DD (e.g., 2026-01-17)
        - MM-DD-YYYY (e.g., 01-17-2026)

    Returns:
        ISO date string (YYYY-MM-DD) or None
    """
    # Remove extension and common separators
    base = os.path.splitext(filename)[0]

    # Pattern: YYYYMMDD (8 consecutive digits starting with 20)
    match = re.search(r'(20\d{2})(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])', base)
    if match:
        year, month, day = match.groups()
        return f"{year}-{month}-{day}"

    # Pattern: MMDDYYYY (8 consecutive digits ending with 20XX)
    match = re.search(r'(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])(20\d{2})', base)
    if match:
        month, day, year = match.groups()
        return f"{year}-{month}-{day}"

    # Pattern: YYYY-MM-DD
    match = re.search(r'(20\d{2})-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])', base)
    if match:
        return match.group(0)

    # Pattern: MM-DD-YYYY
    match = re.search(r'(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])-(20\d{2})', base)
    if match:
        month, day, year = match.groups()
        return f"{year}-{month}-{day}"

    return None


# =============================================================================
# ENDPOINT 1: POST /data-refresh/upload-urls
# =============================================================================

def handle_upload_urls(event):
    """
    Generate presigned S3 URLs for browser uploads.

    Request:
    {
        "files": [
            { "name": "manifest.json", "size": 1024 },
            { "name": "data_20250115_v1.pkl", "size": 52428800 }
        ]
    }

    Response:
    {
        "uploadId": "uuid-v4",
        "urls": {
            "manifest.json": "https://s3.amazonaws.com/...?X-Amz-Signature=...",
            ...
        },
        "expiresIn": 3600
    }
    """
    # Validate user
    is_valid, user_email = validate_user_type(event)
    if not is_valid:
        return cors_response(403, {'error': 'Forbidden - requires Dev userType'})

    try:
        # Parse request body
        body = json.loads(event.get('body', '{}'))
        files = body.get('files', [])

        if not files:
            return cors_response(400, {'error': 'No files specified'})

        # Validate file extensions
        for file_info in files:
            filename = file_info.get('name', '')
            if not validate_file_extension(filename):
                return cors_response(400, {
                    'error': f'Invalid file type: {filename}',
                    'allowed': list(ALLOWED_EXTENSIONS)
                })

        # Generate upload ID
        upload_id = str(uuid.uuid4())

        # Generate presigned URLs for each file
        urls = {}
        for file_info in files:
            filename = file_info.get('name', '')
            s3_key = f'data-refresh/pending/{upload_id}/{filename}'

            presigned_url = s3_client.generate_presigned_url(
                'put_object',
                Params={
                    'Bucket': BUCKET,
                    'Key': s3_key,
                    'ContentType': 'application/octet-stream'
                },
                ExpiresIn=PRESIGN_EXPIRY
            )
            urls[filename] = presigned_url

        # Record pending upload in DynamoDB
        table.put_item(Item={
            'PK': f'UPLOAD#{upload_id}',
            'SK': 'PENDING',
            'uploadId': upload_id,
            'status': 'pending',
            'files': [f.get('name') for f in files],
            'createdAt': datetime.now(timezone.utc).isoformat(),
            'createdBy': user_email,
            'expiresAt': (datetime.now(timezone.utc) + timedelta(seconds=PRESIGN_EXPIRY)).isoformat()
        })

        print(f"Generated presigned URLs for upload {upload_id}, files: {[f.get('name') for f in files]}")

        return cors_response(200, {
            'uploadId': upload_id,
            'urls': urls,
            'expiresIn': PRESIGN_EXPIRY
        })

    except Exception as e:
        print(f"Error generating presigned URLs: {e}")
        return cors_response(500, {'error': 'Internal server error', 'message': str(e)})


# =============================================================================
# ENDPOINT 2: POST /data-refresh/trigger
# =============================================================================

def handle_trigger(event):
    """
    Move staged files to uploads/ folder and trigger Yang Pipeline.

    Request:
    {
        "uploadId": "uuid-from-step-1"
    }

    Response:
    {
        "executionId": "exec-abc123",
        "executionArn": "arn:aws:states:us-east-1:...",
        "status": "RUNNING"
    }
    """
    # Validate user
    is_valid, user_email = validate_user_type(event)
    if not is_valid:
        return cors_response(403, {'error': 'Forbidden - requires Dev userType'})

    try:
        # Parse request body
        body = json.loads(event.get('body', '{}'))
        upload_id = body.get('uploadId')

        if not upload_id:
            return cors_response(400, {'error': 'uploadId is required'})

        # Verify files exist in pending folder
        pending_prefix = f'data-refresh/pending/{upload_id}/'
        response = s3_client.list_objects_v2(
            Bucket=BUCKET,
            Prefix=pending_prefix
        )

        pending_files = response.get('Contents', [])
        if not pending_files:
            return cors_response(404, {'error': f'No files found for upload {upload_id}'})

        # Get list of uploaded file names
        file_names = [os.path.basename(f['Key']) for f in pending_files]

        # Auto-generate manifest.json from uploaded files
        manifest_data, data_as_of_date = generate_manifest_from_files(file_names)

        if not manifest_data.get('files'):
            return cors_response(400, {'error': 'No recognized file types uploaded. Expected: data*.pkl, model*.pkl, *cma*.xlsx, *peer*.xlsx, *attribution*.xlsx, *saa*.xlsx, *screening*.xlsx'})

        print(f"Auto-generated manifest: {json.dumps(manifest_data)}")
        print(f"Extracted data_as_of_date: {data_as_of_date}")

        # Route Security Scanner (screening_excel) through SSCN path.
        # The Screening xlsx lands in security_scanner/uploads/{asOf}/ which triggers
        # opal-security-scanner-processor via the portal-notifications S3 event.
        # It does NOT go through the yang pipeline or Step Functions.
        if 'screening_excel' in manifest_data.get('files', {}):
            screening_filename = manifest_data['files']['screening_excel']
            screening_pending = next(
                (f for f in pending_files if os.path.basename(f['Key']) == screening_filename),
                None
            )
            if not screening_pending:
                return cors_response(400, {'error': f'Screening file not found in pending upload: {screening_filename}'})

            # Derive asOf from filename (extract_date_from_filename handles YYYYMMDD pattern)
            as_of = data_as_of_date or datetime.now(timezone.utc).strftime('%Y-%m-%d')
            as_of_nodashes = as_of.replace('-', '')

            sscn_dest_key = f'security_scanner/uploads/{as_of}/Screening_DIVZ_IDVZ_{as_of_nodashes}.xlsx'

            # Copy from pending to security_scanner/uploads/ — S3 event fires SSCN processor
            s3_client.copy_object(
                Bucket=BUCKET,
                CopySource={'Bucket': BUCKET, 'Key': screening_pending['Key']},
                Key=sscn_dest_key
            )
            print(f"SSCN: copied {screening_filename} -> {sscn_dest_key}")

            # Record the SSCN execution in DynamoDB for status polling
            sscn_exec_id = f"sscn-{uuid.uuid4().hex[:12]}"
            now = datetime.now(timezone.utc).isoformat()
            table.put_item(Item={
                'PK': 'SSCN_EXECUTION',
                'SK': sscn_exec_id,
                'executionId': sscn_exec_id,
                'uploadId': upload_id,
                'status': 'RUNNING',
                'startedAt': now,
                'filesProcessed': [screening_filename],
                'triggeredBy': user_email,
                'dataAsOfDate': as_of,
                's3Key': sscn_dest_key,
                'canRollback': False,
            })

            # Clean up pending folder
            for file_obj in pending_files:
                s3_client.delete_object(Bucket=BUCKET, Key=file_obj['Key'])
            try:
                table.delete_item(Key={'PK': f'UPLOAD#{upload_id}', 'SK': 'PENDING'})
            except Exception:
                pass

            print(f"SSCN trigger complete: executionId={sscn_exec_id}, s3Key={sscn_dest_key}")
            return cors_response(200, {
                'executionId': sscn_exec_id,
                'executionArn': 'sscn',
                'dataAsOfDate': as_of,
                'status': 'RUNNING',
                'type': 'sscn',
            })

        # Upload generated manifest.json to pending folder
        manifest_key = f'{pending_prefix}manifest.json'
        s3_client.put_object(
            Bucket=BUCKET,
            Key=manifest_key,
            Body=json.dumps(manifest_data, indent=2),
            ContentType='application/json'
        )
        file_names.append('manifest.json')
        # Add manifest to pending_files list so it gets copied to archive and uploads
        pending_files.append({'Key': manifest_key})
        print(f"Uploaded auto-generated manifest to {manifest_key}")

        # Generate execution ID (short form for readability)
        execution_id = f"exec-{uuid.uuid4().hex[:12]}"

        # 1. Copy files to archive for rollback capability
        archive_prefix = f'data-refresh/archive/{execution_id}/'
        for file_obj in pending_files:
            source_key = file_obj['Key']
            filename = os.path.basename(source_key)
            archive_key = f'{archive_prefix}{filename}'

            s3_client.copy_object(
                Bucket=BUCKET,
                CopySource={'Bucket': BUCKET, 'Key': source_key},
                Key=archive_key
            )
            print(f"Archived: {source_key} -> {archive_key}")

        # 2. Copy files to uploads/ folder (triggers Yang Pipeline via S3 notification)
        for file_obj in pending_files:
            source_key = file_obj['Key']
            filename = os.path.basename(source_key)
            dest_key = f'uploads/{filename}'

            s3_client.copy_object(
                Bucket=BUCKET,
                CopySource={'Bucket': BUCKET, 'Key': source_key},
                Key=dest_key
            )
            print(f"Copied to uploads: {source_key} -> {dest_key}")

        # 3. Wait for Step Functions to start, then get the execution ARN
        # The trigger Lambda is invoked by S3 notification on manifest.json upload
        # Retry a few times since S3 notifications can have variable latency
        import time

        execution_arn = None
        for attempt in range(5):  # Try up to 5 times (15 seconds total)
            time.sleep(3)  # Wait 3 seconds between attempts

            executions = sfn_client.list_executions(
                stateMachineArn=STATE_MACHINE_ARN,
                statusFilter='RUNNING',
                maxResults=5
            )

            for exec_info in executions.get('executions', []):
                # Check if this execution started recently (within last 30 seconds)
                start_time = exec_info.get('startDate')
                if start_time:
                    age_seconds = (datetime.now(timezone.utc) - start_time.replace(tzinfo=timezone.utc)).total_seconds()
                    if age_seconds < 30:
                        execution_arn = exec_info['executionArn']
                        print(f"Found execution ARN on attempt {attempt + 1}: {execution_arn}")
                        break

            if execution_arn:
                break
            print(f"Attempt {attempt + 1}: No recent execution found, retrying...")

        # 4. Record execution in DynamoDB
        now = datetime.now(timezone.utc).isoformat()
        table.put_item(Item={
            'PK': 'EXECUTION',
            'SK': execution_id,
            'executionId': execution_id,
            'executionArn': execution_arn or 'pending',
            'uploadId': upload_id,
            'status': 'RUNNING',
            'startedAt': now,
            'filesProcessed': file_names,
            'triggeredBy': user_email,
            'archivePath': archive_prefix,
            'canRollback': True,
            'dataAsOfDate': data_as_of_date or ''
        })

        # 5. Write archive metadata.json
        metadata = {
            'executionId': execution_id,
            'executionArn': execution_arn,
            'uploadId': upload_id,
            'startedAt': now,
            'status': 'RUNNING',
            'filesProcessed': file_names,
            'triggeredBy': user_email,
            'dataAsOfDate': data_as_of_date
        }
        s3_client.put_object(
            Bucket=BUCKET,
            Key=f'{archive_prefix}metadata.json',
            Body=json.dumps(metadata, indent=2),
            ContentType='application/json'
        )

        # 6. Clean up pending folder
        for file_obj in pending_files:
            s3_client.delete_object(Bucket=BUCKET, Key=file_obj['Key'])
            print(f"Deleted pending file: {file_obj['Key']}")

        # Delete pending record from DynamoDB
        try:
            table.delete_item(Key={'PK': f'UPLOAD#{upload_id}', 'SK': 'PENDING'})
        except Exception:
            pass

        print(f"Pipeline triggered: executionId={execution_id}, executionArn={execution_arn}")

        return cors_response(200, {
            'executionId': execution_id,
            'executionArn': execution_arn or 'starting',
            'dataAsOfDate': data_as_of_date,
            'manifest': manifest_data,  # Return generated manifest for UI display
            'status': 'RUNNING'
        })

    except Exception as e:
        print(f"Error triggering pipeline: {e}")
        import traceback
        traceback.print_exc()
        return cors_response(500, {'error': 'Internal server error', 'message': str(e)})


# =============================================================================
# ENDPOINT 3: GET /data-refresh/status/{executionId}
# =============================================================================

def handle_sscn_status(event, execution_id):
    """
    Poll status of a Security Scanner upload triggered via DataRefresh.
    The SSCN processor Lambda runs independently (S3 event). We determine
    completion by checking whether factor_metadata.json was written after
    the trigger time.
    """
    is_valid, _ = validate_user_type(event)
    if not is_valid:
        return cors_response(403, {'error': 'Forbidden - requires Dev userType'})

    try:
        db_response = table.get_item(Key={'PK': 'SSCN_EXECUTION', 'SK': execution_id})
        db_item = db_response.get('Item')

        if not db_item:
            return cors_response(404, {'error': f'SSCN execution {execution_id} not found'})

        started_at = db_item.get('startedAt', '')
        status = db_item.get('status', 'RUNNING')
        completed_at = db_item.get('completedAt')

        # Determine completion by checking S3 artifact timestamp
        if status == 'RUNNING':
            try:
                factor_meta_key = f'{SSCN_S3_PREFIX}/factor_metadata.json'
                head = s3_client.head_object(Bucket=BUCKET, Key=factor_meta_key)
                last_modified = head['LastModified']
                trigger_dt = datetime.fromisoformat(started_at.replace('Z', '+00:00'))
                if last_modified.replace(tzinfo=timezone.utc) > trigger_dt:
                    status = 'SUCCEEDED'
                    completed_at = last_modified.isoformat()
                    table.update_item(
                        Key={'PK': 'SSCN_EXECUTION', 'SK': execution_id},
                        UpdateExpression='SET #status = :status, completedAt = :completedAt',
                        ExpressionAttributeNames={'#status': 'status'},
                        ExpressionAttributeValues={':status': 'SUCCEEDED', ':completedAt': completed_at}
                    )
                    print(f"SSCN {execution_id}: SUCCEEDED (factor_metadata written {last_modified})")
            except ClientError:
                pass  # artifact not yet available — still RUNNING

        current_step = None
        if status == 'RUNNING':
            current_step = 'Processing FactSet file'
        elif status == 'SUCCEEDED':
            current_step = 'Complete'

        return cors_response(200, {
            'executionId': execution_id,
            'executionArn': 'sscn',
            'status': status,
            'startedAt': started_at,
            'completedAt': completed_at,
            'currentStep': current_step,
            'steps': [],
            'error': None,
            'type': 'sscn',
        })

    except Exception as e:
        print(f"Error in handle_sscn_status: {e}")
        return cors_response(500, {'error': 'Internal server error'})


# Map Step Functions state names to user-friendly labels
STATE_LABELS = {
    'ReadManifest': 'Validating Files',
    'MoveToProcessed': 'Moving to Processed',
    'GetPriorMetadata': 'Getting Prior Metadata',
    'GenerateLatest': 'Generating Latest Snapshot',
    'CheckNeedsDynamoDBFirst': 'Checking DynamoDB Requirements',
    'IngestDynamoDB': 'Ingesting to DynamoDB',
    'ProcessFileTypes': 'Processing File Types',
    'CheckDataPKL': 'Checking Data PKL',
    'ProcessDataPKLOnly': 'Processing Data PKL',
    'GenerateValuation': 'Generating Valuation',
    'GenerateRiskPremium': 'Generating Risk Premium',
    'GenerateCorrelation': 'Generating Correlations',
    'GenerateMacro': 'Generating Macro Data',
    'GenerateMacroTimeseries': 'Generating Macro Timeseries',
    'CheckModelPKL': 'Checking Model PKL',
    'ProcessModelPKLOnly': 'Processing Model PKL',
    'GenerateFactorTilts': 'Generating Factor Tilts',
    'GenerateETFReturns': 'Generating ETF Returns',
    'GenerateAllocationSummary': 'Generating Allocation Summary',
    'CheckBothPKLs': 'Checking Both PKLs',
    'ProcessBothPKLs': 'Processing Both PKLs',
    'GenerateBenchmarkReturns': 'Generating Benchmark Returns',
    'GenerateModelPortfolioBenchmarks': 'Generating Model Portfolio Benchmarks',
    'GeneratePositioning': 'Generating Positioning',
    'CheckCMAExcel': 'Checking CMA Excel',
    'GenerateCMA': 'Generating CMA',
    'CheckPeerExcel': 'Checking Peer Excel',
    'GeneratePeerPerformance': 'Generating Peer Performance',
    'CheckAttributionExcel': 'Checking Attribution Excel',
    'GenerateHoldingsAttribution': 'Generating Holdings Attribution',
    'CheckNeedsPortalData': 'Checking Portal Data Requirements',
    'GeneratePortalDataParallel': 'Generating Portal Data',
    'GenerateMarketOverviewTiered': 'Generating Market Overview',
    'GenerateRSITiered': 'Generating RSI Data',
    'GenerateMarketRegime': 'Classifying Market Regime',
    'GenerateManifest': 'Generating Manifest',
    'CleanupUploads': 'Cleaning Up',
    'PipelineSuccess': 'Complete',
    'PipelineFailed': 'Failed'
}


def handle_status(event, execution_id):
    """
    Get pipeline execution status.

    Response:
    {
        "executionId": "exec-abc123",
        "status": "RUNNING",
        "startedAt": "2025-01-15T10:30:00Z",
        "completedAt": null,
        "currentStep": "IngestDynamoDB",
        "steps": [...],
        "error": null
    }
    """
    # SSCN executions use a separate status handler
    if execution_id.startswith('sscn-'):
        return handle_sscn_status(event, execution_id)

    # Validate user
    is_valid, _ = validate_user_type(event)
    if not is_valid:
        return cors_response(403, {'error': 'Forbidden - requires Dev userType'})

    try:
        # Get execution record from DynamoDB
        db_response = table.get_item(Key={'PK': 'EXECUTION', 'SK': execution_id})
        db_item = db_response.get('Item')

        if not db_item:
            return cors_response(404, {'error': f'Execution {execution_id} not found'})

        execution_arn = db_item.get('executionArn')

        # If execution ARN is pending, try to find it from recent executions
        if execution_arn == 'pending':
            print(f"Execution ARN is pending, searching for recent execution...")
            started_at_str = db_item.get('startedAt', '')

            # List recent executions and find one that started around the same time
            executions = sfn_client.list_executions(
                stateMachineArn=STATE_MACHINE_ARN,
                maxResults=10
            )

            for exec_info in executions.get('executions', []):
                exec_start = exec_info.get('startDate')
                if exec_start and started_at_str:
                    # Check if execution started within 60 seconds of our record
                    db_start = datetime.fromisoformat(started_at_str.replace('Z', '+00:00'))
                    exec_start_utc = exec_start.replace(tzinfo=timezone.utc)
                    time_diff = abs((exec_start_utc - db_start).total_seconds())

                    if time_diff < 60:
                        execution_arn = exec_info['executionArn']
                        print(f"Found matching execution: {execution_arn}")
                        # Update DynamoDB with the found ARN
                        table.update_item(
                            Key={'PK': 'EXECUTION', 'SK': execution_id},
                            UpdateExpression='SET executionArn = :arn',
                            ExpressionAttributeValues={':arn': execution_arn}
                        )
                        break

        # If we have an execution ARN, get live status from Step Functions
        if execution_arn and execution_arn != 'pending':
            try:
                sfn_response = sfn_client.describe_execution(executionArn=execution_arn)

                status = sfn_response['status']  # RUNNING, SUCCEEDED, FAILED, TIMED_OUT, ABORTED
                started_at = sfn_response['startDate'].isoformat() if sfn_response.get('startDate') else None
                stopped_at = sfn_response.get('stopDate')
                completed_at = stopped_at.isoformat() if stopped_at else None

                # Get execution history to determine current step
                history_response = sfn_client.get_execution_history(
                    executionArn=execution_arn,
                    maxResults=100,
                    reverseOrder=True
                )

                # Parse history to build step status
                steps = []
                current_step = None
                error_info = None

                # Track state entry/exit times
                state_times = {}

                for event_item in reversed(history_response.get('events', [])):
                    event_type = event_item['type']
                    timestamp = event_item['timestamp'].isoformat()

                    if event_type == 'TaskStateEntered':
                        state_name = event_item.get('stateEnteredEventDetails', {}).get('name', '')
                        state_times[state_name] = {'startedAt': timestamp}
                        current_step = state_name
                    elif event_type == 'TaskStateExited':
                        state_name = event_item.get('stateExitedEventDetails', {}).get('name', '')
                        if state_name in state_times:
                            state_times[state_name]['completedAt'] = timestamp
                            state_times[state_name]['status'] = 'SUCCEEDED'
                    elif event_type == 'TaskFailed':
                        if current_step and current_step in state_times:
                            state_times[current_step]['status'] = 'FAILED'
                            error_info = event_item.get('taskFailedEventDetails', {})
                    elif event_type == 'ExecutionFailed':
                        error_info = event_item.get('executionFailedEventDetails', {})

                # Build steps array
                for state_name, times in state_times.items():
                    label = STATE_LABELS.get(state_name, state_name)
                    step_status = times.get('status', 'RUNNING' if state_name == current_step else 'PENDING')

                    steps.append({
                        'name': state_name,
                        'label': label,
                        'status': step_status,
                        'startedAt': times.get('startedAt'),
                        'completedAt': times.get('completedAt')
                    })

                # Update DynamoDB if status changed
                if status != db_item.get('status'):
                    update_expr = 'SET #status = :status'
                    expr_values = {':status': status}

                    if completed_at:
                        update_expr += ', completedAt = :completedAt'
                        expr_values[':completedAt'] = completed_at

                        # Calculate duration
                        if started_at:
                            start_dt = datetime.fromisoformat(started_at.replace('Z', '+00:00'))
                            end_dt = datetime.fromisoformat(completed_at.replace('Z', '+00:00'))
                            duration = int((end_dt - start_dt).total_seconds())
                            update_expr += ', #duration = :duration'
                            expr_values[':duration'] = duration

                    table.update_item(
                        Key={'PK': 'EXECUTION', 'SK': execution_id},
                        UpdateExpression=update_expr,
                        ExpressionAttributeNames={'#status': 'status', '#duration': 'duration'} if 'duration' in update_expr else {'#status': 'status'},
                        ExpressionAttributeValues=expr_values
                    )

                return cors_response(200, {
                    'executionId': execution_id,
                    'executionArn': execution_arn,
                    'status': status,
                    'startedAt': started_at,
                    'completedAt': completed_at,
                    'currentStep': STATE_LABELS.get(current_step, current_step) if current_step else None,
                    'steps': steps,
                    'error': error_info
                })

            except sfn_client.exceptions.ExecutionDoesNotExist:
                return cors_response(404, {'error': f'Step Functions execution not found: {execution_arn}'})

        # Return cached status from DynamoDB
        return cors_response(200, {
            'executionId': execution_id,
            'executionArn': execution_arn,
            'status': db_item.get('status', 'UNKNOWN'),
            'startedAt': db_item.get('startedAt'),
            'completedAt': db_item.get('completedAt'),
            'currentStep': None,
            'steps': [],
            'error': None
        })

    except Exception as e:
        print(f"Error getting status: {e}")
        import traceback
        traceback.print_exc()
        return cors_response(500, {'error': 'Internal server error', 'message': str(e)})


# =============================================================================
# ENDPOINT 4: GET /data-refresh/history
# =============================================================================

def handle_history(event):
    """
    List past executions with metadata.

    Query params:
        limit: Max number of results (default 20)

    Response:
    {
        "executions": [
            {
                "executionId": "exec-abc123",
                "status": "SUCCEEDED",
                "startedAt": "2025-01-15T10:30:00Z",
                "completedAt": "2025-01-15T10:35:00Z",
                "filesProcessed": ["data.pkl", "model.pkl"],
                "duration": 312,
                "triggeredBy": "yang@opalcapital.com",
                "canRollback": true
            }
        ]
    }
    """
    # Validate user
    is_valid, _ = validate_user_type(event)
    if not is_valid:
        return cors_response(403, {'error': 'Forbidden - requires Dev userType'})

    try:
        query_params = event.get('queryStringParameters') or {}
        limit = int(query_params.get('limit', 20))

        # Query all executions from DynamoDB
        response = table.query(
            KeyConditionExpression=Key('PK').eq('EXECUTION'),
            ScanIndexForward=False,  # Newest first
            Limit=limit
        )

        executions = []
        for item in response.get('Items', []):
            execution_arn = item.get('executionArn')
            status = item.get('status')
            completed_at = item.get('completedAt')
            duration = item.get('duration')
            started_at = item.get('startedAt')
            execution_id = item.get('executionId')

            # Fetch live status from Step Functions if we have a valid ARN
            # and status isn't already terminal
            TERMINAL_STATES = ['SUCCEEDED', 'FAILED', 'TIMED_OUT', 'ABORTED']

            # Try to discover ARN if it's "pending"
            if execution_arn == 'pending' and started_at:
                try:
                    recent_executions = sfn_client.list_executions(
                        stateMachineArn=STATE_MACHINE_ARN,
                        maxResults=20
                    )
                    db_start = datetime.fromisoformat(started_at.replace('Z', '+00:00'))

                    for exec_info in recent_executions.get('executions', []):
                        exec_start = exec_info.get('startDate')
                        if exec_start:
                            exec_start_utc = exec_start.replace(tzinfo=timezone.utc)
                            time_diff = abs((exec_start_utc - db_start).total_seconds())
                            if time_diff < 120:  # Within 2 minutes
                                execution_arn = exec_info['executionArn']
                                print(f"Discovered ARN for {execution_id}: {execution_arn}")
                                table.update_item(
                                    Key={'PK': 'EXECUTION', 'SK': execution_id},
                                    UpdateExpression='SET executionArn = :arn',
                                    ExpressionAttributeValues={':arn': execution_arn}
                                )
                                break
                except Exception as e:
                    print(f"Error discovering ARN for {execution_id}: {e}")

            if execution_arn and execution_arn != 'pending' and status not in TERMINAL_STATES:
                try:
                    exec_response = sfn_client.describe_execution(executionArn=execution_arn)
                    live_status = exec_response.get('status', status)

                    if live_status != status:
                        status = live_status

                        # Get completion time if terminal
                        if live_status in TERMINAL_STATES:
                            stop_date = exec_response.get('stopDate')
                            if stop_date:
                                completed_at = stop_date.isoformat()

                                # Calculate duration
                                if started_at:
                                    start_dt = datetime.fromisoformat(started_at.replace('Z', '+00:00'))
                                    duration = int((stop_date.replace(tzinfo=timezone.utc) - start_dt).total_seconds())

                        # Update DynamoDB with live status
                        update_expr = 'SET #status = :status'
                        expr_values = {':status': status}
                        expr_names = {'#status': 'status'}

                        if completed_at:
                            update_expr += ', completedAt = :completedAt'
                            expr_values[':completedAt'] = completed_at
                        if duration:
                            update_expr += ', #duration = :duration'
                            expr_values[':duration'] = duration
                            expr_names['#duration'] = 'duration'

                        table.update_item(
                            Key={'PK': 'EXECUTION', 'SK': execution_id},
                            UpdateExpression=update_expr,
                            ExpressionAttributeNames=expr_names,
                            ExpressionAttributeValues=expr_values
                        )
                        print(f"Updated {execution_id} status: {item.get('status')} -> {status}")

                except Exception as e:
                    print(f"Error fetching live status for {execution_arn}: {e}")

            executions.append({
                'executionId': execution_id,
                'executionArn': execution_arn,
                'status': status,
                'startedAt': started_at,
                'completedAt': completed_at,
                'filesProcessed': item.get('filesProcessed', []),
                'duration': duration,
                'triggeredBy': item.get('triggeredBy'),
                'canRollback': item.get('canRollback', False),
                'isRollback': item.get('isRollback', False),
                'rollbackFrom': item.get('rollbackFrom'),
                'dataAsOfDate': item.get('dataAsOfDate', '')
            })

        # Also include SSCN executions (separate DynamoDB PK)
        try:
            sscn_response = table.query(
                KeyConditionExpression=Key('PK').eq('SSCN_EXECUTION'),
                ScanIndexForward=False,
                Limit=limit
            )
            for item in sscn_response.get('Items', []):
                executions.append({
                    'executionId': item.get('executionId'),
                    'executionArn': 'sscn',
                    'status': item.get('status', 'UNKNOWN'),
                    'startedAt': item.get('startedAt'),
                    'completedAt': item.get('completedAt'),
                    'filesProcessed': item.get('filesProcessed', []),
                    'duration': None,
                    'triggeredBy': item.get('triggeredBy'),
                    'canRollback': False,
                    'isRollback': False,
                    'rollbackFrom': None,
                    'dataAsOfDate': item.get('dataAsOfDate', ''),
                    'type': 'sscn',
                })
        except Exception as e:
            print(f"Error fetching SSCN execution history: {e}")

        # Sort combined list by startedAt descending
        executions.sort(key=lambda x: x.get('startedAt') or '', reverse=True)
        executions = executions[:limit]

        return cors_response(200, {'executions': executions})

    except Exception as e:
        print(f"Error getting history: {e}")
        return cors_response(500, {'error': 'Internal server error', 'message': str(e)})


# =============================================================================
# ENDPOINT 5: POST /data-refresh/rollback
# =============================================================================

def handle_rollback(event):
    """
    Rollback to previous execution state.

    Two methods:
    1. Version-based (preferred): Restore exact S3 versions of JSON outputs
    2. Re-processing (fallback): Re-run pipeline with archived input files

    Request:
    {
        "executionId": "exec-older-123"
    }

    Response (version-based):
    {
        "method": "version-based",
        "executionId": "exec-older-123",
        "filesRestored": [...],
        "message": "Restored exact state from execution exec-older-123"
    }

    Response (re-processing):
    {
        "method": "re-processing",
        "newExecutionId": "exec-rollback-456",
        "status": "RUNNING",
        "message": "Rolling back to execution exec-older-123 (re-processing)"
    }
    """
    # Validate user
    is_valid, user_email = validate_user_type(event)
    if not is_valid:
        return cors_response(403, {'error': 'Forbidden - requires Dev userType'})

    try:
        # Parse request body
        body = json.loads(event.get('body', '{}'))
        source_execution_id = body.get('executionId')

        if not source_execution_id:
            return cors_response(400, {'error': 'executionId is required'})

        # Get source execution from DynamoDB
        db_response = table.get_item(Key={'PK': 'EXECUTION', 'SK': source_execution_id})
        source_item = db_response.get('Item')

        if not source_item:
            return cors_response(404, {'error': f'Execution {source_execution_id} not found'})

        if not source_item.get('canRollback'):
            return cors_response(400, {'error': f'Execution {source_execution_id} cannot be rolled back (archive not available)'})

        archive_path = source_item.get('archivePath')
        if not archive_path:
            return cors_response(400, {'error': 'Archive path not found for this execution'})

        # TRY VERSION-BASED ROLLBACK FIRST (exact restoration)
        outputs_manifest_key = f'{archive_path}outputs-manifest.json'

        try:
            print(f"Checking for outputs manifest: {outputs_manifest_key}")
            manifest_response = s3_client.get_object(Bucket=BUCKET, Key=outputs_manifest_key)
            outputs_manifest = json.loads(manifest_response['Body'].read())

            print(f"✓ Found outputs manifest - using version-based rollback")

            # Restore each JSON file to its exact previous version
            restored_files = []
            outputs = outputs_manifest.get('outputs', {})

            for json_key, version_info in outputs.items():
                version_id = version_info.get('versionId')

                if not version_id:
                    print(f"  ⚠ Warning: No version ID for {json_key}, skipping")
                    continue

                # Copy specific version to current location
                print(f"  Restoring {json_key} to version {version_id}")

                s3_client.copy_object(
                    Bucket=BUCKET,
                    CopySource={
                        'Bucket': BUCKET,
                        'Key': json_key,
                        'VersionId': version_id
                    },
                    Key=json_key,
                    MetadataDirective='REPLACE',
                    CacheControl='no-cache'
                )

                restored_files.append(json_key)

            print(f"✓ Restored {len(restored_files)} files to exact previous versions")

            # Invalidate CloudFront cache so users see restored data immediately
            cloudfront_invalidation_id = None
            try:
                print(f"Invalidating CloudFront cache for distribution {CLOUDFRONT_DIST_ID}")
                invalidation_response = cloudfront_client.create_invalidation(
                    DistributionId=CLOUDFRONT_DIST_ID,
                    InvalidationBatch={
                        'Paths': {
                            'Quantity': 1,
                            'Items': ['/api/public/*']
                        },
                        'CallerReference': f'rollback-{source_execution_id}-{int(datetime.now(timezone.utc).timestamp())}'
                    }
                )
                cloudfront_invalidation_id = invalidation_response['Invalidation']['Id']
                print(f"✓ CloudFront invalidation created: {cloudfront_invalidation_id}")
            except Exception as e:
                print(f"⚠ Warning: CloudFront invalidation failed: {e}")
                # Don't fail rollback if invalidation fails

            # Record rollback in DynamoDB
            now = datetime.now(timezone.utc).isoformat()
            rollback_record_id = f"rollback-{uuid.uuid4().hex[:12]}"

            table.put_item(Item={
                'PK': 'ROLLBACK',
                'SK': rollback_record_id,
                'rollbackId': rollback_record_id,
                'sourceExecutionId': source_execution_id,
                'method': 'version-based',
                'restoredAt': now,
                'restoredBy': user_email,
                'filesRestored': restored_files,
                'fileCount': len(restored_files),
                'dataAsOfDate': outputs_manifest.get('dataAsOfDate', ''),
                'cloudFrontInvalidation': cloudfront_invalidation_id
            })

            return cors_response(200, {
                'method': 'version-based',
                'executionId': source_execution_id,
                'filesRestored': restored_files,
                'fileCount': len(restored_files),
                'dataAsOfDate': outputs_manifest.get('dataAsOfDate'),
                'restoredAt': now,
                'cloudFrontInvalidation': cloudfront_invalidation_id,
                'message': f'Restored exact state from execution {source_execution_id}'
            })

        except s3_client.exceptions.NoSuchKey:
            print(f"⚠ No outputs manifest found - falling back to re-processing rollback")
            # Fall through to re-processing rollback below

        except Exception as e:
            print(f"⚠ Error in version-based rollback: {e}")
            import traceback
            traceback.print_exc()
            print("Falling back to re-processing rollback")
            # Fall through to re-processing rollback below

        # FALLBACK: RE-PROCESSING ROLLBACK (current method)

        # List files in archive
        response = s3_client.list_objects_v2(
            Bucket=BUCKET,
            Prefix=archive_path
        )

        archive_files = [f for f in response.get('Contents', []) if not f['Key'].endswith('metadata.json')]
        if not archive_files:
            return cors_response(400, {'error': 'No files found in archive'})

        # Generate new execution ID
        new_execution_id = f"exec-{uuid.uuid4().hex[:12]}"

        # Copy archived files to uploads/ folder
        file_names = []
        for file_obj in archive_files:
            source_key = file_obj['Key']
            filename = os.path.basename(source_key)
            dest_key = f'uploads/{filename}'

            s3_client.copy_object(
                Bucket=BUCKET,
                CopySource={'Bucket': BUCKET, 'Key': source_key},
                Key=dest_key
            )
            file_names.append(filename)
            print(f"Rollback copy: {source_key} -> {dest_key}")

        # Wait for pipeline to start
        import time
        time.sleep(2)

        # Get execution ARN
        executions = sfn_client.list_executions(
            stateMachineArn=STATE_MACHINE_ARN,
            statusFilter='RUNNING',
            maxResults=5
        )

        execution_arn = None
        for exec_info in executions.get('executions', []):
            execution_arn = exec_info['executionArn']
            break

        # Record new execution (preserve dataAsOfDate from source)
        now = datetime.now(timezone.utc).isoformat()
        table.put_item(Item={
            'PK': 'EXECUTION',
            'SK': new_execution_id,
            'executionId': new_execution_id,
            'executionArn': execution_arn or 'pending',
            'status': 'RUNNING',
            'startedAt': now,
            'filesProcessed': file_names,
            'triggeredBy': user_email,
            'isRollback': True,
            'rollbackFrom': source_execution_id,
            'archivePath': archive_path,  # Reuse same archive
            'canRollback': True,
            'dataAsOfDate': source_item.get('dataAsOfDate', '')
        })

        print(f"Re-processing rollback triggered: newExecutionId={new_execution_id}, from={source_execution_id}")

        return cors_response(200, {
            'method': 're-processing',
            'newExecutionId': new_execution_id,
            'executionArn': execution_arn or 'starting',
            'status': 'RUNNING',
            'message': f'Rolling back to execution {source_execution_id} (re-processing with current generator code)',
            'warning': 'Using re-processing method - outputs may differ if generator code changed'
        })

    except Exception as e:
        print(f"Error in rollback: {e}")
        import traceback
        traceback.print_exc()
        return cors_response(500, {'error': 'Internal server error', 'message': str(e)})


# =============================================================================
# ENDPOINT: POST /security-scanner/upload-url
# =============================================================================

def handle_sscn_upload_url(event):
    """
    Generate a presigned S3 PUT URL for uploading the monthly FactSet Excel.

    Request body:  { "asOf": "YYYY-MM-DD" or "YYYYMMDD" }
    Response body: { "uploadUrl": "...", "s3Key": "security_scanner/uploads/{asOf}/{filename}" }

    S3 key pattern: security_scanner/uploads/{asOf-dashes}/Screening_DIVZ_IDVZ_{asOf-nodashes}.xlsx
    Example:        security_scanner/uploads/2025-10-28/Screening_DIVZ_IDVZ_20251028.xlsx
    Expiry: 15 minutes (SSCN_PRESIGN_EXPIRY)
    Auth: same Dev-claim gate as all /api/scoped/* routes
    """
    is_valid, user_email = validate_user_type(event)
    if not is_valid:
        return cors_response(403, {'error': 'Forbidden - requires Dev userType'})

    try:
        body = json.loads(event.get('body', '{}'))
        as_of_raw = body.get('asOf', '').strip()

        if not as_of_raw:
            return cors_response(400, {'error': 'asOf is required'})

        # Normalize to YYYY-MM-DD (folder) and YYYYMMDD (filename)
        if len(as_of_raw) == 8 and as_of_raw.isdigit():
            as_of_folder = f"{as_of_raw[:4]}-{as_of_raw[4:6]}-{as_of_raw[6:]}"
            as_of_file = as_of_raw
        elif len(as_of_raw) == 10 and as_of_raw[4] == '-' and as_of_raw[7] == '-':
            as_of_folder = as_of_raw
            as_of_file = as_of_raw.replace('-', '')
        else:
            return cors_response(400, {
                'error': 'asOf must be YYYYMMDD or YYYY-MM-DD',
                'received': as_of_raw
            })

        s3_key = f"security_scanner/uploads/{as_of_folder}/Screening_DIVZ_IDVZ_{as_of_file}.xlsx"

        presigned_url = s3_client.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': BUCKET,
                'Key': s3_key,
                'ContentType': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            },
            ExpiresIn=SSCN_PRESIGN_EXPIRY
        )

        print(f"SSCN presign: user={user_email}, asOf={as_of_folder}, key={s3_key}")

        return cors_response(200, {
            'uploadUrl': presigned_url,
            's3Key': s3_key
        })

    except Exception as e:
        print(f"Error in handle_sscn_upload_url: {e}")
        return cors_response(500, {'error': 'Internal server error'})


# =============================================================================
# ENDPOINTS: GET /security-scanner/factors
#            GET /security-scanner/universe/{universeId}/data
#            GET /security-scanner/universe/{universeId}/scanner
# =============================================================================

def handle_sscn_factors(event):
    """
    Serve factor metadata from S3.
    S3 key: json/security_scanner/latest/factor_metadata.json
    Auth: Dev-gated (scoped route)
    """
    is_valid, user_email = validate_user_type(event)
    if not is_valid:
        return cors_response(403, {'error': 'Forbidden - requires Dev userType'})

    try:
        s3_key = f'{SSCN_S3_PREFIX}/factor_metadata.json'
        response = s3_client.get_object(Bucket=BUCKET, Key=s3_key)
        data = json.loads(response['Body'].read())
        print(f"SSCN factors: user={user_email}, key={s3_key}")
        return cors_response(200, data)
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchKey':
            return cors_response(404, {'error': 'Factor metadata not yet available. Upload a FactSet file first.'})
        print(f"Error in handle_sscn_factors: {e}")
        return cors_response(500, {'error': 'Internal server error'})
    except Exception as e:
        print(f"Error in handle_sscn_factors: {e}")
        return cors_response(500, {'error': 'Internal server error'})


def handle_sscn_universe_data(event, universe_id):
    """
    Serve universe security-level data from S3.
    S3 key: json/security_scanner/latest/universes/{universe_id}/universe_data.json
    Auth: Dev-gated (scoped route)
    """
    is_valid, user_email = validate_user_type(event)
    if not is_valid:
        return cors_response(403, {'error': 'Forbidden - requires Dev userType'})

    if universe_id not in SSCN_VALID_UNIVERSES:
        return cors_response(400, {
            'error': f'Invalid universeId: {universe_id}',
            'valid': sorted(SSCN_VALID_UNIVERSES)
        })

    try:
        s3_key = f'{SSCN_S3_PREFIX}/universes/{universe_id}/universe_data.json'
        response = s3_client.get_object(Bucket=BUCKET, Key=s3_key)
        data = json.loads(response['Body'].read())
        print(f"SSCN universe data: user={user_email}, universe={universe_id}, key={s3_key}")
        return cors_response(200, data)
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchKey':
            return cors_response(404, {'error': f'Universe data not yet available for {universe_id}. Upload a FactSet file first.'})
        print(f"Error in handle_sscn_universe_data: {e}")
        return cors_response(500, {'error': 'Internal server error'})
    except Exception as e:
        print(f"Error in handle_sscn_universe_data: {e}")
        return cors_response(500, {'error': 'Internal server error'})


def handle_sscn_universe_scanner(event, universe_id):
    """
    Serve universe scanner (percentile) data from S3.
    S3 key: json/security_scanner/latest/universes/{universe_id}/scanner_data.json
    Auth: Dev-gated (scoped route)
    """
    is_valid, user_email = validate_user_type(event)
    if not is_valid:
        return cors_response(403, {'error': 'Forbidden - requires Dev userType'})

    if universe_id not in SSCN_VALID_UNIVERSES:
        return cors_response(400, {
            'error': f'Invalid universeId: {universe_id}',
            'valid': sorted(SSCN_VALID_UNIVERSES)
        })

    try:
        s3_key = f'{SSCN_S3_PREFIX}/universes/{universe_id}/scanner_data.json'
        response = s3_client.get_object(Bucket=BUCKET, Key=s3_key)
        data = json.loads(response['Body'].read())
        print(f"SSCN scanner: user={user_email}, universe={universe_id}, key={s3_key}")
        return cors_response(200, data)
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchKey':
            return cors_response(404, {'error': f'Scanner data not yet available for {universe_id}. Upload a FactSet file first.'})
        print(f"Error in handle_sscn_universe_scanner: {e}")
        return cors_response(500, {'error': 'Internal server error'})
    except Exception as e:
        print(f"Error in handle_sscn_universe_scanner: {e}")
        return cors_response(500, {'error': 'Internal server error'})


# =============================================================================
# MAIN HANDLER
# =============================================================================

def lambda_handler(event, context):
    """Main Lambda handler - routes requests to appropriate function"""

    print(f"Event: {json.dumps(event)}")

    # Handle OPTIONS (CORS preflight)
    http_method = event.get('httpMethod', event.get('requestContext', {}).get('http', {}).get('method', 'GET'))
    if http_method == 'OPTIONS':
        return cors_response(200, {'message': 'OK'})

    # Extract path
    path = event.get('path', event.get('rawPath', ''))
    path_params = event.get('pathParameters') or {}

    # Normalize path (remove stage prefix)
    if path.startswith('/prod'):
        path = path[5:]
    if path.startswith('/api/scoped'):
        path = path[11:]
    elif path.startswith('/api/private'):
        path = path[12:]

    print(f"Routing: method={http_method}, path={path}")

    # Route to handlers

    # POST /data-refresh/upload-urls
    if http_method == 'POST' and path == '/data-refresh/upload-urls':
        return handle_upload_urls(event)

    # POST /data-refresh/trigger
    if http_method == 'POST' and path == '/data-refresh/trigger':
        return handle_trigger(event)

    # GET /data-refresh/status/{executionId}
    if http_method == 'GET' and path.startswith('/data-refresh/status/'):
        execution_id = path_params.get('executionId') or path.split('/data-refresh/status/')[-1]
        return handle_status(event, execution_id)

    # GET /data-refresh/history
    if http_method == 'GET' and path == '/data-refresh/history':
        return handle_history(event)

    # POST /data-refresh/rollback
    if http_method == 'POST' and path == '/data-refresh/rollback':
        return handle_rollback(event)

    # POST /security-scanner/upload-url
    if http_method == 'POST' and path == '/security-scanner/upload-url':
        return handle_sscn_upload_url(event)

    # GET /security-scanner/factors
    if http_method == 'GET' and path == '/security-scanner/factors':
        return handle_sscn_factors(event)

    # GET /security-scanner/universe/{universeId}/data
    if http_method == 'GET' and path.startswith('/security-scanner/universe/') and path.endswith('/data'):
        universe_id = path[len('/security-scanner/universe/'):-len('/data')]
        return handle_sscn_universe_data(event, universe_id)

    # GET /security-scanner/universe/{universeId}/scanner
    if http_method == 'GET' and path.startswith('/security-scanner/universe/') and path.endswith('/scanner'):
        universe_id = path[len('/security-scanner/universe/'):-len('/scanner')]
        return handle_sscn_universe_scanner(event, universe_id)

    # Unknown route
    return cors_response(404, {
        'error': 'Route not found',
        'path': path,
        'method': http_method,
        'available_routes': [
            'POST /data-refresh/upload-urls',
            'POST /data-refresh/trigger',
            'GET /data-refresh/status/{executionId}',
            'GET /data-refresh/history',
            'POST /data-refresh/rollback',
            'POST /security-scanner/upload-url',
            'GET /security-scanner/factors',
            'GET /security-scanner/universe/{universeId}/data',
            'GET /security-scanner/universe/{universeId}/scanner'
        ]
    })
