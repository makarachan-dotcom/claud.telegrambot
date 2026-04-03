"""
AI STAND WY2.5 - Bot Configuration
"""

from dataclasses import dataclass, field
from typing import List, Optional
import os
from pathlib import Path


@dataclass
class BotConfig:
    """Bot configuration"""
    
    # Bot Info
    name: str = "AI STAND WY2.5"
    version: str = "2.5.0"
    creator: str = "Kimi K2.5"
    description: str = "Advanced AI Assistant based on Claude Code Architecture"
    
    # Telegram
    token: str = field(default_factory=lambda: os.environ.get("TELEGRAM_BOT_TOKEN", ""))
    
    # Admin
    admin_user_ids: List[int] = field(default_factory=list)
    
    # Paths
    data_dir: Path = field(default_factory=lambda: Path("./data"))
    sessions_dir: Path = field(default_factory=lambda: Path("./sessions"))
    
    # Features
    max_message_length: int = 4000
    max_conversation_history: int = 100
    enable_typing_indicator: bool = True
    enable_session_persistence: bool = True
    
    # Query Engine
    max_turns: int = 8
    max_budget_tokens: int = 2000
    
    @classmethod
    def from_env(cls) -> "BotConfig":
        """Load config from environment variables"""
        config = cls()
        
        # Load admin IDs
        admin_ids_str = os.environ.get("ADMIN_USER_IDS", "")
        if admin_ids_str:
            config.admin_user_ids = [int(id.strip()) for id in admin_ids_str.split(",")]
        
        # Load paths
        config.data_dir = Path(os.environ.get("DATA_DIR", "./data"))
        config.sessions_dir = Path(os.environ.get("SESSION_DIR", "./sessions"))
        
        return config
    
    def ensure_directories(self):
        """Ensure required directories exist"""
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.sessions_dir.mkdir(parents=True, exist_ok=True)


# Global config instance
config = BotConfig.from_env()
