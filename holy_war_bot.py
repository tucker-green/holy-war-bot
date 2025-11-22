"""
Holy War Game Bot
Automates gameplay including plundering, training, buying elixirs, and attacking players.
"""

import asyncio
import time
from datetime import datetime, timedelta
from playwright.async_api import async_playwright, Page, Browser
import logging
import config

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class HolyWarBot:
    def __init__(self, username: str, password: str, world: str = "17IN"):
        self.username = username
        self.password = password
        self.world = world
        self.base_url = "https://www.holy-war.net"
        self.page: Page = None
        self.browser: Browser = None
        
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
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(headless=headless)
        self.page = await self.browser.new_page()
        
        logger.info("Bot started")
        
    async def stop(self):
        """Close browser and cleanup"""
        if self.browser:
            await self.browser.close()
        logger.info("Bot stopped")
        
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
        
    async def get_current_gold(self) -> int:
        """Get current gold amount from the status bar"""
        try:
            # Look for the gold indicator in the status bar
            # The gold is in a cell next to the gold image
            gold_cells = await self.page.locator('td:has(img[name*="Gold"]), td:has(img[alt*="Gold"])').all()
            
            for cell in gold_cells:
                text = await cell.text_content()
                if text and text.strip().isdigit():
                    gold = int(text.strip())
                    logger.info(f"Current gold: {gold}")
                    return gold
                    
            # Alternative: look for cells near the gold image
            page_content = await self.page.content()
            import re
            # Look for pattern like Christian 14 100 1 where 14 is gold
            match = re.search(r'Chri\s*tian\s+(\d+)\s+\d+\s+\d+', page_content)
            if match:
                gold = int(match.group(1))
                logger.info(f"Current gold (alt method): {gold}")
                return gold
                
        except Exception as e:
            logger.error(f"Error getting gold: {e}")
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
            
        # Look for plunder duration radio button (10 minutes)
        try:
            # Click the 10-minute plunder option
            await self.page.click(f'input[type="radio"][value="{self.plunder_duration_minutes}"]')
            await asyncio.sleep(1)
            
            # Click the plunder button
            await self.page.click('input[type="image"][name="b1"], input[type="submit"][value*="Plunder"]')
            await asyncio.sleep(2)
            
            self.last_plunder_time = datetime.now()
            self.plunder_time_remaining -= self.plunder_duration_minutes
            
            logger.info(f"Plunder started! Will complete in {self.plunder_duration_minutes} minutes")
            logger.info(f"Plunder time remaining: {self.plunder_time_remaining} minutes")
            return True
            
        except Exception as e:
            logger.error(f"Error during plunder: {e}")
            return False
            
    async def get_training_cost(self):
        """Try to determine the training cost from the page"""
        try:
            # Training cost is usually displayed near the train button
            # Look for numbers in cells or text near the training section
            content = await self.page.content()
            
            # For level 1, training typically costs 1 gold per stat point
            # As level increases, cost increases
            # For now, we'll estimate based on pattern or default to 1
            
            # Try to find cost indicators in the page
            import re
            # Look for patterns like "Cost: X" or numbers near "Train"
            cost_patterns = re.findall(r'(?:Cost|cost):\s*(\d+)', content)
            if cost_patterns:
                return int(cost_patterns[0])
            
            # Default assumption: 1 gold at low levels
            return 1
            
        except Exception as e:
            logger.warning(f"Could not determine training cost: {e}. Assuming 1 gold.")
            return 1
    
    async def train_attributes(self):
        """Train attributes with available gold, keeping minimum reserve"""
        logger.info("Training attributes...")
        
        # Navigate to status/attributes page
        await self.page.goto(f"{self.base_url}/char/attributes/?w={self.world}")
        await asyncio.sleep(3)
        
        current_gold = await self.get_current_gold()
        trained_something = False
        training_count = 0
        
        # Get the estimated training cost
        training_cost = await self.get_training_cost()
        logger.info(f"Estimated training cost: {training_cost} gold per training")
        
        # Keep training while we have enough gold above minimum
        while training_count < 50:  # Max 50 trainings per cycle
            try:
                # Check if we have enough gold to train and still keep reserve
                if current_gold - training_cost <= self.min_gold_reserve:
                    logger.info(f"Insufficient gold to train. Current: {current_gold}, Cost: {training_cost}, Reserve: {self.min_gold_reserve}")
                    logger.info(f"Would have {current_gold - training_cost} gold after training, need > {self.min_gold_reserve}")
                    break
                
                # Get the current page to check for training buttons
                train_buttons = await self.page.locator('img[alt="Train"], img[name="Train"]').all()
                
                if not train_buttons:
                    logger.info("No more training buttons found (all stats maxed)")
                    break
                
                # We have enough gold, proceed with training
                logger.info(f"Gold check passed: {current_gold} - {training_cost} = {current_gold - training_cost} > {self.min_gold_reserve}")
                
                # Click the first available train button
                await train_buttons[0].click()
                await asyncio.sleep(2)
                
                # Check if we're still on the attributes page or if we got an error
                current_url = self.page.url
                if "/char/attributes" not in current_url:
                    # We might have been redirected, go back
                    await self.page.goto(f"{self.base_url}/char/attributes/?w={self.world}")
                    await asyncio.sleep(2)
                
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
                
                # Update our cost estimate based on actual cost
                if actual_cost != training_cost:
                    logger.info(f"Training cost was {actual_cost}, not {training_cost}. Updating estimate.")
                    training_cost = actual_cost
                
                logger.info(f"Training #{training_count} - Cost: {actual_cost} gold. Remaining gold: {current_gold}")
                    
            except Exception as e:
                logger.error(f"Error during training: {e}")
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
                training_cost = await self.get_training_cost()
                if current_gold - training_cost <= self.min_gold_reserve:
                    # Can't train without going below reserve, buy elixirs
                    logger.info(f"Can't train (would leave {current_gold - training_cost} gold, need > {self.min_gold_reserve}). Buying elixirs...")
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
        training_cost = await self.get_training_cost()
        
        # Also check if there are training buttons available
        train_buttons = await self.page.locator('img[alt="Train"], img[name="Train"]').all()
        has_training_available = len(train_buttons) > 0
        
        # Check: current_gold - training_cost > min_gold_reserve?
        can_train = (current_gold - training_cost) > self.min_gold_reserve and has_training_available
        
        if can_train:
            logger.info(f"Can train: {current_gold} - {training_cost} = {current_gold - training_cost} > {self.min_gold_reserve}")
        else:
            if not has_training_available:
                logger.info("Cannot train: No training buttons available (all stats maxed)")
            else:
                logger.info(f"Cannot train: {current_gold} - {training_cost} = {current_gold - training_cost} <= {self.min_gold_reserve}")
        
        return can_train
    
    async def run(self):
        """Main bot loop - follows the exact flowchart logic"""
        try:
            await self.start(headless=config.HEADLESS)
            await self.login()
            
            # Main game loop - follows flowchart exactly
            while True:
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
                            await asyncio.sleep(self.plunder_duration_minutes * 60)
                            logger.info("Plunder complete! Looping back to training check...")
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
                                await asyncio.sleep(self.plunder_duration_minutes * 60)
                                logger.info("Plunder complete! Looping back to training check...")
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
                    await asyncio.sleep(self.attack_cooldown_minutes * 60)
                    
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

