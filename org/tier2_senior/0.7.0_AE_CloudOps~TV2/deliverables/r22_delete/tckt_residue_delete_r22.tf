locals {
  residue = jsondecode(file("${path.module}/tckt_residue_delete_r22.manifest.json")).objects
  chunks  = { for i, c in chunklist(local.residue, 12) : tostring(i) => c }
}
resource "aws_iam_role" "tckt_residue_delete_r22" {
  for_each             = local.chunks
  name                 = "tckt-residue-delete-r22-${each.key}"
  max_session_duration = 3600
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{ Effect = "Allow", Action = "sts:AssumeRole",
    Principal = { AWS = "arn:aws:iam::313476888478:user/cloudops-dell2-agent-user" } }]
  })
}
resource "aws_iam_role_policy" "tckt_residue_delete_r22" {
  for_each = local.chunks
  name     = "tckt-residue-delete-r22-${each.key}"
  role     = aws_iam_role.tckt_residue_delete_r22[each.key].id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Action    = ["s3:DeleteObjectVersion"]
      Resource  = [for o in each.value : "arn:aws:s3:::${o.bucket}/${o.key}"]
      Condition = { StringEquals = { "s3:VersionId" = [for o in each.value : o.version_id] } }
    }]
  })
}
