# Quick Setup Guide for Holy War Bot

## Step 1: Install Python
Download and install Python 3.8 or higher from https://www.python.org/downloads/

During installation, make sure to check "Add Python to PATH"

## Step 2: Install Dependencies

Open a terminal/command prompt in the project folder and run:

```bash
pip install -r requirements.txt
```

Then install Playwright browsers:

```bash
playwright install chromium
```

## Step 3: Configure the Bot

Edit `config.py` and set your credentials:

```python
USERNAME = "tvcker"      # Already set to your username
PASSWORD = "174210Tg"    # Already set to your password
WORLD = "17IN"           # Already set to your world
```

You can also adjust other settings like:
- `TARGET_PLAYER_LEVEL` - What level players to attack
- `MIN_GOLD_RESERVE` - How much gold to always keep
- `ELIXIR_THRESHOLD` - When to start buying elixirs

## Step 4: Run the Bot

**On Windows:**
Double-click `run_bot.bat`

**On Linux/Mac:**
```bash
chmod +x run_bot.sh
./run_bot.sh
```

**Or manually:**
```bash
python holy_war_bot.py
```

## What the Bot Does

1. **Logs in** to your Holy War account
2. **Plunders** for 10 minutes at a time
3. **Waits** for plunder to complete
4. **Trains** your attributes with available gold (keeping minimum reserve)
5. **Buys elixirs** if you have > 100 gold and can't train anymore
6. **Repeats** until all plunder time is used (120 min = 12 plunders per day)
7. **Attacks players** when plunder time runs out (5-minute cooldown)
8. **Checks** for new plunder time each day

## Important Notes

- The bot keeps at least 10 gold at all times
- Elixirs act as a "bank" - they're only bought when gold > 100 AND you can't train
- The bot runs continuously - leave it running and it will handle everything
- Press Ctrl+C to stop the bot

## Troubleshooting

**Problem:** Bot can't find Playwright
**Solution:** Run `pip install playwright` then `playwright install chromium`

**Problem:** Bot can't login
**Solution:** Check your username and password in `config.py`

**Problem:** Bot stops unexpectedly
**Solution:** Check the log output for error messages. The game might have updated.

**Problem:** Want to run without seeing the browser
**Solution:** Set `HEADLESS = True` in `config.py`

## Bot Workflow

```
START
  ↓
Login to Game
  ↓
Check Plunder Time > 10 min?
  ↓
YES → Start Plunder (10 min)
  ↓
Wait 10 minutes
  ↓
Go to Status Page
  ↓
Train Attributes (spend gold, keep > 10)
  ↓
Gold > 100 AND can't train anymore?
  ↓
YES → Buy Elixirs (to ~10 gold)
  ↓
Back to Check Plunder Time
  
NO (Plunder Time < 10 min) → Switch to Player Attacks
  ↓
Search for Player (configured level)
  ↓
Attack Player
  ↓
Wait 5 minutes
  ↓
Check if Plunder Time Refreshed?
  ↓
YES → Back to Plunder
NO → Continue Attacking
```

## Support

If you need help or the game has updated its UI:
1. Check the error logs
2. The bot might need updates to its selectors
3. You can pause/stop the bot anytime with Ctrl+C

