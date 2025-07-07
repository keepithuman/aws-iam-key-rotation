#!/usr/bin/env python3
"""
Test Configuration and Utilities

This module provides test configuration, utilities, and fixtures
for the AWS IAM Key Rotation test suite.

Author: Generated for Itential Automation Gateway
License: MIT
"""

import os
import sys
import unittest
from unittest.mock import Mock, patch
import boto3
from moto import mock_iam
from datetime import datetime, timezone, timedelta

# Test configuration
TEST_CONFIG = {
    'aws_region': 'us-east-1',
    'test_users': ['test-user-1', 'test-user-2', 'test-user-3'],
    'days_threshold': 90,
    'cleanup_days': 30
}


class TestFixtures:
    """Common test fixtures and utilities"""
    
    @staticmethod
    def create_sample_user_data():
        """Create sample user data for testing"""
        return {
            'UserName': 'test-user',
            'Path': '/',
            'CreateDate': datetime(2023, 1, 1, tzinfo=timezone.utc),
            'UserId': 'AIDACKCEVSQ6C2EXAMPLE'
        }
    
    @staticmethod
    def create_sample_old_key():
        """Create sample old access key for testing"""
        return {
            'AccessKeyId': 'AKIAIOSFODNN7EXAMPLE',
            'Status': 'Active',
            'CreateDate': datetime.now(timezone.utc) - timedelta(days=100)
        }
    
    @staticmethod
    def create_sample_new_key():
        """Create sample new access key for testing"""
        return {
            'AccessKeyId': 'AKIAI44QH8DHBEXAMPLE',
            'Status': 'Active',
            'CreateDate': datetime.now(timezone.utc)
        }
    
    @staticmethod
    def setup_mock_iam_client():
        """Set up a mock IAM client with common responses"""
        mock_client = Mock()
        
        # Mock common responses
        mock_client.get_account_summary.return_value = {
            'SummaryMap': {'Users': 10, 'AccessKeysPerUserQuota': 2}
        }
        
        mock_client.list_users.return_value = {
            'Users': [TestFixtures.create_sample_user_data()]
        }
        
        mock_client.list_access_keys.return_value = {
            'AccessKeyMetadata': [TestFixtures.create_sample_old_key()]
        }
        
        return mock_client


class BaseTestCase(unittest.TestCase):
    """Base test case with common setup and utilities"""
    
    def setUp(self):
        """Common setup for all test cases"""
        self.fixtures = TestFixtures()
        self.test_config = TEST_CONFIG.copy()
        
        # Set up test environment
        self.addCleanup(self.cleanup_test_environment)
    
    def cleanup_test_environment(self):
        """Clean up after tests"""
        # Reset any global state if needed
        pass
    
    def assert_rotation_result_valid(self, result, dry_run=False):
        """Assert that a rotation result has valid structure"""
        required_keys = ['username', 'old_key_id', 'success', 'error', 'dry_run']
        
        for key in required_keys:
            self.assertIn(key, result, f"Missing required key: {key}")
        
        self.assertEqual(result['dry_run'], dry_run)
        
        if result['success']:
            if not dry_run:
                self.assertIsNotNone(result.get('new_key_id'))
            self.assertIsNone(result['error'])
        else:
            self.assertIsNotNone(result['error'])
    
    def assert_cleanup_result_valid(self, result, dry_run=False):
        """Assert that a cleanup result has valid structure"""
        required_keys = ['username', 'deleted_keys', 'success', 'error', 'dry_run']
        
        for key in required_keys:
            self.assertIn(key, result, f"Missing required key: {key}")
        
        self.assertEqual(result['dry_run'], dry_run)
        self.assertIsInstance(result['deleted_keys'], list)
        
        if result['success']:
            self.assertIsNone(result['error'])
        else:
            self.assertIsNotNone(result['error'])


class MockAWSEnvironment:
    """Context manager for setting up mock AWS environment"""
    
    def __init__(self, region='us-east-1'):
        self.region = region
        self.mock_iam = mock_iam()
        
    def __enter__(self):
        self.mock_iam.start()
        self.iam_client = boto3.client('iam', region_name=self.region)
        return self.iam_client
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.mock_iam.stop()


def run_test_suite():
    """Run the complete test suite"""
    # Discover and run all tests
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(__file__)
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    # Run test configuration validation
    success = run_test_suite()
    sys.exit(0 if success else 1)
