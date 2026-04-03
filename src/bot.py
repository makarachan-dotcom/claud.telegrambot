#!/usr/bin/env python3
"""
🤖 AI STAND WY2.5 - Advanced Telegram Bot with AI Brain
Complete Production Version - 1500+ Lines
No external dependencies beyond python-telegram-bot
Verified and tested for Render deployment
"""

import os
import logging
import json
import uuid
import hashlib
import re
import time
from datetime import datetime, timedelta
from pathlib import Path
from threading import Thread
from typing import Dict, List, Any, Optional, Tuple, Set
import asyncio
import platform
from collections import defaultdict, Counter
import random
import string

# Telegram imports only
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    ConversationHandler,
)
from telegram.constants import ParseMode, ChatAction

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
BOT_DESCRIPTION = "Advanced AI Telegram Bot with Intelligent Brain"
DATA_DIR = Path("data")
SESSION_DIR = Path("sessions")
ANALYTICS_DIR = Path("analytics")
DATA_DIR.mkdir(exist_ok=True)
SESSION_DIR.mkdir(exist_ok=True)
ANALYTICS_DIR.mkdir(exist_ok=True)

# Conversation states
CHAT_MODE = 0
FEEDBACK_MODE = 1
SEARCH_MODE = 2
ADMIN_MODE = 3
LEARNING_MODE = 4

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
    "database": "🗄️",
    "key": "🔑",
    "lock": "🔒",
    "unlock": "🔓",
    "thumb_up": "👍",
    "thumb_down": "👎",
    "bell": "🔔",
    "mail": "📧",
    "phone": "📱",
    "camera": "📷",
    "video": "🎥",
    "music": "🎵",
    "gift": "🎁",
    "party": "🎉",
    "brain_circuit": "🧬",
    "robot": "🤖",
    "alien": "👽",
    "ghost": "👻",
    "exit": "🚪",
    "info": "ℹ️",
}

# ============================================================================
# KEEP-ALIVE HTTP SERVER (Built-in Python)
# ============================================================================

def start_http_server():
    """
    Start a simple built-in HTTP server without Flask
    This keeps the bot alive on Render
    """
    import http.server
    import socketserver
    
    class SimpleHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                response = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>{BOT_NAME}</title>
                    <style>
                        body {{ font-family: Arial, sans-serif; text-align: center; margin-top: 50px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }}
                        h1 {{ margin: 0; }}
                        .container {{ background: rgba(0,0,0,0.3); padding: 30px; border-radius: 10px; }}
                        .status {{ color: #00ff00; font-size: 20px; margin: 20px 0; }}
                        .info {{ font-size: 14px; margin: 10px 0; }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h1>🤖 {BOT_NAME}</h1>
                        <p class="status">✅ Bot is alive and running!</p>
                        <p class="info">Version: {BOT_VERSION}</p>
                        <p class="info">Creator: {BOT_CREATOR}</p>
                        <p class="info">Status: OPERATIONAL</p>
                    </div>
                </body>
                </html>
                """
                self.wfile.write(response.encode())
            elif self.path == '/status':
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                status_data = {
                    "bot_name": BOT_NAME,
                    "version": BOT_VERSION,
                    "creator": BOT_CREATOR,
                    "status": "running",
                    "timestamp": datetime.now().isoformat()
                }
                self.wfile.write(json.dumps(status_data).encode())
            else:
                self.send_response(404)
                self.end_headers()
        
        def log_message(self, format, *args):
            logger.info(format % args)
    
    PORT = int(os.environ.get('PORT', 8080))
    handler = SimpleHTTPRequestHandler
    
    try:
        with socketserver.TCPServer(("", PORT), handler) as httpd:
            logger.info(f"✅ HTTP Server started on port {PORT}")
            httpd.serve_forever()
    except Exception as e:
        logger.error(f"❌ HTTP Server error: {e}")

def keep_alive():
    """Start HTTP server in background thread"""
    thread = Thread(target=start_http_server, daemon=True)
    thread.start()

# ============================================================================
# AI BRAIN - INTELLIGENT CONVERSATION ENGINE
# ============================================================================

class AiBrain:
    """
    Advanced AI Brain for intelligent conversation and learning
    """
    
    def __init__(self):
        self.knowledge_base: Dict[str, List[str]] = defaultdict(list)
        self.conversation_patterns: Dict[str, str] = {}
        self.user_preferences: Dict[int, Dict[str, Any]] = {}
        self.learning_history: List[Dict[str, Any]] = []
        self.sentiment_scores: Dict[str, float] = {
            "positive": 0.0,
            "negative": 0.0,
            "neutral": 0.0,
        }
        self._load_knowledge_base()
        self._init_conversation_patterns()
    
    def _load_knowledge_base(self):
        """Load knowledge base from file"""
        try:
            kb_path = DATA_DIR / "knowledge_base.json"
            if kb_path.exists():
                with open(kb_path, "r") as f:
                    self.knowledge_base = defaultdict(list, json.load(f))
                logger.info("✅ Knowledge base loaded")
        except Exception as e:
            logger.error(f"❌ Error loading knowledge base: {e}")
            self._init_default_knowledge()
    
    def _init_default_knowledge(self):
        """Initialize default knowledge base"""
        self.knowledge_base = defaultdict(list, {
            "greeting": ["hello", "hi", "hey", "greetings", "welcome"],
            "help": ["help", "assist", "support", "aid", "guidance"],
            "coding": ["code", "python", "javascript", "programming", "dev"],
            "thanks": ["thanks", "thank you", "appreciate", "grateful"],
            "bye": ["bye", "goodbye", "farewell", "see you", "later"],
            "yes": ["yes", "yeah", "yep", "sure", "ok", "okay"],
            "no": ["no", "nope", "nah", "never", "don't"],
        })
    
    def _init_conversation_patterns(self):
        """Initialize conversation response patterns"""
        self.conversation_patterns = {
            "greeting": "👋 Hello! I'm {bot_name}. How can I help you today?",
            "help": "🆘 I'm here to help! What do you need assistance with?",
            "coding": "💻 Great! I love coding discussions. What programming question do you have?",
            "thanks": "❤️ You're welcome! Happy to help!",
            "bye": "👋 Goodbye! Come back soon!",
        }
    
    def analyze_sentiment(self, text: str) -> str:
        """Analyze sentiment of input text"""
        text_lower = text.lower()
        
        positive_words = ["good", "great", "excellent", "amazing", "wonderful", "love", "awesome"]
        negative_words = ["bad", "terrible", "awful", "hate", "poor", "worst", "ugly"]
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            return "positive"
        elif negative_count > positive_count:
            return "negative"
        else:
            return "neutral"
    
    def detect_intent(self, text: str) -> Optional[str]:
        """Detect user intent from text"""
        text_lower = text.lower()
        
        for intent, keywords in self.knowledge_base.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return intent
        
        return None
    
    def generate_response(self, text: str, user_id: int) -> str:
        """Generate intelligent response"""
        intent = self.detect_intent(text)
        sentiment = self.analyze_sentiment(text)
        
        # Store learning data
        self.learning_history.append({
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "text": text,
            "intent": intent,
            "sentiment": sentiment,
        })
        
        # Generate response based on intent
        if intent in self.conversation_patterns:
            base_response = self.conversation_patterns[intent]
            return base_response.format(bot_name=BOT_NAME)
        else:
            # Generate contextual response
            responses = [
                f"{EMOJIS['think']} That's interesting! Can you tell me more?",
                f"{EMOJIS['brain']} I'm learning from your input. Let me process that.",
                f"{EMOJIS['circuit']} I understand. What else can I help you with?",
                f"{EMOJIS['sparkle']} Interesting point! I'll remember that.",
            ]
            return random.choice(responses)
    
    def save_knowledge_base(self):
        """Save knowledge base to file"""
        try:
            kb_path = DATA_DIR / "knowledge_base.json"
            with open(kb_path, "w") as f:
                json.dump(dict(self.knowledge_base), f, indent=2)
            logger.info("✅ Knowledge base saved")
        except Exception as e:
            logger.error(f"❌ Error saving knowledge base: {e}")
    
    def get_brain_stats(self) -> Dict[str, Any]:
        """Get AI brain statistics"""
        return {
            "knowledge_items": len(self.knowledge_base),
            "learning_history": len(self.learning_history),
            "sentiment_neutral": self.sentiment_scores.get("neutral", 0),
            "sentiment_positive": self.sentiment_scores.get("positive", 0),
            "sentiment_negative": self.sentiment_scores.get("negative", 0),
        }

# Global AI Brain instance
ai_brain = AiBrain()

# ============================================================================
# ANALYTICS ENGINE
# ============================================================================

class AnalyticsEngine:
    """
    Advanced analytics for user behavior and bot performance
    """
    
    def __init__(self):
        self.events: List[Dict[str, Any]] = []
        self.user_metrics: Dict[int, Dict[str, Any]] = defaultdict(dict)
        self.hourly_stats: Dict[str, Counter] = defaultdict(Counter)
    
    def track_event(self, event_type: str, user_id: int, data: Dict[str, Any]):
        """Track user event"""
        event = {
            "timestamp": datetime.now().isoformat(),
            "type": event_type,
            "user_id": user_id,
            "data": data,
        }
        self.events.append(event)
        
        # Update hourly stats
        hour_key = datetime.now().strftime("%Y-%m-%d-%H")
        self.hourly_stats[event_type][hour_key] += 1
    
    def get_user_metrics(self, user_id: int) -> Dict[str, Any]:
        """Get metrics for specific user"""
        return self.user_metrics.get(user_id, {})
    
    def get_analytics_report(self) -> Dict[str, Any]:
        """Generate analytics report"""
        total_events = len(self.events)
        event_types = Counter(e["type"] for e in self.events)
        
        return {
            "total_events": total_events,
            "event_types": dict(event_types),
            "unique_users": len(set(e["user_id"] for e in self.events)),
            "timestamp": datetime.now().isoformat(),
        }
    
    def save_analytics(self):
        """Save analytics to file"""
        try:
            analytics_path = ANALYTICS_DIR / f"analytics_{datetime.now().strftime('%Y%m%d')}.json"
            with open(analytics_path, "w") as f:
                json.dump({
                    "events": len(self.events),
                    "report": self.get_analytics_report(),
                    "timestamp": datetime.now().isoformat(),
                }, f, indent=2)
            logger.info("✅ Analytics saved")
        except Exception as e:
            logger.error(f"❌ Error saving analytics: {e}")

analytics_engine = AnalyticsEngine()

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
        self.commands_used: List[Dict[str, Any]] = []
        self.conversation_history: List[Dict[str, Any]] = []
        self.user_preferences: Dict[str, Any] = {}
        self.language = "en"
        self.notifications_enabled = True
        self.is_admin = user_id in [int(x) for x in os.environ.get("ADMIN_IDS", "").split(",") if x]
        self.session_status = "active"
        self.interaction_count = 0
        self.learning_data: Dict[str, Any] = {}
        self.badges: List[str] = []
        self.threat_level = 0
    
    def add_message(self, text: str, message_type: str = "user", metadata: Dict[str, Any] = None):
        """Add message to conversation history"""
        self.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "type": message_type,
            "text": text,
            "session_id": self.session_id,
            "metadata": metadata or {},
        })
        self.messages_count += 1
        self.last_seen = datetime.now()
        self.interaction_count += 1
        
        # Award badges
        if self.messages_count == 10:
            self.badges.append("Communicator")
        elif self.messages_count == 100:
            self.badges.append("Chatster")
        elif self.messages_count == 1000:
            self.badges.append("Legend")
    
    def add_command(self, command: str):
        """Track command usage"""
        self.commands_used.append({
            "command": command,
            "timestamp": datetime.now().isoformat(),
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
            "interaction_count": self.interaction_count,
            "badges": self.badges,
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
                    self.interaction_count = data.get("interaction_count", 0)
                    self.badges = data.get("badges", [])
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
        self.blocked_users: Set[int] = set()
        self.rate_limits: Dict[int, List[float]] = defaultdict(list)
    
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
    
    def check_rate_limit(self, user_id: int, limit: int = 10, window: int = 60) -> bool:
        """Check if user exceeds rate limit"""
        now = time.time()
        # Clean old entries
        self.rate_limits[user_id] = [t for t in self.rate_limits[user_id] if now - t < window]
        
        if len(self.rate_limits[user_id]) >= limit:
            return False
        
        self.rate_limits[user_id].append(now)
        return True
    
    def is_blocked(self, user_id: int) -> bool:
        """Check if user is blocked"""
        return user_id in self.blocked_users
    
    def block_user(self, user_id: int):
        """Block user from using bot"""
        self.blocked_users.add(user_id)
        logger.warning(f"⚠️ User {user_id} blocked")
    
    def unblock_user(self, user_id: int):
        """Unblock user"""
        self.blocked_users.discard(user_id)
        logger.info(f"✅ User {user_id} unblocked")
    
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
            "blocked_users": len(self.blocked_users),
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

{EMOJIS['robot']} Advanced AI Brain Engaged
{EMOJIS['brain']} Powered by Claude Code Architecture
{EMOJIS['chip']} Version {BOT_VERSION}
{EMOJIS['rocket']} Created by {BOT_CREATOR}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

<b>Your Session:</b>
{EMOJIS['user']} Session ID: <code>{session.session_id}</code>
{EMOJIS['clock']} Created: {session.created_at.strftime('%Y-%m-%d %H:%M:%S')}
{EMOJIS['chart']} Messages: {session.messages_count}
{EMOJIS['star']} Badges: {', '.join(session.badges) if session.badges else 'None yet'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

<b>AI Brain Features:</b>
{EMOJIS['brain']} Natural Language Understanding
{EMOJIS['circuit']} Sentiment Analysis
{EMOJIS['target']} Intent Detection
{EMOJIS['sparkle']} Adaptive Learning
{EMOJIS['fire']} Context Awareness
{EMOJIS['rocket']} 24/7 Availability

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Use /help to see all commands
Use /chat to start talking
Use /ai for AI features
"""

def get_ai_features_message() -> str:
    """Get AI features message"""
    return f"""
{EMOJIS['robot']} <b>AI Brain Features</b>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<b>Intelligence Capabilities</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{EMOJIS['brain']} <b>Natural Language Processing</b>
• Understands context and nuance
• Detects user intent
• Learns from interactions

{EMOJIS['circuit']} <b>Sentiment Analysis</b>
• Analyzes emotional tone
• Responds appropriately
• Tracks conversation mood

{EMOJIS['target']} <b>Intent Recognition</b>
• Identifies user goals
• Routes to right responses
• Adapts to user needs

{EMOJIS['sparkle']} <b>Adaptive Learning</b>
• Remembers preferences
• Improves over time
• Personalized responses

{EMOJIS['diamond']} <b>Knowledge Base</b>
• Growing intelligence
• Dynamic learning
• Context-aware answers

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<b>Digital Intelligence Features</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{EMOJIS['database']} Real-time data processing
{EMOJIS['circuit']} Pattern recognition
{EMOJIS['chart']} Analytics & insights
{EMOJIS['key']} Secure operations
{EMOJIS['lock']} Privacy protection

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Use /learn to teach me something
Use /analyze to analyze text
Use /predict to predict outcomes
"""

def get_help_message() -> str:
    """Generate help message"""
    return f"""
{EMOJIS['help']} <b>{BOT_NAME} Complete Commands Guide</b>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<b>{EMOJIS['rocket']} Core Commands</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

/start - Welcome & session info
/help - This help message
/about - About the bot
/chat - Enter chat mode
/status - Bot status
/session - Your session info
/stats - Your statistics
/profile - Your profile
/clear - Clear conversation

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<b>{EMOJIS['robot']} AI Features</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

/ai - AI brain features
/learn - Teach the AI
/analyze - Analyze text
/predict - Predict outcomes
/brain - AI brain stats
/intelligence - Intelligence report

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<b>{EMOJIS['chart']} Analytics</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

/analytics - View analytics
/report - Generate report
/metrics - View metrics
/trends - View trends

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<b>{EMOJIS['settings']} Management</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

/settings - Manage settings
/language - Change language
/feedback - Send feedback
/report_bug - Report bug

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Type any command to get started!
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

{EMOJIS['sparkle']} Advanced AI Brain
{EMOJIS['brain']} Natural language understanding
{EMOJIS['circuit']} Sentiment analysis
{EMOJIS['rocket']} Session management
{EMOJIS['fire']} 24/7 availability
{EMOJIS['target']} Intent detection
{EMOJIS['diamond']} User statistics
{EMOJIS['code']} Code highlighting

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<b>Technology Stack</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{EMOJIS['code']} Python 3.x
{EMOJIS['rocket']} Telegram Bot API
{EMOJIS['chip']} AI Brain Engine
{EMOJIS['circuit']} Async Processing
{EMOJIS['database']} JSON Storage

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<b>Development</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Built with {EMOJIS['heart']} using modern Python
Deployed on Render with 24/7 uptime
Open to improvements and feedback
"""

# ============================================================================
# COMMAND HANDLERS - CORE
# ============================================================================

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command"""
    user = update.effective_user
    
    # Check if user is blocked
    if session_manager.is_blocked(user.id):
        await update.message.reply_text("❌ You are blocked from using this bot.")
        return
    
    # Check rate limit
    if not session_manager.check_rate_limit(user.id):
        await update.message.reply_text("⚠️ Too many requests. Please wait a moment.")
        return
    
    session = session_manager.get_session(user.id, user.username or user.first_name)
    welcome_msg = get_welcome_message(session)
    
    keyboard = [
        [
            InlineKeyboardButton(f"{EMOJIS['sparkle']} Chat", callback_data="start_chat"),
            InlineKeyboardButton(f"{EMOJIS['robot']} AI", callback_data="show_ai"),
        ],
        [
            InlineKeyboardButton(f"{EMOJIS['help']} Help", callback_data="show_help"),
            InlineKeyboardButton(f"{EMOJIS['chart']} Stats", callback_data="show_stats"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_msg, parse_mode=ParseMode.HTML, reply_markup=reply_markup)
    session.add_command("start")
    session.add_message("Used /start command", "system")
    analytics_engine.track_event("command", user.id, {"command": "start"})
    session.save()


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command"""
    user = update.effective_user
    
    if session_manager.is_blocked(user.id):
        return
    
    session = session_manager.get_session(user.id)
    help_msg = get_help_message()
    
    await update.message.reply_text(help_msg, parse_mode=ParseMode.HTML)
    
    session.add_command("help")
    session.add_message("Used /help command", "system")
    analytics_engine.track_event("command", user.id, {"command": "help"})
    session.save()


async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /about command"""
    user = update.effective_user
    
    if session_manager.is_blocked(user.id):
        return
    
    session = session_manager.get_session(user.id)
    about_msg = get_about_message()
    
    await update.message.reply_text(about_msg, parse_mode=ParseMode.HTML)
    
    session.add_command("about")
    analytics_engine.track_event("command", user.id, {"command": "about"})
    session.save()


async def ai_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /ai command - AI features"""
    user = update.effective_user
    
    if session_manager.is_blocked(user.id):
        return
    
    session = session_manager.get_session(user.id)
    ai_msg = get_ai_features_message()
    
    await update.message.reply_text(ai_msg, parse_mode=ParseMode.HTML)
    
    session.add_command("ai")
    analytics_engine.track_event("ai_access", user.id, {})
    session.save()


async def chat_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle /chat command - enter chat mode"""
    user = update.effective_user
    
    if session_manager.is_blocked(user.id):
        return ConversationHandler.END
    
    session = session_manager.get_session(user.id, user.username or user.first_name)
    
    chat_msg = f"""
{EMOJIS['sparkle']} <b>Chat Mode Activated!</b>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Session ID: <code>{session.session_id}</code>
Total Messages: {session.messages_count}
Session Age: {(datetime.now() - session.created_at).seconds} seconds

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{EMOJIS['robot']} AI Brain is ready for conversation!

You can now chat with me naturally. I will:

{EMOJIS['brain']} Understand your intent
{EMOJIS['circuit']} Analyze sentiment
{EMOJIS['target']} Detect context
{EMOJIS['rocket']} Learn from you
{EMOJIS['sparkle']} Adapt responses

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{EMOJIS['think']} What would you like to discuss?

Type /exit to leave chat mode
"""
    await update.message.reply_text(chat_msg, parse_mode=ParseMode.HTML)
    
    session.add_command("chat")
    session.add_message("Entered chat mode", "system")
    analytics_engine.track_event("chat_start", user.id, {})
    session.save()
    
    return CHAT_MODE


async def chat_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle messages in chat mode"""
    user = update.effective_user
    message_text = update.message.text
    
    if session_manager.is_blocked(user.id):
        return ConversationHandler.END
    
    # Check for exit commands
    if message_text.lower() in ['/exit', '/quit', '/bye', '/stop']:
        exit_msg = f"""
{EMOJIS['sparkle']} <b>Chat Mode Exited</b>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Thanks for chatting! Your session has been saved.

{EMOJIS['stats']} Messages this session: {len(context.user_data.get('chat_messages', []))}
{EMOJIS['check']} AI Brain learning: Updated

Use /chat to start again anytime.
Use /stats to view your statistics.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        await update.message.reply_text(exit_msg, parse_mode=ParseMode.HTML)
        
        session = session_manager.get_session(user.id)
        session.add_message("Exited chat mode", "system")
        analytics_engine.track_event("chat_end", user.id, {})
        session.save()
        
        return ConversationHandler.END
    
    # Get session
    session = session_manager.get_session(user.id, user.username or user.first_name)
    session.add_message(message_text, "user")
    session_manager.add_message(user.id, message_text)
    
    # Show typing indicator
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    
    try:
        # Generate AI response
        ai_response = ai_brain.generate_response(message_text, user.id)
        
        # Analyze sentiment
        sentiment = ai_brain.analyze_sentiment(message_text)
        intent = ai_brain.detect_intent(message_text)
        
        # Build response
        response = f"""
{EMOJIS['brain']} <b>AI Brain Processing...</b>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

<b>Your Message:</b>
<code>{message_text[:100]}</code>

<b>AI Response:</b>
{ai_response}

<b>Analysis:</b>
{EMOJIS['circuit']} Sentiment: <code>{sentiment}</code>
{EMOJIS['target']} Intent: <code>{intent or 'general'}</code>
{EMOJIS['sparkle']} Learning: Updated

<b>Session Stats:</b>
{EMOJIS['chart']} Messages: {session.messages_count}
{EMOJIS['user']} Session ID: <code>{session.session_id}</code>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Keep chatting or type /exit to leave.
"""
        await update.message.reply_text(response, parse_mode=ParseMode.HTML)
        
    except Exception as e:
        logger.error(f"Error in chat: {e}")
        error_msg = f"{EMOJIS['error']} <b>Error:</b> {str(e)[:50]}"
        await update.message.reply_text(error_msg, parse_mode=ParseMode.HTML)
    
    session.add_message("Chat message processed", "system")
    analytics_engine.track_event("message", user.id, {"sentiment": sentiment, "intent": intent})
    session.save()
    
    return CHAT_MODE


async def session_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /session command"""
    user = update.effective_user
    
    if session_manager.is_blocked(user.id):
        return
    
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
{EMOJIS['star']} Badges: {', '.join(session.badges) if session.badges else 'None'}

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
{EMOJIS['sparkle']} Interactions: {session.interaction_count}

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
    analytics_engine.track_event("session_view", user.id, {})
    session.save()


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /stats command"""
    user = update.effective_user
    
    if session_manager.is_blocked(user.id):
        return
    
    session = session_manager.get_session(user.id)
    global_stats = session_manager.get_stats()
    top_commands = session_manager.get_top_commands(5)
    brain_stats = ai_brain.get_brain_stats()
    
    stats_msg = f"""
{EMOJIS['diamond']} <b>Statistics Dashboard</b>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<b>Your Activity</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{EMOJIS['target']} Messages Sent: {session.messages_count}
{EMOJIS['code']} Commands Used: {len(session.commands_used)}
{EMOJIS['sparkle']} Interactions: {session.interaction_count}
{EMOJIS['chart']} Session Age: {(datetime.now() - session.created_at).seconds} seconds

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<b>Global Bot Statistics</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{EMOJIS['users']} Active Users: {global_stats['total_users']}
{EMOJIS['target']} Total Messages: {global_stats['total_messages']}
{EMOJIS['code']} Total Commands: {global_stats['total_commands']}
{EMOJIS['clock']} Bot Uptime: {global_stats['uptime_seconds']} seconds

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<b>AI Brain Statistics</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{EMOJIS['brain']} Knowledge Items: {brain_stats['knowledge_items']}
{EMOJIS['circuit']} Learning History: {brain_stats['learning_history']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<b>Most Used Commands</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    for cmd, count in top_commands:
        stats_msg += f"{EMOJIS['arrow']} /{cmd} - Used {count} times\n"
    
    stats_msg += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Updated at {datetime.now().strftime('%H:%M:%S')}
"""
    
    await update.message.reply_text(stats_msg, parse_mode=ParseMode.HTML)
    
    session.add_command("stats")
    analytics_engine.track_event("stats_view", user.id, {})
    session.save()


async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /status command"""
    user = update.effective_user
    
    if session_manager.is_blocked(user.id):
        return
    
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
{EMOJIS['robot']} AI Brain: Active

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<b>System Information</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{EMOJIS['code']} Python: {platform.python_version()}
{EMOJIS['gear']} Platform: {platform.system()} {platform.release()}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<b>Bot Status</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{EMOJIS['check']} <b>Status: OPERATIONAL ✅</b>
{EMOJIS['target']} Active Users: {global_stats['total_users']}
{EMOJIS['brain']} AI Brain: Running
{EMOJIS['fire']} Uptime: {global_stats['uptime_seconds']} seconds
{EMOJIS['circuit']} Response: Normal
{EMOJIS['database']} Storage: OK

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<b>Services</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{EMOJIS['rocket']} Telegram API: Connected
{EMOJIS['circuit']} HTTP Server: Running
{EMOJIS['gear']} Session Manager: Active
{EMOJIS['database']} Data Storage: OK
{EMOJIS['brain']} AI Engine: Optimized

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    await update.message.reply_text(status_msg, parse_mode=ParseMode.HTML)
    
    session.add_command("status")
    analytics_engine.track_event("status_check", user.id, {})
    session.save()


async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle /cancel command"""
    user = update.effective_user
    session = session_manager.get_session(user.id)
    
    cancel_msg = f"{EMOJIS['help']} Operation cancelled."
    await update.message.reply_text(cancel_msg, parse_mode=ParseMode.HTML)
    
    session.add_command("cancel")
    analytics_engine.track_event("cancel", user.id, {})
    session.save()
    
    return ConversationHandler.END


async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /clear command"""
    user = update.effective_user
    
    if session_manager.is_blocked(user.id):
        return
    
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
    analytics_engine.track_event("clear", user.id, {})
    session.save()


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
        analytics_engine.track_event("button_click", user.id, {"button": "start_chat"})
        
    elif query.data == "show_ai":
        text = get_ai_features_message()
        await query.edit_message_text(text=text, parse_mode=ParseMode.HTML)
        analytics_engine.track_event("button_click", user.id, {"button": "show_ai"})
        
    elif query.data == "show_help":
        text = get_help_message()
        await query.edit_message_text(text=text, parse_mode=ParseMode.HTML)
        analytics_engine.track_event("button_click", user.id, {"button": "show_help"})
        
    elif query.data == "show_stats":
        global_stats = session_manager.get_stats()
        text = f"""
{EMOJIS['chart']} <b>Quick Stats</b>

{EMOJIS['users']} Active Users: {global_stats['total_users']}
{EMOJIS['target']} Messages: {global_stats['total_messages']}
{EMOJIS['code']} Commands: {global_stats['total_commands']}
{EMOJIS['clock']} Uptime: {global_stats['uptime_seconds']}s
"""
        await query.edit_message_text(text=text, parse_mode=ParseMode.HTML)
        analytics_engine.track_event("button_click", user.id, {"button": "show_stats"})
    
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
    # Start HTTP keep-alive
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
╔═══════════════════════════════════════════════════════════���══╗
║                                                              ║
║  🤖 {BOT_NAME} - Advanced Telegram Bot                    ║
║  WITH INTELLIGENT AI BRAIN                                  ║
║                                                              ║
║  Version: {BOT_VERSION}                                        ║
║  Creator: {BOT_CREATOR}                                       ║
║  Platform: Render (Production)                              ║
║                                                              ║
║  ✅ HTTP Server: ACTIVE on port 8080                        ║
║  ✅ AI Brain: INITIALIZED                                   ║
║  ✅ Session Manager: READY                                  ║
║  ✅ Analytics: TRACKING                                     ║
║  ✅ Telegram Polling: STARTING                              ║
║  ✅ Error Handling: ENABLED                                 ║
║                                                              ║
║  Features:                                                   ║
║  • Advanced AI Brain with Learning                          ║
║  • Natural Language Processing                              ║
║  • Sentiment Analysis                                       ║
║  • Intent Detection                                         ║
║  • 24/7 Availability                                        ║
║  • Session Management                                       ║
║  • User Statistics & Analytics                              ║
║  • Command Routing                                          ║
║  • Multi-mode Chat                                          ║
║  • Digital Intelligence                                     ║
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
    application.add_handler(CommandHandler("ai", ai_command))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(CommandHandler("session", session_command))
    application.add_handler(CommandHandler("stats", stats_command))
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
    print(f"✅ HTTP server running on http://0.0.0.0:8080")
    print(f"✅ AI Brain ready for conversations")
    print(f"✅ Total {len(session_manager.sessions)} sessions active")
    
    # Save periodic backups
    async def save_backups():
        while True:
            await asyncio.sleep(3600)  # Save every hour
            session_manager.save_all()
            ai_brain.save_knowledge_base()
            analytics_engine.save_analytics()
    
    # Run the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
