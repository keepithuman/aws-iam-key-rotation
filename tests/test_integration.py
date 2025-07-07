#!/usr/bin/env python3
"""
Integration Tests for AWS IAM Key Rotation Script - Part 2

Continuation of integration tests focusing on workflow scenarios
and end-to-end testing.

Author: Generated for Itential Automation Gateway
License: MIT
"""

import unittest
import boto3
import json
import os
import sys
from unittest.mock import patch, Mock, MagicMock
from datetime import datetime, timezone, timedelta
from moto import mock_iam
import subprocess
import tempfile

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rotate_iam_keys import IAMKeyRotator, main


class TestWorkflowIntegrationContinued(unittest.TestCase):
    """Continued integration tests for complete workflow scenarios"""
    
    @mock_iam
    def test_monthly_rotation_workflow(self):
        """Test a complete monthly rotation workflow"""
        rotator = IAMKeyRotator(region='us-east-1')
        rotator.iam_client = boto3.client('iam', region_name='us-east-1')
        
        test_users = ['service-account-1', 'service-account-2', 'dev-user-1']
        
        for username in test_users:
            rotator.iam_client.create_user(UserName=username)
            rotator.iam_client.create_access_key(UserName=username)
        
        old_date = datetime.now(timezone.utc) - timedelta(days=95)
        
        with patch.object(rotator, 'get_users_with_old_keys') as mock_get_old:
            mock_old_keys = []
            for username in test_users[:2]:
                keys = rotator.iam_client.list_access_keys(UserName=username)
                key_id = keys['AccessKeyMetadata'][0]['AccessKeyId']
                mock_old_keys.append({
                    'username': username,
                    'access_key_id': key_id,
                    'create_date': old_date,
                    'age_days': 95,
                    'status': 'Active'
                })
            
            mock_get_old.return_value = mock_old_keys
            
            # Execute workflow
            old_keys = rotator.get_users_with_old_keys(days_threshold=90)
            rotation_results = []
            
            for key_info in old_keys:
                result = rotator.rotate_user_key(
                    key_info['username'],
                    key_info['access_key_id'],
                    dry_run=False
                )
                rotation_results.append(result)
            
            # Verify results
            successful_rotations = sum(1 for r in rotation_results if r['success'])
            self.assertEqual(successful_rotations, 2)
            self.assertEqual(len(rotation_results), 2)

    @mock_iam
    def test_enterprise_scale_workflow(self):
        """Test workflow with large number of users (enterprise scale)"""
        rotator = IAMKeyRotator(region='us-east-1')
        rotator.iam_client = boto3.client('iam', region_name='us-east-1')
        
        # Create 50 test users (simulating enterprise environment)
        enterprise_users = [f'enterprise-user-{i:03d}' for i in range(50)]
        
        for username in enterprise_users:
            rotator.iam_client.create_user(UserName=username)
            rotator.iam_client.create_access_key(UserName=username)
        
        # Mock 30% of users having old keys (15 users)
        users_with_old_keys = enterprise_users[:15]
        old_date = datetime.now(timezone.utc) - timedelta(days=120)
        
        with patch.object(rotator, 'get_users_with_old_keys') as mock_get_old:
            mock_old_keys = []
            for username in users_with_old_keys:
                keys = rotator.iam_client.list_access_keys(UserName=username)
                key_id = keys['AccessKeyMetadata'][0]['AccessKeyId']
                mock_old_keys.append({
                    'username': username,
                    'access_key_id': key_id,
                    'create_date': old_date,
                    'age_days': 120,
                    'status': 'Active'
                })
            
            mock_get_old.return_value = mock_old_keys
            
            # Execute enterprise workflow
            old_keys = rotator.get_users_with_old_keys(days_threshold=90)
            self.assertEqual(len(old_keys), 15)
            
            # Simulate batch processing
            rotation_results = []
            for key_info in old_keys:
                result = rotator.rotate_user_key(
                    key_info['username'],
                    key_info['access_key_id'],
                    dry_run=False
                )
                rotation_results.append(result)
            
            # Verify enterprise scale results
            successful_rotations = sum(1 for r in rotation_results if r['success'])
            self.assertEqual(successful_rotations, 15)

    @mock_iam
    def test_compliance_audit_workflow(self):
        """Test workflow that generates compliance audit data"""
        rotator = IAMKeyRotator(region='us-east-1')
        rotator.iam_client = boto3.client('iam', region_name='us-east-1')
        
        # Create audit scenario users
        audit_users = ['compliance-user-1', 'compliance-user-2', 'compliant-user-1']
        
        for username in audit_users:
            rotator.iam_client.create_user(UserName=username)
            rotator.iam_client.create_access_key(UserName=username)
        
        # Mock audit findings
        old_date = datetime.now(timezone.utc) - timedelta(days=100)
        
        with patch.object(rotator, 'get_users_with_old_keys') as mock_get_old:
            mock_old_keys = []
            # First 2 users have non-compliant keys
            for username in audit_users[:2]:
                keys = rotator.iam_client.list_access_keys(UserName=username)
                key_id = keys['AccessKeyMetadata'][0]['AccessKeyId']
                mock_old_keys.append({
                    'username': username,
                    'access_key_id': key_id,
                    'create_date': old_date,
                    'age_days': 100,
                    'status': 'Active'
                })
            
            mock_get_old.return_value = mock_old_keys
            
            # Generate compliance report
            old_keys = rotator.get_users_with_old_keys(days_threshold=90)
            
            compliance_report = {
                'audit_date': datetime.now(timezone.utc).isoformat(),
                'total_users_scanned': len(audit_users),
                'non_compliant_keys': len(old_keys),
                'compliance_rate': ((len(audit_users) - len(old_keys)) / len(audit_users)) * 100,
                'findings': old_keys
            }
            
            # Verify compliance metrics
            self.assertEqual(compliance_report['non_compliant_keys'], 2)
            self.assertAlmostEqual(compliance_report['compliance_rate'], 33.33, places=2)

    def test_iag_workflow_integration(self):
        """Test IAG workflow integration format"""
        with patch('rotate_iam_keys.IAMKeyRotator') as mock_rotator_class:
            mock_rotator = Mock()
            mock_rotator_class.return_value = mock_rotator
            
            # Mock successful rotation
            mock_rotator.get_users_with_old_keys.return_value = [
                {
                    'username': 'iag-test-user',
                    'access_key_id': 'AKIATEST12345',
                    'create_date': datetime.now(timezone.utc) - timedelta(days=100),
                    'age_days': 100,
                    'status': 'Active'
                }
            ]
            
            mock_rotator.rotate_user_key.return_value = {
                'username': 'iag-test-user',
                'old_key_id': 'AKIATEST12345',
                'new_key_id': 'AKIANEW67890',
                'new_secret_key': 'test-secret-key',
                'success': True,
                'error': None,
                'dry_run': False
            }
            
            # Simulate IAG execution with JSON output
            with patch('sys.argv', ['script', '--output-format', 'json']):
                with patch('sys.exit'):
                    with patch('builtins.print') as mock_print:
                        main()
                        
                        # Verify JSON output was generated
                        self.assertTrue(mock_print.called)
                        
                        # Check if output contains IAG-compatible structure
                        printed_args = [call[0][0] for call in mock_print.call_args_list]
                        json_output = None
                        
                        for arg in printed_args:
                            try:
                                json_output = json.loads(arg)
                                break
                            except (json.JSONDecodeError, TypeError):
                                continue
                        
                        if json_output:
                            self.assertIn('execution_time', json_output)
                            self.assertIn('rotated_keys', json_output)
                            self.assertIn('summary', json_output)


class TestErrorRecoveryIntegration(unittest.TestCase):
    """Integration tests for error recovery and resilience"""
    
    @mock_iam
    def test_partial_failure_recovery(self):
        """Test recovery from partial failures in batch operations"""
        rotator = IAMKeyRotator(region='us-east-1')
        rotator.iam_client = boto3.client('iam', region_name='us-east-1')
        
        # Create test users
        test_users = ['reliable-user-1', 'problem-user-1', 'reliable-user-2']
        
        for username in test_users:
            rotator.iam_client.create_user(UserName=username)
            rotator.iam_client.create_access_key(UserName=username)
        
        # Mock old keys for all users
        old_date = datetime.now(timezone.utc) - timedelta(days=100)
        
        with patch.object(rotator, 'get_users_with_old_keys') as mock_get_old:
            mock_old_keys = []
            for username in test_users:
                keys = rotator.iam_client.list_access_keys(UserName=username)
                key_id = keys['AccessKeyMetadata'][0]['AccessKeyId']
                mock_old_keys.append({
                    'username': username,
                    'access_key_id': key_id,
                    'create_date': old_date,
                    'age_days': 100,
                    'status': 'Active'
                })
            
            mock_get_old.return_value = mock_old_keys
            
            # Simulate failure for middle user
            original_rotate = rotator.rotate_user_key
            
            def mock_rotate_with_failure(username, old_key_id, dry_run=False):
                if username == 'problem-user-1':
                    return {
                        'username': username,
                        'old_key_id': old_key_id,
                        'new_key_id': None,
                        'success': False,
                        'error': 'Simulated failure',
                        'dry_run': dry_run
                    }
                return original_rotate(username, old_key_id, dry_run)
            
            rotator.rotate_user_key = mock_rotate_with_failure
            
            # Execute batch with partial failure
            old_keys = rotator.get_users_with_old_keys(days_threshold=90)
            rotation_results = []
            
            for key_info in old_keys:
                result = rotator.rotate_user_key(
                    key_info['username'],
                    key_info['access_key_id'],
                    dry_run=False
                )
                rotation_results.append(result)
            
            # Verify partial success
            successful_rotations = sum(1 for r in rotation_results if r['success'])
            failed_rotations = sum(1 for r in rotation_results if not r['success'])
            
            self.assertEqual(successful_rotations, 2)
            self.assertEqual(failed_rotations, 1)
            
            # Verify specific failure
            failed_result = next(r for r in rotation_results if not r['success'])
            self.assertEqual(failed_result['username'], 'problem-user-1')

    @mock_iam
    def test_cleanup_after_failure(self):
        """Test cleanup operations after rotation failures"""
        rotator = IAMKeyRotator(region='us-east-1')
        rotator.iam_client = boto3.client('iam', region_name='us-east-1')
        
        test_user = 'cleanup-after-failure-user'
        rotator.iam_client.create_user(UserName=test_user)
        
        initial_key_response = rotator.iam_client.create_access_key(UserName=test_user)
        initial_key_id = initial_key_response['AccessKey']['AccessKeyId']
        
        # Simulate failure after key creation but before deactivation
        with patch.object(rotator.iam_client, 'update_access_key') as mock_update:
            mock_update.side_effect = Exception("Simulated update failure")
            
            rotation_result = rotator.rotate_user_key(
                username=test_user,
                old_key_id=initial_key_id,
                dry_run=False
            )
            
            # Verify failure was handled gracefully
            self.assertFalse(rotation_result['success'])
            
            # Verify cleanup attempt (new key should be deleted)
            # This tests the cleanup logic in the exception handler
            final_keys = rotator.iam_client.list_access_keys(UserName=test_user)
            # Should have original key only (new key cleaned up)
            self.assertEqual(len(final_keys['AccessKeyMetadata']), 1)


if __name__ == '__main__':
    # Run integration tests
    unittest.main(verbosity=2)
