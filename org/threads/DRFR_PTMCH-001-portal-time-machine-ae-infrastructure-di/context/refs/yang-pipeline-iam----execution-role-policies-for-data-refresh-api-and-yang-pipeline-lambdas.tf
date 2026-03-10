# =============================================================================
# IAM: Yang Pipeline Lambda Execution Role
# =============================================================================

resource "aws_iam_role" "lambda_role" {
  name = "yang-pipeline-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "AllowLambdaAssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })

  tags = {
    Name = "yang-pipeline-lambda-role"
  }
}

resource "aws_iam_role_policy" "lambda_permissions" {
  name = "yang-pipeline-lambda-permissions"
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "S3ReadWrite"
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:ListBucket",
          "s3:CopyObject"
        ]
        Resource = [
          "arn:aws:s3:::opal-data-portal-v2",
          "arn:aws:s3:::opal-data-portal-v2/*"
        ]
      },
      {
        Sid      = "S3DeleteForCleanupOnly"
        Effect   = "Allow"
        Action   = "s3:DeleteObject"
        Resource = "arn:aws:s3:::opal-data-portal-v2/uploads/*"
      },
      {
        Sid    = "DynamoDBAccess"
        Effect = "Allow"
        Action = [
          "dynamodb:PutItem",
          "dynamodb:BatchWriteItem",
          "dynamodb:Query",
          "dynamodb:Scan",
          "dynamodb:UpdateItem"
        ]
        Resource = "arn:aws:dynamodb:${local.region}:${local.account_id}:table/opal-portal-market-data"
      },
      {
        Sid    = "ETFClassificationsRead"
        Effect = "Allow"
        Action = [
          "dynamodb:GetItem",
          "dynamodb:Query"
        ]
        Resource = [
          "arn:aws:dynamodb:${local.region}:${local.account_id}:table/etf-classifications",
          "arn:aws:dynamodb:${local.region}:${local.account_id}:table/etf-classifications/index/*"
        ]
      },
      {
        Sid    = "InvokeLambdas"
        Effect = "Allow"
        Action = "lambda:InvokeFunction"
        Resource = [
          "arn:aws:lambda:${local.region}:${local.account_id}:function:yang-*",
          "arn:aws:lambda:${local.region}:${local.account_id}:function:opal-precompute-market-metrics"
        ]
      },
      {
        Sid    = "StartAndCheckStepFunctions"
        Effect = "Allow"
        Action = [
          "states:StartExecution",
          "states:ListExecutions",
          "states:DescribeExecution"
        ]
        Resource = [
          "arn:aws:states:${local.region}:${local.account_id}:stateMachine:YangDataPipeline",
          "arn:aws:states:${local.region}:${local.account_id}:execution:YangDataPipeline:*"
        ]
      },
      {
        Sid    = "CloudWatchLogs"
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:${local.region}:${local.account_id}:log-group:/aws/lambda/yang-*"
      },
      {
        Sid      = "GetOpalSecrets"
        Effect   = "Allow"
        Action   = "secretsmanager:GetSecretValue"
        Resource = "arn:aws:secretsmanager:us-east-2:${local.account_id}:secret:opal/*"
      },
      {
        Sid    = "CloudFrontInvalidation"
        Effect = "Allow"
        Action = "cloudfront:CreateInvalidation"
        Resource = [
          "arn:aws:cloudfront::${local.account_id}:distribution/E2LPCXXBLDGWXY",
          "arn:aws:cloudfront::${local.account_id}:distribution/EVTSA9VEHNZVH"
        ]
      }
    ]
  })
}

# =============================================================================
# IAM: Yang Pipeline Step Functions Execution Role
# =============================================================================

resource "aws_iam_role" "sfn_role" {
  name = "yang-pipeline-sfn-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "states.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })

  tags = {
    Name = "yang-pipeline-sfn-role"
  }
}

resource "aws_iam_role_policy" "sfn_permissions" {
  name = "yang-pipeline-sfn-permissions"
  role = aws_iam_role.sfn_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "InvokeLambdas"
        Effect = "Allow"
        Action = ["lambda:InvokeFunction"]
        Resource = [
          "arn:aws:lambda:${local.region}:${local.account_id}:function:yang-*",
          "arn:aws:lambda:${local.region}:${local.account_id}:function:opal-precompute-market-metrics",
          "arn:aws:lambda:${local.region}:${local.account_id}:function:opal-market-overview-tiered-generator",
          "arn:aws:lambda:${local.region}:${local.account_id}:function:opal-market-rsi-tiered-generator",
          "arn:aws:lambda:${local.region}:${local.account_id}:function:opal-market-regime-classifier"
        ]
      },
      {
        Sid    = "CloudWatchLogs"
        Effect = "Allow"
        Action = [
          "logs:CreateLogDelivery",
          "logs:GetLogDelivery",
          "logs:UpdateLogDelivery",
          "logs:DeleteLogDelivery",
          "logs:ListLogDeliveries",
          "logs:PutResourcePolicy",
          "logs:DescribeResourcePolicies",
          "logs:DescribeLogGroups"
        ]
        Resource = "*"
      },
      {
        Sid    = "XRayTracing"
        Effect = "Allow"
        Action = [
          "xray:PutTraceSegments",
          "xray:PutTelemetryRecords",
          "xray:GetSamplingRules",
          "xray:GetSamplingTargets"
        ]
        Resource = "*"
      }
    ]
  })
}
