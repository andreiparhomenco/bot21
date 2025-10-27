"""
Application settings and configuration
Loads from environment variables
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """Application settings loaded from environment"""
    
    # Telegram Bot
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
    
    # Google Sheets
    SPREADSHEET_ID: str = os.getenv("SPREADSHEET_ID", "")
    CREDENTIALS_PATH: str = os.getenv("CREDENTIALS_PATH", "credentials/google_credentials.json")
    
    # Scheduler
    SCHEDULER_TIMEZONE: str = os.getenv("SCHEDULER_TIMEZONE", "Europe/Moscow")
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", "logs/bot.log")
    
    # Testing mode (shortens delays for testing)
    TESTING_MODE: bool = os.getenv("TESTING_MODE", "False").lower() == "true"
    
    # Reminder delay (1 minute for testing, 24 hours for production)
    REMINDER_DELAY_SECONDS: int = 60 if TESTING_MODE else 86400  # 24 * 60 * 60
    
    @classmethod
    def validate(cls) -> bool:
        """
        Validate that all required settings are present
        
        Returns:
            True if valid, False otherwise
        """
        errors = []
        
        if not cls.BOT_TOKEN:
            errors.append("BOT_TOKEN is not set")
        
        if not cls.SPREADSHEET_ID:
            errors.append("SPREADSHEET_ID is not set")
        
        if not Path(cls.CREDENTIALS_PATH).exists():
            errors.append(f"Google credentials file not found: {cls.CREDENTIALS_PATH}")
        
        if errors:
            print("Configuration errors:")
            for error in errors:
                print(f"  - {error}")
            return False
        
        return True
    
    @classmethod
    def display(cls) -> None:
        """Display current configuration (hiding sensitive data)"""
        print("\nGoalBuddy21 Configuration:")
        print(f"  Bot Token: {'Set' if cls.BOT_TOKEN else 'Not set'}")
        print(f"  Spreadsheet ID: {'Set' if cls.SPREADSHEET_ID else 'Not set'}")
        print(f"  Credentials Path: {cls.CREDENTIALS_PATH}")
        print(f"  Timezone: {cls.SCHEDULER_TIMEZONE}")
        print(f"  Log Level: {cls.LOG_LEVEL}")
        print(f"  Testing Mode: {'ON (1 min delays)' if cls.TESTING_MODE else 'OFF (24h delays)'}")
        print()


# Create settings instance
settings = Settings()

