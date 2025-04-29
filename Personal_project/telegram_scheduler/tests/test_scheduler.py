"""
Test the core functionality of the Telegram Message Scheduler.
This validates that the scheduler logic works correctly.
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

# Import scheduler
from scheduler.models import TelegramScheduler

class TestTelegramScheduler(unittest.TestCase):
    """Test cases for TelegramScheduler class."""
    
    def setUp(self):
        """Set up a test environment with a temporary data directory."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.data_dir = self.temp_dir.name
        
        # Create test config file
        config_file = os.path.join(self.data_dir, 'config.json')
        with open(config_file, 'w') as f:
            json.dump({
                "api_id": 12345,
                "api_hash": "test_hash",
                "phone": "+1234567890",
                "wait_time_min": 1,
                "wait_time_max": 5,
            }, f)
        
        # Create test messages file
        messages_file = os.path.join(self.data_dir, 'messages.json')
        with open(messages_file, 'w') as f:
            json.dump({
                "messages": ["Test message 1", "Test message 2"],
                "targets": [
                    {"name": "Test User", "id": "user1", "type": "user"},
                    {"name": "Test Group", "id": "group1", "type": "group"}
                ]
            }, f)
        
        # Create test sent log file
        sent_log_file = os.path.join(self.data_dir, 'sent_log.json')
        with open(sent_log_file, 'w') as f:
            json.dump({"last_cycle": 0, "sent": {"0": []}}, f)
        
        # Create the scheduler with test data
        self.scheduler = TelegramScheduler(self.data_dir)
    
    def tearDown(self):
        """Clean up temporary files after tests."""
        self.temp_dir.cleanup()
    
    def test_initialization(self):
        """Test that the scheduler initializes correctly."""
        self.assertEqual(self.scheduler.config['api_id'], 12345)
        self.assertEqual(self.scheduler.config['api_hash'], "test_hash")
        self.assertEqual(len(self.scheduler.messages), 2)
        self.assertEqual(len(self.scheduler.targets), 2)
        self.assertEqual(self.scheduler.sent_history['last_cycle'], 0)
    
    def test_add_message(self):
        """Test adding a message."""
        initial_count = len(self.scheduler.messages)
        self.scheduler.add_message("New test message")
        self.assertEqual(len(self.scheduler.messages), initial_count + 1)
        self.assertIn("New test message", self.scheduler.messages)
    
    def test_add_target(self):
        """Test adding a target."""
        initial_count = len(self.scheduler.targets)
        result = self.scheduler.add_target("New User", "new_user", "user")
        self.assertTrue(result)
        self.assertEqual(len(self.scheduler.targets), initial_count + 1)
        
        # Test adding an invalid target type
        result = self.scheduler.add_target("Invalid", "invalid", "invalid_type")
        self.assertFalse(result)
        self.assertEqual(len(self.scheduler.targets), initial_count + 1)
    
    def test_get_unsent_targets(self):
        """Test getting unsent targets."""
        # All targets should be unsent initially
        unsent = self.scheduler.get_unsent_targets(0)
        self.assertEqual(len(unsent), 2)
        
        # Mark one target as sent
        self.scheduler.sent_history['sent']['0'] = ["user1"]
        self.scheduler.save_sent_history()
        
        unsent = self.scheduler.get_unsent_targets(0)
        self.assertEqual(len(unsent), 1)
        self.assertEqual(unsent[0]['id'], "group1")
        
        # Mark all targets as sent, should start a new cycle
        self.scheduler.sent_history['sent']['0'] = ["user1", "group1"]
        self.scheduler.save_sent_history()
        
        unsent = self.scheduler.get_unsent_targets(0)
        self.assertEqual(len(unsent), 2)  # All targets in the new cycle
        self.assertEqual(self.scheduler.sent_history['last_cycle'], 1)
    
    def test_reset_cycle(self):
        """Test resetting the cycle."""
        initial_cycle = self.scheduler.sent_history['last_cycle']
        self.scheduler.reset_cycle()
        self.assertEqual(self.scheduler.sent_history['last_cycle'], initial_cycle + 1)
        self.assertEqual(self.scheduler.sent_history['sent'][str(initial_cycle + 1)], [])
    
    @patch('scheduler.models.TelegramClient')
    async def test_connect(self, mock_client):
        """Test connecting to Telegram API."""
        # Mock the client and its methods
        mock_client_instance = MagicMock()
        mock_client.return_value = mock_client_instance
        mock_client_instance.start.return_value = None
        mock_client_instance.is_user_authorized.return_value = True
        
        # Test connection
        result = await self.scheduler.connect()
        self.assertTrue(result)
        
        # Verify calls
        mock_client.assert_called_once()
        mock_client_instance.start.assert_called_once()
        mock_client_instance.is_user_authorized.assert_called_once()

def run_scheduler_tests():
    """Run all scheduler tests."""
    print("Running scheduler tests for Telegram Message Scheduler")
    print("=" * 50)
    
    test_loader = unittest.TestLoader()
    test_suite = test_loader.loadTestsFromTestCase(TestTelegramScheduler)
    test_runner = unittest.TextTestRunner(verbosity=2)
    test_result = test_runner.run(test_suite)
    
    success = test_result.wasSuccessful()
    
    if success:
        print("All scheduler tests passed! [PASS]")
    else:
        print("Some scheduler tests failed. Please fix the issues before proceeding. [FAIL]")
    
    return success

if __name__ == "__main__":
    success = run_scheduler_tests()
    sys.exit(0 if success else 1)