# Bot Flow Logic - Exact Flowchart Implementation

## Complete Flow Diagram

```
START
  ↓
Login
  ↓
┌─────────────────────────────────────────────────────────┐
│ Do I have enough gold to train a stat                   │
│ AND have > 10 gold left over?                           │
└─────────────────────────────────────────────────────────┘
  │                    │
 YES                   NO
  │                    │
  ↓                    ↓
Train stat and repeat  ────┐
until you don't have       │
enough to train and        │
have > 10 gold left        │
  │                        │
  ↓                        │
┌─────────────────────────────────────────────────────────┐
│ Go to attack page.                                       │
│ Do I have plunder time?                                  │
└─────────────────────────────────────────────────────────┘
  │                    │
 YES                   NO
  │                    │
  ↓                    ↓
┌──────────────────┐  ┌──────────────────────────────────┐
│ Do I have        │  │ Go to status page and see if      │
│ 10 or more gold? │  │ I have enough gold to train       │
└──────────────────┘  └──────────────────────────────────┘
  │                    │
 YES        NO         │
  │         │          │
  ↓         ↓          │
Plunder    Go to city  │
for 10     → Elixir    │
minutes    shop →      │
  │         Sell       │
  │         cheapest   │
  │         elixir     │
  │         │          │
  │         └──────────┘
  │                    │
  └────────────────────┘
         │
         ↓
    Attack a player
         │
         ↓
    Wait 5 minutes
         │
         ↓
    Loop back to
    "Do I have
    plunder time?"
```

## Step-by-Step Logic

### Step 1: Training Check (First Priority)
- **Question**: "Do I have enough gold to train a stat AND have > 10 gold left over?"
- **If YES**: 
  - Train stats repeatedly
  - Continue until: `current_gold - training_cost <= 10`
- **If NO**: Skip to Step 2

### Step 2: Plunder Time Check
- Navigate to attack page
- **Question**: "Do I have plunder time?"
- **If YES** → Go to Step 3
- **If NO** → Go to Step 4

### Step 3: Gold Check for Plundering
- **Question**: "Do I have 10 or more gold?"
- **If YES**: 
  - Plunder for 10 minutes
  - After plunder completes → Loop back to Step 1 (Training Check)
- **If NO**: 
  - Go to city → Elixir shop → Sell cheapest elixir
  - After selling → Try to plunder
  - After plunder completes → Loop back to Step 1 (Training Check)

### Step 4: No Plunder Time Available
- Go to status page
- Check if we can train (optional training while waiting)
- Attack a player
- Wait 5 minutes (cooldown)
- Loop back to Step 2 (Plunder Time Check)

## Key Rules

1. **Training Priority**: Always check training FIRST before plundering
2. **Gold Reserve**: Never train if it would leave ≤ 10 gold
3. **Sell Elixirs**: Only sell when gold < 10 AND want to plunder
4. **Buy Elixirs**: Only buy when gold > 100 AND can't train anymore (not in main flow, but still available)
5. **Plunder Loop**: After plundering, always loop back to training check
6. **Attack Loop**: When no plunder time, attack → wait → check plunder time again

## Differences from Previous Version

- ✅ Training happens FIRST, before checking plunder time
- ✅ After plundering, loops back to training (not directly to plunder again)
- ✅ Sells elixirs when gold < 10 (to get gold for plundering)
- ✅ Checks training even when no plunder time (while waiting)

