resource "aws_sqs_queue" "q" {
  name = "etfs-price-refresh-queue"
}
