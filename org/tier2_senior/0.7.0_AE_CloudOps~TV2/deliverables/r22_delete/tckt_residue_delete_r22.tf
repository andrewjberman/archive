variable "residue_manifest_path" {
  type = string
}
locals {
  residue = jsondecode(file(var.residue_manifest_path)).objects
  chunks  = chunklist(local.residue, 12)
}
resource "aws_iam_role" "residue_delete_0" {
  name                 = "opal-ticket-residue-delete-0-role"
  max_session_duration = 3600
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{ Effect = "Allow", Action = "sts:AssumeRole",
                   Principal = { AWS = "arn:aws:iam::313476888478:user/cloudops-dell2-agent-user" } }]
  })
}
resource "aws_iam_role_policy" "residue_delete_0" {
  name = "opal-ticket-residue-delete-0-policy"
  role = aws_iam_role.residue_delete_0.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Action    = ["s3:DeleteObjectVersion"]
      Resource  = [for o in local.chunks[0] : "arn:aws:s3:::${o.bucket}/${o.key}"]
      Condition = { StringEquals = { "s3:VersionId" = [for o in local.chunks[0] : o.version_id] } }
    }]
  })
}
resource "aws_iam_role" "residue_delete_1" {
  name                 = "opal-ticket-residue-delete-1-role"
  max_session_duration = 3600
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{ Effect = "Allow", Action = "sts:AssumeRole",
                   Principal = { AWS = "arn:aws:iam::313476888478:user/cloudops-dell2-agent-user" } }]
  })
}
resource "aws_iam_role_policy" "residue_delete_1" {
  name = "opal-ticket-residue-delete-1-policy"
  role = aws_iam_role.residue_delete_1.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Action    = ["s3:DeleteObjectVersion"]
      Resource  = [for o in local.chunks[1] : "arn:aws:s3:::${o.bucket}/${o.key}"]
      Condition = { StringEquals = { "s3:VersionId" = [for o in local.chunks[1] : o.version_id] } }
    }]
  })
}
resource "aws_iam_role" "residue_delete_2" {
  name                 = "opal-ticket-residue-delete-2-role"
  max_session_duration = 3600
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{ Effect = "Allow", Action = "sts:AssumeRole",
                   Principal = { AWS = "arn:aws:iam::313476888478:user/cloudops-dell2-agent-user" } }]
  })
}
resource "aws_iam_role_policy" "residue_delete_2" {
  name = "opal-ticket-residue-delete-2-policy"
  role = aws_iam_role.residue_delete_2.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Action    = ["s3:DeleteObjectVersion"]
      Resource  = [for o in local.chunks[2] : "arn:aws:s3:::${o.bucket}/${o.key}"]
      Condition = { StringEquals = { "s3:VersionId" = [for o in local.chunks[2] : o.version_id] } }
    }]
  })
}
resource "aws_iam_role" "residue_delete_3" {
  name                 = "opal-ticket-residue-delete-3-role"
  max_session_duration = 3600
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{ Effect = "Allow", Action = "sts:AssumeRole",
                   Principal = { AWS = "arn:aws:iam::313476888478:user/cloudops-dell2-agent-user" } }]
  })
}
resource "aws_iam_role_policy" "residue_delete_3" {
  name = "opal-ticket-residue-delete-3-policy"
  role = aws_iam_role.residue_delete_3.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Action    = ["s3:DeleteObjectVersion"]
      Resource  = [for o in local.chunks[3] : "arn:aws:s3:::${o.bucket}/${o.key}"]
      Condition = { StringEquals = { "s3:VersionId" = [for o in local.chunks[3] : o.version_id] } }
    }]
  })
}
