from playwright.sync_api import sync_playwright

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://google.com")
    print("Successfully opened Google")
    print("Title",page.title())
    page.wait_for_timeout(3000)
    browser.close()