import json
from playwright.sync_api import sync_playwright


def start_browser():
    playwright = sync_playwright().start()

    # Launch the browser
    browser = playwright.chromium.launch(headless=False)

    # Create a new context with stealth-like options
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        locale="en-US",
        timezone_id="America/New_York",
        color_scheme="light",
    )

    # Add stealth-like script
    context.add_init_script(
        """
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });
    """
    )

    page = context.new_page()

    # Return the browser, context, and page
    return browser, context, page


def stop_browser(browser):
    browser.close()
