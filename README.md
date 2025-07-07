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

```bash
# Create repository in IAG
iag repository create \
  --name "aws-iam-key-rotation" \
  --description "Automated AWS IAM access key rotation service" \
  --url "https://github.com/keepithuman/aws-iam-key-rotation.git" \
  --reference "main"
```

Or using the MCP tool programmatically:

