# Holy War Game Bot

An automated bot for the Holy War browser game that handles plundering, training, elixir buying, and player attacks.

## Features

- **Automatic Login**: Logs in with your credentials
- **Plundering**: Automatically plunders every 10 minutes when plunder time is available
- **Training**: Spends gold on training attributes while keeping a minimum reserve
- **Elixir Banking**: Buys elixirs when gold exceeds 100 (and training is maxed out) to store value
- **Player Attacks**: Attacks other players when plunder time runs out (5-minute cooldown)
- **Smart Gold Management**: Keeps at least 10 gold at all times

## Installation

1. **Install Python** (3.8 or higher recommended)

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Install Playwright browsers**:
```bash
playwright install chromium
```

## Configuration

Edit the `config.py` file to configure your settings:

```python
# Login credentials
USERNAME = "your_username"  # Your game username
PASSWORD = "your_password"  # Your game password
WORLD = "17IN"              # Your world (e.g., "17IN" for International World 17)

# Gold management
MIN_GOLD_RESERVE = 10       # Minimum gold to keep at all times
ELIXIR_THRESHOLD = 100      # Buy elixirs when gold exceeds this (and can't train)

# Plunder settings
PLUNDER_DURATION_MINUTES = 10  # Duration of each plunder (10, 20, 30, 40, 50, or 60)

# Attack settings
TARGET_PLAYER_LEVEL = 1     # Level of players to attack
ATTACK_COOLDOWN_MINUTES = 5 # Wait time between attacks

# Browser settings
HEADLESS = False            # Set to True to run browser in background
```

## Usage

**Quick Start (Windows):**
```bash
run_bot.bat
```

**Quick Start (Linux/Mac):**
```bash
chmod +x run_bot.sh
./run_bot.sh
```

**Or run directly:**
```bash
python holy_war_bot.py
```

The bot will:
1. Login to your account
2. Start plundering (10-minute cycles)
3. After each plunder, train your attributes with available gold (SAFELY - see below)
4. If gold > 100 and training is maxed, buy elixirs
5. When plunder time runs out (after using all 120 minutes), switch to attacking other players
6. Continue the cycle indefinitely

### ⚠️ Important: Training Safety Logic

**The bot will NOT train if training would leave you with ≤ 10 gold (or your configured MIN_GOLD_RESERVE).**

Before clicking any "Train" button, the bot:
1. Checks the training cost
2. Calculates: `current_gold - training_cost`
3. Only trains if the result is > MIN_GOLD_RESERVE

This ensures you always keep your minimum gold reserve.

**What happens if you can't train?**
- If you have > 100 gold AND all stats are maxed → Buy elixirs (acts as a bank)
- If you have < 100 gold → Continue plundering or attacking to earn more gold

## How It Works

### Plunder Phase
- Bot checks if you have at least 10 minutes of plunder time
- Starts a 10-minute plunder
- Waits for plunder to complete
- Goes to status page and trains attributes
- If gold > 100 after training and can't train anymore, buys elixirs
- Repeats until plunder time is exhausted

### Attack Phase
- When plunder time is depleted, bot switches to player attacks
- Searches for players of your configured level
- Attacks them with a 5-minute cooldown between attacks
- Checks periodically if plunder time has refreshed (new day)

## Stopping the Bot

Press `Ctrl+C` to stop the bot gracefully.

## Notes

- The bot runs in non-headless mode by default (you can see the browser window)
- All actions are logged with timestamps
- Make sure you have a stable internet connection
- The bot respects game timers and cooldowns

## Workflow Summary

```
Login → Check Plunder Time Available?
  ├─ YES → Plunder (10 min)
  │         ↓
  │       Wait 10 minutes
  │         ↓
  │       Train Attributes (spend gold, keep > 10)
  │         ↓
  │       Gold > 100 & Can't Train? → Buy Elixirs
  │         ↓
  │       Repeat
  │
  └─ NO → Attack Players (level configurable)
            ↓
          Wait 5 minutes
            ↓
          Check if Plunder Time Refreshed?
            ↓
          Repeat
```

## Troubleshooting

- **Bot can't login**: Check your credentials in the script
- **Bot can't find elements**: The game might have updated its UI, you may need to update the selectors
- **Bot stops unexpectedly**: Check the logs for error messages
- **Playwright errors**: Make sure you ran `playwright install chromium`

