from playwright.sync_api import sync_playwright

def start_browser():
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False)
    # Set viewport size in the context
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    return browser, page

def stop_browser(browser):
    browser.close()
