output "instance_id" {
  description = "FraudShield EC2 instance ID"
  value       = data.aws_instance.fraudshield.id
}

output "instance_type" {
  description = "FraudShield EC2 instance type"
  value       = data.aws_instance.fraudshield.instance_type
}

output "public_ip" {
  description = "FraudShield EC2 public IP"
  value       = data.aws_instance.fraudshield.public_ip
}