terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket = "opal-313476888478-terraform-state"
    key    = "shared-infra/tfstate"
    region = "us-east-1"
  }
}

provider "aws" {
  region = "us-east-1"

  default_tags {
    tags = {
      Project     = "OpalPortal"
      ManagedBy   = "Terraform"
      Environment = "Production"
      System      = "SharedInfra"
    }
  }
}

locals {
  account_id = "313476888478"
  region     = "us-east-1"
}

# =============================================================================
# Lambda Layer Artifact Bucket
# =============================================================================
#
# Stores compiled Lambda Layer zips before they are published via
# aws_lambda_layer_version in each pipeline's Terraform module.
#
# Convention:
#   s3://opal-313476888478-lambda-layers/{layer-name}.zip
#
# Source manifests (requirements.txt) live in:
#   infra/aws/lambda/layers/{layer-name}/requirements.txt
#
# Never store layer zips in the Terraform state bucket
# (opal-313476888478-terraform-state). State bucket = Terraform state only.
# =============================================================================

resource "aws_s3_bucket" "lambda_layers" {
  bucket = "opal-${local.account_id}-lambda-layers"
}

resource "aws_s3_bucket_versioning" "lambda_layers" {
  bucket = aws_s3_bucket.lambda_layers.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "lambda_layers" {
  bucket = aws_s3_bucket.lambda_layers.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "lambda_layers" {
  bucket = aws_s3_bucket.lambda_layers.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# =============================================================================
# Lambda Function Artifact Bucket
# =============================================================================
#
# Stores compiled Lambda function zips before they are deployed via
# aws_lambda_function (s3_bucket/s3_key) in each pipeline's Terraform module.
# Replaces the archive_file inline-zip pattern — S3 is the artifact store,
# consistent with Lambda Layers and EC2 code deployment.
#
# Convention:
#   s3://opal-313476888478-lambda-artifacts/{pipeline}/{function-name}.zip
#
# The {pipeline} prefix matches the Terraform directory name exactly:
#   yang-pipeline, news-pipeline, bd-pipeline, market-overview, etc.
#
# S3 versioning provides full artifact history. Every upload is immutable.
# Uploading a new zip is the trigger for deployment visibility in terraform plan.
#
# Source manifests live in:
#   infra/aws/lambda/v2_portal/{pipeline_dir}/{function}/   (source code)
#   infra/aws/lambda/artifacts/{pipeline}/build-and-upload.sh  (build script)
#   infra/aws/lambda/ci/lambda-source-map.json  (artifact_s3_key + artifact_sha256)
#
# Never store function zips in the Terraform state bucket or the layer bucket.
# =============================================================================

resource "aws_s3_bucket" "lambda_artifacts" {
  bucket = "opal-${local.account_id}-lambda-artifacts"
}

resource "aws_s3_bucket_versioning" "lambda_artifacts" {
  bucket = aws_s3_bucket.lambda_artifacts.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "lambda_artifacts" {
  bucket = aws_s3_bucket.lambda_artifacts.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "lambda_artifacts" {
  bucket = aws_s3_bucket.lambda_artifacts.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# =============================================================================
# IAM: opal-portal-lambda-role — EC2 AMI Snapshot Permissions
# =============================================================================
#
# The shared opal-portal-lambda-role predates Terraform. Rather than importing
# the full role (which would risk breaking many consumers), we attach a scoped
# inline policy for the infrastructure-daily-snapshot Lambda's EC2 needs.
#
# Permissions: ec2:CreateImage, ec2:DescribeImages, ec2:CreateTags
# Scoped to account EC2 resources in us-east-1.
# =============================================================================

# =============================================================================
# DynamoDB: opal-partner-49financial — Partner Identity Table
# =============================================================================
#
# Per-partner identity bridge between portal users (opal-users-v2) and the
# BD gold layer advisor identity (advisorKey, advisorRole). The auth-handler
# Lambda reads this table at login time to inject advisor claims into the JWT.
#
# Schema:
#   PK: email (String) — joins to opal-users-v2
#   Attributes: advisorKey, advisorName, advisorRole, createdAt, createdBy
#   GSI: ByAdvisorRole (advisorRole) — admin enumeration of users by role
#
# Population: manual admin operation at onboarding. Table is created empty.
# PRD: docs/architecture/PARTNER_IDENTITY_TABLE.md
# =============================================================================

resource "aws_dynamodb_table" "opal_partner_49financial" {
  name         = "opal-partner-49financial"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "email"

  attribute {
    name = "email"
    type = "S"
  }

  attribute {
    name = "advisorRole"
    type = "S"
  }

  global_secondary_index {
    name            = "ByAdvisorRole"
    hash_key        = "advisorRole"
    projection_type = "ALL"
  }

  tags = {
    Project   = "ADVI"
    ManagedBy = "terraform"
    Partner   = "49financial"
  }
}

# =============================================================================
# IAM: opalinvest-auth-lambda-role — Partner Identity Read Permissions
# =============================================================================
#
# Grants the auth-handler Lambda (owned by DT, portal-auth module) read access
# to opal-partner-49financial. A role can have multiple inline policies with
# different names — this does NOT conflict with the base opalinvest-auth-permissions
# policy managed in portal-auth/iam.tf.
#
# Actions: GetItem (login lookup by email PK), Query (GSI admin enumeration)
# =============================================================================

resource "aws_iam_role_policy" "partner_identity_read" {
  name = "PartnerIdentityReadPermissions"
  role = "opalinvest-auth-lambda-role"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "AllowPartnerIdentityRead"
        Effect = "Allow"
        Action = [
          "dynamodb:GetItem",
          "dynamodb:Query"
        ]
        Resource = [
          aws_dynamodb_table.opal_partner_49financial.arn,
          "${aws_dynamodb_table.opal_partner_49financial.arn}/index/*"
        ]
      }
    ]
  })
}

# =============================================================================
# IAM: opal-portal-lambda-role — EC2 AMI Snapshot Permissions
# =============================================================================
#
# The shared opal-portal-lambda-role predates Terraform. Rather than importing
# the full role (which would risk breaking many consumers), we attach a scoped
# inline policy for the infrastructure-daily-snapshot Lambda's EC2 needs.
#
# Permissions: ec2:CreateImage, ec2:DescribeImages, ec2:CreateTags
# Scoped to account EC2 resources in us-east-1.
# =============================================================================

resource "aws_iam_role_policy" "portal_lambda_ec2_snapshot" {
  name = "EC2SnapshotPermissions"
  role = "opal-portal-lambda-role"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "AllowEC2ImageCreation"
        Effect = "Allow"
        Action = [
          "ec2:CreateImage",
          "ec2:DescribeImages",
          "ec2:CreateTags"
        ]
        Resource = [
          "arn:aws:ec2:${local.region}:${local.account_id}:instance/*",
          "arn:aws:ec2:${local.region}:${local.account_id}:image/*",
          "arn:aws:ec2:${local.region}::image/*",
          "arn:aws:ec2:${local.region}:${local.account_id}:snapshot/*"
        ]
      },
      {
        Sid      = "AllowDescribeImagesGlobal"
        Effect   = "Allow"
        Action   = ["ec2:DescribeImages"]
        Resource = "*"
      }
    ]
  })
}
