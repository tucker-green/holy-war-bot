# Bot Testing Notes - Complete Testing Session

## ✅ Login Test - SUCCESSFUL
**Status**: Fully working

### Working Selectors:
- **Username field**: `input[type="text"]` (first one)
- **Password field**: `input[type="password"]` (first one)
- **Login button**: Button element with Login image inside

### Login Flow:
1. Navigate to `/auth/loginform/`
2. Fill username in first text input
3. Fill password in password input
4. Click button containing Login image
5. Redirects to `/welcome?w=17IN` on success

---

## ✅ Attack/Plunder Page - ACCESSIBLE
**Status**: Page accessible, plunder selection needs testing

### URL: `/assault/1on1/?w=17IN`
### Key Information:
- Shows "Plunder / protect time remaining today: 120 min"
- Options for plunder duration: 10, 20, 30, 40, 50, 60 minutes
- Options for defend duration: 10, 20, 30, 40, 50, 60 minutes
- Contains radio buttons or form elements (need to test submission)

### Notes:
- Plunder buttons weren't directly testable in this session
- Bot will need to select radio button for "10" minutes
- Then submit the plunder form

---

## ✅ Training/Attributes Page - ACCESSIBLE
**Status**: Page accessible, button clicking needs refinement

### URL: `/char/attributes/?w=17IN`
### Structure:
- Multiple "Train" buttons (images) for each attribute:
  - Strength
  - Attack
  - Defence
  - Agility
  - Stamina

### Training Form Structure:
Each attribute has:
- A form containing:
  - Textbox with value "+1"
  - Train button (image)

### Current Gold Detection:
- Gold shows as "Chri tian 14 100 1" (14 gold, 100 life energy, level 1)
- Regex pattern works: `Chri\s*tian\s+(\d+)`

### Issues Found:
- Clicking the Train image didn't immediately update gold
- May need to click the form's submit action or wait for response
- Training likely costs 1+ gold per click

---

## ✅ City Overview - ACCESSIBLE
**Status**: Successfully navigated

### URL: `/town/overview/?w=17IN`
### Available Locations:
- Blacksmith
- **Elixirs Shop** ✅ (tested)
- Stables
- Mercenary Bulletin Board
- Arena
- Tavern
- Weapon Stall
- Shield Stall
- Armour Stall
- Elixirs Stall
- Horse Stall
- Work

---

## ✅ Elixirs Shop - ACCESSIBLE & TESTED
**Status**: Successfully navigated and examined

### URL: `/town/alchemist/?w=17IN`
### Available Elixirs & Prices:
1. **Consecrated Elixir**: 50 gold (Effect: +50 LP)
2. **Baptised Elixir**: 90 gold (Effect: +100 LP)
3. **Blessed Elixir**: 450 gold (Effect: +500 LP)
4. **Holy Beverage**: 900 gold (Effect: +1000 LP)
5. **Sanctified Spirit**: 2000+ gold (Effect: +2000 LP)

### Notes:
- With 14 gold currently, cannot buy any elixirs
- Minimum elixir costs 50 gold
- Bot logic should target buying elixirs when gold > 100
- Should buy most expensive affordable elixir repeatedly

---

## Current Status After Testing:
- **Gold**: 14
- **Life Energy**: 100
- **Level**: 1
- **Plunder Time Remaining**: 120 minutes (full)

---

## Recommendations for Bot Improvements:

### 1. Login (✅ WORKING)
- Current implementation should work fine
- Uses flexible selectors that matched testing

### 2. Gold Detection (✅ CONFIRMED)
- Regex pattern `Chri\s*tian\s+(\d+)` works
- Alternative: Look for gold icon and adjacent cell

### 3. Plunder System (⚠️ NEEDS TESTING)
- Bot needs to:
  - Find and click radio button for "10" minutes
  - Submit the plunder form
  - Wait for 10-minute timer
  - Repeat until 120 minutes used up

### 4. Training System (⚠️ NEEDS REFINEMENT)
- Bot should:
  - Look for "Train" images or submit buttons
  - Click to train (may need form submission)
  - Check gold after each click
  - Stop when gold <= MIN_RESERVE (10)
- Cost per training: TBD (likely 1-5 gold at level 1)

### 5. Elixir Buying (✅ LOGIC CONFIRMED)
- Only trigger when:
  - Gold > 100
  - No more training available (all stats maxed for current gold)
- Buy most expensive elixir affordable
- Repeat until gold ≈ 10

### 6. Player Attack (❌ NOT TESTED YET)
- Need to test:
  - Search for players by level
  - Click attack button
  - Handle 5-minute cooldown

---

## Next Steps:
1. ✅ Refine bot selectors based on testing
2. ⚠️ Test full plunder cycle (needs game time/testing)
3. ⚠️ Test training with actual gold spending
4. ⚠️ Test player attack search and execution
5. ✅ Update bot with confirmed URLs and selectors
