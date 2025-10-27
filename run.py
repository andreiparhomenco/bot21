"""
Simple runner script for GoalBuddy21 bot
Adds current directory to Python path
"""
import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import and run main
from bot.main import main

if __name__ == "__main__":
    main()

