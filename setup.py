#!/usr/bin/env python3
"""
AI STAND WY2.5 - Setup Script
Created by Kimi K2.5
"""

import os
import subprocess
import sys
from pathlib import Path


def print_banner():
    """Print setup banner"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║  🤖 AI STAND WY2.5 - Setup Script                           ║
║                                                              ║
║  This script will help you set up the bot                   ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")


def check_python_version():
    """Check Python version"""
    print("🔍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print("❌ Python 3.9+ is required!")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True


def create_virtual_environment():
    """Create virtual environment"""
    print("\n📦 Creating virtual environment...")
    if Path("venv").exists():
        print("   Virtual environment already exists")
        return True
    
    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("✅ Virtual environment created")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create virtual environment: {e}")
        return False


def install_dependencies():
    """Install required packages"""
    print("\n📥 Installing dependencies...")
    
    # Determine pip path
    if Path("venv").exists():
        if sys.platform == "win32":
            pip_path = "venv\\Scripts\\pip.exe"
        else:
            pip_path = "venv/bin/pip"
    else:
        pip_path = "pip"
    
    try:
        subprocess.run([pip_path, "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependencies installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False


def setup_environment():
    """Setup environment file"""
    print("\n⚙️  Setting up environment...")
    
    if Path(".env").exists():
        print("   .env file already exists")
        return True
    
    if not Path(".env.example").exists():
        print("❌ .env.example not found!")
        return False
    
    # Copy example file
    with open(".env.example", "r") as f:
        content = f.read()
    
    with open(".env", "w") as f:
        f.write(content)
    
    print("✅ .env file created from .env.example")
    print("\n📝 IMPORTANT: Edit .env and add your bot token!")
    print("   Get your token from @BotFather on Telegram")
    return True


def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    
    dirs = ["data", "sessions", "logs"]
    for dir_name in dirs:
        Path(dir_name).mkdir(exist_ok=True)
        print(f"   ✅ {dir_name}/")
    
    return True


def print_next_steps():
    """Print next steps"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║  🎉 Setup Complete!                                          ║
║                                                              ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Next steps:                                                 ║
║                                                              ║
║  1. Edit .env and add your bot token:                        ║
║     TELEGRAM_BOT_TOKEN=your_token_here                      ║
║                                                              ║
║  2. Activate virtual environment:                            ║
║     Windows: venv\\Scripts\\activate                         ║
║     macOS/Linux: source venv/bin/activate                   ║
║                                                              ║
║  3. Run the bot from the project root:                       ║
║     python run.py                                            ║
║                                                              ║
║  Or use the startup script:                                  ║
║     Windows: start_bot.bat                                   ║
║     macOS/Linux: ./start_bot.sh                             ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")


def main():
    """Main setup function"""
    print_banner()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create virtual environment
    if not create_virtual_environment():
        print("\n⚠️  Continuing without virtual environment...")
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Setup environment
    if not setup_environment():
        sys.exit(1)
    
    # Create directories
    if not create_directories():
        sys.exit(1)
    
    print_next_steps()


if __name__ == "__main__":
    main()
