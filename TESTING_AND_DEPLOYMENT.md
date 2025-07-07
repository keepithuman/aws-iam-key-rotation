# Testing and Deployment Guide

## 🧪 Comprehensive Testing Suite

The AWS IAM Key Rotation service includes a complete testing framework with unit tests, integration tests, and deployment automation.

### 📋 Test Structure

```
tests/
├── test_unit.py          # Unit tests with mocking
├── test_integration.py   # Integration tests with moto
├── test_config.py        # Test utilities and fixtures
└── __init__.py
```

### 🚀 Quick Test Execution

#### Run All Tests
```bash
# Install dependencies and run all tests
python run_tests.py --install-deps --verbose

# Run tests with coverage
python run_tests.py --verbose

# Run only unit tests
python run_tests.py --unit --verbose

# Run only integration tests  
python run_tests.py --integration --verbose
```

#### Manual Test Execution
```bash
# Unit tests with coverage
pytest tests/test_unit.py -v --cov=rotate_iam_keys --cov-report=html

# Integration tests
pytest tests/test_integration.py -v

# All tests
pytest tests/ -v --cov=rotate_iam_keys
```

### 🔍 Test Coverage

Our test suite provides comprehensive coverage:

- ✅ **Unit Tests**: 15+ test cases covering all core functionality
- ✅ **Integration Tests**: 10+ test cases for end-to-end workflows
- ✅ **Mocking**: Complete AWS API mocking with moto
- ✅ **Error Scenarios**: Comprehensive error handling validation
- ✅ **CLI Testing**: Command-line interface validation
- ✅ **IAG Integration**: Workflow format validation

#### Key Test Scenarios

**Unit Tests:**
- IAM client initialization and configuration
- Key age detection and filtering
- Safe key rotation workflow
- Cleanup operations
- Error handling and rollback
- Dry-run mode validation
- Configuration parameter handling

**Integration Tests:**
- Full rotation workflow with mocked AWS
- Bulk user processing
- Enterprise-scale testing (50+ users)
- Partial failure recovery
- Compliance audit workflows
- IAG output format validation

### 📊 Test Results and Coverage

After running tests, view coverage reports:
```bash
# Open HTML coverage report
open htmlcov/index.html

# View coverage summary
cat coverage.xml
```

## 🚢 Deployment Options

### 1. GitHub Actions Pipeline (Automated)

The repository includes a complete CI/CD pipeline that automatically:
- Runs tests on every push/PR
- Deploys to staging on `develop` branch
- Deploys to production on releases
- Includes security scanning and linting

**Setup Requirements:**
```yaml
# GitHub Secrets needed:
IAG_STAGING_HOST      # staging.iag.company.com
IAG_PRODUCTION_HOST   # production.iag.company.com  
IAG_STAGING_SSH_KEY   # SSH private key for staging
IAG_PRODUCTION_SSH_KEY # SSH private key for production
```

**Pipeline Features:**
- ✅ Automated testing (unit + integration)
- ✅ Code quality checks (linting, formatting)
- ✅ Security scanning (bandit, safety)
- ✅ Multi-environment deployment
- ✅ Rollback capabilities
- ✅ Slack/email notifications

### 2. Manual Deployment Script

For environments without GitHub Actions access:

```bash
# Make deployment script executable
chmod +x deploy-to-iag.sh

# Deploy to staging
./deploy-to-iag.sh staging --verbose

# Deploy to production (with backup)
./deploy-to-iag.sh production --verbose

# Dry run to see what would be deployed
./deploy-to-iag.sh production --dry-run

# Deploy without testing
./deploy-to-iag.sh staging --no-test
```

**Environment Variables:**
```bash
export IAG_STAGING_HOST="staging.iag.company.com"
export IAG_PRODUCTION_HOST="production.iag.company.com"
export IAG_SSH_KEY_PATH="$HOME/.ssh/iag_key"
export IAG_USER="iag-user"
export IAG_SERVICE_PATH="/opt/iag/services"
```

### 3. MCP Tool Integration (Programmatic)

Using the Itential MCP tools for automated deployment:

```python
# Create repository in IAG
create_iag_repository(
    name="aws-iam-key-rotation",
    description="Automated AWS IAM access key rotation service",
    url="https://github.com/keepithuman/aws-iam-key-rotation.git",
    reference="main"
)

# Create service in IAG
create_iag_service(
    service_type="python-script",
    name="aws-iam-key-rotation",
    repository="aws-iam-key-rotation",
    description="Rotate AWS IAM access keys older than 90 days",
    filename="rotate_iam_keys.py",
    working_dir="./"
)

# Run the service
run_iag_service(
    service_type="python-script",
    name="aws-iam-key-rotation"
)
```

## 🔒 Security & Quality Assurance

### Security Scanning
```bash
# Security vulnerability scanning
bandit -r rotate_iam_keys.py -f json -o security-report.json

# Dependency vulnerability check
safety check --json --output safety-report.json
```

### Code Quality
```bash
# Code formatting
black --check --diff .

# Import sorting
isort --check-only --diff .

# Linting
flake8 rotate_iam_keys.py tests/ --max-line-length=88
```

### Type Checking
```bash
# Static type analysis
mypy rotate_iam_keys.py --ignore-missing-imports
```

## 🏗 Development Workflow

### Local Development Setup
```bash
# Clone repository
git clone https://github.com/keepithuman/aws-iam-key-rotation.git
cd aws-iam-key-rotation

# Install development dependencies
pip install -r requirements.txt

# Install additional dev tools
pip install black isort flake8 mypy bandit safety

# Run tests
python run_tests.py --install-deps --verbose
```

### Pre-commit Checks
```bash
# Format code
black .
isort .

# Run all tests and checks
python run_tests.py --verbose

# Security check
bandit -r rotate_iam_keys.py
```

### Testing Before Deployment
```bash
# Test CLI functionality
python rotate_iam_keys.py --help
python rotate_iam_keys.py --dry-run --output-format json

# Validate configuration
python -c "import json; print(json.load(open('iag_config.json')))"

# Test script compilation
python -m py_compile rotate_iam_keys.py
```

## 📈 Monitoring and Validation

### Post-Deployment Validation
```bash
# Verify IAG service registration
iag service list | grep aws-iam-key-rotation

# Test service execution
iag service run python-script aws-iam-key-rotation \
  --parameter dry_run=true \
  --parameter output_format=json

# Check service logs
iag service logs python-script aws-iam-key-rotation
```

### Health Checks
```bash
# Service availability
curl -f http://iag-host/api/services/python-script/aws-iam-key-rotation/status

# AWS connectivity test
python rotate_iam_keys.py --dry-run --days-threshold 1 --output-format json
```

## 🚨 Troubleshooting

### Common Issues

#### Test Failures
```bash
# Clean and reinstall dependencies
rm -rf __pycache__ .pytest_cache htmlcov/
pip install --force-reinstall -r requirements.txt

# Run tests with detailed output
python run_tests.py --verbose --unit
```

#### Deployment Issues
```bash
# Check SSH connectivity
ssh -i ~/.ssh/iag_key iag-user@iag-host "echo 'Connection successful'"

# Verify file permissions
ls -la deploy-to-iag.sh
chmod +x deploy-to-iag.sh

# Test deployment script
./deploy-to-iag.sh staging --dry-run --verbose
```

#### IAG Service Issues
```bash
# Check IAG service status
iag service status python-script aws-iam-key-rotation

# Restart IAG services
sudo systemctl reload iag-services

# Check IAG logs
journalctl -u iag-services -f
```

### Debug Mode
```bash
# Enable debug logging in script
export DEBUG=1
python rotate_iam_keys.py --dry-run --verbose

# Run with Python debugger
python -m pdb rotate_iam_keys.py --help
```

## 📝 Best Practices

### Testing
1. **Always run tests before deployment**
2. **Use dry-run mode for validation**
3. **Test in staging before production**
4. **Verify AWS credentials are configured**
5. **Check IAG service health after deployment**

### Deployment
1. **Create backups before updating**
2. **Use version tags for production releases**
3. **Monitor deployment logs**
4. **Validate service functionality post-deployment**
5. **Have rollback plan ready**

### Security
1. **Store AWS credentials securely in IAG**
2. **Use IAM roles when possible**
3. **Regularly update dependencies**
4. **Monitor security scan results**
5. **Follow principle of least privilege**

---

**Next Steps:** After successful testing and deployment, configure scheduled execution in IAG and set up monitoring alerts for the service.
