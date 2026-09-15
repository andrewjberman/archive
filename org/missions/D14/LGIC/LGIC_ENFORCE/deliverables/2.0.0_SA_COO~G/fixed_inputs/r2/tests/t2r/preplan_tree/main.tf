# LGIC_ENFORCE round-2 fixture (check_en_r2.py t2r-deferred-line): one literal name and two names that exist only
# in a plan. The pre-plan limb grades the literal, never refuses it, and prints "2 expressions deferred to plan".
variable "firm" {
  type    = string
  default = "cot"
}

locals {
  queue = "mdpf-cot-local-queue"
}

resource "aws_sqs_queue" "literal" {
  name = "mdpf-cottonwood-publisher-queue"
}

resource "aws_sqs_queue" "template" {
  name = "mdpf-${var.firm}-template-queue"
}

resource "aws_sqs_queue" "reference" {
  name = local.queue
}
