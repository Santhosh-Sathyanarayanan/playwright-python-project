from playwright.sync_api import Page, expect

# Playwright gives page automatically!
def test_chromium(page: Page):
    page.goto("https://demoqa.com")
    page.wait_for_timeout(2000)
    print("Running on default browser!")