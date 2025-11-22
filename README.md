# Holy War Bot 🤖⚔️

An automated bot for Holy War game that handles training, plundering, attacking, and resource management.

## Features

- ✅ **Auto Training** - Trains stats intelligently (prioritizes Strength, then cheapest)
- ✅ **Auto Plundering** - Plunders for gold every 10 minutes
- ✅ **Auto Attacking** - Attacks weaker players when plunder time is unavailable
- ✅ **Smart Stats Comparison** - Only attacks opponents with lower total stats
- ✅ **Elixir Management** - Automatically buys elixirs to avoid losing gold
- ✅ **Gold Management** - Maintains minimum reserve for plundering
- ✅ **Auto Re-login** - Automatically logs back in if session expires
- ✅ **Progress Bars** - Visual feedback for waiting periods
- ✅ **Cooldown Detection** - Detects and waits for active plundering/cooldowns

## Quick Start (Local)

### 1. Install Dependencies

```bash
pip install -r requirements.txt
playwright install firefox
```

### 2. Configure

```bash
cp config.example.py config.py
nano config.py  # Edit with your credentials
```

### 3. Run

```bash
python3 holy_war_bot.py
```

## Cloud Deployment (24/7)

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed instructions on running the bot 24/7 in the cloud.

**Quick Cloud Setup:**

```bash
# On your cloud server
git clone https://github.com/tucker-green/holy-war-bot.git
cd holy-war-bot
./deploy.sh  # Automated setup script
```

### Recommended Cloud Providers

| Provider | Cost | Best For |
|----------|------|----------|
| **Oracle Cloud** | FREE | Best value (free forever) |
| **DigitalOcean** | $4/mo | Easiest setup |
| **AWS EC2** | Free 12mo | Most flexible |

## Configuration

Edit `config.py`:

```python
# Login credentials
USERNAME = "your_username"
PASSWORD = "your_password"
WORLD = "17IN"  # Your world

# Gold management
MIN_GOLD_RESERVE = 10       # Minimum gold to keep
ELIXIR_THRESHOLD = 100      # Buy elixirs when gold > this

# Plunder settings
PLUNDER_DURATION_MINUTES = 10  # 10, 20, 30, 40, 50, or 60

# Attack settings
TARGET_PLAYER_LEVEL = 3     # Level to attack
ATTACK_COOLDOWN_MINUTES = 5 # Wait between attacks

# Browser settings
HEADLESS = False  # Set True for cloud deployment
```

## Bot Logic Flow

```
1. Check if can train (and have > 10 gold left)
   └─ YES: Train stats (Strength priority, then cheapest)
   
2. Check plunder time remaining
   └─ >= 10 minutes?
      ├─ YES: Check gold
      │   ├─ >= 10 gold: Plunder → Wait 10 min → Collect gold
      │   └─ < 10 gold: Sell elixir → Plunder
      └─ NO: Attack player → Wait 5 min → Loop back to step 2
```

## Attack Strategy

1. Get your current stats from attributes page
2. Navigate to attack page and search for target level (exact or lower)
3. Parse opponent's stats
4. Compare total stats:
   - **Opponent weaker**: Attack!
   - **Opponent stronger**: Click "New Opponent" (try up to 10 times)
5. Verify attack success by checking for cooldown timer

## Monitoring

### If using `screen`:
```bash
screen -r holywar  # Reattach to see live output
```

### If using `systemd`:
```bash
sudo systemctl status holywar-bot  # Check status
sudo journalctl -u holywar-bot -f  # Follow logs
```

## Troubleshooting

### Bot stops working
```bash
# Check logs
sudo journalctl -u holywar-bot -n 100

# Restart
sudo systemctl restart holywar-bot
```

### Update bot
```bash
cd ~/holy-war-bot
git pull origin main
sudo systemctl restart holywar-bot
```

### Memory issues
```bash
# Add swap space (if < 1GB RAM)
sudo fallocate -l 1G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

## Files

- `holy_war_bot.py` - Main bot logic
- `config.py` - Your configuration (not in git)
- `config.example.py` - Example configuration
- `requirements.txt` - Python dependencies
- `deploy.sh` - Automated cloud deployment script
- `holywar-bot.service` - Systemd service file
- `DEPLOYMENT_GUIDE.md` - Detailed cloud deployment guide

## Security

- ⚠️ Never commit `config.py` (it contains your password)
- ⚠️ Use SSH keys for cloud servers
- ⚠️ Keep your server updated: `sudo apt update && sudo apt upgrade`

## License

MIT License - Use at your own risk. This bot is for educational purposes.

## Contributing

Pull requests welcome! Please test thoroughly before submitting.

---

Made with ❤️ by Tucker Green
