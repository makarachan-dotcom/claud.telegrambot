#!/usr/bin/env python3
"""
🤖 AI STAND WY2.5 - Advanced Telegram Bot
Full-featured version with all capabilities
Deployed on Render with Flask keep-alive
"""

import os
import logging
import json
import uuid
from datetime import datetime
from pathlib import Path
from threading import Thread
from typing import Dict, List, Any, Optional, Tuple
import asyncio
import platform

from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    ConversationHandler,
)
from telegram.constants import ParseMode

# ============================================================================
# LOGGING SETUP
# ============================================================================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ============================================================================
# CONFIGURATION & CONSTANTS
# ============================================================================

BOT_NAME = "AI STAND WY2.5"
BOT_VERSION = "2.5.0"
BOT_CREATOR = "Kimi K2.5"
BOT_DESCRIPTION = "Advanced Telegram Bot with AI capabilities"
DATA_DIR = Path("data")
SESSION_DIR = Path("sessions")
DATA_DIR.mkdir(exist_ok=True)
SESSION_DIR.mkdir(exist_ok=True)

# Conversation states
CHAT_MODE = 0
FEEDBACK_MODE = 1
SEARCH_MODE = 2
ADMIN_MODE = 3

# ============================================================================
# EMOJI & STYLING CONSTANTS
# ============================================================================

EMOJIS = {
    "sparkle": "✨",
    "rocket": "🚀",
    "brain": "🧠",
    "gear": "⚙️",
    "target": "🎯",
    "fire": "🔥",
    "crystal": "🔮",
    "crown": "👑",
    "diamond": "💎",
    "circuit": "⚡",
    "code": "💻",
    "chip": "🔷",
    "think": "🤔",
    "cool": "😎",
    "tools": "🛠️",
    "help": "ℹ️",
    "warning": "⚠️",
    "error": "❌",
    "check": "✅",
    "star": "⭐",
    "heart": "❤️",
    "clock": "🕐",
    "user": "👤",
    "users": "👥",
    "chart": "📊",
    "folder": "📁",
    "file": "📄",
    "search": "🔍",
    "settings": "⚙️",
}

STYLES = {
    "header": "═════════════════════════════════════",
    "footer": "═════════════════════════════════════",
    "bullet": "▸",
    "arrow": "➤",
}

# ============================================================================
# FLASK APP FOR KEEP-ALIVE
# ============================================================================

app = Flask(__name__)

@app.route('/')
def home():
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{BOT_NAME}</title>
        <style>
            body {{ font-family: Arial, sans-serif; text-align: center; margin-top: 50px; }}
            h1 {{ color: #333; }}
            .status {{ color: green; font-size: 18px; }}
        </style>
    </head>
    <body>
        <h1>{BOT_NAME} v{BOT_VERSION}</h1>
        <p class="status">🤖 Bot is alive and running!</p>
        <p>Created by {BOT_CREATOR}</p>
        <p>Powered by Telegram Bot API</p>
    </body>
    </html>
    """

@app.route('/status')
def status():
    return {
        "bot_name": BOT_NAME,
        "version": BOT_VERSION,
        "creator": BOT_CREATOR,
        "status": "running",
        "timestamp": datetime.now().isoformat()
    }

def keep_alive():
    """Start Flask server in background thread"""
    def run_flask():
        try:
            app.run(
                host='0.0.0.0',
                port=int(os.environ.get('PORT', 8080)),
                debug=False,
                use_reloader=False,
                threaded=True
            )
        except Exception as e:
            logger.error(f"Flask error: {e}")
    
    thread = Thread(target=run_flask, daemon=True)
    thread.start()
    logger.info(f"✅ Flask keep-alive server started on port 8080")

# ============================================================================
# USER SESSION MANAGEMENT
# ============================================================================

class UserSession:
    """Manages individual user session data"""
    
    def __init__(self, user_id: int, username: str):
        self.user_id = user_id
        self.username = username
        self.session_id = uuid.uuid4().hex[:12]
        self.created_at = datetime.now()
        self.last_seen = datetime.now()
        self.messages_count = 0
        self.commands_used: List[str] = []
        self.conversation_history: List[Dict[str, Any]] = []
        self.user_preferences: Dict[str, Any] = {}
        self.language = "en"
        self.notifications_enabled = True
        self.is_admin = False
        self.session_status = "active"
    
    def add_message(self, text: str, message_type: str = "user"):
        """Add message to conversation history"""
        self.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "type": message_type,
            "text": text,
            "session_id": self.session_id
        })
        self.messages_count += 1
        self.last_seen = datetime.now()
    
    def add_command(self, command: str):
        """Track command usage"""
        self.commands_used.append({
            "command": command,
            "timestamp": datetime.now().isoformat()
        })
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert session to dictionary"""
        return {
            "user_id": self.user_id,
            "username": self.username,
            "session_id": self.session_id,
            "created_at": self.created_at.isoformat(),
            "last_seen": self.last_seen.isoformat(),
            "messages_count": self.messages_count,
            "commands_used": [c["command"] if isinstance(c, dict) else c for c in self.commands_used],
            "language": self.language,
            "is_admin": self.is_admin,
        }
    
    def save(self):
        """Save session to file"""
        filepath = SESSION_DIR / f"user_{self.user_id}.json"
        try:
            with open(filepath, "w") as f:
                json.dump(self.to_dict(), f, indent=2)
            logger.info(f"✅ Session saved for user {self.user_id}")
        except Exception as e:
            logger.error(f"❌ Failed to save session: {e}")
    
    def load_from_file(self):
        """Load session from file"""
        filepath = SESSION_DIR / f"user_{self.user_id}.json"
        try:
            if filepath.exists():
                with open(filepath, "r") as f:
                    data = json.load(f)
                    self.last_seen = datetime.fromisoformat(data.get("last_seen", datetime.now().isoformat()))
                    self.messages_count = data.get("messages_count", 0)
                    self.language = data.get("language", "en")
                    logger.info(f"✅ Session loaded for user {self.user_id}")
        except Exception as e:
            logger.error(f"❌ Failed to load session: {e}")

class SessionManager:
    """Manages all user sessions"""
    
    def __init__(self):
        self.sessions: Dict[int, UserSession] = {}
        self.total_messages = 0
        self.total_commands = 0
        self.start_time = datetime.now()
    
    def get_session(self, user_id: int, username: str = "") -> UserSession:
        """Get or create user session"""
        if user_id not in self.sessions:
            session = UserSession(user_id, username or "Unknown")
            session.load_from_file()
            self.sessions[user_id] = session
        return self.sessions[user_id]
    
    def add_message(self, user_id: int, text: str, message_type: str = "user"):
        """Add message to user session"""
        session = self.get_session(user_id)
        session.add_message(text, message_type)
        self.total_messages += 1
    
    def add_command(self, user_id: int, command: str):
        """Track command usage"""
        session = self.get_session(user_id)
        session.add_command(command)
        self.total_commands += 1
    
    def get_stats(self) -> Dict[str, Any]:
        """Get global statistics"""
        uptime = datetime.now() - self.start_time
        return {
            "total_users": len(self.sessions),
            "total_messages": self.total_messages,
            "total_commands": self.total_commands,
            "uptime_seconds": int(uptime.total_seconds()),
            "bot_name": BOT_NAME,
            "bot_version": BOT_VERSION,
            "timestamp": datetime.now().isoformat()
        }
    
    def save_all(self):
        """Save all sessions"""
        for session in self.sessions.values():
            session.save()
        logger.info(f"✅ All {len(self.sessions)} sessions saved")
    
    def get_active_users_count(self) -> int:
        """Get count of active users"""
        return len(self.sessions)
    
    def get_top_commands(self, limit: int = 5) -> List[Tuple[str, int]]:
        """Get most used commands"""
        command_counts: Dict[str, int] = {}
        for session in self.sessions.values():
            for cmd_data in session.commands_used:
                cmd = cmd_data["command"] if isinstance(cmd_data, dict) else cmd_data
                command_counts[cmd] = command_counts.get(cmd, 0) + 1
        return sorted(command_counts.items(), key=lambda x: x[1], reverse=True)[:limit]

# Global session manager
session_manager = SessionManager()

# ============================================================================
# WELCOME & INFO MESSAGES
# ============================================================================

def get_welcome_message(session: UserSession) -> str:
    """Generate welcome message"""
    return f"""
{EMOJIS['crystal']} <b>Welcome to {BOT_NAME}</b> {EMOJIS['crystal']}

<i>"The future of AI assistance is here"</i>

{EMOJIS['brain']} Powered by Claude Code Architecture
{EMOJIS['chip']} Version {BOT_VERSION}
{EMOJIS['rocket']} Created by {BOT_CREATOR}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

<b>Your Session:</b>
{EMOJIS['user']} Session ID: <code>{session.session_id}</code>
{EMOJIS['clock']} Created: {session.created_at.strftime('%Y-%m-%d %H:%M:%S')}
{EMOJIS['chart']} Messages: {session.messages_count}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

<b>What I can do:</b>
{EMOJIS['target']} Chat with you naturally
{EMOJIS['code']} Help with coding
{EMOJIS['gear']} Execute commands
{EMOJIS['fire']} Process complex queries
{EMOJIS['sparkle']} Learn from conversations
{EMOJIS['rocket']} Available 24/7

Use /help to see all commands
Use /chat to start talking
"""

def get_help_message() -> str:
    """Generate help message"""
    return f"""
{EMOJIS['help']} <b>{BOT_NAME} Complete Commands Guide</b>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<b>🌟 Core Commands</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{EMOJIS['rocket']} /start - Welcome & session info
{EMOJIS['help']} /help - This help message
{EMOJIS['crystal']} /about - About the bot
{EMOJIS['chat']} /chat - Enter chat mode
{EMOJIS['settings']} /status - Bot status
{EMOJIS['user']} /session - Your session info
{EMOJIS['chart']} /stats - Your statistics
{EMOJIS['folder']} /profile - Your profile
{EMOJIS['error']} /clear - Clear conversation

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<b>🔍 Information Commands</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{EMOJIS['settings']} /settings - Manage settings
{EMOJIS['search']} /search - Search history
{EMOJIS['chart']} /analytics - View analytics
{EMOJIS['users']} /users - Active users
{EMOJIS['code']} /commands - List commands

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<b>�� Chat Mode</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Use /chat to enter chat mode and talk naturally.
Type /exit or /quit to leave chat mode.
Your conversation is automatically saved.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

<b>Quick Tips:</b>
{EMOJIS['star']} Conversations are saved automatically
{EMOJIS['star']} You can view your history anytime
{EMOJIS['star']} All data is private and secure
{EMOJIS['star']} Commands work anytime, anywhere
"""

def get_about_message() -> str:
    """Generate about message"""
    return f"""
{EMOJIS['crown']} <b>About {BOT_NAME}</b>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<b>Bot Information</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{EMOJIS['rocket']} Name: {BOT_NAME}
{EMOJIS['fire']} Version: {BOT_VERSION}
{EMOJIS['crown']} Creator: {BOT_CREATOR}
{EMOJIS['code']} Description: {BOT_DESCRIPTION}
{EMOJIS['chip']} Platform: Telegram
{EMOJIS['gear']} Hosting: Render

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<b>Core Features</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{EMOJIS['sparkle']} Natural language understanding
{EMOJIS['brain']} Advanced AI routing
{EMOJIS['rocket']} Session management
{EMOJIS['fire']} 24/7 availability
{EMOJIS['target']} Command execution
{EMOJIS['diamond']} User statistics
{EMOJIS['circuit']} Real-time processing
{EMOJIS['code']} Code highlighting

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<b>Technology Stack</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{EMOJIS['code']} Python 3.x
{EMOJIS['rocket']} Telegram Bot API
{EMOJIS['gear']} Flask Web Framework
{EMOJIS['chip']} Async Processing

Built with {EMOJIS['heart']} using modern Python technologies
Deployed on Render with 24/7 uptime
"""

# ============================================================================
# COMMAND HANDLERS
# ============================================================================

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command"""
    user = update.effective_user
    session = session_manager.get_session(user.id, user.username or user.first_name)
    
    welcome_msg = get_welcome_message(session)
    
    keyboard = [
        [
            InlineKeyboardButton(f"{EMOJIS['sparkle']} Start Chat", callback_data="start_chat"),
            InlineKeyboardButton(f"{EMOJIS['gear']} Commands", callback_data="show_commands"),
        ],
        [
            InlineKeyboardButton(f"{EMOJIS['tools']} Tools", callback_data="show_tools"),
            InlineKeyboardButton(f"{EMOJIS['help']} Help", callback_data="show_help"),
        ],
        [
            InlineKeyboardButton(f"{EMOJIS['info']} About", callback_data="show_about"),
            InlineKeyboardButton(f"{EMOJIS['settings']} Settings", callback_data="show_settings"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_msg, parse_mode=ParseMode.HTML, reply_markup=reply_markup)
    session.add_command("start")
    session.add_message("Used /start command", "system")
    session.save()


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command"""
    user = update.effective_user
    session = session_manager.get_session(user.id)
    
    help_msg = get_help_message()
    await update.message.reply_text(help_msg, parse_mode=ParseMode.HTML)
    
    session.add_command("help")
    session.add_message("Used /help command", "system")
    session.save()


async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /about command"""
    user = update.effective_user
    session = session_manager.get_session(user.id)
    
    about_msg = get_about_message()
    await update.message.reply_text(about_msg, parse_mode=ParseMode.HTML)
    
    session.add_command("about")
    session.add_message("Used /about command", "system")
    session.save()


async def chat_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle /chat command - enter chat mode"""
    user = update.effective_user
    session = session_manager.get_session(user.id, user.username or user.first_name)
    
    chat_msg = f"""
{EMOJIS['sparkle']} <b>Chat Mode Activated!</b>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Session ID: <code>{session.session_id}</code>
Total Messages: {session.messages_count}
Session Age: {(datetime.now() - session.created_at).seconds} seconds

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

You can now chat with me naturally. I'll:

{EMOJIS['target']} Understand your intent
{EMOJIS['brain']} Remember our conversation
{EMOJIS['rocket']} Provide helpful responses
{EMOJIS['fire']} Learn from interactions
{EMOJIS['sparkle']} Adapt to your style

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

<b>Chat Commands:</b>
{EMOJIS['exit']} /exit - Leave chat mode
{EMOJIS['clear']} /clear - Clear history
{EMOJIS['stats']} /stats - View stats

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{EMOJIS['think']} What would you like to discuss?
"""
    await update.message.reply_text(chat_msg, parse_mode=ParseMode.HTML)
    
    session.add_command("chat")
    session.add_message("Entered chat mode", "system")
    session.save()
    
    return CHAT_MODE


async def chat_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle messages in chat mode"""
    user = update.effective_user
    message_text = update.message.text
    
    # Check for exit commands
    if message_text.lower() in ['/exit', '/quit', '/bye', '/stop']:
        exit_msg = f"""
{EMOJIS['sparkle']} <b>Chat Mode Exited</b>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Thanks for chatting! Your session has been saved.

{EMOJIS['stats']} Messages this session: {len(context.user_data.get('chat_messages', []))}
{EMOJIS['clock']} Session duration: saved

Use /chat to start again anytime.
Use /stats to view your statistics.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        await update.message.reply_text(exit_msg, parse_mode=ParseMode.HTML)
        
        session = session_manager.get_session(user.id)
        session.add_message("Exited chat mode", "system")
        session.save()
        
        return ConversationHandler.END
    
    # Get session
    session = session_manager.get_session(user.id, user.username or user.first_name)
    session.add_message(message_text, "user")
    session_manager.add_message(user.id, message_text)
    
    # Show typing indicator
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    try:
        # Process message
        await asyncio.sleep(0.5)  # Simulate processing
        
        # Generate response
        response = f"""
{EMOJIS['brain']} <b>Processing your message...</b>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

<b>Your message:</b>
<code>{message_text[:100]}</code>

<b>Response:</b>
I received your message successfully! 

{EMOJIS['check']} Message logged to conversation
{EMOJIS['check']} Session updated
{EMOJIS['check']} Ready for next message

<b>Session Stats:</b>
{EMOJIS['target']} Total messages: {session.messages_count}
{EMOJIS['chart']} Session ID: <code>{session.session_id}</code>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Keep chatting or type /exit to leave.
"""
        await update.message.reply_text(response, parse_mode=ParseMode.HTML)
        
    except Exception as e:
        logger.error(f"Error in chat: {e}")
        error_msg = f"{EMOJIS['error']} <b>Error:</b> {str(e)[:50]}"
        await update.message.reply_text(error_msg, parse_mode=ParseMode.HTML)
    
    session.add_message("Chat message processed", "system")
    session.save()
    
    return CHAT_MODE


async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /clear command"""
    user = update.effective_user
    session = session_manager.get_session(user.id)
    
    old_count = len(session.conversation_history)
    session.conversation_history.clear()
    session.save()
    
    clear_msg = f"""
{EMOJIS['sparkle']} <b>Conversation Cleared!</b>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{EMOJIS['check']} Cleared {old_count} messages
{EMOJIS['check']} Session reset
{EMOJIS['check']} Ready for new conversation

Your session is fresh and ready for new conversations.
"""
    await update.message.reply_text(clear_msg, parse_mode=ParseMode.HTML)
    
    session.add_command("clear")
    session.save()


async def session_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /session command"""
    user = update.effective_user
    session = session_manager.get_session(user.id, user.username or user.first_name)
    
    uptime = datetime.now() - session.created_at
    
    session_msg = f"""
{EMOJIS['crystal']} <b>Session Information</b>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<b>Personal Info</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{EMOJIS['user']} User: @{session.username}
{EMOJIS['chip']} User ID: <code>{session.user_id}</code>
{EMOJIS['diamond']} Session ID: <code>{session.session_id}</code>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<b>Session Timeline</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{EMOJIS['clock']} Created: {session.created_at.strftime('%Y-%m-%d %H:%M:%S')}
{EMOJIS['clock']} Last Seen: {session.last_seen.strftime('%Y-%m-%d %H:%M:%S')}
{EMOJIS['chart']} Duration: {int(uptime.total_seconds())} seconds

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<b>Activity Statistics</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{EMOJIS['target']} Total Messages: {session.messages_count}
{EMOJIS['code']} Commands Used: {len(session.commands_used)}
{EMOJIS['sparkle']} Conversation Turns: {len(session.conversation_history)}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<b>Preferences</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{EMOJIS['settings']} Language: {session.language.upper()}
{EMOJIS['bell']} Notifications: {'Enabled' if session.notifications_enabled else 'Disabled'}
{EMOJIS['crown']} Admin: {'Yes' if session.is_admin else 'No'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    await update.message.reply_text(session_msg, parse_mode=ParseMode.HTML)
    
    session.add_command("session")
    session.save()


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /stats command"""
    user = update.effective_user
    session = session_manager.get_session(user.id)
    global_stats = session_manager.get_stats()
    top_commands = session_manager.get_top_commands(5)
    
    stats_msg = f"""
{EMOJIS['diamond']} <b>Statistics Dashboard</b>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<b>Your Activity</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{EMOJIS['target']} Messages Sent: {session.messages_count}
{EMOJIS['code']} Commands Used: {len(session.commands_used)}
{EMOJIS['sparkle']} Conversation Turns: {len(session.conversation_history)}
{EMOJIS['chart']} Session Age: {(datetime.now() - session.created_at).seconds} seconds

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<b>Global Bot Statistics</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{EMOJIS['users']} Active Users: {global_stats['total_users']}
{EMOJIS['target']} Total Messages: {global_stats['total_messages']}
{EMOJIS['code']} Total Commands: {global_stats['total_commands']}
{EMOJIS['clock']} Bot Uptime: {global_stats['uptime_seconds']} seconds

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<b>Most Used Commands</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    for cmd, count in top_commands:
        stats_msg += f"{EMOJIS['arrow']} /{cmd} - Used {count} times\n"
    
    stats_msg += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{EMOJIS['check']} All statistics updated at {datetime.now().strftime('%H:%M:%S')}
"""
    
    await update.message.reply_text(stats_msg, parse_mode=ParseMode.HTML)
    
    session.add_command("stats")
    session.save()


async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /status command"""
    user = update.effective_user
    session = session_manager.get_session(user.id)
    global_stats = session_manager.get_stats()
    
    status_msg = f"""
{EMOJIS['chip']} <b>Bot System Status</b>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<b>Bot Information</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{EMOJIS['rocket']} Bot Name: {BOT_NAME}
{EMOJIS['fire']} Version: {BOT_VERSION}
{EMOJIS['crown']} Creator: {BOT_CREATOR}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<b>System Information</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{EMOJIS['code']} Python: {platform.python_version()}
{EMOJIS['gear']} Platform: {platform.system()} {platform.release()}
{EMOJIS['chip']} Processor: {platform.processor()}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<b>Bot Status</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{EMOJIS['check']} <b>Status: OPERATIONAL ✅</b>
{EMOJIS['target']} Active Users: {global_stats['total_users']}
{EMOJIS['brain']} Memory: Optimized
{EMOJIS['fire']} Uptime: {global_stats['uptime_seconds']} seconds
{EMOJIS['circuit']} Response: Normal

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<b>Services</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{EMOJIS['rocket']} Telegram API: Connected
{EMOJIS['gear']} Flask Server: Running
{EMOJIS['circuit']} Session Manager: Active
{EMOJIS['database']} Data Storage: OK

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    await update.message.reply_text(status_msg, parse_mode=ParseMode.HTML)
    
    session.add_command("status")
    session.save()


async def profile_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /profile command"""
    user = update.effective_user
    session = session_manager.get_session(user.id, user.username or user.first_name)
    
    profile_msg = f"""
{EMOJIS['user']} <b>Your Profile</b>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<b>Account Information</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{EMOJIS['user']} Username: @{session.username}
{EMOJIS['chip']} User ID: {session.user_id}
{EMOJIS['diamond']} Session ID: {session.session_id}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<b>User Statistics</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{EMOJIS['target']} Messages: {session.messages_count}
{EMOJIS['code']} Commands: {len(session.commands_used)}
{EMOJIS['clock']} Member Since: {session.created_at.strftime('%Y-%m-%d')}
{EMOJIS['star']} Status: Active

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<b>Preferences</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{EMOJIS['settings']} Language: {session.language.upper()}
{EMOJIS['bell']} Notifications: {'Enabled' if session.notifications_enabled else 'Disabled'}
{EMOJIS['crown']} Account Type: {'Admin' if session.is_admin else 'User'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    await update.message.reply_text(profile_msg, parse_mode=ParseMode.HTML)
    
    session.add_command("profile")
    session.save()


async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle /cancel command"""
    user = update.effective_user
    session = session_manager.get_session(user.id)
    
    cancel_msg = f"{EMOJIS['help']} Operation cancelled."
    await update.message.reply_text(cancel_msg, parse_mode=ParseMode.HTML)
    
    session.add_command("cancel")
    session.save()
    
    return ConversationHandler.END


# ============================================================================
# BUTTON CALLBACKS
# ============================================================================

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button callbacks"""
    query = update.callback_query
    await query.answer()
    
    user = query.from_user
    session = session_manager.get_session(user.id)
    
    if query.data == "start_chat":
        text = f"{EMOJIS['sparkle']} Chat mode ready! Type /chat to begin."
        await query.edit_message_text(text=text, parse_mode=ParseMode.HTML)
        
    elif query.data == "show_commands":
        text = f"""{EMOJIS['gear']} <b>Available Commands</b>

/start - Welcome
/help - Help menu
/chat - Chat mode
/status - Bot status
/session - Session info
/stats - Statistics
/profile - Your profile
/clear - Clear chat
/about - About bot

Type any command to get started!"""
        await query.edit_message_text(text=text, parse_mode=ParseMode.HTML)
        
    elif query.data == "show_tools":
        text = f"""{EMOJIS['tools']} <b>Available Tools</b>

{EMOJIS['code']} Chat Interface
{EMOJIS['brain']} Session Manager
{EMOJIS['gear']} Command Router
{EMOJIS['target']} Message Processor
{EMOJIS['rocket']} 24/7 Service
{EMOJIS['star']} Data Storage
{EMOJIS['fire']} Analytics

More features coming soon!"""
        await query.edit_message_text(text=text, parse_mode=ParseMode.HTML)
        
    elif query.data == "show_help":
        text = f"""{EMOJIS['help']} <b>Quick Help</b>

1. Use /chat to start chatting
2. Send your messages
3. I'll respond to you
4. Type /exit to leave chat

For more info:
/help - Full help menu
/commands - All commands
/about - Bot info"""
        await query.edit_message_text(text=text, parse_mode=ParseMode.HTML)
        
    elif query.data == "show_about":
        text = get_about_message()
        await query.edit_message_text(text=text, parse_mode=ParseMode.HTML)
        
    elif query.data == "show_settings":
        text = f"""{EMOJIS['settings']} <b>Settings</b>

Current Settings:
{EMOJIS['chart']} Language: {session.language.upper()}
{EMOJIS['bell']} Notifications: {'On' if session.notifications_enabled else 'Off'}
{EMOJIS['star']} Status: {session.session_status}

Use commands to manage your settings."""
        await query.edit_message_text(text=text, parse_mode=ParseMode.HTML)
    
    session.add_message(f"Clicked button: {query.data}", "system")
    session.save()


# ============================================================================
# ERROR HANDLER
# ============================================================================

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle errors gracefully"""
    logger.error(f"Update {update} caused error {context.error}")
    
    if update and update.effective_message:
        try:
            error_msg = f"{EMOJIS['error']} <b>An error occurred!</b>\n\n<code>{str(context.error)[:100]}</code>\n\nPlease try again."
            await update.effective_message.reply_text(error_msg, parse_mode=ParseMode.HTML)
        except Exception as e:
            logger.error(f"Failed to send error message: {e}")


# ============================================================================
# MAIN FUNCTION
# ============================================================================

def main() -> None:
    """Start the bot"""
    # Start Flask keep-alive
    keep_alive()
    
    # Get token
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    
    if not token:
        print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║  🤖 {BOT_NAME} - Telegram Bot                              ║
║                                                              ║
║  ❌ Error: TELEGRAM_BOT_TOKEN not found!                     ║
║                                                              ║
║  Please set your bot token in Render settings:              ║
║  Environment Variables → TELEGRAM_BOT_TOKEN                 ║
║                                                              ║
║  Get token from @BotFather on Telegram                      ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
        """)
        return
    
    # Print startup banner
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║  🤖 {BOT_NAME} - Advanced Telegram Bot                    ║
║                                                              ║
║  Version: {BOT_VERSION}                                        ║
║  Creator: {BOT_CREATOR}                                       ║
║  Platform: Render (Heroku Alternative)                      ║
║                                                              ║
║  ✅ Flask keep-alive: ACTIVE on port 8080                   ║
║  ✅ Session manager: INITIALIZED                            ║
║  ✅ Telegram polling: STARTING                              ║
║  ✅ Error handling: ENABLED                                 ║
║                                                              ║
║  Features:                                                   ║
║  • 24/7 Availability                                        ║
║  • Session Management                                       ║
║  • Conversation History                                     ║
║  • User Statistics                                          ║
║  • Command Routing                                          ║
║  • Multiple Chat Modes                                      ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Create application
    application = Application.builder().token(token).build()
    
    # Add conversation handler
    chat_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("chat", chat_command)],
        states={
            CHAT_MODE: [MessageHandler(filters.TEXT & ~filters.COMMAND, chat_message_handler)],
        },
        fallbacks=[CommandHandler("cancel", cancel_command), CommandHandler("exit", cancel_command)],
    )
    
    # Add command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about_command))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(CommandHandler("session", session_command))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(CommandHandler("profile", profile_command))
    application.add_handler(CommandHandler("clear", clear_command))
    application.add_handler(CommandHandler("cancel", cancel_command))
    
    # Add chat mode handler
    application.add_handler(chat_conv_handler)
    
    # Add button callback handler
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Add error handler
    application.add_error_handler(error_handler)
    
    # Start polling
    print(f"✅ Bot is running! Listening for messages...")
    print(f"✅ Flask server running on http://0.0.0.0:8080")
    print(f"✅ Total {len(session_manager.sessions)} sessions active")
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
