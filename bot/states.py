"""
User state management using FSM (Finite State Machine)
"""
from enum import Enum


class UserState(Enum):
    """Possible user states during the 3-day journey"""
    IDLE = "IDLE"
    AWAITING_GOAL = "AWAITING_GOAL"
    GOAL_SET = "GOAL_SET"
    AWAITING_PROGRESS = "AWAITING_PROGRESS"
    PROGRESS_RECORDED = "PROGRESS_RECORDED"
    AWAITING_ASSESSMENT = "AWAITING_ASSESSMENT"
    COMPLETED = "COMPLETED"


class ProgressOption(Enum):
    """User's progress choices on Day 2"""
    ON_TRACK = "on_track"
    DIFFICULTIES = "difficulties"
    NOT_STARTED = "not_started"

