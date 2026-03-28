
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    # browser=p.firefox.launch(headless=False)
    # browser =p.webkit.launch(headless=False)

    # page = browser.new_page()

    context=browser.new_context()
    page=context.new_page()
    page.goto("https://demo.automationtesting.in/Register.html")
    radio_button = page.query_selector('//input[@value="FeMale"]')
    radio_button.click()

    if radio_button.is_checked():
        print("pass")
    else:
        print("fail")

    checkbox = page.query_selector('//input[@value="Cricket"]')
    checkbox.check()

    if checkbox.is_checked():
        print("pass")
    else:
        print("fail")
    page.wait_for_timeout(3000)