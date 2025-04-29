"""
Core functionality for the Telegram Message Scheduler.
This module contains the TelegramScheduler class which handles
connecting to Telegram and sending scheduled messages.
"""

import os
import json
import random
import logging
import asyncio
from datetime import datetime, timedelta

from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError

from scheduler.utils import ensure_file_exists

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


class TelegramScheduler:
    """
    Main scheduler class for handling Telegram message scheduling.
    """
    
    def __init__(self, data_dir):
        """Initialize the Telegram Scheduler with configuration."""
        self.data_dir = data_dir
        self.config_file = os.path.join(data_dir, 'config.json')
        self.message_file = os.path.join(data_dir, 'messages.json')
        self.sent_log_file = os.path.join(data_dir, 'sent_log.json')
        
        # Ensure directories and files exist
        os.makedirs(data_dir, exist_ok=True)
        ensure_file_exists(self.config_file, {
            "api_id": 0,
            "api_hash": "",
            "phone": "",
            "wait_time_min": 30,
            "wait_time_max": 60,
        })
        
        # Load configuration and data
        with open(self.config_file, 'r') as f:
            self.config = json.load(f)
            
        self.client = None
        self.messages = []
        self.targets = []
        self.sent_history = {}
        self.auth_code = None
        self.auth_password = None
        self.continue_running = True
        
        self.load_data()
        
    def load_data(self):
        """Load messages and sent history from files."""
        # Load messages and targets
        ensure_file_exists(self.message_file, {
            "messages": [
                "Hello! This is a test message.",
                "How are you doing today?",
                "Welcome to our channel!"
            ],
            "targets": [
                {"name": "Group 1", "id": "username1", "type": "group"},
                {"name": "Person 1", "id": "username2", "type": "user"},
                {"name": "Channel 1", "id": "username3", "type": "channel"}
            ]
        })
        
        with open(self.message_file, 'r') as f:
            data = json.load(f)
            self.messages = data.get('messages', [])
            self.targets = data.get('targets', [])
            
        # Load sent history
        ensure_file_exists(self.sent_log_file, {"last_cycle": 0, "sent": {}})
        
        with open(self.sent_log_file, 'r') as f:
            self.sent_history = json.load(f)
            
    def save_sent_history(self):
        """Save the sent message history to a file."""
        with open(self.sent_log_file, 'w') as f:
            json.dump(self.sent_history, f, indent=4)
            
    def _save_messages(self):
        """Save messages and targets to the messages file."""
        data = {
            "messages": self.messages,
            "targets": self.targets
        }
        with open(self.message_file, 'w') as f:
            json.dump(data, f, indent=4)
            
    async def connect(self):
        """Connect to Telegram API."""
        api_id = self.config.get('api_id')
        api_hash = self.config.get('api_hash')
        phone = self.config.get('phone')
        
        if not api_id or not api_hash or not phone:
            logger.error("API credentials are missing in config.json")
            return False
        
        # Connect to Telegram
        session_file = os.path.join(self.data_dir, 'telegram_scheduler_session')
        self.client = TelegramClient(session_file, api_id, api_hash)
        await self.client.start()
        
        # Check if already authorized
        if not await self.client.is_user_authorized():
            await self.client.send_code_request(phone)
            
            # Wait for auth code to be set by web interface
            max_wait = 60  # Wait max 60 seconds for code
            wait_count = 0
            while not self.auth_code and wait_count < max_wait:
                await asyncio.sleep(1)
                wait_count += 1
                
            if not self.auth_code:
                logger.error("No authentication code provided within timeout period")
                return False
                
            try:
                await self.client.sign_in(phone, self.auth_code)
                self.auth_code = None  # Reset after use
            except SessionPasswordNeededError:
                # Wait for 2FA password to be set by web interface
                max_wait = 60
                wait_count = 0
                while not self.auth_password and wait_count < max_wait:
                    await asyncio.sleep(1)
                    wait_count += 1
                    
                if not self.auth_password:
                    logger.error("No 2FA password provided within timeout period")
                    return False
                    
                await self.client.sign_in(password=self.auth_password)
                self.auth_password = None  # Reset after use
                
        logger.info("Successfully connected to Telegram")
        return True
    
    def get_random_message(self):
        """Get a random message from the list."""
        if not self.messages:
            logger.error("No messages available")
            return None
        return random.choice(self.messages)
    
    def get_unsent_targets(self, current_cycle):
        """Get targets that haven't received messages in the current cycle."""
        if str(current_cycle) not in self.sent_history.get('sent', {}):
            self.sent_history['sent'][str(current_cycle)] = []
            
        sent_to = self.sent_history['sent'][str(current_cycle)]
        unsent = [target for target in self.targets if target['id'] not in sent_to]
        
        if not unsent:  # If all targets have been messaged, start a new cycle
            logger.info(f"Cycle {current_cycle} completed. Starting new cycle.")
            new_cycle = current_cycle + 1
            self.sent_history['sent'][str(new_cycle)] = []
            self.sent_history['last_cycle'] = new_cycle
            self.save_sent_history()
            return self.targets
        
        return unsent
    
    async def send_message_to_target(self, target, message):
        """Send a message to a specific target."""
        try:
            if target['type'] == 'user':
                entity = await self.client.get_entity(target['id'])
                await self.client.send_message(entity, message)
            elif target['type'] in ['group', 'channel']:
                entity = await self.client.get_entity(target['id'])
                await self.client.send_message(entity, message)
            
            logger.info(f"Message sent to {target['name']} ({target['id']})")
            return True
        except Exception as e:
            logger.error(f"Failed to send message to {target['name']}: {str(e)}")
            return False
            
    async def send_batch(self, batch_size=3):
        """Send messages to a batch of random targets."""
        current_cycle = self.sent_history.get('last_cycle', 0)
        unsent_targets = self.get_unsent_targets(current_cycle)
        
        if len(unsent_targets) == 0:
            logger.warning("No targets available to send messages to")
            return 0
            
        # Select up to batch_size random targets
        batch = random.sample(unsent_targets, min(batch_size, len(unsent_targets)))
        sent_count = 0
        
        for target in batch:
            message = self.get_random_message()
            if not message:
                continue
                
            success = await self.send_message_to_target(target, message)
            if success:
                sent_count += 1
                if str(current_cycle) not in self.sent_history['sent']:
                    self.sent_history['sent'][str(current_cycle)] = []
                self.sent_history['sent'][str(current_cycle)].append(target['id'])
                self.save_sent_history()
                
        return sent_count
                
    async def run_scheduler(self):
        """Run the scheduler continuously."""
        if not await self.connect():
            logger.error("Failed to connect to Telegram API")
            return
            
        self.continue_running = True
        
        while self.continue_running:
            # Send a batch of messages
            sent = await self.send_batch(batch_size=random.randint(1, 4))
            logger.info(f"Sent {sent} messages in this batch")
            
            # Wait for random time interval
            wait_min = self.config.get('wait_time_min', 30)
            wait_max = self.config.get('wait_time_max', 60)
            wait_time = random.randint(wait_min, wait_max)
            
            next_time = datetime.now() + timedelta(minutes=wait_time)
            logger.info(f"Next batch will be sent at {next_time.strftime('%H:%M:%S')}")
            
            # Convert minutes to seconds and wait, but check every second if we should stop
            for _ in range(wait_time * 60):
                if not self.continue_running:
                    logger.info("Scheduler stop requested during wait time")
                    return
                await asyncio.sleep(1)
    
    def add_message(self, message):
        """Add a new message to the list."""
        self.messages.append(message)
        self._save_messages()
        
    def add_target(self, name, id, type):
        """Add a new target."""
        if type not in ['user', 'group', 'channel']:
            logger.error(f"Invalid target type: {type}")
            return False
            
        self.targets.append({
            "name": name,
            "id": id,
            "type": type
        })
        self._save_messages()
        return True
        
    def reset_cycle(self):
        """Reset the current sending cycle."""
        current_cycle = self.sent_history.get('last_cycle', 0)
        new_cycle = current_cycle + 1
        self.sent_history['sent'][str(new_cycle)] = []
        self.sent_history['last_cycle'] = new_cycle
        self.save_sent_history()
        logger.info(f"Reset to new cycle: {new_cycle}")