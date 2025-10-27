"""
Scheduler for automated tasks (reminders, etc.)
Uses APScheduler for background job execution
"""
from datetime import datetime, timedelta
from typing import Optional

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from telegram import Bot
from telegram.error import TelegramError

from config.settings import settings
from utils.logger import logger
from bot.states import UserState
from bot.messages import REMINDER_MESSAGE
from bot.keyboards import get_progress_keyboard


# Global scheduler instance
scheduler: Optional[BackgroundScheduler] = None


def initialize_scheduler() -> BackgroundScheduler:
    """
    Initialize and start the scheduler
    
    Returns:
        BackgroundScheduler instance
    """
    global scheduler
    
    if scheduler is None:
        scheduler = BackgroundScheduler(timezone=settings.SCHEDULER_TIMEZONE)
        scheduler.start()
        logger.info("✅ Scheduler started")
    
    return scheduler


async def send_day2_reminder(bot: Bot, user_id: int, username: str, goal_text: str):
    """
    Send Day 2 reminder to user
    
    Args:
        bot: Telegram Bot instance
        user_id: User's Telegram ID
        username: User's username
        goal_text: User's goal text
    """
    try:
        message = REMINDER_MESSAGE.format(username=username, goal=goal_text)
        keyboard = get_progress_keyboard()
        
        await bot.send_message(
            chat_id=user_id,
            text=message,
            reply_markup=keyboard,
            parse_mode='Markdown'
        )
        
        logger.info(f"✅ Sent Day 2 reminder to user {user_id}")
        
    except TelegramError as e:
        logger.error(f"❌ Failed to send reminder to user {user_id}: {e}")
    except Exception as e:
        logger.error(f"❌ Unexpected error sending reminder to user {user_id}: {e}")


def schedule_day2_reminder(bot: Bot, user_id: int, username: str, goal_text: str):
    """
    Schedule a Day 2 reminder for a user
    
    Args:
        bot: Telegram Bot instance
        user_id: User's Telegram ID
        username: User's username
        goal_text: User's goal text
    """
    global scheduler
    
    if scheduler is None:
        scheduler = initialize_scheduler()
    
    # Calculate reminder time (24 hours from now, or 1 minute in testing mode)
    reminder_time = datetime.now() + timedelta(seconds=settings.REMINDER_DELAY_SECONDS)
    
    # Schedule the job
    job_id = f"reminder_{user_id}"
    
    # Remove existing job if any
    existing_job = scheduler.get_job(job_id)
    if existing_job:
        existing_job.remove()
    
    # Add new job
    scheduler.add_job(
        func=lambda: _sync_send_reminder(bot, user_id, username, goal_text),
        trigger=DateTrigger(run_date=reminder_time),
        id=job_id,
        replace_existing=True,
        name=f"Day 2 reminder for user {user_id}"
    )
    
    delay_minutes = settings.REMINDER_DELAY_SECONDS // 60
    logger.info(f"✅ Scheduled Day 2 reminder for user {user_id} in {delay_minutes} minutes")


def _sync_send_reminder(bot: Bot, user_id: int, username: str, goal_text: str):
    """
    Synchronous wrapper for sending reminder (for APScheduler)
    """
    import asyncio
    
    try:
        # Create new event loop for this thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(send_day2_reminder(bot, user_id, username, goal_text))
        loop.close()
    except Exception as e:
        logger.error(f"❌ Error in sync reminder wrapper: {e}")


def restore_pending_reminders(bot: Bot, db):
    """
    Restore pending reminders on bot startup
    Checks for users in GOAL_SET state and reschedules reminders if needed
    
    Args:
        bot: Telegram Bot instance
        db: Database instance
    """
    try:
        users_with_goals = db.get_users_by_state(UserState.GOAL_SET)
        
        if not users_with_goals:
            logger.info("No pending reminders to restore")
            return
        
        for user in users_with_goals:
            # Parse goal date and check if reminder should be sent
            goal_date_str = user.get('goal_date', '')
            if not goal_date_str:
                continue
            
            try:
                goal_date = datetime.strptime(goal_date_str, "%Y-%m-%d %H:%M:%S")
                reminder_time = goal_date + timedelta(seconds=settings.REMINDER_DELAY_SECONDS)
                
                # If reminder time is in the future, reschedule it
                if reminder_time > datetime.now():
                    schedule_day2_reminder(
                        bot,
                        user['user_id'],
                        user['username'],
                        user['goal_text']
                    )
                    logger.info(f"✅ Restored reminder for user {user['user_id']}")
                    
            except ValueError as e:
                logger.error(f"❌ Error parsing date for user {user['user_id']}: {e}")
                continue
        
        logger.info(f"✅ Restored {len(users_with_goals)} pending reminders")
        
    except Exception as e:
        logger.error(f"❌ Error restoring pending reminders: {e}")


def shutdown_scheduler():
    """Gracefully shutdown the scheduler"""
    global scheduler
    
    if scheduler:
        scheduler.shutdown()
        logger.info("✅ Scheduler shut down")

