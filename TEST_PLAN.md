# Bot Test Plan & Verification

## ✅ Code Structure Verification

### 1. Login Function ✓
- **Location**: `async def login()`
- **Selectors**: 
  - Username: `input[type="text"]` (first)
  - Password: `input[type="password"]` (first)
  - Login button: `button:has(img[alt="Login"])`
- **Status**: ✓ Ready

### 2. Gold Detection ✓
- **Location**: `async def get_current_gold()`
- **Method**: Regex pattern `Chri\s*tian\s+(\d+)`
- **Status**: ✓ Tested and working

### 3. Training Cost Detection ✓
- **Location**: `async def get_training_cost()`
- **Method**: Tries regex, defaults to 1 gold
- **Status**: ✓ Will refine based on actual costs

### 4. Training Function ✓
- **Location**: `async def train_attributes()`
- **Safety Check**: Checks `(gold - cost) > reserve` BEFORE clicking
- **Status**: ✓ Logic correct

### 5. Plunder Time Detection ✓
- **Location**: `async def get_plunder_time_remaining()`
- **Method**: Regex `Plunder / protect time remaining today: (\d+) min`
- **Status**: ✓ Ready

### 6. Plunder Function ✓
- **Location**: `async def do_plunder()`
- **Selectors**: Radio button for duration, submit button
- **Status**: ✓ Ready (needs testing with actual plunder)

### 7. Sell Elixir Function ✓
- **Location**: `async def sell_cheapest_elixir()`
- **Method**: Finds sell buttons, clicks first (cheapest)
- **Status**: ✓ Ready (needs testing with actual elixirs)

### 8. Attack Player Function ✓
- **Location**: `async def attack_player()`
- **Selectors**: Level input, search button, attack button
- **Status**: ✓ Ready

## 🔄 Flow Logic Verification

### Main Loop Flow ✓
```
START
  ↓
Login ✓
  ↓
┌─────────────────────────────────────┐
│ Can train with > 10 gold reserve?  │ ✓
└─────────────────────────────────────┘
  │                    │
 YES                   NO
  │                    │
 Train                Skip
  │                    │
  └──────────┬──────────┘
             ↓
┌─────────────────────────────────────┐
│ Go to attack page                   │ ✓
│ Check plunder time                  │ ✓
└─────────────────────────────────────┘
  │                    │
 YES                   NO
  │                    │
  ↓                    ↓
┌──────────────────┐  ┌──────────────────┐
│ Gold >= 10?      │  │ Check training   │ ✓
└──────────────────┘  │ Attack player    │ ✓
  │                    │ Wait 5 min      │ ✓
 YES         NO        │ Loop back       │ ✓
  │         │          └──────────────────┘
  │         ↓
  │    Sell elixir ✓
  │         │
  └─────┬───┘
        ↓
    Plunder ✓
        │
        ↓
    Loop to training check ✓
```

## ⚠️ Potential Issues & Solutions

### Issue 1: Training Cost Detection
**Problem**: Cost might vary by level/stat
**Solution**: Function updates cost estimate based on actual cost after each training
**Status**: ✓ Handled

### Issue 2: Elixir Selling
**Problem**: Need to verify sell button selectors
**Solution**: Uses flexible selectors, will refine based on testing
**Status**: ⚠️ Needs live testing

### Issue 3: Plunder Submission
**Problem**: Radio button and submit button selectors
**Solution**: Uses flexible selectors, will refine based on testing
**Status**: ⚠️ Needs live testing

### Issue 4: Player Attack Search
**Problem**: Search form selectors might vary
**Solution**: Uses flexible selectors, will refine based on testing
**Status**: ⚠️ Needs live testing

## 🧪 Testing Checklist

### Phase 1: Basic Functions (Can test now)
- [x] Login ✓
- [x] Gold detection ✓
- [x] Page navigation ✓
- [x] Training cost logic ✓
- [x] Flow logic structure ✓

### Phase 2: Game Actions (Needs live testing)
- [ ] Training click (will spend gold)
- [ ] Plunder submission (takes 10 minutes)
- [ ] Elixir selling (requires elixirs)
- [ ] Elixir buying (requires > 100 gold)
- [ ] Player attack (requires targets)

### Phase 3: Full Cycle (Needs extended testing)
- [ ] Complete training → plunder cycle
- [ ] Complete plunder → training → plunder loop
- [ ] Complete attack → wait → check plunder loop
- [ ] Elixir sell → plunder flow
- [ ] Long-term stability (hours/days)

## 🎯 Key Safety Features

1. ✓ **Gold Reserve Protection**: Never trains if would leave ≤ 10 gold
2. ✓ **Training Cost Check**: Checks BEFORE clicking, not after
3. ✓ **Plunder Gold Check**: Ensures ≥ 10 gold before plundering
4. ✓ **Elixir Sell Fallback**: Sells elixir if gold < 10 for plundering
5. ✓ **Loop Safety**: Proper continue statements prevent infinite loops
6. ✓ **Error Handling**: Try/except blocks around critical operations

## 📝 Recommendations

1. **First Run**: Monitor closely for first 2-3 cycles
2. **Watch Logs**: Check for any selector failures
3. **Verify Gold**: Confirm gold detection is accurate
4. **Check Training**: Ensure training costs are detected correctly
5. **Test Elixirs**: Verify sell/buy functions work when conditions are met

## 🚀 Ready to Test

The bot is **structurally complete** and follows the flowchart exactly. All logic is in place. The only remaining items are:
- Live testing of game actions (plunder, training, elixirs, attacks)
- Refining selectors based on actual page structure
- Adjusting timing if needed

**Status**: ✅ Ready for live testing!

