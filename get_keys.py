from playwright.sync_api import sync_playwright
import re
import time

def extract_geetest_params():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = browser.new_page()

        # Enable request interception to sniff geetest requests
        geetest_data = {}

        def handle_request(request):
            url = request.url
            if "geetest" in url and ("gt=" in url or "challenge=" in url):
                print(f"[Found] {url}")
                match_gt = re.search(r"gt=([a-zA-Z0-9]+)", url)
                match_challenge = re.search(r"challenge=([a-zA-Z0-9-_]+)", url)
                if match_gt:
                    geetest_data["gt"] = match_gt.group(1)
                if match_challenge:
                    geetest_data["challenge"] = match_challenge.group(1)

        context.on("request", handle_request)

        # Visit the page
        # page.goto("https://www.etsy.com/search?q=handmade+mugs")
        page.goto("https://www.etsy.com/search?q=handmade+mugs&ref=search_bar")


        print("Waiting for CAPTCHA to load... please solve it manually if needed.")
        time.sleep(30)  # Give time for captcha to load or solve manually

        browser.close()
        return geetest_data

# Run it
params = extract_geetest_params()
print("\nExtracted Geetest Params:")
print(params)
