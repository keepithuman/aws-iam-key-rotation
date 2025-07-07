#!/bin/bash
# 
# Manual Deployment Script for AWS IAM Key Rotation Service to IAG
# 
# This script provides manual deployment capabilities for environments
# where GitHub Actions cannot be used or for emergency deployments.
#
# Usage: ./deploy-to-iag.sh [staging|production] [options]
#
# Author: Generated for Itential Automation Gateway
# License: MIT

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVICE_NAME="aws-iam-key-rotation"
SERVICE_TYPE="python-script"

# Default values
ENVIRONMENT="staging"
DRY_RUN=false
VERBOSE=false
BACKUP=true
TEST_AFTER_DEPLOY=true

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
    exit 1
}

# Help function
show_help() {
    cat << EOF
AWS IAM Key Rotation Service - IAG Deployment Script

Usage: $0 [ENVIRONMENT] [OPTIONS]

ENVIRONMENT:
    staging     Deploy to staging IAG environment
    production  Deploy to production IAG environment

OPTIONS:
    --dry-run           Show what would be deployed without making changes
    --no-backup         Skip creating backup of existing files
    --no-test           Skip post-deployment testing
    --verbose           Show detailed output
    --help              Show this help message

EXAMPLES:
    $0 staging --verbose
    $0 production --dry-run
    $0 staging --no-backup --no-test

ENVIRONMENT VARIABLES:
    IAG_STAGING_HOST       Hostname for staging IAG server
    IAG_PRODUCTION_HOST    Hostname for production IAG server
    IAG_SSH_KEY_PATH       Path to SSH private key for IAG servers
    IAG_USER               Username for IAG server (default: iag-user)
    IAG_SERVICE_PATH       Path to IAG services directory (default: /opt/iag/services)

EOF
}

# Parse command line arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            staging|production)
                ENVIRONMENT="$1"
                shift
                ;;
            --dry-run)
                DRY_RUN=true
                shift
                ;;
            --no-backup)
                BACKUP=false
                shift
                ;;
            --no-test)
                TEST_AFTER_DEPLOY=false
                shift
                ;;
            --verbose)
                VERBOSE=true
                shift
                ;;
            --help)
                show_help
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
                ;;
        esac
    done
}

# Validate environment variables
validate_environment() {
    local required_vars=()
    
    if [[ "$ENVIRONMENT" == "staging" ]]; then
        required_vars=("IAG_STAGING_HOST")
    elif [[ "$ENVIRONMENT" == "production" ]]; then
        required_vars=("IAG_PRODUCTION_HOST")
    fi
    
    for var in "${required_vars[@]}"; do
        if [[ -z "${!var:-}" ]]; then
            log_error "Required environment variable $var is not set"
        fi
    done
    
    # Set defaults
    IAG_USER="${IAG_USER:-iag-user}"
    IAG_SERVICE_PATH="${IAG_SERVICE_PATH:-/opt/iag/services}"
    IAG_SSH_KEY_PATH="${IAG_SSH_KEY_PATH:-$HOME/.ssh/id_rsa}"
    
    # Validate SSH key
    if [[ ! -f "$IAG_SSH_KEY_PATH" ]]; then
        log_error "SSH key not found at: $IAG_SSH_KEY_PATH"
    fi
}

# Get IAG host based on environment
get_iag_host() {
    case "$ENVIRONMENT" in
        staging)
            echo "${IAG_STAGING_HOST}"
            ;;
        production)
            echo "${IAG_PRODUCTION_HOST}"
            ;;
        *)
            log_error "Invalid environment: $ENVIRONMENT"
            ;;
    esac
}

# Check if files exist
validate_files() {
    local required_files=(
        "rotate_iam_keys.py"
        "requirements.txt"
        "iag_config.json"
    )
    
    for file in "${required_files[@]}"; do
        if [[ ! -f "$SCRIPT_DIR/$file" ]]; then
            log_error "Required file not found: $file"
        fi
    done
}

# Test SSH connectivity
test_ssh_connection() {
    local host="$1"
    
    log_info "Testing SSH connection to $host..."
    
    if ! ssh -i "$IAG_SSH_KEY_PATH" -o ConnectTimeout=10 -o StrictHostKeyChecking=no \
            "$IAG_USER@$host" "echo 'SSH connection successful'" >/dev/null 2>&1; then
        log_error "SSH connection failed to $host"
    fi
    
    log_success "SSH connection to $host successful"
}

# Create backup of existing files
create_backup() {
    local host="$1"
    
    if [[ "$BACKUP" == "false" ]]; then
        log_info "Skipping backup as requested"
        return 0
    fi
    
    log_info "Creating backup of existing files on $host..."
    
    local backup_timestamp=$(date +%Y%m%d_%H%M%S)
    
    ssh -i "$IAG_SSH_KEY_PATH" -o StrictHostKeyChecking=no "$IAG_USER@$host" << EOF
        cd "$IAG_SERVICE_PATH/$SERVICE_NAME" 2>/dev/null || exit 0
        
        if [[ -f "rotate_iam_keys.py" ]]; then
            cp rotate_iam_keys.py "rotate_iam_keys.py.backup.$backup_timestamp"
            echo "Created backup: rotate_iam_keys.py.backup.$backup_timestamp"
        fi
        
        if [[ -f "requirements.txt" ]]; then
            cp requirements.txt "requirements.txt.backup.$backup_timestamp"
            echo "Created backup: requirements.txt.backup.$backup_timestamp"
        fi
        
        if [[ -f "iag_config.json" ]]; then
            cp iag_config.json "iag_config.json.backup.$backup_timestamp"
            echo "Created backup: iag_config.json.backup.$backup_timestamp"
        fi
EOF
    
    log_success "Backup completed"
}

# Deploy files to IAG server
deploy_files() {
    local host="$1"
    
    log_info "Deploying files to $host..."
    
    if [[ "$DRY_RUN" == "true" ]]; then
        log_warning "DRY RUN: Would deploy the following files:"
        echo "  - rotate_iam_keys.py"
        echo "  - requirements.txt"
        echo "  - iag_config.json"
        echo "  Target: $IAG_USER@$host:$IAG_SERVICE_PATH/$SERVICE_NAME/"
        return 0
    fi
    
    # Ensure target directory exists
    ssh -i "$IAG_SSH_KEY_PATH" -o StrictHostKeyChecking=no "$IAG_USER@$host" \
        "mkdir -p $IAG_SERVICE_PATH/$SERVICE_NAME"
    
    # Copy files
    scp -i "$IAG_SSH_KEY_PATH" -o StrictHostKeyChecking=no \
        "$SCRIPT_DIR/rotate_iam_keys.py" \
        "$SCRIPT_DIR/requirements.txt" \
        "$SCRIPT_DIR/iag_config.json" \
        "$IAG_USER@$host:$IAG_SERVICE_PATH/$SERVICE_NAME/"
    
    log_success "Files deployed successfully"
}

# Update IAG service
update_iag_service() {
    local host="$1"
    
    log_info "Updating IAG service on $host..."
    
    if [[ "$DRY_RUN" == "true" ]]; then
        log_warning "DRY RUN: Would update IAG service configuration"
        return 0
    fi
    
    ssh -i "$IAG_SSH_KEY_PATH" -o StrictHostKeyChecking=no "$IAG_USER@$host" << EOF
        cd "$IAG_SERVICE_PATH/$SERVICE_NAME"
        
        # Install/update Python dependencies
        echo "Installing Python dependencies..."
        pip install -r requirements.txt
        
        # Update IAG service
        echo "Updating IAG service..."
        iag service update $SERVICE_TYPE $SERVICE_NAME
        
        # Reload IAG services if needed
        if command -v systemctl >/dev/null 2>&1; then
            sudo systemctl reload iag-services 2>/dev/null || true
        fi
EOF
    
    log_success "IAG service updated successfully"
}

# Test deployment
test_deployment() {
    local host="$1"
    
    if [[ "$TEST_AFTER_DEPLOY" == "false" ]]; then
        log_info "Skipping post-deployment testing as requested"
        return 0
    fi
    
    log_info "Testing deployment on $host..."
    
    if [[ "$DRY_RUN" == "true" ]]; then
        log_warning "DRY RUN: Would run deployment tests"
        return 0
    fi
    
    ssh -i "$IAG_SSH_KEY_PATH" -o StrictHostKeyChecking=no "$IAG_USER@$host" << EOF
        cd "$IAG_SERVICE_PATH/$SERVICE_NAME"
        
        # Test script syntax
        echo "Testing script syntax..."
        python -m py_compile rotate_iam_keys.py
        
        # Test CLI help
        echo "Testing CLI interface..."
        python rotate_iam_keys.py --help >/dev/null
        
        # Test IAG service listing
        echo "Testing IAG service registration..."
        iag service list | grep "$SERVICE_NAME" >/dev/null
        
        # Test dry run execution
        echo "Testing dry run execution..."
        iag service run $SERVICE_TYPE $SERVICE_NAME \
            --parameter dry_run=true \
            --parameter output_format=json \
            --timeout 60
EOF
    
    log_success "Deployment tests passed"
}

# Main deployment function
main() {
    log_info "Starting deployment of $SERVICE_NAME to $ENVIRONMENT environment"
    
    # Parse arguments
    parse_args "$@"
    
    # Validate environment
    validate_environment
    
    # Get IAG host
    local iag_host
    iag_host=$(get_iag_host)
    
    log_info "Target IAG server: $iag_host"
    log_info "Environment: $ENVIRONMENT"
    log_info "Dry run: $DRY_RUN"
    
    # Validate local files
    validate_files
    
    # Test SSH connection
    test_ssh_connection "$iag_host"
    
    # Create backup
    create_backup "$iag_host"
    
    # Deploy files
    deploy_files "$iag_host"
    
    # Update IAG service
    update_iag_service "$iag_host"
    
    # Test deployment
    test_deployment "$iag_host"
    
    if [[ "$DRY_RUN" == "true" ]]; then
        log_success "Dry run completed successfully - no changes made"
    else
        log_success "Deployment to $ENVIRONMENT completed successfully"
        log_info "Service is now available at: $iag_host"
        log_info "You can test the service with: iag service run $SERVICE_TYPE $SERVICE_NAME --parameter dry_run=true"
    fi
}

# Run main function with all arguments
main "$@"
