import asyncio
from playwright.async_api import async_playwright
import re

async def debug_attack():
    p = await async_playwright().start()
    b = await p.firefox.launch(headless=False)
    ctx = await b.new_context(ignore_https_errors=True)
    page = await ctx.new_page()
    
    print("=== Logging in ===")
    await page.goto('https://www.holy-war.net/auth/loginform/')
    await asyncio.sleep(2)
    await page.fill('input[type="text"]', 'tvcker')
    await page.fill('input[type="password"]', '174210Tg')
    await page.click('button:has(img[alt="Login"])')
    await asyncio.sleep(5)
    
    print("\n=== Step 1: Get my stats ===")
    await page.goto('https://www.holy-war.net/char/attributes/?w=17IN')
    await asyncio.sleep(3)
    
    content = await page.content()
    my_stats = {}
    stat_names = ['Strength', 'Attack', 'Defence', 'Agility', 'Stamina']
    
    for stat in stat_names:
        match = re.search(rf'<td[^>]*>{stat}</td[^>]*>\s*<td[^>]*>(\d+)</td>', content, re.IGNORECASE)
        if match:
            my_stats[stat.lower()] = int(match.group(1))
    
    my_total = sum(my_stats.values())
    print(f"My stats: STR={my_stats.get('strength',0)}, ATT={my_stats.get('attack',0)}, DEF={my_stats.get('defence',0)}, AGI={my_stats.get('agility',0)}, STA={my_stats.get('stamina',0)}, Total={my_total}")
    
    print("\n=== Step 2: Navigate to attack page ===")
    await page.goto('https://www.holy-war.net/assault/1on1/?w=17IN')
    await asyncio.sleep(3)
    
    # Save initial attack page
    with open('attack_page_initial.html', 'w', encoding='utf-8') as f:
        f.write(await page.content())
    await page.screenshot(path='attack_page_initial.png', full_page=True)
    print("Saved attack_page_initial.html and attack_page_initial.png")
    
    print("\n=== Step 3: Fill search form ===")
    
    # Check for searchtype dropdown
    searchtype_dropdown = await page.locator('select[name="searchtype"]').count()
    print(f"Found searchtype dropdown: {searchtype_dropdown > 0}")
    
    if searchtype_dropdown > 0:
        # Get available options
        options = await page.locator('select[name="searchtype"] option').all()
        print(f"Searchtype options ({len(options)}):")
        for opt in options:
            value = await opt.get_attribute('value')
            text = await opt.text_content()
            print(f"  - value='{value}', text='{text}'")
        
        # Select "lower" (Exact or lower)
        print("\nSelecting 'Exact or lower' (value='lower')...")
        await page.select_option('select[name="searchtype"]', value='lower')
        await asyncio.sleep(1)
    
    # Fill level
    print(f"Filling level = 3...")
    await page.fill('input[name="level"]', '3')
    await asyncio.sleep(1)
    
    # Find search button
    search_buttons = await page.locator('button[name="Search"], input[type="image"][alt*="Search"], button:has-text("Search")').all()
    print(f"\nFound {len(search_buttons)} search button(s)")
    
    if len(search_buttons) > 0:
        print("Clicking search button...")
        await search_buttons[0].click()
        await asyncio.sleep(3)
    
    print("\n=== Step 4: Check opponent page ===")
    current_url = page.url
    print(f"Current URL: {current_url}")
    
    # Save opponent page
    with open('attack_page_after_search.html', 'w', encoding='utf-8') as f:
        f.write(await page.content())
    await page.screenshot(path='attack_page_after_search.png', full_page=True)
    print("Saved attack_page_after_search.html and attack_page_after_search.png")
    
    content = await page.content()
    
    # Try to find opponent stats
    print("\n=== Looking for opponent stats ===")
    opp_stats = {}
    for stat in stat_names:
        # Try different patterns
        patterns = [
            rf'<td[^>]*padding-left:30px;">{stat}</td>\s*<td[^>]*>(\d+)</td>',
            rf'<td[^>]*>{stat}</td>\s*<td[^>]*>(\d+)</td>',
            rf'{stat}.*?<td[^>]*>(\d+)</td>',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
            if match:
                opp_stats[stat.lower()] = int(match.group(1))
                print(f"Found {stat}: {match.group(1)} (pattern: {pattern[:50]}...)")
                break
    
    if opp_stats:
        opp_total = sum(opp_stats.values())
        print(f"\nOpponent stats: STR={opp_stats.get('strength',0)}, ATT={opp_stats.get('attack',0)}, DEF={opp_stats.get('defence',0)}, AGI={opp_stats.get('agility',0)}, STA={opp_stats.get('stamina',0)}, Total={opp_total}")
        print(f"My total: {my_total}, Opponent total: {opp_total}")
        print(f"Should attack: {opp_total < my_total}")
    else:
        print("Could not parse opponent stats from page")
        # Try to find any stats-like patterns
        stat_matches = re.findall(r'(Strength|Attack|Defence|Agility|Stamina)[^<]*<[^>]*>(\d+)', content, re.IGNORECASE)
        if stat_matches:
            print(f"Found {len(stat_matches)} stat-like matches:")
            for match in stat_matches[:10]:
                print(f"  - {match[0]}: {match[1]}")
    
    print("\n=== Looking for action buttons ===")
    
    # Look for Attack button
    attack_buttons = await page.locator('button[name="Attack"], input[name="Attack"], button:has-text("Attack")').all()
    print(f"Attack buttons found: {len(attack_buttons)}")
    for i, btn in enumerate(attack_buttons[:5]):
        name = await btn.get_attribute('name')
        value = await btn.get_attribute('value')
        print(f"  Button {i}: name={name}, value={value}")
    
    # Look for New Opponent button
    new_opp_buttons = await page.locator('img[src*="neuer_gegner"], img[alt*="opponent"], button:has-text("New")').all()
    print(f"New Opponent buttons found: {len(new_opp_buttons)}")
    for i, btn in enumerate(new_opp_buttons[:5]):
        src = await btn.get_attribute('src')
        alt = await btn.get_attribute('alt')
        print(f"  Button {i}: src={src}, alt={alt}")
    
    print("\n\nKeeping browser open for 60 seconds for inspection...")
    await asyncio.sleep(60)
    
    await b.close()
    await p.stop()

asyncio.run(debug_attack())

