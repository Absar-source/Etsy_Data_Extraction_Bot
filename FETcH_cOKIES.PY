from playwright.sync_api import sync_playwright
import json

def save_cookies():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://www.etsy.com/search?q=handmade+mugs")

        input("Solve the CAPTCHA manually and press Enter here...")

        # Save cookies after solving CAPTCHA
        cookies = context.cookies()
        with open("etsy_cookies.json", "w") as f:
            json.dump(cookies, f)

        browser.close()

save_cookies()
