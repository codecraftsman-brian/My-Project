"""
Scheduler package for Telegram Message Scheduler.
This package handles the core functionality of the scheduler.
"""

from scheduler.models import TelegramScheduler

def create_scheduler(data_dir):
    """Create a new scheduler instance."""
    return TelegramScheduler(data_dir=data_dir)