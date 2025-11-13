"""
Google Sheets database integration
Handles all data storage and retrieval
"""
import time
from datetime import datetime
from typing import List, Dict, Any, Optional

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from config.settings import settings
from utils.logger import logger
from utils.validators import escape_for_sheets
from bot.states import UserState


class SheetsDatabase:
    """Manages Google Sheets as database"""
    
    def __init__(self):
        """Initialize connection to Google Sheets"""
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]
        
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            settings.CREDENTIALS_PATH,
            scope
        )
        
        client = gspread.authorize(creds)
        self.spreadsheet = client.open_by_key(settings.SPREADSHEET_ID)
        
        # Get or create worksheets
        self.user_data_sheet = self._get_or_create_worksheet("UserData")
        self.analytics_sheet = self._get_or_create_worksheet("Analytics")
        
        # Initialize headers if sheets are new
        if self.user_data_sheet.row_count == 0 or not self.user_data_sheet.get('A1'):
            self._initialize_user_data_headers()
        
        if self.analytics_sheet.row_count == 0 or not self.analytics_sheet.get('A1'):
            self._initialize_analytics_sheet()
        
        logger.info("✅ Successfully connected to Google Sheets")
    
    def _get_or_create_worksheet(self, title: str):
        """Get existing worksheet or create new one"""
        try:
            return self.spreadsheet.worksheet(title)
        except gspread.exceptions.WorksheetNotFound:
            return self.spreadsheet.add_worksheet(title=title, rows=1000, cols=20)
    
    def _initialize_user_data_headers(self):
        """Initialize UserData sheet with column headers"""
        headers = [
            "goal_text", "goal_date", "final_percent", "final_date"
        ]
        self.user_data_sheet.append_row(headers)
        logger.info("✅ Initialized UserData sheet headers")
    
    def _initialize_analytics_sheet(self):
        """Initialize Analytics sheet with formulas"""
        # TODO: Add analytics formulas in a later phase
        self.analytics_sheet.append_row(["Статистика по интенсиву"])
        logger.info("✅ Initialized Analytics sheet")
    
    def _retry_on_rate_limit(self, func, *args, **kwargs):
        """Retry function on rate limit errors"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs)
            except gspread.exceptions.APIError as e:
                if attempt < max_retries - 1 and "RATE_LIMIT_EXCEEDED" in str(e):
                    wait_time = 2 ** attempt  # Exponential backoff
                    logger.warning(f"Rate limit hit, waiting {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    raise
    
    def save_user_goal(self, goal_text: str) -> Optional[int]:
        """
        Save anonymous user goal with security escaping
        
        Args:
            goal_text: User's goal text
            
        Returns:
            Row number of the saved goal, or None if failed
            
        Security:
            - Applies escape_for_sheets to prevent CSV/Formula injection
        """
        try:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Escape goal_text to prevent CSV/Formula injection
            safe_goal_text = escape_for_sheets(goal_text)
            
            # Always insert new anonymous record
            row_data = [safe_goal_text, now, "", ""]
            self._retry_on_rate_limit(self.user_data_sheet.append_row, row_data)
            
            # Get the row number of the newly added record
            all_data = self._retry_on_rate_limit(self.user_data_sheet.get_all_values)
            row_number = len(all_data)  # Last row
            
            logger.info(f"✅ Saved anonymous goal to row {row_number}")
            return row_number
            
        except Exception as e:
            logger.error(f"❌ Error saving user goal: {e}")
            return None
    
    def get_goal_by_row(self, row_number: int) -> Optional[str]:
        """
        Get goal text by row number
        
        Args:
            row_number: Row number in the sheet
            
        Returns:
            Goal text or None if not found
        """
        try:
            cell_value = self._retry_on_rate_limit(
                self.user_data_sheet.cell,
                row_number,
                1  # Column A - goal_text
            )
            return cell_value.value if cell_value else None
            
        except Exception as e:
            logger.error(f"❌ Error getting goal by row: {e}")
            return None
    
    
    def save_final_assessment(self, row_number: int, percent: int) -> bool:
        """
        Save final self-assessment for anonymous record
        
        Args:
            row_number: Row number in the sheet
            percent: Self-assessment percentage (0-100)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Update columns C and D (final_percent, final_date)
            self._retry_on_rate_limit(
                self.user_data_sheet.update,
                f'C{row_number}:D{row_number}',
                [[percent, now]]
            )
            
            logger.info(f"✅ Saved final assessment for row {row_number}: {percent}%")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error saving final assessment: {e}")
            return False


# Lazy initialization of database
_db_instance = None


def get_db() -> SheetsDatabase:
    """Get or create database instance (lazy initialization)"""
    global _db_instance
    if _db_instance is None:
        _db_instance = SheetsDatabase()
    return _db_instance


# For backward compatibility
db = None  # Will be initialized on first use

