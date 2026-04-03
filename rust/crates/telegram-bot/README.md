# AI MAKARAAIIII — Telegram Bot

**Bot Identity:** AI STAND WY2.5  
**Languages:** 🇰🇭 Khmer (primary) · 🇬🇧 English (secondary)

## Features

- 🇰🇭 Khmer greeting on `/start`
- 🔘 Interactive inline keyboard:
  - **Button 1** — `🚫 មិនរញេរញៃ` — deletes the last bot message (no spam/redundancy)
  - `🤖 អំពី AI` — about the bot
  - `❓ ជំនួយ / Help` — help information
  - `🌐 ភាសា / Language` — language info
- ⚡ Real-time AI responses identifying as **AI STAND WY2.5**
- 💬 Supports both Khmer and English conversations
- 🦀 Written in Rust using [teloxide](https://github.com/teloxide/teloxide)

## Usage

```bash
# Build
cargo build -p telegram-bot --release

# Run (uses default token or TELEGRAM_BOT_TOKEN env var)
RUST_LOG=info cargo run -p telegram-bot

# Or with a custom token
TELEGRAM_BOT_TOKEN=your_token_here RUST_LOG=info cargo run -p telegram-bot
```

## Commands

| Command  | Description            |
|----------|------------------------|
| `/start` | Start the bot          |
| `/help`  | Show help information  |
| `/about` | About the bot          |

Any other text triggers an AI-style response from **AI STAND WY2.5**.

## Configuration

Copy `.env.example` to `.env` and set your token:

```
TELEGRAM_BOT_TOKEN=your_bot_token_here
RUST_LOG=info
```
