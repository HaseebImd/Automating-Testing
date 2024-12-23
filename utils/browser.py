from playwright.sync_api import sync_playwright


def start_browser():
    playwright = sync_playwright().start()

    # Launch the browser
    browser = playwright.chromium.launch(
        headless=False  # Set to True in production to reduce resource usage
    )

    # Create a new context with stealth-like features
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",  # Updated to a recent Chrome version
        locale="en-US",
        timezone_id="America/New_York",
        color_scheme="light",
        permissions=["geolocation"],  # Allows geolocation to simulate real users
        ignore_https_errors=True,  # Ignore SSL errors for untrusted certificates
    )

    # Add stealth-like scripts
    context.add_init_script(
        """
        // Hide WebDriver property to make automation harder to detect
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });

        // Mock plugins to appear like a real browser
        Object.defineProperty(navigator, 'plugins', {
            get: () => [1, 2, 3],
        });

        // Mock languages to match user agent
        Object.defineProperty(navigator, 'languages', {
            get: () => ['en-US', 'en'],
        });

        // Mock other navigator properties to match a real browser
        Object.defineProperty(navigator, 'hardwareConcurrency', {
            get: () => 8,  // Set the number of CPU cores
        });

        Object.defineProperty(navigator, 'deviceMemory', {
            get: () => 8,  // Simulate device memory in GB
        });

        Object.defineProperty(navigator, 'platform', {
            get: () => 'Win32',  // Simulate a Windows platform
        });
        """
    )

    # Add headers for realistic browser behavior
    page = context.new_page()
    page.set_extra_http_headers(
        {
            "Accept-Language": "en-US,en;q=0.9",
            "DNT": "1",  # Do Not Track header
            "Cache-Control": "no-cache",  # Prevent cached responses
            "Upgrade-Insecure-Requests": "1",  # Mimic browser requests
        }
    )

    # Return the browser, context, and page
    return browser, context, page


def stop_browser(browser):
    # Gracefully close the browser
    browser.close()
