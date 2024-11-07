import sys
from pathlib import Path
project_root = Path(__file__).resolve().parents[2]  # Go two levels up in directory
sys.path.append(str(project_root))

from playwright.sync_api import Page
from utils.browser import start_browser, stop_browser
from utils.config import load_config
from utils.logger import setup_logging
# Load configuration
config = load_config()

# Set up logging
logger, error_logger = setup_logging()

# Retrieve necessary variables
username = config["username"]
password = config["password"]
base_url = config["base_url"]

# Ensure credentials are loaded correctly
if not username or not password or not base_url:
    raise ValueError("Missing LOGIN_USERNAME, LOGIN_PASSWORD, or BASE_URL in environment variables")


def archive_or_unarchive_first_client(page: Page):
    """
    Archives or unarchives the first client in the clients table by hovering over
    the client row and clicking the respective button based on whether the client is archived or not.

    :param page: Playwright Page object
    """
    try:
        # Wait for the clients table to load
        page.wait_for_selector('table tbody tr')
        # Locate the first client row in the clients table
        first_client_row = page.locator('table tbody tr').first

        # Hover over the first client row to reveal the action icons
        first_client_row.hover()

        # Locate the archive and unarchive buttons within the first client row
        archive_icon = first_client_row.locator('button[title="Archive"]')
        unarchive_icon = first_client_row.locator('button[title="Unarchive"]')

        # Archive the client if it's not already archived
        if archive_icon.is_visible():
            logger.info("Archiving first client")
            archive_icon.click()
            # Handle the confirmation popup (click "Yes")
            page.click('button:text("Yes")')
            logger.info("First client archived successfully.")

        # Unarchive the client if it's archived
        elif unarchive_icon.is_visible():
            logger.info("Unarchiving first client")
            unarchive_icon.click()
            # Handle the confirmation popup (click "Yes")
            page.click('button:text("Yes")')
            logger.info("First client unarchived successfully.")

        else:
            logger.error("No archive or unarchive button found for the first client.")

    except Exception as e:
        logger.error(f"An error occurred while trying to archive/unarchive the first client. Error: {e}", exc_info=True)


def run():
    try:
        # Start browser and get page
        browser, page = start_browser()

        logger.info("Running test: Archive or Unarchive First Client")

        # Navigate to the login page
        page.goto(f"{base_url}/sign-in")

        # Perform login
        page.fill('input[name="email"]', username)
        page.fill('input[name="password"]', password)
        page.click('button[type="submit"]')

        # Check if login was successful by waiting for the URL to change
        try:
            # Wait for the client page URL
            page.wait_for_url(f"{base_url}/apps/clients/", timeout=5000)
            logger.info("Login successful")

        except Exception:
            # Handle the login failure case by checking for error messages or remaining on the login page
            logger.error("Login failed - Invalid credentials")

            stop_browser(browser)
            return  # Exit the function since login failed

        # Archive or Unarchive the first client
        archive_or_unarchive_first_client(page)

        # Close the browser
        stop_browser(browser)
        logger.info("Test completed successfully")

    except Exception as e:
        error_logger.error(f"Error occurred during the test: {str(e)}", exc_info=True)
        logger.info("Test failed")
        stop_browser(browser)


if __name__ == "__main__":
    run()