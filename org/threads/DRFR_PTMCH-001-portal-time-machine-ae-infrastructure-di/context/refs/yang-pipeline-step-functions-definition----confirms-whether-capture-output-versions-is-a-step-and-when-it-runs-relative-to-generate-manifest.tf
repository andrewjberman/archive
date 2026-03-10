# =============================================================================
# Yang Pipeline — Step Functions State Machine
# =============================================================================
#
# Pipeline is triggered by S3 upload (not EventBridge schedule).
# Definition is co-located in this Terraform directory (yang-pipeline-definition.json)
# so changes to the JSON auto-deploy on terraform apply.

resource "aws_sfn_state_machine" "yang_pipeline" {
  name     = "YangDataPipeline"
  role_arn = aws_iam_role.sfn_role.arn

  definition = file("${path.module}/yang-pipeline-definition.json")

  tags = {
    Name = "YangDataPipeline"
  }
}
