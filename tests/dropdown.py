from playwright.sync_api import sync_playwright,Page

def dropdown(p) -> str:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://demo.automationtesting.in/Register.html")
    # Dropdown_Select=page.query_selector("//*[@id='Skills']")
    page.select_option("//*[@id='Skills']", value='AutoCAD')
    page.wait_for_timeout(10000)
    sel="Welcome"
    page.close()

    browser.close()
    return sel
with sync_playwright() as p:
    result=dropdown(p)
    print("Message:",result)
