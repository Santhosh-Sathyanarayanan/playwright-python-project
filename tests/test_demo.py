import pytest
from playwright.sync_api import Page, expect


# Test 1
@pytest.mark.smoke
@pytest.mark.regression
def test_verify_title(page: Page):
    page.goto("https://demoqa.com/text-box")
    page.wait_for_timeout(2000)
    expect(page).to_have_title("demosite")
    print("Title verified!")


# Test 2
@pytest.mark.regression
def test_fill_form(page: Page):
    page.goto("https://demoqa.com/text-box")
    page.wait_for_timeout(2000)
    page.get_by_placeholder("Full Name").fill("Santhosh")
    page.get_by_placeholder("name@example.com").fill("s@gmail.com")
    print("Form filled!")


# Test 3
def test_submit_form(page: Page):
    page.goto("https://demoqa.com/text-box")
    page.wait_for_timeout(2000)
    page.get_by_placeholder("Full Name").fill("Santhosh")
    page.get_by_role("button", name="Submit").click()
    print("Form submitted!")