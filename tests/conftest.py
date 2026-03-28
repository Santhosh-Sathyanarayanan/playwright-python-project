import allure
import base64
import os
import shutil
from datetime import datetime

import pytest
import pytest_html
from playwright.sync_api import sync_playwright


# =========================
# ✅ FIXTURE
# =========================
@pytest.fixture
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        context = browser.new_context(
            record_video_dir="reports/videos/"
        )

        page = context.new_page()

        # 🔥 Capture console logs
        logs = []
        page.on("console", lambda msg: logs.append(f"{msg.type}: {msg.text}"))
        page._logs = logs

        yield page

        # 🔥 Finalize video — context.close() MUST come first so the
        #    .webm file is fully written before we read it.
        context.close()

        video_path = None
        try:
            if page.video:
                video_path = page.video.path()
        except Exception:
            pass

        # Rename to a human-readable name and store on the page object
        # so the report hook can pick it up during teardown phase.
        if video_path and os.path.exists(video_path):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            test_name = os.environ.get("PYTEST_CURRENT_TEST", "test").split("::")[-1].split(" ")[0]
            new_name = f"{test_name}_{timestamp}.webm"
            new_path = os.path.join("reports/videos", new_name)
            try:
                shutil.move(video_path, new_path)
                video_path = new_path
            except Exception:
                pass

        page._video_path = video_path

        browser.close()


# =========================
# ✅ TEST REPORT HOOK
# =========================
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    page = item.funcargs.get("page", None)
    if not page:
        return

    # ── CALL phase: screenshot + logs on failure ──────────────────────
    if report.when == "call" and report.failed:
        report.extras = getattr(report, "extras", [])

        # 📸 Screenshot
        try:
            screenshot = page.screenshot()
            encoded = base64.b64encode(screenshot).decode("utf-8")
            report.extras.append(
                pytest_html.extras.image(encoded, mime_type="image/png")
            )
            allure.attach(
                screenshot,
                name="📸 Failure Screenshot",
                attachment_type=allure.attachment_type.PNG,
            )
        except Exception:
            pass

        # 🧾 Browser logs (collapsible)
        logs = getattr(page, "_logs", [])
        if logs:
            log_text = "<br>".join(logs)
            report.extras.append(
                pytest_html.extras.html(
                    f"""
                    <details>
                        <summary><b>🧾 Browser Logs (click to expand)</b></summary>
                        <div style="margin-top:10px;">{log_text}</div>
                    </details>
                    """
                )
            )

    # ── TEARDOWN phase: video is now fully written ─────────────────────
    # The fixture has already closed the context by this point, so
    # page._video_path is set and the .webm file is complete.
    if report.when == "teardown":
        video_path = getattr(page, "_video_path", None)

        if video_path and os.path.exists(video_path):
            try:
                with open(video_path, "rb") as vf:
                    video_data = vf.read()

                video_b64 = base64.b64encode(video_data).decode("utf-8")

                # 🎥 Embed in pytest-html report
                report.extras = getattr(report, "extras", [])
                report.extras.append(
                    pytest_html.extras.html(
                        f"""
                        <details>
                            <summary><b>🎥 Video for Reference (click to expand)</b></summary>
                            <div style="margin-top:10px;">
                                <video width="600" controls>
                                    <source src="data:video/webm;base64,{video_b64}"
                                            type="video/webm">
                                    Your browser does not support the video tag.
                                </video>
                            </div>
                        </details>
                        """
                    )
                )

                # 🎥 Attach to Allure report
                allure.attach(
                    video_data,
                    name="🎥 Test Recording",
                    attachment_type=allure.attachment_type.WEBM,
                )

            except Exception as e:
                report.extras = getattr(report, "extras", [])
                report.extras.append(
                    pytest_html.extras.html(
                        f"""
                        <details>
                            <summary><b>🎥 Video (could not embed)</b></summary>
                            <div style="margin-top:10px;">
                                <p>Error: {e}</p>
                                <p>File: {video_path}</p>
                            </div>
                        </details>
                        """
                    )
                )


# =========================
# ✅ REPORT TITLE
# =========================
def pytest_html_report_title(report):
    report.title = "Playwright Automation Report"


# =========================
# ✅ COLLAPSIBLE ENVIRONMENT
# pytest-html v4 handles this natively via #environment-header click.
# No custom hook needed.
# =========================