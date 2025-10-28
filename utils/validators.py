"""
Input validation utilities
"""
from typing import Tuple


def validate_assessment_score(text: str) -> Tuple[bool, int]:
    """
    Validate user's self-assessment score (0-100)
    
    Args:
        text: User input string
        
    Returns:
        Tuple of (is_valid, score)
        If invalid, score is -1
    """
    try:
        score = int(text.strip())
        if 0 <= score <= 100:
            return True, score
        return False, -1
    except ValueError:
        return False, -1


def validate_goal_text(text: str, min_length: int = 10, max_length: int = 500) -> Tuple[bool, str]:
    """
    Validate goal text length and content
    
    Args:
        text: Goal text
        min_length: Minimum required length
        max_length: Maximum allowed length
        
    Returns:
        Tuple of (is_valid, error_message)
        If valid, error_message is empty string
    """
    text = text.strip()
    
    if len(text) < min_length:
        return False, f"Цель слишком короткая (минимум {min_length} символов)"
    
    if len(text) > max_length:
        return False, f"Цель слишком длинная (максимум {max_length} символов)"
    
    return True, ""


