# Yang Pipeline — Terraform Module
#
# Manages: S3 trigger → Step Functions → 25+ Lambdas
# Pattern: Canonical 7-file split (lambdas, iam, stepfunctions, triggers, outputs)
# No EC2 or EventBridge schedule — pipeline triggered by S3 upload
#
# Resources imported from existing AWS infrastructure.
# Run IMPORT_COMMANDS.sh after terraform init to import existing resources.

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
    key    = "yang-pipeline/tfstate"
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
      System      = "YangPipeline"
    }
  }
}

locals {
  account_id      = "313476888478"
  region          = "us-east-1"
  lambda_role_arn = "arn:aws:iam::${local.account_id}:role/yang-pipeline-lambda-role"

  # Shared layers
  pandas_layer   = "arn:aws:lambda:${local.region}:${local.account_id}:layer:pandas-pyarrow-layer:1"
  openpyxl_layer = "arn:aws:lambda:${local.region}:${local.account_id}:layer:openpyxl-layer:1"
  aws_pandas_312 = "arn:aws:lambda:${local.region}:336392948345:layer:AWSSDKPandas-Python312:16"
}
