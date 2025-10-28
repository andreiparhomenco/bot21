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
    user_states[user_id] = UserState.AWAITING_GOAL
    
    await update.message.reply_text(WELCOME_MESSAGE, parse_mode='Markdown')


async def assess_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle /assess command
    Allows user to self-assess their progress
    """
    user = update.effective_user
    user_id = user.id
    
    logger.info(f"User {user_id} requested assessment")
    
    # Check if user has a goal
    user_data = get_db().get_user_data(user_id)
    
    if not user_data or not user_data.get('goal_text'):
        await update.message.reply_text(ERROR_NO_GOAL)
        return
    
    # Set state to awaiting assessment
    user_states[user_id] = UserState.AWAITING_ASSESSMENT
    
    goal_text = user_data['goal_text']
    message = ASSESSMENT_REQUEST.format(goal=goal_text)
    
    await update.message.reply_text(message, parse_mode='Markdown')


async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle text messages based on user state
    """
    user = update.effective_user
    user_id = user.id
    username = user.username or user.first_name
    full_name = f"{user.first_name} {user.last_name or ''}".strip()
    text = update.message.text.strip()
    
    current_state = user_states.get(user_id, UserState.IDLE)
    
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
        
        # Save goal to database
        success = get_db().save_user_goal(user_id, username, full_name, text)
        
        if success:
            # Send confirmation
            confirmation = GOAL_CONFIRMATION.format(goal=text)
            await update.message.reply_text(confirmation, parse_mode='Markdown')
            
            # Update state
            user_states[user_id] = UserState.GOAL_SET
            
            logger.info(f"✅ Saved goal for user {user_id}")
        else:
            await update.message.reply_text(ERROR_GENERAL)
    
    # State: Awaiting Assessment
    elif current_state == UserState.AWAITING_ASSESSMENT:
        # Validate assessment score
        is_valid, score = validate_assessment_score(text)
        
        if not is_valid:
            await update.message.reply_text(ERROR_INVALID_ASSESSMENT)
            return
        
        # Save assessment
        success = get_db().save_final_assessment(user_id, score)
        
        if success:
            # Send thanks message
            thanks = ASSESSMENT_THANKS.format(percent=score)
            await update.message.reply_text(thanks, parse_mode='Markdown')
            
            # Update state
            user_states[user_id] = UserState.COMPLETED
            
            logger.info(f"✅ Saved assessment for user {user_id}: {score}%")
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

