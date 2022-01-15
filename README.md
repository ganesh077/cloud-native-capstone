# Cloud-Native Application Deployment (Capstone)

End-to-end reference implementation for a data-driven Python service deployed on AWS with Docker, Terraform, and Jenkins-driven CI/CD.

## Architecture
- **Application** – Flask API that exposes health, analytics, and forecasting endpoints backed by a JSON data source.
- **Containerization** – Dockerfile builds, tests, and packages the service with Gunicorn for production-ready execution.
- **Infrastructure as Code** – Terraform provisions a VPC, public subnets, security groups, ECS Fargate service, ALB, CloudWatch log group, and an ECR repository.
- **CI/CD** – Jenkinsfile automates tests, image builds, pushes to ECR, and Terraform plan/apply steps for reproducible deployments.

## Requirements
- Python 3.11+
- Docker & Docker Compose
- Terraform 1.5+
- AWS CLI + credentials with permissions for ECS, ECR, IAM, EC2, CloudWatch, and ALB
- Jenkins agent with Docker, AWS CLI, Terraform, and the above tools installed

## Local Development
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
FLASK_APP=app.main:create_app flask run --port 8080
```
Endpoints:
- `GET /health`
- `GET /orders`
- `POST /orders`
- `GET /analytics/summary`
- `GET /analytics/regions`
- `GET /analytics/forecast`

## Run Tests
```bash
pytest
```

## Docker Workflow
```bash
# Build and run
docker build -t cloud-native-capstone:dev .
docker run -p 8080:8080 cloud-native-capstone:dev

# Or with Compose
docker compose up --build
```

## Terraform Deployment
1. Copy variables template and edit values:
   ```bash
   cp terraform/terraform.tfvars.example terraform/terraform.tfvars
   ```
2. (Recommended) Configure a remote backend such as S3 + DynamoDB for locking.
3. Ensure AWS credentials are exported (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and optionally `AWS_SESSION_TOKEN`).
4. Deploy:
   ```bash
   cd terraform
   terraform init
   terraform plan -out tfplan
   terraform apply tfplan
   ```
   Terraform outputs the Application Load Balancer URL and the ECR repository URI. Update `container_image_tag` when promoting a new image.

## Jenkins Pipeline
The included `Jenkinsfile` expects the following:
- Jenkins credentials/environment provide `AWS_ACCOUNT_ID`, `AWS_ACCESS_KEY_ID`, and `AWS_SECRET_ACCESS_KEY`.
- Docker daemon is available on the agent.
- Terraform state is persisted (e.g., via an S3 backend) to avoid drift.

Stages:
1. **Setup Python** – Creates a virtualenv and installs dependencies.
2. **Unit Tests** – Runs `pytest` and publishes JUnit results.
3. **Build Docker Image** – Builds the container tagged as `${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com/${PROJECT_NAME}:${BUILD_NUMBER}`.
4. **Push Image to ECR** – Creates the ECR repo if necessary, logs in, and pushes the new tag.
5. **Terraform Plan & Apply** – Applies infrastructure + ECS service updates with the freshly pushed tag.

## GitHub Repository
1. Create a new empty GitHub repository (e.g., `cloud-native-capstone`).
2. Initialize locally and push:
   ```bash
   git init
   git add .
   git commit -m "Initial cloud-native capstone"
   git branch -M main
   git remote add origin git@github.com:<your-username>/cloud-native-capstone.git
   git push -u origin main
   ```

## Next Steps
- Configure monitoring/alerting (e.g., CloudWatch alarms, X-Ray tracing).
- Extend Terraform with RDS, S3, or additional services required for your workload.
- Harden the CI/CD workflow with branch protection, linting, and multi-environment promotion (dev → staging → prod).
