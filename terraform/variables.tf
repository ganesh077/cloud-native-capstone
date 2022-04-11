variable "project_name" {
  description = "Name prefix for all resources"
  type        = string
  default     = "cloud-native-capstone"
}

variable "aws_region" {
  description = "AWS region to deploy the stack"
  type        = string
  default     = "us-east-1"
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidrs" {
  description = "Map of availability zone to CIDR blocks for the public subnets"
  type        = map(string)
  default = {
    "us-east-1a" = "10.0.1.0/24"
    "us-east-1b" = "10.0.2.0/24"
  }
}

variable "allowed_ingress_cidrs" {
  description = "List of CIDR blocks that can reach the load balancer"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

variable "container_port" {
  description = "Container port exposed via the load balancer"
  type        = number
  default     = 8080
}

variable "desired_count" {
  description = "Number of ECS tasks to run"
  type        = number
  default     = 1
}

variable "container_image_tag" {
  description = "Docker image tag to deploy"
  type        = string
  default     = "latest"
}

variable "container_cpu" {
  description = "CPU units for the Fargate task"
  type        = number
  default     = 512
}

variable "container_memory" {
  description = "Memory (MB) for the Fargate task"
  type        = number
  default     = 1024
}
