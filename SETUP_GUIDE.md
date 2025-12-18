# Setup Guide for AWS Lambda CI/CD Template

## 📋 Quick Start Checklist

Follow these steps to get your Lambda function deployed:

### 1. Prerequisites Setup

- [ ] Install Python 3.12+
- [ ] Install Poetry: `curl -sSL https://install.python-poetry.org | python3 -`
- [ ] Install Docker Desktop
- [ ] Install Terraform: Download from [terraform.io](https://www.terraform.io/downloads)
- [ ] Install AWS CLI: `pip install awscli`
- [ ] Configure AWS credentials: `aws configure`

### 2. Local Development Setup

```bash
# Clone and navigate to the repository
cd template-lambda

# Install dependencies
poetry install

# Run Lambda function locally with example data
python entrypoint.py
# Or: make run-local

# Run tests to verify setup
poetry run pytest tests/ -v

# Run linting
poetry run black --check src/ tests/
poetry run flake8 src/ tests/
```

### 3. GitHub Repository Setup

#### A. Create GitHub Secrets

Navigate to your GitHub repository → Settings → Secrets and variables → Actions

Add the following secrets:

1. **AWS_ACCESS_KEY_ID**
   - Your AWS access key ID
   - Get from AWS IAM Console

2. **AWS_SECRET_ACCESS_KEY**
   - Your AWS secret access key
   - Get from AWS IAM Console

3. **SONAR_TOKEN**
   - SonarQube authentication token
   - Get from SonarQube/SonarCloud account

4. **SONAR_HOST_URL**
   - SonarQube server URL
   - Example: `https://sonarcloud.io` or your self-hosted URL

#### B. Configure SonarQube Project

1. Log in to SonarQube/SonarCloud
2. Create a new project
3. Generate an authentication token
4. Update `sonar-project.properties` with your project key

### 4. AWS Infrastructure Setup

#### A. Create ECR Repository (First Time Only)

```bash
# Navigate to terraform directory
cd terraform

# Copy example variables
cp terraform.tfvars.example terraform.tfvars

# Edit terraform.tfvars with your values
# Update: aws_region, environment, lambda_function_name, etc.

# Initialize Terraform
terraform init

# Review the plan
terraform plan

# Apply only ECR first (optional, or apply all at once)
terraform apply -target=aws_ecr_repository.lambda_repo
```

#### B. Build and Push Initial Docker Image

```bash
# Return to project root
cd ..

# Build Docker image
docker build -t lambda-function:latest .

# Tag for ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

docker tag lambda-function:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/lambda-function-repo:latest

# Push to ECR
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/lambda-function-repo:latest
```

#### C. Deploy Lambda Function

```bash
cd terraform

# Apply all infrastructure
terraform apply

# Note the outputs (Lambda URL, ARN, etc.)
terraform output
```

### 5. Verify Deployment

#### A. Test Lambda Function

```bash
# Get function URL
FUNCTION_URL=$(cd terraform && terraform output -raw lambda_function_url)

# Test the function
curl -X POST $FUNCTION_URL \
  -H "Content-Type: application/json" \
  -d '{"name": "Test User"}'

# Expected response:
# {"message": "Hello, Test User! Welcome to AWS Lambda.", "request_id": "..."}
```

#### B. Check CloudWatch Logs

```bash
# View logs
aws logs tail /aws/lambda/example-lambda-function --follow
```

### 6. CI/CD Pipeline Activation

Once you push to `main` or `develop` branch, the GitHub Actions workflow will automatically:

1. ✅ Run code quality checks and tests
2. ✅ Perform SonarQube analysis
3. ✅ Build and push Docker image to ECR
4. ✅ Deploy infrastructure with Terraform
5. ✅ Run integration tests

Monitor the workflow in GitHub Actions tab.

## 🔧 Configuration Details

### Terraform Variables

Edit `terraform/terraform.tfvars`:

```hcl
aws_region           = "us-east-1"        # Your AWS region
environment          = "dev"              # dev, staging, or prod
project_name         = "lambda-function"  # Your project name
lambda_function_name = "my-lambda"        # Your Lambda function name
lambda_memory_size   = 512                # Memory in MB
lambda_timeout       = 30                 # Timeout in seconds
ecr_repository_name  = "my-lambda-repo"   # ECR repository name
log_retention_days   = 7                  # CloudWatch log retention
```

### GitHub Actions Workflow

The workflow is triggered on:
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches

Customize in `.github/workflows/ci-cd.yml`

### SonarQube Configuration

Edit `sonar-project.properties`:

```properties
sonar.projectKey=your-project-key
sonar.projectName=Your Project Name
sonar.organization=your-org  # For SonarCloud
```

## 🧪 Testing Locally

### Run Unit Tests

```bash
# All tests with coverage
make test

# Specific test file
poetry run pytest tests/test_lambda_handler.py -v

# With coverage report
poetry run pytest --cov=src --cov-report=html
open htmlcov/index.html
```

### Test Docker Container Locally

```bash
# Build image
docker build -t lambda-function:latest .

# Run container
docker run -p 9000:8080 lambda-function:latest

# In another terminal, test it
curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" \
  -d '{"body": "{\"name\": \"Local Test\"}"}'
```

## 🔒 Security Checklist

- [ ] Use IAM roles with least privilege
- [ ] Enable ECR image scanning
- [ ] Store secrets in AWS Secrets Manager (not in code)
- [ ] Enable CloudWatch logging
- [ ] Configure VPC for Lambda (if accessing private resources)
- [ ] Set up CloudWatch alarms for errors
- [ ] Enable AWS CloudTrail for audit logs
- [ ] Use HTTPS for all endpoints
- [ ] Implement authentication for Lambda Function URLs

## 📊 Monitoring Setup

### CloudWatch Dashboards

Create a dashboard to monitor:
- Lambda invocations
- Error rates
- Duration
- Throttles
- Concurrent executions

### CloudWatch Alarms

The template creates alarms for:
- Lambda errors (threshold: 5 errors in 5 minutes)
- Lambda duration (threshold: 80% of timeout)

Add more alarms as needed in `terraform/lambda.tf`

## 🚨 Troubleshooting

### Common Issues and Solutions

#### 1. Terraform State Lock

**Error**: "Error acquiring the state lock"

**Solution**:
```bash
# If you're sure no other process is running
terraform force-unlock <lock-id>
```

#### 2. ECR Authentication Failed

**Error**: "no basic auth credentials"

**Solution**:
```bash
# Re-authenticate with ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin \
  <account-id>.dkr.ecr.us-east-1.amazonaws.com
```

#### 3. Lambda Function Not Updating

**Error**: Lambda shows old code

**Solution**:
```bash
# Force update
cd terraform
terraform taint aws_lambda_function.main
terraform apply
```

#### 4. GitHub Actions Failing

**Error**: Various CI/CD errors

**Solution**:
- Check GitHub Secrets are set correctly
- Verify AWS credentials have necessary permissions
- Check SonarQube token is valid
- Review workflow logs in GitHub Actions tab

#### 5. Poetry Lock File Issues

**Error**: "The lock file is not compatible"

**Solution**:
```bash
# Regenerate lock file
poetry lock --no-update
poetry install
```

## 🔄 Update Workflow

### To Update Lambda Code

1. Modify code in `src/lambda_handler.py`
2. Update tests in `tests/test_lambda_handler.py`
3. Run tests locally: `make test`
4. Commit and push to GitHub
5. CI/CD pipeline will automatically deploy

### To Update Infrastructure

1. Modify Terraform files in `terraform/`
2. Run `terraform plan` to preview changes
3. Commit and push to GitHub
4. CI/CD pipeline will apply changes

### To Add Dependencies

```bash
# Add a new dependency
poetry add <package-name>

# Add a dev dependency
poetry add --group dev <package-name>

# Update lock file
poetry lock

# Commit changes
git add pyproject.toml poetry.lock
git commit -m "Add new dependency"
```

## 📈 Performance Optimization

### Lambda Configuration

- **Memory**: Increase for CPU-intensive tasks (128MB - 10GB)
- **Timeout**: Set based on expected execution time (max 15 minutes)
- **Provisioned Concurrency**: For consistent low latency
- **Reserved Concurrency**: To limit maximum concurrent executions

### Cost Optimization

- Use appropriate memory size (more memory = more CPU)
- Set reasonable timeout values
- Implement CloudWatch log retention policies
- Use ECR lifecycle policies to remove old images
- Monitor with AWS Cost Explorer

## 🎯 Next Steps

1. **Customize Lambda Function**
   - Add your business logic to `src/lambda_handler.py`
   - Update tests accordingly

2. **Add API Gateway** (Optional)
   - Create `terraform/api_gateway.tf`
   - Configure REST or HTTP API

3. **Add Database Access** (Optional)
   - Add RDS/DynamoDB resources in Terraform
   - Update IAM policies
   - Add database connection in Lambda code

4. **Implement Monitoring**
   - Set up CloudWatch dashboards
   - Configure SNS for alarm notifications
   - Add X-Ray tracing

5. **Add More Environments**
   - Create separate Terraform workspaces
   - Configure environment-specific variables
   - Update CI/CD for multi-environment deployment

## 📞 Support

For issues or questions:
- Check the main README.md
- Review AWS Lambda documentation
- Check GitHub Issues
- Contact your team lead

## ✅ Deployment Checklist

Before going to production:

- [ ] All tests passing
- [ ] SonarQube quality gate passed
- [ ] Security scan completed
- [ ] CloudWatch alarms configured
- [ ] IAM policies reviewed
- [ ] Secrets stored securely
- [ ] Monitoring dashboard created
- [ ] Documentation updated
- [ ] Team trained on deployment process
- [ ] Rollback plan documented
- [ ] Load testing completed
- [ ] Cost estimates reviewed

---

**Last Updated**: December 2024
**Version**: 1.0.0
