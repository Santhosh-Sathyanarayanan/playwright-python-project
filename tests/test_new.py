import playwright.sync_api
from playwright.sync_api import sync_playwright

def dropdown(p) -> None:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://demo.automationtesting.in/Register.html")
    # Dropdown_Select=page.query_selector("//*[@id='Skills']")
    page.select_option("//*[@id='Skills']", value='AutoCAD')
    page.wait_for_timeout(10000)
    sel="Welcome"
    page.close()
    browser.close()
with sync_playwright() as p:
    dropdown(p)
