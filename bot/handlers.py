"""
Telegram bot handlers for commands, messages, and callbacks
"""
from telegram import Update
from telegram.ext import ContextTypes

from database.sheets import get_db
from bot.states import UserState
from bot.messages import (
    WELCOME_MESSAGE,
    GOAL_CONFIRMATION,
    ASSESSMENT_REQUEST,
    ASSESSMENT_THANKS,
    ERROR_INVALID_ASSESSMENT,
    ERROR_NO_GOAL,
    ERROR_GOAL_TOO_SHORT,
    ERROR_GOAL_TOO_LONG,
    ERROR_GENERAL,
)
from utils.validators import validate_assessment_score, validate_goal_text
from utils.logger import logger


# User state tracking (in-memory, keyed by user_id)
# Stores: user_id -> {'state': UserState, 'row_number': int, 'goal_text': str}
user_states = {}


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle /start command
    Initiates goal setting flow
    """
    user = update.effective_user
    user_id = user.id
    username = user.username or user.first_name
    
    logger.info(f"User {user_id} ({username}) initiated /start")
    
    # Set user state to awaiting goal
    user_states[user_id] = {'state': UserState.AWAITING_GOAL}
    
    await update.message.reply_text(WELCOME_MESSAGE, parse_mode='Markdown')


async def assess_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle /assess command
    Allows user to self-assess their progress
    """
    user = update.effective_user
    user_id = user.id
    
    logger.info(f"User {user_id} requested assessment")
    
    # Check if user has a goal in current session
    user_data = user_states.get(user_id)
    
    if not user_data or 'goal_text' not in user_data:
        await update.message.reply_text(ERROR_NO_GOAL)
        return
    
    # Set state to awaiting assessment
    user_states[user_id]['state'] = UserState.AWAITING_ASSESSMENT
    
    goal_text = user_data['goal_text']
    message = ASSESSMENT_REQUEST.format(goal=goal_text)
    
    await update.message.reply_text(message, parse_mode='Markdown')


async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle text messages based on user state
    """
    user = update.effective_user
    user_id = user.id
    text = update.message.text.strip()
    
    user_data = user_states.get(user_id, {})
    current_state = user_data.get('state', UserState.IDLE)
    
    # State: Awaiting Goal
    if current_state == UserState.AWAITING_GOAL:
        # Validate goal text
        is_valid, error_msg = validate_goal_text(text)
        
        if not is_valid:
            if "короткая" in error_msg:
                await update.message.reply_text(ERROR_GOAL_TOO_SHORT)
            else:
                await update.message.reply_text(ERROR_GOAL_TOO_LONG)
            return
        
        # Save goal to database (anonymous)
        row_number = get_db().save_user_goal(text)
        
        if row_number:
            # Send confirmation
            confirmation = GOAL_CONFIRMATION.format(goal=text)
            await update.message.reply_text(confirmation, parse_mode='Markdown')
            
            # Update state and store goal info in memory
            user_states[user_id] = {
                'state': UserState.GOAL_SET,
                'row_number': row_number,
                'goal_text': text
            }
            
            logger.info(f"✅ Saved anonymous goal to row {row_number}")
        else:
            await update.message.reply_text(ERROR_GENERAL)
    
    # State: Awaiting Assessment
    elif current_state == UserState.AWAITING_ASSESSMENT:
        # Validate assessment score
        is_valid, score = validate_assessment_score(text)
        
        if not is_valid:
            await update.message.reply_text(ERROR_INVALID_ASSESSMENT)
            return
        
        # Get row number from user state
        row_number = user_data.get('row_number')
        
        if not row_number:
            await update.message.reply_text(ERROR_NO_GOAL)
            return
        
        # Save assessment
        success = get_db().save_final_assessment(row_number, score)
        
        if success:
            # Send thanks message
            thanks = ASSESSMENT_THANKS.format(percent=score)
            await update.message.reply_text(thanks, parse_mode='Markdown')
            
            # Update state
            user_states[user_id]['state'] = UserState.COMPLETED
            
            logger.info(f"✅ Saved assessment for row {row_number}: {score}%")
        else:
            await update.message.reply_text(ERROR_GENERAL)
    
    else:
        # User sent message without being in a specific state
        # Ignore or provide help
        pass


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle errors in handlers
    """
    logger.error(f"❌ Update {update} caused error: {context.error}")
    
    if update and update.effective_message:
        await update.effective_message.reply_text(ERROR_GENERAL)

