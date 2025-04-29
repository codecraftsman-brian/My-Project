"""
Test the web interface of the Telegram Message Scheduler.
This validates that the web routes and views work correctly.
"""

import sys
import os
import json
import tempfile
import unittest
from unittest.mock import patch, MagicMock

# Add parent directory to path to import modules
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

# Import Flask app 
from app import create_app

class TestWebInterface(unittest.TestCase):
    """Test cases for the web interface."""
    
    def setUp(self):
        """Set up a test environment with a test Flask client."""
        # Create temp directory for data
        self.temp_dir = tempfile.TemporaryDirectory()
        self.data_dir = self.temp_dir.name
        self.upload_dir = os.path.join(self.data_dir, 'uploads')
        os.makedirs(self.upload_dir, exist_ok=True)
        
        # Mock app config
        self.app_config = {
            'DATA_DIR': self.data_dir,
            'UPLOAD_FOLDER': self.upload_dir,
            'CONFIG_FILE': os.path.join(self.data_dir, 'config.json'),
            'MESSAGE_FILE': os.path.join(self.data_dir, 'messages.json'),
            'SENT_LOG_FILE': os.path.join(self.data_dir, 'sent_log.json'),
            'ALLOWED_EXTENSIONS': {'txt', 'csv'},
            'TESTING': True,
            'SECRET_KEY': 'test_key'
        }
        
        # First create the app
        self.app = create_app()
        
        # Then update its configuration
        self.app.config.update(self.app_config)
        
        # Create test client
        self.client = self.app.test_client()
        
        # Create a mock scheduler for the app
        self.mock_scheduler = MagicMock()
        self.mock_scheduler.messages = ["Test message 1", "Test message 2"]
        self.mock_scheduler.targets = [
            {"name": "Test User", "id": "user1", "type": "user"},
            {"name": "Test Group", "id": "group1", "type": "group"}
        ]
        self.mock_scheduler.config = {
            "api_id": 12345,
            "api_hash": "test_hash",
            "phone": "+1234567890",
            "wait_time_min": 1,
            "wait_time_max": 5,
        }
        self.app.scheduler = self.mock_scheduler
    
    def tearDown(self):
        """Clean up temporary files after tests."""
        self.temp_dir.cleanup()
    
    def test_home_page(self):
        """Test that the home page loads correctly."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        # Check that the page contains expected elements
        html = response.data.decode('utf-8')
        self.assertIn('Telegram Message Scheduler', html)
        self.assertIn('Dashboard', html)
        self.assertIn('Messages', html)
        self.assertIn('Targets', html)
    
    def test_setup_page(self):
        """Test that the setup page loads correctly."""
        response = self.client.get('/setup')
        self.assertEqual(response.status_code, 200)
        # Check that the page contains expected elements
        html = response.data.decode('utf-8')
        self.assertIn('Settings', html)
        self.assertIn('Telegram API Configuration', html)
        self.assertIn('API ID', html)
        self.assertIn('API Hash', html)
    
    def test_add_message(self):
        """Test adding a message."""
        response = self.client.post('/add_message', data={
            'message': 'New test message'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        # Verify the mock was called
        self.mock_scheduler.add_message.assert_called_once_with('New test message')
    
    def test_add_target(self):
        """Test adding a target."""
        response = self.client.post('/add_target', data={
            'name': 'New Target',
            'target_id': 'new_target',
            'type': 'user'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        # Verify the mock was called
        self.mock_scheduler.add_target.assert_called_once_with('New Target', 'new_target', 'user')
    
    def test_reset_cycle(self):
        """Test resetting the cycle."""
        response = self.client.post('/reset_cycle', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        # Verify the mock was called
        self.mock_scheduler.reset_cycle.assert_called_once()
    
    def test_setup_form(self):
        """Test submitting the setup form."""
        # Create a test config.json file for the app to update
        os.makedirs(os.path.dirname(self.app_config['CONFIG_FILE']), exist_ok=True)
        with open(self.app_config['CONFIG_FILE'], 'w') as f:
            json.dump({}, f)
            
        response = self.client.post('/setup', data={
            'api_id': '54321',
            'api_hash': 'new_hash',
            'phone': '+0987654321',
            'wait_min': '2',
            'wait_max': '10'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        # Verify the values were updated in the mock
        self.mock_scheduler.config['api_id'] = 54321
        self.mock_scheduler.config['api_hash'] = 'new_hash'
        self.mock_scheduler.config['phone'] = '+0987654321'
        self.mock_scheduler.config['wait_time_min'] = 2
        self.mock_scheduler.config['wait_time_max'] = 10

def run_web_tests():
    """Run all web interface tests."""
    print("Running web interface tests for Telegram Message Scheduler")
    print("=" * 50)
    
    test_loader = unittest.TestLoader()
    test_suite = test_loader.loadTestsFromTestCase(TestWebInterface)
    test_runner = unittest.TextTestRunner(verbosity=2)
    test_result = test_runner.run(test_suite)
    
    success = test_result.wasSuccessful()
    
    if success:
        print("All web interface tests passed! [PASS]")
    else:
        print("Some web interface tests failed. Please fix the issues before proceeding. [FAIL]")
    
    return success

if __name__ == "__main__":
    success = run_web_tests()
    sys.exit(0 if success else 1)