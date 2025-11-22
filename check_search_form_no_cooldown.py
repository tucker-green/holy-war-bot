import asyncio
from playwright.async_api import async_playwright
import re

async def check_form():
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
    
    print("Going to attack page...")
    await page.goto('https://www.holy-war.net/assault/1on1/?w=17IN')
    await asyncio.sleep(3)
    
    content = await page.content()
    
    # Check for cooldown
    if "You still have to wait" in content or "have to wait for" in content:
        print("\n❌ COOLDOWN ACTIVE - Cannot see search form yet")
        countdown_match = re.search(r'<span id="counter\d+">(\d+):(\d+):(\d+)</span>', content)
        if countdown_match:
            hours = int(countdown_match.group(1))
            minutes = int(countdown_match.group(2))
            seconds = int(countdown_match.group(3))
            print(f"Cooldown remaining: {hours}h {minutes}m {seconds}s")
            print(f"\nWaiting for cooldown to expire...")
            total_seconds = hours * 3600 + minutes * 60 + seconds + 5
            await asyncio.sleep(total_seconds)
            print("Cooldown should be done. Refreshing page...")
            await page.goto('https://www.holy-war.net/assault/1on1/?w=17IN')
            await asyncio.sleep(3)
            content = await page.content()
    
    # Save the page
    with open('attack_no_cooldown.html', 'w', encoding='utf-8') as f:
        f.write(content)
    await page.screenshot(path='attack_no_cooldown.png', full_page=True)
    print("\nSaved attack_no_cooldown.html and attack_no_cooldown.png")
    
    # Look for level input and searchtype dropdown
    print("\n=== Looking for search form elements ===")
    
    # Check for searchtype dropdown
    searchtype = await page.locator('select[name="searchtype"]').count()
    print(f"searchtype dropdown: {searchtype > 0}")
    
    # Check for level input
    level_input = await page.locator('input[name="level"]').count()
    print(f"level input field: {level_input > 0}")
    
    # Check for Search button
    search_btn = await page.locator('button[name="Search"]').count()
    print(f"Search button: {search_btn > 0}")
    
    if level_input > 0:
        # Try to get current value
        try:
            val = await page.locator('input[name="level"]').get_attribute('value')
            print(f"\nCurrent level input value: '{val}'")
        except:
            print("\nCouldn't get level input value")
    
    # Look for all inputs and selects
    inputs = await page.locator('input').all()
    print(f"\n=== All inputs ({len(inputs)}) ===")
    for i, inp in enumerate(inputs[:25]):
        try:
            name = await inp.get_attribute('name')
            input_type = await inp.get_attribute('type')
            value = await inp.get_attribute('value')
            if name and ('level' in str(name).lower() or 'search' in str(name).lower()):
                print(f"  ★ Input {i}: type={input_type}, name={name}, value={value}")
        except:
            pass
    
    selects = await page.locator('select').all()
    print(f"\n=== All selects ({len(selects)}) ===")
    for i, sel in enumerate(selects):
        try:
            name = await sel.get_attribute('name')
            print(f"  Select {i}: name={name}")
        except:
            pass
    
    print("\nKeeping browser open for 30 seconds...")
    await asyncio.sleep(30)
    
    await b.close()
    await p.stop()

asyncio.run(check_form())

