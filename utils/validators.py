"""
Input validation utilities with security measures
"""
import re
from typing import Tuple


def escape_for_sheets(s: str) -> str:
    """
    Escape text for safe insertion into Google Sheets.
    Prevents CSV/Formula injection attacks.
    
    Security measures:
    1. Removes control characters (ASCII < 0x20, except tab/newline)
    2. Prefixes strings starting with =, +, -, @ with single quote
    
    Args:
        s: Input string
        
    Returns:
        Escaped string safe for Google Sheets
        
    Example:
        >>> escape_for_sheets("=SUM(A1:A10)")
        "'=SUM(A1:A10)"
        >>> escape_for_sheets("Normal text")
        "Normal text"
    """
    if not s:
        return s
    
    # Remove control characters (keep only tab \t and newline \n)
    s = ''.join(ch for ch in s if ord(ch) >= 0x20 or ch in '\n\t')
    
    # If string starts with dangerous character, prefix with single quote
    if s and s[0] in ('=', '+', '-', '@'):
        return "'" + s
    
    return s


def safe_log_snippet(s: str, max_len: int = 200) -> str:
    """
    Sanitize user input for safe logging.
    Prevents log injection and protects user privacy.
    
    Security measures:
    1. Removes newlines and carriage returns
    2. Truncates to max_len to prevent log flooding
    3. Removes other control characters
    
    Args:
        s: Input string
        max_len: Maximum length for log output
        
    Returns:
        Sanitized string safe for logging
        
    Example:
        >>> safe_log_snippet("Goal\\nwith\\nnewlines")
        "Goal with newlines"
    """
    if not s:
        return ""
    
    # Replace newlines and carriage returns with spaces
    s = s.replace('\n', ' ').replace('\r', ' ')
    
    # Remove other control characters
    s = ''.join(ch for ch in s if ord(ch) >= 0x20 or ch == ' ')
    
    # Truncate to max length
    if len(s) > max_len:
        return s[:max_len] + '...'
    
    return s


# Strict regex for assessment score: only 0-100
INT_RE = re.compile(r'^\s*(0|[1-9]\d?|100)\s*$')


def validate_assessment_score(text: str) -> Tuple[bool, int]:
    """
    Validate user's self-assessment score (0-100) with strict parsing.
    
    Security measures:
    1. Uses regex to ensure only valid integers
    2. Prevents injection through malformed input
    3. No eval or unsafe conversions
    
    Args:
        text: User input string
        
    Returns:
        Tuple of (is_valid, score)
        If invalid, score is -1
        
    Example:
        >>> validate_assessment_score("85")
        (True, 85)
        >>> validate_assessment_score("100; DROP TABLE")
        (False, -1)
        >>> validate_assessment_score("-5")
        (False, -1)
    """
    m = INT_RE.match(text)
    if not m:
        return False, -1
    
    score = int(m.group(1))
    # Double-check range (should always be true with our regex)
    if 0 <= score <= 100:
        return True, score
    
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


