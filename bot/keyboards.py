"""
Telegram keyboard layouts
"""
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.states import ProgressOption
from bot.messages import (
    BUTTON_ON_TRACK,
    BUTTON_DIFFICULTIES,
    BUTTON_NOT_STARTED,
)


def get_progress_keyboard() -> InlineKeyboardMarkup:
    """
    Day 2 progress check keyboard
    
    Returns:
        InlineKeyboardMarkup with 3 options
    """
    keyboard = [
        [InlineKeyboardButton(BUTTON_ON_TRACK, callback_data=ProgressOption.ON_TRACK.value)],
        [InlineKeyboardButton(BUTTON_DIFFICULTIES, callback_data=ProgressOption.DIFFICULTIES.value)],
        [InlineKeyboardButton(BUTTON_NOT_STARTED, callback_data=ProgressOption.NOT_STARTED.value)],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_goal_options_keyboard() -> InlineKeyboardMarkup:
    """
    Keyboard for goal modification (future use)
    
    Returns:
        InlineKeyboardMarkup with goal options
    """
    keyboard = [
        [InlineKeyboardButton("✏️ Изменить цель", callback_data="change_goal")],
    ]
    return InlineKeyboardMarkup(keyboard)


# Persistent menu button (ReplyKeyboardMarkup alternative)
# This would be set via bot.set_my_commands() in main.py
def get_menu_button_config():
    """Returns configuration for persistent menu button"""
    return {
        "text": "📈 Оценить прогресс",
        "command": "/assess"
    }


