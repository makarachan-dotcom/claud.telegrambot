# 🚀 AI STAND WY2.5 - Quick Start Guide

## 5-Minute Setup

### Step 1: Get Bot Token (1 minute)
1. Open Telegram
2. Search for [@BotFather](https://t.me/BotFather)
3. Send `/newbot`
4. Follow instructions
5. **Copy the token** (looks like `123456789:ABCdef...`)

### Step 2: Install (2 minutes)

```bash
# Navigate to bot folder
cd ai_stand_wy25_bot

# Run setup
python setup.py
```

### Step 3: Configure (1 minute)

```bash
# Edit .env file
nano .env  # or use any text editor
```

Add your token:
```
TELEGRAM_BOT_TOKEN=123456789:YourActualTokenHere
```

### Step 4: Run (1 minute)

```bash
# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Run bot
python bot.py
```

🎉 **Done!** Your bot is now running!

---

## First Commands to Try

Send these to your bot on Telegram:

| Command | What it does |
|---------|--------------|
| `/start` | Welcome message |
| `/help` | Show all commands |
| `/chat` | Enter chat mode |
| `/commands` | List 400+ commands |
| `/tools` | List 300+ tools |
| `/search git` | Search for git-related commands |
| `/status` | Show bot status |
| `/about` | About the bot |

---

## Chat Mode Example

```
You: /chat
Bot: Chat Mode Activated! Session ID: abc123...

You: How do I search for files?
Bot: 🤖 Processing your request...
    🎯 Matched:
      ⚙️ SearchCommand (3)
      🔧 GrepTool (2)
    
    ⚡ Response:
    You can use the SearchCommand or GrepTool...

You: /exit
Bot: Chat Mode Exited. Thanks for chatting!
```

---

## Troubleshooting

### "TELEGRAM_BOT_TOKEN not found"
- Make sure you created `.env` file
- Make sure token is in the file: `TELEGRAM_BOT_TOKEN=your_token`

### "Module not found"
- Make sure virtual environment is activated
- Run: `pip install -r requirements.txt`

### "Permission denied"
- Make scripts executable: `chmod +x start_bot.sh`

---

## Need Help?

- Check `README.md` for full documentation
- Look at `.env.example` for all options
- Review `bot.py` for code details

---

**Enjoy your AI STAND WY2.5 bot!** 🤖✨
