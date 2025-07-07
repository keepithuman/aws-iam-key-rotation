#!/usr/bin/env python3
"""
Unit Tests for AWS IAM Key Rotation Script

This module contains comprehensive unit tests for the IAMKeyRotator class
and its methods. Tests use mocking to avoid actual AWS API calls.

Author: Generated for Itential Automation Gateway
License: MIT
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import pytest
import boto3
from botocore.exceptions import ClientError
from datetime import datetime, timezone, timedelta
import json
import sys
import os

# Add the project root to the path so we can import our module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rotate_iam_keys import IAMKeyRotator


class TestIAMKeyRotator(unittest.TestCase):
    """Test cases for IAMKeyRotator class"""
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.mock_iam_client = Mock()
        self.rotator = IAMKeyRotator()
        self.rotator.iam_client = self.mock_iam_client
        
        # Sample test data
        self.sample_user = {
            'UserName': 'test-user',
            'Path': '/',
            'CreateDate': datetime(2023, 1, 1, tzinfo=timezone.utc),
            'UserId': 'AIDACKCEVSQ6C2EXAMPLE'
        }
        
        self.sample_old_key = {
            'AccessKeyId': 'AKIAIOSFODNN7EXAMPLE',
            'Status': 'Active',
            'CreateDate': datetime.now(timezone.utc) - timedelta(days=100)
        }
        
        self.sample_new_key = {
            'AccessKeyId': 'AKIAI44QH8DHBEXAMPLE',
            'Status': 'Active',
            'CreateDate': datetime.now(timezone.utc)
        }

    def test_init_with_profile(self):
        """Test initialization with AWS profile"""
        with patch('boto3.Session') as mock_session:
            mock_session.return_value.client.return_value.get_account_summary.return_value = {}
            rotator = IAMKeyRotator(aws_profile='test-profile', region='us-west-2')
            mock_session.assert_called_once_with(profile_name='test-profile')

    def test_init_without_profile(self):
        """Test initialization without AWS profile"""
        with patch('boto3.client') as mock_client:
            mock_client.return_value.get_account_summary.return_value = {}
            rotator = IAMKeyRotator(region='us-west-2')
            mock_client.assert_called_once_with('iam', region_name='us-west-2')

    def test_init_connection_failure(self):
        """Test initialization with connection failure"""
        with patch('boto3.client') as mock_client:
            mock_client.return_value.get_account_summary.side_effect = ClientError(
                {'Error': {'Code': 'AccessDenied', 'Message': 'Access denied'}},
                'GetAccountSummary'
            )
            with self.assertRaises(ClientError):
                IAMKeyRotator()

    def test_get_users_with_old_keys_success(self):
        """Test successful retrieval of users with old keys"""
        # Mock the paginator and responses
        mock_paginator = Mock()
        self.mock_iam_client.get_paginator.return_value = mock_paginator
        
        # Mock paginator response
        mock_paginator.paginate.return_value = [
            {
                'Users': [self.sample_user]
            }
        ]
        
        # Mock list_access_keys response
        self.mock_iam_client.list_access_keys.return_value = {
            'AccessKeyMetadata': [self.sample_old_key]
        }
        
        # Test the method
        result = self.rotator.get_users_with_old_keys(days_threshold=90)
        
        # Assertions
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['username'], 'test-user')
        self.assertEqual(result[0]['access_key_id'], 'AKIAIOSFODNN7EXAMPLE')
        self.assertGreater(result[0]['age_days'], 90)

    def test_get_users_with_old_keys_no_old_keys(self):
        """Test retrieval when no old keys exist"""
        # Mock responses for recent keys
        mock_paginator = Mock()
        self.mock_iam_client.get_paginator.return_value = mock_paginator
        mock_paginator.paginate.return_value = [{'Users': [self.sample_user]}]
        
        recent_key = self.sample_old_key.copy()
        recent_key['CreateDate'] = datetime.now(timezone.utc) - timedelta(days=30)
        
        self.mock_iam_client.list_access_keys.return_value = {
            'AccessKeyMetadata': [recent_key]
        }
        
        result = self.rotator.get_users_with_old_keys(days_threshold=90)
        self.assertEqual(len(result), 0)

    def test_get_users_with_old_keys_inactive_keys(self):
        """Test that inactive keys are ignored"""
        mock_paginator = Mock()
        self.mock_iam_client.get_paginator.return_value = mock_paginator
        mock_paginator.paginate.return_value = [{'Users': [self.sample_user]}]
        
        inactive_key = self.sample_old_key.copy()
        inactive_key['Status'] = 'Inactive'
        
        self.mock_iam_client.list_access_keys.return_value = {
            'AccessKeyMetadata': [inactive_key]
        }
        
        result = self.rotator.get_users_with_old_keys(days_threshold=90)
        self.assertEqual(len(result), 0)

    def test_rotate_user_key_dry_run(self):
        """Test key rotation in dry run mode"""
        result = self.rotator.rotate_user_key(
            username='test-user',
            old_key_id='AKIAIOSFODNN7EXAMPLE',
            dry_run=True
        )
        
        self.assertTrue(result['success'])
        self.assertTrue(result['dry_run'])
        self.assertEqual(result['new_key_id'], 'DRY_RUN_KEY_ID')
        self.mock_iam_client.create_access_key.assert_not_called()

    def test_rotate_user_key_success(self):
        """Test successful key rotation"""
        # Mock existing keys check
        self.mock_iam_client.list_access_keys.return_value = {
            'AccessKeyMetadata': [self.sample_old_key]
        }
        
        # Mock create_access_key response
        self.mock_iam_client.create_access_key.return_value = {
            'AccessKey': {
                'AccessKeyId': 'AKIAI44QH8DHBEXAMPLE',
                'SecretAccessKey': 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY'
            }
        }
        
        # Mock update_access_key (no return value needed)
        self.mock_iam_client.update_access_key.return_value = {}
        
        result = self.rotator.rotate_user_key(
            username='test-user',
            old_key_id='AKIAIOSFODNN7EXAMPLE',
            dry_run=False
        )
        
        self.assertTrue(result['success'])
        self.assertFalse(result['dry_run'])
        self.assertEqual(result['new_key_id'], 'AKIAI44QH8DHBEXAMPLE')
        self.assertIn('new_secret_key', result)
        
        # Verify API calls
        self.mock_iam_client.create_access_key.assert_called_once_with(UserName='test-user')
        self.mock_iam_client.update_access_key.assert_called_once_with(
            UserName='test-user',
            AccessKeyId='AKIAIOSFODNN7EXAMPLE',
            Status='Inactive'
        )

    def test_rotate_user_key_too_many_keys(self):
        """Test rotation failure when user has too many keys"""
        # Mock response with 2 existing keys
        self.mock_iam_client.list_access_keys.return_value = {
            'AccessKeyMetadata': [self.sample_old_key, self.sample_new_key]
        }
        
        result = self.rotator.rotate_user_key(
            username='test-user',
            old_key_id='AKIAIOSFODNN7EXAMPLE',
            dry_run=False
        )
        
        self.assertFalse(result['success'])
        self.assertIn('already has 2 access keys', result['error'])
        self.mock_iam_client.create_access_key.assert_not_called()

    def test_rotate_user_key_create_failure(self):
        """Test rotation failure during key creation"""
        self.mock_iam_client.list_access_keys.return_value = {
            'AccessKeyMetadata': [self.sample_old_key]
        }
        
        # Mock create_access_key failure
        self.mock_iam_client.create_access_key.side_effect = ClientError(
            {'Error': {'Code': 'LimitExceeded', 'Message': 'Too many keys'}},
            'CreateAccessKey'
        )
        
        result = self.rotator.rotate_user_key(
            username='test-user',
            old_key_id='AKIAIOSFODNN7EXAMPLE',
            dry_run=False
        )
        
        self.assertFalse(result['success'])
        self.assertIn('Too many keys', result['error'])

    def test_cleanup_old_keys_success(self):
        """Test successful cleanup of old inactive keys"""
        old_inactive_key = {
            'AccessKeyId': 'AKIAOLDKEYEXAMPLE',
            'Status': 'Inactive',
            'CreateDate': datetime.now(timezone.utc) - timedelta(days=35)
        }
        
        self.mock_iam_client.list_access_keys.return_value = {
            'AccessKeyMetadata': [old_inactive_key, self.sample_new_key]
        }
        
        result = self.rotator.cleanup_old_keys(
            username='test-user',
            days_inactive=30,
            dry_run=False
        )
        
        self.assertTrue(result['success'])
        self.assertEqual(len(result['deleted_keys']), 1)
        self.assertIn('AKIAOLDKEYEXAMPLE', result['deleted_keys'])
        
        self.mock_iam_client.delete_access_key.assert_called_once_with(
            UserName='test-user',
            AccessKeyId='AKIAOLDKEYEXAMPLE'
        )

    def test_cleanup_old_keys_dry_run(self):
        """Test cleanup in dry run mode"""
        old_inactive_key = {
            'AccessKeyId': 'AKIAOLDKEYEXAMPLE',
            'Status': 'Inactive',
            'CreateDate': datetime.now(timezone.utc) - timedelta(days=35)
        }
        
        self.mock_iam_client.list_access_keys.return_value = {
            'AccessKeyMetadata': [old_inactive_key]
        }
        
        result = self.rotator.cleanup_old_keys(
            username='test-user',
            days_inactive=30,
            dry_run=True
        )
        
        self.assertTrue(result['success'])
        self.assertTrue(result['dry_run'])
        self.assertEqual(len(result['deleted_keys']), 1)
        self.mock_iam_client.delete_access_key.assert_not_called()

    def test_cleanup_old_keys_no_old_keys(self):
        """Test cleanup when no old keys exist"""
        self.mock_iam_client.list_access_keys.return_value = {
            'AccessKeyMetadata': [self.sample_new_key]
        }
        
        result = self.rotator.cleanup_old_keys(
            username='test-user',
            days_inactive=30,
            dry_run=False
        )
        
        self.assertTrue(result['success'])
        self.assertEqual(len(result['deleted_keys']), 0)
        self.mock_iam_client.delete_access_key.assert_not_called()


class TestMainFunction(unittest.TestCase):
    """Test cases for the main function and CLI argument parsing"""
    
    @patch('rotate_iam_keys.IAMKeyRotator')
    @patch('sys.argv')
    def test_main_dry_run(self, mock_argv, mock_rotator_class):
        """Test main function with dry run argument"""
        mock_argv.__getitem__.return_value = ['rotate_iam_keys.py', '--dry-run']
        mock_rotator = Mock()
        mock_rotator_class.return_value = mock_rotator
        mock_rotator.get_users_with_old_keys.return_value = []
        
        # Import and test main function
        from rotate_iam_keys import main
        
        with patch('sys.exit') as mock_exit:
            main()
            mock_exit.assert_called_with(0)

    @patch('rotate_iam_keys.IAMKeyRotator')
    def test_main_with_specific_user(self, mock_rotator_class):
        """Test main function with specific user argument"""
        mock_rotator = Mock()
        mock_rotator_class.return_value = mock_rotator
        
        # Mock list_access_keys for specific user
        mock_rotator.iam_client.list_access_keys.return_value = {
            'AccessKeyMetadata': []
        }
        
        from rotate_iam_keys import main
        
        with patch('sys.argv', ['script', '--user', 'test-user']):
            with patch('sys.exit') as mock_exit:
                main()
                mock_exit.assert_called_with(0)


if __name__ == '__main__':
    # Configure test runner
    unittest.main(verbosity=2)
