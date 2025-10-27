"""
Main entry point for GoalBuddy21 Telegram bot
Initializes and runs the application
"""
import sys
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters

from config.settings import settings
from utils.logger import logger
from bot.handlers import (
    start_command,
    assess_command,
    handle_text_message,
    handle_progress_callback,
    error_handler,
)
from scheduler import tasks as scheduler_module
from database.sheets import db


def main() -> None:
    """Main function to run the bot"""
    
    # Display banner
    print("\n" + "="*50)
    print("  GoalBuddy21 - Telegram Bot")
    print("="*50)
    
    # Display and validate configuration
    settings.display()
    
    if not settings.validate():
        logger.error("Configuration validation failed")
        sys.exit(1)
    
    logger.info("Starting GoalBuddy21 bot...")
    
    try:
        # Create application
        application = Application.builder().token(settings.BOT_TOKEN).build()
        
        # Initialize scheduler
        scheduler_module.initialize_scheduler()
        
        # Restore pending reminders
        scheduler_module.restore_pending_reminders(application.bot, db)
        
        # Register handlers
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("assess", assess_command))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message))
        application.add_handler(CallbackQueryHandler(handle_progress_callback))
        
        # Register error handler
        application.add_error_handler(error_handler)
        
        # Set up bot commands (shown in menu)
        async def setup_bot_commands(app):
            await app.bot.set_my_commands([
                ("start", "Начать работу и поставить цель"),
                ("assess", "Оценить свой прогресс (0-100%)"),
            ])
            logger.info("✅ Bot commands set up")
        
        application.post_init = setup_bot_commands
        
        logger.info("✅ All handlers registered")
        logger.info("✅ Bot is ready and polling for updates...")
        
        # Run bot
        application.run_polling()
        
    except KeyboardInterrupt:
        logger.info("\nShutting down gracefully...")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)
    finally:
        # Cleanup
        if scheduler_module.scheduler:
            scheduler_module.scheduler.shutdown()
        logger.info("Bot stopped")


if __name__ == "__main__":
    main()

