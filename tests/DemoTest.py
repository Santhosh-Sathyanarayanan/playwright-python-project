from playwright.sync_api import Page, expect


def test_open_demoqa(page: Page):

    # Step 1 — Open demoqa website
    page.goto("https://demoqa.com/text-box")

    # Step 2 — Verify page title
    expect(page).to_have_title("demosite")
    print("Title Verified")

    # Step 3 — Verify heading visible
    heading = page.get_by_role("heading",name="Text Box")
    expect(heading).to_be_visible()
    print("Heading Visible")

    # Step 4 — Fill Full Name
    page.get_by_placeholder("Full Name").fill("Santhosh Shanbouge")
    page.wait_for_timeout(3000)

    # Step 5 — Fill Email
    page.get_by_placeholder("name@example.com").fill("santhosh@gmail.com")
    page.wait_for_timeout(3000)

    # Step 6 — Click Submit
    page.get_by_role("button",name="Submit").click()
    page.wait_for_timeout(3000)

    print("✅Playwright Test Passed!")