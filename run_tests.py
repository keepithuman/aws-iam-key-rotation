#!/usr/bin/env python3
"""
Test Runner for AWS IAM Key Rotation

This script provides a unified interface for running all tests
with proper configuration and reporting.

Usage:
    python run_tests.py [options]

Author: Generated for Itential Automation Gateway
License: MIT
"""

import os
import sys
import subprocess
import argparse
import json
from pathlib import Path


def run_command(cmd, capture_output=True, check=True):
    """Run a command and return the result"""
    print(f"Running: {' '.join(cmd)}")
    try:
        result = subprocess.run(
            cmd, 
            capture_output=capture_output, 
            text=True, 
            check=check
        )
        return result
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}")
        if capture_output:
            print(f"stdout: {e.stdout}")
            print(f"stderr: {e.stderr}")
        return e


def install_dependencies():
    """Install test dependencies"""
    print("Installing test dependencies...")
    result = run_command([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    return result.returncode == 0


def run_unit_tests(coverage=True, verbose=False):
    """Run unit tests"""
    print("\n" + "="*50)
    print("RUNNING UNIT TESTS")
    print("="*50)
    
    cmd = [sys.executable, "-m", "pytest", "tests/test_unit.py"]
    
    if verbose:
        cmd.append("-v")
    
    if coverage:
        cmd.extend([
            "--cov=rotate_iam_keys",
            "--cov-report=html",
            "--cov-report=xml",
            "--cov-report=term"
        ])
    
    result = run_command(cmd, capture_output=False)
    return result.returncode == 0


def run_integration_tests(verbose=False):
    """Run integration tests"""
    print("\n" + "="*50)
    print("RUNNING INTEGRATION TESTS")
    print("="*50)
    
    cmd = [sys.executable, "-m", "pytest", "tests/test_integration.py"]
    
    if verbose:
        cmd.append("-v")
    
    result = run_command(cmd, capture_output=False)
    return result.returncode == 0


def run_syntax_check():
    """Check Python syntax"""
    print("\n" + "="*50)
    print("CHECKING SYNTAX")
    print("="*50)
    
    files_to_check = [
        "rotate_iam_keys.py",
        "tests/test_unit.py",
        "tests/test_integration.py",
        "tests/test_config.py"
    ]
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            result = run_command([sys.executable, "-m", "py_compile", file_path])
            if result.returncode != 0:
                return False
            print(f"✓ {file_path}")
    
    return True


def run_lint_checks():
    """Run linting checks"""
    print("\n" + "="*50)
    print("RUNNING LINT CHECKS")
    print("="*50)
    
    try:
        # Install linting tools
        run_command([
            sys.executable, "-m", "pip", "install", 
            "flake8", "black", "isort"
        ])
        
        # Run flake8
        print("Running flake8...")
        result = run_command([
            "flake8", "rotate_iam_keys.py", "tests/",
            "--max-line-length=88",
            "--ignore=E501,W503"
        ])
        
        if result.returncode == 0:
            print("✓ flake8 passed")
        else:
            print("✗ flake8 failed")
            return False
        
        # Check black formatting
        print("Checking black formatting...")
        result = run_command([
            "black", "--check", "--diff", "."
        ])
        
        if result.returncode == 0:
            print("✓ black formatting passed")
        else:
            print("✗ black formatting failed")
            return False
        
        # Check import sorting
        print("Checking import sorting...")
        result = run_command([
            "isort", "--check-only", "--diff", "."
        ])
        
        if result.returncode == 0:
            print("✓ isort passed")
        else:
            print("✗ isort failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"Linting failed: {e}")
        return False


def run_security_checks():
    """Run security checks"""
    print("\n" + "="*50)
    print("RUNNING SECURITY CHECKS")
    print("="*50)
    
    try:
        # Install security tools
        run_command([
            sys.executable, "-m", "pip", "install", 
            "bandit", "safety"
        ])
        
        # Run bandit
        print("Running bandit security check...")
        result = run_command([
            "bandit", "-r", "rotate_iam_keys.py", "-f", "txt"
        ])
        
        if result.returncode == 0:
            print("✓ bandit security check passed")
        else:
            print("⚠ bandit found potential security issues")
        
        # Run safety check
        print("Running safety dependency check...")
        result = run_command([
            "safety", "check"
        ])
        
        if result.returncode == 0:
            print("✓ safety dependency check passed")
        else:
            print("⚠ safety found vulnerable dependencies")
        
        return True
        
    except Exception as e:
        print(f"Security checks failed: {e}")
        return False


def generate_test_report(results):
    """Generate a test report"""
    print("\n" + "="*50)
    print("TEST SUMMARY REPORT")
    print("="*50)
    
    total_tests = len(results)
    passed_tests = sum(1 for result in results.values() if result)
    
    for test_name, passed in results.items():
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{test_name:.<30} {status}")
    
    print(f"\nTotal: {total_tests}, Passed: {passed_tests}, Failed: {total_tests - passed_tests}")
    
    if passed_tests == total_tests:
        print("🎉 ALL TESTS PASSED!")
        return True
    else:
        print("❌ SOME TESTS FAILED!")
        return False


def main():
    parser = argparse.ArgumentParser(description="Run tests for AWS IAM Key Rotation")
    parser.add_argument("--unit", action="store_true", help="Run only unit tests")
    parser.add_argument("--integration", action="store_true", help="Run only integration tests")
    parser.add_argument("--no-coverage", action="store_true", help="Skip coverage reporting")
    parser.add_argument("--no-lint", action="store_true", help="Skip linting checks")
    parser.add_argument("--no-security", action="store_true", help="Skip security checks")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--install-deps", action="store_true", help="Install dependencies before testing")
    
    args = parser.parse_args()
    
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("AWS IAM Key Rotation - Test Runner")
    print("=" * 50)
    
    # Install dependencies if requested
    if args.install_deps:
        if not install_dependencies():
            print("Failed to install dependencies")
            sys.exit(1)
    
    # Track test results
    results = {}
    
    # Run syntax check
    results["Syntax Check"] = run_syntax_check()
    
    # Run linting if not skipped
    if not args.no_lint:
        results["Lint Checks"] = run_lint_checks()
    
    # Run security checks if not skipped
    if not args.no_security:
        results["Security Checks"] = run_security_checks()
    
    # Run tests based on arguments
    if args.unit or (not args.unit and not args.integration):
        results["Unit Tests"] = run_unit_tests(
            coverage=not args.no_coverage,
            verbose=args.verbose
        )
    
    if args.integration or (not args.unit and not args.integration):
        results["Integration Tests"] = run_integration_tests(verbose=args.verbose)
    
    # Generate report
    success = generate_test_report(results)
    
    # Print coverage info if available
    if not args.no_coverage and os.path.exists("htmlcov/index.html"):
        print(f"\nCoverage report available at: file://{os.path.abspath('htmlcov/index.html')}")
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
