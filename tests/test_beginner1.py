import pytest


@pytest.mark.smoke
@pytest.mark.regression
def test_login(page):
    page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")

    page.fill("//input[@name='username']", "Admin")
    page.fill("//input[@name='password']", "admin123")

    page.screenshot(path="reports/screenshot/login.png")

    page.click("//button[@type='submit']")

    page.wait_for_timeout(5000)

    page.screenshot(path="reports/screenshot/home.png")

    assert "random" in page.url