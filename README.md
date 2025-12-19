# AWS Lambda CI/CD Template

A production-ready AWS Lambda function template with complete CI/CD pipeline using GitHub Actions, Docker, Terraform, and Codecov.

## 🚀 Features

- **Python 3.12** Lambda function with type hints
- **Poetry** for dependency management
- **Ruff** ultra-fast linting and formatting (replaces Black, isort, Flake8)
- **Docker** containerized Lambda deployment
- **Terraform** Infrastructure as Code (IaC)
- **GitHub Actions** CI/CD pipeline
- **Codecov** code coverage tracking
- **Pytest** with comprehensive unit tests and coverage
- **AWS ECR** for container registry
- **CloudWatch** logging and monitoring

## 📁 Project Structure

```
template-lambda/
├── .github/
│   └── workflows/
│       └── ci-cd.yml          # GitHub Actions CI/CD pipeline
├── src/
│   ├── __init__.py
│   └── lambda_handler.py      # Lambda function handler
├── tests/
│   ├── __init__.py
│   ├── conftest.py            # Pytest configuration
│   └── test_lambda_handler.py # Unit tests
├── terraform/
│   ├── main.tf                # Main Terraform configuration
│   ├── variables.tf           # Input variables
│   ├── outputs.tf             # Output values
│   ├── ecr.tf                 # ECR repository configuration
│   ├── lambda.tf              # Lambda function configuration
│   └── terraform.tfvars.example # Example variables file
├── Dockerfile                 # Docker image for Lambda
├── .dockerignore             # Docker ignore patterns
├── entrypoint.py             # Lambda entrypoint (delegates to handler)
├── pyproject.toml            # Poetry configuration
├── poetry.lock               # Poetry lock file
├── sonar-project.properties  # SonarQube configuration
├── .flake8                   # Flake8 linting configuration
├── Makefile                  # Convenience commands
└── README.md                 # This file
```

## 🛠️ Prerequisites

- **Python 3.12+**
- **Poetry** (for dependency management)
- **Docker** (for local testing and building)
- **Terraform** (v1.0+)
- **AWS CLI** configured with appropriate credentials
- **GitHub Account** with repository access
- **SonarQube** instance (or SonarCloud account)

## 📦 Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd template-lambda
```

### 2. Install dependencies

```bash
# Using Poetry
poetry install

# Or using Make
make install
```

### 3. Configure AWS credentials

```bash
aws configure
```

## 🧪 Local Development

### Run Lambda function locally

```bash
# Run the Lambda function with example test cases
python entrypoint.py

# Or using Poetry
poetry run python entrypoint.py
```

### Run tests

```bash
# Run all tests with coverage
make test

# Run tests with verbose output
make test-verbose

# Run specific test file
poetry run pytest tests/test_lambda_handler.py -v
```

### Code quality checks

```bash
# Run all linting checks
make lint

# Format code
make format
```

### Build and test Docker image locally

```bash
# Build Docker image
make docker-build

# Run container locally (in another terminal)
make docker-run

# Test the local container
make docker-test
```

## 🏗️ Infrastructure Setup

### 1. Configure Terraform variables

```bash
cd terraform
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your values
```

### 2. Initialize Terraform

```bash
make terraform-init
```

### 3. Plan infrastructure changes

```bash
make terraform-plan
```

### 4. Apply infrastructure

```bash
make terraform-apply
```

## 🔄 CI/CD Pipeline

The GitHub Actions workflow automatically:

1. **Code Quality & Testing**
   - Runs linting (Black, isort, Flake8)
   - Executes type checking (mypy)
   - Runs unit tests with coverage
   - Performs SonarQube analysis
   - Enforces quality gate

2. **Build & Push Docker Image**
   - Builds Docker image
   - Pushes to AWS ECR
   - Scans image with Trivy
   - Tags with branch and SHA

3. **Deploy Infrastructure**
   - Runs Terraform plan
   - Applies infrastructure changes
   - Updates Lambda function
   - Outputs deployment information

4. **Integration Tests**
   - Tests deployed Lambda function
   - Verifies functionality

### Required GitHub Secrets

Configure these secrets in your GitHub repository:

```
AWS_ACCESS_KEY_ID          # AWS access key
AWS_SECRET_ACCESS_KEY      # AWS secret key
SONAR_TOKEN                # SonarQube authentication token
SONAR_HOST_URL             # SonarQube server URL
```

## 🔧 Configuration

### Environment Variables

The Lambda function uses these environment variables:

- `ENVIRONMENT`: Deployment environment (dev/staging/prod)
- `LOG_LEVEL`: Logging level (INFO/DEBUG/WARNING/ERROR)

### Terraform Variables

Key variables in `terraform/variables.tf`:

- `aws_region`: AWS region for deployment
- `environment`: Environment name
- `lambda_function_name`: Name of Lambda function
- `lambda_memory_size`: Memory allocation (MB)
- `lambda_timeout`: Timeout duration (seconds)
- `ecr_repository_name`: ECR repository name

## 📊 Monitoring

### CloudWatch Logs

View Lambda logs:

```bash
aws logs tail /aws/lambda/example-lambda-function --follow
```

### CloudWatch Alarms

The template creates alarms for:
- Lambda function errors
- Lambda function duration (80% of timeout)

## 🧹 Cleanup

To destroy all AWS resources:

```bash
make terraform-destroy
```

## 📝 Usage Examples

### Invoke Lambda function

```bash
# Using AWS CLI
aws lambda invoke \
  --function-name example-lambda-function \
  --payload '{"body": "{\"name\": \"World\"}"}' \
  response.json

# View response
cat response.json
```

### Using Lambda Function URL

```bash
# Get the function URL from Terraform outputs
FUNCTION_URL=$(cd terraform && terraform output -raw lambda_function_url)

# Invoke via HTTP
curl -X POST $FUNCTION_URL \
  -H "Content-Type: application/json" \
  -d '{"name": "World"}'
```

## 🔒 Security Best Practices

1. **IAM Roles**: Lambda uses least-privilege IAM roles
2. **Encryption**: ECR images encrypted at rest
3. **Image Scanning**: Automatic vulnerability scanning on ECR push
4. **Secrets Management**: Use AWS Secrets Manager for sensitive data
5. **VPC**: Consider deploying Lambda in VPC for private resources
6. **CORS**: Configure appropriate CORS policies

## 🤝 Contributing

1. Create a feature branch
2. Make your changes
3. Run tests and linting: `make all`
4. Submit a pull request

## 📄 License

[Your License Here]

## 🆘 Troubleshooting

### Common Issues

**Issue**: Poetry installation fails
```bash
# Solution: Update Poetry
curl -sSL https://install.python-poetry.org | python3 -
```

**Issue**: Docker build fails
```bash
# Solution: Check Docker daemon is running
docker ps
```

**Issue**: Terraform apply fails
```bash
# Solution: Check AWS credentials
aws sts get-caller-identity
```

**Issue**: Lambda function timeout
```bash
# Solution: Increase timeout in terraform/variables.tf
variable "lambda_timeout" {
  default = 60  # Increase from 30
}
```

## 📚 Additional Resources

- [AWS Lambda Documentation](https://docs.aws.amazon.com/lambda/)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [Poetry Documentation](https://python-poetry.org/docs/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

## 📧 Support

For issues and questions, please open an issue in the GitHub repository.