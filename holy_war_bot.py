"""
Holy War Game Bot
Automates gameplay including plundering, training, buying elixirs, and attacking players.
"""

import asyncio
import time
from datetime import datetime, timedelta
from playwright.async_api import async_playwright, Page, Browser, Playwright
import logging
import config
from tqdm import tqdm

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def wait_with_progress_bar(minutes: int, description: str, total_duration_minutes: int = None):
    """Wait with a visual progress bar showing remaining time
    
    Args:
        minutes: Time to wait in minutes
        description: Description for the progress bar
        total_duration_minutes: Total duration in minutes (for calculating percentage). 
                               If provided, shows progress relative to total duration.
    """
    wait_seconds = minutes * 60
    
    # Print top border
    print("\n" + "="*80)
    
    if total_duration_minutes:
        # Calculate progress relative to total duration
        total_seconds = total_duration_minutes * 60
        elapsed_seconds = total_seconds - wait_seconds
        
        with tqdm(total=total_seconds, desc=description, unit="s", 
                 bar_format='║ {desc}: {bar} {percentage:3.0f}% | {elapsed}/{total}s ║',
                 initial=elapsed_seconds,
                 ncols=78,
                 leave=True) as pbar:
            for i in range(wait_seconds):
                await asyncio.sleep(1)
                pbar.update(1)
    else:
        # Standard progress bar (0% to 100% for the wait time)
        with tqdm(total=wait_seconds, desc=description, unit="s", 
                 bar_format='║ {desc}: {bar} {percentage:3.0f}% | {n_fmt}/{total_fmt}s ║',
                 ncols=78,
                 leave=True) as pbar:
            for i in range(wait_seconds):
                await asyncio.sleep(1)
                pbar.update(1)
    
    # Print bottom border (after progress bar completes)
    print("="*80)


class HolyWarBot:
    def __init__(self, username: str, password: str, world: str = "17IN"):
        self.username = username
        self.password = password
        self.world = world
        self.base_url = "https://www.holy-war.net"
        self.page: Page = None
        self.browser: Browser = None
        self.playwright: Playwright = None
        self.context = None
        
        # Configuration
        self.min_gold_reserve = 10
        self.elixir_threshold = 100
        self.plunder_duration_minutes = 10
        self.attack_cooldown_minutes = 5
        self.target_player_level = 1  # Configurable
        
        # State tracking
        self.plunder_time_remaining = 120  # Start with 2 hours (120 minutes)
        self.last_plunder_time = None
        self.last_attack_time = None
        
    async def start(self, headless=False):
        """Initialize browser and start bot"""
        try:
            logger.info("Starting Playwright...")
            self.playwright = await async_playwright().start()
            
            logger.info("Launching Firefox browser...")
            # Launch browser with minimal options first
            # Using Firefox instead of Chromium due to macOS compatibility issues
            self.browser = await self.playwright.firefox.launch(
                headless=headless,
                timeout=60000  # 60 second timeout
            )
            
            logger.info("Creating browser context...")
            # Create a browser context explicitly with network settings
            self.context = await self.browser.new_context(
                viewport={'width': 1280, 'height': 720},
                ignore_https_errors=True,
                java_script_enabled=True
            )
            
            logger.info("Creating new page...")
            # Create page from context
            self.page = await self.context.new_page()
            
            # Test that page is working by navigating to a simple page
            logger.info("Testing page navigation...")
            await self.page.goto("about:blank", timeout=10000)
            
            logger.info("Bot started successfully")
        except Exception as e:
            logger.error(f"Failed to start browser: {e}")
            import traceback
            logger.error(traceback.format_exc())
            # Cleanup on failure
            await self._cleanup()
            raise
    
    async def _cleanup(self):
        """Internal cleanup method"""
        try:
            if self.context:
                await self.context.close()
        except:
            pass
        try:
            if self.browser:
                await self.browser.close()
        except:
            pass
        try:
            if self.playwright:
                await self.playwright.stop()
        except:
            pass
        
    async def stop(self):
        """Close browser and cleanup"""
        await self._cleanup()
        logger.info("Bot stopped")
        
    async def is_logged_in(self) -> bool:
        """Check if currently logged in"""
        try:
            # Check for elements that only exist when logged in
            # The gold counter (#spMoney) only exists when logged in
            gold_span = self.page.locator('#spMoney')
            if await gold_span.count() > 0:
                return True
            
            # Also check if we're on the login page
            current_url = self.page.url
            if "/auth/loginform" in current_url or "/auth/login" in current_url:
                return False
            
            # Check for login button
            login_button = self.page.locator('button:has(img[alt="Login"])')
            if await login_button.count() > 0:
                return False
            
            # If we can see the username in the page, we're logged in
            content = await self.page.content()
            if self.username in content and "logout" in content.lower():
                return True
                
            return False
            
        except Exception as e:
            logger.warning(f"Error checking login status: {e}")
            return False
    
    async def login(self):
        """Login to the game"""
        logger.info(f"Logging in as {self.username}...")
        
        # Navigate to login page directly
        await self.page.goto(f"{self.base_url}/auth/loginform/")
        await asyncio.sleep(3)
        
        # Fill in credentials - using more flexible selectors
        username_field = self.page.locator('input[type="text"]').first
        await username_field.fill(self.username)
        
        password_field = self.page.locator('input[type="password"]').first
        await password_field.fill(self.password)
        
        # Submit login - click the button containing the Login image
        await self.page.click('button:has(img[alt="Login"])')
        await asyncio.sleep(5)
        
        # Verify login by checking if we're on the welcome page
        if "/welcome" in self.page.url or "/char/attributes" in self.page.url:
            logger.info("Logged in successfully")
        else:
            logger.warning(f"Login might have failed. Current URL: {self.page.url}")
    
    async def ensure_logged_in(self):
        """Check if logged in, and re-login if necessary"""
        try:
            if not await self.is_logged_in():
                logger.warning("Not logged in! Attempting to re-login...")
                await self.login()
                
                # Verify login worked
                if await self.is_logged_in():
                    logger.info("Re-login successful!")
                    return True
                else:
                    logger.error("Re-login failed!")
                    return False
            return True
        except Exception as e:
            logger.error(f"Error in ensure_logged_in: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return False
    
    async def safe_goto(self, url: str, timeout: int = 30000):
        """Navigate to a URL with login check"""
        try:
            await self.page.goto(url, timeout=timeout)
        except Exception as e:
            logger.warning(f"Navigation error: {e}")
            # Check if logged out
            if not await self.is_logged_in():
                logger.warning("Detected logout during navigation. Re-logging in...")
                await self.ensure_logged_in()
                # Try navigation again
                await self.page.goto(url, timeout=timeout)
        
    async def get_current_gold(self) -> int:
        """Get current gold amount from the status bar"""
        try:
            # First try: Use the spMoney span (most reliable)
            gold_span = self.page.locator('#spMoney')
            if await gold_span.count() > 0:
                text = await gold_span.text_content()
                if text and text.strip().isdigit():
                    gold = int(text.strip())
                    logger.info(f"Current gold: {gold}")
                    return gold
            
            # Fallback: Look for the gold indicator in the status bar
            gold_cells = await self.page.locator('td:has(img[name*="Gold"]), td:has(img[alt*="Gold"])').all()
            
            for cell in gold_cells:
                text = await cell.text_content()
                if text and text.strip().isdigit():
                    gold = int(text.strip())
                    logger.info(f"Current gold (fallback method): {gold}")
                    return gold
            
            # If we can't find gold, might be logged out
            logger.warning("Could not detect gold - may be logged out")
            if not await self.is_logged_in():
                logger.warning("Confirmed: not logged in")
                return -1  # Return -1 to signal logout
                
        except Exception as e:
            logger.error(f"Error getting gold: {e}")
            import traceback
            logger.error(traceback.format_exc())
        
        logger.warning("Could not detect gold, returning 0")
        return 0
        
    async def get_plunder_time_remaining(self) -> int:
        """Get remaining plunder time in minutes"""
        try:
            # Look for plunder time indicator
            text = await self.page.content()
            if "Plunder / protect time remaining today:" in text:
                # Extract the time value
                import re
                match = re.search(r'Plunder / protect time remaining today: (\d+) min', text)
                if match:
                    time_remaining = int(match.group(1))
                    logger.info(f"Plunder time remaining: {time_remaining} minutes")
                    return time_remaining
        except Exception as e:
            logger.error(f"Error getting plunder time: {e}")
        return self.plunder_time_remaining
        
    async def do_plunder(self):
        """Execute a plunder action"""
        logger.info("Starting plunder...")
        
        # Navigate to attack page
        await self.page.goto(f"{self.base_url}/assault/1on1/?w={self.world}")
        await asyncio.sleep(2)
        
        # Update plunder time remaining
        self.plunder_time_remaining = await self.get_plunder_time_remaining()
        
        if self.plunder_time_remaining < self.plunder_duration_minutes:
            logger.warning(f"Not enough plunder time remaining ({self.plunder_time_remaining} min)")
            return False
            
        try:
            # Select the plunder duration from the dropdown
            logger.info(f"Selecting {self.plunder_duration_minutes} minute plunder duration...")
            await self.page.select_option('select[name="ravageTime"]', str(self.plunder_duration_minutes))
            await asyncio.sleep(1)
            
            # Click the plunder button
            logger.info("Clicking plunder button...")
            await self.page.click('button[name="PLUNDER_ACTION"]')
            await asyncio.sleep(3)
            
            self.last_plunder_time = datetime.now()
            self.plunder_time_remaining -= self.plunder_duration_minutes
            
            logger.info(f"Plunder started! Will complete in {self.plunder_duration_minutes} minutes")
            logger.info(f"Plunder time remaining: {self.plunder_time_remaining} minutes")
            return True
            
        except Exception as e:
            logger.error(f"Error during plunder: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return False
            
    async def get_training_costs(self):
        """Get the actual training cost for each stat from the page"""
        try:
            costs = []
            
            # Find all train button rows
            train_buttons = await self.page.locator('img[alt="Train"]').all()
            
            for btn in train_buttons:
                # Navigate up to the row, then find the cost
                # The cost is in <td class="ltr"><b>XX</b></td>
                row = btn.locator('xpath=ancestor::tr[1]')
                cost_cell = row.locator('td.ltr b')
                cost_text = await cost_cell.text_content()
                cost = int(cost_text.strip())
                costs.append(cost)
                
            if costs:
                logger.info(f"Training costs found: {costs}")
                return costs
            
            # Default if we can't find any
            logger.warning("Could not find training costs, using default [1]")
            return [1]
            
        except Exception as e:
            logger.warning(f"Error getting training costs: {e}. Using default [1]")
            return [1]
    
    async def train_attributes(self):
        """Train attributes with available gold, keeping minimum reserve"""
        logger.info("Training attributes...")
        
        # Navigate to status/attributes page
        await self.page.goto(f"{self.base_url}/char/attributes/?w={self.world}")
        await asyncio.sleep(3)
        
        current_gold = await self.get_current_gold()
        trained_something = False
        training_count = 0
        
        # Keep training while we have enough gold above minimum
        while training_count < 50:  # Max 50 trainings per cycle
            try:
                # Get current training costs for all available stats
                training_costs = await self.get_training_costs()
                
                if not training_costs:
                    logger.info("No training buttons found (all stats maxed)")
                    break
                
                # Stat order: Strength (0), Attack (1), Defence (2), Agility (3), Stamina (4)
                strength_cost = training_costs[0] if len(training_costs) > 0 else None
                min_cost = min(training_costs)
                cheapest_index = training_costs.index(min_cost)
                
                # Decide which stat to train: prioritize Strength, then cheapest
                train_index = None
                train_cost = None
                
                if strength_cost and current_gold - strength_cost > self.min_gold_reserve:
                    # Can afford Strength, train it
                    train_index = 0
                    train_cost = strength_cost
                    logger.info(f"Training STRENGTH (priority): costs {strength_cost} gold")
                elif current_gold - min_cost > self.min_gold_reserve:
                    # Can't afford Strength but can afford cheapest
                    train_index = cheapest_index
                    train_cost = min_cost
                    stat_names = ["Strength", "Attack", "Defence", "Agility", "Stamina"]
                    stat_name = stat_names[cheapest_index] if cheapest_index < len(stat_names) else f"stat #{cheapest_index}"
                    logger.info(f"Training {stat_name} (cheapest): costs {min_cost} gold")
                else:
                    # Can't afford any training
                    logger.info(f"Insufficient gold to train. Current: {current_gold}, Min cost: {min_cost}, Reserve: {self.min_gold_reserve}")
                    logger.info(f"Would have {current_gold - min_cost} gold after training, need > {self.min_gold_reserve}")
                    break
                
                # Get the train buttons
                train_buttons = await self.page.locator('img[alt="Train"]').all()
                
                if train_index >= len(train_buttons):
                    logger.error(f"Train button index {train_index} out of range")
                    break
                
                # We have enough gold, proceed with training
                logger.info(f"Gold check passed: {current_gold} - {train_cost} = {current_gold - train_cost} > {self.min_gold_reserve}")
                
                # Click the selected train button
                await train_buttons[train_index].click()
                await asyncio.sleep(3)
                
                # Check if we're still on the attributes page or if we got an error
                current_url = self.page.url
                if "/char/attributes" not in current_url:
                    # We might have been redirected, go back
                    await self.page.goto(f"{self.base_url}/char/attributes/?w={self.world}")
                    await asyncio.sleep(2)
                else:
                    # Page might need a moment to update the gold display
                    await asyncio.sleep(0.5)
                
                # Update gold
                new_gold = await self.get_current_gold()
                
                if new_gold >= current_gold or new_gold == 0:
                    # No gold was spent, training failed or we're out of gold
                    logger.info("Cannot train anymore (training failed or maxed)")
                    break
                    
                actual_cost = current_gold - new_gold
                current_gold = new_gold
                trained_something = True
                training_count += 1
                
                logger.info(f"Training #{training_count} - Cost: {actual_cost} gold. Remaining gold: {current_gold}")
                    
            except Exception as e:
                logger.error(f"Error during training: {e}")
                import traceback
                logger.error(traceback.format_exc())
                break
                
        if trained_something:
            logger.info(f"Completed {training_count} trainings. Final gold: {current_gold}")
        else:
            logger.info("No training was possible")
            
        return trained_something, current_gold
        
    async def sell_cheapest_elixir(self):
        """Sell the cheapest elixir to get gold for plundering"""
        logger.info("Selling cheapest elixir...")
        
        # Navigate to elixirs shop
        await self.page.goto(f"{self.base_url}/town/alchemist/?w={self.world}")
        await asyncio.sleep(2)
        
        current_gold = await self.get_current_gold()
        
        try:
            # Try to find and click sell buttons for elixirs
            # Start with cheapest: Consecrated Elixir (50 gold) -> Baptised Elixir (90) -> Blessed Elixir (450)
            
            # Look for sell buttons - they should be near elixir names
            sell_buttons = await self.page.locator('input[type="image"][alt*="Sell"], img[alt*="Sell"]').all()
            
            if len(sell_buttons) > 0:
                # Try to sell the cheapest elixir first (usually first sell button)
                await sell_buttons[0].click()
                await asyncio.sleep(2)
                
                new_gold = await self.get_current_gold()
                if new_gold > current_gold:
                    logger.info(f"Sold elixir. Gold: {current_gold} -> {new_gold}")
                    return True
                else:
                    logger.warning("Sell button clicked but gold didn't increase")
                    return False
            else:
                logger.warning("No sell buttons found - you may not have any elixirs to sell")
                return False
                
        except Exception as e:
            logger.error(f"Error selling elixir: {e}")
            return False
    
    async def buy_elixirs(self):
        """Buy elixirs if gold > threshold"""
        logger.info("Buying elixirs...")
        
        # Navigate to elixirs shop
        await self.page.goto(f"{self.base_url}/town/alchemist/?w={self.world}")
        await asyncio.sleep(2)
        
        current_gold = await self.get_current_gold()
        
        if current_gold < self.elixir_threshold:
            logger.info(f"Gold ({current_gold}) below elixir threshold ({self.elixir_threshold})")
            return False
            
        # Keep buying the most expensive elixir we can afford until we're close to min_gold_reserve
        bought_something = False
        
        while current_gold > self.min_gold_reserve + 50:  # Keep some buffer
            try:
                # Find all buy buttons and their prices
                # Look for elixirs and their prices in the page
                content = await self.page.content()
                
                # Try to find and click buy buttons for expensive elixirs
                # Blessed Elixir (450 gold) -> Baptised Elixir (90) -> Consecrated Elixir (50)
                
                if current_gold >= 450:
                    # Try to buy Blessed Elixir
                    try:
                        await self.page.click('input[type="image"][alt*="Buy"]:near(:text("Blessed Elixir"))')
                        await asyncio.sleep(1)
                        bought_something = True
                        current_gold -= 450
                        logger.info(f"Bought Blessed Elixir for 450 gold. Remaining: {current_gold}")
                        continue
                    except:
                        pass
                        
                if current_gold >= 90:
                    # Try to buy Baptised Elixir
                    try:
                        await self.page.click('input[type="image"][alt*="Buy"]:near(:text("Baptised Elixir"))')
                        await asyncio.sleep(1)
                        bought_something = True
                        current_gold -= 90
                        logger.info(f"Bought Baptised Elixir for 90 gold. Remaining: {current_gold}")
                        continue
                    except:
                        pass
                        
                if current_gold >= 50:
                    # Try to buy Consecrated Elixir
                    try:
                        await self.page.click('input[type="image"][alt*="Buy"]:near(:text("Consecrated Elixir"))')
                        await asyncio.sleep(1)
                        bought_something = True
                        current_gold -= 50
                        logger.info(f"Bought Consecrated Elixir for 50 gold. Remaining: {current_gold}")
                        continue
                    except:
                        pass
                        
                # If we get here, we couldn't buy anything
                break
                
            except Exception as e:
                logger.error(f"Error buying elixirs: {e}")
                break
                
        return bought_something
        
    async def attack_player(self):
        """Attack a player of the target level"""
        logger.info(f"Attacking player of level {self.target_player_level}...")
        
        # Navigate to attack page
        await self.page.goto(f"{self.base_url}/assault/1on1/?w={self.world}")
        await asyncio.sleep(2)
        
        try:
            # Fill in search criteria
            # Look for level input field
            await self.page.fill('input[name="level"]', str(self.target_player_level))
            
            # Click search button
            await self.page.click('input[type="submit"][value*="Search"], input[type="image"][alt*="Search"]')
            await asyncio.sleep(2)
            
            # Click attack button on first player in results
            attack_buttons = await self.page.locator('input[type="image"][alt*="Attack"], a:has-text("Attack")').all()
            
            if attack_buttons:
                await attack_buttons[0].click()
                await asyncio.sleep(2)
                
                self.last_attack_time = datetime.now()
                logger.info("Attack initiated!")
                return True
            else:
                logger.warning("No players found to attack")
                return False
                
        except Exception as e:
            logger.error(f"Error attacking player: {e}")
            return False
            
    async def run_plunder_cycle(self):
        """Run one plunder cycle: plunder -> train -> buy elixirs"""
        logger.info("=== Starting plunder cycle ===")
        
        # Do plunder
        plunder_success = await self.do_plunder()
        
        if not plunder_success:
            return False
            
        # Wait for plunder to complete (10 minutes)
        logger.info(f"Waiting {self.plunder_duration_minutes} minutes for plunder to complete...")
        await asyncio.sleep(self.plunder_duration_minutes * 60)
        
        # Go to status page and train
        # train_attributes already checks if we have enough gold (current - cost > min_reserve)
        trained, current_gold = await self.train_attributes()
        
        # After training, check if we should buy elixirs
        # Only buy if: gold > 100 AND we can't train anymore (stats maxed)
        if current_gold > self.elixir_threshold:
            logger.info(f"Gold ({current_gold}) is above elixir threshold ({self.elixir_threshold})")
            
            # Check if there are still training buttons available
            await self.page.goto(f"{self.base_url}/char/attributes/?w={self.world}")
            await asyncio.sleep(2)
            
            train_buttons = await self.page.locator('img[alt="Train"], img[name="Train"]').all()
            
            if len(train_buttons) == 0:
                # No training buttons = all stats maxed, buy elixirs
                logger.info("No training buttons found (all stats maxed). Buying elixirs...")
                await self.buy_elixirs()
            else:
                # Training buttons exist but we stopped training because of gold reserve
                # Check the training cost again
                training_costs = await self.get_training_costs()
                if training_costs:
                    min_training_cost = min(training_costs)
                    if current_gold - min_training_cost <= self.min_gold_reserve:
                        # Can't train without going below reserve, buy elixirs
                        logger.info(f"Can't train (would leave {current_gold - min_training_cost} gold, need > {self.min_gold_reserve}). Buying elixirs...")
                        await self.buy_elixirs()
                    else:
                        logger.info("Can still train. Not buying elixirs yet.")
                
        return True
        
    async def can_train_with_reserve(self):
        """Check if we can train a stat and still have > 10 gold left"""
        # Make sure we're on the attributes page to check training cost
        if "/char/attributes" not in self.page.url:
            await self.page.goto(f"{self.base_url}/char/attributes/?w={self.world}")
            await asyncio.sleep(2)
        
        current_gold = await self.get_current_gold()
        
        # Get all training costs
        training_costs = await self.get_training_costs()
        has_training_available = len(training_costs) > 0
        
        if not has_training_available:
            logger.info("Cannot train: No training buttons available (all stats maxed)")
            return False
        
        # Check if we can afford the cheapest training option
        min_training_cost = min(training_costs)
        can_train = (current_gold - min_training_cost) > self.min_gold_reserve
        
        if can_train:
            logger.info(f"Can train: {current_gold} - {min_training_cost} = {current_gold - min_training_cost} > {self.min_gold_reserve}")
        else:
            logger.info(f"Cannot train: {current_gold} - {min_training_cost} = {current_gold - min_training_cost} <= {self.min_gold_reserve}")
        
        return can_train
    
    async def check_active_plunder(self):
        """Check if already plundering and wait for it to complete"""
        try:
            # Go to attack page to check status
            await self.page.goto(f"{self.base_url}/assault/1on1/?w={self.world}")
            await asyncio.sleep(2)
            
            content = await self.page.content()
            
            if "You're now plundering" in content or "You're now protecting" in content:
                logger.info("Detected active plunder/protection!")
                
                # Try to extract the remaining time from the countdown
                import re
                # Look for countdown timer like "0:07:04"
                countdown_match = re.search(r'<span id="counter\d+">(\d+):(\d+):(\d+)</span>', content)
                
                if countdown_match:
                    hours = int(countdown_match.group(1))
                    minutes = int(countdown_match.group(2))
                    seconds = int(countdown_match.group(3))
                    total_minutes = hours * 60 + minutes + (1 if seconds > 0 else 0)
                    
                    logger.info(f"Plunder will complete in {hours}h {minutes}m {seconds}s ({total_minutes} minutes)")
                    logger.info(f"Waiting for plunder to complete...")
                    
                    # Wait for the plunder to complete with progress bar
                    # Show progress relative to plunder duration
                    await wait_with_progress_bar(total_minutes, f"Waiting for active plunder ({total_minutes}/{self.plunder_duration_minutes} min)", self.plunder_duration_minutes)
                    
                    # After waiting, go back to attack page to collect gold
                    logger.info("Active plunder complete! Collecting gold...")
                    await self.page.goto(f"{self.base_url}/assault/1on1/?w={self.world}")
                    await asyncio.sleep(3)
                    logger.info("Gold collected!")
                    return True
                else:
                    logger.warning("Found active plunder but couldn't parse countdown. Waiting 5 minutes...")
                    await wait_with_progress_bar(5, "Waiting for active plunder (5/10 min)", self.plunder_duration_minutes)
                    await self.page.goto(f"{self.base_url}/assault/1on1/?w={self.world}")
                    await asyncio.sleep(2)
                    return True
            
            logger.info("No active plunder detected. Ready to start!")
            return False
            
        except Exception as e:
            logger.error(f"Error checking active plunder: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return False
    
    async def run(self):
        """Main bot loop - follows the exact flowchart logic"""
        try:
            await self.start(headless=config.HEADLESS)
            await self.login()
            
            # Check if already plundering before starting main loop
            await self.check_active_plunder()
            
            # Main game loop - follows flowchart exactly
            while True:
                # Check if still logged in before each cycle
                if not await self.ensure_logged_in():
                    logger.error("Cannot continue - login failed. Retrying in 60 seconds...")
                    await asyncio.sleep(60)
                    continue
                
                # STEP 1: Check if we can train (and have > 10 gold left)
                logger.info("=== Checking if we can train ===")
                can_train = await self.can_train_with_reserve()
                
                if can_train:
                    # Train stats repeatedly until we can't train anymore
                    logger.info("Training stats...")
                    trained, current_gold = await self.train_attributes()
                    logger.info(f"Training complete. Gold: {current_gold}")
                
                # STEP 2: Go to attack page and check plunder time
                logger.info("=== Checking plunder time ===")
                await self.page.goto(f"{self.base_url}/assault/1on1/?w={self.world}")
                await asyncio.sleep(2)
                
                self.plunder_time_remaining = await self.get_plunder_time_remaining()
                
                if self.plunder_time_remaining >= self.plunder_duration_minutes:
                    # YES - We have plunder time
                    logger.info(f"Plunder time available: {self.plunder_time_remaining} minutes")
                    
                    # Check: Do I have 10 or more gold?
                    current_gold = await self.get_current_gold()
                    
                    if current_gold >= self.min_gold_reserve:
                        # YES - Plunder for 10 minutes
                        logger.info(f"Gold check passed ({current_gold} >= {self.min_gold_reserve}). Starting plunder...")
                        plunder_success = await self.do_plunder()
                        
                        if plunder_success:
                            logger.info(f"Plundering for {self.plunder_duration_minutes} minutes...")
                            await wait_with_progress_bar(self.plunder_duration_minutes, f"Plundering ({self.plunder_duration_minutes} min)", self.plunder_duration_minutes)
                            logger.info("Plunder complete! Collecting gold...")
                            
                            # Go back to attack page to collect the gold
                            await self.page.goto(f"{self.base_url}/assault/1on1/?w={self.world}")
                            await asyncio.sleep(3)
                            logger.info("Gold collected! Looping back to training check...")
                            
                            # Loop back to STEP 1 (training check)
                            continue
                    else:
                        # NO - Sell cheapest elixir, then plunder
                        logger.info(f"Gold too low ({current_gold} < {self.min_gold_reserve}). Selling elixir...")
                        sold = await self.sell_cheapest_elixir()
                        
                        if sold:
                            # After selling, try to plunder
                            logger.info("Elixir sold. Attempting to plunder...")
                            plunder_success = await self.do_plunder()
                            
                            if plunder_success:
                                logger.info(f"Plundering for {self.plunder_duration_minutes} minutes...")
                                await wait_with_progress_bar(self.plunder_duration_minutes, f"Plundering ({self.plunder_duration_minutes} min)", self.plunder_duration_minutes)
                                logger.info("Plunder complete! Collecting gold...")
                                
                                # Go back to attack page to collect the gold
                                await self.page.goto(f"{self.base_url}/assault/1on1/?w={self.world}")
                                await asyncio.sleep(3)
                                logger.info("Gold collected! Looping back to training check...")
                                
                                # Loop back to STEP 1 (training check)
                                continue
                        else:
                            logger.warning("Could not sell elixir. May not have any elixirs.")
                            # Continue anyway - might have enough gold now
                            continue
                else:
                    # NO - No plunder time
                    logger.info(f"No plunder time remaining ({self.plunder_time_remaining} minutes)")
                    
                    # Go to status page and check if we can train
                    logger.info("Checking status page for training...")
                    await self.page.goto(f"{self.base_url}/char/attributes/?w={self.world}")
                    await asyncio.sleep(2)
                    
                    # Check if we can train
                    can_train = await self.can_train_with_reserve()
                    if can_train:
                        logger.info("Can train while waiting for plunder time. Training...")
                        trained, current_gold = await self.train_attributes()
                    
                    # Attack a player, wait 5 minutes, then check plunder time again
                    logger.info("Attacking a player...")
                    await self.attack_player()
                    
                    logger.info(f"Waiting {self.attack_cooldown_minutes} minutes for attack cooldown...")
                    await wait_with_progress_bar(self.attack_cooldown_minutes, f"Attack Cooldown ({self.attack_cooldown_minutes} min)")
                    
                    # Loop back to STEP 2 (check plunder time)
                    continue
                
                await asyncio.sleep(5)  # Small delay between cycles
                
        except KeyboardInterrupt:
            logger.info("Bot interrupted by user")
        except Exception as e:
            logger.error(f"Bot error: {e}")
            import traceback
            logger.error(traceback.format_exc())
        finally:
            await self.stop()


async def main():
    # Load configuration from config.py
    bot = HolyWarBot(config.USERNAME, config.PASSWORD, config.WORLD)
    
    # Apply configuration
    bot.min_gold_reserve = config.MIN_GOLD_RESERVE
    bot.elixir_threshold = config.ELIXIR_THRESHOLD
    bot.target_player_level = config.TARGET_PLAYER_LEVEL
    bot.plunder_duration_minutes = config.PLUNDER_DURATION_MINUTES
    bot.attack_cooldown_minutes = config.ATTACK_COOLDOWN_MINUTES
    
    logger.info("=== Holy War Bot Configuration ===")
    logger.info(f"Username: {config.USERNAME}")
    logger.info(f"World: {config.WORLD}")
    logger.info(f"Min Gold Reserve: {config.MIN_GOLD_RESERVE}")
    logger.info(f"Elixir Threshold: {config.ELIXIR_THRESHOLD}")
    logger.info(f"Target Player Level: {config.TARGET_PLAYER_LEVEL}")
    logger.info(f"Plunder Duration: {config.PLUNDER_DURATION_MINUTES} minutes")
    logger.info(f"Attack Cooldown: {config.ATTACK_COOLDOWN_MINUTES} minutes")
    logger.info("==================================")
    
    await bot.run()


if __name__ == "__main__":
    asyncio.run(main())

