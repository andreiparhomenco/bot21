"""
Application settings and configuration
Loads from environment variables
"""
import os
import json
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
    
    # Google Credentials - support for Railway deployment
    # Try to load from environment variable first (for Railway/Docker)
    @staticmethod
    def _setup_credentials_path():
        """Setup Google credentials, supporting Railway environment variable"""
        if os.getenv("GOOGLE_CREDENTIALS"):
            try:
                # Create credentials from environment variable
                credentials_data = json.loads(os.getenv("GOOGLE_CREDENTIALS"))
                credentials_path = "/tmp/google_credentials.json"
                Path(credentials_path).parent.mkdir(exist_ok=True)
                with open(credentials_path, 'w') as f:
                    json.dump(credentials_data, f)
                print(f"✓ Created credentials file from GOOGLE_CREDENTIALS env var: {credentials_path}")
                return credentials_path
            except json.JSONDecodeError as e:
                print(f"✗ Error parsing GOOGLE_CREDENTIALS: {e}")
                # Fall back to default path
                return os.getenv("CREDENTIALS_PATH", "credentials/google_credentials.json")
        else:
            # Use file path from environment or default
            return os.getenv("CREDENTIALS_PATH", "credentials/google_credentials.json")
    
    CREDENTIALS_PATH: str = _setup_credentials_path.__func__()
    
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
        
        # Check credentials: either file exists OR GOOGLE_CREDENTIALS env var is set
        if not os.getenv("GOOGLE_CREDENTIALS") and not Path(cls.CREDENTIALS_PATH).exists():
            errors.append(f"Google credentials not found: set GOOGLE_CREDENTIALS env var or provide {cls.CREDENTIALS_PATH}")
        
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

