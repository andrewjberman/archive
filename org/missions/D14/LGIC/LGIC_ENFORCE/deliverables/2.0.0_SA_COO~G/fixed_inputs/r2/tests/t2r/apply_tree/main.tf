# LGIC_ENFORCE round-2 fixture (check_en_r2.py t2r-wired-*): the tree safe-apply is pointed at. Its one literal is
# CONFORMANT, so the pre-plan stage has nothing to say; the stub terraform's `show -json` output (a plans/*.json
# fixture) is what the plan-time limb decides on.
resource "aws_sqs_queue" "pub" {
  name = "mdpf-cot-publisher-queue"
}
