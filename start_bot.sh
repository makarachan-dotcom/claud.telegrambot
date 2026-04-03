#!/bin/bash

# AI STAND WY2.5 - Startup Script for Linux/macOS
# Created by Kimi K2.5

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║  🤖 AI STAND WY2.5 - Telegram Bot                           ║"
echo "║                                                              ║"
echo "║  Starting up...                                              ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "📦 Activating virtual environment..."
    source venv/bin/activate
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "   Please copy .env.example to .env and configure your bot token."
    echo ""
    echo "   cp .env.example .env"
    echo "   nano .env  # Edit and add your token"
    echo ""
    exit 1
fi

# Check if TELEGRAM_BOT_TOKEN is set
if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
    export $(grep -v '^#' .env | xargs)
fi

if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
    echo "❌ Error: TELEGRAM_BOT_TOKEN not set!"
    echo "   Please add your bot token to the .env file."
    exit 1
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p data sessions

# Run the bot
echo ""
echo "🚀 Starting bot..."
echo "   Press Ctrl+C to stop"
echo ""

python bot.py
