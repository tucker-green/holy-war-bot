# Bot Dashboard

The Holy War Bot now includes a native desktop UI dashboard that displays real-time statistics and progress!

## Features

- **Real-time Stats Display**: Shows gold, level, and character attributes (Strength, Attack, Defence, Agility, Stamina)
- **Live Status Updates**: See current bot action and status
- **Plunder Progress Bar**: Visual progress bar showing plunder completion percentage
- **Always-on-Top Window**: Dashboard stays visible while you work
- **Non-Blocking**: Runs in a separate thread, doesn't slow down the bot
- **Auto-Updates**: Updates automatically as the bot runs

## What It Looks Like

```
┌─────────────────────────────────────┐
│     ⚔️ HOLY WAR BOT ⚔️             │
├─────────────────────────────────────┤
│ Status                              │
│ Status: Online                      │
│ Action: Plundering (10 min)        │
├─────────────────────────────────────┤
│ Character Info                      │
│ 💰 Gold: 1319                       │
│ ⭐ Level: 1                         │
├─────────────────────────────────────┤
│ Stats                               │
│ Strength:   5                       │
│ Attack:     4                       │
│ Defence:    4                       │
│ Agility:    4                       │
│ Stamina:    4                       │
├─────────────────────────────────────┤
│ Plunder                             │
│ Time Remaining: 80 min              │
│ [████████░░░░░░░░░░] 40%           │
├─────────────────────────────────────┤
│ Last update: 19:45:32               │
└─────────────────────────────────────┘
```

## How It Works

1. When you start the bot with `python3 holy_war_bot.py`, the dashboard window pops up automatically
2. The dashboard appears at the top-left of your screen (400x600px)
3. The Firefox browser window opens alongside it
4. All stats update in real-time as the bot runs

## Position Setup

- **Dashboard**: Top-left corner (0, 0)
- **Browser**: You can manually position it to the right of the dashboard
- Both windows stay open while the bot runs

## Technical Details

- Built with **tkinter** (built into Python, no extra install needed)
- Runs in a **separate thread** (non-blocking)
- Updates via **thread-safe callbacks**
- **Always-on-top** attribute keeps it visible

Enjoy watching your bot work! 🎮

