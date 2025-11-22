# Holy War Bot Dashboard

A real-time web dashboard to monitor your bot's activity!

## Features

- 📊 Real-time stats display (Gold, Level, Plunder Time)
- ⚔️ Character attributes (STR, ATT, DEF, AGI, STA)
- 📈 Live plunder progress bar
- 📜 Activity log with recent actions
- 🎨 Beautiful modern UI with gradient background
- 🔄 Auto-updates every 2 seconds

## Setup

1. Install dependencies:
```bash
pip3 install -r requirements.txt
```

2. Start the dashboard in a separate terminal:
```bash
python3 dashboard.py
```

3. Open your browser to:
```
http://localhost:5000
```

4. Run the bot normally:
```bash
python3 holy_war_bot.py
```

## Usage

### Two Window Setup

**Window 1 (Left):** Playwright Browser (from bot)
- Shows the actual game interface
- Bot performs actions here

**Window 2 (Right):** Dashboard Browser
- Open `http://localhost:5000`
- Shows live stats and progress
- Updates automatically

### Single Monitor Setup

1. Run dashboard first: `python3 dashboard.py`
2. Open dashboard in browser
3. Resize browser to take up right half of screen
4. Run bot: `python3 holy_war_bot.py`
5. Bot browser will appear on left side

## Dashboard Displays

### Resources
- Current gold amount
- Character level
- Available plunder time

### Character Stats
- Strength
- Attack
- Defence
- Agility
- Stamina

### Plunder Progress
- Visual progress bar (0-100%)
- Current status (Idle/Plundering/Training/etc)
- Time remaining

### Activity Log
- Recent bot actions
- Timestamped entries
- Auto-scrolls to show latest

## Customization

Edit `templates/dashboard.html` to customize:
- Colors and styling
- Layout and spacing
- Displayed information
- Update frequency (default 2s)

## Troubleshooting

**Dashboard won't connect:**
- Make sure dashboard.py is running
- Check that port 5000 is not in use
- Try `http://127.0.0.1:5000` instead of localhost

**Stats not updating:**
- Bot must be running for stats to update
- Check bot_state.json file is being created
- Refresh the dashboard page

**Port already in use:**
- Edit dashboard.py and change port from 5000 to another number
- Update browser URL accordingly

