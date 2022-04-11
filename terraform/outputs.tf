output "alb_dns_name" {
  description = "Public DNS name for the load balancer"
  value       = aws_lb.this.dns_name
}

output "alb_url" {
  description = "Convenience HTTP URL"
  value       = "http://${aws_lb.this.dns_name}"
}

output "repository_url" {
  description = "ECR repository URL for container images"
  value       = aws_ecr_repository.app.repository_url
}
