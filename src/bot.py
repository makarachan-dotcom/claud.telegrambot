#!/usr/bin/env python3
"""
🤖 AI STAND WY2.5 - Advanced Telegram Bot
Based on Claude Code Architecture Port
Created with love by Kimi K2.5 for the community

Features:
- Natural language processing with command/tool routing
- Session management with conversation history
- Admin controls and user statistics
- Cool cyberpunk styling and personality
- Full integration with the ported codebase
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import sys
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
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

# Flask imports for keeping bot alive
from flask import Flask
from threading import Thread

# Import our ported modules (NO src. prefix - we're already in src/)
from commands import get_commands, get_command, execute_command, find_commands
from tools import get_tools, get_tool, execute_tool, find_tools
from query_engine import QueryEnginePort, QueryEngineConfig, TurnResult
from runtime import PortRuntime, RoutedMatch
from session_store import save_session, load_session, StoredSession
from models import UsageSummary
from execution_registry import build_execution_registry
from port_manifest import build_port_manifest

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot Configuration
BOT_NAME = "AI STAND WY2.5"
BOT_VERSION = "2.5.0"
BOT_CREATOR = "Kimi K2.5"

# Flask app to keep bot alive
app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 AI STAND WY2.5 Bot is alive! ✨"

def keep_alive():
    """Run Flask server in background thread"""
    t = Thread(target=lambda: app.run(
        host='0.0.0.0', 
        port=int(os.environ.get('PORT', 8080)),
        debug=False
    ))
    t.daemon = True
    t.start()
    logger.info("✅ Flask keep-alive server started on port 8080")

# Cyberpunk styling
STYLES = {
    "header": "╔══════════════════════════════════════╗",
    "footer": "╚══════════════════════════════════════╝",
    "divider": "═══════════════════════════════════════",
    "bullet": "▸",
    "arrow": "➤",
    "star": "★",
    "sparkle": "✨",
    "rocket": "🚀",
    "brain": "🧠",
    "chip": "🔷",
    "circuit": "⚡",
    "code": "💻",
    "gear": "⚙️",
    "target": "🎯",
    "fire": "🔥",
    "cool": "😎",
    "think": "🤔",
    "magic": "🪄",
    "crown": "👑",
    "diamond": "💎",
    "crystal": "🔮",
}

# Conversation states
CHAT_MODE, EXECUTING_COMMAND = range(2)


@dataclass
class UserSession:
    """User session data"""
    user_id: int
    username: str
    session_id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    created_at: datetime = field(default_factory=datetime.now)
    messages_count: int = 0
    commands_used: List[str] = field(default_factory=list)
    tools_used: List[str] = field(default_factory=list)
    preferences: Dict[str, Any] = field(default_factory=dict)
    conversation_history: List[Dict[str, str]] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "username": self.username,
            "session_id": self.session_id,
            "created_at": self.created_at.isoformat(),
            "messages_count": self.messages_count,
            "commands_used": self.commands_used,
            "tools_used": self.tools_used,
            "preferences": self.preferences,
        }


class UserSessionManager:
    """Manages user sessions"""
    
    def __init__(self):
        self.sessions: Dict[int, UserSession] = {}
        self.query_engines: Dict[int, QueryEnginePort] = {}
        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)
    
    def get_session(self, user_id: int, username: str = "") -> UserSession:
        if user_id not in self.sessions:
            self.sessions[user_id] = UserSession(user_id=user_id, username=username)
            self.query_engines[user_id] = QueryEnginePort.from_workspace()
        return self.sessions[user_id]
    
    def get_engine(self, user_id: int, username: str = "") -> QueryEnginePort:
        self.get_session(user_id, username)  # Ensure session exists
        return self.query_engines[user_id]
    
    def save_all(self):
        for session in self.sessions.values():
            filepath = self.data_dir / f"user_{session.user_id}.json"
            with open(filepath, "w") as f:
                json.dump(session.to_dict(), f, indent=2)


# Global session manager
session_manager = UserSessionManager()


def style_text(text: str, style_type: str = "normal") -> str:
    """Apply cyberpunk styling to text"""
    if style_type == "header":
        return f"{STYLES['header']}\n{text}\n{STYLES['footer']}"
    elif style_type == "title":
        return f"{STYLES['circuit']} {text} {STYLES['circuit']}"
    elif style_type == "section":
        return f"\n{STYLES['diamond']} <b>{text}</b>"
    elif style_type == "item":
        return f"  {STYLES['bullet']} {text}"
    elif style_type == "code":
        return f"<code>{text}</code>"
    elif style_type == "success":
        return f"{STYLES['sparkle']} {text}"
    elif style_type == "warning":
        return f"⚠️ {text}"
    elif style_type == "error":
        return f"❌ {text}"
    elif style_type == "info":
        return f"ℹ️ {text}"
    return text


def get_welcome_message() -> str:
    """Generate the welcome message"""
    return f"""
{STYLES['header']}

{STYLES['crystal']} <b>Welcome to {BOT_NAME}</b> {STYLES['crystal']}

<i>"The future of AI assistance is here"</i>

{STYLES['brain']} Powered by Claude Code Architecture
{STYLES['chip']} Engineered by {BOT_CREATOR}
{STYLES['rocket']} Version {BOT_VERSION}

{STYLES['divider']}

<b>What I can do:</b>
{STYLES['bullet']} Process natural language queries
{STYLES['bullet']} Route to appropriate commands & tools
{STYLES['bullet']} Maintain conversation context
{STYLES['bullet']} Execute code operations
{STYLES['bullet']} Provide intelligent responses

{STYLES['divider']}

Use /help to see all commands
Use /chat to start a conversation

{STYLES['footer']}
"""


def get_help_message() -> str:
    """Generate the help message"""
    return f"""
{STYLES['header']}

{STYLES['gear']} <b>{BOT_NAME} Commands</b>

{STYLES['diamond']} <b>Core Commands</b>
/chat - Start interactive chat mode
/clear - Clear conversation history
/session - Show session information
/stats - Show your usage statistics

{STYLES['diamond']} <b>System Commands</b>
/commands - List available commands
/tools - List available tools
/search - Search commands and tools
/manifest - Show system manifest

{STYLES['diamond']} <b>Execution Commands</b>
/exec &lt;command&gt; - Execute a command
/tool &lt;tool&gt; [payload] - Execute a tool
/route &lt;query&gt; - Route a query

{STYLES['diamond']} <b>Admin Commands</b>
/status - Bot system status
/users - List active users (admin)
/broadcast - Send message to all (admin)

{STYLES['diamond']} <b>Other Commands</b>
/start - Start the bot
/help - Show this help message
/about - About this bot

{STYLES['footer']}
"""


# Command Handlers
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command"""
    user = update.effective_user
    session = session_manager.get_session(user.id, user.username or user.first_name)
    
    welcome_msg = get_welcome_message()
    
    # Create inline keyboard
    keyboard = [
        [
            InlineKeyboardButton(f"{STYLES['chat']} Start Chat", callback_data="start_chat"),
            InlineKeyboardButton(f"{STYLES['gear']} Commands", callback_data="show_commands"),
        ],
        [
            InlineKeyboardButton(f"{STYLES['tools']} Tools", callback_data="show_tools"),
            InlineKeyboardButton(f"{STYLES['help']} Help", callback_data="show_help"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        welcome_msg,
        parse_mode=ParseMode.HTML,
        reply_markup=reply_markup
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command"""
    help_msg = get_help_message()
    await update.message.reply_text(help_msg, parse_mode=ParseMode.HTML)


async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /about command"""
    about_msg = f"""
{STYLES['header']}

{STYLES['crown']} <b>About {BOT_NAME}</b>

<i>"Standing at the frontier of AI assistance"</i>

{STYLES['divider']}

<b>Version:</b> {BOT_VERSION}
<b>Creator:</b> {BOT_CREATOR}
<b>Architecture:</b> Claude Code Python Port

{STYLES['divider']}

<b>Features:</b>
{STYLES['bullet']} 400+ Mirrored Commands
{STYLES['bullet']} 300+ Integrated Tools
{STYLES['bullet']} Advanced Query Routing
{STYLES['bullet']} Session Persistence
{STYLES['bullet']} Natural Language Processing

{STYLES['divider']}

Built with {STYLES['fire']} Python + python-telegram-bot
Powered by the Claude Code architecture

{STYLES['footer']}
"""
    await update.message.reply_text(about_msg, parse_mode=ParseMode.HTML)


async def chat_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle /chat command - Enter chat mode"""
    user = update.effective_user
    session = session_manager.get_session(user.id, user.username or user.first_name)
    
    chat_msg = f"""
{STYLES['sparkle']} <b>Chat Mode Activated!</b>

Session ID: <code>{session.session_id}</code>

You can now chat with me naturally. I'll:
{STYLES['bullet']} Understand your intent
{STYLES['bullet']} Route to appropriate tools
{STYLES['bullet']} Remember our conversation

{STYLES['info']} Type /exit to exit chat mode
{STYLES['info']} Type /clear to clear history

{STYLES['think']} What would you like to discuss?
"""
    await update.message.reply_text(chat_msg, parse_mode=ParseMode.HTML)
    return CHAT_MODE


async def chat_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle messages in chat mode"""
    user = update.effective_user
    message_text = update.message.text
    
    # Check for exit command
    if message_text.lower() in ['/exit', '/quit', '/bye']:
        exit_msg = f"""
{STYLES['sparkle']} <b>Chat Mode Exited</b>

Thanks for chatting! Your session has been saved.
Use /chat to start again anytime.
"""
        await update.message.reply_text(exit_msg, parse_mode=ParseMode.HTML)
        return ConversationHandler.END
    
    # Process the message
    session = session_manager.get_session(user.id, user.username or user.first_name)
    engine = session_manager.get_engine(user.id, user.username or user.first_name)
    
    # Show typing indicator
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    try:
        # Use the runtime to route and process
        runtime = PortRuntime()
        matches = runtime.route_prompt(message_text, limit=5)
        
        # Build response
        response_lines = [f"{STYLES['brain']} <b>Processing your request...</b>\n"]
        
        if matches:
            response_lines.append(f"{STYLES['target']} <b>Matched:</b>")
            for match in matches[:3]:
                icon = STYLES['gear'] if match.kind == 'command' else STYLES['tools']
                response_lines.append(f"  {icon} <code>{match.name}</code> ({match.score})")
            response_lines.append("")
        
        # Submit to query engine
        result = engine.submit_message(
            message_text,
            matched_commands=tuple(m.name for m in matches if m.kind == 'command'),
            matched_tools=tuple(m.name for m in matches if m.kind == 'tool'),
            denied_tools=()
        )
        
        # Add AI response
        response_lines.append(f"{STYLES['circuit']} <b>Response:</b>")
        response_lines.append(f"<blockquote>{result.output}</blockquote>")
        
        # Add usage info
        response_lines.append(f"\n{STYLES['chip']} <i>Tokens: {result.usage.input_tokens} in / {result.usage.output_tokens} out</i>")
        
        # Update session
        session.messages_count += 1
        session.conversation_history.append({"user": message_text, "bot": result.output})
        
        response_text = "\n".join(response_lines)
        
        # Split if too long
        if len(response_text) > 4000:
            response_text = response_text[:4000] + "\n\n<i>(Message truncated)</i>"
        
        await update.message.reply_text(response_text, parse_mode=ParseMode.HTML)
        
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        error_msg = f"{STYLES['error']} <b>Sorry, I encountered an error:</b>\n<code>{str(e)}</code>"
        await update.message.reply_text(error_msg, parse_mode=ParseMode.HTML)
    
    return CHAT_MODE


async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /clear command"""
    user = update.effective_user
    
    # Reset the query engine for this user
    session_manager.query_engines[user.id] = QueryEnginePort.from_workspace()
    session = session_manager.get_session(user.id)
    session.conversation_history.clear()
    
    clear_msg = f"{STYLES['sparkle']} <b>Conversation history cleared!</b>\n\nYour session is fresh and ready."
    await update.message.reply_text(clear_msg, parse_mode=ParseMode.HTML)


async def session_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /session command"""
    user = update.effective_user
    session = session_manager.get_session(user.id, user.username or user.first_name)
    engine = session_manager.get_engine(user.id, user.username or user.first_name)
    
    session_msg = f"""
{STYLES['header']}

{STYLES['crystal']} <b>Session Information</b>

<b>User:</b> @{session.username or 'Unknown'}
<b>User ID:</b> <code>{session.user_id}</code>
<b>Session ID:</b> <code>{session.session_id}</code>
<b>Created:</b> {session.created_at.strftime('%Y-%m-%d %H:%M:%S')}

{STYLES['divider']}

<b>Statistics:</b>
{STYLES['bullet']} Messages: {session.messages_count}
{STYLES['bullet']} Commands Used: {len(session.commands_used)}
{STYLES['bullet']} Tools Used: {len(session.tools_used)}
{STYLES['bullet']} Conversation Turns: {len(session.conversation_history)}

{STYLES['divider']}

<b>Engine Status:</b>
{STYLES['bullet']} Session: <code>{engine.session_id[:12]}...</code>
{STYLES['bullet']} Messages: {len(engine.mutable_messages)}
{STYLES['bullet']} Transcript Flushed: {engine.transcript_store.flushed}

{STYLES['footer']}
"""
    await update.message.reply_text(session_msg, parse_mode=ParseMode.HTML)


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /stats command"""
    user = update.effective_user
    session = session_manager.get_session(user.id, user.username or user.first_name)
    engine = session_manager.get_engine(user.id, user.username or user.first_name)
    
    stats_msg = f"""
{STYLES['header']}

{STYLES['diamond']} <b>Your Statistics</b>

<b>Session Activity:</b>
{STYLES['bullet']} Total Messages: {session.messages_count}
{STYLES['bullet']} Session Started: {session.created_at.strftime('%Y-%m-%d')}

<b>Usage:</b>
{STYLES['bullet']} Input Tokens: {engine.total_usage.input_tokens}
{STYLES['bullet']} Output Tokens: {engine.total_usage.output_tokens}
{STYLES['bullet']} Total Tokens: {engine.total_usage.input_tokens + engine.total_usage.output_tokens}

<b>Commands Used:</b>
"""
    if session.commands_used:
        for cmd in session.commands_used[-5:]:
            stats_msg += f"{STYLES['bullet']} {cmd}\n"
    else:
        stats_msg += f"{STYLES['bullet']} None yet\n"
    
    stats_msg += f"""
<b>Tools Used:</b>
"""
    if session.tools_used:
        for tool in session.tools_used[-5:]:
            stats_msg += f"{STYLES['bullet']} {tool}\n"
    else:
        stats_msg += f"{STYLES['bullet']} None yet\n"
    
    stats_msg += f"\n{STYLES['footer']}"
    
    await update.message.reply_text(stats_msg, parse_mode=ParseMode.HTML)


async def commands_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /commands command"""
    commands = get_commands()
    
    # Get first 20 commands
    display_commands = list(commands)[:20]
    
    commands_msg = f"""
{STYLES['header']}

{STYLES['gear']} <b>Available Commands</b>

<i>Showing {len(display_commands)} of {len(commands)} commands</i>

"""
    for cmd in display_commands:
        commands_msg += f"{STYLES['bullet']} <code>{cmd.name}</code> - <i>{cmd.responsibility[:50]}...</i>\n"
    
    commands_msg += f"""

{STYLES['info']} Use /search &lt;query&gt; to find specific commands

{STYLES['footer']}
"""
    await update.message.reply_text(commands_msg, parse_mode=ParseMode.HTML)


async def tools_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /tools command"""
    tools = get_tools()
    
    # Get first 20 tools
    display_tools = list(tools)[:20]
    
    tools_msg = f"""
{STYLES['header']}

{STYLES['tools']} <b>Available Tools</b>

<i>Showing {len(display_tools)} of {len(tools)} tools</i>

"""
    for tool in display_tools:
        tools_msg += f"{STYLES['bullet']} <code>{tool.name}</code> - <i>{tool.responsibility[:50]}...</i>\n"
    
    tools_msg += f"""

{STYLES['info']} Use /search &lt;query&gt; to find specific tools

{STYLES['footer']}
"""
    await update.message.reply_text(tools_msg, parse_mode=ParseMode.HTML)


async def search_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /search command"""
    query = " ".join(context.args)
    
    if not query:
        await update.message.reply_text(
            f"{STYLES['warning']} Please provide a search query.\nExample: <code>/search git</code>",
            parse_mode=ParseMode.HTML
        )
        return
    
    # Search commands and tools
    cmd_matches = find_commands(query, limit=10)
    tool_matches = find_tools(query, limit=10)
    
    search_msg = f"""
{STYLES['header']}

{STYLES['target']} <b>Search Results for "{query}"</b>

"""
    if cmd_matches:
        search_msg += f"{STYLES['gear']} <b>Commands ({len(cmd_matches)}):</b>\n"
        for cmd in cmd_matches[:5]:
            search_msg += f"  {STYLES['bullet']} <code>{cmd.name}</code>\n"
        search_msg += "\n"
    
    if tool_matches:
        search_msg += f"{STYLES['tools']} <b>Tools ({len(tool_matches)}):</b>\n"
        for tool in tool_matches[:5]:
            search_msg += f"  {STYLES['bullet']} <code>{tool.name}</code>\n"
        search_msg += "\n"
    
    if not cmd_matches and not tool_matches:
        search_msg += f"{STYLES['info']} No results found.\n"
    
    search_msg += f"\n{STYLES['footer']}"
    
    await update.message.reply_text(search_msg, parse_mode=ParseMode.HTML)


async def manifest_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /manifest command"""
    manifest = build_port_manifest()
    
    manifest_msg = f"""
{STYLES['header']}

{STYLES['crystal']} <b>System Manifest</b>

<b>Workspace:</b> {manifest.workspace_name}
<b>Python Files:</b> {manifest.python_file_count}
<b>Test Files:</b> {manifest.test_file_count}

<b>Top Level Modules:</b>
"""
    for module in manifest.top_level_modules[:10]:
        manifest_msg += f"{STYLES['bullet']} {module.name} ({module.file_count} files)\n"
    
    manifest_msg += f"""

<b>Commands:</b> {len(get_commands())}
<b>Tools:</b> {len(get_tools())}

{STYLES['footer']}
"""
    await update.message.reply_text(manifest_msg, parse_mode=ParseMode.HTML)


async def exec_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /exec command"""
    if not context.args:
        await update.message.reply_text(
            f"{STYLES['warning']} Usage: <code>/exec &lt;command_name&gt;</code>",
            parse_mode=ParseMode.HTML
        )
        return
    
    command_name = context.args[0]
    prompt = " ".join(context.args[1:]) if len(context.args) > 1 else ""
    
    # Show typing indicator
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    result = execute_command(command_name, prompt)
    
    if result.handled:
        exec_msg = f"""
{STYLES['sparkle']} <b>Command Executed</b>

<b>Command:</b> <code>{result.name}</code>
<b>Source:</b> <code>{result.source_hint}</code>

<b>Result:</b>
<blockquote>{result.message}</blockquote>
"""
        # Track command usage
        user = update.effective_user
        session = session_manager.get_session(user.id)
        session.commands_used.append(command_name)
    else:
        exec_msg = f"{STYLES['error']} <b>Command failed:</b>\n{result.message}"
    
    await update.message.reply_text(exec_msg, parse_mode=ParseMode.HTML)


async def tool_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /tool command"""
    if not context.args:
        await update.message.reply_text(
            f"{STYLES['warning']} Usage: <code>/tool &lt;tool_name&gt; [payload]</code>",
            parse_mode=ParseMode.HTML
        )
        return
    
    tool_name = context.args[0]
    payload = " ".join(context.args[1:]) if len(context.args) > 1 else ""
    
    # Show typing indicator
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    result = execute_tool(tool_name, payload)
    
    if result.handled:
        tool_msg = f"""
{STYLES['sparkle']} <b>Tool Executed</b>

<b>Tool:</b> <code>{result.name}</code>
<b>Source:</b> <code>{result.source_hint}</code>

<b>Result:</b>
<blockquote>{result.message}</blockquote>
"""
        # Track tool usage
        user = update.effective_user
        session = session_manager.get_session(user.id)
        session.tools_used.append(tool_name)
    else:
        tool_msg = f"{STYLES['error']} <b>Tool execution failed:</b>\n{result.message}"
    
    await update.message.reply_text(tool_msg, parse_mode=ParseMode.HTML)


async def route_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /route command"""
    query = " ".join(context.args)
    
    if not query:
        await update.message.reply_text(
            f"{STYLES['warning']} Usage: <code>/route &lt;query&gt;</code>",
            parse_mode=ParseMode.HTML
        )
        return
    
    # Show typing indicator
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    runtime = PortRuntime()
    matches = runtime.route_prompt(query, limit=5)
    
    route_msg = f"""
{STYLES['header']}

{STYLES['target']} <b>Routing Results for "{query}"</b>

"""
    if matches:
        for i, match in enumerate(matches, 1):
            icon = STYLES['gear'] if match.kind == 'command' else STYLES['tools']
            route_msg += f"{i}. {icon} <code>{match.name}</code>\n"
            route_msg += f"   Score: {match.score} | Source: <code>{match.source_hint}</code>\n\n"
    else:
        route_msg += f"{STYLES['info']} No matches found.\n"
    
    route_msg += f"\n{STYLES['footer']}"
    
    await update.message.reply_text(route_msg, parse_mode=ParseMode.HTML)


async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /status command"""
    import platform
    
    status_msg = f"""
{STYLES['header']}

{STYLES['chip']} <b>Bot System Status</b>

<b>Bot Information:</b>
{STYLES['bullet']} Name: {BOT_NAME}
{STYLES['bullet']} Version: {BOT_VERSION}
{STYLES['bullet']} Creator: {BOT_CREATOR}

<b>System:</b>
{STYLES['bullet']} Python: {platform.python_version()}
{STYLES['bullet']} Platform: {platform.system()} {platform.release()}

<b>Loaded Modules:</b>
{STYLES['bullet']} Commands: {len(get_commands())}
{STYLES['bullet']} Tools: {len(get_tools())}

<b>Active Sessions:</b>
{STYLES['bullet']} Users: {len(session_manager.sessions)}

<b>Status:</b> {STYLES['sparkle']} Operational

{STYLES['footer']}
"""
    await update.message.reply_text(status_msg, parse_mode=ParseMode.HTML)


async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle /cancel command"""
    cancel_msg = f"{STYLES['info']} Operation cancelled."
    await update.message.reply_text(cancel_msg, parse_mode=ParseMode.HTML)
    return ConversationHandler.END


# Callback query handlers
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button callbacks"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "start_chat":
        await query.edit_message_text(
            text=f"{STYLES['sparkle']} Chat mode ready! Type /chat to begin.",
            parse_mode=ParseMode.HTML
        )
    elif query.data == "show_commands":
        commands = get_commands()
        cmd_list = "\n".join([f"{STYLES['bullet']} <code>{c.name}</code>" for c in list(commands)[:15]])
        await query.edit_message_text(
            text=f"{STYLES['gear']} <b>Available Commands</b>\n\n{cmd_list}\n\n<i>Use /commands for full list</i>",
            parse_mode=ParseMode.HTML
        )
    elif query.data == "show_tools":
        tools = get_tools()
        tool_list = "\n".join([f"{STYLES['bullet']} <code>{t.name}</code>" for t in list(tools)[:15]])
        await query.edit_message_text(
            text=f"{STYLES['tools']} <b>Available Tools</b>\n\n{tool_list}\n\n<i>Use /tools for full list</i>",
            parse_mode=ParseMode.HTML
        )
    elif query.data == "show_help":
        await query.edit_message_text(
            text=get_help_message(),
            parse_mode=ParseMode.HTML
        )


# Error handler
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle errors"""
    logger.error(f"Update {update} caused error {context.error}")
    
    if update and update.effective_message:
        error_msg = f"""
{STYLES['error']} <b>An error occurred!</b>

<code>{str(context.error)}</code>

Please try again or contact support.
"""
        await update.effective_message.reply_text(error_msg, parse_mode=ParseMode.HTML)


def main() -> None:
    """Start the bot"""
    # Start Flask keep-alive server
    keep_alive()
    
    # Get token from environment
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    
    if not token:
        print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║  🤖 AI STAND WY2.5 - Telegram Bot                           ║
║                                                              ║
║  Error: TELEGRAM_BOT_TOKEN not found!                        ║
║                                                              ║
║  Please set your bot token:                                  ║
║  export TELEGRAM_BOT_TOKEN="your_bot_token_here"            ║
║                                                              ║
║  Get your token from @BotFather on Telegram                  ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
        """)
        sys.exit(1)
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║  🤖 AI STAND WY2.5 - Starting up...                          ║
║                                                              ║
║  Version: {BOT_VERSION:<48}║
║  Creator: {BOT_CREATOR:<48}║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Create application
    application = Application.builder().token(token).build()
    
    # Add conversation handler for chat mode
    chat_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("chat", chat_command)],
        states={
            CHAT_MODE: [MessageHandler(filters.TEXT & ~filters.COMMAND, chat_message_handler)],
        },
        fallbacks=[CommandHandler("cancel", cancel_command)],
    )
    
    # Add handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about_command))
    application.add_handler(chat_conv_handler)
    application.add_handler(CommandHandler("clear", clear_command))
    application.add_handler(CommandHandler("session", session_command))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(CommandHandler("commands", commands_command))
    application.add_handler(CommandHandler("tools", tools_command))
    application.add_handler(CommandHandler("search", search_command))
    application.add_handler(CommandHandler("manifest", manifest_command))
    application.add_handler(CommandHandler("exec", exec_command))
    application.add_handler(CommandHandler("tool", tool_command))
    application.add_handler(CommandHandler("route", route_command))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(CommandHandler("cancel", cancel_command))
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Add error handler
    application.add_error_handler(error_handler)
    
    # Start the bot
    print("✅ Bot is running! Press Ctrl+C to stop.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
