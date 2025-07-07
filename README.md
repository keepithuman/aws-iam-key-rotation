# AWS IAM Key Rotation Automation

An enterprise-grade solution for automatically rotating AWS IAM access keys older than 90 days, designed for seamless integration with Itential Automation Gateway (IAG5).

## 🔑 Overview

This script provides automated AWS IAM access key rotation following AWS security best practices. It identifies access keys older than a specified threshold (default: 90 days), creates new keys, and safely deactivates old ones. The solution includes comprehensive logging, error handling, and is optimized for integration with Itential Automation Gateway.

## 🚀 Business Impact & Value

### Time Savings
- **Automated Process**: Eliminates manual key rotation tasks that typically take 15-30 minutes per user
- **Bulk Operations**: Can process hundreds of users in a single execution
- **Scheduled Execution**: Run via IAG on a scheduled basis (monthly/quarterly)
- **Estimated Savings**: 80-90% reduction in manual effort for key rotation tasks

### Security Benefits
- **Proactive Security**: Automatically enforces key rotation policies
- **Compliance**: Meets SOC 2, PCI DSS, and other compliance requirements
- **Risk Reduction**: Minimizes exposure from long-lived access keys
- **Audit Trail**: Comprehensive logging for security audits

### Operational Excellence
- **Standardization**: Consistent key rotation process across all AWS accounts
- **Error Handling**: Robust error handling with rollback capabilities
- **Dry Run Mode**: Test operations before executing changes
- **Integration Ready**: Built specifically for IAG5 workflow integration

### Cost Optimization
- **Resource Efficiency**: Reduces manual DevOps/Security team overhead
- **Prevents Incidents**: Avoids potential security breaches from stale keys
- **Compliance Costs**: Reduces audit preparation time and costs

## 📋 Features

- ✅ **Smart Detection**: Identifies access keys older than configurable threshold
- ✅ **Safe Rotation**: Creates new keys before deactivating old ones
- ✅ **Dry Run Mode**: Test operations without making changes
- ✅ **Bulk Processing**: Handle multiple users in single execution
- ✅ **Cleanup Operations**: Automatically remove old inactive keys
- ✅ **IAG Integration**: Native support for Itential Automation Gateway
- ✅ **Comprehensive Logging**: Detailed logs for audit and troubleshooting
- ✅ **JSON Output**: Structured output for programmatic consumption
- ✅ **Error Handling**: Robust error handling with cleanup on failures

## 🛠 Prerequisites

### AWS Requirements
- AWS CLI configured with appropriate credentials
- IAM permissions for key management operations
- Python 3.7 or higher

### Required IAM Permissions
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "iam:ListUsers",
                "iam:ListAccessKeys",
                "iam:CreateAccessKey",
                "iam:UpdateAccessKey",
                "iam:DeleteAccessKey",
                "iam:GetAccountSummary"
            ],
            "Resource": "*"
        }
    ]
}
```

## 📦 Installation

### Local Installation
```bash
# Clone the repository
git clone https://github.com/keepithuman/aws-iam-key-rotation.git
cd aws-iam-key-rotation

# Install dependencies
pip install -r requirements.txt

# Make script executable
chmod +x rotate_iam_keys.py
```

### IAG Installation (See detailed instructions below)

## 🎯 Usage Examples

### Basic Usage
```bash
# Rotate all keys older than 90 days (dry run)
python rotate_iam_keys.py --dry-run

# Rotate keys older than 60 days
python rotate_iam_keys.py --days-threshold 60

# Rotate keys for specific user
python rotate_iam_keys.py --user john.doe

# Include cleanup of old inactive keys
python rotate_iam_keys.py --cleanup-inactive

# Output in JSON format (recommended for IAG)
python rotate_iam_keys.py --output-format json
```

### Advanced Usage
```bash
# Use specific AWS profile and region
python rotate_iam_keys.py --profile production --region us-west-2

# Comprehensive rotation with cleanup
python rotate_iam_keys.py --days-threshold 90 --cleanup-inactive --output-format json
```

## 🔧 Itential Automation Gateway (IAG5) Integration

### Step 1: Create Repository in IAG

Using the MCP tool to create a repository in IAG:

```python
# Using MCP tool to create repository
create_iag_repository(
    name="aws-iam-key-rotation",
    description="Automated AWS IAM access key rotation service",
    url="https://github.com/keepithuman/aws-iam-key-rotation.git",
    reference="main"
)
```

### Step 2: Create Python Script Service in IAG

```python
# Using MCP tool to create the service
create_iag_service(
    service_type="python-script",
    name="aws-iam-key-rotation",
    repository="aws-iam-key-rotation",
    description="Rotate AWS IAM access keys older than 90 days",
    filename="rotate_iam_keys.py",
    working_dir="./",
    env=[
        "AWS_DEFAULT_REGION=us-east-1",
        "PYTHONPATH=./"
    ],
    tags=["aws", "iam", "security", "automation"]
)
```

### Step 3: Manual IAG CLI Configuration (Alternative)

If using IAG CLI directly:

```bash
# Create repository
iag repository create \
  --name aws-iam-key-rotation \
  --description "Automated AWS IAM access key rotation service" \
  --url https://github.com/keepithuman/aws-iam-key-rotation.git \
  --reference main

# Create python-script service
iag service create python-script \
  --name aws-iam-key-rotation \
  --repository aws-iam-key-rotation \
  --description "Rotate AWS IAM access keys older than 90 days" \
  --filename rotate_iam_keys.py \
  --working-dir ./ \
  --env AWS_DEFAULT_REGION=us-east-1 \
  --env PYTHONPATH=./ \
  --tag aws \
  --tag iam \
  --tag security \
  --tag automation
```

### Step 4: Configure Service Parameters in IAG

The service accepts the following parameters which can be configured in IAG workflows:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `days_threshold` | integer | 90 | Age threshold in days for key rotation |
| `dry_run` | boolean | false | Perform dry run without making changes |
| `aws_profile` | string | "" | AWS profile to use (optional) |
| `aws_region` | string | "us-east-1" | AWS region |
| `target_user` | string | "" | Specific user to rotate keys for |
| `cleanup_inactive` | boolean | false | Clean up inactive keys older than 30 days |
| `output_format` | string | "json" | Output format (json/text) |

### Step 5: IAG Workflow Integration Example

```json
{
  "workflow": {
    "name": "Monthly AWS Key Rotation",
    "description": "Automated monthly rotation of AWS IAM keys",
    "triggers": [
      {
        "type": "schedule",
        "cron": "0 2 1 * *"
      }
    ],
    "tasks": [
      {
        "name": "rotate_aws_keys",
        "type": "python-script",
        "service": "aws-iam-key-rotation",
        "parameters": {
          "days_threshold": 90,
          "dry_run": false,
          "cleanup_inactive": true,
          "output_format": "json"
        }
      }
    ]
  }
}
```

## 🏃‍♂️ Running the Service in IAG

### Using MCP Tool
```python
# Run the service
run_iag_service(
    service_type="python-script",
    name="aws-iam-key-rotation"
)
```

### Using IAG CLI
```bash
# Run the service with default parameters
iag service run python-script aws-iam-key-rotation

# Run with custom parameters
iag service run python-script aws-iam-key-rotation \
  --parameter days_threshold=60 \
  --parameter dry_run=true
```

## 📊 Output Format

### JSON Output (Recommended for IAG)
```json
{
  "execution_time": "2025-07-07T21:30:00Z",
  "dry_run": false,
  "days_threshold": 90,
  "rotated_keys": [
    {
      "username": "john.doe",
      "old_key_id": "AKIAIOSFODNN7EXAMPLE",
      "new_key_id": "AKIAI44QH8DHBEXAMPLE",
      "new_secret_key": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
      "success": true,
      "error": null,
      "dry_run": false
    }
  ],
  "cleanup_results": [],
  "errors": [],
  "summary": {
    "total_keys_processed": 1,
    "successful_rotations": 1,
    "failed_rotations": 0,
    "cleanup_operations": 0
  }
}
```

## 🔐 Security Considerations

### AWS Credentials
- Use IAM roles when running in AWS environments
- Store AWS credentials securely in IAG credential manager
- Follow principle of least privilege for IAM permissions

### Key Handling
- New secret keys are included in JSON output for IAG workflows
- Implement secure credential distribution to applications
- Monitor for applications using old keys after rotation

### Logging
- All operations are logged with timestamps
- Sensitive information is masked in logs
- Log files are stored securely

## 📈 Monitoring & Alerting

### Success Metrics
- Number of keys rotated successfully
- Execution time
- Error rates

### Recommended Alerts
- Failed key rotations
- Keys approaching rotation threshold
- Applications still using old keys

### IAG Integration Points
- Service execution status
- Output parsing for downstream workflows
- Error handling and notifications

## 🛠 Troubleshooting

### Common Issues

#### Permission Denied
```bash
# Verify IAM permissions
aws iam get-account-summary

# Check specific user permissions
aws iam list-attached-user-policies --user-name username
```

#### Key Limit Exceeded
- AWS limits users to 2 access keys
- Service will fail if user already has 2 active keys
- Use cleanup functionality to remove old inactive keys

#### Service Timeout
- Increase timeout in IAG service configuration
- Consider breaking large operations into smaller batches

### Debugging
```bash
# Enable verbose logging
python rotate_iam_keys.py --dry-run --days-threshold 1

# Check service logs in IAG
iag service logs python-script aws-iam-key-rotation
```

## 📝 Best Practices

### Scheduling
- Run monthly for most environments
- Use dry-run mode for initial testing
- Schedule during maintenance windows

### Key Management
- Rotate keys in non-production environments first
- Implement automated credential distribution
- Monitor application health after rotations

### IAG Integration
- Use JSON output format for workflow integration
- Implement proper error handling in workflows
- Store sensitive outputs securely

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For issues and questions:
- Create an issue in this repository
- Contact your IAG administrator
- Review AWS IAM documentation

## 📚 Additional Resources

- [AWS IAM Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
- [Itential Automation Gateway Documentation](https://docs.itential.com/)
- [AWS SDK for Python (Boto3)](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)

---

**Note**: This script is designed for enterprise use with proper testing and validation. Always test in non-production environments first and ensure you have proper backup and recovery procedures in place.
