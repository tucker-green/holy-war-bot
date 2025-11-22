#!/bin/bash
# Quick deployment script for cloud servers

set -e  # Exit on error

echo "================================"
echo "Holy War Bot - Deployment Script"
echo "================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
    echo -e "${RED}Please do not run as root. Run as regular user (ubuntu).${NC}"
    exit 1
fi

echo -e "${BLUE}Step 1: Updating system...${NC}"
sudo apt update && sudo apt upgrade -y

echo -e "${BLUE}Step 2: Installing dependencies...${NC}"
sudo apt install -y python3 python3-pip git firefox screen

echo -e "${BLUE}Step 3: Installing Python packages...${NC}"
pip3 install -r requirements.txt

echo -e "${BLUE}Step 4: Installing Playwright browsers...${NC}"
playwright install firefox
playwright install-deps firefox

echo -e "${BLUE}Step 5: Checking config file...${NC}"
if [ ! -f "config.py" ]; then
    echo -e "${RED}Config file not found!${NC}"
    echo "Creating config.py from example..."
    cp config.example.py config.py
    echo -e "${RED}IMPORTANT: Edit config.py with your credentials!${NC}"
    echo "Run: nano config.py"
    echo "Make sure to set HEADLESS = True"
    exit 1
fi

# Check if HEADLESS is set to True
if grep -q "HEADLESS = False" config.py; then
    echo -e "${RED}WARNING: HEADLESS is set to False in config.py${NC}"
    echo "For cloud deployment, you should set HEADLESS = True"
    echo "Would you like to automatically update it? (y/n)"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        sed -i 's/HEADLESS = False/HEADLESS = True/g' config.py
        echo -e "${GREEN}Updated HEADLESS to True${NC}"
    fi
fi

echo ""
echo -e "${GREEN}Deployment complete!${NC}"
echo ""
echo "Choose how to run the bot:"
echo ""
echo "Option 1: Run with screen (manual control)"
echo "  screen -S holywar"
echo "  python3 holy_war_bot.py"
echo "  # Press Ctrl+A then D to detach"
echo "  # Reattach with: screen -r holywar"
echo ""
echo "Option 2: Run as systemd service (automatic restart)"
echo "  sudo cp holywar-bot.service /etc/systemd/system/"
echo "  sudo systemctl enable holywar-bot"
echo "  sudo systemctl start holywar-bot"
echo "  sudo systemctl status holywar-bot"
echo "  # View logs: sudo journalctl -u holywar-bot -f"
echo ""
echo -e "${BLUE}Recommendation: Use Option 2 for fully automated 24/7 operation${NC}"

