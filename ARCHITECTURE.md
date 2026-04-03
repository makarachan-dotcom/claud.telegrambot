# 🏗️ AI STAND WY2.5 - Architecture Documentation

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        TELEGRAM USER                            │
└─────────────────────────────────┬───────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                    TELEGRAM BOT API                             │
│              (python-telegram-bot library)                      │
└─────────────────────────────────┬───────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                      BOT.PY (Main Entry)                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │  Command    │  │  Message    │  │    Callback Handlers    │  │
│  │  Handlers   │  │  Handlers   │  │                         │  │
│  └──────┬──────┘  └──────┬──────┘  └────────────┬────────────┘  │
│         └─────────────────┴──────────────────────┘               │
│                              │                                   │
│                              ▼                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              UserSessionManager (Sessions)               │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────┬───────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                    PORTED CORE MODULES                          │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │  commands   │  │    tools    │  │     query_engine        │  │
│  │  (400+)     │  │   (300+)    │  │   (QueryEnginePort)     │  │
│  └──────┬──────┘  └──────┬──────┘  └────────────┬────────────┘  │
│         └─────────────────┴──────────────────────┘               │
│                              │                                   │
│                              ▼                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              runtime (PortRuntime)                       │   │
│  │         - Route prompts to commands/tools                │   │
│  │         - Execute operations                             │   │
│  │         - Manage sessions                                │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

## Module Breakdown

### 1. Bot Layer (`bot.py`)
- **Purpose**: Telegram interface
- **Key Components**:
  - Command handlers (`/start`, `/help`, `/chat`, etc.)
  - Message handlers (chat mode)
  - Callback query handlers (buttons)
  - User session management

### 2. Session Management (`UserSessionManager`)
- **Purpose**: Track user sessions and conversation history
- **Features**:
  - Per-user query engines
  - Conversation history
  - Usage statistics
  - Session persistence

### 3. Core Modules (from `src/`)

#### `commands.py`
- **400+ mirrored commands**
- Command discovery and execution
- Source: `reference_data/commands_snapshot.json`

#### `tools.py`
- **300+ integrated tools**
- Tool discovery and execution
- Permission context support
- Source: `reference_data/tools_snapshot.json`

#### `query_engine.py`
- **QueryEnginePort**: Main processing engine
- **TurnResult**: Conversation turn results
- **QueryEngineConfig**: Configuration
- Features:
  - Message submission
  - Streaming responses
  - Token tracking
  - Session persistence

#### `runtime.py`
- **PortRuntime**: Execution runtime
- Features:
  - Prompt routing
  - Command/tool matching
  - Session bootstrapping
  - Turn loops

#### `execution_registry.py`
- **ExecutionRegistry**: Command/tool registry
- MirroredCommand and MirroredTool wrappers

#### `session_store.py`
- Session persistence to disk
- JSON-based storage

### 4. Data Layer

#### `reference_data/`
- `commands_snapshot.json`: 400+ command definitions
- `tools_snapshot.json`: 300+ tool definitions

#### `data/` (runtime)
- User session data
- Statistics
- Preferences

#### `sessions/` (runtime)
- Persisted conversation sessions

## Data Flow

```
User Message
    │
    ▼
[Telegram API]
    │
    ▼
[Command Handler]
    │
    ├──► /start, /help → Direct response
    │
    ├──► /chat → Enter chat mode
    │              │
    │              ▼
    │         [Message Handler]
    │              │
    │              ▼
    │         [PortRuntime.route_prompt()]
    │              │
    │              ▼
    │         [QueryEnginePort.submit_message()]
    │              │
    │              ▼
    │         [Response to User]
    │
    ├──► /exec → [execute_command()]
    │
    ├──► /tool → [execute_tool()]
    │
    └──► /search → [find_commands()/find_tools()]
```

## Key Features

### 1. Smart Routing
```python
runtime = PortRuntime()
matches = runtime.route_prompt("How do I search files?", limit=5)
# Returns: [RoutedMatch(kind='command', name='SearchCommand', score=3), ...]
```

### 2. Session Management
```python
session = session_manager.get_session(user_id)
engine = session_manager.get_engine(user_id)
result = engine.submit_message(prompt, matched_commands, matched_tools)
```

### 3. Command Execution
```python
result = execute_command("GitStatusCommand", "")
# Returns: CommandExecution with handled status and message
```

### 4. Tool Execution
```python
result = execute_tool("FileReadTool", '{"path": "/file.txt"}')
# Returns: ToolExecution with handled status and message
```

## Configuration

### Environment Variables
- `TELEGRAM_BOT_TOKEN`: Required bot token
- `ADMIN_USER_IDS`: Comma-separated admin IDs
- `LOG_LEVEL`: Logging verbosity
- `DATA_DIR`: Data storage path
- `SESSION_DIR`: Session storage path

### Bot Settings (`config/bot_config.py`)
- Bot metadata (name, version)
- Message limits
- Feature toggles
- Query engine settings

## Security Considerations

1. **Token Security**: Store `TELEGRAM_BOT_TOKEN` in `.env`, never commit it
2. **Admin Controls**: Restrict sensitive commands to admin IDs
3. **Permission Context**: Tool execution respects permission settings
4. **Input Validation**: All user inputs are validated before processing

## Extending the Bot

### Adding a New Command

1. Add to `reference_data/commands_snapshot.json`:
```json
{
  "name": "MyNewCommand",
  "responsibility": "Does something cool",
  "source_hint": "custom/my_command.ts"
}
```

2. Add handler in `bot.py`:
```python
async def mynew_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Implementation
    pass

# Register
application.add_handler(CommandHandler("mynew", mynew_command))
```

### Adding a New Tool

1. Add to `reference_data/tools_snapshot.json`:
```json
{
  "name": "MyNewTool",
  "responsibility": "Performs an action",
  "source_hint": "tools/my_tool.ts"
}
```

2. Implement tool logic (if needed)

---

**Architecture by Kimi K2.5** | Based on Claude Code Python Port
