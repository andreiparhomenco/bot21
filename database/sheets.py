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
            "user_id", "username", "full_name", "goal_text", "goal_date",
            "progress_day2", "progress_date", "final_percent", "final_date",
            "current_state"
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
    
    def save_user_goal(
        self,
        user_id: int,
        username: str,
        full_name: str,
        goal_text: str
    ) -> bool:
        """
        Save user's goal (Day 1)
        
        Args:
            user_id: Telegram user ID
            username: Telegram username
            full_name: User's full name
            goal_text: User's goal text
            
        Returns:
            True if successful, False otherwise
        """
        try:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Check if user already exists
            existing_user = self.get_user_data(user_id)
            
            if existing_user:
                # Update existing user's goal
                row_num = existing_user['row_number']
                self._retry_on_rate_limit(
                    self.user_data_sheet.update,
                    f'D{row_num}:E{row_num}',
                    [[goal_text, now]]
                )
                self._retry_on_rate_limit(
                    self.user_data_sheet.update,
                    f'J{row_num}',
                    [[UserState.GOAL_SET.value]]
                )
                logger.info(f"✅ Updated goal for user {user_id}")
            else:
                # Insert new user
                row_data = [
                    user_id, username, full_name, goal_text, now,
                    "", "", "", "", UserState.GOAL_SET.value
                ]
                self._retry_on_rate_limit(self.user_data_sheet.append_row, row_data)
                logger.info(f"✅ Saved new goal for user {user_id}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error saving user goal: {e}")
            return False
    
    def get_user_data(self, user_id: int) -> Optional[Dict[str, Any]]:
        """
        Get user data by user_id
        
        Args:
            user_id: Telegram user ID
            
        Returns:
            Dict with user data or None if not found
        """
        try:
            all_data = self._retry_on_rate_limit(self.user_data_sheet.get_all_values)
            
            for idx, row in enumerate(all_data[1:], start=2):  # Skip header row
                if row and str(row[0]) == str(user_id):
                    return {
                        'row_number': idx,
                        'user_id': row[0],
                        'username': row[1] if len(row) > 1 else "",
                        'full_name': row[2] if len(row) > 2 else "",
                        'goal_text': row[3] if len(row) > 3 else "",
                        'goal_date': row[4] if len(row) > 4 else "",
                        'progress_day2': row[5] if len(row) > 5 else "",
                        'progress_date': row[6] if len(row) > 6 else "",
                        'final_percent': row[7] if len(row) > 7 else "",
                        'final_date': row[8] if len(row) > 8 else "",
                        'current_state': row[9] if len(row) > 9 else UserState.IDLE.value
                    }
            
            return None
            
        except Exception as e:
            logger.error(f"❌ Error getting user data: {e}")
            return None
    
    def update_progress_day2(
        self,
        user_id: int,
        progress_option: str
    ) -> bool:
        """
        Update user's Day 2 progress response
        
        Args:
            user_id: Telegram user ID
            progress_option: User's chosen progress option
            
        Returns:
            True if successful, False otherwise
        """
        try:
            user_data = self.get_user_data(user_id)
            
            if not user_data:
                logger.error(f"User {user_id} not found")
                return False
            
            row_num = user_data['row_number']
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Map progress option to Russian text
            progress_text = {
                "on_track": "Всё по плану",
                "difficulties": "Есть трудности",
                "not_started": "Ещё не начинал(а)"
            }.get(progress_option, progress_option)
            
            self._retry_on_rate_limit(
                self.user_data_sheet.update,
                f'F{row_num}:G{row_num}',
                [[progress_text, now]]
            )
            
            self._retry_on_rate_limit(
                self.user_data_sheet.update,
                f'J{row_num}',
                [[UserState.PROGRESS_RECORDED.value]]
            )
            
            logger.info(f"✅ Updated Day 2 progress for user {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error updating Day 2 progress: {e}")
            return False
    
    def save_final_assessment(
        self,
        user_id: int,
        percent: int
    ) -> bool:
        """
        Save user's final self-assessment (Day 3)
        
        Args:
            user_id: Telegram user ID
            percent: Assessment percentage (0-100)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            user_data = self.get_user_data(user_id)
            
            if not user_data:
                logger.error(f"User {user_id} not found")
                return False
            
            row_num = user_data['row_number']
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            self._retry_on_rate_limit(
                self.user_data_sheet.update,
                f'H{row_num}:I{row_num}',
                [[percent, now]]
            )
            
            self._retry_on_rate_limit(
                self.user_data_sheet.update,
                f'J{row_num}',
                [[UserState.COMPLETED.value]]
            )
            
            logger.info(f"✅ Saved final assessment for user {user_id}: {percent}%")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error saving final assessment: {e}")
            return False
    
    def get_users_by_state(self, state: UserState) -> List[Dict[str, Any]]:
        """
        Get all users in a specific state
        
        Args:
            state: UserState to filter by
            
        Returns:
            List of user data dictionaries
        """
        try:
            all_data = self._retry_on_rate_limit(self.user_data_sheet.get_all_values)
            users = []
            
            for idx, row in enumerate(all_data[1:], start=2):  # Skip header
                if row and len(row) > 9 and row[9] == state.value:
                    users.append({
                        'row_number': idx,
                        'user_id': int(row[0]),
                        'username': row[1],
                        'full_name': row[2],
                        'goal_text': row[3],
                        'goal_date': row[4],
                        'current_state': row[9]
                    })
            
            return users
            
        except Exception as e:
            logger.error(f"❌ Error getting users by state: {e}")
            return []


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

