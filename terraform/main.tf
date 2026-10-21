data "aws_instance" "fraudshield" {
  instance_id = var.instance_id
}
resource "local_file" "fraudshield_info" {
  filename = "${path.module}/fraudshield-info.txt"

  content = <<EOT
Project: FraudShield AI
Instance ID: ${data.aws_instance.fraudshield.id}
Instance Type: ${data.aws_instance.fraudshield.instance_type}
Region: us-east-2
Environment: Development
EOT
}