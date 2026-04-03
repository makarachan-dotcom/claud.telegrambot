# 🤖 AI STAND WY2.5 - Advanced Telegram Bot

<p align="center">
  <img src="https://img.shields.io/badge/Version-2.5.0-blue?style=for-the-badge" alt="Version">
  <img src="https://img.shields.io/badge/Python-3.9+-green?style=for-the-badge&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Telegram-Bot-blue?style=for-the-badge&logo=telegram" alt="Telegram">
</p>

<p align="center">
  <i>"Standing at the frontier of AI assistance"</i>
</p>

---

## ✨ Features

- **🧠 Natural Language Processing** - Chat naturally with intelligent routing
- **⚡ 400+ Commands** - Full integration with Claude Code architecture
- **🔧 300+ Tools** - Extensive tool library for various operations
- **💬 Session Management** - Persistent conversation history
- **🎯 Smart Routing** - Automatic command/tool matching
- **📊 User Statistics** - Track your usage and activity
- **🔒 Admin Controls** - Built-in admin features
- **🎨 Cyberpunk Styling** - Cool visual design

---

## 🚀 Quick Start

### 1. Get Your Bot Token

1. Open Telegram and search for [@BotFather](https://t.me/BotFather)
2. Start a chat and send `/newbot`
3. Follow the instructions to create your bot
4. Copy the bot token (looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### 2. Install Dependencies

```bash
# Clone or download this repository
cd ai_stand_wy25_bot

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your bot token
TELEGRAM_BOT_TOKEN=your_bot_token_here
```

### 4. Run the Bot

```bash
# Run from the project root directory
python run.py
```

Or use the startup script:

```bash
# On Windows:
start_bot.bat

# On macOS/Linux:
./start_bot.sh
```

> **Important:** Always run the bot from the **project root directory**, not from inside `src/`.

---

## 📱 Bot Commands

### Core Commands
| Command | Description |
|---------|-------------|
| `/start` | Start the bot and show welcome message |
| `/help` | Show all available commands |
| `/about` | About the bot |
| `/chat` | Enter interactive chat mode |
| `/clear` | Clear conversation history |
| `/session` | Show session information |
| `/stats` | Show your usage statistics |

### System Commands
| Command | Description |
|---------|-------------|
| `/commands` | List all available commands |
| `/tools` | List all available tools |
| `/search <query>` | Search commands and tools |
| `/manifest` | Show system manifest |

### Execution Commands
| Command | Description |
|---------|-------------|
| `/exec <command>` | Execute a specific command |
| `/tool <tool> [payload]` | Execute a specific tool |
| `/route <query>` | Route a query and show matches |

### Admin Commands
| Command | Description |
|---------|-------------|
| `/status` | Show bot system status |

---

## 🏗️ Architecture

This bot is built on the **Claude Code Python Port** architecture:

```
ai_stand_wy25_bot/
├── bot.py                 # Main bot entry point
├── requirements.txt       # Python dependencies
├── .env.example          # Environment template
├── README.md             # This file
├── src/                  # Core source code
│   ├── commands.py       # Command registry
│   ├── tools.py          # Tool registry
│   ├── query_engine.py   # Query processing
│   ├── runtime.py        # Execution runtime
│   ├── session_store.py  # Session management
│   └── reference_data/   # Command/tool snapshots
├── config/               # Configuration
│   └── bot_config.py     # Bot settings
├── data/                 # User data (created at runtime)
└── sessions/             # Session storage (created at runtime)
```

---

## 💡 Usage Examples

### Chat Mode
```
User: /chat
Bot: Chat Mode Activated! Session ID: abc123...

User: How do I search for files?
Bot: 🤖 Processing your request...
    🎯 Matched:
      ⚙️ SearchCommand (3)
      🔧 GrepTool (2)
      🔧 FindTool (2)
    
    ⚡ Response:
    You can use the SearchCommand or GrepTool to search for files...
```

### Execute Commands
```
User: /exec GitStatusTool
Bot: ✨ Command Executed
    Command: GitStatusTool
    Result: Git status would be displayed here...
```

### Search
```
User: /search git
Bot: 🎯 Search Results for "git"
    ⚙️ Commands (10):
      • GitStatusCommand
      • GitCommitCommand
      • GitPushCommand
      ...
    
    🔧 Tools (15):
      • GitTool
      • GitStatusTool
      • GitLogTool
      ...
```

---

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `TELEGRAM_BOT_TOKEN` | Your bot token from @BotFather | Required |
| `ADMIN_USER_IDS` | Comma-separated admin Telegram IDs | None |
| `LOG_LEVEL` | Logging level (DEBUG/INFO/WARNING/ERROR) | INFO |
| `DATA_DIR` | Directory for user data | ./data |
| `SESSION_DIR` | Directory for sessions | ./sessions |

### Bot Settings

Edit `config/bot_config.py` to customize:

- Bot name and version
- Message limits
- Feature toggles
- Query engine settings

---

## 🛠️ Development

### Adding New Commands

1. Add command definition to `src/reference_data/commands_snapshot.json`
2. Implement handler in `bot.py`
3. Register in `main()` function

### Adding New Tools

1. Add tool definition to `src/reference_data/tools_snapshot.json`
2. Implement tool logic in appropriate module

---

## 📝 License

This project is based on the Claude Code Python Port.

---

## 🙏 Credits

- **Created by:** Kimi K2.5
- **Architecture:** Claude Code Python Port
- **Framework:** python-telegram-bot

---

<p align="center">
  <i>Made with 💜 and lots of ☕</i>
</p>

<p align="center">
  <b>AI STAND WY2.5</b> - "The future of AI assistance is here"
</p>
