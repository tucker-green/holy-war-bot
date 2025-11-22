import asyncio
from playwright.async_api import async_playwright
import re

async def inspect():
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
    
    # Save HTML
    content = await page.content()
    with open('attack_form.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Saved attack_form.html")
    
    # Look for form inputs
    print("\n=== Looking for input fields ===")
    inputs = await page.locator('input').all()
    print(f"Found {len(inputs)} input fields:")
    for i, inp in enumerate(inputs[:20]):
        name = await inp.get_attribute('name')
        input_type = await inp.get_attribute('type')
        value = await inp.get_attribute('value')
        print(f"  Input {i}: type={input_type}, name={name}, value={value}")
    
    # Look for select dropdowns
    print("\n=== Looking for select dropdowns ===")
    selects = await page.locator('select').all()
    print(f"Found {len(selects)} select fields:")
    for i, sel in enumerate(selects):
        name = await sel.get_attribute('name')
        print(f"  Select {i}: name={name}")
        options = await sel.locator('option').all()
        for opt in options:
            value = await opt.get_attribute('value')
            text = await opt.text_content()
            print(f"    - value='{value}', text='{text}'")
    
    # Search for "level" in the HTML
    print("\n=== Searching for 'level' in HTML ===")
    level_matches = re.findall(r'<[^>]*(level|Level)[^>]*>', content)
    for match in level_matches[:10]:
        print(f"  {match}")
    
    print("\nKeeping browser open for 30 seconds...")
    await asyncio.sleep(30)
    
    await b.close()
    await p.stop()

asyncio.run(inspect())

