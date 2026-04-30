# =============================================================================
# Inf Pipeline -- inf-bronze-runner EC2 (ADVI_INFSHIP.B1)
#
# Single low-volume EC2 (t3.small) that pulls all Inflection bronze dims
# sequentially from the Orion Connect API on a daily cron and lands them at
# s3://opal-data-inf/bronze/orion-api/{date}/{dim}.csv.
#
# Architecture: Path X (CTO-ratified). Single instance, sequential pulls,
# bounded parallelism 3-4 within orchestrator.py. Lean for Inflection volume
# (305 HH / 852 acct / $199M AUA) at $1-2/day vs $9-18/day per-domain mirror.
#
# Triggered by inf-bronze-trigger Lambda (sibling of inf-jwt-trigger). New
# EventBridge cron at 12:30 UTC fires the Lambda; Lambda writes mode marker
# + StartInstances; systemd boot dispatch on this EC2 invokes orchestrator.py
# and self-shutdowns.
#
# IAM: NO lambda:InvokeFunction (per B1 TO §IAM constraint). Silver chain
# Lambda (B2, AE 0.6.1~B) fires on EventBridge S3 ObjectCreated rule
# watching s3://opal-data-inf/bronze/orion-api/*/_BRONZE_COMPLETE.json
# sentinel which orchestrator.py writes as final step.
# =============================================================================

resource "aws_security_group" "inf_bronze_runner" {
  name        = "inf-bronze-runner-sg"
  description = "Security group for inf-bronze-runner EC2 (Orion Connect API pulls)"
  vpc_id      = "vpc-0cc0c6a75e54605e3"

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow all outbound (S3, SSM, CloudWatch, Orion HTTPS)"
  }

  tags = {
    Name   = "inf-bronze-runner-sg"
    System = "InflectionPipeline"
  }
}

resource "aws_iam_role" "inf_bronze_runner" {
  name = "inf-bronze-runner-ec2-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "ec2.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })

  tags = {
    Name   = "inf-bronze-runner-ec2-role"
    System = "InflectionPipeline"
  }
}

resource "aws_iam_instance_profile" "inf_bronze_runner" {
  name = "inf-bronze-runner-profile"
  role = aws_iam_role.inf_bronze_runner.name
}

resource "aws_iam_role_policy" "inf_bronze_runner_s3" {
  name = "s3-scoped-inf"
  role = aws_iam_role.inf_bronze_runner.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid      = "ReadJwt"
        Effect   = "Allow"
        Action   = ["s3:GetObject", "s3:HeadObject"]
        Resource = [
          "arn:aws:s3:::opal-data-inf/orion/jwt/*",
          "arn:aws:s3:::opal-data-inf/orion/bronze-trigger-mode.json",
        ]
      },
      {
        Sid      = "ReadCode"
        Effect   = "Allow"
        Action   = ["s3:GetObject", "s3:ListBucket"]
        Resource = [
          "arn:aws:s3:::opal-data-inf",
          "arn:aws:s3:::opal-data-inf/code/bronze-runner/*",
          "arn:aws:s3:::opal-data-inf/code/bronze/*",
        ]
      },
      {
        Sid      = "WriteBronze"
        Effect   = "Allow"
        Action   = ["s3:GetObject", "s3:PutObject", "s3:HeadObject", "s3:DeleteObject"]
        Resource = [
          "arn:aws:s3:::opal-data-inf/bronze/orion-api/*",
          "arn:aws:s3:::opal-data-inf/bronze/orion-api-v2/*",
          "arn:aws:s3:::opal-data-inf/bronze/logs/inf-bronze-runner/*",
        ]
      },
    ]
  })
}

resource "aws_iam_role_policy" "inf_bronze_runner_cw_logs" {
  name = "cloudwatch-logs"
  role = aws_iam_role.inf_bronze_runner.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents",
      ]
      Resource = "arn:aws:logs:${local.region}:${local.account_id}:log-group:/aws/ec2/inf-bronze-runner*"
    }]
  })
}

resource "aws_iam_role_policy" "inf_bronze_runner_cw_metrics" {
  name = "cloudwatch-put-metric"
  role = aws_iam_role.inf_bronze_runner.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Sid      = "PutInfPipelineMetrics"
      Effect   = "Allow"
      Action   = ["cloudwatch:PutMetricData"]
      Resource = "*"
      Condition = {
        StringEquals = {
          "cloudwatch:namespace" = "InfPipeline"
        }
      }
    }]
  })
}

resource "aws_iam_role_policy" "inf_bronze_runner_sns" {
  name = "sns-otp-alert"
  role = aws_iam_role.inf_bronze_runner.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Sid      = "BronzeChainFailureAlert"
      Effect   = "Allow"
      Action   = "sns:Publish"
      Resource = aws_sns_topic.inf_otp_alert.arn
    }]
  })
}

resource "aws_iam_role_policy" "inf_bronze_runner_kms" {
  name = "kms-ebs-decrypt"
  role = aws_iam_role.inf_bronze_runner.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["kms:Decrypt", "kms:GenerateDataKey", "kms:DescribeKey"]
        Resource = aws_kms_key.inf_ebs.arn
      },
      {
        Sid    = "EBSAttachCreateGrant"
        Effect = "Allow"
        Action = "kms:CreateGrant"
        Resource = aws_kms_key.inf_ebs.arn
        Condition = {
          Bool = { "kms:GrantIsForAWSResource" = "true" }
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "inf_bronze_runner_ssm_core" {
  role       = aws_iam_role.inf_bronze_runner.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

resource "aws_instance" "inf_bronze_runner" {
  ami           = "ami-0c1e21d82fe9c9336" # Amazon Linux 2023 us-east-1 (same as inf-exporter / inf-gold-layer-runner)
  instance_type = "t3.small"               # 2 vCPU / 2 GB; lean per Inflection volume profile (CTO Path X)

  iam_instance_profile   = aws_iam_instance_profile.inf_bronze_runner.name
  subnet_id              = "subnet-023db8cbfd99ffff2"
  vpc_security_group_ids = [aws_security_group.inf_bronze_runner.id]

  instance_initiated_shutdown_behavior = "stop"

  root_block_device {
    volume_type           = "gp3"
    volume_size           = 30
    encrypted             = true
    kms_key_id            = aws_kms_key.inf_ebs.arn
    delete_on_termination = true
  }

  user_data = base64encode(file("${path.module}/../../ec2/inf-bronze-runner/user-data.sh"))

  tags = {
    Name        = "inf-bronze-runner"
    System      = "InflectionPipeline"
    Environment = "production"
    Purpose     = "BronzeApiPulls"
  }

  lifecycle {
    ignore_changes = [ami, user_data]
  }
}

# =============================================================================
# HISTBF.002b: PutMetricData — Inflection/HistBackfill/RateLimiter namespace
# =============================================================================
resource "aws_iam_role_policy" "inf_bronze_runner_cw_histbf" {
  name = "cloudwatch-histbf-namespace"
  role = aws_iam_role.inf_bronze_runner.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Sid      = "PutHistBfMetrics"
      Effect   = "Allow"
      Action   = ["cloudwatch:PutMetricData"]
      Resource = "*"
      Condition = {
        StringEquals = { "cloudwatch:namespace" = "Inflection/HistBackfill/RateLimiter" }
      }
    }]
  })
}

# =============================================================================
# JWTRES.001b: PutMetricData — Inflection/JwtResilience namespace
# =============================================================================
resource "aws_iam_role_policy" "inf_bronze_runner_cw_jwtres" {
  name = "cloudwatch-jwtres-namespace"
  role = aws_iam_role.inf_bronze_runner.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Sid      = "PutJwtResMetrics"
      Effect   = "Allow"
      Action   = ["cloudwatch:PutMetricData"]
      Resource = "*"
      Condition = {
        StringEquals = { "cloudwatch:namespace" = "Inflection/JwtResilience" }
      }
    }]
  })
}

# =============================================================================
# JWTRES.001b: SM GetSecretValue — orion/jwt/current (SM-first JWT load path)
# Previously only inf-gold-layer role had this grant. Bronze runner needs it
# for jwt_freshness.py SM-first load order per JWTRES.001 spec.
# =============================================================================
resource "aws_iam_role_policy" "inf_bronze_runner_sm" {
  name = "secrets-manager-orion-jwt-read"
  role = aws_iam_role.inf_bronze_runner.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Sid    = "OrionJwtRead"
      Effect = "Allow"
      Action = ["secretsmanager:GetSecretValue"]
      Resource = [
        "arn:aws:secretsmanager:us-east-1:${local.account_id}:secret:orion/jwt/current-*",
      ]
    }]
  })
}

# =============================================================================
# HISTBF.002b: S3 R/W — per-dim rate-limiter state files
# CTO amendment 2026-04-30: per-dim state (not shared global file)
# Path pattern: s3://opal-data-inf/orion/rate_limit_state_{dim_name}.json
# =============================================================================
resource "aws_iam_role_policy" "inf_bronze_runner_s3_rate_state" {
  name = "s3-rate-limit-state"
  role = aws_iam_role.inf_bronze_runner.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Sid      = "RateLimiterStateRW"
      Effect   = "Allow"
      Action   = ["s3:GetObject", "s3:PutObject", "s3:HeadObject"]
      Resource = "arn:aws:s3:::opal-data-inf/orion/rate_limit_state_*"
    }]
  })
}
