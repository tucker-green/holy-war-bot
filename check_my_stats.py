import asyncio
from playwright.async_api import async_playwright
import re

async def check_stats():
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
    
    print("Going to attributes/stats page...")
    await page.goto('https://www.holy-war.net/char/attributes/?w=17IN')
    await asyncio.sleep(3)
    
    content = await page.content()
    
    # Save the page
    with open('my_stats_page.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Saved my_stats_page.html")
    
    # Try different patterns to find stats
    print("\n=== Looking for stat patterns ===")
    
    # Pattern 1: <td>Strength</td><td>XX</td>
    matches = re.findall(r'<td[^>]*>(Strength|Attack|Defence|Agility|Stamina)</td>\s*<td[^>]*>(\d+)</td>', content, re.IGNORECASE)
    print(f"Pattern 1 matches: {len(matches)}")
    for match in matches:
        print(f"  - {match[0]}: {match[1]}")
    
    # Pattern 2: Look for the actual stat display table
    print("\n=== Searching for stat table structure ===")
    stat_sections = re.findall(r'<tr[^>]*>.*?(Strength|Attack|Defence|Agility|Stamina).*?</tr>', content, re.IGNORECASE | re.DOTALL)
    print(f"Found {len(stat_sections)} stat rows")
    for i, section in enumerate(stat_sections[:5]):
        print(f"\nRow {i}:")
        print(section[:300])
    
    # Pattern 3: Just find all numbers near stat names
    print("\n=== Numbers near stat names ===")
    for stat in ['Strength', 'Attack', 'Defence', 'Agility', 'Stamina']:
        # Find the stat name and grab 200 chars after it
        match = re.search(rf'{stat}(.{{0,200}})', content, re.IGNORECASE | re.DOTALL)
        if match:
            context = match.group(1)
            # Find numbers in this context
            numbers = re.findall(r'>(\d+)<', context)
            print(f"{stat}: {numbers[:5]}")
    
    print("\n\nKeeping browser open for 30 seconds...")
    await asyncio.sleep(30)
    
    await b.close()
    await p.stop()

asyncio.run(check_stats())

