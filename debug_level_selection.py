import asyncio
from playwright.async_api import async_playwright

async def debug_level():
    p = await async_playwright().start()
    b = await p.firefox.launch(headless=False)
    ctx = await b.new_context(ignore_https_errors=True)
    page = await ctx.new_page()
    
    print("Logging in...")
    await page.goto('https://www.holy-war.net/auth/loginform/')
    await asyncio.sleep(2)
    await page.fill('input[type="text"]', 'tvcker')
    await page.fill('input[type="password"]', '174210Tg')
    await page.click('button:has(img[alt="Login"])')
    await asyncio.sleep(5)
    
    print("\n=== Going to attack page ===")
    await page.goto('https://www.holy-war.net/assault/1on1/?w=17IN')
    await asyncio.sleep(3)
    
    # Check current value
    current_val = await page.input_value('input[name="level"]')
    print(f"Current level value: '{current_val}'")
    
    # Select "Exact or lower"
    print("\n=== Selecting 'Exact or lower' ===")
    await page.select_option('select[name="searchtype"]', value='lower')
    await asyncio.sleep(1)
    
    # Try different methods to set the level
    print("\n=== Method 1: Using fill() ===")
    await page.fill('input[name="level"]', '3')
    await asyncio.sleep(1)
    new_val = await page.input_value('input[name="level"]')
    print(f"After fill('3'): '{new_val}'")
    
    print("\n=== Method 2: Clear then fill ===")
    await page.fill('input[name="level"]', '')
    await asyncio.sleep(0.5)
    await page.fill('input[name="level"]', '3')
    await asyncio.sleep(1)
    new_val = await page.input_value('input[name="level"]')
    print(f"After clear + fill('3'): '{new_val}'")
    
    print("\n=== Method 3: Using type() after clearing ===")
    # Triple-click to select all, then type
    await page.click('input[name="level"]', click_count=3)
    await page.keyboard.type('3')
    await asyncio.sleep(1)
    new_val = await page.input_value('input[name="level"]')
    print(f"After select-all + type('3'): '{new_val}'")
    
    # Take screenshot before search
    await page.screenshot(path='before_search.png')
    print("\nSaved before_search.png")
    
    print("\n=== Clicking Search ===")
    await page.click('button[name="Search"]')
    await asyncio.sleep(3)
    
    # Save the result page
    content = await page.content()
    with open('search_result.html', 'w', encoding='utf-8') as f:
        f.write(content)
    await page.screenshot(path='search_result.png')
    print("Saved search_result.html and search_result.png")
    
    # Check what level opponent we got
    import re
    level_match = re.search(r'Level[:\s]+(\d+)', content, re.IGNORECASE)
    if level_match:
        opponent_level = level_match.group(1)
        print(f"\n=== Opponent Level: {opponent_level} ===")
    
    print("\nKeeping browser open for 30 seconds...")
    await asyncio.sleep(30)
    
    await b.close()
    await p.stop()

asyncio.run(debug_level())

