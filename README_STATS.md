# Statistics Tracking System

The bot now includes comprehensive statistics tracking that monitors all your activities, gold management, and progress!

## 📊 What's Tracked

### 💰 Gold Management
- **Total Gold Earned**: From plundering
- **Total Gold Spent**: On stats + elixirs
- **Net Gold**: Earned minus spent
- **Spent on Stats**: Gold used for training
- **Spent on Elixirs**: Gold used for elixirs

### ⬆️ Stat Upgrades
- **Each Stat Count**: How many times you've upgraded:
  - Strength
  - Attack
  - Defence
  - Agility
  - Stamina
- **Total Trainings**: Total number of stat upgrades
- **Training Sessions**: How many training sessions

### 🧪 Elixir Purchases
- **Consecrated Elixir** (50g): Count and total cost
- **Baptised Elixir** (90g): Count and total cost
- **Blessed Elixir** (450g): Count and total cost

### ⚔️ Combat (Coming Soon)
- **Victories**: Wins in combat
- **Defeats**: Losses in combat
- **Win Rate**: Victory percentage

### 📈 Activity
- **Plunders**: Number of plunder sessions
- **Plunder Hours**: Total time spent plundering
- **Attacks**: Number of attacks
- **Training Sessions**: Number of training sessions

## 💾 Data Persistence

All statistics are saved to `bot_stats.json` and persist across bot restarts. Your stats accumulate over time!

## 📺 Dashboard Display

The statistics are shown in a **scrollable section** at the bottom of the dashboard:

```
┌──────────────────────────────────────────┐
│ Session Statistics                       │
├──────────────────────────────────────────┤
│ 💰 Gold                                  │
│   Earned: 1,250g                         │
│   Spent: 800g                            │
│   Net: 450g                              │
│   On Stats: 650g                         │
│   On Elixirs: 150g                       │
├──────────────────────────────────────────┤
│ ⬆️ Stat Upgrades                         │
│   Strength: 15x                          │
│   Attack: 20x                            │
│   Defence: 18x                           │
│   Agility: 22x                           │
│   Stamina: 19x                           │
│   Total: 94 trainings                    │
├──────────────────────────────────────────┤
│ 🧪 Elixirs                               │
│   Consecrated (50g): 2x = 100g          │
│   Baptised (90g): 1x = 90g              │
│   Blessed (450g): 0x = 0g               │
├──────────────────────────────────────────┤
│ ⚔️ Combat                                │
│   Victories: 0                           │
│   Defeats: 0                             │
│   Win Rate: 0.0%                         │
├──────────────────────────────────────────┤
│ 📊 Activity                              │
│   Plunders: 8                            │
│   Plunder Time: 1.3h                     │
│   Attacks: 3                             │
│   Training Sessions: 12                  │
└──────────────────────────────────────────┘
```

## 🔄 Real-Time Updates

Statistics update automatically when:
- ✅ You train a stat (tracks which stat and cost)
- ✅ You buy an elixir (tracks which elixir and cost)
- ✅ Plunder completes (tracks gold earned)
- ✅ You attack a player
- ✅ Combat results occur

## 📁 Files

- **`bot_stats.py`**: Statistics tracking module
- **`bot_stats.json`**: Persistent data storage (auto-created)

## 🎯 Use Cases

### Track ROI
See exactly how much gold you're earning vs spending!

### Optimize Strategy
- Which stats do you upgrade most?
- Are you spending too much on elixirs?
- How efficient is your plundering?

### Monitor Progress
Watch your stats grow over time and see your bot's accomplishments!

## 🔮 Future Enhancements

- Combat victory/defeat tracking (when combat detection is added)
- Hourly/daily breakdowns
- Export stats to CSV
- Graphs and charts
- Leaderboard comparison

Enjoy tracking your progress! 📈

